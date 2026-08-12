#!/usr/bin/env python3
"""Gate di provenienza per la baseline normativa.

Fa fallire la build quando una regola non e' riconducibile a una fonte pubblica
verificabile, o quando la baseline e' invecchiata oltre la soglia ammessa.

Uso:
    python check_sources.py --sources sources.yml --rules rules/
    python check_sources.py --sources sources.yml --rules rules/ --check-urls

Il controllo di raggiungibilita' degli URL e' opzionale e disattivato per default,
cosi' che la CI resti deterministica anche senza rete.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("Dipendenza mancante: pip install pyyaml")

REQUIRED_SOURCE_FIELDS = ("id", "document", "url", "verification", "retrieved")
VERIFICATION_LEVELS = ("verified", "cited", "unverified")
MATURITY_LEVELS = ("stable", "beta", "stub", "reference_only")
STALE_AFTER_DAYS = 180


class Report:
    """Accumula errori e avvisi mantenendo l'ordine di rilevazione."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def emit(self) -> int:
        for message in self.warnings:
            print(f"warning: {message}")
        for message in self.errors:
            print(f"error: {message}")
        print(
            f"\n{len(self.errors)} errori, {len(self.warnings)} avvisi.",
            file=sys.stderr,
        )
        return 1 if self.errors else 0


def parse_date(value: object, context: str, report: Report) -> dt.date | None:
    if not isinstance(value, (str, dt.date)):
        report.error(f"{context}: data assente o di tipo non valido")
        return None
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        report.error(f"{context}: data '{value}' non in formato ISO YYYY-MM-DD")
        return None


def load_sources(path: Path, report: Report) -> tuple[dict, dict]:
    """Restituisce (indice fonti per id, indice moduli per nome)."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    sources: dict[str, dict] = {}
    modules: dict[str, str] = {}
    today = dt.date.today()

    for domain in data.get("domains", []):
        domain_id = domain.get("id", "<senza id>")
        maturity = domain.get("maturity")
        if maturity not in MATURITY_LEVELS:
            report.error(f"dominio {domain_id}: maturity '{maturity}' non ammessa")
        if domain.get("module"):
            modules[domain["module"]] = maturity

        for source in domain.get("sources", []):
            source_id = source.get("id")
            context = f"fonte {source_id or '<senza id>'} (dominio {domain_id})"

            for field in REQUIRED_SOURCE_FIELDS:
                if not source.get(field):
                    report.error(f"{context}: campo obbligatorio '{field}' mancante")

            if source.get("verification") not in VERIFICATION_LEVELS:
                report.error(
                    f"{context}: verification '{source.get('verification')}' non ammessa"
                )

            url = source.get("url", "")
            if url and not url.startswith("https://"):
                report.error(f"{context}: url non https ({url})")

            retrieved = parse_date(source.get("retrieved"), context, report)
            if retrieved and (today - retrieved).days > STALE_AFTER_DAYS:
                report.error(
                    f"{context}: verificata l'ultima volta il {retrieved}, "
                    f"oltre la soglia di {STALE_AFTER_DAYS} giorni"
                )

            if "review_by" in source:
                review_by = parse_date(source["review_by"], context, report)
                if review_by and review_by < today:
                    report.error(
                        f"{context}: scadenza di revisione {review_by} superata"
                    )

            if source_id:
                if source_id in sources:
                    report.error(f"{context}: id duplicato")
                sources[source_id] = source

    return sources, modules


def check_rules(
    rules_dir: Path, sources: dict, modules: dict, report: Report
) -> int:
    """Verifica che ogni regola sia riconducibile a una fonte ammissibile."""
    count = 0
    for rules_file in sorted(rules_dir.rglob("*.y*ml")):
        document = yaml.safe_load(rules_file.read_text(encoding="utf-8")) or {}
        module = document.get("module")
        maturity = modules.get(module)

        if module is None:
            report.error(f"{rules_file}: campo 'module' mancante")
        elif maturity is None:
            report.error(f"{rules_file}: modulo '{module}' assente da sources.yml")

        for rule in document.get("rules", []):
            count += 1
            rule_id = rule.get("id", "<senza id>")
            context = f"regola {rule_id} ({rules_file.name})"

            source_id = rule.get("source")
            if not source_id:
                report.error(f"{context}: campo 'source' mancante")
                continue

            source = sources.get(source_id)
            if source is None:
                report.error(f"{context}: fonte '{source_id}' inesistente")
                continue

            verification = source.get("verification")
            if verification == "unverified":
                report.error(
                    f"{context}: poggia su una fonte 'unverified' ({source_id})"
                )
            elif verification == "cited" and maturity == "stable":
                report.error(
                    f"{context}: modulo 'stable' non puo' poggiare su fonte "
                    f"'cited' ({source_id})"
                )

            if maturity == "stub":
                report.error(
                    f"{context}: un modulo 'stub' non deve contenere regole attive"
                )

    return count


def check_urls(sources: dict, report: Report) -> None:
    """Verifica opzionale di raggiungibilita'. Richiede rete.

    Molti portali istituzionali sono protetti da un WAF che rifiuta le richieste HEAD
    e gli User-Agent di libreria, rispondendo 403 anche quando la pagina e' pubblica e
    perfettamente raggiungibile da un browser. Trattare quel 403 come errore
    produrrebbe un falso negativo sistematico sulle fonti piu' importanti del registro.

    Di conseguenza:
      - la richiesta usa GET con Range minimo e uno User-Agent realistico
      - solo 404 e 410 sono errori: indicano una fonte effettivamente sparita
      - 401, 403, 405, 406, 429 e i 5xx sono avvisi: indicano un accesso automatico
        negato o un disservizio temporaneo, non un collegamento morto
      - una fonte puo' dichiarare `url_check: skip` con motivazione, per i portali che
        bloccano stabilmente le verifiche automatiche
    """
    import urllib.error
    import urllib.request

    dead = {404, 410}
    blocked = {401, 403, 405, 406, 429}

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9",
        "Range": "bytes=0-0",
    }

    checked = skipped = 0

    for source_id, source in sources.items():
        url = source.get("url")
        if not url:
            continue

        if source.get("url_check") == "skip":
            skipped += 1
            reason = source.get("url_check_reason", "motivazione non indicata")
            report.warn(f"fonte {source_id}: verifica url saltata ({reason})")
            continue

        checked += 1
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                status = response.status
                if status in dead:
                    report.error(f"fonte {source_id}: url risponde {status}, collegamento morto")
                elif status >= 400:
                    report.warn(f"fonte {source_id}: url risponde {status}")
        except urllib.error.HTTPError as exc:
            if exc.code in dead:
                report.error(f"fonte {source_id}: url risponde {exc.code}, collegamento morto")
            elif exc.code in blocked:
                report.warn(
                    f"fonte {source_id}: url risponde {exc.code}, accesso automatico "
                    f"negato dal portale. Verificare a mano oppure impostare url_check: skip"
                )
            else:
                report.warn(f"fonte {source_id}: url risponde {exc.code}")
        except Exception as exc:
            report.warn(f"fonte {source_id}: url non raggiungibile ({type(exc).__name__}: {exc})")

    print(f"URL verificati: {checked}" + (f", saltati: {skipped}" if skipped else ""))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, default=Path("sources.yml"))
    parser.add_argument("--rules", type=Path, default=None)
    parser.add_argument("--check-urls", action="store_true")
    args = parser.parse_args()

    report = Report()

    if not args.sources.exists():
        sys.exit(f"Registro delle fonti non trovato: {args.sources}")

    sources, modules = load_sources(args.sources, report)
    print(f"Fonti registrate: {len(sources)}")

    if args.rules and args.rules.exists():
        total = check_rules(args.rules, sources, modules, report)
        print(f"Regole controllate: {total}")
    elif args.rules:
        report.warn(f"directory delle regole assente: {args.rules}")

    if args.check_urls:
        check_urls(sources, report)

    return report.emit()


if __name__ == "__main__":
    raise SystemExit(main())

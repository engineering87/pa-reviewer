"""Comportamento del gate di provenienza.

Il gate e' l'unico meccanismo che trasforma la politica del progetto in un vincolo
reale. Un gate che non blocca e' peggio di nessun gate, perche' produce fiducia
ingiustificata: da qui l'insistenza sui casi negativi.
"""

from __future__ import annotations

import datetime as dt

import pytest
import yaml


def scrivi(tmp_path, registro, regole=None):
    percorso = tmp_path / "sources.yml"
    percorso.write_text(yaml.safe_dump(registro, allow_unicode=True), encoding="utf-8")
    cartella = None
    if regole is not None:
        cartella = tmp_path / "rules"
        cartella.mkdir()
        (cartella / "prova.yml").write_text(
            yaml.safe_dump(regole, allow_unicode=True), encoding="utf-8"
        )
    return percorso, cartella


def registro_minimo(**override):
    fonte = {
        "id": "TST-001",
        "document": "documento di prova",
        "url": "https://example.org/documento",
        "verification": "verified",
        "retrieved": str(dt.date.today()),
    }
    fonte.update(override.pop("fonte", {}))
    dominio = {
        "id": "TST",
        "name": "Prova",
        "module": "prova",
        "maturity": "beta",
        "sources": [fonte],
    }
    dominio.update(override.pop("dominio", {}))
    return {
        "schema_version": "0.1.0",
        "baseline_date": str(dt.date.today()),
        "domains": [dominio],
        "out_of_scope": [{"id": "OOS", "reason": "motivo"}],
    }


def esegui(gate, sorgenti, regole=None):
    report = gate.Report()
    fonti, moduli = gate.load_sources(sorgenti, report)
    if regole is not None:
        gate.check_rules(regole, fonti, moduli, report)
    return report


# --- casi positivi -----------------------------------------------------------


def test_registro_valido_non_produce_errori(gate, tmp_path):
    sorgenti, _ = scrivi(tmp_path, registro_minimo())
    assert not esegui(gate, sorgenti).errors


def test_regola_ben_formata_non_produce_errori(gate, tmp_path):
    regole = {"module": "prova", "rules": [{"id": "R1", "source": "TST-001"}]}
    sorgenti, cartella = scrivi(tmp_path, registro_minimo(), regole)
    assert not esegui(gate, sorgenti, cartella).errors


def test_il_registro_reale_del_progetto_passa(gate, root):
    report = esegui(gate, root / "sources.yml", root / "rules")
    assert not report.errors, report.errors


# --- casi negativi -----------------------------------------------------------


def test_blocca_regola_senza_fonte(gate, tmp_path):
    regole = {"module": "prova", "rules": [{"id": "R1"}]}
    sorgenti, cartella = scrivi(tmp_path, registro_minimo(), regole)
    errori = esegui(gate, sorgenti, cartella).errors
    assert any("source" in e for e in errori)


def test_blocca_fonte_inesistente(gate, tmp_path):
    regole = {"module": "prova", "rules": [{"id": "R1", "source": "NON-ESISTE"}]}
    sorgenti, cartella = scrivi(tmp_path, registro_minimo(), regole)
    assert any("inesistente" in e for e in esegui(gate, sorgenti, cartella).errors)


def test_blocca_regola_in_modulo_stub(gate, tmp_path):
    registro = registro_minimo(dominio={"maturity": "stub"})
    regole = {"module": "prova", "rules": [{"id": "R1", "source": "TST-001"}]}
    sorgenti, cartella = scrivi(tmp_path, registro, regole)
    assert any("stub" in e for e in esegui(gate, sorgenti, cartella).errors)


def test_blocca_fonte_citata_in_modulo_stabile(gate, tmp_path):
    registro = registro_minimo(
        dominio={"maturity": "stable"}, fonte={"verification": "cited"}
    )
    regole = {"module": "prova", "rules": [{"id": "R1", "source": "TST-001"}]}
    sorgenti, cartella = scrivi(tmp_path, registro, regole)
    assert any("cited" in e for e in esegui(gate, sorgenti, cartella).errors)


def test_blocca_fonte_non_verificata(gate, tmp_path):
    registro = registro_minimo(fonte={"verification": "unverified"})
    regole = {"module": "prova", "rules": [{"id": "R1", "source": "TST-001"}]}
    sorgenti, cartella = scrivi(tmp_path, registro, regole)
    assert any("unverified" in e for e in esegui(gate, sorgenti, cartella).errors)


def test_blocca_url_non_https(gate, tmp_path):
    registro = registro_minimo(fonte={"url": "http://example.org/documento"})
    sorgenti, _ = scrivi(tmp_path, registro)
    assert any("https" in e for e in esegui(gate, sorgenti).errors)


def test_blocca_campo_obbligatorio_mancante(gate, tmp_path):
    registro = registro_minimo()
    del registro["domains"][0]["sources"][0]["document"]
    sorgenti, _ = scrivi(tmp_path, registro)
    assert any("document" in e for e in esegui(gate, sorgenti).errors)


def test_blocca_baseline_invecchiata(gate, tmp_path):
    vecchia = dt.date.today() - dt.timedelta(days=gate.STALE_AFTER_DAYS + 1)
    registro = registro_minimo(fonte={"retrieved": str(vecchia)})
    sorgenti, _ = scrivi(tmp_path, registro)
    assert any("soglia" in e for e in esegui(gate, sorgenti).errors)


def test_blocca_scadenza_di_revisione_superata(gate, tmp_path):
    ieri = dt.date.today() - dt.timedelta(days=1)
    registro = registro_minimo(fonte={"review_by": str(ieri)})
    sorgenti, _ = scrivi(tmp_path, registro)
    assert any("revisione" in e for e in esegui(gate, sorgenti).errors)


def test_blocca_identificativi_duplicati(gate, tmp_path):
    registro = registro_minimo()
    registro["domains"][0]["sources"].append(
        dict(registro["domains"][0]["sources"][0])
    )
    sorgenti, _ = scrivi(tmp_path, registro)
    assert any("duplicato" in e for e in esegui(gate, sorgenti).errors)


def test_blocca_maturita_non_ammessa(gate, tmp_path):
    registro = registro_minimo(dominio={"maturity": "quasi-pronto"})
    sorgenti, _ = scrivi(tmp_path, registro)
    assert any("maturity" in e for e in esegui(gate, sorgenti).errors)


def test_blocca_data_non_iso(gate, tmp_path):
    registro = registro_minimo(fonte={"retrieved": "12 agosto 2026"})
    sorgenti, _ = scrivi(tmp_path, registro)
    assert any("ISO" in e for e in esegui(gate, sorgenti).errors)


# --- classificazione delle risposte HTTP -------------------------------------


def test_403_e_un_avviso_non_un_errore(gate, tmp_path, monkeypatch):
    """I portali istituzionali rispondono 403 alle verifiche automatiche pur
    servendo regolarmente la pagina. Trattarlo come errore produrrebbe un falso
    negativo sistematico sulle fonti piu' importanti del registro."""
    import urllib.error

    def nega(*args, **kwargs):
        raise urllib.error.HTTPError("https://example.org", 403, "Forbidden", {}, None)

    monkeypatch.setattr("urllib.request.urlopen", nega)
    report = gate.Report()
    gate.check_urls({"X": {"url": "https://example.org"}}, report)
    assert not report.errors
    assert report.warnings


def test_404_e_un_errore(gate, monkeypatch):
    import urllib.error

    def sparita(*args, **kwargs):
        raise urllib.error.HTTPError("https://example.org", 404, "Not Found", {}, None)

    monkeypatch.setattr("urllib.request.urlopen", sparita)
    report = gate.Report()
    gate.check_urls({"X": {"url": "https://example.org"}}, report)
    assert any("morto" in e for e in report.errors)


def test_url_check_skip_produce_solo_un_avviso(gate):
    report = gate.Report()
    gate.check_urls(
        {"X": {"url": "https://example.org", "url_check": "skip",
               "url_check_reason": "portale che blocca le verifiche"}},
        report,
    )
    assert not report.errors
    assert any("saltata" in w for w in report.warnings)


@pytest.mark.parametrize("codice", [401, 405, 429, 500, 503])
def test_altri_codici_sono_avvisi(gate, monkeypatch, codice):
    import urllib.error

    def risposta(*args, **kwargs):
        raise urllib.error.HTTPError("https://example.org", codice, "x", {}, None)

    monkeypatch.setattr("urllib.request.urlopen", risposta)
    report = gate.Report()
    gate.check_urls({"X": {"url": "https://example.org"}}, report)
    assert not report.errors


# --- rami d'errore e interfaccia da riga di comando --------------------------


def test_blocca_livello_di_verifica_non_ammesso(gate, tmp_path):
    registro = registro_minimo(fonte={"verification": "quasi-verificata"})
    sorgenti, _ = scrivi(tmp_path, registro)
    assert any("verification" in e for e in esegui(gate, sorgenti).errors)


def test_blocca_file_di_regole_senza_modulo(gate, tmp_path):
    regole = {"rules": [{"id": "R1", "source": "TST-001"}]}
    sorgenti, cartella = scrivi(tmp_path, registro_minimo(), regole)
    assert any("module" in e for e in esegui(gate, sorgenti, cartella).errors)


def test_blocca_modulo_assente_dal_registro(gate, tmp_path):
    regole = {"module": "inventato", "rules": [{"id": "R1", "source": "TST-001"}]}
    sorgenti, cartella = scrivi(tmp_path, registro_minimo(), regole)
    assert any("assente da sources.yml" in e for e in esegui(gate, sorgenti, cartella).errors)


def test_blocca_data_di_tipo_non_valido(gate, tmp_path):
    registro = registro_minimo(fonte={"retrieved": 20260812})
    sorgenti, _ = scrivi(tmp_path, registro)
    assert any("tipo non valido" in e for e in esegui(gate, sorgenti).errors)


def test_accetta_date_gia_convertite_dal_parser_yaml(gate, tmp_path):
    """PyYAML converte le date non quotate in oggetti date: il gate deve
    accettarle senza lamentarsi del tipo."""
    percorso = tmp_path / "sources.yml"
    percorso.write_text(
        "schema_version: '0.1.0'\n"
        f"baseline_date: {dt.date.today()}\n"
        "domains:\n"
        "  - id: TST\n"
        "    name: Prova\n"
        "    module: prova\n"
        "    maturity: beta\n"
        "    sources:\n"
        "      - id: TST-001\n"
        "        document: prova\n"
        "        url: https://example.org/x\n"
        "        verification: verified\n"
        f"        retrieved: {dt.date.today()}\n",
        encoding="utf-8",
    )
    assert not esegui(gate, percorso).errors


def test_il_report_restituisce_zero_quando_non_ci_sono_errori(gate):
    report = gate.Report()
    report.warn("solo un avviso")
    assert report.emit() == 0


def test_il_report_restituisce_uno_in_presenza_di_errori(gate):
    report = gate.Report()
    report.error("un errore")
    assert report.emit() == 1


def test_riga_di_comando_esce_con_zero_sul_registro_reale(gate, root, monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["check_sources.py", "--sources", str(root / "sources.yml"),
         "--rules", str(root / "rules")],
    )
    assert gate.main() == 0


def test_riga_di_comando_avvisa_se_la_cartella_regole_non_esiste(gate, root, monkeypatch, tmp_path):
    monkeypatch.setattr(
        "sys.argv",
        ["check_sources.py", "--sources", str(root / "sources.yml"),
         "--rules", str(tmp_path / "inesistente")],
    )
    assert gate.main() == 0


def test_riga_di_comando_termina_se_il_registro_non_esiste(gate, monkeypatch, tmp_path):
    monkeypatch.setattr(
        "sys.argv", ["check_sources.py", "--sources", str(tmp_path / "assente.yml")]
    )
    with pytest.raises(SystemExit):
        gate.main()

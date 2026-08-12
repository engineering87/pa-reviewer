"""Coerenza fra documentazione e contenuto reale.

Un progetto che dichiara numeri sbagliati nel proprio README perde credibilita' prima
ancora che qualcuno ne legga una regola. Questi test rendono impossibile che la
documentazione e il contenuto divergano in silenzio.
"""

from __future__ import annotations

import re

import pytest

CAMPI_FRONTMATTER_AMMESSI = {
    "allowed-tools",
    "compatibility",
    "description",
    "license",
    "metadata",
    "name",
}


@pytest.fixture(scope="module")
def readme(root) -> str:
    return (root / "README.md").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def skill(root) -> str:
    return (root / "SKILL.md").read_text(encoding="utf-8")


def test_il_badge_dichiara_il_numero_reale_di_fonti(readme, sources):
    dichiarato = int(re.search(r"fonti-(\d+)", readme).group(1))
    assert dichiarato == len(sources)


def test_il_readme_dichiara_il_numero_reale_di_regole(readme, rules):
    dichiarato = int(re.search(r"(\d+) regole", readme).group(1))
    assert dichiarato == len(rules)


def test_la_tabella_dei_moduli_riflette_il_registro(readme, modules):
    for modulo, maturita in modules.items():
        riga = re.search(rf"\| `{modulo}` \| \*{{0,2}}(\w+)", readme)
        assert riga, f"il README non elenca il modulo {modulo}"
        assert riga.group(1) == maturita, (
            f"{modulo}: README dice '{riga.group(1)}', registro dice '{maturita}'"
        )


def test_i_marcatori_di_severita_sono_documentati_ovunque(readme, skill):
    """L'esempio nel README non puo' usare simboli che nessun documento definisce,
    e la skill deve sapere quali emettere."""
    for marcatore in ("[!]", "[·]", "[~]"):
        assert marcatore in readme, f"{marcatore} assente dal README"
        assert marcatore in skill, f"{marcatore} assente da SKILL.md"


def test_il_frontmatter_usa_solo_campi_della_specifica(skill):
    """Una chiave non prevista fa fallire il caricamento della skill."""
    frontmatter = re.match(r"---\n(.*?)\n---", skill, re.S).group(1)
    campi = {
        riga.split(":")[0]
        for riga in frontmatter.split("\n")
        if riga and not riga.startswith((" ", "\t", "#"))
    }
    assert campi <= CAMPI_FRONTMATTER_AMMESSI, campi - CAMPI_FRONTMATTER_AMMESSI


def test_il_frontmatter_dichiara_nome_e_descrizione(skill):
    frontmatter = re.match(r"---\n(.*?)\n---", skill, re.S).group(1)
    assert re.search(r"^name:\s*\S+", frontmatter, re.M)
    assert re.search(r"^description:", frontmatter, re.M)


def test_il_nome_della_skill_coincide_con_la_cartella(skill, root):
    nome = re.search(r"^name:\s*(\S+)", skill, re.M).group(1)
    assert nome == root.name


def test_tutti_i_collegamenti_interni_risolvono(root):
    mancanti = []
    for documento in list(root.glob("*.md")) + list(root.glob("*/*.md")):
        testo = documento.read_text(encoding="utf-8")
        riferimenti = re.findall(
            r"\]\((\./[^)]+|[A-Za-z0-9_./-]+\.(?:md|yml|json|svg|py))\)", testo
        )
        riferimenti += re.findall(r'src="([^"]+)"', testo)
        for riferimento in riferimenti:
            bersaglio = riferimento.split("#")[0]
            if bersaglio.startswith("http"):
                continue
            if not (documento.parent / bersaglio).resolve().exists():
                mancanti.append(f"{documento.name} -> {bersaglio}")
    assert not mancanti, mancanti


def test_il_markup_del_readme_e_bilanciato(readme):
    assert readme.count("```") % 2 == 0, "blocchi di codice non chiusi"
    assert readme.count("<details>") == readme.count("</details>")
    assert readme.count("<div") == readme.count("</div>")


def test_la_documentazione_non_promette_giudizi_di_conformita(readme, skill):
    for documento, nome in ((readme, "README.md"), (skill, "SKILL.md")):
        assert "non emette" in documento.lower() or "mai un giudizio" in documento.lower(), (
            f"{nome} non dichiara il limite sui giudizi di conformita'"
        )


def test_la_licenza_e_completa(root):
    """Il file di licenza deve contenere il testo, non un segnaposto."""
    licenza = (root / "LICENSE").read_text(encoding="utf-8")
    assert "EUROPEAN UNION PUBLIC LICENCE" in licenza
    assert len(licenza) > 10_000, "il testo della licenza sembra troncato"
    assert "DA COMPLETARE" not in licenza


def test_ogni_modulo_ha_condizioni_di_promozione_dichiarate(modules, root):
    for modulo, maturita in modules.items():
        if maturita != "stub":
            continue
        testo = (root / "references" / f"{modulo}.md").read_text(encoding="utf-8")
        assert "Condizioni per passare" in testo, modulo


def test_gli_script_di_delega_sono_eseguibili(root):
    import os

    for script in (root / "scripts").glob("*.sh"):
        assert os.access(script, os.X_OK), f"{script.name} non eseguibile"


def test_gli_script_di_delega_dichiarano_la_fonte_dello_strumento(root):
    """Uno script che invoca uno strumento ufficiale deve dire quale, altrimenti la
    delega non e' verificabile da chi legge."""
    for script in (root / "scripts").glob("run_*.sh"):
        testo = script.read_text(encoding="utf-8")
        assert "Riferimento:" in testo or "Delega" in testo, script.name

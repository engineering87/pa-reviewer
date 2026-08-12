"""Invarianti delle regole.

Una regola mal formata produce rumore, e il rumore e' il modo piu' rapido per far
disinstallare uno strumento di revisione. Questi test fanno rispettare le condizioni
che `CONTRIBUTING.md` dichiara obbligatorie.
"""

from __future__ import annotations

import re

import yaml

from conftest import CHECK, EVIDENCE, SEVERITY


def test_ogni_file_di_regole_dichiara_un_modulo_esistente(rule_files, modules):
    for path in rule_files:
        documento = yaml.safe_load(path.read_text(encoding="utf-8"))
        modulo = documento.get("module")
        assert modulo, f"{path.name}: manca il campo module"
        assert modulo in modules, f"{path.name}: modulo '{modulo}' assente dal registro"


def test_i_moduli_stub_non_hanno_regole(rule_files, modules):
    """Uno stub dichiara il perimetro e tace. Se emettesse rilievi, la promessa
    fatta nel README sarebbe falsa."""
    for path in rule_files:
        documento = yaml.safe_load(path.read_text(encoding="utf-8"))
        if modules.get(documento.get("module")) == "stub":
            assert not documento.get("rules"), (
                f"{path.name}: modulo stub con regole attive"
            )


def test_identificativi_delle_regole_unici(rules):
    identificativi = [r["id"] for _, r in rules]
    duplicati = {i for i in identificativi if identificativi.count(i) > 1}
    assert not duplicati, f"regole duplicate: {duplicati}"


def test_ogni_regola_ha_i_campi_obbligatori(rules):
    obbligatori = ("id", "title", "source", "check", "severity", "evidence",
                   "when", "guard", "message")
    for _, regola in rules:
        for campo in obbligatori:
            assert regola.get(campo), f"{regola.get('id')}: manca {campo}"


def test_ogni_regola_riferisce_una_fonte_esistente(rules, sources):
    for _, regola in rules:
        assert regola["source"] in sources, (
            f"{regola['id']}: fonte '{regola['source']}' inesistente"
        )


def test_nessuna_regola_poggia_su_fonte_non_verificata(rules, sources):
    for _, regola in rules:
        assert sources[regola["source"]]["verification"] != "unverified", (
            f"{regola['id']}: fonte unverified"
        )


def test_regole_dei_moduli_stabili_usano_solo_fonti_verificate(rules, sources, modules):
    for modulo, regola in rules:
        if modules.get(modulo) == "stable":
            assert sources[regola["source"]]["verification"] == "verified", regola["id"]


def test_valori_di_enumerazione_ammessi(rules):
    for _, regola in rules:
        assert regola["severity"] in SEVERITY, regola["id"]
        assert regola["evidence"] in EVIDENCE, regola["id"]
        assert regola["check"] in CHECK, regola["id"]


def test_ogni_regola_ha_una_guardia_non_vuota(rules):
    """`CONTRIBUTING.md` stabilisce che una regola senza guardia non viene
    accettata. Questo test lo rende un vincolo di build anziche' una promessa."""
    for _, regola in rules:
        guardia = str(regola["guard"]).strip()
        assert len(guardia) > 3, f"{regola['id']}: guardia assente o simbolica"


def test_i_rilievi_deterministici_delegano_a_uno_strumento(rules, sources):
    """Un rilievo `deterministic` deve nascere da uno strumento ufficiale, non da
    un giudizio travestito."""
    for _, regola in rules:
        if regola["evidence"] == "deterministic":
            fonte = sources[regola["source"]]
            assert fonte.get("delegation") is True or regola["check"] == "deterministic", (
                f"{regola['id']}: evidenza deterministica senza delega"
            )


def test_nessuna_regola_esprime_un_giudizio_di_conformita(rules):
    """Il progetto dichiara di non emettere giudizi di conformita'. Il messaggio di
    una regola non puo' contraddirlo.

    La guardia serve anche qui: una ricerca per sottostringa colpirebbe frasi
    legittime come "licenze certificate da Open Source Initiative", dove il verbo
    non riguarda affatto il giudizio della skill. I motivi cercano quindi il
    soggetto che certifica o dichiara conforme, non la radice della parola.
    """
    motivi = (
        r"\b(e|è)'?\s+conforme\b",
        r"\bnon\s+conforme\b",
        r"\brisulta\s+conforme\b",
        r"\bcertifica\s+(la|il|l')\b",
        r"\b(attesta|garantisce)\s+(la\s+)?conformit",
    )
    for _, regola in rules:
        testo = f"{regola['title']} {regola['message']}".lower()
        for motivo in motivi:
            assert not re.search(motivo, testo), (
                f"{regola['id']}: il messaggio esprime un giudizio di conformita' "
                f"(motivo: {motivo})"
            )


def test_la_guardia_sui_giudizi_di_conformita_non_e_troppo_larga():
    """Controguardia: la frase legittima non deve essere intercettata, altrimenti
    il test sopra diventa un ostacolo anziche' una tutela."""
    legittima = "la licenza va scelta fra quelle certificate da open source initiative"
    motivi = (
        r"\b(e|è)'?\s+conforme\b",
        r"\bcertifica\s+(la|il|l')\b",
    )
    assert not any(re.search(m, legittima) for m in motivi)


def test_ogni_modulo_non_stub_ha_un_file_di_riferimento(modules, root):
    for modulo, maturita in modules.items():
        atteso = root / "references" / f"{modulo}.md"
        assert atteso.exists(), f"manca references/{modulo}.md"


def test_i_file_di_riferimento_dichiarano_la_maturita_corretta(modules, root):
    for modulo, maturita in modules.items():
        testo = (root / "references" / f"{modulo}.md").read_text(encoding="utf-8")
        assert f"**{maturita}**" in testo, (
            f"references/{modulo}.md non dichiara la maturita' '{maturita}'"
        )

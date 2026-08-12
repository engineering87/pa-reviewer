"""Invarianti del registro delle fonti.

Il registro e' l'unica fonte di verita' del progetto: se cede qui, tutto il resto
poggia sul nulla.
"""

from __future__ import annotations

import datetime as dt

import pytest

from conftest import MATURITY, VERIFICATION


def test_registro_ha_schema_e_data(registry):
    assert registry.get("schema_version")
    assert dt.date.fromisoformat(str(registry["baseline_date"]))


def test_ogni_fonte_ha_i_campi_obbligatori(sources):
    for source_id, source in sources.items():
        for campo in ("document", "url", "verification", "retrieved"):
            assert source.get(campo), f"{source_id}: manca {campo}"


def test_identificativi_delle_fonti_sono_unici(registry):
    visti = []
    for domain in registry["domains"]:
        visti += [s["id"] for s in domain.get("sources", [])]
    duplicati = {i for i in visti if visti.count(i) > 1}
    assert not duplicati, f"identificativi duplicati: {duplicati}"


def test_livelli_di_verifica_ammessi(sources):
    for source_id, source in sources.items():
        assert source["verification"] in VERIFICATION, source_id


def test_maturita_dei_domini_ammessa(registry):
    for domain in registry["domains"]:
        assert domain.get("maturity") in MATURITY, domain.get("id")


def test_tutti_gli_url_sono_https(sources):
    for source_id, source in sources.items():
        assert source["url"].startswith("https://"), source_id


def test_date_in_formato_iso(sources):
    for source_id, source in sources.items():
        for campo in ("retrieved", "act_date", "review_by"):
            valore = source.get(campo)
            if valore:
                dt.date.fromisoformat(str(valore))


def test_baseline_non_e_invecchiata(sources, gate):
    """Verifica di freschezza.

    Questo test fallisce quando una fonte non viene riverificata entro la soglia.
    E' il comportamento voluto: la manutenzione della baseline non deve dipendere
    dalla buona volonta' del manutentore. Se fallisce, si riaprono le fonti e si
    aggiorna `retrieved`; non si allarga la soglia.
    """
    oggi = dt.date.today()
    scadute = [
        source_id
        for source_id, source in sources.items()
        if (oggi - dt.date.fromisoformat(str(source["retrieved"]))).days
        > gate.STALE_AFTER_DAYS
    ]
    assert not scadute, f"fonti da riverificare: {scadute}"


def test_scadenze_di_revisione_non_superate(sources):
    oggi = dt.date.today()
    superate = [
        source_id
        for source_id, source in sources.items()
        if source.get("review_by")
        and dt.date.fromisoformat(str(source["review_by"])) < oggi
    ]
    assert not superate, f"revisioni scadute: {superate}"


def test_moduli_stabili_poggiano_solo_su_fonti_verificate(registry):
    for domain in registry["domains"]:
        if domain.get("maturity") != "stable":
            continue
        for source in domain.get("sources", []):
            assert source["verification"] == "verified", (
                f"{domain['id']} e' stable ma {source['id']} e' "
                f"{source['verification']}"
            )


def test_perimetro_negativo_e_motivato(registry):
    esclusi = registry.get("out_of_scope", [])
    assert esclusi, "il perimetro negativo non puo' essere vuoto"
    for voce in esclusi:
        assert voce.get("id") and voce.get("reason")


@pytest.mark.parametrize("chiave", ["url_check", "delegation", "supported_versions"])
def test_campi_opzionali_hanno_tipo_corretto(sources, chiave):
    tipi = {"url_check": str, "delegation": bool, "supported_versions": list}
    for source_id, source in sources.items():
        if chiave in source:
            assert isinstance(source[chiave], tipi[chiave]), source_id


def test_fonti_con_url_check_skip_hanno_motivazione(sources):
    for source_id, source in sources.items():
        if source.get("url_check") == "skip":
            assert source.get("url_check_reason"), source_id

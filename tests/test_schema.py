"""Schema dei rilievi e metadatazione del progetto.

Lo schema e' il contratto fra la skill e chi ne legge l'output. Se accetta un rilievo
senza `file:line` o senza fonte, l'intera promessa di tracciabilita' salta.
"""

from __future__ import annotations

import json

import pytest
import yaml

jsonschema = pytest.importorskip("jsonschema")


# --- schema dei rilievi ------------------------------------------------------


@pytest.fixture(scope="module")
def schema(root):
    return json.loads((root / "schema" / "finding.schema.json").read_text(encoding="utf-8"))


def rilievo_valido(**override):
    base = {
        "id": "RIU-005-a1b2c3d4",
        "rule": "RIU-005",
        "source": "RIU-PUBLICCODE-SCHEMA",
        "source_citation": "Lo Standard publiccode.yml, estensioni nazionali",
        "module": "riuso",
        "severity": "important",
        "evidence": "inferred",
        "location": {"file": "src/api/UserController.cs", "line": 88},
        "message": "Il progetto dichiara il rispetto del GDPR ma emette dati personali nei log.",
    }
    base.update(override)
    return base


def test_lo_schema_e_valido(schema):
    jsonschema.Draft202012Validator.check_schema(schema)


def test_accetta_un_rilievo_ben_formato(schema):
    jsonschema.validate(rilievo_valido(), schema)


def test_rifiuta_un_rilievo_senza_fonte(schema):
    rilievo = rilievo_valido()
    del rilievo["source"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(rilievo, schema)


def test_rifiuta_un_rilievo_inferito_senza_riga(schema):
    """Il vincolo centrale del progetto: un'affermazione sul comportamento del
    codice richiede una citazione file:line, mai un'inferenza dai nomi."""
    rilievo = rilievo_valido(location={"file": "src/api/UserController.cs"})
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(rilievo, schema)


def test_rifiuta_un_rilievo_inferito_senza_citazione_della_fonte(schema):
    rilievo = rilievo_valido()
    del rilievo["source_citation"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(rilievo, schema)


def test_rifiuta_un_rilievo_deterministico_senza_strumento(schema):
    rilievo = rilievo_valido(evidence="deterministic")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(rilievo, schema)


def test_accetta_un_rilievo_deterministico_con_strumento(schema):
    jsonschema.validate(
        rilievo_valido(evidence="deterministic", tool="publiccode-parser"), schema
    )


def test_rifiuta_severita_non_prevista(schema):
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(rilievo_valido(severity="bloccante"), schema)


def test_rifiuta_modulo_non_previsto(schema):
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(rilievo_valido(module="procurement"), schema)


def test_rifiuta_rischio_accettato_senza_motivazione(schema):
    """Una deroga senza motivazione non e' tracciabile, quindi non e' una deroga."""
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(rilievo_valido(status="accepted_risk"), schema)


def test_accetta_rischio_accettato_con_motivazione(schema):
    jsonschema.validate(
        rilievo_valido(status="accepted_risk", decision_note="Integrazione esterna."),
        schema,
    )


def test_rifiuta_campi_non_previsti(schema):
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(rilievo_valido(priorita="alta"), schema)


def test_i_moduli_dello_schema_coincidono_con_il_registro(schema, modules):
    previsti = set(schema["properties"]["module"]["enum"])
    assert previsti == set(modules), previsti.symmetric_difference(set(modules))


# --- publiccode.yml del progetto ---------------------------------------------

VERSIONI = ["0", "0.2", "0.2.0", "0.2.1", "0.2.2", "0.3", "0.3.0",
            "0.4", "0.4.0", "0.5", "0.5.0", "0.7", "0.7.0"]
TIPI_SOFTWARE = ["standalone/mobile", "standalone/iot", "standalone/desktop",
                 "standalone/web", "standalone/backend", "standalone/other",
                 "addon", "library", "configurationFiles"]
STATI = ["concept", "development", "beta", "stable", "obsolete"]
MANUTENZIONE = ["internal", "contract", "community", "none"]


@pytest.fixture(scope="module")
def publiccode(root):
    return yaml.safe_load((root / "publiccode.yml").read_text(encoding="utf-8"))


def test_versione_dello_standard_ammessa(publiccode):
    assert publiccode["publiccodeYmlVersion"] in VERSIONI


def test_campi_obbligatori_presenti(publiccode):
    for campo in ("name", "url", "developmentStatus", "softwareType"):
        assert publiccode.get(campo), campo
    assert publiccode["legal"]["license"]
    assert publiccode["localisation"]["availableLanguages"]
    assert "localisationReady" in publiccode["localisation"]


def test_enumerazioni_rispettate(publiccode):
    assert publiccode["developmentStatus"] in STATI
    assert publiccode["softwareType"] in TIPI_SOFTWARE
    assert publiccode["maintenance"]["type"] in MANUTENZIONE


def test_contatti_presenti_per_manutenzione_comunitaria(publiccode):
    if publiccode["maintenance"]["type"] in ("community", "internal"):
        assert publiccode["maintenance"].get("contacts")


def test_lunghezze_delle_descrizioni(publiccode):
    descrizione = publiccode["description"]["it"]
    assert 0 < len(descrizione["shortDescription"]) <= 150
    assert 150 <= len(descrizione["longDescription"]) <= 10_000


def test_nessun_campo_valorizzato_a_null(publiccode):
    """Un campo presente ma nullo fallisce il controllo di tipo del parser."""
    nulli = [chiave for chiave, valore in publiccode.items() if valore is None]
    assert not nulli, nulli


def test_le_autodichiarazioni_non_sono_valorizzate(publiccode):
    """Coerenza con la tesi del progetto: non si dichiara cio' che non si e'
    dimostrato. Se un giorno si valorizzano, va prima superato il modulo riuso."""
    assert "conforme" not in publiccode.get("it", {})

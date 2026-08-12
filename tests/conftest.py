"""Fixture condivise.

I test di questo progetto verificano gli *invarianti dell'artefatto*: che le regole
siano ben formate, che i numeri dichiarati nella documentazione corrispondano al
contenuto reale, che il gate di provenienza blocchi cio' che deve bloccare.

Non verificano la *qualita' dei giudizi* prodotti dalla skill: quella si misura sul
campo, con il metodo descritto in `evaluation/README.md`. Confondere le due cose
darebbe una falsa impressione di validazione.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent

MATURITY = ("stable", "beta", "stub", "reference_only")
VERIFICATION = ("verified", "cited", "unverified")
SEVERITY = ("important", "nit", "pre_existing")
EVIDENCE = ("deterministic", "inferred", "not_verifiable")
CHECK = ("deterministic", "coherence", "structural")


@pytest.fixture(scope="session")
def root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def registry() -> dict:
    return yaml.safe_load((ROOT / "sources.yml").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def sources(registry) -> dict:
    """Indice delle fonti per id."""
    out = {}
    for domain in registry["domains"]:
        for source in domain.get("sources", []):
            out[source["id"]] = source
    return out


@pytest.fixture(scope="session")
def modules(registry) -> dict:
    """Indice modulo -> maturita', per i soli domini che hanno un modulo."""
    return {
        d["module"]: d["maturity"]
        for d in registry["domains"]
        if d.get("module")
    }


@pytest.fixture(scope="session")
def rule_files() -> list[Path]:
    return sorted((ROOT / "rules").glob("*.y*ml"))


@pytest.fixture(scope="session")
def rules(rule_files) -> list[tuple[str, dict]]:
    """Elenco di coppie (modulo, regola)."""
    out = []
    for path in rule_files:
        document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for rule in document.get("rules", []):
            out.append((document.get("module"), rule))
    return out


@pytest.fixture(scope="session")
def gate():
    """Importa scripts/check_sources.py come modulo."""
    spec = importlib.util.spec_from_file_location(
        "check_sources", ROOT / "scripts" / "check_sources.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_sources"] = module
    spec.loader.exec_module(module)
    return module

"""Coerenza fra la tabella dei moduli e i file di regole.

La tabella nel README dichiara quante regole ha ogni modulo. E' l'informazione che un
lettore usa per farsi un'idea della copertura reale, quindi non puo' divergere dal
contenuto di `rules/`.
"""

from __future__ import annotations

import re

import pytest
import yaml


@pytest.fixture(scope="module")
def readme(root) -> str:
    return (root / "README.md").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def conteggi(root) -> dict:
    """Numero di regole per modulo, dai file in rules/."""
    out = {}
    for percorso in sorted((root / "rules").glob("*.y*ml")):
        documento = yaml.safe_load(percorso.read_text(encoding="utf-8")) or {}
        out[documento["module"]] = len(documento.get("rules", []))
    return out


def test_la_tabella_dichiara_i_conteggi_reali(readme, conteggi, modules):
    for modulo in modules:
        riga = re.search(rf"\| `{modulo}` \| \*{{0,2}}\w+\*{{0,2}} \| (\d+) \|", readme)
        assert riga, f"il modulo {modulo} non compare nella tabella con un conteggio"
        dichiarato = int(riga.group(1))
        reale = conteggi.get(modulo, 0)
        assert dichiarato == reale, (
            f"{modulo}: la tabella dichiara {dichiarato} regole, ne risultano {reale}"
        )


def test_il_totale_dichiarato_e_la_somma_dei_moduli(readme, conteggi):
    dichiarato = int(re.search(r"In totale (\d+) regole attive", readme).group(1))
    assert dichiarato == sum(conteggi.values())


def test_il_badge_dichiara_il_totale_reale(readme, conteggi):
    dichiarato = int(re.search(r"regole-(\d+)%20attive", readme).group(1))
    assert dichiarato == sum(conteggi.values())


def test_i_moduli_senza_regole_non_dichiarano_copertura(readme, conteggi, modules):
    """Un modulo senza file di regole deve risultare a zero nella tabella, non
    omesso: l'omissione lascerebbe intendere una copertura non dichiarata."""
    for modulo, maturita in modules.items():
        if maturita == "stub":
            assert conteggi.get(modulo, 0) == 0, modulo
            riga = re.search(rf"\| `{modulo}` \| \w+ \| (\d+) \|", readme)
            assert riga and riga.group(1) == "0", (
                f"{modulo} e' stub: la tabella deve dichiarare 0 regole"
            )

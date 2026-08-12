"""Autocoerenza dei numeri dichiarati.

Il badge sul numero di test e' l'unica affermazione del README che parla dei test
stessi. Se resta indietro, il progetto mente proprio nel punto in cui rivendica di
verificarsi.
"""

from __future__ import annotations

import ast
import re

import pytest


@pytest.fixture(scope="module")
def readme(root) -> str:
    return (root / "README.md").read_text(encoding="utf-8")


def conta_test(root) -> int:
    """Conta le funzioni di test dichiarate, comprese quelle parametrizzate.

    Le parametrizzazioni moltiplicano i casi eseguiti: il conteggio tiene conto del
    numero di parametri, cosi' il badge riflette cio' che pytest riporta davvero.
    """
    totale = 0
    for percorso in sorted((root / "tests").glob("test_*.py")):
        albero = ast.parse(percorso.read_text(encoding="utf-8"))
        for nodo in albero.body:
            if not isinstance(nodo, ast.FunctionDef) or not nodo.name.startswith("test_"):
                continue
            moltiplicatore = 1
            for decoratore in nodo.decorator_list:
                sorgente = ast.unparse(decoratore)
                if "parametrize" in sorgente:
                    valori = decoratore.args[1]
                    if isinstance(valori, (ast.List, ast.Tuple)):
                        moltiplicatore *= len(valori.elts)
            totale += moltiplicatore
    return totale


def test_il_badge_dichiara_il_numero_reale_di_test(readme, root):
    dichiarato = int(re.search(r"invarianti-(\d+)%20test", readme).group(1))
    assert dichiarato == conta_test(root), (
        f"il badge dichiara {dichiarato} test, ne risultano {conta_test(root)}"
    )


def test_la_sezione_qualita_dichiara_lo_stesso_numero(readme, root):
    dichiarato = int(re.search(r"(\d+) test che controllano", readme).group(1))
    assert dichiarato == conta_test(root)


def test_la_documentazione_distingue_invarianti_e_qualita_dei_giudizi(readme, root):
    """La distinzione e' il punto piu' delicato nella comunicazione del progetto:
    una suite verde dice che lo strumento e' ben costruito, non che ha ragione."""
    guida = (root / "tests" / "README.md").read_text(encoding="utf-8")
    for documento in (readme, guida):
        assert "evaluation" in documento
        assert "invarianti" in documento.lower()


def test_ogni_file_di_test_e_documentato_nella_guida(root):
    guida = (root / "tests" / "README.md").read_text(encoding="utf-8")
    for percorso in (root / "tests").glob("test_*.py"):
        assert percorso.name in guida, f"{percorso.name} non compare in tests/README.md"


def test_la_soglia_di_copertura_dichiarata_e_quella_imposta_in_ci(root, readme):
    """Il badge sulla copertura dichiara una soglia minima. Deve coincidere con
    quella che la CI fa rispettare, altrimenti e' un numero decorativo."""
    dichiarata = int(re.search(r"copertura-%E2%89%A5(\d+)%25", readme).group(1))
    workflow = (root / ".github" / "workflows" / "tests.yml").read_text(encoding="utf-8")
    imposta = int(re.search(r"--cov-fail-under=(\d+)", workflow).group(1))
    assert dichiarata == imposta, (
        f"il badge dichiara {dichiarata}%, la CI impone {imposta}%"
    )


def test_le_versioni_di_python_dichiarate_sono_quelle_provate(root, readme):
    workflow = (root / ".github" / "workflows" / "tests.yml").read_text(encoding="utf-8")
    provate = set(re.findall(r'"(3\.\d+)"', workflow))
    badge = re.search(r"python-([0-9.%A-C7]+)-", readme).group(1)
    dichiarate = set(re.findall(r"3\.\d+", badge))
    assert dichiarate == provate, f"badge {dichiarate}, matrice {provate}"

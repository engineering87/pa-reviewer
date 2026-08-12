# Test

## Che cosa verificano, e che cosa no

Questi test verificano gli **invarianti dell'artefatto**: che le regole siano ben
formate e riconducibili a una fonte, che i numeri dichiarati nella documentazione
corrispondano al contenuto reale, che il gate di provenienza blocchi cio' che dichiara
di bloccare, che lo schema dei rilievi rifiuti un rilievo senza `file:line`.

Non verificano la **qualita' dei giudizi** prodotti dalla skill. Quella non si simula:
si misura sul campo, con il metodo descritto in [`../evaluation/README.md`](../evaluation/README.md).
Presentare una suite verde come prova di accuratezza sarebbe la stessa scorciatoia che
questo progetto contesta al resto dell'ecosistema.

## Esecuzione

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -q
```

## Organizzazione

| File | Copre |
| :--- | :--- |
| `test_sources.py` | invarianti del registro delle fonti, freschezza, scadenze di revisione |
| `test_rules.py` | forma delle regole, guardia obbligatoria, coerenza con il registro |
| `test_gate.py` | comportamento del gate, con particolare insistenza sui casi negativi |
| `test_docs.py` | coerenza fra documentazione e contenuto, frontmatter, collegamenti |
| `test_schema.py` | schema dei rilievi e metadatazione `publiccode.yml` del progetto |
| `test_moduli.py` | conteggi per modulo nella tabella del README contro i file di regole |
| `test_selfcheck.py` | autocoerenza: i numeri dichiarati nei badge devono essere veri |

## Due test che meritano una nota

**`test_baseline_non_e_invecchiata`** fallisce quando una fonte non viene riverificata
entro la soglia. E' voluto. Se fallisce si riaprono le fonti e si aggiorna `retrieved`;
non si allarga la soglia.

**`test_la_guardia_sui_giudizi_di_conformita_non_e_troppo_larga`** e' una controguardia:
verifica che il test precedente non intercetti frasi legittime. Nella prima stesura lo
faceva, colpendo "licenze certificate da Open Source Initiative" con una ricerca per
sottostringa. Lo stesso difetto che il progetto chiede di evitare nelle regole vale per
i test che le controllano.

## Copertura

La copertura misurata su `scripts/` è del 94%. Il badge nel README dichiara però una
**soglia minima del 90%**, non il valore corrente, e la CI la fa rispettare con
`--cov-fail-under=90`: un badge che dichiarasse il valore esatto invecchierebbe al primo
commit, mentre una soglia imposta resta vera per costruzione.

```bash
python -m pytest tests/ -q --cov=scripts --cov-report=term-missing
```

La misura riguarda solo il codice eseguibile, cioè `scripts/`. Il resto del repository è
contenuto dichiarativo: YAML, markdown, schema. Applicargli una percentuale di copertura
darebbe un numero più alto e meno significativo, quindi non lo facciamo. Quel contenuto è
verificato dagli invarianti, che sono un controllo più severo di una riga eseguita.

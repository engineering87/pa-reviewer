# Contribuire

Grazie per l'interesse. Questo progetto ha una regola di ammissione piu' stringente
del solito, e conviene conoscerla prima di aprire una pull request.

## Vincolo di provenienza pubblica

**Ogni contributo deve poggiare esclusivamente su fonti pubblicamente accessibili.**

Sono escluse, indipendentemente da chi le proponga:

- documentazione contrattuale, capitolati, requisiti di gara
- codice, architetture, convenzioni o nomi di progetto non pubblicati
- fixture di test derivate da sistemi reali, anche se anonimizzate
- conoscenza del funzionamento interno di una specifica amministrazione o di un
  fornitore, quando derivi da un rapporto professionale anziche' da fonte pubblica

Il vincolo tutela chi contribuisce quanto il progetto. Una regola giustificata da
conoscenza non pubblica non e' verificabile da un terzo, e una regola non verificabile
non serve a nessuno in sede di collaudo.

## Aggiungere una regola

1. **Prima la fonte.** Se la fonte non e' gia' in `sources.yml`, aggiungila con
   documento, ente emittente, atto, data, URL pubblico e livello di verifica.
   Consulta la pagina primaria: `verification: verified` significa che l'hai aperta,
   non che ti fidi di chi la cita.
2. **Poi la regola,** in `rules/<modulo>.yml`, con il campo `source` che riferisce
   quell'identificativo.
3. **Sempre una guardia.** Ogni regola dichiara la condizione che evita il falso
   positivo. Una regola senza guardia non viene accettata: il rumore e' il modo piu'
   rapido per rendere inutilizzabile uno strumento di revisione.
4. **Verifica che sia ancorabile.** Se il rilievo migliore che riesci a formulare non
   indica un `file:line`, appartiene ai promemoria di adempimento, non alle regole.

## Verifica locale

```bash
pip install -r requirements-dev.txt
python scripts/check_sources.py --sources sources.yml --rules rules/
python -m pytest tests/ -q
```

La CI esegue gli stessi comandi. I test verificano anche le condizioni che questo
documento dichiara obbligatorie: una regola senza guardia, o con una guardia simbolica,
fa fallire la build.

Fallisce se una regola non ha fonte, se una fonte e'
incompleta, se un modulo `stable` poggia su una fonte non verificata, o se la baseline
e' invecchiata oltre la soglia.

## Permessi degli script

Gli script in `scripts/` devono essere eseguibili, e il permesso va registrato
nell'indice di Git. Se aggiungi uno script o lavori da un filesystem che non
propaga il bit di esecuzione:

```bash
git update-index --chmod=+x scripts/nuovo-script.sh
git ls-files -s scripts/   # i modi devono essere 100755
```

Un `chmod` sul solo filesystem non basta: il permesso non arriva a chi clona il
repository, e la CI se ne accorge.

## Promuovere un modulo

- **stub -> beta:** tutte le fonti `verified`, regole scritte con guardia.
- **beta -> stable:** precisione misurata su campione pubblico e pubblicata in
  `evaluation/`. Nessuna promozione senza numeri.

## Cosa non viene accettato

- Replica della logica di un validatore ufficiale gia' esistente
- Regole su procedure di gara, DPIA, conservazione documentale, qualificazione cloud
- Qualunque formulazione che esprima un giudizio di conformita'

# Modulo `dati-aperti`

Maturita': **beta**
Fonti: `DAT-DLGS36`, `DAT-LG-PATRIMONIO`, `DAT-DCAT-AP-IT`

## Perche' questo modulo esiste

Il profilo nazionale di metadatazione e' documentato elemento per elemento, con esempi
nelle serializzazioni ammesse, ed e' quindi verificabile su codice che espone cataloghi.
Cio' che manca e' il collegamento fra quel profilo e l'applicativo che produce i metadati:
i validatori disponibili leggono il documento pubblicato, non il codice che lo genera.

## Quando si attiva

Solo per progetti che espongono cataloghi, dataset o loro metadati. Un applicativo che
non pubblica dati non e' soggetto a questo modulo, e il profilo non deve attivarlo.

## Sequenza operativa

1. **Individua il punto di produzione dei metadati**, che puo' essere un endpoint, un
   processo di esportazione o un file generato.
2. **Determina la versione del profilo** dichiarata dal progetto: il confronto va fatto
   con quella, non con l'ultima disponibile.
3. **Applica le regole** in `rules/dati-aperti.yml`.

## Guardie contro i falsi positivi

- **Ereditarieta' dal catalogo.** Licenza ed editore possono essere dichiarati a livello
  di catalogo e valere per i dataset: verificarlo prima di segnalare l'assenza.
- **Elementi raccomandati.** Distinguere l'obbligatorio dal raccomandato: il secondo non
  giustifica un rilievo importante.
- **Limitazioni legittime.** Dati personali e diritti di terzi possono motivare
  condizioni di riutilizzo piu' restrittive.
- **Formati di dominio.** Alcuni ambiti, in particolare quello geografico, hanno formati
  di riferimento propri.

## Cosa questo modulo non fa

Non valuta la qualita' dei dati ne' la loro completezza. Non verifica la pubblicazione
sui portali nazionali, che e' un adempimento e non un fatto del codice.

## Condizioni per passare a stable

1. Tutte le fonti del modulo portano `verification: verified`.
2. Precisione per regola misurata su campione pubblico e pubblicata in
   `evaluation/`, con nessuna regola sotto la soglia fissata.
3. Nessuna regola con guardia rivelatasi insufficiente durante la validazione.

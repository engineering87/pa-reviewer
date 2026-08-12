# Modulo `design-system`

Maturita': **stub**
Fonti: `DES-LG-DESIGN`, `DES-MANUALE`, `DES-BI-DOCS`

## Stato

Perimetro mappato, nessun controllo attivo. **Questo modulo non emette finding.**
Quando il profilo lo attiva, il report dichiara: dominio applicabile, copertura non
ancora implementata.

## Perimetro previsto

- Reimplementazione manuale di componenti gia' presenti in Bootstrap Italia, con perdita di accessibilita' garantita dal componente ufficiale.
- Uso di classi Bootstrap non personalizzate al posto delle varianti del design system: il codice compila e appare plausibile, ma non segue le linee guida.
- Override di token e variabili CSS che alterano contrasto, spaziature o indicatore di focus.
- Assenza di elementi strutturali di pagina previsti: intestazione istituzionale, pie' di pagina con i dati dell'ente, briciole di pane, collegamento di salto al contenuto.
- Versione della libreria deprecata dichiarata nel manifest delle dipendenze.
- Componenti inseriti nel markup senza la relativa inizializzazione JavaScript.
- Reimplementazione parallela in progetti React o Angular che potrebbero adottare i kit ufficiali.

Questo e' il dominio in cui non esiste alcun validatore deterministico, e quindi il nucleo tecnico originale del progetto.

## Condizioni per passare a beta

1. Tutte le fonti del modulo in `sources.yml` portano `verification: verified`.
2. Ogni regola prevista e' ancorabile a `file:line`.
3. Le regole sono scritte in `rules/design-system.yml` con guardia esplicita contro i falsi
   positivi.

## Condizioni per passare a stable

Precisione misurata su campione pubblico e pubblicata in `evaluation/`.

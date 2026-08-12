# Modulo `design-system`

Maturita': **beta**
Fonti: `DES-LG-DESIGN`, `DES-MANUALE`, `DES-BI-DOCS`

## Perche' questo modulo esiste

E' l'unico dominio del perimetro privo di validatore deterministico. Nessuno strumento
verifica oggi se un componente e' stato riscritto a mano al posto di quello ufficiale, e
il codice risultante compila, appare plausibile e supera qualunque analisi statica
generica. Cio' che si perde non e' visibile nel diff: e' la gestione da tastiera, i ruoli e
gli stati che il componente del design system porta con se'.

## Sequenza operativa

1. **Determina la versione in uso.** Leggi il manifest delle dipendenze. Il tema deriva
   da un framework di base e ne eredita le classi: senza sapere quale versione e'
   installata non puoi stabilire quali componenti fossero disponibili.
2. **Distingui il layout dalle viste.** Intestazione, pie' di pagina, briciole di pane e
   collegamento di salto stanno quasi sempre nel modello condiviso. Cercarli nella
   singola vista produce falsi positivi in serie.
3. **Applica le regole** in `rules/design-system.yml`.
4. **Riporta** citando la riga del markup, non quella del foglio di stile.

## Guardie contro i falsi positivi

- **Personalizzazione contro rimozione di garanzie.** Un colore istituzionale diverso e'
  legittimo. La rimozione dell'indicatore di messa a fuoco no. La differenza sta nel
  valore risultante, non nella presenza della sovrascrittura.
- **Progetti React e Angular.** I kit ufficiali gestiscono il ciclo di vita dei
  componenti: le regole sull'inizializzazione non si applicano.
- **Componenti applicativi.** Un componente che risolve un problema di dominio non e'
  una duplicazione. Il rilievo riguarda solo cio' che il design system fornisce gia'.
- **Disallineamento fra documentazione e pacchetto.** La versione riportata dalla
  documentazione puo' restare indietro rispetto a quella pubblicata: il riferimento e'
  il pacchetto, come annotato in `sources.yml`.

## Cosa questo modulo non fa

Non valuta la qualita' estetica ne' l'aderenza a un'identita' visiva. Non sostituisce la
verifica di accessibilita', che ha un modulo proprio: qui si segnala la perdita di
garanzie derivante dalla reimplementazione, non la conformita' ai criteri.

## Condizioni per passare a stable

1. Tutte le fonti del modulo portano `verification: verified`.
2. Precisione per regola misurata su campione pubblico e pubblicata in
   `evaluation/`, con nessuna regola sotto la soglia fissata.
3. Nessuna regola con guardia rivelatasi insufficiente durante la validazione.

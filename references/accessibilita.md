# Modulo `accessibilita`

Maturita': **beta**
Fonti: `ACC-LG-EAA`, `ACC-EN301549`, `ACC-WCAG21`, `ACC-L4-2004`

## Perche' questo modulo esiste

La maggior parte dei criteri di accessibilita' si verifica a runtime, e per quelli
esistono strumenti maturi. Restano scoperte tre aree: la semantica osservabile nel
codice modificato, i componenti costruiti a mano che perdono comportamenti garantiti, e
le disposizioni specifiche delle Linee Guida nazionali su sovrapposizioni e tracciamento
riconducibile alla disabilita'.

## Sequenza operativa

1. **Delega prima.** Esegui `scripts/run_axe.sh` quando lo strumento e' disponibile e
   riporta il suo esito. Se manca, dichiaralo nella sezione sui limiti: non dedurre.
2. **Poi la semantica sul diff.** Applica le regole in `rules/accessibilita.yml` alle
   sole modifiche in esame, salvo revisione dell'intero repository.
3. **Riporta** distinguendo cio' che proviene dallo strumento da cio' che hai dedotto.

## Il limite da dichiarare sempre

Contrasto effettivo, ordine di messa a fuoco, comportamento a ingrandimento e uso reale
con tecnologie assistive **non sono verificabili staticamente**. Non vanno dedotti dal
codice in nessuna circostanza. La verifica automatica, anche a runtime, intercetta una
parte dei problemi: il resto richiede prova manuale e con utenti.

## Guardie contro i falsi positivi

- **Alternativa vuota.** Su un'immagine decorativa e' corretta, non e' un difetto.
- **Nome accessibile fornito altrimenti.** Un controllo puo' esporlo senza etichetta
  visibile: verificare prima di segnalare.
- **Frammenti e viste parziali.** Attributo di lingua e gerarchia dei titoli vanno
  valutati sulla pagina composta, non sul singolo componente.
- **Preferenze di sistema.** Adattare l'interfaccia a una preferenza e' legittimo. Il
  rilievo riguarda la registrazione o la trasmissione del dato.

## Cosa questo modulo non fa

Non produce dichiarazioni di accessibilita' ne' attestazioni, che richiedono
sottoscrizione formale e stanno fra gli adempimenti non verificabili dal codice.

## Condizioni per passare a stable

1. Tutte le fonti del modulo portano `verification: verified`.
2. Precisione per regola misurata su campione pubblico e pubblicata in
   `evaluation/`, con nessuna regola sotto la soglia fissata.
3. Nessuna regola con guardia rivelatasi insufficiente durante la validazione.

# Politica di sicurezza

## Ambito

Questo progetto e' una skill di revisione: legge codice e invoca strumenti esterni.
Sono rilevanti ai fini di sicurezza, in particolare:

- l'esecuzione degli script in `scripts/`, che invocano strumenti di terze parti
- il trattamento di codice sorgente potenzialmente riservato che l'utente sottopone
  alla revisione
- la possibilita' che contenuti presenti nel codice revisionato tentino di influenzare
  il comportamento dell'agente

## Segnalare una vulnerabilita'

Non aprire una issue pubblica. Usa la funzione di segnalazione privata di GitHub
(Security, Report a vulnerability) oppure i recapiti indicati nel profilo del
manutentore.

Indica versione, passi per riprodurre e impatto atteso. Riceverai un riscontro entro
un tempo ragionevole; la correzione sara' pubblicata con una voce nel `CHANGELOG.md`.

## Avvertenze per chi la usa

- Gli script di delega eseguono strumenti esterni, anche via container. Verifica di
  fidarti delle immagini e dei binari presenti nel tuo ambiente.
- Il codice sottoposto a revisione non viene inviato altrove da questo progetto, ma il
  contesto in cui la skill gira potrebbe farlo. Valuta il tuo ambiente prima di
  sottoporre codice riservato.
- Il ruleset del checker OpenAPI viene scaricato dalla rete quando non e' fornito
  localmente. In ambienti isolati, valorizza `OAS_RULESET` con una copia locale.

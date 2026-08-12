# Modulo `sicurezza`

Maturita': **beta**
Fonti: `SEC-LG-SVILUPPO`, `SEC-MISURE-MINIME`, `SEC-TLS`

## Perche' questo modulo esiste, e perche' e' volutamente stretto

Gli strumenti generici di analisi statica coprono gran parte di questo dominio, e sono
migliori di qualunque regola scritta qui. Il modulo si limita a cio' che le fonti
nazionali trattano espressamente: sviluppo sicuro, misure minime per le amministrazioni,
raccomandazioni sul protocollo di trasporto. Tutto il resto va delegato.

Una regola entra in questo modulo solo se e' riconducibile a una di quelle fonti. Se
l'unica giustificazione e' la buona pratica generale, la regola non appartiene a questo
progetto.

## Sequenza operativa

1. **Determina il perimetro esposto.** Un servizio raggiungibile dall'esterno e un
   componente interno hanno esigenze diverse: la severita' ne tiene conto.
2. **Applica le regole** in `rules/sicurezza.yml`.
3. **Riporta** citando sempre file e riga, e distinguendo il codice applicativo dai
   percorsi di test.

## Guardie contro i falsi positivi

- **Percorsi di test e dati di esempio.** Un segreto apparente in una fixture non e' una
  violazione: verificare il percorso prima di segnalare.
- **Valori segnaposto.** Distinguere una credenziale reale da un valore dimostrativo.
- **Configurazione condizionata.** Quando una disattivazione dipende da una variabile
  d'ambiente, verificare il valore predefinito.
- **Scopo dell'algoritmo.** Una funzione di sintesi superata usata per deduplicazione
  non e' un difetto di sicurezza.

## Cosa questo modulo non fa

Non sostituisce l'analisi delle dipendenze, la scansione dei segreti ne' l'analisi
statica di sicurezza: quando quegli strumenti esistono nel progetto, il modulo ne
riconosce la presenza e non ne duplica gli esiti.

## Condizioni per passare a stable

1. Tutte le fonti del modulo portano `verification: verified`.
2. Precisione per regola misurata su campione pubblico e pubblicata in
   `evaluation/`, con nessuna regola sotto la soglia fissata.
3. Nessuna regola con guardia rivelatasi insufficiente durante la validazione.

# Modulo `interoperabilita`

Maturita': **stub**
Fonti: `INT-MODI`, `INT-OAS-CHECKER`

## Stato

Perimetro mappato, nessun controllo attivo. **Questo modulo non emette finding.**
Quando il profilo lo attiva, il report dichiara: dominio applicabile, copertura non
ancora implementata.

## Perimetro previsto

- Delega integrale al checker ufficiale per la verifica statica della specifica OpenAPI.
- Scostamento fra specifica dichiarata e implementazione: rotte presenti nel codice e assenti dalla specifica e viceversa, codici di stato divergenti, parametri non documentati, intestazioni di sicurezza previste dalla specifica e non applicate dal codice.

Lo scostamento fra specifica e implementazione e' cio' che nessun linter di specifiche puo' rilevare, perche' guarda un solo lato del contratto.

## Condizioni per passare a beta

1. Tutte le fonti del modulo in `sources.yml` portano `verification: verified`.
2. Ogni regola prevista e' ancorabile a `file:line`.
3. Le regole sono scritte in `rules/interoperabilita.yml` con guardia esplicita contro i falsi
   positivi.

## Condizioni per passare a stable

Precisione misurata su campione pubblico e pubblicata in `evaluation/`.

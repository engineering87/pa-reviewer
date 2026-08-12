# Modulo `sicurezza`

Maturita': **stub**
Fonti: `SEC-LG-SVILUPPO`, `SEC-MISURE-MINIME`, `SEC-TLS`

## Stato

Perimetro mappato, nessun controllo attivo. **Questo modulo non emette finding.**
Quando il profilo lo attiva, il report dichiara: dominio applicabile, copertura non
ancora implementata.

## Perimetro previsto

- Contestualizzazione dei rilievi generici di sicurezza rispetto alle linee guida AgID per lo sviluppo del software sicuro.
- Versioni del protocollo TLS e suite crittografiche nelle configurazioni.
- Gestione dei segreti, delle sessioni e delle tracce di audit.

**Attenzione alla sovrapposizione:** gli strumenti generici di analisi statica coprono gia' gran parte di questo dominio. Il modulo ha senso solo per la parte specificamente riconducibile alle fonti AgID; il resto va delegato.

## Condizioni per passare a beta

1. Tutte le fonti del modulo in `sources.yml` portano `verification: verified`.
2. Ogni regola prevista e' ancorabile a `file:line`.
3. Le regole sono scritte in `rules/sicurezza.yml` con guardia esplicita contro i falsi
   positivi.

## Condizioni per passare a stable

Precisione misurata su campione pubblico e pubblicata in `evaluation/`.

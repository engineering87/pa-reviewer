# Modulo `accessibilita`

Maturita': **stub**
Fonti: `ACC-LG-EAA`, `ACC-EN301549`, `ACC-WCAG21`, `ACC-L4-2004`

## Stato

Perimetro mappato, nessun controllo attivo. **Questo modulo non emette finding.**
Quando il profilo lo attiva, il report dichiara: dominio applicabile, copertura non
ancora implementata.

## Perimetro previsto

- Semantica del markup sulle modifiche introdotte dal diff: attributi di lingua, etichette dei campi, struttura dei titoli, ruoli ARIA malformati.
- Componenti custom che sostituiscono componenti accessibili gia' disponibili nel design system, perdendo gestione da tastiera e annunci.
- Presenza di overlay di accessibilita' e di meccanismi di tracciamento riconducibili a disabilita': le Linee guida contengono una disposizione esplicita sulla verifica di cookie, fingerprinting e overlay.
- Delega ad axe-core o pa11y per contrasto, ordine di focus e comportamento a zoom, che richiedono esecuzione.

**Fuori perimetro:** dichiarazione di accessibilita', obiettivi annuali, attestazioni sottoscritte digitalmente. Sono adempimenti, non fatti del codice.

## Condizioni per passare a beta

1. Tutte le fonti del modulo in `sources.yml` portano `verification: verified`.
2. Ogni regola prevista e' ancorabile a `file:line`.
3. Le regole sono scritte in `rules/accessibilita.yml` con guardia esplicita contro i falsi
   positivi.

## Condizioni per passare a stable

Precisione misurata su campione pubblico e pubblicata in `evaluation/`.

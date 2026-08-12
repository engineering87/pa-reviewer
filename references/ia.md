# Modulo `ia`

Maturita': **stub**
Fonti: `IA-LG-ADOZIONE`, `IA-LG-SVILUPPO`, `IA-L132-2025`

## Stato

Perimetro mappato, nessun controllo attivo. **Questo modulo non emette finding.**
Quando il profilo lo attiva, il report dichiara: dominio applicabile, copertura non
ancora implementata.

## Perimetro previsto

- Perimetro da definire dopo l'adozione definitiva delle linee guida.

**Blocco esplicito:** le fonti di questo modulo risultavano in iter di adozione alle
date di verifica registrate in `sources.yml`. Nessuna regola operativa puo' derivarne
finche' lo stato non e' confermato sulla pagina istituzionale. La scadenza di revisione
e' registrata nel campo `review_by` delle fonti e viene fatta valere dalla CI.

## Condizioni per passare a beta

1. Tutte le fonti del modulo in `sources.yml` portano `verification: verified`.
2. Ogni regola prevista e' ancorabile a `file:line`.
3. Le regole sono scritte in `rules/ia.yml` con guardia esplicita contro i falsi
   positivi.

## Condizioni per passare a stable

Precisione misurata su campione pubblico e pubblicata in `evaluation/`.

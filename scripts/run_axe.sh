#!/usr/bin/env bash
# Delega a un motore di verifica dell'accessibilita' in esecuzione.
# Copre solo i criteri verificabili a runtime; la semantica sul diff resta al modulo.
set -euo pipefail

TARGET="${1:?URL o percorso da verificare}"

if command -v pa11y >/dev/null 2>&1; then
  pa11y --standard WCAG2AA --reporter json "$TARGET"
else
  echo "STRUMENTO NON DISPONIBILE: pa11y non installato." >&2
  echo "Dichiarare la copertura mancante nel report." >&2
  exit 3
fi

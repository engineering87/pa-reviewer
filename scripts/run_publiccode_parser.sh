#!/usr/bin/env bash
# Delega al validatore ufficiale publiccode-parser-go (Developers Italia).
# Questo script NON implementa alcuna logica di validazione propria.
# Riferimento: https://github.com/italia/publiccode-parser-go
set -euo pipefail

FILE="${1:-publiccode.yml}"

if [[ ! -f "$FILE" ]]; then
  echo "publiccode.yml assente in $(pwd)" >&2
  exit 2   # 2 = file assente, distinto da 1 = file invalido
fi

if command -v publiccode-parser >/dev/null 2>&1; then
  publiccode-parser "$FILE"
elif command -v docker >/dev/null 2>&1; then
  docker run --rm -i italia/publiccode-parser-go /dev/stdin < "$FILE"
else
  echo "STRUMENTO NON DISPONIBILE: ne' publiccode-parser ne' docker." >&2
  echo "Dichiarare la copertura mancante nel report. Non sostituire con un giudizio." >&2
  exit 3   # 3 = strumento indisponibile
fi

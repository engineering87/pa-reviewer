#!/usr/bin/env bash
# Delega al checker ufficiale delle API secondo il ModI (Dipartimento per la
# trasformazione digitale). Questo script NON implementa regole proprie.
# Riferimento: https://github.com/italia/api-oas-checker-rules
#
# Il profilo "Italian Guidelines Full" e' quello richiesto per la pubblicazione
# nel Catalogo API della PDND, con zero errori attesi.
set -euo pipefail

SPEC="${1:?percorso della specifica OpenAPI}"
RULESET="${OAS_RULESET:-https://italia.github.io/api-oas-checker/spectral-full.yml}"

if command -v spectral >/dev/null 2>&1; then
  spectral lint "$SPEC" -r "$RULESET" -f json
elif command -v docker >/dev/null 2>&1; then
  docker run --rm -v "$(pwd)":/locale stoplight/spectral \
    lint "/locale/$SPEC" -r "$RULESET" -f json
else
  echo "STRUMENTO NON DISPONIBILE: ne' spectral ne' docker." >&2
  echo "Dichiarare la copertura mancante nel report." >&2
  exit 3
fi

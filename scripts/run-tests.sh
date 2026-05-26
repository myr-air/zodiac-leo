#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ $# -eq 0 ]]; then
  set -- tests
fi

exec bash "$ROOT/scripts/dev-python.sh" --require-pytest -m pytest "$@"

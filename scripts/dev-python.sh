#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: bash scripts/dev-python.sh [--print] [--require-pytest] [python args...]

Runs Python through uv for this repo.

Use `bash scripts/run-tests.sh` for pytest. Do not use `rtk pytest`, bare
`pytest`, or bare `python3 -m pytest` in this repo.
EOF
}

want_print=0
require_pytest=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --print)
      want_print=1
      shift
      ;;
    --require-pytest)
      require_pytest=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    *)
      break
      ;;
  esac
done

UV_BIN="${MELLOW_UV:-}"
if [[ -z "$UV_BIN" ]]; then
  UV_BIN="$(command -v uv 2>/dev/null || true)"
fi

if [[ -z "$UV_BIN" || ! -x "$UV_BIN" ]]; then
  printf 'uv is required for repo Python execution. Install uv or set MELLOW_UV.\n' >&2
  exit 127
fi

if [[ "$want_print" -eq 1 ]]; then
  "$UV_BIN" run --project "$ROOT" python - <<'PY'
import sys
print(sys.executable)
PY
fi

if [[ "$require_pytest" -eq 1 ]]; then
  "$UV_BIN" run --project "$ROOT" python - <<'PY' >/dev/null
import pytest  # noqa: F401
PY
fi

if [[ $# -eq 0 ]]; then
  exit 0
fi

exec "$UV_BIN" run --project "$ROOT" python "$@"

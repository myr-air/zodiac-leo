#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bash scripts/run_hil.sh [--json] [--hil <hil>] <episode-id>

Examples:
  bash scripts/run_hil.sh s01e05-night-moon-longplay
  bash scripts/run_hil.sh --json s01e05-night-moon-longplay
  bash scripts/run_hil.sh --hil 3 s01e05-night-moon-longplay

Flags:
  --json    Print JSON output from episode_hil_flow.
  --hil N   Run only one HIL stage (1,2,3,4 or hil-1..hil-4).
EOF
}

JSON_MODE=0
HIL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --json)
      JSON_MODE=1
      shift
      ;;
    --hil)
      if [[ $# -lt 2 ]]; then
        echo "error: --hil requires a value" >&2
        usage
        exit 1
      fi
      HIL="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --*)
      echo "error: unknown option: $1" >&2
      usage
      exit 1
      ;;
    *)
      if [[ -z "${EPISODE_ID:-}" ]]; then
        EPISODE_ID="$1"
        shift
      else
        echo "error: unexpected positional arg: $1" >&2
        usage
        exit 1
      fi
      ;;
  esac
done

if [[ -z "${EPISODE_ID:-}" ]]; then
  usage
  exit 1
fi

RUNNER=("bash" "scripts/dev-python.sh" "scripts/episode_hil_flow.py" "--episode-id" "$EPISODE_ID")
if [[ $JSON_MODE -eq 1 ]]; then
  RUNNER+=("--json")
fi

run_one() {
  local label="$1"
  local cmd=("${RUNNER[@]}")
  if [[ "$label" != "all" ]]; then
    cmd+=("--hil" "$label")
  fi
  echo "[run] ${cmd[*]}"
  "${cmd[@]}"
}

if [[ -n "$HIL" ]]; then
  run_one "$HIL"
  exit 0
fi

run_one "all"
run_one "hil-1"
run_one "hil-2"
run_one "hil-3"
run_one "hil-4"

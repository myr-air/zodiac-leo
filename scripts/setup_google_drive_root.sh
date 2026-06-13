#!/usr/bin/env bash

set -euo pipefail

SCRIPT_ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${LEO_SETUP_PROJECT_ROOT:-$(CDPATH= cd -- "${SCRIPT_ROOT}/.." && pwd)}"
DEFAULT_RESOURCE_ROOT="${HOME}/GoogleDrive/zodiac/leo"
RESOURCE_ROOT="${1:-${LEO_RESOURCE_ROOT:-$DEFAULT_RESOURCE_ROOT}}"

RESOURCE_ROOT="${RESOURCE_ROOT%/}"
if [[ -z "$RESOURCE_ROOT" ]]; then
  echo "RESOURCE_ROOT is empty. Set LEO_RESOURCE_ROOT in your shell or pass it as argument." >&2
  exit 1
fi

if [[ "${RESOURCE_ROOT##*/}" == "candidates" ]]; then
  CANDIDATE_ROOT="$RESOURCE_ROOT"
else
  CANDIDATE_ROOT="$RESOURCE_ROOT/candidates"
fi

if [[ ! -d "$CANDIDATE_ROOT" ]]; then
  echo "Candidate root not found: $CANDIDATE_ROOT" >&2
  echo "Create it first or point to an existing Google Drive sync folder." >&2
  exit 1
fi

LINK_PATH="$PROJECT_ROOT/candidates"
if [[ -L "$LINK_PATH" ]]; then
  ln -sfn "$CANDIDATE_ROOT" "$LINK_PATH"
elif [[ -e "$LINK_PATH" ]]; then
  BACKUP_PATH="${LINK_PATH}.old-$(date +%s)"
  if ! mv "$LINK_PATH" "$BACKUP_PATH"; then
    echo "Blocking: could not move existing $LINK_PATH; please move or remove it manually." >&2
    exit 1
  fi
  echo "Backed up existing candidates directory to: $BACKUP_PATH"
  ln -s "$CANDIDATE_ROOT" "$LINK_PATH"
else
  ln -s "$CANDIDATE_ROOT" "$LINK_PATH"
fi

echo "Linked $LINK_PATH -> $CANDIDATE_ROOT"
echo "export LEO_RESOURCE_ROOT=\"$RESOURCE_ROOT\""
echo
echo "Run this on each shell:"
echo "  export LEO_RESOURCE_ROOT=\"$RESOURCE_ROOT\""

#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bash scripts/migrate_leo_new_machine.sh [options]

Options:
  --repo-dir PATH        Local repo checkout path (default: ~/workspaces/zodiac/leo)
  --resource-root PATH   Shared resource root (default: ~/GoogleDrive/zodiac/leo)
  --branch NAME          Git branch to checkout (default: main)
  --repo-url URL         Optional origin URL if target directory is not already a repo.
  --write-shell-profile  Append LEO_RESOURCE_ROOT export to your shell profile.
  -h, --help             Show help

Examples:
  bash scripts/migrate_leo_new_machine.sh
  bash scripts/migrate_leo_new_machine.sh --repo-dir ~/projects/leo --resource-root /Volumes/Drive/zodiac/leo --branch main
EOF
}

WRITE_PROFILE=0
REPO_DIR="${HOME}/workspaces/zodiac/leo"
RESOURCE_ROOT="${HOME}/GoogleDrive/zodiac/leo"
BRANCH="main"
REPO_URL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-dir)
      REPO_DIR="$2"
      shift 2
      ;;
    --resource-root)
      RESOURCE_ROOT="$2"
      shift 2
      ;;
    --branch)
      BRANCH="$2"
      shift 2
      ;;
    --repo-url)
      REPO_URL="$2"
      shift 2
      ;;
    --write-shell-profile)
      WRITE_PROFILE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

REPO_DIR="${REPO_DIR%/}"
RESOURCE_ROOT="${RESOURCE_ROOT%/}"

if [[ -z "$REPO_DIR" || -z "$RESOURCE_ROOT" ]]; then
  echo "error: repo-dir and resource-root must be non-empty." >&2
  exit 1
fi

if ! command -v git >/dev/null 2>&1; then
  echo "error: git is required but not found." >&2
  exit 1
fi

mkdir -p "$(dirname "$REPO_DIR")"

if [[ ! -d "$REPO_DIR/.git" ]]; then
  if [[ -d "$REPO_DIR" ]]; then
    echo "error: $REPO_DIR exists but is not a git repository." >&2
    exit 1
  fi
  if [[ -z "$REPO_URL" ]]; then
    echo "error: repo not found at $REPO_DIR and --repo-url is not provided." >&2
    echo "Hint: pass --repo-url git@github.com:<owner>/zodiac-leo.git" >&2
    exit 1
  fi
  mkdir -p "$REPO_DIR"
  git clone "$REPO_URL" "$REPO_DIR"
fi

cd "$REPO_DIR"

if [[ -n "${REPO_URL}" ]]; then
  git remote set-url origin "$REPO_URL" || git remote add origin "$REPO_URL" || true
fi

if ! git fetch --all --prune; then
  echo "warning: git fetch failed; continuing with local state."
fi

if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  git checkout "$BRANCH"
elif git show-ref --verify --quiet "refs/remotes/origin/$BRANCH"; then
  git checkout -B "$BRANCH" "origin/$BRANCH"
else
  echo "warning: branch '$BRANCH' not found locally or remotely; staying on current branch."
fi

if [[ "$BRANCH" == "$(git rev-parse --abbrev-ref HEAD)" ]]; then
  git pull --ff-only origin "$BRANCH" || true
fi

mkdir -p "$RESOURCE_ROOT/candidates"
bash scripts/setup_google_drive_root.sh "$RESOURCE_ROOT"
eval "export LEO_RESOURCE_ROOT=\"$RESOURCE_ROOT\""

if [[ "$WRITE_PROFILE" -eq 1 ]]; then
  SHELL_RC="$HOME/.zshrc"
  [[ "${SHELL:-}" != *zsh* ]] && SHELL_RC="$HOME/.bashrc"
  PROFILE_LINE="export LEO_RESOURCE_ROOT=\"${RESOURCE_ROOT}\""
  if ! grep -Fq "$PROFILE_LINE" "$SHELL_RC" 2>/dev/null; then
    {
      echo
      echo "# Leo shared resource root"
      echo "$PROFILE_LINE"
    } >> "$SHELL_RC"
    echo "Updated profile: $SHELL_RC"
  else
    echo "Profile already contains LEO_RESOURCE_ROOT."
  fi
fi

echo
echo "Done."
echo "Project: $REPO_DIR"
echo "Resource root: $RESOURCE_ROOT"
echo "Candidates root: $RESOURCE_ROOT/candidates"
echo "LEO_RESOURCE_ROOT is currently: $LEO_RESOURCE_ROOT"
echo "Run this if needed in current shell:"
echo "  export LEO_RESOURCE_ROOT=\"$RESOURCE_ROOT\""
if [[ "$WRITE_PROFILE" -eq 0 ]]; then
  echo
  echo "Optional: rerun with --write-shell-profile to persist environment variable."
fi


# Python / uv Policy

Status: active  
Updated: 2026-05-26

## Rule

Use `uv` as the only repo Python entrypoint.

```bash
bash scripts/dev-python.sh --print
bash scripts/dev-python.sh -m py_compile scripts/example.py
bash scripts/run-tests.sh
bash scripts/verify-standalone.sh
```

Do not use `rtk pytest`, bare `pytest`, or bare `python3 -m pytest` in this
repo. This machine has multiple Python installs; `/usr/bin/python3` lacks the
repo test dependencies, while `rtk pytest` fails to spawn `pytest` in this shell.

## Do Not Delete System Python

Do not remove or symlink over `/usr/bin/python3` or Apple CommandLineTools
Python. macOS, Xcode/CLT, Homebrew, and unrelated tools may rely on them. The
safe control point is the repo runner and optional shell aliases/functions, not
system Python deletion.

## Optional Shell Guard

If you want day-to-day shell commands to prefer `uv` while still preserving
system tools, scope any shell helper to this repository's exact root. Do not use
a generic `pyproject.toml` / `uv.lock` detector for every directory; that would
run untrusted projects through `uv` unexpectedly.

```zsh
_mellow_repo_root="/Users/xiivth/workspaces/mellow-longplay"

python() {
  local cwd_root
  cwd_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
  if [[ "$cwd_root" == "$_mellow_repo_root" ]]; then
    command bash "$_mellow_repo_root/scripts/dev-python.sh" "$@"
  else
    command python3 "$@"
  fi
}

pytest() {
  local cwd_root
  cwd_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
  if [[ "$cwd_root" == "$_mellow_repo_root" ]]; then
    command bash "$_mellow_repo_root/scripts/run-tests.sh" "$@"
  else
    command pytest "$@"
  fi
}
```

This does not mutate system Python and can be removed from the shell config if a
non-project tool needs the original behavior.

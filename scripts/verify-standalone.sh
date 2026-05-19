#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 - <<'PY'
from pathlib import Path
import csv
import json
import sys

required_files = [
    'README.md',
    'AGENTS.md',
    'KNOWLEDGE.md',
    '.gitignore',
    'docs/operating-boundary.md',
    'docs/provider-platform-boundary.md',
    'channel/channel.md',
    'channel/roadmap.md',
    'channel/signature-visual-system.md',
    'channel/signature-references/README.md',
    'channel/signature-references/gold-crescent-record-charm.png',
    'channel/signature-references/recurring-campus-listener-character-sheet.png',
    '.agents/skills/suno-song-production-guardrails/SKILL.md',
    '.agents/skills/lyric-craft-multilingual-guardrails/SKILL.md',
    '.agents/skills/gpt-image-prompting-guardrails/SKILL.md',
    '.agents/skills/episode-state-gatekeeper/SKILL.md',
    '.opencode/agents/creative-director.md',
    '.opencode/agents/song-concept-designer.md',
    '.opencode/agents/songwriter.md',
    '.opencode/agents/lyric-reviewer.md',
    '.opencode/agents/suno-reviewer.md',
    '.opencode/agents/production-manager.md',
    '.opencode/agents/readiness-reviewer.md',
]

required_dirs = [
    'channel/episodes',
    'channel/templates',
    'channel/signature-references',
    'candidates',
    'scripts',
    'tests',
]

errors = []
for path in required_files:
    if not Path(path).is_file():
        errors.append(f'missing file: {path}')
for path in required_dirs:
    if not Path(path).is_dir():
        errors.append(f'missing dir: {path}')

for path in sorted(Path('.').glob('**/*.json')):
    if any(part in {'.git', '.tmp', 'node_modules', '__pycache__'} for part in path.parts):
        continue
    try:
        json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f'invalid JSON {path}: {exc}')

for path in sorted(Path('.').glob('**/*.csv')):
    if any(part in {'.git', '.tmp', 'node_modules', '__pycache__'} for part in path.parts):
        continue
    try:
        with path.open(newline='', encoding='utf-8') as handle:
            rows = list(csv.reader(handle))
    except Exception as exc:
        errors.append(f'invalid CSV {path}: {exc}')
        continue
    if not rows:
        errors.append(f'empty CSV: {path}')
        continue
    width = len(rows[0])
    for index, row in enumerate(rows, start=1):
        if len(row) != width:
            errors.append(f'CSV width mismatch {path}:{index}: expected {width}, got {len(row)}')

blocked_paths = [
    Path('channels'),
    Path('tools/chrome-prompt-helper'),
]
for path in blocked_paths:
    if path.exists():
        errors.append(f'old-scope path exists: {path}')

for path in Path('.').glob('**/.DS_Store'):
    if not any(part in {'.git', '.tmp', 'node_modules', '__pycache__'} for part in path.parts):
        print(f'WARN: OS metadata file present but ignored by .gitignore: {path}')

text_blockers = [
    'channels/mellow-longplay',
    'channels/miniature-epics',
    'miniature-epics',
    'youtube-api-read-only-sync',
    'ml-pilot-001',
    'ML-PILOT-001',
]
for path in sorted(Path('.').glob('**/*')):
    if not path.is_file() or any(part in {'.git', '.tmp', 'node_modules', '__pycache__'} for part in path.parts):
        continue
    if path == Path('scripts/verify-standalone.sh'):
        continue
    if path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.mp3', '.wav', '.mp4', '.mov'}:
        continue
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    for token in text_blockers:
        if token in text:
            errors.append(f'old-scope reference {token!r} in {path}')

media_extensions = {'.mp3', '.wav', '.flac', '.aiff', '.aif', '.png', '.jpg', '.jpeg', '.webp', '.tif', '.tiff', '.mp4', '.mov', '.mkv', '.webm'}
tracked_like_media = [str(path) for path in Path('.').glob('**/*') if path.is_file() and path.suffix.lower() in media_extensions]
allowed_media = {
    'channel/signature-references/gold-crescent-record-charm.png',
    'channel/signature-references/recurring-campus-listener-character-sheet.png',
}
for path in tracked_like_media:
    if path not in allowed_media:
        errors.append(f'media file present in source tree: {path}')

if errors:
    for error in errors:
        print(f'FAIL: {error}', file=sys.stderr)
    sys.exit(1)

print('PASS: standalone Mellow Longplay structure verified')
PY

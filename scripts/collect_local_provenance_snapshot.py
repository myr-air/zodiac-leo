#!/usr/bin/env python3
"""Collect a compact local provenance fingerprint for S01E01 evidence files.

The report stores hashes, sizes, and paths only. It intentionally does not
record credentials, account state, browser data, private analytics, or provider
claims that are not already known.
"""

from __future__ import annotations

import hashlib
import glob
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EPISODE = "s01e01-campus-cafe-longplay"
EPISODE_ROOT = ROOT / "channel" / "episodes" / EPISODE
OUTPUT = EPISODE_ROOT / "reviews" / "local-provenance-evidence.md"


GROUPS = {
    "selected_audio_wav": ROOT / "candidates" / EPISODE / "audio" / "selected" / "*.wav",
    "subtitle_draft_json": ROOT / "candidates" / EPISODE / "subtitles" / "proofs" / "track-*" / "s01e01-track-*-subtitle-alignment-draft-01.json",
    "visual_v6_proof_media": ROOT / "candidates" / EPISODE / "visual" / "proofs" / "animated-v6" / "s01e01-vis-c01-v6-*",
    "source_truth_docs": EPISODE_ROOT / "source" / "*.md",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def records_for(pattern: Path) -> list[dict[str, str | int]]:
    matches = [Path(match) for match in sorted(glob.glob(str(pattern)))]
    records: list[dict[str, str | int]] = []
    for path in matches:
        if path.is_file():
            stat = path.stat()
            records.append(
                {
                    "path": str(path.relative_to(ROOT)),
                    "bytes": stat.st_size,
                    "sha256": sha256(path),
                }
            )
    return records


def main() -> None:
    groups = {name: records_for(pattern) for name, pattern in GROUPS.items()}
    lines: list[str] = []
    lines.append("# S01E01 Local Provenance Evidence")
    lines.append("")
    lines.append("Status: local fingerprint snapshot / source-only / no provider-account claim  ")
    lines.append(f"Updated: {date.today().isoformat()}")
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(
        "This report fingerprints local source/evidence files only. It does not prove provider model, account ownership, copyright status, Content ID status, monetization status, platform safety, upload readiness, or release readiness."
    )
    lines.append("")
    lines.append("Do not store credentials, cookies, OAuth tokens, browser profiles, private analytics exports, account IDs, or raw private account state here.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Group | File count | Evidence status |")
    lines.append("|---|---:|---|")
    for name, records in groups.items():
        lines.append(f"| `{name}` | {len(records)} | local hash/size recorded; source-only |")
    lines.append("")
    lines.append("Provider/model/date/account-boundary facts for candidate media remain `unknown_user_supplied` unless the user separately provides non-secret provenance details. This report is still useful for local file identity, duplicate checks, and source-review continuity.")
    lines.append("")

    for name, records in groups.items():
        lines.append(f"## {name}")
        lines.append("")
        lines.append("| Path | Bytes | SHA-256 |")
        lines.append("|---|---:|---|")
        for record in records:
            lines.append(f"| `{record['path']}` | {record['bytes']} | `{record['sha256']}` |")
        lines.append("")

    lines.append("## Still Blocked")
    lines.append("")
    lines.append("- Treat these hashes as local evidence only, not rights/platform/release evidence.")
    lines.append("- Final subtitle sidecars, assembly, render/export, upload/publish, analytics, account actions, Content ID actions, and rights/platform-safety claims remain blocked until separate explicit gates.")
    lines.append("")
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUTPUT.relative_to(ROOT)))


if __name__ == "__main__":
    main()

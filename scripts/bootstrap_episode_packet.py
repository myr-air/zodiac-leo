#!/usr/bin/env python3
"""Create a source-only Mellow Longplay episode packet scaffold.

The helper creates repo source files only. It never creates candidate media,
provider facts, render outputs, YouTube resources, credentials, or account state.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EPISODE_ID_RE = re.compile(r"^s\d{2}e\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")


S01E02_DEFAULTS = {
    "episode_id": "s01e02-classroom-window-longplay",
    "working_longplay": "Classroom Window Longplay",
    "hook": "college classroom light, afternoon window",
    "lyric_lane": "curiosity, almost-said feelings, study-day warmth",
}


@dataclass
class EpisodeBootstrapConfig:
    episode_id: str
    working_longplay: str
    hook: str
    lyric_lane: str
    prepared_by: str = "Mayr"
    prepared_date: str = date.today().isoformat()
    season: int = 1
    week: int = 2
    main_songs: int = 12
    bonus_songs: int = 1
    language: str = "English-first"


def validate_config(config: EpisodeBootstrapConfig) -> None:
    if not EPISODE_ID_RE.fullmatch(config.episode_id):
        raise ValueError(
            "episode_id must look like s01e02-classroom-window-longplay and contain only lowercase slug parts"
        )
    required = {
        "working_longplay": config.working_longplay,
        "hook": config.hook,
        "lyric_lane": config.lyric_lane,
        "prepared_by": config.prepared_by,
        "prepared_date": config.prepared_date,
    }
    missing = [name for name, value in required.items() if not value.strip()]
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def planned_paths(config: EpisodeBootstrapConfig, root: Path = PROJECT_ROOT) -> list[Path]:
    packet = root / "channel" / "episodes" / config.episode_id
    return [
        packet / "manifest.json",
        packet / "reviews" / "current-state.md",
        packet / "reviews" / "episode-production-worksheet.md",
        packet / "reviews" / "release-decision-plan.md",
        packet / "source" / "songs.md",
        packet / "source" / "suno-manual-fields.md",
        packet / "source" / "prompt-pack.md",
        packet / "source" / "visual.md",
        packet / "source" / "metadata.md",
        packet / "subtitles" / "README.md",
        packet / "tracking" / "status.csv",
        packet / "tracking" / "assets.csv",
        packet / "tracking" / "provenance.csv",
        packet / "tracking" / "decisions.csv",
    ]


def manifest(config: EpisodeBootstrapConfig) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "episode_id": config.episode_id,
        "channel": "Mellow Longplay",
        "status": "gate_0_scaffolded_source_only",
        "gate": "gate_0_bootstrap",
        "created": config.prepared_date,
        "updated": config.prepared_date,
        "working_longplay": config.working_longplay,
        "format_target": {
            "main_songs": config.main_songs,
            "bonus_songs": config.bonus_songs,
            "language": config.language,
        },
        "source_state": {
            "episode_brief": "scaffolded_needs_shape_review",
            "lyrics": "not_started_source_only",
            "suno_tracks": "not_started_source_only",
            "prompt_pack": "not_started_source_only",
            "metadata": "not_started_source_only",
            "audio_candidates": "none_do_not_create_ids_before_real_files",
            "visual_candidates": "none_do_not_create_ids_before_real_files",
            "subtitles": "not_started_source_only",
            "assembly_package": "not_started_source_only",
            "render_export_plan": "blocked_until_explicit_gate",
            "release_decision": "blocked_not_opened",
            "youtube_api_video_upload_package": "blocked_not_created",
            "youtube_api_thumbnail_upload_package": "blocked_not_created",
        },
        "claim_boundary": (
            "Source-only scaffold for a future episode packet. Not provider approval, media existence, "
            "render/export approval, upload/API execution. Not public publish/release approval or rights/platform-safety claim."
        ),
    }


def current_state_md(config: EpisodeBootstrapConfig) -> str:
    return f"""# {config.episode_id.upper()} Current State — {config.working_longplay}

Status: Gate 0 scaffolded source-only / Gate 1 not locked / public publish blocked  
Updated: {config.prepared_date}

- Episode packet scaffolded for Season {config.season} Week {config.week}: `{config.working_longplay}`.
- Roadmap hook: {config.hook}.
- Lyric lane: {config.lyric_lane}.
- Gate 1 source packet is not locked yet. Song titles, lyrics, Suno fields, prompt pack, visual source, metadata, subtitles, audio candidates, render outputs, and release evidence are all pending.
- No candidate IDs, media files, provider facts, render/export facts, YouTube video IDs, analytics, or release facts exist for this episode.
- public publish remains blocked until a separate final release gate.
- Render/export, upload/API, public publish, scheduling, captions, playlists, analytics, Content ID, account edits, credentials in repo, and positive rights/platform-safety claims remain blocked until narrow explicit gates are opened and recorded.

Verdict: `gate_0_scaffolded_source_only_public_publish_blocked`
"""


def production_worksheet_md(config: EpisodeBootstrapConfig) -> str:
    return f"""# {config.episode_id.upper()} Production Worksheet — {config.working_longplay}

Status: template copied / source-only scaffold / no media or release gate  
Episode: `{config.episode_id}`  
Prepared by: {config.prepared_by}  
Prepared date: {config.prepared_date}  
Source packet version: `v0.0-scaffold`

## 0. Boundary

This worksheet is an internal source-to-video checklist. It does not approve provider use, media generation, render/export, upload, publishing, Suno/YouTube/API/browser automation, account mutation, credential storage, Content ID registration, public release, or positive rights/platform-safety claims.

Fastlane rule: reuse approved channel-level defaults by citation; approve only episode deltas and real external/local actions.

## 1. Episode Delta Seed

| Field | Value |
|---|---|
| Working longplay | {config.working_longplay} |
| Roadmap hook | {config.hook} |
| Lyric lane | {config.lyric_lane} |
| Default format | {config.main_songs} main songs + {config.bonus_songs} bonus / {config.language} |
| Current gate | Gate 0 scaffold only |

## 2. Build Path Status

| Step | Exit evidence | Status / notes |
|---:|---|---|
| 0. Scaffold | manifest, current state, source/review/tracking placeholders | pass_source_only |
| 1. Source packet lock | `source/songs.md`, `source/suno-manual-fields.md`, `source/suno-tracks/*.md`, reviews/tracking | pending |
| 2. Candidate intake | real local audio/visual files exist before IDs/provenance | blocked_until_gate |
| 3. Sequence + metadata | chapter timeline, disclosure, title/description/tags policy | pending |
| 4. Subtitles + sidecars | final `.srt`/`.vtt`, parser checks, human watch/spot evidence | pending |
| 5. Local render QA | explicit render/export gate, video path, mechanical QA, human spot pass | blocked_until_gate |
| 6. YouTube handoff planning | release decision, current public policy/account check, API/manual package | blocked_until_gate |
| 7. Public publish decision | user-owned final action, rollback owner, no-store hygiene | blocked_until_explicit_final_gate |

Do not open the next step by implication. Each local media render/export or external platform/API action still needs its own explicit gate.

## 3. Current Verdict

```text
Verdict: scaffolded_source_only
Scope: reusable episode packet skeleton only
Evidence: manifest.json, reviews/current-state.md, source placeholders, tracking CSVs
Critical blockers: source packet not written; no local candidate media; render/export and YouTube actions blocked
Next allowed action: shape Gate 1 source packet from roadmap and channel defaults
Still blocked: provider/account automation, media generation without gate, render/export without gate, upload/publish/API without gate, credentials in repo, Content ID, rights/platform-safety claims
```
"""


def release_decision_plan_md(config: EpisodeBootstrapConfig) -> str:
    return f"""# {config.episode_id.upper()} Release Decision Plan — {config.working_longplay}

Status: not opened / placeholder only / public publish blocked  
Episode: `{config.episode_id}`  
Prepared: {config.prepared_date}

## 0. Boundary

This file is a placeholder for a future release decision gate. It is not opened and does not approve upload, private API execution, thumbnail upload, public publishing, scheduling, analytics, provider/browser/account actions, credentials or tokens stored in repo, Content ID action, release readiness, or positive rights/platform claims.

Public publish remains blocked until a future explicit final gate records current final assets, metadata/disclosure review, current official policy check, user-owned account-specific check, provenance/risk acceptance, and rollback owner.

## 1. Required Evidence Before This Gate Can Open

| Area | Required evidence | Current state |
|---|---|---|
| Final local asset selection | exact final MP4/render output and sidecars after QA | none |
| Metadata/disclosure | title, description, chapters, tags, AI-assisted disclosure | pending |
| Current policy/account check | official current public platform policy and user-owned account constraints | pending / user-owned |
| Provenance/risk acceptance | non-secret source provenance and known limitations | pending |
| Upload route | manual Studio handoff or guarded private API path, selected explicitly | not selected |
| Rollback owner | user owns privacy changes, delete/unlist, edits, comments, analytics | pending |

## 2. Current Verdict

```text
Verdict: release_gate_not_opened_public_publish_blocked
Scope: placeholder only
Next allowed action: continue source-only Gate 1 work
Still blocked: private upload, thumbnail upload, public publish, schedule, visibility mutation, captions, playlists, analytics, Content ID, account edits, credentials/account-state storage in repo, and rights/platform-safety claims
```
"""


def songs_md(config: EpisodeBootstrapConfig) -> str:
    return f"""# {config.episode_id.upper()} Songs — {config.working_longplay}

Status: scaffold / not written / source-only  
Updated: {config.prepared_date}

## Boundary

No lyrics, Suno fields, provider handoff, generated audio, candidates, render/export, upload, public publish, or rights/platform-safety claim is approved by this scaffold.

## Episode Seed

- Working longplay: {config.working_longplay}
- Roadmap hook: {config.hook}
- Lyric lane: {config.lyric_lane}
- Default format: {config.main_songs} main songs + {config.bonus_songs} bonus, {config.language}

## Episode Style & Theme Spine

Pending. Before drafting tracks, define listener job, theme thesis, base sonic lane, BPM range, vocal lane, core instrumentation, base excludes, control baseline, allowed variation slots, motif/lexical budgets, and safety boundaries.

## Track Plan

Do not invent final titles or candidate IDs here. Fill one track at a time after Story + Reference Brief, Track Delta, lexical ledger, and review.

| Track | Working title | Story/object function | Macro/rhetorical delta | Style/BPM delta | Status |
|---:|---|---|---|---|---|
| 1 | `<pending>` | `<pending>` | `<pending>` | `<pending>` | not_started |
| 2 | `<pending>` | `<pending>` | `<pending>` | `<pending>` | not_started |
| 3 | `<pending>` | `<pending>` | `<pending>` | `<pending>` | not_started |
| 4 | `<pending>` | `<pending>` | `<pending>` | `<pending>` | not_started |
| 5 | `<pending>` | `<pending>` | `<pending>` | `<pending>` | not_started |
| 6 | `<pending>` | `<pending>` | `<pending>` | `<pending>` | not_started |
| 7 | `<pending>` | `<pending>` | `<pending>` | `<pending>` | not_started |
| 8 | `<pending>` | `<pending>` | `<pending>` | `<pending>` | not_started |
| 9 | `<pending>` | `<pending>` | `<pending>` | `<pending>` | not_started |
| 10 | `<pending>` | `<pending>` | `<pending>` | `<pending>` | not_started |
| 11 | `<pending>` | `<pending>` | `<pending>` | `<pending>` | not_started |
| 12 | `<pending>` | `<pending>` | `<pending>` | `<pending>` | not_started |
| 13 bonus | `<pending>` | `<pending>` | `<pending>` | `<pending>` | not_started |
"""


def suno_manual_fields_md(config: EpisodeBootstrapConfig) -> str:
    return f"""# {config.episode_id.upper()} Suno Manual Fields — {config.working_longplay}

Status: scaffold / not ready for provider use / source-only  
Updated: {config.prepared_date}

This index is pending. Before any manual provider handoff, every track must have a copy-ready file under `source/suno-tracks/` with: Song Title, Lyrics Mode, Lyrics, Styles with approximate BPM, Exclude Styles, Vocal Gender, Weirdness, and Style Influence.

Provider/browser/API/account actions and generated audio remain blocked until a separate explicit gate.
"""


def prompt_pack_md(config: EpisodeBootstrapConfig) -> str:
    return f"""# {config.episode_id.upper()} Prompt Pack — {config.working_longplay}

Status: scaffold / source-only  
Updated: {config.prepared_date}

Prompt/control materials are pending. Use the Episode Style & Theme Spine and per-track Track Delta before drafting any provider-facing fields. No provider operation or generated media is approved here.
"""


def visual_md(config: EpisodeBootstrapConfig) -> str:
    return f"""# {config.episode_id.upper()} Visual Source — {config.working_longplay}

Status: scaffold / source-only  
Updated: {config.prepared_date}

Visual direction is pending. Reuse channel signature motifs only as source-only design guidance unless a later visual gate approves a different direction. No image generation, reference-image input, proof output, render/export, upload, or rights/platform claim is approved here.
"""


def metadata_md(config: EpisodeBootstrapConfig) -> str:
    return f"""# {config.episode_id.upper()} Metadata — {config.working_longplay}

Status: scaffold / source-only  
Updated: {config.prepared_date}

Title, description, disclosure, chapters, tags, and blocked-claim scan are pending. This file is not final upload metadata and does not approve YouTube API/browser/account action or public publish.
"""


def subtitles_readme_md(config: EpisodeBootstrapConfig) -> str:
    return f"""# {config.episode_id.upper()} Subtitles

Status: not started / source-only  
Updated: {config.prepared_date}

Final sidecars do not exist yet. Create subtitle timing only after selected local audio exists and the subtitle timing gate is opened. Do not invent timings, cue counts, sidecar byte-match claims, render facts, or upload facts.
"""


def write_csv(path: Path, header: list[str], rows: Iterable[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def write_packet(config: EpisodeBootstrapConfig, root: Path) -> list[Path]:
    packet = root / "channel" / "episodes" / config.episode_id
    if packet.exists():
        raise FileExistsError(f"episode packet already exists: {rel(packet, root)}")

    for directory in [packet / "reviews", packet / "source" / "suno-tracks", packet / "subtitles", packet / "tracking"]:
        directory.mkdir(parents=True, exist_ok=False)

    files: dict[Path, str] = {
        packet / "manifest.json": json.dumps(manifest(config), indent=2, ensure_ascii=False) + "\n",
        packet / "reviews" / "current-state.md": current_state_md(config),
        packet / "reviews" / "episode-production-worksheet.md": production_worksheet_md(config),
        packet / "reviews" / "release-decision-plan.md": release_decision_plan_md(config),
        packet / "source" / "songs.md": songs_md(config),
        packet / "source" / "suno-manual-fields.md": suno_manual_fields_md(config),
        packet / "source" / "prompt-pack.md": prompt_pack_md(config),
        packet / "source" / "visual.md": visual_md(config),
        packet / "source" / "metadata.md": metadata_md(config),
        packet / "subtitles" / "README.md": subtitles_readme_md(config),
    }
    for path, text in files.items():
        path.write_text(text, encoding="utf-8")

    write_csv(
        packet / "tracking" / "status.csv",
        ["date", "episode_id", "gate", "area", "status", "source_path", "notes"],
        [
            [
                config.prepared_date,
                config.episode_id,
                "gate_0_bootstrap",
                "episode_packet",
                "scaffolded_source_only",
                rel(packet / "manifest.json", root),
                "Fresh episode packet scaffold created with no media candidates or release facts",
            ],
            [
                config.prepared_date,
                config.episode_id,
                "gate_0_bootstrap",
                "source_packet",
                "pending",
                rel(packet / "source" / "songs.md", root),
                "Gate 1 source packet still needs shape review song source Suno fields visual source metadata and reviews",
            ],
            [
                config.prepared_date,
                config.episode_id,
                "gate_0_bootstrap",
                "release_gate",
                "blocked",
                rel(packet / "reviews" / "release-decision-plan.md", root),
                "Upload publish API browser schedule analytics Content ID and account actions remain blocked",
            ],
        ],
    )
    write_csv(
        packet / "tracking" / "assets.csv",
        ["date", "episode_id", "asset_type", "asset_id", "path", "status", "notes"],
        [
            [config.prepared_date, config.episode_id, "source_doc", "manifest", rel(packet / "manifest.json", root), "active", "Episode truth file scaffold"],
            [config.prepared_date, config.episode_id, "review_doc", "current_state", rel(packet / "reviews" / "current-state.md", root), "active", "Current source-only state scaffold"],
            [config.prepared_date, config.episode_id, "media", "candidate_media", "candidates/", "none", "No candidate media or IDs exist"],
        ],
    )
    write_csv(
        packet / "tracking" / "provenance.csv",
        ["date", "episode_id", "item_type", "item_id", "source_path", "provenance_status", "notes"],
        [
            [config.prepared_date, config.episode_id, "planning_hook", "season_week", "channel/roadmap.md", "source_internal", f"Seeded from roadmap concept: {config.working_longplay}"],
            [config.prepared_date, config.episode_id, "operating_boundary", "local_source_first", "docs/operating-boundary.md", "source_internal", "Only source packet work is allowed by this scaffold"],
        ],
    )
    write_csv(
        packet / "tracking" / "decisions.csv",
        ["date", "episode_id", "decision_id", "decision", "status", "source_path", "notes"],
        [
            [config.prepared_date, config.episode_id, "D000", f"Open Gate 0 scaffold for {config.working_longplay}", "scaffolded_source_only", rel(packet / "manifest.json", root), "No provider media render export upload public publish or rights/platform approval"],
        ],
    )
    return planned_paths(config, root)


def bootstrap_episode_packet(
    config: EpisodeBootstrapConfig,
    *,
    root: Path = PROJECT_ROOT,
    dry_run: bool = False,
) -> dict[str, object]:
    root = root.resolve()
    validate_config(config)
    paths = planned_paths(config, root)
    packet = root / "channel" / "episodes" / config.episode_id
    if packet.exists():
        raise FileExistsError(f"episode packet already exists: {rel(packet, root)}")
    if dry_run:
        return {
            "mode": "dry_run",
            "episode_id": config.episode_id,
            "planned_files": [rel(path, root) for path in paths],
            "creates_candidate_media": False,
            "opens_external_gate": False,
        }
    written = write_packet(config, root)
    return {
        "mode": "write",
        "episode_id": config.episode_id,
        "planned_files": [rel(path, root) for path in paths],
        "written_files": [rel(path, root) for path in written],
        "creates_candidate_media": False,
        "opens_external_gate": False,
    }


def config_from_args(args: argparse.Namespace) -> EpisodeBootstrapConfig:
    values = dict(S01E02_DEFAULTS) if args.s01e02 else {}
    for key in ["episode_id", "working_longplay", "hook", "lyric_lane"]:
        supplied = getattr(args, key)
        if supplied:
            values[key] = supplied
    missing = [key for key in ["episode_id", "working_longplay", "hook", "lyric_lane"] if not values.get(key)]
    if missing:
        raise ValueError(f"missing required args: {', '.join('--' + key.replace('_', '-') for key in missing)}")
    return EpisodeBootstrapConfig(
        episode_id=values["episode_id"],
        working_longplay=values["working_longplay"],
        hook=values["hook"],
        lyric_lane=values["lyric_lane"],
        prepared_by=args.prepared_by,
        prepared_date=args.prepared_date,
        season=args.season,
        week=args.week,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--s01e02", action="store_true", help="Use the Season 1 Week 2 roadmap seed")
    parser.add_argument("--episode-id", help="Episode slug, e.g. s01e02-classroom-window-longplay")
    parser.add_argument("--working-longplay", help="Working longplay title")
    parser.add_argument("--hook", help="Roadmap/location-time hook")
    parser.add_argument("--lyric-lane", help="Lyric lane summary")
    parser.add_argument("--prepared-by", default="Mayr")
    parser.add_argument("--prepared-date", default=date.today().isoformat())
    parser.add_argument("--season", type=int, default=1)
    parser.add_argument("--week", type=int, default=2)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    config = config_from_args(args)
    summary = bootstrap_episode_packet(config, dry_run=args.dry_run)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

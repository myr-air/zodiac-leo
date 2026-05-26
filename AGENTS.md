# Mellow Longplay Agent Notes

Scope: this file applies to `/Users/xiivth/workspaces/mellow-longplay/`.

## Purpose

This project is a single-channel, source-first operating system for `Mellow Longplay`. It exists to keep one cozy chill vocal longplay channel organized without carrying the old multi-channel YouTube AI Music scope.

## Required Reads

- Read `KNOWLEDGE.md` before project work.
- Use `channel/episodes/*/manifest.json` as episode truth.
- Use `channel/episodes/*/reviews/current-state.md` before changing an episode state.
- Use `channel/episodes/*/tracking/*.csv` for durable provenance, assets, decisions, and status.
- Use `.agents/skills/suno-song-production-guardrails/SKILL.md` before song, lyric, Suno field, prompt pack, or manual-generation handoff work.
- Use `.agents/skills/lyric-craft-multilingual-guardrails/SKILL.md` before lyric craft, multilingual, or subtitle-ready lyric work.
- Use `.agents/skills/gpt-image-prompting-guardrails/SKILL.md` before visual prompt, still-frame prompt, thumbnail/background prompt, or image-generation planning work.
- Use `.agents/skills/episode-state-gatekeeper/SKILL.md` before changing episode status, accepted preview direction, render/export planning, or tracking sync.

## Source Of Truth

- Channel strategy: `channel/channel.md` and `channel/roadmap.md`.
- Episode packet: `channel/episodes/<episode-id>/`.
- Song source: `source/songs.md`.
- Visual source: `source/visual.md` plus `reviews/visual.md`.
- Metadata source: `source/metadata.md`.
- Subtitle source and sidecars: `subtitles/`.
- Durable tracking: `tracking/status.csv`, `tracking/provenance.csv`, `tracking/assets.csv`, `tracking/decisions.csv`.

## Verification

- Validate changed JSON with `bash scripts/dev-python.sh -m json.tool <file>` or the standalone verifier.
- Parse changed CSVs with the standalone verifier.
- Run `bash scripts/dev-python.sh -m py_compile <script>` after Python script changes.
- Run Python/tests through `bash scripts/dev-python.sh ...` or `bash scripts/run-tests.sh` after script/test changes; these route through `uv`. Avoid `rtk pytest`, bare `pytest`, bare `python3 -m pytest`, and bare `/usr/bin/python3` because this workspace has multiple Python installs.
- Run `bash scripts/verify-standalone.sh` after structural, manifest, tracking, agent, skill, or source-of-truth changes.

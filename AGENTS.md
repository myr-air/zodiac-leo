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

## Current Boundary

- Do not automate Suno, YouTube, browsers, providers, APIs, OAuth, uploads, publishing, scheduling, analytics, or external accounts.
- Do not create OAuth tokens, browser profiles, cookies, credentials, API keys, or account-state files.
- Do not generate or fetch images, audio, video, renders, exports, candidate media, screenshots, or provider output unless a future explicit gate approves that exact local step.
- Do not represent AI-generated or Suno-assisted music as human-recorded, exclusive, copyright-free, royalty-free, Content ID-safe, monetization-safe, platform-safe, upload-ready, or publish-ready.
- Candidate media remains ignored by default; durable facts belong in episode tracking CSVs and review docs.

## Source Of Truth

- Channel strategy: `channel/channel.md` and `channel/roadmap.md`.
- Episode packet: `channel/episodes/<episode-id>/`.
- Song source: `source/songs.md`.
- Visual source: `source/visual.md` plus `reviews/visual.md`.
- Metadata source: `source/metadata.md`.
- Subtitle source and sidecars: `subtitles/`.
- Durable tracking: `tracking/status.csv`, `tracking/provenance.csv`, `tracking/assets.csv`, `tracking/decisions.csv`.

## Verification

- Validate changed JSON with `python3 -m json.tool <file>` or the standalone verifier.
- Parse changed CSVs with the standalone verifier.
- Run `python3 -m py_compile <script>` after Python script changes.
- Run relevant tests after script/test changes.
- Run `bash scripts/verify-standalone.sh` after structural, manifest, tracking, agent, skill, or source-of-truth changes.

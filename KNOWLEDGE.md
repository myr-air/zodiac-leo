# Mellow Longplay Knowledge Contract

Status: active  
Updated: 2026-05-18

## Purpose

`/Users/xiivth/workspaces/mellow-longplay/` is the reduced standalone project for one channel: `Mellow Longplay`. The old multi-lane `youtube-ai-music` scope is intentionally not preserved here.

## Active Episode

- `s01e01-campus-cafe-longplay` — Season 1 Week 1 `Campus Cafe Longplay`.
- Status: Gate 1 source packet open; tracks 1-13 have revised source-only lyric drafts; source-only Suno manual fields, prompt/control pack, visual prompt pack, and future candidate-intake checklist exist; metadata source, review gates, and tracking CSVs exist.
- No audio, image, video, render/export, subtitle timing, candidate media, upload plan, release approval, analytics, or platform/account action exists.

## Current Source Truth

- Channel strategy: `channel/channel.md` and `channel/roadmap.md`.
- Reusable templates: `channel/templates/`.
- Signature visual system: `channel/signature-visual-system.md` records source-only channel motifs with stored local reference images in `channel/signature-references/`.
- Active episode truth: `channel/episodes/s01e01-campus-cafe-longplay/manifest.json`.
- Active song source: `channel/episodes/s01e01-campus-cafe-longplay/source/songs.md`.
- Active Suno manual fields: `channel/episodes/s01e01-campus-cafe-longplay/source/suno-manual-fields.md` plus `channel/episodes/s01e01-campus-cafe-longplay/reviews/suno-manual-fields.md`.
- Active prompt pack: `channel/episodes/s01e01-campus-cafe-longplay/source/prompt-pack.md` plus `channel/episodes/s01e01-campus-cafe-longplay/reviews/prompt-pack.md`.
- Active candidate-intake checklist: `channel/episodes/s01e01-campus-cafe-longplay/reviews/candidate-intake-checklist.md`.
- Active lyrics review: `channel/episodes/s01e01-campus-cafe-longplay/reviews/lyrics.md`.
- Active visual source: `channel/episodes/s01e01-campus-cafe-longplay/source/visual.md` and `channel/episodes/s01e01-campus-cafe-longplay/source/visual-prompt-pack.md` plus visual reviews.
- Active metadata source: `channel/episodes/s01e01-campus-cafe-longplay/source/metadata.md`.
- Active tracking: `channel/episodes/s01e01-campus-cafe-longplay/tracking/*.csv`.

## Current Decisions

- The first episode direction is `Campus Cafe Longplay`: sunlit cafe table, notebook, coffee, and young-adult first-crush details.
- Baseline format is 12 main songs plus 1 bonus full closing song, English-first, target about 30-35 minutes if later generated naturally.
- Controlled variation is limited to one piano-forward song and one soft sax accent song unless re-reviewed.
- Tracks 1-13 passed a revised source-only full lyric arc/repetition checkpoint at 92/100; user-approved Gemini CLI review is complete and recommended revisions have been applied in source.
- Source-only Suno manual fields are prepared for future user copy reference; they are not provider approval or media approval.
- Source-only prompt/control pack passed review; it is not provider approval or media approval.
- Source-only candidate-intake checklist is prepared for a future separate manual gate; it does not create candidate IDs or approve provider/media/release actions.
- Source-only visual prompt pack is prepared; it is not image generation approval or visual candidate acceptance.
- No current audio candidates, visual candidates, render evidence, subtitle sidecars, readiness gate, or release gate are active.
- Upload/public-publish planning, render/export, provider/account/API/browser automation, Content ID registration, and rights/platform-safety claims remain blocked.
- Future visual prompts may reuse the channel-level signature motifs only as source-only design guidance unless a later explicit visual gate overrides that rule.

## Safety

- Candidate media under `candidates/` is ignored local evidence and should only be added after a fresh episode packet exists.
- Do not invent candidate IDs, provenance, generation dates, analytics, media existence, or release facts.
- Use forbidden terms such as `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `upload-ready`, and `publish-ready` only as blocked/caution language.
- Before any future external platform work, require a separate explicit gate and current policy/account review.

## Verification

Run:

```bash
bash scripts/verify-standalone.sh
python3 -m pytest tests
```

# Mellow Longplay Knowledge Contract

Status: active  
Updated: 2026-05-18

## Purpose

`/Users/xiivth/workspaces/mellow-longplay/` is the reduced standalone project for one channel: `Mellow Longplay`. The old multi-lane `youtube-ai-music` scope is intentionally not preserved here.

## Active Episode

- None.
- The previous episode packet and its candidate drop zones were permanently removed from this workspace at user direction on 2026-05-18.
- The next workflow should start cleanly from a new episode packet, new tracking, and new review gates.

## Current Source Truth

- Channel strategy: `mellow-longplay/channel.md` and `mellow-longplay/roadmap.md`.
- Reusable templates: `mellow-longplay/templates/`.
- Signature visual system: `mellow-longplay/signature-visual-system.md` records source-only channel motifs with stored local reference images in `mellow-longplay/signature-references/`.
- There is currently no active episode manifest, song source, visual source, metadata source, subtitle sidecar, or episode tracking CSV.

## Current Decisions

- No current audio candidates, visual candidates, render evidence, subtitle sidecars, readiness gate, or release gate are active.
- New episode work must begin with source planning, then create a fresh episode packet and tracking files before any media candidate review.
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

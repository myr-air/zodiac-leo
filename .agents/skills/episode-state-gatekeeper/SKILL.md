---
name: episode-state-gatekeeper
description: Use this project-local safety skill before changing Mellow Longplay episode status, accepted preview direction, render/export planning, manifest/review/tracking sync, or release-gate decisions. It prevents stale source truth, preview approval being confused with release approval, and unsafe rights/platform claims.
---

# Episode State Gatekeeper

Use this skill before changing any durable episode state in `/Users/xiivth/workspaces/mellow-longplay`.

## Read First

- `AGENTS.md`
- `KNOWLEDGE.md`
- The episode `manifest.json`
- `reviews/current-state.md`
- Relevant `tracking/*.csv`
- Relevant review/source files for the area being changed

## Rules

- Confirm current state from tracking and current-state docs, not memory.
- Preview-direction approval is not render/export approval.
- Internal readiness is not upload/public-publish approval.
- Generated media and candidate files are evidence only until review/tracking records say otherwise.
- Do not create candidate/provenance facts before real files exist.
- Do not make positive rights/platform/upload/publish claims.

## Required Sync

When durable state changes, update the relevant subset together:

- `manifest.json`
- `reviews/current-state.md`
- Area review file in `reviews/`
- Relevant `tracking/*.csv`
- `KNOWLEDGE.md` if the project-level summary changes

## Verification

Run the smallest relevant checks, then `bash scripts/verify-standalone.sh` after structural, manifest, tracking, agent, skill, or state changes.

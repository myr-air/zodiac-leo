# S01E05-APARTMENT-WINDOW-LONGPLAY Release Decision Plan — Apartment Window Longplay

Status: public visibility + top-level comment posted, policy checks pending / route evidence ready
Episode: `s01e05-apartment-window-longplay`
Prepared: 2026-06-11

## 0. Boundary

This file now moves from placeholder to the release planning gate. It does not approve public publishing, upload-execution itself, scheduling, analytics, provider/browser/account actions, credentials or tokens stored in repo, Content ID action, positive rights/platform claims, or account-side rollback actions.

Public publish execution is complete (video observed as public). Policy/account checks and rollback-owner governance remain pending for final rollout confirmation.

## 1. Required Evidence Before This Gate Can Open

| Area | Required evidence | Current state |
|---|---|---|
| Final local asset selection | exact final MP4/render output and sidecars after QA | pass (render + promoted source sidecars + timeline checks complete) |
| Metadata/disclosure | title, description, chapters, tags, AI-assisted disclosure, English post-upload comment draft | pass (source draft locked in `source/metadata.md`) |
| Current policy/account check | official current public platform policy and user-owned account constraints | pending / user-owned |
| Provenance/risk acceptance | non-secret source provenance and known limitations | pass (source-only tracking and episode review trail exists) |
| Upload route | manual Studio handoff or guarded private API path, selected explicitly | pass (private API packets in source/... with evidence recorded) |
| Rollback owner | user owns privacy changes, delete/unlist, edits, comments/pinning, analytics | pending explicit user confirmation |

## 2. Current Verdict

```text
Verdict: manual_public_release_completed_pending_governance
Scope: private API route and follow-up visibility update executed for video upload + thumbnail; local QC-complete subtitle/track alignment remains the creative gate source
Current assets: final MP4 render-01 (`199e1e7d4eb56a`) + source `.srt/.vtt` + public YouTube asset `ShWN-wK-ZNY` (thumbnail uploaded) + top-level comment `UgyS7hWhDBqla58T9214AaABAg` posted (latest)
Pending for final rollout governance: policy/account checks and explicit user confirmation of rollback/visibility controls
Still blocked: schedule/account-side actions, captions, playlists, analytics, Content ID, account edits, credentials/account-state storage in repo, and rights/platform-safety claims
```

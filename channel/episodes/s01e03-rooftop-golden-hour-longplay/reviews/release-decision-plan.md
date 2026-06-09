# S01E03-ROOFTOP-GOLDEN-HOUR-LONGPLAY Release Decision Plan — Rooftop Golden Hour Longplay

Status: S01E03 public state observed / pin pending manual
Episode: `s01e03-rooftop-golden-hour-longplay`
Prepared: 2026-05-30

## 0. Boundary

This file records the S01E03 release decision plan. Outputs are ignored local QA evidence under `candidates/`. The user approved the exact render-02 candidate for upload on 2026-06-02, and that upload completed as video ID `2P6fPs7NB0E`; a later API check observed the video as `public` and `processed`. This does not approve scheduling, captions, playlists, analytics, provider/browser/account actions beyond the completed guarded API calls, credentials or tokens stored in repo, Content ID action, release readiness, or positive rights/platform claims.

Public publish/schedule and account-side operations remain blocked except for manual pin completion or other explicit account actions.

## 1. Release Scheduling Policy

> [!IMPORTANT]
> The user has instructed that video releases must be spaced out **3 to 4 days apart** to maintain healthy viewer pacing and engagement.
>
> * **S01E02 Release Date**: May 29-30, 2026
> * **S01E03 Scheduled Release Date**: **June 2 or June 3, 2026** (exactly 3 to 4 days after EP2)

When the S01E03 upload package is executed, the video will be uploaded as `private`. Public release will be scheduled or manually triggered on the target date.

## 2. Required Evidence Before This Gate Can Open

| Area | Required evidence | Current state |
|---|---|---|
| Final local asset selection | exact final MP4/render output and sidecars after QA | render-02 completed, mechanical QA passed |
| Metadata/disclosure | title, description, chapters, tags, AI-assisted disclosure, English post-upload comment draft | chapter timestamps compiled, description drafted |
| Current policy/account check | official current public platform policy and user-owned account constraints | pending / user-owned |
| Provenance/risk acceptance | non-secret source provenance and known limitations | documented in provenance.csv |
| Upload route | manual Studio handoff or guarded private API path, selected explicitly | API route executed; private video ID `2P6fPs7NB0E` |
| Rollback owner | user owns privacy changes, delete/unlist, edits, comments/pinning, analytics | user-owned |

## 3. Current Verdict

```text
Verdict: public_video_state_observed_pin_pending_manual
Scope: private API upload completed; scheduling policy remains locked to 3-4 days interval (June 2 or June 3, 2026 target)
Next allowed action: complete comment pinning on manual/browser path if still needed, then optionally record scheduling/account-side operations under a new explicit gate
Still blocked: schedule execution, visibility mutation, captions, playlists, analytics, Content ID, account edits, credentials/account-state storage in repo, and rights/platform-safety claims
```

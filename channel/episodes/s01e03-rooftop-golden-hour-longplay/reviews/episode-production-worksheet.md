# S01E03-ROOFTOP-GOLDEN-HOUR-LONGPLAY Production Worksheet — Rooftop Golden Hour Longplay

Status: Gate 6 private YouTube API upload completed / comment blocked / release blocked
Episode: `s01e03-rooftop-golden-hour-longplay`
Prepared by: Mayr
Prepared date: 2026-05-30
Source packet version: `v1.0-locked`

## 0. Boundary

This worksheet is an internal source-to-video checklist. It does not approve provider use, media generation, render/export, upload, publishing, Suno/YouTube/API/browser automation, account mutation, credential storage, Content ID registration, public release, or positive rights/platform-safety claims.

Fastlane rule: reuse approved channel-level defaults by citation; approve only episode deltas and real external/local actions.

## 1. Episode Delta Seed

| Field | Value |
|---|---|
| Working longplay | Rooftop Golden Hour Longplay |
| Roadmap hook | rooftop, warm sky, late-afternoon breeze |
| Lyric lane | wholesome teenage first-love confidence, golden-hour anticipation, mood-led looking ahead |
| Default format | 12 main songs + 1 bonus / English-first |
| Current gate | Gate 6 private YouTube API upload completed |

## 2. Build Path Status

| Step | Exit evidence | Status / notes |
|---:|---|---|
| 0. Scaffold | manifest, current state, source/review/tracking placeholders | pass_source_only |
| 1. Source packet lock | `source/songs.md`, `source/suno-manual-fields.md`, `source/suno-tracks/*.md`, reviews/tracking | pass |
| 2. Candidate intake | real local audio/visual files exist before IDs/provenance | pass |
| 3. Sequence + metadata | chapter timeline, upload-description timestamps, disclosure, title/description/tags policy, English post-upload comment draft | pass |
| 4. Subtitles + sidecars | final `.srt`/`.vtt`, parser checks, human watch/spot evidence | pass |
| 5. Local render QA | explicit render/export gate, video path, mechanical QA, human spot pass | render-02 complete, mechanical QA passed, snapshots compiled; user approved upload |
| 6. YouTube handoff planning | release decision, current public policy/account check, API/manual package | private API upload completed; comment API blocked |
| 7. Public publish decision | user-owned final action, rollback owner, no-store hygiene | blocked_until_explicit_final_gate |

Do not open the next step by implication. Each local media render/export or external platform/API action still needs its own explicit gate.

## 3. Current Verdict

```text
Verdict: gate_6_private_youtube_upload_completed_comment_blocked
Scope: local render-02 approved by user and uploaded as private YouTube video ID 2P6fPs7NB0E
Critical blockers: public publish/schedule, thumbnail upload, comment pinning, and broader account/platform actions remain blocked pending explicit gates
Next allowed action: decide/execute thumbnail upload, public release scheduling/manual publish, or manual/browser comment pinning under a new explicit gate
Still blocked: provider/account automation outside the opened gate, publish/schedule/visibility mutation, credentials in repo, Content ID, rights/platform-safety claims
```

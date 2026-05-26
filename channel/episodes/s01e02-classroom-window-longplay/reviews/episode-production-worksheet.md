# S01E02-CLASSROOM-WINDOW-LONGPLAY Production Worksheet — Classroom Window Longplay

Status: pre-final audio subtitle visual approved / final video approval pending / release blocked  
Episode: `s01e02-classroom-window-longplay`  
Prepared by: Mayr  
Prepared date: 2026-05-27  
Source packet version: `v0.7-pre-final-approvals-recorded`

## 0. Boundary

This worksheet is an internal source-to-video checklist. It does not approve provider use, media generation, additional render/export beyond render-01, upload, publishing, Suno/YouTube/API/browser automation, account mutation, credential storage, Content ID registration, public release, or positive rights/platform-safety claims.

Fastlane rule: reuse approved channel-level defaults by citation; approve only episode deltas and real external/local actions.

## 1. Episode Delta Seed

| Field | Value |
|---|---|
| Working longplay | Classroom Window Longplay |
| Roadmap hook | college classroom light, afternoon window |
| Lyric lane | curiosity, almost-said feelings, study-day warmth |
| Default format | 12 main songs + 1 bonus / English-first |
| Current gate | Gate 5 final video approval pending; release blocked |

## 2. Build Path Status

| Step | Exit evidence | Status / notes |
|---:|---|---|
| 0. Scaffold | manifest, current state, source/review/tracking placeholders | pass_source_only |
| 1. Source packet lock | `source/songs.md`, `source/suno-manual-fields.md`, `source/suno-tracks/*.md`, reviews/tracking | Tracks 1-13 lyrics/fields/prompt/visual/metadata/subtitle plan complete source-only |
| 2. Candidate intake | real local audio/visual files exist before IDs/provenance | selected c01 audio set user-approved source-only; c02 pool retained; vis-c01 agy PASS and user-approved source-only |
| 3. Sequence + metadata | chapter timeline, disclosure, title/description/tags policy | local render-01 timeline `39:45.96` and chapter draft recorded; public metadata still not final |
| 4. Subtitles + sidecars | subtitle files, parser checks, approval/spot evidence | current render subtitle lane user-approved source-only with 532 cues; transcript certification blocked |
| 5. Local render QA | explicit render/export gate, video path, mechanical QA, approval evidence | render-01 mechanical QA passed and agy visual/layout PASS; final video approval pending |
| 6. YouTube handoff planning | release decision, current public policy/account check, API/manual package | blocked_until_gate |
| 7. Public publish decision | user-owned final action, rollback owner, no-store hygiene | blocked_until_explicit_final_gate |

Do not open the next step by implication. Each local media render/export or external platform/API action still needs its own explicit gate.

## 3. Current Verdict

```text
Verdict: pre_final_audio_subtitle_visual_approved_final_video_approval_pending_release_blocked
Scope: source-only episode spine, Tracks 1-13 lyrics/Suno fields, synced prompt pack, approved visual direction, selected local audio/visual candidates, local timeline, current render subtitle lane, local render-01 mechanical QA, agy visual/layout review, and user-directed pre-final approvals
Evidence: manifest.json, reviews/current-state.md, source/songs.md, source/batch-draft-tracks-2-13.md, source/suno-manual-fields.md, source/prompt-pack.md, reviews/prompt-pack.md, source/visual.md, reviews/visual.md, reviews/visual-candidate-intake.md, source/metadata.md, reviews/metadata.md, subtitles/README.md, reviews/subtitles.md, reviews/lyrics.md, reviews/suno-manual-fields.md, reviews/source-shaping.md, tracking CSVs
Critical blockers: final video approval is pending; upload/public release remains blocked
Next allowed action: final video approval decision for render-01 or narrow issue-led local revision if needed
Still blocked: provider/account automation, reference-image input use, exact face/pose copying, additional render without new gate, upload/publish/API, credentials in repo, Content ID, transcript certification, rights/platform-safety claims
```

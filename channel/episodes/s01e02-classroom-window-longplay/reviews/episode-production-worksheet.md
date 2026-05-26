# S01E02-CLASSROOM-WINDOW-LONGPLAY Production Worksheet — Classroom Window Longplay

Status: Gate 1 source shaping complete / Tracks 1-13 source synced / prompt pack synced / visual source approved / metadata source passed / subtitle plan passed / source-only / no media or release gate  
Episode: `s01e02-classroom-window-longplay`  
Prepared by: Mayr  
Prepared date: 2026-05-26  
Source packet version: `v0.5-source-shaping-subtitle-plan-closure`

## 0. Boundary

This worksheet is an internal source-to-video checklist. It does not approve provider use, media generation, render/export, upload, publishing, Suno/YouTube/API/browser automation, account mutation, credential storage, Content ID registration, public release, or positive rights/platform-safety claims.

Fastlane rule: reuse approved channel-level defaults by citation; approve only episode deltas and real external/local actions.

## 1. Episode Delta Seed

| Field | Value |
|---|---|
| Working longplay | Classroom Window Longplay |
| Roadmap hook | college classroom light, afternoon window |
| Lyric lane | curiosity, almost-said feelings, study-day warmth |
| Default format | 12 main songs + 1 bonus / English-first |
| Current gate | Gate 1 source shaping open; Gate 1 not locked |

## 2. Build Path Status

| Step | Exit evidence | Status / notes |
|---:|---|---|
| 0. Scaffold | manifest, current state, source/review/tracking placeholders | pass_source_only |
| 1. Source packet lock | `source/songs.md`, `source/suno-manual-fields.md`, `source/suno-tracks/*.md`, reviews/tracking | Tracks 1-13 lyrics are source-approved, Tracks 1-13 source-only copy packs are field-synced, the prompt pack is synced, the visual direction is approved source-only, metadata/disclosure is passed source-only, and subtitle planning is passed source-only; Gate 1 still not locked because local audio intake and later gates remain pending |
| 2. Candidate intake | real local audio/visual files exist before IDs/provenance | blocked_until_gate |
| 3. Sequence + metadata | chapter timeline, disclosure, title/description/tags policy | metadata_pass_source_only; chapter timestamps blocked until selected audio sequence exists |
| 4. Subtitles + sidecars | final `.srt`/`.vtt`, parser checks, human watch/spot evidence | subtitle_plan_pass_source_only_no_sidecars; timing and sidecars blocked until selected audio and explicit timing gate |
| 5. Local render QA | explicit render/export gate, video path, mechanical QA, human spot pass | blocked_until_gate |
| 6. YouTube handoff planning | release decision, current public policy/account check, API/manual package | blocked_until_gate |
| 7. Public publish decision | user-owned final action, rollback owner, no-store hygiene | blocked_until_explicit_final_gate |

Do not open the next step by implication. Each local media render/export or external platform/API action still needs its own explicit gate.

## 3. Current Verdict

```text
Verdict: gate_1_source_shaping_complete_tracks_1_13_visual_metadata_subtitle_plan_not_locked
Scope: source-only episode spine, Tracks 1-13 lyrics/Suno fields, synced prompt pack, approved visual direction, source-only metadata/disclosure pack, source-only subtitle plan, and Gate 1 shaping closure
Evidence: manifest.json, reviews/current-state.md, source/songs.md, source/batch-draft-tracks-2-13.md, source/suno-manual-fields.md, source/prompt-pack.md, reviews/prompt-pack.md, source/visual.md, reviews/visual.md, source/metadata.md, reviews/metadata.md, subtitles/README.md, reviews/subtitles.md, reviews/lyrics.md, reviews/suno-manual-fields.md, reviews/source-shaping.md, tracking CSVs
Critical blockers: Gate 1 still lacks local audio candidates and all downstream media/platform evidence; no local candidate media; subtitle timings and sidecars are blocked; render/export and YouTube actions blocked; chapter timestamps are blocked until selected audio sequence exists
Next allowed action: stop for explicit local audio candidate intake or another narrow source review gate without opening provider/media/render/upload gates by implication
Still blocked: provider/account automation, media generation without gate, subtitle timing/sidecars without selected audio, render/export without gate, upload/publish/API without gate, credentials in repo, Content ID, transcript certification, rights/platform-safety claims
```

# S01E04-BOOKSTORE-AFTERNOON-LONGPLAY Production Worksheet — Bookstore Afternoon Longplay

Status: Gate 3 render package opened / source-only
Episode: `s01e04-bookstore-afternoon-longplay`
Prepared by: Mayr
Prepared date: 2026-06-07
Source packet version: `v1.0-source-lock-source-only`

## 0. Boundary

This worksheet is an internal source-to-video checklist. It does not approve provider use, media generation, render/export, upload, publishing, Suno/YouTube/API/browser/account actions, credentials storage, Content ID registration, public publish, scheduling, analytics, or rights/platform-safety claims.

Fastlane rule: reuse approved channel-level defaults by citation; approve only episode deltas and real external/local actions.

## 1. Episode Delta Seed

| Field | Value |
|---|---|
| Working longplay | Bookstore Afternoon Longplay |
| Roadmap hook | quiet bookstore corner, paper texture |
| Lyric lane | teenage love, private thoughts, shy hope, calm reflection |
| Default format | 12 main songs + 1 bonus / English-first |
| Current gate | Gate 3 render package opened |

## 2. Build Path Status

| Step | Exit evidence | Status / notes |
|---:|---|---|
| 0. Scaffold | manifest, current state, source/review/tracking placeholders | pass_source_only |
| 1. Source packet lock | `source/songs.md`, `source/suno-manual-fields.md`, `source/suno-tracks/*.md`, `source/prompt-pack.md`, `source/visual.md`, `source/metadata.md` | pass_source_only |
| 2. Candidate intake | `reviews/audio-candidate-intake.md`, `reviews/visual-candidate-intake.md`, `audio/selected`, `audio/pool`, `visual/selected` | pass_source_only |
| 3. Sequence + metadata | chapter timeline, subtitle timing plan, disclosure, title/description/tags policy, English post-upload comment draft | pending |
| 4. Subtitles + sidecars | final `.srt`/`.vtt`, parser checks, human watch/spot evidence | pass_source_only |
| 5. Local render QA | explicit render/export gate, video path, mechanical QA, human spot pass | local_render_01_recut_after_track3_change |
| 6. YouTube handoff planning | release decision, current public policy/account check, API/manual package | private API packet prepared (route selected), execution pending user-owned policy/channel confirmation |
| 7. Public release decision | user-owned final action, rollback owner, no-store hygiene | blocked_until_explicit_final_gate |

Do not open the next step by implication. Each local media render/export or external platform/API action still needs its own explicit gate.



## 2.1 Core subtitle audit workflow (SRT promotion gate)
- After each draft track is re-run from song-source, run batch promotion only after per-track first-pass alignment acceptance.
- Canonical commands:
  - `python3 scripts/subtitle_alignment_pipeline.py align-song-source-track --track-number N --out-dir candidates/s01e04-bookstore-afternoon-longplay/subtitles/track-0N --prefix s01e04 --fast-mode --onset-evidence --no-render`
  - `python3 scripts/subtitle_alignment_pipeline.py promote-final-sidecars --episode-id s01e04-bookstore-afternoon-longplay --proof-root candidates/s01e04-bookstore-afternoon-longplay/subtitles --out-dir channel/episodes/s01e04-bookstore-afternoon-longplay/subtitles --proof-prefix s01e04 --prefix s01e04-bookstore-afternoon-longplay --tracks 1 2 3 4 5 6 7 8 9 10 11 12 13 --gap-seconds 1.0 --max-line-chars 37`
- Evidence target: [subtitles-audit-all-tracks.md](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/reviews/subtitles-audit-all-tracks.md)

## 3. Current Verdict

```text
Verdict: gate_3_ready_for_gate4_planning
Scope: source packet locked; full-track subtitle + local render-01 package finalized and promoted
Evidence: manifest.json, reviews/current-state.md, reviews/episode-production-worksheet.md, reviews/subtitles.md, reviews/release-precheck.md, reviews/audio-candidate-intake.md, reviews/visual-candidate-intake.md, source/songs.md, source/suno-manual-fields.md, source/suno-tracks/
Critical blockers: current platform policy/account validation, user-owned rollout confirmation, upload execution confirmation from approved route
Next allowed action: finalize policy/account checks, keep public publish blocked, then execute planned private API route if approved
Still blocked: provider/account automation, provider/media generation claims, render/export outside opened gate, upload/publish/API/browser actions, transcript certification, Content ID, rights/platform-safety claims

```

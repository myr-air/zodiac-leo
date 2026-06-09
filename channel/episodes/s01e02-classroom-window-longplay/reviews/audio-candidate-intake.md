# S01E02 Audio Candidate Intake — Classroom Window Longplay

Status: selected_c01_user_approved_source_only / render-02 subtitle-sync revision required / release blocked
Updated: 2026-05-27

## Boundary

This review records local user-supplied audio candidate intake for S01E02. Candidate WAV files remain ignored local evidence under `candidates/`. This does not approve provider/browser/API/account action, upload/publish, Content ID action, release readiness, transcript certification, or rights/platform-safety claims.

## Gate And Selection Rule

- User opened an unattended local build/run after placing image and audio files.
- Raw audio pattern matched two WAV variants per track under `candidates/s01e02-classroom-window-longplay/audio/`.
- Deterministic fallback was used overnight: filename without `(1)` became `c01` and was selected for the local draft render; filename with `(1)` became `c02` and was pooled.
- All selected files are stereo `48000 Hz` 16-bit WAV and were copied without altering source audio content.
- User later instructed that after agy check the selected audio/subtitle/visual gates should be treated as approved source-only. The earlier render-02 final-video approval is now superseded by a subtitle timing blocker; this is not an independent agy audio-quality proof or release approval.

## Selected Draft Set

| Track | Title | Selected ID | Duration | Selected path |
|---:|---|---|---:|---|
| 1 | Chalk Dust on the Window Rail | `aud-t01_c01` | `183.72s` | `candidates/s01e02-classroom-window-longplay/audio/selected/aud-t01_c01--chalk-dust-on-the-window-rail.wav` |
| 2 | Second Seat from the Sun | `aud-t02_c01` | `180.00s` | `candidates/s01e02-classroom-window-longplay/audio/selected/aud-t02_c01--second-seat-from-the-sun.wav` |
| 3 | Pencil Tap Before the Bell | `aud-t03_c01` | `152.40s` | `candidates/s01e02-classroom-window-longplay/audio/selected/aud-t03_c01--pencil-tap-before-the-bell.wav` |
| 4 | Folded Quiz at the Corner | `aud-t04_c01` | `177.60s` | `candidates/s01e02-classroom-window-longplay/audio/selected/aud-t04_c01--folded-quiz-at-the-corner.wav` |
| 5 | Library Stamp at 3:10 | `aud-t05_c01` | `199.92s` | `candidates/s01e02-classroom-window-longplay/audio/selected/aud-t05_c01--library-stamp-at-3-10.wav` |
| 6 | Study Room Reservation | `aud-t06_c01` | `171.68s` | `candidates/s01e02-classroom-window-longplay/audio/selected/aud-t06_c01--study-room-reservation.wav` |
| 7 | Highlighter Under Monday | `aud-t07_c01` | `189.60s` | `candidates/s01e02-classroom-window-longplay/audio/selected/aud-t07_c01--highlighter-under-monday.wav` |
| 8 | Campus Map Turned Sideways | `aud-t08_c01` | `169.92s` | `candidates/s01e02-classroom-window-longplay/audio/selected/aud-t08_c01--campus-map-turned-sideways.wav` |
| 9 | Notebook Margin, Left Blank | `aud-t09_c01` | `181.16s` | `candidates/s01e02-classroom-window-longplay/audio/selected/aud-t09_c01--notebook-margin-left-blank.wav` |
| 10 | Notice Pin by the Stairs | `aud-t10_c01` | `249.92s` | `candidates/s01e02-classroom-window-longplay/audio/selected/aud-t10_c01--notice-pin-by-the-stairs.wav` |
| 11 | Projector Cord Across the Floor | `aud-t11_c01` | `174.80s` | `candidates/s01e02-classroom-window-longplay/audio/selected/aud-t11_c01--projector-cord-across-the-floor.wav` |
| 12 | Last Slide Before Dismissal | `aud-t12_c01` | `188.40s` | `candidates/s01e02-classroom-window-longplay/audio/selected/aud-t12_c01--last-slide-before-dismissal.wav` |
| 13 | Window Latch After Class | `aud-t13_c01` | `154.84s` | `candidates/s01e02-classroom-window-longplay/audio/selected/aud-t13_c01--window-latch-after-class.wav` |

## Technical QA Summary

- Selected audio content duration: `2373.96s`.
- Assembly timeline with 12 x `1.00s` gaps: `2385.96s` / `39:45.96`.
- Selected WAV parameters: stereo, `48000 Hz`, 16-bit PCM.
- Peak levels observed across raw selected set ranged from about `-4.38 dBFS` to `-2.50 dBFS`; no zero-duration, missing, or wrong-format selected files were observed.

## Approval State

- Selected c01 set remains approved source-only for the current render-02 local QA evidence; final-video approval is blocked by subtitle sync.
- c02 pool remains available only if a later issue-led revision gate is opened.
- No upload, public release, transcript certification, Content ID, or rights/platform-safety claim is approved by this audio intake.

## Verdict

```text
Verdict: selected_c01_user_approved_source_only_render_02_subtitle_sync_revision_required_release_blocked
Scope: local user-supplied audio intake and deterministic c01 selected / c02 pool organization
Still blocked: final video approval, subtitle sung-lyric alignment pass, provider/account automation, upload/publish, transcript certification, Content ID, rights/platform-safety claims
```

# S01E01 Selected Audio QA / Listening Handoff

Status: selected_draft_human_listen_passed_needs_lyric_alignment_duration_source_only
Updated: 2026-05-19

## Boundary

This handoff prepares local listening and lyric-alignment QA for selected audio candidates. It does not approve render/export, upload/publish, Content ID action, rights/platform safety, or release readiness.

## Inputs

- Intake review: `reviews/audio-candidate-intake.md`
- Selected audio root: `candidates/s01e01-campus-cafe-longplay/audio/selected/`
- Pool audio root: `candidates/s01e01-campus-cafe-longplay/audio/pool/`
- Source lyrics: `source/songs.md`
- Prompt/style source: `source/suno-manual-fields.md` and `source/suno-tracks/*.md`

## Local Technical Summary

- Selected draft count: 13 WAV files.
- Selected draft duration: about `41:31`.
- All selected files observed as WAV PCM s16le, 48 kHz, stereo, 16-bit.
- Local peak check found no severe clipping; observed selected max peaks were roughly `-4.1 dB` to `-2.8 dB`.
- Technical blocker status: `none_observed_at_intake`. User human listening pass is recorded for all 13 selected candidates; lyric-alignment QA and duration/sequence decision remain required.

## Human Listening Result

- Date recorded: 2026-05-19
- Source: user verdict `all pass`, confirmed as human listening pass only.
- Scope: all 13 selected draft candidates.
- Not included in this verdict: lyric alignment spot-check, acceptance of the 41:31 duration, render/export readiness, upload/publish readiness, rights/platform safety, or release approval.

## Listening QA Checklist

For each selected candidate, listen for:

- correct title/track identity and no wrong-song mismatch;
- sung lyric follows `source/songs.md` enough for the episode story, with no harmful unsupported ad-libs;
- comfortable vocal, non-childlike, non-sexualized, same-age PG mood;
- no named-artist/known-song/real-person voice imitation concern;
- no harsh genre break, trap/aggressive rap/EDM drop/hard rock, or bombastic finale drift;
- no severe artifacts: clipping, garbled vocal, broken silence, timing collapse, repeated broken section;
- sequence fit and adjacent variation;
- duration/pacing fit for longplay use.

## Selected Draft Review Table

| Track | Candidate | Duration | Local technical status | Human listen | Lyric alignment | Notes / next action |
|---:|---|---:|---|---|---|---|
| 1 | `aud-t01_c02--margin-notes-at-table-three.wav` | 279.92s | pass_intake; long watch | pass | pending | Human listening passed; long opener still needs duration/sequence decision. |
| 2 | `aud-t02_c01--two-lids-one-tray.wav` | 225.00s | pass_intake | pass | pending | Human listening passed; lyric alignment pending. |
| 3 | `aud-t03_c01--borrowed-eraser-written-name.wav` | 204.12s | pass_intake | pass | pending | Human listening passed; lyric alignment pending. |
| 4 | `aud-t04_c01--checkout-slip-at-chapter-nine.wav` | 209.56s | pass_intake | pass | pending | Human listening passed; lyric alignment pending. |
| 5 | `aud-t05_c01--steam-on-the-glass-door.wav` | 218.40s | pass_intake | pass | pending | Human listening passed; lyric alignment pending. |
| 6 | `aud-t06_c02--peach-can-at-b4.wav` | 159.92s | pass_intake | pass | pending | Human listening passed; lyric alignment pending. |
| 7 | `aud-t07_c01--green-dot-on-your-schedule.wav` | 194.92s | pass_intake | pass | pending | Human listening passed; lyric alignment pending. |
| 8 | `aud-t08_c01--cushion-seat-charging-cord.wav` | 131.88s | pass_intake; short watch | pass | pending | Human listening passed; short duration still needs sequence decision. |
| 9 | `aud-t09_c01--crosswalk-stripes-before-six.wav` | 165.92s | pass_intake | pass | pending | Human listening passed; lyric alignment pending. |
| 10 | `aud-t10_c01--yellow-tag-on-the-umbrella-rack.wav` | 192.44s | pass_intake | pass | pending | Human listening passed; lyric alignment pending. |
| 11 | `aud-t11_c01--quiz-key-in-blue-ink.wav` | 159.88s | pass_intake | pass | pending | Human listening passed; lyric alignment pending. |
| 12 | `aud-t12_c01--tray-return-at-559.wav` | 199.32s | pass_intake | pass | pending | Human listening passed; lyric alignment pending. |
| 13 | `aud-t13_c01--latch-click-at-the-courtyard-gate.wav` | 150.00s | pass_intake | pass | pending | Human listening passed; bonus-close lyric alignment pending. |

## Sequence-Level Watchlist

- Selected draft is about `41:31`, longer than the earlier 30-35 minute baseline. Decide later whether to accept a longer first episode, swap shorter pool variants, regenerate long tracks, or trim in a future render/export gate.
- Track 1 is long at `279.92s`; Track 8 is short at `131.88s`.
- Human listening pass is recorded for all selected tracks, including local-technical-fallback tracks 1, 2, 3, 5, 10, and 12.
- Gemini-reviewed selections remain advisory background only; the recorded pass is the user human-listening verdict.

## Exit Criteria For This QA Step

Before any future render/export planning gate, all selected candidates need:

- human listen verdict: `pass | swap_pool | regenerate | reject` — complete: all 13 selected candidates pass;
- lyric alignment spot-check verdict;
- sequence duration decision;
- updated tracking/review docs with no unsupported platform/rights claims.

Still blocked: render/export, video assembly, subtitle timing, upload/publish, scheduling, analytics, Content ID action, rights/platform-safety claims, and release readiness.

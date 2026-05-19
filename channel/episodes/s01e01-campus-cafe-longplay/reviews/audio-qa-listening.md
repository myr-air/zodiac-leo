# S01E01 Selected Audio QA / Listening Handoff

Status: selected_draft_needs_human_listen_source_only
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
- Technical blocker status: `none_observed_at_intake`, but human listening and lyric-alignment QA remain required.

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
| 1 | `aud-t01_c02--margin-notes-at-table-three.wav` | 279.92s | pass_intake; long watch | pending | pending | Long opener; confirm it does not drag. |
| 2 | `aud-t02_c01--two-lids-one-tray.wav` | 225.00s | pass_intake | pending | pending | Confirm hook repetition feels intentional. |
| 3 | `aud-t03_c01--borrowed-eraser-written-name.wav` | 204.12s | pass_intake | pending | pending | Compare with pool if vocal tone feels less cozy. |
| 4 | `aud-t04_c01--checkout-slip-at-chapter-nine.wav` | 209.56s | pass_intake | pending | pending | Confirm piano-forward lane remains restrained. |
| 5 | `aud-t05_c01--steam-on-the-glass-door.wav` | 218.40s | pass_intake | pending | pending | Confirm title absence from lyric still feels earned. |
| 6 | `aud-t06_c02--peach-can-at-b4.wav` | 159.92s | pass_intake | pending | pending | Confirm vending-machine scene is clear despite shorter duration. |
| 7 | `aud-t07_c01--green-dot-on-your-schedule.wav` | 194.92s | pass_intake | pending | pending | Gemini flagged pool timing weakness; verify selected timing. |
| 8 | `aud-t08_c01--cushion-seat-charging-cord.wav` | 131.88s | pass_intake; short watch | pending | pending | Very short; consider pool/regeneration if it feels incomplete. |
| 9 | `aud-t09_c01--crosswalk-stripes-before-six.wav` | 165.92s | pass_intake | pending | pending | Confirm sax stays secondary and not sax-led. |
| 10 | `aud-t10_c01--yellow-tag-on-the-umbrella-rack.wav` | 192.44s | pass_intake | pending | pending | Confirm promise/understatement blockers did not return. |
| 11 | `aud-t11_c01--quiz-key-in-blue-ink.wav` | 159.88s | pass_intake | pending | pending | Confirm near-whisper section is intelligible. |
| 12 | `aud-t12_c01--tray-return-at-559.wav` | 199.32s | pass_intake | pending | pending | Confirm main-set close feels calm, not finale-bombastic. |
| 13 | `aud-t13_c01--latch-click-at-the-courtyard-gate.wav` | 150.00s | pass_intake | pending | pending | Confirm bonus close feels complete and not too abrupt. |

## Sequence-Level Watchlist

- Selected draft is about `41:31`, longer than the earlier 30-35 minute baseline. Decide later whether to accept a longer first episode, swap shorter pool variants, regenerate long tracks, or trim in a future render/export gate.
- Track 1 is long at `279.92s`; Track 8 is short at `131.88s`.
- Tracks selected by local technical fallback need especially careful human listening: 1, 2, 3, 5, 10, 12.
- Gemini-reviewed selected tracks are still advisory only and need human listening.

## Exit Criteria For This QA Step

Before any future render/export planning gate, all selected candidates need:

- human listen verdict: `pass | swap_pool | regenerate | reject`;
- lyric alignment spot-check verdict;
- sequence duration decision;
- updated tracking/review docs with no unsupported platform/rights claims.

Still blocked: render/export, video assembly, subtitle timing, upload/publish, scheduling, analytics, Content ID action, rights/platform-safety claims, and release readiness.

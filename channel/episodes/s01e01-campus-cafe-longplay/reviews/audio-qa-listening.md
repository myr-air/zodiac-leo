# S01E01 Selected Audio QA / Listening Handoff

Status: selected_draft_human_listen_lyric_anchor_duration_accepted_source_only
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
- Technical blocker status: `none_observed_at_intake`. User human listening pass, Gemini supplemental lyric anchor spot-check pass, and 41:31 duration/sequence acceptance are recorded for all 13 selected candidates.

## Human Listening Result

- Date recorded: 2026-05-19
- Source: user verdict `all pass`, confirmed as human listening pass only.
- Scope: all 13 selected draft candidates.
- Not included in this verdict: lyric alignment spot-check, render/export readiness, upload/publish readiness, rights/platform safety, or release approval.

## Lyric Alignment Spot-Check Result

- Date recorded: 2026-05-19
- Method: Gemini CLI supplemental audio anchor spot-check using temporary non-repo-stored preview clips and compact source-lyric anchors from `source/songs.md`.
- Model used: `gemini-3.1-flash-lite-preview` after `gemini-3-flash-preview` returned blank/timeout on longer prompts.
- Result: all 13 selected candidates received lyric anchor spot-check pass at track level; no wrong-song or harmful major lyric mismatch was observed in the recorded spot-check.
- Caveat: Track 13 opening/dialogue clip was inconclusive, but mid-verse and end/closing anchors passed. This is a spot-check, not a full word-for-word transcript verification.
- Not included: duration acceptance, render/export readiness, upload/publish readiness, rights/platform safety, or release approval.

## Duration / Sequence Decision

- Date recorded: 2026-05-19
- Decision: accept the selected draft duration of about `41:31` for S01E01 source-only.
- Basis: user accepted `41:31` after Mayr's market-length research recommendation that 40-45 minutes is a reasonable first-episode balance for a cozy chill vocal longplay.
- This supersedes the earlier 30-35 minute baseline for S01E01 only; future episodes may still target 40-45 minutes or be retested with analytics.
- Not included: render/export readiness, upload/publish readiness, rights/platform safety, or release approval.

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
| 1 | `aud-t01_c02--margin-notes-at-table-three.wav` | 279.92s | pass_intake; long watch | pass | pass_anchor_spot_check | Human listening and lyric anchors passed; long opener accepted within 41:31 source-only duration. |
| 2 | `aud-t02_c01--two-lids-one-tray.wav` | 225.00s | pass_intake | pass | pass_anchor_spot_check | Human listening and lyric anchors passed. |
| 3 | `aud-t03_c01--borrowed-eraser-written-name.wav` | 204.12s | pass_intake | pass | pass_anchor_spot_check | Human listening and lyric anchors passed. |
| 4 | `aud-t04_c01--checkout-slip-at-chapter-nine.wav` | 209.56s | pass_intake | pass | pass_anchor_spot_check | Human listening and lyric anchors passed. |
| 5 | `aud-t05_c01--steam-on-the-glass-door.wav` | 218.40s | pass_intake | pass | pass_anchor_spot_check | Human listening and lyric anchors passed. |
| 6 | `aud-t06_c02--peach-can-at-b4.wav` | 159.92s | pass_intake | pass | pass_anchor_spot_check | Human listening and lyric anchors passed. |
| 7 | `aud-t07_c01--green-dot-on-your-schedule.wav` | 194.92s | pass_intake | pass | pass_anchor_spot_check | Human listening and lyric anchors passed. |
| 8 | `aud-t08_c01--cushion-seat-charging-cord.wav` | 131.88s | pass_intake; short watch | pass | pass_anchor_spot_check | Human listening and lyric anchors passed; short track accepted within 41:31 source-only sequence. |
| 9 | `aud-t09_c01--crosswalk-stripes-before-six.wav` | 165.92s | pass_intake | pass | pass_anchor_spot_check | Human listening and lyric anchors passed. |
| 10 | `aud-t10_c01--yellow-tag-on-the-umbrella-rack.wav` | 192.44s | pass_intake | pass | pass_anchor_spot_check | Human listening and lyric anchors passed. |
| 11 | `aud-t11_c01--quiz-key-in-blue-ink.wav` | 159.88s | pass_intake | pass | pass_anchor_spot_check | Human listening and lyric anchors passed. |
| 12 | `aud-t12_c01--tray-return-at-559.wav` | 199.32s | pass_intake | pass | pass_anchor_spot_check | Human listening and lyric anchors passed. |
| 13 | `aud-t13_c01--latch-click-at-the-courtyard-gate.wav` | 150.00s | pass_intake | pass | pass_anchor_spot_check_with_opening_caveat | Human listening passed; mid/end lyric anchors passed; opening dialogue clip inconclusive. |

## Sequence-Level Watchlist

- Selected draft is about `41:31`, longer than the earlier 30-35 minute baseline, and is accepted for S01E01 source-only.
- Track 1 is long at `279.92s`; Track 8 is short at `131.88s`; both are accepted within the current source-only sequence.
- Human listening pass is recorded for all selected tracks, including local-technical-fallback tracks 1, 2, 3, 5, 10, and 12.
- Lyric anchor spot-check pass is recorded for all selected tracks; Track 13 has an opening-dialogue caveat.
- Gemini candidate-selection reviews and lyric anchor checks remain supplemental evidence only; the human-listening pass comes from the user verdict.

## Exit Criteria For This QA Step

Before any future render/export planning gate, all selected candidates need:

- human listen verdict: `pass | swap_pool | regenerate | reject` — complete: all 13 selected candidates pass;
- lyric alignment spot-check verdict — complete: all 13 selected candidates passed anchor spot-check, with Track 13 opening-dialogue caveat;
- sequence duration decision — complete: accept the selected draft at about `41:31` source-only;
- updated tracking/review docs with no unsupported platform/rights claims.

Still blocked: render/export, video assembly, subtitle timing, upload/publish, scheduling, analytics, Content ID action, rights/platform-safety claims, and release readiness.

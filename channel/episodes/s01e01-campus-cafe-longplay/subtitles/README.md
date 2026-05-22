# S01E01 Subtitles

Status: Tracks 1-12 draft timing evidence / Track 13 blocked / source-only / final sidecars blocked  
Episode: `s01e01-campus-cafe-longplay`

## Boundary

Final subtitle sidecars are still blocked until a later approved assembly package defines the exact subtitle target. Track 1 reviewed proof timing and the Gate 8 chapter plan are source-only evidence, not final `.srt`/`.vtt` sidecars. Do not invent timestamps, audio durations, or transcript text.

## Open Improvement Gate

User passed the V6 visual direction source-only, then opened subtitle improvement because the proof subtitles did not align closely enough with the sung vocal and some cues were too long. User passed the current Track 1 subtitle proof after human sung-lyric watch source-only. Tracks 2-12 now have no-render draft timing sidecars that require human watch pass. Track 13 alignment is blocked because local alignment did not cover all approved lyric lines.

## Draft Proofs

Local ignored evidence exists at `candidates/s01e01-campus-cafe-longplay/subtitles/proofs/`:

- `s01e01-track-01-subtitle-alignment-draft-01.json`
- `s01e01-track-01-subtitle-alignment-draft-01.draft.srt`
- `s01e01-track-01-subtitle-alignment-draft-01.draft.vtt`
- `s01e01-track-01-subtitle-alignment-draft-01.proof.ass`
- `s01e01-track-01-subtitle-alignment-draft-01.proof.mp4`
- Tracks 2-12: matching `.json`, `.draft.srt`, `.draft.vtt`, and `.proof.ass` sidecars in `track-02/` through `track-12/`; generated with `--no-render`, so no MP4 proof was created for these tracks.
- Track 13: incomplete accurate alignment in `track-13/` and incomplete fast-check alignment in `track-13-fast-check/`; both require human review before any promotion.

Track 1 mechanical checks pass for cue count, no overlap, 0.08s minimum gap, and 37-character maximum line length. Proof subtitles use proof-only `1.5s` fade/slide in, then `1.0s` fade-only out with no exit slide while keeping cue start/end timing unchanged. Cues 58-59 remain mechanically low-confidence evidence, but the user passed the human sung-lyric watch pass source-only. Tracks 2-12 pass line-count and no-overlap mechanical checks, but they still need human sung-lyric watch pass. Track 13 does not pass mechanical coverage and blocks Gate 10 pass.

## Track 2-13 Gate 10 Status

| Track | Draft status | Mechanical status | Watch status |
|---:|---|---|---|
| 1 | proof video + draft sidecars | pass; low-confidence cues retained | user watch-passed source-only |
| 2-12 | no-render draft sidecars | line-count match, no overlap, 0.08s min gap; low-confidence flags vary by track | needs human watch pass |
| 13 bonus | accurate and fast-check attempts generated | blocked; expected 40 lyric lines but accurate alignment returned 11 display cues and fast check returned 31 | needs human review/manual timing/swap/regeneration |

Allowed source-only work:

- Use the Track 1 reviewed proof timing as source-only reference for later final timeline planning.
- Use Tracks 2-12 draft timing sidecars as local review inputs only, not final sidecars.
- Resolve Track 13 alignment coverage before Gate 10 can pass.
- Preserve `vocal_start`/`vocal_end` evidence separately from display timing if timing is carried forward.
- Keep final sidecar creation blocked until a later approved assembly package defines the exact output target.

Still blocked:

- Final `.srt` or `.vtt` sidecars.
- Full video assembly, render/export, upload/publish, release readiness, platform/account actions, or rights/platform-safety claims.

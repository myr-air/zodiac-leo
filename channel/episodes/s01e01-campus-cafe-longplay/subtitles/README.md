# S01E01 Subtitles

Status: Track 1 proof human watch-passed / source-only / final sidecars blocked  
Episode: `s01e01-campus-cafe-longplay`

## Boundary

Final subtitle sidecars are still blocked until a later approved assembly package defines the exact subtitle target. Track 1 reviewed proof timing and the Gate 8 chapter plan are source-only evidence, not final `.srt`/`.vtt` sidecars. Do not invent timestamps, audio durations, or transcript text.

## Open Improvement Gate

User passed the V6 visual direction source-only, then opened subtitle improvement because the proof subtitles did not align closely enough with the sung vocal and some cues were too long. User passed the current Track 1 subtitle proof after human sung-lyric watch source-only.

## Track 1 Draft Proof

Local ignored evidence exists at `candidates/s01e01-campus-cafe-longplay/subtitles/proofs/track-01/`:

- `s01e01-track-01-subtitle-alignment-draft-01.json`
- `s01e01-track-01-subtitle-alignment-draft-01.draft.srt`
- `s01e01-track-01-subtitle-alignment-draft-01.draft.vtt`
- `s01e01-track-01-subtitle-alignment-draft-01.proof.ass`
- `s01e01-track-01-subtitle-alignment-draft-01.proof.mp4`

Mechanical checks pass for cue count, no overlap, 0.08s minimum gap, and 37-character maximum line length. Proof subtitles use proof-only `1.5s` fade/slide in, then `1.0s` fade-only out with no exit slide while keeping cue start/end timing unchanged. Cues 58-59 remain mechanically low-confidence evidence, but the user passed the human sung-lyric watch pass source-only.

Allowed source-only work:

- Use the Track 1 reviewed proof timing as source-only reference for later final timeline planning.
- Preserve `vocal_start`/`vocal_end` evidence separately from display timing if timing is carried forward.
- Keep final sidecar creation blocked until a later approved assembly package defines the exact output target.

Still blocked:

- Final `.srt` or `.vtt` sidecars.
- Full video assembly, render/export, upload/publish, release readiness, platform/account actions, or rights/platform-safety claims.

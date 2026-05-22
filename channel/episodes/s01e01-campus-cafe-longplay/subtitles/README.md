# S01E01 Subtitles

Status: Gate 10 subtitle/source timing plan passed / all tracks human-watch passed / assembly target defined / source-only / final sidecars blocked  
Episode: `s01e01-campus-cafe-longplay`

## Boundary

Final subtitle sidecars are still blocked until a later approved sidecar promotion gate. `reviews/assembly-package.md` now defines the exact planned subtitle target paths, but Track 1 reviewed proof timing, Tracks 2-13 watched draft timings, and the Gate 8 chapter plan remain source-only evidence, not final `.srt`/`.vtt` sidecars. Do not invent timestamps, audio durations, or transcript text.

## Gate 10 Human Watch Status

User passed the V6 visual direction source-only, then opened subtitle improvement because the proof subtitles did not align closely enough with the sung vocal and some cues were too long. User passed the current Track 1 subtitle proof after human sung-lyric watch source-only, then reported all remaining Tracks 2-13 PASS source-only. Tracks 1-13 now have human-watch-passed draft timing evidence, and the source-only assembly package defines final target paths, but final sidecar promotion still requires a later separate approval.

## Planned Final Sidecar Targets

Defined in `reviews/assembly-package.md`, not yet created:

```text
channel/episodes/s01e01-campus-cafe-longplay/subtitles/s01e01-campus-cafe-longplay.en.srt
channel/episodes/s01e01-campus-cafe-longplay/subtitles/s01e01-campus-cafe-longplay.en.vtt
```

Future promotion policy: shift the human-watch-passed track-local draft timings by the exact Gate 8 chapter starts, keep the 1-second gaps subtitle-empty, preserve Track 13 `Dialogue First` exclusion because that section is absent from the selected audio, and validate both sidecar files before treating them as final source sidecars.

## Draft Proofs

Local ignored evidence exists at `candidates/s01e01-campus-cafe-longplay/subtitles/proofs/`:

- `s01e01-track-01-subtitle-alignment-draft-01.json`
- `s01e01-track-01-subtitle-alignment-draft-01.draft.srt`
- `s01e01-track-01-subtitle-alignment-draft-01.draft.vtt`
- `s01e01-track-01-subtitle-alignment-draft-01.proof.ass`
- `s01e01-track-01-subtitle-alignment-draft-01.proof.mp4`
- Tracks 2-12: matching `.json`, `.draft.srt`, `.draft.vtt`, and `.proof.ass` sidecars in `track-02/` through `track-12/`; generated with `--no-render`, so no MP4 proof was created for these tracks.
- Track 13: complete sung-section draft sidecars in `track-13/` generated with `--exclude-sections "Dialogue First"`, because the selected audio begins at Verse 1 and does not contain the source dialogue section. Historical incomplete fast-check evidence remains in `track-13-fast-check/` as local evidence only.

Track 1 mechanical checks pass for cue count, no overlap, 0.08s minimum gap, and 37-character maximum line length. Proof subtitles use proof-only `1.5s` fade/slide in, then `1.0s` fade-only out with no exit slide while keeping cue start/end timing unchanged. Cues 58-59 remain mechanically low-confidence evidence, but the user passed the human sung-lyric watch pass source-only. Tracks 2-13 pass line-count and no-overlap mechanical checks, and the user reported all remaining draft timings PASS after human watch source-only.

## Track 2-13 Gate 10 Status

| Track | Draft status | Mechanical status | Watch status |
|---:|---|---|---|
| 1 | proof video + draft sidecars | pass; low-confidence cues retained | user watch-passed source-only |
| 2-12 | no-render draft sidecars | line-count match, no overlap, 0.08s min gap; low-confidence flags vary by track | user watch-passed source-only |
| 13 bonus | no-render sung-section draft sidecars; `Dialogue First` excluded because absent from selected audio | line-count match: 32 expected sung-section lines / 32 display cues, no overlap, 0.08s min gap | user watch-passed source-only |

Allowed source-only work:

- Use the Track 1 reviewed proof timing as source-only reference for later final timeline planning.
- Use Tracks 2-13 watched draft timing sidecars as local review inputs only, not final sidecars.
- Preserve `vocal_start`/`vocal_end` evidence separately from display timing if timing is carried forward.
- Keep final sidecar creation blocked until a later approved sidecar promotion gate uses the assembly package target.

Still blocked:

- Final `.srt` or `.vtt` sidecars.
- Full video assembly, render/export, upload/publish, release readiness, platform/account actions, or rights/platform-safety claims.

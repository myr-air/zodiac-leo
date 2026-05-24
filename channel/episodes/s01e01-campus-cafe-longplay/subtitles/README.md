# S01E01 Subtitles

Status: final English sidecars promoted / Track 1 cue 58 text corrected / source-only / render-export blocked  
Episode: `s01e01-campus-cafe-longplay`

## Boundary

Final English subtitle sidecars are promoted source-only from the human-watch-passed track-local draft timings and the Gate 8 chapter plan. They are not full assembly, render/export, upload/publish, release readiness, platform/account action, transcript certification, or rights/platform-safety approval. Do not invent timestamps, audio durations, or transcript text if a future sidecar revision is needed.

## Gate 10 Human Watch Status

User passed the V6 visual direction source-only, then opened subtitle improvement because the proof subtitles did not align closely enough with the sung vocal and some cues were too long. User passed the current Track 1 subtitle proof after human sung-lyric watch source-only, then reported all remaining Tracks 2-13 PASS source-only. Tracks 1-13 have human-watch-passed draft timing evidence, and the source-only sidecar promotion gate has produced the final source `.srt` and `.vtt` targets. On 2026-05-24, after render-04 review, the user identified a Track 1 late-song text mismatch; cue 58 at `00:04:10.280 --> 00:04:16.540` was corrected from `Save my seat and I'll walk you home` to `Same seat tomorrow after school` with timing unchanged.

## Promoted Final Sidecar Targets

Created source-only on 2026-05-22:

```text
channel/episodes/s01e01-campus-cafe-longplay/subtitles/s01e01-campus-cafe-longplay.en.srt
channel/episodes/s01e01-campus-cafe-longplay/subtitles/s01e01-campus-cafe-longplay.en.vtt
```

Promotion policy used: shifted the human-watch-passed track-local draft timings by the exact Gate 8 chapter starts, kept the 1-second gaps subtitle-empty, preserved Track 13 `Dialogue First` exclusion because that section is absent from the selected audio, and validated both sidecar files mechanically before recording them as final source sidecars.

Mechanical promotion summary:

- Cue count: 598 across 13 tracks.
- Planned timeline duration: `41:43.28`.
- Max line length: 37 chars.
- Checks passed: all cues remain inside track windows, inter-track gaps remain subtitle-empty, cue order has no overlaps, line length limit respected.

## Draft Proofs

Local ignored evidence exists at `candidates/s01e01-campus-cafe-longplay/subtitles/proofs/`:

- `s01e01-track-01-subtitle-alignment-draft-01.json`
- `s01e01-track-01-subtitle-alignment-draft-01.draft.srt`
- `s01e01-track-01-subtitle-alignment-draft-01.draft.vtt`
- `s01e01-track-01-subtitle-alignment-draft-01.proof.ass`
- `s01e01-track-01-subtitle-alignment-draft-01.proof.mp4`
- Tracks 2-12: matching `.json`, `.draft.srt`, `.draft.vtt`, and `.proof.ass` sidecars in `track-02/` through `track-12/`; generated with `--no-render`, so no MP4 proof was created for these tracks.
- Track 13: complete sung-section draft sidecars in `track-13/` generated with `--exclude-sections "Dialogue First"`, because the selected audio begins at Verse 1 and does not contain the source dialogue section. Historical incomplete fast-check evidence remains in `track-13-fast-check/` as local evidence only.

Track 1 mechanical checks pass for cue count, no overlap, 0.08s minimum gap, and 37-character maximum line length. Proof subtitles use proof-only `1.5s` fade/slide in, then `1.0s` fade-only out with no exit slide while keeping cue start/end timing unchanged. Cues 58-59 were mechanically low-confidence evidence; cue 58 text is now source-corrected per user-reported sung audio while preserving its timing. Tracks 2-13 pass line-count and no-overlap mechanical checks, and the user reported all remaining draft timings PASS after human watch source-only.

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
- Treat future sidecar edits or regeneration as a separate review/promotion gate.

Still blocked:

- Full video assembly, render/export, upload/publish, release readiness, platform/account actions, or rights/platform-safety claims.

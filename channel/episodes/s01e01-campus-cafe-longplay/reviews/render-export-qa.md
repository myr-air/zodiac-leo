# S01E01 Render/Export QA — After-School First Love Longplay

Status: local render/export mechanical QA recorded / release blocked  
Episode: `s01e01-campus-cafe-longplay`  
Updated: 2026-05-23

## 0. Boundary

This file records the one user-approved local render/export execution for S01E01. The outputs are ignored local QA evidence under `candidates/` only. This does not approve upload, publishing, scheduling, analytics, provider/API/browser/account actions, credentials, Content ID action, release readiness, or positive rights/platform claims.

Any additional or revised render/export output, sidecar revision, bumper media, thumbnail, upload package, public metadata package, or release decision requires a separate explicit future gate.

## 1. Current State

| Checkpoint | Status | Evidence |
|---|---|---|
| Execution gate | approved by user | User approved local render/export execution for S01E01 according to `reviews/render-export-plan.md`. |
| Render helper | completed | `scripts/render_s01e01_local.py`; local-only helper writes under ignored `candidates/`. |
| Local audio timeline | created | `candidates/s01e01-campus-cafe-longplay/render/future-local-render-01/audio/s01e01-campus-cafe-longplay.timeline-41m43s28.wav` |
| Local QA video | created | `candidates/s01e01-campus-cafe-longplay/render/future-local-render-01/video/s01e01-campus-cafe-longplay.v6-subtitled-1080p24-qa.mp4` |
| Copied sidecars in render folder | created | `candidates/s01e01-campus-cafe-longplay/render/future-local-render-01/subtitles/`; copies byte-match authoritative source sidecars. |
| Snapshot evidence | created | 7 PNG samples under `candidates/s01e01-campus-cafe-longplay/render/future-local-render-01/qa/snapshots/`. |
| Mechanical render QA | passed | Duration/format/sidecar/subtitle/snapshot assertions passed; video decode produced no ffmpeg errors. |
| Release/upload readiness | blocked | No release-decision gate exists; no platform/account action is approved. |

## 2. Output Inventory

| Output | Observed facts | QA status |
|---|---|---|
| WAV timeline | `480629804` bytes; PCM S16LE; stereo; `48000 Hz`; `120157440` frames; `2503.28s` / `41:43.28`. | pass mechanical |
| MP4 QA render | `321619448` bytes; H.264/AAC; `1920x1080`; `24/1 fps`; stereo AAC `48000 Hz`; `2503.28s`. | pass mechanical |
| SRT copy | `38599` bytes; byte-matches `subtitles/s01e01-campus-cafe-longplay.en.srt`. | pass mechanical |
| VTT copy | `36323` bytes; byte-matches `subtitles/s01e01-campus-cafe-longplay.en.vtt`. | pass mechanical |
| Snapshots | `s01e01-render-sample-01.png` through `s01e01-render-sample-06.png`, plus `s01e01-render-sample-07-track13-subtitle.png`; all 7 image reads succeeded. | pass sampled visual/readability check |

## 3. Timeline And Subtitle QA

| Check | Result |
|---|---|
| Track order | Tracks 1-13 rendered in Gate 8 order. |
| Gap policy | 12 x `1.00s` gaps; no crossfades; no bumper time. |
| Duration target | Target `2503.28s`; WAV and MP4 observed at `2503.28s`. |
| Final sidecar cue count | `598` SRT cues. |
| Max subtitle line length | `37` characters. |
| Subtitle overlap count | `0`. |
| Gap cue count | `0`. |
| Track 13 policy | `Dialogue First` remains excluded because selected audio begins at Verse 1; sampled Track 13 rendered subtitle starts at about `2366.08s` with `Courtyard trees drop brown leaves`. |
| Source sidecar authority | Episode `subtitles/` sidecars remain authoritative; render-folder copies are local QA copies only. |

## 4. Visual / Decode / Boundary QA

| Check | Result |
|---|---|
| Video decode | `ffmpeg -v error -i ... -f null -` completed with no errors. |
| Video target | `1920x1080`, `24fps` confirmed by probe. |
| Sampled visual readability | 7 snapshots opened successfully; sampled header/title/subtitle/equalizer layout carried V6 direction and no obvious crop/clipping was observed in those samples. |
| Candidate-media hygiene | Render outputs remain under ignored `candidates/` paths. |
| Boundary scan | No credentials, account state, provider artifacts, upload artifacts, Content ID action, or positive rights/platform claims were created by this gate. |

## 5. Remaining Stop Conditions

Do not mark release/public readiness unless a future gate closes these:

- full-length human watch/listen pass is still not recorded for the final QA MP4;
- final release decision and current platform/account policy review do not exist;
- any upload/publish/scheduling/API/browser/provider action remains blocked;
- readiness remains `96/100`; do not raise it without fresh final-output evidence and explicit score review;
- additional/revised render/export outputs, sidecar revisions, bumper media, thumbnails, or upload packages require a new explicit gate.

## 6. Current Verdict

```text
Verdict: pass_local_render_export_mechanical_qa_release_blocked
Scope: one approved local render/export QA output under ignored candidates/
Timeline: 13 selected tracks, 12 x 1.00s gaps, 41:43.28 / 2503.28s
Audio QA: WAV timeline created and duration/format verified
Video QA: 1080p24 H.264/AAC QA MP4 created, decoded, and sampled
Subtitle QA: final SRT/VTT copies byte-match source; 598 cues, no overlaps, no gap cues, max line length 37
Readiness score: remains 96/100
Still blocked: full human final-output watch/listen, release decision, upload/publish, provider/account/API/browser actions, Content ID registration, positive rights/platform claims, and additional/revised outputs without a new gate
```

# S01E01 Render/Export QA — After-School First Love Longplay

Status: render-05 local QA user-approved / release decision planning open / release blocked  
Episode: `s01e01-campus-cafe-longplay`  
Updated: 2026-05-25

## 0. Boundary

This file records local render/export QA evidence for S01E01. The outputs are ignored local QA evidence under `candidates/` only. This does not approve upload, publishing, scheduling, analytics, provider/API/browser/account actions, credentials, Content ID action, release readiness, or positive rights/platform claims.

Render-05 was explicitly approved as a local corrected subtitle refresh after the user identified a Track 1 cue 58 text mismatch in render-04 and the authoritative source sidecars were corrected. Render-05 carries forward the render-04 visual revision while copying and burning in the corrected source sidecars. The user later approved render-05 as the current local QA output. This is not release/upload/platform approval. A source-only release decision planning gate is now open in `reviews/release-decision-plan.md`, but release is not passed. Any additional or revised render/export output, sidecar revision, bumper media, thumbnail, upload package, public metadata package, or release action requires a separate explicit future gate.

## 1. Current State

| Checkpoint | Status | Evidence |
|---|---|---|
| Render-01 local execution | superseded / human visual FAIL | `future-local-render-01`; user flagged visual fidelity blockers listed below. |
| Render-02 revision gate | superseded / mechanical QA pass | Render-02 passed mechanical QA but was superseded by render-03 visual refinements. |
| Render-03 revision gate | superseded / mechanical QA pass | User accepted the overall look but requested subtler subtitle motion and a better headphone icon/spacing. |
| Render-04 revision gate | superseded / subtitle text stale | Render-04 mechanical QA passed before the Track 1 cue 58 source correction; copied sidecars and burned-in text are stale for that cue. |
| Render-05 corrected refresh gate | approved by user | User approved one local-only corrected render/copy refresh with no upload/release/provider/account action. |
| Render helper | revised | `scripts/render_s01e01_local.py`; now targets allowlisted `future-local-render-05`, renders one resumable video segment per song, applies global-time visual offsets for smooth segment joins, and muxes one continuous WAV master into the final QA MP4. |
| Render-05 audio timeline | created | `candidates/s01e01-campus-cafe-longplay/render/future-local-render-05/audio/s01e01-campus-cafe-longplay.timeline-41m43s28.wav` |
| Render-05 segment videos | created | 13 MP4 segments under `candidates/s01e01-campus-cafe-longplay/render/future-local-render-05/video/segments/`. |
| Render-05 QA video | created | `candidates/s01e01-campus-cafe-longplay/render/future-local-render-05/video/s01e01-campus-cafe-longplay.v6-subtitled-1080p24-qa.mp4` |
| Render-05 copied sidecars | created | `candidates/s01e01-campus-cafe-longplay/render/future-local-render-05/subtitles/`; copies byte-match authoritative corrected source sidecars. |
| Render-05 snapshots | created | 7 PNG samples under `candidates/s01e01-campus-cafe-longplay/render/future-local-render-05/qa/snapshots/`. |
| Render-05 mechanical QA | passed | Duration/format/sidecar/subtitle/snapshot/segment assertions passed; video decode produced no ffmpeg errors. |
| Render-05 human/local QA review | user-approved | User approved render-05 as the current local QA output; release remains blocked. |
| Release/upload readiness | release decision planning open / blocked | Source-only release decision planning is open; no release pass or platform/account action is approved. |

## 2. Render-01 Human Visual Review Fail

User review found these blockers in render-01:

1. particle / light atmosphere was missing;
2. visual equalizer did not match the accepted V6 direction;
3. `Now Playing` typography did not match the desired accepted look;
4. parallax still was not smooth enough.

Render-01 remains mechanical evidence only and is superseded for visual QA by later renders. Do not use render-01 as a release or final visual reference.

## 3. Render-05 Revision Summary

| Area | Render-05 change | Current status |
|---|---|---|
| Subtitle text correction | Carries corrected Track 1 cue 58 text from source sidecars: `Same seat tomorrow after school`. | mechanical QA passed; user-approved local QA |
| Subtitle motion | Carries forward render-04 movement: very subtle upward slide with minimal right drift: `x=2px`, `y=-8px`, with smooth per-cue fade. | preview-approved by user; mechanical QA passed; user-approved local QA |
| Headphone icon | Carries forward the symmetric Bézier-based warm vector mark using balanced ear-cup geometry, rounded caps, and a small warm accent. | preview-approved by user; sampled locally; user-approved local QA |
| Icon placement | Carries forward headphone mark placement at `x=48`, `y=88` so spacing before the divider is balanced. | preview-approved by user; sampled locally; user-approved local QA |
| Music notes | Carries forward three tiny warm low-opacity vector notes drifting upward beside the headphone icon. | preview-approved by user; sampled locally; user-approved local QA |
| Segment rendering | Rendered one resumable video segment per song including its following 1s gap, then concatenated the segments and muxed the continuous full WAV timeline. | mechanical QA passed |
| Smoothness across segments | Background parallax, particles, light sweep, reflections, shadows, equalizer phase, and music notes use global timeline offsets so segment joins do not visually reset. Final audio uses one continuous master WAV rather than stitched AAC chunks. | mechanical/sampled QA passed; user-approved local QA |
| Existing V6 fidelity | Carries forward V6-style ribbon/dot equalizer, near-still parallax, richer sunlight/reflection/shadow/particle layers, header-matched `Now Playing`, and final source sidecar timings. | mechanical/sampled QA passed; user-approved local QA |

## 4. Render-05 Output Inventory

| Output | Observed facts | QA status |
|---|---|---|
| WAV timeline | PCM S16LE; stereo; `48000 Hz`; `120157440` frames; `2503.28s` / `41:43.28`. | pass mechanical |
| Segment videos | 13 H.264 video-only segments under `video/segments/`; one segment per song with the following 1s gap included for Tracks 1-12. | pass mechanical |
| MP4 QA render | `239157664` bytes; H.264/AAC; `1920x1080`; `24/1 fps`; stereo AAC `48000 Hz`; container duration `2503.28s`. | pass mechanical |
| SRT copy | byte-matches corrected `subtitles/s01e01-campus-cafe-longplay.en.srt`. | pass mechanical |
| VTT copy | byte-matches corrected `subtitles/s01e01-campus-cafe-longplay.en.vtt`. | pass mechanical |
| Snapshots | 7 render-05 PNG samples: open, Tracks 2/4/7/9/11, and Track 13 subtitle-motion sample; all 7 image reads succeeded at `1920x1080`. | pass sampled visual/readability check; user-approved local QA |

## 5. Render-05 Timeline And Subtitle QA

| Check | Result |
|---|---|
| Track order | Tracks 1-13 rendered in Gate 8 order. |
| Segment policy | 13 resumable video segments; Tracks 1-12 include their following `1.00s` gap; Track 13 ends at timeline end. |
| Gap policy | 12 x `1.00s` gaps; no crossfades; no bumper time. |
| Duration target | Target `2503.28s`; WAV and final MP4 observed at `2503.28s`. |
| Final sidecar cue count | `598` SRT cues. |
| Max subtitle line length | `37` characters. |
| Subtitle overlap count | `0`. |
| Gap cue count | `0`. |
| Track 13 policy | `Dialogue First` remains excluded because selected audio begins at Verse 1; sampled Track 13 rendered subtitle shows `Courtyard trees drop brown leaves`. |
| Track 1 cue 58 source correction | Authoritative source sidecars and render-05 copied sidecars show `Same seat tomorrow after school` at `00:04:10.280 --> 00:04:16.540`; render-05 was generated after this correction. |
| Source sidecar authority | Episode `subtitles/` sidecars remain authoritative; render-folder copies are local QA copies only. |
| Subtitle motion | Generated RGBA subtitle overlay uses smooth per-cue fade and subtle upward movement `x=2px`, `y=-8px`; final human watch remains required for motion feel. |

## 6. Render-05 Visual / Decode / Boundary QA

| Check | Result |
|---|---|
| Video decode | `ffmpeg -v error -i ... -f null -` completed with no errors. |
| Video target | `1920x1080`, `24fps` confirmed by probe. |
| Sampled visual readability | 7 snapshots opened successfully; header/title/subtitle/equalizer remain readable and not obviously clipped in sampled frames. |
| V6 fidelity sample | Render-05 samples carry forward the V6-style ribbon/dot equalizer and near-still parallax plus the refined headphone mark, subtle animated music notes, subtitle motion approved in preview, denser particles, and moving sunlight/reflection/shadow layers. |
| Candidate-media hygiene | Render outputs remain under ignored `candidates/` paths; final MP4 and segment MP4s are ignored by `.gitignore`. |
| Boundary scan | No credentials, account state, provider artifacts, upload artifacts, Content ID action, or positive rights/platform claims were created by this gate. |

## 7. Remaining Stop Conditions

Do not mark release/public readiness unless a future gate closes these:

- source-only release decision planning is open, but the final release decision and current platform/account policy review are not passed;
- any upload/publish/scheduling/API/browser/provider action remains blocked;
- readiness remains `96/100`; do not raise it without fresh final-output evidence and explicit score review;
- additional/revised render/export outputs beyond render-05, sidecar revisions, bumper media, thumbnails, upload packages, or release actions require a new explicit gate.

## 8. Current Verdict

```text
Verdict: render_05_local_qa_user_approved_release_blocked
Scope: explicitly approved local render-05 corrected subtitle QA refresh under ignored candidates/
Render-01: superseded by human visual FAIL for particle/light, equalizer, Now Playing typography, and parallax fidelity
Render-02: mechanical QA pass superseded by render-03 visual revision request
Render-03: mechanical QA pass superseded by render-04 subtitle/icon/music-note revision request
Render-04: mechanical QA pass superseded for subtitle QA by Track 1 cue 58 source correction and render-05 refresh
Timeline: 13 selected tracks, 12 x 1.00s gaps, 41:43.28 / 2503.28s
Chunking: 13 resumable video-only segments plus final concat/mux with one continuous WAV master; visual effects use global timeline offsets for smooth joins
Audio QA: WAV timeline created and duration/format verified
Video QA: 1080p24 H.264/AAC QA MP4 created, decoded, segment-checked, and sampled
Subtitle QA: render-05 SRT/VTT copies byte-match corrected source; Track 1 cue 58 corrected; 598 cues, no overlaps, no gap cues, max line length 37
Human/local QA: user approved render-05 as the current local QA output
Visual QA: render-05 sampled locally for refined headphone icon, subtle music notes, approved subtitle motion, V6-style equalizer, richer light/particle/reflection/shadow layers, and smoother parallax
Readiness score: remains 96/100
Still blocked: final release decision, upload/publish, provider/account/API/browser actions, Content ID registration, positive rights/platform claims, and additional/revised outputs without a new gate
```

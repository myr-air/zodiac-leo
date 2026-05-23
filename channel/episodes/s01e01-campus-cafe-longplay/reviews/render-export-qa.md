# S01E01 Render/Export QA — After-School First Love Longplay

Status: render-02 local mechanical QA recorded / human visual review pending / release blocked  
Episode: `s01e01-campus-cafe-longplay`  
Updated: 2026-05-23

## 0. Boundary

This file records local render/export QA evidence for S01E01. The outputs are ignored local QA evidence under `candidates/` only. This does not approve upload, publishing, scheduling, analytics, provider/API/browser/account actions, credentials, Content ID action, release readiness, or positive rights/platform claims.

Render-02 was explicitly approved as a local revision after render-01 failed human visual review. Any additional or revised render/export output, sidecar revision, bumper media, thumbnail, upload package, public metadata package, or release decision requires a separate explicit future gate.

## 1. Current State

| Checkpoint | Status | Evidence |
|---|---|---|
| Render-01 local execution | superseded / human visual FAIL | `future-local-render-01`; user flagged visual fidelity blockers listed below. |
| Render-02 revision gate | approved by user | User approved revision plan + helper fix + new local render-02 QA. |
| Render helper | revised | `scripts/render_s01e01_local.py`; now targets allowlisted `future-local-render-02`, refuses arbitrary roots/overwrites, and restores V6-like particles/light/equalizer/parallax. |
| Render-02 audio timeline | created | `candidates/s01e01-campus-cafe-longplay/render/future-local-render-02/audio/s01e01-campus-cafe-longplay.timeline-41m43s28.wav` |
| Render-02 QA video | created | `candidates/s01e01-campus-cafe-longplay/render/future-local-render-02/video/s01e01-campus-cafe-longplay.v6-subtitled-1080p24-qa.mp4` |
| Render-02 copied sidecars | created | `candidates/s01e01-campus-cafe-longplay/render/future-local-render-02/subtitles/`; copies byte-match authoritative source sidecars. |
| Render-02 snapshots | created | 7 PNG samples under `candidates/s01e01-campus-cafe-longplay/render/future-local-render-02/qa/snapshots/`. |
| Render-02 mechanical QA | passed | Duration/format/sidecar/subtitle/snapshot assertions passed; video decode produced no ffmpeg errors. |
| Render-02 human full watch/listen | pending | User has not yet passed the revised full QA MP4. |
| Release/upload readiness | blocked | No release-decision gate exists; no platform/account action is approved. |

## 2. Render-01 Human Visual Review Fail

User review found these blockers in render-01:

1. particle / light atmosphere was missing;
2. visual equalizer did not match the accepted V6 direction;
3. `Now Playing` typography did not match the desired accepted look;
4. parallax still was not smooth enough.

Render-01 remains mechanical evidence only and is superseded for visual QA by render-02. Do not use render-01 as a release or final visual reference.

## 3. Render-02 Revision Summary

| Blocker | Render-02 change | Current status |
|---|---|---|
| Missing particle/light atmosphere | Added deterministic warm particle texture, drifting particle overlay, and soft moving light sweep. | sampled locally; human review pending |
| Equalizer mismatch | Replaced ffmpeg `showwaves` line with generated soft V6-style ribbon/dot equalizer overlay from smoothed audio energy. | sampled locally; human review pending |
| Now Playing typography mismatch | Keeps V6 header typography source (`create_v6_cute_smooth_motion_proof.py`) and render-02 screenshots show the same top-left system. | sampled locally; human review pending |
| Parallax not smooth | Reduced background motion to near-still lower-amplitude sinusoidal crop for smoother longplay movement. | sampled locally; human review pending |

## 4. Render-02 Output Inventory

| Output | Observed facts | QA status |
|---|---|---|
| WAV timeline | PCM S16LE; stereo; `48000 Hz`; `120157440` frames; `2503.28s` / `41:43.28`. | pass mechanical |
| MP4 QA render | `219741296` bytes; H.264/AAC; `1920x1080`; `24/1 fps`; stereo AAC `48000 Hz`; `2503.28s`. | pass mechanical |
| SRT copy | byte-matches `subtitles/s01e01-campus-cafe-longplay.en.srt`. | pass mechanical |
| VTT copy | byte-matches `subtitles/s01e01-campus-cafe-longplay.en.vtt`. | pass mechanical |
| Snapshots | 7 render-02 PNG samples: open, Tracks 2/4/7/9/11, and Track 13 subtitle sample; all 7 image reads succeeded. | pass sampled visual/readability check; human review pending |

## 5. Render-02 Timeline And Subtitle QA

| Check | Result |
|---|---|
| Track order | Tracks 1-13 rendered in Gate 8 order. |
| Gap policy | 12 x `1.00s` gaps; no crossfades; no bumper time. |
| Duration target | Target `2503.28s`; WAV and MP4 observed at `2503.28s`. |
| Final sidecar cue count | `598` SRT cues. |
| Max subtitle line length | `37` characters. |
| Subtitle overlap count | `0`. |
| Gap cue count | `0`. |
| Track 13 policy | `Dialogue First` remains excluded because selected audio begins at Verse 1; sampled Track 13 rendered subtitle shows `Courtyard trees drop brown leaves`. |
| Source sidecar authority | Episode `subtitles/` sidecars remain authoritative; render-folder copies are local QA copies only. |

## 6. Render-02 Visual / Decode / Boundary QA

| Check | Result |
|---|---|
| Video decode | `ffmpeg -v error -i ... -f null -` completed with no errors. |
| Video target | `1920x1080`, `24fps` confirmed by probe. |
| Sampled visual readability | 7 snapshots opened successfully; header/title/subtitle/equalizer remain readable and not obviously clipped in sampled frames. |
| V6 fidelity sample | Render-02 samples show visible warm particles, soft light atmosphere, V6-style ribbon/dot equalizer, V6 top-left typography, and lower-amplitude near-still parallax setup. |
| Candidate-media hygiene | Render outputs remain under ignored `candidates/` paths. |
| Boundary scan | No credentials, account state, provider artifacts, upload artifacts, Content ID action, or positive rights/platform claims were created by this gate. |

## 7. Remaining Stop Conditions

Do not mark release/public readiness unless a future gate closes these:

- render-02 full-length human watch/listen pass is still not recorded;
- final release decision and current platform/account policy review do not exist;
- any upload/publish/scheduling/API/browser/provider action remains blocked;
- readiness remains `96/100`; do not raise it without fresh final-output evidence and explicit score review;
- additional/revised render/export outputs, sidecar revisions, bumper media, thumbnails, or upload packages require a new explicit gate.

## 8. Current Verdict

```text
Verdict: render_02_local_mechanical_qa_pass_human_review_pending_release_blocked
Scope: explicitly approved local render-02 QA revision under ignored candidates/
Render-01: superseded by human visual FAIL for particle/light, equalizer, Now Playing typography, and parallax fidelity
Timeline: 13 selected tracks, 12 x 1.00s gaps, 41:43.28 / 2503.28s
Audio QA: WAV timeline created and duration/format verified
Video QA: 1080p24 H.264/AAC QA MP4 created, decoded, and sampled
Subtitle QA: final SRT/VTT copies byte-match source; 598 cues, no overlaps, no gap cues, max line length 37
Visual QA: render-02 sampled locally for V6-style particles/light/equalizer/header/parallax; human full watch/listen still pending
Readiness score: remains 96/100
Still blocked: render-02 human full watch/listen pass, release decision, upload/publish, provider/account/API/browser actions, Content ID registration, positive rights/platform claims, and additional/revised outputs without a new gate
```

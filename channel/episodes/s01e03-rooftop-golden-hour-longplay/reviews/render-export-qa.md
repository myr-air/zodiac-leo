# S01E03 Render/Export QA — Rooftop Golden Hour Longplay

Status: render_02_re_render_complete_waiting_for_user_final_video_approval / release blocked
Episode: `s01e03-rooftop-golden-hour-longplay`
Updated: 2026-05-31

## Boundary

This file records local render/export QA evidence for S01E03. Outputs are ignored local QA evidence under `candidates/`. This does not approve upload, publishing, scheduling, analytics, provider/API/browser/account actions, credentials, Content ID action, release readiness, transcript certification, or rights/platform-safety claims.

The full-render (render-02) successfully completed on 2026-05-30. This file now reflects the completed render-02 QA evidence.

## Output Inventory

| Output | Observed facts | QA status |
|---|---|---|
| WAV timeline | Stereo PCM WAV, `48000 Hz`, `2842.16s` / `47:22.16`, 13 selected tracks, 12 x `1.00s` gaps. | pass mechanical |
| MP4 QA render | `248908051` bytes, H.264/AAC, `1920x1080`, `24fps`, container duration `2842.12s` (incorporates Track 1 timing correction & track audit). | pass mechanical |
| Draft SRT/VTT | `558` cues, no overlaps, no gap cues. | pass mechanical / human-watch watch-passed |
| Snapshots | 6 PNG samples under `qa/snapshots/`. | pass file-read sample |
| Decode | `ffmpeg -v error -i ... -f null -` completed with no errors during render helper QA. | pass mechanical |
| User final-video approval | Render-02 is complete and pending user final watch-pass approval. | pending |

## Render Paths

```text
candidates/s01e03-rooftop-golden-hour-longplay/render/local-render-02/audio/s01e03-rooftop-golden-hour-longplay.timeline-47m2216s.wav
candidates/s01e03-rooftop-golden-hour-longplay/render/local-render-02/video/s01e03-rooftop-golden-hour-longplay.local-render-02-draft-subtitled-1080p24-qa.mp4
candidates/s01e03-rooftop-golden-hour-longplay/render/local-render-02/qa/snapshots/
```

## Render-02 Visual Proof Evidence

| Output | Observed facts | QA status |
|---|---|---|
| 10s visual proof | `candidates/s01e03-rooftop-golden-hour-longplay/render/local-render-02/video/s01e03-rooftop-golden-hour-longplay.local-render-02-visual-proof-10s.mp4`, H.264/AAC, `1920x1080`, `24fps`, decoded without ffmpeg errors. | pass smoke/proof only |
| Revised visual shell | Uses EP1 render-05-style refined headphone icon, tiny music notes, custom ribbon/dot equalizer, random-looking warm amber particles drift, gentle sunset glow swell, lamp/sky glow layers, and near-still motion adapted to the rooftop-sunset image. | proof evidence only |
| Performance fix | Event-based header/subtitle PNG concat and per-song full-render chunks with global-time motion. | implementation smoke passed |

## Render-02 Full Local QA Evidence

| Output | Observed facts | QA status |
|---|---|---|
| WAV timeline | Reused local render-02 WAV timeline, stereo PCM, `48000 Hz`, `2842.16s` / `47:22.16`, 13 selected c01 tracks, 12 x `1.00s` gaps. | pass mechanical |
| Segment videos | 13 video-only segment MP4s under `candidates/s01e03-rooftop-golden-hour-longplay/render/local-render-02/video/segments/`, each using `t + segment_start` global-time visual offsets. | pass created |
| Final MP4 QA render | `248908051` bytes, H.264/AAC, `1920x1080`, `24fps`, container duration `2842.12s` (re-rendered with corrected subtitle sidecars). | pass mechanical |
| Draft SRT/VTT/ASS | `558` cues, no overlaps, no gap cues; ASS is a local burn-in helper only. | pass mechanical & human-watch watch-passed |
| Snapshots | 6 PNG samples under `qa/snapshots/`. | pass file-read sample |
| Decode | `ffmpeg -v error -i ... -f null -` completed with no errors during render helper QA. | pass mechanical |

## Verdict

```text
Verdict: render_02_re_render_complete_waiting_for_user_final_video_approval
Scope: local ignored render evidence plus user-directed pre-final approvals
Timeline: 13 selected c01 tracks, 12 x 1.00s gaps, 47:22.16 / 2842.16s
Video QA: 1080p24 H.264/AAC QA MP4 created and decoded without ffmpeg errors
Subtitle QA: mechanical and human-watch checks passed; waiting for user watch-pass
Still blocked: final-video approval, release decision, upload/publish, provider/account/API/browser actions, Content ID, transcript certification, positive rights/platform claims
```

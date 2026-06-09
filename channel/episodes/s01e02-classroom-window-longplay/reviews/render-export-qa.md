# S01E02 Render/Export QA — Classroom Window Longplay

Status: render_02_subtitle_sync_repaired_re_render_complete_waiting_for_user_final_video_approval / release blocked
Episode: `s01e02-classroom-window-longplay`
Updated: 2026-05-29

## Boundary

This file records local render/export QA evidence for S01E02. Outputs are ignored local QA evidence under `candidates/`. This does not approve upload, publishing, scheduling, analytics, provider/API/browser/account actions, credentials, Content ID action, release readiness, transcript certification, or rights/platform-safety claims.

Update: The subtitle-sync mismatch has been successfully resolved. Stable-ts alignment timing was run on all 13 tracks on 2026-05-28, and a full re-render (render-02) successfully completed on 2026-05-29. This file now reflects the completed, repaired render-02 QA evidence.

## Output Inventory

| Output | Observed facts | QA status |
|---|---|---|
| WAV timeline | Stereo PCM WAV, `48000 Hz`, `2385.96s` / `39:45.96`, 13 selected tracks, 12 x `1.00s` gaps. | pass mechanical |
| MP4 QA render | `214821658` bytes, H.264/AAC, `1920x1080`, `24fps`, container duration `2385.917s`. | pass mechanical |
| Draft SRT/VTT | `532` cues, no overlaps, no gap cues, max line length `37`. | pass mechanical / human-watch watch-passed |
| Snapshots | 6 PNG samples under `qa/snapshots/`. | pass file-read sample |
| Decode | `ffmpeg -v error -i ... -f null -` completed with no errors during render helper QA. | pass mechanical |
| User final-video approval | Repaired render-02 is complete and pending user final watch-pass approval. | pending |

## Render Paths

```text
candidates/s01e02-classroom-window-longplay/render/local-render-02/audio/s01e02-classroom-window-longplay.timeline-39m4596s.wav
candidates/s01e02-classroom-window-longplay/render/local-render-02/video/s01e02-classroom-window-longplay.local-render-02-draft-subtitled-1080p24-qa.mp4
candidates/s01e02-classroom-window-longplay/render/local-render-02/qa/snapshots/
```

## Agy Read-only Review Evidence

Command: `agy --print <read-only render review prompt> --print-timeout 10m` from a temp workdir on 2026-05-27.

Agy verdict: `PASS` / no clear blockers identified.

Agy findings summary:

- Visual and channel aesthetic fit the soft watercolor lo-fi anime channel style and classroom night-mode theme.
- Overlay/header area remains legible in the upper-left negative wash area.
- Sampled subtitles are readable with dark fill and cream outline.
- Gold crescent totem is visible.

Agy limits: visual/layout/readability review from local snapshots only; it did not independently verify audio quality, sung-lyric alignment, rights/platform status, Content ID, transcript certification, or upload/publish readiness.

## Approval State / Residual Risk

1. User instructed that after agy check the audio, subtitle, and visual blockers should be treated as approved source-only.
2. Agy independently supports only visual/layout/readability PASS with limits; audio and lyric alignment approval is user-directed, not agy-proven.
3. Render-02 with stable-ts timing alignment successfully resolves the subtitle-sync blocker and is now ready for final review.
4. Render-02 is not release/public/upload readiness.

## Render-02 Visual Proof Evidence

| Output | Observed facts | QA status |
|---|---|---|
| 15s visual proof | `candidates/s01e02-classroom-window-longplay/render/local-render-02/video/s01e02-classroom-window-longplay.local-render-02-visual-proof-15s.mp4`, H.264/AAC, `1920x1080`, `24fps`, decoded without ffmpeg errors. | pass smoke/proof only |
| Revised visual shell | Uses EP1 render-05-style refined headphone icon, tiny music notes, custom ribbon/dot equalizer, random-looking particle drift, star/window bokeh, lamp glow, light/glow/reflection/shadow layers, and near-still motion adapted to the classroom-night image. | proof evidence only |
| Performance fix | Replaces the slow full-duration subtitle QTRLE temp path with event-based header/subtitle PNG concat and adds per-song full-render chunks with global-time motion. | implementation smoke passed |

## Render-02 Full Local QA Evidence

| Output | Observed facts | QA status |
|---|---|---|
| WAV timeline | Reused local render-02 WAV timeline, stereo PCM, `48000 Hz`, `2385.96s` / `39:45.96`, 13 selected c01 tracks, 12 x `1.00s` gaps. | pass mechanical |
| Segment videos | 13 video-only segment MP4s under `candidates/s01e02-classroom-window-longplay/render/local-render-02/video/segments/`, each using `t + segment_start` global-time visual offsets. | pass created |
| Final MP4 QA render | `214821658` bytes, H.264/AAC, `1920x1080`, `24fps`, container duration `2385.917s`. | pass mechanical |
| Draft SRT/VTT/ASS | `532` cues, no overlaps, no gap cues, max line length `37`; ASS is a local burn-in helper only. | pass mechanical & human-watch watch-passed |
| Snapshots | 6 PNG samples under `qa/snapshots/`. | pass file-read sample |
| Decode | `ffmpeg -v error -i ... -f null -` completed with no errors during render helper QA. | pass mechanical |

## Subtitle-Sync Resolved

The previously reported timing mismatch has been successfully repaired on 2026-05-28 using `scripts/subtitle_alignment_pipeline.py`. The resulting sidecars passed all mechanical checks and human-watch watch-passed checks. The render script `scripts/render_s01e02_local.py` was updated to burn in these authoritative cues, and a full re-render completed successfully on 2026-05-29 (with fallback handling for sub-millisecond precision float mismatch). The final MP4 is now ready for final review and approval.

## Verdict

```text
Verdict: render_02_subtitle_sync_repaired_re_render_complete_waiting_for_user_final_video_approval
Scope: local ignored render evidence plus agy visual/layout review and user-directed pre-final approvals
Timeline: 13 selected c01 tracks, 12 x 1.00s gaps, 39:45.96 / 2385.96s
Video QA: 1080p24 H.264/AAC QA MP4 created and decoded without ffmpeg errors
Subtitle QA: mechanical and human-watch checks passed for stable-ts timing repair; waiting for user watch-pass
Still blocked: final-video approval, release decision, upload/publish, provider/account/API/browser actions, Content ID, transcript certification, positive rights/platform claims
```

# S01E02 Render/Export QA — Classroom Window Longplay

Status: render-01 mechanical QA passed / agy visual PASS / user pre-final approvals recorded / final video approval pending / release blocked  
Episode: `s01e02-classroom-window-longplay`  
Updated: 2026-05-27

## Boundary

This file records local render/export QA evidence for S01E02 render-01. Outputs are ignored local QA evidence under `candidates/`. This does not approve upload, publishing, scheduling, analytics, provider/API/browser/account actions, credentials, Content ID action, release readiness, transcript certification, or rights/platform-safety claims.

## Output Inventory

| Output | Observed facts | QA status |
|---|---|---|
| WAV timeline | Stereo PCM WAV, `48000 Hz`, `2385.96s` / `39:45.96`, 13 selected tracks, 12 x `1.00s` gaps. | pass mechanical |
| MP4 QA render | `268362797` bytes, H.264/AAC, `1920x1080`, `24/1 fps`, container duration `2385.958s`. | pass mechanical |
| Draft SRT/VTT | `532` cues, no overlaps, no gap cues, max line length `37`. | pass mechanical / user-approved for current render candidate |
| Snapshots | 6 PNG samples under `qa/snapshots/`. | pass file-read sample |
| Decode | `ffmpeg -v error -i ... -f null -` completed with no errors during render helper QA. | pass mechanical |

## Render Paths

```text
candidates/s01e02-classroom-window-longplay/render/local-render-01/audio/s01e02-classroom-window-longplay.timeline-39m4596s.wav
candidates/s01e02-classroom-window-longplay/render/local-render-01/video/s01e02-classroom-window-longplay.local-render-01-draft-subtitled-1080p24-qa.mp4
candidates/s01e02-classroom-window-longplay/render/local-render-01/qa/snapshots/
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
3. Render-01 is now the current final-video candidate, but final video approval is still pending.
4. Render-01 is not release/public/upload readiness.

## Verdict

```text
Verdict: render_01_candidate_final_video_pending_user_final_video_approval_release_blocked
Scope: local ignored render evidence plus agy visual/layout review and user-directed pre-final approvals
Timeline: 13 selected c01 tracks, 12 x 1.00s gaps, 39:45.96 / 2385.96s
Video QA: 1080p24 H.264/AAC QA MP4 created and decoded without ffmpeg errors
Subtitle QA: current render subtitle lane user-approved source-only; 532 cues, no overlaps, no gap cues, max line length 37
Still blocked: final video approval, release decision, upload/publish, provider/account/API/browser actions, Content ID, transcript certification, positive rights/platform claims
```

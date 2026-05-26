# S01E02 Render/Export Plan — Classroom Window Longplay

Status: render-01 candidate final video / pre-final approvals recorded / final video approval pending / release blocked  
Episode: `s01e02-classroom-window-longplay`  
Plan ID: `s01e02-render-export-plan-local-render-01`  
Updated: 2026-05-27

## Boundary

This document records the local render/export execution scope opened by the user for an unattended overnight local build. Outputs are ignored local QA evidence under `candidates/`. This does not approve upload, publishing, scheduling, analytics, provider/API/browser/account actions, credentials, Content ID action, release readiness, transcript certification, or rights/platform-safety claims.

## Inputs

| Area | Source truth | Local decision |
|---|---|---|
| Audio | `reviews/audio-candidate-intake.md` | Use user-approved c01 selected set for Tracks 1-13; c02 variants remain pool for issue-led revision only. |
| Visual | `reviews/visual-candidate-intake.md`, `source/visual.md` | Use agy PASS / user-approved `vis-c01` night-mode image with mandatory channel style lock. |
| Assembly | `reviews/assembly-package.md` | Use 1.00s gaps, no crossfades, no bumper. |
| Subtitles | `subtitles/README.md`, `reviews/subtitles.md` | Use current render subtitle lane approved source-only; transcript certification remains blocked. |
| Render helper | `scripts/render_s01e02_local.py` | Local-only helper with Python/Pillow overlays and FFmpeg render. |

## Output Targets

```text
candidates/s01e02-classroom-window-longplay/render/local-render-01/audio/s01e02-classroom-window-longplay.timeline-39m4596s.wav
candidates/s01e02-classroom-window-longplay/render/local-render-01/video/s01e02-classroom-window-longplay.local-render-01-draft-subtitled-1080p24-qa.mp4
candidates/s01e02-classroom-window-longplay/render/local-render-01/subtitles/s01e02-classroom-window-longplay.draft.en.srt
candidates/s01e02-classroom-window-longplay/render/local-render-01/subtitles/s01e02-classroom-window-longplay.draft.en.vtt
candidates/s01e02-classroom-window-longplay/render/local-render-01/qa/snapshots/
```

## Render Behavior

- Output: `1920x1080`, `24fps`, H.264/AAC local QA MP4.
- Background: selected night-mode image scaled/cropped to 16:9.
- Header: dynamic top-left `MELLOW LONGPLAY • S01 - E02`, `Now Playing`, and current track title.
- Equalizer: bottom-right FFmpeg `showwaves` line overlay from the audio timeline.
- Subtitles: burned-in draft mechanical subtitle overlay generated from approved source lyrics.

## Stop Conditions

Stop or require a new gate before any of these actions:

- provider/account/API/browser/upload/public-publish action;
- revised selected audio after final video review;
- subtitle timing/content replacement;
- additional render beyond local-render-01;
- thumbnail/package/upload metadata creation;
- rights/platform-safety or publish-ready claim.

## Verdict

```text
Verdict: render_01_candidate_final_video_pending_user_final_video_approval_release_blocked
Still blocked: final video approval, final readiness/release decision, upload/publish, provider/account/API/browser actions, Content ID, transcript certification, positive rights/platform claims
```

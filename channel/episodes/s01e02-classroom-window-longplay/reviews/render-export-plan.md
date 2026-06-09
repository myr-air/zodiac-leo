# S01E02 Render/Export Plan — Classroom Window Longplay

Status: render-02 subtitle-sync revision required / EP1 render-05 video standard adopted / release blocked
Episode: `s01e02-classroom-window-longplay`
Plan ID: `s01e02-render-export-plan-local-render-02-visual-revision`
Updated: 2026-05-27

## Boundary

This document records the local render/export revision scope opened by the user after render-01 visual fidelity concerns. Outputs are ignored local QA evidence under `candidates/`. This does not approve upload, publishing, scheduling, analytics, provider/API/browser/account actions, credentials, Content ID action, release readiness, transcript certification, or rights/platform-safety claims.

Render-01 remains mechanical QA evidence, but it is no longer the visual target because the user approved the S01E01 render-05 visual language as the canonical video overlay/motion standard for S01E02 and every future video.

## Inputs

| Area | Source truth | Local decision |
|---|---|---|
| Audio | `reviews/audio-candidate-intake.md` | Use user-approved c01 selected set for Tracks 1-13; c02 variants remain pool for issue-led revision only. |
| Visual | `reviews/visual-candidate-intake.md`, `source/visual.md`, `channel/signature-visual-system.md` | Use user-approved `vis-c01` night-mode image, but revise the video overlay/motion shell to carry forward EP1 render-05 and adapt it to the classroom-night image. |
| Assembly | `reviews/assembly-package.md` | Use 1.00s gaps, no crossfades, no bumper. |
| Subtitles | `subtitles/README.md`, `reviews/subtitles.md` | Current draft sidecars are mechanical evidence only; user-reported sung-lyric timing mismatch requires subtitle repair and human-watch alignment evidence before final-video approval. Transcript certification remains blocked. |
| Render helper | `scripts/render_s01e02_local.py` | Local-only helper now targets render-02, includes short proof mode, and uses the EP1 render-05 visual standard with event-based subtitle/header overlay to avoid full-duration subtitle QTRLE temp files. |

## Output Targets

```text
candidates/s01e02-classroom-window-longplay/render/local-render-01/audio/s01e02-classroom-window-longplay.timeline-39m4596s.wav
candidates/s01e02-classroom-window-longplay/render/local-render-01/video/s01e02-classroom-window-longplay.local-render-01-draft-subtitled-1080p24-qa.mp4
candidates/s01e02-classroom-window-longplay/render/local-render-01/subtitles/s01e02-classroom-window-longplay.draft.en.srt
candidates/s01e02-classroom-window-longplay/render/local-render-01/subtitles/s01e02-classroom-window-longplay.draft.en.vtt
candidates/s01e02-classroom-window-longplay/render/local-render-01/qa/snapshots/
```

Current render-02 visual proof evidence:

```text
candidates/s01e02-classroom-window-longplay/render/local-render-02/video/s01e02-classroom-window-longplay.local-render-02-visual-proof-15s.mp4
```

Earlier smoke proof retained as local evidence: `...local-render-02-visual-proof-12s.mp4`.

Full render-02 local QA targets now created:

```text
candidates/s01e02-classroom-window-longplay/render/local-render-02/audio/s01e02-classroom-window-longplay.timeline-39m4596s.wav
candidates/s01e02-classroom-window-longplay/render/local-render-02/video/s01e02-classroom-window-longplay.local-render-02-draft-subtitled-1080p24-qa.mp4
candidates/s01e02-classroom-window-longplay/render/local-render-02/subtitles/s01e02-classroom-window-longplay.draft.en.srt
candidates/s01e02-classroom-window-longplay/render/local-render-02/subtitles/s01e02-classroom-window-longplay.draft.en.vtt
candidates/s01e02-classroom-window-longplay/render/local-render-02/qa/snapshots/
```

Observed full render-02 facts: 13 per-song video-only segments were created, then concatenated and muxed with one continuous WAV master. Final MP4 path: `candidates/s01e02-classroom-window-longplay/render/local-render-02/video/s01e02-classroom-window-longplay.local-render-02-draft-subtitled-1080p24-qa.mp4`; bytes `197241811`; container duration `2385.917s`; format `1920x1080`, `24fps`, H.264/AAC; ffmpeg decode passed; 6 sampled snapshots were extracted.

## Render Behavior

- Output: `1920x1080`, `24fps`, H.264/AAC local QA MP4 or short visual proof MP4.
- Background: selected night-mode image scaled/cropped to 16:9 with near-still parallax.
- Header: dynamic top-left `MELLOW LONGPLAY • S01 - E02`, `Now Playing`, current track title, and the refined EP1 render-05 Bézier headphone icon.
- Music notes: three tiny warm low-opacity animated notes beside the headphone icon.
- Equalizer: bottom-right custom V6-style ribbon/dot equalizer with smoothed audio energy; do not use the plain FFmpeg `showwaves` line for the final visual shell.
- Atmosphere: S01E02 night-adapted warm particles with slow random-looking x/y drift rather than upward-only scrolling, star/window bokeh, lamp glow, soft light sweep, amber glow, desk reflections, and low-contrast shadows with gentle slow flicker/sway.
- Subtitles/header overlay: event-based PNG concat from draft cues and track/title events, avoiding the previous full-duration raw RGBA/QTRLE subtitle movie bottleneck.
- Full render-02 mode: render one video-only segment per song, including the following `1.00s` gap; every segment keys motion to global time (`t + segment_start`), then concatenates video segments and muxes one continuous WAV master so visual effects and audio do not reset at song boundaries.

## Processing Issue Found / Fix

The first render-02 implementation was too slow because it generated a full `39:45.96` subtitle overlay as raw RGBA/QTRLE video. The failed temp run produced a multi-GB subtitle overlay and did not complete a full MP4. The helper now uses event-based header/subtitle PNG concat plus per-song chunked full-render mode with global-time effects; the short `15s` visual proof completed and decoded successfully.

## Stop Conditions

Stop or require a new gate before any of these actions:

- provider/account/API/browser/upload/public-publish action;
- revised selected audio after final video review;
- subtitle timing/content replacement;
- additional full render beyond local-render-02;
- thumbnail/package/upload metadata creation;
- rights/platform-safety or publish-ready claim.

## Verdict

```text
Verdict: render_02_subtitle_sync_revision_required_hold_release_blocked
Still blocked: final-video approval, final readiness/release decision, upload/publish, provider/account/API/browser actions, Content ID, transcript certification, positive rights/platform claims
```

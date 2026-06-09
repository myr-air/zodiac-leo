# S01E03 Render/Export Plan — Rooftop Golden Hour Longplay

Status: full_render_in_progress_gate_opened / EP1 render-05 video standard adopted / release blocked
Episode: `s01e03-rooftop-golden-hour-longplay`
Plan ID: `s01e03-render-export-plan-local-render-02-sunset-revision`
Updated: 2026-05-30

## Boundary

This document records the local render/export plan opened by the user on 2026-05-30. Outputs are ignored local QA evidence under `candidates/`. This does not approve upload, publishing, scheduling, analytics, provider/API/browser/account actions, credentials, Content ID action, release readiness, transcript certification, or rights/platform-safety claims.

The S01E01/S01E02 render-05 visual language is the canonical video overlay/motion standard for S01E03 and future videos.

## Inputs

| Area | Source truth | Local decision |
|---|---|---|
| Audio | `reviews/audio-candidate-intake.md` | Use approved c01 selected set for Tracks 1-13; c02 variants remain pool. |
| Visual | `reviews/visual-candidate-intake.md`, `source/visual.md`, `channel/signature-visual-system.md` | Use approved `vis-c01` sunset-mode image, with video overlay/motion shell matching EP1 render-05 and adapted to rooftop golden hour. |
| Assembly | `manifest.json` | Use 1.00s gaps, no crossfades, no bumper. |
| Subtitles | `subtitles/s01e03-rooftop-golden-hour-longplay.en.srt`, `reviews/subtitles.md` | Dynamic subtitle timings successfully generated via stable-ts and sidecars promoted. ASS is a local burn-in helper. |
| Render helper | `scripts/render_s01e03_local.py` | Local-only helper chunked by track, uses event-based subtitle/header overlay to avoid raw video temp file bottlenecks. |

## Output Targets

Full render-02 local QA targets:

```text
candidates/s01e03-rooftop-golden-hour-longplay/render/local-render-02/audio/s01e03-rooftop-golden-hour-longplay.timeline-47m22s16.wav
candidates/s01e03-rooftop-golden-hour-longplay/render/local-render-02/video/s01e03-rooftop-golden-hour-longplay.local-render-02-draft-subtitled-1080p24-qa.mp4
candidates/s01e03-rooftop-golden-hour-longplay/render/local-render-02/subtitles/s01e03-rooftop-golden-hour-longplay.draft.en.srt
candidates/s01e03-rooftop-golden-hour-longplay/render/local-render-02/subtitles/s01e03-rooftop-golden-hour-longplay.draft.en.vtt
candidates/s01e03-rooftop-golden-hour-longplay/render/local-render-02/qa/snapshots/
```

## Render Behavior

- Output: `1920x1080`, `24fps`, H.264/AAC local QA MP4.
- Background: selected sunset-mode image scaled/cropped to 16:9 with near-still parallax.
- Header: dynamic top-left `MELLOW LONGPLAY • S01 - E03`, `Now Playing`, current track title, and refined Bézier headphone icon.
- Music notes: three tiny warm low-opacity animated notes beside the headphone icon.
- Equalizer: bottom-right custom V6-style ribbon/dot equalizer with smoothed audio energy.
- Atmosphere: S01E03 warm amber particles with slow random-looking x/y drift, slow gentle sunset glow swell, low-opacity equalizer blending into concrete/rail, and clean high-contrast left negative wash.
- Performance: event-based header/subtitle PNG concat and per-song full-render chunks with global-time motion.

## Stop Conditions

Stop or require a new gate before any of these actions:

- provider/account/API/browser/upload/public-publish action;
- revised selected audio after final video review;
- subtitle timing/content replacement;
- additional full render beyond local-render-02;
- release readiness or rights/platform-safety claims.

## Verdict

```text
Verdict: render_02_full_render_in_progress_release_blocked
Still blocked: final-video approval, final readiness/release decision, upload/publish, provider/account/API/browser actions, Content ID, transcript certification, positive rights/platform claims
```

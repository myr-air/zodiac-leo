# S01E01 Render/Export QA — After-School First Love Longplay

Status: qa template prepared / source-only / no render outputs exist  
Episode: `s01e01-campus-cafe-longplay`  
Updated: 2026-05-23

## 0. Boundary

This file is a durable QA template for a future separately approved local render/export execution. It does not record completed render QA yet because no full audio master, video render, export, upload package, provider/account action, or release artifact exists.

Do not fill output-specific results until a separate explicit local render/export execution gate creates the relevant local output files.

## 1. Current State

| Checkpoint | Status | Evidence |
|---|---|---|
| Render/export plan | prepared source-only | `reviews/render-export-plan.md` |
| Local audio master | not created | Execution blocked. |
| Local video render | not created | Execution blocked. |
| Copied sidecars in render folder | not created | Execution blocked. Source sidecars remain in `subtitles/`. |
| Render QA result | not run | No output exists to inspect. |
| Release/upload readiness | blocked | No release-decision gate exists. |

## 2. Future QA Checklist

When a future gate explicitly approves local render/export execution, update this file with actual evidence instead of assumptions.

Minimum future checks:

- Confirm output duration target `2503.28s` / `41:43.28` within documented tolerance.
- Confirm Tracks 1-13 appear in order with 12 x `1.00s` gaps and no crossfades.
- Confirm no unintended silence, clipped joins, missing tracks, or extra audio beyond Track 13.
- Confirm video target `1920x1080`, `24fps`, and no obvious corrupt/dropped sampled frames.
- Confirm top-left header/title, middle-left subtitles, and lower-right equalizer remain readable and crop-safe.
- Confirm subtitle cues match rendered audio context at sampled points across all tracks, including Track 13.
- Confirm source `.en.srt` and `.en.vtt` sidecars still parse and align to the rendered timeline.
- Confirm metadata/disclosure and chapters still match the actual output duration and track order.
- Confirm no credentials, account state, provider artifacts, upload artifacts, Content ID action, or positive rights/platform claims were created.

## 3. Stop Conditions

Do not mark QA passed if any of these are true:

- no local render/export execution gate was approved;
- no actual output exists;
- selected audio, order, gap, visual direction, sidecar timing, or metadata changed without re-planning;
- output duration, subtitle sync, crop/readability, audio continuity, or source-sidecar parsing is unverified;
- release/upload/platform/account language appears without a separate release-decision gate.

## 4. Current Verdict

```text
Verdict: qa_template_prepared_source_only_no_outputs_exist
Scope: placeholder for future local render/export QA evidence
Render/export execution: blocked pending separate explicit gate
Readiness score: remains 96/100 source-only
Still blocked: output creation, upload/publish, provider/account/API/browser actions, Content ID registration, positive rights/platform claims
```

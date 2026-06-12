# S01E05 Render/Export QA — Apartment Window Longplay

Status: render_01_visual_proof_completed_waiting_for_user_final_video_approval / release blocked
Episode: `s01e05-apartment-window-longplay`
Updated: 2026-06-11

## Boundary

This file records local render/export QA evidence for S01E05. Outputs are ignored local QA evidence under `candidates/`. This does not approve upload, publishing, scheduling, analytics, provider/API/browser/account actions, credentials, Content ID action, release readiness, transcript certification, or rights/platform-safety claims.

## Output Inventory

| Output | Observed facts | QA status |
|---|---|---|
| WAV timeline | 13 selected tracks, 12 x `1.75s` gaps, final planned duration `2767.76s` / `46:07.76`. | pass mechanical |
| MP4 QA render (10s proof) | H.264/AAC, `1920x1080`, `24fps`, container duration `10.00s`. | pass mechanical |
| Draft SRT/VTT | `448` cues, no overlaps, no gap cues, max line length `37`. | pass mechanical |
| Decode | `ffmpeg -v error -i ... -f null -` completed with no errors during render helper QA. | pass mechanical |
| User final-video approval | 10s visual proof render is complete and pending user final watch-pass approval. | pending |

## Render Paths

```text
candidates/s01e05-apartment-window-longplay/render/local-render-01/video/s01e05-apartment-window-longplay.local-render-01-visual-proof-10s-9e2b5396e39ac2.mp4
```

## Render-01 Visual Proof Evidence

| Output | Observed facts | QA status |
|---|---|---|
| 10s visual proof | `candidates/s01e05-apartment-window-longplay/render/local-render-01/video/s01e05-apartment-window-longplay.local-render-01-visual-proof-10s-9e2b5396e39ac2.mp4`, H.264/AAC, `1920x1080`, `24fps`, decoded without ffmpeg errors. | pass smoke/proof only |
| Overlays | Refined headphone icon, music notes, equalizer, and visual atmosphere layers (glow, shadow, reflections) are generated and blended with the apartment background illustration. | pass smoke |

## Verdict

```text
Verdict: render_01_visual_proof_completed_waiting_for_user_final_video_approval
Scope: local ignored render evidence and 10s visual proof render validation
Timeline: 13 selected c01 tracks, 12 x 1.75s gaps, 46:07.76 / 2767.76s
Video QA: 1080p24 H.264/AAC visual-proof MP4 created and decoded without ffmpeg errors
Subtitle QA: mechanical checks passed for final promoted and translated subtitles
Still blocked: final-video approval, release decision, upload/publish, provider/account/API/browser actions, Content ID, transcript certification, positive rights/platform claims
```

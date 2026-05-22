# S01E01 Render/Export Plan — After-School First Love Longplay

Status: render/export planning passed / source-only / no outputs created / execution blocked  
Episode: `s01e01-campus-cafe-longplay`  
Plan ID: `s01e01-render-export-plan-01`  
Updated: 2026-05-23

## 0. Boundary

This document defines a future local render/export execution plan only. It does not create or approve audio masters, video files, exports, uploads, publishing, scheduling, analytics, provider/API/browser/account actions, credentials, Content ID action, or positive rights/platform claims.

No media output paths listed here exist because of this planning gate. Treat every media path in the output section as a future target placeholder that requires a separate explicit local render/export execution gate before creation.

## 1. Source Inputs Confirmed For Planning

| Area | Source truth | Planning decision |
|---|---|---|
| Episode state | `manifest.json`, `reviews/current-state.md` | Source packet remains open. Render/export planning is source-only; execution stays blocked. |
| Assembly package | `reviews/assembly-package.md` | Carry forward selected Tracks 1-13 with `1.00s` inter-track gaps and planned `41:43.28` timeline. |
| Audio candidates | `reviews/audio-qa-listening.md`, `tracking/assets.csv` | Future execution should use the 13 selected local WAV candidates in the exact order below. No swaps, trims, or normalization policy changes are approved here. |
| Visual direction | `source/visual-overlay-motion-plan.md`, `reviews/visual-layout-proof-review.md` | Carry forward V6 cute-smooth visual direction with crop/safe-zone and downscale proof evidence. |
| Subtitles | `subtitles/README.md`, `reviews/subtitle-improvement.md` | Use the promoted final English `.srt` and `.vtt` sidecars as source truth for subtitle timing. |
| Metadata/disclosure | `source/metadata.md` | Use Gate 11 title/description/disclosure and chapter display drafts only as local QA references. Not final upload metadata. |
| Internal readiness | `reviews/episode-production-worksheet.md` | Remains `96/100` source-only. This plan alone does not support a score increase. |

## 2. Future Local Timeline Target

Policy for a future approved local execution:

- Use the selected WAV candidates untrimmed.
- Insert exactly `1.00s` silence/space between Tracks 1-12 and the next track.
- Use no crossfades.
- Reserve no intro/outro bumper time.
- Keep Track 13 as the bonus closing song.
- Keep selected audio content duration `41:31.28`; planned full timeline `41:43.28` including gaps.

| Track | Working title | Selected audio path | Chapter start | Track audio end | Gap after |
|---:|---|---|---:|---:|---:|
| 1 | Margin Notes at Table Three | `candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t01_c02--margin-notes-at-table-three.wav` | 00:00.00 | 04:39.92 | 1.00s |
| 2 | Two Lids, One Tray | `candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t02_c01--two-lids-one-tray.wav` | 04:40.92 | 08:25.92 | 1.00s |
| 3 | Borrowed Eraser, Written Name | `candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t03_c01--borrowed-eraser-written-name.wav` | 08:26.92 | 11:51.04 | 1.00s |
| 4 | Checkout Slip at Chapter Nine | `candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t04_c01--checkout-slip-at-chapter-nine.wav` | 11:52.04 | 15:21.60 | 1.00s |
| 5 | Steam on the Glass Door | `candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t05_c01--steam-on-the-glass-door.wav` | 15:22.60 | 19:01.00 | 1.00s |
| 6 | Peach Can at B4 | `candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t06_c02--peach-can-at-b4.wav` | 19:02.00 | 21:41.92 | 1.00s |
| 7 | Green Dot on Your Schedule | `candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t07_c01--green-dot-on-your-schedule.wav` | 21:42.92 | 24:57.84 | 1.00s |
| 8 | Cushion Seat, Charging Cord | `candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t08_c01--cushion-seat-charging-cord.wav` | 24:58.84 | 27:10.72 | 1.00s |
| 9 | Crosswalk Stripes Before Six | `candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t09_c01--crosswalk-stripes-before-six.wav` | 27:11.72 | 29:57.64 | 1.00s |
| 10 | Yellow Tag on the Umbrella Rack | `candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t10_c01--yellow-tag-on-the-umbrella-rack.wav` | 29:58.64 | 33:11.08 | 1.00s |
| 11 | Quiz Key in Blue Ink | `candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t11_c01--quiz-key-in-blue-ink.wav` | 33:12.08 | 35:51.96 | 1.00s |
| 12 | Tray Return at 5:59 | `candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t12_c01--tray-return-at-559.wav` | 35:52.96 | 39:12.28 | 1.00s |
| 13 bonus | Latch Click at the Courtyard Gate | `candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t13_c01--latch-click-at-the-courtyard-gate.wav` | 39:13.28 | 41:43.28 | none |

## 3. Future Local Output Targets And QA Template

The candidate media paths below are planning placeholders only. Do not create them without a separate explicit local render/export execution gate. Candidate media paths stay ignored local evidence. The QA template exists as a durable review doc path, not a generated candidate artifact.

```text
candidates/s01e01-campus-cafe-longplay/render/future-local-render-01/audio/s01e01-campus-cafe-longplay.timeline-41m43s28.wav
candidates/s01e01-campus-cafe-longplay/render/future-local-render-01/video/s01e01-campus-cafe-longplay.v6-subtitled-1080p24-qa.mp4
candidates/s01e01-campus-cafe-longplay/render/future-local-render-01/sidecars/s01e01-campus-cafe-longplay.en.srt
candidates/s01e01-campus-cafe-longplay/render/future-local-render-01/sidecars/s01e01-campus-cafe-longplay.en.vtt
channel/episodes/s01e01-campus-cafe-longplay/reviews/render-export-qa.md
```

Planning notes:

- Use a `qa` filename, not a release/public filename, until a later final QA and release-decision gate exists.
- Any generated render files should remain ignored local evidence under `candidates/` unless a future repo rule explicitly changes that.
- Use `reviews/render-export-qa.md` for future durable render/export QA evidence after a later execution gate creates outputs; do not write generated Markdown under `candidates/`.
- If future execution copies sidecars into the render folder for local QA, the source sidecars under `channel/episodes/s01e01-campus-cafe-longplay/subtitles/` remain the authoritative subtitle source.
- Do not create thumbnails, upload packages, public metadata files, account exports, or platform-specific package artifacts in this gate.

## 4. Future Visual Render Target

Carry forward V6 visual language from `source/visual-overlay-motion-plan.md`:

- output target: `1920x1080`, `24fps`, derived from the V6 proof convention;
- top-left info block with header retained and track title slide-in/out at track boundaries;
- middle-left lyric subtitle layer using final sidecar timings;
- lower-right smoothed waveform/ribbon equalizer with honey dots and secondary opacity;
- near-still parallax, warm particles, cup steam, subtle local hair/leaf movement, and gentle light sweep;
- deterministic motion seed and no hard particle reset at track boundaries;
- conservative crop-safe inset for header, track title, subtitles, and equalizer unless a future proof demonstrates safety.

Future execution must re-check the V6 crop/safe-zone and downscale proof sheets before rendering, then sample the actual full-length output after rendering. The V6 proof narrows source-planning risk but is not final-render QA.

## 5. Future Subtitle Target

Authoritative source sidecars:

```text
channel/episodes/s01e01-campus-cafe-longplay/subtitles/s01e01-campus-cafe-longplay.en.srt
channel/episodes/s01e01-campus-cafe-longplay/subtitles/s01e01-campus-cafe-longplay.en.vtt
```

Known source-sidecar facts to preserve:

- 598 cues across 13 tracks.
- No overlaps.
- No cues in the 1-second inter-track gaps.
- Max line length: 37 chars.
- Track 13 `Dialogue First` remains excluded from timing because the selected audio begins at Verse 1.
- Final cue timeline remains within `41:43.28`.

Future execution should use these timings to drive on-video lyric subtitles and local sidecar QA. Do not revise cue text, cue boundaries, language, Track 13 section policy, or gap cue policy without a separate sidecar revision gate.

## 6. Metadata / Disclosure QA Reference

Use `source/metadata.md` as a local QA reference only:

- listener-facing title draft;
- description draft with AI-assisted workflow disclosure;
- rounded chapter display draft;
- modest tag policy;
- blocked-claim guardrails.

Do not upload, publish, schedule, edit public metadata, use YouTube Studio/API/browser automation, or mark the metadata as final. Re-review against actual final local assets and current platform/account policy before any future release-decision gate.

## 7. Future Render/Export QA Checklist

A future separately approved local execution should produce a QA note before any readiness claim. Minimum checks:

### Preflight before rendering

- Re-read `AGENTS.md`, `KNOWLEDGE.md`, this plan, `reviews/current-state.md`, `reviews/assembly-package.md`, `source/metadata.md`, `source/visual-overlay-motion-plan.md`, `subtitles/README.md`, and tracking CSVs.
- Confirm the 13 selected WAV paths exist and match the selected candidate IDs.
- Confirm final `.en.srt` and `.en.vtt` sidecars parse.
- Confirm no selected audio, order, gap, crossfade, bumper, visual, or metadata decision changed.
- Confirm the explicit local render/export execution gate is approved before creating outputs.

### Mechanical output checks after rendering

- Duration: target `2503.28s` / `41:43.28`, within a documented tolerance.
- Track boundaries: 13 tracks in order, 12 gaps at `1.00s`, no crossfades.
- Audio continuity: no unintended silence, clipped joins, missing tracks, or extra audio beyond Track 13.
- Video: `1920x1080`, `24fps`, no obvious dropped/corrupt frames in sampled checks.
- Visual readability: top-left header/title, subtitles, and lower-right equalizer remain crop-safe and readable at representative samples, including downscale checks.
- Subtitle sync: cue starts/ends match the rendered audio context at multiple sampled points per track, including Track 13.
- Sidecar match: source sidecars still parse and remain aligned to the rendered timeline.
- Metadata consistency: local QA title/description/chapter draft still matches actual duration and track order.
- Boundary scan: no positive rights/platform/upload/public-publish claims, credentials, account state, or provider/platform artifacts added.

### Human review before any later release decision

- Full-length watch/listen pass or a documented sampling plan plus risk acceptance.
- Subtitle readability review in the actual rendered context.
- Visual crop/readability review on target viewports.
- Fresh readiness score decision; do not raise `96/100` without new final-output evidence.

## 8. Stop Conditions

Stop and re-plan before local render/export execution if any of these change:

- selected audio candidate, duration, order, gap, crossfade, bumper, or trim policy;
- subtitle sidecar timing, text, Track 13 exclusion, or language policy;
- V6 visual direction, overlay placement, crop/safe-zone evidence, font availability, or motion behavior;
- metadata/disclosure wording, chapter source, or forbidden-claim boundary;
- provenance, account, credential, provider, platform, rights, or release assumptions;
- source docs conflict with manifest, current-state, or tracking CSVs;
- user requests actual render/export without naming the local execution scope and stop conditions.

## 9. Verdict

```text
Verdict: pass_render_export_planning_source_only
Scope: future local render/export input map, output target placeholders, and QA checklist only
Timeline target: selected Tracks 1-13 with 12 x 1.00s gaps for planned 41:43.28 duration
Subtitle target: promoted final English en.srt and en.vtt sidecars carried forward source-only
Visual target: V6 cute-smooth direction carried forward source-only with safe-zone checks required later
Readiness score: remains 96/100 source-only
Outputs created by this gate: none
Next allowed action: separately approve local render/export execution if moving beyond planning
Still blocked: actual full video assembly, render/export output creation, upload/publish, provider/account/API/browser actions, Content ID registration, positive rights/platform claims
```

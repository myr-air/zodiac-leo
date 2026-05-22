# S01E01 Assembly Package Plan — After-School First Love Longplay

Status: assembly package planning passed / source-only / final sidecars and render-export blocked  
Episode: `s01e01-campus-cafe-longplay`  
Package ID: `s01e01-assembly-package-plan-01`  
Updated: 2026-05-22

## 0. Boundary

This document defines the source-only assembly package target for later approval gates. It does not create final `.srt`/`.vtt` sidecars, audio masters, rendered videos, exports, uploads, release readiness, account actions, credentials, API calls, analytics, Content ID registration, or positive rights/platform claims.

Use this plan only as the next source truth for a separately approved final subtitle sidecar promotion gate or a later render/export planning gate.

## 1. Inputs Carried Forward

| Area | Source truth | Carry-forward decision |
|---|---|---|
| Episode manifest | `manifest.json` | Source packet remains open; no provider/media/release approval. |
| Audio order and duration | `source/metadata.md`, `reviews/audio-qa-listening.md` | Use selected draft Tracks 1-13 in current order. Audio content duration is `41:31.28`. |
| Gap policy | `source/metadata.md` | Use `1.00s` between tracks; no crossfade; no intro/outro bumper time reserved. |
| Planned full timeline | `source/metadata.md` | Planned sequence duration is `41:43.28` including 12 gaps. |
| Visual direction | `reviews/visual-layout-proof-review.md`, `source/visual-overlay-motion-plan.md` | Carry forward V6 cute-smooth visual direction source-only. |
| Subtitle timing evidence | `subtitles/README.md`, `reviews/subtitle-improvement.md` | Tracks 1-13 draft timings are human-watch passed source-only; final sidecars remain blocked. |
| Metadata/disclosure | `source/metadata.md` | Gate 11 source-only title, description, disclosure, chapters, and tags policy remain the draft metadata source. |
| Internal readiness | `reviews/episode-production-worksheet.md` | Gate 12 remains `96/100` source-only; no score uplift from this planning document alone. |

## 2. Assembly Timeline Target

| Track | Working title | Selected draft duration | Chapter start | Track audio end | Gap after |
|---:|---|---:|---:|---:|---:|
| 1 | Margin Notes at Table Three | 279.92s | 00:00.00 | 04:39.92 | 1.00s |
| 2 | Two Lids, One Tray | 225.00s | 04:40.92 | 08:25.92 | 1.00s |
| 3 | Borrowed Eraser, Written Name | 204.12s | 08:26.92 | 11:51.04 | 1.00s |
| 4 | Checkout Slip at Chapter Nine | 209.56s | 11:52.04 | 15:21.60 | 1.00s |
| 5 | Steam on the Glass Door | 218.40s | 15:22.60 | 19:01.00 | 1.00s |
| 6 | Peach Can at B4 | 159.92s | 19:02.00 | 21:41.92 | 1.00s |
| 7 | Green Dot on Your Schedule | 194.92s | 21:42.92 | 24:57.84 | 1.00s |
| 8 | Cushion Seat, Charging Cord | 131.88s | 24:58.84 | 27:10.72 | 1.00s |
| 9 | Crosswalk Stripes Before Six | 165.92s | 27:11.72 | 29:57.64 | 1.00s |
| 10 | Yellow Tag on the Umbrella Rack | 192.44s | 29:58.64 | 33:11.08 | 1.00s |
| 11 | Quiz Key in Blue Ink | 159.88s | 33:12.08 | 35:51.96 | 1.00s |
| 12 | Tray Return at 5:59 | 199.32s | 35:52.96 | 39:12.28 | 1.00s |
| 13 bonus | Latch Click at the Courtyard Gate | 150.00s | 39:13.28 | 41:43.28 | none |

Assembly policy:

- Keep the exact order above.
- Insert only the planned `1.00s` gaps between tracks.
- Keep crossfades disabled.
- Keep bumper media and revised duration blocked unless a separate future gate approves them.
- Treat candidate audio files under `candidates/` as local ignored evidence until a later approved local assembly/render step.

## 3. Final Subtitle Sidecar Target

Planned final sidecar paths, not yet created:

```text
channel/episodes/s01e01-campus-cafe-longplay/subtitles/s01e01-campus-cafe-longplay.en.srt
channel/episodes/s01e01-campus-cafe-longplay/subtitles/s01e01-campus-cafe-longplay.en.vtt
```

Sidecar promotion policy for a future approved gate:

- Build from the human-watch-passed track-local draft timings under `candidates/s01e01-campus-cafe-longplay/subtitles/proofs/`.
- Shift each track-local cue by the exact chapter start in Section 2.
- Keep the planned 1-second inter-track gaps subtitle-empty unless a future approved cue policy says otherwise.
- Preserve Track 13 selected-audio policy: exclude the absent `Dialogue First` source section from final sidecar timing because the selected audio begins at Verse 1.
- Do not invent lyric text, timestamps, translation text, speaker labels, or transcript claims.
- Validate generated sidecars with parser/mechanical checks and at least one human spot-check before treating them as final source sidecars.

## 4. Visual Carry-forward Target

Future render/export planning should carry forward V6 source-only direction:

- cute readable typography;
- smoother equalizer behavior;
- near-still parallax;
- local hair/leaf motion;
- header hold;
- track title slide-in/out;
- safe-zone and downscale evidence from the V6 crop proof review.

This plan does not approve generating a full visual render. Final video readiness still needs rendered evidence for readability, clipping, crop, subtitle placement, audio sync, and duration.

## 5. Future Verification Gates

### Final sidecar promotion gate, if separately approved

- Generate only the planned `.srt` and `.vtt` targets above.
- Parse both files successfully.
- Check chronological cue order, no overlap, no unintended cue in gap windows, line length/readability, Track 13 `Dialogue First` exclusion, and final cue end within the planned `41:43.28` timeline.
- Record results in `subtitles/README.md`, `reviews/current-state.md`, tracking CSVs, and this package document if the target changes.

### Render/export planning gate, if separately approved later

- Re-read this package, `manifest.json`, `current-state.md`, `source/metadata.md`, `subtitles/README.md`, visual reviews, and tracking CSVs.
- Define exact local render inputs and output paths before rendering.
- Require rendered-media QA before any ready claim: duration, audio continuity, subtitle readability, safe-zone/crop, frame sampling, final sidecar match, and metadata/disclosure consistency.
- Keep upload/public-publish planning and external account actions blocked unless a separate future gate explicitly approves them.

## 6. Stop Conditions

Stop and re-plan before sidecar promotion or render/export if any of these change:

- selected audio candidate, duration, order, gap, crossfade, or bumper policy;
- approved lyrics or Track 13 absent-section policy;
- V6 visual direction, crop/safe-zone evidence, or overlay behavior;
- metadata title/description/disclosure/chapter wording;
- provenance, rights, platform, account, credential, or upload boundary;
- any source file conflicts with `manifest.json`, `current-state.md`, or tracking CSVs.

## 7. Verdict

```text
Verdict: pass_assembly_package_planning_source_only
Scope: source-only assembly package target for later sidecar or render planning gates
Timeline target: selected Tracks 1-13 with 12 x 1.00s gaps for planned 41:43.28 duration
Subtitle target: planned final en.srt and en.vtt paths defined but not created
Visual target: V6 cute-smooth direction carried forward source-only
Readiness score: remains 96/100 source-only
Next allowed action: separately approve final subtitle sidecar promotion using this package plan, or separately approve render/export planning after final sidecar policy is settled
Still blocked: final sidecars until separate sidecar gate, full video assembly, render/export, upload/publish, provider/account/API/browser actions, Content ID registration, positive rights/platform claims
```

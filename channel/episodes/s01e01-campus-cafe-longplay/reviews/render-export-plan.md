# S01E01 Render/Export Plan — After-School First Love Longplay

Status: render/export planning passed / render-05 local QA user-approved / release blocked  
Episode: `s01e01-campus-cafe-longplay`  
Plan ID: `s01e01-render-export-plan-01`  
Updated: 2026-05-24

## 0. Boundary

This document defines the approved local render/export execution plan and records that render-01 was superseded by user-approved render-02/render-03/render-04 visual revisions and the user-approved render-05 corrected subtitle refresh. It does not approve uploads, publishing, scheduling, analytics, provider/API/browser/account actions, credentials, Content ID action, release readiness, or positive rights/platform claims.

The render-01, render-02, render-03, render-04, and render-05 media paths listed here now exist as ignored local QA evidence from approved local gates. Render-01 is not a final visual reference because it failed human visual review, render-02 is superseded by render-03, render-03 is superseded by render-04, and render-04 is stale for Track 1 cue 58 after the source correction. Render-05 is the current user-approved local QA output with corrected source sidecars copied and burned in. Treat any additional render/export output, corrected render/copy refresh, revised media, thumbnail, upload package, or public/release artifact as blocked until a separate explicit gate approves it.

## 1. Source Inputs Confirmed For Planning

| Area | Source truth | Planning decision |
|---|---|---|
| Episode state | `manifest.json`, `reviews/current-state.md` | Source packet remains open. Render-05 is the current user-approved local QA output after the Track 1 cue 58 correction; release remains blocked. |
| Assembly package | `reviews/assembly-package.md` | Carry forward selected Tracks 1-13 with `1.00s` inter-track gaps and planned `41:43.28` timeline. |
| Audio candidates | `reviews/audio-qa-listening.md`, `tracking/assets.csv` | The approved local execution used the 13 selected local WAV candidates in the exact order below. No swaps, trims, or normalization policy changes are approved here. |
| Visual direction | `source/visual-overlay-motion-plan.md`, `reviews/visual-layout-proof-review.md` | Carry forward V6 cute-smooth visual direction with crop/safe-zone and downscale proof evidence. |
| Subtitles | `subtitles/README.md`, `reviews/subtitle-improvement.md` | Use the promoted final English `.srt` and `.vtt` sidecars as source truth for subtitle timing and text. Track 1 cue 58 now reads `Same seat tomorrow after school` at the existing timing. |
| Metadata/disclosure | `source/metadata.md` | Use Gate 11 title/description/disclosure and chapter display drafts only as local QA references. Not final upload metadata. |
| Internal readiness | `reviews/episode-production-worksheet.md` | Remains `96/100` internal readiness. Render-05 mechanical QA alone does not support a score increase or release claim. |

## 2. Local Timeline Target Used

Policy used for the approved local execution:

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

## 3. Local Output Targets Created

The candidate media paths below were created by approved local executions and remain ignored local evidence. The QA result lives in a durable review doc path, not as generated Markdown under `candidates/`.

Render-01 was created first and then superseded by human visual FAIL:

```text
candidates/s01e01-campus-cafe-longplay/render/future-local-render-01/audio/s01e01-campus-cafe-longplay.timeline-41m43s28.wav
candidates/s01e01-campus-cafe-longplay/render/future-local-render-01/video/s01e01-campus-cafe-longplay.v6-subtitled-1080p24-qa.mp4
candidates/s01e01-campus-cafe-longplay/render/future-local-render-01/subtitles/s01e01-campus-cafe-longplay.en.srt
candidates/s01e01-campus-cafe-longplay/render/future-local-render-01/subtitles/s01e01-campus-cafe-longplay.en.vtt
```

Render-02 passed mechanical QA and is superseded by render-03:

```text
candidates/s01e01-campus-cafe-longplay/render/future-local-render-02/audio/s01e01-campus-cafe-longplay.timeline-41m43s28.wav
candidates/s01e01-campus-cafe-longplay/render/future-local-render-02/video/s01e01-campus-cafe-longplay.v6-subtitled-1080p24-qa.mp4
candidates/s01e01-campus-cafe-longplay/render/future-local-render-02/subtitles/s01e01-campus-cafe-longplay.en.srt
candidates/s01e01-campus-cafe-longplay/render/future-local-render-02/subtitles/s01e01-campus-cafe-longplay.en.vtt
candidates/s01e01-campus-cafe-longplay/render/future-local-render-02/qa/snapshots/
channel/episodes/s01e01-campus-cafe-longplay/reviews/render-export-qa.md
```

Render-03 passed mechanical QA and is superseded by render-04:

```text
candidates/s01e01-campus-cafe-longplay/render/future-local-render-03/audio/s01e01-campus-cafe-longplay.timeline-41m43s28.wav
candidates/s01e01-campus-cafe-longplay/render/future-local-render-03/video/s01e01-campus-cafe-longplay.v6-subtitled-1080p24-qa.mp4
candidates/s01e01-campus-cafe-longplay/render/future-local-render-03/subtitles/s01e01-campus-cafe-longplay.en.srt
candidates/s01e01-campus-cafe-longplay/render/future-local-render-03/subtitles/s01e01-campus-cafe-longplay.en.vtt
candidates/s01e01-campus-cafe-longplay/render/future-local-render-03/qa/snapshots/
channel/episodes/s01e01-campus-cafe-longplay/reviews/render-export-qa.md
```

Render-04 is the latest local QA revision but predates the Track 1 cue 58 source correction:

```text
candidates/s01e01-campus-cafe-longplay/render/future-local-render-04/audio/s01e01-campus-cafe-longplay.timeline-41m43s28.wav
candidates/s01e01-campus-cafe-longplay/render/future-local-render-04/video/s01e01-campus-cafe-longplay.v6-subtitled-1080p24-qa.mp4
candidates/s01e01-campus-cafe-longplay/render/future-local-render-04/video/segments/
candidates/s01e01-campus-cafe-longplay/render/future-local-render-04/subtitles/s01e01-campus-cafe-longplay.en.srt
candidates/s01e01-campus-cafe-longplay/render/future-local-render-04/subtitles/s01e01-campus-cafe-longplay.en.vtt
candidates/s01e01-campus-cafe-longplay/render/future-local-render-04/qa/snapshots/
channel/episodes/s01e01-campus-cafe-longplay/reviews/render-export-qa.md
```

Render-05 is the current corrected local QA revision:

```text
candidates/s01e01-campus-cafe-longplay/render/future-local-render-05/audio/s01e01-campus-cafe-longplay.timeline-41m43s28.wav
candidates/s01e01-campus-cafe-longplay/render/future-local-render-05/video/s01e01-campus-cafe-longplay.v6-subtitled-1080p24-qa.mp4
candidates/s01e01-campus-cafe-longplay/render/future-local-render-05/video/segments/
candidates/s01e01-campus-cafe-longplay/render/future-local-render-05/subtitles/s01e01-campus-cafe-longplay.en.srt
candidates/s01e01-campus-cafe-longplay/render/future-local-render-05/subtitles/s01e01-campus-cafe-longplay.en.vtt
candidates/s01e01-campus-cafe-longplay/render/future-local-render-05/qa/snapshots/
channel/episodes/s01e01-campus-cafe-longplay/reviews/render-export-qa.md
```

Output notes:

- The video uses a `qa` filename, not a release/public filename, until a later final QA and release-decision gate exists.
- Any generated render files should remain ignored local evidence under `candidates/` unless a future repo rule explicitly changes that.
- Use `reviews/render-export-qa.md` for durable render/export QA evidence; do not write generated Markdown under `candidates/`.
- Copied sidecars in the render folder are local QA copies only; the source sidecars under `channel/episodes/s01e01-campus-cafe-longplay/subtitles/` remain authoritative. Render-05 copied sidecars byte-match the corrected source; render-04 copied sidecars no longer match after the Track 1 cue 58 text fix.
- Do not create thumbnails, upload packages, public metadata files, account exports, or platform-specific package artifacts in this gate.

## 4. Visual Render Target Used

Carry forward V6 visual language from `source/visual-overlay-motion-plan.md`:

- output target: `1920x1080`, `24fps`, derived from the V6 proof convention;
- top-left info block with header retained and track title slide-in/out at track boundaries;
- middle-left lyric subtitle layer using final sidecar timings;
- lower-right smoothed waveform/ribbon equalizer with honey dots and secondary opacity;
- near-still parallax, warm particles, cup steam, subtle local hair/leaf movement, and gentle light sweep;
- deterministic motion seed and no hard particle reset at track boundaries;
- conservative crop-safe inset for header, track title, subtitles, and equalizer unless a future proof demonstrates safety.

Render-01 did not satisfy user visual fidelity expectations. Render-02 revised the helper to restore visible particles/light, a V6-style soft ribbon/dot equalizer, V6 top-left typography, and smoother near-still parallax. Render-03 added header-matched `Now Playing`, generated subtitle motion, and richer moving sunlight/reflection/shadow/particle layers. Render-04 kept the accepted render-03 look while reducing subtitle movement to `x=2px`, `y=-8px`, replacing the loose headphone mark with a balanced Bézier vector icon at `x=48`, `y=88`, adding subtle low-opacity animated music notes beside the icon, and rendering one resumable video segment per song with global-time visual offsets before muxing one continuous WAV master. Render-05 carries forward render-04 visuals and refreshes the subtitle burn/copies after the Track 1 cue 58 source correction. Render-05 samples narrow mechanical/readability risk but are not a full human final-output QA pass.

## 5. Subtitle Target Used

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
- Track 1 cue 58 at `00:04:10.280 --> 00:04:16.540` is corrected to `Same seat tomorrow after school`; timing and cue count are unchanged.

The approved local executions used the current timings to drive on-video lyric subtitles and local sidecar QA. Render-05 was generated after the Track 1 cue 58 text correction and copied the corrected source sidecars. Do not revise cue text, cue boundaries, language, Track 13 section policy, or gap cue policy without a separate sidecar revision gate.

## 6. Metadata / Disclosure QA Reference

Use `source/metadata.md` as a local QA reference only:

- listener-facing title draft;
- description draft with AI-assisted workflow disclosure;
- rounded chapter display draft;
- modest tag policy;
- blocked-claim guardrails.

Do not upload, publish, schedule, edit public metadata, use YouTube Studio/API/browser automation, or mark the metadata as final. Re-review against actual final local assets and current platform/account policy before any future release-decision gate.

## 7. Render/Export QA Checklist

The approved local executions produced `reviews/render-export-qa.md` updates before any readiness claim. Minimum checks:

### Preflight before rendering

- Re-read `AGENTS.md`, `KNOWLEDGE.md`, this plan, `reviews/current-state.md`, `reviews/assembly-package.md`, `source/metadata.md`, `source/visual-overlay-motion-plan.md`, `subtitles/README.md`, and tracking CSVs.
- Confirm the 13 selected WAV paths exist and match the selected candidate IDs.
- Confirm final `.en.srt` and `.en.vtt` sidecars parse.
- Confirm no selected audio, order, gap, crossfade, bumper, visual, or metadata decision changed.
- Confirm the explicit local render/export execution gate is approved before creating any new or revised outputs.

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

- Render-05 local QA is user-approved; any future release decision still needs a separate release gate and current platform/account/policy review.
- Subtitle readability review in the actual rendered context.
- Visual crop/readability review on target viewports.
- Fresh readiness score decision; do not raise `96/100` without new final-output evidence and explicit score review.

## 8. Stop Conditions

Stop and re-plan before any additional local render/export execution if any of these change:

- selected audio candidate, duration, order, gap, crossfade, bumper, or trim policy;
- subtitle sidecar timing, text, Track 13 exclusion, or language policy;
- V6 visual direction, overlay placement, crop/safe-zone evidence, font availability, or motion behavior;
- metadata/disclosure wording, chapter source, or forbidden-claim boundary;
- provenance, account, credential, provider, platform, rights, or release assumptions;
- source docs conflict with manifest, current-state, or tracking CSVs;
- user requests actual render/export without naming the local execution scope and stop conditions.
- any future corrected sidecars need to be copied or burned into a new QA output; this requires a new explicit local render gate.

## 9. Verdict

```text
Verdict: render_05_local_qa_user_approved_release_blocked
Scope: local render/export input map, ignored output targets, render-01 fail record, render-02/render-03/render-04 supersession, and render-05 QA result only
Timeline target: selected Tracks 1-13 with 12 x 1.00s gaps for planned 41:43.28 duration
Subtitle target: promoted final English en.srt and en.vtt sidecars carried forward source-only with Track 1 cue 58 text corrected
Visual target: V6 cute-smooth direction carried forward with render-05 sampled local output checks and full human QA required later
Readiness score: remains 96/100 internal readiness
Outputs created by approved local gates: render-01 ignored outputs superseded by human visual FAIL; render-02 ignored outputs superseded by render-03; render-03 ignored outputs superseded by render-04; render-04 ignored outputs superseded for corrected subtitle QA by render-05; render-05 ignored WAV timeline, per-song segment MP4s, final QA MP4, sidecar copies, and sampled PNG snapshots under candidates/
Next allowed action: separate release-decision planning gate if the user wants to move beyond local QA
Still blocked: additional/revised render/export output creation beyond render-05 without a new gate, upload/publish, provider/account/API/browser actions, Content ID registration, positive rights/platform claims
```

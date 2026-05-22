# S01E01 Visual Layout Proof Review

Status: v1_v3_rejected_v4_07_rejected_v5_revised_v6_visual_passed_source_only_subtitle_improvement_open  
Updated: 2026-05-22

## Boundary

This review records local static layout proof mockups, summarized AGY visual reviews, and user-requested local animated proof iterations. It does not approve full video assembly, full render/export, upload/publish, provider/API/browser/account action, release readiness, or rights/platform-safety claims. Candidate/proof media remain ignored local evidence under `candidates/`.

## Local Proof Set V1

- Background: `candidates/s01e01-campus-cafe-longplay/visual/G.png` as `vis-c01`.
- Generator script: `scripts/create_visual_layout_mockups.py`.
- Output root: `candidates/s01e01-campus-cafe-longplay/visual/proofs/static-layout-mockups/`.
- Contact sheet: `candidates/s01e01-campus-cafe-longplay/visual/proofs/static-layout-mockups/s01e01-vis-c01-layout-contact-sheet.png`.
- Static layout mockups created: 8 PNG files.

The V1 mockups include the required static components: channel plus S01E01, episode title, mood tagline, current song title, lyric subtitle sample, equalizer shape, warm particles, and the `G.png` background.

User verdict on V1: rejected all layouts. Required changes: remove text boxes, remove drop-shadow treatment, make text glow/stroke match the background, use more suitable line/dot accents, center subtitles in the left blank area below the title, move now-playing and song title to the lower-left at smaller scale, reduce title scale, create more breathing room, try a bar equalizer as the background/companion for now-playing, use cuter typography, and make text feel embedded in the picture rather than floating UI.

## Layouts Created

| Layout | File | Equalizer | Track-title behavior represented | Local note |
|---:|---|---|---|---|
| 01 | `s01e01-vis-c01-layout-01-editorial-left.png` | wave | fade-out card | Best local balance: strong left hierarchy and subtitle readability. |
| 02 | `s01e01-vis-c01-layout-02-compact-open-lower.png` | bars | fade-out card | More compact title; slightly more player-like due bar equalizer. |
| 03 | `s01e01-vis-c01-layout-03-soft-sidebar.png` | bars | persistent/sidebar | Readable but too much UI container weight for a calm longplay. |
| 04 | `s01e01-vis-c01-layout-04-floating-center-card.png` | wave | fade-out center card | Tests center motion, but risks covering character/story details. |
| 05 | `s01e01-vis-c01-layout-05-bottom-ribbon.png` | bars | persistent/ribbon | High contrast but bottom-heavy and less airy. |
| 06 | `s01e01-vis-c01-layout-06-window-corner-title.png` | wave | fade-out corner card | Tests top-right title position; risks subject interference. |
| 07 | `s01e01-vis-c01-layout-07-chapter-rail.png` | bars | fade-out card plus rail | Premium chapter feel; needs warmer equalizer treatment. |
| 08 | `s01e01-vis-c01-layout-08-circle-equalizer.png` | circle | fade-out card | Useful equalizer experiment, but center-right placement competes with subject. |

## AGY Supplemental Review Summary V1

AGY review was run from a fresh temp directory outside the repo with `agy --sandbox --print`, using absolute `@` image references. No install, migration, auth change, repo-root run, or auto-edit permission was used. The raw model output is not stored in the repo; this section records the durable summary only.

AGY selected:

- Winner: Layout 01, `Editorial left stack`.
- Runner-up: Layout 07, `Chapter rail`.

Key findings:

- High severity: Layouts 04 and 08 place UI too close to the subject's hair, shoulder, or writing area. Keep key UI in the left margin.
- High severity: song title should fade out after a short hold. Persistent full-song title cards increase fatigue and feel like a player UI over a longplay.
- Medium severity: bar equalizers in Layouts 02, 03, 05, and 07 feel too technical. The organic wave in Layout 01 better fits the cozy hand-drawn mood.
- Medium severity: lyric subtitles need a semi-transparent cream backing because backpack sketch lines can reduce readability.
- Low severity: stacked episode title has stronger editorial weight than single-line title treatment.

AGY concrete recommendations:

- Use Layout 01 as the primary direction.
- After each track title fades out, let the lyric card gently move upward by about 20-30 px to close the gap.
- Keep the equalizer as a slow, low-amplitude organic wave rather than sharp bars.
- Increase subtitle card opacity slightly, about 5%, while keeping the charm visible.
- If using Layout 07 as the alternate, replace bars with the Layout 01 wave or a much smaller sunburst/circle motif and reduce rail opacity.

## V2 Response And AGY Review

V2 output root: `candidates/s01e01-campus-cafe-longplay/visual/proofs/static-layout-mockups-v2/`.

V2 changes applied: removed text boxes, replaced directional drop shadows with centered warm glow/stroke, reduced title scale, added line/dot accents, centered subtitles in the left blank field, moved now-playing to the lower-left, tried bar equalizer beds, and tested serif/rounded/hand-soft typography.

AGY V2 findings:

- High severity: bar equalizer collided with now-playing text in most V2 variants, reducing legibility.
- Medium severity: lower-left now-playing still sat too close to backpack/charm details.
- Strongest V2 layouts: `v2-03-hand-subtitle` for typography/subtitle placement and `v2-08-hand-soft` for legibility/organic accents.
- V3 direction: merge V2-03/V2-08, keep handwritten subtitle, and separate the bar equalizer from text rather than layering text over bars.

## V3 Static Layout Set

V3 output root: `candidates/s01e01-campus-cafe-longplay/visual/proofs/static-layout-mockups-v3/`.

V3 contact sheet: `candidates/s01e01-campus-cafe-longplay/visual/proofs/static-layout-mockups-v3/s01e01-vis-c01-layout-v3-contact-sheet.png`.

| Layout | File | Equalizer | Local note |
|---:|---|---|---|
| 01 | `s01e01-vis-c01-layout-v3-01-hand-right-bars.png` | right-side bars | V2-03 typography with separated bars to the right of song info. |
| 02 | `s01e01-vis-c01-layout-v3-02-hand-under-bars.png` | under-title bars | Bars act as a progress texture below song title instead of cutting text. |
| 03 | `s01e01-vis-c01-layout-v3-03-low-right-bars.png` | low-right bars | Moves song info up and bars lower-right to protect charm/backpack detail. |
| 04 | `s01e01-vis-c01-layout-v3-04-centered-hand.png` | right-side bars | Centers title/subtitle in the left blank field with extra line/dot rhythm. |
| 05 | `s01e01-vis-c01-layout-v3-05-soft-center-under.png` | under-title bars | Airier centered title plus separated lower-left equalizer. |
| 06 | `s01e01-vis-c01-layout-v3-06-minimal-wave.png` | wave | Lowest UI density and strongest organic fallback. |
| 07 | `s01e01-vis-c01-layout-v3-07-rounded-right-bars.png` | right-side bars | Cuter rounded title with separated bar equalizer. |
| 08 | `s01e01-vis-c01-layout-v3-08-hand-soft-right-bars.png` | right-side bars | V2-08-like hand-soft layout with requested bar equalizer restored without text collision. |

AGY V3 selected:

- Winner: `v3-08-hand-soft-right-bars` for dreamy/cozy-classic text integration and rounded warm bar equalizer.
- Runner-up: `v3-06-minimal-wave` for organic sketch-art consistency and zero collision risk.

AGY V3 remaining concerns:

- Right-side bar equalizers in `v3-01`, `v3-03`, `v3-07`, and `v3-08` should move about `10-15px` left or reduce width before animation to avoid backpack strap line collision when bars move.
- Subtitle framing lines should use shorter centered proportions like `v3-05` to avoid crowding the left negative space.
- If using `v3-06`, animate the wave as a gentle anchored string/ripple rather than a jagged digital bounce.

Post-AGY local adjustment applied: the right-side bar equalizer in the generator was shortened and nudged left before regenerating the V3 files, reducing the backpack strap collision risk called out by AGY.

User verdict on V3: rejected. Required reset: rebuild the layout around a top-left information block using the same serif family as the old `After Class, Gently` title, move the subtitle to the balanced middle-left blank area, and move the equalizer to the bottom-right as a quarter-circle brick/bar visualizer.

## V4 Static Layout Set

V4 output root: `candidates/s01e01-campus-cafe-longplay/visual/proofs/static-layout-mockups-v4/`.

V4 contact sheet: `candidates/s01e01-campus-cafe-longplay/visual/proofs/static-layout-mockups-v4/s01e01-vis-c01-layout-v4-contact-sheet.png`.

V4 user-specified structure:

- Top-left: vector headphone icon, `MELLOW LONGPLAY`, dot, `S01 - E01`, then `Now Playing`, current song title, long line, terminal dot.
- Top-left font: `NewYork` serif, matching the previous `After Class, Gently` title family.
- Middle-left: subtitle only, centered in the blank left area and moved slightly upward for balance.
- Bottom-right: quarter-circle visual equalizer built from brick/bar segments with curved spacing, planned to move with song rhythm later.
- No title/tagline block, no text boxes, no directional drop shadows.

| Layout | File | Local note |
|---:|---|---|
| 01 | `s01e01-vis-c01-layout-v4-01-balanced-quarter.png` | Balanced baseline: medium quarter-brick equalizer, subtitle centered slightly above mid-left. |
| 02 | `s01e01-vis-c01-layout-v4-02-higher-subtitle-wide-arc.png` | Subtitle higher; wider, softer quarter arc. |
| 03 | `s01e01-vis-c01-layout-v4-03-serif-subtitle-tight-arc.png` | Full serif subtitle; tighter quarter arc. |
| 04 | `s01e01-vis-c01-layout-v4-04-compact-header-left-arc.png` | More compact header; equalizer shifted left for motion clearance. |
| 05 | `s01e01-vis-c01-layout-v4-05-airy-wide-arc.png` | Airier layout; larger faint equalizer texture. |
| 06 | `s01e01-vis-c01-layout-v4-06-lower-subtitle-dense-arc.png` | Lower subtitle test; denser quarter-brick equalizer. |
| 07 | `s01e01-vis-c01-layout-v4-07-user-reference-match.png` | Closest match to the user-supplied reference: larger separated headphone icon, vertical divider, one-line NewYork Italic subtitle, ornament, and larger off-canvas quarter equalizer. |

Mayr local read after the user reference check: `v4-07-user-reference-match` best matches the requested composition. `v4-01-balanced-quarter` remains a cleaner minimal fallback, and `v4-04-compact-header-left-arc` remains the safer motion-clearance fallback if the large equalizer needs more room. User lock is still pending.

## AGY Supplemental Review Summary V4

AGY review was run from a fresh temp directory outside the repo with `agy --sandbox --print`, using absolute `@` image references for the V4 contact sheet and all seven V4 PNG proofs. No install, migration, auth change, repo-root run, or auto-edit permission was used. The raw model output is not stored in the repo; this section records the durable summary only.

AGY selected:

- Winner: `v4-07-user-reference-match`.
- Reason: it is the only V4 candidate that satisfies the supplied reference structure: separated headphone icon, vertical divider, serif header, `Now Playing`, one-line NewYork Italic subtitle, ornament, and large off-canvas quarter equalizer.

AGY key findings:

- High confidence: the local generator can create this static proof with the existing Python/PIL workflow; no external rendering API or browser service is required for the static image.
- Medium production risk: the bottom-right equalizer overlays foreground foliage. If animated, bars should stay low-amplitude or be masked/layered so they do not fight the leaves, table, cup, or notebook.
- Medium production risk: the generator currently depends on macOS system fonts such as `NewYork.ttf`, `NewYorkItalic.ttf`, and `Noteworthy.ttc`; another render machine may silently fall back unless fonts are bundled or paths are controlled.
- Low risk: subtitle and ornament sit cleanly in the middle-left negative space above the backpack and do not cover the character, cup, notebook, or charm in the static proof.

## Mayr Current Recommendation

The V3 recommendation is superseded by the user rejection. The later V4-07 animated proof was also rejected by the user, and V5 was revised again after user feedback. Current accepted visual direction is V6 cute-smooth motion proof, source-only:

- Top-left information block replaces the old large title/tagline block and keeps the separated icon/divider structure from the user reference.
- Header stays visible after fade-in; track title slides in/out from behind the vertical divider.
- Subtitle stays in the middle-left blank area with timed Track 1 proof cues and readable cute typography.
- Bottom-right equalizer uses a subdued soft waveform/ribbon with honey dots and smoothed audio energy instead of brick bars.
- Motion uses near-still parallax, soft particles, steam, light sweep, and subtle local hair/leaf movement.
- Keep no text boxes and no directional text shadows.

The V1 Layout 01 and V3 recommendations are historical only and superseded by the user's V4 reset request.

## V4-07 Short Animated Proof

User request: after the AGY-reviewed V4-07 static proof, the user approved trying a short local animated proof.

Proof output: `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v4-07/s01e01-vis-c01-v4-07-animated-proof-15s-01.mp4`.

Snapshot evidence: `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v4-07/s01e01-vis-c01-v4-07-animated-proof-15s-01-snapshot-03s.png`.

Script: `scripts/create_v4_07_animated_proof.py`.

Observed proof facts:

- Duration: `15.0s`.
- Video: H.264, `1920x1080`, `24fps`.
- Audio: AAC from selected Track 1 excerpt, `aud-t01_c02--margin-notes-at-table-three.wav`.
- Motion: top-left block fades in, subtitle/ornament fade in, warm particles drift, and the bottom-right quarter equalizer pulses at conservative low amplitude from Track 1 audio energy.

Boundary: this is a local animated proof only. It is not full assembly, final subtitle timing, full render/export, upload/publish, release readiness, or a rights/platform-safety claim.

User review of V4-07 animated proof: rejected/revise. Required changes:

- Keep the header, but change fonts; the previous typography was too hard to read.
- Keep decorative styling only on `Now Playing`; use more suitable readable fonts for other text.
- Replace the headphone icon with a better vector-style icon.
- Make subtitles follow the song instead of staying static.
- Redesign the visual equalizer completely.
- Make motion effects more interesting.

## V5 Readable-Motion Proof

V5 proof output: `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v5/s01e01-vis-c01-v5-readable-motion-proof-30s-01.mp4`.

V5 snapshot evidence:

- `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v5/s01e01-vis-c01-v5-readable-motion-proof-30s-01-snapshot-02s.png`
- `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v5/s01e01-vis-c01-v5-readable-motion-proof-30s-01-snapshot-06s.png`
- `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v5/s01e01-vis-c01-v5-readable-motion-proof-30s-01-snapshot-14s.png`
- `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v5/s01e01-vis-c01-v5-readable-motion-proof-30s-01-snapshot-24s.png`

Script: `scripts/create_v5_readable_motion_proof.py`.

Observed V5 proof facts:

- Duration: `30.0s`.
- Video: H.264, `1920x1080`, `24fps`.
- Audio: AAC from selected Track 1 excerpt, `aud-t01_c02--margin-notes-at-table-three.wav`.
- Typography: full header is retained; header/track title/subtitles use more readable sans fonts; decorative font is kept only for `Now Playing`.
- Icon: original line-vector headphone icon replaces the blocky filled icon.
- Subtitles: timed proof cues from Track 1 lyric lines fade in/out across the first 30 seconds.
- Equalizer: brick/quarter bars are replaced by a lower-right soft waveform/ribbon with honey dots and thin curves.
- Motion: subtle parallax, drifting particles, cup steam, light sweep, timed subtitles, and audio-reactive waveform.

Boundary: this is a local animated proof only. User visual pass is not final subtitle timing, full assembly, full render/export, upload/publish, release readiness, or a rights/platform-safety claim.

User review of V6: pass as the visual direction source-only. Residual issue: subtitles in the V6 proof are not aligned closely enough to the sung vocal and some cue chunks are too long. That issue is moved to `reviews/subtitle-improvement.md` and `subtitles/README.md`; it does not reopen the visual layout/motion proof gate.

User review of V5: revise. Required changes:

- Use a cuter prettier font that fits the image while keeping non-decorative text readable.
- Keep the header present through the proof.
- Make parallax extremely slow, nearly imperceptible.
- Add subtle image-native motion where feasible, especially hair or leaves.
- Smooth the equalizer more against the audio.
- Make the track title slide in and out from the left at the vertical divider.

## V6 Cute-Smooth Motion Proof

V6 proof output: `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v6/s01e01-vis-c01-v6-cute-smooth-motion-proof-30s-01.mp4`.

V6 snapshot evidence:

- `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v6/s01e01-vis-c01-v6-cute-smooth-motion-proof-30s-01-snapshot-02s.png`
- `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v6/s01e01-vis-c01-v6-cute-smooth-motion-proof-30s-01-snapshot-06s.png`
- `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v6/s01e01-vis-c01-v6-cute-smooth-motion-proof-30s-01-snapshot-14s.png`
- `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v6/s01e01-vis-c01-v6-cute-smooth-motion-proof-30s-01-snapshot-24s.png`
- `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v6/s01e01-vis-c01-v6-cute-smooth-motion-proof-30s-01-snapshot-29s.png`

Script: `scripts/create_v6_cute_smooth_motion_proof.py`.

Observed V6 proof facts:

- Duration: `30.0s`.
- Video: H.264, `1920x1080`, `24fps`.
- Audio: AAC from selected Track 1 excerpt, `aud-t01_c02--margin-notes-at-table-three.wav`.
- Typography: full header is retained and uses cute readable local font fallbacks; decorative styling remains limited to `Now Playing`.
- Icon: original anti-aliased line-vector headphone icon replaces the prior blocky icon.
- Subtitles: timed proof cues from Track 1 lyric lines fade in/out across the first 30 seconds.
- Equalizer: lower-right waveform/ribbon uses smoothed audio energy with honey dots and thin curves; it remains secondary to subtitles.
- Motion: near-still parallax, drifting particles, cup steam, light sweep, subtle local hair/leaf movement, and title slide-in/out from the vertical divider.

Boundary: this is a local animated proof only. It is not final subtitle timing, full assembly, full render/export, upload/publish, release readiness, or a rights/platform-safety claim.

## Next Action

Recommended next step is subtitle improvement for vocal alignment and shorter cue segmentation. Any revised/longer visual proof still requires explicit direction and would not be full assembly, render/export, upload, or release approval.

## Still Blocked

Additional animated proof creation unless separately approved, final subtitle timing, full video assembly, full render/export, upload/publish, provider/browser/API/account automation, credentials, Content ID action, and rights/platform-safety claims remain blocked.

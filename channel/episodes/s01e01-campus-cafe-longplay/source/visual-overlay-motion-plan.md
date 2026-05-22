# S01E01 Visual Overlay Motion Plan

Status: source-only v6 visual direction passed / crop proof recorded / final assembly blocked  
Episode: `s01e01-campus-cafe-longplay`  
Updated: 2026-05-22

## Boundary

This file defines overlay placement and motion timing for a future local proof only. It does not approve image generation, video render/export, upload/publish, provider/API/browser/account action, release readiness, or rights/platform-safety claims.

## Inputs

- Background direction: `candidates/s01e01-campus-cafe-longplay/visual/G.png` as `vis-c01` in `reviews/visual-candidate-intake.md`.
- Image facts observed locally: PNG, `1672x941`, near 16:9.
- Header copy: `[line-vector headphone icon] MELLOW LONGPLAY . S01 - E01`.
- Now-playing label: `Now Playing`.
- Song title source: `source/songs.md` track titles, displayed as `01 - Margin Notes at Table Three` style copy.
- Subtitle source: Gate 10 draft timings are human watch-passed source-only; `reviews/assembly-package.md` defines planned final sidecar targets; final subtitle sidecars still require a separate sidecar promotion gate.

## Recommended Layout For G.png

Coordinate reference: design at `1920x1080`, scale proportionally for final output.

| Layer | Position | Styling | Reason |
|---|---|---|---|
| Top-left info block | x `86-112`, y `82-96`, max width `720` | `NewYork` serif; warm dark brown; vector headphone icon; uppercase channel/episode line; `Now Playing`; current song title; long dash rule ending with dot | Replaces old large title/tagline system and matches the user-requested `After Class, Gently` title family. |
| Lyrics subtitle | x `165-210`, y `455-505`, max width `850` | 42-50 px serif or soft sans, warm dark brown, 1-2 lines, centered warm glow/stroke only when needed | Uses the balanced middle-left blank field and stays slightly above center for visual weight. |
| Quarter equalizer | bottom-right origin around x `1650-1750`, y `900-980` | honey-brown rounded brick/bar segments on a quarter-circle arc, 34-58% opacity | Keeps motion away from the header and subtitle while feeling like a decorative music motif. |
| Particles | full frame, denser near window light and left negative space | warm dust motes, small bokeh specks, no hard resets | Creates continuous atmosphere without interrupting lyrics. |

## Now-Playing Behavior

| Element | Behavior | Verdict |
|---|---|---|
| Top-left `Now Playing` title | Persists as a small record-sleeve annotation and updates at each track boundary. | Current V4 direction. |
| Separate large track title card | Do not use by default. | Superseded by V4 because it would compete with the middle-left subtitle. |
| Micro chapter marker | Not needed while the top-left song number is visible. | Reserve only if later proof review shows orientation is weak. |

Current proof after user review of V4-07 and V5: use V6 cute-smooth motion direction as the user-passed visual direction source-only. It keeps the full header, uses cute readable header/track/subtitle fonts, keeps decorative styling only on `Now Playing`, replaces the blocky headphone icon with an original anti-aliased line-vector icon, uses timed Track 1 proof subtitle cues, replaces the brick equalizer with a soft smoother waveform/ribbon equalizer, slows parallax to near-still, adds subtle local hair/leaf motion, holds the header through the proof, and demonstrates track-title slide-in/out from the vertical divider. Current proof: `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v6/s01e01-vis-c01-v6-cute-smooth-motion-proof-30s-01.mp4`. Gate 10 subtitle timing is source-passed with human-watch-passed draft timings and `reviews/assembly-package.md` defines planned final sidecar targets, but final sidecars remain blocked until a separate sidecar promotion gate.

## Crop / Safe-Zone Carry-Forward

Local crop/safe-zone proof sheets are recorded as ignored local evidence:

- `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v6/s01e01-vis-c01-v6-crop-safe-zone-proof-sheet-01.png`
- `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v6/s01e01-vis-c01-v6-downscale-readability-proof-sheet-01.png`

For the source-only assembly package and any future render/export planning, preserve the V6 visual language but enforce a conservative crop-safe carry-forward rule: keep critical header/title text within a target-safe inset unless a fresh proof shows the target output is safe. Use the proof sheets to check the top-left header, middle-left subtitles, and lower-right equalizer before final sidecar promotion or render/export planning.

This proof narrows the crop/readability caveat for source planning, but it is still not full-episode assembly QA, final subtitle sidecar QA, render/export approval, upload approval, or rights/platform-safety evidence.

For the V4 treatment, do not use subtitle backing cards by default. Use a centered warm glow/stroke on the text and only add a backing haze if an animated proof shows lyric readability failure. The old lower-left now-playing/equalizer direction is superseded.

## Recommended Motion Timing

### Episode Open

| Time | Motion |
|---:|---|
| `0.00-0.40s` | Background is already visible; particles are already drifting so the video does not feel like it starts from a dead still. |
| `0.40-1.40s` | Top-left information block fades in with a 4-6 px upward ease. |
| `1.40-7.80s` | Hold the top-left block steady. Quarter equalizer starts with low-amplitude smoothing in the bottom-right. |
| `7.80-15.00s` | Keep the Track 1 song title in the top-left `Now Playing` slot; no separate title card. |
| `15.00s+` | Subtitles become the main reading layer in the middle-left blank field. Keep top-left info, quarter equalizer, and particles secondary. |

### Each Later Track Start

Use the track start time `T` from the future final timeline.

| Time | Motion |
|---:|---|
| `T+0.00s` | No hard cut in particles. Equalizer continues and retimes to the new audio. |
| `T+0.00-T+0.80s` | Top-left `Now Playing` song number/title crossfades to the new track. |
| `T+0.80s+` | Subtitles remain the only large text layer until the next track. |

Track 13 caveat: because the selected audio has an opening-dialogue caveat, the top-left song-title crossfade should finish quickly if subtitles need to start immediately.

## Subtitle Motion

- Fade in each subtitle cue over `0.16-0.22s`; avoid bouncing, typewriter, karaoke syllable highlight, or large slide motion.
- Fade out over `0.10-0.16s` at cue end.
- Use 1-2 lines only; keep each cue short enough to follow the sung vocal without rushing. The subtitle improvement gate should prefer phrase-level chunks over long two-line blocks.
- If a lyric cue overlaps any non-subtitle overlay, subtitle wins. Reduce the competing overlay opacity or shorten its transition rather than pushing subtitles into the face/cup/notebook area.

## Equalizer Direction

Preferred style for V6: a soft bottom-right waveform/ribbon equalizer with honey dots and thin curves, not brick bars. It should pulse gently with smoothed audio energy while staying secondary to the timed subtitles and avoiding the face, cup, notebook, and charm.

AGY V4 production caution: the current `v4-07` equalizer overlaps foreground foliage in the static proof. If animated, keep amplitude conservative or use a foreground foliage mask/layering strategy so bars do not visually fight the leaves, table edge, cup, notebook, or charm.

Motion rules:

- Use smoothed RMS or band energy rather than raw jitter.
- Attack: `0.10-0.16s`.
- Release: `0.35-0.55s`.
- Maximum bar extension: about `34-48px` from each quarter-arc segment in static layout scale; never pulse into subtitles, face, cup, notebook, or charm.
- Keep opacity below subtitles; the equalizer should feel like moving sunlight, not a music-player UI.
- Avoid placing bars directly under song-title letterforms; V4 separates equalizer motion into the bottom-right to prevent legibility failure.

Font implementation note: the current local proof uses macOS system font fallbacks such as `ChalkboardSE.ttc`, `MarkerFelt.ttc`, and `Avenir Next.ttc`. Bundle or otherwise pin fonts before relying on identical output from another OS/render node.

## Particle Direction

Preferred style: visible warm dust motes and tiny honey light particles drifting through the window light.

Motion rules:

- Continuous loop across the whole longplay with deterministic seed and no reset at track boundaries.
- Drift speed: slow, about `3-8px/s` with subtle parallax.
- Brightness gently breathes with long musical energy only; no beat-synced flashes.
- Avoid particles crossing the subtitle baseline at high opacity.
- Keep particles most visible in the upper-left negative space and window glow, less visible over the face.

## Copy Direction

Primary top-left information system:

```text
[headphone icon] MELLOW LONGPLAY . S01 - E01
Now Playing
01 - Margin Notes at Table Three
---------------------------------------------- .
```

Psychology basis: the copy now behaves like a quiet record sleeve annotation rather than a large title card. It keeps orientation visible without competing with the middle-left lyric subtitle.

## Still Blocked

- Full video assembly.
- Final subtitle timing.
- Render/export.
- Upload/publish planning.
- Provider/account/API/browser automation.
- Rights/platform-safety or release-readiness claims.

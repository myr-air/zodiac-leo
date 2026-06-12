# S01E05-APARTMENT-WINDOW-LONGPLAY Suno Manual Fields — Apartment Window Longplay

Status: source-only fields synced for all 13 tracks / not ready for provider use / source-only
Updated: 2026-06-09

This index records the episode-level suno-ready structure for future source-only handoff. It does not approve provider operation, generated audio, candidate IDs, or media release.

Provider/browser/API/account actions and generated audio remain blocked until a separate explicit gate.

## Episode Style & Theme Spine

- **Listener job:** Relaxed evening/late-night listening for quiet study, journaling, late-night tea, winding down, and solitary thinking in a city apartment.
- **Theme thesis:** Solitary spaces in the city feel warm when filled with small familiar habits: kettle steam, window reflections, tea cups, bookshelf outlines, and passing headlights below. Independence is not lonely; missing someone is soft, comforting, and full of quiet hope without melodrama.
- **Base `Styles` lane:** cozy chill vocal, soft R&B / lofi city-pop blend, warm electric keys, clean guitar, rounded bass, soft room-reverb drums (with brush or light shaker), airy pads, patient chorus motion, and subtitle-friendly lyric pacing.
- **BPM lane:** Overall about 75-88 BPM; opener/closer 75-80, middle arc 80-86, one brighter lift up to 88.
- **Vocal lane:** Natural adult/young-adult female vocal, warm and intimate without childlike framing or named-voice imitation.
- **Base `Exclude Styles`:** auto-generated lyrics, lyric rewrite, named-artist imitation, known-song imitation, real school or school-brand naming, trap, aggressive rap, EDM drop, hard rock, busy jazz soloing, orchestral drama, saxophone, novelty or childlike vocal, sexualized framing, teacher-student romance, adult-minor framing, rights/platform claims.
- **Control baseline:** Weirdness 10-14%; Style Influence 82% unless a track-specific review approves a change.
- **Reserved variation slot:** Track 6 is the only planned **warm, intimate cello** color. It must stay secondary and emotionally supportive. No other track may claim an additional special spotlight instrument.

## Handoff Readiness

Before any manual provider handoff, every track must have a reviewed file under `source/suno-tracks/` with:
`Song Title`, `Lyrics Mode`, `Lyrics`, `Styles` (+ approximate BPM), `Exclude Styles`, `Vocal Gender`, `Weirdness`, `Style Influence`, and `Reject Criteria`.

## Track Files (synced)

1. `source/suno-tracks/01-corner-glow.md` — source_only_fields_synced_no_provider_approval
2. `source/suno-tracks/02-steam-rising.md` — source_only_fields_synced_no_provider_approval
3. `source/suno-tracks/03-reflections-on-glass.md` — source_only_fields_synced_no_provider_approval
4. `source/suno-tracks/04-gravel-and-glow.md` — source_only_fields_synced_no_provider_approval
5. `source/suno-tracks/05-a-folded-corner.md` — source_only_fields_synced_no_provider_approval
6. `source/suno-tracks/06-deep-strings.md` — source_only_fields_synced_no_provider_approval
7. `source/suno-tracks/07-kitchen-timer.md` — source_only_fields_synced_no_provider_approval
8. `source/suno-tracks/08-city-bokeh.md` — source_only_fields_synced_no_provider_approval
9. `source/suno-tracks/09-shelved-spines.md` — source_only_fields_synced_no_provider_approval
10. `source/suno-tracks/10-shadows-on-the-wall.md` — source_only_fields_synced_no_provider_approval
11. `source/suno-tracks/11-the-keys-by-the-door.md` — source_only_fields_synced_no_provider_approval
12. `source/suno-tracks/12-warm-fabric.md` — source_only_fields_synced_no_provider_approval
13. `source/suno-tracks/13-bonus-winding-down.md` — source_only_fields_synced_no_provider_approval

## Planned Parameter Matrix

| # | Working title | Planned BPM in Styles | Weirdness | Style Influence | Track Delta | Handoff readiness |
|---:|---|---:|---:|---:|---|---|
| 1 | Corner Glow | 78 | 12% | 82% | Opener with lamp-warming light-spine object anchor. | source_only_fields_synced_no_provider_approval |
| 2 | Steam Rising | 82 | 12% | 82% | Adds tactile mug steam and early hook placement. | source_only_fields_synced_no_provider_approval |
| 3 | Reflections on Glass | 80 | 12% | 82% | Double-view reflections on pane, short verse-first shape. | source_only_fields_synced_no_provider_approval |
| 4 | Gravel and Glow | 84 | 12% | 82% | Sweeping yellow flare on ceiling, mid-verse texture pivot. | source_only_fields_synced_no_provider_approval |
| 5 | A Folded Corner | 86 | 12% | 82% | Paper fold in journal, bridge carries emotional shift. | source_only_fields_synced_no_provider_approval |
| 6 | Deep Strings | 79 | 10% | 82% | Cozy cello counterline + gentle guitar, cello spotlight bridge. | source_only_fields_synced_no_provider_approval |
| 7 | Kitchen Timer | 85 | 12% | 82% | Mechanical ticking, brighter groove, two-part hook. | source_only_fields_synced_no_provider_approval |
| 8 | City Bokeh | 83 | 12% | 82% | Blurry rain droplets, call-and-response refrain. | source_only_fields_synced_no_provider_approval |
| 9 | Shelved Spines | 81 | 12% | 82% | Rows of paperbacks, sparse chorus, image-driven pause. | source_only_fields_synced_no_provider_approval |
| 10 | Shadows on the Wall | 82 | 12% | 82% | Moving tree silhouette shadows, late-night calmness. | source_only_fields_synced_no_provider_approval |
| 11 | The Keys by the Door | 87 | 12% | 82% | Entryway key ring drop, emotional arc tilts toward vulnerability. | source_only_fields_synced_no_provider_approval |
| 12 | Warm Fabric | 84 | 12% | 82% | Cozy knitted blanket on chair, wide chorus, open ending. | source_only_fields_synced_no_provider_approval |
| 13 | Winding Down | 76 | 12% | 82% | Closer with desk lamp click off, quiet skyline reflection. | source_only_fields_synced_no_provider_approval |

## Review Blockers Before Handoff

- Missing lyrics, missing `source/suno-tracks/*.md`, missing explicit BPM in `Styles`, missing Lyrics Mode, missing Vocal Gender, missing Weirdness, or missing Style Influence.
- Repeated title-first chorus grids, `No big...`, `Maybe...`, `Nothing...`, `No ..., no ...`, or `one small/soft note/sign/line` payoffs.
- More than one cello-forward spotlight track.
- Named-reference collision in title, lyrics, `Styles`, or `Exclude Styles`.
- Any missing sub-theme / mini-story evidence, melody-contour plan, or rhythm/groove direction.
- Any provider/media/render/upload/release or rights/platform-safety claim.

# S01E06-CROSSWALK-EVENING-LONGPLAY Suno Manual Fields — Crosswalk Evening Longplay

Status: source-only fields synced for all 13 tracks / not ready for provider use / source-only
Updated: 2026-06-12

This index records the episode-level suno-ready structure for future source-only handoff. It does not approve provider operation, generated audio, candidate IDs, or media release.

Provider/browser/API/account actions and generated audio remain blocked until a separate explicit gate.

## Episode Style & Theme Spine

- **Listener job:** Relaxed evening commute/after-work study, journaling, late-night wind down, city walking background, cozy evening companion.
- **Theme thesis:** The city street at dusk is alive with rhythm and motion—passing headlights, glowing neon crosswalk signs, crosswalk walk/don't walk lights, footsteps on wet pavement, train platform chimes, and the soft hum of the evening commute. Amidst this bustling flow, two people cross paths or experience the quiet excitement of a first meeting. The feeling is warm, curious, rhythmic, and cozy, showing city life as a space of connection and quiet wonder.
- **Base `Styles` lane:** cozy chill vocal, soft R&B / lofi city-pop blend, warm electric keys (Rhodes/DX7), clean rhythmic guitar, rounded bass, soft room-reverb drums (with brush, light shaker, or gentle kick/snare lofi beat), airy pads, patient chorus motion, and subtitle-friendly lyric pacing.
- **BPM lane:** Overall about 76-88 BPM; opener/closer 76-80, middle arc 80-86, one brighter groove lift up to 88.
- **Vocal lane:** Natural adult/young-adult female vocal, warm and intimate without childlike framing or named-voice imitation.
- **Base `Exclude Styles`:** auto-generated lyrics, lyric rewrite, under 3 minutes, short sketch, abrupt ending, cut-off, named-artist imitation, known-song imitation, real school or school-brand naming, trap, aggressive rap, EDM drop, hard rock, busy jazz soloing, orchestral drama, saxophone, novelty or childlike vocal, sexualized framing, teacher-student romance, adult-minor framing, rights/platform claims.
- **Control baseline:** Weirdness 12%; Style Influence 82% unless a track-specific review approves a change.
- **Reserved variation slot:** Track 7 is the only planned **cozy mellow vibraphone** color. Vibraphone is our chosen non-sax special instrument. It must stay secondary and emotionally supportive. No other track may claim an additional special spotlight instrument.

## Handoff Readiness

Before any manual provider handoff, every track must have a reviewed file under `source/suno-tracks/` with:
`Song Title`, `Lyrics Mode`, `Lyrics`, `Styles` (+ approximate BPM), `Exclude Styles`, `Vocal Gender`, `Weirdness`, `Style Influence`, and `Reject Criteria`.

## Track Files (synced)

1. `source/suno-tracks/01-yellow-blink.md` — source_only_fields_synced_no_provider_approval
2. `source/suno-tracks/02-transit-chime.md` — source_only_fields_synced_no_provider_approval
3. `source/suno-tracks/03-reflections-on-asphalt.md` — source_only_fields_synced_no_provider_approval
4. `source/suno-tracks/04-to-go-warmth.md` — source_only_fields_synced_no_provider_approval
5. `source/suno-tracks/05-tapping-in.md` — source_only_fields_synced_no_provider_approval
6. `source/suno-tracks/06-edge-of-the-umbrella.md` — source_only_fields_synced_no_provider_approval
7. `source/suno-tracks/07-vibraphone-square.md` — source_only_fields_synced_no_provider_approval
8. `source/suno-tracks/08-bus-window-pane.md` — source_only_fields_synced_no_provider_approval
9. `source/suno-tracks/09-paper-bag-steam.md` — source_only_fields_synced_no_provider_approval
10. `source/suno-tracks/10-zebra-lines.md` — source_only_fields_synced_no_provider_approval
11. `source/suno-tracks/11-streetlamp-glow.md` — source_only_fields_synced_no_provider_approval
12. `source/suno-tracks/12-ticket-in-pocket.md` — source_only_fields_synced_no_provider_approval
13. `source/suno-tracks/13-the-door-key.md` — source_only_fields_synced_no_provider_approval

## Planned Parameter Matrix

| # | Working title | Planned BPM in Styles | Weirdness | Style Influence | Track Delta | Handoff readiness |
|---:|---|---:|---:|---:|---|---|
| 1 | Yellow Blink | 78 | 12% | 82% | Flashing warning crosswalk signal. Opener with curb-stepping object anchor. | source_only_fields_synced_no_provider_approval |
| 2 | Transit Chime | 82 | 12% | 82% | Metro card barrier swipe, metallic gate sound. | source_only_fields_synced_no_provider_approval |
| 3 | Reflections on Asphalt | 80 | 12% | 82% | Rain puddles reflecting red/blue neon signs, downward-looking gaze. | source_only_fields_synced_no_provider_approval |
| 4 | To-Go Warmth | 84 | 12% | 82% | Holding a warm paper coffee cup, simple comfort walk. | source_only_fields_synced_no_provider_approval |
| 5 | Tapping In | 86 | 12% | 82% | Stepping onto the bus and tapping transit card, upper deck bus view. | source_only_fields_synced_no_provider_approval |
| 6 | Edge of the Umbrella | 81 | 12% | 82% | Walking under clear vinyl umbrella, mist and rain droplets. | source_only_fields_synced_no_provider_approval |
| 7 | Vibraphone Square | 85 | 10% | 82% | Special instrument vibraphone solo and chorus bells, street player scene. | source_only_fields_synced_no_provider_approval |
| 8 | Bus Window Pane | 83 | 12% | 82% | Leaning head against bus glass pane, passing lights blur, breath fog. | source_only_fields_synced_no_provider_approval |
| 9 | Paper Bag Steam | 80 | 12% | 82% | Warm brown paper pastry bag, simple food sharing, intimate guitar. | source_only_fields_synced_no_provider_approval |
| 10 | Zebra Lines | 82 | 12% | 82% | Walking across white crosswalk stripes in sync, side-by-side walk. | source_only_fields_synced_no_provider_approval |
| 11 | Streetlamp Glow | 87 | 12% | 82% | Streetlamps flickering to life at dusk, sodium bulb hum. | source_only_fields_synced_no_provider_approval |
| 12 | Ticket in Pocket | 84 | 12% | 82% | Feeling folded paper ticket stub in coat pocket, nostalgia. | source_only_fields_synced_no_provider_approval |
| 13 | The Door Key | 76 | 12% | 82% | Key sliding into apartment lock, homecoming closer, piano-forward. | source_only_fields_synced_no_provider_approval |

## Review Blockers Before Handoff

- Missing lyrics, missing `source/suno-tracks/*.md`, missing explicit BPM in `Styles`, missing Lyrics Mode, missing Vocal Gender, missing Weirdness, or missing Style Influence.
- Repeated title-first chorus grids, `No big...`, `Maybe...`, `Nothing...`, `No ..., no ...`, or `one small/soft note/sign/line` payoffs.
- More than one vibraphone-forward spotlight track.
- Named-reference collision in title, lyrics, `Styles`, or `Exclude Styles`.
- Any missing sub-theme / mini-story evidence, melody-contour plan, or rhythm/groove direction.
- Any provider/media/render/upload/release or rights/platform-safety claim.

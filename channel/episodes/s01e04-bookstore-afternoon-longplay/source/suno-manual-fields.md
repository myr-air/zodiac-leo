# S01E04-BOOKSTORE-AFTERNOON-LONGPLAY Suno Manual Fields — Bookstore Afternoon Longplay

Status: source-only fields synced for all 13 tracks / not ready for provider use / source-only
Updated: 2026-06-05

This index records the episode-level suno-ready structure for future source-only handoff. It does not approve provider operation, generated audio, candidate IDs, or media release.

Provider/browser/API/account actions and generated audio remain blocked until a separate explicit gate.

## Episode Style & Theme Spine

- Listener job: browsing-to-reading calm for late afternoon reading breaks, writing moments, and quiet emotional check-ins.
- Theme thesis: private thoughts become clearer when small bookstore objects do the emotional work (paper, receipts, counter sounds, and soft light).
- Base `Styles` lane: cozy chill vocal, soft R&B / easy-listening city-pop, warm electric keys, clean guitar, rounded bass, soft brushed drums, airy pads, subtitle-friendly phrasing.
- BPM lane: about 74-92 BPM overall; main flow 80-88 BPM; opener/bonus 74-80 BPM.
- Vocal lane: natural adult/young-adult female vocal, soft intimacy, no named-voice imitation or childlike framing.
- Base `Exclude Styles`: named-artist imitation, known-song imitation, real school identity branding, trap, aggressive rap, EDM drops, orchestral drama, novelty vocal, rights/platform claims, provider/browser/API actions, content-safety exceptions.
- Control baseline: Weirdness 10-14%; Style Influence 82% unless a reviewed exception is approved.
- Reserved variation slot: Track 6 is the only planned **vintage upright piano** spotlight color.
- Review must confirm no second special instrument track appears before handoff.

## Handoff Readiness

Before any manual provider handoff, every track must have a reviewed file under `source/suno-tracks/` with:
`Song Title`, `Lyrics Mode`, `Lyrics`, `Styles` (+ approximate BPM), `Exclude Styles`, `Vocal Gender`, `Weirdness`, `Style Influence`, and `Reject Criteria`.

## Track Files (synced)

1. `source/suno-tracks/01-quiet-cover.md` — source_only_fields_synced_no_provider_approval
2. `source/suno-tracks/02-between-two-chapters.md` — source_only_fields_synced_no_provider_approval
3. `source/suno-tracks/03-tucked-in-the-drawer.md` — source_only_fields_synced_no_provider_approval
4. `source/suno-tracks/04-drifting-like-dust.md` — source_only_fields_synced_no_provider_approval
5. `source/suno-tracks/05-catching-orange-light.md` — source_only_fields_synced_no_provider_approval
6. `source/suno-tracks/06-steady-feelings.md` — source_only_fields_synced_no_provider_approval
7. `source/suno-tracks/07-a-rhythm-at-dusk.md` — source_only_fields_synced_no_provider_approval
8. `source/suno-tracks/08-no-need-to-rush.md` — source_only_fields_synced_no_provider_approval
9. `source/suno-tracks/09-quiet-shape-at-night.md` — source_only_fields_synced_no_provider_approval
10. `source/suno-tracks/10-pocket-of-shy-courage.md` — source_only_fields_synced_no_provider_approval
11. `source/suno-tracks/11-mist-on-the-window.md` — source_only_fields_synced_no_provider_approval
12. `source/suno-tracks/12-late-and-low-lamp.md` — source_only_fields_synced_no_provider_approval
13. `source/suno-tracks/13-bonus-last-bookstore-hour.md` — source_only_fields_synced_no_provider_approval

## Planned Parameter Matrix

| # | Working title | Planned BPM in Styles | Weirdness | Style Influence | Track Delta | Handoff readiness |
|---:|---|---:|---:|---:|---|---|
| 1 | Quiet Cover | 80 | 12% | 82% | Opener with ambient aisle-spine object anchor. | source_only_fields_synced_no_provider_approval |
| 2 | Between Two Chapters | 84 | 12% | 82% | Adds tactile page-turn anticipation and early hook placement. | source_only_fields_synced_no_provider_approval |
| 3 | Tucked in the Drawer | 78 | 11% | 82% | Turns timestamp object into emotional pause and restrained chorus. | source_only_fields_synced_no_provider_approval |
| 4 | Drifting Like Dust | 82 | 10% | 82% | Soft mechanical lift feel; texture-led transition move. | source_only_fields_synced_no_provider_approval |
| 5 | Catching Orange Light | 88 | 12% | 82% | Light-beam image turn with brighter pre-chorus. | source_only_fields_synced_no_provider_approval |
| 6 | Steady Feelings | 79 | 10% | 82% | Only upright piano-forward counterline; emotional bridge pivot. | source_only_fields_synced_no_provider_approval |
| 7 | A Rhythm at Dusk | 90 | 12% | 82% | Scanner-like rhythmic lift and two-part chorus role. | source_only_fields_synced_no_provider_approval |
| 8 | No Need to Rush | 86 | 11% | 82% | Rhythmic call-answer with quieter center-space. | source_only_fields_synced_no_provider_approval |
| 9 | Quiet Shape at Night | 84 | 11% | 82% | Window/light image in midpoint and restrained tempo arc. | source_only_fields_synced_no_provider_approval |
| 10 | Pocket of Shy Courage | 82 | 12% | 82% | Everyday object care moment with conversational hook function. | source_only_fields_synced_no_provider_approval |
| 11 | Mist on the Window | 87 | 11% | 82% | Mid-late emotional rise with warm pad density. | source_only_fields_synced_no_provider_approval |
| 12 | Late and Low Lamp | 84 | 12% | 82% | Peak emotional register, wide chorus with open ending. | source_only_fields_synced_no_provider_approval |
| 13 | Last Bookstore Hour | 78 | 10% | 82% | Bonus closer with reduced density and gentle fade. | source_only_fields_synced_no_provider_approval |

## Review Blockers Before Handoff

- Missing lyrics, missing `source/suno-tracks/*.md`, missing explicit BPM in `Styles`, missing Lyrics Mode, missing Vocal Gender, missing Weirdness, or missing Style Influence.
- Repeated title-first chorus grids, `No big...`, `Maybe...`, `Nothing...`, `No ..., no ...`, or `one small/soft note/sign/line` payoffs.
- More than one piano-forward spotlight track.
- Named-reference collision in title, lyrics, `Styles`, or `Exclude Styles`.
- Any missing sub-theme / mini-story evidence, melody-contour plan, or rhythm/groove direction.
- Any provider/media/render/upload/release or rights/platform-safety claim.

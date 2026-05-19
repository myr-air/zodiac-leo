# S01E01 Source Approval Workflow

Status: active source-only workflow log  
Updated: 2026-05-19

## Boundary

This workflow records source-only lyric and Suno field approval steps. It does not approve provider/browser/API/account action, generated media, render/export, upload/publish, or rights/platform claims.

## Per-Track Workflow

1. Read current episode state, guardrails, source, copy-pack, reviews, and tracking context.
2. Define or consume the Episode Style & Theme Spine before any song drafting: listener job, theme thesis, base sonic lane, BPM range, vocal lane, core instrumentation, reserved variation slots, motif/lexical budgets, and safety boundaries.
3. Define a Track Delta before lyrics: story function, object/action function, macro-form or rhetorical delta, style/BPM delta, and motif/lexical delta against the episode spine and nearby tracks.
4. Create a Story + Reference Brief before lyrics: scene, object/action, emotional beat, listener job, hook promise, ending image, and a 2-3 real-song reference triangle reduced to abstract traits only.
5. Draft the track through `songwriter` with title, object/action, arrangement lane, reference-safe abstract traits, episode spine fit, Track Delta, adjacent-track macro-form constraints, safety boundaries, and no file writes.
6. Send the draft to `lyric-reviewer`; revise until episode spine fit, Track Delta usefulness, reference safety, lyric quality, macro-form variety, micro-pattern variety, rhyme, singability, and PG safety pass.
7. Run a set-level pattern and lexical gate before sync: compare at least the previous three approved/proposed songs for title-repeat count per block, chorus shape, `No ..., no ...` or `No big...` usage, repeated `Maybe...`/`Nothing...` bridge openers, `one small/soft note/sign/line` payoffs, final-hook stacking, dominant nouns, repeated hook/payoff vocabulary, generic AI comfort words, and lexical count budgets. Any repeated template or stale vocabulary is `REVISE` unless it has a new scene function.
8. Send final lyrics and fields to `suno-reviewer`; revise until Suno 5.5 source fields, episode base style plus Track Delta, prompt hygiene, explicit BPM in `Styles`, controls, reject criteria, reference-safety, named-reference collision scan, lyric-pattern clearance, and lexical-freshness clearance pass.
9. After each lyric PASS, update `reviews/lyric-antipatterns.md` with the track's avoid-next list before drafting the next track.
10. Sync only after review pass or sync-only blocker: `source/songs.md`, the matching `source/suno-tracks/*.md`, area review docs, current state, manifest, tracking CSVs, and project knowledge when the episode summary changes.
11. Validate changed JSON/structure and run `bash scripts/verify-standalone.sh` after state/tracking changes.
12. Ask `work-verifier` to verify the final claim before reporting done/final/ready-for-source-review.

## Episode Style & Theme Spine Gate

- Every episode must define the style/theme spine before track concepts or lyrics are drafted.
- Required fields: listener job, emotional/theme thesis, base `Styles` lane, BPM range, vocal lane, core instrumentation, base exclusions, control baseline, allowed variation slots, motif/lexical budgets, and safety blockers.
- Track concepts and lyrics must not redefine the episode one song at a time; they must use the spine as the stable center.
- Each Track Delta should be narrow and intentional: a story/object function change, a hook or section-function change, a controlled BPM/style color, or a motif-function change.
- Return `REVISE` if a track has no delta, duplicates an adjacent track's delta, breaks the spine, or reuses reserved colors such as piano-forward or sax-accent without review.

## Story + Reference Brief Gate

- Use 2-3 real songs only as source-only inspiration anchors.
- Store only abstract takeaways: tempo feel, arrangement density, hook function, lyric camera distance, mood curve, and transition energy.
- Do not use named references in final Suno fields, lyrics, metadata, title hooks, or provider prompts.
- Do not copy melody, chords, lyrics, vocal tone, arrangement signatures, or artist identity.
- If reference influence is not transformed into original track-specific choices, the track is `REVISE`.

## Title/Arrangement Separation Gate

- Choose titles from story objects, actions, places, or emotional turns.
- Do not require instrument words in titles just because a track is piano-forward, sax-accented, guitar-led, or drum-forward.
- Keep arrangement labels in `Styles`, arrangement notes, and reject criteria.
- If an instrument title is not a real diegetic story object, retitle before approval.

## Title/Lyric Relationship Gate

- A title does not have to appear verbatim in the lyrics.
- Do not make the title the first hook line by default.
- Titles may work as mood labels, scene labels, object labels, or after-the-fact summaries.
- If the title is absent from lyrics, the lyric imagery must still earn it.
- If the title appears in lyrics, its placement must have a clear hook or payoff function.

## Strict Pattern Gate

Do not approve a track or set if the listener would hear the same template even though section labels differ. Blockers include:

- title repeated twice inside the same chorus/refrain block without a new function;
- multiple adjacent songs using `Title / image line / Title / payoff line` chorus shape;
- recurring `No ..., no ...`, `No big...`, `Maybe...`, or `Nothing...` rhetoric as emotional shorthand;
- repeated `one small/soft note/sign/line` or similar minimal-object payoff;
- same bridge opener or same final-hook stack across adjacent tracks;
- same title placement in four consecutive tracks.

## Lexical Freshness Gate

- Build a per-track avoid/budget list from at least the previous three tracks.
- Track repeated nouns, verbs, adjectives, and payoff words, not just section structures.
- For future episodes/new tracks, record a Lexical Count Ledger before approval: title plus sung lyrics, per song and cumulative episode counts, focused on high-salience nouns, pronouns, adjectives/adverbs, colors, object words, and hook/payoff terms.
- Include harmless-looking repeated words when they accumulate, including examples learned from S01E01 such as `tray`, `blue`, `ink`, plus pronoun/modifier load such as `you`, `my`, `your`, `soft`, and `warm`.
- Set a next-track budget from the ledger. If a nonessential token dominates one song or appears across multiple recent songs, reduce it in the next track, usually to 0-1 uses unless it has a new concrete scene function.
- Avoid repeated hook/payoff vocabulary unless the word is a necessary story object with a new action.
- Current overuse watchlist: `soft`, `quiet`, `small`, `little`, `gentle`, `warm`, `slow`, `line`, `sign`, `page`, `name`, `same`, `tomorrow`, `smile`, `light`, `street`, `door`, `glass`, `hand`, `walk`, `wait`, `close`, `after school`, `glow`, `dream`, `vibe`, `cosmic`, `destiny`.
- If the new track uses three or more watchlist words as emotional shorthand instead of scene mechanics, return `REVISE`.
- Do not revise S01E01 solely to satisfy this new ledger; carry the counting/budget rule into the next episode unless a separate revision task is explicitly opened.

## Antipattern Registry

- Maintain `reviews/lyric-antipatterns.md` as a source-only rolling guardrail.
- After each track review, append the next-track avoid list: title/hook shape, overused words, scene objects, final image, bridge opener, and arrangement trap.
- Treat active registry items as blockers unless the new track uses them with a clearly different scene function.

## Suno Styles BPM Gate

- Every final `Styles` field must include an explicit approximate BPM.
- Keep BPM cohesive across the longplay arc: lower for closers/bonus reprises, mid-slow for cozy study scenes, and only modestly brighter for lift tracks.
- Missing BPM, implausible BPM, or BPM that fights the track function is a Suno field `REVISE` before manual handoff.

## Run Log

| Date | Track | Version | Workflow result | Notes |
|---|---:|---|---|---|
| 2026-05-19 | 4 | `Piano Between Shelves` v1.0 | songwriter draft → lyric-reviewer REVISE/PASS → suno-reviewer sync-only REVISE/PASS → verification | Earlier instrument-led title; superseded by story-led retitle. |
| 2026-05-19 | 1-4 | pattern gate | user blocker recorded → stricter guardrails added | Track approvals are under set-level pattern review because title-repeat blocks and `No ..., no ...` style rhetoric made songs feel structurally same. Rewrite before Track 5/provider handoff. |
| 2026-05-19 | 4+ | reference gate | user approved reference-led story brief step | Tracks 1-3 are user-accepted as-is; Track 4 onward must start from Story + Reference Brief before lyrics. |
| 2026-05-19 | 4 | `Checkout Slip at Chapter Nine` v1.1 | title/arrangement separation → lyric-reviewer PASS → suno-reviewer PASS → source sync | Replaces instrument-led title while keeping Track 4 as the sole piano-forward arrangement color. |
| 2026-05-19 | 5+ | title/lyric gate | user clarified title need not appear in lyrics | Future tracks may use mood/object/scene titles without making the title the first hook line; lyric imagery must earn the title. |
| 2026-05-19 | 5 | `Steam on the Glass Door` v1.0 | Story + Reference Brief → title/lyric independence → lyric-reviewer PASS → suno-reviewer PASS → source sync | Exact title is absent from lyric; fogged glass/hand mark imagery earns the mood label. |
| 2026-05-19 | 6+ | lexical gate | user requested lower repeated/common AI wording | Future tracks must include a lexical avoid/budget list and reviewer lexical freshness matrix before PASS. |
| 2026-05-19 | 6+ | antipattern registry | user requested automatic next-song antipatterns | `reviews/lyric-antipatterns.md` records rolling avoid lists after each approved/reviewed track. |
| 2026-05-19 | 6 | `Bus Stop Receipt` v1.0 | lexical gate → lyric-reviewer PASS → suno-reviewer PASS → source sync | Track 6 owns bus-shelter receipt/route/rain-delay imagery; no media/provider approval. |
| 2026-05-19 | 6 reset | `Peach Can at B4` v1.0 | Mayr decision → lyric-reviewer REVISE/PASS → suno-reviewer planned-state PASS → source sync | Replaces `Bus Stop Receipt`; resets Tracks 7-13 to one-by-one review pending. |
| 2026-05-19 | 7 | `Two Taps in the Hallway` v1.0 | historical draft review superseded | Track 6 reset created a tap/button adjacency risk; superseded by `Green Dot on Your Schedule`. |
| 2026-05-19 | 7 reset | `Green Dot on Your Schedule` v1.0 | Mayr decision → lyric-reviewer PASS → Mayr hard-avoid cleanup → suno-reviewer planned-state PASS → source sync | Replaces `Two Taps in the Hallway`; resets Tracks 8-13 to one-by-one review pending. |
| 2026-05-19 | 8 | `Worn Fabric, Shared Charger` v1.0 | historical draft review superseded | Keep as draft only until one-by-one review after Track 7. |
| 2026-05-19 | 9 | `White Stripes Before Six` v1.0 | historical draft review superseded | Sax remains reserved as secondary accent, but Track 9 needs one-by-one sequence review after Tracks 7-8. |
| 2026-05-19 | 8 | `Cushion Seat, Charging Cord` v1.0 | songwriter draft → lyric-reviewer REVISE/PASS → suno-reviewer PASS → source sync | Replaces charger/corner draft; removes `Save...` hook echo and call-response number break. |
| 2026-05-19 | 9 | `Crosswalk Stripes Before Six` v1.0 | songwriter draft → lyric-reviewer REVISE/PASS → suno-reviewer REVISE/PASS → source sync | Replaces `White Stripes` wording to avoid named-reference collision; sax remains secondary accent only. |
| 2026-05-19 | 10 | `Yellow Tag on the Umbrella Rack` v1.0 | songwriter draft → lyric-reviewer REVISE/PASS → suno-reviewer PASS → source sync | Removes `Not a promise...`; tag is practical meeting marker, not title-hook. |
| 2026-05-19 | 11 | `Quiz Key in Blue Ink` v1.0 | songwriter draft → lyric-reviewer PASS → suno-reviewer PASS → source sync | Study-help quiz key scene with near-whisper break; no locker/title-hook pattern. |
| 2026-05-19 | 12 | `Tray Return at 5:59` v1.0 | songwriter draft → lyric-reviewer PASS → suno-reviewer PASS → source sync | Main-set closer with tray-return object and no finale bombast. |
| 2026-05-19 | 13 | `Latch Click at the Courtyard Gate` v1.0 | songwriter draft → lyric-reviewer REVISE/PASS → suno-reviewer PASS → source sync | Bonus closing uses dialogue-first gate-latch image; avoids `walk` title/hook and grand-forever claim. |
| 2026-05-19 | 1-13 | review lessons + BPM gate | full-set issues folded into songwriter/lyric-reviewer/suno-reviewer guardrails → BPM added to current Styles | Future drafts must apply issue ledger, named-reference collision scan, and explicit BPM in Styles. |
| 2026-05-19 | episode | style/theme spine gate | user preference recorded → skills/agents/workflow updated | Future episodes must define an Episode Style & Theme Spine before track drafting; every track must state a controlled Track Delta against the spine and nearby songs. |
| 2026-05-19 | future episodes | lexical count ledger gate | user preference recorded → skills/agents/workflow updated | Future songs must record per-song counts for high-salience nouns, pronouns, modifiers, colors, objects, and hook/payoff terms, then reduce budgeted repeats in following songs; S01E01 is not being revised for this. |

## Re-Review Triggers

Re-run this workflow if episode style/theme spine, Track Delta, lexical count ledger/budgets, lyrics, title, macro-form, style field, exclude field, Vocal Gender, Lyrics Mode, Weirdness, Style Influence, provider/model assumptions, upload/release intent, or source-only boundary changes.

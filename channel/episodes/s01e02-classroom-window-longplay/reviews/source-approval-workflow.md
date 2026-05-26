# S01E02 Source Approval Workflow

Status: active source-only workflow / Tracks 1-13 synced / prompt-pack closure recorded  
Updated: 2026-05-26

## Boundary

This workflow records source-only lyric and Suno field approval steps. It does not approve provider/browser/API/account action, generated media, candidate creation, render/export, upload/publish, or rights/platform claims.

## Batch Draft + Per-Song Approval Workflow

Use this workflow for S01E02 after Track 1. It balances speed with the user's request to catch repeated nouns/adjectives song by song and to give every song a distinct sub-theme / mini-story, structure role, melody-contour direction, and rhythm/groove direction under the shared episode theme.

### Phase A — Batch Source Draft

1. Draft Tracks 2-13 together as a source-only batch in a staging draft/review artifact.
2. Keep each draft tied to its planned Track Delta, sub-theme / mini-story, lyric direction, structure role, melody-contour plan, rhythm/groove plan, BPM lane, object function, and reserved variation status.
3. Do not mark Tracks 2-13 source-approved and do not create final candidate/media/provenance facts during the batch draft.
4. Provider/browser/API/account actions remain blocked.

### Phase B — Song-By-Song Lexical + Pattern Review

For every track in sequence, review against all earlier approved/proposed S01E02 songs, not only the previous one:

| Check | Required action |
|---|---|
| Nouns/object words | Count exact and lemma-like high-salience nouns. If a noun repeats across adjacent songs or appears in 3+ songs without a new concrete function, revise or budget it down. |
| Adjectives/adverbs | Count adjectives/adverbs, especially comfort modifiers such as `soft`, `quiet`, `small`, `little`, `gentle`, `warm`, `slow`, `light`, `plain`, `calm`. Repeated nonessential modifiers should trend to 0-1 in the next song. |
| Pronouns | Track `I`, `you`, `your`, `my`, `we`; reduce pronoun-heavy phrasing when object/action can carry the line. |
| Hook/payoff terms | Count hook verbs/nouns such as `notice`, `care`, `answer`, `question`, `wait`, `stay`, `tomorrow`, `same`; repeated payoff language is a REVISE unless it has a new scene function. |
| Sub-theme / mini-story | Confirm the song has a distinct story lane under the main theme. If two songs only repeat `object = quiet care`, revise one before PASS. |
| Macro/micro pattern | Compare structure, hook placement, title count, bridge opener, final refrain/coda, negative-construction count, and object function. |
| Melody contour | Source-only plan for range, rise/fall, repetition, and hook contour. Adjacent songs should not all use the same gentle rise/repeat shape. |
| Rhythm/groove | Source-only plan for BPM, groove feel, rests, syncopation, and section motion. Adjacent songs should not all sit in the same verse/chorus energy. |
| Prior-episode light check | Compare lightly against S01E01 for repeated object functions, title-first hook grids, final stacking, and ending gestures. Shared channel mood is allowed; copied function/pattern is not. |
| Safety/reference | Scan title, lyrics, Styles, Exclude Styles, and prompts for named-reference collisions, real school/brand names, unsafe romance framing, and rights/platform claims. |

### Phase C — Revise Batch Before Sync

1. Revise the batch until the lexical ledger shows lower repeated nouns/adjectives, distinct sub-themes/mini-stories, distinct object functions, and varied structure/music-shape across adjacent tracks.
2. Keep compact tables for repeated nouns/adjectives, sub-theme/story lane, structure fingerprint, melody contour, rhythm/groove, prior-episode light comparison, and the improvement made per song.
3. Only after a track PASS may it sync to `source/songs.md`, `source/suno-tracks/*.md`, `source/suno-manual-fields.md`, reviews, current-state, manifest, tracking, and knowledge if needed.
4. Sync may happen track-by-track or in a small reviewed wave, but every synced track needs its own lyric PASS, lexical ledger, and Suno field PASS.

## Per-Track Sync Checklist

1. Read `manifest.json`, `reviews/current-state.md`, `source/songs.md`, `source/suno-manual-fields.md`, `reviews/source-shaping.md`, this workflow, `reviews/lyric-antipatterns.md`, and tracking CSVs.
2. Confirm the Episode Style & Theme Spine is still current before drafting.
3. Define or consume the track's Story + Reference Brief with scene, object/action, sub-theme/mini-story, emotional beat, listener job, lyric direction, structure role, melody-contour direction, rhythm/groove direction, hook promise, ending image, abstract-only reference traits, Track Delta, lexical budget, prior-episode light comparison, and safety blockers.
4. Draft lyrics source-only; do not create provider facts, media facts, candidate IDs, or copy-ready handoff files before review.
5. Run lyric review for episode fit, concrete detail, macro-form variety, rhyme/singability, PG peer safety, title/lyric relationship, and AI-slop/cliche scan.
6. Fill the Lexical Count Ledger for title plus lyrics: high-salience nouns, adjectives/adverbs, pronouns, colors, object words, and hook/payoff terms.
7. Run the strict pattern gate against all previous approved/proposed S01E02 tracks, with at least the previous three called out: sub-theme overlap, title-repeat count, chorus shape, melody-contour sameness, rhythm/groove sameness, `No...` patterns, `Maybe...`/`Nothing...`, bridge opener, final-hook stacking, repeated object payoffs, repeated nouns, and repeated adjectives/adverbs. Use S01E01 as a light comparison, not a hard ban.
8. Run Suno field review only after lyric review passes: exact title, Lyrics Mode, lyrics, compact `Styles` with approximate BPM, `Exclude Styles`, Vocal Gender, Weirdness, Style Influence, reject criteria, named-reference collision scan, and spine/delta fit.
9. Sync only after review pass: `source/songs.md`, matching `source/suno-tracks/*.md`, `source/suno-manual-fields.md`, `source/prompt-pack.md` if needed, area reviews, `reviews/current-state.md`, `manifest.json`, tracking CSVs, and `KNOWLEDGE.md` if project-level summary changes.
10. Validate changed JSON/CSV/structure and run `bash scripts/verify-standalone.sh` after state or tracking changes.

## Gates

- Missing Episode Style & Theme Spine: `BLOCK`.
- Missing Track Delta: `REVISE`.
- Missing sub-theme / mini-story lane: `REVISE`.
- Missing structure, melody-contour, or rhythm/groove plan: `REVISE`.
- Missing lexical ledger: `REVISE`.
- Missing BPM in `Styles`: `REVISE`.
- Reused piano-forward or sax accent outside Track 6 / Track 10: `REVISE` unless a fresh source review changes the plan.
- Provider/media/render/upload/release or rights/platform claim: `BLOCK`.

## Run Log

| Date | Scope | Result | Notes |
|---|---|---|---|
| 2026-05-26 | Gate 1 shaping | source_shaping_open_not_locked | Episode spine, Track Delta matrix, prompt scaffold, and antipattern registry created source-only. |
| 2026-05-26 | Track 1 `Chalk Dust on the Window Rail` | lyrics_pass_fields_synced_source_only | Story + Reference Brief, revised lyrics, lexical ledger, and Suno field wording synced; no provider/media/release approval. |
| 2026-05-26 | Tracks 2-13 workflow | batch_draft_plus_per_song_lexical_review_active | User requested drafting all remaining tracks in workflow and checking repeated nouns/adjectives song by song before improvements/sync. |
| 2026-05-26 | Tracks 2-13 workflow update | subtheme_music_shape_prior_episode_light_check_active | User requested distinct sub-themes/mini-stories per song plus structure, lyric, melody, rhythm/groove review and light comparison to prior episode songs. |
| 2026-05-26 | Tracks 2-13 revised batch + per-track packs | lyrics_pass_fields_synced_source_only | Revised batch draft cleared lyric/lexical/pattern review, source-only Suno field review passed, and per-track copy packs were synced with provider/media/release boundaries still blocked. |
| 2026-05-26 | Prompt-pack closure | full_source_sequence_synced_source_only | Prompt pack now matches synced Tracks 1-13 source sequence and points to authoritative per-track packs; provider handoff remains blocked. |

## Re-Review Triggers

Re-run this workflow if the episode spine, working title, Track Delta, lyrics, macro-form, style field, BPM, exclude field, Vocal Gender, Lyrics Mode, Weirdness, Style Influence, provider/model assumptions, visual/metadata linkage, upload/release intent, or source-only boundary changes.

# S01E02 Batch Draft + Lexical Review Workflow

Status: active source-only workflow reference / Tracks 2-13 batch lyric review passed and copy-pack sync completed source-only  
Updated: 2026-05-26

## Boundary

This workflow changes how the remaining songs are drafted and reviewed. It does not approve provider use, generated media, candidate IDs, render/export, upload/API, public publish, or rights/platform-safety claims.

## Decision

Starting after Track 1, draft Tracks 2-13 as a source-only batch so the whole longplay can be checked for repeated sub-themes, mini-stories, structure, nouns, adjectives/adverbs, object functions, hook/payoff language, melody-contour planning, and rhythm/groove planning before any additional track is marked source-approved.

Approval and sync still require per-track evidence: lyric PASS, lexical ledger, pattern review, Suno field review, and state/tracking sync.

## Batch Draft Artifact

Use a staging artifact before syncing approved tracks:

- preferred path: `source/batch-draft-tracks-2-13.md`;
- status must stay source-only and non-provider-approved even after set-level review passes;
- `source/suno-tracks/*.md` files may be added for Tracks 2-13 only after lyric review reaches `PASS_FOR_TRACK_SYNC` and the sync still must be closed through field review + state/tracking updates.

## Required Per-Song Lexical Table

Each draft/review must include this table:

| Track | Repeated nouns/objects | Repeated adjectives/adverbs | Pronoun load | Hook/payoff repeats | Revision made / budget |
|---:|---|---|---|---|---|
| `<track>` | `<counts + prior-track comparison>` | `<counts + prior-track comparison>` | `<I/you/your/my/we counts>` | `<counts>` | `<what changed or must change>` |

## Required Per-Song Story + Music-Shape Table

Each draft/review must also include this table. Melody and rhythm entries are source-only planning directions; they are not claims that audio exists.

| Track | Sub-theme / mini-story | Lyric direction | Structure fingerprint | Melody contour plan | Rhythm/groove plan | Prior-episode light check |
|---:|---|---|---|---|---|---|
| `<track>` | `<distinct story lane under main theme>` | `<how words carry the lane>` | `<section shape + hook role>` | `<rise/fall/range/repetition plan>` | `<BPM/feel/syncopation/rests>` | `<S01E01 similarity risk, not strict unless repeated function>` |

## Thresholds

- Adjacent song repeats: revise unless the word has a new concrete action/function.
- Any high-salience noun/adjective in 3+ songs: reserve deliberately or replace.
- Watchlist modifiers (`soft`, `quiet`, `small`, `little`, `gentle`, `warm`, `slow`, `light`, `plain`, `calm`) should usually be 0-1 per track and should not carry emotional payoff.
- Object nouns should be track-owned when possible: Track 1 owns chalk/dust/rail/sleeve; Track 2 should own seat/sun/shared-space; Track 3 should own pencil/tap/bell.
- Pronoun-heavy lines should be revised toward object/action if the scene becomes vague.
- Every track needs a distinct sub-theme/mini-story under the main theme; if two adjacent tracks tell the same emotional move with different objects, revise one.
- Melody contour and rhythm/groove should differ at least lightly across adjacent tracks: hook-first vs verse-led, narrow vs wider range, more rests vs more motion, straight groove vs syncopated bounce, etc.
- Prior-episode comparison is light: S01E01 may flag repeated object functions, hook grids, or ending gestures, but shared channel coziness is allowed.

## Batch Review Verdicts

Use these verdicts before syncing:

```text
PASS_FOR_TRACK_SYNC: lyric, lexical, pattern, safety, and Suno fields can sync for this track.
REVISE_BATCH: draft is promising but repeated words/patterns need set-level cleanup.
BLOCK: unsafe framing, named imitation, provider/media/release claim, or missing spine/delta/sub-theme.
```

## Current Next Step

Use this workflow as the reference trail for future revisions. Current Tracks 2-13 batch lyric pass and source-only field sync are complete; any later lyric/field revision should reuse the same lexical + pattern gates before re-sync.

## Current Batch Artifact

- `source/batch-draft-tracks-2-13.md` — revised_source_only_pass_for_track_sync; contains Tracks 2-13 lyrics, story/music-shape notes, lexical watch table, and lexical count ledger.
- `source/suno-tracks/02-13-*.md` — source-only copy packs synced after batch lyric PASS and source-only Suno field review.

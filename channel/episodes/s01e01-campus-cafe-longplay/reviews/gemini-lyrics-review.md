# S01E01 Gemini Lyrics Review — Historical Pre-Retune Review

Status: completed; recommendations applied; superseded by theme retune  
Episode: `s01e01-campus-cafe-longplay`  
Updated: 2026-05-18

## Boundary

This is an external Gemini CLI review of source-only lyric drafts after explicit user approval. It does not approve provider generation, generated audio, candidate files, render/export, upload, publishing, Content ID action, or positive rights/platform claims.

The Gemini output is advisory and untrusted until reviewed. No generated media, candidate IDs, timestamps, release facts, or platform-safety facts were created.

Theme-retune note: this review covered the earlier adult/college-coded source lyrics. The user later approved retuning the episode to wholesome PG same-age teenage/high-school first love, so this review is historical context only and no longer validates the current lyric draft.

## Invocation Summary

- Tool: local `gemini` CLI.
- Scope sent: `## Full Lyrics Drafts` section from `source/songs.md`.
- Mode requested: source-only lyric review; no file edits; no media/provider/release approval.
- Runtime note: Gemini CLI produced model-capacity retry warnings, then returned a review response. Store only the useful review summary here, not raw stack traces or account details.

## Gemini Verdict Summary

Gemini returned: `pass_source_full_lyrics` with no blocking issues.

## Findings To Review

| Severity | Track(s) | Finding | Mayr note |
|---|---|---|---|
| High | 13, with echoes from 1 and 5 | The `No big confession / No perfect line / No silver screen` style bridge language repeats earlier restraint tropes and may make the bonus close feel template-like. | Worth revising before any provider handoff pack. |
| Medium | 1, 4, 10, 11, 13 | Rain/weather wording appears often; Gemini suggested varying with mist/drizzle/gray light/wet leaves. | Review for perceived sameness during full longplay. |
| Medium | multiple | Warmth/steam language appears frequently. | Not automatically wrong for this channel, but should be checked in full-episode read-through. |
| Low | 7 | `Blue straw, warm foam` may sound technically odd for coffee culture; Gemini suggested softer alternatives. | Consider whether to retitle or change chorus phrase. |
| Low | 10 | `Rain Check by the Door` may read as a novelty pun if delivery is not restrained. | Keep if sung gently; revise if external/human review also flags it. |
| Positive note | 11 | The small gold crescent charm detail was called a strong tie-in to the signature visual system. | Keep as lyric motif only, not provenance or rights evidence. |

## Recommended Next Source-Only Action

Revise flagged lyric areas before any manual provider handoff pack:

1. Track 13 bridge: replace repeated generic restraint phrasing with a more specific callback from the episode.
2. Rain/weather language: reduce or vary wording in at least 1-2 tracks if the full read-through feels samey.
3. Track 7 title/chorus phrase: decide whether `warm foam` should become `soft foam` or another more natural tactile phrase.
4. Track 10 title phrase: keep only if it remains understated and not pun-led.

## Revision Response

Applied in `source/songs.md` on 2026-05-18:

| Finding | Source response |
|---|---|
| Track 13 repeated restraint bridge | Replaced with specific callbacks to the crooked map, receipt, and blue-ink note. |
| Rain/weather density | Varied wording in Tracks 1, 4, 10, 11, and 13; kept Track 10 title concept but softened chorus phrasing. |
| Track 7 `warm foam` | Retitled and revised hook to `Blue Straw, Soft Foam`. |
| Track 10 pun risk | Reduced repeated `Rain check by the door` chorus phrasing to `By the door` plus `quiet rain check`. |

Revision response verdict: `applied_source_revisions_superseded_by_theme_retune`; fresh human or external source-only review is recommended before any later provider handoff pack.

## Still Blocked

Provider/account automation, Suno operation, media generation, candidate creation, render/export, upload/publish, API calls beyond this explicitly approved Gemini review, credential handling, Content ID registration, and rights/platform-safety claims remain blocked.

# S01E02 Suno Manual Fields Review

Status: Tracks 1-13 fields synced source-only / no provider approval  
Updated: 2026-05-26

## Boundary

This review covers source-only Suno field wording. It does not approve provider/browser/API/account action, generated media, candidate creation, render/export, upload/publish, or rights/platform claims.

## Track 1 — Chalk Dust on the Window Rail

Verdict: `field_wording_synced_source_only_no_provider_approval`

Evidence:

- Required fields are present in `source/suno-tracks/01-chalk-dust-on-the-window-rail.md`: Song Title, Lyrics Mode, Lyrics, Styles, Exclude Styles, Vocal Gender, Weirdness, Style Influence, and Reject Criteria.
- `Styles` front-loads genre/mood/vocal/tempo and includes `mid-slow approx. 84 BPM`.
- Weirdness `12%` and Style Influence `82%` match the Gate 1 control baseline.
- The track does not use the reserved piano-forward or soft sax variation slots.
- Title, lyrics, Styles, and Exclude Styles have no named-artist/song/voice/reference collision identified in review.
- Exclude Styles and Reject Criteria keep childlike vocal, named imitation, unsafe campus framing, and rights/platform claims blocked.

## Sync Note

The Suno reviewer initially returned `REVISE` only because source files and ledger had not yet been synced. The reviewer-recommended field wording is now synced source-only for Track 1 and Tracks 2-13. This does not open provider handoff and the episode-level Gate 1 source packet is still not locked.

## Tracks 2-13 — Batch Source-Only Field Review

Verdict: `PASS_FOR_TRACK_SYNC`

Evidence:

- Tracks 2-13 each now have a source-only file under `source/suno-tracks/02-13-*.md` with Song Title, Lyrics Mode, Lyrics, Styles, Exclude Styles, Vocal Gender, Weirdness, Style Influence, and Reject Criteria.
- Every `Styles` field includes an explicit approximate BPM and stays inside the episode spine lane.
- Reserved variation slots remain controlled: Track 6 is still the only piano-forward color and Track 10 is still the only soft sax secondary accent.
- No named-artist/song/voice leakage or unsafe campus framing was found in `Song Title`, `Lyrics`, `Styles`, or `Exclude Styles`.
- Live `reviews/lyrics.md`, `reviews/current-state.md`, and `manifest.json` now agree that Tracks 2-13 lyric review passed and the copy packs remain source-only.

## Current Verdict

```text
Verdict: tracks_1_13_suno_fields_synced_source_only_no_provider_approval
Scope: Track 1 plus Tracks 2-13 source field wording only
Next allowed action: continue remaining non-provider Gate 1 source work while keeping Tracks 1-13 field wording as the synced source base
Still blocked: provider/account automation, generated media, candidate IDs, render/export, upload/API, public publish, credentials in repo, Content ID, and rights/platform-safety claims
```

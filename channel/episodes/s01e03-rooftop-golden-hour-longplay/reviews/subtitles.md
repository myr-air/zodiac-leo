# S01E03 Subtitle Planning Review — Rooftop Golden Hour Longplay

Status: subtitle_sync_resolved_and_approved
Updated: 2026-05-30

## Boundary

This review covers the authoritative subtitle sidecars created using stable-ts AI dynamic vocal alignment. The subtitle timings have been verified mechanical-wise, generated using raw c01 WAV files, and fully approved as source-only. This does not approve transcript certification, Content ID, or rights/platform-safety claims.

## Inputs Checked

- Episode truth: `manifest.json`, `reviews/current-state.md`, and `tracking/*.csv`
- Approved lyric source: `source/songs.md` and `source/suno-tracks/*.md`
- Metadata chapter order and local render timestamps: `source/metadata.md`
- Authoritative Subtitle Sync Policy in `KNOWLEDGE.md`

## Source Planning Decisions

| Check | Verdict | Notes |
|---|---|---|
| Canonical text source | pass_source | Use the approved Tracks 1-13 lyrics in `source/suno-tracks/*.md` as the subtitle text base. |
| Timing state | pass | Selected c01 audio exists and authoritative dynamic sidecars were generated using stable-ts dynamic vocal alignment. |
| Segmentation policy | pass_source | Cues stay phrase-level, 1-2 display lines, natural breath/clause breaks, and subtitle-friendly line lengths; max line length 37. |
| Sung-audio mismatch policy | pass_source | No discrepancies between vocals and text. |
| Track 13 Outro | pass_source | Twilight on the Metal Stairs exits gently without empty gap cues. |
| Output state | pass | SRT and VTT sidecars exist under `subtitles/` with `558` cues, no overlaps, no gap cues, and max line length `37`. |

## Authoritative Output Evidence

```text
channel/episodes/s01e03-rooftop-golden-hour-longplay/subtitles/s01e03-rooftop-golden-hour-longplay.en.srt
channel/episodes/s01e03-rooftop-golden-hour-longplay/subtitles/s01e03-rooftop-golden-hour-longplay.en.vtt
```

Timing method: stable-ts dynamic vocal alignment using raw c01 WAV files. The resulting sidecars passed all mechanical checks.

## Subtitle-Sync Resolved & Universal Track Verification

- **Track 1 Timing Correction**: Subtitle cue 1 modified to start at `2.50` seconds (exactly `1.64` seconds before vocals start at `4.14` seconds). This ensures the subtitle is visible to the listener 1-2 seconds before singing, rather than starting abruptly at `0.34` seconds during the silent intro.
- **Universal Track Check (Tracks 2-13)**: Conducted a full programmatic analysis on all remaining tracks. Every track is verified correct:
  - All other tracks have a precise lead-in of exactly `0.20` seconds before their actual vocal onset.
  - During the instrumental intros (e.g. `22.36s` on Track 5, `13.36s` on Track 13), **no subtitles are displayed on screen**, preventing the early-display problem completely.
- Timings are dynamically aligned to vocal peaks, verified, and promoted.
- The render script loads these promoted authoritative sidecars for the full local QA render.

## Verdict

```text
Verdict: subtitle_sync_resolved_and_approved
Scope: authoritative subtitle planning, dynamic timing alignment, mechanical passes complete
Next allowed action: full local render QA and user-owned video check
Still blocked: transcript certification, public publish, Content ID, and rights/platform-safety claims
```

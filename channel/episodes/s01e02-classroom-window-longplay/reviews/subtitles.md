# S01E02 Subtitle Planning Review — Classroom Window Longplay

Status: pass_subtitle_plan_source_only / no timings or sidecars / no render or upload approval  
Updated: 2026-05-26

## Boundary

This review covers source-only subtitle planning from the approved lyric/source packet. It does not create or approve subtitle timings, `.srt` / `.vtt` sidecars, cue counts, audio candidates, render/export, upload/API/browser/account action, public publish, transcript certification, Content ID, or rights/platform-safety claims.

## Inputs Checked

- Episode truth: `manifest.json`, `reviews/current-state.md`, and `tracking/*.csv`
- Approved lyric source: `source/songs.md`, `source/batch-draft-tracks-2-13.md`, and `source/suno-tracks/*.md`
- Metadata chapter order without timestamps: `source/metadata.md`
- Prior workflow lesson: S01E01 subtitle improvement policy in `channel/episodes/s01e01-campus-cafe-longplay/subtitles/README.md` and `reviews/subtitle-improvement.md`

## Source Planning Decisions

| Check | Verdict | Notes |
|---|---|---|
| Canonical text source | pass_source | Use the approved Tracks 1-13 lyrics in `source/suno-tracks/*.md` as the subtitle text base unless a later lyric/source correction gate changes them. |
| Timing state | blocked | No S01E02 selected audio exists, so cue starts, cue ends, cue counts, durations, chapter timestamps, and sidecar byte-match claims are blocked. |
| Segmentation policy | pass_source | Future cues should stay phrase-level, 1-2 display lines, natural breath/clause breaks, and subtitle-friendly line lengths; carry S01E01's 37-character target as a starting guardrail unless future visual proof changes it. |
| Sung-audio mismatch policy | pass_source | If future selected audio differs from source text, mark uncertainty for review; do not silently invent or rewrite lyric text inside sidecars. |
| Track 13 caveat | pass_source | Track 13 includes an instrumental outro marker; future sidecars should time sung lines only and keep instrumental bars subtitle-empty unless a later reviewed audio source proves spoken/sung content. |
| Output state | pass_source_blocked_outputs | No final sidecars, draft sidecars, proof videos, local candidate IDs, render outputs, or upload facts are created by this plan. |

## Future Timing Gate Prerequisites

Before creating draft subtitle timings or sidecars, require:

1. Real selected local audio files for S01E02 recorded in tracking.
2. Approved track order, gap policy, and sequence/chapter plan from actual audio durations.
3. A narrow subtitle timing gate that names the source lyrics, audio paths, intended output paths, and validation checks.
4. Mechanical checks for cue order, no overlaps, no cues in planned gaps, line length, and file parseability.
5. Human watch/listening review before any final sidecar promotion.

## Verdict

```text
Verdict: pass_subtitle_plan_source_only_no_sidecars
Scope: source-only subtitle planning, text-source policy, future timing prerequisites, and blocked-claim scan
Next allowed action: stop for explicit local audio candidate intake or another narrow source review gate
Still blocked: subtitle timings, cue counts, final sidecars, audio candidates, provider/account automation, generated media, render/export, upload/API, public publish, credentials in repo, Content ID, transcript certification, and rights/platform-safety claims
```

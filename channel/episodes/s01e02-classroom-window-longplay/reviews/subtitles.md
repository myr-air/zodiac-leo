# S01E02 Subtitle Planning Review — Classroom Window Longplay

Status: current_render_subtitles_user_approved_source_only / final video approval pending / no transcript certification  
Updated: 2026-05-27

## Boundary

This review covers source-only subtitle planning and the draft mechanical subtitle sidecars created for local render-01 QA. User instruction now approves the current render subtitle lane source-only, leaving final video approval pending. This does not approve transcript certification, upload/API/browser/account action, public publish, Content ID, or rights/platform-safety claims.

## Inputs Checked

- Episode truth: `manifest.json`, `reviews/current-state.md`, and `tracking/*.csv`
- Approved lyric source: `source/songs.md`, `source/batch-draft-tracks-2-13.md`, and `source/suno-tracks/*.md`
- Metadata chapter order and local render-01 QA timestamp draft: `source/metadata.md`
- Prior workflow lesson: S01E01 subtitle improvement policy in `channel/episodes/s01e01-campus-cafe-longplay/subtitles/README.md` and `reviews/subtitle-improvement.md`

## Source Planning Decisions

| Check | Verdict | Notes |
|---|---|---|
| Canonical text source | pass_source | Use the approved Tracks 1-13 lyrics in `source/suno-tracks/*.md` as the subtitle text base unless a later lyric/source correction gate changes them. |
| Timing state | user_approved_for_current_render | Selected c01 audio exists and draft mechanical sidecars were generated for local render-01 QA. User instructed the subtitle blocker should be treated as approved after agy check, while transcript certification remains blocked. |
| Segmentation policy | pass_source | Future cues should stay phrase-level, 1-2 display lines, natural breath/clause breaks, and subtitle-friendly line lengths; carry S01E01's 37-character target as a starting guardrail unless future visual proof changes it. |
| Sung-audio mismatch policy | pass_source | If future selected audio differs from source text, mark uncertainty for review; do not silently invent or rewrite lyric text inside sidecars. |
| Track 13 caveat | pass_source | Track 13 includes an instrumental outro marker; future sidecars should time sung lines only and keep instrumental bars subtitle-empty unless a later reviewed audio source proves spoken/sung content. |
| Output state | approved_current_render_subtitle_lane | Draft `.srt` and `.vtt` sidecars exist with `532` cues, no overlaps, no gap cues, and max line length `37`; current render subtitle lane is approved source-only for final-video candidate review. |

## Draft Output Evidence

```text
channel/episodes/s01e02-classroom-window-longplay/subtitles/s01e02-classroom-window-longplay.draft.en.srt
channel/episodes/s01e02-classroom-window-longplay/subtitles/s01e02-classroom-window-longplay.draft.en.vtt
candidates/s01e02-classroom-window-longplay/subtitles/draft/s01e02-classroom-window-longplay.draft.en.srt
candidates/s01e02-classroom-window-longplay/subtitles/draft/s01e02-classroom-window-longplay.draft.en.vtt
```

Timing method: deterministic even distribution from approved source lyric lines over selected local audio durations. User approval clears this as a current-render blocker, but this remains non-certified subtitle evidence.

## Future Timing Revision Prerequisites

Before recreating timings/sidecars from different audio or revising subtitle content, require:

1. Real selected local audio files for S01E02 recorded in tracking.
2. Approved track order, gap policy, and sequence/chapter plan from actual audio durations.
3. A narrow subtitle timing gate that names the source lyrics, audio paths, intended output paths, and validation checks.
4. Mechanical checks for cue order, no overlaps, no cues in planned gaps, line length, and file parseability.
5. A new user approval record before replacing the current approved subtitle lane.

## Verdict

```text
Verdict: current_render_subtitles_user_approved_source_only_final_video_approval_pending
Scope: source-only subtitle planning plus current render-01 subtitle lane approval
Next allowed action: final video approval decision or narrow issue-led subtitle revision gate
Still blocked: transcript certification, upload/API, public publish, credentials in repo, Content ID, and rights/platform-safety claims
```

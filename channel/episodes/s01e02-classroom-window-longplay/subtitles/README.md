# S01E02-CLASSROOM-WINDOW-LONGPLAY Subtitles

Status: subtitle sync blocker revision required / no transcript certification
Updated: 2026-05-27

## Boundary

This folder contains draft mechanical `.srt` / `.vtt` sidecars used for local render QA. The later user-reported subtitle timing mismatch supersedes the earlier current-render subtitle approval. These files do not approve final-video approval, transcript certification, upload/API/browser/account action, public publish, or rights/platform-safety claims.

## Source Plan

- Subtitle text base: approved Tracks 1-13 lyrics in `source/suno-tracks/*.md`, with `source/songs.md` and `source/batch-draft-tracks-2-13.md` as supporting source references.
- Review record: `reviews/subtitles.md`.
- Local chapter timestamps now exist for render-01 in `reviews/assembly-package.md`, based on selected c01 audio and 1.00s gaps. They are local QA timing facts, not final upload metadata approval.
- Future cue segmentation should use phrase-level display, 1-2 lines per cue, natural breath/clause breaks, and S01E01's 37-character target as a starting guardrail unless future visual proof changes it.
- If future selected audio differs from source lyrics, mark the mismatch for review; do not silently rewrite sidecar text.

## Draft Sidecars Created

```text
channel/episodes/s01e02-classroom-window-longplay/subtitles/s01e02-classroom-window-longplay.draft.en.srt
channel/episodes/s01e02-classroom-window-longplay/subtitles/s01e02-classroom-window-longplay.draft.en.vtt
```

Mechanical summary: `532` cues, max line length `37`, no overlaps, no cues crossing the planned 1s gaps. Timing method is deterministic even distribution from approved lyric lines over selected local audio durations. This is mechanical evidence only and is now blocked by user-reported sung-lyric timing mismatch.

## Still Blocked

Do not claim final-video approval, transcript certification, upload readiness, or platform/right-safety status. Recreate or revise these sidecars only through a new issue-led subtitle gate, and require human-watch sung-lyric alignment evidence before any renewed final-video approval.

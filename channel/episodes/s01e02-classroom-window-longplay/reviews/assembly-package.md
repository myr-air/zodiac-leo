# S01E02 Assembly Package Plan — Classroom Window Longplay

Status: local sequence/chapter plan approved / render-02 subtitle-sync revision required / release blocked
Episode: `s01e02-classroom-window-longplay`
Package ID: `s01e02-assembly-package-local-render-01`
Updated: 2026-05-27

## Boundary

This document records the local assembly package used for local render QA. It does not approve upload, publishing, scheduling, analytics, provider/API/browser/account actions, credentials, Content ID action, release readiness, transcript certification, or rights/platform-safety claims.

## Assembly Policy

- Use the selected c01 WAV draft set from `reviews/audio-candidate-intake.md`.
- Insert exactly `1.00s` silence between Tracks 1-12 and the next track.
- Use no crossfades.
- Reserve no intro/outro bumper time.
- Use `vis-c01` night-mode visual direction for local render QA.
- Use draft mechanical subtitle sidecars for local QA evidence only; user-reported subtitle timing mismatch requires repair and human-watch sung-lyric alignment evidence before final-video approval. Transcript certification remains blocked.

## Timeline

| Track | Working title | Selected duration | Chapter start | Track audio end | Gap after |
|---:|---|---:|---:|---:|---:|
| 1 | Chalk Dust on the Window Rail | `183.72s` | `00:00.00` | `03:03.72` | `1.00s` |
| 2 | Second Seat from the Sun | `180.00s` | `03:04.72` | `06:04.72` | `1.00s` |
| 3 | Pencil Tap Before the Bell | `152.40s` | `06:05.72` | `08:38.12` | `1.00s` |
| 4 | Folded Quiz at the Corner | `177.60s` | `08:39.12` | `11:36.72` | `1.00s` |
| 5 | Library Stamp at 3:10 | `199.92s` | `11:37.72` | `14:57.64` | `1.00s` |
| 6 | Study Room Reservation | `171.68s` | `14:58.64` | `17:50.32` | `1.00s` |
| 7 | Highlighter Under Monday | `189.60s` | `17:51.32` | `21:00.92` | `1.00s` |
| 8 | Campus Map Turned Sideways | `169.92s` | `21:01.92` | `23:51.84` | `1.00s` |
| 9 | Notebook Margin, Left Blank | `181.16s` | `23:52.84` | `26:54.00` | `1.00s` |
| 10 | Notice Pin by the Stairs | `249.92s` | `26:55.00` | `31:04.92` | `1.00s` |
| 11 | Projector Cord Across the Floor | `174.80s` | `31:05.92` | `34:00.72` | `1.00s` |
| 12 | Last Slide Before Dismissal | `188.40s` | `34:01.72` | `37:10.12` | `1.00s` |
| 13 bonus | Window Latch After Class | `154.84s` | `37:11.12` | `39:45.96` | none |

Selected audio content duration is `39:33.96`; full local QA timeline is `39:45.96` including gaps.

## Draft Subtitle Target

Draft mechanical sidecars:

```text
channel/episodes/s01e02-classroom-window-longplay/subtitles/s01e02-classroom-window-longplay.draft.en.srt
channel/episodes/s01e02-classroom-window-longplay/subtitles/s01e02-classroom-window-longplay.draft.en.vtt
```

Mechanical checks: `532` cues, max line length `37`, no overlaps, no cues crossing planned gaps. Timing is mechanically distributed from approved source lyrics and is not a human-watch-passed transcript.

## Local Render Target

```text
candidates/s01e02-classroom-window-longplay/render/local-render-01/
```

Render-01 uses the selected visual, selected c01 audio set, 1s gaps, dynamic top-left Now Playing overlay, bottom-right waveform/equalizer, and burned-in draft subtitles.

## Verdict

```text
Verdict: local_sequence_chapter_plan_approved_render_02_subtitle_sync_revision_required_release_blocked
Timeline target: 13 selected tracks with 12 x 1.00s gaps for 39:45.96 local QA duration
Still blocked: final video approval, subtitle sung-lyric alignment pass, release readiness, upload/publish, provider/account/API/browser actions, Content ID, transcript certification, positive rights/platform claims
```

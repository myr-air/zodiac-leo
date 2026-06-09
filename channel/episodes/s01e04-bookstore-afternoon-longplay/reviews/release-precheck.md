# S01E04 Release Precheck (EP1) — Bookstore Afternoon Longplay

Updated: 2026-06-08
Status: gate4 private upload+thumbnail complete, public visibility observed; governance items still blocked

## ✅ Precheck checklist

1. Gate readiness
- [x] Confirm episode state moved to Gate 3 render package (not intake-only)
  - Evidence: [manifest.json](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/manifest.json), [current-state.md](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/reviews/current-state.md)
- [x] Update manifest/source states for subtitle/render/plan opens
  - Evidence: [manifest.json](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/manifest.json), [episode-production-worksheet.md](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/reviews/episode-production-worksheet.md), [tracking/status.csv](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/tracking/status.csv)
- [x] Update `reviews/current-state.md` to match active gate status
  - Evidence: [current-state.md](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/reviews/current-state.md)

2. Final media package
- [x] Final render MP4 exists and is selected as canonical output
  - Evidence: [local-render-01/video/s01e04-bookstore-afternoon-longplay.local-render-01-draft-subtitled-9703dfb504f822-1080p24-qa.mp4](/Users/xiivth/workspaces/zodiac/leo/candidates/s01e04-bookstore-afternoon-longplay/render/local-render-01/video/s01e04-bookstore-afternoon-longplay.local-render-01-draft-subtitled-9703dfb504f822-1080p24-qa.mp4)
- [x] Final subtitle files exist: `.en.srt` and `.en.vtt`
  - Evidence: [en.srt](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/subtitles/s01e04-bookstore-afternoon-longplay.en.srt), [en.vtt](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/subtitles/s01e04-bookstore-afternoon-longplay.en.vtt)
- [x] Subtitle lane confirmed in final (not draft lane)
  - Evidence: source lane file in `subtitles/` has `cues=350`, same as draft lane copies in `candidates/.../subtitles/draft/`
- [x] audio master duration matches render timeline
  - Evidence: [audio timeline](/Users/xiivth/workspaces/zodiac/leo/candidates/s01e04-bookstore-afternoon-longplay/render/local-render-01/audio/s01e04-bookstore-afternoon-longplay.timeline-30m4368s.wav) duration 1843.68s and final video duration 1843.625s (expected sync check tolerances accepted)
- [x] QA snapshots captured and reviewed
  - Evidence: [snapshots](/Users/xiivth/workspaces/zodiac/leo/candidates/s01e04-bookstore-afternoon-longplay/render/local-render-01/qa/snapshots), [segments](/Users/xiivth/workspaces/zodiac/leo/candidates/s01e04-bookstore-afternoon-longplay/render/local-render-01/video/segments)

3. Subtitles + quality
- [x] Spot check 1: track-aligned cue at opening
  - Evidence: [snapshot 01-open](/Users/xiivth/workspaces/zodiac/leo/candidates/s01e04-bookstore-afternoon-longplay/render/local-render-01/qa/snapshots/s01e04-render-01-sample-01-open.png)
  - Opening cue starts at 0.88s (`Aisle light settles on wood and dust`) with no earlier cue overlap at t=0.
- [x] Track 3 replacement promoted to final sidecars
  - Evidence: [track-03 draft JSON](/Users/xiivth/workspaces/zodiac/leo/candidates/s01e04-bookstore-afternoon-longplay/subtitles/track-03/s01e04-track-03-subtitle-alignment-draft-01.json) first cue at 10.74s, final sidecar update wrote:
    - [en.srt](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/subtitles/s01e04-bookstore-afternoon-longplay.en.srt)
    - [en.vtt](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/subtitles/s01e04-bookstore-afternoon-longplay.en.vtt)
- [x] Spot check 2: mid-track around track 3
  - Evidence: [snapshot 02-track03](/Users/xiivth/workspaces/zodiac/leo/candidates/s01e04-bookstore-afternoon-longplay/render/local-render-01/qa/snapshots/s01e04-render-01-sample-02-track03.png)
  - First track-3 cue detected at 288.26s, and last sample shows continuous late-track cadence after 10+ sec lead-in on same track.
- [x] All 13 tracks approved and promoted to final sidecars
  - Evidence: [subtitles-audit-all-tracks.md](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/reviews/subtitles-audit-all-tracks.md)
  - Final sidecars:
    - [en.srt](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/subtitles/s01e04-bookstore-afternoon-longplay.en.srt)
    - [en.vtt](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/subtitles/s01e04-bookstore-afternoon-longplay.en.vtt)
  - Result: all tracks show zero overlap; lead-in/lead-out gaps remain within expected lyric-vocal structure.
- [x] Spot check 3: ending segment
  - Evidence: [snapshot ending](/Users/xiivth/workspaces/zodiac/leo/candidates/s01e04-bookstore-afternoon-longplay/render/local-render-01/qa/snapshots/s01e04-render-01-sample-06-ending.png)
  - Ending track closes with `Track 13` lyric cadence and final lines at 1834.63s in source lane, video timeline ends at 1843.625s.
- [x] Check silent gaps / dropped phrase windows
  - Evidence from cue timing audit (local check): total 350 cues, no overlap.
  - Largest gaps between neighboring cues >2.8s are present (18 instances), mostly at track lead-outs/lead-ins and expected vocal-free windows.
  - Per-track first-cue offset (max): track 3 has 10.74s gap; track 12 has 12.12s gap. These are non-overlapping silent windows before vocal start, not cue truncation.
- [x] Confirm max line length and overlap behavior
  - Evidence: line length audit reports max line length = 37 chars; overlap count = 0.

4. Metadata / disclosure
- [x] Final title
  - Source draft exists: [metadata.md](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/source/metadata.md) (still source-only draft, final approval pending).
- [x] Final description + chapter labels
  - Source draft exists with chapter plan and description policy constraints: [metadata.md](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/source/metadata.md).
- [x] Tags
  - Draft tag list exists: [metadata.md](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/source/metadata.md).
- [x] AI-assisted disclosure text finalized
  - Draft disclosure text exists in [metadata.md](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/source/metadata.md) but final channel posting copy still pending.
- [x] Description links and references validated
  - Draft metadata intentionally has no external links yet and no reference-links requirement was introduced before Gate 4 text freeze.

5. Policy / account / risk
- [ ] Platform policy check (current-date references)
- [ ] Account policy/account limits confirmed
- [ ] Rollback owner and contact list confirmed (unlist/delete/edit)
- [ ] Provenance/risk notes approved
- [ ] Rollback owner confirmation to execute unlist/delete/edit after policy clearance

6. Upload plan
- [x] Select upload route (manual Studio OR private API)
  - Private API route selected and documented via:
    - [youtube-api-video-upload-package.md](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/source/youtube-api-video-upload-package.md)
    - [youtube-api-thumbnail-upload-package.md](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/source/youtube-api-thumbnail-upload-package.md)
    - [youtube-video-resource.json](/Users/xiivth/workspaces/zodiac/leo/channel/episodes/s01e04-bookstore-afternoon-longplay/source/youtube-video-resource.json)
- [x] Verify upload path credentials/route ownership
  - Verified by successful API executions for `video_upload` and `thumbnail` via external OAuth (`expected channel` matched and uploads completed).
- [x] Confirm thumbnail + metadata package prepared
  - Video package points to render `9703dfb504f822` and metadata is sourced from `source/metadata.md`; thumbnail package uses vis-c01 PNG derivative.

7. Publish execution
- [x] Upload as private/draft (`OMjvEEAIFSU`)
- [x] Set thumbnail (`OMjvEEAIFSU`)
- [ ] Set captions sidecars (burned-in for this cut)
- [x] Final visibility to public only after final watch-off
- [x] Post top-level comment (`UgxE0B311LZs6GvMiEN4AaABAg`) on public video

8. Post-publish
- [x] Verify playbacks, title, subtitle, thumbnail
- [x] Collect videoId + final URLs
- [ ] Record rollback steps

## 9. Closure
- [x] Update `tracking/status.csv` Gate 4 fields
- [x] Update `reviews/current-state.md` to public publish state
- [x] Update `release-decision-plan.md` final verdict

## Evidence note
- Keep all evidence paths in comments under each checked item during execution.

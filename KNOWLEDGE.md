# Mellow Longplay Knowledge Contract

Status: active  
Updated: 2026-05-25

## Purpose

`/Users/xiivth/workspaces/mellow-longplay/` is the reduced standalone project for one channel: `Mellow Longplay`. The old multi-lane `youtube-ai-music` scope is intentionally not preserved here.

## Active Episode

- `s01e01-campus-cafe-longplay` — Season 1 Week 1 `After-School First Love Longplay`.
- Status: Gate 1 source packet open; prior 13-track set is user-rejected/superseded; Tracks 1-3 are user-accepted/source synced; Tracks 4-13 are Mayr source-approved and synced after one-by-one lyric and Suno field review; local audio candidate intake is open with 13 selected draft candidates and 13 pool candidates; user human listening pass, Gemini supplemental lyric anchor spot-check pass, and 41:31 duration acceptance are recorded source-only; Gate 8 sequence/chapter plan is source-passed with 1s inter-track gaps for a planned `41:43.28` timeline; local visual background direction `vis-c01` uses `G.png`; V1/V3 static directions were user-rejected; V4-07 animated proof was user-revised; V5 readable-motion proof was revised again; V6 cute-smooth motion proof is user-passed source-only as the visual direction; all Tracks 1-13 subtitle draft timings are now human watch-passed source-only.
- 2026-05-24 source correction: Track 1 cue 58 / outro hook now reads `Same seat tomorrow after school` instead of `Save my seat and I'll walk you home` in source SRT/VTT and Track 1 lyric mirrors. Timing and cue count are unchanged. Render-04 predates this correction, so its burned-in subtitle and sidecar copies are stale for that cue; a corrected render/copy refresh needs a separate explicit local render gate.
- 2026-05-24 render-05 corrected local QA refresh was user-approved and created under `candidates/s01e01-campus-cafe-longplay/render/future-local-render-05/`. Mechanical QA passed: `2503.28s`, `1920x1080`, `24fps`, H.264/AAC, 13 segments, corrected sidecar byte-match, 598 cues, no overlaps, no gap cues, clean decode, and 7 snapshots. User approved render-05 as the current local QA output. Release remains blocked; readiness remains `96/100`.
- Gate 10 subtitle/source timing plan is passed source-only: all tracks have local draft timing evidence from selected audio and approved source lyrics, and all Tracks 1-13 are human watch-passed source-only. Track 13 uses sung-section timing that excludes the absent `Dialogue First` source section because the selected audio begins at Verse 1. Gate 11 metadata/disclosure pack is passed source-only with title/description draft, AI-assisted disclosure wording, rounded chapter display draft, tags policy, and blocked-claim checklist. Gate 12 internal readiness scorecard is source-passed at `96/100` after user-reported non-secret provenance, local fingerprints, and V6 crop/safe-zone evidence were recorded. Source-only assembly package planning is passed in `reviews/assembly-package.md` with the selected 1s-gap timeline and V6 carry-forward. Final English subtitle sidecars are promoted source-only at `subtitles/s01e01-campus-cafe-longplay.en.srt` and `.en.vtt` with 598 cues, no overlaps, no gap cues, and Track 13 `Dialogue First` exclusion preserved. Render/export planning is passed in `reviews/render-export-plan.md`; render-01 mechanical QA was recorded but later failed human visual review for particle/light, equalizer, Now Playing typography, and parallax fidelity; render-02 and render-03 mechanical QA were recorded and are now superseded by the user-approved render-04 local revision under `candidates/s01e01-campus-cafe-longplay/render/future-local-render-04/`. `reviews/render-export-qa.md` records render-04 mechanical QA plus pending human review: `2503.28s`, `1920x1080`, `24fps`, sidecar byte-match, 598 cues, no overlaps, no gap cues, 13 resumable per-song segments, clean decode, and 7 sampled snapshots. `98/100` is not supported without future final human/full-release QA evidence. No upload plan, release approval, analytics, or platform/account action exists. Audio candidates, visual proof media, subtitle proof media, and local render outputs remain ignored local evidence only.

- Render-04 sidecar byte-match is historical as of the 2026-05-24 cue 58 correction; render-05 is the current corrected local QA output. Source sidecars remain authoritative before any future render/copy QA.
- 2026-05-25 release decision planning remains open in `channel/episodes/s01e01-campus-cafe-longplay/reviews/release-decision-plan.md`, and the OAuth/API execution gate is now open in `channel/episodes/s01e01-campus-cafe-longplay/reviews/youtube-api-execution-gate.md` for one private YouTube Data API video upload plus selected-thumbnail follow-up. The user selected an API route rather than manual entry; `channel/episodes/s01e01-campus-cafe-longplay/source/youtube-api-video-upload-package.md`, `channel/episodes/s01e01-campus-cafe-longplay/source/youtube-video-resource.json`, `scripts/youtube_api_video_upload.py`, and `scripts/youtube_api_thumbnail.py` define a channel-level guarded workflow with `channels.list(mine=true)` channel verification before `videos.insert(private)` or `thumbnails.set`. The helpers read reusable `MELLOW_YOUTUBE_*` execution inputs from an external env file; the repo contains only a placeholder template at `channel/templates/youtube-api-upload-env.example`. Captions are not uploaded because subtitles are burned in. Public release is not passed; readiness remains `96/100`; public publish/schedule, browser/Studio actions, analytics, Content ID, caption upload, credentials/tokens in repo, account-state storage, and positive rights/platform-safety claims remain blocked.

## Current Source Truth

- Channel strategy: `channel/channel.md` and `channel/roadmap.md`.
- Reusable templates: `channel/templates/`, including the compact next-video fastlane worksheet in `channel/templates/episode-production-worksheet-template.md`.
- YouTube API external env template: `channel/templates/youtube-api-upload-env.example`.
- Reusable local audio candidate intake workflow: `channel/templates/audio-candidate-intake-workflow-template.md`.
- Signature visual system: `channel/signature-visual-system.md` records source-only channel motifs with stored local reference images in `channel/signature-references/`.
- Active episode truth: `channel/episodes/s01e01-campus-cafe-longplay/manifest.json`.
- Active song source: `channel/episodes/s01e01-campus-cafe-longplay/source/songs.md`.
- Active Suno manual fields index/defaults plus Episode Style & Theme Spine and Track Delta matrix: `channel/episodes/s01e01-campus-cafe-longplay/source/suno-manual-fields.md` plus `channel/episodes/s01e01-campus-cafe-longplay/reviews/suno-manual-fields.md`.
- Active Suno track copy packs: `channel/episodes/s01e01-campus-cafe-longplay/source/suno-tracks/*.md` (13 files, one per song).
- Active prompt pack: `channel/episodes/s01e01-campus-cafe-longplay/source/prompt-pack.md` plus `channel/episodes/s01e01-campus-cafe-longplay/reviews/prompt-pack.md`.
- Active candidate-intake checklist: `channel/episodes/s01e01-campus-cafe-longplay/reviews/candidate-intake-checklist.md`.
- Active audio candidate intake review: `channel/episodes/s01e01-campus-cafe-longplay/reviews/audio-candidate-intake.md`.
- Active selected audio QA/listening handoff: `channel/episodes/s01e01-campus-cafe-longplay/reviews/audio-qa-listening.md`.
- Active source-approval workflow log: `channel/episodes/s01e01-campus-cafe-longplay/reviews/source-approval-workflow.md`.
- Active lyrics review: `channel/episodes/s01e01-campus-cafe-longplay/reviews/lyrics.md`.
- Active theme retune review: `channel/episodes/s01e01-campus-cafe-longplay/reviews/theme-retune.md`.
- Active visual source: `channel/episodes/s01e01-campus-cafe-longplay/source/visual.md`, `channel/episodes/s01e01-campus-cafe-longplay/source/visual-prompt-pack.md`, `channel/episodes/s01e01-campus-cafe-longplay/source/visual-overlay-motion-plan.md`, `channel/episodes/s01e01-campus-cafe-longplay/reviews/visual-layout-proof-review.md`, and visual reviews.
- Active subtitle timing review: `channel/episodes/s01e01-campus-cafe-longplay/subtitles/README.md` and `channel/episodes/s01e01-campus-cafe-longplay/reviews/subtitle-improvement.md`.
- Active final subtitle sidecars: `channel/episodes/s01e01-campus-cafe-longplay/subtitles/s01e01-campus-cafe-longplay.en.srt` and `channel/episodes/s01e01-campus-cafe-longplay/subtitles/s01e01-campus-cafe-longplay.en.vtt`.
- Active metadata/disclosure source: `channel/episodes/s01e01-campus-cafe-longplay/source/metadata.md`.
- Active source-only YouTube API video upload package: `channel/episodes/s01e01-campus-cafe-longplay/source/youtube-api-video-upload-package.md`, `channel/episodes/s01e01-campus-cafe-longplay/source/youtube-video-resource.json`, and channel-level helper `scripts/youtube_api_video_upload.py`.
- Historical source-only manual YouTube metadata package: `channel/episodes/s01e01-campus-cafe-longplay/source/youtube-manual-upload-package.md`.
- Active assembly package plan: `channel/episodes/s01e01-campus-cafe-longplay/reviews/assembly-package.md`.
- Active render/export plan: `channel/episodes/s01e01-campus-cafe-longplay/reviews/render-export-plan.md`.
- Active render/export QA result: `channel/episodes/s01e01-campus-cafe-longplay/reviews/render-export-qa.md`.
- Active release decision planning gate: `channel/episodes/s01e01-campus-cafe-longplay/reviews/release-decision-plan.md`.
- Active YouTube API execution gate: `channel/episodes/s01e01-campus-cafe-longplay/reviews/youtube-api-execution-gate.md`.
- Active tracking: `channel/episodes/s01e01-campus-cafe-longplay/tracking/*.csv`.

## Current Decisions

- The first episode direction is `After-School First Love Longplay`: after-school cafe table, notebook, coffee or milk tea, school courtyard, and wholesome PG same-age teenage/high-school first-love details.
- Baseline format is 12 main songs plus 1 bonus full closing song, English-first, target about 30-35 minutes if later generated naturally.
- Controlled variation is limited to one piano-forward song and one soft sax accent song unless re-reviewed.
- Prior track checkpoint is historical only because the set was replaced by explicit user rejection.
- Fresh human or external review is required before any future manual provider gate.
- Track 1 opener is now `Margin Notes at Table Three` v0.6, Track 2 is now `Two Lids, One Tray` v0.9 macro-form revision, and Track 3 is now `Borrowed Eraser, Written Name` v1.0; the user accepted Tracks 1-3 as OK. Track 4 was retitled from instrument-led `Piano Between Shelves` to story-led `Checkout Slip at Chapter Nine` v1.1 while preserving the piano-forward arrangement note. Track 5 `Steam on the Glass Door` v1.0 uses title/lyric independence: the exact title is absent from the lyric and works as a mood/scene label. Track 6 is `Peach Can at B4`, Track 7 is `Green Dot on Your Schedule`, Track 8 is `Cushion Seat, Charging Cord`, Track 9 is `Crosswalk Stripes Before Six`, Track 10 is `Yellow Tag on the Umbrella Rack`, Track 11 is `Quiz Key in Blue Ink`, Track 12 is `Tray Return at 5:59`, and bonus Track 13 is `Latch Click at the Courtyard Gate`. This is source-only and not provider/media/release approval.
- Source approval workflow now requires a strict micro-pattern gate before approval: compare previous three tracks for title-repeat count, chorus shape, `No ..., no ...`/`No big...`/`Maybe...` rhetoric, bridge opener, final-hook stacking, and repeated small-object payoffs.
- Source approval workflow now requires a Story + Reference Brief before lyrics and a title/arrangement separation gate: instruments belong in arrangement notes/Styles unless they are real story objects.
- Source approval workflow now also requires a title/lyric relationship gate: titles do not have to appear in lyrics or hooks if the imagery earns the title.
- Source approval workflow now also requires issue-led review carryover from prior blockers, accidental named-reference collision scanning, and explicit approximate BPM in every Suno `Styles` field before future manual handoff review.
- Source approval workflow now requires an Episode Style & Theme Spine before track drafting and a controlled Track Delta for each new or revised track, including story/object function, macro/rhetorical change, style/BPM change, and motif/lexical change against the spine and nearby tracks.
- Future episode lyric workflow must maintain a Lexical Count Ledger per song: count high-salience nouns, pronouns, adjectives/adverbs, colors, object words, and hook/payoff terms, then lower nonessential repeats in following songs. S01E01 is not being revised solely for this; carry the lesson forward.
- Source-only Suno manual handoff is split into 13 copy-ready per-track files under `source/suno-tracks/`; `source/suno-manual-fields.md` now acts as index/defaults. These remain source-only and are not provider approval or media approval.
- Source-only Suno prompt retune research trail is recorded in `channel/episodes/s01e01-campus-cafe-longplay/reviews/suno-prompt-research.md`; style/exclude wording and control values were retuned for clearer less repetitive prompts.
- Source-only prompt/control pack is theme-retuned; it is not provider approval or media approval.
- Candidate-intake checklist is now active for local user-supplied S01E01 audio files; candidate IDs exist only for local audio evidence and do not approve provider/media/render/release actions.
- S01E01 local audio candidate intake is recorded: 26 user-supplied WAV candidates were organized into a selected draft set and a pool set. User human listening pass, Gemini supplemental lyric anchor spot-check pass, and 41:31 duration/sequence acceptance are recorded source-only. This is not render/export/upload/release approval.
- The local audio candidate intake + Gemini supplemental A/B method is confirmed usable and recorded as a reusable workflow template for future episodes.
- Source-only visual prompt pack is theme-retuned; `G.png` is recorded as visual background direction `vis-c01`; V6 cute-smooth motion proof was created after user rejected V4-07 and revised V5 for cuter readable typography, smoother equalizer behavior, slower parallax, local hair/leaf motion, header hold, and title slide-in/out. User passed V6 as the visual direction source-only; all Tracks 1-13 subtitle draft timings are also human watch-passed source-only. This is not image generation approval, full render/export approval, or release approval.
- Current audio candidates, static visual proof images, V4-07 proof, V5 proof, V6 proof, subtitle timing proofs, and render-01 through render-05 local render/export QA outputs exist as ignored local evidence only; Gate 8 chapter timestamps are source-passed with 1s gaps, Gate 10 subtitle/source timing plan is source-passed with all tracks human watch-passed, Gate 11 metadata/disclosure is source-passed, Gate 12 internal readiness scorecard is source-passed, source-only assembly package planning is source-passed, final English sidecars are promoted source-only with Track 1 cue 58 corrected, render/export planning is passed, render-01 is superseded by human visual FAIL, render-02/render-03/render-04 are superseded, and render-05 local QA is user-approved while release gate remains blocked.
- Release decision planning is open and the OAuth/API execution gate is open for one private `videos.insert` upload plus selected-thumbnail follow-up with channel-id verification and no caption upload, but public release/public-publish approval, additional render/export output creation beyond the approved render-05 local QA output, provider/browser automation, Content ID registration, caption upload, extra thumbnail variants, credentials/tokens in repo, account-state storage, and rights/platform-safety claims remain blocked.
- Future visual prompts may reuse the channel-level signature motifs only as source-only design guidance unless a later explicit visual gate overrides that rule.
- Future videos should start from the compact next-video fastlane worksheet: reuse approved channel defaults by citation, review only changed episode deltas, and keep local render/export plus external platform/API actions behind explicit gates.

## Safety

- Candidate media under `candidates/` is ignored local evidence and should only be added after a fresh episode packet exists.
- Do not invent candidate IDs, provenance, generation dates, analytics, media existence, or release facts.
- For the active teen/high-school direction, keep all romance PG, same-age peer only, non-sexualized, non-teacher/student, and non-branded; block adult/minor framing, childlike vocal/visual framing, real school names, and revealing uniform framing.
- Use forbidden terms such as `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `upload-ready`, and `publish-ready` only as blocked/caution language.
- Before any future external platform work, require a separate explicit gate and current policy/account review.

## Verification

Run:

```bash
bash scripts/verify-standalone.sh
python3 -m pytest tests
```

# S01E01 Metadata Source — After-School First Love Longplay

Status: metadata/disclosure pack passed / OAuth API execution gate open private video plus thumbnail follow-up / render-05 local QA user-approved / public release blocked  
Prepared date: 2026-05-19
Updated: 2026-05-25

Audio candidate state: the selected draft audio content is accepted source-only at `41:31.28` in `reviews/audio-qa-listening.md`. Gate 8 sequence/chapter policy is source-only: keep track order 1-13, use `1.00s` inter-track gaps, use no crossfades, and reserve no intro/outro bumper time in this timeline. Planned sequence duration is `41:43.28` including 12 gaps. Gate 10 subtitle draft timings are human watch-passed source-only for Tracks 1-13, final English subtitle sidecars are promoted source-only in `subtitles/`, and Track 1 cue 58 text is corrected there with timing unchanged. Render/export planning is passed in `reviews/render-export-plan.md`, render-01 failed human visual review after mechanical QA, render-02/render-03/render-04 are superseded, render-05 local QA is user-approved in `reviews/render-export-qa.md`, release decision planning is open in `reviews/release-decision-plan.md`, and the OAuth/API execution gate is open in `reviews/youtube-api-execution-gate.md` for one private `videos.insert` upload using `source/youtube-api-video-upload-package.md`, `source/youtube-video-resource.json`, and channel-level helper `scripts/youtube_api_video_upload.py` plus one selected-thumbnail `thumbnails.set` follow-up using `source/youtube-api-thumbnail-upload-package.md`, `scripts/create_s01e01_thumbnail.py`, and channel-level helper `scripts/youtube_api_thumbnail.py` after a private video ID exists. Public publish, schedule, browser/Studio actions, analytics, Content ID, provider/account actions outside the private upload plus thumbnail gate, caption upload, extra thumbnail variants, and additional/revised outputs remain blocked without a new gate.

Bumper note: a simple channel intro/outro bumper can be authored locally later from existing source visuals/text without needing AI, but any actual bumper media, render/export, or revised duration must use a separate explicit future gate. This Gate 8 plan does not create or reserve bumper media.

## Sequence / Chapter Policy

| Field | Decision |
|---|---|
| Scope | Source-only chapter/timeline plan |
| Track order | Current selected draft order, Tracks 1-13 |
| Inter-track gap | `1.00s` silence/space between tracks |
| Crossfade | none |
| Intro bumper | none reserved in Gate 8 timeline |
| Outro bumper | none reserved in Gate 8 timeline |
| Audio content duration | `41:31.28` |
| Gap total | `12.00s` |
| Planned sequence duration | `41:43.28` |
| Still blocked | further sidecar revisions without a new gate, additional/revised render/export outputs beyond render-05 without a new gate, upload/publish, release readiness, rights/platform-safety claims |

## Gate 11 Metadata / Disclosure Pack

Scope: source-only metadata draft for later review. This does not approve final upload metadata, YouTube Studio/API/browser actions, render/export, release, scheduling, analytics, or platform/account changes.

### Listener-facing title draft

Primary title draft:

```text
After-School First Love Longplay | Soft Cozy Vocals for Study & Coffee Breaks
```

Title policy:

- Lead with the listener promise and episode mood, not `AI music` as the hook.
- Keep the episode PG, same-age teen/high-school, non-branded, and non-sexualized.
- Re-review if the title changes the listener job, age framing, duration promise, or release claim.

### Description draft

```text
A warm 41-minute cozy vocal longplay for study, reading, journaling, desk work, or a quiet coffee break.

This episode follows small after-school first-love moments: margin notes, two drink lids on one tray, borrowed erasers, library slips, vending-machine peach cans, schedule stickers, crosswalk stripes, umbrella tags, quiz keys, tray returns, and a gentle courtyard goodbye.

Soft vocals, mellow keys, clean guitar, rounded bass, soft drums, and airy city-pop / soft R&B color keep the mood calm and background-friendly.

Disclosure: this episode is built with AI-assisted music/visual production workflows plus human selection, source review, listening checks, subtitle timing review, and provenance tracking.
```

Description policy:

- Keep wording mood/use-case led and concrete; avoid keyword stuffing.
- Keep AI assistance disclosed in the description copy, not as the title hook.
- Do not claim the episode is human-recorded, exclusive, copyright-free, royalty-free, Content ID-safe, monetization-safe, platform-safe, upload-ready, or publish-ready.
- Re-review before any public metadata use against current platform/account policy and actual final assets.

### Chapter display draft

Display timestamps are rounded to the nearest whole second from the exact Gate 8 source timeline below. Exact chapter source remains the `Chapter Draft` table.

```text
00:00 Margin Notes at Table Three
04:41 Two Lids, One Tray
08:27 Borrowed Eraser, Written Name
11:52 Checkout Slip at Chapter Nine
15:23 Steam on the Glass Door
19:02 Peach Can at B4
21:43 Green Dot on Your Schedule
24:59 Cushion Seat, Charging Cord
27:12 Crosswalk Stripes Before Six
29:59 Yellow Tag on the Umbrella Rack
33:12 Quiz Key in Blue Ink
35:53 Tray Return at 5:59
39:13 Latch Click at the Courtyard Gate
```

### Tags policy and draft list

Tags are optional source suggestions only and must stay modest, relevant, non-branded, and non-imitation-based.

Draft tag list:

```text
mellow longplay, cozy vocal music, soft vocal longplay, soft r&b pop, city pop inspired, study music, reading music, journaling music, coffee break music, after school playlist, first love songs, relaxing vocals, English vocal longplay, cozy background music
```

Reject or re-review tags that imply a named artist/song/channel, real brand, real school, label/station affiliation, guaranteed platform outcome, or unsupported rights/safety status.

### Gate 11 verdict

`pass_metadata_disclosure_pack_source_only`

Assembly package planning is source-passed in `reviews/assembly-package.md`, final English subtitle sidecars are promoted source-only in `subtitles/`, Track 1 cue 58 source text is corrected, render/export planning is passed in `reviews/render-export-plan.md`, render-01 human visual FAIL is recorded, render-02/render-03/render-04 are superseded, and the approved render-05 local QA result is recorded in `reviews/render-export-qa.md`. Release decision planning is now open in `reviews/release-decision-plan.md`, and `source/youtube-api-video-upload-package.md`, `source/youtube-api-thumbnail-upload-package.md`, plus `reviews/youtube-api-execution-gate.md` define the open private video plus selected-thumbnail YouTube Data API execution path with channel-id verification and no caption upload. Public release is not passed. Public publish, schedule, analytics, platform/account actions outside the private upload plus thumbnail gate, caption upload, extra thumbnail variants, additional/revised outputs without a new gate, and rights/platform-safety claims remain blocked.

## Chapter Draft

| Track | Working title | Selected draft duration | Chapter start | Track audio end | Gap after | Notes |
|---:|---|---:|---:|---:|---:|---|
| 1 | Margin Notes at Table Three | 279.92s | 00:00.00 | 04:39.92 | 1.00s | selected audio accepted; Track 1 subtitle proof human watch-passed source-only; cue 58 text corrected in final sidecars |
| 2 | Two Lids, One Tray | 225.00s | 04:40.92 | 08:25.92 | 1.00s | selected audio accepted |
| 3 | Borrowed Eraser, Written Name | 204.12s | 08:26.92 | 11:51.04 | 1.00s | selected audio accepted |
| 4 | Checkout Slip at Chapter Nine | 209.56s | 11:52.04 | 15:21.60 | 1.00s | selected audio accepted |
| 5 | Steam on the Glass Door | 218.40s | 15:22.60 | 19:01.00 | 1.00s | selected audio accepted |
| 6 | Peach Can at B4 | 159.92s | 19:02.00 | 21:41.92 | 1.00s | selected audio accepted |
| 7 | Green Dot on Your Schedule | 194.92s | 21:42.92 | 24:57.84 | 1.00s | selected audio accepted |
| 8 | Cushion Seat, Charging Cord | 131.88s | 24:58.84 | 27:10.72 | 1.00s | selected audio accepted; short track accepted within source-only sequence |
| 9 | Crosswalk Stripes Before Six | 165.92s | 27:11.72 | 29:57.64 | 1.00s | selected audio accepted |
| 10 | Yellow Tag on the Umbrella Rack | 192.44s | 29:58.64 | 33:11.08 | 1.00s | selected audio accepted |
| 11 | Quiz Key in Blue Ink | 159.88s | 33:12.08 | 35:51.96 | 1.00s | selected audio accepted |
| 12 | Tray Return at 5:59 | 199.32s | 35:52.96 | 39:12.28 | 1.00s | selected audio accepted |
| 13 bonus | Latch Click at the Courtyard Gate | 150.00s | 39:13.28 | 41:43.28 | none | selected audio accepted with Track 13 opening-dialogue caveat |

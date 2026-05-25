# S01E01 YouTube API Video Upload Package — After-School First Love Longplay

Status: private video upload completed / thumbnail follow-up separate completed / captions not uploaded / public release not passed  
Episode: `s01e01-campus-cafe-longplay`  
Prepared: 2026-05-25

## 0. Boundary

This file records the S01E01 video-upload packet for the channel-level OAuth/API helper after the user selected the API route. It scoped only one `videos.insert` private video upload after authenticated channel verification succeeded and after OAuth client secrets/token-cache paths were supplied outside this repo. Thumbnail upload is handled by the separate package `source/youtube-api-thumbnail-upload-package.md` and generic helper `scripts/youtube_api_thumbnail.py`; the video helper must not call `thumbnails.set`. This file does not approve browser automation, public publishing, scheduling, visibility mutation after upload, captions, analytics, account edits, playlist edits, comments, Content ID action, credentials or tokens stored in repo, private account-state storage, extra thumbnail variants, or positive rights/platform claims.

The allowed API action for this execution gate is only:

```text
channels.list(mine=true) -> verify authenticated channel ID
videos.insert -> upload the render-05 MP4 with metadata as private
```

Caption upload is intentionally out of scope because the current render has burned-in subtitles. `captions.insert` must not be called for this S01E01 API path unless a new gate changes that decision.

Thumbnail upload is out of scope for this video helper. The selected local thumbnail JPEG and its `thumbnails.set` follow-up are recorded separately in `source/youtube-api-thumbnail-upload-package.md`.

Do not store OAuth client secrets, OAuth tokens, cookies, browser profiles, private analytics exports, account IDs, screenshots of private account state, or generated account-state files in this repo.

Do not describe this episode, render, audio, visual, sidecars, or channel as `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `platform-safe`, `exclusive`, `upload-ready`, or `publish-ready` except as blocked/caution language.

## 1. Source Inputs

| Item | Source path / value | Notes |
|---|---|---|
| Video candidate | `candidates/s01e01-campus-cafe-longplay/render/future-local-render-05/video/s01e01-campus-cafe-longplay.v6-subtitled-1080p24-qa.mp4` | Current user-approved local QA output only. |
| Metadata source | `channel/episodes/s01e01-campus-cafe-longplay/source/metadata.md` | Gate 11 title, description, chapters, tags, and disclosure source. |
| API helper | `scripts/youtube_api_video_upload.py` | Channel-level dry-run default helper. Refuses execution without channel-id and OAuth path guards; accepts per-video `--episode-id`, `--video`, `--resource-json`, and `--metadata-source`. |
| API resource JSON | `channel/episodes/s01e01-campus-cafe-longplay/source/youtube-video-resource.json` | Per-video request body for `videos.insert`; helper validates `privacyStatus: private` and no captions/thumbnail fields. |
| Caption sidecars | `channel/episodes/s01e01-campus-cafe-longplay/subtitles/` | Source sidecars remain evidence/source only for this route; do not upload via API because captions are burned in. |
| Thumbnail | `candidates/s01e01-campus-cafe-longplay/thumbnail/s01e01-campus-cafe-longplay.thumbnail-v4-big-brand-depth-1280x720.jpg` | User-approved selected local derivative from `G.png`; upload is handled by `scripts/youtube_api_thumbnail.py`, not this video helper. |

## 2. API Resource Draft

`videos.insert` request parts:

```text
snippet,status
```

Video resource draft:

```json
{
  "snippet": {
    "title": "After-School First Love Longplay | Soft Cozy Vocals for Study & Coffee Breaks",
    "description": "A warm 41-minute cozy vocal longplay for study, reading, journaling, desk work, or a quiet coffee break.\n\nThis episode follows small after-school first-love moments: margin notes, two drink lids on one tray, borrowed erasers, library slips, vending-machine peach cans, schedule stickers, crosswalk stripes, umbrella tags, quiz keys, tray returns, and a gentle courtyard goodbye.\n\nSoft vocals, mellow keys, clean guitar, rounded bass, soft drums, and airy city-pop / soft R&B color keep the mood calm and background-friendly.\n\nDisclosure: this episode uses AI-assisted music and visual production workflows, with human selection, source review, listening checks, subtitle timing review, and provenance tracking.\n\nChapters:\n00:00 Margin Notes at Table Three\n04:41 Two Lids, One Tray\n08:27 Borrowed Eraser, Written Name\n11:52 Checkout Slip at Chapter Nine\n15:23 Steam on the Glass Door\n19:02 Peach Can at B4\n21:43 Green Dot on Your Schedule\n24:59 Cushion Seat, Charging Cord\n27:12 Crosswalk Stripes Before Six\n29:59 Yellow Tag on the Umbrella Rack\n33:12 Quiz Key in Blue Ink\n35:53 Tray Return at 5:59\n39:13 Latch Click at the Courtyard Gate",
    "tags": [
      "mellow longplay",
      "cozy vocal music",
      "soft vocal longplay",
      "soft r&b pop",
      "city pop inspired",
      "study music",
      "reading music",
      "journaling music",
      "coffee break music",
      "after school playlist",
      "first love songs",
      "relaxing vocals",
      "English vocal longplay",
      "cozy background music"
    ],
    "categoryId": "10",
    "defaultLanguage": "en"
  },
  "status": {
    "privacyStatus": "private",
    "selfDeclaredMadeForKids": false,
    "containsSyntheticMedia": true,
    "license": "youtube"
  }
}
```

## 3. Channel Verification Rule

The helper must verify the authenticated channel before any `videos.insert` call:

```text
1. Call channels.list(part="id,snippet", mine=true).
2. Require exactly one channel in the response.
3. Compare response id against a user-provided expected channel ID.
4. Abort before upload if the expected channel ID is missing or mismatched.
```

The expected channel ID is intentionally not stored in repo source until the user chooses to record a non-secret channel identifier. If the user treats the channel ID as private, keep it outside the repo and pass it only at execution time.

## 4. Helper Behavior

Dry-run default:

```bash
python3 scripts/youtube_api_video_upload.py --expected-channel-id UC_REPLACE_WITH_TARGET_CHANNEL_ID
```

External env-file execution mode under this gate:

```bash
python3 scripts/youtube_api_video_upload.py \
  --execute \
  --env-file "$HOME/.config/mellow-longplay/youtube-upload/channel.env"
```

Direct flag execution mode under this gate:

```bash
python3 scripts/youtube_api_video_upload.py \
  --execute \
  --expected-channel-id UC_REPLACE_WITH_TARGET_CHANNEL_ID \
  --client-secrets /path/outside/repo/client_secret.json \
  --token-cache /path/outside/repo/youtube-token.json
```

Execution guards:

- Refuse `--execute` without `--expected-channel-id`.
- Refuse `--env-file` paths inside this repository.
- Refuse OAuth client secrets or token-cache paths inside this repository.
- Verify the authenticated channel ID before `videos.insert`.
- Use `privacyStatus: private` by default.
- Do not call `captions.insert`.
- Do not call `thumbnails.set` from this video helper; use the separate thumbnail helper after a private video ID exists.
- Do not call playlist, comments, analytics, Content ID, publish, schedule, unlist, delete, or metadata-update operations.

## 5. Execution Gate Packet

```text
Scope: one S01E01 render-05 MP4 upload through YouTube Data API videos.insert only
Mode: OAuth/API execution completed for private upload only
Allowed operations: channels.list(mine=true), videos.insert(private)
Required user inputs at execution time: expected channel ID, OAuth client secrets path outside repo, token-cache path outside repo; may be supplied via an external env file
Credential storage: outside repo only; do not commit, copy, summarize, screenshot, or store tokens/account state here
Blocked operations for this helper: public publish, schedule, visibility update, captions.insert, thumbnails.set from the video helper, playlist action, comments, analytics, Content ID, browser automation, account edits, metadata update after upload
Stop triggers: channel ID mismatch, missing expected channel ID, OAuth paths inside repo, missing local video file, API project/account upload restriction, YouTube copyright/policy/checks notice, user concern changing asset or metadata selection
```

## 6. Current Verdict

```text
Verdict: oauth_api_private_video_upload_completed_public_release_not_passed
Scope: video-only YouTube Data API videos.insert execution after channel verification
Current local QA output: render-05 user-approved local QA only
Caption decision: no API caption upload because subtitles are burned into the render
Channel safety: helper must verify authenticated channel id before videos.insert
Default visibility: private
Execution result: guarded private videos.insert returned video ID 4pOLXPMQO5g for verified channel UC4qQwe3oiykEGhL_WyVFtMg; captions were not uploaded by this route
Still blocked from this helper: public publish schedule Studio browser analytics Content ID credentials or tokens in repo account-state storage caption upload thumbnail upload playlist comments metadata update after upload and positive rights/platform claims
```

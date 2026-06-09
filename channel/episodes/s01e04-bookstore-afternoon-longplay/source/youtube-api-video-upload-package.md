# S01E04 YouTube API Video Upload Package — Bookstore Afternoon Longplay

Status: uploaded successfully (private) / final-video approved / public release blocked
Episode: `s01e04-bookstore-afternoon-longplay`
Prepared: 2026-06-05

## 0. Boundary

This file records the S01E04 video-upload packet for the channel-level OAuth/API helper. It scopes only one `videos.insert` private video upload after authenticated channel verification succeeds and after OAuth client secrets/token-cache paths are supplied outside this repo. Thumbnail upload is handled separately; the video helper must not call `thumbnails.set`. This file does not approve browser automation, public publishing, scheduling, visibility mutation after upload, captions, analytics, account edits, playlist edits, comments, Content ID action, credentials or tokens stored in repo, private account-state storage, or positive rights/platform claims.

The allowed API action for this execution gate is only:

```text
channels.list(mine=true) -> verify authenticated channel ID
videos.insert -> upload the render-01 MP4 with metadata as private
```

Caption upload is out of scope because subtitles are burned in.

Do not store OAuth client secrets, OAuth tokens, cookies, browser profiles, private analytics exports, account IDs, or credentials in this repo.

Do not describe this episode, render, audio, visual, sidecars, or channel as `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `platform-safe`, `upload-ready`, or `publish-ready`.

## 1. Source Inputs

| Item | Source path / value | Notes |
|---|---|---|
| Video candidate | `candidates/s01e04-bookstore-afternoon-longplay/render/local-render-01/video/s01e04-bookstore-afternoon-longplay.local-render-01-draft-subtitled-9703dfb504f822-1080p24-qa.mp4` | User-approved final-video candidate. |
| Metadata source | `channel/episodes/s01e04-bookstore-afternoon-longplay/source/metadata.md` | Gate 1 title, description, chapters, tags, and disclosure source. |
| API helper | `scripts/youtube_api_video_upload.py` | Generic guarded dry-run default helper. |
| API resource JSON | `channel/episodes/s01e04-bookstore-afternoon-longplay/source/youtube-video-resource.json` | Request body for `videos.insert`; validates `privacyStatus: private` and no captions/thumbnail fields. |

## 2. API Resource Draft

`videos.insert` request parts:

```text
snippet,status
```

Video resource draft: (synced with `youtube-video-resource.json`)

## 3. Channel Verification Rule

The helper must verify the authenticated channel before any `videos.insert` call:

```text
1. Call channels.list(part="id,snippet", mine=true).
2. Require exactly one channel in the response.
3. Compare response id against a user-provided expected channel ID.
4. Abort before upload if the expected channel ID is missing or mismatched.
```

## 4. Dry-Run Check Command

Ensure you test the configuration using dry-run first:

```bash
bash scripts/dev-python.sh scripts/youtube_api_video_upload.py \
  --episode-id s01e04-bookstore-afternoon-longplay \
  --video candidates/s01e04-bookstore-afternoon-longplay/render/local-render-01/video/s01e04-bookstore-afternoon-longplay.local-render-01-draft-subtitled-9703dfb504f822-1080p24-qa.mp4 \
  --resource-json channel/episodes/s01e04-bookstore-afternoon-longplay/source/youtube-video-resource.json \
  --metadata-source channel/episodes/s01e04-bookstore-afternoon-longplay/source/youtube-api-video-upload-package.md \
  --expected-channel-id UC4qQwe3oiykEGhL_WyVFtMg
```

## 5. Execution Gate Packet

```text
Scope: S01E04 render-01 MP4 upload through YouTube Data API videos.insert only
Mode: executed private upload completed (video is private)
Allowed operations: channels.list(mine=true), videos.insert(private)
Required user inputs at execution time: expected channel ID, OAuth client secrets path outside repo, token-cache path outside repo; may be supplied via an external env file
Credential storage: outside repo only; do not commit, copy, summarize, screenshot, or store tokens/account state here
Blocked operations for this helper: public publish, schedule, visibility update, captions.insert, thumbnails.set from the video helper, playlist action, comments, analytics, Content ID, browser automation, account edits, metadata update after upload
```

## 6. Current Verdict

```text
Verdict: youtube_video_private_upload_completed
Result: private upload completed via YouTube Data API videos.insert on 2026-06-08
Video ID: OMjvEEAIFSU
Channel: UC4qQwe3oiykEGhL_WyVFtMg
```

# S01E03 YouTube API Video Upload Package — Rooftop Golden Hour Longplay

Status: upload completed / top-level comment posted after retry / pin pending
Episode: `s01e03-rooftop-golden-hour-longplay`
Prepared: 2026-06-02

## 0. Boundary

This file records the S01E03 video-upload packet for the channel-level OAuth/API helper. It scoped one `videos.insert` video upload after authenticated channel verification succeeded and after OAuth client secrets/token-cache paths were supplied outside this repo. The user approved the exact render-02 video candidate for upload on 2026-06-02. The upload completed as video ID `2P6fPs7NB0E`; the helper initially returned `privacy_status: private`, and a later API check during comment retry observed `privacyStatus: public` and `uploadStatus: processed`. Thumbnail upload remains a separate action unless explicitly gated elsewhere.

The allowed API action for this execution gate is only:

```text
channels.list(mine=true) -> verify authenticated channel ID
videos.insert -> upload the render-02 MP4 with metadata as private
```

The user also requested a pinned comment. The helper first attempted one top-level comment with `commentThreads.insert` after the video ID existed, but YouTube returned `403 forbidden`. Retrying after the video was observed as public/processed succeeded and created comment ID `Ugw3CXuFnYeKOp4TNi54AaABAg`. The API helper does not pin comments. Comment pinning remains a manual/browser action after upload unless a separate verified path is used.

Caption upload is out of scope because subtitles are burned in.

Do not store OAuth client secrets, OAuth tokens, cookies, browser profiles, private analytics exports, account IDs, or credentials in this repo.

Do not describe this episode, render, audio, visual, sidecars, or channel as `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `platform-safe`, `upload-ready`, or `publish-ready`.

## 1. Source Inputs

| Item | Source path / value | Notes |
|---|---|---|
| Video candidate | `candidates/s01e03-rooftop-golden-hour-longplay/render/local-render-02/video/s01e03-rooftop-golden-hour-longplay.local-render-02-draft-subtitled-1080p24-qa.mp4` | Render-02 final-video candidate approved by user for upload. |
| Metadata source | `channel/episodes/s01e03-rooftop-golden-hour-longplay/source/metadata.md` | Gate 1 title, description, chapters, tags, disclosure, and comment draft source. |
| Comment source | `channel/episodes/s01e03-rooftop-golden-hour-longplay/source/comment.txt` | Top-level community comment draft. |
| API helper | `scripts/youtube_api_video_upload.py` | Generic guarded dry-run default helper. |
| API resource JSON | `channel/episodes/s01e03-rooftop-golden-hour-longplay/source/youtube-video-resource.json` | Request body for `videos.insert`; validates `privacyStatus: private` and no captions/thumbnail fields. |

## 2. API Resource Draft

`videos.insert` request parts:

```text
snippet,status
```

Video resource draft is synced with `youtube-video-resource.json`.

## 3. Channel Verification Rule

The helper must verify the authenticated channel before any `videos.insert` call:

```text
1. Call channels.list(part="id,snippet", mine=true).
2. Require exactly one channel in the response.
3. Compare response id against a user-provided expected channel ID.
4. Abort before upload if the expected channel ID is missing or mismatched.
```

## 4. Dry-Run Check Command

```bash
bash scripts/dev-python.sh scripts/youtube_api_video_upload.py \
  --episode-id s01e03-rooftop-golden-hour-longplay \
  --video candidates/s01e03-rooftop-golden-hour-longplay/render/local-render-02/video/s01e03-rooftop-golden-hour-longplay.local-render-02-draft-subtitled-1080p24-qa.mp4 \
  --resource-json channel/episodes/s01e03-rooftop-golden-hour-longplay/source/youtube-video-resource.json \
  --metadata-source channel/episodes/s01e03-rooftop-golden-hour-longplay/source/youtube-api-video-upload-package.md \
  --comment-file channel/episodes/s01e03-rooftop-golden-hour-longplay/source/comment.txt \
  --env-file "/Users/xiivth/.config/mellow-longplay/.secret/channel.env"
```

## 5. Execution Gate Packet

```text
Scope: S01E03 render-02 MP4 upload through YouTube Data API videos.insert only, with optional top-level commentThreads.insert after the returned video ID
Mode: completed private upload only
Allowed operations: channels.list(mine=true), videos.insert(private), commentThreads.insert(top-level)
Required user inputs at execution time: expected channel ID, OAuth client secrets path outside repo, token-cache path outside repo; may be supplied via an external env file
Credential storage: outside repo only; do not commit, copy, summarize, screenshot, or store tokens/account state here
Blocked operations for this helper: public publish, schedule, visibility update, captions.insert, thumbnails.set from the video helper, playlist action, analytics, Content ID, browser automation, account edits, metadata update after upload, comment pinning
```

## 6. Execution Result

```text
Video ID: 2P6fPs7NB0E
Verified channel ID: UC4qQwe3oiykEGhL_WyVFtMg
Initial helper privacy status: private
Later API observation during comment retry: privacyStatus public, uploadStatus processed
Caption upload attempted: false
Thumbnail upload attempted: false
First comment attempt: 403 forbidden; comment thread could not be created due to insufficient permissions / request might not be properly authorized
Retry comment posted: true
Comment ID: Ugw3CXuFnYeKOp4TNi54AaABAg
Comment thread ID: Ugw3CXuFnYeKOp4TNi54AaABAg
```

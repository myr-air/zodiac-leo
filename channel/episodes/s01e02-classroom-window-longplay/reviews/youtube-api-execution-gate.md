# S01E02 YouTube API Execution Gate — Classroom Window Longplay

Status: private video API upload completed / selected thumbnail set completed / public release not passed
Episode: `s01e02-classroom-window-longplay`
Opened: 2026-05-29

## 0. Boundary

The user opened the OAuth/API execution gate for the API route. This gate allowed one YouTube Data API `videos.insert` upload of the render-02 MP4 as `private`. The helper verified that the authenticated channel ID matches the user-provided expected channel ID before any API mutation.

This gate does not approve public publishing, scheduling, visibility changes after upload, captions, playlists, comments, analytics, Content ID action, browser automation, YouTube Studio edits, account edits, credential storage in repo, private account-state storage, thumbnail upload, extra thumbnail variants, or positive rights/platform claims.

## 1. Security Packet

```text
Scope: one private S01E02 render-02 video upload using YouTube Data API videos.insert
Mode: narrow execution gate; not public release
Assets: render-02 MP4, metadata payload from source/metadata.md and source/youtube-api-video-upload-package.md
Actors: user-owned Google/YouTube account, OpenCode helper script, YouTube Data API
Trust boundaries: local repo -> external OAuth flow -> YouTube account/channel -> YouTube Data API
Lanes selected: Secrets/Crypto, External Boundary, Agent/Automation, Data Exposure, Abuse/Business Logic
Lanes skipped: Authn/Authz application roles are not implemented here; Config/Deployment and Migration/Destructive Ops are not touched
Allowed actions: channels.list(mine=true), videos.insert(private)
Blocked actions: public publish, schedule, visibility update, captions.insert, playlist/comment/analytics/Content ID/account operations, browser automation, token or client-secret storage in repo, thumbnail upload, extra thumbnail variants
Required inputs: expected channel ID, OAuth client secrets path outside repo, token cache path outside repo; may be supplied through an external env file
Stop triggers: missing or mismatched channel ID, OAuth paths inside repo, missing local video, API/client dependency failure, account upload limit/verification issue, YouTube checks/policy/copyright notice, any user concern requiring metadata or asset change
```

## 2. Env File Workflow

Use one channel-level env file only outside the repository. Reusable env file is at:
`/Users/xiivth/.config/mellow-longplay/.secret/channel.env`

The environment keys:
```text
MELLOW_YOUTUBE_EXPECTED_CHANNEL_ID=UC4qQwe3oiykEGhL_WyVFtMg
MELLOW_YOUTUBE_CLIENT_SECRETS=/Users/xiivth/.config/mellow-longplay/.secret/client_secret.json
MELLOW_YOUTUBE_TOKEN_CACHE=/Users/xiivth/.config/mellow-longplay/.secret/youtube-token.json
```

## 3. Execution Command Shape

Execution under this open gate:

```bash
uv run --project /Users/xiivth/workspaces/zodiac/leo --with google-api-python-client,google-auth,google-auth-oauthlib python scripts/youtube_api_video_upload.py \
  --execute \
  --env-file /Users/xiivth/.config/mellow-longplay/.secret/channel.env \
  --episode-id s01e02-classroom-window-longplay \
  --video candidates/s01e02-classroom-window-longplay/render/local-render-02/video/s01e02-classroom-window-longplay.local-render-02-draft-subtitled-1080p24-qa.mp4 \
  --resource-json channel/episodes/s01e02-classroom-window-longplay/source/youtube-video-resource.json \
  --metadata-source channel/episodes/s01e02-classroom-window-longplay/source/youtube-api-video-upload-package.md
```

## 4. Current Verdict

```text
Verdict: oauth_api_private_video_upload_completed_selected_thumbnail_set_public_release_not_passed
Allowed API calls for this completed S01E02 execution: channels.list(mine=true), videos.insert(private), thumbnails.set after private video ID exists
Upload target: render-02 MP4 only
Caption upload: blocked because subtitles are burned in
Thumbnail upload: selected local JPEG derivative from vis-c01 only
Public release: not passed
Credential/account storage in repo: blocked
```

## 5. Execution Evidence

```text
Private video ID used for thumbnail follow-up: KZNjs0Z7-Pw
Verified channel ID for thumbnail follow-up: UC4qQwe3oiykEGhL_WyVFtMg
Selected thumbnail path: candidates/s01e02-classroom-window-longplay/thumbnail/s01e02-classroom-window-longplay.thumbnail-v4-big-brand-depth-1280x720.jpg
Thumbnail API result: thumbnails.set returned youtube#thumbnailSetResponse with a maxres 1280x720 variant
Still blocked: public publish, schedule, visibility mutation, captions, playlists, comments, analytics, Content ID, browser automation, account edits, credential storage in repo, and positive rights/platform claims
```

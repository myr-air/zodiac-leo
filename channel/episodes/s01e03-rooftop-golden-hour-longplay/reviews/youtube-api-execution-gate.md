# S01E03 YouTube API Execution Gate — Rooftop Golden Hour Longplay

Status: YouTube API upload completed / thumbnail set / top-level comment posted after retry / pin pending
Episode: `s01e03-rooftop-golden-hour-longplay`
Opened: 2026-06-02

## 0. Boundary

The user opened the OAuth/API execution gate for the API route on 2026-06-02 and approved the exact render-02 final-video candidate for upload to YouTube. This gate allowed one YouTube Data API `videos.insert` upload of the render-02 MP4 as `private`. The helper verified that the authenticated channel ID matched the user-provided expected channel ID before any API mutation.

The user also requested a pinned comment. The helper first attempted the approved top-level comment with `commentThreads.insert` after the private video ID existed, but YouTube returned a `403 forbidden` response. A later API check observed the video as `public` and `processed`; retrying `commentThreads.insert` then succeeded and created comment ID `Ugw3CXuFnYeKOp4TNi54AaABAg`. No comment pinning was attempted because the project helper and current official API surface do not provide a pin-comment operation.

This gate does not approve scheduling, captions, playlists, analytics, Content ID action, YouTube Studio edits, account edits, credential storage in repo, private account-state storage, extra thumbnail variants, comment pinning, or positive rights/platform claims. Initial upload helper output returned `private`, but the later retry check observed `privacyStatus: public`; this file records that observed API state without treating it as a rights/platform-safety claim.

## 1. Security Packet

```text
Scope: one S01E03 render-02 video upload using YouTube Data API videos.insert, plus top-level commentThreads.insert after video ID existed
Mode: narrow execution gate; not public release
Assets: render-02 MP4, metadata payload from source/metadata.md and source/youtube-api-video-upload-package.md, comment draft from source/comment.txt
Actors: user-owned Google/YouTube account, local helper script, YouTube Data API
Trust boundaries: local repo -> external OAuth flow -> YouTube account/channel -> YouTube Data API
Allowed actions completed: channels.list(mine=true), videos.insert, commentThreads.insert(top-level), thumbnails.set
Blocked actions: public publish, schedule, visibility update, captions.insert, playlist/analytics/Content ID/account operations, browser automation, token or client-secret storage in repo, thumbnail upload, extra thumbnail variants, comment pinning
Required inputs: expected channel ID, OAuth client secrets path outside repo, token cache path outside repo; supplied through an external env file
Stop triggers: missing or mismatched channel ID, OAuth paths inside repo, missing local video, API/client dependency failure, account upload limit/verification issue, YouTube checks/policy/copyright notice, comment API rejection, any user concern requiring metadata or asset change
```

## 2. Env File Workflow

Reusable env file is outside the repository:

```text
/Users/xiivth/.config/mellow-longplay/.secret/channel.env
```

Do not copy, summarize, screenshot, or store real OAuth client secrets, OAuth tokens, cookies, browser profiles, private analytics exports, or private account-state files in this repo.

## 3. Execution Command Shape

Execution used this guarded shape:

```bash
uv run --project /Users/xiivth/workspaces/zodiac/leo --with google-api-python-client --with google-auth --with google-auth-oauthlib python scripts/youtube_api_video_upload.py \
  --execute \
  --env-file /Users/xiivth/.config/mellow-longplay/.secret/channel.env \
  --episode-id s01e03-rooftop-golden-hour-longplay \
  --video candidates/s01e03-rooftop-golden-hour-longplay/render/local-render-02/video/s01e03-rooftop-golden-hour-longplay.local-render-02-draft-subtitled-1080p24-qa.mp4 \
  --resource-json channel/episodes/s01e03-rooftop-golden-hour-longplay/source/youtube-video-resource.json \
  --metadata-source channel/episodes/s01e03-rooftop-golden-hour-longplay/source/youtube-api-video-upload-package.md \
  --comment-file channel/episodes/s01e03-rooftop-golden-hour-longplay/source/comment.txt
```

## 4. Current Verdict

```text
Verdict: oauth_api_video_upload_completed_thumbnail_set_comment_posted_pin_pending
Allowed API calls for this completed S01E03 execution: channels.list(mine=true), videos.insert, commentThreads.insert(top-level), thumbnails.set
Upload target: render-02 MP4 only
Caption upload: blocked because subtitles are burned in
Thumbnail upload: completed with selected local PNG
Visibility state: initial helper result returned private; later API check observed public and processed
Comment state: top-level comment created as Ugw3CXuFnYeKOp4TNi54AaABAg; pinning remains pending/manual after an explicit comment/pin path is available
Credential/account storage in repo: blocked
```

## 5. Execution Evidence

```text
Video ID: 2P6fPs7NB0E
Verified channel ID: UC4qQwe3oiykEGhL_WyVFtMg
Privacy status returned by upload helper: private
Later API observation during comment retry: privacyStatus public, uploadStatus processed
Caption upload attempted: false
Thumbnail upload attempted: true
Thumbnail path: candidates/s01e03-rooftop-golden-hour-longplay/thumbnail/s01e03-rooftop-golden-hour-longplay.thumbnail-layered-premium-1280x720.png
Thumbnail API result: thumbnails.set returned youtube#thumbnailSetResponse with a maxres 1280x720 variant
First comment API response: 403 forbidden; comment thread could not be created due to insufficient permissions / request might not be properly authorized
Retry comment posted: true
Comment ID: Ugw3CXuFnYeKOp4TNi54AaABAg
Comment thread ID: Ugw3CXuFnYeKOp4TNi54AaABAg
Still blocked: schedule, visibility mutation unless explicitly requested, captions, thumbnail upload, playlists, analytics, Content ID, browser automation, account edits, credential storage in repo, private account-state storage, comment pinning, and positive rights/platform claims
```

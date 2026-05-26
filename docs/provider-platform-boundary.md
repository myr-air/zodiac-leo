# Provider And Platform Boundary

Status: active  
Updated: 2026-05-27

## Suno Boundary

No active provider generation is approved. OpenCode must not operate Suno, automate a browser, call provider APIs, scrape, download, upload, mutate accounts, or create candidate provenance before files exist.

Future provider use requires a fresh source review if any of these change:

- Provider, model, plan, account boundary, generation mode, or UI feature.
- Lyrics, style prompts, exclude prompts, controls, helper-packaged fields, voice settings, uploaded source, personalization, cover/remix mode, or disclosure wording.

## YouTube Boundary

Current exception status: S01E01 used the narrow OAuth/API execution gate in `channel/episodes/s01e01-campus-cafe-longplay/reviews/youtube-api-execution-gate.md` for one private YouTube Data API `videos.insert` upload plus one selected-thumbnail `thumbnails.set` follow-up after authenticated channel verification. Credentials and tokens must stay outside the repo. No further YouTube platform/API mutation is approved without a new explicit gate.

No public publish, schedule, Studio/browser automation, Analytics API, playlist action, metadata edit after upload, comment action, unlist/delete, channel rename, caption upload, extra thumbnail variant, account edit, Content ID action, or positive platform/rights claim is approved in this standalone scope.

Future release work must start after HIL-3 final-video approval or an exact HIL-3 upload/prep instruction. The release-decision gate must check:

- Actual final-video-approved local assets and sidecars.
- AI-assisted disclosure wording.
- Current YouTube policy/account constraints.
- Current provider/source provenance.
- Rollback/manual-only responsibilities.

For future videos, reuse the approved API helper shape and external env-file pattern by citation, but open a fresh episode-specific execution gate before any platform/API mutation. Final video approval alone is not upload/API/browser/account approval.

## Forbidden Positive Claims

Do not claim the channel, track, video, render, or candidate is `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `platform-safe`, `exclusive`, `upload-ready`, or `publish-ready`. Use those phrases only as blockers or warnings.

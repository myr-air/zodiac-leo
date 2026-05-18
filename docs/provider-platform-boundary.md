# Provider And Platform Boundary

Status: active  
Updated: 2026-05-18

## Suno Boundary

No active provider generation is approved. OpenCode must not operate Suno, automate a browser, call provider APIs, scrape, download, upload, mutate accounts, or create candidate provenance before files exist.

Future provider use requires a fresh source review if any of these change:

- Provider, model, plan, account boundary, generation mode, or UI feature.
- Lyrics, style prompts, exclude prompts, controls, helper-packaged fields, voice settings, uploaded source, personalization, cover/remix mode, or disclosure wording.

## YouTube Boundary

No upload, publish, schedule, Studio, OAuth, YouTube API, Analytics API, browser automation, playlist action, metadata edit, comment action, private/unlist/delete, channel rename, or Content ID action is approved in this standalone scope.

Future release work must start with a new release-decision gate that checks:

- Actual final local assets and sidecars.
- AI-assisted disclosure wording.
- Current YouTube policy/account constraints.
- Current provider/source provenance.
- Rollback/manual-only responsibilities.

## Forbidden Positive Claims

Do not claim the channel, track, video, render, or candidate is `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `platform-safe`, `exclusive`, `upload-ready`, or `publish-ready`. Use those phrases only as blockers or warnings.

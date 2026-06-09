# Provider And Platform Boundary

Status: active
Updated: 2026-06-09

## Suno Boundary

No active provider generation is approved. OpenCode must not operate Suno, automate a browser, call provider APIs, scrape, download, upload, mutate accounts, or create candidate provenance before files exist.

Future provider use requires a fresh source review if any of these change:

- Provider, model, plan, account boundary, generation mode, or UI feature.
- Lyrics, style prompts, exclude prompts, controls, helper-packaged fields, voice settings, uploaded source, personalization, cover/remix mode, or disclosure wording.

## YouTube Boundary

Current exception status: EP1-EP4 have episode-specific YouTube/API/manual release evidence recorded in their own `channel/episodes/<episode-id>/` packets. Those records are historical facts inside the core system, not blanket approval for future platform actions. Credentials and tokens must stay outside the repo. No further YouTube platform/API mutation is approved without a fresh explicit gate for the exact action.

No public publish, schedule, Studio/browser automation, Analytics API, playlist action, metadata edit after upload, comment action, unlist/delete, channel rename, caption upload, extra thumbnail variant, account edit, Content ID action, or positive platform/rights claim is approved in this standalone scope.

Future release work must start after HIL-4 release-route approval. The release-decision gate must check:

- Actual final-video-approved local assets and sidecars.
- AI-assisted disclosure wording.
- Current YouTube policy/account constraints.
- Current provider/source provenance.
- Rollback/manual-only responsibilities.

For future videos, reuse the approved API helper shape and external env-file pattern by citation, but open a fresh episode-specific execution gate before any platform/API mutation. Final video approval alone is not upload/API/browser/account approval.

If a later gate selects a post-upload engagement comment, keep it narrow: the official YouTube Data API v3 `commentThreads.insert` method can create one top-level comment after an existing video ID and authenticated-channel verification. The comment helper must first scan existing top-level comments from the authenticated channel and block exact duplicate text unless the user intentionally passes `--force-repost`. Comment pinning is not treated as API-supported in this repo; pin manually in YouTube/Studio only if the user opens that account action. Do not combine comment posting with upload, thumbnail, metadata update, public publish, analytics, or Content ID actions by implication.

## Forbidden Positive Claims

Do not claim the channel, track, video, render, or candidate is `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `platform-safe`, `exclusive`, `upload-ready`, or `publish-ready`. Use those phrases only as blockers or warnings.

# Operating Boundary

Status: active  
Updated: 2026-05-27

Mellow Longplay is source-first. Local docs, manifests, prompts, reviews, tracking rows, subtitles, and scripts are allowed. External accounts and generated media are blocked unless a future explicit gate approves the exact step. The normal production loop uses three planned HIL checkpoints, not per-track/per-gate approval prompts.

Allowed now:

- Write and review source packets.
- Maintain episode manifests and tracking CSVs.
- Maintain local subtitle sidecars and helper scripts.
- Prepare source-only song, visual, metadata, and readiness reviews.
- Record and verify the completed S01E01 private YouTube Data API upload plus selected-thumbnail follow-up evidence as recorded in `channel/episodes/s01e01-campus-cafe-longplay/reviews/youtube-api-execution-gate.md`; credentials/tokens stay outside repo and no further platform/API mutation is allowed without a new explicit gate.

Blocked now:

- Suno, browser, provider, repeat video upload, repeat thumbnail upload, public publish, schedule, delete, privacy mutation after upload, metadata mutation after upload, captions, playlists, comments, analytics, Content ID, or account actions outside a new explicit gate.
- New audio/image/video/render/export generation without a separate approved local gate.
- Credentials, cookies, account IDs, private analytics, raw account exports, or browser profiles.
- Positive rights/platform claims.

Three planned HIL checkpoints:

1. HIL-1: user says to make a new episode; system creates source packet, song prompts, visual prompts, metadata draft, and handoff notes.
2. HIL-2: user says generated/supplied media exists and to continue; system can intake files, assemble, subtitle, render locally, and self-review intensely.
3. HIL-3: user approves the exact final-video candidate for upload prep/execution or sends point revisions.

Internal gates still exist for evidence and tracking, but they should not create extra planned HIL prompts unless a blocker appears. Only HIL-3 can discuss upload/public-publish planning, and it still requires separate exact-action approval.

Fastlane rule: for future videos, approved channel defaults may be reused by citation. Re-open only the changed episode delta, local media/render gate, final-video decision, or external platform/API gate.

# Operating Boundary

Status: active  
Updated: 2026-05-25

Mellow Longplay is source-first. Local docs, manifests, prompts, reviews, tracking rows, subtitles, and scripts are allowed. External accounts and generated media are blocked unless a future explicit gate approves the exact step.

Allowed now:

- Write and review source packets.
- Maintain episode manifests and tracking CSVs.
- Maintain local subtitle sidecars and helper scripts.
- Prepare source-only song, visual, metadata, and readiness reviews.
- Execute the active S01E01 private YouTube Data API upload plus selected-thumbnail follow-up gate only as recorded in `channel/episodes/s01e01-campus-cafe-longplay/reviews/youtube-api-execution-gate.md`, with credentials/tokens outside repo and channel-id verification before `videos.insert` or `thumbnails.set`.

Blocked now:

- Suno, browser, provider, public publish, schedule, delete, privacy mutation after upload, metadata mutation after upload, captions, playlists, comments, analytics, Content ID, or account actions outside the active S01E01 private video plus selected-thumbnail API gate.
- New audio/image/video/render/export generation without a separate approved local gate.
- Credentials, cookies, account IDs, private analytics, raw account exports, or browser profiles.
- Positive rights/platform claims.

Gate model:

1. Source Packet.
2. Candidate Intake.
3. Assembly Package.
4. Internal Readiness.
5. Release Decision.

Only Gate 5 can discuss upload/public-publish planning, and it still requires separate explicit approval.

Fastlane rule: for future videos, approved channel defaults may be reused by citation. Re-open only the changed episode delta, local media/render gate, or external platform/API gate.

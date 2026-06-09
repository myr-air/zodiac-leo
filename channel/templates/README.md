# Mellow Longplay Templates

Status: source-only reusable worksheets / four-HIL fastlane
Updated: 2026-05-27

This folder holds copyable worksheet templates for future `Mellow Longplay` episode planning and review. They are internal source documents only: they do not approve media generation, render/export, upload, publishing, API/browser/provider/account automation, credential handling, or rights/platform-safety claims.

Default rule for the next videos: use the compact four-HIL fastlane worksheet first, cite approved channel defaults and `docs/episode-lessons.md` once, and re-review only changed episode deltas or newly opened local/external gates. Planned HIL happens at new episode command, generated-media-ready continue command, final-video approval/revision, and release-route command.

Recommended copy destinations:

```text
channel/episodes/<episode-id>/reviews/episode-production-worksheet.md
channel/episodes/<episode-id>/reviews/release-decision-plan.md
channel/episodes/<episode-id>/reviews/episode-analytics-loop.md
mellow-longplay/reviews/<cycle-id>-season-scoring-sheet.md
```

Use episode templates after the episode has a real source packet or, for analytics, after a future release is separately approved and non-private manual metrics are available. Use the season scoring template only after enough real episode worksheets exist to score a cycle. Keep placeholders such as `<episode-id>` or `<cycle-id>` until real reviewed facts exist; do not invent candidate IDs, provenance, analytics, or generated-output claims.

## Templates

- `episode-production-worksheet-template.md` — compact four-HIL next-video fastlane worksheet for approved-default reuse, episode-delta review, metadata chapters/comment drafting, source package readiness, local render QA, and final-video/route decisions.
- `episode-zero-to-youtube-runbook-template.md` — four-HIL gated runbook from packet bootstrap to guarded YouTube handoff planning, including chapter/comment handoff notes, the S01E02 bootstrap command, and publish blockers.
- `episode-analytics-loop-template.md` — manual, non-private 24h/7d/30d/season-end notes template for future separately approved releases.
- `season-scoring-sheet-template.md` — 12-week / 12-episode / 3-season cycle source scoring sheet for roadmap rollup, milestone checks, throughput/revision control, content pattern analysis, and final source-system verdict.

## Still Blocked

- Provider/account access, Suno/YouTube/API/browser automation, scraping, OAuth, cookies, credentials, or private analytics unless a narrow episode-specific gate explicitly opens the exact action.
- Audio/image/video generation, downloads, renders, exports, uploads, publishing, schedules, Content ID registration, or external distribution unless a narrow episode-specific gate explicitly opens the exact action.
- Claims that an episode is `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `platform-safe`, `upload-ready`, or `publish-ready`.

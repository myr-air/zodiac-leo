# Mellow Longplay

Standalone source system for one YouTube AI-assisted music channel: `Mellow Longplay`.

This project keeps the channel small on purpose. It stores source packets, review notes, provenance, subtitles, and local helper scripts for Mellow Longplay only. Provider, browser, upload, publish, account, and rights/monetization work stays blocked unless a narrow explicit gate records the exact allowed action.

## Structure

- `channel/channel.md` defines the channel promise and safety boundary.
- `channel/roadmap.md` defines the 12-week source-production roadmap.
- `channel/episodes/` holds episode packets.
- `channel/templates/` contains reusable source-only worksheets, including the compact next-video fastlane.
- `candidates/` is ignored local evidence storage for future user-supplied audio and visuals.
- `scripts/verify-standalone.sh` validates the reduced standalone structure.

## Current Episode

Active source packet: `channel/episodes/s01e01-campus-cafe-longplay/`.

Current gate: S01E01 has source, subtitle, render-05 local QA, release-planning, and a narrow private YouTube API upload plus selected-thumbnail follow-up gate recorded in the episode packet. Public publish/release, account edits, analytics, Content ID, extra renders, and rights/platform-safety claims remain blocked.

## Next Video Fastlane

For future videos, start from `channel/templates/episode-production-worksheet-template.md`: reuse approved channel defaults by citation, review only episode deltas, and keep local render/export or external platform/API actions behind explicit gates.

## Verify

Run from this folder:

```bash
bash scripts/verify-standalone.sh
python3 -m pytest tests
```

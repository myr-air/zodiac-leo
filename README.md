# Mellow Longplay

Standalone source system for one YouTube AI-assisted music channel: `Mellow Longplay`.

This project keeps the channel small on purpose. It stores source packets, review notes, provenance, subtitles, and local helper scripts for Mellow Longplay only. It does not operate Suno, YouTube, browser sessions, APIs, OAuth, uploads, publishing, account state, or rights/monetization claims.

## Structure

- `mellow-longplay/channel.md` defines the channel promise and safety boundary.
- `mellow-longplay/roadmap.md` defines the 12-week source-production roadmap.
- `channel/episodes/` is reserved for future episode packets.
- `mellow-longplay/templates/` contains reusable source-only worksheets.
- `candidates/` is ignored local evidence storage for future user-supplied audio and visuals.
- `scripts/verify-standalone.sh` validates the reduced standalone structure.

## Current Episode

No active episode packet exists right now. Start the next workflow by creating a fresh episode packet, tracking files, and review gates before any media generation, render/export, or release planning.

## Verify

Run from this folder:

```bash
bash scripts/verify-standalone.sh
python3 -m pytest tests
```

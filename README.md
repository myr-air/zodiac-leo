# Mellow Longplay

Standalone source system for one YouTube AI-assisted music channel: `Mellow Longplay`.

This project keeps the channel small on purpose. It stores source packets, review notes, provenance, subtitles, and local helper scripts for Mellow Longplay only. It does not operate Suno, YouTube, browser sessions, APIs, OAuth, uploads, publishing, account state, or rights/monetization claims.

## Structure

- `channel/channel.md` defines the channel promise and safety boundary.
- `channel/roadmap.md` defines the 12-week source-production roadmap.
- `channel/episodes/` is reserved for future episode packets.
- `channel/templates/` contains reusable source-only worksheets.
- `candidates/` is ignored local evidence storage for future user-supplied audio and visuals.
- `scripts/verify-standalone.sh` validates the reduced standalone structure.

## Current Episode

Active source packet: `channel/episodes/s01e01-campus-cafe-longplay/`.

Current gate: Gate 1 source packet only. Lyrics, real media candidates, subtitle timing, render/export, upload, publishing, and release planning remain blocked until later explicit gates.

## Verify

Run from this folder:

```bash
bash scripts/verify-standalone.sh
python3 -m pytest tests
```

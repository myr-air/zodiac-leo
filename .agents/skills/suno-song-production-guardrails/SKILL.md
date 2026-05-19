---
name: suno-song-production-guardrails
description: Use for Mellow Longplay source-only Suno 5.5 song materials: lyrics, Styles with BPM, Exclude Styles, Vocal Gender, Lyrics Mode, Weirdness, Style Influence, song titles, arrangement briefs, prompt packs, manual handoff notes, and provenance templates. Blocks provider/account automation, generated media, imitation, and rights/monetization claims.
---

# Suno Song Production Guardrails

Use for source-only song work in `/Users/xiivth/workspaces/mellow-longplay`.

Read first: `AGENTS.md`, `KNOWLEDGE.md`, `docs/provider-platform-boundary.md`, `channel/channel.md`, relevant episode `manifest.json`, and `source/songs.md`.

Allowed: original titles, briefs, sectioned lyrics, arrangement notes, Suno 5.5 `Styles`, `Exclude Styles`, `Vocal Gender`, `Lyrics Mode`, `Weirdness`, `Style Influence`, reject criteria, provenance instructions, and re-review triggers.

Blocked: provider access, Suno operation, browser automation, APIs, downloads, uploads, generated media, account mutation, fake provenance, named-artist/song/voice/channel/brand imitation, and positive rights/platform claims.

## Episode Style & Theme Spine Requirement

Before new or revised per-song Suno fields are approved, the episode must have an Episode Style & Theme Spine: listener job, theme thesis, base `Styles` lane, BPM range, vocal lane, core instrumentation, base `Exclude Styles`, control baseline, allowed variation slots, and safety blockers.

Each track must carry a source-only Track Delta that explains how its `Styles`, BPM, arrangement color, object/theme function, and motif budget differ from the episode spine and nearby tracks. Keep the final copy-ready `Styles` compact: episode base style plus the approved Track Delta plus explicit approximate BPM. Return `REVISE` if fields have no episode spine, no Track Delta, a genre/BPM drift that breaks the longplay, or a reserved variation slot reused without review.

## Suno 5.5 Required Per-Song Parameters

Preferred handoff format: one copy-ready file per song under `source/suno-tracks/`, with `source/suno-manual-fields.md` as episode index/defaults.

When lyrics or per-track parameters change, update/sync the corresponding `source/suno-tracks/*.md` files and run/refresh the related review entry before manual handoff.

Every Suno 5.5 manual handoff pack must define all fields below for every song. Do not leave placeholders.

| Parameter | Source-only rule |
|---|---|
| `Song Title` | Exact current source title. |
| `Lyrics Mode` | Explicit value, normally `manual`. |
| `Lyrics` | Exact current source lyric block or an unambiguous source pointer to it. Do not rewrite at handoff time. |
| `Styles` | Episode base style plus track-specific style additions and an explicit approximate BPM, e.g. `mid-slow 84 BPM`. Genre/mood/instrument words only; no named-artist imitation. |
| `Exclude Styles` | Episode base exclusions plus track-specific exclusions and safety blockers. |
| `Vocal Gender` | Explicit value, normally `female`; still do not request a real person, named artist, or childlike voice. |
| `Weirdness` | Explicit integer percentage from `0%` to `100%`; keep low/moderate for cohesive longplay unless reviewed. |
| `Style Influence` | Explicit integer percentage from `0%` to `100%`; keep consistent across the episode unless reviewed. |

For cohesive mellow longplays, default starting range is `8-20%` Weirdness and `78-86%` Style Influence. Out-of-range values require a source review explaining why they will not break the episode arc.

## Prompt Hygiene Rules (Source-Only)

- Front-load `genre + mood + vocal + tempo + BPM` in `Styles` so core intent survives truncation.
- Spine/delta gate: verify the `Styles` field reads as episode base plus controlled Track Delta, not a one-off prompt that redefines the episode. Keep recurring base descriptors stable while changing only the reviewed track-specific color, BPM, or section energy.
- BPM gate: every final `Styles` field must include an explicit approximate BPM. Use a cohesive longplay range unless reviewed otherwise: slower bonus/closers roughly `72-82 BPM`, mellow mid-slow songs roughly `80-90 BPM`, and brighter groove tracks roughly `88-98 BPM`. Return `REVISE` for missing BPM, implausible BPM, or BPM values that fight the episode arc.
- Use concise descriptive specs; avoid long keyword salad or command-like phrasing.
- During planning, prefer this scaffold: `STORY BRIEF / REFERENCE TRIANGLE / IDENTITY / PALETTE / VOCALS / SECTION GOALS / CONSTRAINTS`.
- Reference songs/artists may be documented only in source-only story/reference briefs as inspiration anchors. Never put named songs, artists, real voices, sound-alike requests, copied lyric phrases, chord-copy requests, or melody-copy requests in Suno `Styles`, `Exclude Styles`, lyrics, metadata, or provider prompts.
- Scan `Song Title`, `Lyrics`, `Styles`, and `Exclude Styles` for accidental named-reference collisions, not only explicit `style of` wording. If a phrase in a title or hook reads like a known artist/song instead of the intended story object, retitle/rephrase before PASS.
- Keep titles story-led. Do not force arrangement instruments into song titles; use `Styles` and arrangement notes for piano-forward, sax-accent, guitar-led, or drum-feel cues unless an instrument is a real story object.
- Do not require the song title to appear in lyrics or as the first hook line. For source handoff, the `Song Title` field can be a mood/scene/object label while the lyric hook uses a different phrase, as long as the source review records the title/lyric relationship.
- Treat unresolved lexical sameness as a handoff blocker: repeated high-salience words from recent tracks, generic AI comfort words, or reused hook/payoff vocabulary must be cleared by lyric review before Suno field PASS.
- Keep final Suno `Styles` field compact even if planning notes are longer.
- Keep `Exclude Styles` short and targeted to safety/content blockers and key anti-patterns.
- Keep lyrics section tags intentional and varied across adjacent songs; do not repeat the same full macro-form for every track. If using meta or section tags, assign a structure fingerprint and vary hook placement, break function, bridge role, chorus role, title-repeat count, and rhetorical pattern from the previous approved tracks.
- Treat unresolved lyric-pattern sameness as a handoff blocker: repeated title twice in the same chorus/refrain block, repeated `No ..., no ...` phrasing, repeated `one small/soft note/sign/line` payoffs, or identical final-hook stacking must be reviewed by lyric quality before any source-only Suno field PASS.
- Use instrumental/pause tags for breathing room, but do not put free-standing music-instruction lines under tags where they may be sung.
- During retunes, change one variable at a time when possible and record the intent.
- For cohesive longplays, keep Weirdness low/moderate and Style Influence high/consistent unless a reviewed exception is documented.

Require re-review if provider, model, lyrics, title, style prompt, BPM, exclude prompt, Vocal Gender, Lyrics Mode, Weirdness, Style Influence, voice/upload feature, personalization, disclosure, or upload intent changes.

# Mellow Longplay Next-Video Fastlane Worksheet Template

Status: template / compact source-to-video workflow  
Episode: `<episode-id>`  
Prepared by: `<name-or-agent>`  
Prepared date: `<YYYY-MM-DD>`  
Source packet version: `<version>`

## 0. Boundary

This worksheet is an internal source-to-video checklist. It does not approve provider use, media generation, render/export, upload, publishing, Suno/YouTube/API/browser automation, account mutation, credential storage, Content ID registration, public release, or positive rights/platform-safety claims.

Fastlane rule: reuse approved channel-level defaults by citation; approve only episode deltas and real external/local actions.

Still-forbidden positive claims except as blocked/caution language: `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `platform-safe`, `upload-ready`, `publish-ready`.

## 1. Reuse Defaults / Delta Triggers

| Area | Reuse by default | Re-review only if this changes |
|---|---|---|
| Channel promise | Cozy chill vocal longplay, listener-job title/metadata, AI-assisted disclosure style | channel lane, target listener, disclosure wording, or public claim changes |
| Episode format | 12 main songs + 1 bonus, English-first, cohesive soft R&B / city-pop / mellow vocal palette | track count, language, duration target, genre weight, age/romance safety lane changes |
| Song-source guardrails | Episode Style & Theme Spine, Track Delta, Story + Reference Brief, strict pattern gate, lexical ledger, BPM in `Styles`; EP03+ no planned sax, piano allowed, exactly one non-sax special instrument in exactly one song, several feeling/mood-led tracks | lyrics, title, style/exclude/control fields, provider/model assumptions, reference strategy, special instrument, or mood/story mix changes |
| Audio intake | Local user-supplied files only; selected/pool mapping from `audio-candidate-intake-workflow-template.md` | files, candidate IDs, selection, provenance, variant count, or generation/provider facts change |
| Sequence policy | Approved simple assembly pattern: fixed order, `1.00s` gaps, no crossfade, no bumper unless explicitly opened | order, gap, bumper, crossfade, duration, chapter policy, or story arc changes |
| Visual shell | Reuse channel signature motifs and the latest approved calm subtitle/equalizer/overlay behavior as source-only design guidance | background, subject/crop, overlay layout, subtitle region, motion amplitude, thumbnail strategy, or visual prompt changes |
| Subtitles | Track-local timing -> episode sidecars -> mechanical parser checks -> human watch/spot pass | lyrics/sung words, cue policy, timeline, sidecar text, or render target changes |
| Metadata/API workflow | Reuse source metadata structure, reusable external env-file API helper shape, and channel-id verification rule | public release, privacy, captions, playlist, account, thumbnail variant, API method, or channel target changes |

If a row is unchanged, cite the previous approved source/review path once instead of repeating full analysis.

## 2. Six-Step Video Build Path

| Step | Exit evidence | Status / notes |
|---:|---|---|
| 1. Source packet lock | `manifest.json`, `source/songs.md`, `source/suno-manual-fields.md`, `source/suno-tracks/*.md`, relevant reviews/tracking | `<pending/pass/revise/block>` |
| 2. Candidate intake | real local audio/visual files exist before IDs/provenance; selected/pool map recorded | `<pending/pass/revise/block/n/a>` |
| 3. Sequence + metadata | chapter timeline, disclosure, title/description/tags policy, blocked-claim scan | `<pending/pass/revise/block>` |
| 4. Subtitles + sidecars | final `.srt`/`.vtt`, no overlaps/gap cues, line-length/timing checks, human watch/spot evidence | `<pending/pass/revise/block>` |
| 5. Local render QA | explicit render/export gate, video path, mechanical QA, sidecar byte-match/copy result, visual/listening spot pass | `<blocked unless gate opened>` |
| 6. Release/API planning | explicit release decision, current policy/account check, private-upload/package gate if approved | `<blocked unless gate opened>` |

Do not open the next step by implication. Each local media render/export or external platform/API action still needs its own explicit gate.

## 3. Compact Scorecard

| Check | Pass signal | Result |
|---|---|---|
| Source and provenance | source/review/tracking files cite only real facts; no invented candidates or dates | `<pass/revise/block>` |
| Lyric/source quality | concrete scene, PG/safety fit, no stale hook/template/lexical pattern | `<pass/revise/block>` |
| Audio fit | no major artifact, harshness, silence, lyric-anchor, or adjacent-similarity blocker | `<pass/revise/block/n/a>` |
| Visual fit | safe zones, originality, readable overlays/subtitles, calm motion, no brand/real-person implication | `<pass/revise/block>` |
| Subtitle fit | parser/mechanical checks and human watch/spot pass match current audio/source lyrics | `<pass/revise/block>` |
| Metadata/disclosure | listener-job led, disclosure clear, no unsupported rights/platform/release claim | `<pass/revise/block>` |
| Downstream gate | render/export and platform/API scope are explicit and narrow, or remain blocked | `<pass/revise/block>` |

Internal score, if needed: `<0-100>`. `>=90` means internal candidate only; it is not release, upload, platform, monetization, or rights approval.

## 4. Re-Review Triggers

Re-run only the affected rows/steps when any of these change:

- listener job, episode world, age/romance safety lane, language, track count, duration target;
- lyrics, title, section form, hook, style/exclude/control fields, provider/model/manual handoff assumptions;
- actual audio/visual files, selected/pool mapping, local paths, provenance, candidate IDs;
- sequence order, gap, bumper, crossfade, chapter timestamps, final sidecar text/timing;
- visual background, crop, overlay/subtitle placement, motion, thumbnail asset or variant;
- metadata, disclosure, claim wording, privacy/public release, platform/API method, credentials/account boundary.

No trigger means cite the prior approved default and continue.

## 5. Final Verdict Card

```text
Verdict: pass_internal_candidate | revise_source_only | block
Scope: internal source-to-video readiness only
Reused approvals: <paths / rows cited>
Episode deltas reviewed: <short list>
Evidence: <source/review/tracking/asset paths>
Critical blockers: <none or list>
Next allowed action: <source-only action or explicit gate request>
Still blocked: provider/account automation, media generation without gate, render/export without gate, upload/publish/API without gate, credentials in repo, Content ID, rights/platform-safety claims
```

# Mellow Longplay Next-Video Fastlane Worksheet Template

Status: template / compact source-to-video workflow / four-HIL fastlane
Episode: `<episode-id>`
Prepared by: `<name-or-agent>`
Prepared date: `<YYYY-MM-DD>`
Source packet version: `<version>`

## 0. Boundary

This worksheet is an internal source-to-video checklist. It does not approve provider use, media generation, render/export, upload, publishing, Suno/YouTube/API/browser automation, account mutation, credential storage, Content ID registration, public release, or positive rights/platform-safety claims.

Fastlane rule: reuse approved channel-level defaults by citation; planned HIL happens four times: new episode command, generated-media-ready continue command, final local-risk review, and final release/schedule decision. Re-open only episode deltas and real external/local actions.

Still-forbidden positive claims except as blocked/caution language: `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `platform-safe`, `upload-ready`, `publish-ready`.

## 1. Reuse Defaults / Delta Triggers

| Area | Reuse by default | Re-review only if this changes |
|---|---|---|
| Channel promise | Cozy chill vocal longplay, listener-job title/metadata, AI-assisted disclosure style | channel lane, target listener, disclosure wording, or public claim changes |
| Episode format | 12 main songs + 1 bonus, English-first, cohesive soft R&B / city-pop / mellow vocal palette | track count, language, duration target, genre weight, age/romance safety lane changes |
| Song-source guardrails | Episode Style & Theme Spine, Track Delta, Story + Reference Brief, strict pattern gate, lexical ledger, BPM in `Styles`; EP03+ no planned sax, piano allowed, exactly one non-sax special instrument in exactly one song, several feeling/mood-led tracks | lyrics, title, style/exclude/control fields, provider/model assumptions, reference strategy, special instrument, or mood/story mix changes |
| Audio intake | Local user-supplied files only; selected/pool mapping from `audio-candidate-intake-workflow-template.md` | files, candidate IDs, selection, provenance, variant count, or generation/provider facts change |
| Sequence policy | Approved simple assembly pattern: fixed order, `1.00s` gaps, no crossfade, no bumper unless explicitly opened | order, gap, bumper, crossfade, duration, chapter policy, or story arc changes |
| Visual shell | Reuse channel signature motifs plus the EP1 render-05 video overlay/motion standard by default: refined headphone icon, tiny music notes, warm particles/light, custom ribbon/dot equalizer, near-still motion, per-song video chunks with global-time effects, adapted per image | background, subject/crop, overlay layout, subtitle region, motion amplitude, thumbnail strategy, or visual prompt changes |
| Subtitles | Track-local timing -> episode sidecars -> mechanical parser checks -> system review; HIL-3 approves the whole final-video candidate | lyrics/sung words, cue policy, timeline, sidecar text, or render target changes |
| Metadata/API workflow | Reuse source metadata structure, upload-description chapter timestamps whenever a timeline exists, a short English post-upload comment draft (automatically posted via `--comment-file` or `MELLOW_YOUTUBE_COMMENT_FILE`), reusable external env-file API helper shape, and channel-id verification rule | public release, privacy, captions, playlist, account, thumbnail variant, comment posting/pinning, API method, or channel target changes |

If a row is unchanged, cite the previous approved source/review path once instead of repeating full analysis.

## 6-step build path now split by HIL-4 focus

| Step | Exit evidence | Status / notes |
|---:|---|---|
| 1. Source prompt packet after HIL-1 | `manifest.json`, `source/songs.md`, `source/suno-manual-fields.md`, `source/suno-tracks/*.md`, song prompts, visual prompts, relevant reviews/tracking | `<pending/pass/revise/block>` |
| 2. Candidate intake after HIL-2 | real local audio/visual files exist before IDs/provenance; selected/pool map recorded | `<pending/pass/revise/block/n/a>` |
| 3. Sequence + metadata | chapter timeline, upload-description timestamps, disclosure, title/description/tags policy, English post-upload comment draft, blocked-claim scan | `<pending/pass/revise/block>` |
| 4. Subtitles + sidecars | `.srt`/`.vtt`, no overlaps/gap cues, line-length/timing checks, source/render fit review | `<pending/pass/revise/block>` |
| 5. Local render QA + final-video candidate | explicit local render scope from HIL-2, video path, mechanical QA, sidecar checks, visual/layout/listening review, issue-led rerender if allowed | `<pending/pass/revise/block>` |
| 6. HIL-4 final video decision / release route | exact final-video approval, point revision request, or release/upload package gate | `<blocked until HIL-4>` |

Do not open the next step by implication. The system should not ask for routine
per-track/per-subtitle/per-candidate approval in this fastlane; it should stop
only at HIL-1, HIL-2, HIL-3, HIL-4, or a real blocker. Each external platform/API
action still needs its own explicit gate.

## 3. Compact Scorecard

| Check | Pass signal | Result |
|---|---|---|
| Source and provenance | source/review/tracking files cite only real facts; no invented candidates or dates | `<pass/revise/block>` |
| Lyric/source quality | concrete scene, PG/safety fit, no stale hook/template/lexical pattern | `<pass/revise/block>` |
| Audio fit | no major artifact, harshness, silence, lyric-anchor, or adjacent-similarity blocker | `<pass/revise/block/n/a>` |
| Visual fit | safe zones, originality, readable overlays/subtitles, calm motion, no brand/real-person implication | `<pass/revise/block>` |
| Subtitle fit | parser/mechanical checks and final-video candidate review match current audio/source lyrics | `<pass/revise/block>` |
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
- metadata, disclosure, chapter timestamps, post-upload comment text, claim wording, privacy/public release, platform/API method, credentials/account boundary.

If no trigger appears, continue to the next planned HIL instead of asking for
micro-approval.

No trigger means cite the prior approved default and continue.

## 5. Final Verdict Card

```text
Verdict: source_prompt_handoff | final_video_candidate_pending | final_video_approved_hold_release | point_revision_requested | block
Scope: internal source-to-video readiness only
Reused approvals: <paths / rows cited>
Episode deltas reviewed: <short list>
Evidence: <source/review/tracking/asset paths>
Critical blockers: <none or list>
Next allowed action: <HIL-2 media-ready continue / HIL-3 final-video decision / explicit gate request>
Still blocked: provider/account automation, media generation without gate, render/export without gate, upload/publish/API without gate, credentials in repo, Content ID, rights/platform-safety claims
```

# S01E06-CROSSWALK-EVENING-LONGPLAY Production Worksheet — Crosswalk Evening Longplay

Status: Gate 1 source prompts locked / no media or release gate
Episode: `s01e06-crosswalk-evening-longplay`
Prepared by: Mayr
Prepared date: 2026-06-12
Source packet version: `v1.0-source-locked`

## 0. Boundary

This worksheet is an internal source-to-video checklist. It does not approve provider use, media generation, render/export, upload, publishing, Suno/YouTube/API/browser automation, account mutation, credential storage, Content ID registration, public release, or positive rights/platform-safety claims.

Fastlane rule: reuse approved channel-level defaults by citation; approve only episode deltas and real external/local actions.

## 1. Episode Delta Seed

| Field | Value |
|---|---|
| Working longplay | Crosswalk Evening Longplay |
| Roadmap hook | after-work street motion, evening commute |
| Lyric lane | The evening commute, walking through busy streets, city exploration, excitement of first meetings |
| Default format | 12 main songs + 1 bonus / English-first |
| Current gate | Gate 1 source prompts locked |

## 2. Build Path Status

| Step | Exit evidence | Status / notes |
|---:|---|---|
| 0. Scaffold | manifest, current state, source/review/tracking placeholders | pass_source_only |
| 1. Source packet lock | `source/songs.md`, `source/suno-manual-fields.md`, `source/suno-tracks/*.md`, reviews/tracking | pass_source_only |
| 2. Candidate intake | real local audio/visual files exist before IDs/provenance | blocked_until_gate |
| 3. Sequence + metadata | chapter timeline, upload-description timestamps, disclosure, title/description/tags policy, English post-upload comment draft | pending |
| 4. Subtitles + sidecars | final `.srt`/`.vtt`, parser checks, human watch/spot evidence | pending |
| 5. Local render QA | explicit render/export gate, video path, mechanical QA, human spot pass | blocked_until_gate |
| 6. YouTube handoff planning | release decision, current public policy/account check, API/manual package | blocked_until_gate |
| 7. Public publish decision | user-owned final action, rollback owner, no-store hygiene | blocked_until_explicit_final_gate |

Do not open the next step by implication. Each local media render/export or external platform/API action still needs its own explicit gate.

## 3. Current Verdict

```text
Verdict: source_prompts_locked_no_media
Scope: Episode 6 source materials and metadata completed and compiled
Evidence: manifest.json, source/songs.md, source/suno-manual-fields.md, source/suno-tracks/*.md, source/visual.md, source/metadata.md, source/prompt-pack.md
Critical blockers: no local candidate media; render/export and YouTube actions blocked
Next allowed action: Wait for HIL-2 (user supplies real audio/image files or opens media gate) to continue to candidate intake
Still blocked: provider/account automation, media generation without gate, render/export without gate, upload/publish/API without gate, credentials in repo, Content ID, rights/platform-safety claims
```

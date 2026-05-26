# Mellow Longplay Episode Zero-To-YouTube Runbook Template

Status: template / source-first gated workflow  
Episode: `<episode-id>`  
Prepared by: `<name-or-agent>`  
Prepared date: `<YYYY-MM-DD>`

## 0. Boundary

This runbook coordinates an episode from an empty source packet to a guarded
YouTube handoff. It does not approve provider use, generated media,
render/export, upload, public publishing, scheduling, API/browser/account
automation, credential storage, Content ID action, private analytics capture, or
positive rights/platform-safety claims.

For S01E02, start from the roadmap seed only:

```text
Episode ID: s01e02-classroom-window-longplay
Working longplay: Classroom Window Longplay
Hook: college classroom light, afternoon window
Lyric lane: curiosity, almost-said feelings, study-day warmth
```

## 1. Bootstrap Command

Dry-run first:

```bash
bash scripts/dev-python.sh scripts/bootstrap_episode_packet.py --s01e02 --dry-run
```

Create the source-only packet after checking the dry-run list:

```bash
bash scripts/dev-python.sh scripts/bootstrap_episode_packet.py --s01e02
bash scripts/verify-standalone.sh
```

The bootstrap creates source/review/tracking placeholders only. It must not
create `candidates/<episode-id>/`, candidate IDs, provenance facts, generated
media, render outputs, YouTube video IDs, or release facts.

## 2. Gate Flow

| Gate | Goal | Exit evidence | Still blocked |
|---:|---|---|---|
| 0 | Scaffold source packet | manifest, current-state, source placeholders, tracking CSVs | all media/external actions |
| 1 | Lock source packet | episode spine, track deltas, lyrics, Suno fields, prompt pack, reviews | provider use, candidates, render, YouTube |
| 2 | Candidate intake | real local audio/visual files exist first; selected/pool map, provenance rows | render/export, release |
| 3 | Assembly package | sequence, metadata/disclosure, chapter plan, subtitle plan | render/export unless gate opens |
| 4 | Local render/export QA | explicit local render gate, mechanical QA, sidecar match, human watch/listen spot evidence | platform/API/public release |
| 5 | YouTube handoff planning | final asset selection, current policy/account checks, provenance/risk acceptance, rollback owner | public publish unless final gate opens |
| 6 | Private upload/thumbnail, if selected | episode-specific API/manual gate; channel verification; external env; private-only by default | public visibility mutation, captions, analytics, Content ID |
| 7 | Public publish decision | explicit user final approval and user-owned action record | positive rights/platform guarantees |

Do not advance gates by implication. Each local media/render or external
platform/API action needs a separate narrow gate with current evidence.

## 3. Gate 1 Fastlane Checklist

- Reuse `channel/channel.md` and `channel/roadmap.md` by citation.
- Define the Episode Style & Theme Spine before track drafting.
- For EP03 onward, apply the channel/roadmap creative delta: no planned sax
  special color, piano still allowed, exactly one non-sax special instrument in
  exactly one song, and several feeling/mood-led tracks in the 13-track slate.
- For every track, record Story + Reference Brief, Track Delta, structure
  fingerprint, micro-pattern matrix, lexical count ledger, and Suno 5.5 fields.
- Keep references out of final lyrics, titles, Suno fields, metadata, and visual
  prompts unless they are generic abstract traits.
- Block named-artist/song/voice/channel/brand imitation and unsupported rights or
  platform claims.

## 4. YouTube Handoff Checklist

Open only after a final local QA asset exists.

| Check | Evidence | Owner |
|---|---|---|
| Final asset selection | exact MP4/render path, sidecar paths, thumbnail path | user + source review |
| Metadata/disclosure | title, description, chapters, tags, AI-assisted disclosure | source review |
| Current policy check | official current YouTube/public policy sources observed at review time | source review + user |
| Account-specific check | upload limits, channel warnings/strikes, disclosure UI, feature availability | user only; do not store private account state |
| Provenance/risk acceptance | non-secret provenance and known limitations recorded | user |
| Route choice | manual Studio handoff or guarded private API path | user |
| Rollback owner | delete/unlist/privacy/edit responsibilities | user |

Allowed source-only output before execution: a manual copy package or a private
API dry-run package. Actual API/browser/account mutation remains blocked until an
episode-specific execution gate is opened.

## 5. Final Handoff Card

```text
Verdict: source_only_continue | internal_candidate | hold_release | private_upload_gate_requested | public_publish_gate_requested | block
Scope: <source-only / local QA / YouTube handoff planning>
Evidence: <paths>
Allowed next action: <one narrow action>
Still blocked: provider/account automation, media generation without gate, render/export without gate, upload/publish/API without gate, credentials in repo, Content ID, rights/platform-safety claims
```

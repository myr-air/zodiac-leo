# Mellow Longplay Signature Visual System

Status: active source-only visual identity  
Updated: 2026-05-18  
Reference basis: user-provided `Image 1` and `Image 2` in chat on 2026-05-18; files are stored as local source reference assets in `mellow-longplay/signature-references/`.

## Decision

Future Mellow Longplay key visuals should keep two signature references visible unless a later explicit visual gate overrides them:

1. `Gold crescent record charm`.
2. `Recurring campus listener character`.

These are design-signature references, not approval to use the supplied images as provider reference-image inputs, face-copy inputs, generated media, upload assets, or rights/platform-safety evidence.

## Stored Reference Assets

| Asset | Path | Dimensions | SHA256 |
|---|---|---:|---|
| Gold crescent record charm | `mellow-longplay/signature-references/gold-crescent-record-charm.png` | `1254x1254` | `685a152520360306966ce72c5bde6f5f3da79bd641d0eaed920c075bdc5be8c9` |
| Recurring campus listener character sheet | `mellow-longplay/signature-references/recurring-campus-listener-character-sheet.png` | `1448x1086` | `9ce13c40e3fece8ea4f2735f34ba5c5e96933c735c9e3affb29f5edcbb730175` |

## Signature 1: Gold Crescent Record Charm

Visual description:

- Small glossy gold/orange translucent crescent charm shaped like a crescent moon and vinyl record hybrid.
- Concentric record grooves are visible across the crescent surface.
- A small triangular play icon sits near the center.
- A gold loop/ring at the top makes it read as a bag charm, key charm, necklace pendant, or hanging totem.
- `Mellow Longplay` lettering may be embossed when the image scale supports it, but the silhouette, crescent bite, record grooves, and play-triangle mark are more important than readable text.

Usage rules:

- Include it as a visible small signature object in every future key visual.
- Preferred placements: clipped to the recurring character's gray backpack, placed beside a coffee cup/notebook, hanging from a zipper, used as a small table charm, or integrated as a subtle corner totem.
- Keep it tactile, warm, and premium; avoid making it a loud logo badge that fights the calm longplay mood.
- If the image is text-free, keep the charm text unreadable or omitted; preserve the shape instead of forcing tiny readable typography.

## Signature 2: Recurring Campus Listener Character

Visual description:

- Tasteful young-adult/campus-pop listener character, adult-coded and non-eroticized.
- Long dark hair, gentle expression, soft thoughtful posture.
- Cream knit cardigan, bow blouse, plaid skirt, socks/loafers, and a soft gray backpack.
- Mood range: gentle smile, focused/writing, cheerful, calm/daydreaming.
- Personality read: calm, thoughtful, warm-hearted, likes music, coffee, notebooks, and quiet places.

Usage rules:

- Treat this as a recurring character design language, not a real person, celebrity, influencer, or exact face-copy target.
- Future prompts may describe the character's wardrobe, posture, accessories, and mood, but must not ask a provider to replicate the exact face from the supplied sheet.
- Keep the character wholesome, age-ambiguous young adult / college-coded, not childlike, not explicitly underage, not eroticized, and not school-uniform/minor-coded.
- Use the character as the emotional anchor in key visuals when people are present. If a future scene is unusually object-led, keep at least the gray backpack plus gold crescent charm visible as her presence cue unless a visual gate explicitly approves otherwise.

## Default Prompt Fragment

Use this fragment in future source-only visual prompts:

```text
Signature identity: include the small glossy gold crescent-vinyl charm with concentric grooves and a play-triangle mark, preferably clipped to a soft gray backpack or placed near the notebook/coffee objects. Include the recurring Mellow Longplay campus listener character as a tasteful adult-coded young woman with long dark hair, cream knit cardigan, bow blouse, plaid skirt, socks/loafers, soft gray backpack, gentle thoughtful expression, and calm coffee/notebook/music energy. Treat her as an original character archetype, not a real person or exact face-copy reference.
```

## Safety Boundary

- Source-only visual identity guidance with local reference assets.
- No image generation, image editing, render/export, provider/API/browser/account automation, upload, or publishing approval.
- No use of the stored reference images as provider reference-image inputs unless a future explicit gate records provenance and approves that exact action.
- No protected likeness, real-person identity, celebrity/influencer resemblance, school-age/minor framing, or sexualized presentation.
- No rights-safe, platform-safe, Content ID-safe, monetization-safe, upload-ready, publish-ready, copyright-free, royalty-free, or exclusive claim.

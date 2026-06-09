# Mellow Longplay Signature Visual System

Status: active source-only visual identity / mandatory channel image and video overlay-motion style lock
Updated: 2026-05-27
Reference basis: user-provided `Image 1` and `Image 2` in chat on 2026-05-18; files are stored as local source reference assets in `channel/signature-references/`. The user-provided EP1-style image in chat on 2026-05-27 is used as a style-lock cue only; no new reference file is stored by this edit.

## Decision

All future Mellow Longplay images created or selected for channel/episode use must keep the canonical EP1-style watercolor-paper house look and two signature references visible unless a later explicit visual gate records a narrow override:

1. `Gold crescent record charm`.
2. `Recurring campus listener character`.

This applies to key visuals, background/still-frame candidates, thumbnails, visual prompt packs, visual proof stills, overlay/layout mockups, and local longplay video overlay/motion shells. These are design-signature references, not approval to use the supplied images as provider reference-image inputs, face-copy inputs, generated media, upload assets, render/export outputs, or rights/platform-safety evidence.

## Mandatory Channel House Style: Lo-fi Watercolor Anime Poster

Canonical style name:

```text
Soft watercolor semi-realistic anime playlist-cover illustration
```

Short label:

```text
Lo-fi watercolor anime poster style
```

Thai label:

```text
ภาพประกอบอนิเมะกึ่งสมจริง โทนสีน้ำละมุน แบบปกเพลย์ลิสต์ lo-fi
```

Channel rule:

- Every future image used for the channel must carry this style unless a later explicit visual gate records an exception and explains why.
- Episode-specific lighting, season, location, time of day, or object story may change, but the style family must not drift into flat anime, glossy concept art, hard cinematic realism, neon cyberpunk, horror, generic 3D, or unrelated illustration styles.
- The recurring listener woman must stay soft semi-realistic / softly lifelike: expressive but natural face, realistic light on skin and hair, tasteful proportions, and no doll-like, chibi, flat anime, plastic 3D, or over-smoothed beauty-filter look.
- The recurring listener woman is an archetype, not a repeated pose. Each new image should vary posture, gesture, camera angle, object interaction, or scene action so the channel does not repeat the same seated-by-window writing pose.

## Canonical Video Overlay / Motion Standard: EP1 Render-05

User-approved carry-forward decision: use the S01E01 render-05 visual language as the default standard for every Mellow Longplay video, then tune it to the current episode image rather than copying values blindly.

Required default elements for local longplay video shells:

- compact top-left information block with the same calm typography grammar and balanced spacing;
- refined symmetric Bézier headphone icon, not the earlier simple/blocky mark;
- three tiny warm low-opacity animated music notes near the headphone icon;
- custom bottom-right V6-style ribbon/dot equalizer with smoothed audio energy, not a plain FFmpeg `showwaves` line unless used only for debug/proofing;
- visible but gentle particle/light atmosphere: dust motes, soft glows, reflections, shadow breathing, and slow light sweep;
- for night/window episodes, prefer slow random-looking particle drift, subtle star/window bokeh, and warm lamp glow with gentle slow flicker/sway;
- near-still parallax / micro-motion, with global-time continuity so effects do not reset at track boundaries;
- full longplay renders should default to one video-only segment per song, including its following gap, with effects keyed to `t + segment_start`, then concat/mux with one continuous WAV master;
- subtitles and equalizer remain secondary to listening comfort and must stay clear of faces, the charm, important objects, and the readable subtitle lane.

Per-image adaptation rule:

- Match palette and physics to the selected image: cafe scenes use warm window/cup/leaf atmosphere; classroom-night scenes use amber desk-lamp dust, restrained indigo window glow, desk reflections, and lower-contrast shadows.
- Keep the standard recognizable, but adjust opacity, amplitude, mask/position, equalizer height, and glow direction so the overlay feels embedded in the image.
- If a render candidate uses a simpler logo/effect/particle/equalizer system, treat it as a visual-fidelity issue and open an issue-led revision gate before final-video approval.

## Channel House Style Lock: EP1 Watercolor-Paper Longplay Look

Visual description:

- Soft semi-real illustrated portrait with gentle realistic facial rendering, not flat anime and not glossy concept art.
- Warm hand-painted watercolor wash and paper texture, especially an airy cream / parchment left-side negative space.
- Delicate pencil-sketch linework on secondary objects such as backpack, chair, notebook, cup, window frame, or foliage.
- Right-side or center-right emotional anchor: the recurring listener woman by a window, desk, cafe table, classroom seat, train window, or other warm everyday place.
- Soft natural window light, honey cream highlights, muted greens, pale blue-gray, soft browns, subtle film grain, botanical foreground blur, dust or bokeh kept gentle.
- Calm editorial cover composition: left third stays breathable for title/subtitle overlays; character and story objects sit mostly in the center-right 60 percent.
- Mood should feel intimate, wholesome, and quiet: study, writing, daydreaming, coffee, notebooks, music, after-class or late-afternoon softness.

Pose and scene variation rule:

- Do not reuse the same character pose/composition as the previous approved image unless a later explicit visual gate records the reason.
- Allowed recurring identity: same soft semi-real woman archetype, long dark hair, cream/soft outfit family, gray backpack, and gold crescent-vinyl totem.
- Required variation: change at least one major element per image — pose, gesture, gaze direction, camera angle, hand activity, object focus, foreground framing, or distance from the window/desk.
- Good variations: writing in a notebook, turning a page, looking out the window, reaching for the backpack charm, holding a coffee or milk tea, adjusting headphones, arranging notes, standing near a classroom window, walking past a train window, leaning over a desk, or sharing a subtle side glance with an adjacent peer cue.
- Avoid: identical head tilt, same hand-on-cheek pose, same seated table layout, same window angle, same cup/notebook placement, or same character crop across consecutive visuals.

Night-mode adaptation:

- Preserve the same EP1 watercolor-paper identity even when the scene is evening or night.
- Keep the left side as pale parchment / cream wash, not black empty space.
- Put deeper blue or indigo mainly outside the window; keep warm desk-lamp or window glow on the character, hands, desk, notebook, and charm.
- Avoid cyberpunk, horror, nightclub neon, hard cinematic contrast, sci-fi classroom tech, or moody thriller lighting.

Prompt style fragment:

```text
Channel house style lock: soft semi-real Mellow Longplay illustrated portrait, softly lifelike recurring listener woman, EP1 watercolor-paper look, airy cream/parchment negative space on the left, delicate pencil-sketch edges on secondary objects, gentle realistic face rendering, warm natural window or desk-lamp glow, muted green and pale blue-gray accents, soft brown wood, subtle film grain, botanical foreground blur, cozy hand-painted texture, calm editorial 16:9 cover composition, varied pose/gesture/composition from previous channel images; not flat anime, not doll-like, not chibi, not glossy digital concept art, not plastic 3D, not neon cinematic.
```

## Stored Reference Assets

| Asset | Path | Dimensions | SHA256 |
|---|---|---:|---|
| Gold crescent record charm | `channel/signature-references/gold-crescent-record-charm.png` | `1254x1254` | `685a152520360306966ce72c5bde6f5f3da79bd641d0eaed920c075bdc5be8c9` |
| Recurring campus listener character sheet | `channel/signature-references/recurring-campus-listener-character-sheet.png` | `1448x1086` | `9ce13c40e3fece8ea4f2735f34ba5c5e96933c735c9e3affb29f5edcbb730175` |

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

## Signature 2: Recurring Campus Listener Woman

Visual description:

- Tasteful recurring listener woman / character archetype, wholesome and non-eroticized; adult/college-coded by default, or same-age teen/high-school coded only when an episode explicitly records that direction.
- Long dark hair, gentle expression, soft thoughtful posture.
- Cream knit cardigan, bow blouse, plaid skirt, socks/loafers, and a soft gray backpack.
- Mood range: gentle smile, focused/writing, cheerful, calm/daydreaming.
- Personality read: calm, thoughtful, warm-hearted, likes music, coffee, notebooks, and quiet places.

Usage rules:

- Treat this as a recurring character design language, not a real person, celebrity, influencer, or exact face-copy target.
- Future prompts may describe the character's wardrobe, posture, accessories, and mood, but must not ask a provider to replicate the exact face from the supplied sheet.
- Lock the readable character archetype more than exact facial identity: long dark hair, soft realistic face, cream cardigan or knit layer, modest blouse or bow blouse, gentle thoughtful posture, writing/daydreaming by a window, soft gray backpack nearby.
- Require soft semi-real / softly lifelike character rendering: natural facial structure, believable hair detail, gentle skin lighting, and expressive eyes without flat-anime simplification or plastic-perfect realism.
- Vary her pose and gesture across images. Keep the woman recognizable by archetype and motif, but avoid repeating the same hand-on-cheek, seated-writing, or identical window-gaze composition.
- Keep the character wholesome, age-appropriate, non-childlike, and non-eroticized. Default to age-ambiguous young adult / college-coded; for an explicitly approved teen/high-school first-love episode, use same-age peer framing only and avoid sexualized uniform styling, adult/minor implication, or real school identity.
- Use the character as the emotional anchor in key visuals when people are present. If a future scene is unusually object-led, keep at least the gray backpack plus gold crescent charm visible as her presence cue unless a visual gate explicitly approves otherwise.

## Default Prompt Fragment

Use this fragment in future source-only visual prompts after the channel house style lock:

```text
Signature identity: include the small glossy gold crescent-vinyl charm / totem with concentric grooves and a play-triangle mark, preferably clipped to a soft gray backpack or placed near the notebook/coffee objects. Include the recurring Mellow Longplay listener woman as a tasteful wholesome original character archetype with long dark hair, soft realistic / softly lifelike gentle face, cream knit cardigan or modest school cardigan, bow blouse or modest blouse, plaid skirt when appropriate, socks/loafers, soft gray backpack, and calm coffee/notebook/music energy. Vary her pose, gesture, gaze direction, and object interaction from prior channel images; do not repeat the same hand-on-cheek seated-window writing pose. Default to adult/college-coded unless the episode explicitly approves same-age teen/high-school first-love framing. Do not copy an exact face, real person, celebrity, influencer, or supplied reference image.
```

## Canonical YouTube Thumbnail Design System (Premium Layered Spine)

User-approved carry-forward decision: the widescreen (16:9, 1280x720) premium layered thumbnail design is approved as the authoritative visual spine for S01E01, S01E02, S01E03, and all future episodes of Mellow Longplay.

### 1. Typography & Brand Elements (Floating Text)
- **Brand Header:** `"mellow longplay"` in a soft, muted dark color matching the episode's mood and visual color palette (e.g., warm chestnut brown `(76, 56, 42)` for cafe/warm themes, slate-indigo `(42, 34, 52)` for night/cool themes). Rendered in serif Georgia Italic at size 25, placed at `(60, 60)`.
- **Episode Title:** All UPPERCASE, rendered in serif Georgia Bold at size 62. Employs a custom character tracking (letter-spacing) of **10px**, line spacing of **34px**, and shifted UP to **`y = 185`**. Programmatically simulated extrabold weight must be applied using a 3px matching outline stroke (`stroke_width=3` and matching color).
- **Soft Backlit Glow Halo:** Title and brand text layers must be backed by a soft, warm-cream glow contour (`blurred_glow_mask` with 16px to 18px Gaussian blur) to ensure perfect legibility and elegant backlighting.
- **Episode Identifier:** Placed in the top-right corner at `x = WIDTH - 150`, `y = 60` (e.g., `S01E01`, `S01E02`) using Georgia Regular at size 25. Rendered in light cream with a subtle dark outline, placed on top of the foreground character layer to remain fully readable.

### 2. Soft 3D Depth Blending (Text-Behind-Character)
- The brand header and episode title must be layered **behind** the right-side listener character.
- Character isolation uses a soft, feathered alpha mask (`subject_soft_mask` with a Gaussian blur of **22px**) so that hair strands, clothes, and outlines melt naturally over the background text.

### 3. Color-Matched Bottom Badges
- Placed at **`y = 540`** consisting of three beautiful, circular glassmorphic badges spaced horizontally at `x = 100`, `x = 220`, and `x = 340` (center of circles).
- Circle radius must be exactly 32px.
- Spacing between the circle seals and text labels must be exactly **18px**.
- Badge backgrounds are semi-transparent color-matched tones (sage green/dusty rose/warm sand with bronze outlines for S01E01; slate blue/twilight purple/moon sand with cool silver outlines for S01E02) containing custom high-precision outline icons (cafe cup, vinyl record, play button, book, headphones) and spaced label text.

### 4. Centered White Descriptive Caption
- Placed at **`y = 650`** centered horizontally.
- Text displays the exact descriptive suffix of the YouTube video title in standard Arial at size 22.
- Must be bounded by musical notes (`♪` and `♫ ♬` in Arial Bold at size 24).
- Rendered in sharp white with a beautiful soft dark shadow layer underneath (created with a Gaussian blur of 2.0) for perfect visibility.

## Safety Boundary

- Source-only visual identity guidance with local reference assets.
- No image generation, image editing, render/export, provider/API/browser/account automation, upload, or publishing approval.
- No use of the stored reference images as provider reference-image inputs unless a future explicit gate records provenance and approves that exact action.
- No protected likeness, real-person identity, celebrity/influencer resemblance, sexualized presentation, adult/minor implication, teacher/student romance, or real school identity. Teen/high-school framing is allowed only as explicitly approved PG same-age first-love source direction.
- No rights-safe, platform-safe, Content ID-safe, monetization-safe, upload-ready, publish-ready, copyright-free, royalty-free, or exclusive claim.

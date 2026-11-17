---
tags: [style, podcast, meme-clip]
date: 2026-11-17
---
# Meme clip style (VverPaldo concept, different look)

User (2026-11-17): "another style, but same concept as VverPaldo". Same CONCEPT as [[VverPaldo style]]: payoff hook first, then a hard cut
(2-frame white flash + camera flash) into the story, which ends right before the hook line so it loops; speaker zooms, slow
push-in that restarts on every shot, punch-ins on key words, green/red tints on payoff/fail, 15–22 s, music from the resources.

## Look (what is different)
- **Full-screen 9:16 face-cam**, no black bars. Single speaker = crop at full height (zoom 1 shows a 607 px slice of the 1920 source;
  Trevor tight = zoom 1.25–1.45, centre y 500). Group moments = **wide 16:9 band** over a blurred, darkened copy (`zoom < 1`).
- **White top banner** for the hook (Montserrat 800, 56 px, uppercase, black text, red `#E3201B` / green `#1DB954` keywords), like the card-pull refs D/F.
  Small "TREVOR LAWRENCE · NFL QB" pill under it for the first 2.5 s.
- **2–3 word glow captions** (Ref A): Montserrat 800, 82 px, uppercase, no stroke, white glow; keywords yellow/green/red with their own glow;
  words appear as spoken; punctuation stripped (keep "?"); y ≈ 1235 (chest).
- **iOS emoji pop** above the caption (150 px) on key words, with a quiet ding-2.
- **Whip** (horizontal slide + blur, 5 frames) on every cut and crop change, with fast-whoosh lined up on its 550 ms peak.
- Yellow CTA pill near the end (text only: emoji characters don't render as iOS in headless Chrome).
- Grade 67 on the footage (same as VverPaldo) + a light vignette.

## Code
- `viral-short/src/Meme.tsx` (comps `Meme-<id>`), plan `viral-short/plan_meme.py` → `src/meme.cfg.json` + `src/edits.gen.json`.
- **Gotcha (fixed):** each scene's `OffthreadVideo` must sit in its own `<Sequence from={sceneStart}>`, otherwise every scene after
  the first plays the wrong part of the source (and runs off the end = black frames).

---
tags: [style, podcast, stacked]
date: 2026-11-17
---
# Stacked style (VverPaldo concept, split-screen look)

User (2026-11-17): "different style now, but same concept; don't make the colour fade out; don't make it too blurry (a little is fine)".
Same CONCEPT as [[VverPaldo style]] (payoff hook → hard cut → story that loops into the hook, speaker zooms, push-in, punch-ins).

## Look
- Black header (y 0–190) with the hook: Montserrat 800, 56 px, uppercase, white with a 10 px black stroke, one yellow/red keyword.
- **Wide shot of the whole table** (y 190–798, full 16:9) with a **red ring on the speaker's head** (per-crop head positions in `ring`).
- **Speaker close-up** below (y 798–1920); crops (t, x, zoom, y) in source px, zoom 1 = 1040 px slice.
- **Seam captions**: 3-word chunks, white with black stroke, the spoken word in a **yellow highlight box** (tilted 2°).
- iOS emoji pop in the close-up's top-right corner, white CTA pill near the bottom.
- **No colour fades:** no tint flashes, no white fade, no vignette/darkening; the hook → story cut is a 1.15× zoom slam + camera-flash SFX.
- **Light blur only:** 4-frame whip (max 3 px blur) on close-up crop changes; no blurred backgrounds.

## Code
`viral-short/src/Stack.tsx` (comps `Stack-<id>`), plan `viral-short/plan_stack.py` → `src/stack.cfg.json`.
Head heights for the ring: seated ≈ y 320–340 in the 1080 source, standing ≈ 160.

# SEGA × Metaphor: ReFantazio trailer clipping (Clipping Culture) — brief 2026-11-21
- Brief doc 1NZVZllpdcC-XVgALOuqqyPthV1wf0t4xdK9nNEGcyIw. Footage = Frame.io share f.io/WAjz4A2Y (next.frame.io/share/a07dd8c9-…):
  list with Playwright, the graphql response holds assets.frame.io original links → footage/metaphor/{heismay, hero30 (Switch 2 launch), pro (hero faction PV), louis (villain PV)}.mp4
- Rules: caption = own line, then #Ad on its own line as FIRST hashtag, max 3 more related tags. Trailer ≠ "gameplay". No romance/shipping, no made-up dates/claims,
  no AI voice, original audio clearly audible (we use NO music). 50 % US. Min 10 s. Launch date Nov 12, 2026 (out now). Avoid the pre-order end card.
- Layout: native 1080x1080 crop (crisp, no upscale) or full 16:9 band (trailer kinetic text) on black; top white box text, captions in bottom bar. build_mrf.py + YLM.tsx (cfg ids hm/hv/fan).
- Delivered: m1 This is Heismay (22 s), m2 Hero vs Villain (22 s), m3 "more than an empty dream" (19 s).
- Unsure captions left out: "save the men/many" (hero30 21.8).

## Batch 2 (Nov 21) — user's reference TikTok (vt.tiktok.com/ZSpoaSpJc, 16:9 lore edit): copied the STYLE only, our trailer footage only.
Style = full-bleed 9:16 (crop 608 at cx, per-shot keyframes), ONE word at a time centre screen (Cinzel Bold, spaced, sentence-final word big),
punch-in on cuts, white flash into the finale, spaced hook label on top for 2.8 s. Code: build_mrf.py (mode 'full', 6th field = video start), plan_mrf.py → src/mrw.cfg.json, src/MRW.tsx (comp MRW-<id>).
- m4 wh: Heismay ("The only way to beat the darkness…", "I'd thought… I'd need power", "Step by meager step", ends on his Persona) 21 s
- m5 wl: Louis ("Only fair thing in this world is power", "I am the rightful king…", "I have a new world to build…") 15 s
- m6 wa: quotes ("Grief is its own death…", "In my ideal world…", "No matter who someone is…", "Fantasy is more than an empty dream…") 17 s

# ClipFarm × BOXABL "Deranged AI" — brief received 2026-11-19
- Brief: https://docs.google.com/document/d/1weeEQgET-YGyMU41MDfz2wr8mIhcb6IgCzl3rOoVjBk · $1 CPM, max $750/video, $1 min, Content Rewards.
- Wants ORIGINAL photorealistic AI videos (Veo/Kling/Grok etc.) with the BOXABL Casita as the star, BOXABL spelled right on screen + in caption,
  @boxabl tag in caption, platform AI label ON, mostly US audience, 7–30 s, hook in 1–2 s. No fake news/official announcements, no stock talk.
- **Our position:** we do NOT make realistic AI depictions of real people (Elon, Trump, the Tiramanis) — false-endorsement risk; matches the user's
  vault rule "no realistic fakes of real people". Also no AI video generator in the cloud box. Options offered: prompts for house/mascot-only ideas
  (flying BOXABL, robot unfold, nature documentary, invented mascot) that the user generates, then we edit; or non-photoreal animated mascot videos
  (may not qualify — ask ClipFarm first).
- User's page for it: **The Future Is Wild** (purple/orange, house + sparkles icon).

## Batch 1 (2026-11-19) — user picked option 2: animated mascot (non-photoreal), `viral-short/src/Boxabl.tsx` (comps `Boxabl-<id>`)
Mascot **Lil' Casita** (white Casita with window eyes, smile, legs + orange sneakers; catchphrase "Unfold the future!"). BOXABL printed on the
roof fascia in every shot + end card "BOXABL" logo. SVG flat cartoon, scenes zoomed 1.45× so the house is the focal point.
| id | idea | len | audio |
|---|---|---|---|
| bxunfold | truck delivers the box → hops off → unfolds → meet Lil' Casita → end card | 13.3 s | Chess (slowed) |
| bxfly | hook: flying over traffic → stuck → thrusters → "Tesla. SpaceX. Flying cars. BOXABL." → lands in backyard | 14.1 s | Montagem Alquimia |
| bxdoc | nature-doc narration (Kokoro bm_george, TTS input "Boxable" for pronunciation, captions forced to BOXABL), binocular open | 19.8 s | VO + Einaudi |
Kokoro install: `pip install kokoro-onnx` + models in ~/kokoro (github thewh1teagle/kokoro-onnx model-files-v1.0).

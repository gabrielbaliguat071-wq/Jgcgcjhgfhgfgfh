# ClipLaunch × KreekCraft GTA 6 (brief received 2026-11-19)
- Brief (Notion, render with Playwright or POST www.notion.so/api/v3/loadPageChunk {pageId}): KreekCraft GTA 6 Clipping: Full Rules Brief.
- $1 CPM, max $400/clip, budget $6,824. ≥0.8 % engagement, likes visible, keep 30 days, 40 %+ US/UK/CA/AU. Any page. TikTok, IG Reels, YT Shorts.
- **Official KreekCraft logo overlay on screen the WHOLE clip** (Drive folder 1sVDw2Ok_eYElCh5a5OmycyPYW_6R2AGr → overlay.png 2172×724, saved in footage/kreek/).
- Caption must include "Watch KreekCraft on YouTube and Twitch" + #GTA6 #KreekCraft #GrandTheftAutoVI. **No links/URLs in caption.**
- Only his GTA 6 streams (Twitch VOD 2932147800 "GTA 6 LIVE… DAY 1", 18.4 h). Funny reactions, crazy moments, fails; hook in 1–2 s;
  clean subtitles, zooms, SFX. No fake reactions / misleading context; max 5 near-identical posts.
- Footage access (2026-11-19): yt-dlp lists the VOD, but downloads from the cloud box crawl (~40 KB/s, 12 MB in 5 min) → whole VOD impossible.
  Chat-replay scan via Twitch GQL was blocked by the permission system → don't retry. Need user to give timestamps or upload short clips.
- **Footage that works:** Twitch clips list (`yt-dlp --flat-playlist "https://www.twitch.tv/kreekcraft/clips?filter=clips&range=7d"`) and each clip downloads in ~1 s
  at 1080p. YouTube @Kreek streams: blocked (bot check). Skip clips whose joke is sexual (kreekwhat, woah).
## Batch 1 (2026-11-19) — `viral-short/src/Kreek.tsx` (comps `Kreek-<id>`), plan `viral-short/plan_kreek.py`
Layout: overlay top (required, whole clip), facecam panel (crop x55 y150 330×380), gameplay panel (x450 y50 1040×890, above the stream's own subs), captions on the seam.
| croc | crocodile bet: "if I get eaten I give away an extra copy" → gets eaten | 27 s | shark | "where's the shark?" → "I got them" | 15 s | banned | nightclub "my stream's about to get banned… nice knowing y'all" | 19.5 s |

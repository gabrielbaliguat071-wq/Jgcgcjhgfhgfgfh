# ClipFarm × Higgsfield (Alex Mashrabov on 20VC) — brief received 2026-11-18

- Brief: https://docs.google.com/document/d/1QSSHUWVnnPPe0Mtaltvq7IjM0RbgiCJiEDAIjuBGm9M · $1 CPM, max $350/clip, min $1. Submit on Whop.
- **Footage (ONLY these):** full 4K episode on WeTransfer `we.tl/t-pRMHaT4pEb3zn2QX` (1.17 GB, 4542 s). Pull it with the WeTransfer API:
  `POST https://wetransfer.com/api/v4/transfers/<id>/download {"security_hash":"a7bc2d","intent":"entire_transfer"}` → `direct_link`.
  YouTube `jszn8rFtxm4` is only for finding times (brief times = YouTube times = file times).
- Watermark folder `186sFKTq8ZNAHdpduLFoguY0YB88eEfES` (black/white PNG). Drive said "Quota exceeded" → `https://lh3.googleusercontent.com/d/<id>=s0`
  returns the original PNG with alpha. Examples folder `1FLZsy7bTqf6bkqgJA8ycLXAbtJNfSiCs` → `yt-dlp https://drive.google.com/file/d/<id>/view` works when Drive quota blocks.
- Tags: YouTube **@HiggsfieldAI @20VC**, Instagram **@higgsfield.ai @20vchq**. IG Reels + YT Shorts only. 30–60 s. 40 %+ US/UK/CA/AU.
- **REQUIRED:** watermark big + readable + whole clip + never covered; English captions on the whole clip (names/numbers checked, key word highlighted,
  off faces); own hook text in the first seconds that matches the clip. **Never change Alex's words / stitch new sentences / imply he backs a product.**
- Brief's clip-idea table (times + "keep in mind") is in the doc: money numbers, AI hot takes, founder life.

## Look (copied from the 4 examples)
Full-frame 9:16 crop on the speaker (dark blue studio), white bold italic 1–3 word captions mid-frame with yellow key words/numbers,
red boxed hook lines for ~3.5 s, white info cards for numbers, dark bottom gradient. Examples use stock B-roll — we don't (ONLY provided footage).
Code: `viral-short/src/Higgs.tsx` (comp `Higgs-<id>`), plan `viral-short/plan_higgs.py` → `src/higgs.cfg.json`.
Seats: Alex close-up x≈890, Harry close-up x≈930 (centre y 510, zoom 1.15 hides the burned-in sponsor logos), wide shot Alex x≈300 / Harry x≈1420.

## Clips
| id | idea | structure | len |
|---|---|---|---|
| h4m | "$4M a month on AI" (33:23–34:01) | Harry: how much per month? → "over 4 million" → Harry "Wow" → $10K+/person/month, US + Asia → ~400 people, >$10K each | 34.9 s |
Note: the sentence before "prohibitively expensive" names a model the transcript can't hear clearly → left out rather than captioned wrong.

## Feedback log
- (waiting)

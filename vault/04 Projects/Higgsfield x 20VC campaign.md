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
| homes | "I made $1M… I own none" (59:16–1:00:09) | Harry: mega pad in Kazakhstan? → "I don't own any property" → "What? Why?" → sold the company, $1M+, apartments for parents/relatives/wife's parents, culture to give back, parents sacrificed → Tesla Model 3, not a Lamborghini guy | 48.4 s |
| legal | "I thought AI would replace legal and support. I was wrong." (36:27–37:21) | Harry: smaller teams with 10x people? → feeling legal/support would be replaced = one of our main mistakes, didn't grow those teams → legal 10+, customer success 40+, all use AI, no elimination → 60%+ first-line support by AI, but B2B doesn't work | 48.4 s |
| son | "One full day with my son in three months" (1:00:14–1:00:55) | hook = the one-day line → 80–90 hrs/week → wife 3 h, son 5 h a week → no shortcut to hard work | 32.4 s |
| ads | "We don't do any paid ads" (23:14–24:29) | hook = Harry "own content and distribution?" + "we don't do any paid ads" (brief: open at 24:27) → best commercial content made on Higgsfield, 150+ in-house creatives, ~half the workforce, launch videos + tutorials | 35.0 s |
| 100k | "Top creatives could spend $100,000 a month" (35:27–35:57) | hook = "close to 50K and 100K a month" (his prediction) → Harry: $4M, ~$10K/head, in 12 months? → keeps growing → salary raises too | 33.1 s |
| inv | "Investors shook hands, came back 30% lower" (46:38–47:01) | hook = "next day… pulled the syndicate… 30% lower valuation" → Harry: did you know Yuri would write the check? → shook hands… → "but it didn't happen with Yuri" | 33.0 s |
| phd | "You don't need PhD-level AI to make a viral video" (31:08–31:53) | hook = the PhD line → ad creatives by the hundreds, cheaper steerable models → PhD line | 33.9 s (margins part left out on purpose) |
| jensen | "What I learn from Jensen, Elon and Nik looks like micromanagement" (55:35–56:14) | hook = "knowing the details… corporate America would call it micromanagement" → taught corporate management, learns from Jensen/Elon/Nik, no 1:1s or soft feedback | 37.2 s |
| mom | "My mom worked three jobs" (50:23–51:17) | hook = "from the age of 7 to 12 my mother had to work three jobs" → Harry: regret one day with your son in 3.5 months? → goes beyond that → father dedicated his life (camps, he was a minor) → since 2021 Parkinson's, capital/exits can't change it → still misses birthdays, weddings | 43.7 s |
| 30k | "$30K on AI in a week" (34:15–34:58) | hook = "caught a guy who spent over $30K in a week" → Harry: how has it changed? → vibe coding → did it himself, five nights straight → "wouldn't say production ready, but we learned a lot" → many spend $10K+/week → finance team: too relentless | 42.6 s |
| plans | "Google & OpenAI will kill the $20 plans" (19:31–20:22) | hook = "completely demolish… $20 a month subscriptions" → can never win a $20/month market → why: Google/OpenAI → Harry rephrase, "I do believe that" → contrarian bet | 46.5 s |
Night batch (user: "why low views?"): 30–35 s, strongest line in second 1. The "$500,000 a month for legal/finance" bit after 100k sounds wrong in the transcript → not used.
Gotcha: add a crop at EVERY camera cut inside a scene (100k hook showed an empty studio when the wide shot came in).
Note (legal): cut a 2 s pause + one unfinished half-sentence (39.0–46.5).
Note (homes): cut a 1.7 s pause and the unclear words after "Tesla Model 3"; music = Einaudi piano (founder-life mood).
Note: the sentence before "prohibitively expensive" names a model the transcript can't hear clearly → left out rather than captioned wrong.

## Feedback log
- (waiting)

## User's channels (2026-11-18)
- #1 AI Founder Clips (@aifounderclips, blue) · #2 The Founder Files (@thefounderfiles, orange, YouTube) · #3 Big Money Talks (@bigmoneytalks, purple, YouTube).
- Each clip goes on ONE account only (posting the same clip on several pages = spam = unpaid).

## Batch 4 (2026-11-19) for The Founder Files: plan_higgs6.py, excerpts footage/higgs/tx6 (hmom 3000 s, h30k 2040 s, hplans 1160 s), auto crops from a shot map, -16 LUFS.
Captions: model name after "$30K in a week on …" is unclear ("Astra"?) → left out. "ability to capital" → "access to capital", "since 20 first" → 2021.
Unused brief ideas left: churn/NRR (21:20), 90 min film = 100+ h footage (23:55), 3,000-word prompts (27:25), margins (31:52), two US incumbents/China four (32:58+26:23),
AI support harder (37:35), researchers game tests (25:15), Claude→Codex (38:14), Europe (52:57), job-hopping (54:36), Yuri saw media shift (45:23).

## Clip 13 (2026-11-20): bench — "Researchers game tests to get their bonuses" (25:15–25:50, Alex's view, no lab named). plan_higgs7.py, excerpt footage/higgs/tx7/hbench.mp4 (1490 s), 45 s.
hook = "game benchmarks, get quarterly bonuses" → chasing benchmarks = corporate psyops → was in a large org, knows what happens → top researchers put test data into training → "couple million a year… can move to another lab easily".

## Clip 14 (2026-11-20): hop — "Silicon Valley job-hopping is a weakness" (54:36–55:18). plan_higgs8.py, excerpt tx7/hhop.mp4 (3265 s), 31 s. "Fuhn" = Fulham (two models agree).
hook = "people just jump between jobs every two years" → Europe/loyalty → Fulham fan won't root for Arsenal → US: Lakers bandwagon.

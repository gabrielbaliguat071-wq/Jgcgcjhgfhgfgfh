# ClipFarm × Topps (card collecting) — brief received 2026-11-18

- Brief: https://docs.google.com/document/d/1Fh3rSxEqWKC3XEoFOJSM3pmq2acdg40uL1uwYF_NU9A · $1 CPM, max $400/clip, $1 min, paid via Content Rewards, manual review.
- Platforms: YouTube Shorts, Instagram Reels, TikTok (listed as accepted; unlike Higgsfield/BOXED there is no "you must post on all" rule) → **fits a YouTube-only user.**
- **Only dedicated Sports Card / Trading Card pages.** 40 %+ US audience.
- Story-first: **never make the dollar value the hook** ("empty calories"); clip why the card matters, the person, the reaction. Value as a detail is OK.
- Rules: **NO #ad / #sponsored ever**; **no broadcast footage** (ESPN/NBA…); stay in the content bank; **no skull edits** (after 8/4); no slop reposting, no story boosting.
- Captions: nothing required (no tags/hashtags), natural, story-sounding. Tone: excitement, disbelief, FOMO — "He pulled WHAT" energy.
- Edit: hook in 2 s (reaction/reveal first, then rewind to the rip), split screens + over-the-top reactions work, BIG captions naming the card ("1/1 SUPERFRACTOR"), 9:16, fast cuts, every clip different.
- Footage: Topps content bank Drive `1vhBK4xGV_y_U0MgAtdk2xQMb5rFG_YO7`, Hobby House Drive `1BU7MplOoAhWsYOSRMjuCunxHvu1OMIYx`, content sheet `10fLnGpiuo1TrvFCfoe-d9dmu8PFcDZ_11-6q0ArL6kk`,
  Cooper Flagg DPA on SportsCenter (WeTransfer `we.tl/t-cWPTgjT3KaXLCsKs`, hero drop = priority), Topps YouTube long-forms (can't download from the cloud box → need Drive copies),
  Instagram pull reels (Ratatouille 1/1, Cooper Flagg /10, Jeter Superfractor, Ohtani /10, Yamal 1/1, Brady Cosmic, …), Fanatics Fest (Trick, A-Rod, Kevin O'Leary).

## Batch 1 (2026-11-18) — `viral-short/src/Topps.tsx` (comps `Topps-<id>`), plan `viral-short/plan_topps.py` → `src/topps.cfg.json`
Look: reveal first → 12-frame ◀◀ rewind scrub (scanlines + reversed whoosh) → the rip; card-name label (white + yellow, black outline) the whole clip;
the source edit's burned title/ticker hidden under a blurred band (label sits on it); 3-word captions just below; captions clear 0.5 s after the last word.
| id | file (Huge Pulls folder) | hook → story | len |
|---|---|---|---|
| flagg | Cooper Flagg Auto /10 | "Cooper Flagg out of 10! What a hit!" → rewind → top customer's last pack → the pull, "Bang! Let's go!" | 21.5 s |
| jeter | Derek Jeter Superfractor | "Derek Jeter one of one! You can't be serious!" → rewind → slides the cover off: "a one of one in this… for the Yankees!" | 22.5 s |
| ohtani | Shohei Ohtani Patch Auto /10 | "Out of 10. Shohei Ohtani auto patch. That is crazy." → rewind → the reveal from the start | 22.4 s |
Downloads: Drive file → `drive.usercontent…&confirm=t`, fall back to `yt-dlp https://drive.google.com/file/d/<id>/view` on quota.

## Feedback log
- (waiting)

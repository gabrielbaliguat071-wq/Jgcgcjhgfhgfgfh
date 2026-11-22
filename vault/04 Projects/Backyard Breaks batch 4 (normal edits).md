# Backyard Breaks batch 4 — 3 normal card-pull edits (2026-11-19, no narration)
Sheet 1eX0vqF73N9x2gtkRbalnKMHRd3nbd-CEv0Rt4D2glM4: tab gid 1203111212 = Historical Big Pulls (Drive links, value, caption), gid 1029565171 = the Trevor stream clips.
Template src/Pull.tsx (cfg pull.cfg.json, plan viral-short/plan_bb3.py): white banner over the stream bar + iOS emoji, card cam blurred with ❓ in the hook,
whip + whoosh, glow captions, reveal = flash + shake + punch on the card + NAME / CARD / $PRICE + cha-ching, question with iOS emoji. Music 0.1 under the real audio.
| id | card | hook | len |
|---|---|---|---|
| bbshield | Josh Allen NFL shield 1/1 ($5–12K+) — sheet says Allen into Purdy shield, but only Allen is visible, so only Allen named | "Sam, you're paying for your wedding. No more Chick-fil-A" | 24.1 s |
| bbjordan | Michael Jordan 1986 Fleer rookie ($3–5K) | crowd erupting (card blurred) → "sweat of a lifetime", "Clark Kellogg, the goat", "more MJs in chat", "did I just see what I think I saw?" | 28.0 s |
| bbbrady | Tom Brady Black Diamond 1/1 ($8K+, real diamond) | "Oh my God!" → Pick 3 Choose 1 → fireworks | 25.3 s |
Disk: Remotion bundles copy all of public/ → keep public small (old g67/bx/h excerpts deleted 2026-11-19; regenerate from plan scripts).

## Batch 5 (2026-11-20) — user: "I only made $1" → copy BYB's own viral pattern (sheet tab gid 183567664 "Historical Viral Content"):
money stories / generosity / deals / collections beat plain pulls (Josh Allen 1/1 given to a kid 227K, "cards I lost a house on" 210K, "never profit on" 150K, buyback 146K).
plan_bb4.py (appends to pull.cfg.json; Pull.tsx now has bannerY/capY; talk clips zoom 1.6 from the top since the table below is empty; reveal.at = -1 = no stack):
bbsoup 28.7 s (broccoli cheddar "shampoo" advice) · bbjudge 41.7 s (Judge $5.2M sale, "cash is dead", Darren woke up +$100K) · bbgrail 29.9 s (LeBron 10/10 pop 7, bought a grail without knowing) · bbdeal 37.9 s ("I want it all", $5,500 vs $4,500 + Honors box).
More from the Live Stream tab: "Aaron Judge outpays the S&P 500", "Grant talking about how cash is dead", "Big sales in the hobby", "Three nukes come back PSA 10", Wemby red /5 $30K, Flagg PSA 10 $15K.

## Batch 6 (2026-11-20): plan_bb5.py — bbwemby (red auto /5, first ever in product) · bbflagg (Gold auto comes back PSA 10, "eight racks on your head") · bbsp500 (Judge card 25x the S&P; no zoom so captions sit above the phone) · bbtrevor (Silver PSA 9 "bang!") · bbsesko ("he created the light bulb") · bbnukes (3 for 3 PSA 10).

## Trevor batch (2026-11-20, user: Trevor clips = high virality): plan_bb6.py — every Trevor row on the sheet is now used (tab 1 stream clips all done earlier; u1_playbook has no speech after 60 s).
tlkaboom (Green Kaboom 1/1 \$15K) · tlshield (NFL shield auto \$40–100K) · tltalk (football talk: sat 74 min in last 11, up 30) · tlred (red /5 "Trevor forever") · tlteal (teal /199 "He's the NFL!").
More Trevor = new rows on the sheet (team adds clips after streams) — re-export tab gid 133317179 and grep trevor.

## Trevor stream, fresh moments (2026-11-20): plan_tv7.py (VverPaldo) — tvleft (t3 0–56: "best QB I've ever seen" + rolls LEFT), tvfields (nt_rip 94–134: Justin Fields RPA \$20K→\$200–500), tvsweat (nt_rip 14–60: Grant teaches Trevor to sweat a card).
Still unused in sources: nt_rip 0–14 (Jaguar-face patch value), nt_rip 134–141 (redemptions), t4 0–8 (bought for 10, now 20), t4 71–83 (1/1 Clemson vs NFL value).

## bbnever (2026-11-22): user sent YT short dNJZz88Y_Dk ("THESE SPORTS CARDS COULD BUY HIM A HOUSE", BACKYARDBREAKS team) — YouTube blocked (bot check), so used the closest
sheet row: TikTok 7561161222456954142 "Some cards that grant will NEVER sell because he held too long" (same Grant, same set). `viral-short/build_never.py` → YLM-bbnever (54.4 s):
crop 788x1400 from top (drops their burned captions at y≈0.77), white band over their intro title, hook "another 10… makes me sick" → how it started → Trey Lance $15K/30K offer/ankle → Tank Bigsby → Jalen Green $6K→$1.5K → 10 more Lances → "haven't lost if I haven't sold" → COPE OR FACTS?
Gotcha: hook + later span reuse the same source time → caption times must come from the span offset, not a source→timeline lookup.

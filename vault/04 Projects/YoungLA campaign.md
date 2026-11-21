# YoungLA campaign (2026-11-19)
Brief: Google Doc 1SQ0LBBBeynuUffVGPGjIxlk1lnFqeeTLZner23fDRPA. Footage = ONLY the Dropbox "Bodybuilders vs Models" fashion-show video (footage/youngla/bvm.mp4, 1920x1080 23.976, 22.5 min; words in footage/youngla/tx/bvm.words.json).
Rules: YoungLA branding + clothing clearly shown; organic + funny captions; must NOT look like an ad; no account tags; TikTok / IG / YT Shorts;
40%+ Tier-1 audience, >=0.50% engagement, keep up 30 days, likes visible, submit on Whop. Min payout $1.50 IG/TikTok, $2 YT.

Look: Meme.tsx (cfg in meme.cfg.json, plan = viral-short/plan_youngla.py), tints off, bgBlur 10. Interview two-shots + wide runway (YoungLA sign + cars) = band;
runway walks = full-height crop on the model; hook on the guest's close-up G(x) = (x, 1.18, 430). Shot list: .work/brief7/shots.jpg (index -> crop in SHOT dict).
Avoid: the "brand shutting down" joke ending (misleading), leading with the $1M giveaway (ad-like). Star the swears.

| id | hook | src s |
|---|---|---|
| yaneg | "Try negative $152,000" (taxes) -> buy equity in YoungLA, 51% | 760-798 |
| yaaura | most aura = Griffin the sound guy | 825-866 |
| yalate | 3 hours late, straight to the bathroom | 503-535 |
| yahand | "I already have a G-Wagon. I'm already handsome" | 586-618 |
| yajay | Jay Cutler's first fashion show, SF90, compression shirts | 1049-1146 |
| yaceo | owner: craziest collab, biggest franchise -> Dragon Ball Z in April | 923-962 |

## VverPaldo re-cut (user asked, 2026-11-19): yv*
Same moments, Guess.tsx look (plan_youngla_vp.py converts ya* scenes -> yv*, cfg src/yv.cfg.json, registered in Guess.tsx).
Crops: two-shot / wide -> (900, 1, 540) (keeps host + guest / sign + cars), runway model -> (x, 1.15, 560), close-up -> (x+40, 1.6, 460).
Render: .work/render_youngla_vp.sh. The user prefers VverPaldo for this campaign.

## Popular guests x3 (Big Marlon / Jay Cutler), VverPaldo — plan_marlon.py (ml*), cfg in yv.cfg.json
Marlon = pink hoodie + white skully (transcribed "Marlin"). The interview mic holder = left (x~600), co-host right (x~1440).
mlwalk (Burberry model, "don't know how much Gary paid him", skully bit) 164.8-192.4 | mlbrag (Calvin Klein, H&M, "not trying to brag", beats Burberry) 259-300 |
mlaura (Jay Cutler vs Marlon aura battle) 130-146, 164-171, 233-257. Avoid 179-230 + 386-410 (giveaway talk + "EVERY $100" graphic = ad).
Unused: the 0-22 s cold open (burned-in "COMING UP" text), Lukie's Skyline (349-360), Quave in pink (361-385).

## Funny one: mlig (plan_funny.py, 19 s) — backstage reaction-stick test (866-917): keeps dropping it, "take four", then "I need this for my IG bro" -> "so we're all here on your time now, huh?"
Other funny spots still unused: Gary "can I run? No." runway practice (1012-1047, b-roll heavy), "you can go home bro, we need 30 more" (676-686),
Johnny's aura "felt it in my midsection… head, shoulders, knees and toes" (416-447).

## Instagram x6 (2026-11-20): plan_youngla_ig.py (yig*, VverPaldo, cfg yv.cfg.json): johnny aura 31.5 s · lex disney villain 16.3 s · bald spot 18.2 s · can I run 21.4 s · go home 30 more 13.4 s · pink 24.2 s.
IG account: "Gym Fits & Laughs" @gymfitsandlaughs (pfp vault/assets/gymfits_pfp.png).

## Runway montage (2026-11-21, user brief: 10–25 s, funny, freeze-frames/slow-mo, end on "who won?"): src/YLM.tsx over a pre-built ffmpeg cut (public/ylm/base.mp4, script in chat history: segments 1204.05–1206.6 slow 0.6 + 0.7 s freeze cx920 · 1181.6–1185.4 band · 1228.6–1231.6 Jay cx840 · 1276.4–1279.0 slow 0.7 + freeze cx660 · 1291–1295 + 1.2 s freeze cx560). 21.4 s.

## Runway montages 2-4 (Nov 21) — YLM.tsx is now cfg-driven (src/ylm.cfg.json, bases built by build_ylm.py)
- reel8 "little dance move" (dance): 650.3 dance flex hook + freeze, Jay & friend laughing (653.5 band), twins same fit (635.6), double bicep on stage (600.2 slow-mo), dance pt 2 (647.6), navy flex end "who had the best moves?"
- reel9 "rating runway walks" (rate): 1112 entrance / 1078.6 / 1092.3 back / 966 beanie / 934 chains / 1132 stare; score stamps, base audio muted
- reel10 "$1M answer" (million): commentator interview audio 749-797 (the table guy, NOT the navy-tee bodybuilder) over runway b-roll; ends on his face-cover freeze at "51%"

## Funniest moments compilation (Nov 21): yfun (build_ylm.py SEGS 'yfun' + ylm.cfg.json) — handsome / dance + judges / twinning / slipped + take four / he doesn't know / -$152,000. 25 s.
## Hook reels (Nov 21, IG): flash-forward hook = punchline first → freeze 'HOW IT STARTED ⏪' + rewind sfx → full story.
- reel12 model (146–160: 'they told me I can't model… they put me behind the curtains'), reel13 walkout (318–337.7, bleeped swears via cfg mutes + censor beep, crop top=1 to hide the original's burned captions). Skully bit (177–192) dropped: two-shot too dark/small.
- reel14 soclose (Lukey guesses Quave listens to 'Justin Bieber-esque 2008 song' → 'Childish Gambino… I was so close'; sq mode = 1080² crop for the 3-person table). Fresh funny moments in bvm.mp4 are now nearly used up.
- reel15 cars (everyone's car pick → Jay: 'that's Robbie's car' 'I take that one'), reel16 canihave ('Can I have some?' 'No.' + everyone wanting the million; no entry/$100 lines), reel17 favpiece (favourite piece = what they're wearing). Interviews play as VO over runway b-roll in the source.
- edit1 (Nov 21, user: 'edit instead of just clipping'): phonk_n 18.44–37.44 (drop 22.43), 15 walk/flex shots on the beat, slow-mo build-up, zoom pulse per beat, glitch cuts, flash+shake on the drop, 'who walked it best?' end. build_edit.py + MRW cfg ed1.

# Trevor Lawrence x5 in the VverPaldo style (2026-11-17)

User ask: "Create 5 trevor lawrence video using the vverpaldo style". Picked 5 sheet clips that had **no VverPaldo edit yet**
(already done: neck, ant, fans, ticket, celly, redeem, goat). Plan: `viral-short/plan_tv5.py` → `src/tv5.cfg.json` + `src/edits.gen.json`,
comps `Guess-tvjosh|tvgolf|tvslab|tvpeyton|tvplays`, outputs `viral-short/out/final/<id>.mp4` (gitignored).

| id | sheet clip (Drive) | hook (payoff first) → story | song (res/*_n) | len |
|---|---|---|---|---|
| tvjosh | ex-teammate pull `1XOyOUZ…` | "not rookie Josh Allen… the real Josh Hines-Allen" → gold/teal/glove banter → "that's a rookie card" (loops into hook) | funkabn 0.5 s | 19.8 s |
| tvgolf | dream golf foursome `1Do0Wyx…` | "throw Jesus in there" → question → all-time humans → "need a week" → Tiger, golf GOAT | chess 38 s | 20.7 s |
| tvslab | Tiger slab gift `10w4Y3r…` | "whole care package for you… that's for me?" → 4 years in his collection → shirt, tag, glove, cap, wow | brevis 36 s | 17.5 s |
| tvpeyton | Peyton relationship `1CFmd-I…` | "rookie season… when it was not going well" → texts all season → "a guy you look up to? He was one" → Peyton's rough Indy start | blue 21.5 s | 20.2 s |
| tvplays | playbook `1Ye7w4m…` | "8 to 10 new plays a week" → question → hundreds of plays → coaches pick from the whole inventory | phonk (AURA) 0.5 s | 21.5 s |

## How it was built (reuse)
- Footage: `scripts/drive_dl.sh` (one at a time) → `footage/src/`. Resources (BGSONGS, SFX, overlays, emoji PNGs) from the FOMO
  "editing resources" Drive folder `11RA-8-Am7HJW5Hzr0051f_eUgl0YBtMw` (list it with `drive.google.com/embeddedfolderview?id=<folder>`,
  no API needed) → `viral-short/public/res/` with the names Guess.tsx expects (flash, shock, rizz, riser, pop, s_*.mp3, e_*.png, arrow, skull,
  greenflash2, cashfall). Songs → `*_n.mp3` via `loudnorm=I=-20`; drops from `scripts/find_drops.py`.
- Grade 67 is baked into `public/g67_<id>.mp4` excerpts (footage only); the plan shifts source times to the excerpt.
- Crops from one frame strip per clip (`.work/strip.py`); seats are the same in every Trevor clip: left host x≈470, Trevor x 960, right host x≈1500.
  **Tight crops need centre y ≈ 440–460** so faces sit high in the box and the one-word captions (y≈1060) land on the chest, not the face.
- Top line must fit 2 lines (≈ 45 characters incl. 💀); 3 lines looked crowded.
- Captions held until the next word (always on screen). Plain words: "PC" → collection, "auto" → autograph.
- Skipped: NT box rip (the "ew, get that out of here" card can't be read on camera → can't caption it truthfully), and its ending repeats the redemption clip.
- Master: two-pass loudnorm −14 LUFS / −1.5 dBTP, `-map_metadata -1`, video copied.

## Feedback log
- (waiting)

## Batch tv6 (2026-11-19): 6 more, fresh moments — `viral-short/plan_tv6.py` → `src/tv6.cfg.json`
| id | source | hook → story | song | len |
|---|---|---|---|---|
| tvpresnap | presnap `1IFLtTD…` | "I know it should go here and it ends up going there" → % of pre-snap reads (50–65 %, coverage changes 15 %) | Sentamento | 32.2 s |
| tvpacks | Backyard Packs `1OwYNUl…` | "every pack you open would be a Trevor Lawrence… every card?" → digital repacks shipped home | Funk Abnormal | 22.0 s |
| tvking | entrance `1OQKwlc…` | "Boys. Here you go" → "All hail the king" ×3 | Empire | 17.3 s |
| tvmarino | NT rip (50–80 s) | "Top ten? I mean, gotta be" → Atwater, "come on Trevor", Dan Marino all time? "he could sling it" | AURA phonk | 19.4 s |
| tvartist | golf (58–78 s) | "Oh I love Chris (Stapleton)" → favorite artist → shout out mom and dad in the chat | Blue | 17.2 s |
| tvkeepsake | ticket (40–71 s) | "I don't have the ticket for the national championship" → signed a ton for fans, kept a couple game-worn in his closet | Montagem | 25.2 s |
Framing: Trevor crops need centre y ≈ 510–520 (face high, captions on chest). NT rip seat: Trevor x 980.

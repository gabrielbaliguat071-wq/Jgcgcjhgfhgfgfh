"""ClipFarm x Higgsfield clip 3 (2026-11-18): "I thought AI would replace legal and support. I was wrong." (brief 36:27-37:21, hot take).
Source: public/hlegal.mp4 = full episode 2180-2250 s (1080p); times = seconds in that excerpt. Harry's question -> Alex's mistake ->
team sizes today + "I don't see any elimination" -> AI handles 60%+ of first-line support, but for B2B it doesn't work.
Cuts: a 2 s pause (10.3-12.4) and one unfinished half-sentence (39.0-46.5, "like at these professions where I say quite close today...").
Adds the clip to src/higgs.cfg.json (keeps the others)."""
import json
W = json.load(open('../footage/higgs/tx3/hlegal.words.json'))
FIX = {(50.42, '60'): '60%', (50.88, '%'): ''}
HI = {'10x', 'legal', 'customer', 'support', 'replaced.', 'mistakes', '10', '40', 'ai', 'heavily.', 'elimination.', '60%', 'b2b,', 'work', 'doesn\'t'}
HC, AW = (960, 1.15, 510), (290, 1.45, 470)
def ac(x=900): return (x, 1.15, 510)
PLAN = [
 ('q', 0.00, 7.70, [(0.00, HC)]),
 ('a1', 7.80, 10.30, [(7.80, ac(920))]),
 ('a2', 12.38, 27.80, [(12.38, ac(920))]),
 ('a3', 29.40, 39.00, [(29.40, AW), (37.17, ac(880))]),
 ('a4', 46.55, 47.70, [(46.55, ac(880))]),
 ('a5', 48.84, 60.80, [(48.84, ac(880)), (50.25, AW), (56.21, ac(900))]),
]
scenes = []
for sid, a, b, crops in PLAN:
    n = round((b - a) * 30); words = []
    for w in W:
        ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
        if not (a - 0.05 <= ws < b - 0.05): continue
        hit = [v for (ft, fw), v in FIX.items() if abs(ft - ws) < 0.03 and fw == t.lower()]
        t2 = hit[0] if hit else t
        if not t2: continue
        f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
        words.append({'word': t2, 'startFrame': f0, 'endFrame': f1, 'hi': t2.lower().strip('.,?') in {h.strip('.,?') for h in HI}})
    scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'crops': [[round((t - a) * 30), x, z, y] for t, (x, z, y) in crops], 'words': words})
    print(sid, round(n / 30, 2), 's |', ' '.join(w['word'] for w in scenes[-1]['words']))
def at(sid, word, nth=0):
    s = next(x for x in scenes if x['id'] == sid)
    return [sid, [w for w in s['words'] if w['word'].lower().startswith(word.lower())][nth]['startFrame']]
cfg = json.load(open('src/higgs.cfg.json'))
cfg['legal'] = dict(src='hlegal.mp4', wm='higgsfield_wm.png', hook=['AI was supposed to replace', 'legal & support. It didn\'t.'], hookFrames=105,
  music=['loseyou_n', 74.0], musicVol=0.07, scenes=scenes, cards=[
    dict(at=at('a3', '10'), dur=50, big='10+', small='people on the legal team'),
    dict(at=at('a3', '40'), dur=55, big='40+', small='in customer success'),
    dict(at=at('a5', '60%'), dur=70, big='60%+', small='of first-line requests handled by AI')])
print('total', round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's')
json.dump(cfg, open('src/higgs.cfg.json', 'w'), indent=1)

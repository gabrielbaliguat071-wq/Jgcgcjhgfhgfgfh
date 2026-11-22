"""ClipFarm x Higgsfield clip 1 (2026-11-18): "$4M a month on AI models" (brief idea 33:23-34:01, big number first, keep Harry's reaction).
Source: public/h4m.mp4 = full episode 1990-2100 s (1080p). Times below are seconds in that excerpt. Whole sentences only, his meaning kept:
hook = Harry's question + Alex's answer + Harry's "Wow" -> setup (why models are expensive, $10K+/person/month) -> answer (~400 people, >$10K each).
Crops (t, x, zoom, y) in 1920x1080 source px; full-height 9:16 crop (zoom 1 = 608 px wide)."""
import json
W = json.load(open('../footage/higgs/tx/h4m.words.json'))
FIX = {(15.78, 'hicksfield,'): 'Higgsfield,', (18.08, '$10'): '$10,000', (18.50, ',000'): '', (20.68, 'dollars'): '',
       (47.26, '$10'): '$10,000', (49.32, ',000'): ''}
HI = {'$10,000', '4', 'million.', '400', 'expensive.', 'over', 'wow.', 'higgsfield,', 'month', 'person.'}
AC, HC = (890, 1.15, 510), (930, 1.15, 510)          # Alex / Harry close-ups
AW, HW = (300, 1.45, 430), (1420, 1.45, 430)         # Alex / Harry in the wide two-shot
PLAN = [
 ('hook', 27.62, 37.95, [(27.62, HW), (30.46, AC), (35.96, HC)]),
 ('c1', 14.92, 26.62, [(14.92, AC), (16.67, AW)]),
 ('c2', 37.95, 50.72, [(37.95, HC), (39.67, AC)]),
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
        words.append({'word': t2, 'startFrame': f0, 'endFrame': f1, 'hi': t2.lower() in HI})
    scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'crops': [[round((t - a) * 30), x, z, y] for t, (x, z, y) in crops], 'words': words})
    print(sid, round(n / 30, 2), 's |', ' '.join(w['word'] for w in scenes[-1]['words']))
def at(sid, word, nth=0):
    s = next(x for x in scenes if x['id'] == sid)
    return [sid, [w for w in s['words'] if w['word'].lower().startswith(word.lower())][nth]['startFrame']]
CFG = {'h4m': dict(src='h4m.mp4', wm='higgsfield_wm.png', hook=['They spend over $4M', 'a month on AI models'], hookFrames=105,
  music=['loseyou_n', 13.0], musicVol=0.07, scenes=scenes, cards=[
    dict(at=at('hook', '4'), dur=60, big='$4M+', small='per month on AI models'),
    dict(at=at('c1', '$10,000'), dur=75, big='$10K+', small='per person · per month'),
    dict(at=at('c2', '400'), dur=60, big='~400', small='people on the team')])}
print('total', round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's')
json.dump(CFG, open('src/higgs.cfg.json', 'w'), indent=1)

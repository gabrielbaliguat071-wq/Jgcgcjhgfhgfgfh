"""ClipFarm x Higgsfield clip 2 (2026-11-18): "I made $1M and bought homes for my family. I own none." (brief 59:16-1:00:09, founder life).
Source: public/hhomes.mp4 = full episode 3540-3620 s (1080p); times below are seconds in that excerpt. Opens on Harry's short question
(brief: "start with Harry's short question"). Cuts: a 1.7 s pause, and two words after "Tesla Model 3" the transcript can't hear clearly.
Adds the clip to src/higgs.cfg.json (keeps the others)."""
import json
W = json.load(open('../footage/higgs/tx2/hhomes.words.json'))
FIX = {(37.86, 'wife'): "wife's", (33.28, 'apartments'): 'apartments'}
HI = {'kazakhstan?', 'property.', 'million', 'dollars', 'apartments', 'parents,', 'culture.', 'back.', 'sacrificed', 'tesla', 'model', '3', 'lamborghini', 'porsche.', 'what?', 'why?'}
AW, HW = (300, 1.45, 430), (1540, 1.45, 530)
PLAN = [
 ('q', 16.70, 21.29, [(16.70, HW), (18.88, (1000, 1.15, 510))]),
 ('why', 21.29, 23.30, [(21.29, (880, 1.15, 500))]),
 ('a1', 23.30, 47.10, [(23.30, (955, 1.15, 510)), (40.29, AW), (43.21, (955, 1.15, 510))]),
 ('a2', 48.80, 62.20, [(48.80, (955, 1.15, 510)), (58.58, AW)]),
 ('a3', 63.95, 68.60, [(63.95, AW)]),
]
scenes = []
for sid, a, b, crops in PLAN:
    n = round((b - a) * 30); words = []
    for w in W:
        ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
        if not (a - 0.05 <= ws < b - 0.05): continue
        hit = [v for (ft, fw), v in FIX.items() if abs(ft - ws) < 0.03 and fw == t.lower()]
        t2 = hit[0] if hit else t
        f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
        words.append({'word': t2, 'startFrame': f0, 'endFrame': f1, 'hi': t2.lower() in HI})
    scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'crops': [[round((t - a) * 30), x, z, y] for t, (x, z, y) in crops], 'words': words})
    print(sid, round(n / 30, 2), 's |', ' '.join(w['word'] for w in scenes[-1]['words']))
def at(sid, word, nth=0):
    s = next(x for x in scenes if x['id'] == sid)
    return [sid, [w for w in s['words'] if w['word'].lower().startswith(word.lower())][nth]['startFrame']]
cfg = json.load(open('src/higgs.cfg.json'))
cfg['homes'] = dict(src='hhomes.mp4', wm='higgsfield_wm.png', hook=['He made over $1M…', 'and owns no property'], hookFrames=105,
  music=['einaudi_n', 44.0], musicVol=0.08, scenes=scenes, cards=[
    dict(at=at('q', 'property'), dur=60, big='0', small='properties he owns'),
    dict(at=at('a1', 'million'), dur=75, big='$1M+', small='made when his company sold'),
    dict(at=at('a2', 'tesla'), dur=70, big='Tesla Model 3', small='what he drives')])
print('total', round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's')
json.dump(cfg, open('src/higgs.cfg.json', 'w'), indent=1)

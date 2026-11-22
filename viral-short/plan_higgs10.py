"""ClipFarm x Higgsfield clip 21 (2026-11-21): brief idea "two US incumbents / China" — Alex at 26:12-26:58: on OpenRouter data the only
relevant US incumbent is Google; China has Tencent, Xiaomi, Alibaba (+ ByteDance catching up); takeaway = tech bubble obsessed with benchmarks
that don't represent reality, video benchmarks = text-to-video, not real workflows. Excerpt footage/higgs/tx9/hchina.mp4 (1565 s).
Run from viral-short/: python3 plan_higgs10.py"""
import json, shutil, os
A, AW = (880, 1.15, 510), (290, 1.45, 470)
SHOTS = [(0, A), (15.8, AW), (27.87, A), (48.27, AW), (54.97, A), (68.77, AW)]
def crops(a, b):
    cur = [k for t, k in SHOTS if t <= a][-1]
    return [(a, cur)] + [(t, k) for t, k in SHOTS if a < t < b - 0.1]
FIXAT = {11.18: '', 11.38: 'OpenRouter', 13.72: 'relevant', 20.18: 'where', 25.22: 'Xiaomi,', 29.20: 'incumbents', 32.98: 'ByteDance',
         40.20: '', 40.36: '', 53.10: "video's"}
hi = {'google,', 'only', 'china,', 'tencent,', 'xiaomi,', 'alibaba,', 'three', 'bytedance', 'obsession', 'benchmarks', 'reality.', 'text', 'video,', 'workflows', 'openrouter'}
plan = [('hook', 7.1, 15.6), ('c1', 18.45, 35.1), ('c2', 35.15, 47.9), ('c3', 51.65, 57.9)]
src = 'hchina'
if not os.path.exists(f'public/{src}.mp4'): shutil.copy(f'../footage/higgs/tx9/{src}.mp4', f'public/{src}.mp4')
W = json.load(open(f'../footage/higgs/tx9/{src}.words.json')); scenes = []
for sid, a, b in plan:
    n = round((b - a) * 30); words = []
    for w in W:
        ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
        if not (a - 0.05 <= ws < b - 0.05): continue
        hit = [v for ft, v in FIXAT.items() if abs(ft - ws) < 0.015]
        t2 = hit[0] if hit else t
        if not t2: continue
        f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
        words.append({'word': t2, 'startFrame': f0, 'endFrame': f1, 'hi': t2.lower().strip('.,?') in {h.strip('.,?') for h in hi}})
    scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'crops': [[round(max(0, t - a) * 30), x, z, y] for t, (x, z, y) in crops(a, b)], 'words': words})
def at(sid, word):
    s = next(x for x in scenes if x['id'] == sid)
    return [sid, [w for w in s['words'] if w['word'].lower().startswith(word.lower())][0]['startFrame']]
cfg = json.load(open('src/higgs.cfg.json'))
cfg['china'] = dict(src=src + '.mp4', wm='higgsfield_wm.png', hook=['Only ONE US tech giant is', 'relevant in AI models'], hookFrames=100,
                    music=['investigations_n', 60.0], musicVol=0.07, scenes=scenes,
                    cards=[dict(at=at('hook', 'Google'), dur=70, big='GOOGLE', small='the only relevant US incumbent on OpenRouter'),
                           dict(at=at('c1', 'three'), dur=60, big='3 in China', small='Tencent · Xiaomi · Alibaba')])
print('== china', round(sum(s['durationInFrames'] for s in scenes) / 30, 1), 's')
for s in scenes: print('  ', s['id'], s['crops'], '|', ' '.join(w['word'] for w in s['words']))
json.dump(cfg, open('src/higgs.cfg.json', 'w'), indent=1)

"""ClipFarm x Higgsfield clip 14 (2026-11-20): brief idea 'Silicon Valley job-hopping is a weakness' (54:36-55:18, kept about building strong teams), excerpt tx7/hhop.mp4 = 3265 s. Based on plan_higgs6, which covered clips 10-12 (2026-11-19, for The Founder Files): brief ideas "My mom worked three jobs" (50:23),
Whole sentences only; pauses/repeats cut (brief allows). Crops are picked automatically from the shot map (A = Alex close-up,
H = Harry close-up, W = wide -> zoom on whoever speaks). Unclear model name in h30k ("Astra"?) is left out instead of captioned wrong."""
import json, shutil, os
AC, HC = (925, 1.15, 510), (930, 1.15, 510)
AW, HW = (290, 1.45, 470), (1440, 1.45, 470)
SHOTS = {'hhop': [(0, 'W'), (2.37, 'A'), (24.37, 'W'), (37.37, 'A'), (53.17, 'H'), (58.53, 'A')]}
def crops(src, a, b, who):
    def crop(k): return {'A': AC, 'H': HC}.get(k) or (AW if who == 'A' else HW)
    cur = [k for t, k in SHOTS[src] if t <= a][-1]
    out = [(a, crop(cur))] + [(t, crop(k)) for t, k in SHOTS[src] if a < t < b - 0.1]
    return out
CLIPS = {
 'hop': dict(src='hhop', who={},
   fix={(34.95, 'fuhn'): 'Fulham', (48.89, 'fun'): 'fan'},
   hi={'silicon', 'valley,', 'jump', 'jobs', 'two', 'years.', 'europe', 'competitive,', 'loyalty', 'fulham', 'arsenal', 'champions', 'league', 'lakers', 'united', 'states,'},
   plan=[('hook', 15.75, 21.7), ('c1', 22.55, 29.25), ('c2', 33.75, 41.8), ('c3', 42.45, 52.9)],
   hook=['Silicon Valley has a', 'loyalty problem'], music=['blue_n', 21.5],
   cards=[('hook', 'two', 70, 'Every 2 years', 'how often he sees people switch jobs')]),
}
cfg = json.load(open('src/higgs.cfg.json'))
for cid, c in CLIPS.items():
    if not os.path.exists(f"public/{c['src']}.mp4"): shutil.copy(f"../footage/higgs/tx7/{c['src']}.mp4", f"public/{c['src']}.mp4")
    W = json.load(open(f"../footage/higgs/tx7/{c['src']}.words.json")); scenes = []
    for sid, a, b in c['plan']:
        n = round((b - a) * 30); words = []
        for w in W:
            ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
            if not (a - 0.05 <= ws < b - 0.05): continue
            hit = [v for (ft, fw), v in c['fix'].items() if abs(ft - ws) < 0.03 and fw == t.lower()]
            t2 = hit[0] if hit else t
            if not t2: continue
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t2, 'startFrame': f0, 'endFrame': f1, 'hi': t2.lower().strip('.,?') in {h.strip('.,?') for h in c['hi']}})
        for i in range(len(words) - 1, 0, -1):
            if words[i]['word'].startswith('-'): words[i - 1]['word'] += words[i]['word']; words.pop(i)
        cr = crops(c['src'], a, b, c['who'].get(sid, 'A'))
        scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'crops': [[round((t - a) * 30), x, z, y] for t, (x, z, y) in cr], 'words': words})
    def at(sid, word):
        s = next(x for x in scenes if x['id'] == sid)
        return [sid, [w for w in s['words'] if w['word'].lower().startswith(word.lower())][0]['startFrame']]
    cfg[cid] = dict(src=c['src'] + '.mp4', wm='higgsfield_wm.png', hook=c['hook'], hookFrames=100, music=c['music'], musicVol=0.07, scenes=scenes,
                    cards=[dict(at=at(s, w), dur=d, big=b, small=sm) for s, w, d, b, sm in c['cards']])
    print(f'== {cid}', round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's')
    for s in scenes: print('  ', s['id'], '|', ' '.join(w['word'] for w in s['words']))
json.dump(cfg, open('src/higgs.cfg.json', 'w'), indent=1)

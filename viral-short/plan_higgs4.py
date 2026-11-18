"""ClipFarm x Higgsfield clips 4-6 (2026-11-18 night batch). User asked why views are low -> shorter (30-35 s) + strongest line in second 1.
Whole sentences only, his meaning kept (brief allows reordering whole sentences, e.g. its own "open at 24:27, then the part before").
Excerpts (1080p, gitignored): hson = 3600 s, hads = 1385 s, h100k = 2115 s; times below are seconds in the excerpt."""
import json
def ac(x=960, y=510): return (x, 1.15, y)
def aw(x=290, y=470): return (x, 1.45, y)
CLIPS = {
 'son': dict(src='hson', fix={(21.80, 'hicksfield.'): 'Higgsfield.'},
   hi={'three', 'months,', 'one', 'day', 'son', 'son.', 'emails,', '90', 'hours', 'wife.', 'five', 'hard', 'work.', 'luckier'},
   plan=[('hook', 45.30, 54.25, [(45.30, ac())]),
         ('c1', 15.36, 21.95, [(15.36, ac())]),
         ('c2', 23.10, 33.20, [(23.10, ac()), (25.92, aw(320, 520))]),
         ('c3', 54.85, 61.60, [(54.85, ac()), (55.08, aw())])],
   hook=['One full day with his son', 'in 3 months'], music=['einaudi_n', 120.0],
   cards=[('c1', '90', 60, '80–90 hrs', 'a week on Higgsfield'), ('c2', 'five', 60, '5 hrs', 'a week with his son')]),
 'ads': dict(src='hads', fix={(83.88, 'page.'): 'paid ads.', (17.28, 'hicksfield,'): 'Higgsfield,'},
   hi={'paid', 'ads.', '150', '150.', 'half', 'workforce,', 'best', 'commercial', 'tutorials.', 'launch', 'own', 'content', 'distribution.'},
   plan=[('hook', 77.20, 84.12, [(77.20, (900, 1.15, 470)), (83.04, ac(920))]),
         ('c1', 9.66, 28.10, [(9.66, ac()), (21.00, aw(270, 470))]),
         ('c2', 28.55, 29.30, [(28.55, aw(270, 470))]),
         ('c3', 31.00, 39.90, [(31.00, aw(270, 470))])],
   hook=['They don\'t pay', 'for ANY ads'], music=['loseyou_n', 40.0],
   cards=[('c1', '150', 60, '150+', 'in-house creatives'), ('c3', 'half', 60, '~50%', 'of the whole team')]),
 '100k': dict(src='h100k', fix={(7.66, '10'): '$10,000', (7.94, ',000'): '', (29.78, '10'): '10x', (29.98, ',000.'): '', (30.00, 'x'): '', (6.96, '4'): '$4'},
   hi={'50k', '100k', 'month', '10x', '$4', 'million,', '$10,000', '12', 'growing.', 'salary', 'raise'},
   plan=[('hook', 22.36, 31.70, [(22.36, ac(920)), (28.96, aw(280, 470))]),
         ('c1', 5.00, 11.95, [(5.00, (900, 1.15, 480))]),
         ('c2', 12.75, 21.20, [(12.75, ac(920))]),
         ('c3', 32.85, 41.20, [(32.85, aw(280, 470)), (38.46, ac(920))])],
   hook=['Top creatives could spend', '$100K a month on AI'], music=['interstellar_n', 10.0],
   cards=[('hook', '100k', 70, '$50K–100K', 'a month per top creative'), ('c1', '$4', 55, '$4M', 'spent today, ~$10K per head')]),
}
cfg = json.load(open('src/higgs.cfg.json'))
for cid, c in CLIPS.items():
    W = json.load(open(f"../footage/higgs/tx4/{c['src']}.words.json")); scenes = []
    for sid, a, b, crops in c['plan']:
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
        scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'crops': [[round((t - a) * 30), x, z, y] for t, (x, z, y) in crops], 'words': words})
    def at(sid, word):
        s = next(x for x in scenes if x['id'] == sid)
        return [sid, [w for w in s['words'] if w['word'].lower().startswith(word.lower())][0]['startFrame']]
    cfg[cid] = dict(src=c['src'] + '.mp4', wm='higgsfield_wm.png', hook=c['hook'], hookFrames=100, music=c['music'], musicVol=0.07, scenes=scenes,
                    cards=[dict(at=at(s, w), dur=d, big=b, small=sm) for s, w, d, b, sm in c['cards']])
    print(f'== {cid}', round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's')
    for s in scenes: print('  ', s['id'], '|', ' '.join(w['word'] for w in s['words']))
json.dump(cfg, open('src/higgs.cfg.json', 'w'), indent=1)

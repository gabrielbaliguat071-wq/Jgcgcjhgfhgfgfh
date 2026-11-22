"""ClipFarm x Higgsfield clips 7-9 (2026-11-18). User asked why views are low -> shorter (30-35 s) + strongest line in second 1.
Whole sentences only, his meaning kept (brief allows reordering whole sentences, e.g. its own "open at 24:27, then the part before").
Excerpts: hinv = 2770 s, hphd = 1855 s, hjensen = 3320 s; times below are seconds in the excerpt."""
import json
def ac(x=960, y=510): return (x, 1.15, y)
def aw(x=290, y=470): return (x, 1.45, y)
CLIPS = {
 'inv': dict(src='hinv', fix={(43.78, '30'): '30%', (44.02, '%'): '', (43.22, 'invests'): 'invest'},
   hi={'30%', 'lower', 'valuation', 'shook', 'hands', 'games.', 'scars.', 'yuri.', 'yuri', 'check?', 'price.', 'next', 'day,'},
   plan=[('hook', 38.45, 46.30, [(38.45, ac())]),
         ('c1', 25.70, 50.80, [(25.70, (960, 1.15, 500)), (29.04, ac()), (49.46, aw(260, 430))])],
   hook=['They shook hands…', 'then came back 30% lower'], music=['loseyou_n', 60.0],
   cards=[('hook', '30%', 60, '-30%', 'on the deal they shook hands on')]),
 'phd': dict(src='hphd', fix={(31.16, 'phd'): 'PhD'},
   hi={'phd', 'level', 'intelligence', 'viral', 'hundreds', 'week,', 'cheapest,', 'steerable', 'social', 'media', 'video.', 'needed'},
   plan=[('hook', 29.95, 38.35, [(29.95, ac(960))]),
         ('c1', 12.90, 38.35, [(12.90, ac(920)), (17.79, aw(270, 520)), (27.13, ac(960))])],
   hook=["You don't need PhD-level AI", 'to make a viral video'], music=['interstellar_n', 40.0],
   cards=[('c1', 'hundreds', 60, '100s', 'of ad videos a week')]),
 'jensen': dict(src='hjensen', fix={(28.78, 'nick.'): 'Nik.', (30.56, 'nick'): 'Nik', (24.28, "i'm"): "I've", (45.32, 'encouraged,'): 'encourage,'},
   hi={'jensen,', 'elon', 'nik.', 'micromanagement.', 'details,', 'abandon', 'management', 'principles.', 'one-on-one', 'soft', 'feedback.', 'corporate'},
   plan=[('hook', 43.95, 53.40, [(43.95, ac(860))]),
         ('c1', 16.15, 43.95, [(16.15, ac(960)), (22.88, aw(280, 440)), (34.38, ac(860))])],
   hook=['Jensen, Elon & Nik', 'break every management rule'], music=['einaudi_n', 160.0],
   cards=[('c1', 'jensen', 75, 'Jensen · Elon · Nik', 'the CEOs he learns from')]),
}
cfg = json.load(open('src/higgs.cfg.json'))
for cid, c in CLIPS.items():
    W = json.load(open(f"../footage/higgs/tx5/{c['src']}.words.json")); scenes = []
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


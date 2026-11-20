"""ClipFarm x BOXED.GG (2026-11-20): Cam Jordan vs Greg Rousseau box battle (Sack Summit 9x16, Dropbox). Funny loser hook first
("Cam, sorry man… I didn't want this anyway"), then intro, his loyal Mahomes pick, the battle (crop past the app's gem values onto
the players), Greg wins. No odds/values/"at stake" talk. Caption code = ROUSSEAU (Greg Rousseau is in the clip). Appends to boxed.cfg.json."""
import json
def full(cy=960): return (540, 1.0, cy)
PEOPLE = (540, 2.2, 500)   # battle screens: players on top, app UI with gem values below -> crop to the players
C = dict(src='bx_camjordan', band=[1175, 1355], capY=1215, hook=['"I didn\'t want this anyway"', 'Cam Jordan after his BOXED battle'],
   fix={(46.30, 'steff'): 'Steph', (46.30, 'rookie'): 'rookie', (75.64, 'box'): 'BOXED'},
   hi={'cam', 'jordan,', 'greg', 'rousseau,', 'steph', 'curry', 'loyal.', 'mahomes,', 'five', '25.', 'god.', 'hurts.', 'anyway.', 'congrats,', 'boxed', 'both', 'cards,'},
   plan=[('hook', 69.60, 72.70, [(69.60, full())]),
         ('c1', 0.00, 3.75, [(0.00, full())]),
         ('c2', 45.40, 52.25, [(45.40, full())]),
         ('c3', 59.25, 65.70, [(59.25, PEOPLE)]),
         ('c4', 67.25, 68.20, [(67.25, full())]),
         ('c5', 73.65, 77.30, [(73.65, full())])])
W = json.load(open('../footage/boxed/tx/camjordan.words.json')); scenes = []
for sid, a, b, crops in C['plan']:
    n = round((b - a) * 30); words = []
    for w in W:
        ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
        if not (a - 0.05 <= ws < b - 0.05): continue
        hit = [v for (ft, fw), v in C['fix'].items() if abs(ft - ws) < 0.03 and fw == t.lower()]
        t2 = hit[0] if hit else t
        if not t2: continue
        f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
        words.append({'word': t2, 'startFrame': f0, 'endFrame': f1, 'hi': t2.lower() in C['hi']})
    scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'crops': [[round((t - a) * 30), x, z, y] for t, (x, z, y) in crops], 'words': words})
cfg = json.load(open('src/boxed.cfg.json'))
cfg['camjordan'] = dict(src=C['src'] + '.mp4', srcW=1080, srcH=1920, band=C['band'], capY=C['capY'], hook=C['hook'], hookFrames=90, scenes=scenes)
print('camjordan', round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's')
for s in scenes: print('  ', s['id'], '|', ' '.join(w['word'] for w in s['words']))
json.dump(cfg, open('src/boxed.cfg.json', 'w'), indent=1)

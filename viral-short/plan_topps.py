"""ClipFarm x Topps batch 1 (2026-11-18): Cooper Flagg auto /10, Derek Jeter 1/1 Superfractor auto, Shohei Ohtani patch auto /10.
Brief: reveal/reaction first (hook), REWIND to the rip, then the rip + reaction. Story-first: the card + the moment, never the price.
Sources = the Topps content bank 'Huge Pulls & UGC Moments' files (720x1280); times = seconds in those files."""
import json
F = (360, 1.0, 640)
CLIPS = {
 'flagg': dict(band=None, labelY=70, capY=300, label=['Cooper Flagg', 'auto /10'],
   fix={(11.56, 'cooper'): 'Cooper', (11.88, 'flying'): 'Flagg'},
   hi={'cooper', 'flagg', '10!', '10.', 'hit!', 'bang!', 'auto'},
   plan=[('hook', 11.30, 14.40, None), ('rw', 14.40, 1.00, 'rewind'), ('rip', 1.00, 18.95, None)]),
 'jeter': dict(band=[488, 702], labelY=508, capY=715, label=['Derek Jeter', '1/1 Superfractor auto'],
   fix={},
   hi={'one!', 'one', 'derek', 'jeter', 'yankees!', 'serious!', 'baby,', 'baby.'},
   plan=[('hook', 30.90, 37.70, None), ('rw', 37.70, 5.90, 'rewind'), ('s1', 5.90, 12.00, None), ('s2', 17.95, 24.00, None), ('s3', 27.75, 30.90, None)]),
 'ohtani': dict(band=[683, 828], labelY=688, capY=842, label=['Shohei Ohtani', 'patch auto /10'],
   fix={(5.52, 'choyotani'): 'Shohei Ohtani', (12.80, 'fire'): 'fire', (13.42, 'hunter.'): ''},
   hi={'shohei', 'ohtani', '10.', 'crazy.', 'god.', 'fire', 'patch.', 'auto'},
   plan=[('hook', 2.90, 9.70, None), ('rw', 9.70, 0.00, 'rewind'), ('rip', 0.00, 15.20, None)]),
}
cfg = {}
for cid, c in CLIPS.items():
    W = json.load(open(f'../footage/topps/tx/{cid}.words.json')); scenes = []
    for sid, a, b, kind in c['plan']:
        if kind == 'rewind':
            scenes.append({'id': sid, 'videoStartSec': b, 'durationInFrames': 12, 'crops': [[0, *F]], 'words': [], 'rewind': [a, b]}); continue
        n = round((b - a) * 30); words = []
        for w in W:
            ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
            if not (a - 0.05 <= ws < b - 0.05): continue
            hit = [v for (ft, fw), v in c['fix'].items() if abs(ft - ws) < 0.03 and fw == t.lower()]
            t2 = hit[0] if hit else t
            if not t2: continue
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t2, 'startFrame': f0, 'endFrame': f1, 'hi': any(p.lower() in c['hi'] for p in [t2.lower()] + t2.lower().split())})
        scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'crops': [[0, *F]], 'words': words})
    cfg[cid] = dict(src=f'tp_{cid}.mp4', srcW=720, srcH=1280, band=c['band'], capY=c['capY'], label=c['label'], labelY=c['labelY'], scenes=scenes)
    print(f'== {cid}', round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's')
    for s in scenes: print('  ', s['id'], '|', ' '.join(w['word'] for w in s['words']))
json.dump(cfg, open('src/topps.cfg.json', 'w'), indent=1)

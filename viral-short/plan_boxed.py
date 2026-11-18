"""ClipFarm x BOXED.GG batch 1 (2026-11-18): Holloway (Expedition Charizard), Crosby vs Von Miller box battle, IslandGrown Golden Ticket pulls.
Hook = the reaction / best pull first, then the rip/story, ending right before the hook moment (loops). Times = seconds in the source file
(public/bx_<name>.mp4 = the creators' 9:16 files from the BOXED Dropbox). Banned on screen: odds ("Rare: 30%"), gem/dollar values, the
creators' burned captions -> crops avoid/zoom past them and the template blurs the caption band. Swear (crosby 64.9) and "by like a hundred" cut."""
import json
def full(cy=960): return (540, 1.0, cy)
CLIPS = {
 'holloway': dict(src='bx_holloway', band=[1175, 1355], capY=1215, hook=['He pulled an', 'Expedition Charizard'],
   fix={(15.10, 'girl'): 'grail', (21.34, 'charzard'): 'Charizard', (29.52, 'box?'): 'BOXED?', (55.98, 'charzar,'): 'Charizard,', (57.34, 'hollow'): 'holo',
        (70.56, 'box'): 'BOXED', (55.68, 'expedition'): 'Expedition'},
   hi={'grail', 'charizard', 'charizard,', 'brother.', 'boxed?', 'boxed', 'zard.', 'expedition', 'holo', 'family,', 'son', 'sick.'},
   plan=[('hook', 52.45, 58.15, [(52.45, full())]),
         ('c1', 14.65, 22.05, [(14.65, full())]),
         ('c2', 28.10, 31.50, [(28.10, full())]),
         ('c3', 64.95, 74.80, [(64.95, full())])]),
 'crosby': dict(src='bx_crosby', band=[1175, 1355], capY=1215, hook=['Maxx Crosby vs Von Miller', 'last pack decides it'],
   fix={(36.96, 'brian.'): 'Bryant.', (37.64, '2'): '24', (37.64, '.4.'): '', (38.42, '2'): '24', (38.42, '.4.'): '', (40.18, '2'): '24', (40.18, '4.'): '',
        (40.74, '2'): 'Two', (53.22, 'bag'): 'pack', (70.68, 'tommy'): 'Tommy', (71.00, 'b.'): 'B.'},
   hi={'kobe', 'bean', 'bryant.', '24', 'goats', 'head.', 'magic', 'god.', 'battle.', 'signed', 'tommy', 'b.', 'love,', 'wow.', 'this.'},
   plan=[('hook', 52.40, 60.00, [(52.40, full()), (55.50, (540, 3.4, 780)), (57.40, (540, 2.2, 400)), (59.55, full())]),
         ('c1', 36.20, 45.95, [(36.20, full()), (45.40, (540, 3.4, 780))]),
         ('c2', 65.95, 67.62, [(65.95, full())]),
         ('c3', 68.72, 82.65, [(68.72, full())])]),
 'island': dict(src='bx_island', band=None, capY=1430, hook=['Golden Ticket night', 'on BOXED'],
   fix={(0.20, 'boxed'): 'BOXED', (6.18, 'vali'): 'Silvally', (9.50, 'archaeus'): 'Arceus', (10.00, 'di'): '', (10.26, 'alga'): 'Dialga',
        (11.32, 'charzart'): 'Charizard', (12.12, 'braxton.'): 'Braixen.', (13.34, 'mimicu'): 'Mimikyu', (14.54, 'it'): '', (14.70, 'ends'): '', (14.86, 'resolve.'): '',
        (15.78, 'pimplap'): 'Piplup', (18.40, 'flygun.'): 'Flygon.', (19.38, 'songolio'): 'Solgaleo', (20.68, 'stilix'): 'Steelix'},
   hi={'silvally', 'gx.', 'arceus', 'dialga', 'palkia.', 'charizard', 'braixen.', 'mimikyu', 'piplup', 'rainbow', 'flygon.', 'solgaleo', 'lunala.', 'steelix', 'jasmine', 'boxed'},
   plan=[('hook', 19.30, 21.75, [(19.30, full())]),
         ('c1', 0.00, 19.30, [(0.00, full())])]),
}
cfg = {}
for cid, c in CLIPS.items():
    W = json.load(open(f"../footage/boxed/tx/{c['src'].replace('bx_', '')}.words.json")); scenes = []
    for sid, a, b, crops in c['plan']:
        n = round((b - a) * 30); words = []
        for w in W:
            ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
            if not (a - 0.05 <= ws < b - 0.05): continue
            hit = [v for (ft, fw), v in c['fix'].items() if abs(ft - ws) < 0.03 and fw == t.lower()]
            t2 = hit[0] if hit else t
            if not t2: continue
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t2, 'startFrame': f0, 'endFrame': f1, 'hi': t2.lower() in c['hi']})
        scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'crops': [[round((t - a) * 30), x, z, y] for t, (x, z, y) in crops], 'words': words})
    cfg[cid] = dict(src=c['src'] + '.mp4', srcW=1080, srcH=1920, band=c['band'], capY=c['capY'], hook=c['hook'], hookFrames=90, scenes=scenes)
    print(f'== {cid}', round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's')
    for s in scenes: print('  ', s['id'], '|', ' '.join(w['word'] for w in s['words']))
json.dump(cfg, open('src/boxed.cfg.json', 'w'), indent=1)

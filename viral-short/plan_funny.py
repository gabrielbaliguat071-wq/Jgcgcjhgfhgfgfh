"""YoungLA funny one (Nov 19), VverPaldo (Guess.tsx), ~20 s: the backstage reaction-stick test — he keeps dropping it, needs
take after take, then admits it's "for my IG" and gets called out. Hook = the IG line. SFX for the jokes (myinstants files
already in public/res). Short on purpose (user: "not too long, just enough"). Run from viral-short/: python3 plan_funny.py"""
import json, os, subprocess
SRC = '../footage/youngla/bvm.mp4'
G67 = ("split[ga][gb];[gb]gblur=sigma=14[gg];[ga][gg]blend=all_mode=softlight:all_opacity=0.245,unsharp=5:5:1.74:5:5:0,"
       "eq=contrast=1.113:saturation=1.26:gamma=0.98,curves=all='0/0 0.25/0.21 0.75/0.81 1/1',unsharp=3:3:0.79,format=yuv420p")
PLAN = [
    ('hook', 906.2, 909.55, [(906.2, (640, 1.3, 430)), (907.6, (840, 1.3, 430))]),
    ('c1', 867.7, 870.65, [(867.7, (1000, 1.0, 540))]),
    ('c2', 878.0, 883.7, [(878.0, (1000, 1.0, 540)), (880.4, (1180, 1.5, 380)), (882.0, (840, 1.0, 540))]),
    ('c3', 897.4, 899.7, [(897.4, (800, 1.0, 540)), (898.9, (1040, 1.4, 420))]),
    ('c4', 911.55, 916.55, [(911.55, (920, 1.25, 430)), (914.5, (960, 1.25, 430))]),
]
FIX = {'griffin,': 'Griffin', 'dog.': 'dog'}
FIXAT = {880.74: '', 880.78: '', 880.94: '', 881.42: '', 881.28: '', 881.52: '', 881.74: '', 883.44: '', 883.46: '', 883.60: ''}   # "you know I'm supposed to go to them" / stutter
W = [(w['startMs'] / 1000, w['endMs'] / 1000, w['text']) for w in json.load(open('../footage/youngla/tx/bvm.words.json'))]
gen = json.load(open('src/edits.gen.json'))
eid = 'mlig'
xa, xb = min(a for _, a, _, _ in PLAN) - 0.5, max(b for _, _, b, _ in PLAN) + 0.5
out = f'public/g67_{eid}.mp4'
if not os.path.exists(out):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(xa), '-to', str(xb), '-i', SRC, '-vf', G67, '-c:v', 'libx264', '-crf', '17',
                    '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', out], check=True)
scenes = []
for sid, a, b, crops in PLAN:
    n = round((b - a) * 30); words = []
    for ws, we, t in W:
        if not (a - 0.05 <= ws < b - 0.05): continue
        hit = [v for ft, v in FIXAT.items() if abs(ft - ws) < 0.015]
        t2 = (hit[0] if hit else FIX.get(t.lower(), t)).strip(',.')
        if not t2: continue
        f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
        words.append({'word': t2, 'startFrame': f0, 'endFrame': f1})
    for i in range(len(words) - 1): words[i]['endFrame'] = words[i + 1]['startFrame']
    cr = [[max(0, round((t - a) * 30)), x, z, y] for t, (x, z, y) in crops]
    scenes.append({'id': sid, 'videoStartSec': round(a - xa, 3), 'durationInFrames': n, 'cropX': 960, 'crops': cr, 'words': words})
gen[eid] = scenes
print(eid, round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's |', ' / '.join(s['id'] + ': ' + ' '.join(w['word'] for w in s['words']) for s in scenes))
json.dump(gen, open('src/edits.gen.json', 'w'))

def png(at, f, x=870, y=1290, size=200, **k): return dict(at=at, kind='png', file=f, x=x, y=y, size=size, **k)
def sfx(at, f, v=0.45): return dict(at=at, kind='sfx', file=f, v=v)
G, R = 'G', 'R'
c = dict(top='He needed 4 TAKES to catch a stick… for his IG', hl={'4': '#F40305', 'TAKES': '#F40305', 'IG': '#58EE28'}, cta='*how many takes would YOU need?*',
   music=['funkabn_n', 33.2], ctaAt=['c4', 'no'],
   tints=[[['hook', 'ig'], G], [['c2', 'slipped'], R], [['c3', 'four'], R], [['c4', 'time'], R]], rizz=[['hook', 'ig']],
   punch=[['hook', 'ig'], ['hook', 'personal'], ['c1', 'run'], ['c2', 'slipped'], ['c2', 'hands'], ['c2', 'one'], ['c3', 'take'], ['c3', 'four'], ['c4', 'frame'], ['c4', 'time'], ['c4', 'huh']],
   blowouts=[['c3', 'four']], blackFlash=[['c4']], streaks=[['c1'], ['c3']],
   extras=[sfx(['hook', 'ig'], 'm_record-scratch.mp3', 0.3), sfx(['hook', 'personal'], 's_huh.mp3', 0.35),
           sfx(['c2', 'slipped'], 's_fahhh.mp3', 0.3), png(['c2', 'slipped'], 'e_sob.png', 860, 1240),
           sfx(['c3', 'four'], 's_awk.mp3', 0.3), png(['c3', 'four'], 'e_laugh.png', 230, 1240),
           sfx(['c4', 'huh'], 'm_oh-hell-nah.mp3', 0.3), png(['c4', 'no'], 'e_laugh.png', 860, 1240)])
c.update(track='none', calls=[], intro=True, hardcut=True, cutSfx='s_camflash.mp3', src=f'g67_{eid}.mp4')
sc = {s['id']: s for s in scenes}
refs = [r for r, _ in c['tints']] + [r for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks') for r in c[k]] + [c['ctaAt']] + [e['at'] for e in c['extras']]
for r in refs:
    if len(r) == 1: continue
    ws = [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())]
    assert ws, (r, [w['word'] for w in sc[r[0]]['words']])
allc = json.load(open('src/yv.cfg.json')); allc[eid] = c
json.dump(allc, open('src/yv.cfg.json', 'w'), indent=1); print('cfg ok')

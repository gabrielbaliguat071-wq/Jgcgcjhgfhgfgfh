"""YoungLA x3 — the popular guests (Big Marlon + Jay Cutler), VverPaldo style (src/Guess.tsx, Nov 19). Same footage
(footage/youngla/bvm.mp4). Hook = best line, hard cut, story that leads back to it. Crops (t source s, x, zoom, y), Guess
semantics (zoom 1 = ~1083 px of source width). Run from viral-short/: python3 plan_marlon.py"""
import json, os, subprocess
SRC = '../footage/youngla/bvm.mp4'
G67 = ("split[ga][gb];[gb]gblur=sigma=14[gg];[ga][gg]blend=all_mode=softlight:all_opacity=0.245,unsharp=5:5:1.74:5:5:0,"
       "eq=contrast=1.113:saturation=1.26:gamma=0.98,curves=all='0/0 0.25/0.21 0.75/0.81 1/1',unsharp=3:3:0.79,format=yuv420p")
IV = (990, 1.0, 540)              # interview two-shot (host + commentator)
def M(x, z=1.15, y=560): return (x, z, y)   # runway / standing person
MC = (1020, 1.5, 330)
L, RR = (600, 1.25, 430), (1440, 1.25, 430)   # mic holder (left) / co-host (right)             # Marlon leaning in behind the desk (face near the top of frame)
EDITS = {
 'mlbrag': [
     ('hook', 290.9, 295.95, [(290.9, MC), (294.6, IV)]),
     ('c1', 259.0, 268.3, [(259.0, L), (262.1, M(1280)), (264.1, L), (265.4, (1000, 1.0, 540))]),
     ('c2', 275.2, 289.4, [(275.2, (1000, 1.0, 540)), (281.9, MC), (287.6, (1000, 1.0, 540))]),
     ('c3', 297.8, 299.5, [(297.8, (1000, 1.0, 540))])],
 'mlaura': [
     ('hook', 250.8, 256.05, [(250.8, M(880)), (255.95, L)]),
     ('c1', 130.2, 145.8, [(130.2, L), (133.2, M(800)), (135.8, M(880)), (137.6, L)]),
     ('c2', 164.8, 170.6, [(164.8, M(880)), (169.1, M(960))]),
     ('c3', 233.7, 237.6, [(233.7, M(920))]),
     ('c4', 249.6, 250.75, [(249.6, M(880))])],
 'mlwalk': [
     ('hook', 170.7, 175.4, [(170.7, M(960)), (171.4, M(1000)), (172.8, (960, 1.0, 540))]),
     ('c1', 164.8, 170.6, [(164.8, M(880)), (169.1, M(960))]),
     ('c2', 177.0, 192.4, [(177.0, L), (179.26, M(1000, 1.15, 520)), (180.89, M(1440)), (182.22, L), (187.0, RR), (189.7, L)])],
}
FIX = {'marlin.': 'Marlon.', 'marlin': 'Marlon', "marlin's": "Marlon's", 'culler': 'Cutler', 'fucking': 'f***ing', 'shit.': 'sh*t.', 'shit': 'sh*t',
       'very': 'very', 'ora': 'aura', 'jem': 'Gym', 'mogoff?': 'mog-off?', 'cliff.': 'clip.', 'chee': 'Cheese', '-cheez.': '', 'scully.': 'skully.', 'scully,': 'skully,'}
FIXAT = {174.8: 'Gary', 244.0: 'YoungLA,', 244.1: '', 291.8: '', 292.6: '', 298.0: 'YoungLA', 298.1: '', 182.5: 'YoungLA', 182.8: '', 143.0: 'face', 188.6: 'out?', 177.0: '', 177.3: '', 290.7: ''}
W = [(w['startMs'] / 1000, w['endMs'] / 1000, w['text']) for w in json.load(open('../footage/youngla/tx/bvm.words.json'))]
gen = json.load(open('src/edits.gen.json'))
for eid, plan in EDITS.items():
    xa, xb = min(a for _, a, _, _ in plan) - 0.5, max(b for _, _, b, _ in plan) + 0.5
    out = f'public/g67_{eid}.mp4'
    if not os.path.exists(out):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(xa), '-to', str(xb), '-i', SRC, '-vf', G67, '-c:v', 'libx264', '-crf', '17',
                        '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', out], check=True)
    scenes = []
    for sid, a, b, crops in plan:
        n = round((b - a) * 30); words = []
        for ws, we, t in W:
            if not (a - 0.05 <= ws < b - 0.05): continue
            hit = [v for ft, v in FIXAT.items() if abs(ft - ws) < 0.06]
            t2 = hit[0] if hit else FIX.get(t.lower(), t)
            t2 = t2.strip(',.')
            if not t2: continue
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t2, 'startFrame': f0, 'endFrame': f1})
        for i in range(len(words) - 1, 0, -1):
            if words[i]['word'].startswith(('-', "'", '&')): words[i - 1]['word'] += words[i]['word']; words.pop(i)
        for i in range(len(words) - 1): words[i]['endFrame'] = words[i + 1]['startFrame']
        cr = [[max(0, round((t - a) * 30)), x, z, y] for t, (x, z, y) in crops]
        scenes.append({'id': sid, 'videoStartSec': round(a - xa, 3), 'durationInFrames': n, 'cropX': 960, 'crops': cr, 'words': words})
    gen[eid] = scenes
    print(eid, round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's |', ' / '.join(s['id'] + ': ' + ' '.join(w['word'] for w in s['words']) for s in scenes))
json.dump(gen, open('src/edits.gen.json', 'w'))

def png(at, f, x=870, y=1290, size=200, **k): return dict(at=at, kind='png', file=f, x=x, y=y, size=size, **k)
def ov(at, f, dur=34): return dict(at=at, kind='ov', file=f, dur=dur)
def sfx(at, f, v=0.45): return dict(at=at, kind='sfx', file=f, v=v)
G, R = 'G', 'R'
CFG = {
 'mlbrag': dict(top="Big Marlon says the YoungLA runway BEATS Burberry", hl={'BEATS': '#58EE28'}, cta='*better than Burberry?*', music=['phonk_n', 22.4],
   ctaAt=['c2', 'what'],
   tints=[[['hook', 'calvin'], G], [['hook', 'brag'], R], [['c2', 'comparison'], G], [['c3', 'cake'], G]], rizz=[['c2', 'belongs']],
   punch=[['hook', 'calvin'], ['hook', 'h&m'], ['hook', 'brag'], ['c1', 'marlon'], ['c1', 'crushed'], ['c2', 'burberry'], ['c2', 'comparison'], ['c2', 'belongs'], ['c2', 'belong'], ['c3', 'cake']],
   blowouts=[['hook', 'brag']], blackFlash=[['c2']], streaks=[['c1'], ['c3']],
   extras=[png(['hook', 'brag'], 'e_laugh.png', 860, 1240), sfx(['hook', 'wow'], 's_wow.mp3', 0.35), sfx(['c2', 'comparison'], 's_huh.mp3', 0.4), ov(['c3', 'cake'], 'greenflash2.mp4')]),
 'mlaura': dict(top='JAY CUTLER vs BIG MARLON — who has more aura?', hl={'JAY': '#58EE28', 'CUTLER': '#58EE28', 'MARLON': '#F40305', 'BIG': '#F40305'}, cta='*Jay or Marlon?*', music=['empire_n', 18.8],
   ctaAt=['c3', 'people'],
   tints=[[['hook', 'jay'], G], [['c1', 'face'], R], [['c1', 'aura', 1], G], [['c3', 'favorite'], G]], rizz=[['hook', 'jay']],
   punch=[['hook', 'vote'], ['hook', 'jay'], ['hook', 'old'], ['hook', 'look'], ['c1', 'mog'], ['c1', 'aura'], ['c1', 'face'], ['c1', 'aura', 1], ['c2', 'marlon'], ['c2', 'strong'], ['c3', 'big'], ['c3', 'favorite'], ['c4', 'looks']],
   blowouts=[['hook', 'jay']], blackFlash=[['c2']], streaks=[['c1', 'we'], ['c3']],
   extras=[png(['hook', 'look'], 'e_think.png', 860, 1240), sfx(['c1', 'face'], 's_huh.mp3', 0.35), sfx(['c3', 'favorite'], 's_wow.mp3', 0.35), ov(['hook', 'aura'], 'greenflash2.mp4')]),
 'mlwalk': dict(top="Nobody knows how much YoungLA paid Big Marlon", hl={'Big': '#58EE28', 'Marlon': '#58EE28'}, cta='*would you wear the skully?*', music=['montagem_n', 24.0],
   ctaAt=['c2', 'two'],
   tints=[[['hook', 'burberry'], G], [['hook', 'gary'], R], [['c2', 'skully', 1], G], [['c2', 'dead'], R]], rizz=[['hook', 'burberry']],
   punch=[['hook', 'professional'], ['hook', 'burberry'], ['hook', 'gary'], ['c1', 'marlon'], ['c1', 'strong'], ['c1', 'clip'], ['c2', 'marley'], ['c2', 'not'], ['c2', 'skully', 1], ['c2', 'two'], ['c2', 'dead']],
   blowouts=[['hook', 'gary']], blackFlash=[['c2']], streaks=[['c1', 'yeah'], ['c2', 'when']],
   extras=[png(['hook', 'gary'], 'e_think.png', 860, 1240), sfx(['c2', 'not'], 's_huh.mp3', 0.4), png(['c2', 'dead'], 'e_laugh.png', 230, 1240), sfx(['c2', 'thought'], 's_fahhh.mp3', 0.3)]),
}
allc = json.load(open('src/yv.cfg.json'))
for eid, c in CFG.items():
    c.update(track='none', calls=[], intro=True, hardcut=True, cutSfx='s_camflash.mp3', src=f'g67_{eid}.mp4')
    sc = {s['id']: s for s in gen[eid]}
    refs = [('tints', r) for r, _ in c['tints']] + [(k, r) for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks') for r in c[k]] + [('cta', c['ctaAt'])] + [('x', e['at']) for e in c['extras']]
    for key, r in refs:
        assert r[0] in sc, (eid, key, r)
        if len(r) == 1: continue
        ws = [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())]
        assert len(ws) > (r[2] if len(r) > 2 else 0), (eid, key, r, [w['word'] for w in sc[r[0]]['words']])
    allc[eid] = c
json.dump(allc, open('src/yv.cfg.json', 'w'), indent=1); print('cfg ok')

"""YoungLA x6 for Instagram (2026-11-20), VverPaldo (Guess.tsx) — unused moments from bvm.mp4: Johnny's aura, Lex = Disney villain,
"bald spot" photoshoot, "can I run?", "you can go home bro", Quave in pink. Hook = punchline, then the story. Crops (src t, x, zoom, y).
Run from viral-short/: python3 plan_youngla_ig.py"""
import json, os, subprocess
SRC = '../footage/youngla/bvm.mp4'
G67 = ("split[ga][gb];[gb]gblur=sigma=14[gg];[ga][gg]blend=all_mode=softlight:all_opacity=0.245,unsharp=5:5:1.74:5:5:0,"
       "eq=contrast=1.113:saturation=1.26:gamma=0.98,curves=all='0/0 0.25/0.21 0.75/0.81 1/1',unsharp=3:3:0.79,format=yuv420p")
IV, WD = (900, 1.0, 540), (960, 1.0, 540)
def P(x, z=1.15, y=540): return (x, z, y)
SHOTS = {
 'johnny': [(414, P(1000)), (418.08, WD), (420.71, P(1080)), (425.76, P(1080)), (426.68, IV), (430.1, P(1000)), (433.06, WD), (434.98, P(960)), (439.02, IV)],
 'lex': [(808, P(840)), (811.35, WD), (813.81, P(1000))],
 'bald': [(47.6, P(1200, 1.0)), (55.05, P(1360, 1.0)), (64.31, P(1280, 1.0)), (74.16, P(1280, 1.0))],
 'run': [(1012.2, IV), (1013.1, WD), (1024.36, WD), (1026.69, P(880, 1.0))],
 'home': [(675.4, P(760, 1.0)), (684.23, P(1200, 1.0))],
 'pink': [(361.0, P(960)), (364.32, IV), (368.12, P(920)), (372.91, P(1000)), (379.3, WD), (384.18, IV)],
}
CLIPS = {
 'yigjohnny': ('johnny', [('hook', 433.4, 442.55), ('c1', 414.0, 433.4), ('c2', 442.55, 445.4)]),
 'yiglex': ('lex', [('hook', 815.0, 819.05), ('c1', 808.0, 815.0), ('c2', 819.05, 824.2)]),
 'yigbald': ('bald', [('hook', 47.6, 51.7), ('c1', 51.7, 62.75), ('c2', 74.5, 77.45)]),
 'yigrun': ('run', [('hook', 1020.4, 1022.4), ('c1', 1012.2, 1020.4), ('c2', 1024.7, 1035.8)]),
 'yighome': ('home', [('hook', 677.2, 683.35), ('c1', 675.4, 677.2), ('c2', 683.35, 688.75)]),
 'yigpink': ('pink', [('hook', 372.1, 377.45), ('c1', 361.0, 372.1), ('c2', 377.45, 385.15)]),
}
FIX = {'fucking': 'f***ing', 'fucking,': 'f***ing,', 'shit,': 'sh*t,', 'ora': 'aura', 'br,': 'Bro,', 'cuevasaurus': 'Quave-asaurus', 'yx': '', 'single.': 'single'}
W = [(w['startMs'] / 1000, w['endMs'] / 1000, w['text']) for w in json.load(open('../footage/youngla/tx/bvm.words.json'))]
gen = json.load(open('src/edits.gen.json'))
for eid, (sk, plan) in CLIPS.items():
    xa, xb = min(a for _, a, _ in plan) - 0.5, max(b for _, _, b in plan) + 0.5
    out = f'public/g67_{eid}.mp4'
    if not os.path.exists(out):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(xa), '-to', str(xb), '-i', SRC, '-vf', G67, '-c:v', 'libx264', '-crf', '18',
                        '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', out], check=True)
    scenes = []
    for sid, a, b in plan:
        n = round((b - a) * 30); words = []
        for ws, we, t in W:
            if not (a - 0.05 <= ws < b - 0.05): continue
            t2 = FIX.get(t.lower(), t).strip(',.') if FIX.get(t.lower(), t) else ''
            if not t2: continue
            if t2.startswith('-') and words: words[-1]['word'] += t2; continue
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t2, 'startFrame': f0, 'endFrame': f1})
        for i in range(len(words) - 1): words[i]['endFrame'] = words[i + 1]['startFrame']
        cur = [c for t, c in SHOTS[sk] if t <= a + 0.01][-1] if any(t <= a + 0.01 for t, _ in SHOTS[sk]) else SHOTS[sk][0][1]
        cr = [(a, cur)] + [(t, c) for t, c in SHOTS[sk] if a + 0.01 < t < b - 0.2]
        scenes.append({'id': sid, 'videoStartSec': round(a - xa, 3), 'durationInFrames': n, 'cropX': 960,
                       'crops': [[max(0, round((t - a) * 30)), x, z, y] for t, (x, z, y) in cr], 'words': words})
    gen[eid] = scenes
    print(eid, round(sum(s['durationInFrames'] for s in scenes) / 30, 1), 's |', ' / '.join(' '.join(w['word'] for w in s['words']) for s in scenes))
json.dump(gen, open('src/edits.gen.json', 'w'))

def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
def ov(at, f, dur=34): return dict(at=at, kind='ov', file=f, dur=dur)
G, R = 'G', 'R'
CFG = {
 'yigjohnny': dict(top='They felt his AURA from 100 miles away', hl={'AURA': '#58EE28'}, cta='*who has the most aura?*', music=['montagem_n', 24.0], ctaAt=['c2', 'head'],
   tints=[[['hook', '100'], G], [['c1', 'pants'], R], [['c2', 'toes'], G]], rizz=[['hook', 'goosebumps']] if False else [['hook', '100']],
   punch=[['hook', '100'], ['hook', 'mid'], ['hook', 'toe'], ['c1', 'pants'], ['c1', 'face'], ['c1', 'goosebumps'], ['c2', 'head'], ['c2', 'knees']],
   blowouts=[['hook', 'toe']], blackFlash=[['c2']], streaks=[['c1']],
   extras=[png(['hook', 'mid'], 'e_laugh.png', 860, 1240), sfx(['c1', 'pants'], 's_huh.mp3'), sfx(['c2', 'knees'], 's_wow.mp3', 0.35)]),
 'yiglex': dict(top='He looks like a DISNEY VILLAIN', hl={'DISNEY': '#F40305', 'VILLAIN': '#F40305'}, cta='*hero or villain?*', music=['investigations_n', 20.0], ctaAt=['c2', 'evil'],
   tints=[[['hook', 'villain'], R], [['c2', 'evil'], R]], rizz=[['c1', 'lex']],
   punch=[['hook', 'super'], ['hook', 'disney'], ['c1', 'lex'], ['c1', 'good'], ['c2', 'antagonist'], ['c2', 'evil']],
   blowouts=[['c2', 'evil']], blackFlash=[['c2']], streaks=[['c1']],
   extras=[png(['hook', 'disney'], 'e_laugh.png', 860, 1240), sfx(['c2', 'evil'], 's_fahhh.mp3', 0.3)]),
 'yigbald': dict(top='"This flash is gonna make my BALD SPOT go crazy"', hl={'BALD': '#F40305', 'SPOT': '#F40305'}, cta='*would you get retouched?*', music=['funkabn_n', 33.2], ctaAt=['c2', 'none'],
   tints=[[['hook', 'bald'], R], [['c1', 'retoucher'], G], [['c2', 'none'], R]], rizz=[['c1', 'retoucher']],
   punch=[['hook', 'flash'], ['hook', 'bald'], ['hook', 'crazy'], ['c1', 'edit'], ['c1', 'retoucher'], ['c1', 'steam'], ['c2', 'none'], ['c2', 'shot']],
   blowouts=[['hook', 'bald']], blackFlash=[['c2']], streaks=[['c1']],
   extras=[png(['hook', 'crazy'], 'e_laugh.png', 860, 1240), sfx(['c1', 'retoucher'], 's_ding.mp3', 0.3), sfx(['c2', 'none'], 's_huh.mp3')]),
 'yigrun': dict(top='He asked if he could RUN the runway', hl={'RUN': '#F40305'}, cta='*would you run it?*', music=['empire_n', 18.8], ctaAt=['c2', 'fire'],
   tints=[[['hook', 'no'], R], [['c1', 'swag'], G], [['c2', 'fire'], R]], rizz=[['c1', 'swag']],
   punch=[['hook', 'run'], ['hook', 'no'], ['c1', 'runway'], ['c1', 'swag'], ['c2', 'practice'], ['c2', 'dare'], ['c2', 'fire']],
   blowouts=[['hook', 'no']], blackFlash=[['c2']], streaks=[['c1']],
   extras=[sfx(['hook', 'no'], 'm_record-scratch.mp3', 0.3), png(['hook', 'no'], 'e_laugh.png', 860, 1240), sfx(['c2', 'fire'], 's_huh.mp3')]),
 'yighome': dict(top='"You can go home, bro… we need 30 MORE"', hl={'30': '#F40305', 'MORE"': '#F40305'}, cta='*how many takes do YOU need?*', music=['dubist_n', 1.0], ctaAt=['c2', 'thumbnail'],
   tints=[[['hook', 'home'], R], [['hook', '30'], R]], rizz=[['c2', 'photoshop']],
   punch=[['hook', 'home'], ['hook', 'guy'], ['hook', '30'], ['c1', 'that'], ['c2', 'thumbnail'], ['c2', 'photoshop']],
   blowouts=[['hook', '30']], blackFlash=[['c2']], streaks=[['c1']],
   extras=[png(['hook', 'home'], 'e_laugh.png', 860, 1240), sfx(['hook', '30'], 's_huh.mp3')]),
 'yigpink': dict(top='It takes a LEVEL of man to rock pink', hl={'LEVEL': '#58EE28'}, cta='*could YOU pull off pink?*', music=['brevis_n', 0.0], ctaAt=['c2', 'tough'],
   tints=[[['hook', 'pink'], G], [['c1', 'bieber'], R], [['c2', 'tough'], G]], rizz=[['hook', 'level']],
   punch=[['hook', 'pink'], ['hook', 'level'], ['hook', 'man'], ['c1', 'headphones'], ['c1', 'bieber'], ['c1', '2008'], ['c2', 'chain'], ['c2', 'tough']],
   blowouts=[['hook', 'level']], blackFlash=[['c2']], streaks=[['c1']],
   extras=[png(['c1', 'bieber'], 'e_laugh.png', 860, 1240), sfx(['c1', '2008'], 's_huh.mp3'), sfx(['c2', 'tough'], 's_wow.mp3', 0.35)]),
}
allc = json.load(open('src/yv.cfg.json'))
for eid, c in CFG.items():
    c.update(track='none', calls=[], intro=True, hardcut=True, cutSfx='s_camflash.mp3', src=f'g67_{eid}.mp4')
    sc = {s['id']: s for s in gen[eid]}
    refs = [r for r, _ in c['tints']] + [r for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks') for r in c[k]] + [c['ctaAt']] + [e['at'] for e in c['extras']]
    for r in refs:
        if len(r) == 1: continue
        ws = [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())]
        assert ws, (eid, r, [w['word'] for w in sc[r[0]]['words']])
    allc[eid] = c
json.dump(allc, open('src/yv.cfg.json', 'w'), indent=1); print('cfg ok')

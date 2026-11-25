"""Trevor x Grant x Buggsy stream — re-edits (2026-11-25, user: 'make more videos of trevor'; every tracker row already used) with NEW hooks/songs:
tvgoat2 (Dellavedova), tvneck2 (Davis Mills neck roast), tvcelly2 (PSA 10-10 celly). Original VverPaldo + meme SFX/emojis."""
import json, os, subprocess
SRC = '../footage/src'
G67 = ("split[ga][gb];[gb]gblur=sigma=14[gg];[ga][gg]blend=all_mode=softlight:all_opacity=0.245,unsharp=5:5:1.74:5:5:0,"
       "eq=contrast=1.113:saturation=1.26:gamma=0.98,curves=all='0/0 0.25/0.21 0.75/0.81 1/1',unsharp=3:3:0.79,format=yuv420p")
T, GR_, BG, W = (1000, 1.6, 450), (420, 1.6, 450), (1500, 1.6, 450), (960, 1.0, 540)
TN, GS = (1000, 1.6, 500), (380, 1.4, 380)
T, W = (960, 1.6, 510), (960, 1.0, 540)
TT, TL, L, R = (960, 1.8, 465), (715, 1.15, 450), (470, 1.6, 440), (1500, 1.6, 440)
TN, NW, NG = (1000, 1.6, 470), (960, 1.15, 520), (640, 1.35, 430)
EDITS = {
 'tvgoat2': ('nba_goat', (0, 18.8), {'del': 'Dellavedova', 'vadova.': ''}, [
     ('hook', 13.15, 15.45, [(13.15, TT)]),
     ('c1', 0.00, 7.20, [(0.00, TL), (4.40, T)]),
     ('c2', 8.00, 13.10, [(8.00, T), (11.2, TT)]),
     ('c3', 15.45, 18.80, [(15.45, W), (17.0, TT)])]),
 'tvneck2': ('davis', (0, 16.8), {'nashaun,': 'Nashaun,'}, [
     ('hook', 5.85, 11.95, [(5.85, NG), (7.10, TN), (8.85, NW), (11.10, TN)]),
     ('c1', 0.00, 5.80, [(0.00, NW), (3.50, NG)]),
     ('c2', 11.95, 16.75, [(11.95, TN), (14.20, NW)])]),
 'tvcelly2': ('celly', (0, 33.2), {'selly': 'celly', 'tuddy.': 'tuddy'}, [
     ('hook', 26.25, 28.75, [(26.25, L), (27.50, TL)]),
     ('c1', 3.85, 9.45, [(3.85, L), (6.70, T), (8.40, TT)]),
     ('c2', 12.85, 15.40, [(12.85, TT)]),
     ('c3', 19.55, 26.20, [(19.55, L), (23.80, TL)]),
     ('c4', 28.85, 32.40, [(28.85, T), (30.10, TL), (31.80, TT)])]),

 'tvteal2': ('teal', (0, 225.1), {'homes': 'Mahomes', 'slob': 'slab', 'slap': 'slab', 'slobs': 'slabs'}, [
     ('hook', 214.85, 221.05, [(214.85, (960, 1.8, 640)), (217.80, (960, 2.1, 640))]),
     ('c1', 172.25, 177.15, [(172.25, (960, 1.8, 250)), (175.20, (960, 1.8, 640))]),
     ('c2', 206.40, 211.85, [(206.40, (960, 1.8, 640))]),
     ('c3', 221.05, 224.30, [(221.05, (960, 1.8, 250)), (222.50, (960, 2.1, 640))])]),
}
PAD = {'teal'}
gen = json.load(open('src/edits.gen.json'))
for eid, (src, (xa, xb), fix, plan) in EDITS.items():
    out = f'public/g67_{eid}.mp4'
    if not os.path.exists(out):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(xa), '-to', str(xb), '-i', f'{SRC}/{src}.mp4', '-vf', ('scale=608:1080:flags=lanczos,pad=1920:1080:656:0:black,' if src in PAD else '') + G67, '-c:v', 'libx264', '-crf', '17',
                        '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', out], check=True)
    Wd = json.load(open(f'{SRC}/{src}.words.json'))
    scenes = []
    for sid, a, b, crops in plan:
        n = round((b - a) * 30); words = []
        for w in Wd:
            ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
            if not (a - 0.05 <= ws < b - 0.05): continue
            t2 = fix.get(t.lower(), t)
            if not t2: continue
            if words and (t2.startswith('-') or (t2[:1] == ',' and t2[1:2].isdigit())): words[-1]['word'] += t2.rstrip('.'); continue
            t2 = t2.strip(',.') if not t2.endswith('?') else t2
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t2, 'startFrame': f0, 'endFrame': f1})
        for i in range(len(words) - 1): words[i]['endFrame'] = max(words[i]['endFrame'], words[i + 1]['startFrame'])
        scenes.append({'id': sid, 'videoStartSec': round(a - xa, 3), 'durationInFrames': n, 'cropX': 960,
                       'crops': [[max(0, round((t - a) * 30)), x, z, y] for t, (x, z, y) in crops], 'words': words})
    gen[eid] = scenes
    print(eid, round(sum(s['durationInFrames'] for s in scenes) / 30, 1), 's |', ' / '.join(s['id'] + ': ' + ' '.join(w['word'] for w in s['words']) for s in scenes))
json.dump(gen, open('src/edits.gen.json', 'w'))

def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
def ov(at, f, dur=34): return dict(at=at, kind='ov', file=f, dur=dur)
G, R = 'G', 'R'
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
def ov(at, f, dur=34): return dict(at=at, kind='ov', file=f, dur=dur)
G, R = 'G', 'R'
CFG = {
 'tvteal2': dict(top="He called Trevor Lawrence the pride and joy of the NFL", hl={'NFL': '#58EE28'}, cta='*is Trevor the best QB in the league?*', music=['blue_n', 21.5], ctaAt=['c2', 'Mendoza'],
   tints=[[['hook', 'greatest'], G], [['c1', 'lose'], R], [['c3', 'NFL'], G]], rizz=[['hook', 'greatest']],
   punch=[['hook', 'teal'], ['hook', 'greatest'], ['hook', 'quarterback'], ['hook', 'pride'], ['hook', 'NFL'], ['c1', 'Mahomes'], ['c1', 'Brady'], ['c1', 'lose'], ['c2', 'crazy'], ['c3', 'NFL'], ['c3', 'card']],
   blowouts=[['hook', 'pride']], blackFlash=[['c3']], streaks=[['c2']],
   extras=[png(['hook', 'greatest'], 'emoji/1f525.png'), sfx(['hook', 'NFL'], 's_wow.mp3', 0.35), sfx(['c1', 'lose'], 's_huh.mp3', 0.35), png(['c1', 'lose'], 'emoji/1f633.png', 230, 1240),
           sfx(['c3', 'NFL'], 'm_mg-boom.mp3', 0.4), png(['c3', 'card'], 'emoji/1f451.png')]),
 'tvgoat2': dict(top="Asked an NFL QB for his NBA GOAT… he said THIS", hl={'THIS': '#FF2A2A'}, cta='*who is YOUR NBA goat?*', music=['dubist_n', 1.0], ctaAt=['c3', 'tension'],
   tints=[[['hook', 'Dellavedova'], G], [['c3', 'tension'], R]], rizz=[['hook', 'Dellavedova']],
   punch=[['hook', 'Gotta'], ['hook', 'Dellavedova'], ['hook', 'no'], ['c1', 'NBA'], ['c1', 'goat'], ['c1', 'Greatest'], ['c3', 'feel'], ['c3', 'tension']],
   blowouts=[['hook', 'Dellavedova']], blackFlash=[['c3']], streaks=[['c1', 'Greatest']],
   extras=[sfx(['hook', 'Dellavedova'], 's_huh.mp3', 0.45), png(['hook', 'Dellavedova'], 'emoji/1f602.png'), png(['c1', 'goat'], 'emoji/1f914.png', 230, 1240), sfx(['c3', 'tension'], 'm_mg-boom.mp3', 0.4), png(['c3', 'tension'], 'emoji/1f480.png')]),
 'tvneck2': dict(top="When the card you pull gets ROASTED live", hl={'ROASTED': '#FF2A2A'}, cta='*was that too far?*', music=['funkabn_n', 0.5], ctaAt=['c2', 'you'],
   tints=[[['hook', 'Ew'], R], [['hook', 'neck'], G]], rizz=[['hook', 'neck']],
   punch=[['hook', 'Davis'], ['hook', 'Ew'], ['hook', 'longer'], ['hook', 'neck'], ['hook', 'Glennon'], ['hook', 'Trevor'], ['c1', 'Red'], ['c1', 'Adam'], ['c2', 'guys']],
   blowouts=[['hook', 'Ew']], blackFlash=[['c2']], streaks=[['c1', 'here']],
   extras=[sfx(['hook', 'Ew'], 'm_record-scratch.mp3', 0.4), sfx(['hook', 'neck'], 'm_mg-boom.mp3', 0.45), png(['hook', 'neck'], 'emoji/1f480.png'), png(['c2', 'guys'], 'emoji/1f602.png', 230, 1240)]),
 'tvcelly2': dict(top="They invented Trevor's next touchdown celly", hl={'celly': '#58EE28'}, cta='*would you do this celly?*', music=['montagem_n', 24.0], ctaAt=['c3', 'collectors'],
   tints=[[['hook', '10'], G], [['c2', 'dance'], R], [['c4', 'No'], R]], rizz=[['hook', '10']],
   punch=[['hook', 'point'], ['hook', '10'], ['hook', 'easy'], ['c1', 'celly'], ['c1', 'touchdown'], ['c1', 'Maybe'], ['c2', 'choreographed'], ['c2', 'dance'], ['c3', 'PSA'], ['c3', 'best'], ['c4', 'like'], ['c4', 'No']],
   blowouts=[['c4', 'No']], blackFlash=[['c2']], streaks=[['c3']],
   extras=[png(['hook', '10'], 'emoji/1f525.png'), sfx(['c2', 'dance'], 's_huh.mp3', 0.4), png(['c2', 'dance'], 'emoji/1f602.png', 230, 1240), sfx(['c4', 'No'], 'm_oh-hell-nah.mp3', 0.45), png(['c4', 'No'], 'emoji/1f480.png')]),
}
allc = json.load(open('src/yv.cfg.json'))
for eid, c in CFG.items():
    c.update(track='none', calls=[], intro=True, hardcut=True, cutSfx='s_camflash.mp3', src=f'g67_{eid}.mp4')
    sc = {s['id']: s for s in gen[eid]}
    refs = [r for r, _ in c['tints']] + [r for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks') for r in c[k]] + [c['ctaAt']] + [e['at'] for e in c['extras']]
    for r in refs:
        if len(r) == 1: continue
        ws = [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())]
        assert len(ws) > (r[2] if len(r) > 2 else 0), (eid, r, [w['word'] for w in sc[r[0]]['words']])
    allc[eid] = c
json.dump(allc, open('src/yv.cfg.json', 'w'), indent=1); print('cfg ok')

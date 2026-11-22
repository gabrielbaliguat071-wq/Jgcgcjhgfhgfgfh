"""Trevor x Grant x Buggsy stream - 3 more fresh moments (2026-11-22), VverPaldo (Guess.tsx).
tvtells: coverage tells, "looks like that guy's wide open... it's because of a motion" (u6_coen 66-109); tvpen: Peyton Manning told him
a nice signature is a big deal (t1 20-40); tvworth: 1-of-1 Clemson ~$2,000 vs 1-of-1 NFL up to a million (t4 0-7 + 70-82)."""
import json, os, subprocess
SRC = '../footage/src'
G67 = ("split[ga][gb];[gb]gblur=sigma=14[gg];[ga][gg]blend=all_mode=softlight:all_opacity=0.245,unsharp=5:5:1.74:5:5:0,"
       "eq=contrast=1.113:saturation=1.26:gamma=0.98,curves=all='0/0 0.25/0.21 0.75/0.81 1/1',unsharp=3:3:0.79,format=yuv420p")
T, GR_, BG, W = (1000, 1.6, 450), (420, 1.6, 450), (1500, 1.6, 450), (960, 1.0, 540)
TN, GS = (1000, 1.6, 500), (380, 1.4, 380)
T, W = (960, 1.6, 510), (960, 1.0, 540)
TT, TL, L = (960, 1.8, 465), (715, 1.15, 450), (470, 1.5, 415)
EDITS = {
 'tvtells': ('u6_coen_duo', (64, 110), {'lineback': 'linebacker', 'covered': 'cover', 'through.': '3.', 'three.': '3.'}, [
     ('hook', 76.48, 77.70, [(76.48, TT)]),
     ('c1', 66.46, 70.62, [(66.46, T)]),
     ('c2', 74.44, 76.44, [(74.44, W)]),
     ('c3', 77.74, 91.10, [(77.74, T), (82.0, TT), (86.9, W), (89.2, TT)]),
     ('c4', 100.95, 108.95, [(100.95, T), (106.6, TT)])]),
 'tvpen': ('t1_tiger_auto_pen', (19, 42.4), {'goaded': 'goated', 'once.': 'once?'}, [
     ('hook', 36.74, 39.50, [(36.74, TT)]),
     ('c1', 20.50, 27.40, [(20.50, TL), (24.1, W)]),
     ('c2', 27.80, 36.72, [(27.80, T), (30.9, TT), (33.3, T)])]),
 'tvworth': ('t4_natty_ticket', (0, 83), {'-on': '-of'}, [
     ('hook', 75.66, 81.66, [(75.66, L), (81.30, T)]),
     ('c1', 0.66, 6.86, [(0.66, TL), (3.9, T)]),
     ('c2', 70.02, 75.62, [(70.02, L), (72.6, TL)])]),
}
gen = json.load(open('src/edits.gen.json'))
for eid, (src, (xa, xb), fix, plan) in EDITS.items():
    out = f'public/g67_{eid}.mp4'
    if not os.path.exists(out):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(xa), '-to', str(xb), '-i', f'{SRC}/{src}.mp4', '-vf', G67, '-c:v', 'libx264', '-crf', '17',
                        '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', out], check=True)
    Wd = json.load(open(f'../src/plans/data/{src}.words.json'))
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
CFG = {
 'tvtells': dict(top="How an NFL QB knows who's open BEFORE the snap", hl={'BEFORE': '#58EE28'}, cta='*could you read this?*', music=['phonk_n', 22.4], ctaAt=['c4', 'huddle'],
   tints=[[['hook', 'wide'], G], [['c1', 'coverage'], G], [['c3', 'immediately'], G], [['c4', 'seam'], G]], rizz=[['c4', 'seam']],
   punch=[['hook', 'wide'], ['hook', 'open'], ['c1', 'coverages'], ['c1', 'tells'], ['c3', 'motion'], ['c3', 'formation'], ['c3', 'show'], ['c3', 'immediately'], ['c4', 'right'], ['c4', 'cover'], ['c4', 'seam']],
   blowouts=[['c3', 'immediately']], blackFlash=[['c3']], streaks=[['c4']],
   extras=[png(['hook', 'open'], 'e_think.png', 860, 1240), sfx(['c3', 'immediately'], 's_wow.mp3', 0.35), png(['c4', 'seam'], 'e_laugh.png', 230, 1240), sfx(['c4', 'seam'], 's_ding.mp3', 0.3)]),
 'tvpen': dict(top='Peyton Manning CALLED him about his autograph', hl={'CALLED': '#58EE28'}, cta='*is your signature goated?*', music=['blue_n', 21.5], ctaAt=['c2', 'mentioned'],
   tints=[[['hook', 'big'], G], [['c1', 'goated'], G], [['c2', 'peyton'], G]], rizz=[['c1', 'goated']],
   punch=[['hook', 'big'], ['hook', 'nice'], ['hook', 'signature'], ['c1', 'consistent'], ['c1', 'beautiful'], ['c1', 'goated'], ['c2', 'told'], ['c2', 'peyton'], ['c2', 'manning'], ['c2', 'called']],
   blowouts=[['c2', 'peyton']], blackFlash=[['c2']], streaks=[['c1', 'every']],
   extras=[png(['c1', 'goated'], 'e_laugh.png', 860, 1240), sfx(['c2', 'peyton'], 's_wow.mp3', 0.35), png(['hook', 'signature'], 'e_heart.png', 860, 1240)]),
 'tvworth': dict(top='Why his COLLEGE 1 of 1 is worth way LESS', hl={'COLLEGE': '#58EE28', 'LESS': '#F40305'}, cta='*would you rather have which?*', music=['funkabn_n', 33.2], ctaAt=['c2', 'hobby'],
   tints=[[['hook', '$2'], R], [['hook', 'million'], G], [['c1', '20'], G]], rizz=[['hook', 'million']],
   punch=[['hook', '$2'], ['hook', 'potentially'], ['hook', 'million'], ['c1', 'unbelievable'], ['c1', '10'], ['c1', '20'], ['c1', 'works'], ['c2', 'hobby'], ['c2', 'nfl'], ['c2', 'clemson']],
   blowouts=[['hook', 'million']], blackFlash=[['c2']], streaks=[['c1', 'works']],
   extras=[sfx(['hook', 'million'], 's_money.mp3', 0.4), ov(['hook', 'million'], 'cashfall.mp4', 45), png(['hook', 'wow'], 'e_think.png', 860, 1240), sfx(['c1', '20'], 's_ding.mp3', 0.3)]),
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

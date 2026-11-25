"""Trevor batch 12 (2026-11-25, user: 'make a really interesting hook'): tvjesus (dream golf foursome → Jesus), tvwhacked (superfans 'whacked'), tvant2 ('auto looks like an ant'). New style: blurBg + reaction cutouts over the OTHER person."""
import json, os, subprocess
SRC = '../footage/src'
G67 = ("split[ga][gb];[gb]gblur=sigma=14[gg];[ga][gg]blend=all_mode=softlight:all_opacity=0.245,unsharp=5:5:1.74:5:5:0,"
       "eq=contrast=1.113:saturation=1.26:gamma=0.98,curves=all='0/0 0.25/0.21 0.75/0.81 1/1',unsharp=3:3:0.79,format=yuv420p")
T, GR_, BG, W = (1000, 1.6, 450), (420, 1.6, 450), (1500, 1.6, 450), (960, 1.0, 540)
TN, GS = (1000, 1.6, 500), (380, 1.4, 380)
T, W = (960, 1.6, 510), (960, 1.0, 540)
TT, TL, L, R = (960, 1.8, 465), (715, 1.15, 450), (470, 1.6, 440), (1500, 1.6, 440)
TN, NW, NG = (1000, 1.6, 470), (960, 1.15, 520), (640, 1.35, 430)
L1, T1, TT1 = (390, 1.6, 444), (990, 1.6, 470), (990, 1.85, 440)
T3, TT3, L3 = (1020, 1.6, 470), (1020, 1.85, 440), (450, 1.6, 450)
EDITS = {
 'tvjesus': ('t2_dream_golf_four', (8, 58), {'for': 'foursome', 'some': ''}, [
     ('hook', 32.15, 36.75, [(32.15, TT), (34.70, TL)]),
     ('c1', 11.25, 13.75, [(11.25, TL)]),
     ('c2', 16.85, 24.50, [(16.85, L), (20.50, TL), (23.30, T)]),
     ('c3', 26.45, 28.30, [(26.45, TT)]),
     ('c4', 45.45, 54.30, [(45.45, T), (49.00, TT), (52.70, T)])]),
 'tvwhacked': ('t3_traveling_trevors', (56, 100), {'trevers': 'Trevors', 'i': 'I', 'instagram': 'Instagram'}, [
     ('hook', 78.55, 83.40, [(78.55, T3), (81.40, TT3)]),
     ('c1', 58.10, 63.00, [(58.10, L3), (60.30, TL)]),
     ('c2', 64.30, 71.60, [(64.30, T3), (68.00, TT3)]),
     ('c3', 91.70, 98.20, [(91.70, T3), (94.80, TT3)])]),
 'tvant2': ('t1_tiger_auto_pen', (0, 30), {'goaded': 'goated'}, [
     ('hook', 14.95, 20.00, [(14.95, L1), (17.60, (690, 1.15, 440))]),
     ('c1', 9.25, 14.90, [(9.25, L1), (14.60, T1)]),
     ('c2', 20.45, 27.20, [(20.45, L1), (24.10, (690, 1.15, 440)), (25.50, TT1)]),
     ('c3', 5.05, 8.65, [(5.05, T1), (6.70, TT1)])]),
}
PAD = set()
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
            if words and t2.startswith('.') and t2[1:2].isdigit(): words[-1]['word'] += t2; continue
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
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
def ov(at, f, dur=34): return dict(at=at, kind='ov', file=f, dur=dur)
G, R = 'G', 'R'
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
def ov(at, f, dur=34): return dict(at=at, kind='ov', file=f, dur=dur)
G, R = 'G', 'R'
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
def ov(at, f, dur=34): return dict(at=at, kind='ov', file=f, dur=dur)
G, R = 'G', 'R'
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
def ov(at, f, dur=34): return dict(at=at, kind='ov', file=f, dur=dur)
G, R = 'G', 'R'
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
def ov(at, f, dur=34): return dict(at=at, kind='ov', file=f, dur=dur)
G, R = 'G', 'R'
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
def ov(at, f, dur=34): return dict(at=at, kind='ov', file=f, dur=dur)
G, R = 'G', 'R'
CFG = {
 'tvjesus': dict(top="Trevor Lawrence's dream golf foursome includes… JESUS", hl={'JESUS': '#58EE28'}, cta='*who is in YOUR dream foursome?*', music=['dubist_n', 1.0], ctaAt=['c4', 'Tiger'],
   tints=[[['hook', 'Jesus'], G], [['c4', 'goat'], G]], rizz=[['hook', 'Jesus']],
   punch=[['hook', 'throw'], ['hook', 'Jesus'], ['hook', 'unbelievable'], ['c1', 'dream'], ['c2', 'humans'], ['c2', 'anybody'], ['c2', 'artist'], ['c3', 'week'], ['c4', 'Tiger'], ['c4', 'goat'], ['c4', 'sick']],
   blowouts=[['hook', 'Jesus']], blackFlash=[['c3']], streaks=[['c4']],
   extras=[png(['hook', 'Jesus'], 'react/golf_host.png', 540, 1230, 640), sfx(['hook', 'Jesus'], 's_huh.mp3', 0.4), png(['c2', 'humans'], 'react/golf_trevor.png', 540, 1230, 640),
           sfx(['c3', 'week'], 'm_record-scratch.mp3', 0.35), png(['c3', 'week'], 'emoji/1f602.png'), sfx(['c4', 'goat'], 's_wow.mp3', 0.35), png(['c4', 'goat'], 'emoji/1f410.png', 230, 1240)]),
 'tvwhacked': dict(top='Trevor Lawrence met his biggest superfans… and called them WHACKED', hl={'WHACKED': '#FF2A2A'}, cta='*would you join the Traveling Trevors?*', music=['funkabn_n', 0.5], ctaAt=['c3', 'funny'],
   tints=[[['hook', 'whacked'], R], [['c2', 'algorithm'], G], [['c3', 'funny'], G]], rizz=[['c2', 'algorithm']],
   punch=[['hook', 'first'], ['hook', 'think'], ['hook', 'dude'], ['hook', 'whacked'], ['c1', 'biggest'], ['c1', 'Trevors'], ['c2', 'follow'], ['c2', 'algorithm'], ['c3', 'second'], ['c3', 'obviously'], ['c3', 'funny']],
   blowouts=[['hook', 'whacked']], blackFlash=[['c2']], streaks=[['c3']],
   extras=[png(['hook', 'whacked'], 'react/fans_host.png', 540, 1230, 640), sfx(['hook', 'whacked'], 'm_mg-boom.mp3', 0.45), png(['c1', 'Trevors'], 'react/fans_trevor.png', 540, 1230, 640),
           png(['c2', 'algorithm'], 'emoji/1f440.png'), sfx(['c3', 'funny'], 's_ding.mp3', 0.3), png(['c3', 'funny'], 'emoji/1f602.png', 230, 1240)]),
 'tvant2': dict(top="They said this NFL QB's autograph looks like an ANT", hl={'ANT': '#FF2A2A'}, cta='*whose autograph is the worst?*', music=['phonk_n', 22.4], ctaAt=['c2', 'goated'],
   tints=[[['hook', 'ant'], R], [['c1', 'respect'], R], [['c2', 'goated'], G]], rizz=[['c2', 'goated']],
   punch=[['hook', 'auto'], ['hook', 'ant'], ['hook', 'big'], ['hook', 'respect'], ['c1', 'respect'], ['c1', 'Anthony'], ['c1', 'disrespect'], ['c2', 'consistent'], ['c2', 'beautiful'], ['c2', 'goated'], ['c3', 'signature']],
   blowouts=[['hook', 'ant']], blackFlash=[['c2']], streaks=[['c1', 'Like']],
   extras=[png(['hook', 'ant'], 'react/ant_trevor.png', 540, 1230, 640), sfx(['hook', 'ant'], 's_huh.mp3', 0.45), sfx(['c1', 'disrespect'], 'm_record-scratch.mp3', 0.35), png(['c1', 'disrespect'], 'emoji/1f480.png'),
           sfx(['c2', 'goated'], 'm_anime-wow.mp3', 0.35), png(['c2', 'goated'], 'emoji/1f410.png', 230, 1240)]),
}
allc = json.load(open('src/yv.cfg.json'))
for eid, c in CFG.items():
    c.update(track='none', calls=[], intro=True, hardcut=True, cutSfx='s_camflash.mp3', src=f'g67_{eid}.mp4', blurBg=True)
    sc = {s['id']: s for s in gen[eid]}
    refs = [r for r, _ in c['tints']] + [r for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks') for r in c[k]] + [c['ctaAt']] + [e['at'] for e in c['extras']]
    for r in refs:
        if len(r) == 1: continue
        ws = [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())]
        assert len(ws) > (r[2] if len(r) > 2 else 0), (eid, r, [w['word'] for w in sc[r[0]]['words']])
    allc[eid] = c
json.dump(allc, open('src/yv.cfg.json', 'w'), indent=1); print('cfg ok')

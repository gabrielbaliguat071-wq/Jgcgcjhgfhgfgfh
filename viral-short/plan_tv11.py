"""Trevor re-edits batch 11 (2026-11-25) in the NEW reference style (YT O6yC7hsTXnA): VverPaldo + blurred video background (cfg blurBg) + real reaction
cutouts from the stream (rembg, public/res/react/*.png) popping over the box. All > 15 s."""
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
 'tvjosh3': ('t5_ex_teammate', (0, 26.1), {'heinz': 'Hines-Allen', 'allen.': '', 'allen': ''}, [
     ('hook', 19.05, 26.05, [(19.05, TN), (22.30, (1000, 1.9, 450))]),
     ('c1', 1.65, 12.50, [(1.65, NW), (5.40, TN), (8.20, NW), (11.50, TN)]),
     ('c2', 12.55, 19.00, [(12.55, TN), (16.10, NW)])]),
 'tvtiger3': ('tiger_slab', (0, 32.5), {'pc': 'collection', '-5': '.5'}, [
     ('hook', 24.05, 27.75, [(24.05, TL), (26.10, TT)]),
     ('c1', 2.55, 11.10, [(2.55, L), (6.40, W), (9.00, L)]),
     ('c2', 17.95, 23.10, [(17.95, L), (20.20, TL), (22.90, TT)]),
     ('c3', 28.75, 31.45, [(28.75, TT)])]),
 'tvticket3': ('t4_natty_ticket', (9, 42), {}, [
     ('hook', 29.35, 33.30, [(29.35, TL), (31.85, TT)]),
     ('c1', 9.75, 17.30, [(9.75, L), (14.40, TL)]),
     ('c2', 21.45, 29.30, [(21.45, L), (25.50, TT), (27.20, TL)]),
     ('c3', 37.35, 41.20, [(37.35, L), (39.50, TL)])]),
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
CFG = {
 'tvjosh3': dict(top="Pulling your teammate's card from BEFORE he changed his name", hl={'BEFORE': '#FF2A2A'}, cta='*would you keep this card?*', music=['funkabn_n', 0.5], ctaAt=['c2', 'rookie'],
   tints=[[['hook', 'real'], G], [['c1', 'gold'], G], [['c2', 'fire'], G]], rizz=[['c1', 'gold']],
   punch=[['hook', 'rookie'], ['hook', 'real'], ['hook', 'Hines-Allen'], ['hook', 'changed'], ['hook', 'name'], ['c1', 'gold'], ['c1', 'teal'], ['c1', 'glove'], ['c2', 'Josh'], ['c2', 'fire'], ['c2', 'rookie']],
   blowouts=[['hook', 'changed']], blackFlash=[['c2']], streaks=[['c1', 'No']],
   extras=[png(['hook', 'changed'], 'react/t4_grant.png', 540, 1230, 640), sfx(['hook', 'name'], 'm_anime-wow.mp3', 0.4), sfx(['c1', 'glove'], 's_huh.mp3', 0.35), png(['c1', 'glove'], 'emoji/1f602.png'),
           sfx(['c2', 'fire'], 'm_mg-boom.mp3', 0.4), png(['c2', 'fire'], 'emoji/1f525.png', 230, 1240)]),
 'tvtiger3': dict(top='Gifting an NFL QB a TIGER WOODS game-worn auto', hl={'TIGER': '#58EE28', 'WOODS': '#58EE28'}, cta='*best gift ever?*', music=['brevis_n', 36.0], ctaAt=['c2', 'shirt'],
   tints=[[['hook', 'me'], G], [['c1', 'Tiger'], G], [['c2', 'Wow'], G]], rizz=[['c1', 'Tiger']],
   punch=[['hook', 'care'], ['hook', 'package'], ['hook', 'me'], ['c1', 'four'], ['c1', 'exquisite'], ['c1', 'Tiger'], ['c1', 'Patch'], ['c1', '9.5'], ['c2', 'shirt'], ['c2', 'glove'], ['c2', 'cap'], ['c2', 'Wow'], ['c3', 'awesome']],
   blowouts=[['hook', 'me']], blackFlash=[['c2']], streaks=[['c1', 'This']],
   extras=[png(['hook', 'me'], 'emoji/1f633.png'), png(['c1', 'exquisite'], 'react/tiger_forme.png', 540, 1230, 640), sfx(['hook', 'me'], 'm_anime-wow.mp3', 0.4), png(['c1', 'Patch'], 'emoji/1f525.png', 230, 1240), sfx(['c1', '9.5'], 's_ding.mp3', 0.3),
           sfx(['c2', 'Wow'], 's_wow.mp3', 0.35), png(['c2', 'Wow'], 'emoji/1f525.png')]),
 'tvticket3': dict(top='He gave Trevor Lawrence a gift… of HIMSELF', hl={'HIMSELF': '#FF2A2A'}, cta='*would you gift him this?*', music=['montagem_n', 24.0], ctaAt=['c2', 'Clemson'],
   tints=[[['hook', 'thank'], G], [['c1', 'weird'], R], [['c2', 'MVP'], G]], rizz=[['c2', 'MVP']],
   punch=[['hook', 'sweet'], ['hook', 'give'], ['hook', 'me'], ['hook', 'thank'], ['c1', 'gift'], ['c1', 'weird'], ['c1', 'gifting'], ['c2', 'signed'], ['c2', 'national'], ['c2', 'MVP'], ['c2', 'Clemson'], ['c3', 'gifting'], ['c3', 'auto']],
   blowouts=[['c1', 'gifting']], blackFlash=[['c2']], streaks=[['c3']],
   extras=[png(['hook', 'thank'], 'emoji/1f979.png'), png(['c1', 'gifting'], 'react/t4_thanks.png', 540, 1230, 640), png(['c2', 'national'], 'react/t4_grant.png', 540, 1230, 640), sfx(['c1', 'gifting'], 's_huh.mp3', 0.4),
           sfx(['c2', 'MVP'], 'm_anime-wow.mp3', 0.35), png(['c2', 'MVP'], 'emoji/1f525.png'), sfx(['c3', 'auto'], 'm_mg-boom.mp3', 0.35), png(['c3', 'auto'], 'emoji/1f602.png', 230, 1240)]),
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

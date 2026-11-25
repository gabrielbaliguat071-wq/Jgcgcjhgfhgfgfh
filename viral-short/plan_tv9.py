"""Trevor x Grant x Buggsy stream - batch tv9 (2026-11-22), VverPaldo (Guess.tsx).
tvplate: college didn't prepare him - defensive recognition, everything on the QB's plate (u6_coen 28-66);
tvnapkin: a nice patch = $15,000+, a plain one "is like a napkin" (nt_rip 0-14);
tvsign: Rod Woodson redemption - "I don't think Trevor's a redemption. No, you sign" -> true RPA gold (nt_rip 87-104)."""
import json, os, subprocess
SRC = '../footage/src'
G67 = ("split[ga][gb];[gb]gblur=sigma=14[gg];[ga][gg]blend=all_mode=softlight:all_opacity=0.245,unsharp=5:5:1.74:5:5:0,"
       "eq=contrast=1.113:saturation=1.26:gamma=0.98,curves=all='0/0 0.25/0.21 0.75/0.81 1/1',unsharp=3:3:0.79,format=yuv420p")
T, GR_, BG, W = (1000, 1.6, 450), (420, 1.6, 450), (1500, 1.6, 450), (960, 1.0, 540)
TN, GS = (1000, 1.6, 500), (380, 1.4, 380)
T, W = (960, 1.6, 510), (960, 1.0, 540)
TT, TL = (960, 1.8, 465), (715, 1.15, 450)
TN, NW, NG, NC = (1000, 1.6, 470), (960, 1.15, 520), (640, 1.35, 430), (980, 1.3, 545)
EDITS = {
 'tvplate': ('u6_coen_duo', (27, 67), {'recognition': 'recognition', 'me.': 'me'}, [
     ('hook', 27.84, 30.40, [(27.84, TT)]),
     ('c1', 30.62, 43.20, [(30.62, T), (34.2, TT), (39.0, W)]),
     ('c2', 43.90, 53.80, [(43.90, T), (47.8, TT), (51.0, T)]),
     ('c3', 58.98, 66.30, [(58.98, W), (62.3, TT)])]),
 'tvnapkin': ('nt_rip', (0, 21), {'jaguar\'s': "Jaguar's"}, [
     ('hook', 8.16, 9.70, [(8.16, NC)]),
     ('c1', 0.00, 8.10, [(0.00, NG), (3.84, NW), (6.9, TN)]),
     ('c2', 9.78, 14.30, [(9.78, NC), (12.8, NW)]),
     ('c3', 15.50, 20.10, [(15.50, NW), (18.0, TN)])]),
 'tvsign': ('nt_rip', (86, 111), {'chubba.': ''}, [
     ('hook', 92.30, 95.40, [(92.30, NC), (93.38, NW), (94.80, TN)]),
     ('c1', 87.02, 93.30, [(87.02, NW), (91.3, NC)]),
     ('c2', 95.46, 98.40, [(95.46, NC), (97.0, TN)]),
     ('c3', 103.14, 110.70, [(103.14, NW), (106.20, TN)])]),
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
 'tvplate': dict(top='College football did NOT prepare him for this', hl={'NOT': '#F40305'}, cta='*is the NFL jump that big?*', music=['empire_n', 18.8], ctaAt=['c3', 'layer'],
   tints=[[['hook', 'different'], R], [['c1', 'recognition'], G], [['c2', 'plate'], R], [['c3', 'diagnose'], G]], rizz=[['c2', 'plate']],
   punch=[['hook', 'college'], ['hook', 'world'], ['c1', 'ton'], ['c1', 'recognition'], ['c1', 'protections'], ['c1', 'successful'], ['c2', 'plate'], ['c2', 'multiple'], ['c2', 'huddle'], ['c2', 'protection'], ['c3', 'whole'], ['c3', 'diagnose']],
   blowouts=[['c2', 'plate']], blackFlash=[['c2']], streaks=[['c3']],
   extras=[png(['hook', 'world'], 'e_think.png', 860, 1240), sfx(['c2', 'plate'], 's_huh.mp3', 0.4), sfx(['c3', 'diagnose'], 's_wow.mp3', 0.35)]),
 'tvnapkin': dict(top="Why one patch is worth $15,000 and the other is a NAPKIN", hl={'$15,000': '#58EE28', 'NAPKIN': '#F40305'}, cta='*would you know the difference?*', music=['montagem_n', 24.0], ctaAt=['c2', 'nicer'],
   tints=[[['hook', 'napkin'], R], [['c1', '15'], G], [['c2', 'nicer'], G]], rizz=[['c1', '15']],
   punch=[['hook', 'napkin'], ['c1', 'nice'], ['c1', '15'], ['c1', 'jaguar'], ['c1', 'face'], ['c2', 'two'], ['c2', 'nicer'], ['c2', 'covers'], ['c2', 'swoosh'], ['c3', 'risk'], ['c3', 'hands']],
   blowouts=[['c1', '15']], blackFlash=[['c2']], streaks=[['c1', 'like']],
   extras=[png(['hook', 'napkin'], 'e_laugh.png', 860, 1240), sfx(['hook', 'napkin'], 's_huh.mp3', 0.4), sfx(['c1', '15'], 's_money.mp3', 0.35), sfx(['c2', 'swoosh'], 's_ding.mp3', 0.3)]),
 'tvsign': dict(top="Trevor is NOT a redemption guy… here's why", hl={'NOT': '#F40305'}, cta='*should redemptions be banned?*', music=['phonk_n', 22.4], ctaAt=['c3', 'chase'],
   tints=[[['hook', 'redemption'], R], [['c1', 'woodson'], G], [['c2', 'gold'], G]], rizz=[['c2', 'gold']],
   punch=[['hook', 'trevor'], ['hook', 'sign'], ['c1', 'redemption'], ['c1', 'last'], ['c1', 'woodson'], ['c2', 'rookie'], ['c2', 'true'], ['c2', 'gold'], ['c3', 'chase'], ['c3', 'rpa']],
   blowouts=[['c2', 'gold']], blackFlash=[['c2']], streaks=[['c1', 'woodson']],
   extras=[sfx(['hook', 'sign'], 's_correct.mp3', 0.35), png(['c1', 'redemption', 1], 'e_sob.png', 860, 1240), ov(['c2', 'gold'], 'greenflash2.mp4'), sfx(['c2', 'gold'], 's_wow.mp3', 0.35)]),
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

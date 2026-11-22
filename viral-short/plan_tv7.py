"""Trevor x Grant x Buggsy stream — 3 fresh moments from unused parts of the long source clips (2026-11-20), VverPaldo (Guess.tsx).
tvleft: "best QB I've ever seen" + why he throws better rolling LEFT (t3 0-56); tvfields: Justin Fields RPA "$20K in 2021… now 200-500" (nt_rip 94-134);
tvsweat: Grant teaches Trevor how to sweat a National Treasures card (nt_rip 14-60). Appends to edits.gen.json + yv.cfg.json."""
import json, os, subprocess
SRC = '../footage/src'
G67 = ("split[ga][gb];[gb]gblur=sigma=14[gg];[ga][gg]blend=all_mode=softlight:all_opacity=0.245,unsharp=5:5:1.74:5:5:0,"
       "eq=contrast=1.113:saturation=1.26:gamma=0.98,curves=all='0/0 0.25/0.21 0.75/0.81 1/1',unsharp=3:3:0.79,format=yuv420p")
T, GR_, BG, W = (1000, 1.6, 450), (420, 1.6, 450), (1500, 1.6, 450), (960, 1.0, 540)
TN, GS = (1000, 1.6, 500), (380, 1.4, 380)
EDITS = {
 'tvleft': ('t3_traveling_trevors', (0, 56), {'-given,': '-given?'}, [
     ('hook', 50.8, 53.3, [(50.8, GR_)]),
     ('c1', 1.7, 6.3, [(1.7, GR_), (4.2, T)]),
     ('c2', 25.7, 50.65, [(25.7, T), (33.8, W), (38.0, T), (44.8, (1000, 1.8, 440))])]),
 'tvfields': ('nt_rip', (94, 134), {'beals.': 'Fields.', 'pitcher': 'picture', 'micah': 'Micah'}, [
     ('hook', 124.6, 132.3, [(124.6, GS), (128.9, TN)]),
     ('c1', 102.8, 123.6, [(102.8, W), (110.9, TN), (115.2, W), (119.5, TN)])]),
 'tvsweat': ('nt_rip', (14, 61), {'michael': 'Micah', 'alexander': ''}, [
     ('hook', 54.3, 58.9, [(54.3, W)]),
     ('c1', 15.5, 24.0, [(15.5, W), (20.8, TN)]),
     ('c2', 34.0, 46.2, [(34.0, TN), (40.0, W)]),
     ('c3', 50.4, 54.3, [(50.4, TN)])]),
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
 'tvleft': dict(top="Why Trevor throws better rolling LEFT", hl={'LEFT': '#58EE28'}, cta='*can you throw on the run?*', music=['sentamento_n', 57.5], ctaAt=['c2', 'left', 2],
   tints=[[['hook', 'best'], G], [['c2', 'hated'], R], [['c2', 'left'], G]], rizz=[['hook', 'best']],
   punch=[['hook', 'best'], ['hook', 'quarterback'], ['c1', 'accuracy'], ['c1', 'velocity'], ['c2', 'rollouts'], ['c2', 'hated'], ['c2', 'left'], ['c2', 'better']],
   blowouts=[['hook', 'best']], blackFlash=[['c2']], streaks=[['c1']],
   extras=[png(['hook', 'life'], 'e_heart.png', 860, 1240), sfx(['c2', 'hated'], 's_huh.mp3'), sfx(['c2', 'better'], 's_wow.mp3', 0.35)]),
 'tvfields': dict(top="This card was $20,000… now it's worth THIS", hl={'$20,000…': '#58EE28', 'THIS': '#F40305'}, cta='*would you still keep it?*', music=['funkabn_n', 33.2], ctaAt=['c1', 'fields'],
   tints=[[['hook', '$20'], G], [['hook', '200'], R], [['c1', 'fields'], R]], rizz=[['hook', '$20']],
   punch=[['hook', '2021'], ['hook', '$20'], ['hook', '200'], ['hook', '500'], ['c1', 'chase'], ['c1', 'rpa'], ['c1', 'davis'], ['c1', 'fields']],
   blowouts=[['hook', '200']], blackFlash=[['c1']], streaks=[['c1', 'once']],
   extras=[sfx(['hook', '200'], 'm_record-scratch.mp3', 0.3), png(['hook', '500'], 'e_sob.png', 860, 1240), sfx(['c1', 'fields'], 's_huh.mp3')]),
 'tvsweat': dict(top='Grant teaching Trevor how to SWEAT a card', hl={'SWEAT': '#58EE28'}, cta='*do you sweat your cards?*', music=['montagem_n', 24.0], ctaAt=['c3', 'steve'],
   tints=[[['hook', 'trevor'], G], [['c1', 'sweat'], G], [['c2', 'corners'], R]], rizz=[['c1', 'sweat']],
   punch=[['hook', 'come'], ['hook', 'trevor'], ['c1', 'risk'], ['c1', 'hands'], ['c1', 'sweat'], ['c2', 'back'], ['c2', 'corners'], ['c2', 'slide'], ['c3', 'micah']],
   blowouts=[['c1', 'sweat']], blackFlash=[['c2']], streaks=[['c3']],
   extras=[png(['hook', 'trevor'], 'e_laugh.png', 860, 1240), sfx(['c2', 'corners'], 's_ding.mp3', 0.3)]),
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

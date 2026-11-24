"""Dr. Guillaume Dulude batch 5 (unused tribe/animal moments: lion part 2, Hadzabe part 2, water-hole tracking) (2026-11-23), original VverPaldo (Guess.tsx), 3-second rule: visual + audio + text hook.
lion (personal space, crouched near a lion), perfect (flawless = red flag; Tai Lopez intro cut), money (meaning does not come from money).
No colour grade (his footage already looks right) — only a light sharpen. Reaction emojis + SFX where they fit."""
import json, os, subprocess
G67 = "unsharp=5:5:0.8:3:3:0.3,format=yuv420p"
def F(y, z=1.8, x=960): return (x, z, y)
EDITS = {
 'gdlion2': ('close', (512, 602), {}, [
     ('hook', 28.95, 33.35, [(28.95, F(320, 1.8, 1000)), (31.10, F(300, 1.95, 1050))]),
     ('c1', 22.55, 28.25, [(22.55, F(320, 1.8, 1000))]),
     ('c2', 33.65, 41.85, [(33.65, F(320, 1.8, 1000)), (37.00, F(300, 1.95, 1050))]),
     ('c3', 42.30, 45.75, [(42.30, F(300, 2.1, 930))])]),
 'gdmars': ('remote', (505, 575), {'hazabe': 'Hadzabe'}, [
     ('hook', 35.05, 45.10, [(35.05, F(260, 2.0)), (39.40, F(250, 2.3)), (41.70, F(810, 2.0))]),
     ('c1', 69.15, 89.70, [(69.15, F(260, 2.0)), (70.60, F(810, 2.0)), (73.30, F(250, 2.3)), (78.60, F(260, 2.0)), (84.90, F(810, 2.0)), (87.40, F(250, 2.3))]),
     ('c2', 20.95, 35.00, [(20.95, F(260, 2.0)), (22.60, F(810, 2.0)), (26.90, F(260, 2.0)), (30.00, F(810, 2.0)), (32.40, F(250, 2.3))])]),
 'gdtracks': ('track', (558, 612), {'all': 'old'}, [
     ('hook', 18.25, 25.95, [(18.25, F(300)), (21.30, F(280, 2.1))]),
     ('c1', 4.55, 18.20, [(4.55, F(300)), (10.10, F(280, 2.1)), (14.40, F(300))]),
     ('c2', 26.25, 32.40, [(26.25, F(300)), (29.60, F(280, 2.1))])]),
}
gen = json.load(open('src/edits.gen.json'))
for eid, (src, band, fix, plan) in EDITS.items():
    out = f'public/g67_{eid}.mp4'
    bl = f'split[m][n];[n]crop=608:{band[1]-band[0]}:0:{band[0]},boxblur=16:3:8:3[b];[m][b]overlay=0:{band[0]},' if band else ''
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'../footage/gd/{src}.mp4', '-vf',
        f'scale=608:1080:flags=lanczos,{bl}pad=1920:1080:656:0:black,{G67}', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium',
        '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', out], check=True)
    Wd = json.load(open(f'../footage/gd/{src}.words.json')); scenes = []
    for sid, a, b, crops in plan:
        n = round((b - a) * 30); words = []
        for w in Wd:
            ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
            if not (a - 0.05 <= ws < b - 0.05): continue
            t2 = fix.get(t.lower(), t)
            if words and (t2.startswith('-') or (t2[:1] == ',' and t2[1:2].isdigit())): words[-1]['word'] += t2.rstrip('.'); continue
            t2 = t2.strip(',.') if not t2.endswith('?') else t2
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t2, 'startFrame': f0, 'endFrame': f1})
        for i in range(len(words) - 1): words[i]['endFrame'] = max(words[i]['endFrame'], words[i + 1]['startFrame'])
        scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'cropX': 960,
                       'crops': [[max(0, round((t - a) * 30)), x, z, y] for t, (x, z, y) in crops], 'words': words})
    gen[eid] = scenes
    print(eid, round(sum(s['durationInFrames'] for s in scenes) / 30, 1), 's |', ' / '.join(s['id'] + ': ' + ' '.join(w['word'] for w in s['words']) for s in scenes))
json.dump(gen, open('src/edits.gen.json', 'w'))
G, R = 'G', 'R'
CFG = {
 'gdlion2': dict(top='One step closer… and this LION reacts', hl={'LION': '#FF2A2A'}, cta='*follow for more psychology*', music=['brevis_n', 36.0], ctaAt=['c2', 'space'],
   tints=[[['hook', 'react'], R], [['c1', 'millimeter'], G], [['c2', 'inside'], R]], rizz=[['c1', 'millimeter']],
   punch=[['hook', 'closer'], ['hook', 'react'], ['hook', 'limit'], ['c1', 'closer'], ['c1', 'millimeter'], ['c2', 'relaxed'], ['c2', 'limit'], ['c2', 'inside'], ['c2', 'space'], ['c3', 'people'], ['c3', 'principle']],
   blowouts=[['hook', 'react']], blackFlash=[['c2']], streaks=[['c3']]),
 'gdmars': dict(top="We're building rockets to Mars… and they still live 100% traditionally", hl={'Mars…': '#58EE28', '100%': '#58EE28'}, cta='*follow for more human behavior*', music=['empire_n', 18.8], ctaAt=['c1', 'adventure'],
   tints=[[['hook', 'mars'], G], [['c1', 'tired'], R], [['c2', 'moon'], G]], rizz=[['hook', 'mars']],
   punch=[['hook', 'planet'], ['hook', 'rockets'], ['hook', 'mars'], ['hook', 'hadzabe'], ['hook', '100'], ['c1', 'morning'], ['c1', 'energy'], ['c1', 'tired'], ['c1', 'follow'], ['c1', 'exactly'], ['c2', 'moon'], ['c2', 'beautiful'], ['c2', 'surreal']],
   blowouts=[['hook', '100']], blackFlash=[['c1']], streaks=[['c2', 'there']]),
 'gdtracks': dict(top='Fresh tracks or old ones? In the bush it decides if you are SAFE', hl={'SAFE': '#58EE28'}, cta='*follow for more from the bush*', music=['sentamento_n', 57.5], ctaAt=['c2', 'water'],
   tints=[[['hook', 'dangerous'], R], [['c1', 'animals'], G], [['c2', 'water'], G]], rizz=[['hook', 'fresh']],
   punch=[['hook', 'fresh'], ['hook', 'old'], ['hook', 'decisions'], ['hook', 'dangerous'], ['c1', 'identify'], ['c1', 'tracks'], ['c1', 'animals'], ['c1', 'close'], ['c2', 'difference'], ['c2', 'water'], ['c2', 'soft']],
   blowouts=[['hook', 'dangerous']], blackFlash=[['c1']], streaks=[['c2']]),
}
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
EXTRAS = {'gdlion2': [png(['hook', 'react'], 'emoji/1f633.png', 860, 1240), sfx(['hook', 'react'], 's_wow.mp3', 0.3), png(['c2', 'inside'], 'emoji/1f62c.png', 230, 1240), png(['c3', 'people'], 'emoji/1f440.png', 860, 1240)],
  'gdmars': [png(['hook', 'mars'], 'emoji/1f680.png', 860, 1240), sfx(['hook', 'mars'], 's_wow.mp3', 0.3), png(['c1', 'tired'], 'emoji/1f62e.png', 230, 1240), png(['c2', 'moon'], 'emoji/2728.png', 860, 1240), sfx(['c2', 'surreal'], 's_ding.mp3', 0.25)],
  'gdtracks': [png(['hook', 'dangerous'], 'emoji/1f6a8.png', 860, 1240), sfx(['hook', 'dangerous'], 's_wow.mp3', 0.3), png(['c1', 'tracks'], 'emoji/1f50d.png', 230, 1240), png(['c2', 'water'], 'emoji/1f440.png', 860, 1240)]}
allc = json.load(open('src/yv.cfg.json'))
for eid, c in CFG.items():
    c.update(track='none', calls=[], intro=True, hardcut=True, cutSfx='s_camflash.mp3', src=f'g67_{eid}.mp4', extras=EXTRAS[eid])
    sc = {s['id']: s for s in gen[eid]}
    for r in [r for r, _ in c['tints']] + [r for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks') for r in c[k]] + [c['ctaAt']]:
        if len(r) == 1: continue
        ws = [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())]
        assert len(ws) > (r[2] if len(r) > 2 else 0), (eid, r, [w['word'] for w in sc[r[0]]['words']])
    allc[eid] = c
json.dump(allc, open('src/yv.cfg.json', 'w'), indent=1); print('cfg ok')

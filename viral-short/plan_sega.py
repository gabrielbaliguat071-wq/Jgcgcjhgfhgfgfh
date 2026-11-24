"""SEGA Steam Black Friday Sale (Clipping Culture, 2026-11-24), original VverPaldo (Guess.tsx). Official footage only (Frame.io f.io/O1zu3kBp,
Catalog_BFSale2026 9x16 30s: square 1080x1080 at y=420 → centred on a 1920x1080 canvas so the Guess box shows the full square).
Brief: NO added music (silent music track + fxOff: no auto SFX, no extra SFX), only prices shown in the video, limited-time Steam sale.
Trailer has no speech → captions are short on-screen text chunks matching what the trailer shows."""
import json, subprocess
SRC = {'s1': '../footage/sega/Set1_V1_9x16_30s.mp4', 's2': '../footage/sega/Set2_9x16_30s.mp4'}
for k, p in SRC.items():
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', p, '-vf', 'crop=1080:1080:0:420,scale=1080:1080,pad=1920:1080:420:0:black,format=yuv420p',
                    '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', f'public/sega_{k}.mp4'], check=True)
W0 = (960, 1.0, 540)
# scenes: (id, a, b, [(t, text), ...]) — text chunks at source times
EDITS = {
 'segaall': ('s1', [
   ('hook', 20.00, 23.00, [(20.05, 'Total War'), (20.9, 'WARHAMMER III'), (21.9, '85% OFF')]),
   ('c1', 0.00, 30.00, [(5.6, 'Sonic Frontiers'), (6.8, '75% OFF'),
      (8.1, 'Like a Dragon'), (9.6, '80% OFF'), (12.1, 'Persona 3 Reload'), (13.4, '65% OFF'), (15.1, 'Sonic Racing'), (16.4, 'CrossWorlds'), (17.8, '40% OFF'),
      (20.05, 'Warhammer III'), (21.4, '85% OFF'), (23.1, 'Two Point Museum'), (24.8, '33% OFF')])]),
 'segajrpg': ('s2', [
   ('hook', 8.00, 11.00, [(8.05, 'Like a Dragon'), (9.0, 'Infinite Wealth'), (10.0, '80% OFF')]),
   ('c1', 3.00, 5.00, []),
   ('c2', 11.00, 15.00, [(11.05, 'Like a Dragon'), (12.1, 'Persona 3 Reload'), (13.6, '65% OFF')]),
   ('c3', 27.00, 30.00, [])]),
 'segasonic': ('s2', [
   ('hook', 16.50, 19.50, [(16.55, 'Sonic Racing'), (17.5, 'CrossWorlds'), (18.5, '40% OFF')]),
   ('c0', 3.00, 5.00, []),
   ('c1', 5.50, 8.00, [(5.55, 'Sonic Frontiers'), (6.9, '75% OFF')]),
   ('c2', 15.00, 16.50, [(15.05, 'Sonic Racing')]),
   ('c3', 19.50, 20.00, [(19.55, '40% OFF')]),
   ('c4', 27.00, 30.00, [])]),
}
gen = json.load(open('src/edits.gen.json'))
for eid, (src, plan) in EDITS.items():
    scenes = []
    for sid, a, b, chunks in plan:
        n = round((b - a) * 30); words = []
        for i, (t, txt) in enumerate(chunks):
            f0 = max(0, round((t - a) * 30)); f1 = round(((chunks[i + 1][0] if i + 1 < len(chunks) else b) - a) * 30)
            words.append({'word': txt, 'startFrame': f0, 'endFrame': min(n, max(f0 + 6, f1), f0 + 54)})
        scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'cropX': 960, 'crops': [[0, *W0]], 'words': words})
    gen[eid] = scenes
    print(eid, round(sum(s['durationInFrames'] for s in scenes) / 30, 1), 's')
json.dump(gen, open('src/edits.gen.json', 'w'))
def png(at, f, x=870, y=1290, size=190): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
G, R = 'G', 'R'
CFG = {
 'segaall': dict(top='SEGA games are up to 85% OFF on Steam right now', hl={'85%': '#58EE28', 'OFF': '#58EE28'}, cta='*limited time only*', ctaAt=['c1', 'Two'],
   tints=[[['hook', '85%'], G], [['c1', '85%'], G]], rizz=[], punch=[['hook', 'WARHAMMER'], ['hook', '85%'], ['c1', '85%'], ['c1', '75%'], ['c1', '80%'], ['c1', '65%'], ['c1', '40%'], ['c1', '33%']],
   blowouts=[['hook', '85%']], blackFlash=[], streaks=[['c1', 'Sonic']], extras=[png(['hook', '85%'], 'emoji/1f633.png'), png(['c1', 'Like'], 'emoji/1f525.png', 230, 1240), png(['c1', 'Two'], 'emoji/1f440.png')]),
 'segajrpg': dict(top='JRPG fans… these are on sale on Steam right now', hl={'JRPG': '#58EE28'}, cta='*limited time only*', ctaAt=['c3'],
   tints=[[['hook', '80%'], G]], rizz=[], punch=[['hook', 'Infinite'], ['hook', '80%'], ['c2', 'Persona'], ['c2', '65%']],
   blowouts=[['hook', '80%']], blackFlash=[], streaks=[['c2']], extras=[png(['hook', '80%'], 'emoji/1f633.png'), png(['c2', '65%'], 'emoji/1f525.png', 230, 1240), png(['c3'], 'emoji/23f3.png')]),
 'segasonic': dict(top='Sonic games are on sale on Steam for Black Friday', hl={'Sonic': '#2F8CFF'}, cta='*limited time only*', ctaAt=['c4'],
   tints=[[['c1', '75%'], G]], rizz=[], punch=[['hook', 'CrossWorlds'], ['hook', '40%'], ['c1', 'Sonic'], ['c1', '75%'], ['c3', '40%']],
   blowouts=[['c1', '75%']], blackFlash=[], streaks=[['c2']], extras=[png(['hook', '40%'], 'emoji/1f525.png'), png(['c1', '75%'], 'emoji/1f633.png', 230, 1240), png(['c4'], 'emoji/23f3.png')]),
}
allc = json.load(open('src/yv.cfg.json'))
for eid, c in CFG.items():
    c.update(track='none', calls=[], intro=True, hardcut=True, src=f'sega_{EDITS[eid][0]}.mp4', music=['silent_n', 0], fxOff=True)
    sc = {s['id']: s for s in gen[eid]}
    for r in [r for r, _ in c['tints']] + [r for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks') for r in c[k]] + [c['ctaAt']] + [e['at'] for e in c['extras']]:
        if len(r) == 1: continue
        assert [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())], (eid, r)
    allc[eid] = c
json.dump(allc, open('src/yv.cfg.json', 'w'), indent=1); print('cfg ok')

"""SEGA Steam Black Friday Sale (Clipping Culture, 2026-11-24), original VverPaldo (Guess.tsx). Official footage only (Frame.io f.io/O1zu3kBp,
Catalog_BFSale2026 9x16 30s: square 1080x1080 at y=420 → centred on a 1920x1080 canvas so the Guess box shows the full square).
Brief: NO added music (silent music track + fxOff: no auto SFX, no extra SFX), only prices shown in the video, limited-time Steam sale.
Trailer has no speech → captions are short on-screen text chunks matching what the trailer shows."""
import json, subprocess
SRC = {'s1': '../footage/sega/Set1_V1_9x16_30s.mp4', 's2': '../footage/sega/Set2_9x16_30s.mp4', 'q2': '../footage/sega/Set2_9x16_15s.mp4'}
for k, p in SRC.items():
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', p, '-vf', 'crop=1080:1080:0:420,scale=1080:1080,pad=1920:1080:420:0:black,format=yuv420p',
                    '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', f'public/sega_{k}.mp4'], check=True)
W0 = (960, 1.0, 540)
# scenes: (id, a, b, [(t, text), ...]) — text chunks at source times
EDITS = {
 'segapoll': ('s2', [
   ('hook', 1.00, 3.00, []),
   ('c1', 5.60, 7.50, [(5.65, '1'), (6.2, 'Sonic Frontiers'), (6.9, '75% OFF')]),
   ('c2', 8.60, 10.50, [(8.65, '2'), (9.2, 'Like a Dragon'), (9.9, '80% OFF')]),
   ('c3', 12.10, 14.00, [(12.15, '3'), (12.7, 'Persona 3 Reload'), (13.4, '65% OFF')]),
   ('c4', 16.00, 17.90, [(16.05, '4'), (16.6, 'Sonic Racing'), (17.3, '40% OFF')]),
   ('c5', 20.00, 21.90, [(20.05, '5'), (20.6, 'Warhammer III'), (21.3, '85% OFF')]),
   ('c6', 23.20, 25.10, [(23.25, '6'), (23.8, 'Two Point Museum'), (24.5, '33% OFF')]),
   ('c7', 27.00, 30.00, [])]),
 'segapersona': ('s2', [
   ('hook', 12.00, 14.20, [(12.05, 'Persona 3 Reload'), (13.2, '65% OFF')]),
   ('c1', 0.00, 5.00, []),
   ('c2', 14.20, 15.20, [(14.25, '65% OFF')]),
   ('c3', 27.00, 30.00, [])]),
 'segafrontiers': ('s2', [
   ('hook', 5.50, 7.20, [(5.55, 'Sonic Frontiers'), (6.5, '75% OFF')]),
   ('c1', 0.00, 5.00, []),
   ('c2', 7.20, 8.30, [(7.25, '75% OFF')]),
   ('c3', 27.00, 30.00, [])]),
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
 'segapoll': dict(top='You can only pick ONE… which SEGA game are you buying?', hl={'ONE…': '#58EE28'}, cta='*comment your number*', ctaAt=['c7'],
   tints=[[['c5', '85%'], G]], rizz=[], punch=[['c1', '75%'], ['c2', '80%'], ['c3', '65%'], ['c4', '40%'], ['c5', '85%'], ['c6', '33%']],
   blowouts=[['c5', '85%']], blackFlash=[], streaks=[['c2'], ['c4'], ['c6']], extras=[png(['c5', '85%'], 'emoji/1f633.png'), png(['c7'], 'emoji/1f914.png')]),
 'segapersona': dict(top='Persona 3 Reload is 65% OFF on Steam right now', hl={'65%': '#58EE28', 'OFF': '#58EE28'}, cta='*limited time only*', ctaAt=['c3'],
   tints=[[['hook', '65%'], G]], rizz=[], punch=[['hook', 'Persona'], ['hook', '65%'], ['c2', '65%']],
   blowouts=[['hook', '65%']], blackFlash=[], streaks=[['c2']], extras=[png(['hook', '65%'], 'emoji/1f525.png'), png(['c3'], 'emoji/23f3.png')]),
 'segafrontiers': dict(top='Sonic Frontiers is 75% OFF on Steam right now', hl={'75%': '#58EE28', 'OFF': '#58EE28'}, cta='*limited time only*', ctaAt=['c3'],
   tints=[[['hook', '75%'], G]], rizz=[], punch=[['hook', 'Sonic'], ['hook', '75%'], ['c2', '75%']],
   blowouts=[['hook', '75%']], blackFlash=[], streaks=[['c2']], extras=[png(['hook', '75%'], 'emoji/1f633.png'), png(['c3'], 'emoji/23f3.png')]),
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

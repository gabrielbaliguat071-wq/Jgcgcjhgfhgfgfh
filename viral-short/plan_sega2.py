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
 'segastrat': ('s2', [
   ('hook', 20.00, 23.00, [(20.05, 'Total War'), (20.9, 'WARHAMMER III'), (21.9, '85% OFF')]),
   ('c1', 1.00, 3.00, []),
   ('c2', 23.00, 27.00, [(23.1, 'Two Point Museum'), (24.8, '33% OFF')]),
   ('c3', 27.00, 30.00, [])]),
 'segatop3': ('s1', [
   ('hook', 20.00, 21.60, [(20.05, '#1')]),
   ('c1', 5.50, 8.00, [(5.55, '#3'), (6.2, 'Sonic Frontiers'), (7.1, '75% OFF')]),
   ('c2', 8.00, 11.00, [(8.05, '#2'), (8.7, 'Like a Dragon'), (9.9, '80% OFF')]),
   ('c3', 20.00, 23.00, [(20.05, '#1'), (20.7, 'WARHAMMER III'), (21.9, '85% OFF')]),
   ('c4', 27.00, 30.00, [])]),
 'segaquick': ('q2', [
   ('hook', 1.00, 4.50, []),
   ('c1', 5.50, 15.00, [(5.55, '75% OFF'), (6.55, '80% OFF'), (8.05, '65% OFF'), (9.05, '40% OFF'), (10.3, '85% OFF'), (11.8, '33% OFF')])]),
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
 'segastrat': dict(top='Strategy fans… Warhammer III is 85% OFF on Steam', hl={'85%': '#58EE28', 'OFF': '#58EE28'}, cta='*limited time only*', ctaAt=['c3'],
   tints=[[['hook', '85%'], G]], rizz=[], punch=[['hook', 'WARHAMMER'], ['hook', '85%'], ['c2', 'Two'], ['c2', '33%']],
   blowouts=[['hook', '85%']], blackFlash=[], streaks=[['c2']], extras=[png(['hook', '85%'], 'emoji/1f633.png'), png(['c2', '33%'], 'emoji/1f3db-fe0f.png' if False else 'emoji/1f525.png', 230, 1240), png(['c3'], 'emoji/23f3.png')]),
 'segatop3': dict(top="The 3 biggest SEGA discounts on Steam right now", hl={'3': '#58EE28'}, cta='*limited time only*', ctaAt=['c4'],
   tints=[[['c3', '85%'], G]], rizz=[], punch=[['c1', '75%'], ['c2', '80%'], ['c3', 'WARHAMMER'], ['c3', '85%']],
   blowouts=[['c3', '85%']], blackFlash=[], streaks=[['c2'], ['c3']], extras=[png(['c2', '80%'], 'emoji/1f525.png', 230, 1240), png(['c3', '85%'], 'emoji/1f633.png'), png(['c4'], 'emoji/23f3.png')]),
 'segaquick': dict(top='Every SEGA Black Friday deal on Steam in 10 seconds', hl={'10': '#58EE28'}, cta='*limited time only*', ctaAt=['c1', '33%'],
   tints=[[['c1', '85%'], G]], rizz=[], punch=[['c1', '75%'], ['c1', '80%'], ['c1', '65%'], ['c1', '40%'], ['c1', '85%'], ['c1', '33%']],
   blowouts=[['c1', '85%']], blackFlash=[], streaks=[], extras=[png(['c1', '85%'], 'emoji/1f633.png'), png(['c1', '33%'], 'emoji/23f3.png', 230, 1240)]),
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

"""Dr. Guillaume Dulude x3 in the original VverPaldo style (Guess.tsx) — 2026-11-23. Sources: his TikTok lessons (576x1024 vertical),
padded onto a 1920x1080 canvas (video at x 656-1264) so the Guess box shows a ~1.8x square face crop. Campaign is professional: no skull, no meme
emojis/SFX (VverPaldo look + structure kept: hook → hard cut flash → story that loops into the hook). Appends to edits.gen.json + yv.cfg.json."""
import json, os, subprocess
G67 = ("split[ga][gb];[gb]gblur=sigma=14[gg];[ga][gg]blend=all_mode=softlight:all_opacity=0.245,unsharp=5:5:1.74:5:5:0,"
       "eq=contrast=1.113:saturation=1.26:gamma=0.98,curves=all='0/0 0.25/0.21 0.75/0.81 1/1',unsharp=3:3:0.79,format=yuv420p")
def F(y, z=1.8): return (960, z, y)
EDITS = {  # id: (src, band(y0,y1) of his old burned subs in 1080 canvas or None, fixes, scenes)
 'gdfear': ('fear', (500, 575), {}, [
     ('hook', 1.00, 3.85, [(1.00, F(320, 2.05))]),
     ('c1', 4.10, 16.85, [(4.10, F(330)), (10.30, F(300, 2.1))]),
     ('c2', 23.80, 39.10, [(23.80, F(330)), (29.40, F(300, 2.1)), (35.50, F(330))])]),
 'gdlying': ('lying', None, {'lie.': 'lie.'}, [
     ('hook', 34.35, 37.60, [(34.35, F(340, 2.1))]),
     ('c1', 22.25, 31.20, [(22.25, F(370)), (26.40, F(340, 2.1))]),
     ('c2', 37.65, 45.10, [(37.65, F(370))]),
     ('c3', 48.85, 60.80, [(48.85, F(370)), (53.50, F(340, 2.1)), (58.10, F(370))])]),
 'gdsilence': ('silence', None, {}, [
     ('hook', 58.75, 61.25, [(58.75, F(360, 2.1))]),
     ('c1', 14.35, 19.60, [(14.35, F(390))]),
     ('c2', 41.85, 45.70, [(41.85, F(360, 2.1))]),
     ('c3', 48.05, 58.70, [(48.05, F(390)), (52.70, F(360, 2.1))])]),
}
gen = json.load(open('src/edits.gen.json'))
for eid, (src, band, fix, plan) in EDITS.items():
    out = f'public/g67_{eid}.mp4'
    bl = f'split[m][n];[n]crop=608:{band[1]-band[0]}:0:{band[0]},boxblur=16:3:8:3[b];[m][b]overlay=0:{band[0]},' if band else ''
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'../footage/gd/{src}.mp4', '-vf',
        f'scale=608:1080:flags=lanczos,{bl}pad=1920:1080:656:0:black,{G67}', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium',
        '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', out], check=True)
    Wd = json.load(open(f'../footage/gd/{src}.words.json')); scenes = []
    for sid, a, b, crops in plan:
        n = round((b - a) * 30); words = []
        for w in Wd:
            ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
            if not (a - 0.05 <= ws < b - 0.05): continue
            t2 = fix.get(t.lower(), t)
            if words and t2.startswith('-'): words[-1]['word'] += t2; continue
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
 'gdfear': dict(top='Either you control your fears… or they control YOU', hl={'YOU': '#FF2A2A'}, cta='*follow for more psychology*', music=['sentamento_n', 57.5], ctaAt=['c2', 'over'],
   tints=[[['hook', 'control'], R], [['c1', 'expose'], G], [['c2', 'rewire'], G]], rizz=[['c1', 'expose']],
   punch=[['hook', 'fears'], ['hook', 'control', 1], ['c1', 'only'], ['c1', 'controlled'], ['c1', 'low'], ['c1', 'judged'], ['c2', 'drops'], ['c2', 'rewire'], ['c2', 'stronger']],
   blowouts=[['c2', 'stronger']], blackFlash=[['c2']], streaks=[['c1', 'for']]),
 'gdlying': dict(top="Words and body don't match? It's NOT always a lie", hl={'NOT': '#FF2A2A'}, cta='*follow for more body language*', music=['brevis_n', 36.0], ctaAt=['c3', 'trust'],
   tints=[[['hook', 'wrong'], R], [['c1', 'anxiety'], G], [['c3', 'trust'], G]], rizz=[['c1', 'anxiety']],
   punch=[['hook', 'wrong'], ['hook', 'lying'], ['c1', 'conflict'], ['c1', 'lie'], ['c1', 'anxiety'], ['c2', 'conscious'], ['c2', 'stories'], ['c3', 'trust'], ['c3', 'fit']],
   blowouts=[['c2', 'conscious']], blackFlash=[['c3']], streaks=[['c2']]),
 'gdsilence': dict(top='People notice in 10 milliseconds when your attention drifts', hl={'10': '#58EE28', 'milliseconds': '#58EE28'}, cta='*follow for more psychology*', music=['montagem_n', 24.0], ctaAt=['c3', 'ocular'],
   tints=[[['hook', '10'], G], [['c1', 'scared'], R], [['c3', 'sustained'], G]], rizz=[['hook', '10']],
   punch=[['hook', 'detect'], ['hook', '10'], ['c1', 'powerful'], ['c1', 'scared'], ['c2', 'attention'], ['c2', 'wait'], ['c3', 'only'], ['c3', 'sustained'], ['c3', 'ocular'], ['c3', 'consciously']],
   blowouts=[['hook', '10']], blackFlash=[['c3']], streaks=[['c2']]),
}
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
EXTRAS = {'gdfear': [png(['c1', 'judged'], 'e_think.png', 860, 1240), sfx(['c2', 'drops'], 's_ding.mp3', 0.3), sfx(['c2', 'stronger'], 's_wow.mp3', 0.3)],
  'gdlying': [png(['c1', 'anxiety'], 'e_think.png', 860, 1240), sfx(['c2', 'conscious'], 's_wow.mp3', 0.3), sfx(['c3', 'trust'], 's_ding.mp3', 0.3)],
  'gdsilence': [png(['c1', 'scared'], 'e_think.png', 860, 1240), sfx(['hook', '10'], 's_wow.mp3', 0.3), sfx(['c3', 'sustained'], 's_ding.mp3', 0.3)]}
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

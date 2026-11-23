"""Dr. Guillaume Dulude batch 3 (wildlife / bush) (2026-11-23), original VverPaldo (Guess.tsx), 3-second rule: visual + audio + text hook.
lion (personal space, crouched near a lion), perfect (flawless = red flag; Tai Lopez intro cut), money (meaning does not come from money).
No colour grade (his footage already looks right) — only a light sharpen. Reaction emojis + SFX where they fit."""
import json, os, subprocess
G67 = "unsharp=5:5:0.8:3:3:0.3,format=yuv420p"
def F(y, z=1.8, x=960): return (x, z, y)
EDITS = {
 'gdspider': ('remote', (505, 575), {'hazabe': 'Hadzabe', 'spiders': 'spider'}, [
     ('hook', 55.35, 67.15, [(55.35, F(260, 2.0)), (59.00, F(250, 2.3)), (63.60, F(260, 2.0))]),
     ('c1', 0.00, 21.00, [(0.00, F(260, 2.0)), (5.55, F(810, 2.0)), (9.10, F(260, 2.0)), (14.20, F(810, 2.0)), (17.80, F(250, 2.3))]),
     ('c2', 46.15, 55.30, [(46.15, F(260, 2.0)), (49.70, F(250, 2.3)), (53.20, F(810, 2.0))])]),
 'gdgiraffe': ('bush', (548, 608), {}, [
     ('hook', 32.85, 40.75, [(32.85, F(300)), (36.40, F(280, 2.1)), (38.30, F(300))]),
     ('c1', 4.45, 12.10, [(4.45, F(300)), (8.80, F(280, 2.1))]),
     ('c2', 26.05, 32.00, [(26.05, F(300))]),
     ('c3', 44.75, 54.70, [(44.75, F(300)), (49.40, F(280, 2.1)), (53.30, F(300))])]),
 'gdpoison': ('guess', (755, 825), {'uphobia.': 'Euphorbia', 'uphobia': 'Euphorbia'}, [
     ('hook', 23.55, 32.30, [(23.55, F(450)), (28.20, F(520, 2.1, 980)), (31.10, F(420))]),
     ('c1', 12.35, 23.40, [(12.35, F(440)), (16.40, F(400, 2.1)), (19.40, F(440))]),
     ('c2', 32.85, 39.80, [(32.85, F(400)), (36.20, F(380, 2.1))]),
     ('c3', 45.55, 51.00, [(45.55, F(420))]),
     ('c4', 65.15, 80.10, [(65.15, F(420)), (72.60, F(380, 2.1)), (77.30, F(420))])]),
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
 'gdspider': dict(top='His first night with a hunter-gatherer tribe… then THIS fell on his head', hl={'THIS': '#FF2A2A'}, cta='*follow for more human behavior*', music=['brevis_n', 36.0], ctaAt=['c1', 'sleep', 1],
   tints=[[['hook', 'spider'], R], [['c1', 'differently'], G], [['c2', 'dehydration'], R]], rizz=[['c1', 'differently']],
   punch=[['hook', 'falling'], ['hook', 'head'], ['hook', 'jump'], ['hook', 'spider'], ['hook', 'hand'], ['c1', 'night'], ['c1', 'dancing'], ['c1', 'differently'], ['c1', 'minutes'], ['c2', 'privilege'], ['c2', 'hard'], ['c2', 'dehydration']],
   blowouts=[['hook', 'spider']], blackFlash=[['c2']], streaks=[['c1', 'so']]),
 'gdgiraffe': dict(top="A giraffe's kick is like a golf club with a HAMMER", hl={'HAMMER': '#FF2A2A'}, cta='*follow for more psychology*', music=['empire_n', 18.8], ctaAt=['c3', 'body'],
   tints=[[['hook', 'kick'], R], [['c1', 'anxious'], G], [['c3', 'body'], G]], rizz=[['c1', 'control']],
   punch=[['hook', 'close'], ['hook', 'kick'], ['hook', 'dangerous'], ['hook', 'legs'], ['hook', 'hammer'], ['c1', 'see'], ['c1', 'control'], ['c1', 'anxious'], ['c2', 'curious'], ['c2', 'closer'], ['c3', 'distance'], ['c3', 'aggression'], ['c3', 'body']],
   blowouts=[['hook', 'hammer']], blackFlash=[['c3']], streaks=[['c2']]),
 'gdpoison': dict(top='He cut this tree open… and it started bleeding POISON', hl={'POISON': '#FF2A2A'}, cta='*follow for more from the bush*', music=['sentamento_n', 57.5], ctaAt=['c4', 'bush'],
   tints=[[['hook', 'poison'], R], [['c1', 'toxic'], R], [['c4', 'smoke'], R]], rizz=[['hook', 'bleeds']],
   punch=[['hook', 'cut'], ['hook', 'opening'], ['hook', 'bleeds'], ['hook', 'poison'], ['c1', 'euphorbia'], ['c1', 'toxic'], ['c1', 'liquid'], ['c2', 'finger'], ['c2', 'eyes'], ['c3', 'arrow'], ['c4', 'survival'], ['c4', 'burning'], ['c4', 'smoke'], ['c4', 'toxic']],
   blowouts=[['hook', 'poison']], blackFlash=[['c4']], streaks=[['c3']]),
}
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
EXTRAS = {'gdspider': [png(['hook', 'spider'], 'emoji/1f631.png', 860, 1240), sfx(['hook', 'jump'], 's_huh.mp3', 0.3), png(['c1', 'dancing'], 'emoji/1f440.png', 230, 1240), sfx(['c2', 'dehydration'], 's_wow.mp3', 0.25)],
  'gdgiraffe': [png(['hook', 'kick'], 'emoji/1f633.png', 860, 1240), sfx(['hook', 'hammer'], 's_wow.mp3', 0.3), png(['c2', 'curious'], 'emoji/1f440.png', 230, 1240), png(['c3', 'aggression'], 'emoji/1f62c.png', 860, 1240)],
  'gdpoison': [png(['hook', 'bleeds'], 'emoji/1f633.png', 860, 1240), sfx(['hook', 'poison'], 's_wow.mp3', 0.3), png(['c2', 'eyes'], 'emoji/1f62c.png', 230, 1240), png(['c4', 'smoke'], 'emoji/274c.png', 860, 1240), sfx(['c4', 'toxic'], 's_ding.mp3', 0.25)]}
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

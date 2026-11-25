"""Dr. Guillaume Dulude batch 7 (bush: wild nyalas, leopard campsite, flint fire — Psycom Origin footage, lesson parts only, no sales pitch) (2026-11-23), original VverPaldo (Guess.tsx), 3-second rule: visual + audio + text hook.
lion (personal space, crouched near a lion), perfect (flawless = red flag; Tai Lopez intro cut), money (meaning does not come from money).
No colour grade (his footage already looks right) — only a light sharpen. Reaction emojis + SFX where they fit."""
import json, os, subprocess
G67 = "unsharp=5:5:0.8:3:3:0.3,format=yuv420p"
def F(y, z=1.8, x=960): return (x, z, y)
EDITS = {
 'gdwild': ('field', (680, 735), {'nialas': 'nyalas', 'niala': 'nyala', 'nialas.': 'nyalas'}, [
     ('hook', 56.85, 62.65, [(56.85, F(470)), (59.20, F(380))]),
     ('c1', 40.00, 56.80, [(40.00, F(380)), (41.00, F(470)), (45.00, F(380)), (47.00, F(470)), (52.00, F(380)), (53.20, F(470))]),
     ('c2', 62.70, 80.00, [(62.70, F(380)), (67.00, F(470)), (70.00, F(380)), (73.00, F(360, 2.1)), (77.50, F(430))])]),
 'gdleopard': ('campsite', (560, 612), {'unesco,': 'here,', 'big': 'Big', 'fat': 'Five', 'psychome': 'Psycom'}, [
     ('hook', 70.45, 81.60, [(70.45, F(440, 1.8, 1060)), (74.00, F(400, 2.1, 1090)), (78.90, F(440, 1.8, 1060))]),
     ('c1', 0.00, 12.85, [(0.00, F(440, 1.8, 1060)), (4.80, F(400, 2.1, 1090)), (9.50, F(440, 1.8, 1060))]),
     ('c2', 44.35, 70.40, [(44.35, F(440, 1.8, 1060)), (47.90, F(400, 2.1, 1090)), (54.60, F(440, 1.8, 1060)), (60.40, F(400, 2.1, 1090)), (63.50, F(440, 1.8, 1060))])]),
 'gdfire': ('fire', (562, 618), {'flint': 'flint', 'grills': 'Grylls', 'bear': 'Bear'}, [
     ('hook', 2.55, 6.30, [(2.55, F(520)), (5.90, F(330))]),
     ('c1', 6.30, 30.80, [(6.30, F(330)), (11.30, F(300, 2.1)), (16.70, F(330))]),
     ('c2', 61.25, 82.80, [(61.25, F(330)), (68.40, F(300, 2.1)), (76.10, F(330))])]),
}
gen = json.load(open('src/edits.gen.json'))
for eid, (src, band, fix, plan) in EDITS.items():
    out = f'public/g67_{eid}.mp4'
    bl = f'split[m][n];[n]crop=608:{band[1]-band[0]}:0:{band[0]},boxblur=16:3:8:3[b];[m][b]overlay=0:{band[0]},' if band else ''
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'../footage/gd2/{src}.mp4', '-vf',
        f'scale=608:1080:flags=lanczos,{bl}pad=1920:1080:656:0:black,{G67}', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium',
        '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', out], check=True)
    Wd = json.load(open(f'../footage/gd2/{src}.words.json')); scenes = []
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
 'gdwild': dict(top="Walking up to wild animals that aren't used to HUMANS", hl={'HUMANS': '#FF2A2A'}, cta='*follow for more from the bush*', music=['brevis_n', 36.0], ctaAt=['c2', 'closer'],
   tints=[[['hook', 'human'], R], [['c1', 'five'], G], [['c2', 'dangerous'], R]], rizz=[['c1', 'five']],
   punch=[['hook', 'human'], ['hook', 'never'], ['c1', 'surrounded'], ['c1', 'wild'], ['c1', 'elephants'], ['c1', 'rhinos'], ['c1', 'lions'], ['c2', 'rare'], ['c2', 'close'], ['c2', 'dangerous'], ['c2', 'closer']],
   blowouts=[['c2', 'dangerous']], blackFlash=[['c2']], streaks=[['c1', 'here']]),
 'gdleopard': dict(top='Where would YOU sleep if leopards were around?', hl={'YOU': '#FF2A2A'}, cta='*follow for more from the bush*', music=['empire_n', 18.8], ctaAt=['c2', 'escape'],
   tints=[[['hook', 'leopard'], R], [['c2', 'ants'], R], [['c2', 'sheltered'], G]], rizz=[['c1', 'choose']],
   punch=[['hook', 'dangerous'], ['hook', 'caracal'], ['hook', 'leopard'], ['hook', 'escape'], ['c1', 'first'], ['c1', 'choose'], ['c1', 'best'], ['c2', 'flat'], ['c2', 'ants'], ['c2', 'attack'], ['c2', 'never'], ['c2', 'wind'], ['c2', 'escape']],
   blowouts=[['hook', 'leopard']], blackFlash=[['c2']], streaks=[['c1']]),
 'gdfire': dict(top="Making fire looks easy on YouTube… the reality is DIFFERENT", hl={'DIFFERENT': '#FF2A2A'}, cta='*follow for more psychology*', music=['sentamento_n', 57.5], ctaAt=['c2', 'expert'],
   tints=[[['hook', 'fire'], G], [['c1', 'difficult'], R], [['c2', 'skill'], G]], rizz=[['c2', 'skill']],
   punch=[['hook', 'make'], ['hook', 'fire'], ['hook', 'flint'], ['c1', 'easy'], ['c1', 'second'], ['c1', 'reality'], ['c1', 'difficult'], ['c1', 'metaphor'], ['c2', 'magic'], ['c2', 'skill'], ['c2', 'control'], ['c2', 'expert'], ['c2', 'sense']],
   blowouts=[['c2', 'magic']], blackFlash=[['c1']], streaks=[['c2']]),
}
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
EXTRAS = {'gdwild': [png(['hook', 'human'], 'emoji/1f440.png', 860, 1240), sfx(['hook', 'never'], 's_wow.mp3', 0.25), png(['c1', 'lions'], 'emoji/1f631.png', 230, 1240), png(['c2', 'dangerous'], 'emoji/1f6a8.png', 860, 1240), sfx(['c2', 'dangerous'], 's_huh.mp3', 0.25)],
  'gdleopard': [png(['hook', 'leopard'], 'emoji/1f631.png', 860, 1240), sfx(['hook', 'leopard'], 's_wow.mp3', 0.25), png(['c2', 'ants'], 'emoji/1f62c.png', 230, 1240), sfx(['c2', 'never'], 's_huh.mp3', 0.25)],
  'gdfire': [png(['hook', 'flint'], 'emoji/1f525.png', 860, 1240), sfx(['hook', 'fire'], 's_ding.mp3', 0.25), png(['c1', 'difficult'], 'emoji/1f62c.png', 230, 1240), png(['c2', 'skill'], 'emoji/1f9e0.png', 860, 1240), sfx(['c2', 'expert'], 's_wow.mp3', 0.25)]}
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

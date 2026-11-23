"""Dr. Guillaume Dulude batch 2 (2026-11-23), original VverPaldo (Guess.tsx), 3-second rule: visual + audio + text hook.
lion (personal space, crouched near a lion), perfect (flawless = red flag; Tai Lopez intro cut), money (meaning does not come from money).
No colour grade (his footage already looks right) — only a light sharpen. Reaction emojis + SFX where they fit."""
import json, os, subprocess
G67 = "unsharp=5:5:0.8:3:3:0.3,format=yuv420p"
def F(y, z=1.8, x=960): return (x, z, y)
EDITS = {
 'gdlion': ('close', (512, 602), {'distance': 'Distance'}, [
     ('hook', 3.65, 9.62, [(3.65, F(320)), (6.90, F(300, 1.9, 1000))]),
     ('c1', 0.00, 3.62, [(0.00, F(340))]),
     ('c2', 9.70, 22.35, [(9.70, F(340)), (14.70, F(310, 2.1, 930)), (18.60, F(340))]),
     ('c3', 36.90, 53.95, [(36.90, F(340)), (42.30, F(310, 2.1, 930)), (46.00, F(340)), (49.50, F(310, 2.1, 930))])]),
 'gdperfect': ('perfect', None, {'mycophilic,': 'Machiavellian'}, [
     ('hook', 8.55, 12.98, [(8.55, F(340, 2.1))]),
     ('c1', 13.40, 17.50, [(13.40, F(370))]),
     ('c2', 27.50, 41.95, [(27.50, F(370)), (32.55, F(340, 2.1)), (37.30, F(370))]),
     ('c3', 56.85, 62.20, [(56.85, F(340, 2.1))])]),
 'gdmoney': ('money', (590, 645), {}, [
     ('hook', 33.00, 36.30, [(33.00, F(330, 2.1))]),
     ('c1', 15.85, 29.00, [(15.85, F(360)), (22.45, F(330, 2.1)), (25.20, F(360))]),
     ('c2', 36.75, 46.25, [(36.75, F(360)), (42.70, F(330, 2.1))])]),
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
 'gdlion': dict(top='A lion is watching him… and it\'s a lesson about PEOPLE', hl={'PEOPLE': '#58EE28'}, cta='*follow for more psychology*', music=['brevis_n', 36.0], ctaAt=['c3', 'people'],
   tints=[[['hook', 'lion'], R], [['c2', 'psychology'], G], [['c3', 'invasive'], R]], rizz=[['c2', 'psychology']],
   punch=[['hook', 'lion'], ['hook', 'looking'], ['hook', 'eyes'], ['c1', 'distance'], ['c2', 'attention'], ['c2', 'humans'], ['c2', 'closer'], ['c3', 'inside'], ['c3', 'people'], ['c3', 'close'], ['c3', 'invasive']],
   blowouts=[['hook', 'me']], blackFlash=[['c3']], streaks=[['c2', 'but']]),
 'gdperfect': dict(top='If someone looks PERFECT… it\'s a red flag', hl={'PERFECT…': '#FF2A2A'}, cta='*follow for more psychology*', music=['empire_n', 18.8], ctaAt=['c2', 'careful'],
   tints=[[['hook', 'red'], R], [['c2', 'psychopathic'], R], [['c3', 'perfect'], G]], rizz=[['c2', 'expert']],
   punch=[['hook', 'flawless'], ['hook', 'red'], ['c1', 'hidden'], ['c1', 'perfect'], ['c2', 'narcissistic'], ['c2', 'psychopathic'], ['c2', 'expert'], ['c2', 'true'], ['c2', 'manipulation'], ['c3', 'social'], ['c3', 'perfect']],
   blowouts=[['c2', 'true']], blackFlash=[['c2']], streaks=[['c3']]),
 'gdmoney': dict(top='Does money buy happiness? A psychologist answers', hl={'happiness?': '#58EE28'}, cta='*follow for more psychology*', music=['sentamento_n', 57.5], ctaAt=['c2', 'manage'],
   tints=[[['hook', 'meaning'], G], [['c1', 'anxiety'], R], [['c2', 'meaning'], G]], rizz=[['hook', 'resource']],
   punch=[['hook', 'meaning'], ['hook', 'money'], ['hook', 'resource'], ['c1', 'anxiety'], ['c1', 'bills'], ['c1', 'decrease'], ['c1', 'happiness'], ['c2', 'meaning'], ['c2', 'bill'], ['c2', 'happiness']],
   blowouts=[['hook', 'resource']], blackFlash=[['c1']], streaks=[['c2']]),
}
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
EXTRAS = {'gdlion': [png(['hook', 'looking'], 'emoji/1f633.png', 860, 1240), sfx(['hook', 'looking'], 's_wow.mp3', 0.3), png(['c2', 'humans'], 'emoji/1f440.png', 230, 1240), sfx(['c3', 'invasive'], 's_huh.mp3', 0.3), png(['c3', 'invasive'], 'emoji/1f62c.png', 860, 1240)],
  'gdperfect': [png(['hook', 'red'], 'emoji/1f6a8.png', 860, 1240), sfx(['hook', 'red'], 's_ding.mp3', 0.3), png(['c2', 'psychopathic'], 'emoji/1f633.png', 230, 1240), sfx(['c2', 'true'], 's_wow.mp3', 0.3), png(['c3', 'perfect'], 'emoji/1f914.png', 860, 1240)],
  'gdmoney': [png(['hook', 'money'], 'emoji/1f4b8.png', 860, 1240), sfx(['hook', 'resource'], 's_ding.mp3', 0.3), png(['c1', 'bills'], 'emoji/1f62c.png', 230, 1240), sfx(['c2', 'happiness'], 's_wow.mp3', 0.3), png(['c2', 'meaning'], 'emoji/1f914.png', 860, 1240)]}
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

"""Dr. Guillaume Dulude batch 6 (giraffe first move, disgust/metacognition, eye contact — Vanessa inserts cut) (2026-11-23), original VverPaldo (Guess.tsx), 3-second rule: visual + audio + text hook.
lion (personal space, crouched near a lion), perfect (flawless = red flag; Tai Lopez intro cut), money (meaning does not come from money).
No colour grade (his footage already looks right) — only a light sharpen. Reaction emojis + SFX where they fit."""
import json, os, subprocess
G67 = "unsharp=5:5:0.8:3:3:0.3,format=yuv420p"
def F(y, z=1.8, x=960): return (x, z, y)
EDITS = {
 'gdgiraffe2': ('bush', (548, 608), {}, [
     ('hook', 66.05, 73.40, [(66.05, F(300)), (68.10, F(280, 2.1)), (71.50, F(300))]),
     ('c1', 51.20, 66.00, [(51.20, F(300)), (55.60, F(280, 2.1)), (59.50, F(300)), (64.00, F(280, 2.1))])]),
 'gddisgust': ('disgust', None, {}, [
     ('hook', 57.15, 61.10, [(57.15, F(340, 2.1))]),
     ('c1', 2.75, 20.55, [(2.75, F(360)), (7.20, F(330, 2.1)), (11.10, F(360)), (15.00, F(330, 2.1))]),
     ('c2', 31.75, 57.10, [(31.75, F(360)), (34.10, F(330, 2.1)), (38.40, F(360)), (44.20, F(330, 2.1)), (50.10, F(360)), (54.20, F(330, 2.1))])]),
 'gdeyecontact': ('eyecontact', (505, 575), {}, [
     ('hook', 37.05, 42.45, [(37.05, F(260, 2.0)), (39.40, F(250, 2.3))]),
     ('c1', 13.45, 37.00, [(13.45, F(260, 2.0)), (18.10, F(250, 2.3)), (23.90, F(260, 2.0)), (29.50, F(250, 2.3)), (33.90, F(260, 2.0))]),
     ('c2', 44.95, 51.25, [(44.95, F(260, 2.0)), (49.40, F(250, 2.3))])]),
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
 'gdgiraffe2': dict(top="Never make the first move with a giraffe… let it come to YOU", hl={'YOU': '#58EE28'}, cta='*follow for more from the bush*', music=['brevis_n', 36.0], ctaAt=['c1', 'giraffe'],
   tints=[[['hook', 'first'], G], [['c1', 'body'], G], [['c1', 'stop'], R]], rizz=[['c1', 'body']],
   punch=[['hook', 'wait'], ['hook', 'giraffe'], ['hook', 'first'], ['hook', 'decision'], ['c1', 'communicate'], ['c1', 'body'], ['c1', 'towards'], ['c1', 'stop'], ['c1', 'contact']],
   blowouts=[['hook', 'first']], blackFlash=[['c1']], streaks=[['c1', 'but']]),
 'gddisgust': dict(top='Your brain can feel DISGUST… toward yourself', hl={'DISGUST…': '#FF2A2A'}, cta='*follow for more psychology*', music=['empire_n', 18.8], ctaAt=['c2', 'metacognition'],
   tints=[[['hook', 'reject'], R], [['c1', 'disgust'], R], [['c2', 'metacognition'], G]], rizz=[['c2', 'metacognition']],
   punch=[['hook', 'reject'], ['hook', 'ugly'], ['c1', 'guard'], ['c1', 'corrupt'], ['c1', 'disgust'], ['c1', 'distance'], ['c1', 'contaminate'], ['c2', 'brain'], ['c2', 'judging'], ['c2', 'metacognition'], ['c2', 'ugly'], ['c2', 'separate'], ['c2', 'integrity']],
   blowouts=[['hook', 'ugly']], blackFlash=[['c2']], streaks=[['c1', 'and']]),
 'gdeyecontact': dict(top="Looking away while you talk is NOT a bad sign", hl={'NOT': '#58EE28'}, cta='*follow for more body language*', music=['sentamento_n', 57.5], ctaAt=['c1', 'translate'],
   tints=[[['hook', 'normal'], G], [['c1', 'cognitively'], G], [['c2', 'eyes'], G]], rizz=[['hook', 'normal']],
   punch=[['hook', 'normal'], ['hook', 'away'], ['hook', 'absolutely'], ['c1', 'rehearsed'], ['c1', 'natural'], ['c1', 'cognitively'], ['c1', 'information'], ['c1', 'translate'], ['c2', 'end'], ['c2', 'back'], ['c2', 'eyes']],
   blowouts=[['hook', 'absolutely']], blackFlash=[['c1']], streaks=[['c2']]),
}
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
EXTRAS = {'gdgiraffe2': [png(['hook', 'giraffe'], 'emoji/1f440.png', 860, 1240), sfx(['hook', 'first'], 's_wow.mp3', 0.25), png(['c1', 'body'], 'emoji/1f9e0.png', 230, 1240)],
  'gddisgust': [png(['hook', 'ugly'], 'emoji/1f922.png', 860, 1240), sfx(['hook', 'reject'], 's_wow.mp3', 0.25), png(['c2', 'metacognition'], 'emoji/1f9e0.png', 230, 1240), sfx(['c2', 'metacognition'], 's_ding.mp3', 0.25)],
  'gdeyecontact': [png(['hook', 'away'], 'emoji/1f440.png', 860, 1240), sfx(['hook', 'absolutely'], 's_ding.mp3', 0.25), png(['c1', 'cognitively'], 'emoji/1f9e0.png', 230, 1240), png(['c2', 'eyes'], 'emoji/1f440.png', 860, 1240)]}
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

"""Dr. Guillaume Dulude batch 4 (eye movement interview, Himba tribe, reading the ground) (2026-11-23), original VverPaldo (Guess.tsx), 3-second rule: visual + audio + text hook.
lion (personal space, crouched near a lion), perfect (flawless = red flag; Tai Lopez intro cut), money (meaning does not come from money).
No colour grade (his footage already looks right) — only a light sharpen. Reaction emojis + SFX where they fit."""
import json, os, subprocess
G67 = "unsharp=5:5:0.8:3:3:0.3,format=yuv420p"
def F(y, z=1.8, x=960): return (x, z, y)
EDITS = {
 'gdeyes': ('eyecred', None, {'psychiatric': 'saccadic', 'psychedelic': 'saccadic'}, [
     ('hook', 17.75, 26.10, [(17.75, F(380)), (20.00, F(350, 2.1)), (22.40, F(400, 1.8)), (24.40, F(350, 2.1))]),
     ('c1', 0.00, 1.85, [(0.00, F(380))]),
     ('c2', 6.15, 17.70, [(6.15, F(380)), (10.40, F(350, 2.1)), (14.30, F(380))]),
     ('c3', 55.35, 57.40, [(55.35, F(350, 2.1))]),
     ('c4', 73.65, 89.70, [(73.65, F(380)), (78.70, F(350, 2.1)), (84.30, F(380))])]),
 'gdhimba': ('himba', (512, 572), {'humba': 'Himba'}, [
     ('hook', 27.15, 33.45, [(27.15, F(330)), (30.70, F(300, 2.1))]),
     ('c1', 2.85, 15.10, [(2.85, F(330)), (8.00, F(400, 1.8)), (11.80, F(330))]),
     ('c2', 18.55, 27.10, [(18.55, F(330)), (22.60, F(300, 2.1))]),
     ('c3', 33.65, 37.70, [(33.65, F(330))])]),
 'gdground': ('ground', (558, 612), {}, [
     ('hook', 24.25, 31.20, [(24.25, F(330)), (27.20, F(420, 1.8)), (29.00, F(300, 2.1))]),
     ('c1', 8.55, 23.40, [(8.55, F(330)), (14.70, F(300, 2.1)), (19.70, F(330))]),
     ('c2', 32.25, 46.95, [(32.25, F(330)), (37.40, F(300, 2.1)), (42.80, F(330))]),
     ('c3', 52.45, 66.20, [(52.45, F(330)), (56.30, F(300, 2.1)), (59.70, F(330))])]),
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
 'gdeyes': dict(top='This tiny eye movement can destroy your CREDIBILITY', hl={'CREDIBILITY': '#FF2A2A'}, cta='*follow for more body language*', music=['brevis_n', 36.0], ctaAt=['c4', 'notice'],
   tints=[[['hook', 'credibility'], R], [['c2', 'anxiety'], R], [['c4', 'avoidance'], G]], rizz=[['c1', 'saccadic']],
   punch=[['hook', 'fine'], ['hook', 'finished'], ['hook', 'lost'], ['hook', 'credibility'], ['c1', 'saccadic'], ['c2', 'anxiety'], ['c2', 'positive'], ['c3', 'avoidance'], ['c4', 'brain'], ['c4', 'avoidance'], ['c4', 'notice'], ['c4', 'kick']],
   blowouts=[['hook', 'credibility']], blackFlash=[['c4']], streaks=[['c2']]),
 'gdhimba': dict(top="Why this food had to go through the tribe's CHIEF first", hl={'CHIEF': '#58EE28'}, cta='*follow for more human behavior*', music=['empire_n', 18.8], ctaAt=['c2', 'authority'],
   tints=[[['hook', 'chief'], G], [['hook', 'hierarchy'], R], [['c1', '200'], G]], rizz=[['c1', '200']],
   punch=[['hook', 'chief'], ['hook', 'responsible'], ['hook', 'never'], ['hook', 'hierarchy'], ['c1', 'himba'], ['c1', 'namibia'], ['c1', '200'], ['c1', 'maize'], ['c2', 'works'], ['c2', 'authority'], ['c3', 'top'], ['c3', 'distributes']],
   blowouts=[['hook', 'hierarchy']], blackFlash=[['c2']], streaks=[['c1', 'so', 1]]),
 'gdground': dict(top='Early humans could read the ground like a STORY', hl={'STORY': '#58EE28'}, cta='*follow for more psychology*', music=['sentamento_n', 57.5], ctaAt=['c3', 'relationship'],
   tints=[[['hook', 'soil'], G], [['c1', 'dangerous'], R], [['c2', 'elimination'], G]], rizz=[['c2', 'tracks']],
   punch=[['hook', 'answer'], ['hook', 'rocks'], ['hook', 'soil'], ['hook', 'story'], ['c1', 'questions'], ['c1', '10,000'], ['c1', 'animals'], ['c1', 'dangerous'], ['c2', 'humans'], ['c2', 'tracks'], ['c2', 'elimination'], ['c3', 'recent'], ['c3', 'running'], ['c3', 'ground']],
   blowouts=[['hook', 'story']], blackFlash=[['c3']], streaks=[['c2']]),
}
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
EXTRAS = {'gdeyes': [png(['hook', 'fine'], 'emoji/1f440.png', 860, 1240), png(['hook', 'credibility'], 'emoji/1f62c.png', 230, 1240), sfx(['hook', 'lost'], 's_wow.mp3', 0.3), png(['c4', 'avoidance'], 'emoji/1f9e0.png', 860, 1240), sfx(['c4', 'kick'], 's_ding.mp3', 0.25)],
  'gdhimba': [png(['hook', 'chief'], 'emoji/1f451.png', 860, 1240), sfx(['hook', 'chief'], 's_ding.mp3', 0.25), png(['c1', '200'], 'emoji/1f633.png', 230, 1240), sfx(['hook', 'hierarchy'], 's_wow.mp3', 0.25)],
  'gdground': [png(['hook', 'story'], 'emoji/1f50d.png', 860, 1240), sfx(['hook', 'story'], 's_ding.mp3', 0.25), png(['c1', 'dangerous'], 'emoji/1f62c.png', 230, 1240), png(['c2', 'tracks'], 'emoji/1f440.png', 860, 1240), png(['c3', 'ground'], 'emoji/1f9e0.png', 860, 1240)]}
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

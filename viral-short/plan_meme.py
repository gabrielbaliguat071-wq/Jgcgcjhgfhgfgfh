"""Trevor x3 (Nov 17) in the new "meme clip" look (src/Meme.tsx) with the VverPaldo concept: payoff hook -> hard cut ->
story that loops into the hook. Crops are full-frame: (t, centre x, zoom, centre y) in 1920x1080 source px; zoom 1 shows a
607 px wide slice at full height; zoom < 1 = wide 16:9 band over a blurred copy (y = band centre in OUTPUT px).
Run from viral-short/: python3 plan_meme.py ../footage/src"""
import json, os, subprocess, sys
SRC = sys.argv[1]
G67 = ("split[ga][gb];[gb]gblur=sigma=14[gg];[ga][gg]blend=all_mode=softlight:all_opacity=0.245,unsharp=5:5:1.74:5:5:0,"
       "eq=contrast=1.113:saturation=1.26:gamma=0.98,curves=all='0/0 0.25/0.21 0.75/0.81 1/1',unsharp=3:3:0.79,format=yuv420p")
BAND = (960, 0.5, 830)
def tv(z=1.25): return (960, z, 500)        # Trevor
LH, RH = (470, 1.0, 540), (1480, 1.0, 540)  # left / right host, full height

EDITS = {
 'mrogers': ('v_rogers_realm', (0, 26.6), {}, [
     ('hook', 17.60, 20.58, [(17.60, BAND), (19.60, (520, 1.0, 540))]),
     ('c1', 0.00, 3.82, [(0.00, LH)]),
     ('c2', 3.96, 9.30, [(3.96, tv()), (6.20, tv(1.45))]),
     ('c3', 11.18, 17.06, [(11.18, BAND), (12.90, tv()), (14.40, BAND)])]),
 'mlair': ('v_lair', (0, 20.8), {(1.94, 'in'): 'and', (6.96, 'layer'): 'Lair', (12.76, 'rip'): 'open', (12.94, 'product'): 'packs'}, [
     ('hook', 14.20, 18.12, [(14.20, tv()), (16.70, tv(1.45))]),
     ('c1', 0.00, 5.52, [(0.00, BAND), (4.70, tv())]),
     ('c2', 5.66, 14.10, [(5.66, LH), (8.20, BAND), (10.00, tv()), (11.10, BAND), (12.36, LH)])]),
 'mcoen': ('u6_coen_duo', (0, 117), {(6.74, 'cohen'): 'Coen'}, [
     ('hook', 110.10, 114.30, [(110.10, tv()), (112.90, tv(1.45))]),
     ('c1', 4.70, 8.10, [(4.70, LH)]),
     ('c2', 11.40, 16.58, [(11.40, (470, 1.15, 520)), (14.20, BAND)]),
     ('c3', 18.30, 23.34, [(18.30, tv()), (21.20, tv(1.45))]),
     ('c4', 23.40, 27.90, [(23.40, BAND), (25.00, tv(1.3))])]),
}
gen = json.load(open('src/edits.gen.json'))
for eid, (src, (xa, xb), fix, plan) in EDITS.items():
    out = f'public/g67_{eid}.mp4'
    if not os.path.exists(out):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(xa), '-to', str(xb), '-i', f'{SRC}/{src}.mp4', '-vf', G67, '-c:v', 'libx264', '-crf', '17',
                        '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', out], check=True)
    W = [(w['startMs'] / 1000, w['endMs'] / 1000, w['text']) for w in json.load(open(f'../src/plans/data/{src}.words.json'))]
    scenes = []
    for sid, a, b, crops in plan:
        n = round((b - a) * 30); words = []
        for ws, we, t in W:
            if not (a - 0.05 <= ws < b - 0.05): continue
            k = t.lower().strip(',.?!'); hit = [v for (ft, fw), v in fix.items() if abs(ft - ws) < 0.03 and fw == k]
            t2 = hit[0] if hit else t
            if not t2: continue
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t2, 'startFrame': f0, 'endFrame': f1})
        for i in range(len(words) - 1, 0, -1):
            if words[i]['word'].startswith('-'): words[i - 1]['word'] += words[i]['word']; words.pop(i)
        cr = [[max(0, round((t - a) * 30)), x, z, y] for t, (x, z, y) in crops]
        scenes.append({'id': sid, 'videoStartSec': round(a - xa, 3), 'durationInFrames': n, 'cropX': 960, 'crops': cr, 'words': words})
    gen[eid] = scenes
    print(eid, round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's |', ' / '.join(s['id'] + ': ' + ' '.join(w['word'] for w in s['words']) for s in scenes))
json.dump(gen, open('src/edits.gen.json', 'w'))

G, R = 'G', 'R'
Y, GR, RD = '#FFE14D', '#5CFF5C', '#FF4D4D'
CFG = {
 'mrogers': dict(top='Jags fans vs Eagles fans got OUT OF HAND', hl={'OUT': '#E3201B', 'OF': '#E3201B', 'HAND': '#E3201B'}, label='TREVOR LAWRENCE · NFL QB',
   music=['dubist_n', 1.0], cta='WHO WINS THIS FIGHT?', ctaAt=['c3', 'we'],
   kw={'jags': Y, 'eagles': GR, 'philly': GR, 'insane': RD, 'nuts': RD, 'home': Y, 'box': RD, 'versus': RD, 'rogers': GR, 'traveling': Y, 'happen': GR, 'out': RD},
   emoji=[[['hook', 'versus'], '1f94a'], [['c1', 'eagles'], '1f985'], [['c2', 'insane'], '1f631'], [['c2', 'philly'], '1f62d'], [['c3', 'box'], '1f94a'], [['c3', 'oh'], '1f633']],
   tints=[[['hook', 'happen'], G], [['c2', 'philly'], R], [['c3', 'box'], R]],
   punch=[['hook', 'versus'], ['hook', 'happen'], ['c1', 'cheering'], ['c1', 'eagles'], ['c2', 'insane'], ['c2', 'home'], ['c2', 'philly'], ['c3', 'rogers'], ['c3', 'god'], ['c3', 'box'], ['c3', 'out']],
   sfx=[[['hook', 'happen'], 'm_air-horn.mp3', 0.0], [['c3', 'box'], 'm_oh-hell-nah.mp3', 0.35], [['c2', 'philly'], 'm_record-scratch.mp3', 0.35]]),
 'mlair': dict(top='Would an NFL QB REALLY come hang at their place?', hl={'REALLY': '#1DB954'}, label='TREVOR LAWRENCE · NFL QB',
   music=['blue_n', 21.5], cta='WOULD YOU INVITE HIM?', ctaAt=['c2', 'like'],
   kw={'always': GR, 'welcome': GR, 'jacksonville': Y, 'awesome': GR, 'envisioned': Y, 'honestly': GR, 'lair': Y, 'florida': Y, 'lauderdale': Y, 'chill': GR},
   emoji=[[['hook', 'awesome'], '1f91d'], [['hook', 'jacksonville'], '1f3c8'], [['c1', 'honestly'], '2764-fe0f-200d-1fa79'], [['c2', 'florida'], '1f3dd-fe0f'], [['c2', 'chill'], '1f60e']],
   tints=[[['hook', 'always'], G], [['c1', 'honestly'], G]],
   punch=[['hook', 'awesome'], ['hook', 'always'], ['hook', 'jacksonville'], ['c1', 'everything'], ['c1', 'enjoy'], ['c1', 'honestly'], ['c2', 'lair'], ['c2', 'florida'], ['c2', 'lauderdale'], ['c2', 'chill']],
   sfx=[[['c1', 'honestly'], 'm_anime-wow.mp3', 0.3]]),
 'mcoen': dict(top='His coach taught him more in 1 YEAR than his WHOLE CAREER', hl={'1': '#1DB954', 'YEAR': '#1DB954', 'WHOLE': '#E3201B', 'CAREER': '#E3201B'},
   label='TREVOR LAWRENCE · NFL QB', music=['sentamento_n', 57.0], cta='BEST COACH IN THE NFL?', ctaAt=['c4', 'different'],
   kw={'confidence': GR, 'snapped': Y, 'rip': RD, 'coen': GR, 'warner': Y, 'year': GR, 'life': RD, 'true': Y, 'definitely': GR, 'different': Y, 'staff': GR, 'system': Y},
   emoji=[[['hook', 'confidence'], '1f60e'], [['c1', 'coen'], '1f9e0'], [['c2', 'life'], '1f92f'], [['c2', 'true'], '1f914'], [['c3', 'definitely'], '1f4af'], [['c4', 'different'], '1f3c8']],
   tints=[[['hook', 'confidence'], G], [['c2', 'life'], R], [['c3', 'definitely'], G]],
   punch=[['hook', 'most'], ['hook', 'confidence'], ['hook', 'rip'], ['c1', 'coen'], ['c1', 'taught'], ['c2', 'year'], ['c2', 'life'], ['c2', 'true'], ['c3', 'definitely'], ['c3', 'year'], ['c4', 'different']],
   sfx=[[['c2', 'true'], 'm_record-scratch.mp3', 0.3]]),
}
for eid, c in CFG.items():
    c['src'] = f'g67_{eid}.mp4'
    c['sfx'] = [s for s in c['sfx'] if s[2] > 0]
    sc = {s['id']: s for s in gen[eid]}
    refs = [r for r, _ in c['tints']] + c['punch'] + [r for r, _ in c['emoji']] + [c['ctaAt']] + [s[0] for s in c['sfx']]
    for r in refs:
        ws = [w for w in sc[r[0]]['words'] if ''.join(ch for ch in w['word'].lower() if ch.isalnum() or ch in '$-').startswith(r[1])]
        assert len(ws) > (r[2] if len(r) > 2 else 0), (eid, r, [w['word'] for w in sc[r[0]]['words']])
    for e in [e for _, e in c['emoji']]: assert os.path.exists(f'public/res/emoji/{e}.png'), (eid, e)
json.dump(CFG, open('src/meme.cfg.json', 'w'), indent=1); print('cfg ok')

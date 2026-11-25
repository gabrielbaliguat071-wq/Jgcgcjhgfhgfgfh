"""Wa-Chaa batch 2 (2026-11-25): Kung-Fu Legends skits (Gerald Okamura, Evergreen folder). User: use the 'Everybody was kung fu fighting' meme sound ONLY on the old-master kung-fu clips → res/kungfu_n.mp3 (myinstants kung-fu-fightinggg, -23 LUFS, under the original audio). blurBg."""
import json, os, subprocess
G67 = "unsharp=5:5:0.6:3:3:0.2,format=yuv420p"
def F(y=330, z=1.8, x=960): return (x, z, y)
K = (960, 1.8, 560)
EDITS = {
 'wcchucks': ('chucks', {}, [
     ('hook', 6.00, 9.90, [(6.00, K), (7.20, (960, 2.1, 520))], [(6.0, 'what chucks??'), (6.9, 'SEE?!'), (7.2, 'what chucks??'), (9.4, 'SEE?!')]),
     ('c1', 0.00, 6.00, [(0.00, K), (2.00, (960, 2.0, 500)), (3.60, K)], [(0.05, 'INVISIBLE CHUCKS'), (2.1, 'what chucks?'), (4.3, 'who??'), (5.0, 'him.')]),
     ('c2', 9.90, 17.90, [(9.90, K)], [(9.95, 'see?!'), (11.0, 'what chucks'), (12.2, 'KUNG-FU LEGENDS'), (15.2, 'bag: opened')])]),
 'wcweapons': ('weapons', {}, [
     ('hook', 2.00, 4.00, [(2.00, (960, 1.8, 600))], [(2.05, 'PEANUT CRUSHER')]),
     ('c1', 4.00, 7.80, [(4.00, K), (5.40, (960, 2.1, 500))], [(4.05, 'hold up…'), (5.4, 'BONK'), (6.6, 'peanuts: crushed')]),
     ('c2', 10.00, 19.80, [(10.00, K), (12.0, (960, 2.0, 520)), (15.0, K)], [(10.05, 'NUNCHAKU!'), (12.0, 'for a snack bag??'), (15.0, 'bro is not playing'), (18.0, 'opened.')]),
     ('c3', 20.00, 27.00, [(20.00, K), (22.0, (960, 2.1, 480)), (24.5, K)], [(20.05, "DEVIL'S REVENGE"), (22.0, 'on a PEANUT bag'), (24.5, 'respect.')]),
     ('c4', 8.00, 9.80, [(8.00, K)], [(8.05, 'KUNG-FU LEGENDS')])]),
}
gen = json.load(open('src/edits.gen.json'))
for eid, (src, fix, plan) in EDITS.items():
    out = f'public/g67_{eid}.mp4'
    if not os.path.exists(out):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'../footage/wachaa/{src}.mp4', '-map', '0:v:0', '-map', '0:a:0', '-vf', f'scale=608:1080:flags=lanczos,pad=1920:1080:656:0:black,fps=30,{G67}',
                        '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-map_metadata', '-1', out], check=True)
    Wd = json.load(open(f'../footage/wachaa/{src}.words.json')) if os.path.exists(f'../footage/wachaa/{src}.words.json') else []
    scenes = []
    for sid, a, b, crops, chunks in plan:
        n = round((b - a) * 30); words = []
        if chunks is not None:
            for i, (t, txt) in enumerate(chunks):
                f0 = max(0, round((t - a) * 30)); f1 = round(((chunks[i + 1][0] if i + 1 < len(chunks) else b) - a) * 30)
                words.append({'word': txt, 'startFrame': f0, 'endFrame': min(n, max(f0 + 6, f1))})
        else:
            for w in Wd:
                ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
                if not (a - 0.05 <= ws < b - 0.05): continue
                t2 = fix.get(t.lower(), t); t2 = t2.strip(',.') if not t2.endswith(('?', '…')) else t2
                f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
                words.append({'word': t2, 'startFrame': f0, 'endFrame': f1})
            for i in range(len(words) - 1): words[i]['endFrame'] = max(words[i]['endFrame'], words[i + 1]['startFrame'])
        scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'cropX': 960,
                       'crops': [[max(0, round((t - a) * 30)), x, z, y] for t, (x, z, y) in crops], 'words': words})
    gen[eid] = scenes
    print(eid, round(sum(s['durationInFrames'] for s in scenes) / 30, 1), 's |', ' / '.join(s['id'] + ': ' + ' '.join(w['word'] for w in s['words']) for s in scenes))
json.dump(gen, open('src/edits.gen.json', 'w'))
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
G, R = 'G', 'R'
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
G, R = 'G', 'R'
CFG = {
 'wcchucks': dict(top='POV: he opens his snacks with INVISIBLE nunchucks', hl={'INVISIBLE': '#58EE28'}, cta='*would you trust him with your snacks?*', music=['kungfu_n', 0], ctaAt=['c2', 'KUNG-FU'],
   tints=[[['hook', 'SEE'], G], [['c1', 'INVISIBLE'], G]], rizz=[['c1', 'INVISIBLE']],
   punch=[['hook', 'what'], ['hook', 'SEE'], ['c1', 'INVISIBLE'], ['c1', 'who'], ['c2', 'see'], ['c2', 'KUNG-FU'], ['c2', 'bag']],
   blowouts=[['hook', 'SEE']], blackFlash=[['c2', 'KUNG-FU']], streaks=[['c1', 'what']],
   extras=[sfx(['hook', 'SEE'], 's_huh.mp3', 0.45), png(['hook', 'SEE'], 'emoji/1f602.png'), sfx(['c1', 'who'], 'm_record-scratch.mp3', 0.4), png(['c1', 'who'], 'emoji/1f914.png', 230, 1240),
           sfx(['c2', 'bag'], 'm_anime-wow.mp3', 0.4), png(['c2', 'bag'], 'emoji/1f525.png')]),
 'wcweapons': dict(top='This kung-fu master opens snacks with REAL weapons', hl={'REAL': '#FF2A2A'}, cta='*which weapon would you pick?*', music=['kungfu_n', 0], ctaAt=['c3', 'respect'],
   tints=[[['hook', 'PEANUT'], R], [['c2', 'NUNCHAKU'], G], [['c3', 'DEVIL'], R]], rizz=[['c2', 'NUNCHAKU']],
   punch=[['hook', 'PEANUT'], ['c1', 'BONK'], ['c1', 'peanuts'], ['c2', 'NUNCHAKU'], ['c2', 'for'], ['c2', 'bro'], ['c3', 'DEVIL'], ['c3', 'on'], ['c3', 'respect'], ['c4', 'KUNG-FU']],
   blowouts=[['c1', 'BONK']], blackFlash=[['c3', 'DEVIL']], streaks=[['c2', 'opened']],
   extras=[png(['hook', 'PEANUT'], 'emoji/1f633.png'), sfx(['c1', 'BONK'], 'm_mg-boom.mp3', 0.45), png(['c1', 'BONK'], 'emoji/1f480.png', 230, 1240), sfx(['c2', 'for'], 's_huh.mp3', 0.4),
           png(['c2', 'bro'], 'emoji/1f602.png'), sfx(['c3', 'on'], 'm_oh-hell-nah.mp3', 0.4), png(['c3', 'respect'], 'emoji/1f525.png', 230, 1240)]),
}
allc = json.load(open('src/yv.cfg.json'))
for eid, c in CFG.items():
    c.update(track='none', calls=[], intro=True, hardcut=True, cutSfx='s_camflash.mp3', src=f'g67_{eid}.mp4', blurBg=True)
    sc = {s['id']: s for s in gen[eid]}
    for r in [r for r, _ in c['tints']] + [r for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks') for r in c[k]] + [c['ctaAt']] + [e['at'] for e in c['extras']]:
        if len(r) == 1: continue
        assert [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())], (eid, r, [w['word'] for w in sc[r[0]]['words']])
    allc[eid] = c
json.dump(allc, open('src/yv.cfg.json', 'w'), indent=1); print('cfg ok')

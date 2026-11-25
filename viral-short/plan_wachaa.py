"""Wa-Chaa x The RZA — Grandmaster Collection (Clipping Culture, 2026-11-25). User: 'choose funny clips, make it short'.
Official folder f.io/LGgDvyP3 > 'Final Heat Reactions_Ad Content (Non-RZA)'. Original VverPaldo (Guess.tsx) + meme SFX/emojis, music allowed under original audio.
Vertical sources padded onto a 1920x1080 canvas (video 608x1080 at x 656), ~1.8x square crop. Never say RZA wrote it / RZA song (these clips don't mention RZA).
Caption tag: TikTok/IG @wachaaworldwide, YT @WACHAAWorldwide."""
import json, os, subprocess
G67 = "unsharp=5:5:0.6:3:3:0.2,format=yuv420p"
def F(y=330, z=1.8, x=960): return (x, z, y)
EDITS = {
 'wcmatthew': ('matthew', {'everyone\'s.': "everyone's…"}, [
     ('hook', 21.75, 28.05, [(21.75, F(320)), (25.0, F(300, 2.1))], None),
     ('c1', 10.55, 14.05, [(10.55, F(330))], None),
     ('c2', 15.75, 20.10, [(15.75, F(330)), (18.20, F(300, 2.1))], None),
     ('c3', 33.90, 37.45, [(33.90, F(330)), (34.90, F(300, 2.1))], None)]),
 'wcjp': ('jp', {'huachao': 'Wa-Chaa'}, [
     ('hook', 50.85, 54.60, [(50.85, F(300, 2.1))], None),
     ('c1', 4.45, 6.95, [(4.45, F(320))], None),
     ('c2', 15.65, 17.25, [(15.65, F(300, 2.1))], None),
     ('c3', 37.75, 42.65, [(37.75, F(320)), (40.70, F(300, 2.1))], None),
     ('c4', 45.15, 50.80, [(45.15, F(320)), (48.80, F(300, 2.1))], None)]),
 'wcchop': ('img4490', {}, [
     ('hook', 40.00, 42.60, [(40.00, F(330, 2.0))], [(40.05, 'one peanut…'), (41.2, 'NOT FINE')]),
     ('c1', 2.00, 6.00, [(2.00, F(420, 1.8))], [(2.05, 'wait…'), (3.0, 'GIANT chopsticks??')]),
     ('c2', 14.00, 20.00, [(14.00, F(330)), (16.0, F(310, 2.1))], [(14.05, 'ok just one'), (15.6, 'it\'s fine'), (17.5, 'it\'s… fine?')]),
     ('c3', 35.00, 40.00, [(35.00, F(330)), (37.0, F(310, 2.1))], [(35.05, 'the heat'), (36.4, 'is coming'), (38.0, 'uh oh')])]),
}
AUD = {'img4490': '0:2'}
gen = json.load(open('src/edits.gen.json'))
for eid, (src, fix, plan) in EDITS.items():
    out = f'public/g67_{eid}.mp4'
    if not os.path.exists(out):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'../footage/wachaa/{src}.mov', '-map', '0:v:0', '-map', AUD.get(src, '0:a:0'), '-vf', f'scale=608:1080:flags=lanczos,pad=1920:1080:656:0:black,fps=30,{G67}',
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
CFG = {
 'wcmatthew': dict(top='"So far it\'s fine"… 10 seconds later 💀', hl={'fine"…': '#58EE28'}, cta='*would you try Final Heat?*', music=['funkabn_n', 33.2], ctaAt=['c3', 'good'],
   tints=[[['hook', 'water'], R], [['c1', 'fine'], G], [['c2', 'tingling'], R]], rizz=[['c1', 'fine']],
   punch=[['hook', "can't"], ['hook', 'bottom'], ['hook', 'water'], ['c1', 'fine'], ['c2', 'lips'], ['c2', 'Wow'], ['c3', 'good'], ['c3', 'another']],
   blowouts=[['hook', 'water']], blackFlash=[['c2']], streaks=[['c3', 'But']],
   extras=[sfx(['hook', 'water'], 's_fahhh.mp3', 0.45), png(['hook', 'water'], 'emoji/1f62d.png'), sfx(['c1', 'everyone'], 'm_record-scratch.mp3', 0.4),
           sfx(['c2', 'Wow'], 'm_mg-boom.mp3', 0.45), png(['c2', 'Wow'], 'emoji/1f525.png', 230, 1240), sfx(['c3', 'another'], 's_huh.mp3', 0.35), png(['c3', 'another'], 'emoji/1f480.png')]),
 'wcjp': dict(top='"I grew up eating hot peppers"… then THIS 💀', hl={'THIS': '#FF2A2A'}, cta='*could you handle it?*', music=['phonk_n', 22.4], ctaAt=['c3', 'heat'],
   tints=[[['hook', 'sweating'], R], [['c1', 'peppers'], G], [['c4', 'lips'], R]], rizz=[['c1', 'peppers']],
   punch=[['hook', "can't"], ['hook', 'bottom'], ['hook', 'sweating'], ['c1', 'got'], ['c1', 'peppers'], ['c2', 'fine'], ['c3', 'heat'], ['c3', 'numbing'], ['c4', 'tingling'], ['c4', 'lips']],
   blowouts=[['hook', 'sweating']], blackFlash=[['c3']], streaks=[['c4']],
   extras=[sfx(['hook', 'sweating'], 'm_mg-boom.mp3', 0.45), png(['hook', 'sweating'], 'emoji/1f62d.png'), sfx(['c1', 'peppers'], 'm_rizz-sound-effect.mp3', 0.35), png(['c1', 'peppers'], 'emoji/1f60e.png', 230, 1240),
           sfx(['c2', 'fine'], 'm_record-scratch.mp3', 0.4), sfx(['c4', 'lips'], 's_fahhh.mp3', 0.4), png(['c4', 'lips'], 'emoji/1f480.png')]),
 'wcchop': dict(top='GIANT chopsticks… for ONE spicy peanut 💀', hl={'GIANT': '#58EE28', 'ONE': '#FF2A2A'}, cta='*would you try it?*', music=['montagem_n', 24.0], ctaAt=['c2', 'it\'s…'],
   tints=[[['hook', 'NOT'], R], [['c1', 'GIANT'], G], [['c3', 'uh'], R]], rizz=[['c1', 'GIANT']],
   punch=[['hook', 'NOT'], ['c1', 'GIANT'], ['c2', 'ok'], ['c2', "it's"], ['c3', 'the'], ['c3', 'uh']],
   blowouts=[['hook', 'NOT']], blackFlash=[['c3', 'uh']], streaks=[['c2']],
   extras=[sfx(['hook', 'NOT'], 'm_mg-boom.mp3', 0.45), png(['hook', 'NOT'], 'emoji/1f631.png'), sfx(['c1', 'GIANT'], 's_huh.mp3', 0.4), png(['c1', 'GIANT'], 'emoji/1f602.png', 230, 1240),
           sfx(['c3', 'uh'], 'm_oh-hell-nah.mp3', 0.45), png(['c3', 'uh'], 'emoji/1f480.png')]),
}
allc = json.load(open('src/yv.cfg.json'))
for eid, c in CFG.items():
    c.update(track='none', calls=[], intro=True, hardcut=True, cutSfx='s_camflash.mp3', src=f'g67_{eid}.mp4', noSkull=True)
    sc = {s['id']: s for s in gen[eid]}
    for r in [r for r, _ in c['tints']] + [r for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks') for r in c[k]] + [c['ctaAt']] + [e['at'] for e in c['extras']]:
        if len(r) == 1: continue
        assert [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())], (eid, r, [w['word'] for w in sc[r[0]]['words']])
    allc[eid] = c
json.dump(allc, open('src/yv.cfg.json', 'w'), indent=1); print('cfg ok')

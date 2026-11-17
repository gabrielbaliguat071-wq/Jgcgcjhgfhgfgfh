# R3born Ep2 "top 10" (Nov 17): the 10 strongest moments, rebuilt for retention + comments.
# - hook = wildest second (straight cut, no intro blur, so frame 1 is already the action); story; ending loops into the hook
# - cooler grade (67 + 9000 K, less saturation) - the old look was too orange
# - centre emoji pops (see-through, small->big, echo rings) + an echo-pop SFX on every pop; every overlay carries its own SFX
# - resource overlays: green flashes, cash fall, "a few moments later" insert, emojis, skull
# - comment prompt pill (ask) at the end + progress bar
# Excerpts public/g67_t<k>.mp4 = the edit's source windows concatenated; scenes carry their own window offset.
# Usage: python3 plan13.py <tx.json> <r3ep2.mp4> [--no-excerpts] [--only=a,b]
import ast, glob, json, subprocess, sys
W = [w for s in json.load(open(sys.argv[1])) for w in s['w']]
SRC = sys.argv[2]
ONLY = [x for a in sys.argv if a.startswith('--only=') for x in a[7:].split(',')]
TR = [(k, [tuple(c) for c in v['crops']]) for f in sorted(glob.glob('src/tracks/r3*/auto_edits.json')) for k, v in json.load(open(f)).items() if v['crops']]
FIX = {'neon': 'N3on', 'fuck': 'f***', 'fucking': 'f***ing', 'shitting': 'sh*tting', 'shit': 'sh*t', 'dumbass': 'dumba**'}
src8 = open('plan8.py').read(); ATW = ast.literal_eval(src8[src8.index('ATW = ') + 6: src8.index('\ndef crops')])
ATW.update({(419.3, 'to'): 'at', (419.5, 'ask'): 'a**', (418.1, 'the'): 'at the', (252.3, 'cuz'): "'cause", (259.7, 'one'): 'in one',
            (175.6, 'in'): '', (175.8, 'this'): '', (176.2, 'fucking'): '', (176.7, 'hard'): '',   # burned into the source already
            (450.4, 'i'): 'I', (222.5, 'you'): "You're", (222.9, 'look'): '', (450.5, 'should'): 'asked', (450.6, 'use'): '', (687.4, 'cuz'): "'cause", (698.8, 'burn'): 'burned',
            (448.2, 'you'): 'You', (722.9, 'bring'): 'Bring'})
G67 = ("split[ga][gb];[gb]gblur=sigma=14[gg];[ga][gg]blend=all_mode=softlight:all_opacity=0.245,unsharp=5:5:1.74:5:5:0,"
       "eq=contrast=1.113:saturation=1.26:gamma=0.98,curves=all='0/0 0.25/0.21 0.75/0.81 1/1',unsharp=3:3:0.79,"
       "colortemperature=temperature=10000,eq=saturation=0.92,format=yuv420p")
def crops(a, b):
    best = max(TR, key=lambda t: min(b, t[1][-1][0] + 2) - max(a, t[1][0][0]))
    k, cr = best
    if min(b, cr[-1][0] + 2) - max(a, cr[0][0]) <= 0: return [(a, 960)]
    c = [x for x in cr if a - 0.01 <= x[0] < b]; prev = [x for x in cr if x[0] <= a]
    first = prev[-1][1] if prev else (c[0][1] if c else 960)
    return [(a, first)] + [x for x in c if x[0] > a + 0.01]
G, R = 'G', 'R'
def pop(at, f, react=None, rv=0.45): return dict(at=at, kind='png', file=f, **({'sfx': react, 'sv': rv} if react else {}))
def ov(at, f, sfx, dur=34, sv=0.45): return dict(at=at, kind='ov', file=f, dur=dur, sfx=sfx, sv=sv)
def sfx(at, f, v=0.5): return dict(at=at, kind='sfx', file=f, v=v)
INS = lambda sid, f, d: (sid, 'insert', f, d)
E = {
 'tmoney': dict(scenes=[('hook', 258.20, 260.35), ('c1', 249.08, 257.30), ('c2', 258.20, 266.70)],
   top='She made HOW much in ONE night?!', hl={'HOW': R, 'ONE': R}, music=['aura_n', 0], ask=[['c2', 'three'], 'Is $3K a good night?'],
   tints=[[['hook', 'money'], G], [['c1', 'stripper'], R], [['c2', 'three'], G], [['c2', 'strip'], R]], rizz=[['c2', 'three']],
   punch=[['hook', 'most'], ['hook', 'money'], ['hook', 'night'], ['c1', '17'], ['c1', 'clarify'], ['c1', 'stripper'], ['c1', 'stripper', 1], ['c2', 'money'], ['c2', 'night'], ['c2', 'three'], ['c2', 'grand'], ['c2', 'sorry']],
   blowouts=[['c2', 'three']], blackFlash=[['c1', 'stripper', 1]], streaks=[['c2', 'what']],
   extras=[pop(['c1', 'stripper', 1], 'e_laugh.png', 's_ayo.mp3'), ov(['c2', 'three'], 'cashfall.mp4', 's_ding.mp3', 52), pop(['c2', 'sorry'], 'e_sob.png', 's_awk.mp3')]),
 'treveal': dict(scenes=[('hook', 745.80, 747.40), ('c1', 721.45, 728.70), ('c2', 730.15, 741.80)],
   top='Loser gets WAXED… who lost?', hl={'WAXED': R}, music=['suspense_n', 0], ask=[['c2', '389'], 'Would YOU take this bet?'],
   tints=[[['hook', 'hot'], R], [['c2', '326'], G], [['c2', '389'], R], [['c2', 'calf'], R]], rizz=[['c2', '326']],
   punch=[['hook', 'f***ing'], ['hook', 'hot'], ['c1', 'won'], ['c1', 'phones'], ['c1', 'grand'], ['c1', 'total'], ['c2', '326'], ['c2', 'dumba**'], ['c2', '389'], ['c2', 'eyebrow'], ['c2', 'calf']],
   blowouts=[['c2', '389']], blackFlash=[['c2', '389']], streaks=[['c1', 'phones']],
   extras=[pop(['c2', '326'], 'e_laugh.png', 's_huh.mp3'), ov(['c2', '389'], 'greenflash2.mp4', 's_wow.mp3'), pop(['c2', 'calf'], 'e_sob.png', 's_fahhh.mp3')]),
 'tpole': dict(scenes=[('hook', 353.20, 355.75), ('c1', 333.90, 340.40), ('c2', 349.34, 355.80)],
   top='N3on tried POLE dancing', hl={'POLE': R}, music=['phonk_n', 40], ask=[['c2', 'just'], 'Rate his spin 1-10'],
   tints=[[['hook', 'stop'], R], [['c1', 'stupid'], R], [['c1', 'spins'], G], [['c2', 'whoa'], R]], rizz=[['c1', 'spins']],
   punch=[['hook', 'whoa'], ['hook', 'stop'], ['hook', 'stop', 1], ['hook', 'stop', 2], ['c1', 'hard'], ['c1', 'stupid'], ['c1', 'stupid', 1], ['c1', 'great'], ['c1', 'spins'], ['c2', 'pole'], ['c2', 'whoa'], ['c2', 'stop'], ['c2', 'stop', 2]],
   blowouts=[['c2', 'whoa']], blackFlash=[['c2', 'stop', 2]], streaks=[['c2', 'your']],
   extras=[pop(['c1', 'stupid', 1], 'e_laugh.png', 's_huh.mp3'), ov(['c1', 'spins'], 'greenflash.mp4', 's_correct.mp3'), pop(['c2', 'stop', 2], 'e_sob.png', 's_fahhh.mp3')]),
 'trip': dict(scenes=[('hook', 759.85, 762.60), ('c1', 750.90, 756.00), ('c2', 759.20, 767.40)],
   top='He said "sue me"… then THIS', hl={'THIS': R}, music=['empire_n', 20], ask=[['c2', 'wow'], 'Would you let her wax you?'],
   tints=[[['c1', 'hard'], R], [['c1', 'lawyers'], G], [['c2', 'one'], R], [['c2', 'wow'], G]], rizz=[['c1', 'lawyers']],
   punch=[['c1', 'hard'], ['c1', 'check'], ['c1', 'touch'], ['c1', 'sue'], ['c1', 'sue', 1], ['c1', 'lawyers'], ['c2', 'two'], ['c2', 'one'], ['c2', 'wow'], ['c2', 'good']],
   blowouts=[['c2', 'one']], blackFlash=[['c2', 'one']], streaks=[['c1', 'let']],
   extras=[pop(['c1', 'touch'], 'e_laugh.png', 's_ayo.mp3'), pop(['c2', 'one'], 'skull.png', 's_fahhh.mp3'), ov(['c2', 'wow'], 'greenflash2.mp4', 's_nice.mp3')]),
 'tsus': dict(scenes=[('hook', 175.50, 177.05), ('c1', 170.30, 177.05), ('c2', 528.60, 535.40)],
   top='This workout got SUS real quick', hl={'SUS': R}, music=['brega_n', 0], ask=[['c2', 'yep'], 'What did YOU hear?'],
   tints=[[['c1', 'between'], R], [['c1', 'kneel'], R], [['c2', 'hips'], R], [['c2', 'arch'], R]], rizz=[['c1', 'thigh'], ['c2', 'forward']],
   punch=[['c1', 'ball'], ['c1', 'between'], ['c1', 'thigh'], ['c1', 'kneel'], ['c1', 'down'], ['c2', 'rock'], ['c2', 'push'], ['c2', 'hips'], ['c2', 'forward'], ['c2', 'backbend'], ['c2', 'arch']],
   blowouts=[['c2', 'arch']], blackFlash=[['c1', 'down']], streaks=[['c2', 'now']],
   extras=[pop(['c1', 'thigh'], 'e_laugh.png', 's_twitch.mp3'), sfx(['c1', 'down'], 's_huh.mp3'), pop(['c2', 'hips'], 'skull.png', 's_ayo.mp3'), sfx(['c2', 'arch'], 's_twitch.mp3')]),
 'tcheat': dict(scenes=[('hook', 684.80, 686.10), ('c1', 639.45, 642.70), INS('afml', 'afml.mp4', 2.2), ('c2', 659.20, 661.80), ('c3', 677.00, 679.50),
                         ('c4', 684.80, 692.20), ('c5', 694.00, 694.95), ('c6', 697.75, 701.80)],
   top='N3on said he had to use the BATHROOM…', hl={'BATHROOM…': R}, music=['funkabn_n', 4], ask=[['c6', "there's"], 'Cheating or genius?'],
   tints=[[['hook', 'f***'], R], [['c1', 'restroom'], G], [['c4', 'calories'], R], [['c6', 'sue'], R]], rizz=[['c1', 'restroom']],
   punch=[['hook', 'f***'], ['hook', 'doing'], ['c1', '50'], ['c1', 'restroom'], ['c4', 'f***'], ['c4', 'tired'], ['c4', 'burn'], ['c4', 'calories'], ['c5', 'sorry'], ['c6', 'no'], ['c6', '50'], ['c6', 'sue']],
   blowouts=[['c4', 'calories']], blackFlash=[['c4', 'what']], streaks=[['c2'], ['c3'], ['c6']],
   extras=[pop(['c1', 'restroom'], 'e_laugh.png', 's_ahh.mp3'), sfx(['c2'], 's_loading.mp3', 0.4), ov(['c4', 'calories'], 'greenflash2.mp4', 's_wow.mp3'),
           pop(['c5', 'sorry'], 'e_sob.png', 's_awk.mp3'), pop(['c6', 'sue'], 'skull.png', 's_fahhh.mp3')]),
 'tpilates': dict(scenes=[('hook', 214.90, 216.70), ('c1', 208.80, 216.70), ('c2', 216.70, 223.95)],
   top='N3on burned 103 calories doing Pilates…', hl={'103': R}, music=['sentamento_n', 55], ask=[['c2', 'close'], 'Could YOU beat 103?'],
   tints=[[['hook', '103'], R], [['c1', 'embarrassing'], R], [['c2', '161'], G], [['c2', 'close', 1], R]], rizz=[['c2', '161']],
   punch=[['hook', '103'], ['hook', 'impossible'], ['c1', 'calories'], ['c1', 'embarrassing'], ['c1', 'malfunction'], ['c1', '103'], ['c1', 'impossible'], ['c2', 'generous'], ['c2', '161'], ['c2', 'close'], ['c2', '60']],
   blowouts=[['c2', '161']], blackFlash=[['c1', 'embarrassing']], streaks=[['c2']],
   extras=[pop(['c1', 'embarrassing'], 'e_laugh.png', 's_huh.mp3'), pop(['c1', 'impossible'], 'e_sob.png', 's_fahhh.mp3'), ov(['c2', '161'], 'greenflash2.mp4', 's_correct.mp3')]),
 'thand': dict(scenes=[('hook', 386.00, 388.90), ('c1', 379.60, 388.90), ('c2', 397.85, 402.20)],
   top='N3on tried a HANDSTAND', hl={'HANDSTAND': R}, music=['xcool_n', 0], ask=[['c2', 'trusted'], 'Stripper or Sarah?'],
   tints=[[['hook', 'butt'], R], [['c1', 'kick'], G], [['c1', 'nothing'], R], [['c2', 'stripper'], R]], rizz=[['c1', 'kick']],
   punch=[['hook', 'butt'], ['hook', 'nothing'], ['c1', 'push'], ['c1', 'kick'], ['c1', 'tuck'], ['c1', 'butt'], ['c1', 'nothing'], ['c2', 'again'], ['c2', 'no'], ['c2', 'stripper'], ['c2', 'sarah']],
   blowouts=[['c2', 'sarah']], blackFlash=[['c1', 'nothing']], streaks=[['c2']],
   extras=[pop(['c1', 'butt'], 'e_laugh.png', 's_ayo.mp3'), sfx(['c1', 'nothing'], 's_huh.mp3'), pop(['c2', 'stripper'], 'skull.png', 's_awk.mp3')]),
 'tclub': dict(scenes=[('hook', 418.00, 420.30), ('c1', 416.30, 429.95)],
   top='N3on admitted what he REALLY looks at', hl={'REALLY': R}, music=['montagem_n', 25], ask=[['c1', 'salute'], 'Is he wrong though?'],
   tints=[[['hook', 'a**'], R], [['c1', 'club'], R], [['c1', 'technique'], G], [['c1', 'him'], R]], rizz=[['c1', 'technique']],
   punch=[['hook', 'strip'], ['hook', 'a**'], ['c1', 'hard'], ['c1', 'strip'], ['c1', 'a**'], ['c1', 'technique'], ['c1', 'salute'], ['c1', 'him'], ['c1', 'brother']],
   blowouts=[['c1', 'a**']], blackFlash=[['c1', 'him']], streaks=[['c1', 'this', 1]],
   extras=[pop(['c1', 'a**'], 'e_laugh.png', 's_ayo.mp3'), ov(['c1', 'salute'], 'greenflash.mp4', 's_nice.mp3'), pop(['c1', 'him'], 'skull.png', 's_huh.mp3')]),
 'tgpt': dict(scenes=[('hook', 450.30, 453.20), ('c1', 431.40, 439.70), ('c2', 441.40, 444.00), ('c3', 448.15, 457.40)],
   top="N3on's ChatGPT excuse is CRAZY", hl={'CRAZY': R}, music=['alquimia_n', 0], ask=[['c3', 'oh'], 'Do men REALLY burn more?'],
   tints=[[['hook', 'men'], R], [['c1', '50'], R], [['c1', 'crushed'], G], [['c3', 'woman'], R]], rizz=[['c1', 'crushed']],
   punch=[['hook', 'ChatGPT'], ['hook', 'men'], ['c1', 'calories'], ['c1', 'hundred'], ['c1', '50'], ['c1', 'crushed'], ['c2', 'women'], ['c3', 'genes'], ['c3', 'woman'], ['c3', 'ChatGPT'], ['c3', 'men'], ['c3', 'comeback'], ['c3', 'LeBron']],
   blowouts=[['c1', 'crushed']], blackFlash=[['c3', 'woman']], streaks=[['c2'], ['c3']],
   extras=[pop(['c1', '50'], 'e_sob.png', 's_fahhh.mp3'), ov(['c1', 'crushed'], 'greenflash2.mp4', 's_wow.mp3'), pop(['c3', 'woman'], 'e_laugh.png', 's_ayo.mp3'), pop(['c3', 'LeBron'], 'skull.png', 's_huh.mp3')]),
}
gen = json.load(open('src/edits.gen.json')); CFG = {}
for eid, spec in E.items():
    # source windows: merge the scenes' ranges (pad 0.2 s), concatenated into one graded excerpt
    rng = sorted((a - 0.2, b + 0.2) for sid, a, b, *_ in spec['scenes'] if a != 'insert')
    win = []
    for a, b in rng:
        if win and a <= win[-1][1] + 1.0: win[-1][1] = max(win[-1][1], b)
        else: win.append([a, b])
    offs, t = [], 0.0
    for a, b in win: offs.append((a, b, t)); t += b - a
    scenes = []
    for sc in spec['scenes']:
        if sc[1] == 'insert':
            scenes.append({'id': sc[0], 'videoStartSec': 0, 'durationInFrames': round(sc[3] * 30), 'cropX': 960, 'crops': [[0, 960]], 'insert': sc[2], 'words': []}); continue
        sid, a, b = sc; n = round((b - a) * 30); words = []
        wa, wb, wt = next(o for o in offs if o[0] <= a and b <= o[1])
        for (ws, we, tx) in W:
            if a - 0.05 <= ws < b - 0.05:
                k = (round(ws, 1), tx.lower().strip(',.?!')); tt = ATW[k] if k in ATW else FIX.get(tx.lower().strip(',.?!'), tx.strip(',.'))
                if not tt: continue
                f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
                words.append({'word': tt, 'startFrame': f0, 'endFrame': f1})
        for i in range(len(words) - 1): words[i]['endFrame'] = min(words[i]['endFrame'], words[i + 1]['startFrame'])
        cr = crops(a, b)
        scenes.append({'id': sid, 'videoStartSec': round(a - wa + wt, 3), 'durationInFrames': n, 'cropX': cr[0][1], 'crops': [[round((s - a) * 30), x] for s, x in cr], 'words': words})
    gen[eid] = scenes
    print(eid, round(sum(s['durationInFrames'] for s in scenes) / 30, 1), 's |', ' / '.join(s['id'] + ': ' + ' '.join(w['word'] for w in s['words']) for s in scenes))
    if '--no-excerpts' not in sys.argv and (not ONLY or eid in ONLY):
        cmd = ['ffmpeg', '-v', 'error', '-y']; fc = []
        for i, (a, b, _) in enumerate(offs):
            cmd += ['-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', SRC]
            fc.append(f'[{i}:v]fps=30,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1,format=yuv420p[v{i}]')
            fc.append(f'[{i}:a]asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{b - a:.3f}[a{i}]')
        fc.append(''.join(f'[v{i}][a{i}]' for i in range(len(offs))) + f'concat=n={len(offs)}:v=1:a=1[cv][ca]'); fc.append('[cv]' + G67 + '[gv]')
        subprocess.run(cmd + ['-filter_complex', ';'.join(fc), '-map', '[gv]', '-map', '[ca]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
                              '-g', '15', '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', f'public/g67_{eid}.mp4'], check=True)
    c = {k: v for k, v in spec.items() if k != 'scenes'}
    c['hl'] = {w: ('#FF2A2A' if col == R else '#58EE28') for w, col in c['hl'].items()}
    c.update(cta='*full episode on @HardScope*', ctaAt=c['ask'][0], ask={'at': c['ask'][0], 'text': c['ask'][1]}, track='none', calls=[], src=f'g67_{eid}.mp4',
             intro=False, hardcut=True, cutSfx='s_camflash.mp3', sat=1.1, progress=True, popMid=True)
    sc = {s['id']: s for s in scenes}
    refs = [r for r, _ in c['tints']] + [c['ctaAt']] + [e['at'] for e in c['extras']] + sum((c[k] for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks')), [])
    for r in refs:
        assert r[0] in sc, (eid, r)
        if len(r) == 1: continue
        ws = [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())]
        assert len(ws) > (r[2] if len(r) > 2 else 0), (eid, r, [w['word'] for w in sc[r[0]]['words']])
    for e in c['extras']: assert e['kind'] in ('sfx', 'png') or e.get('sfx'), (eid, 'overlay without SFX', e)   # pngs get the echo-pop automatically
    CFG[eid] = c
json.dump(gen, open('src/edits.gen.json', 'w'))
json.dump(CFG, open('src/r3t.cfg.json', 'w'), indent=1); print('cfg ok')

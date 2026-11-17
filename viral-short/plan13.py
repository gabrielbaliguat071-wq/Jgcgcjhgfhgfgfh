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
def pop(at, f, react=None, rv=0.45, off=0, after=False): return dict(at=at, kind='png', file=f, off=off, after=after, **({'sfx': react, 'sv': rv} if react else {}))
def ov(at, f, sfx, dur=34, sv=0.45): return dict(at=at, kind='ov', file=f, dur=dur, sfx=sfx, sv=sv)
def sfx(at, f, v=0.5): return dict(at=at, kind='sfx', file=f, v=v)
INS = lambda sid, f, d: (sid, 'insert', f, d)
def txt(at, text, color='#58EE28', size=150, off=0, y=None, dur=30, after=False): return dict(at=at, kind='txt', file=text, color=color, size=size, off=off, dur=dur, after=after, **({'y': y} if y else {}))
Y = '#FFE14A'; W_ = '#FFFFFF'
UI = (1.18, 560)
E = {
 'tmoney': dict(scenes=[('hook', 258.20, 260.35), ('c1', 261.38, 262.95), ('c2', 263.48, 266.70), ('c3', 252.05, 257.00)],
   top='She made HOW much in ONE night?!', hl={'HOW': R, 'ONE': R}, sub='She teaches pole dancing for a living', music=['aura_n', 0],
   ask=[[['hook'], 'Would YOU do it for $3K?']],
   tints=[[['c1', 'three'], G], [['c2', 'strip'], R], [['c3', 'stripper', 1], R]], rizz=[['c1', 'three']],
   punch=[['hook', 'most'], ['hook', 'money'], ['hook', 'night'], ['c1', 'three'], ['c1', 'grand'], ['c2', 'strip'], ['c2', 'sorry'], ['c3', 'stripper'], ['c3', 'stripper', 1]],
   blowouts=[['c1', 'three']], blackFlash=[], streaks=[['c3']],
   extras=[ov(['c1', 'three'], 'cashfall.mp4', 's_ding.mp3', 52), txt(['c1', 'three'], '$3,000', off=4), pop(['c2', 'dancing'], 'e_laugh.png', 's_huh.mp3', after=True),
           pop(['c3', 'stripper', 1], 'skull.png', 's_ayo.mp3', after=True)]),
 'treveal': dict(scenes=[('c1', 726.40, 731.90), ('c2', 732.40, 737.75), ('c3', 741.00, 741.85), ('c4', 759.85, 763.60)],
   top='Loser gets WAXED… who lost?', hl={'WAXED': R}, sub='Bet: most calories burned wins', music=['suspense_n', 0],
   ask=[[['c1'], 'Who wins? Guess'], [['c4'], 'Rate his pain 1-10']],
   tints=[[['c1', '326'], G], [['c2', '389'], R]], rizz=[['c1', '326']],
   punch=[['c1', 'grand'], ['c1', '326'], ['c2', '389'], ['c3', 'calf']],
   blowouts=[['c2', '389']], blackFlash=[], streaks=[['c3'], ['c4']],
   extras=[txt(['c1'], 'CALORIES BURNED', color=Y, size=72, y=560, dur=80), txt(['c1', '326'], '326', off=2), ov(['c2', '389'], 'greenflash2.mp4', 's_wow.mp3'),
           txt(['c2', '389'], '389', color='#FF2A2A', off=2), txt(['c4'], 'RIIIP', color='#FF2A2A', size=170, y=560, off=10, dur=34), sfx(['c4'], 's_rip.mp3', 0.6) | {'off': 10},
           pop(['c4'], 'e_sob.png', 's_fahhh.mp3', off=80)]),
 'tpole': dict(scenes=[('hook', 353.20, 354.10), ('rw', 'rewind', 354.10, 336.40, 12), ('c1', 336.40, 338.85), ('c2', 351.30, 356.90)], zoom={'hook': UI, 'c2': UI},
   top='His first pole class went…', hl={'pole': R}, sub='First time ever on a pole', music=['phonk_n', 40],
   ask=[[['c2'], 'Rate his spin 1-10']],
   tints=[[['c2', 'oh'], R]], rizz=[],
   punch=[['hook', 'whoa'], ['c1', 'stupid'], ['c1', 'stupid', 1], ['c1', 'great'], ['c2', 'whoa'], ['c2', 'stop'], ['c2', 'stop', 2], ['c2', 'oh']],
   blowouts=[], blackFlash=[], streaks=[['c2']],
   extras=[txt(['rw'], 'HOW IT STARTED', color=W_, size=90, y=560, dur=45), txt(['c2', 'oh'], 'SHE HAD TO CATCH HIM', color=Y, size=80, y=560, dur=40), sfx(['c2', 'oh'], 'shock.mp3', 0.5),
           pop(['c2', 'oh'], 'e_laugh.png', 's_huh.mp3', off=14)]),
 'trip': dict(scenes=[('c1', 753.00, 756.00), ('c2', 759.20, 762.20), ('c3', 764.85, 766.45)],
   top='"I got good lawyers"… then THIS', hl={'THIS': R}, sub='He lost the bet. Loser gets waxed.', music=['empire_n', 20],
   ask=[[['c1'], 'Rate his pain 1-10']],
   tints=[[['c1', 'sue'], R], [['c1', 'lawyers'], G]], rizz=[['c1', 'lawyers']],
   punch=[['c1', 'touch'], ['c1', 'sue'], ['c1', 'sue', 1], ['c1', 'lawyers'], ['c2', 'two'], ['c2', 'one']],
   blowouts=[], blackFlash=[], streaks=[['c2']],
   extras=[pop(['c1', 'lawyers'], 'e_laugh.png', 's_ayo.mp3', after=True), txt(['c2', 'one'], 'RIIIP', color='#FF2A2A', size=170, y=560, off=17, dur=34), sfx(['c2', 'one'], 's_rip.mp3', 0.6) | {'off': 17}]),
 'tsus': dict(scenes=[('c1', 171.20, 174.45), ('c2', 531.30, 537.60)],
   top='This workout got SUS real quick', hl={'SUS': R}, sub='Just Pilates instructions… right?', music=['brega_n', 0],
   ask=[[['c1'], 'Pilates or…?']],
   tints=[[['c1', 'between'], R], [['c2', 'hips'], R]], rizz=[['c1', 'thigh']],
   punch=[['c1', 'ball'], ['c1', 'between'], ['c1', 'thigh'], ['c2', 'push'], ['c2', 'hips'], ['c2', 'forward'], ['c2', 'arch'], ['c2', 'hard']],
   blowouts=[['c2', 'arch']], blackFlash=[], streaks=[['c2']],
   extras=[txt(['c1', 'inner'], 'INNER THIGH', color=Y, size=110, y=560, dur=36), sfx(['c1', 'inner'], 's_twitch.mp3'), pop(['c1', 'thigh'], 'e_laugh.png', 's_huh.mp3', after=True),
           txt(['c2', 'hips'], 'HIPS FORWARD', color=Y, size=110, y=560, dur=36), pop(['c2', 'arch'], 'skull.png', 's_ayo.mp3', after=True), sfx(['c2', 'hard'], 's_twitch.mp3')]),
 'tcheat': dict(scenes=[('hook', 684.80, 686.10), ('c1', 639.45, 642.70), INS('afml', 'afml.mp4', 0.8), ('c2', 659.20, 661.80),
                        ('c4', 690.55, 692.20), ('c5', 694.00, 694.95), ('c6', 697.75, 701.80)],
   top='He said he had to use the BATHROOM…', hl={'BATHROOM…': R}, sub='Bet: most calories burned wins', music=['funkabn_n', 4],
   ask=[[['hook'], 'Cheating or genius?']],
   tints=[[['hook', 'f***'], R], [['c1', 'restroom'], G], [['c4', 'calories'], R]], rizz=[['c1', 'restroom']],
   punch=[['hook', 'f***'], ['hook', 'doing'], ['c1', '50'], ['c1', 'restroom'], ['c4', 'burn'], ['c4', 'calories'], ['c5', 'sorry'], ['c6', 'no'], ['c6', '50'], ['c6', 'sue']],
   blowouts=[], blackFlash=[], streaks=[['c2'], ['c6']],
   extras=[txt(['c1', '50'], "HE'S DOWN 50 CALORIES", color=Y, size=80, y=560, dur=36), pop(['c1', 'restroom'], 'e_laugh.png', 's_ahh.mp3', after=True), sfx(['c2'], 's_loading.mp3', 0.4),
           txt(['c2'], 'SECRET WORKOUT', color=Y, size=90, y=560, dur=60), ov(['c4', 'calories'], 'greenflash2.mp4', 's_wow.mp3'), pop(['c6', 'sue'], 'skull.png', 's_fahhh.mp3', after=True)]),
 'tpilates': dict(scenes=[('c1', 214.90, 216.70), ('c2', 216.70, 223.95)],
   top='He burned 103 calories doing Pilates…', hl={'103': R}, sub='Then she checked HER watch…', music=['sentamento_n', 55],
   ask=[[['c1'], 'Malfunction or excuse?']],
   tints=[[['c1', '103'], R], [['c2', '161'], G]], rizz=[['c2', '161']],
   punch=[['c1', '103'], ['c1', 'impossible'], ['c2', 'generous'], ['c2', '161'], ['c2', 'close'], ['c2', '60']],
   blowouts=[['c2', '161']], blackFlash=[], streaks=[['c2']],
   extras=[txt(['c1', '103'], '103', color='#FF2A2A', off=2), pop(['c1', 'impossible'], 'e_sob.png', 's_huh.mp3', after=True), txt(['c2', '161'], '161', off=2),
           ov(['c2', '161'], 'greenflash2.mp4', 's_correct.mp3'), pop(['c2', 'close', 1], 'e_laugh.png', 's_awk.mp3', after=True)]),
 'thand': dict(scenes=[('c1', 384.84, 388.90), ('c2', 397.90, 402.20)], eq='eq=brightness=0.05:gamma=1.22',
   top='She ROASTED him mid-handstand', hl={'ROASTED': R}, sub='Coach 1: Sarah. Coach 2: a former stripper.', music=['xcool_n', 0],
   ask=[[['c1'], 'Rate that roast 1-10']],
   tints=[[['c1', 'butt'], R], [['c2', 'stripper'], R]], rizz=[],
   punch=[['c1', 'tuck'], ['c1', 'butt'], ['c1', 'nothing'], ['c2', 'help'], ['c2', 'again'], ['c2', 'stripper'], ['c2', 'sarah']],
   blowouts=[], blackFlash=[], streaks=[['c2']],
   extras=[pop(['c1', 'at'], 'e_laugh.png', 's_ayo.mp3', after=True), pop(['c2', 'sarah'], 'skull.png', 's_awk.mp3', after=True)]),
 'tclub': dict(scenes=[('c1', 416.30, 425.70)],
   top='He admitted what he REALLY looks at', hl={'REALLY': R}, sub='After his first pole class', music=['montagem_n', 25],
   ask=[[['c1'], 'Is he wrong though?']],
   tints=[[['c1', 'a**'], R], [['c1', 'salute'], G]], rizz=[['c1', 'salute']],
   punch=[['c1', 'hard'], ['c1', 'strip'], ['c1', 'a**'], ['c1', 'technique'], ['c1', 'salute']],
   blowouts=[], blackFlash=[], streaks=[],
   extras=[pop(['c1', 'technique'], 'e_laugh.png', 's_ayo.mp3', after=True), ov(['c1', 'salute'], 'greenflash.mp4', 's_nice.mp3'), pop(['c1', 'teaching'], 'skull.png', 's_huh.mp3', after=True)]),
 'tgpt': dict(scenes=[('hook', 450.30, 453.20), ('c1', 436.28, 439.70), ('c2', 441.40, 444.00), ('c3', 448.15, 450.30), ('c4', 455.00, 457.45)],
   zoom={'c1': (1.3, 420), 'hook': (1.22, 560), 'c3': (1.22, 560)},
   top='His excuse for losing is CRAZY', hl={'CRAZY': R}, sub='She burned 100. He burned 50.', music=['alquimia_n', 0],
   ask=[[['hook'], 'Do men REALLY burn more?']],
   tints=[[['hook', 'men'], R], [['c1', 'crushed'], G], [['c3', 'woman'], R]], rizz=[['c1', 'crushed']],
   punch=[['hook', 'ChatGPT'], ['hook', 'men'], ['c1', '50'], ['c1', 'crushed'], ['c2', 'women'], ['c3', 'genes'], ['c3', 'woman'], ['c4', 'comeback'], ['c4', 'LeBron']],
   blowouts=[], blackFlash=[], streaks=[['c2'], ['c3']],
   extras=[txt(['c1', '50'], '50', color='#FF2A2A', off=2), ov(['c1', 'crushed'], 'greenflash2.mp4', 's_wow.mp3'), pop(['c1', 'man'], 'e_sob.png', 's_fahhh.mp3', after=True),
           pop(['c3', 'woman'], 'e_laugh.png', 's_ayo.mp3', after=True), pop(['c4', 'James'], 'skull.png', 's_huh.mp3', after=True)]),
}

gen = json.load(open('src/edits.gen.json')); CFG = {}
for eid, spec in E.items():
    # source windows: merge the scenes' ranges (pad 0.2 s), concatenated into one graded excerpt
    rng = sorted((a - 0.2, b + 0.2) for sid, a, b, *_ in spec['scenes'] if a not in ('insert', 'rewind'))
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
        if sc[1] == 'rewind':
            xs = lambda t: next(t - o[0] + o[2] for o in offs if o[0] <= t <= o[1])
            scenes.append({'id': sc[0], 'videoStartSec': round(xs(sc[3]), 3), 'durationInFrames': sc[4], 'cropX': 960, 'crops': [[0, 960]], 'rewind': [round(xs(sc[2]), 3), round(xs(sc[3]), 3)], 'words': []}); continue
        sid, a, b = sc; n = round((b - a) * 30); words = []
        wa, wb, wt = next(o for o in offs if o[0] <= a and b <= o[1])
        for (ws, we, tx) in W:
            if a - 0.05 <= ws < b - 0.05:
                k = (round(ws, 1), tx.lower().strip(',.?!')); tt = ATW[k] if k in ATW else FIX.get(tx.lower().strip(',.?!'), tx.strip(',.'))
                if not tt: continue
                f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
                words.append({'word': tt, 'startFrame': f0, 'endFrame': f1})
        for i in range(len(words) - 1): words[i]['endFrame'] = min(words[i]['endFrame'], words[i + 1]['startFrame'])
        cr = crops(a, b); z = spec.get('zoom', {}).get(sid)
        scenes.append({'id': sid, 'videoStartSec': round(a - wa + wt, 3), 'durationInFrames': n, 'cropX': cr[0][1], 'crops': [[round((s - a) * 30), x, *z] if z else [round((s - a) * 30), x] for s, x in cr], 'words': words})
    gen[eid] = scenes
    print(eid, round(sum(s['durationInFrames'] for s in scenes) / 30, 1), 's |', ' / '.join(s['id'] + ': ' + ' '.join(w['word'] for w in s['words']) for s in scenes))
    if '--no-excerpts' not in sys.argv and (not ONLY or eid in ONLY):
        cmd = ['ffmpeg', '-v', 'error', '-y']; fc = []
        for i, (a, b, _) in enumerate(offs):
            cmd += ['-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', SRC]
            fc.append(f'[{i}:v]fps=30,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1,format=yuv420p[v{i}]')
            fc.append(f'[{i}:a]asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{b - a:.3f}[a{i}]')
        fc.append(''.join(f'[v{i}][a{i}]' for i in range(len(offs))) + f'concat=n={len(offs)}:v=1:a=1[cv][ca]'); fc.append('[cv]' + G67 + (',' + spec['eq'] if spec.get('eq') else '') + '[gv]')
        subprocess.run(cmd + ['-filter_complex', ';'.join(fc), '-map', '[gv]', '-map', '[ca]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
                              '-g', '15', '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', f'public/g67_{eid}.mp4'], check=True)
    c = {k: v for k, v in spec.items() if k not in ('scenes', 'zoom', 'eq')}
    c['hl'] = {w: ('#FF2A2A' if col == R else '#58EE28') for w, col in c['hl'].items()}
    c.update(cta='*full episode on @HardScope*', ctaAt=[scenes[-1]['id']], ask=[{'at': r, 'text': t} for r, t in c['ask']], track='none', calls=[], src=f'g67_{eid}.mp4',
             intro=False, ctaEnd=True, hardcut=True, cutSfx='s_camflash.mp3', sat=1.1, progress=True, popMid=True)
    sc = {s['id']: s for s in scenes}
    for e in c['extras']:
        if e.pop('after', False):
            w = [x for x in sc[e['at'][0]]['words'] if x['word'].lower().startswith(e['at'][1].lower())][e['at'][2] if len(e['at']) > 2 else 0]
            e['off'] = w['endFrame'] - w['startFrame'] + 4
    refs = [r for r, _ in c['tints']] + [c['ctaAt']] + [q['at'] for q in c['ask']] + [e['at'] for e in c['extras']] + sum((c[k] for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks')), [])
    for r in refs:
        assert r[0] in sc, (eid, r)
        if len(r) == 1: continue
        ws = [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())]
        assert len(ws) > (r[2] if len(r) > 2 else 0), (eid, r, [w['word'] for w in sc[r[0]]['words']])
    for e in c['extras']: assert e['kind'] in ('sfx', 'png', 'txt') or e.get('sfx'), (eid, 'overlay without SFX', e)   # pngs get the echo-pop automatically
    CFG[eid] = c
json.dump(gen, open('src/edits.gen.json', 'w'))
json.dump(CFG, open('src/r3t.cfg.json', 'w'), indent=1); print('cfg ok')

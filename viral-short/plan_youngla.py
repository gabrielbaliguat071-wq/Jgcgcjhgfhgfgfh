"""YoungLA x6 (Nov 19) — "Bodybuilders vs Models" fashion show, Meme look (src/Meme.tsx): the hook is the funniest/most
shocking line, then a hard cut into the story that leads back to it. Interview two-shots and wide runway shots use the band
(both people + the YoungLA sign/cars stay visible), runway walks use a full-height crop on the model (clothes visible).
No colour tints, light background blur (house rules). Run from viral-short/: python3 plan_youngla.py"""
import json, os, subprocess
SRC = '../footage/youngla/bvm.mp4'
G67 = ("split[ga][gb];[gb]gblur=sigma=14[gg];[ga][gg]blend=all_mode=softlight:all_opacity=0.245,unsharp=5:5:1.74:5:5:0,"
       "eq=contrast=1.113:saturation=1.26:gamma=0.98,curves=all='0/0 0.25/0.21 0.75/0.81 1/1',unsharp=3:3:0.79,format=yuv420p")
B = (960, 0.5, 830)                       # band
def X(x, z=1.0, y=540): return (x, z, y)  # full-height crop on x
def G(x=1340): return (x, 1.18, 430)      # guest (right) close-up in the interview
# shot index (from .work/brief7/shots.jpg) -> crop
SHOT = {0: B, 1: B, 2: X(960), 3: B, 4: X(420), 5: B, 6: X(1000), 7: X(1000), 8: X(960), 9: B, 10: B, 11: X(920), 12: X(840), 13: X(840), 14: B, 15: B,
        16: B, 17: B, 18: X(1000), 19: X(960), 20: X(800), 21: X(880), 22: B, 23: X(1200), 24: X(840), 25: B, 26: B,
        27: X(960), 28: X(1300), 29: X(960), 30: X(880), 31: X(1120), 32: X(1040), 33: X(960), 34: X(1260), 35: X(1200),
        36: B, 37: X(960), 38: X(800), 39: X(1340), 40: B, 41: X(840), 42: B, 43: X(960), 44: X(920), 45: X(960), 46: B, 47: B, 48: X(880), 49: X(960),
        50: B, 51: B, 52: B, 53: B, 54: B, 55: B, 56: X(680), 57: X(880), 58: B, 59: X(880), 60: B, 61: B, 62: B, 63: X(1360), 64: B, 65: X(1120),
        66: B, 67: X(1200), 68: X(1200), 69: X(1200), 70: B, 71: X(1120), 72: X(560), 73: B, 74: X(880), 75: B, 76: X(1000), 77: B, 78: X(960),
        79: B, 80: B, 81: X(1000), 82: X(960), 83: B, 84: B}
SHOTS = json.load(open('/tmp/claude-0/ya/shots.json'))
# clip -> scenes (id, a, b, crop overrides [(t, crop)]) in SOURCE seconds; first scene = hook
CLIPS = {
 'yaneg': [('hook', 766.3, 768.75, [(766.3, G(1320))]), ('c1', 760.1, 766.3, []), ('c1b', 768.7, 780.0, [(768.7, G(1320)), (771.6, B)]), ('c2', 782.7, 786.1, []), ('c3', 790.6, 797.6, [])],
 'yaaura': [('hook', 860.6, 865.6, [(860.6, G(1320)), (864.9, B)]), ('c1', 825.2, 829.85, []), ('c2', 831.4, 833.9, []), ('c3', 841.7, 860.6, [(847.2, G(1320)), (851.5, B)])],
 'yalate': [('hook', 527.3, 531.0, []), ('c1', 503.2, 527.3, []), ('c2', 531.9, 535.4, [])],
 'yahand': [('hook', 610.6, 614.4, []), ('c1', 586.4, 610.6, []), ('c2', 614.4, 618.3, [])],
 'yajay': [('hook', 1061.5, 1068.5, [(1063.9, G(1390))]), ('c1', 1049.3, 1053.5, []), ('c2', 1069.0, 1080.2, []), ('c3', 1133.5, 1145.9, [])],
 'yaceo': [('hook', 943.2, 948.75, [(943.2, G(1360))]), ('c1', 923.1, 943.2, [(935.0, G(1360))]), ('c2', 948.75, 952.95, []), ('c3', 958.2, 962.45, [])],
}
FIX = {'culler': 'Cutler', 'piss': 'p*ss', 'shit': 'sh*t', 'shit.': 'sh*t.', 'zee': 'Z', 'chegg': 'check', 'f***': 'f***'}
FIXAT = {1142.70: 'shirts.', 928.86: 'crumb.', 793.12: 'YoungLA.', 793.30: '', 1075.96: 'SF90.', 1076.40: '', 783.54: ''}
W = [(w['startMs'] / 1000, w['endMs'] / 1000, w['text']) for w in json.load(open('../footage/youngla/tx/bvm.words.json'))]
gen = json.load(open('src/edits.gen.json'))
for cid, plan in CLIPS.items():
    xa, xb = min(a for _, a, _, _ in plan) - 0.5, max(b for _, _, b, _ in plan) + 0.5
    out = f'public/g67_{cid}.mp4'
    if not os.path.exists(out):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(xa), '-to', str(xb), '-i', SRC, '-vf', G67, '-c:v', 'libx264', '-crf', '17',
                        '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', out], check=True)
    scenes = []
    for sid, a, b, over in plan:
        n = round((b - a) * 30); words = []
        for ws, we, t in W:
            if not (a - 0.05 <= ws < b - 0.05): continue
            hit = [v for ft, v in FIXAT.items() if abs(ft - ws) < 0.015]
            t2 = hit[0] if hit else FIX.get(t.lower(), t)
            if sid == 'c2' and cid == 'yaneg' and t2 == 'million,' and ws > 783.5: continue
            if not t2: continue
            if t2.startswith(',') and words: words[-1]['word'] += t2; continue
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t2, 'startFrame': f0, 'endFrame': f1})
        for i in range(len(words) - 1, 0, -1):
            if words[i]['word'].startswith('-'): words[i - 1]['word'] += words[i]['word']; words.pop(i)
        cr = {}
        for _, s0, s1 in [r for r in SHOTS if r[0] == cid[2:] or (cid == 'yaneg' and r[0] == 'neg')]:
            if s1 > a and s0 < b:
                cr[max(0, round((s0 - a) * 30))] = SHOT[SHOTS.index([_, s0, s1])]
        for t, c in over: cr[max(0, round((t - a) * 30))] = c
        crops = [[k, *cr[k]] for k in sorted(cr) if k < n - 6]
        if not crops or crops[0][0] != 0: crops.insert(0, [0, *(cr[max(k for k in cr if k <= 0)] if any(k <= 0 for k in cr) else B)])
        scenes.append({'id': sid, 'videoStartSec': round(a - xa, 3), 'durationInFrames': n, 'cropX': 960, 'crops': crops, 'words': words})
    gen[cid] = scenes
    print(cid, round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's |', ' / '.join(s['id'] + ': ' + ' '.join(w['word'] for w in s['words']) for s in scenes))
json.dump(gen, open('src/edits.gen.json', 'w'))

Y, GR, RD = '#FFE14D', '#5CFF5C', '#FF4D4D'
LBL = 'YOUNGLA · BODYBUILDERS VS MODELS'
CFG = {
 'yaneg': dict(top='His bank account hit -$152,000', hl={'-$152,000': '#E3201B'}, music=['phonk_n', 0.0], cta='HOW DO YOU EVEN GET HERE?', ctaAt=['c3', 'okay'],
   kw={'negative': RD, '$152000': RD, 'zero': RD, 'robbed': RD, 'taxes': Y, 'consent': Y, 'wild': GR, 'million': GR, 'equity': GR, 'youngla': Y, '51': GR, 'emptied': RD},
   emoji=[[['hook', '$152'], '1f480'], [['c1b', 'robbed'], '1f6a8'], [['c1b', 'taxes'], '1f62d'], [['c2', 'million'], '1f4b0'], [['c3', 'youngla'], '1f60f'], [['c3', '51'], '1f92f']],
   punch=[['hook', 'negative'], ['hook', '$152'], ['c1', 'zero'], ['c1b', 'robbed'], ['c1b', 'taxes'], ['c1b', 'consent'], ['c1b', 'wild'], ['c2', 'million'], ['c3', 'equity'], ['c3', 'youngla'], ['c3', '51']],
   sfx=[[['hook', '$152'], 'm_record-scratch.mp3', 0.3], [['c1b', 'wild'], 's_huh.mp3', 0.3], [['c3', '51'], 'm_cha-ching.mp3', 0.3]]),
 'yaaura': dict(top='The most aura at the show went to… the SOUND GUY', hl={'SOUND': '#1DB954', 'GUY': '#1DB954'}, music=['montagem_n', 24.0], cta='WHO HAS MORE AURA THAN GRIFFIN?', ctaAt=['c3', 'volumes'],
   kw={'noise': Y, 'produce': GR, 'wow': GR, 'aura': Y, 'jay': GR, 'cutler': GR, 'sound': Y, 'griffin': GR, 'speak': RD, 'volumes': GR, 'awarded': Y},
   emoji=[[['hook', 'noise'], '1f3a7'], [['hook', 'wow'], '1f5ff'], [['c1', 'aura'], '2728'], [['c2', 'jay'], '1f4aa'], [['c3', 'sound'], '1f3a7'], [['c3', 'awarded'], '1f3c6'], [['c3', 'speak'], '1f5ff'], [['c3', 'volumes'], '1f92f']],
   punch=[['hook', 'noise'], ['hook', 'produce'], ['hook', 'wow'], ['c1', 'aura'], ['c2', 'jay'], ['c3', 'sound'], ['c3', 'griffin'], ['c3', 'awarded'], ['c3', 'speak'], ['c3', 'volumes']],
   sfx=[[['hook', 'wow'], 'm_anime-wow.mp3', 0.3], [['c3', 'awarded'], 'm_crowd-cheer.mp3', 0.22]]),
 'yalate': dict(top='Showed up 3 HOURS LATE to the YoungLA show', hl={'3': '#E3201B', 'HOURS': '#E3201B', 'LATE': '#E3201B'}, music=['funkabn_n', 2.0], cta='WOULD YOU HAVE WAITED?', ctaAt=['c2', 'go'],
   kw={'bathroom': Y, 'pss': Y, 'long': RD, 'three': RD, 'hours': RD, 'late': RD, 'ready': GR, 'pee': Y, 'bad': RD, 'aaron': GR, 'mad': RD, 'bro': GR},
   emoji=[[['hook', 'bathroom'], '1f6bd'], [['hook', 'long'], '1f62d'], [['c1', 'three'], '23f0'], [['c1', 'ready'], '1f440'], [['c1', 'pee'], '1f6bd'], [['c1', 'aaron'], '1f62c'], [['c2', 'go', 1], '1f602']],
   punch=[['hook', 'directly'], ['hook', 'bathroom'], ['hook', 'long'], ['c1', 'three'], ['c1', 'literally'], ['c1', 'ready'], ['c1', 'pee'], ['c1', 'mad'], ['c2', 'go', 1]],
   sfx=[[['hook', 'bathroom'], 'm_record-scratch.mp3', 0.3], [['c1', 'literally'], 's_huh.mp3', 0.3]]),
 'yahand': dict(top='"I already have a G-Wagon. I\'m already HANDSOME"', hl={'HANDSOME"': '#1DB954'}, music=['brevis_n', 0.0], cta='WHAT WOULD YOU BUY FIRST?', ctaAt=['c2', 'tough'],
   kw={'g-wagon': Y, 'handsome': GR, 'mature': GR, 'apartment': Y, 'six': Y, 'crib': GR, 'lavish': Y, 'pool': GR, 'safe': RD, 'tough': RD, 'check': GR, 'backyard': GR},
   emoji=[[['hook', 'g-wagon'], '1f3ce-fe0f'], [['hook', 'handsome'], '1f60e'], [['c1', 'mature'], '1f9d0'], [['c1', 'crib'], '1f4cd'], [['c1', 'pool'], '1f3dd-fe0f'], [['c1', 'safe'], '1f62c'], [['c2', 'tough'], '1f914']],
   punch=[['hook', 'g-wagon'], ['hook', 'handsome'], ['c1', 'mature'], ['c1', 'apartment'], ['c1', 'crib'], ['c1', 'pool'], ['c1', 'safe'], ['c2', 'think'], ['c2', 'tough']],
   sfx=[[['hook', 'handsome'], 'm_rizz-sound-effect.mp3', 0.3], [['c2', 'tough'], 's_huh.mp3', 0.25]]),
 'yajay': dict(top="JAY CUTLER'S first ever fashion show", hl={'JAY': '#1DB954', "CUTLER'S": '#1DB954'}, music=['empire_n', 0.0], cta='WOULD YOU WALK FOR YOUNGLA?', ctaAt=['c3', 'keep'],
   kw={'first': Y, 'last': RD, 'jay': GR, 'cutler': GR, 'applause': Y, 'ferrari': RD, 'sf90': RD, 'robbies': Y, 'compressions': Y, 'physique': GR, 'compression': Y, 'business': GR},
   emoji=[[['hook', 'first'], '1f633'], [['hook', 'last'], '1f480'], [['c1', 'jay'], '1f451'], [['c2', 'ferrari'], '1f3ce-fe0f'], [['c2', 'robbie'], '1f602'], [['c3', 'physique'], '1f4aa'], [['c3', 'business'], '1f4b0']],
   punch=[['hook', 'first'], ['hook', 'last'], ['c1', 'jay'], ['c1', 'applause'], ['c2', 'ferrari'], ['c2', 'sf90'], ['c2', 'robbie'], ['c3', 'compressions'], ['c3', 'physique'], ['c3', 'business']],
   sfx=[[['hook', 'last'], 'm_record-scratch.mp3', 0.3], [['c1', 'applause'], 'm_crowd-cheer.mp3', 0.25], [['c2', 'robbie'], 's_huh.mp3', 0.3]]),
 'yaceo': dict(top="YoungLA's owner almost LEAKED their next collab", hl={'LEAKED': '#E3201B'}, music=['dubist_n', 1.0], cta='WHAT COLLAB DO YOU WANT NEXT?', ctaAt=['c3', 'april'],
   kw={'biggest': Y, 'franchise': Y, 'insane': RD, '2027': GR, 'craziest': RD, 'collab': Y, 'achievable': GR, 'excited': GR, 'nobody': RD, 'dragon': Y, 'ball': Y, 'z': Y, 'april': GR},
   emoji=[[['hook', 'franchise'], '1f440'], [['hook', 'insane'], '1f92f'], [['c1', 'craziest'], '1f525'], [['c1', 'achievable'], '1f633'], [['c2', 'excited'], '1f525'], [['c3', 'dragon'], '1f409'], [['c3', 'april'], '1f4c5']],
   punch=[['hook', 'biggest'], ['hook', 'insane'], ['c1', '2027'], ['c1', 'craziest'], ['c1', 'collab'], ['c1', 'achievable'], ['c2', 'excited'], ['c2', 'done'], ['c3', 'dragon'], ['c3', 'april']],
   sfx=[[['hook', 'insane'], 'm_record-scratch.mp3', 0.3], [['c3', 'dragon'], 'm_anime-wow.mp3', 0.3]]),
}
allcfg = json.load(open('src/meme.cfg.json'))
for eid, c in CFG.items():
    c.update(src=f'g67_{eid}.mp4', label=LBL, tints=[], bgBlur=10)
    sc = {s['id']: s for s in gen[eid]}
    refs = c['punch'] + [r for r, _ in c['emoji']] + [c['ctaAt']] + [s[0] for s in c['sfx']]
    for r in refs:
        ws = [w for w in sc[r[0]]['words'] if ''.join(ch for ch in w['word'].lower() if ch.isalnum() or ch in "$-").startswith(r[1].replace("'", ''))]
        assert len(ws) > (r[2] if len(r) > 2 else 0), (eid, r, [w['word'] for w in sc[r[0]]['words']])
    for e in [e for _, e in c['emoji']]: assert os.path.exists(f'public/res/emoji/{e}.png'), (eid, e)
    for _, f, _ in c['sfx']: assert os.path.exists(f'public/res/{f}'), f
    allcfg[eid] = c
json.dump(allcfg, open('src/meme.cfg.json', 'w'), indent=1); print('cfg ok')

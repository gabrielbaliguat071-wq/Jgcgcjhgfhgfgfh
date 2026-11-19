"""YoungLA x6 re-cut in the VverPaldo style (src/Guess.tsx, Nov 19): same moments as plan_youngla.py (run that first — it builds
the ya* scenes + g67_ya*.mp4 excerpts), converted to yv*: square video box, one white word at a time (always on), Montserrat
top line + skull, flat green/red tints, punch-ins, blow-out, black flash, streak, white hard cut + camera flash after the hook.
Crops (Guess semantics, zoom 1 = ~1083 px of source width): two-shot / wide runway -> (920|960, 1, 540) so both people and the
YoungLA sign + cars show; runway model -> (x, 1.3, 560); interview close-up -> (x, 1.6, 460). Run: python3 plan_youngla_vp.py"""
import json
gen = json.load(open('src/edits.gen.json'))

def conv(c):
    t, x, z, y = c
    if z < 1: return [t, 900, 1.0, 540]          # band -> full square (both people / sign + cars)
    if z > 1.1: return [t, min(1500, x + 40), 1.6, 460]   # guest close-up
    return [t, x, 1.15, 560]                      # runway model
for ya in ['yaneg', 'yaaura', 'yalate', 'yahand', 'yajay', 'yaceo']:
    scenes = json.loads(json.dumps(gen[ya]))
    for s in scenes:
        s['crops'] = [conv(c) for c in s['crops']]
        w = s['words']
        for i in range(len(w)): w[i]['word'] = w[i]['word'].strip(',.')
        s['words'] = w = [x for x in w if x['word']]
        for i in range(len(w) - 1): w[i]['endFrame'] = max(min(w[i]['endFrame'], w[i + 1]['startFrame']), w[i + 1]['startFrame'])
    gen['yv' + ya[2:]] = scenes
json.dump(gen, open('src/edits.gen.json', 'w'))

def png(at, f, x=870, y=1290, size=200, **k): return dict(at=at, kind='png', file=f, x=x, y=y, size=size, **k)
def ov(at, f, dur=34): return dict(at=at, kind='ov', file=f, dur=dur)
def sfx(at, f, v=0.45): return dict(at=at, kind='sfx', file=f, v=v)
G, R = 'G', 'R'
CFG = {
 'yvneg': dict(top='His bank account hit NEGATIVE $152,000', hl={'NEGATIVE': '#F40305', '$152,000': '#F40305'}, cta='*how do you even get here?*', music=['phonk_n', 22.4],
   ctaAt=['c3', 'okay'],
   tints=[[['hook', 'negative'], R], [['c1', 'zero'], R], [['c1b', 'taxes'], R], [['c2', 'million'], G], [['c3', '51'], G]], rizz=[['c3', 'youngla']],
   punch=[['hook', 'negative'], ['hook', '$152'], ['c1', 'emptied'], ['c1', 'zero'], ['c1b', 'robbed'], ['c1b', 'taxes'], ['c1b', 'consent'], ['c1b', 'wild'], ['c2', 'million'], ['c3', 'equity'], ['c3', '51']],
   blowouts=[['hook', '$152']], blackFlash=[['c1b']], streaks=[['c2'], ['c3']],
   extras=[png(['c1b', 'robbed'], 'e_think.png', 860, 1240), sfx(['c1b', 'wild'], 's_huh.mp3', 0.4), png(['c1b', 'consent'], 'e_sob.png', 230, 1240), ov(['c3', '51'], 'greenflash2.mp4'), sfx(['c3', '51'], 's_money.mp3', 0.35)]),
 'yvaura': dict(top='The most aura at the show went to… the SOUND GUY', hl={'SOUND': '#58EE28', 'GUY': '#58EE28'}, cta='*who has more aura than Griffin?*', music=['montagem_n', 24.0],
   ctaAt=['c3', 'volumes'],
   tints=[[['hook', 'produce'], G], [['c1', 'aura'], G], [['c3', 'awarded'], G], [['c3', 'speak'], R]], rizz=[['c3', 'awarded']],
   punch=[['hook', 'noise'], ['hook', 'produce'], ['hook', 'wow'], ['c1', 'aura'], ['c2', 'jay'], ['c3', 'sound'], ['c3', 'griffin'], ['c3', 'awarded'], ['c3', 'speak'], ['c3', 'volumes']],
   blowouts=[['hook', 'wow']], blackFlash=[['c3']], streaks=[['c2'], ['c3', 'griffin', 1]],
   extras=[sfx(['hook', 'wow'], 's_wow.mp3', 0.4), png(['c3', 'awarded'], 'e_laugh.png', 860, 1240), sfx(['c3', 'awarded'], 's_correct.mp3', 0.3), ov(['c3', 'volumes'], 'greenflash2.mp4')]),
 'yvlate': dict(top='He showed up 3 HOURS LATE to the YoungLA show', hl={'3': '#F40305', 'HOURS': '#F40305', 'LATE': '#F40305'}, cta='*would you have waited?*', music=['funkabn_n', 33.2],
   ctaAt=['c2', 'go'],
   tints=[[['hook', 'bathroom'], R], [['c1', 'three'], R], [['c1', 'ready'], G], [['c1', 'mad'], R]], rizz=[['c1', 'ready']],
   punch=[['hook', 'directly'], ['hook', 'bathroom'], ['hook', 'long'], ['c1', 'three'], ['c1', 'literally'], ['c1', 'ready'], ['c1', 'pee'], ['c1', 'mad'], ['c2', 'go', 1]],
   blowouts=[['hook', 'bathroom']], blackFlash=[['c1', 'come']], streaks=[['c1', 'what'], ['c2']],
   extras=[png(['hook', 'long'], 'e_laugh.png', 860, 1240), sfx(['c1', 'literally'], 's_huh.mp3', 0.4), png(['c1', 'pee', 1], 'e_sob.png', 230, 1240), sfx(['c2', 'go', 1], 's_fahhh.mp3', 0.3)]),
 'yvhand': dict(top='"I already have a G-Wagon… I\'m already HANDSOME"', hl={'HANDSOME"': '#58EE28'}, cta='*what would YOU buy first?*', music=['brevis_n', 0.0],
   ctaAt=['c2', 'tough'],
   tints=[[['hook', 'handsome'], G], [['c1', 'mature'], G], [['c1', 'safe'], R], [['c2', 'tough'], R]], rizz=[['hook', 'handsome']],
   punch=[['hook', 'g-wagon'], ['hook', 'handsome'], ['c1', 'mature'], ['c1', 'apartment'], ['c1', 'crib'], ['c1', 'pool'], ['c1', 'safe'], ['c2', 'think'], ['c2', 'tough']],
   blowouts=[['hook', 'handsome']], blackFlash=[['c1', 'check', 2]], streaks=[['c1', 'backyard'], ['c2']],
   extras=[png(['hook', 'handsome'], 'e_laugh.png', 860, 1240), sfx(['c1', 'mature'], 's_ding.mp3', 0.3), png(['c2', 'tough'], 'e_think.png', 230, 1240), sfx(['c2', 'tough'], 's_huh.mp3', 0.35)]),
 'yvjay': dict(top="JAY CUTLER'S first ever fashion show", hl={'JAY': '#58EE28', "CUTLER'S": '#58EE28'}, cta='*would you walk the runway?*', music=['empire_n', 18.8],
   ctaAt=['c3', 'keep'],
   tints=[[['hook', 'last'], R], [['c1', 'jay'], G], [['c2', 'ferrari'], G], [['c3', 'business'], G]], rizz=[['c1', 'jay']],
   punch=[['hook', 'first'], ['hook', 'last'], ['c1', 'jay'], ['c1', 'applause'], ['c2', 'ferrari'], ['c2', 'sf90'], ['c2', 'robbie'], ['c3', 'compressions'], ['c3', 'physique'], ['c3', 'business']],
   blowouts=[['c2', 'sf90']], blackFlash=[['c2']], streaks=[['c3']],
   extras=[png(['hook', 'last'], 'e_laugh.png', 860, 1240), sfx(['c1', 'applause'], 's_wow.mp3', 0.35), sfx(['c2', 'robbie'], 's_huh.mp3', 0.4), png(['c2', 'robbie'], 'e_sob.png', 230, 1240), ov(['c3', 'business'], 'greenflash2.mp4')]),
 'yvceo': dict(top="YoungLA's owner almost LEAKED their next collab", hl={'LEAKED': '#F40305'}, cta='*what collab do you want next?*', music=['dubist_n', 1.0],
   ctaAt=['c3', 'april'],
   tints=[[['hook', 'insane'], G], [['c1', 'craziest'], R], [['c2', 'excited'], G], [['c3', 'dragon'], G]], rizz=[['c3', 'dragon']],
   punch=[['hook', 'biggest'], ['hook', 'insane'], ['c1', '2027'], ['c1', 'craziest'], ['c1', 'collab'], ['c1', 'achievable'], ['c2', 'excited'], ['c2', 'done'], ['c3', 'dragon'], ['c3', 'april']],
   blowouts=[['hook', 'insane']], blackFlash=[['c3']], streaks=[['c1', 'honestly'], ['c2']],
   extras=[png(['hook', 'franchise'], 'e_think.png', 860, 1240), sfx(['c1', 'craziest'], 's_huh.mp3', 0.4), sfx(['c3', 'dragon'], 's_wow.mp3', 0.35), ov(['c3', 'dragon'], 'greenflash2.mp4')]),
}
for eid, c in CFG.items():
    c.update(track='none', calls=[], intro=True, hardcut=True, cutSfx='s_camflash.mp3', src=f'g67_ya{eid[2:]}.mp4')
    sc = {s['id']: s for s in gen[eid]}
    refs = [('tints', r) for r, _ in c['tints']] + [(k, r) for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks') for r in c[k]] + [('cta', c['ctaAt'])] + [('x', e['at']) for e in c['extras']]
    for key, r in refs:
        assert r[0] in sc, (eid, key, r)
        if len(r) == 1: continue
        ws = [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())]
        assert len(ws) > (r[2] if len(r) > 2 else 0), (eid, key, r, [w['word'] for w in sc[r[0]]['words']])
json.dump(CFG, open('src/yv.cfg.json', 'w'), indent=1); print('cfg ok')

"""WoW Forever FRANCE (Clipping Culture, 2026-11-25) — original VverPaldo (Guess.tsx), French only. Source: official FR 'What is WoW Forever'
(WTC02 …FR-FR, French narrator + Blizzard music; f.io/pr9LAqV0 > FR > What is WoW Forever). No added music (silent track), game presented as released,
avoid end card ('le 5 novembre, précommandez'). Race name not verifiable → dropped from captions. Caption: #Sponsorisé then #blizzardpartner; YT tag @WorldofWarcraftFR."""
import json, os, subprocess
G67 = "format=yuv420p"
def F(y=540, z=1.0, x=960): return (x, z, y)
EDITS = {
 'wowquetes': ('whatis', None, {}, [
     ('hook', 11.15, 15.65, [(11.15, F())]),
     ('c1', 0.00, 4.95, [(0.00, F())]),
     ('c2', 16.15, 22.95, [(16.15, F()), (19.40, F(540, 1.15))]),
     ('c3', 25.00, 38.65, [(25.00, F()), (29.10, F(540, 1.15)), (33.70, F())])]),
 'wowrace': ('whatis', None, {}, [
     ('hook', 170.25, 175.30, [(170.25, F())]),
     ('c1', 153.25, 169.40, [(153.25, F()), (159.30, F(540, 1.15)), (164.90, F())]),
     ('c2', 175.55, 184.30, [(175.55, F()), (180.50, F(540, 1.15))])]),
 'wowraid': ('whatis', None, {}, [
     ('hook', 232.75, 236.40, [(232.75, F())]),
     ('c1', 216.05, 232.60, [(216.05, F()), (220.50, F(540, 1.15)), (224.50, F()), (228.70, F(540, 1.15))]),
     ('c2', 125.85, 129.25, [(125.85, F())]),
     ('c3', 133.55, 143.00, [(133.55, F()), (138.70, F(540, 1.15))])]),
}
DROP = {'wowrace': [(156.0, 159.25), (180.4, 181.25)]}
FIXFR = {'rives': 'Rives', 'claires': 'Claires', 'war': 'WoW', 'dojons': 'donjons', 'eolides,': '', 'eolides': '', 'shen': '', 'dorei,': '', 'connues': '', 'parmi': '', 'leurs': '', 'peuples': '', 'sous': '',
  'réimaginez.': 'réimaginés', 'repère': 'Repaire', 'nixia,': "d'Onyxia", 'ijal': 'Hyjal', 'higèle': 'Hyjal', 'raids.': 'raids'}
gen = json.load(open('src/edits.gen.json'))
for eid, (src, band, fix, plan) in EDITS.items():
    out = 'public/wowfr_whatis.mp4'
    if not os.path.exists(out): subprocess.run(['cp', '../footage/wowfr/whatis.mp4', out], check=True)
    Wd = json.load(open(f'../footage/wowfr/{src}.words.json')); scenes = []
    for sid, a, b, crops in plan:
        n = round((b - a) * 30); words = []
        for w in Wd:
            ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
            if not (a - 0.05 <= ws < b - 0.05): continue
            if any(x0 <= ws < x1 for x0, x1 in DROP.get(eid, [])): continue
            t2 = FIXFR.get(t.lower(), t)
            if t2 == '': continue
            if words and t2.startswith("'"): words[-1]['word'] += t2.rstrip(',.'); continue
            if words and t2 == "d'Onyxia" and words[-1]['word'] == 'de': words[-1]['word'] = t2; continue
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
 'wowquetes': dict(top='Plus de 1000 NOUVELLES quêtes dans WoW Forever', hl={'NOUVELLES': '#58EE28'}, cta='*World of Warcraft: Forever est disponible*', music=['silent_n', 0], ctaAt=['c3', 'jamais'],
   tints=[[['hook', '1000'], G], [['c2', 'raids'], G], [['c3', 'aventure'], G]], rizz=[['hook', '1000']],
   punch=[['hook', '1000'], ['hook', 'race'], ['hook', 'zones'], ['c1', 'massifs'], ['c2', '9'], ['c2', 'raids'], ['c2', 'amis'], ['c2', 'réimaginé'], ['c3', 'jamais'], ['c3', 'aventure']],
   blowouts=[['hook', '1000']], blackFlash=[], streaks=[['c2']]),
 'wowrace': dict(top="La nouvelle race de WoW Forever peut marcher sur L'AIR", hl={"L'AIR": '#58EE28'}, cta='*World of Warcraft: Forever est disponible*', music=['silent_n', 0], ctaAt=['c2', 'Horde'],
   tints=[[['hook', 'glissade'], G], [['c1', 'ciel'], G], [['c2', 'Horde'], R]], rizz=[['hook', 'marche']],
   punch=[['hook', 'marche'], ['hook', 'chute'], ['hook', 'glissade'], ['c1', 'habitants'], ['c1', 'nouvelle'], ['c1', 'ciel'], ['c1', 'éléments'], ['c2', "l'exploration"], ['c2', 'embarrassantes'], ['c2', 'Horde'], ['c2', "l'Alliance"]],
   blowouts=[['hook', 'glissade']], blackFlash=[], streaks=[['c1', 'Leur']]),
 'wowraid': dict(top='Un raid à 40 JOUEURS dans WoW Forever', hl={'JOUEURS': '#58EE28'}, cta='*World of Warcraft: Forever est disponible*', music=['silent_n', 0], ctaAt=['c3', 'Hyjal'],
   tints=[[['hook', '40'], G], [['c1', 'raids'], G], [['c3', 'Hyjal'], G]], rizz=[['hook', '40']],
   punch=[['hook', '40'], ['hook', "d'Onyxia"], ['c1', 'groupe'], ['c1', '15'], ['c1', 'maximum'], ['c1', 'raids'], ['c1', '10'], ['c1', '20'], ['c2', 'mille'], ['c3', 'donjons'], ['c3', 'Hyjal'], ['c3', 'deux']],
   blowouts=[['hook', '40']], blackFlash=[], streaks=[['c3']]),
}
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
EXTRAS = {'wowquetes': [png(['hook', '1000'], 'emoji/1f633.png', 860, 1240), png(['c2', 'raids'], 'emoji/1f525.png', 230, 1240)],
  'wowrace': [png(['hook', 'glissade'], 'emoji/1f633.png', 860, 1240), png(['c2', 'embarrassantes'], 'emoji/1f602.png', 230, 1240)],
  'wowraid': [png(['hook', '40'], 'emoji/1f525.png', 860, 1240), png(['c1', 'raids'], 'emoji/1f440.png', 230, 1240)]}
allc = json.load(open('src/yv.cfg.json'))
for eid, c in CFG.items():
    c.update(track='none', calls=[], intro=True, hardcut=True, cutSfx='s_camflash.mp3', src='wowfr_whatis.mp4', extras=EXTRAS[eid])
    sc = {s['id']: s for s in gen[eid]}
    for r in [r for r, _ in c['tints']] + [r for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks') for r in c[k]] + [c['ctaAt']]:
        if len(r) == 1: continue
        ws = [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())]
        assert len(ws) > (r[2] if len(r) > 2 else 0), (eid, r, [w['word'] for w in sc[r[0]]['words']])
    allc[eid] = c
json.dump(allc, open('src/yv.cfg.json', 'w'), indent=1); print('cfg ok')

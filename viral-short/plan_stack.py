"""Trevor x3 (Nov 17, 3rd look) in the stacked split-screen look (src/Stack.tsx), VverPaldo concept: payoff hook -> hard cut
-> story that ends right before the hook line (loops). Re-edits of today's strongest moments with NEW hook lines, banners and songs.
Reuses the graded excerpts g67_tvjosh / g67_tvslab / g67_mrogers (all start at source 0). Bottom crop = (t, centre x, zoom, centre y)
in source px; zoom 1 shows a 926 px wide slice at full height. ring = head position in the source per crop-x (red ring, top shot).
Run from viral-short/: python3 plan_stack.py"""
import json, os
EDITS = {
 'sjosh': ('t5_ex_teammate', 'g67_tvjosh.mp4', {(22.8, 'heinz'): 'Hines-Allen', (23.16, 'allen.'): '', (23.96, 'heinz'): 'Hines-Allen', (24.30, 'allen'): ''}, [
     ('hook', 23.44, 25.64, [(23.44, (640, 1.0, 420))]),
     ('c1', 1.60, 3.30, [(1.60, (780, 1.05, 420))]),
     ('c2', 5.30, 23.42, [(5.30, (960, 1.4, 420)), (8.18, (780, 1.05, 420)), (11.56, (960, 1.45, 440)), (14.14, (960, 1.1, 450)), (17.14, (960, 1.5, 440)), (21.24, (640, 1.0, 420))])]),
 'sslab': ('tiger_slab', 'g67_tvslab.mp4', {(3.24, 'pc'): 'collection', (9.28, 'auto,'): 'autograph', (9.92, '9'): '9.5', (10.08, '-5'): '', (18.6, 'auto'): 'autograph'}, [
     ('hook', 26.08, 27.26, [(26.08, (960, 1.45, 420)), (26.76, (715, 1.0, 450))]),
     ('c1', 2.50, 11.40, [(2.50, (715, 1.0, 450)), (4.50, (640, 1.3, 470)), (8.10, (715, 1.0, 450))]),
     ('c2', 17.92, 23.32, [(17.92, (640, 1.3, 470)), (21.40, (715, 1.0, 450))]),
     ('c3', 24.04, 26.06, [(24.04, (715, 1.0, 450))])]),
 'srogers': ('v_rogers_realm', 'g67_mrogers.mp4', {}, [
     ('hook', 14.42, 17.04, [(14.42, (470, 1.0, 540))]),
     ('c1', 0.00, 3.82, [(0.00, (470, 1.15, 480))]),
     ('c2', 3.96, 9.30, [(3.96, (960, 1.35, 440)), (6.20, (960, 1.55, 420))]),
     ('c3', 11.18, 14.40, [(11.18, (1300, 1.0, 540)), (12.90, (960, 1.35, 440))]),
     ('c4', 17.60, 20.58, [(17.60, (600, 1.0, 540))])]),
}
gen = json.load(open('src/edits.gen.json'))
for eid, (src, vid, fix, plan) in EDITS.items():
    assert os.path.exists(f'public/{vid}'), vid
    W = [(w['startMs'] / 1000, w['endMs'] / 1000, w['text']) for w in json.load(open(f'../src/plans/data/{src}.words.json'))]
    scenes = []
    for sid, a, b, crops in plan:
        n = round((b - a) * 30); words = []
        for ws, we, t in W:
            if not (a - 0.05 <= ws < b - 0.05): continue
            k = t.lower().strip(',.?!'); hit = [v for (ft, fw), v in fix.items() if abs(ft - ws) < 0.03 and fw.strip(',.?!') == k]
            t2 = hit[0] if hit else t
            if not t2: continue
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t2, 'startFrame': f0, 'endFrame': f1})
        for i in range(len(words) - 1, 0, -1):
            if words[i]['word'].startswith('-'): words[i - 1]['word'] += words[i]['word']; words.pop(i)
        cr = [[max(0, round((t - a) * 30)), x, z, y] for t, (x, z, y) in crops]
        scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'cropX': 960, 'crops': cr, 'words': words})
    gen[eid] = scenes
    print(eid, round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's |', ' / '.join(s['id'] + ': ' + ' '.join(w['word'] for w in s['words']) for s in scenes))
json.dump(gen, open('src/edits.gen.json', 'w'))

Y, R, G = '#FFE11A', '#FF3B3B', '#5CFF5C'
CFG = {
 'sjosh': dict(top='He thought he pulled Josh Allen… LOOK closer', hl={'LOOK': Y, 'closer': Y}, src='g67_tvjosh.mp4', music=['empire_n', 18.5],
   ring={'960': [960, 330], '780': [600, 230], '640': [560, 170]}, cta='DID YOU KNOW THIS?', ctaAt=['c2', 'true', 1],
   emoji=[[['hook', 'changed'], '1f92f'], [['c1', 'gold'], '1f525'], [['c2', 'glove'], '1f602'], [['c2', 'josh'], '1f440'], [['c2', 'rookie'], '1f914']],
   punch=[['hook', 'hines'], ['hook', 'changed'], ['c1', 'true'], ['c2', 'teal'], ['c2', 'glove'], ['c2', 'josh'], ['c2', 'fire'], ['c2', 'rookie'], ['c2', 'real'], ['c2', 'hines']],
   sfx=[[['hook', 'changed'], 's_huh.mp3', 0.4], [['c2', 'glove'], 's_awk.mp3', 0.35], [['c2', 'hines'], 's_wow.mp3', 0.35]]),
 'sslab': dict(top='This card has pieces of Tiger\'s REAL glove and cap', hl={'REAL': Y}, src='g67_tvslab.mp4', music=['montagem_n', 24.0],
   ring={'960': [960, 330], '715': [470, 340], '640': [470, 340]}, cta='WOULD YOU KEEP IT?', ctaAt=['c2', 'glove'],
   emoji=[[['hook', 'me'], '1f633'], [['c1', 'four'], '23f3'], [['c1', 'tiger'], '26f3'], [['c2', 'cap'], '1f9e2'], [['c3', 'care'], '1f381']],
   punch=[['hook', 'me'], ['hook', 'yeah'], ['c1', 'four'], ['c1', 'exquisite'], ['c1', 'tiger'], ['c1', 'patch'], ['c2', 'shirt'], ['c2', 'glove'], ['c2', 'cap'], ['c2', 'wow'], ['c3', 'care']],
   sfx=[[['c1', 'tiger'], 'm_cha-ching.mp3', 0.3], [['c2', 'wow'], 's_wow.mp3', 0.35], [['hook', 'me'], 's_huh.mp3', 0.35]]),
 'srogers': dict(top='This fan war NEEDS to happen', hl={'NEEDS': R}, src='g67_mrogers.mp4', music=['funkabn_n', 0.5],
   ring={'470': [440, 330], '960': [960, 320], '1300': [1520, 330], '600': [480, 160]}, cta='WHO WINS?', ctaAt=['c4', 'traveling'],
   emoji=[[['hook', 'box'], '1f94a'], [['c1', 'eagles'], '1f985'], [['c2', 'insane'], '1f631'], [['c2', 'philly'], '1f62d'], [['c3', 'god'], '1f633'], [['c4', 'happen'], '1f525']],
   punch=[['hook', 'box'], ['hook', 'out'], ['c1', 'cheering'], ['c1', 'eagles'], ['c2', 'insane'], ['c2', 'home'], ['c2', 'philly'], ['c3', 'rogers'], ['c3', 'god'], ['c4', 'versus'], ['c4', 'happen']],
   sfx=[[['hook', 'box'], 'm_oh-hell-nah.mp3', 0.3], [['c2', 'philly'], 'm_record-scratch.mp3', 0.3]]),
}
for eid, c in CFG.items():
    sc = {s['id']: s for s in gen[eid]}
    refs = c['punch'] + [r for r, _ in c['emoji']] + [c['ctaAt']] + [s[0] for s in c['sfx']]
    for r in refs:
        ws = [w for w in sc[r[0]]['words'] if ''.join(ch for ch in w['word'].lower() if ch.isalnum() or ch in '$-').startswith(r[1])]
        assert len(ws) > (r[2] if len(r) > 2 else 0), (eid, r, [w['word'] for w in sc[r[0]]['words']])
    for e in [e for _, e in c['emoji']]: assert os.path.exists(f'public/res/emoji/{e}.png'), (eid, e)
json.dump(CFG, open('src/stack.cfg.json', 'w'), indent=1); print('cfg ok')

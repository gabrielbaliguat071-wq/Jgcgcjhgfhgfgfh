"""Trevor x5 (Nov 17) in the VverPaldo style: payoff hook -> hard cut (2-frame white flash + camera flash) -> story that
ends right before the hook line (loops). Pre-graded (67) excerpts public/g67_<id>.mp4 (gitignored), times below are SOURCE
seconds; the script shifts them to the excerpt. Crops = (t, centre x, zoom, centre y) in 1920x1080 source px, picked from
frame strips of who is talking. Words come from src/plans/data/<src>.words.json (faster-whisper) + fixes below.
Run from viral-short/: python3 plan_tv5.py ../footage/src"""
import json, os, subprocess, sys
SRC = sys.argv[1]
G67 = ("split[ga][gb];[gb]gblur=sigma=14[gg];[ga][gg]blend=all_mode=softlight:all_opacity=0.245,unsharp=5:5:1.74:5:5:0,"
       "eq=contrast=1.113:saturation=1.26:gamma=0.98,curves=all='0/0 0.25/0.21 0.75/0.81 1/1',unsharp=3:3:0.79,format=yuv420p")
T, L, R, TL, TR, W = (960, 1.6, 450), (470, 1.6, 460), (1500, 1.6, 460), (715, 1.15, 450), (1230, 1.15, 450), (960, 1.0, 540)
def tt(z=1.75): return (960, z, 440)  # tighter on Trevor

EDITS = {  # id: (source, excerpt [a, b], fixes {(t, word): new}, scenes [(id, a, b, [(t, crop)])])
 'tvjosh': ('t5_ex_teammate', (0, 26.1), {(22.8, 'heinz'): 'Hines-Allen', (23.16, 'allen.'): ''}, [
     ('hook', 19.14, 23.40, [(19.14, (780, 1.2, 420)), (21.24, (700, 1.5, 330))]),
     ('c1', 1.60, 3.30, [(1.60, (780, 1.2, 420))]),
     ('c2', 5.30, 19.10, [(5.30, T), (8.18, (780, 1.2, 420)), (11.56, (960, 1.6, 470)), (14.14, (960, 1.15, 460)), (17.14, (960, 1.7, 460))])]),
 'tvgolf': ('t2_dream_golf_four', (10, 56), {(12.84, 'for'): 'foursome', (13.18, 'some'): '', (13.34, 'of'): 'on'}, [
     ('hook', 32.20, 35.75, [(32.20, T), (34.78, TL)]),
     ('c1', 11.20, 13.95, [(11.20, TR)]),
     ('c2', 16.80, 19.85, [(16.80, L)]),
     ('c3', 26.45, 28.62, [(26.45, tt())]),
     ('c4', 45.40, 54.62, [(45.40, T), (48.62, tt(1.85)), (52.70, TL), (53.70, tt())])]),
 'tvslab': ('tiger_slab', (0, 32.5), {(3.24, 'pc'): 'collection', (9.28, 'auto,'): 'autograph', (9.92, '9'): '9.5', (10.08, '-5'): '',
                                       (18.6, 'auto'): 'autograph'}, [
     ('hook', 24.05, 27.25, [(24.05, TL), (26.10, tt()), (26.76, TL)]),
     ('c1', 2.50, 11.40, [(2.50, TL), (4.50, (640, 1.5, 520)), (8.10, TL)]),
     ('c2', 17.92, 23.32, [(17.92, (640, 1.5, 520)), (21.40, TL)])]),
 'tvpeyton': ('u4_peyton', (0, 56), {(47.82, 'had'): 'led', (48.46, 'and'): 'in'}, [
     ('hook', 38.20, 41.72, [(38.20, T), (40.56, tt(1.85))]),
     ('c1', 14.84, 19.16, [(14.84, (960, 1.45, 460)), (17.64, tt())]),
     ('c2', 20.50, 22.08, [(20.50, TL)]),
     ('c3', 25.55, 26.36, [(25.55, T)]),
     ('c4', 41.72, 51.70, [(41.72, (960, 1.45, 460)), (44.70, tt()), (47.16, (960, 1.45, 460)), (48.74, tt(1.9)), (50.54, W), (50.96, T)])]),
 'tvplays': ('u1_playbook', (0, 60), {}, [
     ('hook', 49.20, 54.96, [(49.20, T), (52.58, tt(1.85))]),
     ('c1', 0.00, 3.04, [(0.00, TL)]),
     ('c2', 14.24, 19.66, [(14.24, (960, 1.45, 460)), (17.00, tt(1.8))]),
     ('c3', 23.02, 24.20, [(23.02, T)]),
     ('c4', 36.80, 42.90, [(36.80, (960, 1.15, 450)), (39.06, T), (41.86, tt(1.8))])]),
}
gen = json.load(open('src/edits.gen.json'))
for eid, (src, (xa, xb), fix, plan) in EDITS.items():
    out = f'public/g67_{eid}.mp4'
    if not os.path.exists(out):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(xa), '-to', str(xb), '-i', f'{SRC}/{src}.mp4', '-vf', G67, '-c:v', 'libx264', '-crf', '16',
                        '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', out], check=True)
    W = [(w['startMs'] / 1000, w['endMs'] / 1000, w['text']) for w in json.load(open(f'../src/plans/data/{src}.words.json'))]
    scenes = []
    for sid, a, b, crops in plan:
        n = round((b - a) * 30); words = []
        for ws, we, t in W:
            if not (a - 0.05 <= ws < b - 0.05): continue
            k = (round(ws, 2), t.lower().strip(',.?!')); hit = [v for (ft, fw), v in fix.items() if abs(ft - ws) < 0.03 and fw.strip(',.?!') == k[1]]
            t2 = hit[0] if hit else t.strip(',.')
            if not t2: continue
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t2, 'startFrame': f0, 'endFrame': f1})
        for i in range(len(words) - 1, 0, -1):
            if words[i]['word'].startswith('-'): words[i - 1]['word'] += words[i]['word']; words.pop(i)
        for i in range(len(words) - 1): words[i]['endFrame'] = min(words[i]['endFrame'], words[i + 1]['startFrame'])
        # captions always on: each word stays until the next one
        for i in range(len(words) - 1): words[i]['endFrame'] = max(words[i]['endFrame'], words[i + 1]['startFrame'])
        cr = [[max(0, round((t - a) * 30)), x, z, y] for t, (x, z, y) in crops]
        scenes.append({'id': sid, 'videoStartSec': round(a - xa, 3), 'durationInFrames': n, 'cropX': 960, 'crops': cr, 'words': words})
    gen[eid] = scenes
    print(eid, round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's |', ' / '.join(s['id'] + ': ' + ' '.join(w['word'] for w in s['words']) for s in scenes))
json.dump(gen, open('src/edits.gen.json', 'w'))

def png(at, f, x=870, y=1290, size=200, **k): return dict(at=at, kind='png', file=f, x=x, y=y, size=size, **k)
def ov(at, f, dur=34): return dict(at=at, kind='ov', file=f, dur=dur)
def sfx(at, f, v=0.45): return dict(at=at, kind='sfx', file=f, v=v)
G, R = 'G', 'R'
CFG = {
 'tvjosh': dict(top='This Josh Allen card has a PLOT TWIST', hl={'PLOT': '#FF2A2A', 'TWIST': '#FF2A2A'}, cta='*did you know he changed his name?*', music=['funkabn_n', 0.5],
   ctaAt=['c2', 'true'],
   tints=[[['hook', 'real'], G], [['c1', 'gold'], G], [['c2', 'josh'], G], [['c2', 'fire'], G], [['c2', 'rookie'], R]], rizz=[['c2', 'josh']],
   punch=[['hook', 'rookie'], ['hook', 'real'], ['hook', 'hines'], ['c1', 'true'], ['c2', 'teal', 1], ['c2', 'glove'], ['c2', 'josh'], ['c2', 'fire'], ['c2', 'rookie']],
   blowouts=[['hook', 'hines']], blackFlash=[['c2']], streaks=[['c2', 'no', 1]],
   extras=[sfx(['hook', 'hines'], 's_huh.mp3', 0.45), png(['hook', 'hines'], 'e_laugh.png', 860, 1240), sfx(['c2', 'glove'], 's_awk.mp3', 0.4),
           ov(['c2', 'josh'], 'greenflash2.mp4'), sfx(['c2', 'josh'], 's_wow.mp3', 0.4), png(['c2', 'rookie'], 'e_think.png', 230, 1240)]),
 'tvgolf': dict(top='His dream golf group starts with JESUS', hl={'JESUS': '#58EE28'}, cta='*who is in YOUR dream foursome?*', music=['chess_n', 38],
   ctaAt=['c4', 'tiger'],
   tints=[[['hook', 'jesus'], G], [['c1', 'dream'], G], [['c3', 'week'], R], [['c4', 'tiger'], G], [['c4', 'goat', 1], G]], rizz=[['c4', 'tiger']],
   punch=[['hook', 'jesus'], ['hook', 'good'], ['c1', 'dream'], ['c1', 'golf'], ['c2', 'anybody'], ['c3', 'week'], ['c4', 'tiger'], ['c4', 'goat'], ['c4', 'goat', 1], ['c4', 'sick']],
   blowouts=[['hook', 'jesus']], blackFlash=[['c3']], streaks=[['c2'], ['c4']],
   extras=[sfx(['hook', 'jesus'], 's_wow.mp3', 0.4), png(['hook', 'jesus'], 'e_heart.png', 860, 1240), sfx(['c3', 'week'], 's_awk.mp3', 0.4),
           png(['c3', 'think'], 'e_think.png', 230, 1240), ov(['c4', 'tiger'], 'greenflash2.mp4'), sfx(['c4', 'goat', 1], 's_correct.mp3', 0.4)]),
 'tvslab': dict(top='He kept this card 4 YEARS… then gave it away', hl={'YEARS…': '#58EE28', '4': '#58EE28'},
   cta='*would you give this away?*', music=['brevis_n', 36], ctaAt=['c2', 'shirt'],
   tints=[[['hook', 'care'], G], [['c1', 'four'], G], [['c1', 'tiger'], G], [['c2', 'glove'], G], [['c2', 'wow'], G]], rizz=[['c1', 'tiger']],
   punch=[['hook', 'care'], ['hook', 'me?'], ['c1', 'four'], ['c1', 'exquisite'], ['c1', 'tiger'], ['c1', 'game'], ['c1', 'patch'], ['c2', 'tiger'], ['c2', 'shirt'], ['c2', 'cap'], ['c2', 'wow']],
   blowouts=[['c1', 'tiger']], blackFlash=[['c1']], streaks=[['c2']],
   extras=[sfx(['hook', 'me?'], 's_huh.mp3', 0.4), png(['hook', 'me?'], 'e_heart.png', 860, 1240), ov(['c1', 'tiger'], 'cashfall.mp4', 52),
           sfx(['c1', 'tiger'], 's_money.mp3', 0.4), sfx(['c2', 'wow'], 's_wow.mp3', 0.4), png(['c2', 'wow'], 'e_sob.png', 230, 1240)]),
 'tvpeyton': dict(top='He called PEYTON when his rookie year went BAD', hl={'BAD': '#FF2A2A', 'PEYTON': '#58EE28'},
   cta='*who would YOU call?*', music=['blue_n', 21.5], ctaAt=['c4', 'yeah'],
   tints=[[['hook', 'not'], R], [['c1', 'text'], G], [['c3', 'one'], G], [['c4', 'challenges'], R], [['c4', 'interceptions'], R]], rizz=[['c1', 'text'], ['c3', 'one']],
   punch=[['hook', 'rookie'], ['hook', 'not'], ['c1', 'text'], ['c1', 'season'], ['c2', 'look'], ['c3', 'one'], ['c4', 'perspective'], ['c4', 'challenges'], ['c4', 'indy'], ['c4', 'interceptions'], ['c4', 'rough']],
   blowouts=[['c4', 'interceptions']], blackFlash=[['c4']], streaks=[['c1'], ['c3']],
   extras=[png(['c1', 'text'], 'e_heart.png', 860, 1240), sfx(['c3', 'one'], 's_ding.mp3', 0.35), sfx(['c4', 'interceptions'], 's_fahhh.mp3', 0.35),
           png(['c4', 'interceptions'], 'e_sob.png', 230, 1240)]),
 'tvplays': dict(top='NFL playbooks have HUNDREDS of plays', hl={'HUNDREDS': '#58EE28'},
   cta='*could you learn a playbook?*', music=['phonk_n', 0.5], ctaAt=['c4', 'inventory'],
   tints=[[['hook', 'eight'], G], [['c1', 'playbook'], G], [['c2', 'hundreds'], G], [['c3', 'everything'], R], [['c4', 'week'], G]], rizz=[['c2', 'hundreds']],
   punch=[['hook', 'new'], ['hook', 'eight'], ['hook', 'ten'], ['c1', 'playbook'], ['c1', 'week'], ['c2', 'entire'], ['c2', 'hundreds'], ['c2', 'ton'], ['c3', 'everything'], ['c4', 'whole'], ['c4', 'running']],
   blowouts=[['c2', 'hundreds']], blackFlash=[['c2']], streaks=[['c3'], ['c4']],
   extras=[ov(['c2', 'hundreds'], 'greenflash2.mp4'), sfx(['c2', 'hundreds'], 's_wow.mp3', 0.4), png(['c3', 'everything'], 'e_sob.png', 860, 1240),
           sfx(['c3', 'everything'], 's_fahhh.mp3', 0.35), png(['hook', 'ten'], 'e_think.png', 230, 1240), sfx(['hook', 'ten'], 's_huh.mp3', 0.4)]),
}
for eid, c in CFG.items():
    c.update(track='none', calls=[], intro=True, hardcut=True, cutSfx='s_camflash.mp3', src=f'g67_{eid}.mp4')
    sc = {s['id']: s for s in gen[eid]}
    refs = [('tints', r) for r, _ in c['tints']] + [(k, r) for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks') for r in c[k]] + [('cta', c['ctaAt'])] + [('x', e['at']) for e in c['extras']]
    for key, r in refs:
        assert r[0] in sc, (eid, key, r)
        if len(r) == 1: continue
        ws = [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())]
        assert len(ws) > (r[2] if len(r) > 2 else 0), (eid, key, r, [w['word'] for w in sc[r[0]]['words']])
json.dump(CFG, open('src/tv5.cfg.json', 'w'), indent=1); print('cfg ok')

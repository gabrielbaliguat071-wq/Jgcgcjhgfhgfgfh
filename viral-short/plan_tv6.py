"""Trevor x5 (Nov 17) in the VverPaldo style: payoff hook -> hard cut (2-frame white flash + camera flash) -> story that
ends right before the hook line (loops). Pre-graded (67) excerpts public/g67_<id>.mp4 (gitignored), times below are SOURCE
seconds; the script shifts them to the excerpt. Crops = (t, centre x, zoom, centre y) in 1920x1080 source px, picked from
frame strips of who is talking. Words come from src/plans/data/<src>.words.json (faster-whisper) + fixes below.
Run from viral-short/: python3 plan_tv5.py ../footage/src"""
import json, os, subprocess, sys
SRC = sys.argv[1]
G67 = ("split[ga][gb];[gb]gblur=sigma=14[gg];[ga][gg]blend=all_mode=softlight:all_opacity=0.245,unsharp=5:5:1.74:5:5:0,"
       "eq=contrast=1.113:saturation=1.26:gamma=0.98,curves=all='0/0 0.25/0.21 0.75/0.81 1/1',unsharp=3:3:0.79,format=yuv420p")
T, L, R, TL, TR, W = (960, 1.6, 520), (470, 1.6, 460), (1500, 1.6, 460), (715, 1.15, 450), (1230, 1.15, 450), (960, 1.0, 540)
def tt(z=1.75): return (960, z, 510)  # tighter on Trevor

EDITS = {
 'tvpresnap': ('v_presnap', (0, 37.5), {(27.66, 'chain'): 'changes'}, [
     ('hook', 20.40, 23.12, [(20.40, T)]),
     ('c1', 0.00, 9.20, [(0.00, (470, 1.6, 460)), (5.90, TL)]),
     ('c2', 9.60, 18.02, [(9.60, T), (13.80, tt(1.8))]),
     ('c3', 23.14, 34.95, [(23.14, T), (29.38, tt(1.85))])]),
 'tvpacks': ('backyard_packs', (0, 29.2), {(16.14, 't'): 'TL', (16.26, '-l'): '', (18.48, 't'): 'TL', (18.66, '-l'): '', (5.28, '.com.'): '.com', (14.64, 'godfather?'): ''}, [
     ('hook', 19.24, 24.96, [(19.24, (470, 1.6, 460)), (24.10, tt(1.8))]),
     ('c1', 2.96, 19.20, [(2.96, (470, 1.6, 460)), (11.50, TL), (15.40, (470, 1.6, 460))])]),
 'tvking': ('u5_trevor_enters', (0, 13.7), {}, [
     ('hook', 9.70, 13.40, [(9.70, (1060, 1.25, 500))]),
     ('c1', 0.00, 13.60, [(0.00, (830, 1.3, 470)), (5.20, W), (9.70, (1060, 1.25, 500))])]),
 'tvmarino': ('nt_rip', (50, 80), {(62.16, 'marino.'): 'Marino.'}, [
     ('hook', 64.70, 66.10, [(64.70, (980, 1.55, 500))]),
     ('c1', 53.20, 71.10, [(53.20, (980, 1.35, 520)), (61.60, (620, 1.15, 450)), (64.70, (980, 1.55, 500)), (67.00, (980, 1.35, 520))])]),
 'tvartist': ('t2_dream_golf_four', (58, 78), {(69.02, 'cablepton'): 'Stapleton', (72.26, 'shout'): 'shout', (72.26, 'on'): 'out'}, [
     ('hook', 70.10, 71.40, [(70.10, T)]),
     ('c1', 60.40, 76.20, [(60.40, TL), (65.90, T), (71.55, tt(1.8)), (74.10, T)])]),
 'tvkeepsake': ('t4_natty_ticket', (40, 71), {(62.58, 'war'): 'worn'}, [
     ('hook', 66.38, 69.95, [(66.38, tt(1.8))]),
     ('c1', 41.50, 47.80, [(41.50, T)]),
     ('c2', 51.00, 66.30, [(51.00, TL), (53.80, T), (59.30, tt(1.8))])]),
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
 'tvpresnap': dict(top='How often does an NFL QB REALLY know who is open?', hl={'REALLY': '#58EE28'}, cta='*could you read a defense?*', music=['sentamento_n', 57.5],
   ctaAt=['c3', 'coverage'],
   tints=[[['hook', 'here'], G], [['c1', 'open'], G], [['c2', '50'], G], [['c3', 'cover'], R]], rizz=[['c2', '50']],
   punch=[['hook', 'should'], ['hook', 'there'], ['c1', 'percentage'], ['c1', 'open'], ['c2', '50'], ['c2', '65'], ['c3', '25'], ['c3', '15'], ['c3', 'move']],
   blowouts=[['c2', '65']], blackFlash=[['c3']], streaks=[['c2'], ['c3']],
   extras=[png(['hook', 'there'], 'e_think.png', 860, 1240), sfx(['hook', 'there'], 's_huh.mp3', 0.4), ov(['c2', '65'], 'greenflash2.mp4'), sfx(['c3', 'cover'], 's_fahhh.mp3', 0.35)]),
 'tvpacks': dict(top='Imagine a pack where EVERY card is YOU', hl={'EVERY': '#58EE28', 'YOU': '#58EE28'}, cta='*would you rip a TL pack?*', music=['funkabn_n', 33.2],
   ctaAt=['c1', 'like'],
   tints=[[['hook', 'every'], G], [['c1', 'digital'], G], [['c1', 'tl'], G]], rizz=[['hook', 'every']],
   punch=[['hook', 'every'], ['hook', 'trevor'], ['hook', 'weird'], ['c1', 'backyard'], ['c1', 'shipped'], ['c1', 'wax'], ['c1', 'tl'], ['c1', 'locked']],
   blowouts=[['hook', 'trevor']], blackFlash=[['c1']], streaks=[['c1', 'like']],
   extras=[sfx(['hook', 'weird'], 's_huh.mp3', 0.4), png(['hook', 'weird'], 'e_laugh.png', 860, 1240), png(['c1', 'tl'], 'e_think.png', 230, 1240), sfx(['c1', 'tl'], 's_ding.mp3', 0.35)]),
 'tvking': dict(top='When an NFL QB walks into your stream', hl={'NFL': '#58EE28', 'QB': '#58EE28'}, cta='*would you bow too?*', music=['empire_n', 18.8],
   ctaAt=['c1', 'boys'],
   tints=[[['hook', 'boys'], G], [['c1', 'king'], G], [['c1', 'king', 2], G]], rizz=[['c1', 'king']],
   punch=[['hook', 'boys'], ['c1', 'hail'], ['c1', 'king'], ['c1', 'hail', 1], ['c1', 'king', 1], ['c1', 'king', 2], ['c1', 'boys']],
   blowouts=[['c1', 'king', 2]], blackFlash=[['c1']], streaks=[['c1', 'boys']],
   extras=[png(['c1', 'king'], 'e_laugh.png', 860, 1240), sfx(['c1', 'king', 1], 's_wow.mp3', 0.35), ov(['c1', 'boys'], 'greenflash2.mp4')]),
 'tvmarino': dict(top='Is Dan Marino a TOP 10 QB of all time?', hl={'TOP': '#58EE28', '10': '#58EE28'}, cta='*top 10 or not?*', music=['phonk_n', 22.4],
   ctaAt=['c1', 'he', 1],
   tints=[[['hook', 'top'], G], [['c1', 'marino'], G], [['c1', 'sling'], G]], rizz=[['c1', 'marino']],
   punch=[['hook', 'top'], ['hook', 'got'], ['c1', 'atwater'], ['c1', 'trevor'], ['c1', 'dan'], ['c1', 'top'], ['c1', 'sling'], ['c1', 'rip']],
   blowouts=[['c1', 'marino']], blackFlash=[['c1']], streaks=[['c1', 'dan']],
   extras=[png(['c1', 'marino'], 'e_think.png', 230, 1240), sfx(['c1', 'top'], 's_huh.mp3', 0.4), sfx(['c1', 'sling'], 's_wow.mp3', 0.35)]),
 'tvartist': dict(top='His parents were in the chat the WHOLE time', hl={'WHOLE': '#58EE28'}, cta='*shout out your parents*', music=['blue_n', 21.5],
   ctaAt=['c1', 'shout'],
   tints=[[['hook', 'love'], G], [['c1', 'stapleton'], G], [['c1', 'mom'], G]], rizz=[['c1', 'mom']],
   punch=[['hook', 'love'], ['hook', 'unbelievable'], ['c1', 'favorite'], ['c1', 'stapleton'], ['c1', 'chris'], ['c1', 'mom'], ['c1', 'dad', 1], ['c1', 'father']],
   blowouts=[['c1', 'mom']], blackFlash=[['c1']], streaks=[['c1', 'favorite', 1]],
   extras=[png(['c1', 'mom'], 'e_heart.png', 860, 1240), sfx(['c1', 'mom'], 's_ding.mp3', 0.3), png(['c1', 'father'], 'e_heart.png', 230, 1240)]),
 'tvkeepsake': dict(top='He has signed a TON of these… but never kept one', hl={'TON': '#58EE28'}, cta='*what would YOU keep?*', music=['montagem_n', 24.0],
   ctaAt=['c2', 'kept'],
   tints=[[['hook', 'national'], G], [['c1', 'signed'], G], [['c2', 'college'], G]], rizz=[['c1', 'signed']],
   punch=[['hook', 'ticket'], ['hook', 'sweet'], ['c1', 'memory'], ['c1', 'signed'], ['c1', 'ton'], ['c2', 'jerseys'], ['c2', 'college'], ['c2', 'closet'], ['c2', 'look']],
   blowouts=[['hook', 'sweet']], blackFlash=[['c2']], streaks=[['c2', 'i', 3]],
   extras=[png(['hook', 'sweet'], 'e_heart.png', 860, 1240), sfx(['c1', 'ton'], 's_wow.mp3', 0.35), sfx(['c2', 'closet'], 's_ding.mp3', 0.3)]),
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
json.dump(CFG, open('src/tv6.cfg.json', 'w'), indent=1); print('cfg ok')

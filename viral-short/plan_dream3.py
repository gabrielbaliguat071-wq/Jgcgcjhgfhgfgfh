"""Dreamscape (Roblox, BloxClips campaign 2026-11-25) x3 — original VverPaldo (Guess.tsx) + AI voiceover (Kokoro am_puck/am_michael) + meme SFX/emojis.
Official footage only (files.bloxclips.com, campaign json). Each video = a timeline assembled from clips under the VO (VO loud, gameplay audio 0.22),
then Guess scenes hook (first ~2.5 s) + story from the same timeline. CTA: 'Play Dreamscape by BackfireStudios on Roblox. It's free.'"""
import json, subprocess, os
D = '../footage/dream/'
TL = {
 'dreameater': [('Dream_Eater_Intro_and_Boss_World_Unlock', 0.0, 1.9), ('Plaza_Walk_Under_the_Dream_Eater', 3.0, 2.5), ('Dream_Eater_Intro_and_Boss_World_Unlock', 3.0, 1.9),
   ('Dream_Eater_Intro_and_Boss_World_Unlock', 1.0, 0.9), ('Nightmare_Bosses_and_Dream_Eater_Wait', 0.0, 0.8), ('Nightmare_Bosses_and_Dream_Eater_Wait', 0.9, 2.2),
   ('Dream_Eater_Intro_and_Boss_World_Unlock', 2.0, 0.9), ('Rock_Toss_Hits_for_102_1K', 1.0, 2.1), ('Plaza_Walk_Under_the_Dream_Eater', 6.0, 4.4)],
 'dreamfame': [('Hall_of_Fame_Leaderboards_Scrolling', 0.0, 1.6), ('Plaza_Walk_Past_Hall_of_Fame_and_Starfall_Gate', 9.5, 3.5), ('Hall_of_Fame_Leaderboards_Scrolling', 1.6, 0.8),
   ('Hall_of_Fame_Leaderboards_Scrolling', 3.0, 2.7), ('Combat_Power_and_Weekly_Kills_Boards', 2.0, 2.0), ('Huge_Glowing_Crystal_Creature_Appears', 4.0, 3.2),
   ('Plaza_Walk_Past_Hall_of_Fame_and_Starfall_Gate', 0.0, 4.5)],
 'dreambay': [('Bubble_Bay_Opens_and_Crabs_Appear', 5.2, 1.6), ('Moonlit_Marsh_Blob_Monsters_Entrance', 2.0, 1.7), ('Bubble_Bay_Opens_and_Crabs_Appear', 4.9, 2.1),
   ('Moonlit_Marsh_Blob_Monsters_Entrance', 4.0, 2.5), ('Walking_Into_Toybox_Town', 1.0, 1.2), ('1_8M_Hit_Among_Golems', 4.0, 2.7),
   ('Plaza_Walk_Past_Hall_of_Fame_and_Starfall_Gate', 5.5, 2.4), ('Riding_a_Mount_Through_Candy_Land', 0.5, 4.4)],
}
VO = {'dreameater': 'eater', 'dreamfame': 'fame', 'dreambay': 'bay'}
HOOK = {'dreameater': 1.9, 'dreamfame': 1.6, 'dreambay': 3.3}
FIX = {'dream': 'Dream', 'eater': 'Eater', 'dreamless': 'Dreamless', 'depths,': 'Depths', 'depths': 'Depths', 'boss': 'Boss', 'world': 'World', 'hall': 'Hall', 'fame?': 'Fame?', 'play': 'Play'}
gen = json.load(open('src/edits.gen.json'))
for eid, segs in TL.items():
    tmp = f'/tmp/claude-0/dr_{eid}'; os.makedirs(tmp, exist_ok=True); parts = []
    for i, (c, a, d) in enumerate(segs):
        o = f'{tmp}/s{i}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-t', str(d), '-i', D + c + '.mp4', '-vf', 'scale=1920:1200:flags=lanczos,crop=1920:1080:0:60,fps=30,format=yuv420p',
                        '-af', 'aresample=48000', '-ac', '2', '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-c:a', 'aac', '-b:a', '192k', o], check=True)
        parts.append(o)
    open(f'{tmp}/l.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/l.txt', '-c', 'copy', f'{tmp}/v.mp4'], check=True)
    vo = f'../public/inside/dr_{VO[eid]}.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{tmp}/v.mp4', '-i', vo, '-filter_complex', '[0:a]volume=0.22[g];[1:a]aresample=48000,volume=1.15[v];[g][v]amix=inputs=2:duration=first:normalize=0[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', f'public/{eid}.mp4'], check=True)
    total = sum(d for _, _, d in segs); h = HOOK[eid]
    W = json.load(open(f'../src/inside/dr_{VO[eid]}.words.json')); m = []
    for w in W:
        t = w['text']; k = t.lower()
        if m and t.startswith(('.', ',')) and t[1:2].isdigit(): m[-1]['text'] += t.rstrip(',.'); continue
        if k.startswith('studios') and m and m[-1]['text'].lower().startswith('backfire'): m[-1]['text'] = 'BackfireStudios'; continue
        m.append(dict(w, text=FIX.get(k, t)))
    scenes = []
    for sid, a, b in [('hook', 0.0, h), ('c1', h, total)]:
        n = round((b - a) * 30); ws = []
        for w in m:
            s0 = w['startMs'] / 1000
            if not (a - 0.02 <= s0 < b - 0.05): continue
            f0 = max(0, round((s0 - a) * 30)); f1 = min(n, max(f0 + 4, round((w['endMs'] / 1000 - a) * 30) + 3))
            t = w['text'].strip(',.') if not w['text'].endswith('?') else w['text']
            ws.append({'word': t, 'startFrame': f0, 'endFrame': f1})
        for i in range(len(ws) - 1): ws[i]['endFrame'] = max(ws[i]['endFrame'], ws[i + 1]['startFrame'])
        scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'cropX': 960, 'crops': [[0, 960, 1.0, 540]], 'words': ws})
    gen[eid] = scenes; print(eid, round(total, 1), 's |', ' '.join(w['word'] for s in scenes for w in s['words'])[:200])
json.dump(gen, open('src/edits.gen.json', 'w'))
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
G, R = 'G', 'R'
def png(at, f, x=870, y=1290, size=200): return dict(at=at, kind='png', file=f, x=x, y=y, size=size)
def sfx(at, f, v=0.4): return dict(at=at, kind='sfx', file=f, v=v)
G, R = 'G', 'R'
CFG = {
 'dreameater': dict(top='This Roblox boss was watching you the WHOLE time', hl={'WHOLE': '#FF2A2A'}, cta='*play Dreamscape on Roblox*', music=['phonk_n', 22.4], ctaAt=['c1', 'Dreamscape'],
   tints=[[['hook', 'woke'], R], [['c1', 'plaza'], R], [['c1', 'nightmare'], R]], rizz=[['c1', 'Dreamless']],
   punch=[['hook', 'Dream'], ['hook', 'woke'], ['c1', 'hanging'], ['c1', 'plaza'], ['c1', 'worlds'], ['c1', 'Dreamless'], ['c1', 'nightmare'], ['c1', 'Boss'], ['c1', 'every'], ['c1', 'Dreamscape']],
   blowouts=[['c1', 'nightmare']], blackFlash=[['c1', 'hanging']], streaks=[['c1', 'then']],
   extras=[png(['hook', 'woke'], 'emoji/1f631.png'), sfx(['c1', 'hanging'], 'm_oh-hell-nah.mp3', 0.45), png(['c1', 'plaza'], 'emoji/1f440.png', 230, 1240), sfx(['c1', 'nightmare'], 'm_mg-boom.mp3', 0.45),
           png(['c1', 'nightmare'], 'emoji/1f480.png'), sfx(['c1', 'Dreamscape'], 'm_meme-tada.mp3', 0.3)]),
 'dreamfame': dict(top='Get top 3 in this Roblox game and your name turns GOLD', hl={'GOLD': '#FFD21F'}, cta='*play Dreamscape on Roblox*', music=['empire_n', 18.8], ctaAt=['c1', 'Dreamscape'],
   tints=[[['hook', 'Hall'], G], [['c1', 'gold'], G]], rizz=[['c1', 'gold']],
   punch=[['hook', 'name'], ['hook', 'Hall'], ['c1', 'top'], ['c1', 'giant'], ['c1', 'plaza'], ['c1', 'coins'], ['c1', 'fastest'], ['c1', 'weekly'], ['c1', 'combat'], ['c1', '3'], ['c1', 'gold'], ['c1', 'Dreamscape']],
   blowouts=[['c1', 'gold']], blackFlash=[['c1', 'Most']], streaks=[['c1', 'and']],
   extras=[png(['hook', 'Hall'], 'emoji/1f451.png'), sfx(['c1', 'giant'], 's_wow.mp3', 0.35), sfx(['c1', 'gold'], 'm_anime-wow.mp3', 0.45), png(['c1', 'gold'], 'emoji/1f525.png', 230, 1240),
           png(['c1', 'coins'], 'emoji/1f4b0.png'), sfx(['c1', 'Dreamscape'], 'm_meme-tada.mp3', 0.3)]),
 'dreambay': dict(top='Every world in this Roblox game looks COMPLETELY different', hl={'COMPLETELY': '#58EE28'}, cta='*play Dreamscape on Roblox*', music=['funkabn_n', 33.2], ctaAt=['c1', 'Dreamscape'],
   tints=[[['hook', 'different'], G], [['c1', 'blob'], R], [['c1', '1.8'], G]], rizz=[['c1', 'Bubble']],
   punch=[['hook', 'world'], ['hook', 'different'], ['c1', 'Bubble'], ['c1', 'crabs'], ['c1', 'Moonlit'], ['c1', 'blob'], ['c1', 'Toybox'], ['c1', 'Crystal'], ['c1', '1.8'], ['c1', 'gate'], ['c1', 'Dreamscape']],
   blowouts=[['c1', '1.8']], blackFlash=[['c1', 'Moonlit']], streaks=[['c1', 'Toybox']],
   extras=[png(['hook', 'different'], 'emoji/1f633.png'), sfx(['c1', 'crabs'], 's_huh.mp3', 0.35), png(['c1', 'crabs'], 'emoji/1f602.png', 230, 1240), sfx(['c1', '1.8'], 'm_anime-wow.mp3', 0.45),
           png(['c1', '1.8'], 'emoji/1f525.png'), sfx(['c1', 'Dreamscape'], 'm_meme-tada.mp3', 0.3)]),
}
allc = json.load(open('src/yv.cfg.json'))
for eid, c in CFG.items():
    c.update(track='none', calls=[], intro=True, hardcut=True, cutSfx='s_camflash.mp3', src=f'{eid}.mp4', blurBg=True)
    sc = {s['id']: s for s in gen[eid]}
    for r in [r for r, _ in c['tints']] + [r for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks') for r in c[k]] + [c['ctaAt']] + [e['at'] for e in c['extras']]:
        if len(r) == 1: continue
        assert [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())], (eid, r, [w['word'] for w in sc[r[0]]['words']])
    allc[eid] = c
json.dump(allc, open('src/yv.cfg.json', 'w'), indent=1); print('cfg ok')

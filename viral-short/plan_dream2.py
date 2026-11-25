"""Dreamscape (Roblox, BloxClips campaign 2026-11-25) x3 — original VverPaldo (Guess.tsx) + AI voiceover (Kokoro am_puck/am_michael) + meme SFX/emojis.
Official footage only (files.bloxclips.com, campaign json). Each video = a timeline assembled from clips under the VO (VO loud, gameplay audio 0.22),
then Guess scenes hook (first ~2.5 s) + story from the same timeline. CTA: 'Play Dreamscape by BackfireStudios on Roblox. It's free.'"""
import json, subprocess, os
D = '../footage/dream/'
TL = {
 'dreamsteal': [('Night_Market_Stalls_and_Steal_Prompts', 0.0, 3.3), ('Night_Market_Stalls_and_Steal_Prompts', 5.4, 1.4), ('Night_Market_Stalls_and_Steal_Prompts', 7.0, 1.3),
   ('Night_Market_Stalls_and_Steal_Prompts', 8.3, 0.8), ('Touring_the_Plaza_Trade_Hall_and_Bank', 0.0, 4.2), ('Touring_the_Plaza_Trade_Hall_and_Bank', 4.6, 1.8),
   ('Bubble_Bay_Opens_and_Crabs_Appear', 4.0, 2.9), ('Moonlit_Marsh_Blob_Monsters_Entrance', 2.0, 1.6)],
 'dreampotions': [('Stacking_Four_Potion_Boosts_At_Once', 4.0, 1.0), ('Stacking_Four_Potion_Boosts_At_Once', 2.0, 1.1), ('Stacking_Four_Potion_Boosts_At_Once', 5.8, 1.2),
   ('Stacking_Four_Potion_Boosts_At_Once', 8.0, 1.4), ('Crystal_Golem_Hits_and_Power_Hour_Banner', 0.0, 3.1), ('Crystal_Golem_Hits_and_Power_Hour_Banner', 6.5, 3.0),
   ('Power_Hour_Golem_Fight_With_883K_Hit', 0.6, 1.4), ('1_7M_Hit_on_Crystal_Golems', 5.6, 1.3), ('Golem_Hits_680K_Under_Lucky_Hour', 0.5, 4.5)],
 'dreamgolem': [('Huge_Glowing_Crystal_Creature_Appears', 2.6, 2.6), ('Crystal_Golem_Awakens_Mid_Fight', 0.4, 1.9), ('Giant_Golem_Shrugs_Off_Blocked_Attack', 3.0, 2.0),
   ('Crystal_Spikes_Erupt_Over_Golem_Fight', 1.0, 1.6), ('Mega_Crystal_Golem_Boss_Fight', 1.0, 2.2), ('Entering_the_Crystal_Rift_Portal', 0.5, 1.3),
   ('Crystal_Rift_Combo_With_1_1M_Damage', 0.0, 2.5), ('Mega_Crystal_Golem_Boss_Fight', 4.0, 4.4)],
}
VO = {'dreamsteal': 'steal', 'dreampotions': 'potions', 'dreamgolem': 'golem'}
HOOK = {'dreamsteal': 3.3, 'dreampotions': 2.1, 'dreamgolem': 2.6}
FIX = {'trade': 'Trade', 'hall': 'Hall', 'exp,': 'XP', 'power': 'Power', 'hour': 'Hour', 'mega': 'Mega', 'crystal': 'Crystal', 'rift': 'Rift', 'play': 'Play', 'kills,': 'KILLS'}
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
 'dreamsteal': dict(top='This Roblox game lets you STEAL from the night market', hl={'STEAL': '#FF2A2A'}, cta='*play Dreamscape on Roblox*', music=['funkabn_n', 33.2], ctaAt=['c1', 'Dreamscape'],
   tints=[[['hook', 'steal'], R], [['c1', 'Steal'], R], [['c1', 'Trade'], G]], rizz=[['c1', 'Trade']],
   punch=[['hook', 'night'], ['hook', 'steal'], ['c1', 'stall'], ['c1', 'prompt'], ['c1', 'Steal'], ['c1', 'risky'], ['c1', 'Trade'], ['c1', 'every'], ['c1', 'bank'], ['c1', 'Dreamscape']],
   blowouts=[['c1', 'Steal']], blackFlash=[['c1', 'Too']], streaks=[['c1', 'Then']],
   extras=[sfx(['hook', 'steal'], 's_huh.mp3', 0.45), png(['hook', 'steal'], 'emoji/1f440.png'), sfx(['c1', 'Steal'], 'm_record-scratch.mp3', 0.45), png(['c1', 'Steal'], 'emoji/1f608.png', 230, 1240),
           sfx(['c1', 'bank'], 'm_cha-ching.mp3', 0.4), png(['c1', 'coins'], 'emoji/1f4b0.png'), sfx(['c1', 'Dreamscape'], 'm_meme-tada.mp3', 0.3)]),
 'dreampotions': dict(top='What happens when you stack ALL 4 potions?', hl={'ALL': '#58EE28', '4': '#58EE28'}, cta='*play Dreamscape on Roblox*', music=['phonk_n', 22.4], ctaAt=['c1', 'Dreamscape'],
   tints=[[['hook', 'KILLS'], G], [['c1', 'stack'], G], [['c1', '1.7'], G]], rizz=[['c1', 'stack']],
   punch=[['hook', 'KILLS'], ['hook', 'XP'], ['c1', 'damage'], ['c1', 'drop'], ['c1', 'stack'], ['c1', 'four'], ['c1', 'Power'], ['c1', 'numbers'], ['c1', '883'], ['c1', '1.7'], ['c1', 'million'], ['c1', 'Dreamscape']],
   blowouts=[['c1', '1.7']], blackFlash=[['c1', 'Power']], streaks=[['c1', 'In']],
   extras=[png(['hook', 'KILLS'], 'emoji/1f633.png'), sfx(['c1', 'stack'], 'm_rizz-sound-effect.mp3', 0.35), sfx(['c1', '883'], 'm_mg-boom.mp3', 0.45), png(['c1', '883'], 'emoji/1f525.png', 230, 1240),
           sfx(['c1', '1.7'], 'm_anime-wow.mp3', 0.45), png(['c1', '1.7'], 'emoji/1f480.png'), sfx(['c1', 'Dreamscape'], 'm_meme-tada.mp3', 0.3)]),
 'dreamgolem': dict(top='This Roblox boss was asleep… until NOW', hl={'NOW': '#FF2A2A'}, cta='*play Dreamscape on Roblox*', music=['empire_n', 18.8], ctaAt=['c1', 'Dreamscape'],
   tints=[[['hook', 'asleep'], G], [['c1', 'wakes'], R], [['c1', 'erupt'], R]], rizz=[['c1', 'Mega']],
   punch=[['hook', 'golem'], ['hook', 'asleep'], ['c1', 'wakes'], ['c1', 'middle'], ['c1', 'shrugs'], ['c1', 'spikes'], ['c1', 'erupt'], ['c1', 'Mega'], ['c1', 'Rift'], ['c1', '1.1'], ['c1', 'Dreamscape']],
   blowouts=[['c1', 'wakes']], blackFlash=[['c1', 'Crystal']], streaks=[['c1', 'Jump']],
   extras=[png(['hook', 'asleep'], 'emoji/1f633.png'), sfx(['c1', 'wakes'], 'm_oh-hell-nah.mp3', 0.45), png(['c1', 'wakes'], 'emoji/1f631.png', 230, 1240), sfx(['c1', 'erupt'], 'm_mg-boom.mp3', 0.45),
           sfx(['c1', '1.1'], 'm_anime-wow.mp3', 0.45), png(['c1', '1.1'], 'emoji/1f525.png'), sfx(['c1', 'Dreamscape'], 'm_meme-tada.mp3', 0.3)]),
}
allc = json.load(open('src/yv.cfg.json'))
for eid, c in CFG.items():
    c.update(track='none', calls=[], intro=True, hardcut=True, cutSfx='s_camflash.mp3', src=f'{eid}.mp4')
    sc = {s['id']: s for s in gen[eid]}
    for r in [r for r, _ in c['tints']] + [r for k in ('rizz', 'punch', 'blowouts', 'blackFlash', 'streaks') for r in c[k]] + [c['ctaAt']] + [e['at'] for e in c['extras']]:
        if len(r) == 1: continue
        assert [w for w in sc[r[0]]['words'] if w['word'].lower().startswith(r[1].lower())], (eid, r, [w['word'] for w in sc[r[0]]['words']])
    allc[eid] = c
json.dump(allc, open('src/yv.cfg.json', 'w'), indent=1); print('cfg ok')

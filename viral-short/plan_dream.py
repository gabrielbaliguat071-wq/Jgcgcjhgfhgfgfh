"""Dreamscape (Roblox, BloxClips campaign 2026-11-25) x3 — original VverPaldo (Guess.tsx) + AI voiceover (Kokoro am_puck/am_michael) + meme SFX/emojis.
Official footage only (files.bloxclips.com, campaign json). Each video = a timeline assembled from clips under the VO (VO loud, gameplay audio 0.22),
then Guess scenes hook (first ~2.5 s) + story from the same timeline. CTA: 'Play Dreamscape by BackfireStudios on Roblox. It's free.'"""
import json, subprocess, os
D = '../footage/dream/'
TL = {  # (clip, start, dur) laid end to end
 'dreamboss': [('Dazed_Tyrant_Takes_771_8K_Hit', 0.0, 2.5), ('Horde_Tyrant_Charge_and_Stomp_in_Plaza', 0.0, 1.1), ('Horde_Tyrant_Charge_and_Stomp_in_Plaza', 1.2, 2.6),
   ('Shield_Down_Banner_on_Horde_Tyrant', 4.0, 2.2), ('Tyrant_Cleave_and_Weak_Point_123_5K_Hit', 3.0, 1.0), ('Dazed_Tyrant_Takes_771_8K_Hit', 0.3, 1.9),
   ('Big_Grumble_Rises_After_Tyrant_Hit', 2.5, 2.9), ('Big_Grumble_Opens_With_623_4K_Hit', 1.0, 3.0), ('Big_Grumble_Fist_Smash_on_the_Plaza', 2.0, 4.0)],
 'dreamfree': [('Dream_Wheel_Spins_With_Reward_Particles', 0.0, 3.0), ('Dream_Wheel_Spins_With_Reward_Particles', 8.0, 1.0), ('Opening_Playtime_Gift_Boxes', 0.5, 1.8),
   ('Claiming_the_Free_Gift_Mount_Roll', 0.5, 1.2), ('Claiming_the_Free_Gift_Mount_Roll', 4.0, 1.2), ('Rolling_a_Common_Gumdrop_Tortoise_Mount', 0.0, 2.1),
   ('Rolling_a_Common_Gumdrop_Tortoise_Mount', 4.0, 2.0), ('Riding_a_Mount_Through_Candy_Land', 0.5, 2.4), ('Riding_a_Mount_Through_Candy_Land', 3.0, 4.0)],
 'dreamworlds': [('First_Puffball_Hits_In_Meadow', 3.0, 1.0), ('Crystal_Caverns_Golem_Fight_With_1_8M_Hit', 4.0, 2.0), ('Zone_Cleared_Next_Is_Crystal_Caverns', 0.0, 2.6),
   ('First_Puffball_Hits_In_Meadow', 6.0, 1.6), ('Zone_Cleared_Next_Is_Crystal_Caverns', 4.0, 1.8), ('Zone_2_Completed_In_Gumdrop_Grove', 0.0, 0.9),
   ('Walking_Into_Toybox_Town', 1.0, 0.9), ('Crystal_Caverns_Golem_Fight_With_1_8M_Hit', 6.0, 2.2), ('MAGIC_LEVEL_60_Reached_in_Combat', 5.0, 1.0),
   ('Mega_Crystal_Golem_Boss_Fight', 2.0, 1.8), ('Plaza_Walk_Toward_Cotton_Cloud_Meadow', 2.0, 1.6), ('Mega_Crystal_Golem_Boss_Fight', 5.0, 3.8)],
}
VO = {'dreamboss': 'boss', 'dreamfree': 'free', 'dreamworlds': 'worlds'}
HOOK = {'dreamboss': 2.5, 'dreamfree': 3.0, 'dreamworlds': 3.0}
FIX = {'big': 'Big', 'grumble': 'Grumble', 'dream': 'Dream', 'wheel.': 'Wheel', 'common': 'Common', 'gumdrop': 'Gumdrop', 'tortoise.': 'Tortoise', 'candy': 'Candy', 'land.': 'Land',
       'mega': 'Mega', 'magic': 'Magic', 'from': 'From'}
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
CFG = {
 'dreamboss': dict(top='This Roblox boss lands on the plaza and NOBODY is ready', hl={'NOBODY': '#FF2A2A'}, cta='*play Dreamscape on Roblox*', music=['phonk_n', 22.4], ctaAt=['c1', 'Dreamscape'],
   tints=[[['hook', 'ready'], R], [['c1', 'dazed'], G], [['c1', 'Grumble'], R]], rizz=[['c1', 'dazed']],
   punch=[['hook', 'boss'], ['hook', 'nobody'], ['c1', 'Horde'], ['c1', 'charges'], ['c1', 'stomps'], ['c1', 'cleaves'], ['c1', 'shield'], ['c1', 'weak'], ['c1', '771'], ['c1', 'Grumble'], ['c1', 'Giant'], ['c1', 'Dreamscape']],
   blowouts=[['c1', '771']], blackFlash=[['c1', 'Big']], streaks=[['c1', 'Giant']],
   extras=[png(['hook', 'nobody'], 'emoji/1f631.png'), sfx(['c1', '771'], 'm_mg-boom.mp3', 0.5), png(['c1', '771'], 'emoji/1f525.png', 230, 1240),
           sfx(['c1', 'Big'], 'm_oh-hell-nah.mp3', 0.5), png(['c1', 'Grumble'], 'emoji/1f480.png'), sfx(['c1', 'Dreamscape'], 'm_meme-tada.mp3', 0.3)]),
 'dreamfree': dict(top='This Roblox game gives you a FREE spin every day', hl={'FREE': '#58EE28'}, cta='*play Dreamscape on Roblox*', music=['funkabn_n', 33.2], ctaAt=['c1', 'Dreamscape'],
   tints=[[['hook', 'free'], G], [['c1', 'odds'], G], [['c1', 'Common'], R]], rizz=[['hook', 'free']],
   punch=[['hook', 'free'], ['hook', 'spin'], ['hook', 'every'], ['c1', 'Wheel'], ['c1', 'gifts'], ['c1', 'mount'], ['c1', 'odds'], ['c1', 'rolled'], ['c1', 'Common'], ['c1', 'Bro'], ['c1', 'Candy'], ['c1', 'Dreamscape']],
   blowouts=[['c1', 'Bro']], blackFlash=[['c1', 'Common']], streaks=[['c1', 'Candy']],
   extras=[png(['hook', 'free'], 'emoji/1f633.png'), sfx(['c1', 'rolled'], 'm_meme-build2.mp3', 0.35), sfx(['c1', 'Common'], 's_fahhh.mp3', 0.5), png(['c1', 'Common'], 'emoji/1f62d.png'),
           sfx(['c1', 'Bro'], 'm_record-scratch.mp3', 0.45), png(['c1', 'Bro'], 'emoji/1f480.png', 230, 1240), sfx(['c1', 'Dreamscape'], 'm_meme-tada.mp3', 0.3)]),
 'dreamworlds': dict(top='From puffballs to 1.8 MILLION damage in this Roblox RPG', hl={'1.8': '#58EE28', 'MILLION': '#58EE28'}, cta='*play Dreamscape on Roblox*', music=['empire_n', 18.8], ctaAt=['c1', 'Dreamscape'],
   tints=[[['hook', 'million'], G], [['c1', 'unlock'], G], [['c1', 'golems'], R]], rizz=[['c1', 'unlock']],
   punch=[['hook', 'puffballs'], ['hook', '1.8'], ['hook', 'million'], ['c1', 'kills'], ['c1', 'unlock'], ['c1', 'Cotton'], ['c1', 'gate'], ['c1', 'Gumdrop'], ['c1', 'Toybox'], ['c1', 'Crystal'], ['c1', 'Magic'], ['c1', 'Mega'], ['c1', 'Eight'], ['c1', 'Dreamscape']],
   blowouts=[['hook', 'million']], blackFlash=[['c1', 'Crystal']], streaks=[['c1', 'Gumdrop']],
   extras=[sfx(['hook', 'million'], 'm_anime-wow.mp3', 0.45), png(['hook', 'million'], 'emoji/1f633.png'), sfx(['c1', 'golems'], 'm_mg-boom.mp3', 0.45), png(['c1', 'golems'], 'emoji/1f480.png', 230, 1240),
           png(['c1', 'Mega'], 'emoji/1f525.png'), sfx(['c1', 'Dreamscape'], 'm_meme-tada.mp3', 0.3)]),
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

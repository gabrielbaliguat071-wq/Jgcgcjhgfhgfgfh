"""Popdarts x Target (ClipHouse Campaign 2, Nov 19) — West Coast Wild Card recap (approved footage, footage/popdarts/recap5.mp4,
1920x1080 59.94). Meme.tsx with noMusic/noSfx (brief: ORIGINAL sound only, no music), hook banner during the hook, then the
approved Target overlay "POPDARTS IS NOW AVAILABLE AT TARGET 🎯" from the first cut to the end (top, never over dart/player/score).
Story = the kid (Slaymaker) vs "one of the villains of this sport" (Mr. T) in the final -> champion. Real result only.
Run from viral-short/: python3 plan_popdarts.py"""
import json, os, subprocess
SRC = '../footage/popdarts/recap5.mp4'
G67 = ("split[ga][gb];[gb]gblur=sigma=14[gg];[ga][gg]blend=all_mode=softlight:all_opacity=0.245,unsharp=5:5:1.74:5:5:0,"
       "eq=contrast=1.113:saturation=1.26:gamma=0.98,curves=all='0/0 0.25/0.21 0.75/0.81 1/1',unsharp=3:3:0.79,format=yuv420p")
B = (960, 0.5, 830)        # 16:9 band (split-screen graphics with the score bug, bracket)
IVW = (880, 1.0, 540)      # interview two-shot (host + kid)
KID = (1000, 1.0, 540)
EDITS = {
 'pdkid': [
    ('hook', 240.6, 246.5, [(240.6, B), (243.9, KID), (245.9, (960, 1.0, 540))]),
    ('c1', 82.4, 84.5, [(82.4, B)]),
    ('c2', 193.0, 195.85, [(193.0, IVW)]),
    ('c3', 203.05, 203.85, [(203.05, (1080, 1.25, 470))]),
    ('c4', 223.4, 228.0, [(223.4, B)]),
    ('c5', 265.05, 269.95, [(265.05, (980, 1.0, 540))]),
 ],
}
W = [(w['startMs'] / 1000, w['endMs'] / 1000, w['text']) for w in json.load(open('../footage/popdarts/recap5.words.json'))]
FIX = {'nober': 'nobber', 'olympia.': '', 'olympi?': ''}
gen = json.load(open('src/edits.gen.json'))
for eid, plan in EDITS.items():
    xa, xb = min(a for _, a, _, _ in plan) - 0.5, max(b for _, _, b, _ in plan) + 0.5
    out = f'public/g67_{eid}.mp4'
    if not os.path.exists(out):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(xa), '-to', str(xb), '-i', SRC, '-vf', G67 + ',fps=30', '-c:v', 'libx264', '-crf', '17',
                        '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-map_metadata', '-1', out], check=True)
    scenes = []
    for sid, a, b, crops in plan:
        n = round((b - a) * 30); words = []
        for ws, we, t in W:
            if not (a - 0.05 <= ws < b - 0.05): continue
            t2 = FIX.get(t.lower(), t)
            if not t2: continue
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t2, 'startFrame': f0, 'endFrame': f1})
        for i in range(len(words) - 1, 0, -1):
            if words[i]['word'].startswith('-'): words[i - 1]['word'] += words[i]['word']; words.pop(i)
        cr = [[max(0, round((t - a) * 30)), x, z, y] for t, (x, z, y) in crops]
        scenes.append({'id': sid, 'videoStartSec': round(a - xa, 3), 'durationInFrames': n, 'cropX': 960, 'crops': cr, 'words': words})
    gen[eid] = scenes
    print(eid, round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's |', ' / '.join(s['id'] + ': ' + ' '.join(w['word'] for w in s['words']) for s in scenes))
json.dump(gen, open('src/edits.gen.json', 'w'))

Y, GR, RD = '#FFE14D', '#5CFF5C', '#FF4D4D'
CFG = {
 'pdkid': dict(top='The KID vs the VILLAIN of Popdarts', hl={'KID': '#1DB954', 'VILLAIN': '#E3201B'}, music=['phonk_n', 0], cta='WOULD YOU MAKE THIS THROW?', ctaAt=['c5', 'best'],
   kw={'villains': RD, 'mr': RD, 'intimidated': RD, 'beat': GR, 'espn': Y, 'ocho': Y, 'way': GR, 'champion': GR, 'insane': Y, 'best': GR},
   emoji=[[['c1', 'villains'], '1f608'], [['c2', 'intimidated'], '1f633'], [['c4', 'no'], '1f631'], [['c5', 'champion'], '1f3c6']],
   punch=[['c1', 'villains'], ['c2', 'intimidated'], ['c3', 'beat'], ['c4', 'get'], ['c4', 'way'], ['c5', 'champion'], ['c5', 'best']],
   tints=[], sfx=[], noMusic=True, noSfx=True, bgBlur=10, after={'text': 'Popdarts is now available at Target', 'emoji': '1f3af'}),
}
allc = json.load(open('src/meme.cfg.json'))
for eid, c in CFG.items():
    c['src'] = f'g67_{eid}.mp4'
    sc = {s['id']: s for s in gen[eid]}
    for r in c['punch'] + [r for r, _ in c['emoji']] + [c['ctaAt']]:
        ws = [w for w in sc[r[0]]['words'] if ''.join(ch for ch in w['word'].lower() if ch.isalnum() or ch in '$-').startswith(r[1])]
        assert ws, (eid, r, [w['word'] for w in sc[r[0]]['words']])
    for _, e in c['emoji']: assert os.path.exists(f'public/res/emoji/{e}.png'), e
    allc[eid] = c
json.dump(allc, open('src/meme.cfg.json', 'w'), indent=1); print('cfg ok')

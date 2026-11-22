"""BYB Trevor batch (2026-11-20, user: Trevor clips have high virality). Sheet rows: green kaboom 1/1, shield auto, football talk (cut 1120 s), red /5, teal /199 (cut 195 s)."""
import json
Y, GR, RD = '#FFE14D', '#5CFF5C', '#FF4D4D'
TOP = [1.6, 540, 0]
NO = dict(at=-1, name='', card='', price='', cx=540, cy=960)
FIX = {'shit,': 'sh*t,', 'kingsney,': "King's knee,", 'jags': 'Jags', 'shit': 'sh*t', 'ass.': 'a**.', 'gbt': 'GPT', 's&b': 'S&P', 'smb.': 'S&P.', 'errand': 'Aaron', 'sisko.': 'Sesko.', 'lord': 'Lawrence', 'damn,': 'dead,', 'flag': 'Flagg', 'wemby': 'Wemby'}
CLIPS = {
 'tlkaboom': dict(src='tl/kaboom.mp4', wf='kaboom.words', zoom=None, bannerY=500, capY=1600, music=['phonk_n', 22.4], top=['$500 BREAK…', 'THEN THIS HAPPENED'], hl={'$500': '#1DB954'}, tEmoji='1f631',
   scenes=[(20.9, 27.0, False), (0.8, 10.0, False), (27.0, 41.0, False)], reveal=dict(at=34.0, name='TREVOR LAWRENCE', card='GREEN KABOOM 1/1', price='$15,000', cx=540, cy=1150),
   question='KEEP IT OR SELL IT?', qEmoji='1f914', qAt=38.5, kw={'$500': GR, 'heart': RD, 'strong.': Y, 'no,': RD, 'no.': RD}, emoji=[(1.5, '1f631')]),
 'tlshield': dict(src='tl/shield.mp4', wf='shield.words', zoom=None, bannerY=500, capY=1600, music=['empire_n', 18.8], top=["HE'S CHASING ONE CARD…", 'IS THIS IT?!'], hl={'IT?!': '#E3201B'}, tEmoji='1f630',
   scenes=[(16.3, 22.0, True), (9.4, 16.3, False), (22.0, 33.0, False)], reveal=dict(at=23.0, name='TREVOR LAWRENCE', card='NFL SHIELD AUTO', price='$40K–$100K', cx=540, cy=1150),
   question='WHAT WOULD YOU DO WITH IT?', qEmoji='1f914', qAt=30.0, kw={'holy': RD, 'sh*t,': RD, 'it?': Y, 'no,': RD, 'no.': RD, 'green.': Y}, emoji=[(1.0, '1f631')]),
 'tltalk': dict(src='tl/talk.mp4', wf='talk.cut.words', zoom=TOP, bannerY=830, capY=1560, music=['dubist_n', 1.0], top=["TREVOR'S STATS WOULD BE", 'EVEN CRAZIER IF…'], hl={'CRAZIER': '#1DB954'}, tEmoji='1f440',
   scenes=[(52.0, 56.4, False), (32.4, 46.0, False), (56.5, 73.8, False), (90.5, 97.1, False)], reveal=NO,
   question='IS TREVOR A TOP 5 QB?', qEmoji='1f914', qAt=94.0,
   kw={'74': RD, 'minutes': RD, '11': Y, 'third': RD, 'quarter.': RD, '30': GR, '30.': GR, '25.': GR, '29.': GR, 'dogs,': Y, 'dogs.': Y, 'trevor': Y, "trevor's": Y}, emoji=[(1.0, '1f440'), (12.0, '1f92f')]),
 'tlred': dict(src='tl/red5.mp4', wf='red5.words', zoom=None, bannerY=500, capY=1600, music=['montagem_n', 24.0], top=['THE KING', 'TO FIVE 👑'], hl={'FIVE': '#E3201B'}, tEmoji='1f451',
   scenes=[(28.6, 36.5, False), (0.9, 15.0, False), (44.0, 50.8, False)], reveal=dict(at=46.0, name='TREVOR LAWRENCE', card='RED AUTO /5', price='', cx=540, cy=1150),
   question='IS TREVOR THE BEST QB?', qEmoji='1f914', qAt=49.5, kw={'trevor': Y, 'forever': GR, 'red': RD, 'rookie': Y, 'auto': Y, 'god': RD}, emoji=[(1.0, '1f631'), (8.0, '1f924' if False else '1f633')]),
 'tlteal': dict(src='tl/teal.mp4', wf='teal.cut.words', zoom=None, bannerY=500, capY=1600, music=['blue_n', 21.5], top=["\"HE'S THE NFL!\"", 'TREVOR TEAL /199'], hl={'NFL!"': '#1DB954'}, tEmoji='1f525',
   scenes=[(17.0, 30.1, False)], reveal=dict(at=21.0, name='TREVOR LAWRENCE', card='TEAL /199', price='', cx=540, cy=1150),
   question="WHO'S THE BEST QB IN THE NFL?", qEmoji='1f914', qAt=27.0, kw={'teal!': Y, 'greatest': GR, 'quarterback': Y, 'nfl!': GR, 'pride': Y, 'joy': Y}, emoji=[(1.0, '1f525')]),
}
cfg = json.load(open('src/pull.cfg.json'))
for cid, c in CLIPS.items():
    W = json.load(open(f"../footage/tl/{c['wf']}.json"))
    scenes = []
    for a, b, blur in c['scenes']:
        ws = []
        for w in W:
            s, e, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
            if not (a - 0.05 <= s < b - 0.05): continue
            t = FIX.get(t.lower(), t)
            if c['src'].endswith('flaggpsa.mp4') and t == '50' and 56.5 < s < 57: t = '15'
            if ws and (t.startswith('-') or (t[:1] in ',.' and t[1:2].isdigit()) or t.startswith('&')): ws[-1]['w'] += t; ws[-1]['e'] = e; continue
            ws.append({'w': t, 's': s, 'e': e})
        for x in ws: x['w'] = x['w'].replace('S&B', 'S&P').replace('s&b', 'S&P').replace('s&B', 'S&P').replace('s&p', 'S&P').replace('SMB', 'S&P')
        sc = {'a': a, 'b': b, 'blur': blur, 'words': ws}
        if c['zoom']: sc['zoom'] = c['zoom']
        scenes.append(sc)
    t = 0.0; q = 0
    for s in scenes:
        if (s is not scenes[0] or len(scenes) == 1) and s['a'] <= c['qAt'] < s['b']: q = round(t + c['qAt'] - s['a'], 2)
        t += s['b'] - s['a']
    cfg[cid] = dict(src=c['src'], srcW=1080, cardY=620, top=c['top'], hl=c['hl'], tEmoji=c['tEmoji'], qEmoji=c['qEmoji'], bannerY=c['bannerY'], capY=c['capY'],
                    scenes=scenes, reveal=c['reveal'], question=c['question'], qAt=q, music=c['music'], kw=c['kw'], emoji=[{'at': x, 'e': e} for x, e in c['emoji']])
    print(cid, round(t, 1), 's | q@', q, '|', ' / '.join(' '.join(w['w'] for w in s['words']) for s in scenes)[:260])
json.dump(cfg, open('src/pull.cfg.json', 'w'), indent=1)

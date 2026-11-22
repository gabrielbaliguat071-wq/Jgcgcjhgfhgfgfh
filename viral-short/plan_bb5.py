"""Backyard Breaks batch 6 (2026-11-20): Live Stream Clips — Wemby red auto /5 ($10-30K), Flagg Gold auto comes back PSA 10 ($12-15K),
Aaron Judge card beat the S&P 500 (talk), Trevor Silver PSA 9 funny reaction, Benjamin Sesko "created the light bulb", three nukes PSA 10.
scenes = (a, b, blur) in source s. Appends to src/pull.cfg.json. Run from viral-short/: python3 plan_bb5.py"""
import json
Y, GR, RD = '#FFE14D', '#5CFF5C', '#FF4D4D'
TOP = [1.6, 540, 0]
NO = dict(at=-1, name='', card='', price='', cx=540, cy=960)
FIX = {'shit': 'sh*t', 'ass.': 'a**.', 'gbt': 'GPT', 's&b': 'S&P', 'smb.': 'S&P.', 'errand': 'Aaron', 'sisko.': 'Sesko.', 'lord': 'Lawrence', 'damn,': 'dead,', 'flag': 'Flagg', 'wemby': 'Wemby'}
CLIPS = {
 'bbwemby': dict(src='bb5/wembyred.mp4', zoom=None, bannerY=500, capY=1600, music=['phonk_n', 22.4], top=['FIRST TIME EVER', 'IN THIS PRODUCT…'], hl={'EVER': '#E3201B'}, tEmoji='1f633',
   scenes=[(83.7, 88.85, True), (24.8, 37.5, False)], reveal=dict(at=31.3, name='WEMBANYAMA', card='RED AUTO /5', price='$10K–$30K', cx=460, cy=1150),
   question='KEEP IT OR SELL IT?', qEmoji='1f914', qAt=35.3, kw={'wemby': Y, 'auto': Y, 'never': RD, 'red.': RD, 'five': RD, 'crazy': GR}, emoji=[(1.5, '1f440')]),
 'bbflagg': dict(src='bb5/flaggpsa.mp4', zoom=None, bannerY=500, capY=1600, music=['empire_n', 18.8], top=['$5K CARD… IF IT', 'COMES BACK A 10?'], hl={'10?': '#1DB954'}, tEmoji='1f630',
   scenes=[(67.0, 72.4, False), (44.4, 59.3, False), (59.3, 67.0, False), (72.4, 80.0, False)], reveal=dict(at=63.5, name='COOPER FLAGG', card='GOLD AUTO · PSA 10', price='$12K–$15K', cx=560, cy=1150),
   question='WOULD YOU SELL IT?', qEmoji='1f4b8', qAt=76.0, kw={'gold': Y, 'flag': Y, 'gem': GR, '8k': GR, 'racks': GR, 'sniper.': Y, '12': GR, 'cooper': Y}, emoji=[(1.0, '1f525')]),
 'bbsp500': dict(src='bb5/judgesp.mp4', zoom=None, bannerY=500, capY=700, music=['investigations_n', 20.0], top=['THIS CARD BEAT', 'THE STOCK MARKET'], hl={'STOCK': '#1DB954', 'MARKET': '#1DB954'}, tEmoji='1f4c8',
   scenes=[(30.0, 36.9, False), (9.6, 25.9, False), (37.1, 52.0, False)], reveal=NO,
   question='CARDS OR STOCKS?', qEmoji='1f914', qAt=48.0, kw={'4.9': GR, 'million': GR, '200,000.': RD, '25x.': GR, '25x': GR, 's&p': Y, 'judge': Y, '$4.7': GR}, emoji=[(3.0, '1f4c8'), (25.0, '1f92f')]),
 'bbtrevor': dict(src='bb5/trevorpsa.mp4', zoom=None, bannerY=500, capY=1600, music=['funkabn_n', 2.0], top=['WHAT IS THIS', 'PSA PULL?!'], hl={'PULL?!': '#E3201B'}, tEmoji='1f480',
   scenes=[(0.0, 13.6, False)], reveal=NO, question='PSA 9… OR A 10?', qEmoji='1f914', qAt=9.5,
   kw={'trevor': Y, 'lawrence': Y, 'silver,': Y, 'bang!': RD, 'whoa,': RD}, emoji=[(2.5, '1f633'), (12.0, '1f480')]),
 'bbsesko': dict(src='bb5/sesko.mp4', zoom=None, bannerY=500, capY=1600, music=['dubist_n', 1.0], top=['WHO IS', 'THIS GUY?'], hl={'GUY?': '#E3201B'}, tEmoji='1f62d',
   scenes=[(11.2, 17.9, False), (0.6, 11.2, False)], reveal=NO, question='DO YOU KNOW WHO HE IS?', qEmoji='1f914', qAt=9.0,
   kw={'benjamin': Y, 'sesko.': Y, 'light': RD, 'bulb.': RD, 'black': Y, 'sapphire': Y}, emoji=[(3.0, '1f4a1' if False else '1f602'), (7.5, '1f480')]),
 'bbnukes': dict(src='bb5/nukes.mp4', zoom=None, bannerY=500, capY=1600, music=['montagem_n', 24.0], top=['3 FOR 3…', 'ALL CAME BACK PSA 10'], hl={'10': '#1DB954'}, tEmoji='1f92f',
   scenes=[(22.0, 30.6, False), (3.4, 10.5, False), (40.3, 47.0, False), (51.8, 57.5, False)], reveal=NO,
   question='WHICH ONE IS YOUR FAVORITE?', qEmoji='1f914', qAt=55.0,
   kw={'curry,': Y, 'curry': Y, 'black,': Y, 'lebron': Y, 'red,': RD, 'cooper,': Y, 'three': GR, 'way.': RD, 'like': GR}, emoji=[(1.0, '1f631'), (9.0, '1f525')]),
}
cfg = json.load(open('src/pull.cfg.json'))
for cid, c in CLIPS.items():
    W = json.load(open(f"../footage/bb5/{c['src'].split('/')[1].replace('.mp4', '')}.words.json"))
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

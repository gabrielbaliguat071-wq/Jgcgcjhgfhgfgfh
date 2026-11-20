"""Backyard Breaks batch 5 (2026-11-20) — copy what went viral for BYB (sheet tab "Historical Viral Content": money stories, funny moments,
deals beat plain pulls). Live Stream Clips: broccoli-cheddar soup advice, Aaron Judge $5.2M sale ("cash is dead"), LeBron 10/10 pop 7 grail at a
card show, Grant's "I want it all" deal. No reveal stack (talk clips) -> reveal.at = -1. Zoom 1.6 from the top on talk clips (empty table below).
Appends to src/pull.cfg.json. Run from viral-short/: python3 plan_bb4.py"""
import json
Y, GR, RD = '#FFE14D', '#5CFF5C', '#FF4D4D'
TOP = [1.6, 540, 0]
SW = {'shit': 'sh*t', 'roly.': 'Rollie.', 'millie?': 'Millie?', 'millie.': 'Millie.'}
CLIPS = {
 'bbsoup': dict(src='bb4/soup.mp4', zoom=TOP, bannerY=830, capY=1560, music=['funkabn_n', 2.0],
   top=['HIS ADVICE FOR BEING SICK', 'IS INSANE'], hl={'INSANE': '#E3201B'}, tEmoji='1f480',
   scenes=[(12.1, 18.25), (4.8, 12.1), (18.25, 33.4)],
   question='WOULD YOU TRY THE CHEDDAR BATH?', qEmoji='1f9c0', qAt=29.5,
   kw={'panera': Y, 'broccoli': GR, 'cheddar': Y, 'shampoo': RD, 'sick': RD, 'bath': Y, 'goo': GR, 'better': GR},
   emoji=[(1.3, '1f9c0'), (3.5, '1f480'), (14.0, '1f62d')]),
 'bbjudge': dict(src='bb4/judge52.mp4', zoom=TOP, bannerY=830, capY=1560, music=['empire_n', 18.8],
   top=['A CARD JUST SOLD FOR', '$5.2 MILLION'], hl={'$5.2': '#1DB954', 'MILLION': '#1DB954'}, tEmoji='1f92f',
   scenes=[(135.1, 142.45), (11.6, 21.6), (31.3, 34.6), (57.8, 61.0), (129.2, 135.1), (144.7, 156.6)],
   question='CARDS OR STOCKS?', qAt=152.5, qEmoji='1f4c8',
   kw={'$100,000': GR, 'hundred': GR, 'clip.': GR, 'judge': Y, '5.2': GR, 'millie?': GR, 'cash': RD, 'dead.': RD, 'instantly.': Y, 'box.': Y, 'dust.': Y, '100k': GR},
   emoji=[(3.5, '1f4b8'), (12.0, '1f480'), (16.5, '1f4c8')]),
 'bbgrail': dict(src='bb4/cardshow.mp4', zoom=None, bannerY=500, capY=1600, music=['dubist_n', 1.0],
   top=['HE BOUGHT A GRAIL', 'WITHOUT KNOWING IT'], hl={'GRAIL': '#E3201B'}, tEmoji='1f633',
   scenes=[(76.9, 83.35), (53.5, 76.9)],
   question="WHAT'S YOUR GRAIL CARD?", qEmoji='1f914', qAt=76.0,
   kw={'grail': Y, 'lebron': Y, 'rookie': GR, 'seven': RD, "seven's": RD, 'pop': RD, 'nasty': GR, '10s': GR},
   emoji=[(1.0, '1f633'), (12.0, '1f451')]),
 'bbdeal': dict(src='bb4/dance.mp4', zoom=TOP, bannerY=830, capY=1560, music=['montagem_n', 24.0],
   top=['"I WANT IT ALL"', 'GRANT MAKES A DEAL'], hl={'ALL"': '#1DB954', 'DEAL': '#1DB954'}, tEmoji='1f91d',
   scenes=[(49.3, 55.2), (13.1, 23.5), (41.3, 49.3), (55.2, 68.7)],
   question='WOULD YOU TAKE THE DEAL?', qEmoji='1f914', qAt=62.0,
   kw={'$5,500.': GR, '$4,500': GR, 'honors': Y, 'offer': Y, 'all.': RD, '4k.': GR, '5k': GR},
   emoji=[(1.0, '1f4b8'), (11.0, '1f91d')]),
}
cfg = json.load(open('src/pull.cfg.json'))
for cid, c in CLIPS.items():
    W = json.load(open(f"../footage/bb4/{c['src'].split('/')[1].replace('.mp4', '')}.words.json"))
    scenes = []
    for a, b in c['scenes']:
        ws = []
        for w in W:
            s, e, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
            if not (a - 0.05 <= s < b - 0.05): continue
            t = SW.get(t.lower(), t)
            if (t.startswith('-') or (t[:1] in ',.' and t[1:2].isdigit())) and ws: ws[-1]['w'] += t; ws[-1]['e'] = e; continue
            if t == '1010': t = '10/10'
            ws.append({'w': t, 's': s, 'e': e})
        sc = {'a': a, 'b': b, 'blur': False, 'words': ws}
        if c['zoom']: sc['zoom'] = c['zoom']
        scenes.append(sc)
    t = 0.0; q = 0
    for s in scenes:
        if s is not scenes[0] and s['a'] <= c['qAt'] < s['b']: q = round(t + c['qAt'] - s['a'], 2)
        t += s['b'] - s['a']
    cfg[cid] = dict(src=c['src'], srcW=1080, cardY=9999, top=c['top'], hl=c['hl'], tEmoji=c['tEmoji'], qEmoji=c['qEmoji'], bannerY=c['bannerY'], capY=c['capY'],
                    scenes=scenes, reveal=dict(at=-1, name='', card='', price='', cx=540, cy=960), question=c['question'], qAt=q, music=c['music'], kw=c['kw'],
                    emoji=[{'at': x, 'e': e} for x, e in c['emoji']])
    print(cid, round(t, 1), 's | q@', q, '|', ' / '.join(' '.join(w['w'] for w in s['words']) for s in scenes)[:300])
json.dump(cfg, open('src/pull.cfg.json', 'w'), indent=1)

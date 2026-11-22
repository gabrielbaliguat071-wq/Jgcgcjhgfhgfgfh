"""Backyard Breaks x3 normal card-pull edits (Nov 19, no narration): Josh Allen NFL shield 1/1 (sheet: Allen shield into Purdy
shield; only Allen is visibly confirmed in this clip, so only Allen is named), Michael Jordan 1986 Fleer rookie, Tom Brady Black
Diamond 1/1. Values from the sheet. Template src/Pull.tsx, cfg src/pull.cfg.json. Run from viral-short/: python3 plan_bb3.py"""
import json
Y, GR, RD = '#FFE14D', '#5CFF5C', '#FF4D4D'
FIX = {'pills': 'Bills', 'foyle.': 'foil.', 'derek': 'Derrick', 'shit,': 'sh*t,', '101.': '1/1.', '101': '1/1', 'home': 'Tom', 'the': 'the'}
CLIPS = {
 'bbshield': dict(src='bb3/shields.mp4', srcW=1080, cardY=640, music=['phonk_n', 22.4],
   top=['SAM PAID FOR', 'HIS WEDDING'], tEmoji='1f48d', hl={'WEDDING': '#E3201B'},
   scenes=[(31.8, 36.25, True), (0.0, 5.85, False), (8.0, 10.1, False), (13.0, 18.6, False), (25.7, 31.75, False)],
   reveal=dict(at=13.45, name='JOSH ALLEN', card='NFL SHIELD 1/1', price='$5K–$12K+', cx=420, cy=1100),
   question='KEEP IT OR PAY FOR THE WEDDING?', qEmoji='1f48d', qAt=29.6,
   kw={'wedding': RD, 'massive': GR, 'sam': Y, 'sam?': Y, 'chick-fil-a': RD, 'bills': Y, 'derrick': Y, 'henry': Y, 'buddy': RD},
   emoji=[(1.0, '1f48d'), (3.3, '1f633'), (5.2, '1f357')]),   # (timeline s, emoji)
 'bbjordan': dict(src='bb3/jordan.mp4', srcW=1080, cardY=600, music=['empire_n', 18.8],
   top=['1986 FLEER PACK…', 'WHO IS IN IT?'], tEmoji='1f440', hl={'1986': '#E3201B'},
   scenes=[(57.0, 61.5, True), (13.9, 18.9, False), (37.45, 39.05, False), (46.12, 48.3, False), (52.0, 55.95, False), (55.95, 64.5, False), (65.5, 67.75, False)],
   reveal=dict(at=56.5, name='MICHAEL JORDAN', card='1986 FLEER ROOKIE', price='$3K–$5K', cx=600, cy=950, ty=1560),
   question='WOULD YOU GRADE IT?', qEmoji='1f914', qAt=65.9,
   kw={'sweating': RD, 'lifetime': Y, 'goat': GR, 'mjs': Y, 'uh-oh': RD, 'saw': Y, 'move': RD, 'kellogg': Y, 'clark': Y},
   emoji=[(5.5, '1f630'), (10.0, '1f410'), (12.4, '1f440')]),
 'bbbrady': dict(src='bb3/brady.mp4', srcW=720, cardY=520, music=['dubist_n', 1.0],
   top=['PICK 3, CHOOSE 1…', 'HE PICKED THIS'], tEmoji='1f633', hl={'THIS': '#E3201B'},
   scenes=[(32.6, 36.4, True), (8.5, 11.2, False), (13.4, 15.8, False), (16.6, 24.0, False), (41.7, 46.7, False), (55.3, 59.3, False)],
   reveal=dict(at=17.9, name='TOM BRADY', card='BLACK DIAMOND 1/1', price='$8,000+', cx=450, cy=1000),
   question='KEEP IT OR SELL IT?', qEmoji='1f48e', qAt=57.9,
   kw={'black': Y, 'diamond': Y, 'diamond?': Y, '1/1': RD, 'sick': GR, 'brady': Y, 'tom': Y, 'hit': GR},
   emoji=[(4.4, '1f48e'), (21.5, '1f525'), (23.8, '1f633')]),
}
cfg = {}
for cid, c in CLIPS.items():
    W = json.load(open(f"../footage/bb3/{c['src'].split('/')[1].replace('.mp4', '')}.words.json"))
    scenes = []
    for a, b, blur in c['scenes']:
        ws = []
        for w in W:
            s, e, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
            if not (a - 0.05 <= s < b - 0.05): continue
            t = FIX.get(t.lower(), t)
            if t.startswith('-') and ws: ws[-1]['w'] += t; ws[-1]['e'] = e; continue
            ws.append({'w': t, 's': s, 'e': e})
        scenes.append({'a': a, 'b': b, 'blur': blur, 'words': ws})
    for i, w in enumerate(scenes[0]['words'] if False else []): pass
    cfg[cid] = dict(tEmoji=c['tEmoji'], qEmoji=c['qEmoji'], src=c['src'], srcW=c['srcW'], cardY=c['cardY'], top=c['top'], hl=c['hl'], scenes=scenes, reveal=c['reveal'], question=c['question'],
                    qAt=0, music=c['music'], kw=c['kw'], emoji=[{'at': t, 'e': e} for t, e in c['emoji']])
    # qAt: timeline seconds of source time c['qAt']
    t = 0.0
    for s in scenes:
        if s is not scenes[0] and s['a'] <= c['qAt'] < s['b']: cfg[cid]['qAt'] = round(t + c['qAt'] - s['a'], 2)
        t += s['b'] - s['a']
    print(cid, round(t, 1), 's | q@', cfg[cid]['qAt'], '|', ' / '.join(' '.join(w['w'] for w in s['words']) for s in scenes))
json.dump(cfg, open('src/pull.cfg.json', 'w'), indent=1)

"""Kai Cenat GTA 6 marathon x4 (2026-11-21). Twitch clips from Nov 18+ (footage/kai/<id>.mp4, words <id>.words.json). Kai's own reactions only.
Facecam top-left (x 20-400, y 430-660), gameplay centre (avoid chat top-right). Swears starred. Run from viral-short/: python3 plan_kai.py"""
import json
CAM = {'x': 30, 'y': 437, 'w': 360, 'h': 208}
CAM_HI = {'x': 12, 'y': 357, 'w': 370, 'h': 208}   # kfirst / kbaby: facecam sits higher
GAME = {'x': 420, 'y': 40, 'w': 1300, 'h': 1000}
FIX = {'fucking': 'f***ing', 'fucking,': 'f***ing,', 'effort!': 'ever!'}
DROP = {('3671060798', 21.8), ('3671060798', 22.2), ('3671060798', 22.3), ('1340057959', 28.1), ('1340057959', 28.6)}
CLIPS = {
 'kfirst': dict(id='774011141', title=['Kai Cenat opening', 'GTA 6 for the FIRST time'], te='1f631', hook=['Kai Cenat opens', 'GTA 6 for the FIRST time'],
   scenes=[('hook', 16.4, 22.3), ('c1', 0.0, 9.6), ('c2', 22.3, 25.2)], hi={'god', 'monitor', 'best', 'shot'}, music=['phonk_n', 22.4]),
 'kbaby': dict(id='3671060798', title=['Kai Cenat found the', 'first BABY in GTA 6'], te='1f62d', hook=['Kai Cenat found the', 'first BABY in GTA 6'],
   scenes=[('hook', 21.7, 28.3), ('c1', 0.6, 19.9), ('c2', 34.2, 37.3)], hi={'baby', 'gta!', 'first', 'god,', 'gta?', 'coffee'}, music=['funkabn_n', 2.0]),
 'khands': dict(id='1340057959', title=['Kai Cenat noticed THIS', 'detail in GTA 6'], te='1f92f', hook=['Kai Cenat noticed', 'THIS in GTA 6'],
   scenes=[('hook', 19.8, 30.0), ('c1', 3.0, 19.8)], hi={'hand.', 'hands', 'wow.'}, music=['investigations_n', 20.0]),
 'kcalm': dict(id='3907402066', title=['Kai Cenat trying to', 'calm her down in GTA 6'], te='1f602', hook=['Kai Cenat trying to', 'calm her down'],
   scenes=[('hook', 0.3, 13.3)], hi={'listen,', 'listen.', 'calm', 'down.', 'okay?'}, music=['montagem_n', 24.0]),
'kbigfoot': dict(id='2131405255', title=[], te='1f440', hook=['Kai Cenat found', 'BIGFOOT in GTA 6'],
   scenes=[('hook', 17.9, 22.7), ('c1', 1.8, 17.9)], hi={'found', 'him.', 'god!', 'catch'}, music=['investigations_n', 20.0]),
}
cfg = {}
for cid, c in CLIPS.items():
    W = json.load(open(f"../footage/kai/{c['id']}.words.json")); scenes = []
    for sid, a, b in c['scenes']:
        n = round((b - a) * 30); words = []
        for w in W:
            ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
            if not (a - 0.05 <= ws < b - 0.05): continue
            if any(c['id'] == i and abs(ws - x) < 0.06 for i, x in DROP): continue
            t = FIX.get(t.lower(), t)
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t, 'startFrame': f0, 'endFrame': f1, 'hi': t.lower() in c['hi']})
        scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'words': words})
    cfg[cid] = dict(src=f"kai/{c['id']}.mp4", hook=c['hook'], title=c['title'], titleEmoji=c['te'], cam=CAM_HI if c['id'] in ('774011141', '3671060798') else CAM, game=GAME, music=c['music'], scenes=scenes)
    print(cid, round(sum(s['durationInFrames'] for s in scenes) / 30, 1), 's |', ' / '.join(' '.join(w['word'] for w in s['words']) for s in scenes))
json.dump(cfg, open('src/kai.cfg.json', 'w'), indent=1)

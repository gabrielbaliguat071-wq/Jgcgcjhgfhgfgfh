"""Metaphor word-by-word edits (style of the user's reference TikTok: one spaced-out word at a time, centre screen, synced to the line,
white flash before the finale). Words come from the trailers' own audio (faster-whisper word times) mapped onto the base cut.
Run from viral-short/: python3 plan_mrf.py"""
import json
from build_mrf import SEGS
FIX = {'hearts': 'heart', 'nought': 'nought'}
EDITS = {
 'wh': dict(top=["HEISMAY'S LINE", 'THAT HITS DIFFERENT'], end='METAPHOR: REFANTAZIO'),
 'wl': dict(top=["LOUIS'S MOST", 'VILLAIN LINES'], end='METAPHOR: REFANTAZIO'),
 'wa': dict(top=['METAPHOR: REFANTAZIO', 'QUOTES THAT HIT DIFFERENT'], end='METAPHOR: REFANTAZIO'),
}
cfg = {}
for eid, e in EDITS.items():
    t = 0; words = []; cuts = []
    for seg in SEGS[eid]:
        f, a, b = seg[:3]
        if t: cuts.append(round(t, 3))
        for w in json.load(open(f'../footage/metaphor/{f}.words.json')):
            ws, we = w['startMs'] / 1000, w['endMs'] / 1000
            if a - 0.05 <= ws < b - 0.05:
                txt = FIX.get(w['text'].lower().strip('.,!?'), None)
                big = w['text'].rstrip('"”')[-1:] in '.!?'
                txt = (txt or w['text']).upper().strip('.,!?"“”')
                words.append({'w': txt, 's': round(t + max(0, ws - a), 3), 'e': round(t + min(b - a, we - a) + 0.25, 3), 'big': big})
        t += b - a
    for i in range(len(words) - 1): words[i]['e'] = min(words[i]['e'], words[i + 1]['s'])
    cfg[eid] = dict(base=f'mrf/{eid}.mp4', dur=round(t, 3), cuts=cuts, flash=cuts[-1], top=e['top'], end=e['end'], words=words)
    print(eid, round(t, 2), 's |', ' '.join(w['w'] for w in words))
json.dump(cfg, open('src/mrw.cfg.json', 'w'), indent=1)

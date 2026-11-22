"""Find voice lines cut mid-sentence at segment edges (user: never cut them before they finish talking)."""
import json
from build_mrf import SEGS
from build_amv import AMV
W = {n: json.load(open(f'../footage/metaphor/{n}.words.json')) for n in ['heismay', 'hero30', 'pro', 'louis']}
def check(eid, f, a, b):
    ws = W[f]; bad = []
    ins = [w for w in ws if a - 0.02 <= w['startMs'] / 1000 < b]
    before = [w for w in ws if w['startMs'] / 1000 < a - 0.02]
    if before and before[-1]['text'][-1:] not in '.!?' and a - before[-1]['endMs'] / 1000 < 1.0: bad.append(f'starts mid-sentence after "{before[-1]["text"]}"')
    if ins and ins[-1]['endMs'] / 1000 > b + 0.02: bad.append(f'cuts word "{ins[-1]["text"]}" (ends {ins[-1]["endMs"]/1000:.2f} > {b})')
    if ins and ins[-1]['text'][-1:] not in '.!?': 
        nxt = [w for w in ws if w['startMs'] / 1000 >= b]
        if nxt and nxt[0]['startMs'] / 1000 - b < 1.0: bad.append(f'sentence continues after "{ins[-1]["text"]}" -> "{nxt[0]["text"]}"')
    if bad: print(f'{eid}: {f} {a}-{b}: ' + '; '.join(bad))
for eid in ['hm', 'hv', 'fan', 'wh', 'wl', 'wa']:
    for s in SEGS[eid]: check(eid, s[0], s[1], s[2])
for eid, c in AMV.items(): check('amv_' + eid, *c['audio'])

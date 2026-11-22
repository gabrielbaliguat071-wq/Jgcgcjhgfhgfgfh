"""ClipFarm x Higgsfield clips 10-12 (2026-11-19, for The Founder Files): brief ideas "My mom worked three jobs" (50:23),
"One person spent $30,000 on AI in a week" (34:15, keep that it did not fully work), "Google and OpenAI will kill the $20 AI plans"
(19:31, open with the threat). Excerpts footage/higgs/tx6/<src>.mp4 (G67, 1080p30): hmom = 3000 s, h30k = 2040 s, hplans = 1160 s.
Whole sentences only; pauses/repeats cut (brief allows). Crops are picked automatically from the shot map (A = Alex close-up,
H = Harry close-up, W = wide -> zoom on whoever speaks). Unclear model name in h30k ("Astra"?) is left out instead of captioned wrong."""
import json, shutil, os
AC, HC = (925, 1.15, 510), (930, 1.15, 510)
AW, HW = (290, 1.45, 470), (1440, 1.45, 470)
SHOTS = {  # excerpt seconds -> shot type
 'hmom': [(0, 'A'), (12.6, 'W'), (18.27, 'H'), (24.37, 'A'), (44.87, 'W'), (59.97, 'A'), (76.87, 'H'), (80.7, 'W'), (89.3, 'H')],
 'h30k': [(0, 'A'), (0.97, 'H'), (3.47, 'W'), (7.33, 'A'), (19.97, 'W'), (29.97, 'A'), (46.47, 'H'), (48.47, 'A'), (52.03, 'H'), (53.97, 'W'), (58.87, 'A')],
 'hplans': [(0, 'A'), (9.03, 'W'), (23.03, 'H'), (25.03, 'A'), (41.53, 'H'), (52.53, 'A'), (61.03, 'H')],
}
def crops(src, a, b, who):
    def crop(k): return {'A': AC, 'H': HC}.get(k) or (AW if who == 'A' else HW)
    cur = [k for t, k in SHOTS[src] if t <= a][-1]
    out = [(a, crop(cur))] + [(t, crop(k)) for t, k in SHOTS[src] if a < t < b - 0.1]
    return out
CLIPS = {
 'mom': dict(src='hmom', who={'c1': 'H', 'c1b': 'H'},
   fix={(41.69, 'going'): '', (42.11, 'tall'): '', (44.11, 'minor'): 'a minor,', (62.61, '20'): '2021,', (63.01, 'first'): '', (69.41, 'ability'): 'access',
        (25.00, 'is'): '', (25.24, 'goals'): 'goes', (24.72, 'this'): 'This', (26.88, 'my'): '', (87.63, 'it'): 'I', (23.98, 'look'): 'Look,'},
   hi={'seven', '12', 'mother', 'three', 'jobs', 'father', 'minor,', 'dedicated', 'sacrifice', 'parkinson\'s', 'disease', '2021,', 'birthdays', 'weddings', 'son', 'regret'},
   plan=[('hk1', 27.30, 27.95), ('hook', 30.45, 38.80), ('c1', 17.55, 17.95), ('c1b', 18.95, 23.90), ('c2', 23.90, 26.80),
         ('c3', 38.85, 46.65), ('c4', 54.50, 59.60), ('c5', 61.95, 72.80), ('c6', 86.15, 88.95)],
   hook=['His mom worked 3 jobs.', 'His dad gave up everything.'], music=['einaudi_n', 30.0],
   cards=[('hook', 'three', 70, '3 JOBS', 'his mom, from when he was 7 to 12')]),
 '30k': dict(src='h30k', who={'c1': 'H', 'c4': 'H'},
   fix={(13.42, 'wipe'): 'vibe', (70.20, 'band,'): 'spend,', (52.32, '30'): '30,000', (52.54, ',000'): '', (56.20, '10'): '10,000', (56.52, ',000'): '',
        (21.72, '30k'): '$30K', (74.60, '30k.'): '$30K.'},
   hi={'$30k', '$30k.', 'week', 'week.', 'vibe', 'coding.', 'myself.', 'five', 'nights', 'learned', 'production', '30,000', '10,000', 'stubborn,', 'relentless', 'control'},
   plan=[('hook', 19.15, 23.70), ('c1', 1.25, 2.65), ('c1b', 8.50, 13.75), ('c2', 27.80, 32.10), ('c2b', 38.75, 40.45), ('c2c', 41.80, 44.55),
         ('c3', 46.75, 57.35), ('c4', 59.70, 61.55), ('c4b', 64.85, 75.00)],
   hook=['One employee spent', '$30K on AI in ONE week'], music=['interstellar_n', 40.0],
   cards=[('hook', '$30k', 70, '$30,000', 'on AI models in one week'), ('c3', '10,000', 60, '$10,000+', 'a week for many people')]),
 'plans': dict(src='hplans', who={'c3': 'H'},
   fix={(27.36, 'openei'): 'OpenAI,', (36.58, 'prosumerary'): 'prosumer', (29.86, 'much.'): 'much.', (30.00, 'much.'): '', (36.30, 'their'): 'the', (61.56, "that's"): 'that'},
   hi={'google', 'openai,', 'demolish', '$20', 'subscriptions.', 'never', 'win', 'contrarian', 'bet,', 'ads', 'horizontal', 'month.', 'subscription'},
   plan=[('hook', 31.15, 41.80), ('c1', 11.95, 22.75), ('c2', 23.70, 29.95), ('c3', 41.85, 55.50), ('c4', 56.75, 61.95)],
   hook=['Google & OpenAI will kill', 'every $20/month AI app'], music=['investigations_n', 20.0],
   cards=[('hook', '$20', 70, '$20 / month', 'the plans he says will get demolished')]),
}
cfg = json.load(open('src/higgs.cfg.json'))
for cid, c in CLIPS.items():
    if not os.path.exists(f"public/{c['src']}.mp4"): shutil.copy(f"../footage/higgs/tx6/{c['src']}.mp4", f"public/{c['src']}.mp4")
    W = json.load(open(f"../footage/higgs/tx6/{c['src']}.words.json")); scenes = []
    for sid, a, b in c['plan']:
        n = round((b - a) * 30); words = []
        for w in W:
            ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
            if not (a - 0.05 <= ws < b - 0.05): continue
            hit = [v for (ft, fw), v in c['fix'].items() if abs(ft - ws) < 0.03 and fw == t.lower()]
            t2 = hit[0] if hit else t
            if not t2: continue
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t2, 'startFrame': f0, 'endFrame': f1, 'hi': t2.lower().strip('.,?') in {h.strip('.,?') for h in c['hi']}})
        for i in range(len(words) - 1, 0, -1):
            if words[i]['word'].startswith('-'): words[i - 1]['word'] += words[i]['word']; words.pop(i)
        cr = crops(c['src'], a, b, c['who'].get(sid, 'A'))
        scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'crops': [[round((t - a) * 30), x, z, y] for t, (x, z, y) in cr], 'words': words})
    def at(sid, word):
        s = next(x for x in scenes if x['id'] == sid)
        return [sid, [w for w in s['words'] if w['word'].lower().startswith(word.lower())][0]['startFrame']]
    cfg[cid] = dict(src=c['src'] + '.mp4', wm='higgsfield_wm.png', hook=c['hook'], hookFrames=100, music=c['music'], musicVol=0.07, scenes=scenes,
                    cards=[dict(at=at(s, w), dur=d, big=b, small=sm) for s, w, d, b, sm in c['cards']])
    print(f'== {cid}', round(sum(s['durationInFrames'] for s in scenes) / 30, 2), 's')
    for s in scenes: print('  ', s['id'], '|', ' '.join(w['word'] for w in s['words']))
json.dump(cfg, open('src/higgs.cfg.json', 'w'), indent=1)

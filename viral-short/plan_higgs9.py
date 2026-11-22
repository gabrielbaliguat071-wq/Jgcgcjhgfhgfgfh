"""ClipFarm x Higgsfield clips 15-20 (2026-11-20): brief ideas not yet clipped — "90 minutes of film took 100+ hours of AI footage" (23:55),
"Our film prompts are 3,000 words long" (27:25), "The faster we ship, the harder AI support gets" (37:35), "Our team moved from Claude to Codex"
(38:14, true when filmed), "Europe can compete in every part of AI" (52:57), "Yuri Milner saw the media shift early" (45:23).
Excerpts footage/higgs/tx8/<src>.mp4. Whole sentences only, his meaning kept. Run from viral-short/: python3 plan_higgs9.py"""
import json, shutil, os
A, H = (880, 1.15, 510), (930, 1.15, 510)
AW, HW = (290, 1.45, 470), (1440, 1.45, 470)
SHOTS = {  # excerpt s -> crop (W shots resolved by speaker)
 'hfilm': [(0, 'W'), (1.53, (800, 1.15, 510)), (24.53, 'W'), (37.03, H), (43.03, A), (44.37, H), (58.47, 'W')],
 'hprompt': [(0, 'W'), (10.83, A), (30.27, 'W'), (41.77, A), (59.27, H), (66.1, A)],
 'hsupport': [(0, H), (2.83, 'W'), (10.47, A), (32.47, H), (39.97, A), (49.83, H)],
 'hcodex': [(0, A), (9.83, H), (17.47, A), (32.47, 'W'), (40.97, A), (55.97, H)],
 'heurope': [(0, H), (2.47, 'W'), (7.97, H), (11.6, A), (31.37, H), (32.87, A), (52.37, 'W'), (65.5, A)],
 'hyuri': [(0, H), (10.3, A), (13.47, H), (16.47, 'W'), (25.27, A), (39.97, 'W'), (50.97, A)],
}
def crops(src, a, b, who):
    def c(k): return (AW if who == 'A' else HW) if k == 'W' else k
    cur = [k for t, k in SHOTS[src] if t <= a][-1]
    return [(a, c(cur))] + [(t, c(k)) for t, k in SHOTS[src] if a < t < b - 0.1]
CLIPS = {
 'film': dict(src='hfilm', who={}, fix={'-generated': '-generated'},
   hi={'90', 'minutes', 'tv', '100', 'hours', 'ai-generated', 'movie,', 'open-sourced', 'creative', 'decisioning,', 'revenue.', 'important.'},
   plan=[('hook', 15.75, 25.4), ('c1', 1.95, 13.4), ('c2', 25.7, 36.9)],
   hook=['90 min of AI film took', '100+ HOURS of AI footage'], music=['interstellar_n', 40.0],
   cards=[('hook', '100', 70, '100+ hours', 'of AI footage for a 90-minute film')]),
 'prompt': dict(src='hprompt', who={}, fix={},
   hi={'3,000', 'words.', 'impossible', 'text.', 'benchmarks', 'prompts,', '10', 'image', 'references', 'complex.', 'represent'},
   plan=[('hook', 10.75, 17.85), ('c1', 2.55, 10.4), ('c2', 27.35, 40.95), ('c3', 53.0, 59.2)],
   hook=['Their AI film prompts are', '3,000 WORDS long'], music=['investigations_n', 20.0],
   cards=[('hook', '3,000', 70, '3,000+ words', 'average prompt length')]),
 'support': dict(src='hsupport', who={'c2': 'H'}, fix={'nick': 'Nik'},
   hi={'context', 'rules', 'twice', 'week,', 'difficult.', 'every', 'week.', 'agents', 'velocity,', 'harder', 'playbooks,', 'smart'},
   plan=[('hook', 40.05, 49.4), ('c1', 10.55, 32.3), ('c2', 32.65, 39.3)],
   hook=['Why AI support gets HARDER', 'the faster you ship'], music=['chess_n', 40.0], cards=[]),
 'codex': dict(src='hcodex', who={'c1': 'H'}, fix={'cursor?': 'Cursor?', 'codex?': 'Codex?', 'call': 'Claude', 'code?': 'Code?'},
   hi={'claude', 'claude,', 'codex', 'mid-june.', 'coders', 'cyclical.', 'creative', 'everyone', '10x'},
   plan=[('hook', 34.15, 44.6), ('c1', 9.75, 17.0), ('c2', 17.45, 25.3), ('c3', 45.65, 57.1)],
   hook=['His whole team switched', 'from Claude to Codex'], music=['blue_n', 21.5], cards=[]),
 'europe': dict(src='heurope', who={}, fix={'neocloughs': 'neoclouds', 'iran,': 'IREN,', 'iran': 'IREN', 'nubius': 'Nebius', 'scale': 'Nscale',
     'ligora,': 'Legora,', '11': 'ElevenLabs,', 'labs,': '', 'lovable,': 'Lovable,', 'asml,': 'ASML,', 'n': 'Nscale,', '-scale,': '', 'story,': 'story,'},
   hi={'europe', 'competitive.', 'asml,', 'thrives', 'uk.', 'netherlands.', 'australia', 'matter.', 'mercor', 'harvey,', 'happen.'},
   plan=[('hook', 73.05, 81.2), ('c1', 11.45, 16.4), ('c2', 23.65, 39.9), ('c3', 40.65, 54.1)],
   hook=["Without this European company", "AI wouldn't happen"], music=['empire_n', 18.8],
   cards=[('hook', 'asml', 70, 'ASML', 'the Dutch chip-machine maker')]),
 'yuri': dict(src='hyuri', who={'c1': 'H'}, fix={},
   hi={'yuri', 'milner', 'trends.', 'content', 'transformation', 'surprised', 'short-form', 'dramas.', 'asia', 'west.', 'ai', 'ads.'},
   plan=[('hook', 33.45, 39.95), ('c1', 6.95, 12.5), ('c2', 13.55, 24.4), ('c3', 39.95, 48.0)],
   hook=['What Yuri Milner saw', 'before everyone else'], music=['einaudi_n', 160.0], cards=[]),
}
cfg = json.load(open('src/higgs.cfg.json'))
for cid, c in CLIPS.items():
    if not os.path.exists(f"public/{c['src']}.mp4"): shutil.copy(f"../footage/higgs/tx8/{c['src']}.mp4", f"public/{c['src']}.mp4")
    W = json.load(open(f"../footage/higgs/tx8/{c['src']}.words.json")); scenes = []
    for sid, a, b in c['plan']:
        n = round((b - a) * 30); words = []
        for w in W:
            ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
            if not (a - 0.05 <= ws < b - 0.05): continue
            t2 = c['fix'].get(t.lower(), t)
            if not t2: continue
            if words and (t2.startswith('-') or (t2[:1] == ',' and t2[1:2].isdigit())): words[-1]['word'] += t2; words[-1]['hi'] = words[-1]['word'].lower().strip('.,?') in {h.strip('.,?') for h in c['hi']}; continue
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t2, 'startFrame': f0, 'endFrame': f1, 'hi': t2.lower().strip('.,?') in {h.strip('.,?') for h in c['hi']}})
        cr = crops(c['src'], a, b, c['who'].get(sid, 'A'))
        scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'crops': [[round((t - a) * 30), x, z, y] for t, (x, z, y) in cr], 'words': words})
    def at(sid, word):
        s = next(x for x in scenes if x['id'] == sid)
        return [sid, [w for w in s['words'] if w['word'].lower().startswith(word.lower())][0]['startFrame']]
    cfg[cid] = dict(src=c['src'] + '.mp4', wm='higgsfield_wm.png', hook=c['hook'], hookFrames=100, music=c['music'], musicVol=0.07, scenes=scenes,
                    cards=[dict(at=at(s, w), dur=d, big=b, small=sm) for s, w, d, b, sm in c['cards']])
    print(f'== {cid}', round(sum(s['durationInFrames'] for s in scenes) / 30, 1), 's')
    for s in scenes: print('  ', s['id'], '|', ' '.join(w['word'] for w in s['words']))
json.dump(cfg, open('src/higgs.cfg.json', 'w'), indent=1)

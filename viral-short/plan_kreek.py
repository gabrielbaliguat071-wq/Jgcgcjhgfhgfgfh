"""ClipLaunch x KreekCraft GTA 6 batch 1 (2026-11-19). Twitch clips from his GTA 6 Day 1 stream (twitch.tv/kreekcraft/clips).
Hook = the reaction first, then the moment in order (no reordered words, real reactions only)."""
import json
CLIPS = {
 'croc': dict(hook=['If a crocodile gets him…', 'chat gets a free GTA 6'], plan=[('hook', 18.3, 22.0), ('s1', 3.2, 26.4)],
   hi={'crocodile,', 'crocodile.', 'eaten', 'kidding', 'giveaway', 'game.', 'extra', 'copy', 'no'}),
 'shark': dict(hook=['He went looking', 'for a SHARK'], plan=[('hook', 9.7, 13.2), ('s1', 2.8, 14.2)],
   hi={'shark?', 'got', 'them.'}),
 'banned': dict(hook=['GTA 6 nightclub', 'almost got him BANNED'], plan=[('hook', 13.2, 16.3), ('s1', 0.0, 3.0), ('s2', 11.1, 24.5)],
   hi={'banned.', 'cooked.', 'nice', 'knowing', 'idea.', 'subscribe'}),
 'milk': dict(hook=['GTA 6 has the', 'MILK update'], plan=[('hook', 16.8, 20.0), ('s1', 7.4, 26.0)],
   hi={'milk.', 'milk,', 'milk', 'weird.', 'shirts.', 'three', 'baby.'}),
 'cooked': dict(hook=['His wife saw THAT clip…'], plan=[('hook', 49.4, 53.3), ('s1', 18.8, 29.0), ('s2', 34.2, 40.0), ('s3', 42.8, 54.4)],
   hi={'ai', 'a.i.', 'me.', 'talk', 'wife', 'girlfriend', 'what?', 'shoe', 'store'}),
 'door': dict(hook=['GTA 6 enemy AI', 'is something else'], plan=[('hook', 4.4, 6.4), ('s1', 0.0, 18.5)],
   hi={'stuck', 'door.', 'him.'}),
}
cfg = json.load(open('src/kreek.cfg.json'))
for cid, c in CLIPS.items():
    W = json.load(open(f'../footage/kreek/clips/tx/{cid}.words.json')); scenes = []
    for sid, a, b in c['plan']:
        n = round((b - a) * 30); words = []
        for w in W:
            ws, we, t = w['startMs'] / 1000, w['endMs'] / 1000, w['text']
            if not (a - 0.05 <= ws < b - 0.05): continue
            f0 = max(0, round((ws - a) * 30)); f1 = min(n, max(f0 + 4, round((we - a) * 30) + 3))
            words.append({'word': t, 'startFrame': f0, 'endFrame': f1, 'hi': t.lower() in c['hi']})
        for i in range(len(words) - 1, 0, -1):
            if words[i]['word'] in ('I', '.I.') and words[i - 1]['word'] in ('a', 'A') and words[i]['startFrame'] - words[i - 1]['startFrame'] < 6: words[i - 1]['word'] = 'AI'; words.pop(i); continue
            if words[i]['word'].startswith("'"): words[i - 1]['word'] += words[i]['word']; words.pop(i)
        scenes.append({'id': sid, 'videoStartSec': a, 'durationInFrames': n, 'words': words})
    cfg[cid] = dict(src=f'kr_{cid}.mp4', hook=c['hook'], scenes=scenes)
    print('==', cid, round(sum(s['durationInFrames'] for s in scenes) / 30, 1), 's |', ' / '.join(' '.join(w['word'] for w in s['words']) for s in scenes))
json.dump(cfg, open('src/kreek.cfg.json', 'w'), indent=1)

"""Dr. Guillaume Dulude psychology clips (2026-11-23) from his TikTok lessons (Drive folder quota-blocked, YouTube bot-blocked).
Professional: no memes/SFX, his voice + soft music, clean subtitles over a blurred band (his old burned subs), short true top text.
Only Guillaume on screen (other creators' intro clips cut). Usage: python3 build_gd.py <id>"""
import json, subprocess, os, sys
G = 'eq=contrast=1.04:saturation=1.06,unsharp=5:5:0.9:3:3:0.4'
C = {
 'fear': dict(segs=[(0.0, 39.2)], band=(860, 1080), wordsY=905, topY=1440, top=[(0, 99, ['How to stop fear', 'from controlling your life'])],
   hl={'control', 'expose', 'low', 'anxiety', 'rewire', 'stronger', 'drops', 'judged'}),
 'lying': dict(segs=[(34.3, 37.7), (22.2, 60.9)], band=(1450, 1610), wordsY=1470, topY=1690,
   top=[(0, 99, ['When words and body language', "don't match"])], hl={'lying', 'wrong', 'conflict', 'anxiety', 'conscious', 'trust', 'stories', 'fit'}),
 'silence': dict(segs=[(58.7, 61.4), (14.3, 45.7), (48.0, 75.5)], band=(1450, 1610), wordsY=1470, topY=1690,
   top=[(0, 99, ['Why silence makes', 'conversations work'])], hl={'silence', 'powerful', 'scared', 'anxiety', 'attention', 'milliseconds', 'manipulation', 'important'}),
}
eid = sys.argv[1]; c = C[eid]; SRC = f'../footage/gd/{eid}.mp4'; W = json.load(open(f'../footage/gd/{eid}.words.json'))
y0, y1 = c['band']; d = f'/tmp/claude-0/gd_{eid}'; os.makedirs(d, exist_ok=True); parts = []; spans = []; t = 0; cuts = []
for i, (a, b) in enumerate(c['segs']):
    out = f'{d}/s{i}.mp4'
    vf = (f'[0:v]scale=1080:1920:flags=lanczos,split[m][n];[n]crop=1080:{y1-y0}:0:{y0},boxblur=30:3,eq=brightness=-0.06[bl];[m][bl]overlay=0:{y0},{G},fps=30[v]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-to', str(b), '-i', SRC, '-filter_complex', vf + ';[0:a]anull[au]', '-map', '[v]', '-map', '[au]',
                    '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', out], check=True)
    parts.append(out); spans.append((t, a, b)); t += b - a; cuts.append(round(t, 3))
open(f'{d}/l.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{d}/l.txt', '-c', 'copy', f'public/ylm/gd{eid}.mp4'], check=True)
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'public/ylm/gd{eid}.mp4']))
words = []
for o, a, b in spans:
    m = [dict(w) for w in W if a - 0.05 <= w['startMs'] / 1000 < b - 0.1]
    cur = []
    for j, w in enumerate(m):
        cur.append(w)
        if w['text'][-1:] in ',.?!' or len(cur) == 3 or j == len(m) - 1:
            txt = ' '.join(x['text'] for x in cur).rstrip(',.')
            hl = any(x['text'].lower().strip(',.?!') in c['hl'] for x in cur)
            words.append(dict(w=txt, s=round(o + cur[0]['startMs'] / 1000 - a, 3), hl=hl) | ({} if j < len(m) - 1 else dict(e=round(o + b - a, 3))))
            cur = []
assert all(words[i]['s'] <= words[i + 1]['s'] for i in range(len(words) - 1))
texts = [{'from': fr, 'to': to, 'lines': ln, 'y': c['topY'], 'size': 54, 'box': True, 'rot': 0} for fr, to, ln in c['top']]
cfg = dict(base=f'ylm/gd{eid}.mp4', dur=round(dur, 3), baseVol=1, music=['einaudi_n', 0, 0.045], punch=False, whooshVol=0, cuts=cuts[:-1], wordsY=c['wordsY'], wordSize=66,
           freezes=[], texts=texts, words=words, sfx=[])
allc = json.load(open('src/ylm.cfg.json')); allc[f'gd{eid}'] = cfg; json.dump(allc, open('src/ylm.cfg.json', 'w'), indent=1)
print(eid, 'dur', round(dur, 2), 'cuts', cuts, '|', ' | '.join(w['w'] for w in words[:10]))

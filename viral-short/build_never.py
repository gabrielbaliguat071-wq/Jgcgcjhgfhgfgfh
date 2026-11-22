"""Backyard Breaks 'cards I will never profit on' (Grant) re-edit -> public/ylm/bbnever.mp4 + ylm.cfg.json entry 'bbnever'.
Source: their TikTok 7561161222456954142 (closest available match to YT short dNJZz88Y_Dk). Crops off their burned captions (y>0.73)."""
import json, subprocess, os
SRC = '../footage/bbhouse/never.mp4'; W = json.load(open('../footage/bbhouse/never.words.json'))
G = 'eq=contrast=1.08:saturation=1.15,unsharp=5:5:0.7'
CROP = 'crop=788:1400:146:0,scale=1080:1920:flags=lanczos'
# (a, b, freeze_after, cover_title)
SEGS = [(60.20, 63.80, 0.6, 0), (0.00, 2.45, 0, 1), (8.08, 21.30, 0, 0), (29.30, 39.55, 0, 0), (46.70, 53.40, 0, 0), (54.38, 63.85, 0, 0), (74.10, 81.15, 1.0, 0)]
os.makedirs('/tmp/claude-0/bbn', exist_ok=True); parts = []; t = 0; cuts = []; spans = []
for i, (a, b, fz, cov) in enumerate(SEGS):
    box = 'drawbox=x=0:y=440:w=1080:h=160:color=white:t=fill,' if cov else ''
    out = f'/tmp/claude-0/bbn/s{i}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-to', str(b), '-i', SRC, '-filter_complex',
        f'[0:v]{box}{CROP},{G},fps=30,tpad=stop_mode=clone:stop_duration={fz}[v];[0:a]apad=pad_dur={fz}[au]', '-map', '[v]', '-map', '[au]',
        '-t', str(b - a + fz), '-c:v', 'libx264', '-crf', '18', '-preset', 'fast', '-c:a', 'aac', '-ar', '48000', out], check=True)
    parts.append(out); spans.append((t, a, b)); t += b - a + fz; cuts.append(round(t, 3))
open('/tmp/claude-0/bbn/l.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', '/tmp/claude-0/bbn/l.txt', '-c', 'copy', 'public/ylm/bbnever.mp4'], check=True)
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'public/ylm/bbnever.mp4']))
def tl(src_t):
    for o, a, b in spans:
        if a - 0.01 <= src_t < b: return round(o + src_t - a, 3)
# caption chunks: up to 3 words, break on punctuation
HL = {'15,000', '30k', 'ankle', 'snapped', 'sick', '10', 'kickoff', 'eagles', '6k', '1500', 'lost', 'sold', 'never', 'big', 'worst', 'done'}
FIX = {'jags': 'JAGS', 'prismojo': 'PRIZM MOJO'}
words = []
for o, a, b in spans:
    cur = []
    ws = [w for w in W if a - 0.05 <= w['startMs'] / 1000 < b - 0.05]
    # merge ',000' fragments
    m = []
    for w in ws:
        if m and w['text'].startswith(','): m[-1] = dict(m[-1], text=m[-1]['text'] + w['text'], endMs=w['endMs'])
        else: m.append(dict(w))
    for j, w in enumerate(m):
        cur.append(w)
        end = w['text'][-1:] in ',.?!' or len(cur) == 3 or j == len(m) - 1
        if end:
            txt = ' '.join(FIX.get(x['text'].lower().strip(',.?!'), x['text'].strip(',.!')) for x in cur).upper()
            hl = any(x['text'].lower().strip(',.?!') in HL for x in cur)
            words.append(dict(w=txt, s=round(o + cur[0]['startMs'] / 1000 - a, 3), hl=hl) | ({} if j < len(m) - 1 else dict(e=round(o + b - a, 3))))
            cur = []
h0 = cuts[0]
cfg = dict(base='ylm/bbnever.mp4', dur=round(dur, 3), baseVol=1, music=['einaudi_n', 0, 0.07], punch=True, whooshVol=0.2, cuts=cuts[:-1],
  freezes=[dict(a=round(h0 - 0.6, 3), b=h0, z=1.1, flash=True), dict(a=round(dur - 1.0, 3), b=99, z=1.08, flash=True)],
  texts=[dict(**{'from': 0, 'to': h0}, lines=['he owns 10 MORE of these…', 'and they make him SICK'], y=210, size=56, box=True, rot=0, emoji='1f922', hl=['SICK']),
         dict(**{'from': round(h0 - 0.6, 3), 'to': h0}, lines=['HOW IT STARTED'], y=1300, size=96, box=False, rot=-3, emoji='23ea'),
         dict(**{'from': h0, 'to': cuts[1]}, lines=['CARDS I WILL NEVER', 'PROFIT ON'], y=560, size=60, box=True, rot=0, emoji='1f4b8', hl=['NEVER']),
         dict(**{'from': cuts[1], 'to': cuts[2]}, lines=['bought for $15,000', 'offered 30K… then:'], y=210, size=54, box=True, rot=0, emoji='1f62c', hl=['30K…']),
         dict(**{'from': cuts[2], 'to': cuts[3]}, lines=['bought the hype year'], y=210, size=56, box=True, rot=0, emoji='1f4c9'),
         dict(**{'from': cuts[3], 'to': cuts[4]}, lines=['$6,000 → $1,500'], y=210, size=60, box=True, rot=0, emoji='1f62d', hl=['$1,500']),
         dict(**{'from': cuts[4], 'to': cuts[5]}, lines=['he didn\'t buy ONE…'], y=210, size=58, box=True, rot=0, emoji='1f480', hl=['ONE…']),
         dict(**{'from': cuts[5], 'to': 99}, lines=['"I haven\'t lost', 'if I haven\'t sold"'], y=210, size=56, box=True, rot=0, emoji='1f9e0'),
         dict(**{'from': round(dur - 1.0, 3), 'to': 99}, lines=['COPE OR FACTS?'], y=1300, size=100, box=False, rot=-4, emoji='1f914')],
  words=words,
  sfx=[['s_huh', 1.2, 0.3], ['m_rewind', round(h0 - 0.6, 3), 0.3, 0.6], ['m_cha-ching', tl(12.5), 0.3], ['s_money', tl(17.3), 0.3],
       ['m_record-scratch', tl(20.2), 0.3], ['s_fahhh', tl(20.6), 0.3], ['m_oh-hell-nah', tl(36.1), 0.3], ['s_awk', tl(50.2), 0.25],
       ['m_anime-wow', round(cuts[4] + 57.4 - 54.38, 3), 0.25], ['s_huh', round(cuts[4] + 62.3 - 54.38, 3), 0.3], ['m_record-scratch', round(dur - 1.0, 3), 0.25]])
allc = json.load(open('src/ylm.cfg.json')); allc['bbnever'] = cfg; json.dump(allc, open('src/ylm.cfg.json', 'w'), indent=1)
print('dur', round(dur, 2), 'cuts', cuts); print(len(words), 'captions:', ' | '.join(w['w'] for w in words[:14]))

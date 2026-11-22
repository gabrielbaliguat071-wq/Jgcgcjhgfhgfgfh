"""Backyard Breaks TikTok re-edits (2026-11-22): brady / grail / psa from @backyardbreaks TikTok -> public/ylm/tt<id>.mp4 + ylm.cfg.json 'tt<id>'.
Their burned captions are covered (white band under our banner, or blurred band under our captions). Usage: python3 build_tt.py <id>"""
import json, subprocess, os, sys
G = 'eq=contrast=1.06:saturation=1.12,unsharp=5:5:0.6'
C = {
 'brady': dict(src='brady', segs=[(16.0, 21.2, 0.6), (3.0, 29.6, 0), (30.0, 34.9, 1.0)], always=[(555, 775, 'white')], first=[], wordsY=1460,
   fix={'patrick': ''}, music=['phonk_n', 22.4, 0.07],
   texts=[(0, 'h', ['he KNEW what was coming…'], 'HOW IT STARTED', '1f631', ['KNEW']), ('h', 22.5, ['"DON\'T YOU DARE…"', 'WAIT FOR THE TEAM'], None, '1f440', ['TEAM']),
          (22.5, 99, ['TOM BRADY', 'TRUE ORANGE AUTO /25'], None, '1f525', ['ORANGE'])], endTxt='GREATEST BREAK EVER?', bannerY=585,
   hl={'no', 'way', 'brady', 'orange', 'dare', 'patriots', 'same', 'moly'}, sfx=[('s_huh', 3.1, 0.3), ('m_crowd-cheer', 17.0, 0.25), ('m_anime-wow', 22.6, 0.3), ('s_wow', 31.3, 0.3)]),
 'grail': dict(src='grail', segs=[(26.7, 31.0, 0.6), (0.0, 4.1, 0), (6.7, 45.9, 1.0)], always=[(1185, 1335, 'blur')], first=[(1320, 1600, 'blur')], wordsY=1190,
   fix={'little': 'Little', 'factor.': 'fractor', 'super': 'Super', "kim's": "Cam's", 'cl': 'CL'}, music=['empire_n', 18.8, 0.07],
   texts=[(0, 'h', ['his ALL-TIME', 'favorite purchase…'], 'HOW IT STARTED', '1f48e', ['ALL-TIME']), ('h', 19.5, ['the GOAT of his position', 'is NOT who you think'], None, '1f914', ['NOT']),
          (19.5, 99, ['CAM LITTLE', 'SUPERFRACTOR 1/1'], None, '1f410', ['SUPERFRACTOR'])], endTxt='GOAT KICKER?', bannerY=210,
   hl={'favorite', 'greatest', 'wrong', 'cl', 'cam', 'little', 'superfractor', 'record', 'goat', 'ring', 'kick'}, sfx=[('s_huh', 13.8, 0.3), ('m_anime-wow', 26.8, 0.3), ('s_ding', 29.5, 0.3), ('m_crowd-cheer', 39.0, 0.22)]),
 'psa': dict(src='psa', segs=[(57.8, 62.6, 0.6), (0.0, 5.0, 0), (15.2, 31.6, 0), (54.0, 65.0, 0), (93.2, 99.4, 1.0)], always=[(1265, 1425, 'blur')], first=[(1400, 1790, 'blur')], wordsY=1270,
   fix={'flag': 'Flagg', 'vembin': 'Wemban', 'yama': 'yama', 'bean': 'beam', 'geo': 'Geo'}, music=['funkabn_n', 33.2, 0.07],
   texts=[(0, 'h', ['the PSA return', 'nobody expected…'], 'HOW IT STARTED', '1f92f', ['nobody']), ('h', 99, ['PSA GRADING RETURN', 'W OR L?'], None, '1f4af', ['W', 'L?'])],
   endTxt='W OR L?', bannerY=210, merge={'yama', '-man'},
   hl={'big', 'christmas', 'flagg', '9', 'superfractor', 'nasty', 'mvp', 'gem', 'spider-man', 'tough', 'shaq', 'orange', 'stop'},
   sfx=[('s_wow', 3.4, 0.25), ('s_awk', 21.9, 0.25), ('s_ding', 24.0, 0.25), ('m_anime-wow', 60.1, 0.3), ('m_cha-ching', 62.0, 0.25), ('m_crowd-cheer', 98.3, 0.22)]),
}
eid = sys.argv[1]; c = C[eid]; SRC = f'../footage/bbtt/{c["src"]}.mp4'; W = json.load(open(f'../footage/bbtt/{c["src"]}.words.json'))
def cover(regs):
    f = '[0:v]scale=1080:1920:flags=lanczos[sc];'; f = '[sc]'; k = 0; chain = ['[0:v]scale=1080:1920:flags=lanczos[sc]']
    for y0, y1, m in regs:
        if m == 'white': chain.append(f'{f}drawbox=x=0:y={y0}:w=1080:h={y1-y0}:color=white:t=fill[c{k}]')
        else: chain.append(f'{f}split[m{k}][n{k}];[n{k}]crop=1080:{y1-y0}:0:{y0},boxblur=28:3,eq=brightness=-0.05[b{k}];[m{k}][b{k}]overlay=0:{y0}[c{k}]')
        f = f'[c{k}]'; k += 1
    return ';'.join(chain) + (';' if chain else ''), f
d = f'/tmp/claude-0/tt_{eid}'; os.makedirs(d, exist_ok=True); parts = []; spans = []; t = 0; cuts = []
for i, (a, b, fz) in enumerate(c['segs']):
    pre, f = cover(c['always'] + (c['first'] if i == 1 else []))
    out = f'{d}/s{i}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-to', str(b), '-i', SRC, '-filter_complex',
        f'{pre}{f}{G},fps=30,tpad=stop_mode=clone:stop_duration={fz}[v];[0:a]apad=pad_dur={fz}[au]', '-map', '[v]', '-map', '[au]',
        '-t', str(b - a + fz), '-c:v', 'libx264', '-crf', '18', '-preset', 'fast', '-c:a', 'aac', '-ar', '48000', out], check=True)
    parts.append(out); spans.append((t, a, b)); t += b - a + fz; cuts.append(round(t, 3))
open(f'{d}/l.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{d}/l.txt', '-c', 'copy', f'public/ylm/tt{eid}.mp4'], check=True)
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'public/ylm/tt{eid}.mp4']))
def tl(s):  # source -> timeline, prefer story spans over the hook
    for o, a, b in spans[1:] + spans[:1]:
        if a - 0.01 <= s < b: return round(o + s - a, 3)
words = []
for o, a, b in spans:
    m = []
    for w in W:
        if not (a - 0.05 <= w['startMs'] / 1000 < b - 0.05): continue
        x = dict(w); k = x['text'].lower().strip(',.?!'); x['text'] = c['fix'].get(k, x['text']) if k in c['fix'] else x['text']
        if not x['text']: continue
        if m and (k in c.get('merge', set()) or x['text'].startswith(',')): m[-1]['text'] = m[-1]['text'].rstrip(',.') + x['text'].lstrip(); continue
        m.append(x)
    cur = []
    for j, w in enumerate(m):
        cur.append(w)
        if w['text'][-1:] in ',.?!' or len(cur) == 3 or j == len(m) - 1:
            txt = ' '.join(x['text'].strip(',.!') for x in cur).upper()
            hl = any(x['text'].lower().strip(',.?!') in c['hl'] for x in cur)
            words.append(dict(w=txt, s=round(o + cur[0]['startMs'] / 1000 - a, 3), hl=hl) | ({} if j < len(m) - 1 else dict(e=round(o + b - a, 3))))
            cur = []
h0 = cuts[0]; T = lambda v: h0 if v == 'h' else (v if v == 0 or v == 99 else tl(v))
texts = []
for fr, to, lines, flash, emo, hl in c['texts']:
    texts.append({'from': T(fr), 'to': T(to), 'lines': lines, 'y': c['bannerY'], 'size': 56, 'box': True, 'rot': 0, 'emoji': emo, 'hl': hl})
    if flash: texts.append({'from': round(h0 - 0.6, 3), 'to': h0, 'lines': [flash], 'y': 1000, 'size': 96, 'box': False, 'rot': -3, 'emoji': '23ea'})
texts.append({'from': round(dur - 1.0, 3), 'to': 99, 'lines': [c['endTxt']], 'y': 1000, 'size': 96, 'box': False, 'rot': -4, 'emoji': '1f914'})
sfx = [['m_rewind', round(h0 - 0.6, 3), 0.3, 0.6], ['m_record-scratch', round(dur - 1.0, 3), 0.22]] + [[n, tl(s), v] for n, s, v in c['sfx'] if tl(s) is not None]
cfg = dict(base=f'ylm/tt{eid}.mp4', dur=round(dur, 3), baseVol=1, music=c['music'], punch=True, whooshVol=0.2, cuts=cuts[:-1], wordsY=c['wordsY'], wordSize=80,
           freezes=[dict(a=round(h0 - 0.6, 3), b=h0, z=1.1, flash=True), dict(a=round(dur - 1.0, 3), b=99, z=1.08, flash=True)], texts=texts, words=words, sfx=sfx)
assert all(words[i]['s'] <= words[i + 1]['s'] for i in range(len(words) - 1))
allc = json.load(open('src/ylm.cfg.json')); allc[f'tt{eid}'] = cfg; json.dump(allc, open('src/ylm.cfg.json', 'w'), indent=1)
print(eid, 'dur', round(dur, 2), 'cuts', cuts, '|', ' | '.join(w['w'] for w in words[:12]))

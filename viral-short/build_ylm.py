"""YoungLA runway montages: builds public/ylm/<id>.mp4 (9:16 crops, slow-mo via setpts+atempo, freeze via tpad) from bvm.mp4
and prints the cut / freeze times for ylm.cfg.json. Usage: python3 build_ylm.py <id>"""
import subprocess, sys, os, json
S = '../footage/youngla/bvm.mp4'
G = 'eq=contrast=1.08:saturation=1.18,unsharp=5:5:0.8'
SEGS = {
 'dance': [dict(a=650.3, b=652.6, cx=990, z=1.25, fz=0.7), dict(a=653.5, b=655.6, band=1, br=1),
           dict(a=635.6, b=638.2, band=1), dict(a=600.2, b=602.0, cx=920, r=0.6, fz=0.6),
           dict(a=647.6, b=650.3, cx=980, z=1.25), dict(a=794.0, b=795.9, cx=940, r=0.7, fz=1.2)],
 'rate':  [dict(a=1112.0, b=1114.5, cx=1100, r=0.7), dict(a=1078.6, b=1081.0, cx=1040), dict(a=1092.3, b=1094.3, cx=1080),
           dict(a=966.0, b=968.3, cx=1080), dict(a=934.0, b=935.75, cx=1020), dict(a=1132.0, b=1135.0, cx=920, fz=1.2)],
 'million': [dict(a=749.0, b=752.75, cx=920, src=778.0), dict(a=766.3, b=769.0, cx=1380, br=1), dict(a=783.2, b=786.3, cx=920),
             dict(a=790.6, b=793.7, cx=900), dict(a=794.0, b=795.9, cx=940, r=0.7), dict(a=796.8, b=797.7, cx=1380, fz=1.4, br=1)],
}
eid = sys.argv[1]; BR = ',eq=gamma=1.4:brightness=0.04'; os.makedirs(f'/tmp/claude-0/ya/{eid}', exist_ok=True); t = 0; parts = []
for i, s in enumerate(SEGS[eid]):
    a, b, r, fz, z = s['a'], s['b'], s.get('r', 1), s.get('fz', 0), s.get('z', 1)
    d = b - a; at = f'atempo={r}' if r < 1 else 'anull'; out = f'/tmp/claude-0/ya/{eid}/s{i}.mp4'
    if s.get('band'):
        v = f'[0:v]split[p][q];[p]scale=3414:1920,crop=1080:1920,boxblur=20:2,eq=brightness=-0.25[bg];[q]scale=1080:608,{G}{BR if s.get("br") else ""}[fg];[bg][fg]overlay=0:656,setpts=PTS/{r},fps=30,tpad=stop_mode=clone:stop_duration={fz}[v]'
    else:
        w, h = round(608 / z / 2) * 2, round(1080 / z / 2) * 2; x = max(0, min(1920 - w, s['cx'] - w // 2)); y = 1080 - h
        v = f'[0:v]crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos,{G}{BR if s.get("br") else ""},setpts=PTS/{r},fps=30,tpad=stop_mode=clone:stop_duration={fz}[v]'
    # 'src': video from another time (picture), audio from a..b (voice line over the flex)
    vin = ['-ss', str(s.get('src', a)), '-t', str(d), '-i', S]; ain = ['-ss', str(a), '-t', str(d), '-i', S]
    fc = v + f';[1:a]{at},apad=pad_dur={fz}[a]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *vin, *ain, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', f'{d / r + fz:.3f}',
                    '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-c:a', 'aac', '-ar', '48000', '-ac', '2', out], check=True)
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out]))
    print(f's{i} start {t:.3f}  freeze {t + d / r:.3f}-{t + dur:.3f}' if fz else f's{i} start {t:.3f}'); t += dur; parts.append(out)
open(f'/tmp/claude-0/ya/{eid}/l.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'/tmp/claude-0/ya/{eid}/l.txt', '-c', 'copy', f'public/ylm/{eid}.mp4'], check=True)
print('total', round(t, 3))

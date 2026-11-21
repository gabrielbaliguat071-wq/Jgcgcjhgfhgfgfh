"""SEGA Metaphor: ReFantazio trailer edits (Nov 21): base cuts from the official trailers only (footage/metaphor/*.mp4, 1080p30).
Modes: sq = native 1080x1080 crop at cx (no upscale = crisp) in the middle of a black 9:16 frame (text goes in the bars);
wide = whole 16:9 frame (keeps the trailer's own kinetic text readable). Usage: python3 build_mrf.py <id>"""
import subprocess, sys, os
D = '../footage/metaphor/'
SEGS = {
 'hm': [('heismay', 44.9, 46.7, 'sq', 960), ('heismay', 8.9, 12.2, 'sq', 960), ('heismay', 15.0, 17.6, 'wide', 0), ('heismay', 28.3, 31.9, 'sq', 960),
        ('heismay', 35.2, 38.7, 'sq', 960), ('heismay', 40.0, 43.9, 'sq', 1150), ('heismay', 50.8, 54.2, 'sq', 960)],
 'hv': [('louis', 51.4, 54.3, 'wide', 0), ('louis', 7.2, 9.4, 'wide', 0), ('louis', 17.7, 20.3, 'wide', 0), ('pro', 29.1, 31.9, 'wide', 0),
        ('pro', 35.4, 38.4, 'wide', 0), ('pro', 38.8, 41.8, 'wide', 0), ('pro', 42.6, 44.6, 'wide', 0), ('louis', 55.7, 59.35, 'sq', 960)],
 'fan': [('pro', 77.4, 79.4, 'wide', 0), ('hero30', 11.0, 15.4, 'wide', 0), ('hero30', 17.6, 19.2, 'sq', 960), ('hero30', 19.2, 22.2, 'sq', 960),
         ('hero30', 24.3, 26.9, 'sq', 960), ('pro', 59.0, 61.2, 'sq', 960), ('pro', 80.2, 82.9, 'sq', 960)],
}
eid = sys.argv[1]; tmp = f'/tmp/claude-0/mrf/{eid}'; os.makedirs(tmp, exist_ok=True); t = 0; parts = []
for i, (f, a, b, mode, cx) in enumerate(SEGS[eid]):
    if mode == 'sq': x = max(0, min(840, cx - 540)); v = f'[0:v]crop=1080:1080:{x}:0,pad=1080:1920:0:420:black'
    else: v = '[0:v]scale=1080:608:flags=lanczos,pad=1080:1920:0:656:black'
    out = f'{tmp}/s{i}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-t', f'{b - a:.3f}', '-i', D + f + '.mp4', '-filter_complex', v + ',fps=30,setsar=1[v]',
                    '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-b:a', '256k', out], check=True)
    print(f's{i} {f} {a}-{b} {mode} start {t:.3f}'); t += b - a; parts.append(out)
open(f'{tmp}/l.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/l.txt', '-c', 'copy', f'public/mrf/{eid}.mp4'], check=True)
print('total', round(t, 3))

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
 'qh': [('heismay', 28.3, 31.9, 'sq', 960), ('heismay', 18.25, 27.95, 'sq', 960, 19.4), ('heismay', 32.8, 38.6, 'sq', 960)],
 'ql': [('louis', 17.7, 20.3, 'wide', 0), ('louis', 7.7, 13.9, 'wide', 0), ('louis', 22.8, 25.1, 'wide', 0), ('louis', 0.0, 2.6, 'wide', 0), ('louis', 43.0, 46.0, 'sq', 960, 56.0)],
 'qa': [('pro', 32.1, 35.1, 'wide', 0), ('pro', 10.2, 13.9, 'sq', 960), ('pro', 14.7, 15.9, 'sq', 960), ('pro', 16.5, 19.75, 'sq', 960), ('pro', 0.0, 3.9, 'wide', 0)],
 'wh': [('heismay', 28.3, 31.9, 'full', 960, 35.2), ('heismay', 18.25, 24.5, 'full', [(22.3, 960), (23.9, 1190), (24.6, 420), (26.3, 1250)], 22.3),
        ('heismay', 25.15, 27.95, 'full', 1150, 32.6), ('heismay', 32.8, 38.6, 'full', [(40.0, 1300), (41.9, 1075), (42.9, 960)], 40.0), ('heismay', 50.8, 54.45, 'full', 960, 5.0)],
 'wl': [('louis', 17.7, 20.3, 'full', [(11.9, 920), (13.9, 1100)], 11.9), ('louis', 7.7, 11.8, 'full', 960, 32.9), ('louis', 11.8, 13.9, 'full', 1400, 31.4),
        ('louis', 22.8, 25.1, 'full', 1100, 40.0), ('louis', 55.7, 59.75, 'full', 960, 56.0, 3.15)],
 'wa': [('pro', 32.1, 35.45, 'full', 960, 59.0), ('pro', 10.2, 13.9, 'full', [(10.2, 960), (11.4, 1000), (12.9, 960)]), ('pro', 14.7, 15.9, 'full', [(14.7, 1100), (15.4, 900)]),
        ('pro', 16.5, 19.75, 'full', [(16.5, 1250), (17.4, 900), (19.4, 1100)]), ('pro', 77.4, 83.0, 'full', 960, 77.9, 4.95)],
 'fan': [('pro', 77.4, 79.4, 'wide', 0), ('hero30', 11.0, 15.4, 'wide', 0), ('hero30', 17.6, 19.2, 'sq', 960), ('hero30', 19.2, 22.2, 'sq', 960),
         ('hero30', 24.3, 26.9, 'sq', 960), ('pro', 59.0, 61.2, 'sq', 960), ('pro', 80.2, 82.9, 'sq', 960)],
}
def main():
    eid = sys.argv[1]; tmp = f'/tmp/claude-0/mrf/{eid}'; os.makedirs(tmp, exist_ok=True); t = 0; parts = []
    for i, seg in enumerate(SEGS[eid]):
        f, a, b, mode, cx = seg[:5]; vs = seg[5] if len(seg) > 5 else a   # optional 6th = video start (audio stays a..b)
        vmax = seg[6] if len(seg) > 6 else b - a   # optional 7th = video length, last frame held to fill
        if mode == 'full':   # full-bleed 9:16: crop 608x1080 (cx may be [(src_t, cx), ...] for cuts inside the segment) -> 1080x1920
            keys = cx if isinstance(cx, list) else [(vs, cx)]
            xs = [max(0, min(1312, c - 304)) for _, c in keys]; e = str(xs[-1])
            for (tk, _), xv in reversed(list(zip(keys[1:], xs[:-1]))): e = f'if(lt(t,{tk - vs:.3f}),{xv},{e})'
            v = f"[0:v]crop=608:1080:'{e}':0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6"
        elif mode == 'sq': x = max(0, min(840, cx - 540)); v = f'[0:v]crop=1080:1080:{x}:0,pad=1080:1920:0:420:black'
        else: v = '[0:v]scale=1080:608:flags=lanczos,pad=1080:1920:0:656:black'
        out = f'{tmp}/s{i}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(vs), '-t', f'{vmax:.3f}', '-i', D + f + '.mp4', '-ss', str(a), '-t', f'{b - a:.3f}', '-i', D + f + '.mp4',
                        '-filter_complex', v + f',fps=30,setsar=1,tpad=stop_mode=clone:stop_duration={b - a - vmax + 0.1:.3f}[v]', '-t', f'{b - a:.3f}', '-map', '[v]', '-map', '1:a', '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-b:a', '256k', out], check=True)
        print(f's{i} {f} {a}-{b} {mode} start {t:.3f}'); t += b - a; parts.append(out)
    open(f'{tmp}/l.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/l.txt', '-c', 'copy', f'public/mrf/{eid}.mp4'], check=True)
    print('total', round(t, 3))
if __name__ == '__main__': main()

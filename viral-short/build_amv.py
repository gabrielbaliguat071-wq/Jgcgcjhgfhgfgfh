"""Metaphor AMV edits (style of the user's 2nd reference TikTok: beat-synced fast cuts, stacked-panel collages, glowing-eye run, flashes).
Audio = ONE continuous stretch of an official trailer (its own music + lines, brief: original audio clearly audible, no outside music).
Clips = (t_out_start, t_out_end, mode, sources) cut on the trailer's beats (librosa). Modes: full (608x1080 crop at cx -> 9:16),
stack (3 x 16:9 panels), wide (16:9 band on black, keeps the trailer's own title cards readable). Usage: python3 build_amv.py <id>"""
import subprocess, sys, os, json
D = '../footage/metaphor/'
AMV = {
 'awaken': dict(audio=('pro', 26.05, 44.78), clips=[
   (0, 2.25, 'stack', [('pro', 77.9), ('hero30', 18.0), ('heismay', 5.0)]),
   (2.25, 3.43, 'full', [('pro', 77.9, 960)]),
   (3.43, 4.57, 'full', [('heismay', 9.0, 960)]), (4.57, 5.78, 'full', [('pro', 61.0, 960)]),
   (5.78, 7.05, 'full', [('heismay', 41.9, 1075)]), (7.05, 8.21, 'full', [('heismay', 35.2, 960)]),
   (8.21, 9.45, 'stack', [('louis', 32.9), ('pro', 11.4), ('hero30', 23.0)]),
   (9.45, 10.61, 'full', [('pro', 17.4, 900)]), (10.61, 11.72, 'full', [('pro', 12.9, 960)]),
   (11.72, 13.02, 'full', [('louis', 40.0, 1100)]), (13.02, 14.21, 'full', [('pro', 15.4, 900)]),
   (14.21, 15.34, 'full', [('louis', 12.0, 920)]),
   (15.34, 15.88, 'full', [('heismay', 44.95, 960)]), (15.88, 16.41, 'full', [('hero30', 18.0, 960)]), (16.41, 16.97, 'full', [('pro', 59.1, 960)]),
   (16.97, 18.73, 'full', [('pro', 81.3, 960)])]),
 'fantasy': dict(audio=('louis', 40.25, 55.37), clips=[
   (0, 0.86, 'full', [('louis', 40.0, 1100)]), (0.86, 1.67, 'full', [('louis', 41.1, 1100)]),
   (1.67, 2.58, 'stack', [('louis', 33.0), ('louis', 36.0), ('louis', 11.0)]),
   (2.58, 3.58, 'full', [('louis', 43.2, 960)]), (3.58, 4.46, 'full', [('louis', 12.0, 920)]),
   (4.46, 5.36, 'full', [('hero30', 26.0, 960)]), (5.36, 6.25, 'full', [('louis', 31.4, 1400)]),
   (6.25, 7.22, 'full', [('louis', 55.7, 960)]), (7.22, 8.13, 'stack', [('pro', 59.1), ('hero30', 18.2), ('heismay', 44.95)]),
   (8.13, 9.01, 'full', [('pro', 61.0, 960)]), (9.01, 9.82, 'full', [('heismay', 40.0, 1300)]), (9.82, 10.66, 'full', [('louis', 32.9, 960)]),
   (10.66, 11.11, 'full', [('heismay', 44.95, 960)]), (11.11, 11.56, 'full', [('pro', 59.3, 960)]),
   (11.56, 12.47, 'full', [('louis', 56.5, 960)]), (12.47, 13.37, 'wide', [('louis', 52.9)]), (13.37, 15.12, 'wide', [('louis', 54.0)])]),
'heismay': dict(audio=('heismay', 35.25, 56.3), clips=[
   (0, 3.45, 'full', [('heismay', 35.25, 960)]),
   (3.45, 4.75, 'stack', [('heismay', 9.0), ('pro', 19.6), ('hero30', 16.0)]),
   (4.75, 6.0, 'full', [('heismay', 40.0, 1300)]), (6.0, 7.05, 'full', [('heismay', 41.9, 1075)]),
   (7.05, 8.4, 'full', [('heismay', 43.3, 960)]),
   (8.4, 9.05, 'full', [('heismay', 44.95, 960)]), (9.05, 9.7, 'full', [('pro', 59.1, 960)]),
   (9.7, 11.2, 'full', [('pro', 19.5, 1000)]), (11.2, 13.0, 'full', [('heismay', 47.0, 960)]),
   (13.0, 14.3, 'stack', [('heismay', 50.0), ('hero30', 24.0), ('pro', 61.0)]),
   (14.3, 15.55, 'full', [('heismay', 32.6, 1150, 0.6)]), (15.55, 17.2, 'full', [('heismay', 50.8, 960)]),
   (17.2, 19.05, 'full', [('heismay', 5.0, 960)]), (19.05, 21.05, 'wide', [('heismay', 15.0)])]),
 'launch': dict(audio=('hero30', 7.4, 27.0), clips=[
   (0, 1.2, 'stack', [('hero30', 18.0), ('pro', 77.9), ('heismay', 9.0)]),
   (1.2, 2.4, 'full', [('pro', 1.0, 960)]), (2.4, 3.6, 'full', [('pro', 80.2, 960, 0.6)]),
   (3.6, 5.0, 'full', [('hero30', 11.0, 960)]), (5.0, 6.2, 'full', [('hero30', 12.4, 960)]),
   (6.2, 7.4, 'full', [('hero30', 13.6, 1100)]), (7.4, 8.4, 'full', [('hero30', 14.8, 960)]),
   (8.4, 9.4, 'full', [('hero30', 15.8, 960)]), (9.4, 10.4, 'full', [('hero30', 16.8, 960)]),
   (10.4, 11.9, 'full', [('hero30', 17.8, 960)]), (11.9, 14.7, 'full', [('hero30', 19.3, 960)]),
   (14.7, 17.0, 'stack', [('hero30', 23.0), ('hero30', 24.0), ('heismay', 47.0)]),
   (17.0, 19.6, 'full', [('hero30', 24.4, 960)])]),
 'party': dict(audio=('pro', 61.95, 83.05), clips=[
   (0, 1.0, 'full', [('pro', 61.95, 960)]), (1.0, 2.05, 'full', [('heismay', 35.4, 960)]),
   (2.05, 3.05, 'full', [('heismay', 41.9, 1075)]), (3.05, 4.6, 'full', [('pro', 65.0, 960)]),
   (4.6, 6.0, 'full', [('pro', 66.55, 960)]), (6.0, 8.0, 'full', [('pro', 68.0, 960)]),
   (8.0, 9.9, 'full', [('louis', 12.0, 920, 0.7)]), (9.9, 11.1, 'full', [('pro', 1.0, 960)]),
   (11.1, 12.0, 'full', [('hero30', 26.0, 960)]), (12.0, 12.8, 'full', [('pro', 74.0, 960)]),
   (12.8, 14.0, 'full', [('pro', 74.75, 960)]),
   (14.0, 14.47, 'full', [('heismay', 44.95, 960)]), (14.47, 14.94, 'full', [('hero30', 18.0, 960)]), (14.94, 15.4, 'full', [('pro', 59.1, 960)]),
   (15.4, 18.2, 'full', [('pro', 77.9, 960)]), (18.2, 21.1, 'full', [('pro', 80.15, 960)])])
}
G = 'eq=contrast=1.06:saturation=1.12'
def main():
    eid = sys.argv[1]; c = AMV[eid]; tmp = f'/tmp/claude-0/mrf/amv_{eid}'; os.makedirs(tmp, exist_ok=True); parts = []
    for i, (a, b, mode, srcs) in enumerate(c['clips']):
        d = b - a; out = f'{tmp}/c{i}.mp4'; ins = []
        for s in srcs: ins += ['-ss', str(s[1]), '-t', f'{d:.3f}', '-i', D + s[0] + '.mp4']
        if mode == 'full':   # 4th field = speed (<1 = slow-mo); video held on last frame if the source runs out
            sp = srcs[0][3] if len(srcs[0]) > 3 else 1
            ins = ['-ss', str(srcs[0][1]), '-t', f'{d * sp:.3f}', '-i', D + srcs[0][0] + '.mp4']
            x = max(0, min(1312, srcs[0][2] - 304))
            fc = f'[0:v]crop=608:1080:{x}:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,{G},setpts=PTS/{sp},tpad=stop_mode=clone:stop_duration=2[v]'
        elif mode == 'wide': fc = f'[0:v]scale=1080:608:flags=lanczos,pad=1080:1920:0:656:black[v]'
        else: fc = ';'.join(f'[{k}:v]scale=1080:608:flags=lanczos,{G}[p{k}]' for k in range(3)) + ';[p0][p1][p2]vstack=3,pad=1080:1920:0:48:black[v]'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', fc + ';[v]fps=30,setsar=1[o]', '-map', '[o]', '-an', '-t', f'{d:.3f}',
                        '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', out], check=True)
        parts.append(out)
    open(f'{tmp}/l.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
    f, a, b = c['audio']
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/l.txt', '-ss', str(a), '-t', f'{b - a:.3f}', '-i', D + f + '.mp4',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-shortest', f'public/mrf/amv_{eid}.mp4'], check=True)
    print(eid, 'ok', round(b - a, 2), 's')
if __name__ == '__main__': main()

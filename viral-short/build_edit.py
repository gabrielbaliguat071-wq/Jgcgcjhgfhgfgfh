"""Music EDITS (not clips) from the YoungLA show: beat-synced cuts of the best walks/flexes, slow-mo build-up -> drop.
Audio = music only (phonk, from 18.44 s, drop at 22.43). Clip = (out_a, out_b, src_t, cx, speed[, z]); speed<1 = slow-mo.
Effects (zoom pulse on every beat, shake/flash on the drop, glitch on cuts) are added in MRW.tsx (cfg 'ed_*')."""
import subprocess, sys, os
S = '../footage/youngla/bvm.mp4'
G = 'eq=contrast=1.1:saturation=1.22,curves=all=0/0 0.25/0.22 0.75/0.79 1/0.98,unsharp=5:5:0.8'
EDITS = {
 'ed1': dict(music=('public/res/phonk_n.mp3', 18.44, 37.44), clips=[
   (0, 1.34, 1112.0, 1100, 0.5), (1.34, 2.67, 600.2, 920, 0.6), (2.67, 3.99, 794.0, 940, 0.6),
   (3.99, 5.34, 1204.05, 920, 1), (5.34, 6.66, 749.0, 1000, 1), (6.66, 8.0, 556.4, 960, 1), (8.0, 8.66, 1078.6, 1040, 1),
   (8.66, 9.33, 1092.3, 1080, 1), (9.33, 10.66, 966.0, 1080, 0.8), (10.66, 12.0, 934.0, 1020, 1), (12.0, 13.34, 648.6, 950, 1, 1.25),
   (13.34, 14.67, 1228.6, 840, 1), (14.67, 16.0, 361.2, 960, 1), (16.0, 17.34, 1134.0, 920, 0.8), (17.34, 19.0, 1291.0, 560, 0.7)]),
}
import librosa as _lb
def beats_of(path, a, b):
    import numpy as np
    y, sr = _lb.load(path, sr=22050, offset=a, duration=b - a)
    _, bt = _lb.beat.beat_track(y=y, sr=sr)
    return [round(float(x), 3) for x in _lb.frames_to_time(bt, sr=sr)]
# shot pool (src, cx, z)
P = {'backlit': (1112.0, 1100, 1), 'bicep': (600.2, 920, 1), 'navy': (794.0, 940, 1), 'walk1': (1204.05, 920, 1), 'tank': (749.0, 1000, 1), 'red': (556.4, 960, 1),
     'big': (1078.6, 1040, 1), 'back': (1092.3, 1080, 1), 'beanie': (966.0, 1080, 1), 'chains': (934.0, 1020, 1), 'dance': (648.6, 950, 1.25), 'jay': (1228.6, 840, 1),
     'quave': (361.2, 960, 1), 'stare': (1134.0, 920, 1), 'navyclose': (1291.0, 560, 1), 'tankclose': (751.0, 1000, 1), 'flex2': (795.4, 940, 1), 'walk2': (602.5, 920, 1),
     'wide': (1132.0, 920, 1.0), 'redclose': (565.0, 960, 1), 'quave2': (369.0, 920, 1), 'chains2': (936.0, 1020, 1)}
def auto(music, a, b, plan, bpath):
    """plan: list of (n_beats, shot, speed); returns clips with out times on the song's beats"""
    bt = [x for x in beats_of(bpath, a, b)]
    clips, i = [], 0
    for n, shot, sp in plan:
        if i + n >= len(bt): break
        src, cx, z = P[shot]; clips.append((bt[i], bt[i + n], src, cx, sp, z)); i += n
    clips[0] = (0,) + clips[0][1:]
    return dict(music=(music, a, a + clips[-1][1]), clips=clips, beats=bt[:i + 1])

def main():
    eid = sys.argv[1]; c = EDITS[eid]; tmp = f'/tmp/claude-0/ed/{eid}'; os.makedirs(tmp, exist_ok=True); parts = []
    for i, cl in enumerate(c['clips']):
        a, b, src, cx, sp = cl[:5]; z = cl[5] if len(cl) > 5 else 1; d = b - a
        w, h = round(608 / z / 2) * 2, round(1080 / z / 2) * 2; x = max(0, min(1920 - w, cx - w // 2)); y = 1080 - h
        out = f'{tmp}/c{i}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(src), '-t', f'{d * sp + 0.1:.3f}', '-i', S, '-vf',
                        f"crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos,{G},setpts=PTS/{sp},fps=30,tpad=stop_mode=clone:stop_duration=1",
                        '-an', '-t', f'{d:.3f}', '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', out], check=True); parts.append(out)
    open(f'{tmp}/l.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
    m, ma, mb = c['music']
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/l.txt', '-ss', str(ma), '-t', f'{mb - ma:.3f}', '-i', m,
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-shortest', f'public/mrf/{eid}.mp4'], check=True)
    print(eid, 'ok')
EDITS['ed2'] = auto('public/res/montagem_n.mp3', 20.81, 39.2, [(2, 'backlit', 0.5), (2, 'navy', 0.55), (2, 'bicep', 0.6), (1, 'flex2', 0.6), (1, 'walk1', 1), (1, 'walk2', 1),
    (2, 'tank', 1), (2, 'red', 1), (2, 'back', 1), (2, 'beanie', 0.85), (2, 'chains', 1), (2, 'jay', 1), (2, 'dance', 1), (2, 'quave', 1), (2, 'stare', 0.8), (3, 'navyclose', 0.7)], '/tmp/claude-0/montagem_n.wav')
EDITS['ed3'] = auto('public/res/funkabn_n.mp3', 2.69, 18.3, [(2, 'wide', 0.6), (2, 'backlit', 0.6), (2, 'tankclose', 0.6), (1, 'flex2', 0.6), (4, 'big', 1), (4, 'red', 1), (4, 'quave2', 1),
    (3, 'stare', 0.8)], '/tmp/claude-0/funkabn_n.wav')
EDITS['ed4'] = auto('../public/music/spooky-phonk-fennecxx.mp3', 0.0, 12.25, [(2, 'navyclose', 1), (2, 'tankclose', 1), (2, 'jay', 1), (2, 'bicep', 1), (2, 'back', 1), (2, 'stare', 1),
    (2, 'redclose', 1), (2, 'dance', 1), (2, 'beanie', 1), (2, 'flex2', 1), (2, 'chains', 1), (2, 'quave', 1), (2, 'navy', 1)], '/tmp/claude-0/spooky-phonk-fennecxx.wav')
if __name__ == '__main__': main()

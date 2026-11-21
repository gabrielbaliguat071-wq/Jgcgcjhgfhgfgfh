"""The Weeknd — Hong Kong performance (Dropbox video, 1920x1080 23.976, instrumental). Recap-style edits <= 30 s:
audio = one continuous stretch of the performance (the official sound gets added MUTED in the app, per the brief);
visuals = best screen moments from the whole show, cut on the performance's own beats. Modes: full (608x1080 crop at cx), wide (16:9 band on black).
Usage: python3 build_hk.py <id>"""
import subprocess, sys, os
import librosa
S = '../footage/weeknd/hk.mp4'
G = 'eq=contrast=1.08:saturation=1.15,unsharp=5:5:0.6'
_y, _sr = librosa.load('/tmp/claude-0/nc/hk.wav', sr=22050)
_, _bt = librosa.beat.beat_track(onset_envelope=librosa.onset.onset_strength(y=_y, sr=_sr), sr=_sr)
BEATS = [float(x) for x in librosa.frames_to_time(_bt, sr=_sr)]
def plan(start_beat_t, shots):
    i0 = min(range(len(BEATS)), key=lambda i: abs(BEATS[i] - start_beat_t)); a0 = BEATS[i0]; i = i0; clips = []
    for n, src, mode, cx in shots:
        clips.append((round(BEATS[i] - a0, 3), round(BEATS[i + n] - a0, 3), src, mode, cx)); i += n
    return dict(audio=(a0, BEATS[i]), clips=clips, beats=[round(b - a0, 3) for b in BEATS[i0:i + 1]])
EDITS = {
 'hk1': plan(140.64, [(4, 8.0, 'wide', 0), (4, 12.0, 'wide', 0), (4, 18.0, 'full', 960), (4, 32.0, 'full', 900), (4, 36.0, 'full', 1000), (4, 45.0, 'full', 1100),
                      (4, 60.0, 'full', 900), (4, 92.0, 'full', 960), (4, 82.0, 'full', 960), (4, 100.0, 'full', 960), (4, 113.0, 'full', 900), (4, 179.0, 'full', 960),
                      (4, 176.0, 'full', 900), (4, 186.5, 'full', 960), (6, 190.5, 'full', 960)]),
 'hk2': plan(168.53, [(4, 83.0, 'full', 960), (2, 84.5, 'full', 960), (2, 98.5, 'full', 960), (2, 102.0, 'full', 960), (2, 106.0, 'full', 960), (4, 160.0, 'full', 900),
                      (2, 162.0, 'full', 900), (2, 164.0, 'full', 1000), (2, 168.0, 'full', 960), (2, 170.0, 'full', 960), (4, 174.5, 'full', 900), (2, 176.5, 'full', 900),
                      (2, 180.0, 'full', 960), (2, 182.0, 'full', 960), (2, 184.0, 'full', 960), (4, 186.0, 'full', 960), (2, 124.5, 'full', 960), (2, 126.5, 'full', 960),
                      (2, 131.0, 'full', 960), (6, 190.0, 'full', 960)]),
}
def main():
    eid = sys.argv[1]; c = EDITS[eid]; tmp = f'/tmp/claude-0/nc/{eid}'; os.makedirs(tmp, exist_ok=True); parts = []
    for i, (a, b, src, mode, cx) in enumerate(c['clips']):
        d = b - a; out = f'{tmp}/c{i}.mp4'
        if mode == 'full': x = max(0, min(1312, cx - 304)); vf = f'crop=608:1080:{x}:0,scale=1080:1920:flags=lanczos,{G}'
        else: vf = f'scale=1080:608:flags=lanczos,{G},pad=1080:1920:0:656:black'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(src), '-t', f'{d + 0.1:.3f}', '-i', S, '-vf', vf + ',fps=30,setsar=1', '-an', '-t', f'{d:.3f}',
                        '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', out], check=True); parts.append(out)
    open(f'{tmp}/l.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
    a, b = c['audio']
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/l.txt', '-ss', str(a), '-t', f'{b - a:.3f}', '-i', S,
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-shortest', f'public/mrf/{eid}.mp4'], check=True)
    print(eid, 'ok', round(b - a, 2), 's')
if __name__ == '__main__': main()

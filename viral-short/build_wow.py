"""Blizzard WoW: Forever (Clipping Culture, UK views): beat-synced hype edit from the OFFICIAL vertical Gameplay Reveal Trailer
(footage/wow/reveal_vrt.mp4, 1080x1920 native). Audio = one continuous stretch of the trailer's own music (no outside music);
inserts from the same trailer land on its beats; the trailer's own CARVE / A NEW / PATH cards stay in their own timing.
Avoid the end card ("4 November 2026 · pre-purchase now") — the game is out (brief). Usage: python3 build_wow.py <id>"""
import subprocess, sys, os
S = '../footage/wow/reveal_vrt.mp4'
EDITS = {
 'wow1': dict(audio=(127.27, 150.27), clips=[
   (0, 1.14, 98.3), (1.14, 2.30, 45.5), (2.30, 3.44, 52.5), (3.44, 4.60, 56.0), (4.60, 5.69, 73.3), (5.69, 6.89, 75.8),
   (6.89, 8.01, 82.0), (8.01, 8.64, 86.0), (8.64, 10.49, 135.91), (10.49, 11.68, 100.2), (11.68, 12.89, 138.95), (12.89, 14.02, 109.0),
   (14.02, 15.56, 141.29), (15.56, 16.76, 120.5), (16.76, 17.97, 125.0), (17.97, 18.55, 92.5), (18.55, 23.0, 145.82)]),
}
def main():
    eid = sys.argv[1]; c = EDITS[eid]; tmp = f'/tmp/claude-0/nb/{eid}'; os.makedirs(tmp, exist_ok=True); parts = []
    for i, (a, b, src) in enumerate(c['clips']):
        out = f'{tmp}/c{i}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(src), '-t', f'{b - a:.3f}', '-i', S, '-vf', 'scale=1080:1920,fps=30,setsar=1', '-an',
                        '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', out], check=True); parts.append(out)
    open(f'{tmp}/l.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
    a, b = c['audio']
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/l.txt', '-ss', str(a), '-t', f'{b - a:.3f}', '-i', S,
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-shortest', f'public/mrf/{eid}.mp4'], check=True)
    print(eid, 'ok')
if __name__ == '__main__': main()

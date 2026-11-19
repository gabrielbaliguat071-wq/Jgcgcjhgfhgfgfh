"""BloxClips x ForgeGUI MCP — 3 narrated funny edits (Nov 19). Kokoro TTS am_michael (user declined the ElevenLabs key this time;
house rule is ElevenLabs "Alex" when available). Each shot = one VO line; shot length follows the line. Captions = faster-whisper
word times on each line. Hooks talk to DEVS (making the game). Footage = campaign Gameplay Phone clips only; music = campaign track."""
import json, os, shutil, subprocess, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from faster_whisper import WhisperModel
PV = '../footage/forge/pv'
K = Kokoro('/root/kokoro/kokoro-v1.0.int8.onnx', '/root/kokoro/voices-v1.0.bin')
M = WhisperModel('small.en', device='cpu', compute_type='int8')
VIDS = {
 'fgfish': dict(hook="i asked claude + forgegui mcp for ONE cute fish in my roblox game", hookEmoji='1f41f', music=['MONTAGEM PERIGOSA', 8.0], end='never prompting at 3am again', endEmoji='1f480',
   shots=[('Abyss_Station_13', 2.0, "I asked Claude plus ForgeGUI MCP to add one cute little fish to my underwater Roblox game."),
          ('Abyss_Station_8', 0.5, "Something small. Something kids would like."),
          ('Abyss_Station_8', 5.2, "Claude said, got it."),
          ('Abyss_Station_4', 12.4, "That is NOT a fish. Why does it have TEETH?!"),
          ('Abyss_Station_5', 16.8, "I'm never prompting at three A M again.")]),
 'fgtitan': dict(hook="lil bro said i can't make attack on titan in roblox", hookEmoji='1f480', music=['Devil Eyes', 20.0], end='he lives in my room now', endEmoji='1f62d',
   shots=[('Titan_Slayers_6', 0.6, "My little brother asked me to make Attack on Titan in Roblox."),
          ('Titan_Slayers_4', 0.8, "I told him that takes a whole studio and like five years."),
          ('Titan_Slayers_7', 2.0, "So I typed one prompt into Claude with ForgeGUI MCP, just to prove him wrong."),
          ('Titan_Slayers_13', 0.6, "Now we have titans. Swinging. Explosions."),
          ('Titan_Slayers_15', 2.4, "He hasn't left my room in three days.")]),
 'fgufo': dict(hook="i asked claude + forgegui mcp for ONE ufo in my roblox game", hookEmoji='1f6f8', music=['MEOW BOSS', 0.0], end='i said ONE ufo', endEmoji='1f62d',
   shots=[('Beam_Them_Up_1', 1.6, "I asked Claude plus ForgeGUI MCP for one UFO in my Roblox game. Just one."),
          ('Beam_Them_Up_5', 4.0, "Okay, it's beaming up the house. Kind of cool."),
          ('Beam_Them_Up_2', 2.8, "Now it's stealing cows. Why is there a cow counter?"),
          ('Beam_Them_Up_6', 3.0, "Crop circles. In my farm."),
          ('Beam_Them_Up_11', 2.8, "I said ONE UFO. Why are there twelve?!")]),
}
camp = json.load(open('/home/user/Me-editing/.work/brief11/camp.json'))
def music(prefix):
    import urllib.parse
    f = [x for x in camp['files'] if x['name'].startswith(prefix)][0]; out = f'public/forge/m_{f["id"]}.mp3'
    if not os.path.exists(out): subprocess.run(['curl', '-sfL', '-o', out, 'https://files.bloxclips.com/' + urllib.parse.quote(f['url'])], check=True)
    return out[len('public/'):]
def screen_cy(path, t):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t + 0.5), '-i', path, '-frames:v', '1', '-vf', 'scale=108:192,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(192, 108).astype(float).mean(1)
    rows = np.where(a > 0.55 * a.max())[0]
    return float((rows[0] + rows[-1]) / 2 * 10), float((rows[-1] - rows[0]) * 10)
cfg = {}
for vid, v in VIDS.items():
    shots = []; voparts = []; t = 0.0
    for i, (clip, frm, line) in enumerate(v['shots']):
        a, sr = K.create(line, voice='am_michael', speed=1.08, lang='en-us')
        a = np.asarray(a, np.float32); dur = len(a) / sr
        segs, _ = M.transcribe(a if sr == 16000 else __import__('scipy.signal', fromlist=['resample']).resample(a, int(len(a) * 16000 / sr)).astype(np.float32), language='en', word_timestamps=True)
        words = [{'w': w.word.strip(), 's': round(t + 0.15 + w.start, 2), 'e': round(t + 0.15 + w.end, 2)} for s in segs for w in s.words]
        sdur = round(dur + (0.45 if i < len(v['shots']) - 1 else 1.6), 2)
        src = f'forge/{clip}.mp4'
        if not os.path.exists('public/' + src): shutil.copy(f'{PV}/{clip}.mp4', 'public/' + src)
        cy, h = screen_cy(f'{PV}/{clip}.mp4', frm)
        shots.append(dict(src=src, from_=frm, dur=sdur, cy=cy, sh=h, words=words, line=line))
        voparts.append((t + 0.15, a, sr)); t += sdur
    total = t; sr = voparts[0][2]; buf = np.zeros(int(total * sr) + sr, np.float32)
    for st, a, _ in voparts: i0 = int(st * sr); buf[i0:i0 + len(a)] += a
    sf.write(f'public/forge/vo/{vid}_raw.wav', buf, sr)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'public/forge/vo/{vid}_raw.wav', '-af', 'acompressor=threshold=-24dB:ratio=4:makeup=6dB,loudnorm=I=-14:TP=-1.5', '-ar', '48000', f'public/forge/vo/{vid}.wav'], check=True)
    cfg[vid] = dict(hook=v['hook'], hookEmoji=v['hookEmoji'], end=v['end'], endEmoji=v['endEmoji'], music=[music(v['music'][0]), v['music'][1]], vo=f'forge/vo/{vid}.wav',
                    shots=[{**{k: s[k] for k in ('src', 'dur', 'cy', 'sh', 'words')}, 'from': s['from_']} for s in shots])
    print(vid, round(total, 2), 's'); [print('  ', s['dur'], round(s['cy']), round(s['sh']), ' '.join(w['w'] for w in s['words'])) for s in shots]
json.dump(cfg, open('src/forgevo.cfg.json', 'w'), indent=1)

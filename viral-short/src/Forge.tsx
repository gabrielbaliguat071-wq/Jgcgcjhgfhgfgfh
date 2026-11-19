// BloxClips x ForgeGUI MCP (Nov 19) — "prompt escalation" meme for Roblox DEVS: the same game gets one more prompt per shot
// (rain -> tsunami -> tornado -> volcano -> "ok go crazy"), each prompt pops in as a chat bubble, chaos grows, the music drop
// lands on the last prompt. Footage = campaign "Gameplay Phone" clips (phone filming the monitor) zoomed onto the screen.
// Required: "ForgeGUI MCP" on screen and easy to read (bottom pill, whole video). Music = campaign track only.
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
type Shot = {src: string; from: number; dur: number; prompt: string; emoji: string; shake?: number; z?: number};
type FCfg = {hook: string; hookEmoji: string; shots: Shot[]; music: [string, number]; end: string; endEmoji: string};
export const FORGE: Record<string, FCfg> = {
  fgprompt: {
    hook: 'me prompting my roblox game with claude + forgegui mcp', hookEmoji: '1f62d',
    music: ['forge/music.mp3', 15.2], end: 'that was ONE prompt each', endEmoji: '1f940',
    shots: [
      {src: 'forge/td2.mp4', from: 4.0, dur: 2.6, prompt: '"add some rain to my game"', emoji: '1f642'},
      {src: 'forge/td5.mp4', from: 3.0, dur: 2.8, prompt: '"ok now a tsunami"', emoji: '1f610'},
      {src: 'forge/td3.mp4', from: 2.0, dur: 2.8, prompt: '"add a tornado too"', emoji: '1f633', shake: 4},
      {src: 'forge/td17.mp4', from: 2.6, dur: 2.6, prompt: '"and a volcano"', emoji: '1f630', shake: 7},
      {src: 'forge/td14.mp4', from: 3.0, dur: 3.6, prompt: '"ok go crazy"', emoji: '1f480', shake: 12, z: 1.08},
    ],
  },
};
const F = (s: number) => Math.round(s * 30);
export const forgeFrames = (id: string) => FORGE[id].shots.reduce((a, s) => a + F(s.dur), 0);
const stroke = (w: number): React.CSSProperties => ({WebkitTextStroke: `${w}px #000`, paintOrder: 'stroke fill'});

export const Forge: React.FC<{edit: string}> = ({edit}) => {
  const cfg = FORGE[edit], f = useCurrentFrame(), {fps} = useVideoConfig(), END = forgeFrames(edit);
  const starts: number[] = []; cfg.shots.reduce((a, s) => { starts.push(a); return a + F(s.dur); }, 0);
  const si = starts.filter((s) => s <= f).length - 1, sh = cfg.shots[si], lf = f - starts[si], n = F(sh.dur);
  const last = si === cfg.shots.length - 1;
  // zoom onto the monitor (phone footage: screen ~ y 0-1150 of 1920); slow push + punch on each cut
  const punch = interpolate(lf, [0, 3, 10], [1.12, 1.06, 1], clamp);
  const zoom = 1.5 * (sh.z ?? 1) * punch * (1 + 0.05 * lf / n);
  const sk = sh.shake ? Math.sin(lf * 2.1) * sh.shake * (lf < 18 || last ? 1 : 0.35) : 0;
  const whip = lf < 4 && f > 0 ? [-90, -40, -12, 0][lf] : 0;
  const bub = spring({frame: lf - 4, fps, config: {damping: 11, stiffness: 230}});
  const typed = Math.min(sh.prompt.length, Math.max(0, Math.floor((lf - 4) * 1.6)));
  const emo = spring({frame: lf - 4 - Math.ceil(sh.prompt.length / 1.6), fps, config: {damping: 9, stiffness: 260}});
  const endAt = END - 40, endK = spring({frame: f - endAt, fps, config: {damping: 11, stiffness: 220}});
  return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
    <AbsoluteFill style={{transform: `translate(${whip + sk}px, ${sk * 0.6}px) scale(${zoom})`, transformOrigin: '540px 430px', filter: whip ? `blur(${Math.abs(whip) / 30}px)` : undefined}}>
      {cfg.shots.map((s, i) => <Sequence key={i} from={starts[i]} durationInFrames={F(s.dur)} layout="none">
        <OffthreadVideo src={staticFile(s.src)} startFrom={F(s.from)} volume={0.25} style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920}} />
      </Sequence>)}
    </AbsoluteFill>
    {last && lf < 4 && <AbsoluteFill style={{background: '#fff', opacity: [0.9, 0.6, 0.3, 0.1][lf]}} />}
    {/* hook (whole video) */}
    <div style={{position: 'absolute', top: 110, left: 40, right: 40, textAlign: 'center', background: 'rgba(0,0,0,0.72)', borderRadius: 26, padding: '14px 20px', transform: `scale(${interpolate(f, [0, 5, 8], [0.7, 1.05, 1], clamp)})`}}>
      <span style={{fontFamily: MONT, fontWeight: 800, fontSize: 58, lineHeight: '72px', color: '#fff', ...stroke(12)}}>{cfg.hook} </span>
      <Img src={staticFile(`res/emoji/${cfg.hookEmoji}.png`)} style={{width: 66, height: 66, verticalAlign: 'middle'}} />
    </div>
    {/* prompt chat bubble */}
    {lf >= 4 && f < endAt && <div style={{position: 'absolute', top: 470, left: 0, right: 0, display: 'flex', justifyContent: 'center', transform: `scale(${0.6 + 0.4 * bub})`}}>
      <div style={{background: '#F4EFE6', borderRadius: 30, padding: '20px 30px', boxShadow: '0 10px 30px rgba(0,0,0,0.55)', display: 'flex', alignItems: 'center', gap: 16, maxWidth: 940}}>
        <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 30, color: '#fff', background: '#D97757', borderRadius: 14, padding: '6px 12px'}}>prompt</div>
        <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 50, color: '#1a1a1a'}}>{sh.prompt.slice(0, typed)}<span style={{opacity: typed < sh.prompt.length && lf % 10 < 5 ? 1 : 0}}>|</span></div>
        <Img src={staticFile(`res/emoji/${sh.emoji}.png`)} style={{width: 72, height: 72, transform: `scale(${emo})`}} />
      </div>
    </div>}
    {/* step counter */}
    {f < endAt && <div style={{position: 'absolute', top: 395, left: 0, right: 0, textAlign: 'center', fontFamily: MONT, fontWeight: 800, fontSize: 38, color: '#FFE14D', ...stroke(8)}}>prompt {si + 1}</div>}
    {f >= endAt && <div style={{position: 'absolute', top: 470, left: 40, right: 40, textAlign: 'center', transform: `scale(${0.6 + 0.4 * endK}) rotate(-3deg)`}}>
      <span style={{fontFamily: MONT, fontWeight: 800, fontSize: 80, color: '#FFE14D', ...stroke(14)}}>{cfg.end} </span>
      <Img src={staticFile(`res/emoji/${cfg.endEmoji}.png`)} style={{width: 86, height: 86, verticalAlign: 'middle'}} />
    </div>}
    {/* REQUIRED: ForgeGUI MCP on screen, whole video */}
    <div style={{position: 'absolute', bottom: 250, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
      <div style={{background: 'rgba(0,0,0,0.78)', borderRadius: 20, padding: '14px 30px', fontFamily: MONT, fontWeight: 800, fontSize: 48, color: '#fff', border: '3px solid #D97757'}}>
        made w/ claude + <span style={{color: '#FFE14D'}}>forgegui mcp</span></div>
    </div>
    <Audio src={staticFile(cfg.music[0])} startFrom={F(cfg.music[1])} volume={0.75} />
  </AbsoluteFill>;
};

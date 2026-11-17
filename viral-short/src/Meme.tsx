// "Meme clip" look (Nov 17): the VverPaldo CONCEPT (payoff hook -> 2-frame white flash hard cut -> story that loops into
// the hook, speaker zooms, slow push-in, punch-ins, green/red tints) in a DIFFERENT look:
//  - full-screen 9:16 face-cam (no black bars); wide two-shots become a band over a blurred, zoomed copy of the shot
//  - white top banner (heavy black uppercase Montserrat, red/green keywords), like the card-pull refs D/F
//  - 2-3 word glow captions (Ref A: no stroke, white glow, coloured keywords) that build word by word + iOS emoji
//  - motion-blur whip on every cut with fast-whoosh, emoji pops with ding-2, green flash on the payoff
// Data: scenes from edits.gen.json (same planner as Guess), cfg from meme.cfg.json.
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import GEN from './edits.gen.json';
import CFG from './meme.cfg.json';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const GREEN = 'rgb(92,255,92)', RED = 'rgb(255,60,60)', YEL = '#FFE14D';
type Ref = [string, string?, number?];
type Word = {word: string; startFrame: number; endFrame: number};
type Scene = {id: string; videoStartSec: number; durationInFrames: number; crops: number[][]; words: Word[]};
type MemeCfg = {top: string; hl: Record<string, string>; src: string; music: [string, number]; musicVol?: number; label?: string;
  kw: Record<string, string>; emoji: [Ref, string][]; tints: [Ref, string][]; punch: Ref[]; cta: string; ctaAt: Ref;
  sfx?: [Ref, string, number][]};
export const MEME = CFG as unknown as Record<string, MemeCfg>;
const SC = GEN as unknown as Record<string, Scene[]>;
export const memeFrames = (id: string) => SC[id].reduce((a, s) => a + s.durationInFrames, 0);

const glow = (c: string) => `0 0 10px ${c}99, 0 0 24px ${c}66, 0 3px 8px #000c, 0 0 2px #000`;

export const Meme: React.FC<{edit: string}> = ({edit}) => {
  const cfg = MEME[edit], SCENES = SC[edit], f = useCurrentFrame(), {fps} = useVideoConfig();
  const START: Record<string, number> = {}; SCENES.reduce((a, s) => { START[s.id] = a; return a + s.durationInFrames; }, 0);
  const END = memeFrames(edit);
  const at = ([id, word, nth = 0]: Ref) => {
    if (!word) return START[id!];
    const w = SCENES.find((s) => s.id === id)!.words.filter((x) => x.word.toLowerCase().replace(/[^a-z0-9$-]/g, '').startsWith(word.toLowerCase()))[nth];
    if (!w) throw new Error(`no word ${id}/${word}/${nth}`);
    return START[id!] + w.startFrame;
  };
  const near = (list: number[], len: number) => list.map((t) => f - t).find((d) => d >= 0 && d < len);

  // scene + crop
  const si = Math.max(0, SCENES.findIndex((s) => f >= START[s.id] && f < START[s.id] + s.durationInFrames)), sc = SCENES[si], lf = f - START[sc.id];
  const ci = sc.crops.filter(([t]) => t <= lf).length - 1, crop = sc.crops[Math.max(0, ci)];
  const shotA = crop[0], shotB = sc.crops[ci + 1]?.[0] ?? sc.durationInFrames;
  const [cx, cz, cy] = [crop[1], crop[2] ?? 1, crop[3] ?? 540];
  const band = cz < 1;   // wide two-shot: 16:9 band over a blurred copy
  const CUTS = SCENES.map((s) => START[s.id]).concat(SCENES.flatMap((s) => s.crops.slice(1).map(([t]) => START[s.id] + t)));
  const whip = near(CUTS.filter((t) => t > 0), 5);
  const PUNCH = cfg.punch.map(at), pu = near(PUNCH, 10);
  const push = 1 + 0.05 * Math.min(1, (lf - shotA) / Math.max(1, shotB - shotA));
  const punch = pu === undefined ? 1 : interpolate(pu, [0, 2, 10], [1.12, 1.1, 1], clamp);
  const TINTS = cfg.tints.map(([r, c]) => [at(r), c === 'G' ? GREEN : RED] as const);
  const tint = TINTS.map(([t, c]) => [[0.55, 0.45, 0.32, 0.2, 0.1][f - t], c] as const).find(([a]) => a !== undefined);
  const hard = SCENES[1] ? f - START[SCENES[1].id] : -9;   // hook -> story hard cut (VverPaldo concept)
  const intro = f < 10 ? interpolate(f, [0, 10], [1.12, 1], clamp) : 1;
  const zoomAll = punch * push * intro, shake = pu === 0 ? 10 : pu === 1 ? -6 : 0;
  const wx = whip === undefined ? 0 : [-140, -70, -25, -8, 0][whip], wb = whip === undefined ? 0 : [40, 26, 12, 4, 0][whip];
  const tSrc = sc.videoStartSec + lf / fps;
  const video = (style: React.CSSProperties, muted = false) => <Sequence key={sc.id + (muted ? 'm' : '')} from={START[sc.id]} durationInFrames={sc.durationInFrames} layout="none"><OffthreadVideo src={staticFile(cfg.src)} muted={muted} startFrom={Math.round(sc.videoStartSec * fps)} style={style} /></Sequence>;

  // full-frame crop: source scaled so its height fills 1920*z
  const S = (1920 / 1080) * cz, vw = 1920 * S, vh = 1080 * S;
  const left = Math.min(0, Math.max(1080 - vw, 540 - cx * S)), top = Math.min(0, Math.max(1920 - vh, 960 - cy * S));

  // captions: chunks of <=3 words (break on scene change or a pause), words appear as they are spoken
  const words = SCENES.flatMap((s) => s.words.map((w) => ({...w, s: s.id, at: START[s.id] + w.startFrame, end: START[s.id] + w.endFrame})));
  const chunks: (typeof words)[] = [];
  words.forEach((w, i) => { const c = chunks[chunks.length - 1], p = words[i - 1];
    if (!c || c.length >= 3 || p.s !== w.s || w.at - p.end > 9 || /[.?!,]$/.test(p.word)) chunks.push([w]); else c.push(w); });
  const ch = chunks.filter((c) => f >= c[0].at).pop(), chEnd = ch ? (chunks[chunks.indexOf(ch) + 1]?.[0].at ?? END) : 0;
  const showCap = ch && f < chEnd && f >= ch[0].at;
  const chK = ch ? f - ch[0].at : 0, chPop = spring({frame: chK, fps, config: {damping: 12, stiffness: 220}});
  const EMO = cfg.emoji.map(([r, e]) => ({t: at(r), e}));
  const emo = EMO.filter((x) => f >= x.t && f < x.t + 30).pop();
  const ctaFrom = at(cfg.ctaAt);

  const FX: [string, number, number][] = [];
  const add = (file: string, t: number, v: number) => { if (t >= 0 && !FX.some(([, u]) => Math.abs(u - t) < 4)) FX.push([file, t, v]); };
  if (SCENES[1]) add('s_camflash.mp3', START[SCENES[1].id], 0.45);
  TINTS.forEach(([t, c]) => add(c === GREEN ? 'rizz.mp3' : 'shock.mp3', t, 0.38));
  (cfg.sfx ?? []).forEach(([r, file, v]) => add(file, at(r), v));
  EMO.forEach(({t}) => add('m_ding-2.mp3', t, 0.16));
  CUTS.filter((t) => t > 0).forEach((t) => add('m_fast-whoosh.mp3', t - 16, 0.3));   // whoosh peak (550 ms) on the cut
  PUNCH.forEach((t) => add('pop.mp3', t, 0.2));

  return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
    <AbsoluteFill style={{transform: `translateX(${wx + shake}px) scale(${zoomAll})`, filter: `saturate(1.12) contrast(1.05)${wb ? ` blur(${wb / 6}px)` : ''}`}}>
      {band ? <>
        <AbsoluteFill style={{filter: 'blur(28px) brightness(0.55)', transform: 'scale(1.15)'}}>{video({position: 'absolute', top: 0, left: (1080 - 3413) / 2, width: 3413, height: 1920}, true)}</AbsoluteFill>
        {video({position: 'absolute', left: 0, top: cy - 304, width: 1080, height: 608, boxShadow: '0 10px 40px #000'})}
      </> : video({position: 'absolute', left, top, width: vw, height: vh})}
      {tint && <AbsoluteFill style={{background: tint[1], opacity: tint[0], mixBlendMode: 'screen'}} />}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, transparent 55%, rgba(0,0,0,0.45) 100%)'}} />
    </AbsoluteFill>
    {hard >= 0 && hard < 3 && <AbsoluteFill style={{background: '#fff', opacity: [0.95, 0.55, 0.2][hard]}} />}
    {f < 4 && <AbsoluteFill style={{background: '#fff', opacity: 1 - f / 4}} />}

    {/* white hook banner, whole video */}
    <div style={{position: 'absolute', top: 150, left: 50, right: 50, display: 'flex', justifyContent: 'center', transform: `scale(${interpolate(f, [0, 6, 9], [0.6, 1.05, 1], clamp)})`}}>
      <div style={{background: '#fff', borderRadius: 18, padding: '18px 30px', boxShadow: '0 8px 26px rgba(0,0,0,0.55)', fontFamily: MONT, fontWeight: 800, fontSize: 56, lineHeight: '64px', color: '#111', textAlign: 'center', textTransform: 'uppercase'}}>
        {cfg.top.split(' ').map((w, i) => <span key={i} style={{color: cfg.hl[w] ?? '#111'}}>{w} </span>)}
      </div>
    </div>
    {cfg.label && f < 75 && <div style={{position: 'absolute', top: 395, left: 0, right: 0, textAlign: 'center', opacity: interpolate(f, [0, 6, 66, 75], [0, 1, 1, 0], clamp)}}>
      <span style={{fontFamily: MONT, fontWeight: 800, fontSize: 32, color: '#fff', background: 'rgba(0,0,0,0.65)', borderRadius: 12, padding: '6px 18px', letterSpacing: 1}}>{cfg.label}</span>
    </div>}

    {/* emoji pop above the caption */}
    {emo && (() => { const k = f - emo.t, s = interpolate(k, [0, 4, 7], [0.2, 1.2, 1], clamp) * (1 + 0.04 * Math.sin(k / 3)), o = k > 24 ? (30 - k) / 6 : 1;
      return <Img src={staticFile(`res/emoji/${emo.e}.png`)} style={{position: 'absolute', left: 540 - 75, top: 1060, width: 150, height: 150, opacity: o, transform: `scale(${s}) rotate(${6 * Math.sin(k / 4)}deg)`, filter: 'drop-shadow(0 6px 10px rgba(0,0,0,0.5))'}} />; })()}
    {/* captions */}
    {showCap && <div style={{position: 'absolute', top: 1235, left: 40, right: 40, textAlign: 'center', transform: `scale(${0.8 + 0.2 * chPop})`}}>
      {ch!.map((w, i) => { const said = f >= w.at, cur = said && (ch![i + 1] ? f < ch![i + 1].at : true), key = w.word.toLowerCase().replace(/[^a-z0-9$-]/g, '');
        const col = cfg.kw[key] ?? '#FFFFFF';
        return <span key={i} style={{display: 'inline-block', margin: '0 20px', fontFamily: MONT, fontWeight: 800, fontSize: 82, lineHeight: '96px', textTransform: 'uppercase',
          color: col, textShadow: glow(col === '#FFFFFF' ? '#ffffff' : col), opacity: said ? 1 : 0, transform: `scale(${cur ? 1.04 : 1})`}}>{w.word.replace(/[.,!]+$/, '')}</span>; })}
    </div>}
    {f >= ctaFrom && f < ctaFrom + 80 && <div style={{position: 'absolute', top: 1560, left: 0, right: 0, textAlign: 'center', opacity: Math.min(1, (f - ctaFrom) / 5)}}>
      <span style={{fontFamily: MONT, fontWeight: 800, fontSize: 44, color: '#111', background: YEL, borderRadius: 14, padding: '8px 22px', boxShadow: '0 6px 18px rgba(0,0,0,0.5)'}}>{cfg.cta}</span>
    </div>}

    <Audio src={staticFile(`res/${cfg.music[0]}.mp3`)} startFrom={Math.round(cfg.music[1] * fps)} volume={cfg.musicVol ?? 0.45} loop />
    {FX.map(([file, t, v], i) => <Sequence key={i} from={t}><Audio src={staticFile(`res/${file}`)} volume={v} /></Sequence>)}
    {/* tSrc kept for debugging stills */}
    <div style={{display: 'none'}}>{tSrc}</div>
  </AbsoluteFill>;
};

// "Stacked" look (Nov 17, 3rd look): VverPaldo CONCEPT (payoff hook -> hard cut -> story that loops into the hook, speaker
// zooms, push-in, punch-ins) in a split-screen layout (Ref A stacked): wide table shot on top with a red ring on whoever
// talks, speaker close-up below, captions on the seam with the spoken word in a yellow highlight box.
// User rules (2026-11-17): NO colour fades (no tint flashes, no white fade, no darkening) and only a little blur.
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import GEN from './edits.gen.json';
import CFG from './stack.cfg.json';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
type Ref = [string, string?, number?];
type Scene = {id: string; videoStartSec: number; durationInFrames: number; crops: number[][]; words: {word: string; startFrame: number; endFrame: number}[]};
type StackCfg = {top: string; hl: Record<string, string>; src: string; music: [string, number]; musicVol?: number;
  ring: Record<string, number[]>; emoji: [Ref, string][]; punch: Ref[]; cta: string; ctaAt: Ref; sfx?: [Ref, string, number][]};
export const STACK = CFG as unknown as Record<string, StackCfg>;
const SC = GEN as unknown as Record<string, Scene[]>;
export const stackFrames = (id: string) => SC[id].reduce((a, s) => a + s.durationInFrames, 0);

const HEAD_H = 190, TOP_H = 608, TOP_Y = HEAD_H, BOT_Y = HEAD_H + TOP_H, BOT_H = 1920 - BOT_Y;
const norm = (w: string) => w.toLowerCase().replace(/[^a-z0-9$-]/g, '');

export const Stack: React.FC<{edit: string}> = ({edit}) => {
  const cfg = STACK[edit], SCENES = SC[edit], f = useCurrentFrame(), {fps} = useVideoConfig();
  const START: Record<string, number> = {}; SCENES.reduce((a, s) => { START[s.id] = a; return a + s.durationInFrames; }, 0);
  const END = stackFrames(edit);
  const at = ([id, word, nth = 0]: Ref) => {
    if (!word) return START[id!];
    const w = SCENES.find((s) => s.id === id)!.words.filter((x) => norm(x.word).startsWith(word))[nth];
    if (!w) throw new Error(`no word ${id}/${word}/${nth}`);
    return START[id!] + w.startFrame;
  };
  const near = (list: number[], len: number) => list.map((t) => f - t).find((d) => d >= 0 && d < len);
  const si = Math.max(0, SCENES.findIndex((s) => f >= START[s.id] && f < START[s.id] + s.durationInFrames)), sc = SCENES[si], lf = f - START[sc.id];
  const ci = sc.crops.filter(([t]) => t <= lf).length - 1, crop = sc.crops[Math.max(0, ci)];
  const shotA = crop[0], shotB = sc.crops[ci + 1]?.[0] ?? sc.durationInFrames;
  const [cx, cz, cy] = [crop[1], crop[2] ?? 1, crop[3] ?? 540];
  const CUTS = SCENES.flatMap((s) => s.crops.map(([t]) => START[s.id] + t)).filter((t) => t > 0);
  const whip = near(CUTS, 4), PUNCH = cfg.punch.map(at), pu = near(PUNCH, 10);
  const hard = SCENES[1] ? f - START[SCENES[1].id] : -9;
  const slam = hard >= 0 && hard < 6 ? interpolate(hard, [0, 6], [1.15, 1], clamp) : 1;
  const push = 1 + 0.05 * Math.min(1, (lf - shotA) / Math.max(1, shotB - shotA));
  const punch = pu === undefined ? 1 : interpolate(pu, [0, 2, 10], [1.12, 1.1, 1], clamp);
  const zoom = push * punch * slam, shake = pu === 0 ? 8 : pu === 1 ? -5 : 0;
  const wx = whip === undefined ? 0 : [-90, -40, -12, 0][whip], wb = whip === undefined ? 0 : [3, 2, 1, 0][whip];   // light blur only
  const vid = (key: string, style: React.CSSProperties, muted: boolean) => <Sequence key={key + sc.id} from={START[sc.id]} durationInFrames={sc.durationInFrames} layout="none">
    <OffthreadVideo src={staticFile(cfg.src)} muted={muted} startFrom={Math.round(sc.videoStartSec * fps)} style={style} /></Sequence>;

  // top: whole frame, scaled to TOP_H tall (1173 wide), centred; slow push
  const TS = (TOP_H / 1080) * (1 + 0.03 * (lf / sc.durationInFrames)), tw = 1920 * TS, tl = (1080 - tw) / 2, tt = (TOP_H - 1080 * TS) / 2;
  // bottom: close-up crop scaled so the source height fills BOT_H * z
  const S = (BOT_H / 1080) * cz, vw = 1920 * S, vh = 1080 * S;
  const left = Math.min(0, Math.max(1080 - vw, 540 - cx * S)), top = Math.min(0, Math.max(BOT_H - vh, BOT_H / 2 - cy * S));
  // red ring on the speaker in the top shot (head position per crop x, from cfg.ring {x: [headX, headY]})
  const rk = Object.keys(cfg.ring).map(Number).reduce((b, k) => (Math.abs(k - cx) < Math.abs(b - cx) ? k : b), 1e9);
  const head = cz >= 1 && Number.isFinite(rk) && Math.abs(rk - cx) < 160 ? cfg.ring[String(rk)] : null;
  const ringK = interpolate(f - (CUTS.filter((t) => t <= f).pop() ?? 0), [0, 8], [0, 1], clamp);

  // captions: 3-word chunks on the seam, spoken word in a yellow box
  const words = SCENES.flatMap((s) => s.words.map((w) => ({...w, s: s.id, at: START[s.id] + w.startFrame, end: START[s.id] + w.endFrame})));
  const chunks: (typeof words)[] = [];
  words.forEach((w, i) => { const c = chunks[chunks.length - 1], p = words[i - 1];
    if (!c || c.length >= 3 || p.s !== w.s || w.at - p.end > 9 || /[.?!]$/.test(p.word)) chunks.push([w]); else c.push(w); });
  const ch = chunks.filter((c) => f >= c[0].at).pop(), chEnd = ch ? (chunks[chunks.indexOf(ch) + 1]?.[0].at ?? END) : 0;
  const cur = ch ? ch.filter((w) => f >= w.at).pop() : null;
  const EMO = cfg.emoji.map(([r, e]) => ({t: at(r), e})), emo = EMO.filter((x) => f >= x.t && f < x.t + 30).pop();
  const ctaFrom = at(cfg.ctaAt);

  const FX: [string, number, number][] = [];
  const add = (file: string, t: number, v: number) => { if (t >= 0 && !FX.some(([, u]) => Math.abs(u - t) < 4)) FX.push([file, t, v]); };
  if (SCENES[1]) add('s_camflash.mp3', START[SCENES[1].id], 0.45);
  (cfg.sfx ?? []).forEach(([r, file, v]) => add(file, at(r), v));
  EMO.forEach(({t}) => add('m_ding-2.mp3', t, 0.16));
  CUTS.forEach((t) => add('m_fast-whoosh.mp3', t - 16, 0.28));
  PUNCH.forEach((t) => add('pop.mp3', t, 0.2));

  return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
    {/* top: wide shot */}
    <div style={{position: 'absolute', left: 0, top: TOP_Y, width: 1080, height: TOP_H, overflow: 'hidden'}}>
      {vid('t', {position: 'absolute', left: tl, top: tt, width: tw, height: 1080 * TS}, true)}
      {head && <div style={{position: 'absolute', left: tl + head[0] * TS - 66, top: tt + head[1] * TS - 78, width: 132, height: 156, borderRadius: '50%',
        border: '8px solid #FF2020', boxShadow: '0 0 0 3px rgba(0,0,0,0.4)', transform: `scale(${0.6 + 0.4 * ringK})`, opacity: ringK}} />}
      </div>
    <div style={{position: 'absolute', top: 0, left: 0, right: 0, height: HEAD_H, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{padding: '0 40px', textAlign: 'center', fontFamily: MONT, fontWeight: 800, fontSize: 56, lineHeight: '66px', textTransform: 'uppercase',
        color: '#fff', WebkitTextStroke: '10px #000', paintOrder: 'stroke fill', transform: `scale(${interpolate(f, [0, 5, 8], [0.7, 1.05, 1], clamp)})`}}>
        {cfg.top.split(' ').map((w, i) => <span key={i} style={{color: cfg.hl[w] ?? '#fff'}}>{w} </span>)}
      </div>
    </div>
    {/* bottom: speaker close-up */}
    <div style={{position: 'absolute', left: 0, top: BOT_Y, width: 1080, height: BOT_H, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `translateX(${wx + shake}px) scale(${zoom})`, filter: `saturate(1.08)${wb ? ` blur(${wb}px)` : ''}`}}>
        {vid('b', {position: 'absolute', left, top, width: vw, height: vh}, false)}
      </AbsoluteFill>
      {emo && (() => { const k = f - emo.t, s = interpolate(k, [0, 4, 7], [0.2, 1.2, 1], clamp), o = k > 24 ? (30 - k) / 6 : 1;
        return <Img src={staticFile(`res/emoji/${emo.e}.png`)} style={{position: 'absolute', right: 70, top: 120, width: 160, height: 160, opacity: o, transform: `scale(${s}) rotate(${6 * Math.sin(k / 4)}deg)`, filter: 'drop-shadow(0 6px 10px rgba(0,0,0,0.5))'}} />; })()}
      {f >= ctaFrom && f < ctaFrom + 80 && <div style={{position: 'absolute', bottom: 120, left: 0, right: 0, textAlign: 'center'}}>
        <span style={{fontFamily: MONT, fontWeight: 800, fontSize: 44, color: '#111', background: '#fff', borderRadius: 40, padding: '12px 30px', boxShadow: '0 6px 18px rgba(0,0,0,0.5)'}}>{cfg.cta}</span>
      </div>}
    </div>
    <div style={{position: 'absolute', left: 0, right: 0, top: BOT_Y - 4, height: 8, background: '#000'}} />
    {/* seam captions */}
    {ch && f < chEnd && <div style={{position: 'absolute', top: BOT_Y - 52, left: 30, right: 30, textAlign: 'center'}}>
      {ch.map((w, i) => { const on = cur === w, said = f >= w.at;
        return <span key={i} style={{display: 'inline-block', margin: '0 8px', padding: '0 14px', borderRadius: 14, background: on ? '#FFE11A' : 'transparent',
          fontFamily: MONT, fontWeight: 800, fontSize: 74, lineHeight: '104px', textTransform: 'uppercase', color: on ? '#111' : '#fff', opacity: said ? 1 : 0,
          WebkitTextStroke: on ? '0px' : '9px #000', paintOrder: 'stroke fill', transform: `rotate(${on ? -2 : 0}deg)`}}>{w.word.replace(/[.,!]+$/, '')}</span>; })}
    </div>}

    <Audio src={staticFile(`res/${cfg.music[0]}.mp3`)} startFrom={Math.round(cfg.music[1] * fps)} volume={cfg.musicVol ?? 0.45} loop />
    {FX.map(([file, t, v], i) => <Sequence key={i} from={t}><Audio src={staticFile(`res/${file}`)} volume={v} /></Sequence>)}
  </AbsoluteFill>;
};

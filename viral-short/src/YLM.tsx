// YoungLA runway montages (Nov 21, user brief): base cuts pre-built with ffmpeg (build_ylm.py: 9:16 crops, slow-mo, freeze-frames)
// = public/ylm/<id>.mp4; this comp adds the hook, callouts, word-pop captions, end question, whooshes, meme SFX and low music
// (ylm.cfg.json). No ad text, no tags.
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import CFG from './ylm.cfg.json';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const F = (s: number) => Math.round(s * 30);
type T = {from: number; to: number; lines: string[]; y: number; size: number; emoji?: string; box?: boolean; hl?: string[]; rot?: number};
type W = {w: string; s: number; e?: number; emoji?: string; hl?: boolean};
type C = {base: string; dur: number; baseVol: number; music: [string, number, number]; cuts: number[]; freezes: {a: number; b: number; z: number; flash?: boolean}[];
  texts: T[]; words: W[]; sfx: [string, number, number][]};
export const YLMS = CFG as unknown as Record<string, C>;
export const ylmFrames = (id: string) => F(YLMS[id].dur);
const stroke = (w: number): React.CSSProperties => ({WebkitTextStroke: `${w}px #000`, paintOrder: 'stroke fill', textShadow: '0 6px 16px rgba(0,0,0,0.6)'});

export const YLM: React.FC<{edit: string}> = ({edit}) => {
  const c = YLMS[edit], f = useCurrentFrame(), {fps} = useVideoConfig(), t = f / fps;
  const cutD = c.cuts.map((x) => f - F(x)).filter((d) => d >= 0 && d < 5).pop();
  const whip = cutD === undefined ? 0 : [-90, -40, -12, -3, 0][cutD];
  const fz = c.freezes.find((x) => t >= x.a && t < x.b);
  const zoom = fz ? interpolate(t, [fz.a, fz.a + 0.15], [1, fz.z], clamp) : 1;
  let wi = -1; c.words.forEach((w, i) => { if (t >= w.s) wi = i; }); const wd = wi >= 0 ? c.words[wi] : undefined;
  const wEnd = wd ? (wd.e ?? c.words[wi + 1]?.s ?? 99) : 0, wOn = wd && t < wEnd;
  const wp = wd ? spring({frame: f - F(wd.s), fps, config: {damping: 9, stiffness: 320}}) : 1;
  return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
    <AbsoluteFill style={{transform: `translateX(${whip}px) scale(${zoom})`, filter: cutD !== undefined && cutD < 3 ? `blur(${[6, 3, 1][cutD]}px)` : undefined}}>
      <OffthreadVideo src={staticFile(c.base)} volume={c.baseVol} style={{width: 1080, height: 1920}} />
    </AbsoluteFill>
    {fz?.flash && <AbsoluteFill style={{background: '#fff', opacity: interpolate(t, [fz.a, fz.a + 0.1], [0.6, 0], clamp)}} />}
    {c.texts.filter((x) => t >= x.from && t < x.to).map((x, i) => { const k = spring({frame: f - F(x.from), fps, config: {damping: 11, stiffness: 240}});
      return <div key={i} style={{position: 'absolute', top: x.y, left: 40, right: 40, display: 'flex', justifyContent: 'center', transform: `scale(${0.6 + 0.4 * k}) rotate(${x.rot ?? 0}deg)`}}>
        <div style={{textAlign: 'center', ...(x.box ? {background: '#fff', borderRadius: 22, padding: '14px 28px', boxShadow: '0 10px 28px rgba(0,0,0,0.5)'} : {})}}>
          {x.lines.map((l, j) => <div key={j} style={{fontFamily: MONT, fontWeight: 800, fontSize: x.size, lineHeight: 1.15, color: x.box ? '#111' : '#FFE14D', ...(x.box ? {} : stroke(14))}}>
            {l.split(' ').map((w, m) => <span key={m} style={{color: x.hl?.includes(w) ? '#E3201B' : undefined}}>{w} </span>)}
            {j === x.lines.length - 1 && x.emoji && <Img src={staticFile(`res/emoji/${x.emoji}.png`)} style={{width: x.size * 1.05, height: x.size * 1.05, verticalAlign: 'middle'}} />}</div>)}
        </div></div>; })}
    {wOn && <div style={{position: 'absolute', top: 1400, left: 30, right: 30, textAlign: 'center', transform: `scale(${0.7 + 0.3 * wp})`}}>
      <span style={{fontFamily: MONT, fontWeight: 800, fontSize: wd!.w.length > 14 ? 80 : 104, lineHeight: 1.1, color: wd!.hl ? '#FFE14D' : '#fff', ...stroke(16)}}>{wd!.w}</span>
      {wd!.emoji && <Img src={staticFile(`res/emoji/${wd!.emoji}.png`)} style={{width: 100, height: 100, verticalAlign: 'middle', marginLeft: 12}} />}
    </div>}
    <Audio src={staticFile(`res/${c.music[0]}.mp3`)} startFrom={F(c.music[1])} volume={c.music[2]} />
    {c.cuts.map((x, i) => <Sequence key={'c' + i} from={Math.max(0, F(x) - 14)}><Audio src={staticFile('res/m_fast-whoosh.mp3')} volume={0.25} /></Sequence>)}
    {c.sfx.map(([s, at, v], i) => <Sequence key={'s' + i} from={F(at)}><Audio src={staticFile(`res/${s}.mp3`)} volume={v} /></Sequence>)}
  </AbsoluteFill>;
};

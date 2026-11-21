// YoungLA runway montage (Nov 21, user brief): base cut pre-built with ffmpeg (9:16 crops, slow-mo, freeze-frames) = public/ylm/base.mp4;
// this comp only adds the hook, freeze callouts, word-pop captions, end question, whooshes, record scratch and low music. No ad text, no tags.
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const F = (s: number) => Math.round(s * 30);
export const YLM_FRAMES = F(21.3);
const CUTS = [4.967, 8.8, 11.8, 16.1];
type T = {from: number; to: number; lines: string[]; y: number; size: number; emoji?: string; box?: boolean; hl?: string[]; rot?: number};
const TEXTS: T[] = [
  {from: 0, to: 4.967, lines: ['Bodybuilders were NOT', 'made for the runway'], y: 210, size: 64, emoji: '1f480', box: true, hl: ['NOT']},
  {from: 4.267, to: 4.967, lines: ['THE POSE'], y: 1300, size: 120, emoji: '1f62d', rot: -4},
  {from: 8.8, to: 10.9, lines: ["Jay Cutler's runway walk"], y: 210, size: 60, emoji: '1f410', box: true},
  {from: 15.5, to: 16.1, lines: ['RUNWAY READY?'], y: 1300, size: 104, emoji: '1f4aa', rot: 4},
  {from: 17.8, to: 21.3, lines: ['GYM BROS vs MODELS', 'who won?'], y: 230, size: 70, emoji: '1f914', box: true, hl: ['who', 'won?']},
];
const WORDS = [{w: 'INSANE', s: 5.07}, {w: 'WOW', s: 5.61}, {w: 'OH', s: 6.81}, {w: 'OH OH', s: 7.25}, {w: 'OH OH OH', s: 7.9}];
const stroke = (w: number): React.CSSProperties => ({WebkitTextStroke: `${w}px #000`, paintOrder: 'stroke fill', textShadow: '0 6px 16px rgba(0,0,0,0.6)'});

export const YLM: React.FC = () => {
  const f = useCurrentFrame(), {fps} = useVideoConfig(), t = f / fps;
  const cutD = CUTS.map((c) => f - F(c)).filter((d) => d >= 0 && d < 5).pop();
  const whip = cutD === undefined ? 0 : [-90, -40, -12, -3, 0][cutD];
  const fz1 = t >= 4.267 && t < 4.967, fz2 = t >= 15.5 && t < 16.1, fz3 = t >= 20.1;
  const zoom = fz1 ? interpolate(t, [4.267, 4.4], [1, 1.12], clamp) : fz2 ? interpolate(t, [15.5, 15.63], [1, 1.12], clamp) : fz3 ? interpolate(t, [20.1, 20.3], [1, 1.08], clamp) : 1;
  const wd = WORDS.filter((w) => t >= w.s).pop(), wOn = wd && t < 8.8;
  const wp = wd ? spring({frame: f - F(wd.s), fps, config: {damping: 9, stiffness: 320}}) : 1;
  return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
    <AbsoluteFill style={{transform: `translateX(${whip}px) scale(${zoom})`, filter: cutD !== undefined && cutD < 3 ? `blur(${[6, 3, 1][cutD]}px)` : undefined}}>
      <OffthreadVideo src={staticFile('ylm/base.mp4')} style={{width: 1080, height: 1920}} />
    </AbsoluteFill>
    {(fz1 || fz2) && <AbsoluteFill style={{background: '#fff', opacity: interpolate(t, [fz1 ? 4.267 : 15.5, (fz1 ? 4.267 : 15.5) + 0.1], [0.6, 0], clamp)}} />}
    {TEXTS.filter((x) => t >= x.from && t < x.to).map((x, i) => { const k = spring({frame: f - F(x.from), fps, config: {damping: 11, stiffness: 240}});
      return <div key={i} style={{position: 'absolute', top: x.y, left: 40, right: 40, display: 'flex', justifyContent: 'center', transform: `scale(${0.6 + 0.4 * k}) rotate(${x.rot ?? 0}deg)`}}>
        <div style={{textAlign: 'center', ...(x.box ? {background: '#fff', borderRadius: 22, padding: '14px 28px', boxShadow: '0 10px 28px rgba(0,0,0,0.5)'} : {})}}>
          {x.lines.map((l, j) => <div key={j} style={{fontFamily: MONT, fontWeight: 800, fontSize: x.size, lineHeight: 1.15, color: x.box ? '#111' : '#FFE14D', ...(x.box ? {} : stroke(14))}}>
            {l.split(' ').map((w, m) => <span key={m} style={{color: x.hl?.includes(w) ? '#E3201B' : undefined}}>{w} </span>)}
            {j === x.lines.length - 1 && x.emoji && <Img src={staticFile(`res/emoji/${x.emoji}.png`)} style={{width: x.size * 1.05, height: x.size * 1.05, verticalAlign: 'middle'}} />}</div>)}
        </div></div>; })}
    {wOn && <div style={{position: 'absolute', top: 1400, left: 0, right: 0, textAlign: 'center', transform: `scale(${0.7 + 0.3 * wp})`}}>
      <span style={{fontFamily: MONT, fontWeight: 800, fontSize: 104, color: '#fff', ...stroke(16)}}>{wd!.w}</span>
      {wd!.w.startsWith('OH') && <Img src={staticFile('res/emoji/1f602.png')} style={{width: 110, height: 110, verticalAlign: 'middle', marginLeft: 12}} />}
    </div>}
    <Audio src={staticFile('res/funkabn_n.mp3')} startFrom={F(2)} volume={0.12} />
    {CUTS.map((c, i) => <Sequence key={i} from={Math.max(0, F(c) - 14)}><Audio src={staticFile('res/m_fast-whoosh.mp3')} volume={0.25} /></Sequence>)}
    <Sequence from={F(4.267)}><Audio src={staticFile('res/m_record-scratch.mp3')} volume={0.3} /></Sequence>
    <Sequence from={F(15.5)}><Audio src={staticFile('res/m_record-scratch.mp3')} volume={0.25} /></Sequence>
    <Sequence from={F(17.8)}><Audio src={staticFile('res/m_ding-2.mp3')} volume={0.2} /></Sequence>
  </AbsoluteFill>;
};

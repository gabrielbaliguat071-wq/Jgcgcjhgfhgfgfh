// Metaphor: ReFantazio word-by-word edits (Nov 21) — style copied from the user's reference TikTok: full-bleed trailer footage,
// ONE spaced-out serif word at a time in the centre synced to the spoken line (sentence-final words bigger), punch-in on cuts,
// white flash into the finale. Hook label on top for the first seconds (brief: text in the first second). cfg = mrw.cfg.json.
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, OffthreadVideo, Sequence, Audio, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import CFG from './mrw.cfg.json';

loadFont({family: 'Cinzel', url: staticFile('res/Cinzel-Bold.woff2'), weight: '700'});
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
type W = {w: string; s: number; e: number; big: boolean};
type C = {base: string; dur: number; cuts: number[]; flash: number; top: string[]; end: string; words: W[]};
export const MRWS = CFG as unknown as Record<string, C>;
export const mrwFrames = (id: string) => Math.round(MRWS[id].dur * 30);
const glow = '0 0 18px rgba(0,0,0,0.85), 0 0 40px rgba(0,0,0,0.6), 0 4px 10px rgba(0,0,0,0.9)';

export const MRW: React.FC<{edit: string}> = ({edit}) => {
  const c = MRWS[edit], f = useCurrentFrame(), {fps} = useVideoConfig(), t = f / fps;
  const cutD = c.cuts.map((x) => f - Math.round(x * fps)).filter((d) => d >= 0 && d < 6).pop();
  const zoom = cutD === undefined ? 1 + 0.03 * ((t % 4) / 4) : [1.09, 1.06, 1.035, 1.015, 1.005, 1][cutD];
  const wd = c.words.find((w) => t >= w.s && t < w.e);
  const wk = wd ? interpolate(t - wd.s, [0, 0.12], [0, 1], clamp) : 0;
  const fl = t >= c.flash - 0.1 ? interpolate(t, [c.flash - 0.1, c.flash, c.flash + 0.35], [0, 1, 0], clamp) : 0;
  const label = (lines: string[], o: number) => <div style={{position: 'absolute', top: 210, left: 30, right: 30, textAlign: 'center', opacity: o}}>
    {lines.map((l, i) => <div key={i} style={{fontFamily: 'Cinzel', fontWeight: 700, fontSize: 50, letterSpacing: 8, color: i === lines.length - 1 ? '#FFE9A8' : '#fff', textShadow: glow, lineHeight: 1.25}}>{l}</div>)}</div>;
  return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
    <AbsoluteFill style={{transform: `scale(${zoom})`}}><OffthreadVideo src={staticFile(c.base)} style={{width: 1080, height: 1920}} /></AbsoluteFill>
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(0,0,0,0.35) 0%, rgba(0,0,0,0) 45%, rgba(0,0,0,0.45) 100%)'}} />
    {t < 2.8 && label(c.top, interpolate(t, [2.4, 2.8], [1, 0], clamp))}
    {t >= c.flash && label([c.end], interpolate(t, [c.flash, c.flash + 0.4], [0, 1], clamp))}
    {wd && <div style={{position: 'absolute', top: 0, bottom: 0, left: 20, right: 20, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <span style={{fontFamily: 'Cinzel', fontWeight: 700, fontSize: (wd.big ? 150 : 96) * (wd.w.length > 9 ? 0.75 : 1), letterSpacing: wd.big ? 14 : 18, color: '#fff',
        textShadow: glow, opacity: wk, transform: `scale(${1.12 - 0.12 * wk})`, whiteSpace: 'nowrap'}}>{wd.w}</span></div>}
    {fl > 0 && <AbsoluteFill style={{background: '#fff', opacity: fl}} />}
    {c.cuts.map((x, i) => <Sequence key={i} from={Math.max(0, Math.round(x * fps) - 12)}><Audio src={staticFile('res/m_fast-whoosh.mp3')} volume={0.08} /></Sequence>)}
  </AbsoluteFill>;
};

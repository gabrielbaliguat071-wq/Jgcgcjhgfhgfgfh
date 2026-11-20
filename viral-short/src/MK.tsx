// Meta-Klage (German, Nov 20): full official video UNCUT (brief), German word captions (1-2 words, key words red/green),
// hook box for the first seconds (factual question, no money claims), meta-klage logo overlay whole clip, quiet background music.
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import CFG from './mk.cfg.json';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
type W = {w: string; s: number; e: number};
type C = {src: string; dur: number; hook: string[]; hookEmoji: string; hookUntil: number; words: W[]; kw: Record<string, string>; music: [string, number]; capY?: number};
export const MKC = CFG as unknown as Record<string, C>;
export const mkFrames = (id: string) => Math.round(MKC[id].dur * 30);
const stroke = (w: number): React.CSSProperties => ({WebkitTextStroke: `${w}px #000`, paintOrder: 'stroke fill', textShadow: '0 6px 14px rgba(0,0,0,0.5)'});

export const MK: React.FC<{edit: string}> = ({edit}) => {
  const c = MKC[edit], f = useCurrentFrame(), {fps} = useVideoConfig(), t = f / fps;
  const chunks: W[][] = [];
  c.words.forEach((w, i) => { const k = chunks[chunks.length - 1], p = c.words[i - 1];
    if (!k || k.length >= 2 || w.s - p.e > 0.35 || /[.?!,]$/.test(p.w)) chunks.push([w]); else k.push(w); });
  const ch = chunks.filter((k) => t >= k[0].s).pop(), nx = ch ? chunks[chunks.indexOf(ch) + 1] : undefined;
  const show = ch && t < Math.min(nx ? nx[0].s : 999, ch[ch.length - 1].e + 0.5);
  const pop = ch ? spring({frame: f - Math.round(ch[0].s * fps), fps, config: {damping: 11, stiffness: 260}}) : 1;
  const hk = spring({frame: f, fps, config: {damping: 12, stiffness: 220}}), hookOn = t < c.hookUntil;
  return <AbsoluteFill style={{background: '#000'}}>
    <OffthreadVideo src={staticFile(c.src)} style={{width: 1080, height: 1920}} />
    {hookOn && <div style={{position: 'absolute', top: 170, left: 0, right: 0, display: 'flex', justifyContent: 'center', transform: `scale(${0.7 + 0.3 * hk})`,
      opacity: interpolate(t, [c.hookUntil - 0.25, c.hookUntil], [1, 0], clamp)}}>
      <div style={{background: '#fff', borderRadius: 22, padding: '16px 34px', boxShadow: '0 10px 30px rgba(0,0,0,0.35)', textAlign: 'center'}}>
        {c.hook.map((l, i) => <div key={i} style={{fontFamily: MONT, fontWeight: 800, fontSize: 66, lineHeight: '80px', color: i === 0 ? '#111' : '#3B82F6'}}>{l}
          {i === c.hook.length - 1 && <Img src={staticFile(`res/emoji/${c.hookEmoji}.png`)} style={{width: 68, height: 68, verticalAlign: 'middle', marginLeft: 10}} />}</div>)}
      </div></div>}
    {show && (() => { const n = ch!.reduce((a, w) => a + w.w.length, 0) + ch!.length; const fs = Math.min(84, Math.floor(1500 / n)); return <div style={{position: 'absolute', top: c.capY ?? 1180, left: 30, right: 30, textAlign: 'center', transform: `scale(${0.8 + 0.2 * pop})`}}>
      {ch!.map((w, i) => { const col = c.kw[w.w.toLowerCase()] ?? c.kw[w.w.toLowerCase().replace(/[.,?!]+$/, '')] ?? '#fff';
        return <span key={i} style={{display: 'inline-block', margin: '0 12px', fontFamily: MONT, fontWeight: 800, fontSize: fs, lineHeight: '100px', textTransform: 'uppercase', color: col, opacity: t >= w.s ? 1 : 0, ...stroke(12)}}>{w.w.replace(/[,.]+$/, '')}</span>; })}
    </div>; })()}
    {/* REQUIRED: Meta-Klage logo overlay */}
    <div style={{position: 'absolute', top: 1480, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><div style={{background: 'rgba(10,14,30,0.78)', borderRadius: 18, padding: '14px 26px'}}><Img src={staticFile('mk/logo.png')} style={{width: 560, display: 'block'}} /></div></div>
    <Audio src={staticFile(`res/${c.music[0]}.mp3`)} startFrom={Math.round(c.music[1] * fps)} volume={0.08} />
  </AbsoluteFill>;
};

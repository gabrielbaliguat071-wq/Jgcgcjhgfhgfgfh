// CONCESSIONS movie clips (ClipHouse, Nov 20). Brief: NEVER alter the movie (no crop/zoom/filters/speed), text never on faces/action,
// no added music, spoiler-free, positive. Layout = full 16:9 frame untouched in the middle, hook above, captions below,
// official title card + "@concessionsmovie · link in bio" CTA at the bottom (text only in the black space).
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import CFG from './con.cfg.json';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
type W = {w: string; s: number; e: number};
type C = {src: string; dur: number; hook: string[]; hookEmoji: string; hl: string[]; kw: Record<string, string>; words: W[]};
export const CON = CFG as unknown as Record<string, C>;
export const conFrames = (id: string) => Math.round(CON[id].dur * 30);
const VT = 656, VH = 608;   // 1920x1080 scaled to 1080 wide, centred
const stroke = (w: number): React.CSSProperties => ({WebkitTextStroke: `${w}px #000`, paintOrder: 'stroke fill'});

export const Con: React.FC<{edit: string}> = ({edit}) => {
  const c = CON[edit], f = useCurrentFrame(), {fps} = useVideoConfig(), t = f / fps;
  const chunks: W[][] = [];
  c.words.forEach((w, i) => { const k = chunks[chunks.length - 1], p = c.words[i - 1];
    if (!k || k.length >= 3 || w.s - p.e > 0.4 || /[.?!,]$/.test(p.w)) chunks.push([w]); else k.push(w); });
  const ch = chunks.filter((k) => t >= k[0].s).pop(), nx = ch ? chunks[chunks.indexOf(ch) + 1] : undefined;
  const show = ch && t < Math.min(nx ? nx[0].s : 999, ch[ch.length - 1].e + 0.7);
  const pop = ch ? spring({frame: f - Math.round(ch[0].s * fps), fps, config: {damping: 12, stiffness: 230}}) : 1;
  const hk = interpolate(f, [0, 6, 9], [0.7, 1.05, 1], clamp);
  return <AbsoluteFill style={{background: '#000'}}>
    <OffthreadVideo src={staticFile(c.src)} style={{position: 'absolute', left: 0, top: VT, width: 1080, height: VH}} />
    <div style={{position: 'absolute', top: 330, left: 50, right: 50, textAlign: 'center', transform: `scale(${hk})`}}>
      {c.hook.map((l, i) => <div key={i} style={{fontFamily: MONT, fontWeight: 800, fontSize: 52, lineHeight: '70px', color: '#fff', whiteSpace: 'nowrap'}}>
        {l.split(' ').map((w, j) => <span key={j} style={{color: c.hl.includes(w) ? '#FFE14D' : '#fff'}}>{w} </span>)}
        {i === c.hook.length - 1 && <Img src={staticFile(`res/emoji/${c.hookEmoji}.png`)} style={{width: 64, height: 64, verticalAlign: 'middle'}} />}</div>)}
    </div>
    {show && <div style={{position: 'absolute', top: VT + VH + 50, left: 30, right: 30, textAlign: 'center', transform: `scale(${0.85 + 0.15 * pop})`}}>
      {ch!.map((w, i) => { const col = c.kw[w.w.toLowerCase()] ?? '#fff';
        return <span key={i} style={{display: 'inline-block', margin: '0 12px', fontFamily: MONT, fontWeight: 800, fontSize: 70, lineHeight: '84px', textTransform: 'uppercase', color: col, opacity: t >= w.s ? 1 : 0, ...stroke(10)}}>{w.w.replace(/[.,]+$/, '')}</span>; })}
    </div>}
    <Img src={staticFile('con/con_tt.png')} style={{position: 'absolute', top: 1560, left: 140, width: 800}} />
    <div style={{position: 'absolute', top: 1735, left: 0, right: 0, textAlign: 'center', fontFamily: MONT, fontWeight: 800, fontSize: 40, color: '#fff'}}>
      watch it → <span style={{color: '#FFE14D'}}>@concessionsmovie</span> · link in bio</div>
  </AbsoluteFill>;
};

// Backyard Breaks card pulls, "normal edit" (Nov 19, no narration): vertical stream clips (hosts cam top, stream bar, card cam).
// White hook banner over the stream bar, card cam blurred in the hook (no spoiler), whip + whoosh on every cut, glow captions
// (3 words, swears starred), reveal = white flash + shake + punch-in on the card + PLAYER / CARD / $PRICE stack + cha-ching,
// engagement question at the end. Music low under the real reactions.
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import CFG from './pull.cfg.json';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
type W = {w: string; s: number; e: number};
type Sc = {a: number; b: number; zoom?: [number, number, number]; words: W[]; blur?: boolean};
type P = {src: string; srcW: number; top: string[]; hl: Record<string, string>; scenes: Sc[]; reveal: {at: number; name: string; card: string; price: string; cx: number; cy: number; ty?: number};
  question: string; qAt: number; tEmoji: string; qEmoji: string; bannerY?: number; capY?: number; music: [string, number]; kw: Record<string, string>; emoji: {at: number; e: string}[]; cardY: number};
export const PULL = CFG as unknown as Record<string, P>;
const F = (s: number) => Math.round(s * 30);
export const pullFrames = (id: string) => PULL[id].scenes.reduce((a, s) => a + F(s.b - s.a), 0);
const glow = (c: string) => `0 0 10px ${c}aa, 0 0 22px ${c}66, 0 3px 8px #000, 0 0 3px #000`;

export const Pull: React.FC<{edit: string}> = ({edit}) => {
  const p = PULL[edit], f = useCurrentFrame(), {fps} = useVideoConfig(), END = pullFrames(edit);
  const st: number[] = []; p.scenes.reduce((a, s) => { st.push(a); return a + F(s.b - s.a); }, 0);
  const si = st.filter((s) => s <= f).length - 1, sc = p.scenes[si], lf = f - st[si];
  const tSrc = sc.a + lf / fps, k = p.srcW ? 1080 / p.srcW : 1;
  // timeline-time of the reveal (first scene containing it, not the hook)
  const rIdx = p.scenes.findIndex((s, i) => i > 0 && p.reveal.at >= s.a && p.reveal.at < s.b);
  const R = rIdx >= 0 ? st[rIdx] + F(p.reveal.at - p.scenes[rIdx].a) : -999, rd = f - R;
  const whip = lf < 5 && f > 0 ? [-130, -60, -22, -6, 0][lf] : 0;
  const rz = rd >= 0 ? (rd < 3 ? 1.45 : interpolate(rd, [3, 14, 60], [1.4, 1.22, 1.15], clamp)) : 1;
  const z = (sc.zoom ? interpolate(lf, [0, F(sc.b - sc.a)], [sc.zoom[0], sc.zoom[0] * 1.05], clamp) : 1.0) * (rd >= 0 && rd < 90 ? rz : 1) * interpolate(lf, [0, 4], [1.08, 1], clamp);
  const ox = rd >= 0 && rd < 90 ? p.reveal.cx : sc.zoom?.[1] ?? 540, oy = rd >= 0 && rd < 90 ? p.reveal.cy : sc.zoom?.[2] ?? 1000;
  const shake = rd >= 0 && rd < 16 ? Math.sin(rd * 2.4) * (16 - rd) * 1.6 : 0;
  // captions
  const words = p.scenes.flatMap((s, i) => s.words.map((w) => ({...w, at: st[i] + F(w.s - s.a), end: st[i] + F(w.e - s.a), si: i})));
  const chunks: (typeof words)[] = [];
  words.forEach((w, i) => { const c = chunks[chunks.length - 1], q = words[i - 1];
    if (!c || c.length >= 3 || q.si !== w.si || w.at - q.end > 10 || /[.?!,]$/.test(q.w)) chunks.push([w]); else c.push(w); });
  const ch = chunks.filter((c) => f >= c[0].at).pop(), nx = ch ? chunks[chunks.indexOf(ch) + 1] : undefined;
  const capOn = ch && f < Math.min(nx ? nx[0].at : END, ch[ch.length - 1].end + 18) && !(rd >= 0 && rd < 75);
  const cp = ch ? spring({frame: f - ch[0].at, fps, config: {damping: 12, stiffness: 230}}) : 1;
  const tk = (d: number) => spring({frame: rd - d, fps, config: {damping: 10, stiffness: 220}});
  const emo = p.emoji.map((e) => ({...e, t: F(e.at)})).filter((e) => f >= e.t && f < e.t + 30).pop();
  const Q = F(p.qAt);
  const FX: [string, number, number][] = [];
  st.slice(1).forEach((s) => FX.push(['m_fast-whoosh.mp3', s - 16, 0.25]));
  if (R > 0) FX.push(['s_camflash.mp3', R, 0.4], ['m_cha-ching.mp3', R + 14, 0.32], ['m_crowd-cheer.mp3', R, 0.15]);
  p.emoji.forEach((e) => FX.push(['m_ding-2.mp3', F(e.at), 0.14]));
  FX.push(['m_ding-2.mp3', Q, 0.2]);
  return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
    <AbsoluteFill style={{transform: `translate(${whip + shake}px, ${shake * 0.6}px) scale(${z})`, transformOrigin: `${ox}px ${oy}px`, filter: whip ? `blur(${Math.abs(whip) / 25}px)` : undefined}}>
      {p.scenes.map((s, i) => <Sequence key={i} from={st[i]} durationInFrames={F(s.b - s.a)} layout="none">
        <OffthreadVideo src={staticFile(p.src)} startFrom={F(s.a)} volume={1} style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920}} />
        {s.blur && <div style={{position: 'absolute', left: 0, right: 0, top: p.cardY, bottom: 0, backdropFilter: 'blur(38px)', WebkitBackdropFilter: 'blur(38px)', background: 'rgba(0,0,0,0.15)'}} />}
      </Sequence>)}
    </AbsoluteFill>
    {sc.blur && <div style={{position: 'absolute', top: p.cardY + 380, left: 0, right: 0, textAlign: 'center', fontSize: 190, filter: 'drop-shadow(0 8px 14px #000)'}}>
      <Img src={staticFile('res/emoji/2753.png')} style={{width: 200, height: 200, transform: `scale(${1 + 0.08 * Math.sin(f / 4)})`}} /></div>}
    {rd >= 0 && rd < 3 && <AbsoluteFill style={{background: '#fff', opacity: [1, 0.7, 0.3][rd]}} />}
    {/* hook banner over the stream bar */}
    <div style={{position: 'absolute', top: p.bannerY ?? 500, left: 40, right: 40, display: 'flex', justifyContent: 'center', transform: `scale(${interpolate(f, [0, 6, 9], [0.6, 1.05, 1], clamp)})`}}>
      <div style={{background: '#fff', borderRadius: 18, padding: '14px 26px', boxShadow: '0 8px 26px rgba(0,0,0,0.6)', fontFamily: MONT, fontWeight: 800, fontSize: 52, lineHeight: '60px', color: '#111', textAlign: 'center', textTransform: 'uppercase'}}>
        {p.top.map((l, i) => <div key={i}>{l.split(' ').map((w, j) => <span key={j} style={{color: p.hl[w] ?? '#111'}}>{w} </span>)}{i === p.top.length - 1 && <Img src={staticFile(`res/emoji/${p.tEmoji}.png`)} style={{width: 56, height: 56, verticalAlign: 'middle'}} />}</div>)}
      </div>
    </div>
    {emo && (() => { const d = f - emo.t, s = interpolate(d, [0, 4, 7], [0.2, 1.2, 1], clamp);
      return <Img src={staticFile(`res/emoji/${emo.e}.png`)} style={{position: 'absolute', left: 465, top: 1440, width: 150, height: 150, transform: `scale(${s}) rotate(${6 * Math.sin(d / 4)}deg)`, opacity: d > 24 ? (30 - d) / 6 : 1}} />; })()}
    {capOn && <div style={{position: 'absolute', top: p.capY ?? 1600, left: 30, right: 30, textAlign: 'center', transform: `scale(${0.8 + 0.2 * cp})`}}>
      {ch!.map((w, i) => { const key = w.w.toLowerCase().replace(/[^a-z0-9$-]/g, ''), col = p.kw[key] ?? '#FFFFFF';
        return <span key={i} style={{display: 'inline-block', margin: '0 14px', fontFamily: MONT, fontWeight: 800, fontSize: 80, lineHeight: '94px', textTransform: 'uppercase', color: col,
          textShadow: glow(col === '#FFFFFF' ? '#ffffff' : col), opacity: f >= w.at ? 1 : 0}}>{w.w.replace(/[.,!]+$/, '')}</span>; })}
    </div>}
    {rd >= 2 && rd < 105 && <div style={{position: 'absolute', top: p.reveal.ty ?? 1360, left: 0, right: 0, textAlign: 'center'}}>
      {[[p.reveal.name, '#fff', 92, 4], [p.reveal.card, '#FF3B3B', 64, 12], [p.reveal.price, '#5CFF5C', 104, 20]].map(([t, c, s, d], i) =>
        <div key={i} style={{fontFamily: MONT, fontWeight: 800, fontSize: s as number, lineHeight: 1.1, color: c as string, WebkitTextStroke: '12px #000', paintOrder: 'stroke fill', textShadow: '0 8px 18px rgba(0,0,0,0.7)',
          transform: `scale(${tk(d as number)}) rotate(-2deg)`}}>{t}</div>)}
    </div>}
    {f >= Q && <div style={{position: 'absolute', top: 1440, left: 40, right: 40, textAlign: 'center', transform: `scale(${spring({frame: f - Q, fps, config: {damping: 11, stiffness: 220}})})`}}>
      <span style={{fontFamily: MONT, fontWeight: 800, fontSize: 54, color: '#111', background: '#FFE14D', borderRadius: 16, padding: '10px 22px', boxShadow: '0 6px 18px rgba(0,0,0,0.5)'}}>{p.question} <Img src={staticFile(`res/emoji/${p.qEmoji}.png`)} style={{width: 54, height: 54, verticalAlign: 'middle'}} /></span>
    </div>}
    <Audio src={staticFile(`res/${p.music[0]}.mp3`)} startFrom={F(p.music[1])} volume={0.1} />
    {FX.filter(([, t]) => t >= 0).map(([file, t, v], i) => <Sequence key={i} from={t}><Audio src={staticFile(`res/${file}`)} volume={v} /></Sequence>)}
  </AbsoluteFill>;
};

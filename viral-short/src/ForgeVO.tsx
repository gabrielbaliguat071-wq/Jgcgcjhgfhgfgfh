// BloxClips x ForgeGUI MCP — narrated funny edits (Nov 19): one VO line per shot (dev telling the story of prompting his game),
// big 1-3 word captions, punch-in on ALL-CAPS/key words, dev-facing hook box on top, REQUIRED "made w/ claude + forgegui mcp" pill.
// Campaign footage (phone filming the monitor) zoomed onto the screen (cy/sh = detected screen centre/height). Campaign music under VO.
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import CFG from './forgevo.cfg.json';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
type W = {w: string; s: number; e: number};
type Shot = {src: string; from: number; dur: number; cy: number; sh: number; words: W[]; line?: string};
type V = {hook: string; hookEmoji: string; end: string; endEmoji: string; music: [string, number]; vo: string; shots: Shot[]};
export const FVO = CFG as unknown as Record<string, V>;
const F = (s: number) => Math.round(s * 30);
export const fvoFrames = (id: string) => FVO[id].shots.reduce((a, s) => a + F(s.dur), 0);
const stroke = (w: number): React.CSSProperties => ({WebkitTextStroke: `${w}px #000`, paintOrder: 'stroke fill'});
const KEY = /^(not|teeth|one|cows?|twelve|12|titans?|explosions|three|five|prompt|claude|forgegui|got|fish|ufo|studio|room|house|circles)\b/i;

export const ForgeVO: React.FC<{edit: string}> = ({edit}) => {
  const cfg = FVO[edit], f = useCurrentFrame(), {fps} = useVideoConfig(), END = fvoFrames(edit), t = f / fps;
  const starts: number[] = []; cfg.shots.reduce((a, s) => { starts.push(a); return a + F(s.dur); }, 0);
  const si = starts.filter((s) => s <= f).length - 1, sh = cfg.shots[si], lf = f - starts[si], n = F(sh.dur);
  const words = cfg.shots.flatMap((s) => s.words);
  const chunks: W[][] = [];
  words.forEach((w, i) => { const c = chunks[chunks.length - 1], p = words[i - 1];
    if (!c || c.length >= 3 || w.s - p.e > 0.35 || /[.?!,]$/.test(p.w)) chunks.push([w]); else c.push(w); });
  const ch = chunks.filter((c) => t >= c[0].s).pop(), nx = ch ? chunks[chunks.indexOf(ch) + 1] : undefined;
  const show = ch && t < Math.min(nx ? nx[0].s : 99, ch[ch.length - 1].e + 0.6);
  const pop = ch ? spring({frame: f - F(ch[0].s), fps, config: {damping: 11, stiffness: 240}}) : 1;
  const hits = words.filter((w) => KEY.test(w.w) || (w.w.replace(/[^A-Za-z]/g, '').length > 1 && w.w === w.w.toUpperCase() && /[A-Z]/.test(w.w))).map((w) => F(w.s));
  const hd = hits.map((h) => f - h).filter((d) => d >= 0 && d < 8).pop();
  const punch = hd === undefined ? 1 : interpolate(hd, [0, 2, 8], [1.1, 1.08, 1], clamp);
  const zoom = Math.min(1.75, Math.max(1.3, 1350 / Math.max(500, sh.sh))) * punch * (1 + 0.05 * lf / n) * interpolate(lf, [0, 4], [1.08, 1], clamp);
  const whip = lf < 4 && f > 0 ? [-80, -36, -10, 0][lf] : 0, shake = hd !== undefined && hd < 6 ? Math.sin(hd * 2.5) * 9 : 0;
  const endAt = END - F(1.5), endK = spring({frame: f - endAt, fps, config: {damping: 11, stiffness: 220}});
  return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
    <AbsoluteFill style={{transform: `translate(${whip + shake}px, ${shake * 0.5}px) scale(${zoom})`, transformOrigin: "540px 960px", filter: whip ? `blur(${Math.abs(whip) / 30}px)` : undefined}}>
      {cfg.shots.map((s, i) => <Sequence key={i} from={starts[i]} durationInFrames={F(s.dur)} layout="none">
        <div style={{position: 'absolute', left: 0, width: 1080, height: 1920, top: 960 - s.cy}}>
          <OffthreadVideo src={staticFile(s.src)} startFrom={F(s.from)} volume={cfg.vo ? 0.12 : 0.3} style={{width: 1080, height: 1920}} /></div>
      </Sequence>)}
    </AbsoluteFill>
    <div style={{position: 'absolute', top: 110, left: 40, right: 40, textAlign: 'center', background: 'rgba(0,0,0,0.72)', borderRadius: 26, padding: '14px 20px', transform: `scale(${interpolate(f, [0, 5, 8], [0.7, 1.05, 1], clamp)})`}}>
      <span style={{fontFamily: MONT, fontWeight: 800, fontSize: 54, lineHeight: '66px', color: '#fff'}}>{cfg.hook} </span>
      <Img src={staticFile(`res/emoji/${cfg.hookEmoji}.png`)} style={{width: 60, height: 60, verticalAlign: 'middle'}} />
    </div>
    {show && f < endAt && <div style={{position: 'absolute', top: 1080, left: 40, right: 40, textAlign: 'center', transform: `scale(${0.75 + 0.25 * pop})`}}>
      {ch!.map((w, i) => { const k = KEY.test(w.w) || (w.w.length > 1 && w.w === w.w.toUpperCase());
        return <span key={i} style={{display: 'inline-block', margin: '0 12px', fontFamily: MONT, fontWeight: 800, fontSize: 86, lineHeight: '100px', textTransform: 'uppercase',
          color: k ? '#FFE14D' : '#fff', opacity: t >= w.s ? 1 : 0, ...stroke(14)}}>{w.w.replace(/[,.]+$/, '')}</span>; })}
    </div>}
    {!cfg.vo && f < endAt && sh.line && (() => { const k = spring({frame: lf - 2, fps, config: {damping: 11, stiffness: 230}});
      const parts = sh.line.split(/(\p{Extended_Pictographic}\uFE0F?)/u).filter(Boolean);
      return <div style={{position: 'absolute', top: 980, left: 50, right: 50, display: 'flex', justifyContent: 'center', transform: `scale(${0.6 + 0.4 * k}) rotate(${si % 2 ? 1.5 : -1.5}deg)`}}>
        <div style={{background: '#fff', borderRadius: 26, padding: '18px 28px', boxShadow: '0 10px 30px rgba(0,0,0,0.6)', fontFamily: MONT, fontWeight: 800, fontSize: 60, lineHeight: '72px', color: '#111', textAlign: 'center'}}>
          {parts.map((p, i) => /\p{Extended_Pictographic}/u.test(p) ? <Img key={i} src={staticFile(`res/emoji/${[...p.replace(/\uFE0F/g, '')].map((c) => c.codePointAt(0)!.toString(16)).join('-')}.png`)} style={{width: 66, height: 66, verticalAlign: 'middle', margin: '0 4px'}} />
            : <span key={i}>{p.split(/(ONE|NOT|TEETH|COW COUNTER|12|3am|5 years|ONE prompt)/).map((q, j) => j % 2 ? <span key={j} style={{color: '#E3201B'}}>{q}</span> : q)}</span>)}
        </div></div>; })()}
    {f >= endAt && <div style={{position: 'absolute', top: 1040, left: 40, right: 40, textAlign: 'center', transform: `scale(${0.6 + 0.4 * endK}) rotate(-3deg)`}}>
      <span style={{fontFamily: MONT, fontWeight: 800, fontSize: 78, color: '#FFE14D', ...stroke(14)}}>{cfg.end} </span>
      <Img src={staticFile(`res/emoji/${cfg.endEmoji}.png`)} style={{width: 84, height: 84, verticalAlign: 'middle'}} />
    </div>}
    <div style={{position: 'absolute', bottom: 250, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
      <div style={{background: 'rgba(0,0,0,0.78)', borderRadius: 20, padding: '14px 30px', fontFamily: MONT, fontWeight: 800, fontSize: 48, color: '#fff', border: '3px solid #D97757'}}>
        made w/ claude + <span style={{color: '#FFE14D'}}>forgegui mcp</span></div>
    </div>
    {cfg.vo && <Audio src={staticFile(cfg.vo)} volume={1} />}
    <Audio src={staticFile(cfg.music[0])} startFrom={F(cfg.music[1])} volume={cfg.vo ? 0.16 : 0.75} />
  </AbsoluteFill>;
};

// ClipFarm x BOXED.GG clip template (2026-11-18). Brief: hook in 3 s (lead with the reaction, then the rip), BIG captions naming the card
// and the moment (white text, black outline), 9:16, fast cuts, organic feel (keep the creators' own audio, no ad look).
// NEVER gambling: no odds / bets / values on screen -> crops zoom away from UI numbers, and a blurred strip hides the creators' own
// burned-in captions (some of theirs say things like "BET IT").
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import CFG from './boxed.cfg.json';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
type Word = {word: string; startFrame: number; endFrame: number; hi?: boolean};
type Scene = {id: string; videoStartSec: number; durationInFrames: number; crops: number[][]; words: Word[]};
type BCfg = {src: string; srcW: number; srcH: number; band?: [number, number]; capY: number; hook: string[]; hookFrames: number; scenes: Scene[]};
export const BOXED = CFG as unknown as Record<string, BCfg>;
export const boxedFrames = (id: string) => BOXED[id].scenes.reduce((a, s) => a + s.durationInFrames, 0);

const stroke = (w: number): React.CSSProperties => ({WebkitTextStroke: `${w}px #000`, paintOrder: 'stroke fill', textShadow: '0 6px 16px rgba(0,0,0,0.6)'});

export const Boxed: React.FC<{edit: string}> = ({edit}) => {
  const cfg = BOXED[edit], SCENES = cfg.scenes, f = useCurrentFrame(), {fps} = useVideoConfig();
  const START: Record<string, number> = {}; SCENES.reduce((a, s) => { START[s.id] = a; return a + s.durationInFrames; }, 0);
  const si = Math.max(0, SCENES.findIndex((s) => f >= START[s.id] && f < START[s.id] + s.durationInFrames)), sc = SCENES[si], lf = f - START[sc.id];
  const ci = sc.crops.filter(([t]) => t <= lf).length - 1, crop = sc.crops[Math.max(0, ci)];
  const shotA = crop[0], shotB = sc.crops[ci + 1]?.[0] ?? sc.durationInFrames;
  // crop = [frame, centre x, zoom, centre y] in source px; zoom 1 = the whole (vertical) frame
  const [cx, cz, cy] = [crop[1], crop[2] ?? 1, crop[3] ?? cfg.srcH / 2];
  const push = 1 + 0.035 * Math.min(1, (lf - shotA) / Math.max(1, shotB - shotA));
  const S = (1920 / cfg.srcH) * cz, vw = cfg.srcW * S, vh = cfg.srcH * S;
  const left = Math.min(0, Math.max(1080 - vw, 540 - cx * S)), top = Math.min(0, Math.max(1920 - vh, 960 - cy * S));
  const cutAge = f - Math.max(...SCENES.flatMap((s) => s.crops.map(([t]) => START[s.id] + t)).filter((t) => t <= f));
  const whip = cutAge < 4 && f > 4 ? [-60, -24, -8, 0][cutAge] : 0;

  const words = SCENES.flatMap((s) => s.words.map((w) => ({...w, s: s.id, at: START[s.id] + w.startFrame, end: START[s.id] + w.endFrame})));
  const chunks: (typeof words)[] = [];
  words.forEach((w, i) => { const c = chunks[chunks.length - 1], p = words[i - 1];
    if (!c || c.length >= 3 || p.s !== w.s || w.at - p.end > 8 || /[.?!,]$/.test(p.word)) chunks.push([w]); else c.push(w); });
  const ch = chunks.filter((c) => f >= c[0].at).pop(), next = ch ? chunks[chunks.indexOf(ch) + 1] : undefined;
  const chEnd = next ? next[0].at : boxedFrames(edit);
  const pop = ch ? spring({frame: f - ch[0].at, fps, config: {damping: 12, stiffness: 240}}) : 1;
  const cuts = SCENES.slice(1).map((s) => START[s.id]);

  return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
    <AbsoluteFill style={{transform: `translateX(${whip}px) scale(${push})`}}>
      <Sequence key={sc.id} from={START[sc.id]} durationInFrames={sc.durationInFrames} layout="none">
        <OffthreadVideo src={staticFile(cfg.src)} startFrom={Math.round(sc.videoStartSec * fps)} style={{position: 'absolute', left, top, width: vw, height: vh}} />
      </Sequence>
    </AbsoluteFill>
    {/* hide the creators' burned-in captions (only on full-frame shots, where they sit at a fixed height) */}
    {cfg.band && cz <= 1.01 && <div style={{position: 'absolute', left: 0, right: 0, top: cfg.band[0], height: cfg.band[1] - cfg.band[0], backdropFilter: 'blur(22px)', WebkitBackdropFilter: 'blur(22px)', background: 'rgba(0,0,0,0.12)'}} />}

    {f < cfg.hookFrames && <div style={{position: 'absolute', top: 170, left: 40, right: 40, textAlign: 'center', opacity: interpolate(f, [cfg.hookFrames - 6, cfg.hookFrames], [1, 0], clamp)}}>
      {cfg.hook.map((l, i) => { const k = spring({frame: f - 3 * i, fps, config: {damping: 13, stiffness: 210}});
        return <div key={i} style={{fontFamily: MONT, fontWeight: 800, fontSize: 74, lineHeight: '86px', color: i === cfg.hook.length - 1 ? '#FFE11A' : '#fff', textTransform: 'uppercase', transform: `scale(${0.6 + 0.4 * k})`, ...stroke(11)}}>{l}</div>; })}
    </div>}

    {ch && f < chEnd && <div style={{position: 'absolute', top: cfg.capY, left: 40, right: 40, textAlign: 'center', transform: `scale(${0.85 + 0.15 * pop})`}}>
      {ch.map((w, i) => <span key={i} style={{display: 'inline-block', margin: '0 12px', fontFamily: MONT, fontWeight: 800, fontSize: 84, lineHeight: '98px', textTransform: 'uppercase',
        color: w.hi ? '#FFE11A' : '#fff', opacity: f >= w.at ? 1 : 0, ...stroke(12)}}>{w.word.replace(/[,.!]+$/, '')}</span>)}
    </div>}

    {cuts.map((t, i) => <Sequence key={'w' + i} from={Math.max(0, t - 16)}><Audio src={staticFile('res/m_fast-whoosh.mp3')} volume={0.16} /></Sequence>)}
  </AbsoluteFill>;
};

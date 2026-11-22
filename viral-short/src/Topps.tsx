// ClipFarm x Topps clip template (2026-11-18). Brief: hook in 2 s = the reveal/reaction first, then REWIND to the rip; big captions that
// name the card and the moment; 9:16; fast cuts; story-first (never the price as the hook); no skull edits; no #ad (caption rule).
// Scenes: normal ones play the source; a scene with `rewind: [from, to]` scrubs backwards (muted, scanlines + ◀◀) like a tape rewind.
// A persistent label names the card for the whole clip; a blurred strip hides the source edit's own burned-in title/ticker.
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, OffthreadVideo, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import CFG from './topps.cfg.json';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
type Word = {word: string; startFrame: number; endFrame: number; hi?: boolean};
type Scene = {id: string; videoStartSec: number; durationInFrames: number; crops: number[][]; words: Word[]; rewind?: [number, number]};
type TCfg = {src: string; srcW: number; srcH: number; band?: [number, number]; capY: number; label: string[]; labelY: number; scenes: Scene[]};
export const TOPPS = CFG as unknown as Record<string, TCfg>;
export const toppsFrames = (id: string) => TOPPS[id].scenes.reduce((a, s) => a + s.durationInFrames, 0);
const stroke = (w: number): React.CSSProperties => ({WebkitTextStroke: `${w}px #000`, paintOrder: 'stroke fill', textShadow: '0 6px 16px rgba(0,0,0,0.6)'});

export const Topps: React.FC<{edit: string}> = ({edit}) => {
  const cfg = TOPPS[edit], SCENES = cfg.scenes, f = useCurrentFrame(), {fps} = useVideoConfig();
  const START: Record<string, number> = {}; SCENES.reduce((a, s) => { START[s.id] = a; return a + s.durationInFrames; }, 0);
  const si = Math.max(0, SCENES.findIndex((s) => f >= START[s.id] && f < START[s.id] + s.durationInFrames)), sc = SCENES[si], lf = f - START[sc.id];
  const ci = sc.crops.filter(([t]) => t <= lf).length - 1, crop = sc.crops[Math.max(0, ci)];
  const shotA = crop[0], shotB = sc.crops[ci + 1]?.[0] ?? sc.durationInFrames;
  const [cx, cz, cy] = [crop[1], crop[2] ?? 1, crop[3] ?? cfg.srcH / 2];
  const push = sc.rewind ? 1 : 1 + 0.04 * Math.min(1, (lf - shotA) / Math.max(1, shotB - shotA));
  const S = (1920 / cfg.srcH) * cz, vw = cfg.srcW * S, vh = cfg.srcH * S;
  const left = Math.min(0, Math.max(1080 - vw, 540 - cx * S)), top = Math.min(0, Math.max(1920 - vh, 960 - cy * S));
  const style: React.CSSProperties = {position: 'absolute', left, top, width: vw, height: vh};
  const cutAge = f - Math.max(...SCENES.flatMap((s) => s.crops.map(([t]) => START[s.id] + t)).filter((t) => t <= f));
  const whip = cutAge < 4 && f > 4 && !sc.rewind ? [-60, -24, -8, 0][cutAge] : 0;

  const words = SCENES.flatMap((s) => s.words.map((w) => ({...w, s: s.id, at: START[s.id] + w.startFrame, end: START[s.id] + w.endFrame})));
  const chunks: (typeof words)[] = [];
  words.forEach((w, i) => { const c = chunks[chunks.length - 1], p = words[i - 1];
    if (!c || c.length >= 3 || p.s !== w.s || w.at - p.end > 8 || /[.?!,]$/.test(p.word)) chunks.push([w]); else c.push(w); });
  const ch = chunks.filter((c) => f >= c[0].at).pop(), next = ch ? chunks[chunks.indexOf(ch) + 1] : undefined;
  const chEnd = Math.min(next ? next[0].at : toppsFrames(edit), ch ? ch[ch.length - 1].end + 15 : 0);
  const pop = ch ? spring({frame: f - ch[0].at, fps, config: {damping: 12, stiffness: 240}}) : 1;
  const lk = spring({frame: f, fps, config: {damping: 13, stiffness: 200}});

  return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
    <AbsoluteFill style={{transform: `translateX(${whip}px) scale(${push})`}}>
      {sc.rewind ? (() => { const [a, b] = sc.rewind!, t = a - (a - b) * (lf / Math.max(1, sc.durationInFrames - 1));
        return <Sequence key={'rw' + f} from={f} durationInFrames={1} layout="none"><OffthreadVideo src={staticFile(cfg.src)} muted startFrom={Math.round(t * fps)} style={style} /></Sequence>; })()
        : <Sequence key={sc.id} from={START[sc.id]} durationInFrames={sc.durationInFrames} layout="none"><OffthreadVideo src={staticFile(cfg.src)} startFrom={Math.round(sc.videoStartSec * fps)} style={style} /></Sequence>}
    </AbsoluteFill>
    {cfg.band && <div style={{position: 'absolute', left: 0, right: 0, top: cfg.band[0], height: cfg.band[1] - cfg.band[0], backdropFilter: 'blur(24px)', WebkitBackdropFilter: 'blur(24px)', background: 'rgba(0,0,0,0.18)'}} />}
    {sc.rewind && <AbsoluteFill style={{background: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.25) 0 3px, transparent 3px 7px)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 170, color: '#fff', ...stroke(10)}}>◀◀</div></AbsoluteFill>}

    {/* card name label, whole clip */}
    <div style={{position: 'absolute', top: cfg.labelY, left: 30, right: 30, textAlign: 'center', transform: `scale(${0.7 + 0.3 * lk})`}}>
      {cfg.label.map((l, i) => <div key={i} style={{fontFamily: MONT, fontWeight: 800, fontSize: 66, lineHeight: '78px', textTransform: 'uppercase', color: i === cfg.label.length - 1 ? '#FFD400' : '#fff', ...stroke(11)}}>{l}</div>)}
    </div>

    {ch && f < chEnd && !sc.rewind && <div style={{position: 'absolute', top: cfg.capY, left: 40, right: 40, textAlign: 'center', transform: `scale(${0.85 + 0.15 * pop})`}}>
      {ch.map((w, i) => <span key={i} style={{display: 'inline-block', margin: '0 12px', fontFamily: MONT, fontWeight: 800, fontSize: 86, lineHeight: '100px', textTransform: 'uppercase',
        color: w.hi ? '#FFD400' : '#fff', opacity: f >= w.at ? 1 : 0, ...stroke(12)}}>{w.word.replace(/[,.]+$/, '')}</span>)}
    </div>}
    {SCENES.filter((s) => s.rewind).map((s) => <Sequence key={'r' + s.id} from={START[s.id]}><Audio src={staticFile('res/m_rev-whoosh.mp3')} volume={0.4} /></Sequence>)}
    {SCENES.slice(1).filter((s) => !s.rewind).map((s) => <Sequence key={'w' + s.id} from={Math.max(0, START[s.id] - 16)}><Audio src={staticFile('res/m_fast-whoosh.mp3')} volume={0.16} /></Sequence>)}
  </AbsoluteFill>;
};

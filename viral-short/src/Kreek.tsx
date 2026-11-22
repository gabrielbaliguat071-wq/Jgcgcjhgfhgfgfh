// ClipLaunch x KreekCraft GTA 6 — streamer split layout: official KreekCraft logo overlay (REQUIRED, whole clip, drawn last),
// facecam panel on top, gameplay panel below (cropped above the stream's own burned-in captions), our captions on the seam,
// hook = the loudest reaction first, then the moment in order. Source = Twitch clips of his GTA 6 Day 1 stream (1920x1080).
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import CFG from './kreek.cfg.json';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
type Word = {word: string; startFrame: number; endFrame: number; hi?: boolean};
type Scene = {id: string; videoStartSec: number; durationInFrames: number; words: Word[]};
type KCfg = {src: string; hook: string[]; scenes: Scene[]};
export const KREEK = CFG as unknown as Record<string, KCfg>;
export const kreekFrames = (id: string) => KREEK[id].scenes.reduce((a, s) => a + s.durationInFrames, 0);

const TOP = 300, CAM_H = 640, SEAM = TOP + CAM_H, GAME_H = 1920 - SEAM;
// source regions (1920x1080): facecam top-left, gameplay centre (y < 940 keeps the stream's burned captions out)
const CAM = {x: 55, y: 150, w: 330, h: 380};
const GAME = {x: 450, y: 50, w: 1040, h: 890};
const stroke = (w: number): React.CSSProperties => ({WebkitTextStroke: `${w}px #000`, paintOrder: 'stroke fill', textShadow: '0 6px 14px rgba(0,0,0,0.6)'});

const Panel: React.FC<{src: string; start: number; region: typeof CAM; W: number; H: number; zoom: number; muted?: boolean}> = ({src, start, region, W, H, zoom, muted}) => {
  const s = Math.max(W / region.w, H / region.h) * zoom;
  const left = W / 2 - (region.x + region.w / 2) * s, top = H / 2 - (region.y + region.h / 2) * s;
  return <OffthreadVideo src={staticFile(src)} muted={muted} startFrom={start} style={{position: 'absolute', left, top, width: 1920 * s, height: 1080 * s}} />;
};

export const Kreek: React.FC<{edit: string}> = ({edit}) => {
  const cfg = KREEK[edit], SC = cfg.scenes, f = useCurrentFrame(), {fps} = useVideoConfig();
  const START: Record<string, number> = {}; SC.reduce((a, s) => { START[s.id] = a; return a + s.durationInFrames; }, 0);
  const si = Math.max(0, SC.findIndex((s) => f >= START[s.id] && f < START[s.id] + s.durationInFrames)), sc = SC[si], lf = f - START[sc.id];
  const hook = si === 0, start = Math.round(sc.videoStartSec * fps);
  const punch = hook ? interpolate(lf, [0, 6, sc.durationInFrames], [1.18, 1.1, 1.14]) : 1 + 0.04 * (lf / sc.durationInFrames);
  const whip = lf < 4 && f > 0 ? [-60, -24, -8, 0][lf] : 0;
  const words = SC.flatMap((s) => s.words.map((w) => ({...w, s: s.id, at: START[s.id] + w.startFrame, end: START[s.id] + w.endFrame})));
  const chunks: (typeof words)[] = [];
  words.forEach((w, i) => { const c = chunks[chunks.length - 1], p = words[i - 1];
    if (!c || c.length >= 3 || p.s !== w.s || w.at - p.end > 8 || /[.?!,]$/.test(p.word)) chunks.push([w]); else c.push(w); });
  const ch = chunks.filter((c) => f >= c[0].at).pop(), next = ch ? chunks[chunks.indexOf(ch) + 1] : undefined;
  const chEnd = Math.min(next ? next[0].at : kreekFrames(edit), ch ? ch[ch.length - 1].end + 15 : 0);
  const pop = ch ? spring({frame: f - ch[0].at, fps, config: {damping: 12, stiffness: 240}}) : 1;
  const hk = spring({frame: f, fps, config: {damping: 12, stiffness: 210}});

  return <AbsoluteFill style={{background: '#0b0b10', overflow: 'hidden'}}>
    <Sequence key={sc.id} from={START[sc.id]} durationInFrames={sc.durationInFrames} layout="none">
      <div style={{position: 'absolute', left: 0, top: TOP, width: 1080, height: CAM_H, overflow: 'hidden', transform: `translateX(${whip}px)`}}>
        <Panel src={cfg.src} start={start} region={CAM} W={1080} H={CAM_H} zoom={punch} muted />
      </div>
      <div style={{position: 'absolute', left: 0, top: SEAM, width: 1080, height: GAME_H, overflow: 'hidden', transform: `translateX(${whip}px)`}}>
        <Panel src={cfg.src} start={start} region={GAME} W={1080} H={GAME_H} zoom={hook ? 1.08 : 1} />
      </div>
    </Sequence>
    <div style={{position: 'absolute', left: 0, right: 0, top: SEAM - 5, height: 10, background: '#000'}} />

    {hook && <div style={{position: 'absolute', top: SEAM + 70, left: 30, right: 30, textAlign: 'center', transform: `scale(${0.7 + 0.3 * hk})`}}>
      {cfg.hook.map((l, i) => <div key={i} style={{fontFamily: MONT, fontWeight: 800, fontSize: 62, lineHeight: 1.15, textTransform: 'uppercase', color: i === cfg.hook.length - 1 ? '#FFE14D' : '#fff', ...stroke(11)}}>{l}</div>)}
    </div>}

    {ch && f < chEnd && <div style={{position: 'absolute', top: SEAM - 62, left: 30, right: 30, textAlign: 'center', transform: `scale(${0.85 + 0.15 * pop})`}}>
      {ch.map((w, i) => <span key={i} style={{display: 'inline-block', margin: '0 10px', fontFamily: MONT, fontWeight: 800, fontSize: 84, lineHeight: '100px', textTransform: 'uppercase',
        color: w.hi ? '#FFE14D' : '#fff', opacity: f >= w.at ? 1 : 0, ...stroke(12)}}>{w.word.replace(/[,.]+$/, '')}</span>)}
    </div>}

    {/* REQUIRED: official KreekCraft logo overlay, whole video, never covered */}
    <Img src={staticFile('res/kreek_overlay.png')} style={{position: 'absolute', top: 40, left: 160, width: 760}} />
    {SC.slice(1).map((s) => <Sequence key={'w' + s.id} from={Math.max(0, START[s.id] - 16)}><Audio src={staticFile('res/m_fast-whoosh.mp3')} volume={0.2} /></Sequence>)}
  </AbsoluteFill>;
};

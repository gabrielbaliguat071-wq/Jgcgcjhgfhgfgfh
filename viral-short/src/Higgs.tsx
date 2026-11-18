// ClipFarm x Higgsfield (20VC, Alex Mashrabov) clip template, copied from the campaign's footage examples:
// full-frame 9:16 crop on the speaker (dark blue studio), white bold italic 1-3 word captions mid-frame with the key word/number
// in yellow, a red boxed hook for the first seconds, small white info cards for numbers, soft dark bottom gradient.
// REQUIRED by the brief: the Higgsfield watermark, big, readable, on the whole clip and never covered (drawn last, at the top).
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import CFG from './higgs.cfg.json';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
type Word = {word: string; startFrame: number; endFrame: number; hi?: boolean};
type Scene = {id: string; videoStartSec: number; durationInFrames: number; crops: number[][]; words: Word[]};
type Card = {at: [string, number]; dur: number; big: string; small: string};
type HCfg = {src: string; hook: string[]; hookFrames: number; music: [string, number]; musicVol: number; scenes: Scene[]; cards: Card[]; wm: string};
export const HIGGS = CFG as unknown as Record<string, HCfg>;
export const higgsFrames = (id: string) => HIGGS[id].scenes.reduce((a, s) => a + s.durationInFrames, 0);

export const Higgs: React.FC<{edit: string}> = ({edit}) => {
  const cfg = HIGGS[edit], SCENES = cfg.scenes, f = useCurrentFrame(), {fps} = useVideoConfig();
  const START: Record<string, number> = {}; SCENES.reduce((a, s) => { START[s.id] = a; return a + s.durationInFrames; }, 0);
  const si = Math.max(0, SCENES.findIndex((s) => f >= START[s.id] && f < START[s.id] + s.durationInFrames)), sc = SCENES[si], lf = f - START[sc.id];
  const ci = sc.crops.filter(([t]) => t <= lf).length - 1, crop = sc.crops[Math.max(0, ci)];
  const shotA = crop[0], shotB = sc.crops[ci + 1]?.[0] ?? sc.durationInFrames;
  const [cx, cz, cy] = [crop[1], crop[2] ?? 1, crop[3] ?? 540];
  const push = 1 + 0.04 * Math.min(1, (lf - shotA) / Math.max(1, shotB - shotA));
  const S = (1920 / 1080) * cz, vw = 1920 * S, vh = 1080 * S;
  const left = Math.min(0, Math.max(1080 - vw, 540 - cx * S)), top = Math.min(0, Math.max(1920 - vh, 960 - cy * S));

  // captions: 1-3 words, break on punctuation / scene change / pause; words appear as spoken
  const words = SCENES.flatMap((s) => s.words.map((w) => ({...w, s: s.id, at: START[s.id] + w.startFrame, end: START[s.id] + w.endFrame})));
  const chunks: (typeof words)[] = [];
  words.forEach((w, i) => { const c = chunks[chunks.length - 1], p = words[i - 1];
    if (!c || c.length >= 3 || p.s !== w.s || w.at - p.end > 8 || /[.?!,]$/.test(p.word)) chunks.push([w]); else c.push(w); });
  const ch = chunks.filter((c) => f >= c[0].at).pop(), next = ch ? chunks[chunks.indexOf(ch) + 1] : undefined;
  const chEnd = next ? next[0].at : higgsFrames(edit);
  const cards = cfg.cards.map((c) => ({...c, t: START[c.at[0]] + c.at[1]}));
  const card = cards.find((c) => f >= c.t && f < c.t + c.dur);
  const cuts = SCENES.slice(1).map((s) => START[s.id]);

  return <AbsoluteFill style={{background: '#050a18', overflow: 'hidden'}}>
    <AbsoluteFill style={{transform: `scale(${push})`}}>
      <Sequence key={sc.id} from={START[sc.id]} durationInFrames={sc.durationInFrames} layout="none">
        <OffthreadVideo src={staticFile(cfg.src)} startFrom={Math.round(sc.videoStartSec * fps)} style={{position: 'absolute', left, top, width: vw, height: vh}} />
      </Sequence>
    </AbsoluteFill>
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.35) 0%, transparent 18%, transparent 62%, rgba(0,0,0,0.75) 100%)'}} />

    {/* caption, mid-lower frame (chest), key words/numbers yellow */}
    {ch && f < chEnd && <div style={{position: 'absolute', top: 1170, left: 50, right: 50, textAlign: 'center'}}>
      {ch.map((w, i) => <span key={i} style={{display: 'inline-block', margin: '0 10px', fontFamily: MONT, fontWeight: 800, fontStyle: 'italic', fontSize: 70, lineHeight: '84px',
        color: w.hi ? '#FFD400' : '#fff', opacity: f >= w.at ? 1 : 0, textShadow: '0 4px 14px rgba(0,0,0,0.85), 0 0 3px rgba(0,0,0,0.9)'}}>{w.word.replace(/[,]+$/, '')}</span>)}
    </div>}

    {/* hook: red boxed lines, first seconds */}
    {f < cfg.hookFrames && <div style={{position: 'absolute', top: 1310, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6,
      opacity: interpolate(f, [cfg.hookFrames - 6, cfg.hookFrames], [1, 0], clamp)}}>
      {cfg.hook.map((l, i) => { const k = spring({frame: f - 2 - 3 * i, fps, config: {damping: 14, stiffness: 200}});
        return <span key={i} style={{background: '#E5312F', color: '#fff', fontFamily: MONT, fontWeight: 800, fontSize: 60, lineHeight: '70px', padding: '2px 18px', borderRadius: 10,
          transform: `scale(${0.7 + 0.3 * k})`, opacity: k}}>{l}</span>; })}
    </div>}

    {/* info card for numbers */}
    {card && (() => { const k = f - card.t, s = spring({frame: k, fps, config: {damping: 13, stiffness: 190}}), o = k > card.dur - 6 ? (card.dur - k) / 6 : 1;
      return <div style={{position: 'absolute', top: 1320, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: o}}>
        <div style={{background: '#fff', borderRadius: 22, padding: '18px 44px', textAlign: 'center', boxShadow: '0 12px 34px rgba(0,0,0,0.55)', transform: `scale(${0.6 + 0.4 * s}) translateY(${(1 - s) * 30}px)`}}>
          <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 92, lineHeight: '100px', color: '#111', letterSpacing: -2}}>{card.big}</div>
          <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 30, color: '#555', letterSpacing: 2, textTransform: 'uppercase'}}>{card.small}</div>
        </div></div>; })()}

    {/* REQUIRED watermark: big, readable, whole clip, drawn last so nothing covers it */}
    <Img src={staticFile(`res/${cfg.wm}`)} style={{position: 'absolute', top: 96, left: 140, width: 800}} />

    <Audio src={staticFile(`res/${cfg.music[0]}.mp3`)} startFrom={Math.round(cfg.music[1] * fps)} volume={cfg.musicVol} loop />
    {cuts.map((t, i) => <Sequence key={'w' + i} from={Math.max(0, t - 16)}><Audio src={staticFile('res/m_fast-whoosh.mp3')} volume={0.18} /></Sequence>)}
    {cards.map((c, i) => <Sequence key={'c' + i} from={c.t}><Audio src={staticFile('res/pop.mp3')} volume={0.22} /></Sequence>)}
  </AbsoluteFill>;
};

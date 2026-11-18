// BloxClips x Cursed Voyage (Roblox) — 3 TikToks built from the campaign's key art (no gameplay footage was provided).
// Each scene = one artwork with a slow push/pan, hard cut + light whip, big outlined caption. Ends on the required CTA:
// "Cursed Voyage", out now, free to play on Roblox. Only facts from the brief (no made-up features, rewards or codes).
// House rules: no colour fades, light blur only, no loud booms.
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
type Scene = {img: string; dur: number; text: string[]; hl?: number; zoom?: [number, number]; pan?: [number, number]; focus?: number};
type Clip = {scenes: Scene[]; music: number};
const T = (s: number) => Math.round(s * 30);

export const CURSED: Record<string, Clip> = {
  cvroblox: {music: 4, scenes: [
    {img: 'key_art_8', dur: 1.6, text: ['Wait…'], zoom: [1.16, 1.27], focus: 0.62},
    {img: 'key_art_8', dur: 1.5, text: ['this is', 'ROBLOX?!'], hl: 1, zoom: [1.27, 1.34], focus: 0.62},
    {img: 'key_art_4', dur: 1.7, text: ['stone', 'GOLEMS'], hl: 1, zoom: [1.11, 1.20], focus: 0.3},
    {img: 'key_art_3', dur: 1.7, text: ['first-person', 'GUNFIGHTS'], hl: 1, zoom: [1.14, 1.23], focus: 0.55},
    {img: 'key_art_1', dur: 1.7, text: ['a haunted', 'JUNGLE RIVER'], hl: 1, zoom: [1.09, 1.18], pan: [-60, 40], focus: 0.4},
    {img: 'key_art_2', dur: 1.7, text: ['temple', 'TRAPS'], hl: 1, zoom: [1.11, 1.20], focus: 0.5},
    {img: 'key_art_7', dur: 1.7, text: ['and CURSED', 'TREASURE'], hl: 1, zoom: [1.14, 1.23], focus: 0.25},
    {img: 'cursed_voyage_icon', dur: 3.4, text: ['CURSED VOYAGE', 'free on Roblox — play now'], hl: 0, zoom: [1.0, 1.08]},
  ]},
  cvrelic: {music: 30, scenes: [
    {img: 'key_art_7', dur: 1.9, text: ['we had', 'ENOUGH GOLD…'], hl: 1, zoom: [1.14, 1.25], focus: 0.2},
    {img: 'key_art_7', dur: 1.7, text: ['but he grabbed', 'ONE MORE RELIC'], hl: 1, zoom: [1.27, 1.38], focus: 0.2},
    {img: 'key_art_6', dur: 1.9, text: ['every cursed relic', 'RAISES YOUR CURSE'], hl: 1, zoom: [1.11, 1.20], focus: 0.55},
    {img: 'key_art_2', dur: 1.8, text: ['then the temple', 'TURNED ON US'], hl: 1, zoom: [1.11, 1.20], focus: 0.45},
    {img: 'key_art_4', dur: 1.8, text: ['golems', 'EVERYWHERE'], hl: 1, zoom: [1.14, 1.23], focus: 0.35},
    {img: 'key_art_5', dur: 1.9, text: ['dragging the loot', 'BACK TO THE BOAT'], hl: 1, zoom: [1.11, 1.20], focus: 0.4},
    {img: 'cursed_voyage_icon', dur: 3.4, text: ['would you grab it?', 'CURSED VOYAGE', 'free on Roblox — play now'], hl: 1, zoom: [1.0, 1.08]},
  ]},
  cvshift: {music: 55, scenes: [
    {img: 'key_art_3', dur: 2.0, text: ['almost nobody reaches', 'SHIFT 50'], hl: 1, zoom: [1.23, 1.34], focus: 0.62},
    {img: 'key_art_1', dur: 1.9, text: ['most players never pass', 'SHIFT 10'], hl: 1, zoom: [1.09, 1.18], pan: [40, -40], focus: 0.45},
    {img: 'key_art_4', dur: 1.7, text: ['every shift', 'GETS HARDER'], hl: 1, zoom: [1.11, 1.20], focus: 0.3},
    {img: 'key_art_6', dur: 1.7, text: ['the deeper you sail', 'THE DARKER IT GETS'], hl: 1, zoom: [1.14, 1.23], focus: 0.6},
    {img: 'key_art_5', dur: 1.8, text: ['bring up to', '3 FRIENDS'], hl: 1, zoom: [1.11, 1.20], focus: 0.4},
    {img: 'cursed_voyage_icon', dur: 3.4, text: ['how deep can YOUR crew go?', 'CURSED VOYAGE', 'free on Roblox — play now'], hl: 1, zoom: [1.0, 1.08]},
  ]},
};
export const cursedFrames = (id: string) => CURSED[id].scenes.reduce((a, s) => a + T(s.dur), 0);
const stroke = (w: number): React.CSSProperties => ({WebkitTextStroke: `${w}px #000`, paintOrder: 'stroke fill', textShadow: '0 8px 20px rgba(0,0,0,0.7)'});

export const Cursed: React.FC<{edit: string}> = ({edit}) => {
  const clip = CURSED[edit], f = useCurrentFrame(), {fps} = useVideoConfig();
  const starts: number[] = []; clip.scenes.reduce((a, s) => { starts.push(a); return a + T(s.dur); }, 0);
  const si = Math.max(0, starts.filter((s) => s <= f).length - 1), sc = clip.scenes[si], lf = f - starts[si], n = T(sc.dur);
  const icon = sc.img === 'cursed_voyage_icon', k = lf / n;
  const z = interpolate(k, [0, 1], sc.zoom ?? [1.2, 1.35]), px = interpolate(k, [0, 1], sc.pan ?? [0, 0]);
  const whip = lf < 4 && f > 0 ? [-70, -28, -8, 0][lf] : 0, blur = lf < 3 && f > 0 ? [3, 1.5, 0][lf] : 0;
  // landscape art: height-fill the 9:16 frame around a horizontal focus point (0..1); the icon sits centred
  const fx = sc.focus ?? 0.5;
  const pop = spring({frame: lf, fps, config: {damping: 12, stiffness: 230}});
  const shake = lf < 6 && (si === 1 || icon) ? Math.sin(lf * 3) * (6 - lf) * 2 : 0;
  const isCTA = icon;

  return <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 45%, #10241c 0%, #04080a 75%)', overflow: 'hidden'}}>
    {!icon && <div style={{position: 'absolute', left: 0, top: 360, width: 1080, height: 760, overflow: 'hidden', borderTop: '6px solid #5CF29A', borderBottom: '6px solid #5CF29A', boxShadow: '0 0 60px rgba(92,242,154,0.25)'}}>
      <div style={{position: 'absolute', inset: 0, transform: `translate(${whip + px + shake}px, 0) scale(${z})`, filter: blur ? `blur(${blur}px)` : undefined}}>
        <Img src={staticFile(`res/cv/${sc.img}.jpg`)} style={{position: 'absolute', top: 0, left: Math.min(0, Math.max(1080 - 1351, 540 - fx * 1351)), width: 1351, height: 760, objectFit: 'cover'}} />
      </div>
    </div>}
    {icon && <AbsoluteFill style={{display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'radial-gradient(circle at 50% 42%, #1d3b30 0%, #04080a 70%)'}}>
      <Img src={staticFile('res/cv/cursed_voyage_icon.jpg')} style={{width: 640, height: 640, borderRadius: 72, boxShadow: '0 30px 80px rgba(0,0,0,0.7)', transform: `translateY(-150px) scale(${(0.7 + 0.3 * pop) * z}) translateX(${shake}px)`}} />
    </AbsoluteFill>}
    {!isCTA && <div style={{position: 'absolute', top: 210, left: 0, right: 0, textAlign: 'center'}}><span style={{fontFamily: MONT, fontWeight: 800, fontSize: 40, letterSpacing: 4, color: '#04150c', background: '#5CF29A', borderRadius: 14, padding: '8px 22px'}}>ROBLOX · CURSED VOYAGE</span></div>}
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.45) 0%, transparent 22%, transparent 60%, rgba(0,0,0,0.55) 100%)'}} />

    <div style={{position: 'absolute', left: 50, right: 50, top: isCTA ? 1180 : 1170, textAlign: 'center', transform: `scale(${0.75 + 0.25 * pop})`}}>
      {sc.text.map((l, i) => { const cta = isCTA && i === sc.text.length - 1;
        return <div key={i} style={{fontFamily: MONT, fontWeight: 800, textTransform: cta ? 'none' : 'uppercase', fontSize: cta ? 58 : i === sc.hl ? 112 : 70,
          lineHeight: cta ? '74px' : i === sc.hl ? '122px' : '84px', color: i === sc.hl ? '#5CF29A' : '#fff', marginTop: cta ? 26 : 0,
          ...(cta ? {display: 'inline-block', background: '#5CF29A', color: '#04150c', borderRadius: 18, padding: '10px 28px', textShadow: 'none'} : stroke(i === sc.hl ? 14 : 10))}}>{l}</div>; })}
    </div>

    <Audio src={staticFile('res/investigations_n.mp3')} startFrom={T(clip.music)} volume={0.55} />
    {starts.slice(1).map((s, i) => <Sequence key={'w' + i} from={Math.max(0, s - 16)}><Audio src={staticFile('res/m_fast-whoosh.mp3')} volume={0.28} /></Sequence>)}
    <Sequence from={T(clip.scenes[0].dur)}><Audio src={staticFile('res/m_mg-boom.mp3')} volume={0.18} /></Sequence>
    <Sequence from={starts[starts.length - 1]}><Audio src={staticFile('res/m_mg-boom.mp3')} volume={0.16} /></Sequence>
  </AbsoluteFill>;
};

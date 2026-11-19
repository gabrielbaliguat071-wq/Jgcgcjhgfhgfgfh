// ClipFarm x BOXABL — videos from the user's own photorealistic AI images (house-only scenes, no real people).
// Each shot: slow push toward a focal point + light whip on the cut; a BOXABL sign is composited onto the house's roof fascia
// (AI can't spell it), big caption on top, BOXABL end card. House rules: no colour fades, light blur only, no loud booms.
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
const K = 1080 / 768;   // source images are 768x1376 -> 1080x1935
const S = (s: number) => Math.round(s * 30);
// sign = [centre x, centre y, width] in SOURCE px (on the roof fascia / top of the front wall)
const IMG: Record<string, {sign: [number, number, number]; focus: [number, number]}> = {
  fly: {sign: [388, 288, 250], focus: [390, 420]},
  unfold: {sign: [318, 607, 170], focus: [380, 640]},
  mars: {sign: [302, 638, 230], focus: [330, 720]},
  dino: {sign: [308, 566, 230], focus: [380, 700]},
  west: {sign: [488, 538, 200], focus: [440, 700]},
  alien: {sign: [378, 548, 240], focus: [400, 760]},
};
type Shot = {capY?: number; img: string; dur: number; text: string[]; hl?: number; z?: [number, number]; shake?: boolean; num?: string};
type Clip = {shots: Shot[]; music: [string, number]; endSub: string; endQ?: string};
export const BXP: Record<string, Clip> = {
  bxtraffic: {music: ['montagem_n', 24], endSub: 'the future gets delivered', shots: [
    {img: 'fly', dur: 2.6, text: ['traffic?', 'NOT TODAY'], hl: 1, z: [1.0, 1.12], capY: 1000},
    {img: 'unfold', dur: 2.6, text: ['it unfolds like a', 'TRANSFORMER'], hl: 1, z: [1.05, 1.18], shake: true},
    {img: 'mars', dur: 2.8, text: ['next stop:', 'MARS'], hl: 1, z: [1.0, 1.12]},
  ]},
  bxanywhere: {music: ['funkabn_n', 2], endSub: 'a home that goes anywhere', shots: [
    {img: 'dino', dur: 2.6, text: ['a T-REX found', 'its dream home'], hl: 0, z: [1.0, 1.12]},
    {img: 'west', dur: 2.6, text: ['delivered the', 'OLD-FASHIONED WAY'], hl: 1, z: [1.0, 1.12]},
    {img: 'alien', dur: 2.8, text: ['even ALIENS', 'want one'], hl: 0, z: [1.0, 1.1]},
  ]},
  bxpick: {music: ['chess_n', 40], endSub: 'where would YOU put yours?', endQ: 'comment your number 👇', shots: [
    {img: 'mars', dur: 1.7, text: ['where would YOU', 'put your BOXABL?'], hl: 1, z: [1.0, 1.08], num: '1'},
    {img: 'dino', dur: 1.5, text: ['the jungle'], z: [1.0, 1.08], num: '2'},
    {img: 'west', dur: 1.5, text: ['the desert'], z: [1.0, 1.08], num: '3'},
    {img: 'alien', dur: 1.5, text: ['the backyard'], z: [1.0, 1.08], num: '4'},
    {img: 'fly', dur: 1.5, text: ['the sky'], z: [1.0, 1.08], num: '5'},
    {img: 'unfold', dur: 1.7, text: ['your street'], z: [1.0, 1.1], num: '6', shake: true},
  ]},
};
const END = 2.8;
export const bxpFrames = (id: string) => BXP[id].shots.reduce((a, s) => a + S(s.dur), 0) + S(END);
const stroke = (w: number): React.CSSProperties => ({WebkitTextStroke: `${w}px #000`, paintOrder: 'stroke fill', textShadow: '0 8px 18px rgba(0,0,0,0.5)'});

export const BoxablPhoto: React.FC<{edit: string}> = ({edit}) => {
  const clip = BXP[edit], f = useCurrentFrame(), {fps} = useVideoConfig();
  const starts: number[] = []; clip.shots.reduce((a, s) => { starts.push(a); return a + S(s.dur); }, 0);
  const endAt = starts[starts.length - 1] + S(clip.shots[clip.shots.length - 1].dur);
  if (f >= endAt) {
    const lf = f - endAt, k = spring({frame: lf, fps, config: {damping: 12, stiffness: 200}});
    return <AbsoluteFill style={{background: '#fff'}}>
      <Img src={staticFile(`res/bxp/${clip.shots[0].img}.jpg`)} style={{position: 'absolute', left: 0, top: -8, width: 1080, height: 1935, filter: 'blur(6px) brightness(0.45)'}} />
      <div style={{position: 'absolute', top: 640, left: 0, right: 0, textAlign: 'center', transform: `scale(${0.6 + 0.4 * k})`}}>
        <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 190, letterSpacing: 18, color: '#fff', ...stroke(4)}}>BOXABL</div>
        <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 56, color: '#FFE14D', marginTop: 10, ...stroke(8)}}>{clip.endSub}</div>
        {clip.endQ && <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 52, color: '#fff', marginTop: 40, ...stroke(8)}}>{clip.endQ}</div>}
      </div>
      <Audio src={staticFile('res/m_meme-tada.mp3')} volume={0.3} />
    </AbsoluteFill>;
  }
  const si = starts.filter((s) => s <= f).length - 1, sh = clip.shots[si], lf = f - starts[si], n = S(sh.dur), info = IMG[sh.img];
  const z = interpolate(lf, [0, n], sh.z ?? [1, 1.1]);
  const [fx, fy] = [info.focus[0] * K, info.focus[1] * K];
  const whip = lf < 4 && f > 0 ? [-70, -28, -8, 0][lf] : 0, blur = lf < 3 && f > 0 ? [3, 1.5, 0][lf] : 0;
  const shake = sh.shake && lf < 24 ? Math.sin(lf * 2.6) * (24 - lf) * 0.6 : 0;
  const pop = spring({frame: lf, fps, config: {damping: 12, stiffness: 230}});
  const [sx, sy, sw] = info.sign;
  return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
    <AbsoluteFill style={{transform: `translate(${whip + shake}px, ${shake * 0.4}px) scale(${z})`, transformOrigin: `${fx}px ${fy}px`, filter: blur ? `blur(${blur}px)` : undefined}}>
      <Img src={staticFile(`res/bxp/${sh.img}.jpg`)} style={{position: 'absolute', left: 0, top: -8, width: 1080, height: 1935}} />
      {/* BOXABL sign on the house (spelled right, every shot) */}
      <div style={{position: 'absolute', left: (sx - sw / 2) * K, top: sy * K - sw * K * 0.11, width: sw * K, height: sw * K * 0.22, background: '#1c1f24', borderRadius: 6,
        display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 4px 10px rgba(0,0,0,0.4)'}}>
        <span style={{fontFamily: MONT, fontWeight: 800, color: '#fff', fontSize: sw * K * 0.13, letterSpacing: sw * K * 0.025}}>BOXABL</span>
      </div>
    </AbsoluteFill>
    {sh.num && <div style={{position: 'absolute', top: 560, left: 60, width: 150, height: 150, borderRadius: 75, background: '#FFE14D', border: '8px solid #000', display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontFamily: MONT, fontWeight: 800, fontSize: 96, color: '#000', transform: `scale(${pop})`}}>{sh.num}</div>}
    <div style={{position: 'absolute', top: sh.capY ?? 200, left: 40, right: 40, textAlign: 'center', transform: `scale(${0.75 + 0.25 * pop})`}}>
      {sh.text.map((l, i) => <div key={i} style={{fontFamily: MONT, fontWeight: 800, fontSize: i === sh.hl ? 104 : 78, lineHeight: 1.15, textTransform: l.includes('BOXABL') ? 'none' : 'uppercase',
        color: i === sh.hl ? '#FFE14D' : '#fff', ...stroke(i === sh.hl ? 14 : 11)}}>{l}</div>)}
    </div>
    <Audio src={staticFile(`res/${clip.music[0]}.mp3`)} startFrom={S(clip.music[1])} volume={0.4} />
    {starts.slice(1).map((s, i) => <Sequence key={i} from={Math.max(0, s - 16)}><Audio src={staticFile('res/m_fast-whoosh.mp3')} volume={0.28} /></Sequence>)}
    {clip.shots.map((s, i) => s.shake ? <Sequence key={'b' + i} from={starts[i]}><Audio src={staticFile('res/m_mg-boom.mp3')} volume={0.18} /></Sequence> : null)}
  </AbsoluteFill>;
};

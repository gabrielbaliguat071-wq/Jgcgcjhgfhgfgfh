// WEIRD HISTORY · EP. 1 — "The Great Emu War" v2 (1080x1920, 30 fps, ~72 s). Own SVG cartoon (bean-head characters),
// Kokoro narration (own channel, not a campaign), one-word captions. Facts + sources: stories/002-emu-war/SCRIPT.md (v2).
// Music: "Fluffing a Duck" Kevin MacLeod (incompetech.com), CC BY 4.0 — credit in the description. SFX: myinstants (public/sfx).
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, spring, staticFile, useCurrentFrame} from 'remotion';
import '../mgFonts';
import raw from '../inside/vo_emu2.words.json';

const FPS = 30, OFF = 400, INK = '#1d1a1f';
const W = (raw as {text: string; startMs: number; endMs: number}[]).map((w) => ({t: w.text, a: w.startMs + OFF, b: w.endMs + OFF}));
export const EMU2_MS = W[W.length - 1].b + 2600;
const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9,]/g, '').replace(/,$/, '');
const at = (word: string, n = 0) => W.filter((w) => norm(w.t) === norm(word))[n]?.a ?? 0;
export const cl = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const ease = (o: number, a: number, b: number) => interpolate(o, [a, b], [0, 1], {...cl, easing: (x) => x * x * (3 - 2 * x)});
export const pop = (o: number, ms: number, k = 180) => spring({frame: Math.max(0, (o - ms) / (1000 / FPS)), fps: FPS, config: {damping: 10, stiffness: k}});
export const blink = (o: number, seed = 0) => ((o + seed * 811) % 3100) < 110;

// ======================= characters =======================
export type Hat = 'slouch' | 'cap' | 'farmer' | 'none' | 'top' | 'beret' | 'bicorne' | 'plume' | 'bowler' | 'fedora' | 'hood' | 'bonnet' | 'doctor' | 'crown';
type BeanP = {x: number; y: number; s?: number; shirt?: string; pants?: string; hat?: Hat; mustache?: boolean; glasses?: boolean; mouth?: 'smile' | 'flat' | 'o' | 'frown' | 'grin' | 'talk' | 'yell';
  walk?: number; armL?: number; armR?: number; flip?: boolean; eyes?: 'dot' | 'wide' | 'tired' | 'closed' | 'squint' | 'cry'; brows?: 'none' | 'smug' | 'worried' | 'angry'; tilt?: number; sweat?: boolean;
  look?: number; o: number; seed?: number; uniform?: boolean; hold?: React.ReactNode; jump?: number; dress?: string; hair?: string; skin?: string; blush?: boolean};
export const Bean = ({x, y, s = 1, shirt = '#7b8b4a', pants = '#5b4a36', hat = 'slouch', mustache, glasses, mouth = 'smile', walk = 0, armL = 0.25, armR = -0.25, flip, eyes = 'dot', brows = 'none', tilt = 0, sweat, look = 0, o, seed = 0, uniform = true, hold, jump = 0, dress, hair, skin = '#fffdf8', blush}: BeanP) => {
  const sw = Math.sin(walk) * 0.5, bob = (walk ? Math.abs(Math.cos(walk)) * 7 : 0) + Math.sin(o / 520 + seed) * 2.5 + jump;
  const leg = (dx: number, a: number) => <g transform={`translate(${dx} -72) rotate(${a * 57})`}><rect x={-9} y={0} width={18} height={66} rx={9} fill={pants} stroke={INK} strokeWidth={6} /><path d="M-14 62 L22 62 Q28 76 14 78 L-14 78 Z" fill="#3a2a1e" stroke={INK} strokeWidth={5} /></g>;
  const arm = (dx: number, a: number, h?: React.ReactNode) => <g transform={`translate(${dx} -158) rotate(${a * 57})`}><rect x={-11} y={-4} width={22} height={80} rx={11} fill={shirt} stroke={INK} strokeWidth={6} /><circle cx={0} cy={84} r={13} fill="#fffdf8" stroke={INK} strokeWidth={5} />{h && <g transform="translate(0 90)">{h}</g>}</g>;
  const eb = blink(o, seed) && eyes !== 'closed' && eyes !== 'cry';
  const eye = (ex: number) => {
    if (eb || eyes === 'closed' || eyes === 'tired') return <path d={eyes === 'tired' ? `M${ex - 12} -4 L${ex + 12} -4` : `M${ex - 12} -2 Q${ex} 8 ${ex + 12} -2`} stroke={INK} strokeWidth={6} fill="none" strokeLinecap="round" />;
    if (eyes === 'squint') return <path d={`M${ex - 12} -8 L${ex + 12} -2`} stroke={INK} strokeWidth={6} strokeLinecap="round" />;
    if (eyes === 'cry') return <g><path d={`M${ex - 12} -2 Q${ex} -12 ${ex + 12} -2`} stroke={INK} strokeWidth={6} fill="none" strokeLinecap="round" /><path d={`M${ex} 4 Q${ex - 6} 30 ${ex} ${34 + (o / 8) % 20} Q${ex + 6} 30 ${ex} 4`} fill="#7fc8ff" /></g>;
    if (eyes === 'wide') return <g><circle cx={ex} cy={-4} r={17} fill="#fff" stroke={INK} strokeWidth={5} /><circle cx={ex + look * 6} cy={-4} r={7} fill={INK} /></g>;
    return <g><circle cx={ex + look * 5} cy={-4} r={9} fill={INK} /><circle cx={ex + look * 5 + 3} cy={-7} r={3} fill="#fff" /></g>;
  };
  const mouthEl = {smile: <path d="M-22 22 Q0 40 22 22" />, grin: <path d="M-28 14 Q0 56 28 14 Z" fill="#7a2a2a" />, flat: <path d="M-16 28 L16 28" />, frown: <path d="M-18 36 Q0 18 18 36" />,
    o: <ellipse cx={0} cy={30} rx={10} ry={13} fill="#7a2a2a" />, talk: <ellipse cx={0} cy={28} rx={15} ry={4 + 10 * Math.abs(Math.sin(o / 75))} fill="#7a2a2a" />,
    yell: <path d={`M-26 14 Q0 ${58 + Math.sin(o / 50) * 6} 26 14 Z`} fill="#7a2a2a" />}[mouth];
  const sh = (c: string) => c;
  return <g transform={`translate(${x} ${y}) scale(${(flip ? -1 : 1) * s} ${s})`}>
    <ellipse cx={0} cy={6} rx={70} ry={14} fill="rgba(0,0,0,0.18)" />
    <g transform={`translate(0 ${-bob}) rotate(${tilt})`}>
      {leg(-20, sw)}{leg(20, -sw)}
      <path d="M-56 -196 Q-60 -110 -52 -70 L52 -70 Q60 -110 56 -196 Q0 -214 -56 -196 Z" fill={sh(shirt)} stroke={INK} strokeWidth={8} />
      <path d="M20 -200 Q48 -196 56 -196 Q60 -110 52 -70 L30 -70 Q40 -130 20 -200 Z" fill="rgba(0,0,0,0.13)" />
      {uniform && <><rect x={-56} y={-104} width={112} height={16} fill="#4a3826" stroke={INK} strokeWidth={4} /><rect x={-10} y={-106} width={20} height={20} rx={3} fill="#d9b24a" stroke={INK} strokeWidth={3} />
        <rect x={-42} y={-172} width={28} height={22} rx={4} fill="rgba(0,0,0,0.12)" stroke={INK} strokeWidth={3} /><rect x={14} y={-172} width={28} height={22} rx={4} fill="rgba(0,0,0,0.12)" stroke={INK} strokeWidth={3} />
        {[-140, -124].map((by) => <circle key={by} cx={0} cy={by} r={4} fill="#d9b24a" stroke={INK} strokeWidth={2} />)}</>}
      {!uniform && <path d="M-20 -200 L0 -176 L20 -200" stroke={INK} strokeWidth={5} fill="none" />}
      {dress && <path d="M-56 -110 L-86 -10 Q0 10 86 -10 L56 -110 Z" fill={dress} stroke={INK} strokeWidth={8} />}
      {arm(-54, armL - sw * 0.6)}{arm(54, armR + sw * 0.6, hold)}
      <g transform="translate(0 -270)">
        {hair && <path d="M-72 -10 Q-80 -90 0 -86 Q80 -90 72 -10 L76 80 Q60 96 50 60 L-50 60 Q-60 96 -76 80 Z" fill={hair} stroke={INK} strokeWidth={7} />}
        <ellipse cx={0} cy={0} rx={66} ry={76} fill={skin} stroke={INK} strokeWidth={8} />
        {hair && <path d="M-64 -30 Q-40 -86 0 -80 Q40 -86 64 -30 Q30 -54 0 -50 Q-30 -54 -64 -30 Z" fill={hair} stroke={INK} strokeWidth={6} />}
        <path d="M30 -64 Q70 -20 50 50 Q40 70 20 74 Q60 20 30 -64 Z" fill="rgba(0,0,0,0.07)" />
        <ellipse cx={-40} cy={20} rx={12} ry={7} fill="rgba(255,120,110,0.35)" /><ellipse cx={40} cy={20} rx={12} ry={7} fill="rgba(255,120,110,0.35)" />
        {blush && <><ellipse cx={-42} cy={22} rx={18} ry={10} fill="rgba(255,80,80,0.55)" /><ellipse cx={42} cy={22} rx={18} ry={10} fill="rgba(255,80,80,0.55)" /></>}
        {eye(-25)}{eye(25)}
        {glasses && <g fill="none" stroke={INK} strokeWidth={5}><circle cx={-25} cy={-4} r={20} /><circle cx={25} cy={-4} r={20} /><path d="M-5 -6 L5 -6" /></g>}
        {brows !== 'none' && <g stroke={INK} strokeWidth={7} strokeLinecap="round">
          {brows === 'smug' && <><path d="M-40 -34 L-12 -28" /><path d="M12 -32 L40 -44" /></>}
          {brows === 'worried' && <><path d="M-40 -30 L-12 -42" /><path d="M12 -42 L40 -30" /></>}
          {brows === 'angry' && <><path d="M-40 -44 L-12 -30" /><path d="M12 -30 L40 -44" /></>}</g>}
        <g stroke={INK} strokeWidth={6} fill="none" strokeLinecap="round" strokeLinejoin="round">{mouthEl}</g>
        {mustache && <path d="M-34 14 Q-16 0 0 12 Q16 0 34 14 Q18 24 0 17 Q-18 24 -34 14 Z" fill="#5a3b22" stroke={INK} strokeWidth={4} />}
        {sweat && <path d={`M56 ${-44 + (o / 12) % 20} q10 18 0 24 q-10 -6 0 -24 Z`} fill="#8fd0ff" stroke={INK} strokeWidth={3} />}
        {hat === 'slouch' && <g><path d="M-96 -44 Q0 -72 96 -44 Q64 -30 0 -36 Q-64 -30 -96 -44 Z" fill="#9b8656" stroke={INK} strokeWidth={6} /><path d="M-54 -50 Q-50 -108 0 -112 Q50 -108 54 -50 Z" fill="#a8925f" stroke={INK} strokeWidth={6} /><rect x={-54} y={-62} width={108} height={12} fill="#5a4a2a" /><path d="M-54 -52 Q-80 -80 -70 -104 Q-50 -80 -54 -52 Z" fill="#9b8656" stroke={INK} strokeWidth={5} /></g>}
        {hat === 'cap' && <g><path d="M-60 -46 Q0 -116 60 -46 Z" fill="#6b6f3c" stroke={INK} strokeWidth={6} /><path d="M-62 -46 L76 -46 L88 -38 L-62 -38 Z" fill="#3e3f22" stroke={INK} strokeWidth={5} /><circle cx={0} cy={-76} r={10} fill="#e8c34a" stroke={INK} strokeWidth={3} /><path d="M-40 -56 L40 -56" stroke="#c9493c" strokeWidth={6} /></g>}
        {hat === 'farmer' && <g><ellipse cx={0} cy={-46} rx={100} ry={18} fill="#e5c56a" stroke={INK} strokeWidth={6} /><path d="M-52 -48 Q-48 -104 0 -106 Q48 -104 52 -48 Z" fill="#edd27c" stroke={INK} strokeWidth={6} /><rect x={-52} y={-64} width={104} height={12} fill="#b5463a" />{[-30, -10, 10, 30].map((hx) => <line key={hx} x1={hx} y1={-100} x2={hx - 4} y2={-66} stroke="#c9a94a" strokeWidth={3} />)}</g>}
        {hat === 'top' && <g><rect x={-46} y={-140} width={92} height={96} rx={6} fill="#2d2a2e" stroke={INK} strokeWidth={6} /><ellipse cx={0} cy={-46} rx={80} ry={14} fill="#2d2a2e" stroke={INK} strokeWidth={6} /><rect x={-46} y={-66} width={92} height={12} fill="#8a1f2a" /></g>}
        {hat === 'bicorne' && <g><path d="M-110 -40 Q-60 -120 0 -112 Q60 -120 110 -40 Q60 -64 0 -60 Q-60 -64 -110 -40 Z" fill="#1f1f2a" stroke={INK} strokeWidth={6} /><circle cx={0} cy={-80} r={14} fill="#2b4f9a" stroke="#fff" strokeWidth={4} /><path d="M-6 -80 L6 -80" stroke="#c9493c" strokeWidth={6} /></g>}
        {hat === 'plume' && <g><path d="M-104 -40 Q-50 -110 0 -104 Q50 -110 104 -40 Q50 -62 0 -58 Q-50 -62 -104 -40 Z" fill="#1f1f2a" stroke={INK} strokeWidth={6} /><path d="M20 -100 Q60 -170 -10 -170 Q40 -140 10 -100 Z" fill="#fff" stroke={INK} strokeWidth={5} /><path d="M10 -100 Q-30 -160 -70 -150 Q-20 -130 -4 -98 Z" fill="#c9493c" stroke={INK} strokeWidth={5} /></g>}
        {hat === 'bowler' && <g><ellipse cx={0} cy={-46} rx={84} ry={14} fill="#2d2a2e" stroke={INK} strokeWidth={6} /><path d="M-54 -48 Q-54 -112 0 -112 Q54 -112 54 -48 Z" fill="#2d2a2e" stroke={INK} strokeWidth={6} /><rect x={-54} y={-62} width={108} height={10} fill="#5a4a3a" /></g>}
        {hat === 'fedora' && <g><path d="M-100 -40 Q0 -64 100 -40 Q70 -30 0 -34 Q-70 -30 -100 -40 Z" fill="#3a3640" stroke={INK} strokeWidth={6} /><path d="M-56 -44 Q-56 -110 -10 -100 Q0 -88 10 -100 Q56 -110 56 -44 Z" fill="#46424c" stroke={INK} strokeWidth={6} /><rect x={-56} y={-58} width={112} height={12} fill="#1f1d22" /></g>}
        {hat === 'hood' && <g><path d="M-80 30 Q-90 -100 0 -104 Q90 -100 80 30 Q70 -60 0 -64 Q-70 -60 -80 30 Z" fill="#8a3a2a" stroke={INK} strokeWidth={6} /></g>}
        {hat === 'bonnet' && <g><path d="M-78 10 Q-86 -96 0 -100 Q86 -96 78 10 Q70 -50 0 -56 Q-70 -50 -78 10 Z" fill="#f4f0e6" stroke={INK} strokeWidth={6} /></g>}
        {hat === 'doctor' && <g><rect x={-50} y={-130} width={100} height={84} rx={14} fill="#2d2a2e" stroke={INK} strokeWidth={6} /><ellipse cx={0} cy={-46} rx={78} ry={14} fill="#2d2a2e" stroke={INK} strokeWidth={6} /></g>}
        {hat === 'crown' && <g><path d="M-56 -46 L-56 -110 L-28 -80 L0 -120 L28 -80 L56 -110 L56 -46 Z" fill="#ffd84a" stroke={INK} strokeWidth={6} strokeLinejoin="round" /></g>}
        {hat === 'beret' && <g><ellipse cx={-6} cy={-60} rx={70} ry={28} fill="#2d2a2e" stroke={INK} strokeWidth={6} /><circle cx={-6} cy={-90} r={6} fill="#2d2a2e" /></g>}
      </g>
    </g>
  </g>;
};

type EmuP = {x: number; y: number; s?: number; run?: number; peck?: number; flip?: boolean; hat?: boolean; o: number; eye?: 'dot' | 'angry' | 'happy' | 'smug' | 'wide'; seed?: number; tank?: boolean; dust?: boolean; kick?: number};
export const Emu = ({x, y, s = 1, run = 0, peck = 0, flip, hat, o, eye = 'dot', seed = 0, tank, dust, kick = 0}: EmuP) => {
  const sw = Math.sin(run) * 0.7, bob = run ? Math.abs(Math.cos(run)) * 12 : Math.sin(o / 430 + seed) * 3;
  const nb = peck * 90, eb = blink(o, seed + 3);
  const legEl = (dx: number, a: number) => <g transform={`translate(${dx} -96) rotate(${a * 57})`}><line x1={0} y1={0} x2={0} y2={92} stroke="#5b5348" strokeWidth={11} strokeLinecap="round" /><path d="M0 92 L-18 104 M0 92 L18 104 M0 92 L6 108" stroke="#5b5348" strokeWidth={7} strokeLinecap="round" /></g>;
  return <g transform={`translate(${x} ${y}) scale(${(flip ? -1 : 1) * s} ${s})`}>
    <ellipse cx={0} cy={12} rx={86} ry={14} fill="rgba(0,0,0,0.18)" />
    {dust && run !== 0 && [0, 1, 2].map((i) => { const p = ((o / 220 + i / 3 + seed) % 1); return <circle key={i} cx={-90 - p * 160} cy={-10 - p * 40} r={18 + p * 28} fill={`rgba(220,190,140,${0.55 * (1 - p)})`} />; })}
    <g transform={`translate(0 ${-bob})`}>
      {tank ? <g><rect x={-120} y={-70} width={240} height={70} rx={34} fill="#555b3a" stroke={INK} strokeWidth={8} />{[-80, -27, 27, 80].map((wx) => <circle key={wx} cx={wx} cy={-35} r={22} fill="#3a3d28" stroke={INK} strokeWidth={5} transform={`rotate(${o / 3} ${wx} -35)`} />)}</g>
        : <>{legEl(-16, sw)}{legEl(16, -sw + kick * -1.4)}</>}
      <ellipse cx={0} cy={-150} rx={96} ry={70} fill="#6a5240" stroke={INK} strokeWidth={8} />
      <path d="M-70 -170 Q-40 -220 20 -214 Q-20 -190 -70 -170 Z" fill="#7d6450" />
      {[-60, -32, -4, 24, 52].map((dx, i) => <path key={i} d={`M${dx} -182 q 16 30 -6 60`} stroke="#4b392b" strokeWidth={6} fill="none" strokeLinecap="round" />)}
      <path d="M-90 -130 q-30 10 -40 40 q20 -10 44 -10" fill="#5a4434" stroke={INK} strokeWidth={5} />
      <path d={`M66 -178 Q${102 + nb * 0.3} ${-250 + nb} ${88 + nb * 0.5} ${-310 + nb * 1.9}`} stroke={INK} strokeWidth={32} fill="none" strokeLinecap="round" />
      <path d={`M66 -178 Q${102 + nb * 0.3} ${-250 + nb} ${88 + nb * 0.5} ${-310 + nb * 1.9}`} stroke="#8aa1c8" strokeWidth={20} fill="none" strokeLinecap="round" />
      <g transform={`translate(${90 + nb * 0.5} ${-324 + nb * 1.9}) rotate(${peck * 70})`}>
        <ellipse cx={0} cy={0} rx={32} ry={26} fill="#7f6a56" stroke={INK} strokeWidth={6} />
        <path d="M-20 -22 q4 -16 12 -2 q4 -14 12 0" stroke="#4b392b" strokeWidth={5} fill="none" />
        <path d="M28 -4 L62 6 L28 14 Z" fill="#d8b46a" stroke={INK} strokeWidth={5} strokeLinejoin="round" />
        {eye === 'happy' || eb ? <path d="M2 -6 Q11 -15 20 -6" stroke={INK} strokeWidth={5} fill="none" strokeLinecap="round" />
          : eye === 'wide' ? <g><circle cx={11} cy={-6} r={12} fill="#fff" stroke={INK} strokeWidth={4} /><circle cx={13} cy={-6} r={5} fill={INK} /></g>
          : <g><circle cx={11} cy={-6} r={8} fill={INK} /><circle cx={14} cy={-9} r={2.5} fill="#fff" /></g>}
        {eye === 'angry' && <path d="M-2 -22 L24 -13" stroke={INK} strokeWidth={6} strokeLinecap="round" />}
        {eye === 'smug' && <path d="M-2 -16 L24 -20" stroke={INK} strokeWidth={6} strokeLinecap="round" />}
        {hat && <g transform="translate(-4 -20)"><path d="M-44 -6 Q0 -24 44 -6 Q22 2 0 -2 Q-22 2 -44 -6 Z" fill="#9b8656" stroke={INK} strokeWidth={5} /><path d="M-26 -8 Q-22 -48 0 -50 Q22 -48 26 -8 Z" fill="#a8925f" stroke={INK} strokeWidth={5} /><path d="M-26 -10 Q-46 -30 -38 -46 Q-24 -30 -26 -10 Z" fill="#9b8656" stroke={INK} strokeWidth={4} /></g>}
      </g>
    </g>
  </g>;
};
export const Rabbit = ({x, y, s = 1, o, seed = 0}: {x: number; y: number; s?: number; o: number; seed?: number}) => { const h = Math.abs(Math.sin(o / 160 + seed)) * 60;
  return <g transform={`translate(${x} ${y - h}) scale(${s})`}><ellipse cx={0} cy={-40} rx={46} ry={36} fill="#c9b8a6" stroke={INK} strokeWidth={6} /><circle cx={40} cy={-74} r={26} fill="#c9b8a6" stroke={INK} strokeWidth={6} />
    <ellipse cx={34} cy={-126} rx={10} ry={30} fill="#c9b8a6" stroke={INK} strokeWidth={5} /><ellipse cx={52} cy={-122} rx={10} ry={28} fill="#c9b8a6" stroke={INK} strokeWidth={5} /><circle cx={48} cy={-78} r={5} fill={INK} /><circle cx={-44} cy={-36} r={12} fill="#fff" stroke={INK} strokeWidth={4} /></g>; };

// ======================= world =======================
export const Defs = () => <defs>
  <linearGradient id="skyD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#6cbcf0" /><stop offset="1" stopColor="#ffe7b8" /></linearGradient>
  <linearGradient id="skyS" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#f2865a" /><stop offset="1" stopColor="#ffd59a" /></linearGradient>
  <radialGradient id="vig" cx="0.5" cy="0.45" r="0.75"><stop offset="0.6" stopColor="rgba(0,0,0,0)" /><stop offset="1" stopColor="rgba(0,0,0,0.35)" /></radialGradient>
  <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={3} /><feColorMatrix values="0 0 0 0 0.3 0 0 0 0 0.25 0 0 0 0 0.2 0 0 0 0.09 0" /></filter>
</defs>;
export const Cloud = ({x, y, s = 1}: {x: number; y: number; s?: number}) => <g transform={`translate(${x} ${y}) scale(${s})`}><path d="M-120 20 Q-130 -30 -70 -30 Q-60 -80 0 -70 Q40 -110 90 -60 Q150 -60 140 0 Q150 30 110 30 L-100 30 Q-130 30 -120 20 Z" fill="#fff" stroke={INK} strokeWidth={6} /><path d="M-90 20 L100 20" stroke="#dfeaf2" strokeWidth={10} /></g>;
export const Sky = ({o, sunset, sun = true}: {o: number; sunset?: boolean; sun?: boolean}) => <>
  <rect x={-800} y={-800} width={2700} height={3500} fill={sunset ? 'url(#skyS)' : 'url(#skyD)'} />
  {sun && <g transform={`translate(${sunset ? 760 : 960} ${sunset ? 760 : 700}) rotate(${o / 60})`}>{Array.from({length: 12}, (_, i) => <path key={i} d="M0 -150 L14 -118 L-14 -118 Z" fill={sunset ? '#ffb35a' : '#ffd84a'} stroke={INK} strokeWidth={4} transform={`rotate(${i * 30})`} />)}<circle r={100} fill={sunset ? '#ff9f4a' : '#ffd84a'} stroke={INK} strokeWidth={8} /></g>}
  <Cloud x={((o / 18) % 1600) - 300} y={220} s={0.9} /><Cloud x={((o / 26 + 900) % 1700) - 350} y={430} s={0.6} />
</>;
export const Hills = ({y, green, o}: {y: number; green?: boolean; o: number}) => { const far = green ? '#a9cf7a' : '#e9c08a', mid = green ? '#93bd5f' : '#dcae6e';
  return <>
    <path d={`M-400 ${y - 140} Q100 ${y - 260} 500 ${y - 150} Q900 ${y - 60} 1500 ${y - 180} L1500 ${y + 200} L-400 ${y + 200} Z`} fill={far} stroke={INK} strokeWidth={6} />
    <path d={`M-400 ${y - 40} Q300 ${y - 130} 800 ${y - 50} Q1200 ${y} 1500 ${y - 70} L1500 ${y + 200} L-400 ${y + 200} Z`} fill={mid} stroke={INK} strokeWidth={6} />
  </>; };
export const Ground = ({y, green, o}: {y: number; green?: boolean; o: number}) => { const c = green ? '#86b452' : '#e0a95c', c2 = green ? '#6f9a40' : '#c98d45';
  return <>
    <path d={`M-600 ${y} Q300 ${y - 50} 1100 ${y - 10} Q1500 ${y + 20} 1800 ${y - 30} L1800 2800 L-600 2800 Z`} fill={c} stroke={INK} strokeWidth={8} />
    {Array.from({length: 30}, (_, i) => { const gx = (i * 193) % 1500 - 200, gy = y + 60 + (i * 127) % 700, sway = Math.sin(o / 400 + i) * 4;
      return <path key={i} d={`M${gx} ${gy} l${-10 + sway} -34 M${gx + 10} ${gy} l${sway} -46 M${gx + 20} ${gy} l${10 + sway} -32`} stroke={c2} strokeWidth={7} strokeLinecap="round" />; })}
    {Array.from({length: 8}, (_, i) => <ellipse key={'r' + i} cx={(i * 311) % 1300 - 100} cy={y + 200 + (i * 211) % 600} rx={26} ry={14} fill="#b8a48a" stroke={INK} strokeWidth={4} />)}
  </>; };
export const GumTree = ({x, y, s = 1, o}: {x: number; y: number; s?: number; o: number}) => <g transform={`translate(${x} ${y}) scale(${s}) rotate(${Math.sin(o / 900 + x) * 1.5})`}>
  <path d="M-16 0 Q-6 -140 -10 -270 L12 -270 Q8 -140 18 0 Z" fill="#efe4d0" stroke={INK} strokeWidth={6} /><path d="M0 -190 Q40 -230 70 -250" stroke={INK} strokeWidth={10} fill="none" />
  <ellipse cx={-50} cy={-300} rx={120} ry={72} fill="#6f9a52" stroke={INK} strokeWidth={7} /><ellipse cx={70} cy={-330} rx={104} ry={66} fill="#83ad5f" stroke={INK} strokeWidth={7} /><ellipse cx={0} cy={-390} rx={96} ry={58} fill="#96c06d" stroke={INK} strokeWidth={7} /></g>;
export const Wheat = ({x, y, w = 900, eaten = 0, grow = 1, o}: {x: number; y: number; w?: number; eaten?: number; grow?: number; o: number}) => <g>{Array.from({length: Math.floor(w / 24)}, (_, i) => {
  const h = ((i * 37) % 3 === 0 ? 160 : 135) * grow, gone = (i / (w / 24)) < eaten, sway = Math.sin(o / 350 + i * 0.4) * 8;
  return gone ? <line key={i} x1={x + i * 24} y1={y} x2={x + i * 24} y2={y - 22} stroke="#a8803a" strokeWidth={8} strokeLinecap="round" />
    : <g key={i}><path d={`M${x + i * 24} ${y} Q${x + i * 24 + sway / 2} ${y - h / 2} ${x + i * 24 + sway} ${y - h}`} stroke="#c99a3c" strokeWidth={8} fill="none" strokeLinecap="round" />
      {grow > 0.6 && <ellipse cx={x + i * 24 + sway} cy={y - h - 14} rx={11} ry={25} fill="#f0c95a" stroke={INK} strokeWidth={5} />}</g>; })}</g>;
export const Fence = ({x, y, n = 8, broken = 0, o}: {x: number; y: number; n?: number; broken?: number; o: number}) => <g>{Array.from({length: n}, (_, i) => { const br = i >= 3 && i <= 4 ? broken : 0;
  return <g key={i} transform={`translate(${x + i * 130 + br * (i === 3 ? -200 : 260)} ${y - br * 300 + br * br * 500}) rotate(${br * (i === 3 ? -200 : 240)})`}><rect x={-14} y={-150} width={28} height={150} fill="#b08050" stroke={INK} strokeWidth={6} /></g>; })}
  <rect x={x - 20} y={y - 120} width={n * 130} height={20} fill="#c9955f" stroke={INK} strokeWidth={5} opacity={1 - broken} /><rect x={x - 20} y={y - 60} width={n * 130} height={20} fill="#c9955f" stroke={INK} strokeWidth={5} opacity={1 - broken} /></g>;
export const Farmhouse = ({x, y}: {x: number; y: number}) => <g transform={`translate(${x} ${y})`}><rect x={-170} y={-230} width={340} height={230} fill="#efe6d2" stroke={INK} strokeWidth={8} /><path d="M-200 -230 L0 -380 L200 -230 Z" fill="#b5463a" stroke={INK} strokeWidth={8} strokeLinejoin="round" />
  {Array.from({length: 6}, (_, i) => <line key={i} x1={-200 + i * 70} y1={-230} x2={-120 + i * 40} y2={-300} stroke="#8d3229" strokeWidth={5} />)}<rect x={90} y={-360} width={44} height={90} fill="#8a6a54" stroke={INK} strokeWidth={6} />
  <rect x={-42} y={-130} width={84} height={130} fill="#6b4a2c" stroke={INK} strokeWidth={6} /><circle cx={24} cy={-64} r={6} fill="#d9b24a" /><rect x={-140} y={-180} width={66} height={60} fill="#8fd0ff" stroke={INK} strokeWidth={6} /><rect x={74} y={-180} width={66} height={60} fill="#8fd0ff" stroke={INK} strokeWidth={6} /><path d="M-140 -150 L-74 -150 M-107 -180 L-107 -120 M74 -150 L140 -150 M107 -180 L107 -120" stroke={INK} strokeWidth={4} /></g>;
export const Crate = ({x, y, label, s = 1}: {x: number; y: number; label?: string; s?: number}) => <g transform={`translate(${x} ${y}) scale(${s})`}><rect x={-100} y={-120} width={200} height={120} fill="#c79a5a" stroke={INK} strokeWidth={7} /><path d="M-100 -120 L100 0 M100 -120 L-100 0" stroke="#a87c42" strokeWidth={6} /><rect x={-100} y={-120} width={200} height={120} fill="none" stroke={INK} strokeWidth={7} />{label && <g><rect x={-80} y={-80} width={160} height={50} fill="#f4e6c4" stroke={INK} strokeWidth={4} /><text x={0} y={-43} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={34} fill={INK}>{label}</text></g>}</g>;
const Gun = ({x, y, s = 1, flash = 0, smoke = 0, rot = 0}: {x: number; y: number; s?: number; flash?: number; smoke?: number; rot?: number}) => <g transform={`translate(${x} ${y}) scale(${s}) rotate(${rot})`}>
  <line x1={-30} y1={0} x2={-70} y2={-90} stroke={INK} strokeWidth={10} /><line x1={30} y1={0} x2={70} y2={-90} stroke={INK} strokeWidth={10} />
  <rect x={-100} y={-140} width={220} height={48} rx={12} fill="#4d5530" stroke={INK} strokeWidth={7} /><rect x={120} y={-128} width={130} height={20} fill="#3b3f26" stroke={INK} strokeWidth={5} /><circle cx={-30} cy={-162} r={32} fill="#4d5530" stroke={INK} strokeWidth={6} />
  {flash > 0 && <path d="M255 -118 l60 -40 l-20 34 l70 -6 l-66 26 l52 36 l-70 -20 Z" fill="#ffd84a" stroke={INK} strokeWidth={5} opacity={flash} />}
  {smoke > 0 && [0, 1, 2].map((i) => <circle key={i} cx={260 + i * 40 * smoke} cy={-130 - i * 50 * smoke} r={30 + i * 14} fill="#ddd" stroke={INK} strokeWidth={5} opacity={1 - smoke * 0.6} />)}</g>;
const Truck = ({x, y, shake = 0, o, s = 1}: {x: number; y: number; shake?: number; o: number; s?: number}) => { const dy = Math.sin(o / 45) * shake, rot = Math.sin(o / 60) * shake * 0.25, wr = o / 40;
  return <g transform={`translate(${x} ${y + dy}) rotate(${rot}) scale(${s})`}>
    <rect x={-300} y={-260} width={420} height={170} rx={16} fill="#7b8b4a" stroke={INK} strokeWidth={8} /><path d="M-300 -200 L120 -200" stroke="#66763c" strokeWidth={8} />
    <path d="M120 -260 L230 -260 L290 -170 L290 -90 L120 -90 Z" fill="#6e7d40" stroke={INK} strokeWidth={8} strokeLinejoin="round" /><path d="M140 -245 L220 -245 L262 -180 L140 -180 Z" fill="#8fd0ff" stroke={INK} strokeWidth={6} /><circle cx={282} cy={-110} r={12} fill="#ffe08a" stroke={INK} strokeWidth={4} />
    {[-190, 190].map((wx, i) => <g key={i} transform={`translate(${wx} -80) rotate(${wr * 57})`}><circle r={64} fill="#2d2a2e" stroke={INK} strokeWidth={8} /><circle r={26} fill="#bbb" stroke={INK} strokeWidth={5} /><line x1={-26} y1={0} x2={26} y2={0} stroke={INK} strokeWidth={5} /><line x1={0} y1={-26} x2={0} y2={26} stroke={INK} strokeWidth={5} /></g>)}
    {[0, 1].map((i) => { const p = ((o / 260 + i * 0.5) % 1); return <circle key={'d' + i} cx={-330 - p * 200} cy={-40 - p * 50} r={24 + p * 34} fill={`rgba(220,190,140,${0.6 * (1 - p)})`} />; })}
  </g>; };
export const SpeedLines = ({o, n = 14, c = '#fff'}: {o: number; n?: number; c?: string}) => <g opacity={0.55}>{Array.from({length: n}, (_, i) => { const yy = 200 + (i * 131) % 1500, xx = ((o * 2.4 + i * 300) % 1700) - 300; return <line key={i} x1={xx} y1={yy} x2={xx + 280} y2={yy} stroke={c} strokeWidth={10} strokeLinecap="round" />; })}</g>;
export const Burst = ({o, c1 = '#ffd84a', c2 = '#ffb84a', cx = 540, cy = 1100}: {o: number; c1?: string; c2?: string; cx?: number; cy?: number}) => <g><rect x={-200} y={-200} width={1480} height={2320} fill={c1} />{Array.from({length: 18}, (_, i) => { const an = (i / 18) * Math.PI * 2 + o / 5000; return <path key={i} d={`M${cx} ${cy} L${cx + Math.cos(an) * 2200} ${cy + Math.sin(an) * 2200} L${cx + Math.cos(an + 0.17) * 2200} ${cy + Math.sin(an + 0.17) * 2200} Z`} fill={c2} />; })}</g>;
export const Feathers = ({o, t0, cx, cy, n = 8}: {o: number; t0: number; cx: number; cy: number; n?: number}) => { const p = Math.max(0, (o - t0) / 1400); if (p <= 0 || p > 1) return null;
  return <g>{Array.from({length: n}, (_, i) => { const an = (i / n) * Math.PI * 2, d = 220 * p; return <path key={i} d="M0 0 q12 -30 0 -60 q-12 30 0 60" fill="#6a5240" stroke={INK} strokeWidth={3} transform={`translate(${cx + Math.cos(an) * d} ${cy + Math.sin(an) * d + p * p * 260}) rotate(${an * 57 + o / 4})`} opacity={1 - p} />; })}</g>; };
export const Card = ({text, sub, k}: {text: string; sub?: string; k: number}) => <g transform={`translate(540 760) scale(${k}) rotate(${-4 * (1 - k)})`}><rect x={-300} y={-120} width={600} height={sub ? 280 : 220} rx={26} fill="#f4e6c4" stroke={INK} strokeWidth={10} /><rect x={-300} y={-120} width={600} height={40} rx={20} fill="#c9493c" stroke={INK} strokeWidth={8} />
  <text x={0} y={46} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={120} fill={INK}>{text}</text>{sub && <text x={0} y={130} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={48} fill="#8a3a2a">{sub}</text>}</g>;
export const Bubble = ({x, y, children, k = 1, w = 300, h = 200}: {x: number; y: number; children: React.ReactNode; k?: number; w?: number; h?: number}) => <g transform={`translate(${x} ${y}) scale(${k})`}><path d={`M${-w / 2} ${-h} h${w} q30 0 30 30 v${h - 60} q0 30 -30 30 h${-w + 90} l-50 50 l10 -50 h${-50} q-30 0 -30 -30 v${-h + 60} q0 -30 30 -30 Z`} fill="#fff" stroke={INK} strokeWidth={7} />{children}</g>;
const Australia = ({k}: {k: number}) => <g transform={`translate(540 1000) scale(${1.15 * k})`}>
  <path d="M-330 -60 Q-320 -150 -220 -190 Q-150 -260 -80 -230 Q-30 -300 30 -250 Q70 -320 120 -260 Q150 -200 190 -230 Q230 -170 280 -130 Q330 -60 320 30 Q300 120 230 170 Q160 230 70 210 Q20 260 -40 220 Q-90 180 -160 190 Q-250 200 -300 130 Q-350 60 -330 -60 Z" fill="#e9b26a" stroke={INK} strokeWidth={10} strokeLinejoin="round" />
  <path d="M150 260 Q190 250 200 290 Q170 320 140 295 Z" fill="#e9b26a" stroke={INK} strokeWidth={8} /><path d="M-100 -230 Q-110 -100 -100 200" stroke="#c98d45" strokeWidth={6} strokeDasharray="18 14" fill="none" />
</g>;
export const Coin = ({x, y, k}: {x: number; y: number; k: number}) => <g transform={`translate(${x} ${y}) scale(${k})`}><circle r={46} fill="#ffd84a" stroke={INK} strokeWidth={7} /><circle r={32} fill="none" stroke="#d9a830" strokeWidth={5} /><text y={16} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={44} fill="#8a6a20">$</text></g>;
const Bullet = ({x, y, k}: {x: number; y: number; k: number}) => <g transform={`translate(${x} ${y}) scale(${k})`}><rect x={-14} y={-30} width={28} height={50} rx={4} fill="#c79a3a" stroke={INK} strokeWidth={5} /><path d="M-14 -30 Q0 -70 14 -30 Z" fill="#b87333" stroke={INK} strokeWidth={5} /></g>;
const Camera = ({x, y, o}: {x: number; y: number; o: number}) => <g transform={`translate(${x} ${y})`}><line x1={0} y1={0} x2={-60} y2={180} stroke={INK} strokeWidth={10} /><line x1={0} y1={0} x2={60} y2={180} stroke={INK} strokeWidth={10} /><line x1={0} y1={0} x2={0} y2={180} stroke={INK} strokeWidth={10} />
  <rect x={-90} y={-110} width={180} height={110} rx={10} fill="#3a3a40" stroke={INK} strokeWidth={7} /><rect x={90} y={-80} width={60} height={50} fill="#2d2a2e" stroke={INK} strokeWidth={6} />{[-50, 40].map((rx) => <g key={rx} transform={`translate(${rx} -150) rotate(${o / 3})`}><circle r={46} fill="#2d2a2e" stroke={INK} strokeWidth={6} />{[0, 1, 2].map((i) => <circle key={i} cx={Math.cos(i * 2.09) * 24} cy={Math.sin(i * 2.09) * 24} r={9} fill="#777" />)}</g>)}
  <g transform={`translate(-90 -60) rotate(${o / 2})`}><line x1={0} y1={0} x2={-40} y2={0} stroke={INK} strokeWidth={8} /><circle cx={-40} cy={0} r={8} fill={INK} /></g></g>;

// ======================= shots =======================
type ShotFn = (o: number, t: number, a: number, b: number) => React.ReactNode;
export const camWrap = (z: number, cx: number, cy: number, node: React.ReactNode, dx = 0, dy = 0) => <g transform={`translate(${cx + dx} ${cy + dy}) scale(${z}) translate(${-cx} ${-cy})`}>{node}</g>;
const SH: [string, number, ShotFn][] = [
  ['hook', 0, (o, t) => camWrap(1 + 0.1 * t, 540, 1000, <><Sky o={o} /><Burst o={o} c1="#bfe3f7" c2="#d6eefa" cy={1000} /><Australia k={pop(o, 150, 120)} />
    <g transform={`translate(${540 - 200} ${1000 - 120})`}><path d="M0 0 L0 -160" stroke={INK} strokeWidth={10} /><path d="M0 -160 L120 -130 L0 -100 Z" fill="#c9493c" stroke={INK} strokeWidth={6} /><circle r={18} fill="#c9493c" stroke={INK} strokeWidth={6} /></g>
    <g transform={`translate(540 520) scale(${pop(o, at('1932'), 200)})`}><rect x={-200} y={-90} width={400} height={150} rx={18} fill="#f4e6c4" stroke={INK} strokeWidth={9} /><text x={0} y={36} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={120} fill={INK}>1932</text></g>
    <Bean x={260} y={1700} s={1.25} armR={-2.7} mouth="flat" brows="angry" o={o} /><Bean x={820} y={1700} s={1.25} armL={2.7} flip mouth="flat" brows="angry" o={o} seed={2} /></>)],
  ['smug', at('birds'), (o, t, a) => <>{camWrap(1.05 + 0.05 * t, 540, 1100, <><Burst o={o} /><Emu x={480} y={1500} s={2.3} eye="smug" o={o} /></>)}
    {o > at('lost') && <g transform={`translate(540 640) scale(${pop(o, at('lost'), 240)}) rotate(-8)`}><rect x={-230} y={-90} width={460} height={170} rx={16} fill="none" stroke="#c9493c" strokeWidth={14} /><text x={0} y={40} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={130} fill="#c9493c">LOST</text></g>}</>],
  ['farm', at('after'), (o, t) => { const farmer = o > at('land'); return camWrap(1 + 0.08 * t, 540, 1300, <><Sky o={o} /><Hills y={1180} green o={o} /><Ground y={1200} green o={o} /><Farmhouse x={790} y={1210} /><GumTree x={120} y={1220} s={0.7} o={o} />
    <Wheat x={-40} y={1560} w={1200} grow={ease(o, at('wheat') - 300, at('wheat') + 500)} o={o} />
    <Bean x={interpolate(t, [0, 0.45], [-100, 420], cl)} y={1680} s={1.3} hat={farmer ? 'farmer' : 'slouch'} shirt={farmer ? '#c9493c' : '#7b8b4a'} pants={farmer ? '#3f5b8a' : '#5b4a36'} uniform={!farmer} walk={t < 0.45 ? o / 130 : 0} mouth="grin" armR={farmer ? -2.4 : -0.25} o={o} />
    {o > at('land') && o < at('land') + 500 && <circle cx={420} cy={1330} r={60 + (o - at('land')) / 4} fill="none" stroke="#fff" strokeWidth={10} opacity={1 - (o - at('land')) / 500} />}</>); }],
  ['horde', at('then'), (o, t, a) => camWrap(1 + 0.06 * t, 540, 1200, <><Sky o={o} /><Hills y={1180} green o={o} /><Ground y={1200} green o={o} /><Farmhouse x={850} y={1210} /><Wheat x={-40} y={1560} w={1200} o={o} />
    {Array.from({length: 14}, (_, i) => { const x = interpolate(o - a - i * 80, [0, 1800], [1400 + (i % 5) * 120, 80 + (i % 7) * 150], cl); return <Emu key={i} x={x} y={1300 + (i % 4) * 70} s={0.55} run={o / 70 + i} flip dust o={o} seed={i} />; })}
    <g transform={`translate(540 560) scale(${pop(o, at('20,000'), 200)})`}><rect x={-260} y={-100} width={520} height={170} rx={20} fill="#c9493c" stroke={INK} strokeWidth={9} /><text x={0} y={32} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={110} fill="#fff">20,000</text></g>
    <Bean x={170} y={1800} s={1.0} hat="farmer" shirt="#c9493c" pants="#3f5b8a" uniform={false} eyes="wide" look={1} mouth="o" sweat armL={1.0} armR={-1.0} o={o} /></>)],
  ['ate', at('they'), (o, t, a) => camWrap(1.15, 540, 1500, <><Sky o={o} /><Ground y={1150} green o={o} /><Wheat x={-40} y={1560} w={1200} eaten={ease(o, a, a + 900)} o={o} />
    {Array.from({length: 5}, (_, i) => <Emu key={i} x={120 + i * 220} y={1600} s={0.75} peck={(Math.sin(o / 110 + i) + 1) / 2} o={o} seed={i} />)}</>)],
  ['fence', at('they', 1), (o, t, a) => camWrap(1.1, 540, 1400, <><Sky o={o} /><Hills y={1150} green o={o} /><Ground y={1200} green o={o} /><Fence x={-30} y={1560} broken={ease(o, a + 250, a + 750)} o={o} />
    <Emu x={520} y={1700} s={1.05} eye="angry" kick={Math.sin(Math.min(1, (o - a) / 300) * Math.PI)} o={o} />{o > a + 250 && o < a + 700 && <text x={700} y={1240} fontFamily="Inter" fontWeight={800} fontSize={110} fill="#fff" stroke={INK} strokeWidth={10} paintOrder="stroke" transform="rotate(-10 700 1240)">CRACK!</text>}</>)],
  ['rabbits', at('and', 1), (o, t, a) => camWrap(1.05, 540, 1400, <><Sky o={o} /><Hills y={1150} green o={o} /><Ground y={1200} green o={o} /><Fence x={-30} y={1560} broken={1} o={o} /><Wheat x={-40} y={1820} w={1200} eaten={ease(o, a + 600, a + 1800) * 0.7} o={o} />
    {Array.from({length: 6}, (_, i) => <Rabbit key={i} x={interpolate(o - a - i * 200, [0, 1500], [380, 380 + (i % 3 - 1) * 260 + 60], cl)} y={interpolate(o - a - i * 200, [0, 1500], [1480, 1760 + (i % 2) * 80], cl)} s={0.8} o={o} seed={i} />)}</>)],
  ['minister', at('so'), (o, t, a) => camWrap(1 + 0.05 * t, 540, 1200, <><rect x={-200} y={-200} width={1480} height={2320} fill="#e9dcc0" /><rect x={-200} y={1380} width={1480} height={800} fill="#8a6a44" stroke={INK} strokeWidth={8} />
    {Array.from({length: 7}, (_, i) => <line key={i} x1={-200 + i * 220} y1={-200} x2={-200 + i * 220} y2={1380} stroke="#dfd0b0" strokeWidth={18} />)}
    <g transform="translate(830 520)"><rect x={-130} y={-90} width={260} height={180} fill="#2b3f7a" stroke={INK} strokeWidth={7} /><rect x={-130} y={-90} width={120} height={80} fill="#c9493c" stroke={INK} strokeWidth={5} /><line x1={-130} y1={-90} x2={-130} y2={300} stroke={INK} strokeWidth={10} /></g>
    <rect x={430} y={1180} width={600} height={60} fill="#6b4a2c" stroke={INK} strokeWidth={8} /><rect x={470} y={1240} width={520} height={260} fill="#7a5532" stroke={INK} strokeWidth={8} />
    <Bean x={760} y={1180} s={1.1} hat="none" glasses shirt="#2d2a2e" pants="#2d2a2e" uniform={false} mouth={o > at('guns') ? 'o' : 'flat'} eyes={o > at('guns') ? 'wide' : 'dot'} brows="worried" o={o} seed={4} />
    <Bean x={260} y={1700} s={1.3} hat="farmer" shirt="#c9493c" pants="#3f5b8a" uniform={false} mouth={o > at('asked') ? 'yell' : 'talk'} brows="angry" armR={o > at('asked') ? -1.6 - Math.abs(Math.sin(o / 120)) * 0.4 : -0.3} o={o} />
    {o > at('machine') && <Bubble x={420} y={760} k={pop(o, at('machine'))} w={340} h={220}><g transform="translate(20 -100) scale(0.55)"><Gun x={-40} y={60} /></g><text x={20} y={-10} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={52} fill="#c9493c">x2!!</text></Bubble>}</>)],
  ['army', at('the', 6), (o, t, a) => camWrap(1, 540, 1200, <><Sky o={o} /><Hills y={1220} o={o} /><Ground y={1250} o={o} /><GumTree x={980} y={1260} s={0.7} o={o} />
    {(() => { const k = pop(o, at('major')); return <g transform={`translate(540 1700) scale(${k}) translate(-540 -1700)`}><Bean x={540} y={1700} s={1.35} hat="cap" mustache shirt="#6b6f3c" pants="#3e3f22" mouth="grin" brows="smug" armR={-2.6} o={o} seed={1} /></g>; })()}
    {[0, 1].map((i) => { const k = pop(o, at('soldiers', 1) + i * 140); return <g key={i} transform={`translate(${200 + i * 680} 1640) scale(${k}) translate(${-(200 + i * 680)} -1640)`}><Bean x={200 + i * 680} y={1640} s={1.05} armR={-2.6} flip={i === 1} mouth="grin" o={o} seed={i + 5} /></g>; })}
    {[0, 1].map((i) => { const k = pop(o, at('two', 1) + i * 150); return <g key={'g' + i} transform={`translate(${260 + i * 520} 1250) scale(${k}) translate(${-(260 + i * 520)} -1250)`}><Gun x={260 + i * 520} y={1250} s={0.95} /></g>; })}
    {(() => { const k = pop(o, at('10,000')); return <g transform={`translate(540 1960) scale(${k}) translate(-540 -1960)`}><Crate x={330} y={1900} label="10,000" s={1.1} /><Crate x={560} y={1900} label="BULLETS" s={1.1} /><Crate x={790} y={1900} s={1.1} /></g>; })()}</>)],
  ['camera', at('they', 2), (o, t, a) => camWrap(1 + 0.08 * t, 540, 1300, <><Sky o={o} /><Hills y={1220} o={o} /><Ground y={1250} o={o} />
    <Camera x={720} y={1460} o={o} /><Bean x={420} y={1720} s={1.25} hat="beret" shirt="#3a5a8a" pants="#2d2a2e" uniform={false} mouth="grin" eyes="squint" armR={-1.4 + Math.sin(o / 90) * 0.5} o={o} />
    <g transform={`translate(540 520) scale(${pop(o, at('victory'))})`}><rect x={-280} y={-80} width={560} height={140} rx={16} fill="#2d2a2e" stroke={INK} strokeWidth={8} /><text x={0} y={22} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={72} fill="#ffd84a">"VICTORY"</text></g></>)],
  ['day1', at('day'), (o, t, a) => <>{camWrap(1, 540, 1200, <><Sky o={o} /><Hills y={1220} o={o} /><Ground y={1250} o={o} />
    {Array.from({length: 6}, (_, i) => <Emu key={i} x={interpolate(o - a, [800, 3200], [500 + i * 90, 1400 + i * 90], cl)} y={1320 + (i % 2) * 40} s={0.4} run={o > a + 800 ? o / 60 + i : 0} dust o={o} seed={i} />)}
    <Bean x={240} y={1760} s={1.25} eyes="squint" mouth="flat" brows="angry" armL={-2.2} armR={2.2} o={o} hold={undefined} />
    <g transform="translate(240 1490)"><rect x={-60} y={-24} width={50} height={40} rx={8} fill="#2d2a2e" stroke={INK} strokeWidth={5} /><rect x={10} y={-24} width={50} height={40} rx={8} fill="#2d2a2e" stroke={INK} strokeWidth={5} /></g></>)}
    {o < a + 900 && <Card text="DAY 1" k={pop(o, a, 220)} />}</>],
  ['day3', at('day', 1), (o, t, a) => <>{camWrap(1, 540, 1200, <><Sky o={o} /><Hills y={1180} o={o} /><Ground y={1200} o={o} /><ellipse cx={600} cy={1520} rx={380} ry={110} fill="#6fb6e0" stroke={INK} strokeWidth={8} /><ellipse cx={560} cy={1500} rx={240} ry={40} fill="#9fd3f0" />
    {Array.from({length: 16}, (_, i) => <Emu key={i} x={interpolate(o - a, [600, 3600], [1300 + (i % 6) * 120, 520 + (i % 6) * 110], cl)} y={1300 + Math.floor(i / 6) * 80} s={0.45} run={o / 90 + i} flip o={o} seed={i} />)}
    <ellipse cx={130} cy={1820} rx={220} ry={130} fill="#6f9a52" stroke={INK} strokeWidth={8} /><g transform="translate(150 1820)"><Bean x={0} y={60} s={0.9} mouth="grin" brows="smug" eyes="squint" o={o} /></g><ellipse cx={130} cy={1900} rx={230} ry={90} fill="#83ad5f" stroke={INK} strokeWidth={8} /></>)}
    {o < a + 900 && <Card text="DAY 3" k={pop(o, a, 220)} />}
    <g transform={`translate(540 640) scale(${pop(o, at('1,000'))})`}><rect x={-230} y={-80} width={460} height={140} rx={18} fill="#c9493c" stroke={INK} strokeWidth={8} /><text x={0} y={30} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={96} fill="#fff">~1,000</text></g></>],
  ['fire', at('the', 9), (o, t, a) => { const sh = Math.sin(o / 25) * 10; return camWrap(1.05, 540, 1300, <><Sky o={o} /><Ground y={1200} o={o} />
    {Array.from({length: 8}, (_, i) => { const p = ease(o, a + 200, a + 1100); return <Emu key={i} x={560 + (i % 4) * 150 + p * (i % 2 ? 200 : -50)} y={1420 + Math.floor(i / 4) * 140 - Math.abs(Math.sin(o / 90 + i)) * 120 * p} s={0.5} eye="wide" run={o / 60 + i} o={o} seed={i} />; })}
    <Feathers o={o} t0={a + 300} cx={740} cy={1300} n={10} /><g transform={`translate(${sh} 0)`}><Gun x={200} y={1700} s={1.1} flash={Math.floor(o / 70) % 2} /><Bean x={60} y={1820} s={1.0} mouth="yell" brows="angry" o={o} /></g></>, sh * 0.5); }],
  ['jam', at('and', 5), (o, t, a) => camWrap(1.25, 380, 1500, <><Sky o={o} /><Ground y={1200} o={o} /><Gun x={300} y={1700} s={1.2} smoke={ease(o, a, a + 700)} rot={Math.sin(o / 30) * 2 * (1 - t)} />
    <Bean x={120} y={1840} s={1.05} eyes="wide" mouth="o" sweat brows="worried" o={o} /><text x={560} y={1220} fontFamily="Inter" fontWeight={800} fontSize={120} fill="#fff" stroke={INK} strokeWidth={10} paintOrder="stroke" transform={`rotate(-8 560 1220) scale(${pop(o, at('jammed'))})`}>*CLICK*</text></>)],
  ['bolt', at('so', 1), (o, t, a) => camWrap(1, 540, 1300, <><Sky o={o} /><Hills y={1220} o={o} /><Ground y={1250} o={o} /><Truck x={600} y={1700} o={o * 0.02} /><Gun x={500} y={1450 - 200 * (1 - pop(o, at('truck')))} s={0.75} />
    <Bean x={180} y={1760} s={1.05} mouth="grin" brows="smug" armR={-1.8 + Math.sin(o / 60) * 0.6} o={o} hold={<rect x={-8} y={-10} width={16} height={60} rx={6} fill="#999" stroke={INK} strokeWidth={4} />} /></>)],
  ['chase', at('but'), (o, t, a) => { const x = interpolate(o - a, [0, 4200], [-200, 420], cl), sk = o > at('bumpy') ? 26 : 8;
    return camWrap(1, 540, 1300, <><Sky o={o} /><Hills y={1220} o={o} /><Ground y={1250} o={o} /><SpeedLines o={o} />
      <Truck x={x} y={1700} shake={sk} o={o} /><g transform={`translate(0 ${Math.sin(o / 45) * sk})`}><Gun x={x - 120} y={1440} s={0.7} rot={Math.sin(o / 50) * sk * 0.4} /><Bean x={x - 230} y={1490} s={0.8} eyes={sk > 10 ? 'wide' : 'squint'} mouth={sk > 10 ? 'o' : 'grin'} sweat={sk > 10} tilt={Math.sin(o / 60) * sk * 0.6} o={o} /></g>
      {[0, 1, 2].map((i) => <Emu key={i} x={x + 640 + i * 170 + (o - a) / 12} y={1620 + i * 40} s={0.55} run={o / 45 + i} eye="smug" dust o={o} seed={i} />)}</>); }],
  ['quote', at('meredith', 1), (o, t, a) => { const tankOn = o > at('tanks') - 200;
    return <>{camWrap(1 + 0.04 * t, 540, 1100, <><rect x={-200} y={-200} width={1480} height={2320} fill="#d9c79a" /><rect x={-200} y={1450} width={1480} height={700} fill="#8a6a44" stroke={INK} strokeWidth={8} />
      <g transform="translate(250 420)"><rect x={-150} y={-110} width={300} height={220} fill="#f4e6c4" stroke={INK} strokeWidth={8} /><path d="M-120 -60 Q-60 -100 0 -40 Q60 0 120 -60" stroke="#c9493c" strokeWidth={6} fill="none" strokeDasharray="14 10" /><text x={0} y={70} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={40} fill={INK}>CAMPION</text></g>
      <Bean x={tankOn ? 280 : 540} y={1850} s={tankOn ? 1.6 : 2.2} hat="cap" mustache shirt="#6b6f3c" pants="#3e3f22" mouth="talk" brows="worried" armR={-2.3} o={o} seed={1} /></>)}
      {tankOn && <g transform={`translate(0 0)`}>{camWrap(pop(o, at('tanks') - 200, 160), 760, 1500, <g><Emu x={760} y={1560} s={1.25} tank eye="angry" hat o={o} /><text x={760} y={1080} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={88} fill="#fff" stroke={INK} strokeWidth={10} paintOrder="stroke">EMU TANK</text></g>)}</g>}</>; }],
  ['home', at('after', 1), (o, t, a) => camWrap(1, 540, 1300, <><Sky o={o} sunset /><Hills y={1220} o={o} /><Ground y={1250} o={o} /><GumTree x={160} y={1260} s={0.8} o={o} />
    <g transform="scale(-1 1)"><Truck x={-interpolate(o - a, [0, 2200], [600, -500], cl)} y={1720} o={o} /></g>
    <g transform={`translate(540 540) scale(${pop(o, at('six'))})`}><rect x={-250} y={-80} width={500} height={140} rx={18} fill="#f4e6c4" stroke={INK} strokeWidth={8} /><text x={0} y={30} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={86} fill={INK}>6 DAYS</text></g>
    <Emu x={880} y={1600} s={0.75} eye="happy" flip o={o} /></>)],
  ['back', at('then', 1), (o, t, a) => { const army = o > at('so', 3); return camWrap(1, 540, 1300, <><Sky o={o} /><Hills y={1220} green o={o} /><Ground y={1250} green o={o} /><Wheat x={-40} y={1420} w={1200} o={o} />
    {Array.from({length: 6}, (_, i) => { const k = pop(o, a + i * 120, 220); return <g key={i} transform={`translate(${130 + i * 170} 1560) scale(${k}) translate(${-(130 + i * 170)} -1560)`}><Emu x={130 + i * 170} y={1560} s={0.6} eye="smug" o={o} seed={i} /></g>; })}
    {army && <Truck x={interpolate(o - at('so', 3), [0, 1300], [1500, 640], cl)} y={1840} o={o} s={0.8} />}</>); }],
  ['tally', at('in', 3), (o, t, a) => { const per = o > at('that\'s', 0) - 100;
    return camWrap(1, 540, 1100, <><rect x={-200} y={-200} width={1480} height={2320} fill="#2d4a3a" /><rect x={90} y={380} width={900} height={1040} rx={20} fill="#294236" stroke="#6b4a2c" strokeWidth={30} />
      {!per && <><text x={540} y={560} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={70} fill="#f4f0e0">FINAL SCORE</text>
        <g opacity={ease(o, at('claimed') - 200, at('claimed') + 200)}><Emu x={300} y={940} s={0.55} eye="wide" o={o} /><text x={720} y={860} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={100} fill="#f4f0e0">~1,000</text></g>
        <g opacity={ease(o, at('almost') - 200, at('almost') + 200)}><Bullet x={300} y={1220} k={2.4} /><text x={720} y={1240} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={100} fill="#f4f0e0">~10,000</text></g></>}
      {per && <><Emu x={540} y={1150} s={0.9} eye="smug" o={o} />{Array.from({length: 10}, (_, i) => <Bullet key={i} x={190 + i * 78} y={1330} k={pop(o, at('that\'s', 0) + i * 70, 260) * 1.4} />)}
        <text x={540} y={560} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={90} fill="#ffd84a">10 BULLETS</text><text x={540} y={660} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={70} fill="#f4f0e0">PER BIRD</text></>}</>); }],
  ['again', at('years'), (o, t, a) => camWrap(1, 540, 1100, <><rect x={0} y={0} width={1080} height={960} fill="#ffe7b8" /><rect x={0} y={960} width={1080} height={960} fill="#cfd8a8" /><line x1={0} y1={960} x2={1080} y2={960} stroke={INK} strokeWidth={10} />
    <Bean x={330} y={880} s={1.0} hat="farmer" shirt="#c9493c" pants="#3f5b8a" uniform={false} mouth="talk" brows="worried" armR={-2.4} o={o} />
    {Array.from({length: 3}, (_, i) => { const k = pop(o, a + 200 + i * 350); return <g key={i} transform={`translate(${620 + i * 120} ${520 + i * 90}) scale(${k}) rotate(${-8 + i * 8})`}><rect x={-80} y={-55} width={160} height={110} fill="#fff" stroke={INK} strokeWidth={5} /><path d="M-80 -55 L0 10 L80 -55" stroke={INK} strokeWidth={5} fill="none" /><text x={0} y={-70} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={34} fill="#c9493c">{['1934', '1943', '1948'][i]}</text></g>; })}
    <Bean x={720} y={1840} s={1.0} hat="cap" mustache shirt="#6b6f3c" pants="#3e3f22" mouth={o > at('no') ? 'flat' : 'talk'} flip brows="angry" armL={o > at('no') ? -2.4 : 0.2} o={o} seed={1} />
    {o > at('no') - 100 && <g transform={`translate(340 1400) scale(${pop(o, at('no') - 100, 300)}) rotate(-12)`}><rect x={-170} y={-100} width={340} height={190} rx={18} fill="none" stroke="#c9493c" strokeWidth={16} /><text x={0} y={48} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={150} fill="#c9493c">NO</text></g>}</>)],
  ['bounty', at('instead'), (o, t, a) => camWrap(1, 540, 1300, <><Sky o={o} /><Hills y={1180} green o={o} /><Ground y={1200} green o={o} /><Farmhouse x={820} y={1210} /><Wheat x={-40} y={1460} w={1200} o={o} />
    <Bean x={400} y={1760} s={1.35} hat="farmer" shirt="#c9493c" pants="#3f5b8a" uniform={false} mouth="grin" eyes={o > at('better') ? 'closed' : 'dot'} armL={-2.4} armR={2.4} jump={Math.abs(Math.sin(o / 160)) * 20} o={o} />
    {Array.from({length: 7}, (_, i) => { const t0 = at('paid') + i * 220, p = Math.max(0, (o - t0) / 900); return p > 0 ? <Coin key={i} x={200 + i * 110} y={-100 + Math.min(1, p) * (1260 + (i % 3) * 60)} k={1} /> : null; })}</>)],
  ['end', at('and', 8), (o, t, a, b) => { const zoom = 1 + 0.15 * ease(o, at('birds', 2) - 300, b);
    return camWrap(zoom, 540, 1400, <><Sky o={o} /><Burst o={o} c1="#9fd6f5" c2="#bfe3f7" cy={1200} /><Hills y={1250} green o={o} /><Ground y={1300} green o={o} /><Wheat x={-40} y={1380} w={1200} eaten={1} o={o} />
      <g transform="translate(540 800)"><path d="M0 0 L0 -300" stroke={INK} strokeWidth={14} /><path d="M0 -300 L240 -258 L0 -210 Z" fill="#e8c34a" stroke={INK} strokeWidth={7} /><g transform="translate(110 -258) scale(0.25)"><Emu x={0} y={110} s={1} eye="happy" o={o} /></g></g>
      {[0, 1, 3, 4].map((i) => <Emu key={i} x={60 + i * 250} y={1600 + (i % 2) * 60 - Math.abs(Math.sin(o / 170 + i)) * 50} s={0.7} eye="happy" flip={i % 2 === 0} o={o} seed={i} />)}
      <Emu x={540} y={1860 - Math.abs(Math.sin(o / 150)) * 60} s={1.25} eye="happy" hat o={o} /></>); }],
  ['outro', W[W.length - 1].b + 500, (o, t, a) => <><Burst o={o} c1="#2d2a2e" c2="#3a363b" />
    <g transform={`translate(540 760) scale(${pop(o, a, 200)})`}><rect x={-380} y={-130} width={760} height={260} rx={30} fill="#ffd84a" stroke={INK} strokeWidth={10} /><text x={0} y={-12} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={88} fill={INK}>WEIRD HISTORY</text><text x={0} y={80} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={64} fill="#c9493c">EPISODE 1</text></g>
    <g transform={`translate(540 1180) scale(${pop(o, a + 400, 200)})`}><text x={0} y={0} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={70} fill="#fff">Follow for Episode 2</text></g>
    <Emu x={540} y={1760} s={1.0} eye="happy" hat o={o} /></>],
];
const shotAt = (o: number) => { let i = 0; SH.forEach(([, t], j) => { if (o >= t) i = j; }); return {i, a: SH[i][1], b: SH[i + 1]?.[1] ?? EMU2_MS}; };

const KEY = /^(1932|birds|lost|20,000|fences|rabbits|machine|guns|10,000|cameraman|victory|range|ambush|jammed|truck|bumpy|tanks|home|back|1,000|10|bird|no|paid|better|war)$/i;
const Caption = ({o}: {o: number}) => {
  const w = [...W].reverse().find((x) => o >= x.a - 40);
  if (!w || o > w.b + 400) return null;
  const k = interpolate(o - w.a, [0, 90], [0.75, 1], cl), txt = w.t.replace(/[.?!"]/g, '').replace(/,$/, '');
  return <div style={{position: 'absolute', top: 250, left: 0, right: 0, textAlign: 'center', transform: `scale(${k}) rotate(${KEY.test(txt) ? -3 : 0}deg)`}}>
    <span style={{fontFamily: 'Inter', fontWeight: 800, fontSize: KEY.test(txt) ? 120 : 104, color: KEY.test(txt) ? '#ffd84a' : '#fff', WebkitTextStroke: '15px #1d1a1f', paintOrder: 'stroke fill'}}>{txt}</span></div>;
};

export const EmuShort2 = () => {
  const f = useCurrentFrame(), o = (f / FPS) * 1000;
  const {i, a, b} = shotAt(o), t = (o - a) / Math.max(1, b - a);
  const punch = interpolate(o - a, [0, 160], [1.07, 1], cl), wipe = interpolate(o - a, [0, 140], [1, 0], cl);
  const voiceAt = (ms: number) => W.some((w) => ms >= w.a - 100 && ms <= w.b + 250);
  const sfx: [string, number, number][] = [['jorho-pop', at('1932'), 0.3], ['record-scratch', at('lost'), 0.22], ['jorho-pop', at('20,000'), 0.3], ['metal-pipe-clang', at('they', 1) + 260, 0.12],
    ['jorho-pop', at('major'), 0.28], ['jorho-pop', at('soldiers'), 0.28], ['jorho-pop', at('two', 1), 0.28], ['jorho-pop', at('10,000'), 0.28], ['camera-shutter', at('cameraman'), 0.3],
    ['fast-whoosh', at('ran'), 0.2], ['meme-impact', at('fire'), 0.15], ['jorho-click', at('jammed'), 0.5], ['meme-bonk', at('bumpy'), 0.25], ['crickets', at('six'), 0.3],
    ['jorho-ting', at('that\'s', 0), 0.3], ['meme-fahh', at('no'), 0.18], ['cha-ching', at('paid'), 0.25], ['meme-tada', W[W.length - 1].b + 500, 0.25]];
  const Shot = SH[i][2];
  return <AbsoluteFill style={{background: '#000'}}>
    <AbsoluteFill style={{transform: `scale(${punch})`}}><svg width={1080} height={1920} viewBox="0 0 1080 1920"><Defs />{Shot(o, t, a, b)}
      <rect width={1080} height={1920} fill="url(#vig)" /><rect width={1080} height={1920} filter="url(#grain)" opacity={0.5} /></svg></AbsoluteFill>
    {wipe > 0 && i > 0 && <AbsoluteFill style={{background: '#fffdf8', clipPath: `circle(${wipe * 80}% at 50% 50%)`, opacity: 0.85}} />}
    {o < SH[SH.length - 1][1] && <div style={{position: 'absolute', top: 70, left: 44, padding: '10px 22px', borderRadius: 16, background: '#ffd84a', border: '6px solid #1d1a1f', fontFamily: 'Inter', fontWeight: 800, fontSize: 34, color: '#1d1a1f'}}>WEIRD HISTORY · EP. 1</div>}
    <Caption o={o} />
    <Sequence from={Math.round((OFF / 1000) * FPS)}><Audio src={staticFile('inside/vo_emu2.wav')} /></Sequence>
    <Audio src={staticFile('music/Fluffing_a_Duck.mp3')} loop volume={(fr) => { const ms = (fr / FPS) * 1000; return (voiceAt(ms) ? 0.055 : 0.11) * Math.min(1, (EMU2_MS - ms) / 900); }} />
    {SH.slice(1).map(([, t0], k) => <Sequence key={'w' + k} from={Math.max(0, Math.round((t0 / 1000) * FPS) - 7)}><Audio src={staticFile('sfx/mg-whoosh.mp3')} volume={0.1} /></Sequence>)}
    {sfx.map(([s, t0, v], k) => <Sequence key={k} from={Math.max(0, Math.round((t0 / 1000) * FPS))}><Audio src={staticFile(`sfx/${s}.mp3`)} volume={v} /></Sequence>)}
  </AbsoluteFill>;
};

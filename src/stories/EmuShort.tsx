// "The Great Emu War" — 2D bean-head cartoon short (1080x1920, 30 fps, ~45 s). Own drawings (SVG), Kokoro narration,
// one-word captions. Facts: stories/002-emu-war/SCRIPT.md. Music: "Fluffing a Duck" Kevin MacLeod (incompetech.com), CC BY 4.0.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, spring, staticFile, useCurrentFrame} from 'remotion';
import '../mgFonts';
import raw from '../inside/vo_emu.words.json';

const FPS = 30, OFF = 300, INK = '#1d1a1f';
const W = (raw as {text: string; startMs: number; endMs: number}[]).map((w) => ({t: w.text, a: w.startMs + OFF, b: w.endMs + OFF}));
export const EMU_MS = W[W.length - 1].b + 1600;
const at = (word: string, n = 0) => { const m = W.filter((w) => w.t.toLowerCase().replace(/[^a-z0-9,]/g, '').replace(/,$/, '') === word.toLowerCase()); return m[n]?.a ?? 0; };
const cl = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const ease = (o: number, a: number, b: number) => interpolate(o, [a, b], [0, 1], {...cl, easing: (x) => x * x * (3 - 2 * x)});

// ---------- characters ----------
type BeanP = {x: number; y: number; s?: number; shirt?: string; pants?: string; hat?: 'slouch' | 'cap' | 'farmer' | 'none'; mustache?: boolean; mouth?: 'smile' | 'flat' | 'o' | 'frown' | 'grin' | 'talk';
  walk?: number; armL?: number; armR?: number; flip?: boolean; eyes?: 'dot' | 'wide' | 'tired' | 'closed'; brows?: 'none' | 'smug' | 'worried' | 'angry'; tilt?: number; sweat?: boolean; o: number};
const Bean = ({x, y, s = 1, shirt = '#7b8b4a', pants = '#5b4a36', hat = 'slouch', mustache, mouth = 'smile', walk = 0, armL = 0.25, armR = -0.25, flip, eyes = 'dot', brows = 'none', tilt = 0, sweat, o}: BeanP) => {
  const sw = Math.sin(walk) * 0.5, bob = Math.abs(Math.cos(walk)) * 6 * (walk ? 1 : 0) + Math.sin(o / 500) * 2;
  const leg = (dx: number, a: number) => <line x1={dx} y1={-70} x2={dx + Math.sin(a) * 70} y2={0} stroke={INK} strokeWidth={14} strokeLinecap="round" />;
  const arm = (dx: number, a: number) => <g transform={`translate(${dx} -150) rotate(${a * 57})`}><line x1={0} y1={0} x2={0} y2={78} stroke={INK} strokeWidth={13} strokeLinecap="round" /><circle cx={0} cy={82} r={11} fill="#fff" stroke={INK} strokeWidth={6} /></g>;
  const mouthEl = {smile: <path d="M-22 22 Q0 40 22 22" />, grin: <path d="M-26 16 Q0 52 26 16 Z" fill={INK} />, flat: <path d="M-16 28 L16 28" />, frown: <path d="M-18 34 Q0 18 18 34" />,
    o: <ellipse cx={0} cy={28} rx={10} ry={13} fill={INK} />, talk: <ellipse cx={0} cy={28} rx={14} ry={4 + 9 * Math.abs(Math.sin(o / 70))} fill={INK} />}[mouth];
  const eye = (ex: number) => eyes === 'closed' || eyes === 'tired' ? <path d={eyes === 'tired' ? `M${ex - 11} -6 L${ex + 11} -6` : `M${ex - 11} -2 Q${ex} 8 ${ex + 11} -2`} stroke={INK} strokeWidth={6} fill="none" strokeLinecap="round" />
    : eyes === 'wide' ? <g><circle cx={ex} cy={-4} r={15} fill="#fff" stroke={INK} strokeWidth={5} /><circle cx={ex} cy={-4} r={6} fill={INK} /></g> : <circle cx={ex} cy={-4} r={8} fill={INK} />;
  return <g transform={`translate(${x} ${y - bob}) scale(${(flip ? -1 : 1) * s} ${s}) rotate(${tilt})`}>
    {leg(-18, sw)}{leg(18, -sw)}
    <rect x={-52} y={-190} width={104} height={125} rx={30} fill={shirt} stroke={INK} strokeWidth={8} />
    <rect x={-52} y={-95} width={104} height={30} rx={10} fill={pants} stroke={INK} strokeWidth={8} />
    {arm(-50, armL - sw * 0.6)}{arm(50, armR + sw * 0.6)}
    <g transform="translate(0 -262)">
      <ellipse cx={0} cy={0} rx={64} ry={74} fill="#fffdf8" stroke={INK} strokeWidth={8} />
      {eye(-24)}{eye(24)}
      {brows === 'smug' && <><path d="M-38 -32 L-12 -26" stroke={INK} strokeWidth={6} strokeLinecap="round" /><path d="M12 -30 L38 -40" stroke={INK} strokeWidth={6} strokeLinecap="round" /></>}
      {brows === 'worried' && <><path d="M-38 -30 L-12 -40" stroke={INK} strokeWidth={6} strokeLinecap="round" /><path d="M12 -40 L38 -30" stroke={INK} strokeWidth={6} strokeLinecap="round" /></>}
      {brows === 'angry' && <><path d="M-38 -40 L-12 -28" stroke={INK} strokeWidth={6} strokeLinecap="round" /><path d="M12 -28 L38 -40" stroke={INK} strokeWidth={6} strokeLinecap="round" /></>}
      <g stroke={INK} strokeWidth={6} fill="none" strokeLinecap="round">{mouthEl}</g>
      {mustache && <path d="M-30 14 Q-15 2 0 12 Q15 2 30 14 Q15 22 0 16 Q-15 22 -30 14 Z" fill="#5a3b22" stroke={INK} strokeWidth={4} />}
      {sweat && <path d="M54 -40 Q64 -20 54 -14 Q44 -20 54 -40 Z" fill="#8fd0ff" stroke={INK} strokeWidth={3} />}
      {hat === 'slouch' && <g><path d="M-92 -42 Q0 -70 92 -42 Q60 -30 0 -36 Q-60 -30 -92 -42 Z" fill="#9b8656" stroke={INK} strokeWidth={6} /><path d="M-52 -48 Q-48 -104 0 -108 Q48 -104 52 -48 Z" fill="#a8925f" stroke={INK} strokeWidth={6} /><rect x={-52} y={-60} width={104} height={12} fill="#5a4a2a" /><path d="M52 -50 Q70 -80 60 -100" stroke={INK} strokeWidth={6} fill="none" /></g>}
      {hat === 'cap' && <g><path d="M-58 -46 Q0 -112 58 -46 Z" fill="#6b6f3c" stroke={INK} strokeWidth={6} /><path d="M-60 -46 L72 -46 L84 -38 L-60 -38 Z" fill="#3e3f22" stroke={INK} strokeWidth={5} /><circle cx={0} cy={-74} r={9} fill="#e8c34a" stroke={INK} strokeWidth={3} /></g>}
      {hat === 'farmer' && <g><ellipse cx={0} cy={-46} rx={96} ry={18} fill="#e5c56a" stroke={INK} strokeWidth={6} /><path d="M-50 -48 Q-46 -100 0 -102 Q46 -100 50 -48 Z" fill="#edd27c" stroke={INK} strokeWidth={6} /><rect x={-50} y={-62} width={100} height={12} fill="#b5463a" /></g>}
    </g>
  </g>;
};

type EmuP = {x: number; y: number; s?: number; run?: number; peck?: number; flip?: boolean; hat?: boolean; o: number; eye?: 'dot' | 'angry' | 'happy'};
const Emu = ({x, y, s = 1, run = 0, peck = 0, flip, hat, o, eye = 'dot'}: EmuP) => {
  const sw = Math.sin(run) * 0.7, bob = run ? Math.abs(Math.cos(run)) * 10 : Math.sin(o / 400 + x) * 2;
  const neckBend = peck * 90;
  return <g transform={`translate(${x} ${y - bob}) scale(${(flip ? -1 : 1) * s} ${s})`}>
    <line x1={-14} y1={-90} x2={-14 + Math.sin(sw) * 60} y2={0} stroke={INK} strokeWidth={9} strokeLinecap="round" />
    <line x1={14} y1={-90} x2={14 - Math.sin(sw) * 60} y2={0} stroke={INK} strokeWidth={9} strokeLinecap="round" />
    <ellipse cx={0} cy={-140} rx={92} ry={66} fill="#6a5240" stroke={INK} strokeWidth={8} />
    {[-50, -20, 10, 40].map((dx, i) => <path key={i} d={`M${dx} -170 q 14 26 -6 52`} stroke="#4b392b" strokeWidth={6} fill="none" strokeLinecap="round" />)}
    <path d={`M62 -168 Q${98 + neckBend * 0.3} ${-240 + neckBend} ${84 + neckBend * 0.5} ${-300 + neckBend * 1.9}`} stroke={INK} strokeWidth={30} fill="none" strokeLinecap="round" />
    <path d={`M62 -168 Q${98 + neckBend * 0.3} ${-240 + neckBend} ${84 + neckBend * 0.5} ${-300 + neckBend * 1.9}`} stroke="#8aa1c8" strokeWidth={18} fill="none" strokeLinecap="round" />
    <g transform={`translate(${86 + neckBend * 0.5} ${-312 + neckBend * 1.9}) rotate(${peck * 70})`}>
      <ellipse cx={0} cy={0} rx={30} ry={24} fill="#7f6a56" stroke={INK} strokeWidth={6} />
      <path d="M26 -2 L58 6 L26 12 Z" fill="#d8b46a" stroke={INK} strokeWidth={5} strokeLinejoin="round" />
      {eye === 'happy' ? <path d="M2 -6 Q10 -14 18 -6" stroke={INK} strokeWidth={5} fill="none" /> : <circle cx={10} cy={-6} r={7} fill={INK} />}
      {eye === 'angry' && <path d="M-2 -20 L22 -12" stroke={INK} strokeWidth={6} />}
      {hat && <g transform="translate(-4 -18)"><path d="M-40 -6 Q0 -22 40 -6 Q20 0 0 -2 Q-20 0 -40 -6 Z" fill="#9b8656" stroke={INK} strokeWidth={5} /><path d="M-24 -8 Q-20 -44 0 -46 Q20 -44 24 -8 Z" fill="#a8925f" stroke={INK} strokeWidth={5} /></g>}
    </g>
  </g>;
};

// ---------- props / backgrounds ----------
const Sky = ({top = '#7cc6f2', bottom = '#ffe7b8'}: {top?: string; bottom?: string}) => <>
  <defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={top} /><stop offset="1" stopColor={bottom} /></linearGradient></defs>
  <rect x={-600} y={-600} width={2400} height={3200} fill="url(#sky)" />
</>;
const Ground = ({y = 1300, c = '#e0a95c', c2 = '#c98d45'}: {y?: number; c?: string; c2?: string}) => <>
  <path d={`M-600 ${y} Q300 ${y - 60} 1100 ${y - 10} Q1500 ${y + 20} 1800 ${y - 30} L1800 2600 L-600 2600 Z`} fill={c} stroke={INK} strokeWidth={8} />
  {Array.from({length: 24}, (_, i) => <path key={i} d={`M${(i * 173) % 1700 - 300} ${y + 80 + (i * 97) % 600} q 30 -14 60 0`} stroke={c2} strokeWidth={8} fill="none" strokeLinecap="round" />)}
</>;
const Sun = ({x = 860, y = 300}: {x?: number; y?: number}) => <g><circle cx={x} cy={y} r={95} fill="#ffd84a" stroke={INK} strokeWidth={8} />{Array.from({length: 10}, (_, i) => { const a = (i / 10) * Math.PI * 2; return <line key={i} x1={x + Math.cos(a) * 120} y1={y + Math.sin(a) * 120} x2={x + Math.cos(a) * 160} y2={y + Math.sin(a) * 160} stroke={INK} strokeWidth={8} strokeLinecap="round" />; })}</g>;
const GumTree = ({x, y, s = 1}: {x: number; y: number; s?: number}) => <g transform={`translate(${x} ${y}) scale(${s})`}><path d="M-14 0 L-8 -260 L10 -260 L16 0 Z" fill="#e8dcc8" stroke={INK} strokeWidth={6} /><ellipse cx={-40} cy={-300} rx={110} ry={70} fill="#7aa35a" stroke={INK} strokeWidth={7} /><ellipse cx={60} cy={-330} rx={100} ry={64} fill="#8bb366" stroke={INK} strokeWidth={7} /><ellipse cx={0} cy={-380} rx={90} ry={56} fill="#9cc172" stroke={INK} strokeWidth={7} /></g>;
const Wheat = ({x, y, w = 900, eaten = 0}: {x: number; y: number; w?: number; eaten?: number}) => <g>{Array.from({length: Math.floor(w / 26)}, (_, i) => { const h = (i * 37) % 3 === 0 ? 150 : 130; const gone = (i / (w / 26)) < eaten; return gone ? <line key={i} x1={x + i * 26} y1={y} x2={x + i * 26} y2={y - 26} stroke="#b88c3a" strokeWidth={8} strokeLinecap="round" />
  : <g key={i}><line x1={x + i * 26} y1={y} x2={x + i * 26 + 6} y2={y - h} stroke="#c99a3c" strokeWidth={8} strokeLinecap="round" /><ellipse cx={x + i * 26 + 8} cy={y - h - 14} rx={10} ry={24} fill="#f0c95a" stroke={INK} strokeWidth={5} /></g>; })}</g>;
const Farmhouse = ({x, y}: {x: number; y: number}) => <g transform={`translate(${x} ${y})`}><rect x={-160} y={-220} width={320} height={220} fill="#e9e1cf" stroke={INK} strokeWidth={8} /><path d="M-190 -220 L0 -360 L190 -220 Z" fill="#b5463a" stroke={INK} strokeWidth={8} strokeLinejoin="round" /><rect x={-40} y={-120} width={80} height={120} fill="#6b4a2c" stroke={INK} strokeWidth={6} /><rect x={-130} y={-170} width={60} height={56} fill="#8fd0ff" stroke={INK} strokeWidth={6} /><rect x={70} y={-170} width={60} height={56} fill="#8fd0ff" stroke={INK} strokeWidth={6} /></g>;
const Crate = ({x, y, label}: {x: number; y: number; label?: string}) => <g transform={`translate(${x} ${y})`}><rect x={-90} y={-110} width={180} height={110} fill="#c79a5a" stroke={INK} strokeWidth={7} /><line x1={-90} y1={-55} x2={90} y2={-55} stroke={INK} strokeWidth={5} />{label && <text x={0} y={-40} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={40} fill={INK}>{label}</text>}</g>;
const Gun = ({x, y, s = 1}: {x: number; y: number; s?: number}) => <g transform={`translate(${x} ${y}) scale(${s})`}><line x1={-30} y1={0} x2={-60} y2={-80} stroke={INK} strokeWidth={10} /><line x1={30} y1={0} x2={60} y2={-80} stroke={INK} strokeWidth={10} /><rect x={-90} y={-130} width={200} height={44} rx={10} fill="#4d5530" stroke={INK} strokeWidth={7} /><rect x={110} y={-118} width={110} height={18} fill="#3b3f26" stroke={INK} strokeWidth={5} /><circle cx={-30} cy={-150} r={30} fill="#4d5530" stroke={INK} strokeWidth={6} /></g>;
const Truck = ({x, y, shake = 0, o}: {x: number; y: number; shake?: number; o: number}) => { const dy = Math.sin(o / 45) * shake, rot = Math.sin(o / 60) * shake * 0.25; const wr = o / 40;
  return <g transform={`translate(${x} ${y + dy}) rotate(${rot})`}>
    <rect x={-300} y={-260} width={420} height={170} rx={16} fill="#7b8b4a" stroke={INK} strokeWidth={8} /><path d="M120 -260 L230 -260 L290 -170 L290 -90 L120 -90 Z" fill="#6e7d40" stroke={INK} strokeWidth={8} strokeLinejoin="round" /><path d="M140 -245 L220 -245 L262 -180 L140 -180 Z" fill="#8fd0ff" stroke={INK} strokeWidth={6} />
    {[-190, 190].map((wx, i) => <g key={i} transform={`translate(${wx} -80) rotate(${wr * 57})`}><circle r={62} fill="#2d2a2e" stroke={INK} strokeWidth={8} /><circle r={24} fill="#bbb" stroke={INK} strokeWidth={5} /><line x1={-24} y1={0} x2={24} y2={0} stroke={INK} strokeWidth={5} /></g>)}
  </g>; };
const Phone = ({x, y}: {x: number; y: number}) => <g transform={`translate(${x} ${y})`}><rect x={-60} y={-60} width={120} height={90} rx={14} fill="#2d2a2e" stroke={INK} strokeWidth={6} /><circle cx={0} cy={-15} r={26} fill="#d9d2c4" stroke={INK} strokeWidth={5} /><path d="M-70 -80 Q0 -120 70 -80" stroke="#2d2a2e" strokeWidth={26} fill="none" strokeLinecap="round" /></g>;
const SpeedLines = ({o, n = 14}: {o: number; n?: number}) => <g opacity={0.5}>{Array.from({length: n}, (_, i) => { const y = 200 + (i * 131) % 1500, x = ((o * 2.2 + i * 300) % 1600) - 300; return <line key={i} x1={x} y1={y} x2={x + 260} y2={y} stroke="#fff" strokeWidth={10} strokeLinecap="round" />; })}</g>;

// ---------- shots ----------
const S: [string, number][] = [['title', 0], ['farm', at('after')], ['emus', at('then')], ['phone', at('so')], ['army', at('the', 2)], ['easy', at('easy')], ['split', at('the', 3)],
  ['truck', at('so', 1)], ['shake', at('but')], ['week', at('after', 1)], ['cmd', at('their')], ['hero', at('bullet')], ['cmd2', at('it', 1)], ['home', at('so', 3)], ['end', at('and', 5)]];
const shotAt = (o: number) => { let i = 0; S.forEach(([, t], j) => { if (o >= t) i = j; }); return {id: S[i][0], a: S[i][1], b: S[i + 1]?.[1] ?? EMU_MS}; };

const Shot = ({id, o, a, b}: {id: string; o: number; a: number; b: number}) => {
  const t = (o - a) / Math.max(1, b - a), lo = o - a;
  const pop = (ms: number) => spring({frame: Math.max(0, (o - ms) / (1000 / FPS)), fps: FPS, config: {damping: 11, stiffness: 180}});
  switch (id) {
    case 'title': { const z = 1 + 0.35 * ease(o, at('birds') - 200, at('birds') + 300);
      return <g transform={`translate(540 1100) scale(${z}) translate(${-540 + 220 * ease(o, at('birds') - 200, at('birds') + 300)} -1100)`}>
        <Sky /><Sun /><Ground y={1250} /><GumTree x={120} y={1260} s={0.9} />
        <g transform="translate(540 760)"><rect x={-150} y={-90} width={300} height={130} rx={10} fill="#f4e6c4" stroke={INK} strokeWidth={8} /><text x={0} y={10} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={96} fill={INK}>1932</text><line x1={0} y1={40} x2={0} y2={470} stroke={INK} strokeWidth={14} /></g>
        <Bean x={300} y={1500} s={1.2} armR={-2.6} mouth="flat" brows="angry" o={o} />
        <Emu x={800} y={1520} s={1.25} flip eye="angry" o={o} />
      </g>; }
    case 'farm': return <g><Sky /><Sun x={180} y={260} /><Ground y={1150} c="#9cbd5a" c2="#86a64a" /><Farmhouse x={760} y={1160} /><Wheat x={-40} y={1480} w={1200} />
      <Bean x={420} y={1560 + 0} s={1.25} hat="farmer" shirt="#c9493c" pants="#3f5b8a" armR={-2.4 + Math.sin(o / 200) * 0.2} mouth="grin" o={o} /></g>;
    case 'emus': { const n = 9; return <g><Sky /><Ground y={1150} c="#9cbd5a" c2="#86a64a" /><Farmhouse x={860} y={1160} /><Wheat x={-40} y={1520} w={1200} eaten={ease(o, at('eating'), b)} />
      {Array.from({length: n}, (_, i) => { const x = interpolate(lo, [0, 1400], [1300 + i * 160, 120 + i * 110], cl), eating = o > at('eating'); return <Emu key={i} x={x} y={1380 + (i % 3) * 60} s={0.65} run={eating ? 0 : o / 70 + i} peck={eating ? (Math.sin(o / 120 + i) + 1) / 2 : 0} flip={!eating} o={o} />; })}
      <Bean x={160} y={1700} s={0.9} hat="farmer" shirt="#c9493c" pants="#3f5b8a" eyes="wide" mouth="o" sweat armL={0.9} armR={-0.9} o={o} /></g>; }
    case 'phone': return <g><rect x={0} y={0} width={1080} height={960} fill="#ffe7b8" /><rect x={0} y={960} width={1080} height={960} fill="#cfd8a8" /><line x1={0} y1={960} x2={1080} y2={960} stroke={INK} strokeWidth={10} />
      <Bean x={360} y={860} s={1.0} hat="farmer" shirt="#c9493c" pants="#3f5b8a" mouth="talk" armR={-2.7} brows="worried" o={o} /><Phone x={700} y={760} />
      <Bean x={700} y={1820} s={1.0} hat="cap" mustache shirt="#6b6f3c" pants="#3e3f22" mouth={o > at('help') ? 'smile' : 'flat'} armL={-2.7} flip o={o} /><Phone x={360} y={1720} /></g>;
    case 'army': return <g><Sky /><Sun /><Ground y={1250} /><GumTree x={940} y={1260} s={0.8} />
      {[0, 1, 2].map((i) => { const k = pop(at('three') + i * 120); return <g key={i} transform={`translate(${210 + i * 330} 1560) scale(${k}) translate(${-(210 + i * 330)} -1560)`}><Bean x={210 + i * 330} y={1640} s={1.3} armR={-2.6} mouth="grin" brows="smug" o={o} /></g>; })}
      {[0, 1].map((i) => { const k = pop(at('two') + i * 150); return <g key={'g' + i} transform={`translate(${300 + i * 460} 1180) scale(${k * 1.05}) translate(${-(300 + i * 460)} -1260)`}><Gun x={300 + i * 460} y={1260} /></g>; })}
      {(() => { const k = pop(at('10,000')); return <g transform={`translate(540 1880) scale(${k * 1.5}) translate(-540 -1880)`}><Crate x={430} y={1880} label="10,000" /><Crate x={650} y={1880} label="BULLETS" /></g>; })()}
    </g>;
    case 'easy': return <g transform={`translate(540 960) scale(${1 + 0.06 * t}) translate(-540 -960)`}><Sky /><Ground y={1500} /><Bean x={540} y={1900} s={2.3} brows="smug" mouth="grin" armL={-2.4} armR={0.3} o={o} /></g>;
    case 'split': return <g><Sky /><Sun /><Ground y={1150} />
      {Array.from({length: 12}, (_, i) => { const ang = (i / 12) * Math.PI * 2, d = 900 * ease(lo, 150, 1600); return <Emu key={i} x={540 + Math.cos(ang) * d} y={1450 + Math.sin(ang) * d * 0.45} s={0.55} run={o / 60 + i} flip={Math.cos(ang) < 0} o={o} />; })}
      <Bean x={540} y={1650} s={1.1} eyes="wide" mouth="o" sweat brows="worried" armL={1.0} armR={-1.0} tilt={Math.sin(o / 150) * 6} o={o} /></g>;
    case 'truck': { const x = interpolate(lo, [0, 2600], [-300, 700], cl); return <g><Sky /><Sun /><Ground y={1250} /><SpeedLines o={o} />
      <Truck x={x} y={1650} o={o} /><Gun x={x - 120} y={1390} s={0.7} /><Bean x={x - 220} y={1440} s={0.75} mouth="grin" brows="angry" o={o} />
      {[0, 1, 2].map((i) => <Emu key={i} x={x + 700 + i * 180} y={1600 + i * 40} s={0.55} run={o / 50 + i} o={o} />)}</g>; }
    case 'shake': { const x = 480, sk = 24; return <g><Sky /><Sun /><Ground y={1250} />
      <Truck x={x} y={1650} shake={sk} o={o} /><g transform={`rotate(${Math.sin(o / 50) * 8} ${x - 120} 1400)`}><Gun x={x - 120} y={1390 + Math.sin(o / 45) * sk} s={0.7} /></g>
      <Bean x={x - 220} y={1440 + Math.sin(o / 45) * sk} s={0.75} eyes="wide" mouth="o" sweat tilt={Math.sin(o / 60) * 14} o={o} />
      {[0, 1, 2].map((i) => <Emu key={i} x={interpolate(lo, [0, 3400], [900, 1500], cl) + i * 120} y={1560 + i * 40} s={0.45} run={o / 45 + i} o={o} />)}</g>; }
    case 'week': { const day = Math.min(7, 1 + Math.floor(ease(o, a, at('dent')) * 6.99)); return <g><Sky top="#f2a65a" bottom="#ffe0b0" /><Ground y={1250} />
      <g transform="translate(540 620)"><rect x={-170} y={-170} width={340} height={300} rx={18} fill="#fff" stroke={INK} strokeWidth={8} /><rect x={-170} y={-170} width={340} height={80} rx={18} fill="#c9493c" stroke={INK} strokeWidth={8} /><text x={0} y={-112} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={44} fill="#fff">DAY</text><text x={0} y={70} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={150} fill={INK}>{day}</text></g>
      {[0, 1, 2].map((i) => <Bean key={i} x={220 + i * 320} y={1720} s={1.2} eyes="tired" mouth="frown" armL={0.15} armR={-0.15} o={o} />)}
      {[0, 1].map((i) => <Emu key={'e' + i} x={850 + i * 120} y={1330} s={0.5} peck={(Math.sin(o / 130 + i) + 1) / 2} o={o} />)}</g>; }
    case 'cmd': case 'cmd2': return <g transform={`translate(540 960) scale(${1 + 0.05 * t}) translate(-540 -960)`}><rect width={1080} height={1920} fill="#d9c79a" /><rect y={1450} width={1080} height={470} fill="#8a6a44" stroke={INK} strokeWidth={8} />
      <rect x={160} y={300} width={300} height={220} fill="#f4e6c4" stroke={INK} strokeWidth={8} /><text x={310} y={440} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={60} fill={INK}>MAP</text>
      <Bean x={540} y={1800} s={2.2} hat="cap" mustache shirt="#6b6f3c" pants="#3e3f22" mouth="talk" brows={id === 'cmd' ? 'worried' : 'angry'} armR={id === 'cmd2' ? -2.5 : -0.3} o={o} /></g>;
    case 'hero': return <g><rect width={1080} height={1920} fill="#ffd84a" />{Array.from({length: 16}, (_, i) => { const an = (i / 16) * Math.PI * 2 + o / 4000; return <path key={i} d={`M540 1100 L${540 + Math.cos(an) * 1800} ${1100 + Math.sin(an) * 1800} L${540 + Math.cos(an + 0.2) * 1800} ${1100 + Math.sin(an + 0.2) * 1800} Z`} fill="#ffb84a" />; })}
      <g transform={`translate(540 1500) scale(${1 + 0.08 * t}) translate(-540 -1500)`}><Emu x={480} y={1600} s={2.1} run={o / 140} hat eye="angry" o={o} /></g><SpeedLines o={o} n={10} /></g>;
    case 'home': return <g><Sky top="#f29a5a" bottom="#ffd9a0" /><Ground y={1250} /><GumTree x={900} y={1260} s={0.8} />
      {[0, 1, 2].map((i) => { const x = interpolate(lo, [0, 2400], [620 + i * 200, 160 + i * 200], cl); return <g key={i}><Bean x={x} y={1720} s={1.1} flip walk={o / 140 + i} eyes="tired" mouth="frown" o={o} /><Crate x={x + 10} y={1340} /></g>; })}</g>;
    case 'end': return <g transform={`translate(540 1300) scale(${1 + 0.18 * ease(o, at('birds', 2) - 300, b)}) translate(-540 -1300)`}><Sky /><Sun /><Ground y={1150} c="#9cbd5a" c2="#86a64a" /><Wheat x={-40} y={1250} w={1200} eaten={1} />
      {[0, 1, 3, 4].map((i) => <Emu key={i} x={60 + i * 250} y={1520 + (i % 2) * 60 - Math.abs(Math.sin(o / 180 + i)) * 40} s={0.75} eye="happy" flip={i % 2 === 0} o={o} />)}<Emu x={480} y={1760 - Math.abs(Math.sin(o / 160)) * 50} s={1.3} eye="happy" hat o={o} />
      <g transform="translate(540 700)"><path d="M0 0 L0 -260" stroke={INK} strokeWidth={12} /><path d="M0 -260 L220 -220 L0 -170 Z" fill="#e8c34a" stroke={INK} strokeWidth={6} /></g></g>;
  }
  return null;
};

const Caption = ({o}: {o: number}) => {
  const w = [...W].reverse().find((x) => o >= x.a - 40);
  if (!w || o > w.b + 400) return null;
  const k = interpolate(o - w.a, [0, 90], [0.8, 1], cl);
  return <div style={{position: 'absolute', top: 280, left: 0, right: 0, textAlign: 'center', transform: `scale(${k})`}}>
    <span style={{fontFamily: 'Inter', fontWeight: 800, fontSize: 104, color: '#fff', WebkitTextStroke: '14px #1d1a1f', paintOrder: 'stroke fill'}}>{w.t.replace(/[.?!"]/g, '').replace(/,$/, '')}</span></div>;
};

export const EmuShort = () => {
  const f = useCurrentFrame(), o = (f / FPS) * 1000;
  const {id, a, b} = shotAt(o);
  const k = interpolate(o - a, [0, 140], [1.06, 1], cl);
  const voiceAt = (ms: number) => W.some((w) => ms >= w.a - 100 && ms <= w.b + 250);
  const sfx: [string, number, number][] = [['jorho-pop', at('three'), 0.3], ['jorho-pop', at('two'), 0.3], ['jorho-pop', at('10,000'), 0.3], ['huh-cat', at('easy') + 300, 0.25],
    ['crickets', at('after', 1), 0.35], ['meme-bonk', at('but') + 400, 0.25], ['record-scratch', at('so', 3), 0.22]];
  return <AbsoluteFill style={{background: '#000'}}>
    <AbsoluteFill style={{transform: `scale(${k})`}}><svg width={1080} height={1920} viewBox="0 0 1080 1920"><Shot id={id} o={o} a={a} b={b} /></svg></AbsoluteFill>
    <Caption o={o} />
    <Sequence from={Math.round((OFF / 1000) * FPS)}><Audio src={staticFile('inside/vo_emu.wav')} /></Sequence>
    <Audio src={staticFile('music/Fluffing_a_Duck.mp3')} volume={(fr) => { const ms = (fr / FPS) * 1000; return (voiceAt(ms) ? 0.06 : 0.12) * Math.min(1, (EMU_MS - ms) / 800); }} />
    {S.slice(1).map(([, t], i) => <Sequence key={'w' + i} from={Math.max(0, Math.round((t / 1000) * FPS) - 8)}><Audio src={staticFile('sfx/mg-whoosh.mp3')} volume={0.12} /></Sequence>)}
    {sfx.map(([s, t, v], i) => <Sequence key={i} from={Math.round((t / 1000) * FPS)}><Audio src={staticFile(`sfx/${s}.mp3`)} volume={v} /></Sequence>)}
  </AbsoluteFill>;
};

// ClipFarm x BOXABL — 3 animated videos starring an invented BOXABL mascot, "Lil' Casita" (catchphrase: "Unfold the future!").
// NOT photorealistic and NO real people (we don't make realistic fakes of real people). The BOXABL Casita is a clean white modular
// home with big glass doors that folds up, ships on a truck and unfolds on site — that's the only product fact used.
// BOXABL is always spelled B-O-X-A-B-L, printed on the house and on screen. House rules: no colour fades, light blur only, no loud booms.
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, Easing, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
const C = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const io = Easing.inOut(Easing.cubic), out = Easing.out(Easing.cubic);
const lerp = (f: number, a: number, b: number, v0: number, v1: number, e = io) => interpolate(f, [a, b], [v0, v1], {...C, easing: e});
const S = (s: number) => Math.round(s * 30);

// ---------- the Casita (bottom-centre at x,y) ----------
type CasitaP = {x: number; y: number; s?: number; unfold?: number; face?: number; legs?: number; blink?: boolean; flame?: number; t: number; tilt?: number; smile?: number};
const Casita: React.FC<CasitaP> = ({x, y, s = 1, unfold = 1, face = 0, legs = 0, blink, flame = 0, t, tilt = 0, smile = 1}) => {
  const W = 300, H = 230, WW = 220, legH = 70 * legs, hop = legs > 0 ? Math.abs(Math.sin(t / 5)) * 10 * legs : 0;
  const glass = (gx: number, gy: number, gw: number, gh: number, k: string) => <g key={k}>
    <rect x={gx} y={gy} width={gw} height={gh} rx={4} fill="url(#glass)" stroke="#1c1f24" strokeWidth={5} />
    <polygon points={`${gx + gw * 0.15},${gy + 4} ${gx + gw * 0.42},${gy + 4} ${gx + gw * 0.12},${gy + gh - 4} ${gx + 4},${gy + gh - 4} ${gx + 4},${gy + gh * 0.4}`} fill="rgba(255,255,255,0.18)" />
    <line x1={gx + gw / 2} y1={gy} x2={gx + gw / 2} y2={gy + gh} stroke="#1c1f24" strokeWidth={4} />
  </g>;
  const wing = (side: -1 | 1) => <g transform={`translate(${side * W / 2},0) scale(${side * Math.max(0.001, unfold)},1)`}>
    <rect x={0} y={-H} width={WW} height={H} fill="#f6f6f3" stroke="#c9ccd0" strokeWidth={3} />
    {[0.33, 0.66].map((p) => <line key={p} x1={WW * p} y1={-H} x2={WW * p} y2={0} stroke="#e1e3e6" strokeWidth={3} />)}
    {glass(30, -H + 50, WW - 60, H - 70, 'w')}
    <rect x={0} y={-H - 16} width={WW} height={18} fill="#2a2d33" />
  </g>;
  return <g transform={`translate(${x},${y - hop - legH}) rotate(${tilt}) scale(${s})`}>
    {flame > 0 && [-0.3, 0, 0.3].map((p, i) => { const fl = 90 + 40 * Math.sin(t * 1.7 + i * 2);
      return <g key={i} transform={`translate(${p * W},0)`}>
        <polygon points={`-26,0 26,0 0,${fl * flame}`} fill="#ff7a1a" /><polygon points={`-14,0 14,0 0,${fl * flame * 0.6}`} fill="#ffe14d" /></g>; })}
    {legs > 0 && [-1, 1].map((d) => { const sw = Math.sin(t / 5 + (d > 0 ? Math.PI : 0)) * 10 * legs;
      return <g key={d} transform={`translate(${d * 70 + sw},0)`}>
        <rect x={-11} y={0} width={22} height={legH} rx={10} fill="#1c1f24" />
        <ellipse cx={d * 10} cy={legH} rx={36} ry={16} fill="#ff5e3a" stroke="#1c1f24" strokeWidth={5} /></g>; })}
    {wing(-1)}{wing(1)}
    <rect x={-W / 2} y={-H} width={W} height={H} fill="#fbfbf9" stroke="#c9ccd0" strokeWidth={3} />
    {glass(-W / 2 + 46, -H + 70, W - 92, H - 70, 'c')}
    <rect x={-W / 2 - 8} y={-H - 30} width={W + 16} height={34} fill="#2a2d33" />
    <text x={0} y={-H - 4} textAnchor="middle" fontFamily={MONT} fontWeight={800} fontSize={30} letterSpacing={6} fill="#ffffff">BOXABL</text>
    {face > 0 && <g opacity={face}>
      {[-1, 1].map((d) => <g key={d} transform={`translate(${d * 62},${-H + 38})`}>
        <ellipse rx={30} ry={blink ? 3 : 26} fill="#fff" stroke="#1c1f24" strokeWidth={5} />
        {!blink && <circle cx={d * 3} cy={4} r={12} fill="#1c1f24" />}
        {!blink && <circle cx={d * 3 + 4} cy={-1} r={4} fill="#fff" />}</g>)}
      <path d={`M ${-46} ${-H + 120} Q 0 ${-H + 120 + 46 * smile} 46 ${-H + 120}`} fill="none" stroke="#ffffff" strokeWidth={9} strokeLinecap="round" />
      {[-1, 1].map((d) => <ellipse key={'c' + d} cx={d * 100} cy={-H + 70} rx={18} ry={10} fill="#ff8fa0" opacity={0.7} />)}
    </g>}
  </g>;
};

const Truck: React.FC<{x: number; y: number; t: number}> = ({x, y, t}) => <g transform={`translate(${x},${y})`}>
  <rect x={-330} y={-70} width={480} height={36} fill="#3a3f47" />
  <rect x={150} y={-200} width={170} height={170} rx={18} fill="#ff5e3a" stroke="#1c1f24" strokeWidth={6} />
  <rect x={210} y={-180} width={90} height={70} rx={8} fill="#9fd3ff" stroke="#1c1f24" strokeWidth={5} />
  <rect x={-330} y={-40} width={650} height={20} fill="#1c1f24" />
  {[-250, -140, 240].map((wx) => <g key={wx} transform={`translate(${wx},-10) rotate(${t * 12})`}>
    <circle r={42} fill="#1c1f24" /><circle r={18} fill="#9aa1ab" /><rect x={-3} y={-30} width={6} height={60} fill="#9aa1ab" /></g>)}
</g>;

const Car: React.FC<{x: number; y: number; c: string; s?: number}> = ({x, y, c, s = 1}) => <g transform={`translate(${x},${y}) scale(${s})`}>
  <rect x={-90} y={-70} width={180} height={50} rx={16} fill={c} stroke="#1c1f24" strokeWidth={5} />
  <path d="M -55 -70 L -35 -110 L 40 -110 L 60 -70 Z" fill={c} stroke="#1c1f24" strokeWidth={5} />
  <path d="M -42 -74 L -28 -102 L 0 -102 L 0 -74 Z M 8 -74 L 8 -102 L 34 -102 L 48 -74 Z" fill="#9fd3ff" />
  {[-50, 50].map((wx) => <circle key={wx} cx={wx} cy={-20} r={22} fill="#1c1f24" />)}
</g>;

const Sky: React.FC<{night?: boolean; sunset?: boolean}> = ({night, sunset}) => <>
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stopColor={night ? '#0b1236' : sunset ? '#ff9a5a' : '#5db8ff'} /><stop offset="1" stopColor={night ? '#2a2f6a' : sunset ? '#ffd9a0' : '#c8ecff'} /></linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#3b5a7a" /><stop offset="1" stopColor="#16263a" /></linearGradient>
  </defs>
  <rect x={0} y={0} width={1080} height={1920} fill="url(#sky)" />
</>;
const Cloud: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => <g transform={`translate(${x},${y}) scale(${s})`} fill="#fff">
  <circle cx={0} cy={0} r={50} /><circle cx={55} cy={-20} r={62} /><circle cx={115} cy={0} r={48} /><rect x={0} y={0} width={115} height={48} /></g>;
const Yard: React.FC<{y: number}> = ({y}) => <g>
  <rect x={0} y={y} width={1080} height={1920 - y} fill="#59c35a" />
  {Array.from({length: 12}).map((_, i) => <g key={i}><rect x={i * 92} y={y - 120} width={22} height={130} fill="#f2e3c6" stroke="#b9a37c" strokeWidth={3} />
    <polygon points={`${i * 92},${y - 120} ${i * 92 + 11},${y - 140} ${i * 92 + 22},${y - 120}`} fill="#f2e3c6" /></g>)}
  <rect x={0} y={y - 95} width={1080} height={16} fill="#e3d1ad" /><rect x={0} y={y - 45} width={1080} height={16} fill="#e3d1ad" />
  <circle cx={120} cy={y - 220} r={120} fill="#2f9e45" /><rect x={105} y={y - 120} width={30} height={120} fill="#7a5230" />
</g>;
const Sparkles: React.FC<{x: number; y: number; t: number; n?: number; r?: number}> = ({x, y, t, n = 8, r = 260}) => <g>
  {Array.from({length: n}).map((_, i) => { const a = (i / n) * Math.PI * 2 + t / 20, k = (t % 20) / 20, rr = r * (0.6 + 0.4 * k), sz = 18 * (1 - k) + 6;
    const cx = x + Math.cos(a) * rr, cy = y + Math.sin(a) * rr * 0.7;
    return <polygon key={i} points={`${cx},${cy - sz} ${cx + sz * 0.3},${cy - sz * 0.3} ${cx + sz},${cy} ${cx + sz * 0.3},${cy + sz * 0.3} ${cx},${cy + sz} ${cx - sz * 0.3},${cy + sz * 0.3} ${cx - sz},${cy} ${cx - sz * 0.3},${cy - sz * 0.3}`} fill="#ffe14d" />; })}
</g>;

// ---------- text ----------
const stroke = (w: number): React.CSSProperties => ({WebkitTextStroke: `${w}px #000`, paintOrder: 'stroke fill', textShadow: '0 8px 18px rgba(0,0,0,0.45)'});
const Cap: React.FC<{lines: string[]; at: number; f: number; y?: number; hl?: number; size?: number}> = ({lines, at, f, y = 230, hl = -1, size = 84}) => {
  const k = spring({frame: f - at, fps: 30, config: {damping: 12, stiffness: 230}});
  return <div style={{position: 'absolute', top: y, left: 40, right: 40, textAlign: 'center', transform: `scale(${0.7 + 0.3 * k})`}}>
    {lines.map((l, i) => <div key={i} style={{fontFamily: MONT, fontWeight: 800, fontSize: i === hl ? size * 1.25 : size, lineHeight: 1.15, textTransform: 'uppercase', color: i === hl ? '#FFE14D' : '#fff', ...stroke(i === hl ? 14 : 11)}}>{l}</div>)}
  </div>;
};
const Bubble: React.FC<{text: string; x: number; y: number; at: number; f: number}> = ({text, x, y, at, f}) => {
  const k = spring({frame: f - at, fps: 30, config: {damping: 11, stiffness: 260}});
  return <div style={{position: 'absolute', left: x - 330, top: y, width: 660, textAlign: 'center', transform: `scale(${k})`, transformOrigin: '50% 100%'}}>
    <div style={{display: 'inline-block', background: '#fff', border: '7px solid #1c1f24', borderRadius: 40, padding: '20px 34px', fontFamily: MONT, fontWeight: 800, fontSize: 64, color: '#1c1f24'}}>{text}</div>
  </div>;
};
const EndCard: React.FC<{f: number; at: number; t: number; sub: string}> = ({f, at, t, sub}) => {
  const lf = f - at, k = spring({frame: lf, fps: 30, config: {damping: 12, stiffness: 200}});
  return <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 45%, #ffffff 0%, #e8eef5 70%)'}}>
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}><defs><linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#3b5a7a" /><stop offset="1" stopColor="#16263a" /></linearGradient></defs>
      <Casita x={540} y={1180} s={1.25 * k} unfold={1} face={1} legs={1} t={t} blink={lf % 70 < 4} /><Sparkles x={540} y={950} t={lf} r={420} /></svg>
    <div style={{position: 'absolute', top: 300, left: 0, right: 0, textAlign: 'center', transform: `scale(${0.6 + 0.4 * k})`}}>
      <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 170, letterSpacing: 16, color: '#1c1f24'}}>BOXABL</div>
      <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 46, color: '#ff5e3a', marginTop: 4}}>{sub}</div>
    </div>
    <div style={{position: 'absolute', bottom: 260, left: 60, right: 60, textAlign: 'center', fontFamily: MONT, fontWeight: 800, fontSize: 58, color: '#1c1f24'}}>"Unfold the future!"</div>
  </AbsoluteFill>;
};

const Sfx: React.FC<{at: number; file: string; v?: number}> = ({at, file, v = 0.35}) => <Sequence from={Math.max(0, at)}><Audio src={staticFile(`res/${file}`)} volume={v} /></Sequence>;

// ---------- video 1: the unfold ----------
const Unfold: React.FC = () => {
  const f = useCurrentFrame(), t = f;
  const truckX = f < S(2) ? lerp(f, 0, S(2), -500, 470, out) : lerp(f, S(3.1), S(3.8), 470, 1700);
  const jump = lerp(f, S(2.2), S(3.0), 0, 1), boxX = f < S(2.2) ? truckX + 0 : lerp(f, S(2.2), S(3.0), 470, 540);
  const boxY = f < S(2.2) ? 1250 : 1430 - Math.sin(jump * Math.PI) * 260 - (1 - jump) * 180;
  const unfold = lerp(f, S(3.9), S(5.6), 0, 1, Easing.out(Easing.back(1.4)));
  const face = lerp(f, S(6.0), S(6.4), 0, 1), legs = lerp(f, S(6.6), S(7.0), 0, 1, Easing.out(Easing.back(2)));
  const shake = f > S(3.9) && f < S(5.6) ? Math.sin(f * 2.3) * 6 : 0;
  const end = S(10.6);
  return <AbsoluteFill>
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0, transform: `translateX(${shake}px)`}}>
      <Sky /><Cloud x={120} y={420} /><Cloud x={720} y={560} s={0.8} />
      <circle cx={900} cy={300} r={90} fill="#ffe14d" />
      <g transform="translate(540 1500) scale(1.45) translate(-540 -1430)">
      <Yard y={1430} />
      <rect x={0} y={1250} width={1080} height={60} fill="#5e6570" opacity={f < S(3.8) ? 1 : 0} />
      {f < S(3.8) && <Truck x={truckX} y={1290} t={t} />}
      <Casita x={boxX} y={boxY} s={f < S(2.2) ? 0.7 : 1} unfold={unfold} face={face} legs={legs} t={t} blink={f > S(6.4) && f % 60 < 4} />
      {unfold > 0.95 && f < S(7.5) && <Sparkles x={540} y={1250} t={f} />}
      </g>
    </svg>
    {f < S(2.2) && <Cap lines={['POV:', 'your house', 'arrives on a truck']} at={0} f={f} hl={2} />}
    {f >= S(2.2) && f < S(3.9) && <Cap lines={['it hops off…']} at={S(2.2)} f={f} />}
    {f >= S(3.9) && f < S(6.0) && <Cap lines={['and UNFOLDS', 'into a whole house']} at={S(3.9)} f={f} hl={0} />}
    {f >= S(6.0) && f < end && <Cap lines={['meet', "LIL' CASITA"]} at={S(6.0)} f={f} hl={1} />}
    {f >= S(7.6) && f < end && <Bubble text="Unfold the future!" x={540} y={720} at={S(7.6)} f={f} />}
    {f >= end && <EndCard f={f} at={end} t={t} sub="the house that ships on a truck" />}
    <Audio src={staticFile('res/chess_n.mp3')} startFrom={S(40)} volume={0.32} />
    <Sfx at={S(2.2) - 6} file="m_fast-whoosh.mp3" /><Sfx at={S(3.0)} file="pop.mp3" v={0.5} />
    <Sfx at={S(3.9)} file="m_fast-whoosh.mp3" /><Sfx at={S(5.6)} file="m_ding-2.mp3" v={0.3} /><Sfx at={S(7.6)} file="pop.mp3" v={0.5} /><Sfx at={end} file="m_meme-tada.mp3" v={0.3} />
  </AbsoluteFill>;
};

// ---------- video 2: the flying BOXABL ----------
const Flying: React.FC = () => {
  const f = useCurrentFrame(), t = f;
  const hookEnd = S(1.8);
  const lf = f - hookEnd;            // story clock after the hook
  const lift = lerp(lf, S(2.6), S(3.6), 0, 1, Easing.in(Easing.cubic));
  const flyX = lerp(lf, S(3.6), S(6.6), 540, 540), camY = lerp(lf, S(3.4), S(4.4), 0, 1);
  const land = lerp(lf, S(6.6), S(7.6), 0, 1, out);
  const end = hookEnd + S(9.4);
  const cars = ['#ff5e3a', '#3b82f6', '#22c55e', '#f59e0b', '#a855f7', '#ef4444'];
  const Traffic = ({dy = 0, k = 1}: {dy?: number; k?: number}) => <g transform={`translate(0,${dy})`}>
    <rect x={0} y={1300} width={1080} height={620} fill="#4b515b" /><rect x={0} y={1290} width={1080} height={14} fill="#ffe14d" />
    {[1450, 1650, 1850].map((ry, r) => cars.map((c, i) => <Car key={r + '-' + i} x={((i * 260 + r * 120 + (k * t * (r % 2 ? 2 : -2))) % 1500) - 160} y={ry} c={c} s={0.95} />))}
    {[0, 1, 2, 3].map((i) => <rect key={i} x={i * 300 + 40} y={950 - (i % 2) * 120} width={180} height={350 + (i % 2) * 120} fill="#8aa3c2" opacity={0.6} />)}
  </g>;
  const hook = f < hookEnd;
  const houseY = hook ? 820 + Math.sin(f / 4) * 14 : lf < S(2.6) ? 1420 : lf < S(6.6) ? 1420 - lift * 520 + Math.sin(lf / 4) * 12 : lerp(lf, S(6.6), S(7.6), 900, 1500, out);
  const inYard = lf >= S(6.6);
  return <AbsoluteFill>
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
      <Sky sunset={inYard} />
      {[0, 1, 2].map((i) => <Cloud key={i} x={((i * 420 - (hook || lf > S(3.6) ? t * 9 : 0)) % 1400 + 1400) % 1400 - 200} y={300 + i * 170} s={0.9} />)}
      {!inYard && <Traffic dy={hook ? 500 : camY * 520} />}
      {inYard && <Yard y={1500} />}
      <Casita x={hook ? 540 : flyX} y={houseY} unfold={inYard ? land : 1} face={1} legs={inYard ? land : hook || lf > S(2.6) ? 0 : 1} t={t}
        flame={hook ? 1 : inYard ? 1 - land : lerp(lf, S(2.2), S(2.8), 0, 1)} tilt={hook ? Math.sin(f / 6) * 3 : 0} blink={f % 75 < 4} />
      {inYard && land > 0.95 && <Sparkles x={540} y={1300} t={f} />}
    </svg>
    {hook && <Cap lines={['traffic?', 'NOT TODAY']} at={0} f={f} hl={1} y={260} />}
    {!hook && lf < S(2.6) && <Cap lines={['stuck in traffic…']} at={hookEnd} f={f} y={300} />}
    {!hook && lf >= S(2.6) && lf < S(3.8) && <Cap lines={['so it fired up', 'the THRUSTERS']} at={hookEnd + S(2.6)} f={f} hl={1} y={300} />}
    {!hook && lf >= S(3.8) && lf < S(6.6) && <Cap lines={['Tesla. SpaceX.', 'flying cars.', 'BOXABL.']} at={hookEnd + S(3.8)} f={f} hl={2} y={300} />}
    {!hook && lf >= S(6.6) && f < end && <Cap lines={['and parked in', 'the BACKYARD']} at={hookEnd + S(6.6)} f={f} hl={1} y={300} />}
    {f >= end && <EndCard f={f} at={end} t={t} sub="the future gets delivered" />}
    <Audio src={staticFile('res/montagem_n.mp3')} startFrom={S(22)} volume={0.32} />
    <Sfx at={0} file="m_meme-build2.mp3" v={0.25} /><Sfx at={hookEnd - 8} file="m_fast-whoosh.mp3" />
    <Sfx at={hookEnd + S(2.6)} file="m_meme-build2.mp3" v={0.3} /><Sfx at={hookEnd + S(3.8)} file="m_fast-whoosh.mp3" />
    <Sfx at={hookEnd + S(7.6)} file="m_ding-2.mp3" v={0.3} /><Sfx at={end} file="m_meme-tada.mp3" v={0.3} />
  </AbsoluteFill>;
};

// ---------- video 3: nature documentary (Kokoro narration, captions from its word timings) ----------
type W = {text: string; startMs: number; endMs: number};
const Docu: React.FC<{words: W[]; dur: number}> = ({words, dur}) => {
  const f = useCurrentFrame(), t = f, ms = (f / 30) * 1000;
  const at = (w: string) => S((words.find((x) => x.text.toLowerCase().replace(/[^a-z]/g, '').startsWith(w))?.startMs ?? 0) / 1000);
  const tArrive = at('arrives'), tUnfold = at('unfolds'), tHome = at('whole'), tMag = at('magnificent');
  const end = S(dur);
  const truckX = lerp(f, tArrive - 10, tArrive + S(1.6), -500, 470, out);
  const onYard = f > tArrive + S(2.2);
  const unfold = lerp(f, tUnfold, tUnfold + S(1.6), 0, 1, Easing.out(Easing.back(1.4)));
  const peek = lerp(f, tUnfold - S(1.2), tUnfold - S(0.6), 0, 1);
  const bino = f < tArrive ? 1 : lerp(f, tArrive, tArrive + 10, 1, 0);
  const chunks: W[][] = [];
  words.forEach((w, i) => { const c = chunks[chunks.length - 1], p = words[i - 1];
    if (!c || c.length >= 3 || /[.,?!]$/.test(p.text)) chunks.push([w]); else c.push(w); });
  const chunk = chunks.filter((c) => c[0].startMs <= ms).pop() ?? [];
  return <AbsoluteFill>
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
      <Sky sunset /><Cloud x={80} y={380} s={0.8} /><Cloud x={700} y={520} s={0.7} />
      <circle cx={820} cy={430} r={120} fill="#ffcf6a" />
      <g transform="translate(540 1500) scale(1.45) translate(-540 -1430)">
      <Yard y={1430} />
      {!onYard && f >= tArrive - 10 && <><rect x={0} y={1250} width={1080} height={60} fill="#5e6570" /><Truck x={truckX} y={1290} t={t} /></>}
      {!onYard && f >= tArrive - 10 && <Casita x={truckX} y={1250} s={0.7} unfold={0} t={t} />}
      {(onYard || f < tArrive - 10) && <Casita x={540} y={1430} unfold={f < tArrive - 10 ? 1 : unfold} face={f < tArrive - 10 ? 1 : Math.max(peek, unfold)} legs={unfold > 0.9 ? lerp(f, tHome, tHome + 10, 0, 1) : 0} t={t} blink={f % 80 < 4} smile={unfold > 0.5 ? 1 : 0.2} />}
      {unfold > 0.95 && <Sparkles x={540} y={1250} t={f} />}
      </g>
      {bino > 0 && <g opacity={bino}><mask id="bino"><rect x={0} y={0} width={1080} height={1920} fill="#fff" /><circle cx={330} cy={1250} r={310} fill="#000" /><circle cx={750} cy={1250} r={310} fill="#000" /></mask>
        <rect x={0} y={0} width={1080} height={1920} fill="#000" mask="url(#bino)" /></g>}
    </svg>
    {f < S(3) && <div style={{position: 'absolute', left: 50, bottom: 360, background: '#ffe14d', padding: '10px 24px', fontFamily: MONT, fontWeight: 800, fontSize: 40, color: '#1c1f24', borderRadius: 10}}>THE BOXABL CASITA · in the wild</div>}
    {f < end && chunk.length > 0 && <div style={{position: 'absolute', top: 250, left: 50, right: 50, textAlign: 'center'}}>
      {chunk.map((w, i) => <span key={i} style={{display: 'inline-block', margin: '0 10px', fontFamily: MONT, fontWeight: 800, fontSize: 76, textTransform: 'uppercase',
        color: /boxabl|unfolds|home|magnificent/i.test(w.text) ? '#FFE14D' : '#fff', opacity: w.startMs <= ms ? 1 : 0, ...stroke(11)}}>{w.text.replace(/[,.…]+$/, '')}</span>)}
    </div>}
    {f >= end && <EndCard f={f} at={end} t={t} sub="spotted in a backyard near you" />}
    <Audio src={staticFile('res/boxabl_doc_vo.wav')} volume={1} />
    <Audio src={staticFile('res/einaudi_n.mp3')} startFrom={S(44)} volume={0.12} />
    <Sfx at={tUnfold} file="m_fast-whoosh.mp3" /><Sfx at={tUnfold + S(1.6)} file="m_ding-2.mp3" v={0.25} /><Sfx at={end} file="m_meme-tada.mp3" v={0.3} />
    {tMag > 0 && null}
  </AbsoluteFill>;
};

import DOC from './boxabl_doc.words.json';
const DOC_DUR = Math.max(10, ((DOC as W[]).slice(-1)[0]?.endMs ?? 12000) / 1000 + 0.6);
export const BOXABL: Record<string, {dur: number; C: React.FC}> = {
  bxunfold: {dur: 13.2, C: Unfold},
  bxfly: {dur: 1.8 + 9.4 + 2.8, C: Flying},
  bxdoc: {dur: DOC_DUR + 2.8, C: () => <Docu words={DOC as W[]} dur={DOC_DUR} />},
};
export const Boxabl: React.FC<{edit: string}> = ({edit}) => { const X = BOXABL[edit].C; return <AbsoluteFill style={{background: '#fff'}}><X /></AbsoluteFill>; };

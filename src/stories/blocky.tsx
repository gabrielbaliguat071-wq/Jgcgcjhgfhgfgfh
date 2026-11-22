// Blocky storyteller characters, v2 (own design for the horror-story channel; genre look: box head/torso/limbs + painted face).
// NOT Roblox assets: own face set, own outfits, own hair blocks, no logos. 1 unit ≈ one block; a grown-up is ~5.4 tall.
// Detail: per-face clothing textures (collar/placket/buttons/pocket on the front, seams on the sides, cuffs + hems), skin
// hands, shoes, hair chunks, faces with blink / look / tears / sweat / mouth-open. Animation helpers at the bottom.
import {useMemo} from 'react';
import * as THREE from 'three';

export type Mouth = 'smile' | 'flat' | 'frown' | 'o' | 'open' | 'grin' | 'whisper' | 'hum';
export type FaceSpec = {brow?: 'calm' | 'worried' | 'angry' | 'raised' | 'none'; mouth?: Mouth; open?: number; blink?: number; lookX?: number; lookY?: number; tears?: boolean; sweat?: boolean; eyes?: 'normal' | 'wide' | 'tiny' | 'glow'};
export type Outfit = {top: string; bottom: string; pattern?: 'stars' | 'plaid' | 'stripes' | 'dots' | 'none'; patternColor?: string; shoes?: string; collar?: string; buttons?: boolean; pocket?: boolean; cuffs?: string; topStyle?: 'pajama' | 'tee' | 'sweater' | 'robe'};
export type Pose = {armL?: number; armR?: number; armLz?: number; armRz?: number; legL?: number; legR?: number; head?: number; headTilt?: number; headRoll?: number; lean?: number; bob?: number};
export type Hair = {color: string; style: 'spiky' | 'short' | 'long' | 'bob' | 'bun' | 'none'};
export type Char = {outfit: Outfit; hair: Hair; skin?: string};

const cache = new Map<string, THREE.Texture>();
const tex = (key: string, w: number, h: number, draw: (g: CanvasRenderingContext2D) => void) => {
  const hit = cache.get(key); if (hit) return hit;
  const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d')!);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; cache.set(key, t); return t;
};
export const shade = (hex: string, k: number) => { const c = new THREE.Color(hex); c.multiplyScalar(k); return '#' + c.getHexString(); };
const rnd = (s: number) => { const x = Math.sin(s * 127.1) * 43758.5453; return x - Math.floor(x); };
const star = (g: CanvasRenderingContext2D, x: number, y: number, r: number) => { g.beginPath(); for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + (i * Math.PI) / 5, rr = i % 2 ? r * 0.45 : r; g.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr); } g.closePath(); g.fill(); };

const fabric = (g: CanvasRenderingContext2D, base: string, o: Outfit, w: number, h: number, seed: number) => {
  g.fillStyle = base; g.fillRect(0, 0, w, h);
  for (let i = 0; i < (w * h) / 60; i++) { g.fillStyle = `rgba(${rnd(seed + i) < 0.5 ? '255,255,255' : '0,0,0'},0.05)`; g.fillRect(rnd(seed + i * 3.1) * w, rnd(seed + i * 7.7) * h, 2, 2); }
  const pc = o.patternColor ?? '#ffd84a';
  if (o.pattern === 'stars') { g.fillStyle = pc; for (let y = 22, r = 0; y < h; y += 58, r++) for (let x = r % 2 ? 50 : 18; x < w; x += 64) star(g, x, y, 14); g.fillStyle = 'rgba(255,255,255,0.8)'; for (let i = 0; i < 18; i++) { g.beginPath(); g.arc(rnd(seed + i) * w, rnd(seed + i * 2) * h, 2.5, 0, 7); g.fill(); } }
  if (o.pattern === 'dots') { g.fillStyle = pc; for (let y = 16, r = 0; y < h; y += 34, r++) for (let x = r % 2 ? 30 : 12; x < w; x += 36) { g.beginPath(); g.arc(x, y, 7, 0, 7); g.fill(); } }
  if (o.pattern === 'plaid') { g.globalAlpha = 0.33; g.fillStyle = shade(base, 0.4); for (let x = 0; x < w; x += 52) g.fillRect(x, 0, 16, h); for (let y = 0; y < h; y += 52) g.fillRect(0, y, w, 16); g.globalAlpha = 0.25; g.fillStyle = '#fff'; for (let x = 26; x < w; x += 52) g.fillRect(x, 0, 3, h); g.globalAlpha = 1; }
  if (o.pattern === 'stripes') { g.fillStyle = pc; for (let y = 0; y < h; y += 44) g.fillRect(0, y, w, 16); }
};
const top = (o: Outfit, face: 'front' | 'back' | 'side') => tex(`top-${JSON.stringify(o)}-${face}`, 256, 256, (g) => {
  fabric(g, o.top, o, 256, 256, face === 'front' ? 1 : 2);
  const dk = shade(o.top, 0.7), col = o.collar ?? shade(o.top, 0.75);
  g.fillStyle = dk; g.fillRect(0, 236, 256, 20);
  if (face === 'side') { g.fillStyle = 'rgba(0,0,0,0.12)'; g.fillRect(124, 0, 8, 256); return; }
  if (face === 'back') { g.fillStyle = col; g.fillRect(70, 0, 116, 16); return; }
  const st = o.topStyle ?? 'pajama';
  if (st === 'pajama' || st === 'robe') {
    g.fillStyle = col; g.beginPath(); g.moveTo(64, 0); g.lineTo(128, 70); g.lineTo(192, 0); g.lineTo(168, 0); g.lineTo(128, 44); g.lineTo(88, 0); g.fill();
    g.fillStyle = shade(o.top, 0.85); g.beginPath(); g.moveTo(88, 0); g.lineTo(128, 44); g.lineTo(168, 0); g.fill();
    g.strokeStyle = col; g.lineWidth = 5; g.beginPath(); g.moveTo(128, 70); g.lineTo(128, 236); g.stroke();
    if (o.buttons !== false) for (let y = 92; y < 236; y += 38) { g.fillStyle = '#f4f1e8'; g.beginPath(); g.arc(138, y, 7, 0, 7); g.fill(); g.fillStyle = 'rgba(0,0,0,0.25)'; g.fillRect(135, y - 1, 6, 2); }
    if (o.pocket !== false) { g.strokeStyle = col; g.lineWidth = 5; g.strokeRect(160, 84, 50, 46); g.fillStyle = col; g.fillRect(160, 84, 50, 9); }
    if (st === 'robe') { g.fillStyle = shade(o.top, 0.6); g.fillRect(0, 150, 256, 18); }
  } else if (st === 'tee') { g.fillStyle = col; g.beginPath(); g.arc(128, -6, 44, 0, Math.PI); g.fill(); g.fillStyle = shade(o.top, 0.9); g.beginPath(); g.arc(128, -6, 34, 0, Math.PI); g.fill(); }
  else { g.fillStyle = col; g.fillRect(80, 0, 96, 18); g.fillStyle = 'rgba(0,0,0,0.12)'; for (let y = 236; y < 256; y += 5) g.fillRect(0, y, 256, 2); }
});
const sleeve = (o: Outfit) => tex(`sleeve-${JSON.stringify(o)}`, 128, 256, (g) => {
  fabric(g, o.top, o, 128, 256, 3);
  g.fillStyle = o.cuffs ?? o.collar ?? shade(o.top, 0.7); g.fillRect(0, 218, 128, 38);
  g.fillStyle = 'rgba(0,0,0,0.15)'; g.fillRect(0, 120, 128, 3);
});
const pants = (o: Outfit, face: 'front' | 'side') => tex(`pants-${JSON.stringify(o)}-${face}`, 128, 256, (g) => {
  fabric(g, o.bottom, o, 128, 256, 4);
  g.fillStyle = shade(o.bottom, 0.7); g.fillRect(0, 0, 128, 14);
  g.fillStyle = o.cuffs ?? shade(o.bottom, 0.72); g.fillRect(0, 196, 128, 18);
  g.fillStyle = o.shoes ?? '#e8e4dc'; g.fillRect(0, 214, 128, 42);
  g.fillStyle = 'rgba(0,0,0,0.25)'; g.fillRect(0, 248, 128, 8);
  if (face === 'side') { g.fillStyle = 'rgba(0,0,0,0.12)'; g.fillRect(60, 14, 6, 182); }
});

export const faceTex = (f: FaceSpec, skin: string) => {
  const q = (v: number | undefined, s = 4) => Math.round((v ?? 0) * s) / s;
  const k = {...f, open: q(f.open), blink: q(f.blink), lookX: q(f.lookX), lookY: q(f.lookY)};
  return tex(`face-${JSON.stringify(k)}-${skin}`, 256, 256, (g) => {
    g.fillStyle = skin; g.fillRect(0, 0, 256, 256);
    g.fillStyle = 'rgba(255,140,120,0.18)'; g.beginPath(); g.arc(70, 150, 18, 0, 7); g.arc(186, 150, 18, 0, 7); g.fill();
    const lx = k.lookX * 7, ly = k.lookY * 6, bl = k.blink;
    const eyeR = k.eyes === 'wide' ? 22 : k.eyes === 'tiny' ? 9 : 17;
    const eye = (x: number) => {
      const h = eyeR * (1 - bl);
      if (h < 3) { g.strokeStyle = '#1b1b1f'; g.lineWidth = 5; g.beginPath(); g.moveTo(x - 13, 118); g.lineTo(x + 13, 118); g.stroke(); return; }
      if (k.eyes === 'wide') { g.fillStyle = '#fff'; g.beginPath(); g.ellipse(x, 118, 20, h + 2, 0, 0, 7); g.fill(); }
      g.fillStyle = k.eyes === 'glow' ? '#e8f6ff' : '#1b1b1f'; g.beginPath(); g.ellipse(x + lx, 118 + ly, k.eyes === 'wide' ? 10 : 12, k.eyes === 'wide' ? Math.min(h, 12) : h, 0, 0, 7); g.fill();
      if (k.eyes !== 'glow') { g.fillStyle = '#fff'; g.beginPath(); g.arc(x + lx + 4, 110 + ly, 4, 0, 7); g.fill(); }
    };
    eye(92); eye(164);
    g.strokeStyle = '#2a2220'; g.lineWidth = 7; g.lineCap = 'round';
    const b = k.brow ?? 'calm', by = b === 'raised' ? 78 : 86;
    const brow = (x: number, s: number) => { if (b === 'none') return; const inner = b === 'worried' ? -9 : b === 'angry' ? 9 : 0; g.beginPath(); g.moveTo(x - s * 16, by); g.lineTo(x + s * 16, by + inner); g.stroke(); };
    brow(92, 1); brow(164, -1);
    const m = k.mouth ?? 'flat', op = k.open;
    g.lineWidth = 6; g.beginPath();
    if (m === 'smile') g.arc(128, 150, 20, 0.15 * Math.PI, 0.85 * Math.PI);
    else if (m === 'grin') { g.fillStyle = '#3a1717'; g.arc(128, 152, 24, 0, Math.PI); g.fill(); g.fillStyle = '#fff'; g.fillRect(108, 152, 40, 7); }
    else if (m === 'frown') g.arc(128, 182, 16, 1.15 * Math.PI, 1.85 * Math.PI);
    else if (m === 'o' || m === 'open' || m === 'hum') { const r = m === 'hum' ? 5 + 6 * op : m === 'o' ? 11 : 10 + 12 * Math.max(0.3, op); g.fillStyle = '#3a1717'; g.ellipse(128, 168, m === 'hum' ? 9 : 13, r, 0, 0, 7); g.fill(); }
    else if (m === 'whisper') { g.moveTo(116, 166); g.quadraticCurveTo(128, 160 + 8 * op, 140, 166); }
    else { g.moveTo(116, 166); g.lineTo(140, 166); }
    g.stroke();
    if (k.tears) { g.fillStyle = 'rgba(140,200,255,0.9)'; g.beginPath(); g.ellipse(84, 146, 6, 12, 0, 0, 7); g.ellipse(172, 150, 6, 12, 0, 0, 7); g.fill(); }
    if (k.sweat) { g.fillStyle = 'rgba(160,215,255,0.95)'; g.beginPath(); g.moveTo(206, 54); g.quadraticCurveTo(224, 84, 206, 92); g.quadraticCurveTo(190, 84, 206, 54); g.fill(); }
  });
};

const mat = (map?: THREE.Texture, color = '#ffffff') => new THREE.MeshStandardMaterial({map, color, roughness: 0.88});
const MBox = ({s, p, m, r = [0, 0, 0]}: {s: [number, number, number]; p: [number, number, number]; m: THREE.Material | THREE.Material[]; r?: [number, number, number]}) =>
  <mesh position={p} rotation={r} material={m} castShadow receiveShadow><boxGeometry args={s} /></mesh>;
export const Box = ({s, p, c, r = [0, 0, 0], e, ei = 1}: {s: [number, number, number]; p: [number, number, number]; c: string; r?: [number, number, number]; e?: string; ei?: number}) =>
  <mesh position={p} rotation={r} castShadow receiveShadow><boxGeometry args={s} /><meshStandardMaterial color={c} roughness={0.85} emissive={e ?? '#000'} emissiveIntensity={ei} /></mesh>;

const Arm = ({at, rx = 0, rz = 0, m, skin}: {at: [number, number, number]; rx?: number; rz?: number; m: THREE.Material[]; skin: string}) =>
  <group position={at} rotation={[rx, 0, rz]}>
    <MBox s={[0.96, 1.72, 0.96]} p={[0, -0.86, 0]} m={m} />
    <Box s={[0.9, 0.3, 0.9]} p={[0, -1.86, 0]} c={skin} />
  </group>;
const Leg = ({at, rx = 0, m}: {at: [number, number, number]; rx?: number; m: THREE.Material[]}) =>
  <group position={at} rotation={[rx, 0, 0]}><MBox s={[0.98, 2, 0.98]} p={[0, -1, 0]} m={m} /></group>;

export type BlockyProps = Char & {face?: FaceSpec; pose?: Pose; pos?: [number, number, number]; rot?: [number, number, number]; scale?: number; hip?: boolean; sitUp?: number};
/** hip=true: origin at the hips. sitUp (with hip): 0 = lying on the back (head toward -z, face up), 1 = sitting, legs forward */
export const Blocky = ({outfit, hair, skin = '#f1c7a1', face = {}, pose = {}, pos = [0, 0, 0], rot = [0, 0, 0], scale = 1, hip = false, sitUp}: BlockyProps) => {
  const M = useMemo(() => {
    const tf = mat(top(outfit, 'front')), tb = mat(top(outfit, 'back')), ts = mat(top(outfit, 'side')), dk = mat(undefined, shade(outfit.top, 0.8));
    const sl = mat(sleeve(outfit)), sd = mat(undefined, shade(outfit.top, 0.82)), sk = mat(undefined, skin);
    const pf = mat(pants(outfit, 'front')), ps = mat(pants(outfit, 'side')), sh = mat(undefined, outfit.shoes ?? '#e8e4dc');
    return {torso: [ts, ts, dk, dk, tf, tb], arm: [sl, sl, sd, sk, sl, sl], leg: [ps, ps, pf, sh, pf, pf]};
  }, [outfit, skin]);
  const fm = faceTex(face, skin);
  const head = useMemo(() => { const s = mat(undefined, skin); return [s, s, s, s, mat(fm), s]; }, [fm, skin]);
  const H = 2.0, bob = pose.bob ?? 0, s = sitUp;
  const legRx = s === undefined ? undefined : -Math.PI / 2 * s;
  const body = <>
    <Leg at={[-0.5, H, 0]} rx={legRx ?? pose.legL ?? 0} m={M.leg} />
    <Leg at={[0.5, H, 0]} rx={legRx ?? pose.legR ?? 0} m={M.leg} />
    <group position={[0, H, 0]} rotation={[pose.lean ?? 0, 0, 0]}>
      <group position={[0, bob, 0]}>
        <MBox s={[2, 2, 1]} p={[0, 1, 0]} m={M.torso} />
        <Arm at={[-1.5, 1.95, 0]} rx={pose.armL ?? 0} rz={-(pose.armLz ?? 0)} m={M.arm} skin={skin} />
        <Arm at={[1.5, 1.95, 0]} rx={pose.armR ?? 0} rz={pose.armRz ?? 0} m={M.arm} skin={skin} />
        <group position={[0, 2.02, 0]} rotation={[pose.headTilt ?? 0, pose.head ?? 0, pose.headRoll ?? 0]}>
          <Box s={[0.7, 0.12, 0.7]} p={[0, 0.04, 0]} c={shade(skin, 0.85)} />
          <mesh position={[0, 0.66, 0]} material={head} castShadow><boxGeometry args={[1.24, 1.24, 1.24]} /></mesh>
          <HairBlocks hair={hair} />
        </group>
      </group>
    </group>
  </>;
  if (hip) return <group position={pos} rotation={rot} scale={scale}><group rotation={[s === undefined ? 0 : -Math.PI / 2 * (1 - s), 0, 0]}><group position={[0, -H, 0]}>{body}</group></group></group>;
  return <group position={pos} rotation={rot} scale={scale}>{body}</group>;
};

const HairBlocks = ({hair}: {hair: Hair}) => {
  const c = hair.color, d = shade(c, 0.82), l = shade(c, 1.15);
  if (hair.style === 'none') return null;
  const b = (sz: [number, number, number], p: [number, number, number], r: [number, number, number] = [0, 0, 0], col = c) => <Box s={sz} p={p} r={r} c={col} />;
  const cap = <>{b([1.34, 0.36, 1.34], [0, 1.36, -0.02])}{b([1.34, 0.95, 0.3], [0, 0.98, -0.56])}{b([0.26, 0.7, 1.2], [-0.62, 1.02, -0.06], [0, 0, 0], d)}{b([0.26, 0.7, 1.2], [0.62, 1.02, -0.06], [0, 0, 0], d)}</>;
  if (hair.style === 'spiky') return <group>{cap}
    {[-0.42, -0.14, 0.14, 0.42].map((x, i) => <group key={i}>{b([0.34, 0.48, 0.34], [x, 1.66, 0.22 - (i % 2) * 0.34], [0.35 * (i % 2 ? 1 : -1), 0, 0.4 * (x < 0 ? 1 : -1)], i % 2 ? d : l)}</group>)}
    {b([0.46, 0.34, 0.24], [-0.32, 1.16, 0.62], [0, 0, 0.35])}{b([0.46, 0.34, 0.24], [0.22, 1.18, 0.62], [0, 0, -0.3], d)}{b([0.3, 0.3, 0.22], [0.5, 1.1, 0.6], [0, 0, -0.6], l)}
  </group>;
  if (hair.style === 'short') return <group>{cap}{b([1.34, 0.22, 0.22], [0, 1.22, 0.6], [0, 0, 0], d)}{b([0.5, 0.18, 0.22], [-0.3, 1.36, 0.62], [0, 0, 0.2], l)}</group>;
  if (hair.style === 'bob') return <group>{cap}{b([0.28, 1.2, 1.34], [-0.7, 0.78, 0])}{b([0.28, 1.2, 1.34], [0.7, 0.78, 0])}{b([1.38, 1.2, 0.28], [0, 0.78, -0.68])}{b([1.38, 0.24, 0.24], [0, 1.24, 0.62], [0, 0, 0], d)}{b([0.4, 0.4, 0.4], [0.55, 1.45, 0.3], [0, 0.4, 0.4], '#ff8fb8')}</group>;
  if (hair.style === 'bun') return <group>{cap}{b([0.62, 0.62, 0.62], [0, 1.72, -0.3], [0.3, 0.3, 0], l)}{b([1.38, 0.24, 0.24], [0, 1.24, 0.62], [0, 0, 0], d)}</group>;
  return <group>{cap}{b([0.28, 2.0, 1.34], [-0.7, 0.4, 0])}{b([0.28, 2.0, 1.34], [0.7, 0.4, 0])}{b([1.38, 2.3, 0.3], [0, 0.25, -0.68])}{b([1.38, 0.24, 0.24], [0, 1.24, 0.62], [0, 0, 0], d)}{b([0.5, 0.26, 0.24], [-0.32, 1.12, 0.64], [0, 0, 0.3], l)}</group>;
};

// ---- animation helpers (o = ms) ----
export const breathe = (o: number, amt = 0.03) => Math.sin(o / 620) * amt;
export const blinkAt = (o: number, seed = 0) => { const p = (o + seed * 997) % 3300; return p < 120 ? 1 - Math.abs(p - 60) / 60 : 0; };
export const tremble = (o: number, amt = 0.04) => Math.sin(o / 23) * amt + Math.sin(o / 37) * amt * 0.6;
export const walk = (o: number, speed = 1): Pose => { const a = Math.sin((o / 260) * speed) * 0.55; return {legL: a, legR: -a, armL: -a * 0.8, armR: a * 0.8, bob: Math.abs(Math.cos((o / 260) * speed)) * 0.08}; };

export const CAST = {
  me: {outfit: {top: '#4f8fe0', bottom: '#4f8fe0', pattern: 'stars', patternColor: '#ffd84a', collar: '#24539a', cuffs: '#24539a', shoes: '#f0ece4'} as Outfit, hair: {color: '#7a4a24', style: 'spiky'} as Hair},
  leo: {outfit: {top: '#3fae6a', bottom: '#2f7f4f', pattern: 'stripes', patternColor: '#8fdcac', collar: '#1f6a3e', cuffs: '#1f6a3e', shoes: '#d9d4ca', pocket: false} as Outfit, hair: {color: '#2a1d16', style: 'short'} as Hair},
  mia: {outfit: {top: '#f39bc0', bottom: '#f39bc0', pattern: 'dots', patternColor: '#ffffff', collar: '#c9628c', cuffs: '#c9628c', shoes: '#ffe3ef'} as Outfit, hair: {color: '#e8b04a', style: 'bob'} as Hair},
  mom: {outfit: {top: '#7d63b5', bottom: '#3a3a52', pattern: 'none', topStyle: 'robe', collar: '#5c4790', cuffs: '#5c4790', shoes: '#c9b9a6', buttons: false, pocket: false} as Outfit, hair: {color: '#5a2e1c', style: 'long'} as Hair},
};

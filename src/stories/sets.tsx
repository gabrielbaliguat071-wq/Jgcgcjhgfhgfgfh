// Sets for the blocky horror stories: kids' bedroom (3 beds, window, door to a lit hallway), beds, night exterior.
import {useMemo} from 'react';
import * as THREE from 'three';
import {Box, shade} from './blocky';

const cache = new Map<string, THREE.Texture>();
const tex = (key: string, w: number, h: number, rep: [number, number], draw: (g: CanvasRenderingContext2D) => void) => {
  const hit = cache.get(key); if (hit) return hit;
  const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d')!);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...rep); t.anisotropy = 8; cache.set(key, t); return t;
};
const rnd = (s: number) => { const x = Math.sin(s * 91.7) * 43758.5453; return x - Math.floor(x); };
export const woodTex = () => tex('wood', 512, 512, [3, 3], (g) => {
  for (let i = 0; i < 8; i++) { g.fillStyle = shade('#8a5a36', 0.85 + rnd(i) * 0.3); g.fillRect(0, i * 64, 512, 64); g.fillStyle = 'rgba(0,0,0,0.35)'; g.fillRect(0, i * 64, 512, 3); g.fillRect(((i * 173) % 512), i * 64, 3, 64); }
  for (let i = 0; i < 400; i++) { g.fillStyle = `rgba(40,20,10,${0.05 + rnd(i + 9) * 0.08})`; g.fillRect(rnd(i) * 512, rnd(i * 3) * 512, 30 + rnd(i * 5) * 60, 1.5); }
});
export const wallTex = (base = '#6d86b8') => tex('wall' + base, 256, 256, [6, 3], (g) => {
  g.fillStyle = base; g.fillRect(0, 0, 256, 256);
  g.fillStyle = shade(base, 1.12); for (let x = 0; x < 256; x += 32) g.fillRect(x, 0, 10, 256);
  g.fillStyle = 'rgba(255,255,255,0.18)'; for (let i = 0; i < 12; i++) { const x = 16 + (i % 4) * 64, y = 20 + Math.floor(i / 4) * 86 + (i % 2) * 30; g.beginPath(); g.arc(x, y, 4, 0, 7); g.fill(); }
});
const quiltTex = (c: string) => tex('quilt' + c, 256, 256, [1, 1], (g) => {
  g.fillStyle = c; g.fillRect(0, 0, 256, 256);
  g.strokeStyle = shade(c, 0.75); g.lineWidth = 4; for (let x = 0; x <= 256; x += 64) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, 256); g.stroke(); g.beginPath(); g.moveTo(0, x); g.lineTo(256, x); g.stroke(); }
  g.fillStyle = 'rgba(255,255,255,0.25)'; for (let y = 32; y < 256; y += 64) for (let x = 32; x < 256; x += 64) { g.beginPath(); g.arc(x, y, 6, 0, 7); g.fill(); }
});
const grassTex = () => tex('grass', 256, 256, [14, 14], (g) => { g.fillStyle = '#2f4a2a'; g.fillRect(0, 0, 256, 256); for (let i = 0; i < 1600; i++) { g.fillStyle = `rgba(${rnd(i) < 0.5 ? '120,170,90' : '20,40,20'},0.25)`; g.fillRect(rnd(i * 2) * 256, rnd(i * 3) * 256, 2, 4); } });
const sidingTex = (c: string) => tex('siding' + c, 256, 256, [3, 4], (g) => { g.fillStyle = c; g.fillRect(0, 0, 256, 256); g.fillStyle = 'rgba(0,0,0,0.22)'; for (let y = 0; y < 256; y += 32) g.fillRect(0, y + 28, 256, 4); });

/** a bed: headboard at -z. top of mattress at y = BED_TOP; clear space under it (y < 1.3) for the thing under the bed */
export const BED_TOP = 2.3;
export const Bed = ({x, quilt, blanket = 1, z = 0}: {x: number; quilt: string; blanket?: number; z?: number}) => {
  const q = useMemo(() => quiltTex(quilt), [quilt]);
  const frame = '#6b4126';
  return <group position={[x, 0, z]}>
    {[[-1.6, -3.1], [1.6, -3.1], [-1.6, 3.1], [1.6, 3.1]].map(([a, b], i) => <Box key={i} s={[0.3, 1.3, 0.3]} p={[a, 0.65, b]} c={shade(frame, 0.8)} />)}
    <Box s={[3.5, 0.3, 6.6]} p={[0, 1.45, 0]} c={frame} />
    <Box s={[3.3, 0.7, 6.4]} p={[0, 1.95, 0]} c="#e9e6df" />
    <Box s={[3.7, 3.6, 0.3]} p={[0, 1.8, -3.4]} c={frame} />
    <Box s={[3.7, 0.3, 0.45]} p={[0, 3.6, -3.4]} c={shade(frame, 1.2)} />
    <Box s={[3.7, 1.3, 0.3]} p={[0, 1.95, 3.4]} c={frame} />
    <Box s={[2.4, 0.45, 1.1]} p={[0, 2.5, -2.55]} c="#f5f2ea" />
    {blanket > 0 && <mesh position={[0, 2.88, 1.35 + (1 - blanket) * 1.0]} castShadow receiveShadow><boxGeometry args={[3.5, 0.62, 4.1 - (1 - blanket) * 2.0]} /><meshStandardMaterial map={q} roughness={0.95} /></mesh>}
    {/* slats seen from under the bed */}
    {[-2.4, -1.2, 0, 1.2, 2.4].map((b, i) => <Box key={'s' + i} s={[3.3, 0.12, 0.5]} p={[0, 1.34, b]} c={shade(frame, 0.6)} />)}
  </group>;
};

export const BEDS = {leo: -5.4, me: 0, mia: 5.4};
/** the kids' room: back wall z=-4, right wall x=9.5 with a door to a lit hallway (x>9.5), window over Mia's bed */
export const Bedroom = ({moon = 1, hall = 1, gloom = 1, blankets = {leo: 1, me: 1, mia: 1}}: {moon?: number; hall?: number; gloom?: number; blankets?: {leo: number; me: number; mia: number}}) => {
  const wood = woodTex(), wall = wallTex();
  return <group>
    <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[40, 40]} /><meshStandardMaterial map={wood} roughness={0.8} /></mesh>
    <mesh position={[0, 6, -4.1]} receiveShadow><planeGeometry args={[40, 12]} /><meshStandardMaterial map={wall} /></mesh>
    <mesh position={[-11, 6, 4]} rotation={[0, Math.PI / 2, 0]} receiveShadow><planeGeometry args={[24, 12]} /><meshStandardMaterial map={wall} /></mesh>
    {/* right wall with a door opening (z 0.6..3.8) */}
    <mesh position={[9.5, 6, -1.9]} rotation={[0, -Math.PI / 2, 0]} receiveShadow><planeGeometry args={[5, 12]} /><meshStandardMaterial map={wall} /></mesh>
    <mesh position={[9.5, 6, 9.9]} rotation={[0, -Math.PI / 2, 0]} receiveShadow><planeGeometry args={[12.2, 12]} /><meshStandardMaterial map={wall} /></mesh>
    <mesh position={[9.5, 9.6, 2.2]} rotation={[0, -Math.PI / 2, 0]}><planeGeometry args={[3.2, 4.8]} /><meshStandardMaterial map={wall} /></mesh>
    <Box s={[0.4, 7.4, 0.3]} p={[9.5, 3.7, 0.5]} c="#efe8dc" /><Box s={[0.4, 7.4, 0.3]} p={[9.5, 3.7, 3.9]} c="#efe8dc" /><Box s={[0.4, 0.3, 3.7]} p={[9.5, 7.3, 2.2]} c="#efe8dc" />
    {/* open door leaf */}
    <Box s={[3.0, 7.0, 0.25]} p={[11.0, 3.5, 3.95]} c="#d9cdb8" />
    {/* hallway */}
    <mesh position={[15, 6, 2.2]} rotation={[0, -Math.PI / 2, 0]}><planeGeometry args={[14, 12]} /><meshStandardMaterial color="#c9a27a" /></mesh>
    <mesh position={[12.5, 0.01, 2.2]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[6, 14]} /><meshStandardMaterial map={wood} /></mesh>
    <pointLight position={[13, 7.5, 2.2]} intensity={60 * hall} distance={18} decay={1.6} color="#ffb766" castShadow />
    {/* window over Mia's bed */}
    <group position={[5.4, 6.6, -4.0]}>
      <Box s={[3.4, 3.0, 0.1]} p={[0, 0, 0]} c="#1c2a4a" e="#4a6aa8" ei={0.6 * moon} />
      <Box s={[3.7, 0.25, 0.3]} p={[0, 1.6, 0.1]} c="#efe8dc" /><Box s={[3.7, 0.25, 0.3]} p={[0, -1.6, 0.1]} c="#efe8dc" />
      <Box s={[0.25, 3.4, 0.3]} p={[-1.75, 0, 0.1]} c="#efe8dc" /><Box s={[0.25, 3.4, 0.3]} p={[1.75, 0, 0.1]} c="#efe8dc" /><Box s={[0.15, 3.0, 0.2]} p={[0, 0, 0.1]} c="#efe8dc" />
      <Box s={[4.6, 3.8, 0.12]} p={[-3.3, -0.2, 0.25]} c="#3d4f86" /><Box s={[1.0, 3.8, 0.12]} p={[2.4, -0.2, 0.25]} c="#3d4f86" />
    </group>
    {/* furniture + clutter */}
    <Box s={[1.6, 1.8, 1.4]} p={[-2.7, 0.9, -3.2]} c="#7a4d2c" /><Box s={[0.6, 0.9, 0.6]} p={[-2.7, 2.25, -3.2]} c="#d8c28a" e="#ffcf7a" ei={0} />
    <Box s={[1.6, 1.8, 1.4]} p={[2.7, 0.9, -3.2]} c="#7a4d2c" />
    <mesh position={[0, 0.02, 4.8]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow><circleGeometry args={[3.2, 40]} /><meshStandardMaterial color="#b3483f" roughness={1} /></mesh>
    <Box s={[2.2, 2.8, 0.1]} p={[-8.2, 7.2, -4.0]} c="#22305a" /><Box s={[1.6, 1.6, 0.12]} p={[-8.2, 7.2, -3.94]} c="#f3c74a" />
    <Box s={[1.2, 1.2, 1.2]} p={[-8.6, 0.6, 2.5]} c="#c44a4a" /><Box s={[1.0, 0.8, 1.0]} p={[-8.4, 1.6, 2.6]} c="#4a86c4" />
    <Bed x={BEDS.leo} quilt="#3e8c5a" blanket={blankets.leo} />
    <Bed x={BEDS.me} quilt="#3f6fbf" blanket={blankets.me} />
    <Bed x={BEDS.mia} quilt="#d96c9a" blanket={blankets.mia} />
    {/* night light */}
    <hemisphereLight args={['#7f97d8', '#2a2030', 1.25 * gloom]} />
    <ambientLight intensity={0.35 * gloom} color="#8090c0" />
    <directionalLight position={[8, 12, -14]} target-position={[0, 0, 2]} intensity={2.6 * moon} color="#a9c2ff" castShadow shadow-mapSize={[1024, 1024]} shadow-camera-left={-14} shadow-camera-right={14} shadow-camera-top={14} shadow-camera-bottom={-14} />
  </group>;
};

const Tree = ({p, s = 1}: {p: [number, number, number]; s?: number}) => <group position={p} scale={s}>
  <Box s={[0.9, 3, 0.9]} p={[0, 1.5, 0]} c="#4a3020" />
  <Box s={[4.2, 2.2, 4.2]} p={[0, 3.6, 0]} c="#1f3d26" /><Box s={[3.2, 2, 3.2]} p={[0, 5.4, 0]} c="#244a2d" /><Box s={[2, 1.8, 2]} p={[0, 7, 0]} c="#2a5634" />
</group>;
/** night street: the family house (lit window upstairs = the kids' room), fence, trees, street lamp, moon */
export const HouseNight = ({window = 1}: {window?: number}) => {
  const grass = grassTex(), siding = sidingTex('#8b9cc4');
  const roof = '#3a3346';
  return <group>
    <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[160, 160]} /><meshStandardMaterial map={grass} roughness={1} /></mesh>
    <mesh position={[0, 0.02, 14]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[160, 6]} /><meshStandardMaterial color="#2c2c33" /></mesh>
    <mesh position={[0, 6, 0]} castShadow receiveShadow><boxGeometry args={[14, 12, 9]} /><meshStandardMaterial map={siding} /></mesh>
    <mesh position={[0, 14.2, 0]} rotation={[0, 0, Math.PI / 4]} castShadow><boxGeometry args={[10.4, 10.4, 9.6]} /><meshStandardMaterial color={roof} /></mesh>
    {/* windows: upstairs left = kids' room (lit) */}
    {[[-3.8, 8.6, window], [3.8, 8.6, 0.05], [-3.8, 3.2, 0], [3.8, 3.2, 0.12]].map(([x, y, l], i) => <group key={i} position={[x, y, 4.52]}>
      <Box s={[3, 2.8, 0.1]} p={[0, 0, 0]} c={l > 0.2 ? '#ffcf7a' : '#1b2238'} e={l > 0.2 ? '#ffb24a' : '#000'} ei={1.4 * l} />
      <Box s={[3.3, 0.25, 0.3]} p={[0, 1.5, 0.05]} c="#e8e2d6" /><Box s={[3.3, 0.25, 0.3]} p={[0, -1.5, 0.05]} c="#e8e2d6" /><Box s={[0.2, 2.8, 0.25]} p={[0, 0, 0.05]} c="#e8e2d6" />
    </group>)}
    <pointLight position={[-3.8, 8.6, 6.5]} intensity={18 * window} distance={12} color="#ffb24a" />
    <Box s={[2.2, 4.2, 0.2]} p={[0, 2.1, 4.55]} c="#5b2f2a" /><Box s={[4.5, 0.4, 2.4]} p={[0, 0.2, 5.6]} c="#9a9488" />
    {Array.from({length: 18}, (_, i) => <Box key={i} s={[0.3, 1.6, 0.3]} p={[-13 + i * 1.6, 0.8, 9.5]} c="#d9d4ca" />)}
    <Box s={[28, 0.25, 0.2]} p={[0, 1.3, 9.5]} c="#d9d4ca" />
    <Tree p={[-12, 0, -2]} s={1.3} /><Tree p={[13, 0, -4]} s={1.5} /><Tree p={[-20, 0, 6]} s={1.2} /><Tree p={[20, 0, 4]} s={1.1} />
    <group position={[9, 0, 12]}><Box s={[0.35, 9, 0.35]} p={[0, 4.5, 0]} c="#2a2a30" /><Box s={[1.4, 0.6, 1.4]} p={[0, 9.1, 0]} c="#ffe3a8" e="#ffcf7a" ei={2} />
      <pointLight position={[0, 8.4, 0]} intensity={40} distance={16} color="#ffd59a" castShadow /></group>
    <mesh position={[-30, 46, -80]}><sphereGeometry args={[6, 32, 32]} /><meshBasicMaterial color="#e8eeff" /></mesh>
    <hemisphereLight args={['#6a80c4', '#141826', 1.1]} />
    <directionalLight position={[-20, 30, 10]} intensity={0.9} color="#9db8ff" castShadow shadow-mapSize={[1024, 1024]} shadow-camera-left={-30} shadow-camera-right={30} shadow-camera-top={30} shadow-camera-bottom={-30} />
  </group>;
};

// HORROR STORY #1 — "The Count" (1080x1920, 30 fps, ~45 s). Own blocky characters + sets (src/stories), Kokoro narration,
// one-word captions (style of the user's reference). Every shot hangs off the narration's word timestamps.
// Music: "Darkest Child" Kevin MacLeod (incompetech.com), CC BY 4.0 — credit in the description. SFX: myinstants.
import {ThreeCanvas} from '@remotion/three';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import * as THREE from 'three';
import '../mgFonts';
import {Cam, Env, lerp3, prog, smoother, type V3} from '../inside/kit/three';
import {Blocky, CAST, blinkAt, breathe, tremble, walk, type FaceSpec, type Pose} from './blocky';
import {BED_TOP, BEDS, Bedroom, HouseNight} from './sets';
import raw from '../inside/vo_count.words.json';

const FPS = 30, OFF = 300;
const W = (raw as {text: string; startMs: number; endMs: number}[]).map((w) => ({t: w.text, a: w.startMs + OFF, b: w.endMs + OFF}));
export const COUNT_MS = W[W.length - 1].b + 1500;
const S: [string, number][] = [
  ['house', 0], ['mom1', 2380], ['me', 3560], ['leo', 3920], ['mia', 4160], ['wide', 4580], ['frozen', 5800], ['momwalk', 6840], ['four', 8120],
  ['leo2', 9700], ['mia2', 10920], ['me2', 11800], ['shook', 12680], ['nobody', 13920], ['gap', 15080], ['lookdown', 17220], ['kid', 18000],
  ['hair', 18780], ['pj', 19360], ['face', 20200], ['finger', 21180], ['point', 22440], ['momsaid', 23940], ['real', 24640], ['momhum', 26500],
  ['leohum', 28080], ['miahum', 28880], ['kidhum', 29780], ['everyone', 31920], ['mouth', 33140], ['dont', 35180], ['never', 36200],
  ['flash', 37560], ['under', 40100], ['wait', 41000],
].map(([k, t]) => [k as string, (t as number) + OFF]);
const shotAt = (o: number) => { let i = 0; S.forEach(([, t], j) => { if (o >= t) i = j; }); return {id: S[i][0], a: S[i][1], b: S[i + 1]?.[1] ?? COUNT_MS}; };

const KID = 0.8;
const kidZ = 0.6, kidY = BED_TOP + 0.42;
const headOf = (bx: number): V3 => [bx, kidY + 0.35, kidZ - 2.14];       // face-up head centre of a kid lying in bed
const MOM: V3 = [9.3, 0, 2.2];

/** kid in bed: lying (sit 0) .. sitting up (sit 1) */
const BedKid = ({who, bx, o, sit = 0, face, pose = {}}: {who: 'me' | 'leo' | 'mia'; bx: number; o: number; sit?: number; face?: FaceSpec; pose?: Pose}) =>
  <Blocky {...CAST[who]} hip sitUp={sit} pos={[bx, kidY, kidZ]} scale={KID} face={{blink: blinkAt(o, bx), ...face}} pose={{bob: breathe(o, 0.04), ...pose}} />;
/** the thing under the bed: lying on its stomach, head out toward +x, face lifted */
const UnderKid = ({o, face, pose = {}}: {o: number; face?: FaceSpec; pose?: Pose}) =>
  <>
    <Blocky {...CAST.me} hip pos={[BEDS.me, 0.36, 0.9]} rot={[Math.PI / 2, 0, 0]} scale={0.75} face={{blink: blinkAt(o, 7), ...face}} pose={{headTilt: -Math.PI / 2 + 0.12, ...pose}} />
    <pointLight position={[0, 0.5, 5.5]} intensity={6} distance={9} color="#8fb0ff" />
  </>;
const Mom = ({o, face, pose = {}, x = MOM[0], turn = 0}: {o: number; face?: FaceSpec; pose?: Pose; x?: number; turn?: number}) =>
  <Blocky {...CAST.mom} pos={[x, 0, MOM[2]]} rot={[0, -Math.PI / 2 + turn, 0]} scale={1.02} face={{blink: blinkAt(o, 3), ...face}} pose={{bob: breathe(o, 0.03), ...pose}} />;

const Room = ({o, kids = {}, mom, under, moon = 1, blankets}: {o: number; kids?: {leo?: Partial<Parameters<typeof BedKid>[0]>; me?: Partial<Parameters<typeof BedKid>[0]>; mia?: Partial<Parameters<typeof BedKid>[0]>}; mom?: React.ReactNode; under?: React.ReactNode; moon?: number; blankets?: {leo: number; me: number; mia: number}}) => <>
  <Env bg="#05060c" fog={['#070a14', 18, 46]} />
  <Bedroom moon={moon} blankets={blankets} />
  <BedKid who="leo" bx={BEDS.leo} o={o} {...kids.leo} />
  <BedKid who="me" bx={BEDS.me} o={o} {...kids.me} />
  <BedKid who="mia" bx={BEDS.mia} o={o} {...kids.mia} />
  {mom ?? <Mom o={o} />}
  {under}
  <pointLight position={[3, 7, 6]} intensity={9} distance={22} color="#8fa6e8" />
</>;

const closeOn = (h: V3, t: number, d = 3.4): {p: V3; l: V3} => ({p: lerp3([h[0], h[1] + d, h[2] + 1.6], [h[0], h[1] + d * 0.78, h[2] + 1.1], smoother(t)), l: h});
const momHead = (x = MOM[0]): V3 => [x, 5.3, MOM[2]];

const Shot = ({id, o, t}: {id: string; o: number; t: number}) => {
  const st = smoother(t);
  const sh = (amt: number) => tremble(o, amt);
  switch (id) {
    case 'house': return <><Env bg="#060814" fog={['#0a1022', 30, 110]} /><HouseNight /><Cam p={lerp3([2, 5, 34], [-2.5, 8.6, 20], st)} l={[-2.5, 8, 0]} fov={42} far={300} /></>;
    case 'mom1': {
      const look = o < 2620 + OFF ? 0.35 : o < 2980 + OFF ? 0 : -0.35;
      return <><Room o={o} mom={<Mom o={o} face={{brow: 'calm', mouth: 'o'}} pose={{armR: -1.45, armRz: 0.05, head: look}} />} /><Cam p={lerp3([3.4, 5.6, 3.0], [4.2, 5.5, 2.6], st)} l={momHead()} fov={40} /></>;
    }
    case 'me': case 'leo': case 'mia': {
      const bx = BEDS[id as 'me']; const c = closeOn(headOf(bx), t);
      return <><Room o={o} /><Cam p={c.p} l={c.l} fov={38} /></>;
    }
    case 'wide': return <><Room o={o} kids={{me: {face: {lookX: 0.6}}, leo: {face: {lookX: 0.6}}, mia: {face: {lookX: 0.6}}}} mom={<Mom o={o} pose={{armR: -1.2}} />} />
      <Cam p={lerp3([7, 10, 17], [5.5, 9, 14.5], st)} l={[-1, 2.2, -0.5]} fov={52} /></>;
    case 'frozen': return <><Room o={o} kids={{me: {face: {eyes: 'wide', blink: 0, mouth: 'flat'}}, leo: {face: {eyes: 'wide', blink: 0}}, mia: {face: {eyes: 'wide', blink: 0}}}} />
      <Cam p={lerp3([-9.5, 6.2, 7.5], [-8.6, 5.8, 6.4], st)} l={[1, 2.8, -1]} fov={46} /></>;
    case 'momwalk': {
      const x = 9.3 - 2.6 * st;
      return <><Room o={o} mom={<Mom o={o} x={x} face={{brow: 'worried', mouth: 'flat', lookX: Math.sin(o / 500) * 0.8}} pose={{...walk(o, 0.7), head: Math.sin(o / 600) * 0.4}} />} />
        <Cam p={[3.0, 4.2, 5.8]} l={[x, 4.3, 2.2]} fov={44} /></>;
    }
    case 'four': return <><Room o={o} mom={<Mom o={o} x={6.7} face={{brow: 'worried', eyes: 'wide', blink: 0, mouth: 'o'}} pose={{armR: -1.5, head: 0.15}} />} />
      <Cam p={lerp3([1.2, 5.5, 3.4], [2.0, 5.4, 2.8], st)} l={momHead(6.7)} fov={38} /></>;
    case 'leo2': case 'mia2': case 'me2': {
      const who = id.replace('2', '') as 'me'; const c = closeOn(headOf(BEDS[who]), t, 2.6);
      return <><Room o={o} kids={{[who]: {face: {eyes: 'wide', blink: 0, brow: 'worried', lookX: who === 'me' ? 0 : 0.8}}}} mom={<Mom o={o} x={6.7} />} /><Cam p={c.p} l={c.l} fov={38} /></>;
    }
    case 'shook': return <><Room o={o} mom={<Mom o={o} x={6.7} face={{brow: 'worried', eyes: 'wide', mouth: 'frown', sweat: true, lookX: sh(0.4)}} pose={{headRoll: sh(0.05), bob: sh(0.03)}} />} />
      <Cam p={lerp3([1.8, 5.4, 2.4], [2.4, 5.35, 2.2], st)} l={momHead(6.7)} fov={34} /></>;
    case 'nobody': return <><Room o={o} moon={0.7} mom={<Mom o={o} x={6.7} face={{brow: 'worried', eyes: 'wide', blink: 0, mouth: 'whisper', open: (Math.sin(o / 90) + 1) / 2}} pose={{armR: -2.0, armRz: -0.3}} />} />
      <Cam p={lerp3([-2, 6.5, 9], [0, 6, 7], st)} l={[4, 3, 0.5]} fov={46} /></>;
    case 'gap': return <><Room o={o} moon={0.8} /><pointLight position={[0, 0.5, 5.5]} intensity={5} distance={9} color="#8fb0ff" /><Cam p={lerp3([0.3, 0.8, 9.5], [0.1, 0.8, 6.2], st)} l={[0, 0.7, 1]} fov={40} /></>;
    case 'lookdown': return <><Room o={o} moon={0.7} kids={{me: {sit: 1, face: {eyes: 'wide', blink: 0, brow: 'worried', lookY: 1}, pose: {headTilt: 0.6, lean: 0.45}}}} />
      <Cam p={lerp3([0.6, 0.9, 8.6], [0.4, 1.0, 7.4], st)} l={[0, 4.6, 0.8]} fov={46} /></>;
    case 'kid': return <><Room o={o} moon={0.6} under={<UnderKid o={o} face={{eyes: 'wide', blink: 0, mouth: 'flat'}} />} />
      <Cam p={lerp3([0.2, 1.0, 8.2], [0.1, 0.95, 6.0], st)} l={[0, 0.85, 2.9]} fov={38} /></>;
    case 'hair': return <><Room o={o} moon={0.6} under={<UnderKid o={o} face={{eyes: 'wide', blink: 0}} />} /><Cam p={lerp3([0.9, 1.25, 5.4], [0.7, 1.2, 5.0], st)} l={[0, 1.1, 2.9]} fov={34} /></>;
    case 'pj': return <><Room o={o} moon={0.6} under={<UnderKid o={o} face={{eyes: 'wide', blink: 0}} />} /><Cam p={lerp3([2.7, 0.9, 3.0], [2.7, 0.9, -0.6], st)} l={[0, 0.4, lerp3([0, 0, 2.2], [0, 0, -0.4], st)[2]]} fov={42} /></>;
    case 'face': return <><Room o={o} moon={0.6} under={<UnderKid o={o} face={{eyes: 'wide', blink: 0, mouth: 'flat'}} />} /><Cam p={lerp3([0, 0.9, 6.2], [0, 0.88, 5.2], st)} l={[0, 0.86, 2.95]} fov={34} /></>;
    case 'finger': return <><Room o={o} moon={0.6} under={<UnderKid o={o} face={{eyes: 'wide', blink: 0, mouth: 'whisper'}} pose={{armR: -2.95 * smoother(prog(t, 0, 0.4)), armRz: -0.6 * smoother(prog(t, 0, 0.4))}} />} />
      <Cam p={[0.4, 0.95, 5.9]} l={[0, 0.85, 2.9]} fov={38} /></>;
    case 'point': return <><Room o={o} moon={0.6} under={<UnderKid o={o} face={{eyes: 'wide', blink: 0, mouth: 'smile'}} pose={{armR: -3.14 * smoother(prog(t, 0, 0.35)), armRz: -0.15}} />} />
      <Cam p={lerp3([1.2, 1.0, 7.2], [0.9, 1.1, 6.4], st)} l={[0, 1.0, 3.0]} fov={42} /></>;
    case 'momsaid': return <><Room o={o} mom={<Mom o={o} x={6.7} face={{brow: 'calm', mouth: 'flat'}} />} /><Cam p={lerp3([1, 4.8, 6], [2, 4.9, 5], st)} l={momHead(6.7)} fov={44} /></>;
    case 'real': return <><Room o={o} mom={<Mom o={o} x={6.7} face={{brow: 'angry', mouth: 'whisper', open: (Math.sin(o / 110) + 1) / 2, eyes: 'normal'}} />} />
      <Cam p={lerp3([1.6, 5.3, 2.4], [2.3, 5.3, 2.2], st)} l={momHead(6.7)} fov={34} /></>;
    case 'momhum': return <><Room o={o} mom={<Mom o={o} x={6.7} face={{brow: 'calm', mouth: 'hum', open: (Math.sin(o / 160) + 1) / 2, blink: 1}} pose={{headRoll: Math.sin(o / 400) * 0.1}} />} />
      <Cam p={lerp3([1.8, 5.3, 1.6], [2.3, 5.3, 2.0], st)} l={momHead(6.7)} fov={36} /></>;
    case 'leohum': case 'miahum': {
      const who = id === 'leohum' ? 'leo' : 'mia', bx = BEDS[who];
      return <><Room o={o} kids={{[who]: {sit: smoother(prog(t, 0, 0.45)), face: {mouth: 'hum', open: (Math.sin(o / 150) + 1) / 2, brow: 'worried'}, pose: {head: who === 'leo' ? -0.5 : 0.5}}}} mom={<Mom o={o} x={6.7} />} />
        <Cam p={lerp3([bx + 0.4, 5.4, 6.6], [bx + 0.2, 5.2, 5.6], st)} l={[bx, 4.5, kidZ]} fov={40} /></>;
    }
    case 'kidhum': return <><Room o={o} moon={0.6} under={<UnderKid o={o} face={{eyes: 'normal', mouth: 'hum', open: (Math.sin(o / 150) + 1) / 2, brow: 'raised', blink: 0}} />} />
      <Cam p={lerp3([0.5, 0.95, 6.4], [0.2, 0.92, 5.4], st)} l={[0, 0.86, 2.95]} fov={34} /></>;
    case 'everyone': return <><Room o={o} kids={{leo: {sit: 1, face: {lookX: 1, eyes: 'wide', blink: 0}, pose: {head: 0.9}}, mia: {sit: 1, face: {lookX: -1, eyes: 'wide', blink: 0}, pose: {head: -0.9}}, me: {sit: 1, face: {eyes: 'wide', brow: 'worried', blink: 0}}}}
      mom={<Mom o={o} x={3.6} face={{brow: 'angry', lookX: -0.4}} turn={0.35} />} />
      <Cam p={lerp3([0, 8.5, 15], [0, 7.6, 11.5], st)} l={[0, 3.6, 0]} fov={50} /></>;
    case 'mouth': return <><Room o={o} kids={{me: {sit: 1, face: {eyes: 'wide', blink: 0, brow: 'worried', mouth: 'open', open: 0.9, sweat: true}, pose: {headRoll: sh(0.05), bob: sh(0.03)}}, leo: {sit: 1}, mia: {sit: 1}}} mom={<Mom o={o} x={3.6} turn={0.35} />} />
      <Cam p={lerp3([0.2, 5.0, 4.8], [0.1, 4.95, 3.9], st)} l={[0, 4.75, kidZ]} fov={36} /></>;
    case 'dont': return <><Room o={o} kids={{me: {sit: 1, face: {eyes: 'normal', blink: 0, brow: 'worried', mouth: 'frown', tears: true}, pose: {headTilt: 0.15}}, leo: {sit: 1}, mia: {sit: 1}}} mom={<Mom o={o} x={3.6} turn={0.35} />} />
      <Cam p={lerp3([0.6, 4.95, 3.8], [0.3, 4.9, 3.3], st)} l={[0, 4.75, kidZ]} fov={34} /></>;
    case 'never': return <><Room o={o} moon={0.5} kids={{me: {sit: 1, face: {blink: 0, brow: 'worried', mouth: 'frown', tears: true}, pose: {headTilt: 0.3}}, leo: {sit: 1}, mia: {sit: 1}}} mom={<Mom o={o} x={3.6} turn={0.35} />} />
      <Cam p={lerp3([0, 6, 7], [0, 9, 14], st)} l={[0, 4, 0]} fov={46} /></>;
    case 'flash': return <><Room o={o} moon={0.9} blankets={{leo: 1, me: 1, mia: 1}} kids={{me: {face: {blink: 1}}}} />
      <Cam p={lerp3([0.2, 0.75, 0.6], [-0.4, 0.75, 0.9], st)} l={[-9, 1.8, 2.5]} fov={52} /><pointLight position={[-3, 1, 1]} intensity={8} distance={10} color="#ffd9a0" /></>;
    case 'under': return <><Room o={o} moon={0.5} under={<UnderKid o={o} face={{eyes: 'glow', blink: 0, mouth: 'flat', brow: 'none'}} />} />
      <Cam p={lerp3([0.4, 0.95, 6.6], [0.1, 0.9, 5.3], st)} l={[0, 0.86, 2.95]} fov={34} /></>;
    case 'wait': return <><Room o={o} moon={0.6} kids={{me: {face: {blink: 1}}}} under={<UnderKid o={o} face={{eyes: 'glow', blink: 0, mouth: t > 0.55 ? 'smile' : 'flat', brow: 'none'}} />} />
      <Cam p={lerp3([2.6, 4.2, 9.5], [0.3, 0.95, 6.2], smoother(prog(t, 0.1, 1)))} l={lerp3([0, 2.6, 0], [0, 0.86, 2.95], smoother(prog(t, 0.1, 1)))} fov={42} /></>;
  }
  return null;
};

const Caption = ({o}: {o: number}) => {
  const w = [...W].reverse().find((x) => o >= x.a - 40);
  if (!w || o > w.b + 450) return null;
  const k = interpolate(o - w.a, [0, 90], [0.82, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const txt = w.t.replace(/[.,!?"]/g, '');
  return <div style={{position: 'absolute', top: 1150, left: 0, right: 0, textAlign: 'center', transform: `scale(${k})`}}>
    <span style={{fontFamily: 'Inter', fontWeight: 800, fontSize: 92, color: '#fff', WebkitTextStroke: '12px #000', paintOrder: 'stroke fill', textShadow: '0 6px 18px rgba(0,0,0,0.7)'}}>{txt}</span>
  </div>;
};

export const CountShort = () => {
  const f = useCurrentFrame(), o = (f / FPS) * 1000;
  const {id, a, b} = shotAt(o), t = (o - a) / Math.max(1, b - a);
  const flash = id === 'flash';
  const cutK = interpolate(o - a, [0, 120], [1.04, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const voiceAt = (ms: number) => W.some((w) => ms >= w.a - 100 && ms <= w.b + 250);
  return <AbsoluteFill style={{background: '#000'}}>
    <AbsoluteFill style={{transform: `scale(${cutK})`, filter: flash ? 'sepia(0.55) saturate(0.7) contrast(1.1) brightness(0.95)' : undefined}}>
      <ThreeCanvas width={1080} height={1920} shadows camera={{fov: 40, position: [0, 0, 10]}} gl={{toneMapping: THREE.ACESFilmicToneMapping, toneMappingExposure: 1.45}}>
        <Shot id={id} o={o} t={t} />
      </ThreeCanvas>
    </AbsoluteFill>
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 45%, rgba(0,0,0,0.55) 100%)'}} />
    {flash && <AbsoluteFill style={{background: `rgba(255,255,255,${interpolate(o - a, [0, 250], [0.7, 0], {extrapolateRight: 'clamp'})})`}} />}
    <Caption o={o} />
    <Sequence from={Math.round((OFF / 1000) * FPS)}><Audio src={staticFile('inside/vo_count.wav')} /></Sequence>
    <Audio src={staticFile('music/Darkest_Child.mp3')} volume={(fr) => { const ms = (fr / FPS) * 1000; return (voiceAt(ms) ? 0.07 : 0.14) * Math.min(1, (COUNT_MS - ms) / 800); }} />
    {([['h_creaky-door-opens', 6840, 0.35], ['h_d-damage-heartbeat-slow', 8120, 0.55], ['h_horror-sting-1', 18000, 0.45], ['h_d-damage-heartbeat-slow', 33140, 0.5], ['h_horror-game-stinger-boom', 40100, 0.55]] as [string, number, number][])
      .map(([s, t, v], i) => <Sequence key={i} from={Math.round(((t + OFF) / 1000) * FPS)}><Audio src={staticFile(`sfx/${s}.mp3`)} volume={v} /></Sequence>)}
  </AbsoluteFill>;
};

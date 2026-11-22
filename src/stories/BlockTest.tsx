import {ThreeCanvas} from '@remotion/three';
import {AbsoluteFill} from 'remotion';
import * as THREE from 'three';
import {Cam, Env} from '../inside/kit/three';
import {Blocky, CAST} from './blocky';
export const BlockTest = () => <AbsoluteFill style={{background: '#9fc3e8'}}>
  <ThreeCanvas width={1080} height={1920} shadows gl={{toneMapping: THREE.ACESFilmicToneMapping}}>
    <Env bg="#a9c9ec" />
    <Cam p={[0, 4.2, 17]} l={[0, 3.3, 0]} fov={40} />
    <hemisphereLight args={['#ffffff', '#6f8f5a', 1.1]} />
    <directionalLight position={[5, 10, 8]} intensity={2.2} castShadow />
    <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[40, 40]} /><meshStandardMaterial color="#6f9e55" /></mesh>
    <Blocky {...CAST.me} face={{brow: "worried", mouth: "frown"}} pos={[-1.4, 0, 1]} rot={[0, 0.2, 0]} scale={0.85} pose={{armL: 0.1, armR: -0.1}} />
    <Blocky {...CAST.mom} face={{mouth: "smile"}} pos={[1.9, 0, -1.2]} rot={[0, -0.2, 0]} scale={1.0} />
  </ThreeCanvas>
</AbsoluteFill>;

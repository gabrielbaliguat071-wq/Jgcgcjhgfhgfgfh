// CNPL pickleball (Content Rewards, Nov 20): true 9:16 re-crop that follows the action (cx = tracked centre per 0.1 s),
// hook text top third (white, bold, soft shadow, 2 lines max), CNPL icon watermark bottom-left ~9% width for the whole clip
// (above the platform UI zone, off the ball). Original match audio, no intro/outro.
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import CFG from './pickle.cfg.json';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
type P = {src: string; srcW: number; srcH: number; dur: number; cx: number[]; hook: string[]; hl: string[]; hookY?: number};
export const PICKLE = CFG as unknown as Record<string, P>;
export const pickleFrames = (id: string) => Math.round(PICKLE[id].dur * 30);

export const Pickle: React.FC<{edit: string}> = ({edit}) => {
  const p = PICKLE[edit], f = useCurrentFrame(), {fps} = useVideoConfig();
  const s = 1920 / p.srcH, vw = p.srcW * s;
  const i = (f / fps) * 10, i0 = Math.min(p.cx.length - 1, Math.floor(i)), i1 = Math.min(p.cx.length - 1, i0 + 1);
  const cx = p.cx[i0] + (p.cx[i1] - p.cx[i0]) * (i - Math.floor(i));
  const left = Math.min(0, Math.max(1080 - vw, 540 - cx * s));
  const parts = (l: string) => l.split(/(\p{Extended_Pictographic}️?)/u).filter(Boolean);
  return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
    <OffthreadVideo src={staticFile(p.src)} style={{position: 'absolute', top: 0, left, width: vw, height: 1920}} />
    <div style={{position: 'absolute', top: p.hookY ?? 250, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><div style={{background: 'rgba(0,0,0,0.5)', borderRadius: 24, padding: '14px 30px', textAlign: 'center'}}>
      {p.hook.map((l, k) => <div key={k} style={{fontFamily: MONT, fontWeight: 800, fontSize: 68, lineHeight: '84px', whiteSpace: 'nowrap', color: '#fff',
        textShadow: '0 4px 14px rgba(0,0,0,0.75), 0 2px 4px rgba(0,0,0,0.9)'}}>
        {parts(l).map((q, j) => /\p{Extended_Pictographic}/u.test(q)
          ? <Img key={j} src={staticFile(`res/emoji/${[...q.replace(/️/g, '')].map((c) => c.codePointAt(0)!.toString(16)).join('-')}.png`)} style={{width: 78, height: 78, verticalAlign: 'middle'}} />
          : <span key={j}>{q.split(' ').map((w, m) => <span key={m} style={{color: p.hl.includes(w) ? '#E02020' : '#fff'}}>{w} </span>)}</span>)}
      </div>)}
    </div></div>
    {/* REQUIRED: CNPL icon watermark, whole clip, bottom corner */}
    <Img src={staticFile('cnpl/wm.png')} style={{position: 'absolute', left: 40, top: 1390, width: 100, height: 100, opacity: interpolate(f, [0, 1], [1, 1])}} />
  </AbsoluteFill>;
};

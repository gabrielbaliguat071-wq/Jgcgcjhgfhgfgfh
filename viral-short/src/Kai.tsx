// Kai Cenat GTA 6 marathon (pool campaign, Nov 21) — layout copied from the user's reference Short ("Kai Cenat Found Bigfoot"):
// Kai's facecam BIG on the top half (reactions first), gameplay full width on the bottom half, ONE big word at a time on the seam
// (white caps on a black box). Hook line names Kai Cenat (campaign rule) on the game panel for the first seconds.
// Campaign rules: NO logos, Kai = main focus, positive only. Source = Twitch clips (1920x1080) from Nov 18+.
import {loadFont} from '@remotion/fonts';
import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import CFG from './kai.cfg.json';

const MONT = 'Montserrat';
loadFont({family: MONT, url: staticFile('res/Montserrat-Black.woff2'), weight: '800'});
type R = {x: number; y: number; w: number; h: number};
type Word = {word: string; startFrame: number; endFrame: number; hi?: boolean};
type Scene = {id: string; videoStartSec: number; durationInFrames: number; words: Word[]};
type KCfg = {src: string; hook: string[]; title?: string[]; titleEmoji: string; cam: R; game: R; music: [string, number]; scenes: Scene[]};
export const KAI = CFG as unknown as Record<string, KCfg>;
export const kaiFrames = (id: string) => KAI[id].scenes.reduce((a, s) => a + s.durationInFrames, 0);

const CAM_H = 900, SEAM = CAM_H, GAME_H = 1920 - SEAM;
const stroke = (w: number): React.CSSProperties => ({WebkitTextStroke: `${w}px #000`, paintOrder: 'stroke fill', textShadow: '0 6px 14px rgba(0,0,0,0.6)'});

const Panel: React.FC<{src: string; start: number; region: R; W: number; H: number; zoom: number; muted?: boolean}> = ({src, start, region, W, H, zoom, muted}) => {
  const s = Math.max(W / region.w, H / region.h) * zoom;
  const left = W / 2 - (region.x + region.w / 2) * s, top = H / 2 - (region.y + region.h / 2) * s;
  return <OffthreadVideo src={staticFile(src)} muted={muted} startFrom={start} style={{position: 'absolute', left, top, width: 1920 * s, height: 1080 * s}} />;
};

export const Kai: React.FC<{edit: string}> = ({edit}) => {
  const cfg = KAI[edit], SC = cfg.scenes, f = useCurrentFrame(), {fps} = useVideoConfig();
  const START: Record<string, number> = {}; SC.reduce((a, s) => { START[s.id] = a; return a + s.durationInFrames; }, 0);
  const si = Math.max(0, SC.findIndex((s) => f >= START[s.id] && f < START[s.id] + s.durationInFrames)), sc = SC[si], lf = f - START[sc.id];
  const hook = si === 0, start = Math.round(sc.videoStartSec * fps);
  const punch = hook ? interpolate(lf, [0, 6, sc.durationInFrames], [1.15, 1.06, 1.1]) : 1 + 0.05 * (lf / sc.durationInFrames);
  const whip = lf < 4 && f > 0 ? [-70, -28, -8, 0][lf] : 0;
  const words = SC.flatMap((s) => s.words.map((w) => ({...w, at: START[s.id] + w.startFrame, end: START[s.id] + w.endFrame})));
  const cur = words.filter((w) => f >= w.at).pop(), nx = cur ? words[words.indexOf(cur) + 1] : undefined;
  const on = cur && f < Math.min(nx ? nx.at : kaiFrames(edit), cur.end + 18);
  const pop = cur ? spring({frame: f - cur.at, fps, config: {damping: 10, stiffness: 300}}) : 1;
  const hk = spring({frame: f, fps, config: {damping: 12, stiffness: 210}});
  const word = cur ? cur.word.replace(/[,.!?]+$/, '').toUpperCase() : '';

  return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
    <Sequence key={sc.id} from={START[sc.id]} durationInFrames={sc.durationInFrames} layout="none">
      <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: CAM_H, overflow: 'hidden', transform: `translateX(${whip}px)`}}>
        <Panel src={cfg.src} start={start} region={cfg.cam} W={1080} H={CAM_H} zoom={punch} muted />
      </div>
      <div style={{position: 'absolute', left: 0, top: SEAM, width: 1080, height: GAME_H, overflow: 'hidden', transform: `translateX(${whip}px)`}}>
        <Panel src={cfg.src} start={start} region={cfg.game} W={1080} H={GAME_H} zoom={hook ? 1.06 : 1} />
      </div>
    </Sequence>

    {hook && <div style={{position: 'absolute', top: SEAM + 120, left: 40, right: 40, textAlign: 'center', transform: `scale(${0.7 + 0.3 * hk})`}}>
      {cfg.hook.map((l, i) => <div key={i} style={{fontFamily: MONT, fontWeight: 800, fontSize: 62, lineHeight: 1.15, textTransform: 'uppercase', color: i === cfg.hook.length - 1 ? '#FFE14D' : '#fff', ...stroke(11)}}>{l}
        {i === cfg.hook.length - 1 && <Img src={staticFile(`res/emoji/${cfg.titleEmoji}.png`)} style={{width: 66, height: 66, verticalAlign: 'middle', marginLeft: 10}} />}</div>)}
    </div>}

    {on && <div style={{position: 'absolute', top: SEAM - 56, left: 0, right: 0, display: 'flex', justifyContent: 'center', transform: `scale(${0.8 + 0.2 * pop})`}}>
      <span style={{fontFamily: MONT, fontWeight: 800, fontSize: 92, lineHeight: '112px', letterSpacing: -1, color: cur!.hi ? '#FFE14D' : '#fff', background: '#000', padding: '0 22px', borderRadius: 6}}>{word}</span>
    </div>}

    <Audio src={staticFile(`res/${cfg.music[0]}.mp3`)} startFrom={Math.round(cfg.music[1] * fps)} volume={0.07} />
    {SC.slice(1).map((s) => <Sequence key={'w' + s.id} from={Math.max(0, START[s.id] - 16)}><Audio src={staticFile('res/m_fast-whoosh.mp3')} volume={0.2} /></Sequence>)}
  </AbsoluteFill>;
};

import React from 'react';
import { Composition } from 'remotion';
import { ViralShort } from './ViralShort';
import { TOTAL_FRAMES } from './clipData';
import { Guess, EDITS, framesOf } from './Guess';
import { Meme, MEME, memeFrames } from './Meme';
import { Stack, STACK, stackFrames } from './Stack';
import { Higgs, HIGGS, higgsFrames } from './Higgs';
import { Boxed, BOXED, boxedFrames } from './Boxed';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="GuessTheFakeMillionaire"
        component={ViralShort}
        durationInFrames={TOTAL_FRAMES}
        fps={30}
        width={1080}
        height={1920}
      />
      {Object.keys(EDITS).map((id) => (
        <Composition key={id} id={`Guess-${id}`} component={Guess} defaultProps={{edit: id}} durationInFrames={framesOf(id)} fps={30} width={1080} height={1920} />
      ))}
      {Object.keys(MEME).map((id) => (
        <Composition key={'m' + id} id={`Meme-${id}`} component={Meme} defaultProps={{edit: id}} durationInFrames={memeFrames(id)} fps={30} width={1080} height={1920} />
      ))}
      {Object.keys(STACK).map((id) => (
        <Composition key={'s' + id} id={`Stack-${id}`} component={Stack} defaultProps={{edit: id}} durationInFrames={stackFrames(id)} fps={30} width={1080} height={1920} />
      ))}
      {Object.keys(HIGGS).map((id) => (
        <Composition key={'h' + id} id={`Higgs-${id}`} component={Higgs} defaultProps={{edit: id}} durationInFrames={higgsFrames(id)} fps={30} width={1080} height={1920} />
      ))}
      {Object.keys(BOXED).map((id) => (
        <Composition key={'b' + id} id={`Boxed-${id}`} component={Boxed} defaultProps={{edit: id}} durationInFrames={boxedFrames(id)} fps={30} width={1080} height={1920} />
      ))}
    </>
  );
};

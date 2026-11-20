import React from 'react';
import { Composition } from 'remotion';
import { ViralShort } from './ViralShort';
import { TOTAL_FRAMES } from './clipData';
import { Guess, EDITS, framesOf } from './Guess';
import { Meme, MEME, memeFrames } from './Meme';
import { Stack, STACK, stackFrames } from './Stack';
import { Higgs, HIGGS, higgsFrames } from './Higgs';
import { Forge, FORGE, forgeFrames } from './Forge';
import { ForgeVO, FVO, fvoFrames } from './ForgeVO';
import { Pull, PULL, pullFrames } from './Pull';
import { Con, CON, conFrames } from './Con';
import { Pickle, PICKLE, pickleFrames } from './Pickle';
import { Boxed, BOXED, boxedFrames } from './Boxed';
import { Topps, TOPPS, toppsFrames } from './Topps';
import { Cursed, CURSED, cursedFrames } from './Cursed';
import { Boxabl, BOXABL } from './Boxabl';
import { BoxablPhoto, BXP, bxpFrames } from './BoxablPhoto';
import { Kreek, KREEK, kreekFrames } from './Kreek';

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
      {Object.keys(PICKLE).map((id) => (
        <Composition key={'pk' + id} id={`Pickle-${id}`} component={Pickle} defaultProps={{edit: id}} durationInFrames={pickleFrames(id)} fps={30} width={1080} height={1920} />
      ))}
      {Object.keys(CON).map((id) => (
        <Composition key={'cn' + id} id={`Con-${id}`} component={Con} defaultProps={{edit: id}} durationInFrames={conFrames(id)} fps={30} width={1080} height={1920} />
      ))}
      {Object.keys(PULL).map((id) => (
        <Composition key={'pl' + id} id={`Pull-${id}`} component={Pull} defaultProps={{edit: id}} durationInFrames={pullFrames(id)} fps={30} width={1080} height={1920} />
      ))}
      {Object.keys(FVO).map((id) => (
        <Composition key={'fv' + id} id={`FVO-${id}`} component={ForgeVO} defaultProps={{edit: id}} durationInFrames={fvoFrames(id)} fps={30} width={1080} height={1920} />
      ))}
      {Object.keys(FORGE).map((id) => (
        <Composition key={'fg' + id} id={`Forge-${id}`} component={Forge} defaultProps={{edit: id}} durationInFrames={forgeFrames(id)} fps={30} width={1080} height={1920} />
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
      {Object.keys(TOPPS).map((id) => (
        <Composition key={'t' + id} id={`Topps-${id}`} component={Topps} defaultProps={{edit: id}} durationInFrames={toppsFrames(id)} fps={30} width={1080} height={1920} />
      ))}
      {Object.keys(CURSED).map((id) => (
        <Composition key={'c' + id} id={`Cursed-${id}`} component={Cursed} defaultProps={{edit: id}} durationInFrames={cursedFrames(id)} fps={30} width={1080} height={1920} />
      ))}
      {Object.keys(BOXABL).map((id) => (
        <Composition key={'x' + id} id={`Boxabl-${id}`} component={Boxabl} defaultProps={{edit: id}} durationInFrames={Math.round(BOXABL[id].dur * 30)} fps={30} width={1080} height={1920} />
      ))}
      {Object.keys(BXP).map((id) => (
        <Composition key={'p' + id} id={`BXP-${id}`} component={BoxablPhoto} defaultProps={{edit: id}} durationInFrames={bxpFrames(id)} fps={30} width={1080} height={1920} />
      ))}
      {Object.keys(KREEK).map((id) => (
        <Composition key={'k' + id} id={`Kreek-${id}`} component={Kreek} defaultProps={{edit: id}} durationInFrames={kreekFrames(id)} fps={30} width={1080} height={1920} />
      ))}
    </>
  );
};

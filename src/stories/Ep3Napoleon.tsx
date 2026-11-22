// WEIRD HISTORY · EP. 3 — Napoleon vs. the Rabbits (1807, per General Thiébault's memoir). Facts: stories/004-napoleon-rabbits/SCRIPT.md.
import {interpolate} from 'remotion';
import {Burst, Coin, Ground, Hills, Sky, SpeedLines, camWrap, cl, ease, pop} from './EmuShort2';
import raw from '../inside/vo_napo.words.json';
import {Badge, Bean, Bunny, Cage, Carriage, Carrot, Episode, EuropeMap, INK, Musket, Napoleon, NameCard, Picnic, Question, Scroll, Stamp, T, Think, atOf, words, type Shot} from './series';

const W = words(raw), at = atOf(W);
export const EP3_MS = W[W.length - 1].b + 3000;
const Berthier = (p: {x: number; y: number; s?: number; o: number; mouth?: 'smile' | 'grin' | 'talk' | 'o' | 'flat'; eyes?: 'dot' | 'wide'; armR?: number; hold?: React.ReactNode; flip?: boolean}) =>
  <Bean hat="plume" shirt="#2b4f9a" pants="#f4f0e6" uniform={false} mustache seed={5} {...p} />;
const Field = ({o, green = true}: {o: number; green?: boolean}) => <><Sky o={o} /><Hills y={1180} green={green} o={o} /><Ground y={1200} green={green} o={o} /></>;
const Horde = ({o, n, cx, cy, spread = 1, toward = 0, s = 0.55}: {o: number; n: number; cx: number; cy: number; spread?: number; toward?: number; s?: number}) =>
  <g>{Array.from({length: n}, (_, i) => { const ang = i * 2.39, r = (60 + (i % 7) * 70) * spread; return <Bunny key={i} x={cx + Math.cos(ang) * r * (1 - toward)} y={cy + Math.sin(ang) * r * 0.45 * (1 - toward) + toward * 120} s={s} o={o} seed={i} flip={Math.cos(ang) > 0} c={['#f4f0e6', '#c9b8a6', '#8a7060', '#f4f0e6'][i % 4]} />; })}</g>;

const shots: Shot[] = [
  ['hook', 0, (o, t) => camWrap(1 + 0.08 * t, 540, 1300, <><rect x={-200} y={-200} width={1480} height={2320} fill="#e2cfa6" /><rect x={-200} y={1420} width={1480} height={800} fill="#8a6a44" stroke={INK} strokeWidth={8} />
    <Badge x={540} y={520} k={pop(o, at('1807'))} fill="#f4e6c4" c={INK} s={120} w={420} h={170}>1807</Badge>
    <rect x={240} y={1300} width={600} height={50} fill="#6b4a2c" stroke={INK} strokeWidth={8} /><Scroll x={540} y={1240} k={0.45} lines={['PEACE', 'TREATY']} />
    <Napoleon x={540} y={1700} s={1.35} mouth="smile" brows="smug" armR={-1.4 + Math.sin(o / 120) * 0.3} o={o} hold={<line x1={0} y1={0} x2={10} y2={-80} stroke={INK} strokeWidth={8} />} />
    {o > at('peace') && <Stamp x={760} y={1000} k={pop(o, at('treaty'), 240)} text="SIGNED" c="#2b8a3a" s={80} />}</>)],
  ['hunt', at('with'), (o, t) => camWrap(1.1, 540, 1300, <><Burst o={o} c1="#9fd6f5" c2="#bfe3f7" /><Napoleon x={420} y={1750} s={1.7} mouth="grin" brows="smug" eyes="closed" o={o} armR={-2.6} />
    <Think x={760} y={700} k={pop(o, at('rabbit'))}><Bunny x={-10} y={70} s={1} o={o} hop={0.3} /></Think></>)],
  ['berthier', at('his'), (o, t) => camWrap(1, 540, 1300, <><Field o={o} /><Berthier x={430} y={1720} s={1.35} o={o} mouth="talk" armR={-1.3} hold={<rect x={-50} y={-20} width={100} height={130} fill="#fff" stroke={INK} strokeWidth={5} />} />
    <NameCard k={pop(o, at('alexandre'))} name="BERTHIER" sub="chief of staff" />
    <g transform="translate(800 820)">{[['big', 'FIELD'], ['lunch', 'LUNCH'], ['hundreds', 'RABBITS']].map(([w, l], i) => o > at(w) - 600 ? <g key={l} transform={`translate(0 ${i * 110}) scale(${pop(o, at(w) - 600)})`}><rect x={-30} y={-30} width={50} height={50} fill="#fff" stroke={INK} strokeWidth={5} /><path d="M-22 -6 L-6 12 L22 -22" stroke="#2b8a3a" strokeWidth={9} fill="none" /><T x={130} y={10} s={50} c={INK}>{l}</T></g> : null)}</g></>)],
  ['field', at('a', 2), (o, t) => camWrap(1.15 - 0.15 * t, 540, 1300, <><Field o={o} />{[[200, 'flag'], [880, 'flag']].map(([x]) => <g key={x as number} transform={`translate(${x} 1220)`}><path d="M0 0 L0 -220" stroke={INK} strokeWidth={8} /><path d="M0 -220 L110 -190 L0 -160 Z" fill="#2b4f9a" stroke={INK} strokeWidth={5} /></g>)}
    {o > at('lunch') && <Picnic x={540} y={1560} k={pop(o, at('lunch'))} />}</>)],
  ['cages', at('and', 1), (o, t) => camWrap(1, 540, 1350, <><Field o={o} />{Array.from({length: 9}, (_, i) => <Cage key={i} x={200 + (i % 3) * 340} y={1450 + Math.floor(i / 3) * 190} k={0.95 - Math.floor(i / 3) * 0.05} o={o} />)}
    {o > at('3,000') - 200 && <Badge x={540} y={640} k={pop(o, at('3,000') - 200)} s={100} w={560}>UP TO 3,000</Badge>}</>)],
  ['arrive', at('napoleon', 1), (o, t, a) => camWrap(1, 540, 1300, <><Field o={o} /><Carriage x={interpolate(o - a, [0, 900], [1300, 760], cl)} y={1640} k={0.9} o={o - a < 900 ? o : 0} />
    <Napoleon x={interpolate(o - a, [900, 1400], [700, 380], cl)} y={1760} s={1.15} walk={o - a > 900 && o - a < 1400 ? o / 120 : 0} mouth="grin" brows="smug" armR={-2.5} o={o} /></>)],
  ['open', at('the', 1), (o, t, a) => camWrap(1.25, 540, 1500, <><Field o={o} />{[0, 1, 2].map((i) => <Cage key={i} x={200 + i * 340} y={1650} k={1.1} open={ease(o, a + i * 120, a + 400 + i * 120)} o={o} />)}<T x={540} y={1180} s={110} k={pop(o, a + 150)}>CLANG!</T></>)],
  ['guns', at('hunters'), (o, t) => camWrap(1, 540, 1300, <><Field o={o} />{[0, 1, 2].map((i) => <g key={i}><Bean x={230 + i * 310} y={1760} s={1.0} hat="bicorne" shirt="#3a6a3a" pants="#f4f0e6" uniform={false} eyes="squint" mouth="grin" brows="smug" o={o} seed={i} armR={-1.5} armL={-1.2} /><Musket x={260 + i * 310} y={1530} k={0.7} rot={-14} /></g>)}
    <Horde o={o} n={5} cx={540} cy={1330} spread={0.6} s={0.35} /></>)],
  ['turn', at('but'), (o, t) => camWrap(1.1, 540, 1400, <><Field o={o} /><Horde o={o} n={10} cx={540} cy={1500} s={0.6} spread={0.8} />{Array.from({length: 3}, (_, i) => <T key={i} x={300 + i * 240} y={1150} s={90} k={pop(o, at('away') + i * 120)}>!</T>)}</>)],
  ['charge', at('they'), (o, t, a) => camWrap(1 + 0.25 * t, 540, 1500, <><Field o={o} /><SpeedLines o={o} n={10} c="#fff" /><Horde o={o} n={22} cx={540} cy={1500 + 300 * t} spread={1.3 - 0.6 * t} s={0.6 + 0.35 * t} />
    {o > at('most') && <Badge x={540} y={640} k={pop(o, at('most'))} fill="#2b4f9a" s={54} w={760} h={120}>MOST POWERFUL MAN IN EUROPE</Badge>}</>)],
  ['napo', at('most'), (o, t) => camWrap(1, 540, 1300, <><Burst o={o} c1="#ffd84a" c2="#ffb84a" /><Napoleon x={540} y={1760} s={1.8} eyes="wide" mouth="o" sweat brows="worried" o={o} />
    <Horde o={o} n={14} cx={540} cy={1880} spread={0.9} s={0.55} /><Badge x={540} y={560} k={1} fill="#2b4f9a" s={54} w={760} h={120}>MOST POWERFUL MAN IN EUROPE</Badge></>)],
  ['laugh', at('at', 2), (o, t) => camWrap(1, 540, 1300, <><Field o={o} />{[0, 1, 2].map((i) => <Bean key={i} x={230 + i * 310} y={1760} s={1.05} hat={i === 1 ? 'plume' : 'bicorne'} shirt={['#3a6a3a', '#2b4f9a', '#7a2a3a'][i]} pants="#f4f0e6" uniform={false} eyes="closed" mouth="grin" o={o} seed={i} tilt={Math.sin(o / 90 + i) * 8} jump={Math.abs(Math.sin(o / 110 + i)) * 20} />)}
    {['HA', 'HA', 'HA'].map((h, i) => <T key={i} x={200 + i * 340} y={1100 - Math.abs(Math.sin(o / 150 + i)) * 40} s={90} c="#ffd84a">{h}</T>)}</>)],
  ['climb', at('then'), (o, t) => camWrap(1.15, 540, 1450, <><Field o={o} /><Napoleon x={540} y={1800} s={1.6} eyes="wide" mouth="yell" sweat brows="worried" o={o} armL={-2.4 + Math.sin(o / 70) * 0.5} armR={2.4 - Math.sin(o / 70) * 0.5} />
    {Array.from({length: 6}, (_, i) => { const p = Math.min(1, Math.max(0, (o - at('climbing') + 200 - i * 180) / 1200)); return <Bunny key={i} x={460 + (i % 2) * 160} y={1800 - p * (180 + (i % 3) * 90)} s={0.5} o={o} seed={i} hop={0.2} flip={i % 2 === 1} />; })}<Horde o={o} n={8} cx={540} cy={1880} spread={0.9} s={0.5} /></>)],
  ['whips', at('the', 6), (o, t) => camWrap(1, 540, 1300, <><Field o={o} /><Horde o={o} n={14} cx={540} cy={1600} s={0.5} />
    <Bean x={200} y={1760} s={1.05} hat="top" shirt="#5a3a22" pants="#2d2a2e" uniform={false} mouth="yell" brows="angry" o={o} armR={-2.6 + Math.sin(o / 60) * 0.8} hold={<path d={`M0 0 Q${60 + Math.sin(o / 60) * 60} -80 ${140 + Math.sin(o / 50) * 40} -10`} stroke={INK} strokeWidth={6} fill="none" />} />
    {o > at('hunters', 1) && <Bean x={880} y={1760} s={1.05} hat="bicorne" shirt="#3a6a3a" pants="#f4f0e6" uniform={false} mouth="yell" brows="angry" flip o={o} armR={-2.6 + Math.sin(o / 55) * 0.8} hold={<rect x={-6} y={-140} width={12} height={150} fill="#7a5532" stroke={INK} strokeWidth={4} />} seed={3} />}
    {o > at('nothing') && <Stamp x={540} y={900} k={pop(o, at('nothing'), 260)} text="NOTHING WORKED" s={80} />}</>)],
  ['flee', at('napoleon', 3), (o, t, a) => camWrap(1, 540, 1300, <><Field o={o} /><SpeedLines o={o} /><Carriage x={820} y={1660} k={0.85} o={0} />
    <Napoleon x={interpolate(o - a, [0, 1400], [80, 640], cl)} y={1780} s={1.0} walk={o / 70} eyes="wide" mouth="yell" sweat o={o} tilt={10} />
    {Array.from({length: 10}, (_, i) => <Bunny key={i} x={interpolate(o - a, [0, 1400], [-200, 380], cl) - (i % 5) * 90} y={1800 + Math.floor(i / 5) * 60} s={0.45} o={o} seed={i} flip />)}</>)],
  ['inside', at('some', 1), (o, t, a) => camWrap(1.35, 540, 1350, <><Field o={o} /><Carriage x={540} y={1660} k={1.1} o={0} />
    <g transform="translate(540 1300)"><rect x={-90} y={-70} width={180} height={130} fill="#8fd0ff" /><g transform={`translate(0 ${Math.sin(o / 60) * 6})`}><Napoleon x={0} y={210} s={0.55} eyes="wide" mouth="o" sweat o={o} /></g></g>
    {Array.from({length: 4}, (_, i) => { const p = Math.min(1, Math.max(0, (o - at('jumped') + 300 - i * 250) / 600)); return <Bunny key={i} x={240 + i * 180 + p * (540 - 240 - i * 180) * 0.6} y={1700 - Math.sin(p * Math.PI) * 420 - p * 100} s={0.5} o={o} hop={0} seed={i} />; })}</>)],
  ['why', at('why'), (o) => <><Burst o={o} c1="#2d2a2e" c2="#3a363b" /><Question x={540} y={1150} k={pop(o, at('why')) * 3} /></>],
  ['tame', at('berthier', 1), (o, t) => <g style={{filter: 'sepia(0.5)'}}>{camWrap(1, 540, 1300, <><Field o={o} /><rect x={560} y={1000} width={420} height={300} fill="#c79a5a" stroke={INK} strokeWidth={8} /><text x={770} y={1100} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={52} fill={INK}>TAME</text><text x={770} y={1170} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={52} fill={INK}>RABBITS</text>
    <Berthier x={260} y={1760} s={1.1} o={o} mouth="grin" armR={-1.4} /><Bean x={800} y={1760} s={1.1} hat="farmer" shirt="#c9493c" pants="#3f5b8a" uniform={false} mouth="grin" flip o={o} seed={2} />
    {[0, 1, 2].map((i) => o > at('bought') + i * 200 && <Coin key={i} x={520 + i * 30} y={1420 - Math.min(1, (o - at('bought') - i * 200) / 400) * 160} k={0.8} />)}
    {o < at('bought') && <Stamp x={540} y={760} k={pop(o, at('wild'))} text="NOT WILD" s={90} />}
    <Bunny x={760} y={1850} s={0.6} o={o} hop={0.3} /><Bunny x={900} y={1880} s={0.55} o={o} hop={0.3} seed={2} /></>)}</g>],
  ['food', at('and', 3), (o, t) => camWrap(1.1, 540, 1300, <><Burst o={o} c1="#ffd2a8" c2="#ffe2c4" /><Bunny x={360} y={1700} s={2.0} o={o} hop={0.1} />
    <Think x={720} y={760} k={pop(o, at('humans'))}><Bean x={-70} y={90} s={0.42} hat="none" shirt="#2b4f9a" uniform={false} mouth="smile" o={o} /><T x={30} y={30} s={70} c={INK}>=</T><Carrot x={120} y={80} k={0.6} /></Think>
    {o > at('food') && <T x={540} y={1300} s={130} c="#ffd84a" k={pop(o, at('food'), 260)}>FOOD!</T>}</>)],
  ['memoir', at('at', 3), (o, t) => camWrap(1, 540, 1300, <><rect x={-200} y={-200} width={1480} height={2320} fill="#e2cfa6" /><rect x={-200} y={1420} width={1480} height={800} fill="#8a6a44" stroke={INK} strokeWidth={8} />
    <Bean x={360} y={1750} s={1.2} hat="bicorne" shirt="#3a6a3a" pants="#f4f0e6" uniform={false} mustache mouth="smile" eyes="squint" o={o} armR={-1.2 + Math.sin(o / 80) * 0.15} hold={<line x1={0} y1={0} x2={20} y2={-90} stroke={INK} strokeWidth={8} />} />
    <Scroll x={760} y={1150} k={pop(o, at('least'))} lines={['MY MEMOIRS', '"...rabbits..."']} /><Badge x={540} y={620} k={pop(o, at('generals'))} fill="#f4e6c4" c={INK} s={56} w={720} h={120}>ONE GENERAL'S STORY</Badge></>)],
  ['end', at('so'), (o, t, a, b) => camWrap(1 + 0.12 * t, 540, 1300, <><Sky o={o} sunset /><Hills y={1180} green o={o} /><Ground y={1200} green o={o} />
    {o < at('chased') ? <EuropeMap k={pop(o, at('conquered'))} /> : <><Napoleon x={interpolate(o - at('chased'), [0, 3400], [150, 980], cl)} y={1760} s={1.0} walk={o / 70} eyes="wide" mouth="yell" sweat o={o} flip tilt={-10} />
      {Array.from({length: 12}, (_, i) => <Bunny key={i} x={interpolate(o - at('chased'), [0, 3400], [-150, 760], cl) - (i % 6) * 90} y={1800 + Math.floor(i / 6) * 60} s={0.45} o={o} seed={i} hat={i === 0} />)}</>}</>)],
];
const sfx: [string, number, number][] = [['jorho-pop', at('1807'), 0.3], ['jorho-click', at('treaty'), 0.35], ['jorho-pop', at('rabbit'), 0.25], ['jorho-ting', at('big'), 0.25], ['jorho-ting', at('lunch'), 0.25],
  ['jorho-pop', at('3,000') - 200, 0.25], ['metal-pipe-clang', at('opened') - 200, 0.12], ['record-scratch', at('but'), 0.2], ['fast-whoosh', at('they'), 0.2], ['huh-cat', at('most'), 0.2],
  ['meme-fahh', at('nothing'), 0.15], ['fast-whoosh', at('ran', 1), 0.2], ['meme-bonk', at('jumped'), 0.25], ['cha-ching', at('bought'), 0.22], ['jorho-ting', at('food'), 0.3]];
export const Ep3Napoleon = () => <Episode cfg={{W, vo: 'inside/vo_napo.wav', ep: 3, next: 'The Man Who Sold the Eiffel Tower', shots, sfx, total: EP3_MS,
  key: /^(1807|napoleon|rabbit|rabbits|3,000|cages|guns|away|europe|laughed|legs|whips|sticks|worked|carriage|inside|why|wild|tame|food|bunnies)$/i}} />;

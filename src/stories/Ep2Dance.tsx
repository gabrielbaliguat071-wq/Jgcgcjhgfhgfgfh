// WEIRD HISTORY · EP. 2 — The Dancing Plague of 1518 (Strasbourg). Facts: stories/003-dancing-plague/SCRIPT.md.
import {interpolate} from 'remotion';
import {Burst, Card, Ground, Hills, Sky, camWrap, cl, ease, pop} from './EmuShort2';
import raw from '../inside/vo_dance.words.json';
import {Badge, Bean, Bulb, Candle, Chapel, Cobbles, Drum, Episode, INK, Lute, MedievalStreet, Mountains, NameCard, Night, Notes, Question, RedShoe, Scroll, Stage, Stamp, T, Think, TimberHouse, atOf, dance, words, type Shot} from './series';

const W = words(raw), at = atOf(W);
export const EP2_MS = W[W.length - 1].b + 3000;
const TROFFEA = {hat: 'bonnet' as const, shirt: '#3f7a5a', pants: '#3f7a5a', dress: '#2f6a4a', uniform: false};
const TOWN = [{shirt: '#8a3a2a', dress: '#6b2a1f'}, {shirt: '#3a5a8a'}, {shirt: '#c9a24a', dress: '#a8822a'}, {shirt: '#6b4a8a'}, {shirt: '#4a7a3a', dress: '#3a6a2a'}, {shirt: '#a85a3a'}];
const Townie = ({i, x, y, s = 0.8, o, k = 1, face}: {i: number; x: number; y: number; s?: number; o: number; k?: number; face?: 'tired' | 'happy' | 'lost'}) => {
  const d = dance(o, i * 1.7, k), t = TOWN[i % TOWN.length];
  return <Bean x={x} y={y} s={s} hat={i % 3 === 0 ? 'hood' : i % 3 === 1 ? 'bonnet' : 'none'} hair={i % 3 === 2 ? '#5a3a22' : undefined} pants="#4a3a2a" uniform={false} {...t}
    eyes={face === 'tired' ? 'tired' : face === 'lost' ? 'wide' : 'closed'} mouth={face === 'tired' ? 'frown' : face === 'lost' ? 'o' : 'grin'} sweat={face === 'tired'} o={o} seed={i} {...d} />;
};
const Crowd = ({o, n, y0 = 1500, k = 1, face, s = 0.62}: {o: number; n: number; y0?: number; k?: number; face?: 'tired' | 'happy' | 'lost'; s?: number}) =>
  <g>{Array.from({length: n}, (_, i) => <Townie key={i} i={i} x={80 + ((i * 173) % 920)} y={y0 + Math.floor(i / 6) * 110 + (i % 2) * 30} s={s - Math.floor(i / 6) * 0.04} o={o} k={k} face={face} />).reverse()}</g>;

const shots: Shot[] = [
  ['hook', 0, (o, t) => camWrap(1 + 0.12 * t, 540, 1300, <><Sky o={o} /><MedievalStreet o={o} />
    <Badge x={540} y={520} k={pop(o, at('1518'))} fill="#f4e6c4" c={INK} s={120} w={420} h={170}>1518</Badge>
    <Bean x={540} y={1700} s={1.4} {...TROFFEA} eyes="closed" mouth="grin" o={o} {...dance(o, 0)} />
    {o > at('couldn\'t') && <Stamp x={540} y={1030} k={pop(o, at('couldn\'t'), 240)} text="CAN'T STOP" s={90} />}
    {[180, 900].map((x, i) => <Bean key={x} x={x} y={1820} s={0.85} hat={i ? 'hood' : 'bonnet'} shirt={i ? '#8a3a2a' : '#3a5a8a'} pants="#4a3a2a" uniform={false} eyes="wide" mouth="o" look={i ? -1 : 1} flip={!!i} o={o} seed={i + 3} />)}</>)],
  ['name', at('her'), (o, t) => camWrap(1.1 + 0.06 * t, 540, 1200, <><Burst o={o} c1="#9fd6a5" c2="#b8e2bc" /><Bean x={540} y={1650} s={2.1} {...TROFFEA} eyes="closed" mouth="grin" o={o} {...dance(o, 1)} />
    <NameCard k={pop(o, at('frau'), 200)} name="FRAU TROFFEA" sub="the first dancer" /></>)],
  ['daynight', at('she', 1), (o, t, a, b) => { const night = o > at('then'); return camWrap(1, 540, 1300, <>{night ? <Night o={o} /> : <Sky o={o} />}<MedievalStreet o={o} />
    {night && <rect x={-200} y={-200} width={1480} height={2320} fill="rgba(20,30,80,0.35)" />}
    <Bean x={540} y={1720} s={1.3} {...TROFFEA} eyes={o > at('week') ? 'tired' : 'closed'} mouth={o > at('week') ? 'frown' : 'grin'} sweat={o > at('week')} o={o} {...dance(o, 2)} />
    {o > at('almost') && <Card text="DAY 6" sub="still dancing" k={pop(o, at('almost'), 220)} />}</>); }],
  ['joined', at('and', 1), (o, t, a) => { const n = o > at('400') ? 18 : o > at('100') ? 12 : o > at('30') ? 6 : 2; return camWrap(1.05 - 0.05 * t, 540, 1300, <><Sky o={o} /><MedievalStreet o={o} /><Crowd o={o} n={n} />
    <Badge x={540} y={560} k={pop(o, o > at('400') ? at('400') : o > at('100') ? at('100') : at('30'), 260)} s={110} w={460}>{o > at('400') ? '~400' : o > at('100') ? '100' : '30'}</Badge></>); }],
  ['why', at('nobody'), (o) => camWrap(1.1, 540, 1400, <><Sky o={o} /><MedievalStreet o={o} /><Crowd o={o} n={12} face="lost" />
    {[200, 540, 880].map((x, i) => <Question key={x} x={x} y={1150 - Math.abs(Math.sin(o / 200 + i)) * 30} k={pop(o, at('why') - 300 + i * 100)} />)}</>)],
  ['feet', at('their'), (o, t, a) => camWrap(1.35, 540, 1650, <><Sky o={o} /><Cobbles y={1250} /><Crowd o={o} n={6} y0={1600} face="tired" s={0.8} />
    {o > at('fainted') && <g transform={`rotate(${interpolate(o - at('fainted'), [0, 500], [0, -88], cl)} 300 1880)`}><Bean x={300} y={1880} s={0.8} hat="hood" shirt="#8a3a2a" pants="#4a3a2a" uniform={false} eyes="closed" mouth="o" o={o} /></g>}
    {o > at('fainted') && <T x={420} y={1450} s={80} k={pop(o, at('fainted') + 300)}>THUD</T>}</>)],
  ['grim', at('some', 1), (o, t) => <g style={{filter: 'grayscale(0.7)'}}>{camWrap(1 + 0.05 * t, 540, 1300, <><rect x={-200} y={-200} width={1480} height={2320} fill="#6a7088" /><MedievalStreet o={o} /><rect x={-200} y={-200} width={1480} height={2320} fill="rgba(30,30,50,0.35)" />
    <Crowd o={o} n={6} face="tired" k={0.4} /><Scroll x={540} y={720} k={pop(o, at('reports'))} lines={['SOME REPORTS', 'SAY PEOPLE DIED', '(accounts differ)']} /></>)}</g>],
  ['council', at('so'), (o, t) => camWrap(1, 540, 1250, <><rect x={-200} y={-200} width={1480} height={2320} fill="#e2cfa6" /><rect x={-200} y={1400} width={1480} height={800} fill="#8a6a44" stroke={INK} strokeWidth={8} />
    {[200, 880].map((x) => <g key={x}><rect x={x - 70} y={300} width={140} height={300} rx={70} fill="#8fb8e0" stroke={INK} strokeWidth={7} /><path d={`M${x} 300 L${x} 600 M${x - 70} 450 L${x + 70} 450`} stroke={INK} strokeWidth={6} /></g>)}
    {[0, 1, 2].map((i) => <Bean key={i} x={240 + i * 150} y={1700} s={0.95} hat="top" shirt="#5a2a3a" pants="#2d2a2e" uniform={false} mouth="talk" brows="worried" o={o} seed={i} />)}
    <Bean x={850} y={1720} s={1.15} hat="doctor" shirt="#2d2a2e" pants="#2d2a2e" uniform={false} glasses mustache mouth={o > at('help') ? 'smile' : 'flat'} brows="smug" o={o} seed={6} hold={<rect x={-30} y={-10} width={60} height={80} fill="#f4e6c4" stroke={INK} strokeWidth={4} />} armR={-1.2} /></>)],
  ['hotblood', at('the', 3), (o, t) => { const cure = o > at('cure'); return camWrap(1 + 0.05 * t, 540, 1300, <><Burst o={o} c1={cure ? '#ffd84a' : '#f29a8a'} c2={cure ? '#ffb84a' : '#e87a6a'} />
    <Bean x={540} y={1750} s={2.0} hat="doctor" shirt="#2d2a2e" pants="#2d2a2e" uniform={false} glasses mustache mouth={cure ? 'grin' : 'talk'} brows="smug" o={o} seed={6} {...(cure ? dance(o, 3) : {armR: -2.3})} />
    {!cure && <Think x={760} y={600} k={pop(o, at('hot'))}><path d="M-40 40 Q-60 -20 0 -70 Q10 -20 40 -40 Q70 20 30 60 Z" fill="#ff6a3a" stroke={INK} strokeWidth={7} /><T x={0} y={120} s={50} c="#c9493c">HOT BLOOD</T></Think>}
    {cure && <><Notes o={o} y={1100} /><T x={540} y={640} s={100} c="#ffd84a" k={pop(o, at('more'), 240)}>MORE DANCING!</T></>}</>); }],
  ['stage', at('so', 1), (o, t) => camWrap(1, 540, 1300, <><Sky o={o} /><MedievalStreet o={o} />
    <Stage x={540} y={1560} k={pop(o, at('built'), 150)} />
    {o > at('hired') && <><Bean x={300} y={1470} s={0.75} hat="hood" shirt="#c9a24a" pants="#4a3a2a" uniform={false} eyes="closed" mouth="grin" o={o} seed={2} armR={-1 + Math.sin(o / 90) * 0.4} /><Lute x={330} y={1300} k={0.9} />
      <Bean x={780} y={1470} s={0.75} hat="hood" shirt="#3a5a8a" pants="#4a3a2a" uniform={false} eyes="closed" mouth="grin" o={o} seed={4} armL={-1.4 + Math.abs(Math.sin(o / 100))} armR={-1.4 + Math.abs(Math.cos(o / 100))} /><Drum x={780} y={1440} k={0.9} /><Notes o={o} y={1150} /></>}
    {o > at('professional') && <Crowd o={o} n={6} y0={1700} s={0.7} />}
    {o > at('professional') && <Badge x={540} y={620} k={pop(o, at('professional'))} fill="#2b4f9a" s={64} w={640} h={120}>PAID DANCERS</Badge>}</>)],
  ['worse', at('it', 1), (o, t) => camWrap(1.06 + 0.06 * Math.sin(o / 90), 540, 1300, <><Burst o={o} c1="#c9493c" c2="#e2675a" /><Crowd o={o} n={18} y0={1350} face="tired" />
    {o > at('worse') && <Stamp x={540} y={760} k={pop(o, at('worse'), 260)} text="WORSE" s={150} />}</>)],
  ['banned', at('finally'), (o, t) => camWrap(1, 540, 1300, <><Sky o={o} /><MedievalStreet o={o} /><rect x={330} y={600} width={420} height={560} fill="#f4e6c4" stroke={INK} strokeWidth={9} />
    <text x={540} y={720} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={64} fill={INK}>BY ORDER</text><text x={540} y={800} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={48} fill={INK}>OF THE CITY</text>
    <g transform="translate(540 960)"><circle r={110} fill="none" stroke="#c9493c" strokeWidth={16} /><text y={30} textAnchor="middle" fontSize={110}>♪</text><line x1={-78} y1={-78} x2={78} y2={78} stroke="#c9493c" strokeWidth={16} /></g>
    <Bean x={850} y={1800} s={1.0} hat="hood" shirt="#c9a24a" pants="#4a3a2a" uniform={false} eyes="cry" mouth="frown" o={o} hold={<g transform="scale(0.6)"><Lute x={0} y={0} /></g>} armR={-0.4} /></>)],
  ['mountains', at('sent'), (o, t) => camWrap(1 + 0.06 * t, 540, 1200, <><Sky o={o} /><Mountains y={1300} o={o} /><Chapel x={720} y={760} k={0.7} /><path d="M-100 1700 Q300 1400 500 1200 Q640 1000 700 780" stroke="#c9a46a" strokeWidth={70} fill="none" />
    {Array.from({length: 7}, (_, i) => { const p = Math.min(1, Math.max(0, ease(o, at('sent'), at('where')) * 1.2 - i * 0.07)); const x = interpolate(p, [0, 1], [-60, 640]), y = interpolate(p, [0, 0.6, 1], [1680, 1250, 820]);
      return <Bean key={i} x={x} y={y} s={0.4 - p * 0.15} hat={i % 2 ? 'hood' : 'bonnet'} shirt={TOWN[i % 6].shirt} pants="#4a3a2a" uniform={false} eyes="tired" mouth="flat" walk={o / 150 + i} o={o} seed={i} />; })}</>)],
  ['shrine', at('where'), (o, t) => camWrap(1, 540, 1300, <><rect x={-200} y={-200} width={1480} height={2320} fill="#3a2a3a" /><rect x={-200} y={1400} width={1480} height={800} fill="#5a4030" stroke={INK} strokeWidth={8} />
    <rect x={380} y={420} width={320} height={460} rx={160} fill="#ffe7a0" stroke={INK} strokeWidth={9} /><rect x={520} y={480} width={40} height={300} fill="#d9b24a" /><rect x={460} y={560} width={160} height={40} fill="#d9b24a" />
    {[160, 920].map((x) => <Candle key={x} x={x} y={1400} o={o} />)}
    <g transform={`translate(540 1270) scale(${pop(o, at('red'), 220)})`}><RedShoe x={-110} y={0} /><RedShoe x={110} y={0} flip /></g>
    {[0, 1, 2].map((i) => <Bean key={i} x={250 + i * 290} y={1820} s={0.85} hat={i === 1 ? 'hood' : 'bonnet'} shirt={TOWN[i].shirt} pants="#4a3a2a" uniform={false} eyes="closed" mouth="flat" armL={-0.9} armR={0.9} o={o} seed={i} />)}</>)],
  ['stopped', at('and', 8), (o, t, a) => { const k = 1 - ease(o, a + 200, at('stopped') + 400); return camWrap(1, 540, 1300, <><Sky o={o} sunset /><MedievalStreet o={o} /><rect x={-200} y={-200} width={1480} height={2320} fill="rgba(255,140,80,0.15)" /><Crowd o={o} n={12} k={k} face="tired" /></>); }],
  ['mystery', at('to', 3), (o, t) => camWrap(1, 540, 1100, <><rect x={-200} y={-200} width={1480} height={2320} fill="#2d2a2e" /><Question x={540} y={1050} k={pop(o, at('nobody', 1)) * 3.2} c="#ffd84a" /><T x={540} y={1450} s={84} k={pop(o, at('why', 0) > 0 ? at('happened') : 0)}>WHY?!</T></>)],
  ['theory', at('historians'), (o, t) => camWrap(1, 540, 1300, <><rect x={-200} y={-200} width={1480} height={2320} fill="#e2cfa6" /><rect x={-200} y={1400} width={1480} height={800} fill="#8a6a44" stroke={INK} strokeWidth={8} />
    <Bean x={300} y={1760} s={1.2} hat="none" hair="#9a9a9a" glasses shirt="#5a4a8a" pants="#2d2a2e" uniform={false} mouth="talk" o={o} hold={<g><rect x={-60} y={-20} width={120} height={80} fill="#c9493c" stroke={INK} strokeWidth={5} /></g>} armR={-1.3} />
    <Bulb x={300} y={980} k={pop(o, at('think'))} o={o} />
    <g transform={`translate(760 760) scale(${pop(o, at('stress'))})`}><circle r={110} fill="#fff" stroke={INK} strokeWidth={8} /><path d="M-60 -10 L-20 -40 L0 0 L30 -50 L60 0" stroke="#c9493c" strokeWidth={12} fill="none" strokeLinejoin="round" /><T x={0} y={170} s={56}>STRESS</T></g>
    <g transform={`translate(640 1220) scale(${pop(o, at('famine'))})`}><ellipse cx={0} cy={0} rx={110} ry={40} fill="#c98d45" stroke={INK} strokeWidth={7} /><T x={0} y={110} s={50}>FAMINE</T></g>
    <g transform={`translate(900 1220) scale(${pop(o, at('disease'))})`}><Bean x={0} y={60} s={0.5} hat="none" shirt="#7a8a5a" uniform={false} eyes="tired" mouth="frown" sweat skin="#d8f0b0" o={o} /><T x={0} y={110} s={50}>DISEASE</T></g></>)],
  ['end', at('in', 3), (o, t, a, b) => camWrap(1.25 - 0.3 * ease(o, a, b), 540, 1300, <><Sky o={o} sunset /><MedievalStreet o={o} /><Crowd o={o} n={24} y0={1320} s={0.55} />
    <Bean x={540} y={1780} s={1.2} {...TROFFEA} eyes="closed" mouth="grin" o={o} {...dance(o, 9)} /></>)],
];
const sfx: [string, number, number][] = [['jorho-pop', at('1518'), 0.3], ['record-scratch', at('couldn\'t'), 0.2], ['jorho-pop', at('frau'), 0.25], ['jorho-pop', at('30'), 0.25], ['jorho-pop', at('100'), 0.25],
  ['jorho-pop', at('400'), 0.28], ['huh-cat', at('why'), 0.2], ['meme-bonk', at('fainted') + 300, 0.22], ['jorho-ting', at('hot'), 0.25], ['meme-tada', at('more'), 0.22], ['jorho-pop', at('built'), 0.25],
  ['meme-impact', at('worse'), 0.15], ['jorho-click', at('banned'), 0.4], ['mg-shimmer', at('red'), 0.25], ['jorho-ting', at('think'), 0.25]];
export const Ep2Dance = () => <Episode cfg={{W, vo: 'inside/vo_dance.wav', ep: 2, next: 'Napoleon vs. the Rabbits', shots, sfx, total: EP2_MS,
  key: /^(1518|stop|week|30|100|400|why|bled|died|hot|blood|cure|dancing|musicians|professional|worse|banned|mountains|red|shoes|stopped|stress|famine|disease)$/i}} />;

// WEIRD HISTORY · EP. 4 — The Man Who Sold the Eiffel Tower (Victor Lustig, 1925). Facts: stories/005-eiffel-tower/SCRIPT.md.
import {interpolate} from 'remotion';
import {Burst, Coin, camWrap, cl, ease, pop} from './EmuShort2';
import raw from '../inside/vo_eiffel.words.json';
import {Badge, Bean, Bulb, Doc, Eiffel, Episode, Hotel, INK, MoneyBag, NameCard, Newspaper, ParisSky, Press, Question, ScrapPile, Stamp, T, Think, Train, atOf, words, type Shot} from './series';

const W = words(raw), at = atOf(W);
export const EP4_MS = W[W.length - 1].b + 3000;
type BP = {x: number; y: number; s?: number; o: number; mouth?: 'smile' | 'grin' | 'talk' | 'o' | 'flat' | 'frown' | 'yell'; eyes?: 'dot' | 'wide' | 'squint' | 'closed' | 'tired'; brows?: 'none' | 'smug' | 'worried' | 'angry'; armR?: number; armL?: number; flip?: boolean; walk?: number; hold?: React.ReactNode; sweat?: boolean; blush?: boolean; tilt?: number; jump?: number};
const Lustig = (p: BP) => <Bean hat="fedora" shirt="#3a3640" pants="#2d2a2e" uniform={false} mustache brows="smug" seed={7} {...p} />;
const Poisson = (p: BP) => <Bean hat="bowler" shirt="#7a5a3a" pants="#5a4a3a" uniform={false} seed={8} {...p} />;
const Wife = (p: BP) => <Bean hat="none" hair="#3a2a1a" shirt="#8a3a5a" pants="#8a3a5a" dress="#7a2a4a" uniform={false} seed={9} {...p} />;
const Paris = ({o, sunset, rust = 0, scrap = 0, k = 1}: {o: number; sunset?: boolean; rust?: number; scrap?: number; k?: number}) => <><ParisSky o={o} sunset={sunset} /><Eiffel x={540} y={1260} k={k} rust={rust} scrap={scrap} /></>;
const Room = () => <><rect x={-200} y={-200} width={1480} height={2320} fill="#d9c7a0" />{Array.from({length: 8}, (_, i) => <rect key={i} x={-200 + i * 200} y={-200} width={100} height={1620} fill="#d0bd94" />)}<rect x={-200} y={1420} width={1480} height={800} fill="#7a2a2a" stroke={INK} strokeWidth={8} />
  <g transform="translate(540 520)"><path d="M-160 0 L160 0 L120 120 L-120 120 Z" fill="#ffd84a" stroke={INK} strokeWidth={7} />{[-100, -30, 40, 110].map((x) => <circle key={x} cx={x} cy={150} r={16} fill="#fff6a8" stroke={INK} strokeWidth={5} />)}<line x1={0} y1={-200} x2={0} y2={0} stroke={INK} strokeWidth={8} /></g></>;

const shots: Shot[] = [
  ['hook', 0, (o, t) => camWrap(1 + 0.1 * t, 540, 1200, <><Paris o={o} /><Badge x={540} y={520} k={pop(o, at('1925'))} fill="#f4e6c4" c={INK} s={120} w={420} h={170}>1925</Badge>
    {o > at('sold') && <g transform={`translate(760 1000) scale(${pop(o, at('sold'), 220)}) rotate(-8)`}><rect x={-160} y={-70} width={320} height={130} rx={14} fill="#c9493c" stroke={INK} strokeWidth={8} /><text y={30} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={96} fill="#fff">SOLD</text><line x1={-120} y1={-70} x2={-60} y2={-200} stroke={INK} strokeWidth={6} /><line x1={120} y1={-70} x2={60} y2={-200} stroke={INK} strokeWidth={6} /></g>}
    <Lustig x={240} y={1780} s={1.2} o={o} mouth="grin" armR={-2.6} /></>)],
  ['name', at('his'), (o, t) => camWrap(1.05, 540, 1300, <><Burst o={o} c1="#3a3640" c2="#46424c" /><Lustig x={540} y={1650} s={2.0} o={o} mouth="smile" armR={-2.0 + Math.sin(o / 300) * 0.3} /><NameCard k={pop(o, at('victor'))} name="VICTOR LUSTIG" sub="con man" /></>)],
  ['news', at('one'), (o, t) => camWrap(1, 540, 1200, <><Room /><Lustig x={300} y={1780} s={1.25} o={o} mouth="flat" eyes="squint" armL={-1.4} armR={-1.4} />
    <Newspaper x={680} y={1100} k={pop(o, at('newspaper'))} rot={-4} head={o > at('rusting') ? 'EIFFEL TOWER|RUSTING!|COSTS A FORTUNE' : 'PARIS NEWS|...'} /></>)],
  ['rust', at('the', 1), (o, t) => camWrap(1.1 - 0.1 * t, 540, 1150, <><Paris o={o} rust={ease(o, at('rusting'), at('rusting') + 600)} />
    {o > at('painting') && <g transform={`translate(${380 + Math.sin(o / 300) * 20} 900)`}><rect x={-60} y={-10} width={240} height={20} fill="#7a5532" stroke={INK} strokeWidth={5} /><Bean x={60} y={0} s={0.45} hat="beret" shirt="#f4f0e6" pants="#3a5a8a" uniform={false} mouth="frown" sweat o={o} armR={-2.2 + Math.sin(o / 80) * 0.4} /></g>}
    {Array.from({length: 4}, (_, i) => o > at('fortune') + i * 150 && <MoneyBag key={i} x={700 + i * 60 + (o - at('fortune')) / 8} y={1100 - (o - at('fortune') - i * 150) / 4} k={0.5} />)}
    {o > at('keep') - 300 && <Question x={820} y={720} k={pop(o, at('keep') - 300)} />}</>)],
  ['idea', at('lustig', 1), (o, t) => camWrap(1.1, 540, 1300, <><Burst o={o} c1="#ffd84a" c2="#ffe48a" /><Lustig x={540} y={1760} s={1.8} o={o} mouth="grin" eyes="squint" armR={-2.6} /><Bulb x={540} y={760} k={pop(o, at('idea'), 240)} o={o} /></>)],
  ['press', at('he', 1), (o, t, a) => camWrap(1, 540, 1300, <><Room /><Press x={540} y={1440} k={1.1} o={o} />
    {Array.from({length: 4}, (_, i) => { const p = Math.max(0, (o - a - 300 - i * 380) / 900); return p > 0 ? <Doc key={i} x={540 + p * (200 + i * 60) * (i % 2 ? -1 : 1)} y={1360 - Math.min(1, p) * 300 + p * p * 80} k={0.7} rot={(i % 2 ? -1 : 1) * p * 30} label="OFFICIAL" /> : null; })}
    <Lustig x={180} y={1800} s={1.05} o={o} mouth="grin" armR={-1.4} /></>)],
  ['hotel', at('invited'), (o, t) => camWrap(1, 540, 1300, <><ParisSky o={o} /><Hotel x={540} y={1250} k={0.95} />
    {Array.from({length: 6}, (_, i) => o > at('six') + i * 120 ? <g key={i} transform={`translate(${130 + i * 165} 1800) scale(${pop(o, at('six') + i * 120)}) translate(${-(130 + i * 165)} -1800)`}><Bean x={130 + i * 165} y={1800} s={0.62} hat={i % 2 ? 'bowler' : 'top'} shirt={['#7a5a3a', '#3a5a3a', '#5a3a5a'][i % 3]} pants="#2d2a2e" uniform={false} mouth="smile" o={o} seed={i} /></g> : null)}
    {o > at('six') && <Badge x={540} y={560} k={pop(o, at('six'))} s={70} w={640} h={130} fill="#2b4f9a">6 SCRAP DEALERS</Badge>}</>)],
  ['secret', at('he', 2), (o, t) => { const scrapNow = o > at('scrap', 1); return camWrap(1.05, 540, 1300, <><Room />
    <Lustig x={360} y={1780} s={1.4} o={o} mouth="talk" armR={-2.0} />{[0, 1, 2].map((i) => <Bean key={i} x={720 + i * 140} y={1840} s={0.7} hat="bowler" shirt="#7a5a3a" pants="#2d2a2e" uniform={false} eyes="wide" mouth="o" flip o={o} seed={i} />)}
    <T x={540} y={700} s={100} c="#ffd84a" k={pop(o, at('secret'))}>SHHH...</T>
    {o > at('city') && <Think x={540} y={1060} k={pop(o, at('city'))} r={170}>{scrapNow ? <ScrapPile x={0} y={60} k={0.6} /> : <Eiffel x={0} y={130} k={0.2} />}</Think>}</>); }],
  ['tons', at('over'), (o, t) => camWrap(1, 540, 1300, <><ParisSky o={o} /><ScrapPile x={540} y={1270} k={1.4} /><Badge x={540} y={620} k={pop(o, at('7,000'))} s={90} w={680}>7,000+ TONS</Badge>
    {o > at('highest') && [0, 1, 2].map((i) => <g key={i}><Bean x={240 + i * 300} y={1820} s={0.85} hat="bowler" shirt="#7a5a3a" pants="#2d2a2e" uniform={false} mouth="grin" o={o} seed={i} armR={-2.6 - Math.abs(Math.sin(o / 120 + i)) * 0.2} jump={Math.abs(Math.sin(o / 120 + i)) * 20} /><T x={300 + i * 300} y={1300} s={60} c="#2b8a3a">${(i + 2) * 1000}?</T></g>)}</>)],
  ['poisson', at('one', 1), (o, t) => camWrap(1.05, 540, 1300, <><Burst o={o} c1="#b8d8a8" c2="#cce6c0" /><Poisson x={540} y={1650} s={2.0} o={o} mouth="grin" eyes="closed" armL={-2.4} armR={2.4} jump={Math.abs(Math.sin(o / 150)) * 25} />
    <NameCard k={pop(o, at('poisson'))} name="ANDRÉ POISSON" sub="scrap dealer" /></>)],
  ['wife', at('but'), (o, t) => camWrap(1.1, 540, 1300, <><Room /><Poisson x={320} y={1780} s={1.2} o={o} mouth="grin" /><Wife x={760} y={1780} s={1.2} o={o} flip mouth="flat" eyes="squint" brows="angry" armR={-1.0} />
    <Think x={760} y={760} k={pop(o, at('something'))} r={110}><Question x={0} y={50} k={0.8} c="#c9493c" /></Think></>)],
  ['genius', at('so'), (o, t) => camWrap(1.1, 540, 1300, <><Burst o={o} c1="#3a3640" c2="#46424c" /><Lustig x={540} y={1760} s={1.9} o={o} mouth="grin" eyes="squint" armR={-1.8 + Math.sin(o / 200) * 0.3} /><T x={540} y={700} s={110} c="#ffd84a" k={pop(o, at('genius'), 240)}>GENIUS</T></>)],
  ['bribe', at('he', 3), (o, t) => camWrap(1.1, 540, 1300, <><Room /><Lustig x={360} y={1780} s={1.3} o={o} mouth="smile" armR={-1.5} /><Poisson x={760} y={1780} s={1.2} o={o} flip mouth="o" eyes="wide" sweat />
    {o > at('bribe') && <Badge x={540} y={700} k={pop(o, at('bribe'))} s={80} w={540} fill="#c9a24a" c={INK}>A BRIBE?!</Badge>}</>)],
  ['sure', at('now'), (o, t) => camWrap(1.05, 540, 1300, <><Burst o={o} c1="#b8d8a8" c2="#cce6c0" /><Poisson x={540} y={1760} s={1.8} o={o} mouth="grin" eyes="closed" armR={-2.6} />
    {o > at('only') && <Badge x={540} y={700} k={pop(o, at('official'))} s={56} w={760} h={130} fill="#2b8a3a">REAL OFFICIAL ✓</Badge>}</>)],
  ['paid', at('he', 4), (o, t) => camWrap(1, 540, 1300, <><Room /><Poisson x={260} y={1780} s={1.1} o={o} mouth="smile" armR={-1.4} /><Lustig x={820} y={1780} s={1.1} o={o} flip mouth="grin" />
    {[at('paid'), at('paid', 1)].map((t0, i) => { const p = Math.min(1, Math.max(0, (o - t0) / 700)); return p > 0 ? <MoneyBag key={i} x={300 + p * 450} y={1500 - Math.sin(p * Math.PI) * 300 - i * 120} k={0.9} label={i ? 'BRIBE' : '$'} /> : null; })}</>)],
  ['fled', at('lustig', 3), (o, t, a) => camWrap(1, 540, 1300, <><ParisSky o={o} sunset /><Train x={interpolate(o - a, [300, 2000], [560, 1500], cl)} y={1640} k={0.9} o={o} />
    <Badge x={540} y={620} k={pop(o, at('vienna'))} s={80} w={560} fill="#f4e6c4" c={INK}>→ VIENNA</Badge>
    {o - a < 600 && <Lustig x={300} y={1780} s={1.0} o={o} walk={o / 100} mouth="grin" />}</>)],
  ['shame', at('and', 4), (o, t) => camWrap(1.1, 540, 1300, <><Burst o={o} c1="#f2a6a6" c2="#f7c0c0" /><Poisson x={540} y={1760} s={1.9} o={o} mouth="frown" eyes="closed" blush armL={-2.6} armR={2.6} />
    {o > at('police') && <g transform={`translate(780 820) scale(${pop(o, at('police'))})`}><rect x={-120} y={-80} width={240} height={150} rx={16} fill="#2b4f9a" stroke={INK} strokeWidth={7} /><text y={20} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={44} fill="#fff">POLICE</text><line x1={-150} y1={-110} x2={150} y2={110} stroke="#c9493c" strokeWidth={18} /></g>}</>)],
  ['back', at('so', 1), (o, t, a) => camWrap(1, 540, 1250, <><Paris o={o} /><Train x={interpolate(o - a, [0, 1300], [1500, 640], cl)} y={1640} k={0.9} o={o} />
    {o > at('came') + 300 && <Lustig x={240} y={1780} s={1.1} o={o} mouth="grin" armR={-2.6} />}
    {o > at('again') - 200 && <Badge x={540} y={620} k={pop(o, at('again') - 200)} s={72} w={620} h={130}>ROUND 2</Badge>}</>)],
  ['police', at('this'), (o, t, a) => camWrap(1, 540, 1300, <><Paris o={o} />
    {Array.from({length: 2}, (_, i) => <Bean key={i} x={interpolate(o - a, [800, 2600], [-200 - i * 160, 500 - i * 160], cl)} y={1800} s={0.95} hat="cap" shirt="#2b4f9a" pants="#1f2a4a" uniform={false} mouth="yell" brows="angry" walk={o / 80 + i} o={o} seed={i} armR={-2.4} />)}
    {o < at('lustig', 5) ? <Poisson x={760} y={1800} s={1.0} o={o} flip mouth="talk" brows="angry" armR={-2.4} />
      : <><Lustig x={interpolate(o - at('lustig', 5), [0, 900], [700, 1300], cl)} y={1800} s={1.0} o={o} walk={o / 70} mouth="grin" /><T x={540} y={700} s={110} c="#ffd84a" k={pop(o, at('escaped'))}>ESCAPED!</T></>}</>)],
];
const sfx: [string, number, number][] = [['jorho-pop', at('1925'), 0.3], ['cha-ching', at('sold'), 0.22], ['jorho-pop', at('victor'), 0.25], ['paper-tear', at('newspaper'), 0.25], ['jorho-ting', at('idea'), 0.3],
  ['camera-shutter', at('printed'), 0.25], ['jorho-pop', at('six'), 0.25], ['huh-cat', at('secret'), 0.2], ['jorho-pop', at('7,000'), 0.25], ['jorho-pop', at('poisson'), 0.25], ['huh-cat', at('off'), 0.22],
  ['meme-tada', at('genius'), 0.2], ['record-scratch', at('bribe'), 0.2], ['cha-ching', at('paid'), 0.22], ['cha-ching', at('paid', 1), 0.22], ['fast-whoosh', at('fled'), 0.22], ['fast-whoosh', at('escaped'), 0.22]];
export const Ep4Eiffel = () => <Episode cfg={{W, vo: 'inside/vo_eiffel.wav', ep: 4, next: 'coming soon', shots, sfx, total: EP4_MS,
  key: /^(1925|eiffel|tower|sold|lustig|rusting|fortune|idea|fake|six|secret|scrap|7,000|wins|wife|off|genius|bribe|sure|paid|vienna|embarrassed|again|police|escaped)$/i}} />;

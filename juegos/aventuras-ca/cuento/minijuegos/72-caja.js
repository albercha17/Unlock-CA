// Carta 72 — La caja de música: los siete animales de la melodía están en la partitura (carta 75, no en la app);
// el xilófono (carta 79) dice qué nota toca cada animal (conejo Do, ciervo Re, búho Mi, rana Fa, ardilla Sol, zorro La).
// Melodía: rana, conejo, ardilla, búho, ciervo, zorro, rana = Fa, Do, Sol, Mi, Re, La, Fa. Las notas suenan y también se iluminan (alternativa visual).
// Letra del libro: R.
import { openGame } from './ui.js';
import { estilo, guardarLetra } from './libro.js';

const TABLA = { conejo: 'Do', ciervo: 'Re', 'búho': 'Mi', rana: 'Fa', ardilla: 'Sol', zorro: 'La' };
const PARTITURA = ['rana', 'conejo', 'ardilla', 'búho', 'ciervo', 'zorro', 'rana'];
const NOTAS = [
  { n: 'Do', f: 261.63, c: '#ff8a8a' }, { n: 'Re', f: 293.66, c: '#ffb86b' }, { n: 'Mi', f: 329.63, c: '#ffe27a' },
  { n: 'Fa', f: 349.23, c: '#8fe28f' }, { n: 'Sol', f: 392.0, c: '#6fd6e8' }, { n: 'La', f: 440.0, c: '#8fa8ff' }, { n: 'Si', f: 493.88, c: '#d6a0ff' }
];

let ctx = null;
function sonar(freq) {
  try {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    ctx = ctx || new AC();
    if (ctx.state === 'suspended') ctx.resume();
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.type = 'triangle';
    o.frequency.value = freq;
    const t0 = ctx.currentTime;
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(0.25, t0 + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.6);
    o.connect(g); g.connect(ctx.destination);
    o.start(t0);
    o.stop(t0 + 0.65);
  } catch (e) { /* sin audio: la nota se ilumina igualmente */ }
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 72 — La caja de música',
    instr: 'Tocad la melodía de la partitura (carta 75) con las teclas. Qué nota toca cada animal os lo dice el xilófono del bosque (carta 79). Las notas suenan y se iluminan.',
    ...opts
  });
  estilo('cu-caja-estilo', `
    .caj-puntos{display:flex;justify-content:center;gap:8px;margin:6px 0 12px}
    .caj-punto{width:16px;height:16px;border-radius:50%;border:2px solid rgba(255,224,138,.6);background:rgba(255,255,255,.08);transition:all .2s}
    .caj-punto.hecho{background:#9dffb0;border-color:#9dffb0;box-shadow:0 0 10px rgba(120,255,160,.6)}
    .caj-punto.ahora{border-color:#ffe08a;box-shadow:0 0 12px rgba(255,224,138,.9)}
    .caj-teclas{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin-bottom:8px}
    .caj-nota{min-height:84px;border-radius:8px 8px 14px 14px;border:2px solid rgba(255,255,255,.6);background:linear-gradient(180deg,#fff,var(--c));color:#2a1450;font:800 .85rem inherit;font-family:inherit;cursor:pointer;padding:0;display:flex;align-items:flex-end;justify-content:center;padding-bottom:8px;min-width:0}
    .caj-nota.suena{filter:brightness(1.15);box-shadow:0 0 22px var(--c),inset 0 0 18px #fff;transform:translateY(3px)}
    .caj-cont{font-size:.85rem;color:#d8e2ee}
  `);

  const puntos = document.createElement('div');
  puntos.className = 'caj-puntos';
  puntos.setAttribute('aria-hidden', 'true');
  const teclas = document.createElement('div');
  teclas.className = 'caj-teclas';
  teclas.setAttribute('role', 'group');
  teclas.setAttribute('aria-label', 'Teclas de la caja de música');
  const cont = document.createElement('div');
  cont.className = 'caj-cont';
  ui.body.append(puntos, teclas, cont);

  const tiles = [];
  PARTITURA.forEach(() => {
    const p = document.createElement('i');
    p.className = 'caj-punto';
    puntos.appendChild(p);
    tiles.push(p);
  });

  let paso = 0;
  let resuelto = false;

  NOTAS.forEach((nt) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'caj-nota';
    b.dataset.n = nt.n;
    b.style.setProperty('--c', nt.c);
    b.textContent = nt.n;
    b.setAttribute('aria-label', 'Nota ' + nt.n);
    b.addEventListener('click', () => tocar(nt));
    teclas.appendChild(b);
  });

  function pintar() {
    tiles.forEach((t, i) => { t.classList.toggle('hecho', i < paso); t.classList.toggle('ahora', i === paso && !resuelto); });
    cont.textContent = resuelto ? 'La melodía está completa.' : 'Notas tocadas: ' + paso + ' de ' + PARTITURA.length;
  }

  function tocar(nt) {
    if (resuelto) return;
    sonar(nt.f);
    const tecla = teclas.querySelector('[data-n="' + nt.n + '"]');
    tecla.classList.add('suena');
    setTimeout(() => tecla.classList.remove('suena'), 320);
    const animal = PARTITURA[paso];
    if (TABLA[animal] === nt.n) {
      paso++;
      ui.say('');
      pintar();
      if (paso === PARTITURA.length) {
        resuelto = true;
        pintar();
        guardarLetra('72', 'R');
        ui.say('¡La melodía suena entera y la caja de música se abre como una flor! Coged la carta 82. Letra del libro: R.', 'ok');
      }
    } else {
      paso = 0;
      pintar();
      ui.say('Esa no es la nota del animal número ' + (paso + 1) + ' según el xilófono de la carta 79. La melodía vuelve a empezar desde el primer animal.', 'bad');
    }
  }

  ui.button('Empezar la melodía de nuevo', 'ghost', () => { if (!resuelto) { paso = 0; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}

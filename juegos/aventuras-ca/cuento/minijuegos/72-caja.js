// Carta 72 — La caja de música: la partitura es una fila de siete animales; la carta 76 dice qué nota toca cada animal
// (conejo Do, ciervo Re, búho Mi, rana Fa, ardilla Sol, zorro La). Hay que tocar las notas en el orden de la partitura:
// rana, conejo, ardilla, búho, ciervo, zorro, rana = Fa, Do, Sol, Mi, Re, La, Fa. Las notas suenan y también se iluminan (alternativa visual).
// Esta app no da letra del libro.
import { openGame } from './ui.js';
import { estilo, conImagen } from './libro.js';

const TABLA = { conejo: 'Do', ciervo: 'Re', 'búho': 'Mi', rana: 'Fa', ardilla: 'Sol', zorro: 'La' };
const PARTITURA = ['rana', 'conejo', 'ardilla', 'búho', 'ciervo', 'zorro', 'rana'];
const NOTAS = [
  { n: 'Do', f: 261.63, c: '#ff8a8a' }, { n: 'Re', f: 293.66, c: '#ffb86b' }, { n: 'Mi', f: 329.63, c: '#ffe27a' },
  { n: 'Fa', f: 349.23, c: '#8fe28f' }, { n: 'Sol', f: 392.0, c: '#6fd6e8' }, { n: 'La', f: 440.0, c: '#8fa8ff' }, { n: 'Si', f: 493.88, c: '#d6a0ff' }
];
const COLOR_ANIMAL = { conejo: '#e8d9f5', ciervo: '#c98f55', 'búho': '#8a7a6a', rana: '#7ccf6a', ardilla: '#d9743a', zorro: '#f08a3a' };

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
    instr: 'La partitura es una fila de animales. Toca las notas en el mismo orden; la carta 76 dice qué nota toca cada animal. Las notas suenan y se iluminan.',
    ...opts
  });
  estilo('cu-caja-estilo', `
    .caj-partitura{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin:4px 0 10px}
    .caj-animal{position:relative;aspect-ratio:1/1.3;border-radius:10px;border:2px solid rgba(255,224,138,.35);background:rgba(255,255,255,.07);display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:6px 2px 4px;font:700 .62rem/1.1 inherit;font-family:inherit;color:#fff;text-align:center;min-width:0}
    .caj-animal .cuerpo{width:70%;aspect-ratio:1;border-radius:50% 50% 44% 44%;background:var(--c);border:2px solid rgba(0,0,0,.3);position:relative}
    .caj-animal .cuerpo::before,.caj-animal .cuerpo::after{content:"";position:absolute;top:32%;width:12%;aspect-ratio:1;border-radius:50%;background:#1a0e30}
    .caj-animal .cuerpo::before{left:26%}.caj-animal .cuerpo::after{right:26%}
    .caj-animal.hecho{border-color:#9dffb0;background:rgba(120,255,160,.16)}
    .caj-animal.ahora{border-color:#ffe08a;box-shadow:0 0 14px rgba(255,224,138,.8)}
    .caj-teclas{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin-bottom:8px}
    .caj-nota{min-height:84px;border-radius:8px 8px 14px 14px;border:2px solid rgba(255,255,255,.6);background:linear-gradient(180deg,#fff,var(--c));color:#2a1450;font:800 .85rem inherit;font-family:inherit;cursor:pointer;padding:0;display:flex;align-items:flex-end;justify-content:center;padding-bottom:8px;min-width:0}
    .caj-nota.suena{filter:brightness(1.15);box-shadow:0 0 22px var(--c),inset 0 0 18px #fff;transform:translateY(3px)}
    .caj-cont{font-size:.85rem;color:#d8e2ee}
    .caj-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.5;pointer-events:none}
  `);

  const partitura = document.createElement('div');
  partitura.className = 'caj-partitura';
  partitura.setAttribute('role', 'list');
  const teclas = document.createElement('div');
  teclas.className = 'caj-teclas';
  teclas.setAttribute('role', 'group');
  teclas.setAttribute('aria-label', 'Teclas de la caja de música');
  const cont = document.createElement('div');
  cont.className = 'caj-cont';
  ui.body.append(partitura, teclas, cont);

  const tiles = [];
  PARTITURA.forEach((a, i) => {
    const t = document.createElement('div');
    t.className = 'caj-animal';
    t.setAttribute('role', 'listitem');
    t.dataset.i = String(i);
    t.dataset.a = a;
    t.innerHTML = '<span class="cuerpo" style="--c:' + COLOR_ANIMAL[a] + '"></span><span>' + a.charAt(0).toUpperCase() + a.slice(1) + '</span>';
    partitura.appendChild(t);
    tiles.push(t);
    conImagen(t, 'animales/' + a.normalize('NFD').replace(/[̀-ͯ]/g, '') + '.jpg', { clase: 'caj-img', mezcla: 'screen' });
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
        ui.say('¡La melodía suena entera y la caja de música se abre como una flor! Dentro brilla el Tintero Dorado. Coged la carta 82.', 'ok');
      }
    } else {
      paso = 0;
      pintar();
      ui.say('Esa no es la nota del ' + animal + ' según la tabla de la carta 76. La melodía vuelve a empezar desde el primer animal.', 'bad');
    }
  }

  ui.button('Empezar la melodía de nuevo', 'ghost', () => { if (!resuelto) { paso = 0; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}

// Carta 14 — Cartel de la panadería: una cuenta hecha con palitos de canela que está mal. Hay que mover UN palito para arreglarla.
// La lista de precios (carta 16) dice cuál debe ser la cuenta. Instancia: 9 + 4 = 5  ->  5 + 4 = 9 (una única solución de un movimiento).
// Letra del libro: C.
import { openGame } from './ui.js';
import { guardarLetra, estilo, conImagen } from './libro.js';

const LETRA = 'C';
// segmentos de un dígito: arriba, arriba-dcha, abajo-dcha, abajo, abajo-izda, arriba-izda, centro
const G7 = [['h', 10, 0], ['v', 52, 8], ['v', 52, 56], ['h', 10, 96], ['v', 0, 56], ['v', 0, 8], ['h', 10, 48]];
const GOP = [['h', 5, 48], ['v', 21, 28]]; // bit 0: horizontal (resta); bit 1: vertical (suma)
const MASK = { 0: 'abcdef', 1: 'bc', 2: 'abdeg', 3: 'abcdg', 4: 'bcfg', 5: 'acdfg', 6: 'acdefg', 7: 'abc', 8: 'abcdefg', 9: 'abcdfg' };
const DIG = {};
Object.keys(MASK).forEach((d) => { DIG[[...MASK[d]].reduce((m, ch) => m | (1 << 'abcdefg'.indexOf(ch)), 0)] = +d; });
const INICIAL = [111, 3, 102, 109]; // 9, +, 4, 5
const NOMBRES = ['primer número', 'signo', 'segundo número', 'resultado'];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 14 — Cartel de la panadería',
    instr: 'La cuenta del cartel está mal. Mueve UN solo palito de canela (tócalo y luego toca un hueco vacío) para que la cuenta sea la de la lista de precios.',
    ...opts
  });
  estilo('cu-cartel-estilo', `
    .cer-cartel{position:relative;margin:4px auto 10px;padding:16px 8px 12px;border-radius:12px;border:4px solid #6b3f1d;background:linear-gradient(180deg,#e9c58a,#c99650);box-shadow:inset 0 0 22px rgba(90,50,10,.45),0 6px 0 #3f2410}
    .cer-cartel::before,.cer-cartel::after{content:"";position:absolute;top:-16px;width:6px;height:18px;background:#4a2a12;border-radius:3px}
    .cer-cartel::before{left:22%}.cer-cartel::after{right:22%}
    .cer-cuenta{display:flex;justify-content:center;align-items:center;gap:6px;flex-wrap:nowrap;transform-origin:center}
    .cer-sim{position:relative;width:60px;height:104px;flex:none}
    .cer-sim.op{width:50px}.cer-sim.igual{width:50px}
    .cer-slot{position:absolute;border:0;padding:0;border-radius:5px;background:rgba(90,50,10,.14);cursor:pointer;min-width:0;min-height:0}
    .cer-slot.h{width:40px;height:9px}.cer-slot.v{width:9px;height:40px}
    .cer-slot::after{content:"";position:absolute;inset:-10px}
    .cer-slot.on{background:linear-gradient(90deg,#8a4b1f,#c4783a 45%,#8a4b1f);box-shadow:0 0 0 1px #4a2410,0 2px 3px rgba(0,0,0,.45)}
    .cer-slot.on::before{content:"";position:absolute;inset:2px 6px;border-radius:3px;background:repeating-linear-gradient(90deg,rgba(255,225,170,.35) 0 3px,transparent 3px 9px);display:block}
    .cer-slot.v.on::before{inset:6px 2px;background:repeating-linear-gradient(0deg,rgba(255,225,170,.35) 0 3px,transparent 3px 9px)}
    .cer-slot.sel{outline:3px solid #fff2a8;box-shadow:0 0 14px #fff2a8}
    .cer-slot:focus-visible{outline:3px solid #fff}
    .cer-fijo{position:absolute;width:40px;height:9px;border-radius:5px;background:linear-gradient(90deg,#8a4b1f,#c4783a 45%,#8a4b1f);box-shadow:0 0 0 1px #4a2410;left:5px}
    .cer-pista{margin:6px 0 0;font-size:.82rem;color:#4a2a10}
    .cer-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55;pointer-events:none;border-radius:8px}
  `);

  const cartel = document.createElement('div');
  cartel.className = 'cer-cartel';
  conImagen(cartel, 'cartel.jpg', { clase: 'cer-img', mezcla: 'multiply' });
  const cuenta = document.createElement('div');
  cuenta.className = 'cer-cuenta';
  cuenta.setAttribute('role', 'group');
  cuenta.setAttribute('aria-label', 'Cuenta del cartel hecha con palitos de canela');
  const nota = document.createElement('p');
  nota.className = 'cer-pista';
  nota.textContent = 'Solo se puede mover un palito. No se rompen ni se parten.';
  cartel.append(cuenta, nota);
  ui.body.appendChild(cartel);

  let estado, sel, movido, resuelto = false;

  function simbolo(k) {
    const d = document.createElement('div');
    d.className = 'cer-sim' + (k === 1 ? ' op' : '');
    (k === 1 ? GOP : G7).forEach((g, s) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'cer-slot ' + g[0];
      b.style.left = g[1] + 'px';
      b.style.top = g[2] + 'px';
      b.dataset.k = String(k);
      b.dataset.s = String(s);
      b.addEventListener('click', () => tocar(k, s));
      d.appendChild(b);
    });
    return d;
  }
  function igual() {
    const d = document.createElement('div');
    d.className = 'cer-sim igual';
    [36, 62].forEach((t) => { const f = document.createElement('div'); f.className = 'cer-fijo'; f.style.top = t + 'px'; d.appendChild(f); });
    return d;
  }
  [0, 1, 2].forEach((k) => cuenta.appendChild(simbolo(k)));
  cuenta.appendChild(igual());
  cuenta.appendChild(simbolo(3));
  // la cuenta cabe siempre en pantalla estrecha
  const ajustar = () => { const w = cartel.clientWidth - 16; const esc = Math.min(1, w / 290); cuenta.style.transform = 'scale(' + esc + ')'; cuenta.style.height = (104 * esc) + 'px'; };
  setTimeout(ajustar, 0);
  window.addEventListener('resize', ajustar);
  ui.onClose(() => window.removeEventListener('resize', ajustar));

  function valida() {
    const a = DIG[estado[0]], b = DIG[estado[2]], c = DIG[estado[3]], op = estado[1];
    if (a === undefined || b === undefined || c === undefined || (op !== 1 && op !== 3)) return null;
    return (op === 3 ? a + b : a - b) === c;
  }
  function pintar() {
    cuenta.querySelectorAll('.cer-slot').forEach((b) => {
      const k = +b.dataset.k, s = +b.dataset.s;
      const on = !!((estado[k] >> s) & 1);
      b.classList.toggle('on', on);
      b.classList.toggle('sel', !!sel && sel[0] === k && sel[1] === s);
      b.setAttribute('aria-label', NOMBRES[k] + ', palito ' + (s + 1) + (on ? ' con canela' : ' vacío'));
    });
  }
  function tocar(k, s) {
    if (resuelto) return;
    if (movido) { ui.say('Solo se puede mover un palito. Pulsa «Empezar de nuevo» para volver a probar.', 'bad'); return; }
    const on = !!((estado[k] >> s) & 1);
    if (!sel) {
      if (!on) { ui.say('Primero toca un palito de canela para cogerlo.', ''); return; }
      sel = [k, s]; ui.say(''); pintar(); return;
    }
    if (on) { sel = (sel[0] === k && sel[1] === s) ? null : [k, s]; pintar(); return; }
    estado[sel[0]] &= ~(1 << sel[1]);
    estado[k] |= 1 << s;
    sel = null; movido = true; pintar();
    const v = valida();
    if (v) {
      resuelto = true;
      guardarLetra('14', LETRA);
      ui.say('¡El cartel ya cuenta bien! Doña Hogaza aplaude y os cuenta lo que sabe. Coged la carta 26. Letra del libro: ' + LETRA + '.', 'ok');
    } else if (v === null) {
      ui.say('Ese número o signo no existe: los palitos no forman una cifra. Empezad de nuevo.', 'bad');
    } else {
      ui.say('La cuenta sigue sin cuadrar con la lista de precios. Empezad de nuevo y probad otro palito.', 'bad');
    }
  }
  function inicio() { estado = INICIAL.slice(); sel = null; movido = false; resuelto = false; ui.say(''); pintar(); }
  ui.button('Empezar de nuevo', 'primary', inicio);
  inicio();
  return { close: ui.close };
}

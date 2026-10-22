// Carta 72 — Las torres de hielo (torres de Hanói): llevar los cuatro discos de la torre I a la III, de uno en uno y nunca sobre uno más pequeño, antes de que
// el reloj de arena dé 15 vueltas (una por movimiento). La torre y las reglas, en las cartas 75 y 79 (instancias_trono.py, TORRES).
import { openGame } from './ui.js';
import { estilo } from './reino.js';

const D = /*DATOS*/{"discos": 4, "limite": 15}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 72 — Las torres de hielo', instr: 'Tocad una torre para coger el disco de arriba y luego otra torre para dejarlo. Llevad todos de la torre I a la III. Reglas y reloj de arena, en las cartas 75 y 79.', ...opts });
  estilo('tr-tor', `.tor-pl{display:flex;gap:10px;justify-content:center;margin:12px 0}.tor-t{width:100px;height:190px;border:3px solid #6d8aa6;border-radius:8px;background:rgba(0,0,0,.25);display:flex;flex-direction:column-reverse;align-items:center;gap:3px;padding:6px 0;cursor:pointer;position:relative}.tor-t.sel{border-color:#ffd36a}.tor-t::before{content:'';position:absolute;bottom:0;top:14px;width:8px;background:#6d8aa6;z-index:0}.tor-d{height:24px;border-radius:6px;border:2px solid #0c121a;z-index:1}.tor-cu{text-align:center;color:#e6f1fb;font:700 .85rem system-ui}`);
  const t = [[], [], []];
  for (let k = D.discos; k >= 1; k--) t[0].push(k);
  let sel = null, movs = 0, resuelto = false;
  const pl = document.createElement('div'); pl.className = 'tor-pl';
  const cu = document.createElement('div'); cu.className = 'tor-cu';
  ui.body.append(pl, cu);
  const cols = ['#c9a050', '#a0b070', '#70a8b0', '#7098c8'];
  function pintar() {
    pl.innerHTML = '';
    t.forEach((p, i) => {
      const e = document.createElement('button'); e.type = 'button'; e.className = 'tor-t' + (sel === i ? ' sel' : ''); e.dataset.t = String(i); e.setAttribute('aria-label', 'Torre ' + (i + 1));
      p.forEach(k => { const d = document.createElement('div'); d.className = 'tor-d'; d.style.width = (30 + k * 16) + 'px'; d.style.background = cols[(k - 1) % 4]; d.dataset.k = String(k); e.appendChild(d); });
      e.addEventListener('click', () => toca(i)); pl.appendChild(e);
    });
    cu.textContent = 'Vueltas del reloj de arena: ' + movs + ' de ' + D.limite;
    pl.dataset.torres = t.map(p => p.join('')).join('/');
  }
  function toca(i) {
    if (resuelto) return;
    if (sel === null) { if (t[i].length) { sel = i; pintar(); } return; }
    const o = sel; sel = null;
    if (o === i) { pintar(); return; }
    const d = t[o][t[o].length - 1];
    if (t[i].length && t[i][t[i].length - 1] < d) { ui.say('Un disco nunca va sobre otro más pequeño (carta 79).', 'bad'); pintar(); return; }
    t[i].push(t[o].pop()); movs++; ui.say('');
    pintar();
    if (t[2].length === D.discos) {
      resuelto = true;
      ui.say('La corona queda entera en la torre III antes de que se vacíe el reloj de arena: se abre el altar. Coged la carta 82.', 'ok');
    } else if (movs >= D.limite) {
      ui.say('El reloj de arena se ha vaciado y la corona no está en su sitio: hay que empezar de nuevo (carta 79).', 'bad');
      setTimeout(() => { if (!resuelto) { t[0] = []; for (let k = D.discos; k >= 1; k--) t[0].push(k); t[1] = []; t[2] = []; movs = 0; pintar(); } }, 700);
    }
  }
  ui.button('Empezar de nuevo', 'ghost', () => { if (!resuelto) { t[0] = []; for (let k = D.discos; k >= 1; k--) t[0].push(k); t[1] = []; t[2] = []; movs = 0; sel = null; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}

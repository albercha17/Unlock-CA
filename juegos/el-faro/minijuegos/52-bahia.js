// Carta 52 — El plano de la bahía: marcar en una rejilla de 7 x 7 qué casillas son islote (tipo Nurikabe). Los números de cada islote están en el plano de
// Anselmo, partido en dos cartas (54 y 55), y las reglas, en sus versos (carta 59). Solución única (herramientas/instancias_faro.py, bahia).
import { openGame } from './ui.js';

const B = /*DATOS*/{"n": 7, "tierra": [[0, 0], [0, 1], [0, 5], [0, 6], [1, 0], [1, 3], [1, 4], [1, 6], [2, 2], [2, 4], [3, 1], [3, 2], [3, 6], [4, 4], [4, 6], [5, 1], [5, 3], [5, 6], [6, 1], [6, 3], [6, 5], [6, 6]], "cifra": 6}/*FIN*/;
const FILAS = 'ABCDEFGH';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 52 — El plano de la bahía',
    instr: 'Tocad las casillas que son islote (otra vez para devolverlas al mar). Los números de los islotes están en el plano de Anselmo (cartas 54 y 55) y sus versos (carta 59) dicen las reglas. Cuando el canal esté claro, pulsad «Transmitir».',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-bahia{display:grid;grid-template-columns:20px repeat(${B.n},1fr);gap:3px;width:min(88vw,330px);margin:6px auto;align-items:center}
    .far-bahia b{font:700 .75rem system-ui;color:#cfe3ee;text-align:center}
    .far-cas{aspect-ratio:1;border:0;border-radius:4px;background:linear-gradient(160deg,#3a7a96,#24586e);cursor:pointer;padding:0}
    .far-cas.tierra{background:radial-gradient(circle at 40% 35%,#e8d29a,#b89a5a 75%)}
    .far-bahia.ok .far-cas:not(.tierra){box-shadow:inset 0 0 0 2px #7be495}
  `;
  ui.body.appendChild(style);
  const g = document.createElement('div');
  g.className = 'far-bahia';
  ui.body.appendChild(g);

  const tierra = new Set();
  let resuelto = false;
  g.appendChild(document.createElement('span'));
  for (let c = 0; c < B.n; c++) { const t = document.createElement('b'); t.textContent = String(c + 1); g.appendChild(t); }
  for (let f = 0; f < B.n; f++) {
    const t = document.createElement('b'); t.textContent = FILAS[f]; g.appendChild(t);
    for (let c = 0; c < B.n; c++) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'far-cas';
      b.dataset.f = String(f);
      b.dataset.c = String(c);
      b.setAttribute('aria-label', 'Casilla ' + FILAS[f] + (c + 1));
      b.addEventListener('click', () => {
        if (resuelto) return;
        const k = f + ',' + c;
        tierra.has(k) ? tierra.delete(k) : tierra.add(k);
        b.classList.toggle('tierra', tierra.has(k));
        ui.say('');
      });
      g.appendChild(b);
    }
  }

  ui.button('Transmitir', 'primary', () => {
    if (resuelto) return;
    const sol = new Set(B.tierra.map(([f, c]) => f + ',' + c));
    if (sol.size === tierra.size && [...sol].every(k => tierra.has(k))) {
      resuelto = true;
      g.classList.add('ok');
      ui.say('«Recibido, Cabo Niebla: tomamos el canal». La guardia costera os da las gracias, pero añade que el capitán necesita ver la luz del faro. Cifra de la bahía: ' + B.cifra + '. Coged la carta 44.', 'ok');
    } else {
      ui.say('La guardia costera no lo entiende: ese plano no cuadra. Cada islote mide lo que dice su número, no se tocan entre ellos, y el mar va todo unido y sin charcos de 2 × 2 (cartas 54, 55 y 59).', 'bad');
    }
  });
  ui.button('Todo mar', '', () => { if (!resuelto) { tierra.clear(); g.querySelectorAll('.far-cas.tierra').forEach(b => b.classList.remove('tierra')); ui.say(''); } });
  return { close: ui.close };
}

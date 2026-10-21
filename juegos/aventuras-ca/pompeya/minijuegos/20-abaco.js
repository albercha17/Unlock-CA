// Carta 20 — El arca de Lucrecia: poner en el ábaco romano (columnas de millares, centenas, decenas y unidades; la cuenta de arriba vale 5)
// el total verdadero de las tres tablillas de cuentas (cartas 21, 23 y 24), leídas con la regla del escriba (carta 25).
import { openGame } from './ui.js';

const D = /*DATOS*/{"total": 1747}/*FIN*/;
const COLS = [['M', 1000], ['C', 100], ['X', 10], ['I', 1]];

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 20 — El arca de Lucrecia', instr: 'El ábaco de la tapa: en cada columna, la cuenta de arriba vale cinco y las de abajo, una. Tocad para subir o bajar cuentas y abrid el arca.', ...opts });
  const style = document.createElement('style');
  style.textContent = `
    .pom-abaco{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;max-width:300px;margin:6px auto;padding:10px;border-radius:10px;background:#5a3a1c;border:4px solid #c8a050}
    .pom-col{display:flex;flex-direction:column;align-items:center;gap:4px;background:linear-gradient(90deg,transparent 46%,#c8a050 46% 54%,transparent 54%)}
    .pom-col b{font:800 1rem Georgia,serif;color:#f6e4b8;background:#5a3a1c;padding:0 4px}
    .pom-cuenta{width:40px;height:22px;border-radius:12px;border:2px solid #3a2410;background:#8a8070;cursor:pointer;padding:0}
    .pom-cuenta.on{background:radial-gradient(circle at 40% 35%,#ffe9a0,#d0a030)}
    .pom-sep{width:100%;height:4px;background:#2a1a08;margin:4px 0}`;
  ui.body.appendChild(style);
  const ab = document.createElement('div'); ab.className = 'pom-abaco'; ui.body.appendChild(ab);
  const v = { M: [0, 0], C: [0, 0], X: [0, 0], I: [0, 0] };   // [cuenta de cinco, cuentas de uno]
  let resuelto = false;
  function pintar() {
    ab.innerHTML = '';
    COLS.forEach(([k]) => {
      const c = document.createElement('div'); c.className = 'pom-col';
      c.innerHTML = '<b>' + k + '</b>';
      const cinco = document.createElement('button'); cinco.type = 'button'; cinco.className = 'pom-cuenta' + (v[k][0] ? ' on' : '');
      cinco.dataset.col = k; cinco.dataset.t = '5'; cinco.setAttribute('aria-label', 'Cuenta de cinco de la columna ' + k);
      cinco.addEventListener('click', () => { if (!resuelto) { v[k][0] = 1 - v[k][0]; ui.say(''); pintar(); } });
      c.appendChild(cinco);
      const sep = document.createElement('div'); sep.className = 'pom-sep'; c.appendChild(sep);
      for (let i = 0; i < 4; i++) {
        const u = document.createElement('button'); u.type = 'button'; u.className = 'pom-cuenta' + (i < v[k][1] ? ' on' : '');
        u.dataset.col = k; u.dataset.t = '1'; u.dataset.i = String(i); u.setAttribute('aria-label', 'Cuenta de uno de la columna ' + k);
        u.addEventListener('click', () => { if (!resuelto) { v[k][1] = (i < v[k][1]) ? i : i + 1; ui.say(''); pintar(); } });
        c.appendChild(u);
      }
      ab.appendChild(c);
    });
  }
  ui.button('Abrir el arca', 'primary', () => {
    if (resuelto) return;
    const n = COLS.reduce((s, [k, m]) => s + (v[k][0] * 5 + v[k][1]) * m, 0);
    if (n === D.total) { resuelto = true; ui.say('Clac: el arca se abre. Lucrecia sabía que su esclavo no sabía sumar. Coged la carta 26.', 'ok'); }
    else ui.say('La tapa no se mueve. ¿Habéis comprobado bien las cuentas de Tiro (cartas 21, 23 y 24)?', 'bad');
  });
  pintar();
  return { close: ui.close };
}

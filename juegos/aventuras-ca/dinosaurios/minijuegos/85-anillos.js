// Carta 85 — El calibrador del Cronoportal: pide cuántos años lleva la doctora Ibarra en el Cretácico, para traerla de vuelta con vosotros.
// Llegó el día de la gran erupción (último anillo del tronco del volcán, carta 86) y el tronco de la entrada cayó esta mañana (carta 76);
// el tronco del río (carta 87) une los dos por los dibujos de sus anillos. Solución: instancias_dinosaurios.py, ANILLOS.
import { openGame } from './ui.js';
import { estilo } from './valle.js';

const D = /*DATOS*/{"troncos": ["fmfgmmffffmgm", "fmgmffggmmff", "mmffmffgmmffm"], "solucion": 17, "tramos": [[0, 13], [9, 21], [17, 30]]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 85 — El calibrador', instr: 'El Cronoportal solo se lleva a la doctora si le decís cuántos años lleva aquí. Girad las dos ruedas y pulsad «Calibrar».', ...opts });
  estilo('dn-anillos', `
    .ani-ruedas{display:flex;justify-content:center;gap:14px;margin:10px 0}
    .ani-rueda{display:flex;flex-direction:column;align-items:center;gap:4px}
    .ani-rueda button{width:52px;height:36px;border-radius:8px;border:2px solid #b5e35b;background:#3d5a24;color:#f2ffd6;font:800 1rem system-ui;cursor:pointer}
    .ani-rueda b{width:62px;height:70px;border-radius:12px;background:radial-gradient(circle,#6a4a24,#2a1a0c);color:#ffe08a;font:800 2.4rem Georgia,serif;display:flex;align-items:center;justify-content:center}`);
  const c = document.createElement('div'); c.className = 'ani-ruedas';
  ui.body.appendChild(c);
  const dig = [0, 0];
  const caras = [];
  dig.forEach((_, i) => {
    const w = document.createElement('div'); w.className = 'ani-rueda'; w.dataset.i = String(i);
    const up = document.createElement('button'); up.type = 'button'; up.textContent = '▲'; up.dataset.d = '1';
    const b = document.createElement('b');
    const dn = document.createElement('button'); dn.type = 'button'; dn.textContent = '▼'; dn.dataset.d = '-1';
    [up, dn].forEach(x => x.addEventListener('click', () => { if (!resuelto) { dig[i] = (dig[i] + Number(x.dataset.d) + 10) % 10; ui.say(''); pintar(); } }));
    w.append(up, b, dn); c.appendChild(w); caras.push(b);
  });
  let resuelto = false;
  const pintar = () => { caras.forEach((b, i) => { b.textContent = String(dig[i]); }); c.dataset.n = String(dig[0] * 10 + dig[1]); };
  ui.button('Calibrar', 'primary', () => {
    if (resuelto) return;
    const n = dig[0] * 10 + dig[1];
    if (n === D.solucion) {
      resuelto = true;
      ui.say('El anillo del Cronoportal se ilumina: ' + n + ' años. La doctora Ibarra llora de alegría y se agarra a vuestro brazo. Coged la carta 99.', 'ok');
    } else ui.say('El anillo parpadea en rojo: no son ' + n + ' años. Comparad los dibujos de los anillos de los tres troncos (cartas 76, 86 y 87).', 'bad');
  });
  pintar();
  return { close: ui.close };
}

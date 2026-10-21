// Carta 85 — La consola de lanzamiento (metapuzle): la clave son cuatro cifras, los «datos de la misión» que mostraron al resolverse cuatro puzles
// distintos, en el orden de los acertijos de las cartas 86 y 87: cableado, satélites, brazo de la antena e invernadero (instancias_marte.py).
import { openGame } from './ui.js';
import { estilo } from './cupula.js';

const D = /*DATOS*/{"codigo": [5, 3, 2, 8]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 85 — La consola de lanzamiento', instr: 'Marcad la clave de lanzamiento: son los datos de la misión de cuatro puzles que ya habéis resuelto, en el orden de los acertijos (cartas 86 y 87).', ...opts });
  estilo('mr-con', `.con-ruedas{display:flex;gap:12px;justify-content:center;margin:14px 0}.con-r{display:flex;flex-direction:column;align-items:center;gap:6px}.con-r button{width:54px;height:36px;border-radius:8px;border:2px solid #ff8a50;background:#4a2a1c;color:#ffe6d6;font:800 1rem system-ui;cursor:pointer}.con-r b{width:62px;height:76px;border-radius:12px;background:radial-gradient(circle,#4a2a1c,#1c0e0a);color:#ffb085;font:800 2.6rem Georgia,serif;display:flex;align-items:center;justify-content:center;border:2px solid #ff8a50}`);
  const c = document.createElement('div'); c.className = 'con-ruedas';
  ui.body.appendChild(c);
  const v = D.codigo.map(() => 0), caras = [];
  D.codigo.forEach((_, i) => {
    const w = document.createElement('div'); w.className = 'con-r'; w.dataset.i = String(i);
    const up = document.createElement('button'); up.type = 'button'; up.textContent = '▲'; up.dataset.d = '1'; up.setAttribute('aria-label', 'Subir la cifra ' + (i + 1));
    const b = document.createElement('b');
    const dn = document.createElement('button'); dn.type = 'button'; dn.textContent = '▼'; dn.dataset.d = '-1'; dn.setAttribute('aria-label', 'Bajar la cifra ' + (i + 1));
    [up, dn].forEach(x => x.addEventListener('click', () => { if (!resuelto) { v[i] = (v[i] + Number(x.dataset.d) + 10) % 10; ui.say(''); pintar(); } }));
    w.append(up, b, dn); c.appendChild(w); caras.push(b);
  });
  let resuelto = false;
  const pintar = () => { caras.forEach((b, i) => { b.textContent = String(v[i]); }); c.dataset.clave = v.join(''); };
  ui.button('Lanzar', 'primary', () => {
    if (resuelto) return;
    if (v.every((x, i) => x === D.codigo[i])) {
      resuelto = true;
      ui.say('La clave es correcta: el Cronoportal se enciende con un zumbido grave y se abre un anillo de luz azul. Coged la carta 99.', 'ok');
    } else ui.say('La consola parpadea en rojo: esa no es la clave. Recordad el dato que mostró cada puzle al resolverse y el orden de los acertijos (cartas 86 y 87).', 'bad');
  });
  pintar();
  return { close: ui.close };
}

// Carta 52 — El cañón: tres barcos enemigos a tiro, seis cargas de pólvora y cinco elevaciones. El alcance es la suma de lo que da la carga (carta 54), lo que
// da la elevación (carta 55) y el viento de cada barco (carta 59); cada barco necesita una carga distinta y la pólvora es limitada
// (instancias_piratas.py, CANON, solución única). Distancia del cañón: D.distancia.
import { openGame } from './ui.js';
import { estilo, opcion } from './comun.js';

const D = /*DATOS*/{"base": [2, 6, 7, 8, 9, 12], "corr": [4, 3, 0, 5, -1], "barcos": [{"dist": 8, "viento": 0}, {"dist": 12, "viento": 0}, {"dist": 9, "viento": 2}], "limite": 8, "solucion": [[3, 2], [2, 3], [0, 3]], "distancia": 4}/*FIN*/;
const ELEV = [0, 5, 10, 15, 20];

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 52 — El cañón', instr: 'Para cada barco, elegid los sacos de pólvora y la elevación del cañón para que el tiro caiga justo en él. Las tablas están en las cartas 54 y 55 y los barcos, el viento y la pólvora que queda, en la 59.', ...opts });
  estilo('pi-can', '.can-f{max-width:340px;margin:8px auto;padding:8px;border-radius:8px;background:#0c2a34;border:2px solid #e8b84a}.can-f b{display:block;color:#e8b84a;font:800 .9rem system-ui,sans-serif;margin-bottom:4px}.can-f .pi-btns{margin:2px 0;gap:4px}.can-f .pi-opc{min-width:44px;padding:0 6px}.can-f small{display:block;color:#9fe0e0;font:700 .72rem system-ui,sans-serif;margin-top:4px}');
  const carga = D.barcos.map(() => -1);
  const elev = D.barcos.map(() => -1);
  let resuelto = false;
  const refs = D.barcos.map((_, i) => {
    const f = document.createElement('div');
    f.className = 'can-f';
    f.dataset.i = String(i);
    const t = document.createElement('b');
    t.textContent = 'Barco ' + (i + 1);
    const l1 = document.createElement('small');
    l1.textContent = 'Sacos de pólvora';
    const fc = document.createElement('div');
    fc.className = 'pi-btns';
    const bc = D.base.map((_, c) => {
      const b = opcion(String(c + 1), () => { if (resuelto) return; carga[i] = c; ui.say(''); pintar(); });
      b.dataset.t = 'c';
      b.dataset.i = String(i);
      b.dataset.v = String(c);
      b.setAttribute('aria-label', 'Barco ' + (i + 1) + ', ' + (c + 1) + ' sacos');
      fc.appendChild(b);
      return b;
    });
    const l2 = document.createElement('small');
    l2.textContent = 'Elevación';
    const fe = document.createElement('div');
    fe.className = 'pi-btns';
    const be = ELEV.map((a, e) => {
      const b = opcion(a + '°', () => { if (resuelto) return; elev[i] = e; ui.say(''); pintar(); });
      b.dataset.t = 'e';
      b.dataset.i = String(i);
      b.dataset.v = String(e);
      b.setAttribute('aria-label', 'Barco ' + (i + 1) + ', elevación ' + a + ' grados');
      fe.appendChild(b);
      return b;
    });
    f.append(t, l1, fc, l2, fe);
    ui.body.appendChild(f);
    return { bc, be };
  });
  function pintar() { refs.forEach((r, i) => { r.bc.forEach((b, c) => b.classList.toggle('sel', carga[i] === c)); r.be.forEach((b, e) => b.classList.toggle('sel', elev[i] === e)); }); }
  ui.button('¡Fuego!', 'primary', () => {
    if (resuelto) return;
    if (carga.some(c => c < 0) || elev.some(e => e < 0)) { ui.say('Falta cargar o apuntar algún cañón.', 'bad'); return; }
    if (new Set(carga).size < carga.length) { ui.say('Dos barcos con la misma carga: solo hay un barril de cada tamaño.', 'bad'); return; }
    const gasto = carga.reduce((a, c) => a + c + 1, 0);
    if (gasto > D.limite) { ui.say('Gastáis ' + gasto + ' sacos de pólvora y solo quedan ' + D.limite + '.', 'bad'); return; }
    const fallos = D.barcos.map((b, i) => D.base[carga[i]] + D.corr[elev[i]] + b.viento !== b.dist ? i + 1 : 0).filter(x => x);
    if (fallos.length) { ui.say('¡Plof! ' + (fallos.length === 1 ? 'El tiro al barco ' + fallos[0] + ' cae al agua' : 'Los tiros a los barcos ' + fallos.join(' y ') + ' caen al agua') + ': no aciertan.', 'bad'); return; }
    resuelto = true;
    ui.say('Los tres tiros dan en el blanco y los barcos enemigos se retiran. Distancia del cañón: ' + D.distancia + (D.distancia === 1 ? ' casilla' : ' casillas') + '. Coged la carta 44.', 'ok');
  });
  ui.button('Borrar todo', '', () => { if (!resuelto) { carga.fill(-1); elev.fill(-1); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}

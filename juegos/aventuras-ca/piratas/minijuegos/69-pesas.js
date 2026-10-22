// Carta 69 — La balanza: tres cofres del botín (carta 70) y cuatro pesas de hierro de 1, 3, 9 y 27 libras (carta 71). Cada pesa puede ir en el mismo platillo
// que el cofre, en el contrario o quedarse fuera; hay que equilibrar la balanza de cada cofre (instancias_piratas.py, PESAS: ternario equilibrado,
// solución única). Distancia de la balanza: D.distancia.
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"pesas": [1, 3, 9, 27], "objetos": [22, 31, 17], "solucion": [[1, 1, -1, 1], [1, 1, 0, 1], [-1, 0, -1, 1]], "distancia": 1}/*FIN*/;
const ESTADOS = ['fuera', 'con el cofre', 'enfrente'];
const COEF = [0, -1, 1];                       // con el cofre: -1 (suma al lado del cofre); enfrente: +1

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 69 — La balanza', instr: 'Para cada cofre, tocad cada pesa para ponerla fuera, en el mismo platillo que el cofre o en el platillo de enfrente, hasta equilibrar la balanza. Los pesos de los cofres están en la carta 70 y las pesas, en la 71.', ...opts });
  estilo('pi-pes', '.pes-f{max-width:340px;margin:8px auto;padding:8px;border-radius:8px;background:#0c2a34;border:2px solid #e8b84a}.pes-f b{display:block;color:#e8b84a;font:800 .9rem system-ui,sans-serif;margin-bottom:6px}.pes-f .pi-btns{margin:2px 0;gap:4px}.pes-f .pi-opc{flex:1;min-width:0;padding:4px 2px;font-size:.8rem;min-height:56px}');
  const est = D.objetos.map(() => D.pesas.map(() => 0));
  let resuelto = false;
  const refs = D.objetos.map((_, o) => {
    const f = document.createElement('div');
    f.className = 'pes-f';
    f.dataset.o = String(o);
    const t = document.createElement('b');
    t.textContent = 'Cofre ' + (o + 1);
    const fila = document.createElement('div');
    fila.className = 'pi-btns';
    const bs = D.pesas.map((w, p) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'pi-opc';
      b.dataset.o = String(o);
      b.dataset.p = String(p);
      b.addEventListener('click', () => { if (resuelto) return; est[o][p] = (est[o][p] + 1) % 3; ui.say(''); pintar(); });
      fila.appendChild(b);
      return b;
    });
    f.append(t, fila);
    ui.body.appendChild(f);
    return bs;
  });
  function pintar() {
    refs.forEach((bs, o) => bs.forEach((b, p) => {
      b.textContent = D.pesas[p] + ' lb · ' + ESTADOS[est[o][p]];
      b.dataset.e = String(est[o][p]);
      b.classList.toggle('sel', est[o][p] !== 0);
      b.setAttribute('aria-label', 'Cofre ' + (o + 1) + ', pesa de ' + D.pesas[p] + ' libras: ' + ESTADOS[est[o][p]]);
    }));
  }
  ui.button('Pesar', 'primary', () => {
    if (resuelto) return;
    for (let o = 0; o < D.objetos.length; o++) {
      const suma = D.pesas.reduce((a, w, p) => a + w * COEF[est[o][p]], 0);
      if (suma !== D.objetos[o]) {
        ui.say('La balanza del cofre ' + (o + 1) + (suma < D.objetos[o] ? ' se inclina hacia el cofre: faltan pesas enfrente o sobran con él.' : ' se inclina hacia las pesas: sobran pesas enfrente o faltan con el cofre.'), 'bad');
        return;
      }
    }
    resuelto = true;
    ui.say('Los tres cofres quedan en equilibrio, con el fiel de la balanza a plomo. Distancia de la balanza: ' + D.distancia + (D.distancia === 1 ? ' casilla' : ' casillas') + '. Coged la carta 80.', 'ok');
  });
  ui.button('Quitar todas las pesas', '', () => { if (!resuelto) { est.forEach(r => r.fill(0)); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}

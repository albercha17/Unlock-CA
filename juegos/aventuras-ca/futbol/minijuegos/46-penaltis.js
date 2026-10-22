// Carta 46 — La tanda de penaltis: el portero rival decide su salto mirando solo los dos últimos tiros; la regla sale del informe de once penaltis (cartas 37 y
// 39; cómo se lee, en la 33). Hay que marcar cinco seguidos: si el portero para uno, la tanda empieza de nuevo (instancias_futbol.py, PENALTIS).
import { openGame } from './ui.js';
import { estilo, opcion } from './comun.js';

const D = /*DATOS*/{"regla": {"00": 0, "01": 0, "02": 0, "10": 1, "11": 0, "12": 2, "20": 2, "21": 1, "22": 1}, "ultimos": [0, 2], "tanda": 5}/*FIN*/;
const LADOS = ['izquierda', 'centro', 'derecha'];

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 46 — La tanda de penaltis', instr: 'Elegid hacia dónde tirar cada penalti para marcar los cinco seguidos. El informe del portero está en las cartas 37 y 39 y su explicación, en la 33.', ...opts });
  estilo('fu-pen', '.pen-m{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;max-width:340px;margin:8px auto}.pen-m div{min-height:44px;border-radius:8px;border:2px solid #c9f5c0;background:#0e3a18;color:#f4fff0;font:800 1rem system-ui,Arial,sans-serif;display:flex;align-items:center;justify-content:center}.pen-m div.gol{background:#f2c230;color:#12310f}');
  let tiros, goles = 0, resuelto = false;
  const marcador = document.createElement('div');
  marcador.className = 'pen-m';
  const casillas = Array.from({ length: D.tanda }, (_, k) => {
    const c = document.createElement('div');
    c.dataset.k = String(k);
    marcador.appendChild(c);
    return c;
  });
  const fila = document.createElement('div');
  fila.className = 'fu-btns';
  LADOS.forEach((t, k) => {
    const b = opcion(t[0].toUpperCase() + t.slice(1), () => tirar(k));
    b.dataset.l = String(k);
    fila.appendChild(b);
  });
  ui.body.append(marcador, fila);
  function empezar() { tiros = D.ultimos.slice(); goles = 0; pintar(); }
  function pintar() { casillas.forEach((c, k) => { c.textContent = k < goles ? 'GOL' : String(k + 1); c.classList.toggle('gol', k < goles); }); }
  function tirar(k) {
    if (resuelto) return;
    const salto = D.regla[String(tiros[tiros.length - 2]) + String(tiros[tiros.length - 1])];
    tiros.push(k);
    if (salto === k) {
      ui.say('El portero se lanza a la ' + LADOS[salto] + ' y la para. Hay que empezar la tanda de nuevo.', 'bad');
      empezar();
      return;
    }
    goles++;
    pintar();
    if (goles === D.tanda) {
      resuelto = true;
      ui.say('Cinco penaltis, cinco goles: el portero no ha adivinado ninguno. Coged la carta 56.', 'ok');
    } else {
      ui.say('¡Gol! El portero se tiró a la ' + LADOS[salto] + '.', 'ok');
    }
  }
  empezar();
  return { close: ui.close };
}

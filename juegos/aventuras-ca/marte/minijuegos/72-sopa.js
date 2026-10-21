// Carta 72 — La base de datos: la clave de acceso es la palabra que forman, leídas en orden, las letras de la sopa que no pertenecen a ninguna de
// las palabras de la lista. La sopa y la lista, en las cartas 75 y 79 (dos mitades). La app solo pide la clave (instancias_marte.py, SOPA).
import { openGame } from './ui.js';
import { estilo } from './cupula.js';

const D = /*DATOS*/{"secreta": "LANZADOR"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 72 — La base de datos', instr: 'Escribid la clave de acceso a los archivos de la colonia: las letras sobrantes de la sopa de letras (cartas 75 y 79), leídas en orden.', ...opts });
  estilo('mr-sop', `.sop-in{display:block;margin:14px auto;width:min(80vw,280px);padding:10px;text-align:center;letter-spacing:.2em;text-transform:uppercase;border-radius:10px;border:2px solid #ff8a50;background:#ffe6d6;color:#2a120c;font:800 1.3rem Georgia,serif}`);
  const e = document.createElement('input'); e.type = 'text'; e.className = 'sop-in'; e.maxLength = 16; e.autocomplete = 'off'; e.setAttribute('aria-label', 'Clave de acceso');
  e.addEventListener('input', () => ui.say(''));
  ui.body.appendChild(e);
  let resuelto = false;
  const prueba = () => {
    if (resuelto) return;
    const v = e.value.trim().toUpperCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
    if (!v) { ui.say('Escribid la clave.', 'bad'); return; }
    if (v === D.secreta) {
      resuelto = true;
      ui.say('«Acceso concedido.» Los archivos de la colonia se abren: planos del cohete y coordenadas de lanzamiento. Coged la carta 82.', 'ok');
    } else ui.say('«Clave incorrecta.» Tiene ' + D.secreta.length + ' letras: son las que no pertenecen a ninguna palabra de la lista (cartas 75 y 79).', 'bad');
  };
  e.addEventListener('keydown', ev => { if (ev.key === 'Enter') prueba(); });
  ui.button('Probar la clave', 'primary', prueba);
  return { close: ui.close };
}

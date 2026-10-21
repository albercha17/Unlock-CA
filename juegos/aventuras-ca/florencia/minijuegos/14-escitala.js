// Carta 14 — El cofre del maestro (escítala): la tapa lleva cosida una tira de cuero con letras (carta 16). Leonardo la escribió enrollada en una vara de
// cuatro caras; para leerla hay que volver a enrollarla. El cofre se abre con la palabra que pide el mensaje. Solución: ALAS (instancias_florencia.py, ESCITALA).
import { openGame } from './ui.js';
import { estilo } from './taller.js';

const D = /*DATOS*/{"caras": 4, "solucion": "ALAS", "letras": null}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 14 — El cofre del maestro', instr: 'La cerradura pide una palabra: la que dice el mensaje de la tira de cuero de la tapa (carta 16). Escribidla sin espacios.', ...opts });
  estilo('fl-esc', `.esc-in{display:block;margin:14px auto;width:min(80vw,280px);padding:10px;text-align:center;letter-spacing:.25em;text-transform:uppercase;border-radius:10px;border:2px solid #d9a441;background:#f6e7bf;color:#2a1f0c;font:800 1.3rem Georgia,serif}`);
  const e = document.createElement('input'); e.type = 'text'; e.className = 'esc-in'; e.maxLength = 16; e.autocomplete = 'off'; e.setAttribute('aria-label', 'Palabra de la cerradura');
  e.addEventListener('input', () => ui.say(''));
  ui.body.appendChild(e);
  let resuelto = false;
  const prueba = () => {
    if (resuelto) return;
    const v = e.value.trim().toUpperCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
    if (!v) { ui.say('Escribid la palabra.', 'bad'); return; }
    if (v === D.solucion) {
      resuelto = true;
      ui.say('La cerradura gira con un chasquido y la tapa del cofre se levanta. Coged la carta 24.', 'ok');
    } else ui.say('La cerradura no cede. Tiene ' + D.solucion.length + ' letras y es lo que dice el mensaje de la tira: recordad que la vara tiene ' + D.caras + ' caras (carta 16).', 'bad');
  };
  e.addEventListener('keydown', ev => { if (ev.key === 'Enter') prueba(); });
  ui.button('Probar', 'primary', prueba);
  return { close: ui.close };
}

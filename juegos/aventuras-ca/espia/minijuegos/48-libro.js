// Carta 48 — La cifra del libro: un mensaje escondido en una novela de bolsillo. Cada palabra se da como página, renglón y palabra (carta 53); las páginas
// están en las cartas 42 y 49. Hay que escribir el mensaje que sale (instancias_espia.py, LIBRO).
import { openGame } from './ui.js';
import { limpio } from './comun.js';

const D = /*DATOS*/{"claro": "CRISTAL BAJO LA RULETA"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 48 — La cifra del libro', instr: 'Escribid las palabras del mensaje, en orden (con o sin espacios). Las páginas del libro están en las cartas 42 y 49 y los renglones del mensaje, en la 53.', ...opts });
  const campo = document.createElement('input');
  campo.type = 'text';
  campo.className = 'es-in';
  campo.autocomplete = 'off';
  campo.setAttribute('aria-label', 'Mensaje del libro');
  ui.body.appendChild(campo);
  const claro = limpio(D.claro);
  let resuelto = false;
  ui.button('Entregar el mensaje', 'primary', () => {
    if (resuelto) return;
    const t = limpio(campo.value);
    if (!t) { ui.say('Todavía no habéis escrito nada.', 'bad'); return; }
    if (t !== claro) {
      ui.say('No tiene sentido: el mensaje de Zorro tiene ' + D.claro.split(' ').length + ' palabras y las vuestras no encajan.', 'bad');
      return;
    }
    resuelto = true;
    ui.say('Es el aviso que esperaba Zorro: el botín está bajo la mesa de la ruleta. Coged la carta 36.', 'ok');
  });
  return { close: ui.close };
}

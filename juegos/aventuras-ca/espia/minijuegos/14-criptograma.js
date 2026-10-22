// Carta 14 — La nota de la Agente Zorro: un mensaje cifrado por sustitución simple (cada letra es siempre otra). Hay que escribir el mensaje original.
// La nota cifrada, solo en la carta 16; la primera palabra se da como pista. Pulsaciones del teléfono rojo: D.pulsa (instancias_espia.py, CRIPTOGRAMA).
import { openGame } from './ui.js';
import { limpio } from './comun.js';

const D = /*DATOS*/{"claro": "AGENTE ZORRO ESPERA EN EL MUELLE DE LA RULETA AZUL", "pulsa": "9999"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 14 — La nota de la Agente Zorro', instr: 'Escribid el mensaje original de la nota (con o sin espacios, da igual). La nota cifrada está en la carta 16.', ...opts });
  const campo = document.createElement('input');
  campo.type = 'text';
  campo.className = 'es-in';
  campo.autocomplete = 'off';
  campo.setAttribute('aria-label', 'Mensaje descifrado');
  ui.body.appendChild(campo);
  const claro = limpio(D.claro);
  let resuelto = false;
  ui.button('Entregar el mensaje', 'primary', () => {
    if (resuelto) return;
    const t = limpio(campo.value);
    if (!t) { ui.say('Todavía no habéis escrito nada.', 'bad'); return; }
    if (t.length !== claro.length) { ui.say('La nota tiene ' + claro.length + ' letras y lo que habéis escrito tiene ' + t.length + '.', 'bad'); return; }
    if (t !== claro) {
      const bien = t.split('').filter((c, i) => c === claro[i]).length;
      ui.say('Zorro niega con la cabeza: ' + bien + ' de las ' + claro.length + ' letras están en su sitio.', 'bad');
      return;
    }
    resuelto = true;
    ui.say('Zorro asiente: el mensaje está claro. Teléfono rojo: pulsad ' + D.pulsa + '. Coged la carta 24.', 'ok');
  });
  return { close: ui.close };
}

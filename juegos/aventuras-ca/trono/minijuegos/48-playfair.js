// Carta 48 — La carta de la prisionera (cifrado de Playfair): el mensaje, en pares de letras (carta 42), está cifrado con el cuadrado de la clave
// (carta 49); la regla para cifrar, en la carta 53. Hay que escribir el mensaje descifrado (instancias_trono.py, PLAYFAIR).
import { openGame } from './ui.js';
import { estilo } from './reino.js';

const D = /*DATOS*/{"claro": "DRAGONES"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 48 — La carta de la prisionera', instr: 'Escribid el mensaje que la prisionera esconde en la carta, ya descifrado. Las letras cifradas, el cuadrado y la regla, en las cartas 42, 49 y 53.', ...opts });
  estilo('tr-pla', `.pla-in{display:block;margin:14px auto;width:min(80vw,300px);padding:10px;text-align:center;letter-spacing:.25em;text-transform:uppercase;border-radius:10px;border:2px solid #8fc7ee;background:#e6f1fb;color:#0c121a;font:800 1.3rem Georgia,serif}`);
  const e = document.createElement('input'); e.type = 'text'; e.className = 'pla-in'; e.maxLength = 16; e.autocomplete = 'off'; e.setAttribute('aria-label', 'Mensaje descifrado');
  e.addEventListener('input', () => ui.say(''));
  ui.body.appendChild(e);
  let resuelto = false;
  const prueba = () => {
    if (resuelto) return;
    const v = e.value.trim().toUpperCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^A-Z]/g, '');
    if (!v) { ui.say('Escribid el mensaje.', 'bad'); return; }
    if (v === D.claro) {
      resuelto = true;
      ui.say('La prisionera lo confirma en voz baja: es justo lo que quería decir. Se abre la celda. Coged la carta 36.', 'ok');
    } else ui.say('Eso no tiene sentido: es una palabra de ' + D.claro.length + ' letras. Repasad pareja a pareja (cartas 42, 49 y 53).', 'bad');
  };
  e.addEventListener('keydown', ev => { if (ev.key === 'Enter') prueba(); });
  ui.button('Descifrar', 'primary', prueba);
  return { close: ui.close };
}

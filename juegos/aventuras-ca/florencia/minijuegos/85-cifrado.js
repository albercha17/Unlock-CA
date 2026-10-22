// Carta 85 — El lucernario (metapuzle, cifrado de Vigenère): el mensaje de Leonardo (carta 86) está cifrado con una clave de cuatro letras, una por cada
// uno de cuatro puzles resueltos (pigmentos, poleas, mastermind y caballo, en ese orden); la tabla, en la carta 87. Se pide la palabra que dice
// el mensaje (instancias_florencia.py, CIFRADO).
import { openGame } from './ui.js';
import { estilo } from './taller.js';

const D = /*DATOS*/{"claro": "AMANECER"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 85 — El lucernario', instr: 'El mensaje del cristal (carta 86) se lee con la clave de cuatro letras que dejaron cuatro puzles resueltos y la tabla de la carta 87. Escribid la palabra que dice.', ...opts });
  estilo('fl-cif', `.cif-in{display:block;margin:14px auto;width:min(80vw,300px);padding:10px;text-align:center;letter-spacing:.25em;text-transform:uppercase;border-radius:10px;border:2px solid #d9a441;background:#f6e7bf;color:#2a1f0c;font:800 1.3rem Georgia,serif}`);
  const e = document.createElement('input'); e.type = 'text'; e.className = 'cif-in'; e.maxLength = 16; e.autocomplete = 'off'; e.setAttribute('aria-label', 'Palabra del mensaje');
  e.addEventListener('input', () => ui.say(''));
  ui.body.appendChild(e);
  let resuelto = false;
  const prueba = () => {
    if (resuelto) return;
    const v = e.value.trim().toUpperCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
    if (!v) { ui.say('Escribid la palabra.', 'bad'); return; }
    if (v === D.claro) {
      resuelto = true;
      ui.say('El cristal del lucernario se enciende con la palabra y el primer rayo del alba cruza la lente. Coged la carta 99.', 'ok');
    } else ui.say('El cristal sigue oscuro. Es una palabra de ' + D.claro.length + ' letras: comprobad la clave y el orden de los puzles (cartas 86 y 87).', 'bad');
  };
  e.addEventListener('keydown', ev => { if (ev.key === 'Enter') prueba(); });
  ui.button('Descifrar', 'primary', prueba);
  return { close: ui.close };
}

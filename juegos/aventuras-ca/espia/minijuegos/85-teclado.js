// Carta 85 — El teléfono rojo: un teclado de teléfono con letras (multitoque: la tecla 7 una vez es P, dos veces Q...). La palabra final se marca con las
// pulsaciones que dejaron cinco puzles. El orden, en la carta 86; el teclado, en la 87 (instancias_espia.py, PALABRA, TECLADO).
import { openGame } from './ui.js';

const D = /*DATOS*/{"palabra": "ZARPA"}/*FIN*/;
const TECLAS = { '2': 'ABC', '3': 'DEF', '4': 'GHI', '5': 'JKL', '6': 'MNO', '7': 'PQRS', '8': 'TUV', '9': 'WXYZ' };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 85 — El teléfono rojo', instr: 'Marcad la clave pulsando las teclas tantas veces como pida cada letra. Entre una letra y la siguiente, tocad «Pausa». El orden de las cinco pulsaciones está en la carta 86 y el teclado, en la 87.', ...opts });
  const estilo = document.createElement('style');
  estilo.textContent = '.tel-pantalla{max-width:340px;margin:8px auto;padding:10px;border-radius:8px;background:#04141a;border:2px solid #7fe8f0;color:#7fe8f0;font:700 1.2rem ui-monospace,Consolas,monospace;min-height:2.6em;word-break:break-all}.tel-teclas{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;max-width:300px;margin:8px auto}.tel-teclas button{min-height:56px;border-radius:50%;border:3px solid #ff6fa8;background:linear-gradient(180deg,#e2467e,#7a1c40);color:#fff;font:800 1.3rem system-ui,Arial,sans-serif;cursor:pointer;padding:0}.tel-teclas button small{display:block;font:600 .6rem system-ui,Arial,sans-serif}';
  document.head.appendChild(estilo);
  let marcado = [], resuelto = false;      // lista de grupos de pulsaciones; cada grupo es un string de la misma cifra
  const pantalla = document.createElement('div');
  pantalla.className = 'tel-pantalla';
  const teclas = document.createElement('div');
  teclas.className = 'tel-teclas';
  Object.keys(TECLAS).forEach(k => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.k = k;
    b.setAttribute('aria-label', 'Tecla ' + k + ', letras ' + TECLAS[k].split('').join(' '));
    b.innerHTML = k + '<small>' + TECLAS[k] + '</small>';
    b.addEventListener('click', () => {
      if (resuelto) return;
      const ult = marcado[marcado.length - 1];
      if (ult && ult[0] === k && !ult.cerrado) ult.push(k); else { const g = [k]; marcado.push(g); }
      ui.say('');
      pintar();
    });
    teclas.appendChild(b);
  });
  ui.body.append(pantalla, teclas);
  function letra(g) {
    const l = TECLAS[g[0]];
    return l ? l[(g.length - 1) % l.length] : '?';
  }
  function pintar() {
    pantalla.textContent = marcado.length ? marcado.map(g => letra(g)).join('') + '  (' + marcado.map(g => g.join('')).join(' ') + ')' : '—';
    pantalla.dataset.v = marcado.map(g => letra(g)).join('');
  }
  ui.button('Pausa', 'ghost', () => { if (!resuelto && marcado.length) { marcado[marcado.length - 1].cerrado = true; } });
  ui.button('Borrar una letra', 'ghost', () => { if (!resuelto) { marcado.pop(); ui.say(''); pintar(); } });
  ui.button('Marcar', 'primary', () => {
    if (resuelto) return;
    if (!marcado.length) { ui.say('Todavía no habéis marcado nada.', 'bad'); return; }
    const t = marcado.map(g => letra(g)).join('');
    if (t !== D.palabra) { ui.say('Al otro lado suena un tono agudo y cuelgan: la clave marcada no es la buena.', 'bad'); return; }
    resuelto = true;
    ui.say('Una voz grave contesta: «Palabra correcta: ' + D.palabra + '». Se abre el canal del Neptuno. Coged la carta 99.', 'ok');
  });
  pintar();
  return { close: ui.close };
}

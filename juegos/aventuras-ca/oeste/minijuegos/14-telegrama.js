// Carta 14 — El telegrama en zigzag: el telegrafista escribió el mensaje bajando y subiendo por cuatro «rieles» y luego lo leyó por pisos. Hay que
// escribir el mensaje original. El telegrama cifrado y el zigzag, solo en la carta 16. Coordenada de Polibio: D.coord (instancias_oeste.py, VALLAS).
import { openGame } from './ui.js';
import { estilo, limpio } from './comun.js';

const D = /*DATOS*/{"claro": "ELORONOVIAJAENELTERCERVAGONDETRAS", "rieles": 4, "coord": "51"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 14 — El telegrama en zigzag', instr: 'Escribid el mensaje original del telegrafista (sin espacios, o con ellos: da igual). El telegrama y el zigzag están en la carta 16.', ...opts });
  estilo('oe-tel', `.tel-in{display:block;width:100%;max-width:340px;margin:10px auto;padding:12px;border-radius:8px;border:3px solid #8a5a2a;background:#f2e2b8;color:#3a2412;font:700 1.1rem Georgia,serif;text-transform:uppercase}`);
  const campo = document.createElement('input');
  campo.type = 'text';
  campo.className = 'tel-in';
  campo.autocomplete = 'off';
  campo.setAttribute('aria-label', 'Mensaje del telegrama');
  ui.body.appendChild(campo);
  let resuelto = false;
  ui.button('Entregar el mensaje', 'primary', () => {
    if (resuelto) return;
    const t = limpio(campo.value);
    if (!t) { ui.say('Todavía no habéis escrito nada.', 'bad'); return; }
    if (t.length !== D.claro.length) { ui.say('El telegrama tiene ' + D.claro.length + ' letras y lo que habéis escrito tiene ' + t.length + '.', 'bad'); return; }
    if (t !== D.claro) {
      const bien = t.split('').filter((c, i) => c === D.claro[i]).length;
      ui.say('El telegrafista arruga el papel: ' + bien + ' de las ' + D.claro.length + ' letras están en su sitio.', 'bad');
      return;
    }
    resuelto = true;
    ui.say('El telegrafista asiente: el mensaje está claro. Coordenada de Polibio: ' + D.coord + '. Coged la carta 24.', 'ok');
  });
  return { close: ui.close };
}

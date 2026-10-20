// Carta 66 — La tapa del cofre: tocar las seis tachuelas-estrella que forman la Calavera de la carta celeste (carta 64), que en la tapa
// aparece girada y más pequeña entre otras estrellas. Instancia de herramientas/instancias_piratas.py: la figura aparece una sola vez.
import { openGame } from './ui.js';

const C = /*DATOS*/{"estrellas": [[234, 199], [56, 229], [134, 254], [186, 144], [281, 107], [222, 24], [96, 168], [212, 163], [69, 39], [48, 105], [172, 179], [124, 112], [31, 250], [259, 79], [116, 61], [243, 169], [41, 16], [241, 117], [77, 277], [276, 173], [160, 108], [138, 146], [98, 125], [28, 58], [202, 265], [178, 279], [171, 73], [232, 258], [206, 121], [141, 31]], "solucion": [7, 10, 11, 20, 21, 28]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 66 — La tapa del cofre',
    instr: 'La tapa del cofre del capitán Calavera es un cielo de tachuelas. Tocad las seis estrellas que forman la Calavera de la carta celeste (aquí está girada y es más pequeña) y abrid el cofre.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .pir-tapa{position:relative;width:min(84vw,300px);aspect-ratio:1;margin:4px auto 8px;border-radius:14px;border:6px solid #6a4422;
      background:radial-gradient(circle at 50% 40%,#2a3a6a,#121a36 70%,#0a0e20);box-shadow:inset 0 0 0 3px #b88a26,0 6px 16px rgba(0,0,0,.5)}
    .pir-tachuela{position:absolute;width:26px;height:26px;margin:-13px 0 0 -13px;border-radius:50%;border:0;padding:0;cursor:pointer;background:transparent}
    .pir-tachuela::after{content:'';position:absolute;inset:8px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff8d8,#e8c060 55%,#8a6a1a)}
    .pir-tachuela.sel::after{inset:4px;background:radial-gradient(circle,#fff,#ffe08a 45%,#ffb020);box-shadow:0 0 12px 4px rgba(255,220,120,.8)}
    .pir-tapa.ok{border-color:#7be495}
    .pir-cuenta{text-align:center;color:#9fe0e0;font:700 .9rem system-ui,sans-serif;margin:0 0 6px}
  `;
  ui.body.appendChild(style);

  const tapa = document.createElement('div');
  tapa.className = 'pir-tapa';
  const cuenta = document.createElement('p');
  cuenta.className = 'pir-cuenta';
  ui.body.appendChild(tapa);
  ui.body.appendChild(cuenta);

  const elegidas = new Set();
  let resuelto = false;

  function pintar() {
    tapa.querySelectorAll('.pir-tachuela').forEach(b => b.classList.toggle('sel', elegidas.has(Number(b.dataset.i))));
    tapa.classList.toggle('ok', resuelto);
    cuenta.textContent = 'Estrellas elegidas: ' + elegidas.size;
  }

  C.estrellas.forEach(([x, y], i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'pir-tachuela';
    b.dataset.i = String(i);
    b.style.left = (x / 3) + '%';
    b.style.top = (y / 3) + '%';
    b.setAttribute('aria-label', 'Tachuela ' + (i + 1));
    b.addEventListener('click', () => {
      if (resuelto) return;
      elegidas.has(i) ? elegidas.delete(i) : elegidas.add(i);
      ui.say('');
      pintar();
    });
    tapa.appendChild(b);
  });

  ui.button('Abrir el cofre', 'primary', () => {
    if (resuelto) return;
    if (elegidas.size !== C.solucion.length) { ui.say('La Calavera tiene seis estrellas, ni una más ni una menos.', 'bad'); return; }
    if (C.solucion.every(i => elegidas.has(i))) {
      resuelto = true;
      pintar();
      ui.say('Las seis tachuelas se hunden a la vez con un clic y la tapa se levanta sola. ¡El cofre del capitán Calavera está abierto! Coged la carta 72.', 'ok');
    } else {
      ui.say('La tapa no cede: esas seis estrellas no forman la Calavera. Comparad la forma con la carta celeste (carta 64), girándola.', 'bad');
    }
  });
  ui.button('Quitar todas', '', () => { if (!resuelto) { elegidas.clear(); ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}

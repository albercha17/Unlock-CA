// Carta 36 — El marcador del crupier: ordenar a los cuatro jugadores de mejor a peor mano de póker. Las manos están en las cartas 37,
// 39, 41 y 42; la lista de jugadas, aquí. Instancia de herramientas/instancias_ampliacion.py.
import { openGame } from './ui.js';

const DEF = {
  'escalera de color': 'cinco seguidas del mismo palo', 'póker': 'cuatro iguales', 'full': 'tres iguales y otras dos iguales',
  'color': 'cinco del mismo palo', 'escalera': 'cinco seguidas (J = 11, Q = 12, K = 13)', 'trío': 'tres iguales',
  'dobles parejas': 'dos parejas', 'pareja': 'dos iguales', 'carta alta': 'nada de lo anterior'
};

const P = /*DATOS*/{"jugadores": ["La Condesa", "El Barón", "El Dr. Noche", "La Agente Zorro"], "orden": ["El Barón", "El Dr. Noche", "La Condesa", "La Agente Zorro"], "ranking": ["escalera de color", "póker", "full", "color", "escalera", "trío", "dobles parejas", "pareja", "carta alta"]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 36 — El marcador del crupier',
    instr: 'Tocad a los jugadores en orden, del que ganó la mano al que quedó último. Las manos están en las cartas 37, 39, 41 y 42.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .esp-marcador{max-width:330px;margin:4px auto;padding:10px;border-radius:10px;background:#0e3a2a;border:3px solid #e0c070;color:#f4e6c0}
    .esp-marcador h4{margin:0 0 6px;font:700 .85rem Georgia,serif;text-align:center;color:#e0c070}
    .esp-jugadas{margin:0 0 8px;padding:0 0 0 20px;font:500 .78rem system-ui,sans-serif;line-height:1.45}
    .esp-jugadores{display:grid;grid-template-columns:1fr 1fr;gap:6px}
    .esp-jug{padding:10px 6px;border-radius:8px;border:2px solid #e0c070;background:#14513a;color:#fff;font:600 .85rem Georgia,serif;cursor:pointer;position:relative}
    .esp-jug b{position:absolute;right:6px;top:4px;color:#ffd84a;font:800 .9rem system-ui}
    .esp-jug.puesto{background:#2a6a4a}
  `;
  ui.body.appendChild(style);
  const m = document.createElement('div');
  m.className = 'esp-marcador';
  m.innerHTML = '<h4>Jugadas, de la mejor a la peor</h4><ol class="esp-jugadas">' + P.ranking.map(r => '<li><b>' + r + '</b>: ' + DEF[r] + '</li>').join('') + '</ol>';
  const js = document.createElement('div');
  js.className = 'esp-jugadores';
  m.appendChild(js);
  ui.body.appendChild(m);

  let orden = [], resuelto = false;
  function pintar() {
    js.innerHTML = '';
    P.jugadores.forEach(j => {
      const b = document.createElement('button');
      b.type = 'button';
      const pos = orden.indexOf(j);
      b.className = 'esp-jug' + (pos >= 0 ? ' puesto' : '');
      b.dataset.j = j;
      b.innerHTML = j + (pos >= 0 ? '<b>' + (pos + 1) + '.º</b>' : '');
      b.addEventListener('click', () => {
        if (resuelto) return;
        orden = pos >= 0 ? orden.filter(x => x !== j) : orden.concat(j);
        ui.say('');
        pintar();
      });
      js.appendChild(b);
    });
  }

  ui.button('Entregar', 'primary', () => {
    if (resuelto) return;
    if (orden.length < P.jugadores.length) { ui.say('Faltan jugadores por ordenar.', 'bad'); return; }
    if (orden.every((j, i) => j === P.orden[i])) {
      resuelto = true;
      ui.say('El crupier asiente sin mover un músculo y os desliza una llave dorada bajo una ficha: «El ascensor de la torre, caballeros». Coged la carta 58.', 'ok');
    } else {
      ui.say('El crupier niega con la cabeza: así no quedó la partida. Mirad bien cada mano (cartas 37, 39, 41 y 42): palos y números.', 'bad');
    }
  });
  ui.button('Borrar', '', () => { if (!resuelto) { orden = []; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}

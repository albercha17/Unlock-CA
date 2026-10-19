// Carta 48 — El panel de la liguilla: poner los tres marcadores que faltan para que, con los resultados conocidos (carta 53), salga la clasificación de la carta 52.
// Instancia (herramientas/instancias_futbol.py): solución única. Faltan Rayos–Leones 1-0, Rayos–Toros 0-3 y Leones–Águilas 3-1.
import { openGame } from './ui.js';

const EQUIPOS = ['Rayos', 'Leones', 'Águilas', 'Toros'];
const PARTIDOS = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]];
const RESULTADOS = [[1, 0], [2, 0], [0, 3], [3, 1], [2, 1], [2, 1]];      // los de los partidos conocidos (1, 4 y 5) cuentan; los demás los pone el jugador
const CONOCIDOS = [1, 4, 5];
const DESCONOCIDOS = [0, 2, 3];
const TABLA = [[6, 3, 3], [6, 5, 3], [3, 3, 6], [3, 5, 4]];               // puntos, goles a favor y goles en contra de cada equipo

function calcular(res) {
  const t = EQUIPOS.map(() => [0, 0, 0]);
  PARTIDOS.forEach(([a, b], i) => {
    const [ga, gb] = res[i];
    t[a][1] += ga; t[a][2] += gb; t[b][1] += gb; t[b][2] += ga;
    if (ga > gb) t[a][0] += 3; else if (ga < gb) t[b][0] += 3; else { t[a][0] += 1; t[b][0] += 1; }
  });
  return t;
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 48 — El panel de la liguilla',
    instr: 'Pon los marcadores de los tres partidos que faltan. Debajo verás la clasificación que saldría: tiene que ser la de la carta 52.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .fut-partidos{display:flex;flex-direction:column;gap:8px;margin:6px 0 10px}
    .fut-partido{display:grid;grid-template-columns:1fr auto auto auto 1fr;gap:6px;align-items:center;padding:8px;border-radius:8px;background:#14281c;border:2px solid #3a6a4a;color:#f4f0e0;font:700 .85rem system-ui,sans-serif}
    .fut-partido .eq{text-align:center}
    .fut-marcador{display:flex;align-items:center;gap:4px}
    .fut-marcador button{width:30px;height:30px;border-radius:6px;border:2px solid #f2c230;background:#1f3a28;color:#f2c230;font:800 1rem system-ui,sans-serif;cursor:pointer;padding:0}
    .fut-marcador span{min-width:22px;text-align:center;font:800 1.4rem Impact,"Arial Black",sans-serif;color:#fff}
    .fut-tabla{width:100%;max-width:320px;margin:0 auto 8px;border-collapse:collapse;color:#f4f0e0;font:700 .85rem system-ui,sans-serif;text-align:center}
    .fut-tabla th{color:#f2c230;font-weight:700;padding:3px}
    .fut-tabla td{padding:3px;border-top:1px solid #3a4a40}
    .fut-tabla td:first-child{text-align:left}
    .fut-tabla.ok td{color:#9be58a}
  `;
  ui.body.appendChild(style);

  const partidos = document.createElement('div');
  partidos.className = 'fut-partidos';
  const tabla = document.createElement('table');
  tabla.className = 'fut-tabla';
  ui.body.appendChild(partidos);
  ui.body.appendChild(tabla);

  const goles = DESCONOCIDOS.map(() => [0, 0]);
  let resuelto = false;

  function resultadosActuales() {
    const r = RESULTADOS.map(x => x.slice());
    DESCONOCIDOS.forEach((i, k) => { r[i] = goles[k].slice(); });
    return r;
  }

  function pintar() {
    partidos.innerHTML = '';
    DESCONOCIDOS.forEach((i, k) => {
      const [a, b] = PARTIDOS[i];
      const d = document.createElement('div');
      d.className = 'fut-partido';
      d.dataset.m = String(k);
      d.innerHTML = '<span class="eq">' + EQUIPOS[a] + '</span>';
      [0, 1].forEach(l => {
        const m = document.createElement('div');
        m.className = 'fut-marcador';
        m.innerHTML = '<button type="button" data-m="' + k + '" data-l="' + l + '" data-d="-1" aria-label="Quitar un gol a ' + EQUIPOS[l ? b : a] + '">−</button><span data-m="' + k + '" data-l="' + l + '">' + goles[k][l] + '</span><button type="button" data-m="' + k + '" data-l="' + l + '" data-d="1" aria-label="Poner un gol a ' + EQUIPOS[l ? b : a] + '">+</button>';
        m.querySelectorAll('button').forEach(bt => bt.addEventListener('click', () => {
          if (resuelto) return;
          goles[k][l] = Math.max(0, Math.min(5, goles[k][l] + Number(bt.dataset.d)));
          ui.say('');
          pintar();
        }));
        d.appendChild(m);
        if (l === 0) { const g = document.createElement('span'); g.textContent = '–'; d.appendChild(g); }
      });
      const e2 = document.createElement('span');
      e2.className = 'eq';
      e2.textContent = EQUIPOS[b];
      d.appendChild(e2);
      partidos.appendChild(d);
    });
    const t = calcular(resultadosActuales());
    tabla.className = 'fut-tabla' + (resuelto ? ' ok' : '');
    tabla.innerHTML = '<tr><th>Equipo</th><th>PTS</th><th>GF</th><th>GC</th></tr>' + EQUIPOS.map((e, i) => '<tr data-e="' + i + '"><td>' + e + '</td><td>' + t[i][0] + '</td><td>' + t[i][1] + '</td><td>' + t[i][2] + '</td></tr>').join('');
  }

  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const t = calcular(resultadosActuales());
    if (t.every((f, i) => f.every((v, j) => v === TABLA[i][j]))) {
      resuelto = true;
      pintar();
      ui.say('La clasificación sale clavada: el locutor la lee por megafonía y el estadio aplaude. Un mozo os da paso al túnel de salida. Coged la carta 58.', 'ok');
    } else {
      ui.say('La clasificación que sale no coincide con la de la carta 52. Mirad qué equipos no cuadran en puntos o en goles y repasad los resultados conocidos de la carta 53.', 'bad');
    }
  });
  ui.button('Poner a cero', '', () => { if (!resuelto) { goles.forEach(g => { g[0] = 0; g[1] = 0; }); ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}

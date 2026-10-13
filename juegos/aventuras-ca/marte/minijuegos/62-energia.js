// Carta 62 — Panel de energía: activar sistemas cuyo consumo sume justo la capacidad (15) con el escudo siempre activo.
// La capacidad y la regla del escudo vienen del protocolo del reactor (carta 59). El panel no dice cuánto falta.
import { openGame } from './ui.js';

const SISTEMAS = [
  { id: 'escudo', nombre: 'Escudo', w: 8, icono: 'escudo' },
  { id: 'radio', nombre: 'Radio', w: 4, icono: 'radio' },
  { id: 'luz', nombre: 'Luz', w: 3, icono: 'luz' },
  { id: 'bomba', nombre: 'Bomba', w: 5, icono: 'bomba' },
  { id: 'calor', nombre: 'Calefacción', w: 6, icono: 'calefaccion' },
  { id: 'orden', nombre: 'Ordenador', w: 9, icono: 'ordenador' }
];
const CAPACIDAD = 15;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 62 — Panel de energía',
    instr: 'Activa los sistemas cuyo consumo sume la capacidad del reactor y pulsa Conectar.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-sist{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:10px}
    .far-sis{display:flex;flex-direction:column;align-items:center;gap:2px;padding:8px 4px;border-radius:12px;border:1px solid rgba(255,255,255,.12);background:linear-gradient(rgba(6,10,16,.78),rgba(6,10,16,.92)),url(./img/ui/panel.jpg) center/cover;color:#9fb4c8;cursor:pointer;font:inherit;transition:box-shadow .2s,border-color .2s}
    .far-sis .ic{display:block;width:100%;height:74px;line-height:0}
    .far-sis .ic img{width:100%;height:100%;object-fit:contain;mix-blend-mode:screen;filter:grayscale(.7) brightness(.62);transition:filter .25s}
    .far-sis.on .ic img{filter:brightness(1.12) saturate(1.15) drop-shadow(0 0 8px rgba(76,201,240,.65))}
    .far-sis .nom{font-size:.78rem;font-weight:700}
    .far-sis .w{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:1rem;color:#ffd27a}
    .far-sis.on{border-color:#4cc9f0;background:#0f2a36;color:#fff;box-shadow:0 0 10px rgba(76,201,240,.4)}
  `;
  ui.body.appendChild(style);

  const grid = document.createElement('div');
  grid.className = 'far-sist';
  ui.body.appendChild(grid);

  const activos = new Set();
  let resuelto = false;

  function pintar() {
    grid.innerHTML = '';
    SISTEMAS.forEach(s => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'far-sis' + (activos.has(s.id) ? ' on' : '');
      b.dataset.sis = s.id;
      b.setAttribute('aria-pressed', String(activos.has(s.id)));
      b.innerHTML = '<span class="ic"><img alt="" src="./img/ui/modulos/' + s.icono + '.jpg"></span><span class="nom">' + s.nombre + '</span><span class="w">' + s.w + ' MW</span>';
      b.addEventListener('click', () => {
        if (resuelto) return;
        if (activos.has(s.id)) activos.delete(s.id); else activos.add(s.id);
        ui.say('');
        pintar();
      });
      grid.appendChild(b);
    });
  }

  ui.button('Conectar', 'primary', () => {
    if (resuelto) return;
    const total = SISTEMAS.filter(s => activos.has(s.id)).reduce((a, s) => a + s.w, 0);
    if (!activos.has('escudo')) {
      ui.say('Sin el escudo, la radiación apaga el reactor al instante.', 'bad');
    } else if (total !== CAPACIDAD) {
      ui.say('El reactor no arranca: la carga no es la adecuada.', 'bad');
    } else {
      resuelto = true;
      ui.say('El reactor arranca y el núcleo de fusión queda libre. Coged la carta 54.', 'ok');
    }
  });

  pintar();
  return { close: ui.close };
}

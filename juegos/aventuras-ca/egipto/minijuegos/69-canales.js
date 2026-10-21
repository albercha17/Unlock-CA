// Carta 69 — Los canales de riego: unir con zanjas los siete campos del valle gastando lo menos posible. Qué canales se pueden cavar y lo que
// cuesta cada uno, en el mapa de la carta 70; lo que quiere el visir, en la 71. En la app los canales posibles no se ven: se toca un campo
// y luego otro para cavar o rellenar el canal entre ellos. Solución única (árbol de expansión mínimo, instancias_egipto.py, CANALES).
import { openGame } from './ui.js';
import { estilo, guardarSello, NS } from './nilo.js';

const D = /*DATOS*/{"campos": {"A": [12, 24], "B": [40, 12], "C": [70, 22], "D": [88, 50], "E": [62, 70], "F": [30, 74], "G": [10, 52]}, "canales": [["A", "G", 6], ["B", "C", 3], ["D", "E", 27], ["E", "F", 20], ["F", "G", 5], ["C", "E", 16], ["A", "B", 25], ["C", "D", 10], ["B", "G", 26]], "solucion": [["A", "G"], ["B", "C"], ["C", "D"], ["C", "E"], ["E", "F"], ["F", "G"]], "coste": 60}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 69 — Los canales de riego', instr: 'Tocad un campo y luego otro para cavar un canal entre ellos (otra vez para rellenarlo). Que el agua llegue a todos los campos gastando lo menos posible.', ...opts });
  estilo('eg-can', `.can-mapa{width:min(88vw,330px);aspect-ratio:1;margin:8px auto;border-radius:10px;background:#8c7a4a;position:relative}.can-mapa svg{position:absolute;inset:0;width:100%;height:100%}.can-campo{position:absolute;width:46px;height:46px;margin:-23px;border-radius:50%;border:3px solid #2a1f0c;background:#d9a441;color:#2a1f0c;font:800 1.1rem Georgia,serif;cursor:pointer;padding:0}.can-campo.sel{background:#ffe08a;outline:3px solid #fff}`);
  const mapa = document.createElement('div'); mapa.className = 'can-mapa';
  const svg = document.createElementNS(NS, 'svg'); svg.setAttribute('viewBox', '0 0 100 100'); svg.setAttribute('aria-hidden', 'true');
  mapa.appendChild(svg); ui.body.appendChild(mapa);
  const pie = document.createElement('p'); pie.className = 'eg-pie'; ui.body.appendChild(pie);
  const existe = (a, b) => D.canales.some(([x, y]) => (x === a && y === b) || (x === b && y === a));
  const clave = (a, b) => [a, b].sort().join('');
  let cavados = new Set(), sel = null, resuelto = false;
  const Y = v => 8 + v[1] * 0.84, X = v => 8 + v[0] * 0.84;
  function pintar() {
    svg.innerHTML = '';
    cavados.forEach(k => {
      const a = D.campos[k[0]], b = D.campos[k[1]];
      const l = document.createElementNS(NS, 'line');
      l.setAttribute('x1', X(a)); l.setAttribute('y1', Y(a)); l.setAttribute('x2', X(b)); l.setAttribute('y2', Y(b));
      l.setAttribute('stroke', '#5fb3e0'); l.setAttribute('stroke-width', '3.5'); l.setAttribute('stroke-linecap', 'round');
      svg.appendChild(l);
    });
    mapa.querySelectorAll('.can-campo').forEach(b => b.classList.toggle('sel', b.dataset.k === sel));
    mapa.dataset.canales = [...cavados].sort().join(',');
    pie.textContent = 'Canales cavados: ' + cavados.size;
  }
  Object.keys(D.campos).forEach(k => {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'can-campo'; b.dataset.k = k; b.textContent = k;
    b.style.left = X(D.campos[k]) + '%'; b.style.top = Y(D.campos[k]) + '%';
    b.addEventListener('click', () => {
      if (resuelto) return;
      if (!sel) { sel = k; pintar(); return; }
      if (sel === k) { sel = null; pintar(); return; }
      if (!existe(sel, k)) { ui.say('Entre ' + sel + ' y ' + k + ' no se puede cavar un canal (mapa, carta 70).', 'bad'); sel = null; pintar(); return; }
      const c = clave(sel, k);
      cavados.has(c) ? cavados.delete(c) : cavados.add(c);
      sel = null; ui.say(''); pintar();
    });
    mapa.appendChild(b);
  });
  ui.button('Abrir las compuertas', 'primary', () => {
    if (resuelto) return;
    const padre = {}; Object.keys(D.campos).forEach(k => { padre[k] = k; });
    const raiz = x => { while (padre[x] !== x) x = padre[x]; return x; };
    cavados.forEach(c => { padre[raiz(c[0])] = raiz(c[1]); });
    if (new Set(Object.keys(D.campos).map(raiz)).size > 1) { ui.say('El agua no llega a todos los campos: alguno ha quedado aislado.', 'bad'); return; }
    const sol = new Set(D.solucion.map(e => clave(e[0], e[1])));
    if (cavados.size === sol.size && [...cavados].every(c => sol.has(c))) {
      resuelto = true; guardarSello('69');
      ui.say('El agua corre por las zanjas y llega a todos los campos sin desperdiciar ni un codo. El visir se frota las manos. Coged la carta 80.', 'ok');
    } else ui.say('Todos los campos tienen agua, pero se ha gastado más de lo necesario (mapa, carta 70; nota del visir, carta 71).', 'bad');
  });
  pintar();
  return { close: ui.close };
}

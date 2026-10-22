// Carta 14 — Las jarras del senescal: medir en el cuenco del rey justo la cantidad de hidromiel que marca el fuego, con dos jarras sin marcas.
// Cuánto cabe en cada jarra y cuánto se quiere en el cuenco, en la carta 16 (la app no pone números). Vale cualquier secuencia que lo consiga
// (instancias_trono.py, JARRAS). Cifra de la profecía: 6.
import { openGame } from './ui.js';
import { estilo } from './reino.js';

const D = /*DATOS*/{"A": 3, "B": 10, "objetivo": 5, "dato": 6}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 14 — Las jarras del senescal', instr: 'Llenad, vaciad y pasad hidromiel de una jarra a otra hasta que una de las dos tenga justo lo que marca el cuenco del rey (carta 16). Las jarras no tienen marcas.', ...opts });
  estilo('tr-jar', `.jar-pl{display:flex;gap:30px;justify-content:center;align-items:flex-end;height:210px;margin:10px 0}.jar-j{width:90px;border:3px solid #8fc7ee;border-top:0;border-radius:0 0 12px 12px;background:rgba(0,0,0,.25);position:relative;overflow:hidden}.jar-j i{position:absolute;left:0;right:0;bottom:0;background:linear-gradient(#e8a030,#b06818);transition:height .3s}.jar-botones{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;max-width:330px;margin:8px auto}.jar-botones button{padding:8px 4px;border-radius:9px;border:2px solid #8fc7ee;background:#2c3a4a;color:#e6f1fb;font:700 .75rem system-ui;cursor:pointer}.jar-cuenta{text-align:center;color:#e6f1fb;font:700 .8rem system-ui}`);
  const pl = document.createElement('div'); pl.className = 'jar-pl';
  const bs = document.createElement('div'); bs.className = 'jar-botones';
  const cu = document.createElement('div'); cu.className = 'jar-cuenta';
  ui.body.append(pl, bs, cu);
  const cap = [D.A, D.B], niv = [0, 0], dib = [];
  let movs = 0, resuelto = false;
  const maxCap = Math.max(D.A, D.B);
  [0, 1].forEach(i => {
    const j = document.createElement('div'); j.className = 'jar-j'; j.style.height = (cap[i] / maxCap * 200) + 'px'; j.dataset.j = 'AB'[i];
    const r = document.createElement('i'); j.appendChild(r); pl.appendChild(j); dib.push(r);
  });
  function pintar() {
    dib.forEach((r, i) => { r.style.height = (niv[i] / cap[i] * 100) + '%'; });
    pl.dataset.niveles = niv.join(',');
    cu.textContent = 'Movimientos: ' + movs;
  }
  const acciones = {
    'Llenar I': () => { niv[0] = cap[0]; }, 'Llenar II': () => { niv[1] = cap[1]; },
    'Vaciar I': () => { niv[0] = 0; }, 'Vaciar II': () => { niv[1] = 0; },
    'I → II': () => { const t = Math.min(niv[0], cap[1] - niv[1]); niv[0] -= t; niv[1] += t; },
    'II → I': () => { const t = Math.min(niv[1], cap[0] - niv[0]); niv[1] -= t; niv[0] += t; }
  };
  Object.keys(acciones).forEach(n => {
    const b = document.createElement('button'); b.type = 'button'; b.textContent = n; b.dataset.a = n;
    b.addEventListener('click', () => {
      if (resuelto) return;
      acciones[n](); movs++; ui.say(''); pintar();
      if (niv.includes(D.objetivo)) {
        resuelto = true;
        ui.say('Una de las jarras tiene justo lo que marca el cuenco: el senescal asiente satisfecho y abre el paso a la muralla. Cifra de la profecía: ' + D.dato + '. Coged la carta 24.', 'ok');
      }
    });
    bs.appendChild(b);
  });
  ui.button('Empezar de nuevo', 'ghost', () => { if (!resuelto) { niv[0] = niv[1] = 0; movs = 0; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}

// Carta 15 — Cuaderno del guardián: lector de páginas (no hay nada que resolver).
// No pausa el temporizador: leer también cuesta tiempo.
import { openGame } from './ui.js';

const MORSE = [
  ['A', '·−'], ['B', '−···'], ['C', '−·−·'], ['D', '−··'], ['E', '·'], ['F', '··−·'], ['G', '−−·'],
  ['H', '····'], ['I', '··'], ['J', '·−−−'], ['K', '−·−'], ['L', '·−··'], ['M', '−−'], ['N', '−·'],
  ['O', '−−−'], ['P', '·−−·'], ['Q', '−−·−'], ['R', '·−·'], ['S', '···'], ['T', '−'], ['U', '··−'],
  ['V', '···−'], ['W', '·−−'], ['X', '−··−'], ['Y', '−·−−'], ['Z', '−−··']
];

const PAGINAS = [
  {
    titulo: 'Para entenderme con los barcos',
    tabla: MORSE,
    pie: 'Punto = destello corto. Raya = destello largo. Mi abuelo me enseñó esto con una linterna y un cobertizo a oscuras.'
  },
  {
    titulo: 'Avisos para mí mismo',
    texto: [
      'El reloj del recibidor atrasa 1 hora y 20 minutos desde la última tormenta. Nunca lo arreglé: sé la hora de memoria.',
      'La llave de máquinas está donde nadie la buscaría: con lo que sujeta a los barcos.',
      'La frecuencia de la radio del faro la tengo apuntada en el mapa, en el cuarto de máquinas.',
      'No dejar el termo cerca de la lente. Otra vez.'
    ]
  },
  {
    titulo: 'Arranque de la lámpara',
    texto: [
      'Cinco cosas, y el orden importa. Si las hago mal, la lente se atasca y vuelta a empezar.',
      'Lo primero, siempre, el aceite.',
      'La mecha se ceba antes de girar nada.',
      'El piloto se enciende justo después del engranaje.',
      'El freno de la lente se suelta el último. Siempre el último.'
    ]
  },
  {
    titulo: 'Diario · última entrada',
    texto: [
      'Esta noche el parte da tormenta fuerte. Pondré la lámpara a punto antes de que anochezca.',
      'Si Inés viene a verme, que mire en la despensa: he guardado esas galletas de las que tanto presume.',
      'Voy un momento a por el termo... vuelvo enseguida.'
    ]
  }
];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 15 — Cuaderno del guardián',
    instr: 'Pasa las páginas con calma. Aquí hay cosas que os harán falta.',
    onClose: opts.onClose
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-hoja{background:#efe3c4;color:#2a2012;border-radius:8px;padding:16px 16px 14px;text-align:left;font-family:Georgia,"Times New Roman",serif;min-height:260px;box-shadow:inset 0 0 22px rgba(90,60,20,.25)}
    .far-hoja h4{margin:0 0 10px;font-size:1.05rem;font-style:italic;border-bottom:1px solid rgba(42,32,18,.35);padding-bottom:6px}
    .far-hoja p{margin:0 0 10px;font-size:.95rem;line-height:1.45}
    .far-hoja .pie{font-size:.82rem;font-style:italic;opacity:.85;margin-top:10px}
    .far-morse{display:grid;grid-template-columns:repeat(3,1fr);gap:4px 12px;font-family:"IBM Plex Mono",ui-monospace,Consolas,monospace;font-size:.95rem}
    .far-morse span b{display:inline-block;width:1.4em}
    .far-pag{margin-top:10px;color:#93a4b5;font-size:.85rem}
  `;
  ui.body.appendChild(style);

  const hoja = document.createElement('div');
  hoja.className = 'far-hoja';
  const pag = document.createElement('div');
  pag.className = 'far-pag';
  ui.body.append(hoja, pag);

  let i = 0;
  function pintar() {
    const p = PAGINAS[i];
    hoja.innerHTML = '';
    const h = document.createElement('h4');
    h.textContent = p.titulo;
    hoja.appendChild(h);
    if (p.tabla) {
      const t = document.createElement('div');
      t.className = 'far-morse';
      p.tabla.forEach(([l, c]) => {
        const s = document.createElement('span');
        const b = document.createElement('b');
        b.textContent = l;
        s.append(b, c);
        t.appendChild(s);
      });
      hoja.appendChild(t);
    }
    (p.texto || []).forEach(linea => {
      const el = document.createElement('p');
      el.textContent = linea;
      hoja.appendChild(el);
    });
    if (p.pie) {
      const el = document.createElement('p');
      el.className = 'pie';
      el.textContent = p.pie;
      hoja.appendChild(el);
    }
    pag.textContent = 'Página ' + (i + 1) + ' de ' + PAGINAS.length;
    ant.disabled = i === 0;
    sig.disabled = i === PAGINAS.length - 1;
  }

  const ant = ui.button('← Anterior', 'ghost', () => { if (i > 0) { i--; pintar(); } });
  const sig = ui.button('Siguiente →', 'primary', () => { if (i < PAGINAS.length - 1) { i++; pintar(); } });

  function onKey(e) {
    if (e.key === 'ArrowLeft') ant.click();
    if (e.key === 'ArrowRight') sig.click();
  }
  document.addEventListener('keydown', onKey);
  ui.onClose(() => document.removeEventListener('keydown', onKey));

  pintar();
  return { close: ui.close };
}

// Carta 48 — La marioneta: tirar de los mandos de la cruceta para que Pipo haga la postura del cartel (carta 53); qué mando mueve cada
// mano y cada pie se ve siguiendo los hilos enredados (carta 52). Datos de herramientas/instancias_juguetes.py.
import { openGame } from './ui.js';

const M = /*DATOS*/{"mandos": ["rojo", "azul", "amarillo", "verde"], "miembros": ["brazo_izq", "brazo_der", "pierna_izq", "pierna_der"], "hilos": {"rojo": "pierna_der", "azul": "brazo_izq", "amarillo": "brazo_der", "verde": "pierna_izq"}, "postura": ["brazo_der", "pierna_izq"]}/*FIN*/;
const FORMA = { rojo: 'circle(50%)', azul: 'inset(6% round 4px)', amarillo: 'polygon(50% 4%,96% 92%,4% 92%)',
  verde: 'polygon(50% 0%,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%)' };
const COLOR = { rojo: '#d63430', azul: '#2c68c4', amarillo: '#f6c42a', verde: '#3aa054' };
const NOMBRE = { rojo: 'rojo con círculo', azul: 'azul con cuadrado', amarillo: 'amarillo con triángulo', verde: 'verde con estrella' };

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 48 — La marioneta',
    instr: 'Toca un mando de la cruceta para tirar de su hilo (otra vez para soltarlo). Dejad a Pipo como en el cartel de la función y pulsad «¡Saluda!».',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .jug-cruceta{display:flex;justify-content:space-around;align-items:center;width:min(84vw,300px);margin:4px auto 0;padding:10px 6px;border-radius:8px;background:linear-gradient(180deg,#c48c56,#8a5c30);border:3px solid #4a2e18}
    .jug-mando{width:52px;height:52px;border:0;padding:0;cursor:pointer;transition:transform .15s}
    .jug-mando.tira{transform:translateY(-8px) scale(1.1);filter:drop-shadow(0 0 8px #fff)}
    .jug-teatro{width:min(70vw,230px);aspect-ratio:240 / 320;margin:0 auto 6px;border-radius:0 0 10px 10px;border:4px solid #8a1a2a;border-top:0;
      background:#3a2450 center / contain no-repeat}
    .jug-teatro.ok{box-shadow:0 0 24px rgba(255,204,51,.7)}
  `;
  ui.body.appendChild(style);

  const cruceta = document.createElement('div');
  cruceta.className = 'jug-cruceta';
  const teatro = document.createElement('div');
  teatro.className = 'jug-teatro';
  ui.body.appendChild(cruceta);
  ui.body.appendChild(teatro);

  const tirando = new Set();
  let resuelto = false;

  function arriba() { return M.mandos.filter(m => tirando.has(m)).map(m => M.hilos[m]); }
  function pintar() {
    const ar = arriba();
    const bits = M.miembros.reduce((s, x, i) => s + (ar.includes(x) ? 1 << i : 0), 0);
    teatro.style.backgroundImage = "url('./img/ui/pipo-" + bits + ".png')";
    teatro.dataset.arriba = ar.slice().sort().join(',');
    cruceta.querySelectorAll('.jug-mando').forEach(b => b.classList.toggle('tira', tirando.has(b.dataset.m)));
  }

  M.mandos.forEach(m => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'jug-mando';
    b.dataset.m = m;
    b.style.background = COLOR[m];
    b.style.clipPath = FORMA[m];
    b.setAttribute('aria-label', 'Mando ' + NOMBRE[m]);
    b.addEventListener('click', () => {
      if (resuelto) return;
      tirando.has(m) ? tirando.delete(m) : tirando.add(m);
      ui.say('');
      pintar();
    });
    cruceta.appendChild(b);
  });

  ui.button('¡Saluda!', 'primary', () => {
    if (resuelto) return;
    const ar = arriba().sort().join(','), pide = M.postura.slice().sort().join(',');
    if (ar === pide) {
      resuelto = true;
      teatro.classList.add('ok');
      ui.say('¡Pipo saluda igual que en el cartel! Los juguetes aplauden y, con un clic, se abre el cajón del teatrillo. Coged la carta 58.', 'ok');
    } else {
      ui.say('Pipo no está como en el cartel (carta 53). Seguid los hilos (carta 52) para ver qué mando mueve cada mano y cada pie.', 'bad');
    }
  });
  ui.button('Soltar todo', '', () => { if (!resuelto) { tirando.clear(); ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}

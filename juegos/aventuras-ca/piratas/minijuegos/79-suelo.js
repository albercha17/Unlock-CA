// Carta 79 — El suelo de la cueva: cruzar de abajo arriba pisando losas vecinas que siguen, una y otra vez, los cuatro símbolos del
// testamento plegado (carta 76). Instancia de herramientas/instancias_piratas.py: hay un único camino.
import { openGame } from './ui.js';

const S = /*DATOS*/{"n": 5, "ciclo": ["luna", "llave", "calavera", "corona"], "suelo": [["calavera", "calavera", "campana", "corona", "ancla"], ["luna", "llave", "llave", "campana", "calavera"], ["corona", "calavera", "espada", "estrella", "espada"], ["luna", "llave", "ancla", "llave", "ancla"], ["corona", "calavera", "llave", "luna", "calavera"]]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 79 — El suelo de la cueva',
    instr: 'Entrad por abajo y cruzad hasta la fila de arriba pisando solo losas vecinas (arriba, abajo o a los lados), con los símbolos del testamento en su orden, una y otra vez. Una pisada en falso y la losa se hunde.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .pir-fondo{text-align:center;font:700 .75rem system-ui,sans-serif;letter-spacing:.2em;color:#e8b84a;margin:0}
    .pir-suelo{display:grid;grid-template-columns:repeat(${S.n},1fr);gap:5px;width:min(80vw,290px);margin:4px auto}
    .pir-losa{position:relative;aspect-ratio:1;border-radius:5px;border:2px solid #1a1410;padding:5px;cursor:pointer;
      background:radial-gradient(circle at 30% 25%,#8a8274,#5a544a 60%,#3a352e);box-shadow:inset 0 2px 0 rgba(255,255,255,.18),0 4px 0 #1a1612}
    .pir-losa img{width:100%;height:100%;object-fit:contain;mix-blend-mode:screen;opacity:.8;pointer-events:none}
    .pir-losa.pisada{transform:translateY(3px);box-shadow:0 1px 0 #1a1612;background:radial-gradient(circle at 30% 25%,#9a8a5a,#6a5a30 60%,#3a3018)}
    .pir-losa.aqui{outline:3px solid #ffd27a;outline-offset:-3px}
    .pir-losa.hunde{animation:pir-hunde .5s}
    @keyframes pir-hunde{50%{transform:translateY(10px) scale(.92);filter:brightness(.4)}}
    @media (prefers-reduced-motion:reduce){.pir-losa.hunde{animation:none}}
  `;
  ui.body.appendChild(style);

  const fondo = document.createElement('p');
  fondo.className = 'pir-fondo';
  fondo.textContent = 'FONDO DE LA CUEVA';
  const suelo = document.createElement('div');
  suelo.className = 'pir-suelo';
  const entrada = document.createElement('p');
  entrada.className = 'pir-fondo';
  entrada.textContent = 'ENTRADA';
  ui.body.appendChild(fondo);
  ui.body.appendChild(suelo);
  ui.body.appendChild(entrada);

  let camino = [], resuelto = false;

  function pintar() {
    const ultimo = camino[camino.length - 1];
    suelo.querySelectorAll('.pir-losa').forEach(b => {
      const x = Number(b.dataset.x), y = Number(b.dataset.y);
      b.classList.toggle('pisada', camino.some(c => c[0] === x && c[1] === y));
      b.classList.toggle('aqui', !!ultimo && ultimo[0] === x && ultimo[1] === y);
    });
  }

  function pisar(x, y, b) {
    if (resuelto) return;
    const ultimo = camino[camino.length - 1];
    if (camino.some(c => c[0] === x && c[1] === y)) return;
    const vecina = ultimo ? Math.abs(ultimo[0] - x) + Math.abs(ultimo[1] - y) === 1 : y === S.n - 1;
    if (!vecina) {
      ui.say(ultimo ? 'Solo se puede pisar una losa vecina: arriba, abajo o a un lado de donde estáis.' : 'Se entra por la fila de abajo.', 'bad');
      return;
    }
    if (S.suelo[y][x] !== S.ciclo[camino.length % S.ciclo.length]) {
      camino = [];
      b.classList.remove('hunde');
      void b.offsetWidth;
      b.classList.add('hunde');
      pintar();
      ui.say('¡La losa se hunde y volvéis a la entrada de un salto! No tocaba ese símbolo. El orden está en el testamento (carta 76)... ¿lo habéis plegado?', 'bad');
      return;
    }
    camino.push([x, y]);
    pintar();
    if (y === 0) {
      resuelto = true;
      ui.say('Llegáis al fondo sin hundir ni una losa. La pared de roca se abre con un ruido sordo: un pasadizo baja hacia la oscuridad. Coged la carta 80.', 'ok');
    } else {
      ui.say('');
    }
  }

  for (let y = 0; y < S.n; y++) {
    for (let x = 0; x < S.n; x++) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'pir-losa';
      b.dataset.x = String(x);
      b.dataset.y = String(y);
      b.dataset.s = S.suelo[y][x];
      b.setAttribute('aria-label', 'Losa con ' + S.suelo[y][x] + ', fila ' + (S.n - y) + ', columna ' + (x + 1));
      b.innerHTML = '<img src="./img/ui/sim-' + S.suelo[y][x] + '.png" alt="">';
      b.addEventListener('click', () => pisar(x, y, b));
      suelo.appendChild(b);
    }
  }
  ui.button('Volver a la entrada', '', () => { if (!resuelto) { camino = []; ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}

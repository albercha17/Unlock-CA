// Carta 69 — El desactivador: cuatro cargas con cinco cables cada una; hay que cortar un cable de cada carga según las reglas del manual (carta 70).
// Reglas (en orden, vale la primera que se cumpla; los cables se cuentan de arriba abajo):
//   1. Más cables azules que rojos: cortar el último azul.   2. Sin rojos y con el último amarillo: cortar el primero.
//   3. Exactamente un cable blanco: cortar el cuarto.        4. Si no: cortar el último negro (si no hay negros, el segundo).
import { openGame } from './ui.js';

const CARGAS = [
  ['rojo', 'azul', 'azul', 'negro', 'blanco'],
  ['rojo', 'amarillo', 'blanco', 'rojo', 'negro'],
  ['negro', 'blanco', 'negro', 'blanco', 'amarillo'],
  ['amarillo', 'rojo', 'negro', 'blanco', 'blanco']
];
const COLOR = { rojo: '#d63a3a', azul: '#2e6fd6', amarillo: '#e8c42a', blanco: '#f2f2ee', negro: '#1c1c20' };
const TEXTO = { rojo: '#fff', azul: '#fff', amarillo: '#2a2200', blanco: '#222', negro: '#fff' };

function cableCorrecto(cables) {
  const rojos = cables.filter(x => x === 'rojo').length;
  const azules = cables.filter(x => x === 'azul').length;
  if (azules > rojos) return cables.lastIndexOf('azul');
  if (rojos === 0 && cables[cables.length - 1] === 'amarillo') return 0;
  if (cables.filter(x => x === 'blanco').length === 1) return 3;
  const n = cables.lastIndexOf('negro');
  return n >= 0 ? n : 1;
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 69 — El desactivador',
    instr: 'Corta un cable de cada carga, el que diga el manual del desactivador. Si te equivocas, la carga se reinicia.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .esp-carga{margin:6px 0 10px;padding:10px;border-radius:10px;border:2px solid #7fe8f0;background:linear-gradient(180deg,#14242c,#0a1218)}
    .esp-carga h4{margin:0 0 8px;font:700 .9rem system-ui,sans-serif;color:#7fe8f0;display:flex;justify-content:space-between}
    .esp-cables{display:flex;flex-direction:column;gap:6px}
    .esp-cable{height:34px;border-radius:17px;border:2px solid #000;font:700 .8rem system-ui,sans-serif;cursor:pointer;text-align:left;padding:0 16px;box-shadow:0 2px 0 rgba(0,0,0,.6)}
    .esp-cable:disabled{opacity:.35;cursor:default}
    .esp-cable.cortado{opacity:.35;text-decoration:line-through}
    .esp-cable.rojo{background:repeating-linear-gradient(90deg,#d63a3a 0 14px,#b02828 14px 18px)}
    .esp-cable.azul{background:#2e6fd6}
    .esp-cable.amarillo{background:repeating-linear-gradient(45deg,#e8c42a 0 8px,#b89a1a 8px 12px)}
    .esp-cable.blanco{background:linear-gradient(180deg,#f8f8f4,#d8d8d0)}
    .esp-cable.negro{background:repeating-linear-gradient(90deg,#1c1c20 0 6px,#3a3a42 6px 9px)}
  `;
  ui.body.appendChild(style);

  const panel = document.createElement('div');
  ui.body.appendChild(panel);

  let ronda = 0;
  let resuelto = false;

  function pintar() {
    panel.innerHTML = '';
    CARGAS.forEach((cables, r) => {
      if (r > ronda) return;
      const d = document.createElement('div');
      d.className = 'esp-carga';
      d.dataset.r = String(r);
      d.innerHTML = '<h4><span>Carga ' + (r + 1) + ' de ' + CARGAS.length + '</span><span>' + (r < ronda || resuelto ? 'desactivada' : 'activa') + '</span></h4>';
      const lista = document.createElement('div');
      lista.className = 'esp-cables';
      cables.forEach((col, i) => {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'esp-cable ' + col + (r < ronda || resuelto ? ' cortado' : '');
        b.dataset.c = col;
        b.dataset.i = String(i);
        b.style.color = TEXTO[col];
        b.textContent = (i + 1) + '. Cable ' + col;
        b.setAttribute('aria-label', 'Carga ' + (r + 1) + ', cable ' + (i + 1) + ': ' + col);
        b.disabled = r < ronda || resuelto;
        b.addEventListener('click', () => cortar(r, i));
        lista.appendChild(b);
      });
      d.appendChild(lista);
      panel.appendChild(d);
    });
  }

  function cortar(r, i) {
    if (resuelto || r !== ronda) return;
    if (i === cableCorrecto(CARGAS[r])) {
      ronda++;
      if (ronda === CARGAS.length) {
        resuelto = true;
        pintar();
        ui.say('Clic. El reloj del maletín se detiene en el último segundo: las cuatro cargas están desactivadas. Al fondo de la sala se abre un panel secreto. Coged la carta 82.', 'ok');
        return;
      }
      pintar();
      ui.say('Clic. Carga desactivada. Pasad a la siguiente.', '');
    } else {
      pintar();
      ui.say('La carga parpadea en rojo: ese no era el cable. Se reinicia esta carga; releed el manual del desactivador (carta 70), comprobando las reglas por orden.', 'bad');
    }
  }

  pintar();
  return { close: ui.close };
}

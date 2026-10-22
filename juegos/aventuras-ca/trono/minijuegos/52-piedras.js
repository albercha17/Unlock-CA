// Carta 52 — El juego de las piedras (Nim): hay que ganar al carcelero. Se parte de 21 piedras, se toman 1, 2 o 3 por turno y quien se lleva la última gana.
// Empieza el retador. Las reglas, en la carta 54; las partidas de otros retadores, en la 55; el dicho del carcelero, en la 59. El carcelero juega
// bien siempre que puede (instancias_trono.py, PIEDRAS). Cifra de la profecía: 3.
import { openGame } from './ui.js';
import { estilo } from './reino.js';

const D = /*DATOS*/{"piedras": 21, "dato": 3}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 52 — El juego de las piedras', instr: 'Jugáis contra el carcelero. Hay ' + D.piedras + ' piedras; cada uno toma 1, 2 o 3 por turno y gana quien se lleva la última. Empezáis vosotros. Reglas y partidas anteriores, en las cartas 54, 55 y 59.', ...opts });
  estilo('tr-pie', `.pie-mesa{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;max-width:320px;margin:12px auto}.pie-p{width:34px;height:24px;border-radius:50%;background:#8a96a2;border:2px solid #0c121a}.pie-p.fuera{opacity:.12}.pie-bot{display:flex;gap:10px;justify-content:center;margin:8px 0}.pie-bot button{width:64px;height:48px;border-radius:12px;border:2px solid #8fc7ee;background:#2c3a4a;color:#e6f1fb;font:800 1.3rem Georgia,serif;cursor:pointer}.pie-log{text-align:center;color:#e6f1fb;font:600 .8rem system-ui;min-height:2.4em;margin:6px 0}`);
  const mesa = document.createElement('div'); mesa.className = 'pie-mesa';
  const bot = document.createElement('div'); bot.className = 'pie-bot';
  const log = document.createElement('div'); log.className = 'pie-log';
  ui.body.append(mesa, bot, log);
  let quedan = D.piedras, resuelto = false, bloqueado = false;
  const piedras = [];
  for (let i = 0; i < D.piedras; i++) { const p = document.createElement('div'); p.className = 'pie-p'; mesa.appendChild(p); piedras.push(p); }
  function pintar() {
    piedras.forEach((p, i) => p.classList.toggle('fuera', i >= quedan));
    mesa.dataset.quedan = String(quedan);
  }
  function reiniciar() { quedan = D.piedras; log.textContent = ''; bloqueado = false; pintar(); }
  function rey() {
    const t = quedan % 4 === 0 ? 1 : quedan % 4;
    const toma = Math.min(t, quedan);
    quedan -= toma;
    log.textContent += ' El carcelero toma ' + toma + '.';
    pintar();
    if (quedan === 0) {
      ui.say('El carcelero se lleva la última piedra: habéis perdido esta partida. Probad otra vez y pensad con qué cuenta se gana.', 'bad');
      bloqueado = true;
      setTimeout(() => { if (!resuelto) reiniciar(); }, 500);
    }
  }
  [1, 2, 3].forEach(n => {
    const b = document.createElement('button'); b.type = 'button'; b.dataset.n = String(n); b.textContent = String(n); b.setAttribute('aria-label', 'Tomar ' + n);
    b.addEventListener('click', () => {
      if (resuelto || bloqueado || n > quedan) return;
      ui.say(''); log.textContent = 'Tomáis ' + n + '.';
      quedan -= n; pintar();
      if (quedan === 0) {
        resuelto = true;
        ui.say('¡Os lleváis la última piedra! El carcelero se rasca la cabeza y abre la puerta del fondo. Cifra de la profecía: ' + D.dato + '. Coged la carta 44.', 'ok');
        return;
      }
      rey();
    });
    bot.appendChild(b);
  });
  ui.button('Empezar de nuevo', 'ghost', () => { if (!resuelto) { ui.say(''); reiniciar(); } });
  pintar();
  return { close: ui.close };
}

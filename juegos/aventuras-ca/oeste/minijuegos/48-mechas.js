// Carta 48 — Las mechas: dos mechas que tardan una hora en consumirse (a ritmo irregular); hay que dar la señal a los minutos que marca el reloj del capataz (carta 52).
// Solución: 45 minutos. Mecha A por los dos extremos y mecha B por uno; cuando se apaga la A (a los 30), se enciende el otro extremo de la B; se apaga a los 45.
import { openGame } from './ui.js';

const META = 45;
const TOTAL = 60;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 48 — Las mechas',
    instr: 'Enciende los extremos de las mechas y espera a que se apague una. Da la señal a la hora exacta del reloj del capataz.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .oes-mechas{display:flex;flex-direction:column;gap:12px;margin:6px 0 10px}
    .oes-mecha{padding:10px;border-radius:10px;border:2px solid #b8742a;background:linear-gradient(180deg,#4a2c14,#2a180a)}
    .oes-mecha h4{margin:0 0 8px;font:700 .9rem Georgia,serif;color:#f5d48a}
    .oes-cuerda{height:16px;border-radius:8px;background:#1a0e06;overflow:hidden;border:1px solid #6a4020}
    .oes-cuerda b{display:block;height:100%;background:repeating-linear-gradient(90deg,#d4a050 0 8px,#b0803a 8px 16px)}
    .oes-extremos{display:flex;gap:8px;margin-top:8px}
    .oes-extremo{flex:1;padding:8px 4px;border-radius:8px;border:2px solid #f0b860;background:linear-gradient(180deg,#c88a3a,#7a4a1a);color:#fff2d6;font:700 .8rem system-ui,sans-serif;cursor:pointer;box-shadow:0 3px 0 #2a1608}
    .oes-extremo.encendido{background:linear-gradient(180deg,#ff9a3a,#d8541e);border-color:#fff}
    .oes-extremo:disabled{opacity:.45;cursor:default}
    .oes-reloj{text-align:center;font:800 1.5rem Georgia,serif;color:#fff2d6;margin:2px 0 6px}
  `;
  ui.body.appendChild(style);

  const reloj = document.createElement('div');
  reloj.className = 'oes-reloj';
  const mechas = document.createElement('div');
  mechas.className = 'oes-mechas';
  ui.body.appendChild(reloj);
  ui.body.appendChild(mechas);

  let t, m;
  let resuelto = false;
  function reiniciar() { t = 0; m = { A: { r: TOTAL, e: [false, false] }, B: { r: TOTAL, e: [false, false] } }; }

  function encendidos(f) { return f.e.filter(Boolean).length; }
  function apagada(f) { return f.r <= 1e-9; }

  function pintar() {
    reloj.dataset.t = String(t);
    reloj.textContent = 'Minutos: ' + t;
    mechas.innerHTML = '';
    ['A', 'B'].forEach(k => {
      const f = m[k];
      const d = document.createElement('div');
      d.className = 'oes-mecha';
      d.dataset.m = k;
      d.innerHTML = '<h4>Mecha ' + k + (apagada(f) ? ' (apagada)' : '') + '</h4><div class="oes-cuerda"><b style="width:' + Math.max(0, f.r / TOTAL * 100) + '%"></b></div><div class="oes-extremos"></div>';
      const ex = d.querySelector('.oes-extremos');
      [0, 1].forEach(e => {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'oes-extremo' + (f.e[e] ? ' encendido' : '');
        b.dataset.m = k;
        b.dataset.e = String(e + 1);
        b.textContent = f.e[e] ? 'Extremo ' + (e + 1) + ' encendido' : 'Encender extremo ' + (e + 1);
        b.setAttribute('aria-label', 'Mecha ' + k + ', extremo ' + (e + 1) + (f.e[e] ? ' (encendido)' : ''));
        b.disabled = resuelto || f.e[e] || apagada(f);
        b.addEventListener('click', () => { f.e[e] = true; ui.say(''); pintar(); });
        ex.appendChild(b);
      });
      mechas.appendChild(d);
    });
  }

  function esperar() {
    if (resuelto) return;
    let dt = Infinity;
    ['A', 'B'].forEach(k => { const f = m[k]; if (!apagada(f) && encendidos(f) > 0) dt = Math.min(dt, f.r / encendidos(f)); });
    if (dt === Infinity) { ui.say('No hay ninguna mecha encendida: enciende algún extremo antes de esperar.', 'bad'); return; }
    ['A', 'B'].forEach(k => {
      const f = m[k];
      if (!apagada(f) && encendidos(f) > 0) {
        f.r = Math.max(0, f.r - encendidos(f) * dt);
        if (apagada(f)) f.e = [false, false];
      }
    });
    t = Math.round((t + dt) * 1e6) / 1e6;
    pintar();
    ui.say('Se ha apagado una mecha. Han pasado ' + t + ' minutos desde el principio.', '');
  }

  function señal() {
    if (resuelto) return;
    if (Math.abs(t - META) < 1e-6) {
      resuelto = true;
      pintar();
      ui.say('¡BUUUM! La dinamita salta justo a la hora del reloj del capataz: el derrumbe cae hacia fuera y el túnel queda libre. Coged la carta 58.', 'ok');
    } else {
      reiniciar();
      pintar();
      ui.say('La señal ha sonado a los ' + (Math.round(t) === t ? t : t.toFixed(1)) + ' minutos y no a la hora del reloj del capataz. Se han consumido las mechas: empezad de nuevo. Una mecha encendida por los dos extremos tarda la mitad.', 'bad');
    }
  }

  ui.button('Esperar hasta que se apague una mecha', 'primary', esperar);
  ui.button('Dar la señal', '', señal);
  ui.button('Reiniciar', '', () => { if (!resuelto) { reiniciar(); pintar(); ui.say(''); } });

  reiniciar();
  pintar();
  return { close: ui.close };
}

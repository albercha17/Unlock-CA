// Prototipo de puzle con el MICRÓFONO: «La niebla del faro». Primero hay que mantener el silencio 6 segundos (la niebla se asienta) y luego soplar
// 1,2 segundos hacia el móvil para despejarla. Si el micrófono no está disponible, hay una versión táctil (mantener pulsado y pulsar 12 veces).
import { openGame } from './ui.js';
import { estilo } from './comun.js';
import { SIM, abrirMicro, botonesSim } from './sensores.js';

const SEG_SILENCIO = 6;
const SEG_SOPLO = 1.2;
const TOQUES = 12;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Prueba — La niebla del faro',
    instr: 'Una niebla espesa cubre la lámpara. Pulsad «Activar micrófono», quedaos en silencio 6 segundos y, cuando la niebla se asiente, soplad hacia el móvil para despejarla.',
    ...opts
  });
  estilo('fa-sil', '.sil-m{height:16px;border-radius:8px;background:rgba(0,0,0,.4);border:1px solid rgba(255,255,255,.25);overflow:hidden;margin:6px 0}.sil-m i{display:block;height:100%;width:0;background:linear-gradient(90deg,#7be495,#ffd27a,#ff7a6a);transition:width .08s}.sil-p i{background:linear-gradient(90deg,#4ab0ff,#cfe8ff)}.sil-e{min-height:2.6em;text-align:center;color:#cfe3ee;font:600 .95rem system-ui,sans-serif;margin:8px 0}.sil-b{display:block;width:100%;margin:8px 0;padding:18px 0;border-radius:12px;border:2px solid #c9a45a;background:rgba(255,255,255,.1);color:#fff;font:800 1.05rem system-ui,sans-serif;touch-action:none}.sil-b.sel{background:#c9a45a;color:#10202c}');

  const estado = document.createElement('div');
  estado.className = 'sil-e';
  const medidor = document.createElement('div');
  medidor.className = 'sil-m';
  medidor.innerHTML = '<i></i>';
  const progreso = document.createElement('div');
  progreso.className = 'sil-m sil-p';
  progreso.innerHTML = '<i></i>';
  const area = document.createElement('div');
  ui.body.append(estado, medidor, progreso, area);

  let micro = null, modo = 'espera', fase = 'calibrar', t = 0, amb = 0, nCal = 0, umbSil = 0.03, umbSoplo = 0.2, hecho = false, pulsado = false, toques = 0, reloj = null;
  let sim = 0.002;                         // volumen simulado (?sim=1)
  const nivel = () => (SIM && modo === 'sim' ? sim : micro ? micro.nivel() : 0);

  function pintar(n) {
    medidor.firstChild.style.width = Math.min(100, Math.round(n * 300)) + '%';
    const total = fase === 'silencio' ? SEG_SILENCIO : fase === 'soplo' ? (modo === 'tactil' ? TOQUES : SEG_SOPLO) : 1;
    const v = fase === 'calibrar' ? 0 : fase === 'soplo' && modo === 'tactil' ? toques : t;
    progreso.firstChild.style.width = Math.min(100, Math.round(v / total * 100)) + '%';
  }

  function terminar() {
    hecho = true;
    clearInterval(reloj);
    if (micro) micro.parar();
    estado.textContent = '';
    ui.say('¡La niebla se despeja y la lámpara brilla! (Prototipo del puzle con micrófono superado.)', 'ok');
  }

  function paso() {
    if (hecho) return;
    const n = nivel();
    if (modo === 'tactil') {
      if (fase === 'calibrar') { fase = 'silencio'; t = 0; }
      if (fase === 'silencio') {
        t = pulsado ? t + 0.1 : 0;
        estado.textContent = pulsado ? 'Mantened pulsado sin soltar… ' + Math.max(0, SEG_SILENCIO - t).toFixed(1) + ' s' : 'Mantened pulsado el botón de abajo ' + SEG_SILENCIO + ' segundos.';
        if (t >= SEG_SILENCIO) { fase = 'soplo'; t = 0; toques = 0; renderTactil(); }
      } else if (fase === 'soplo') {
        estado.textContent = 'Soplad pulsando el botón ' + TOQUES + ' veces (' + toques + ').';
        if (toques >= TOQUES) terminar();
      }
      pintar(0);
      return;
    }
    if (fase === 'calibrar') {
      amb += n;
      nCal++;
      estado.textContent = 'Midiendo el ruido de la sala… no habléis todavía.';
      if (nCal >= 12) {
        amb /= nCal;
        umbSil = Math.max(0.02, amb * 1.8 + 0.015);
        umbSoplo = Math.max(0.2, amb + 0.12);
        fase = 'silencio';
        t = 0;
      }
    } else if (fase === 'silencio') {
      if (n < umbSil) {
        t += 0.1;
        estado.textContent = 'Silencio… ' + Math.max(0, SEG_SILENCIO - t).toFixed(1) + ' s';
      } else {
        t = 0;
        estado.textContent = '¡Shhh! Se oyó algo: la niebla se remueve. Empezad de nuevo.';
      }
      if (t >= SEG_SILENCIO) { fase = 'soplo'; t = 0; }
    } else if (fase === 'soplo') {
      estado.textContent = 'La niebla se ha asentado. ¡Soplad hacia el móvil!';
      if (n > umbSoplo) t += 0.1; else t = Math.max(0, t - 0.05);
      if (t >= SEG_SOPLO) terminar();
    }
    pintar(n);
  }

  function arrancar() {
    fase = 'calibrar';
    t = 0; amb = 0; nCal = 0;
    clearInterval(reloj);
    reloj = setInterval(paso, 100);
  }

  function renderTactil() {
    area.innerHTML = '';
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'sil-b';
    b.dataset.tactil = fase;
    b.textContent = fase === 'silencio' ? 'Mantener pulsado' : 'Soplar (pulsar)';
    if (fase === 'silencio') {
      const dentro = () => { pulsado = true; b.classList.add('sel'); };
      const fuera = () => { pulsado = false; b.classList.remove('sel'); };
      b.addEventListener('pointerdown', dentro);
      b.addEventListener('pointerup', fuera);
      b.addEventListener('pointercancel', fuera);
      b.addEventListener('pointerleave', fuera);
    } else {
      b.addEventListener('click', () => { toques++; });
    }
    area.appendChild(b);
  }

  ui.onClose(() => { clearInterval(reloj); if (micro) micro.parar(); });

  const activar = ui.button('Activar micrófono', 'primary', async () => {
    if (modo !== 'espera') return;
    try {
      micro = await abrirMicro();
      modo = 'micro';
      activar.disabled = true;
      ui.say('');
      arrancar();
    } catch (e) {
      ui.say('No se pudo usar el micrófono: ' + (e && e.message ? e.message : 'permiso denegado') + ' Usad la versión táctil.', 'bad');
    }
  });
  ui.button('No puedo usar el micrófono', 'ghost', () => {
    if (hecho) return;
    modo = 'tactil';
    activar.disabled = true;
    if (micro) { micro.parar(); micro = null; }
    ui.say('');
    arrancar();
    fase = 'silencio';
    t = 0;
    renderTactil();
  });
  botonesSim(ui, [
    ['Simular sala', () => { if (modo === 'espera') { modo = 'sim'; activar.disabled = true; arrancar(); } }, 'sala'],
    ['Silencio', () => { sim = 0.002; }, 'silencio'],
    ['Ruido', () => { sim = 0.08; }, 'ruido'],
    ['Soplo', () => { sim = 0.5; }, 'soplo']
  ]);
  pintar(0);
  return { close: ui.close };
}

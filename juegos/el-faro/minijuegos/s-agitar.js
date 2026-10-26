// Prototipo de puzle con el ACELERÓMETRO: «El generador». Agitar el móvil carga una barra; si se agita demasiado fuerte salta el fusible y hay que
// empezar de nuevo. Hay que mantener la carga dentro de la franja verde durante 3 segundos. Versión táctil de respaldo: pulsar el botón al ritmo justo.
import { openGame } from './ui.js';
import { estilo } from './comun.js';
import { SIM, abrirMovimiento, botonesSim } from './sensores.js';

const ZONA = [55, 75];
const SEG_ZONA = 3;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Prueba — El generador',
    instr: 'Pulsad «Activar movimiento» y agitad el móvil con fuerza media y constante. Mantened la barra en la franja verde 3 segundos: si agitáis demasiado fuerte, salta el fusible.',
    ...opts
  });
  estilo('fa-agi', '.agi-b{position:relative;height:30px;border-radius:8px;background:rgba(0,0,0,.4);border:1px solid rgba(255,255,255,.25);overflow:hidden;margin:10px 0}.agi-b i{position:absolute;left:0;top:0;bottom:0;width:0;background:linear-gradient(90deg,#4ab0ff,#ffd27a);transition:width .08s}.agi-b u{position:absolute;top:0;bottom:0;background:rgba(123,228,149,.35);border-left:2px solid #7be495;border-right:2px solid #7be495}.agi-m{height:16px;border-radius:8px;background:rgba(0,0,0,.4);border:1px solid rgba(255,255,255,.25);overflow:hidden;margin:6px 0}.agi-m i{display:block;height:100%;width:0;background:linear-gradient(90deg,#4ab0ff,#cfe8ff);transition:width .08s}.agi-e{min-height:2.6em;text-align:center;color:#cfe3ee;font:600 .95rem system-ui,sans-serif;margin:8px 0}.agi-t{display:block;width:100%;padding:18px 0;border-radius:12px;border:2px solid #c9a45a;background:rgba(255,255,255,.1);color:#fff;font:800 1.05rem system-ui,sans-serif}');

  const estado = document.createElement('div');
  estado.className = 'agi-e';
  const barra = document.createElement('div');
  barra.className = 'agi-b';
  barra.innerHTML = '<u style="left:' + ZONA[0] + '%;width:' + (ZONA[1] - ZONA[0]) + '%"></u><i></i>';
  const mantener = document.createElement('div');
  mantener.className = 'agi-m';
  mantener.innerHTML = '<i></i>';
  const area = document.createElement('div');
  ui.body.append(estado, barra, mantener, area);

  let sensor = null, modo = 'espera', carga = 0, suave = 0, tac = 0, sobre = 0, t = 0, hecho = false, reloj = null, simInt = 0;
  const intensidad = () => (SIM && modo === 'sim' ? simInt : sensor ? sensor.intensidad() : 0);

  function paso() {
    if (hecho) return;
    if (modo === 'tactil') { tac *= 0.95; carga += (tac - carga) * 0.3; }
    else { suave += (intensidad() - suave) * 0.25; carga = suave / 25 * 100; }
    sobre = carga >= 100 ? sobre + 1 : 0;
    if (sobre >= 3) {
      carga = 0; suave = 0; tac = 0; sobre = 0;
      t = 0;
      estado.textContent = '¡Se fundió el fusible! Agitad más suave y empezad de nuevo.';
    } else if (carga >= ZONA[0] && carga <= ZONA[1]) {
      t += 0.1;
      estado.textContent = 'Carga estable… ' + Math.max(0, SEG_ZONA - t).toFixed(1) + ' s';
    } else {
      t = 0;
      estado.textContent = carga < ZONA[0] ? 'Poca carga: agitad.' : 'Demasiada carga: agitad más suave o esperad.';
    }
    barra.querySelector('i').style.width = Math.min(100, carga) + '%';
    mantener.firstChild.style.width = Math.min(100, Math.round(t / SEG_ZONA * 100)) + '%';
    if (t >= SEG_ZONA) {
      hecho = true;
      clearInterval(reloj);
      if (sensor) sensor.parar();
      ui.say('¡El generador ronca y se enciende! (Prototipo del puzle con acelerómetro superado.)', 'ok');
    }
  }
  function arrancar() { clearInterval(reloj); carga = 0; suave = 0; tac = 0; sobre = 0; t = 0; reloj = setInterval(paso, 100); }

  ui.onClose(() => { clearInterval(reloj); if (sensor) sensor.parar(); });

  const activar = ui.button('Activar movimiento', 'primary', async () => {
    if (modo !== 'espera') return;
    try {
      sensor = await abrirMovimiento();
      modo = 'sensor';
      activar.disabled = true;
      ui.say('');
      arrancar();
    } catch (e) {
      ui.say('No se pudo usar el movimiento: ' + (e && e.message ? e.message : 'permiso denegado') + ' Usad la versión táctil.', 'bad');
    }
  });
  ui.button('No puedo usar el movimiento', 'ghost', () => {
    if (hecho) return;
    modo = 'tactil';
    activar.disabled = true;
    if (sensor) { sensor.parar(); sensor = null; }
    ui.say('');
    arrancar();
    area.innerHTML = '';
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'agi-t';
    b.dataset.tactil = '1';
    b.textContent = 'Girar la manivela (pulsar al ritmo)';
    b.addEventListener('click', () => { tac += 12; });
    area.appendChild(b);
  });
  botonesSim(ui, [
    ['Simular generador', () => { if (modo === 'espera') { modo = 'sim'; activar.disabled = true; arrancar(); } }, 'generador'],
    ['Quieto', () => { simInt = 0; }, 'quieto'],
    ['Suave', () => { simInt = 6; }, 'suave'],
    ['Medio', () => { simInt = 16; }, 'medio'],
    ['Fuerte', () => { simInt = 30; }, 'fuerte']
  ]);
  return { close: ui.close };
}

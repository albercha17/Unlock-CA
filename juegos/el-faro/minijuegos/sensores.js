// Sensores del móvil para los puzles de «sensor» (prototipo del 26 oct 2026, pensado para iPhone): micrófono y acelerómetro.
// En iPhone los permisos solo se piden dentro de un toque del jugador, así que estas funciones se llaman desde el clic de un botón.
// Con ?sim=1 en la dirección aparecen botones que simulan el sensor (para las pruebas automáticas y para probar en el ordenador).

export const SIM = /[?&]sim=1/.test(location.search);

/** Abre el micrófono. Devuelve { nivel(): volumen 0..1 (RMS), parar() }. Lanza un error si no hay permiso. */
export async function abrirMicro() {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) throw new Error('Este navegador no permite usar el micrófono.');
  const AC = window.AudioContext || window.webkitAudioContext;
  const ctx = new AC();
  if (ctx.state === 'suspended') { try { await ctx.resume(); } catch (e) { /* ignore */ } }
  const stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: false, noiseSuppression: false, autoGainControl: false } });
  const fuente = ctx.createMediaStreamSource(stream);
  const analizador = ctx.createAnalyser();
  analizador.fftSize = 1024;
  fuente.connect(analizador);
  const buf = new Float32Array(analizador.fftSize);
  return {
    nivel() {
      analizador.getFloatTimeDomainData(buf);
      let s = 0;
      for (let i = 0; i < buf.length; i++) s += buf[i] * buf[i];
      return Math.sqrt(s / buf.length);
    },
    parar() {
      stream.getTracks().forEach(t => t.stop());
      try { ctx.close(); } catch (e) { /* ignore */ }
    }
  };
}

/** Abre el acelerómetro. Devuelve { intensidad(): cuánto se mueve el móvil (0 quieto, ~5 suave, ~20 fuerte), parar() }. */
export async function abrirMovimiento() {
  const D = window.DeviceMotionEvent;
  if (!D) throw new Error('Este navegador no tiene acelerómetro.');
  if (typeof D.requestPermission === 'function') {
    const r = await D.requestPermission();
    if (r !== 'granted') throw new Error('Permiso de movimiento denegado.');
  }
  let ultimo = 0;
  const alMover = e => {
    const a = e.acceleration && e.acceleration.x !== null ? e.acceleration : e.accelerationIncludingGravity;
    if (!a) return;
    const m = Math.hypot(a.x || 0, a.y || 0, a.z || 0);
    ultimo = e.acceleration && e.acceleration.x !== null ? m : Math.abs(m - 9.81);
  };
  window.addEventListener('devicemotion', alMover);
  return {
    intensidad() { return ultimo; },
    parar() { window.removeEventListener('devicemotion', alMover); }
  };
}

/** Botones de simulación (solo con ?sim=1). `acciones` es [[texto, funcion, dato]...]. */
export function botonesSim(ui, acciones) {
  if (!SIM) return;
  const fila = document.createElement('div');
  fila.className = 'fa-fila';
  acciones.forEach(([texto, fn, dato]) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'fa-opc';
    b.dataset.sim = dato;
    b.textContent = texto;
    b.addEventListener('click', fn);
    fila.appendChild(b);
  });
  ui.body.appendChild(fila);
}

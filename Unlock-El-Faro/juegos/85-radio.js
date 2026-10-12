// Carta 85 — Radio de onda corta: sintonizar 91,7 MHz (anotado en el mapa, carta 74).
import { openGame } from './ui.js';

const TARGET = 91.7;
const DECOYS = [
  { f: 95.3, msg: 'Solo música de verbena y publicidad de colchones... Seguid buscando.' },
  { f: 101.9, msg: 'Un partido de fútbol atronador. Esa no es.' }
];
const MESSAGE = '«...aquí guardacostas de Cabo Niebla. Estrella del Norte, a 25 minutos de Los Dientes. El señor Anselmo dejó el mecanismo preparado en la sala de la lente, arriba del todo. Subid. Cambio y corto.»';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 85 — Radio de onda corta',
    instr: 'Gira el dial hasta sintonizar la frecuencia del faro.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-freq{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:2.2rem;font-weight:700;color:#ffd27a;background:#05080c;border:1px solid #2a3a4a;border-radius:10px;padding:8px 0;margin-bottom:12px}
    .far-meter{height:12px;border-radius:6px;background:#1a2430;overflow:hidden;margin:6px 0 14px}
    .far-meter>div{height:100%;width:0;background:linear-gradient(90deg,#c44,#fc4,#4c6);transition:width .08s}
    .far-dial{width:100%;accent-color:#ffd27a}
    .far-msg{min-height:3.2em;color:#cfe0ef;font-size:.9rem;font-style:italic}
  `;
  ui.body.appendChild(style);

  const freqEl = document.createElement('div');
  freqEl.className = 'far-freq';
  const dial = document.createElement('input');
  dial.type = 'range';
  dial.id = 'farDial';
  dial.className = 'far-dial';
  dial.min = '88';
  dial.max = '108';
  dial.step = '0.1';
  dial.value = '99.0';
  dial.setAttribute('aria-label', 'Sintonía en megahercios');
  const meterWrap = document.createElement('div');
  meterWrap.className = 'far-meter';
  const meter = document.createElement('div');
  meterWrap.appendChild(meter);
  const msg = document.createElement('div');
  msg.className = 'far-msg';
  ui.body.append(freqEl, dial, meterWrap, msg);

  let ctx = null, noiseGain = null, toneGain = null, nodes = [], muted = false, solved = false, holdTimer = null;

  function startAudio() {
    try {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return;
      ctx = new AC();
      const buf = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate);
      const data = buf.getChannelData(0);
      for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
      const noise = ctx.createBufferSource();
      noise.buffer = buf;
      noise.loop = true;
      noiseGain = ctx.createGain();
      noiseGain.gain.value = 0.18;
      noise.connect(noiseGain).connect(ctx.destination);
      const osc = ctx.createOscillator();
      osc.type = 'sine';
      osc.frequency.value = 440;
      toneGain = ctx.createGain();
      toneGain.gain.value = 0;
      osc.connect(toneGain).connect(ctx.destination);
      noise.start();
      osc.start();
      nodes = [noise, osc];
    } catch (e) { ctx = null; }
  }
  function stopAudio() {
    nodes.forEach(n => { try { n.stop(); } catch (e) { /* ignore */ } });
    if (ctx) { try { ctx.close(); } catch (e) { /* ignore */ } }
  }
  ui.onClose(() => { stopAudio(); clearTimeout(holdTimer); });

  const strength = f => Math.max(0, 1 - Math.abs(f - TARGET) / 1.5);

  function update() {
    const f = Math.round(parseFloat(dial.value) * 10) / 10;
    freqEl.textContent = f.toFixed(1) + ' MHz';
    const s = strength(f);
    meter.style.width = Math.round(s * 100) + '%';
    if (ctx && noiseGain && toneGain) {
      noiseGain.gain.value = muted || solved ? 0 : 0.2 * (1 - s);
      toneGain.gain.value = muted || solved ? 0 : 0.06 * s;
    }
    if (solved) return;
    clearTimeout(holdTimer);
    if (f === TARGET) {
      msg.textContent = '...señal clara...';
      holdTimer = setTimeout(() => {
        solved = true;
        msg.textContent = MESSAGE;
        ui.say('¡Sintonizado! Coged la carta 78.', 'ok');
        update();
      }, 700);
      return;
    }
    const decoy = DECOYS.find(d => Math.abs(d.f - f) <= 0.3);
    msg.textContent = decoy ? decoy.msg : (s > 0.3 ? 'Se oye algo entre la estática... acercaos.' : 'Solo estática.');
  }

  dial.addEventListener('input', update);
  ui.button('Silenciar / activar sonido', 'ghost', () => { muted = !muted; update(); });
  startAudio();
  update();
  return { close: ui.close };
}

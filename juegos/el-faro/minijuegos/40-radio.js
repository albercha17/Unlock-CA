// Carta 40 — Radio de onda corta: rueda de sintonía (grande) + ajuste fino (pequeña) hasta la frecuencia de Cabo Niebla. El 80 y las boyas rojas del mapa
// (carta 41), los versos del radioaficionado (carta 45) y la décima de la brújula (carta 43) dan la frecuencia (herramientas/instancias_faro.py, radio).
import { openGame } from './ui.js';

const D = /*DATOS*/{"objetivo": 91.7, "falsas": [95.3, 101.9], "cifra": 5}/*FIN*/;
const TARGET = D.objetivo;
const MIN_F = 88;
const MAX_F = 108;
const TOLERANCIA = 0.05;
const DECOYS = [
  { f: D.falsas[0], msg: 'Solo música de verbena y publicidad de colchones... Seguid buscando.' },
  { f: D.falsas[1], msg: 'Un partido de fútbol atronador. Esa no es.' }
];
const MESSAGE = '«...aquí guardacostas de Cabo Niebla. Estrella del Norte, a 25 minutos de Los Dientes. El señor Anselmo dejó media llave de la sala de la lente en la caja de la radio. Cogedla. Cambio y corto.»';
const NS = 'http://www.w3.org/2000/svg';
const X0 = 15;
const X1 = 285;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 40 — Radio de onda corta',
    instr: 'Gira la rueda grande para buscar la emisora y la pequeña para afinar. Sintoniza la frecuencia de Cabo Niebla (cartas 41, 43 y 45).',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-radio{background:linear-gradient(rgba(20,10,4,.18),rgba(20,10,4,.35)),url(./img/ui/radio-madera.jpg) center/cover,#3b2414;border:3px solid #24150a;border-radius:16px;padding:12px 12px 14px;box-shadow:inset 0 0 18px rgba(0,0,0,.6),0 8px 20px rgba(0,0,0,.5)}
    .far-escala{background:linear-gradient(180deg,#f1dfae,#d9c186);border:3px solid #24150a;border-radius:8px;box-shadow:inset 0 0 14px rgba(120,70,10,.45)}
    .far-escala svg{display:block;width:100%}
    .far-panel{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:10px}
    .far-lectura{flex:0 0 auto;font-family:"IBM Plex Mono",ui-monospace,Consolas,monospace;font-weight:700;font-size:1.25rem;color:#ffb347;background:#150c05;border:2px solid #24150a;border-radius:6px;padding:4px 10px;text-shadow:0 0 8px rgba(255,160,40,.8)}
    .far-ruedas{display:flex;justify-content:space-around;align-items:flex-end;margin-top:12px}
    .far-rueda{display:flex;flex-direction:column;align-items:center;gap:6px;color:#e8d3a8;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase}
    .far-knob{position:relative;width:116px;height:116px;border-radius:50%;background:url(./img/ui/radio-perilla.jpg) center/cover,#1b1007;background-blend-mode:screen;border:4px solid #1b1007;box-shadow:0 6px 14px rgba(0,0,0,.6),inset 0 2px 4px rgba(255,255,255,.18);touch-action:none;cursor:grab;user-select:none;-webkit-user-select:none}
    .far-knob:active{cursor:grabbing}
    .far-knob:focus-visible{outline:3px solid #ffd27a;outline-offset:4px}
    .far-knob.fino{width:78px;height:78px}
    .far-knob::before{content:"";position:absolute;inset:0;border-radius:50%;box-shadow:inset 0 0 14px rgba(0,0,0,.55)}
    .far-knob .nota{position:absolute;left:50%;top:5px;width:7px;height:24px;margin-left:-3.5px;border-radius:4px;background:#ffd27a;box-shadow:0 0 6px rgba(255,210,122,.8)}
    .far-knob.fino .nota{height:16px}
    .far-msg{min-height:3.4em;margin-top:10px;color:#cfe0ef;font-size:.9rem;font-style:italic}
  `;
  ui.body.appendChild(style);

  const radio = document.createElement('div');
  radio.className = 'far-radio';

  // ---- escala con aguja ----
  const escala = document.createElement('div');
  escala.className = 'far-escala';
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '0 0 300 74');
  svg.setAttribute('role', 'img');
  svg.setAttribute('aria-label', 'Escala de frecuencias de 88 a 108 megahercios');
  escala.appendChild(svg);
  const x = f => X0 + (f - MIN_F) / (MAX_F - MIN_F) * (X1 - X0);
  function el(tag, attrs) {
    const e = document.createElementNS(NS, tag);
    Object.keys(attrs).forEach(k => e.setAttribute(k, attrs[k]));
    svg.appendChild(e);
    return e;
  }
  for (let f = MIN_F; f <= MAX_F + 1e-9; f += 0.5) {
    const entero = Math.abs(f - Math.round(f)) < 1e-9;
    const par = entero && Math.round(f) % 2 === 0;
    el('line', { x1: x(f), x2: x(f), y1: 38, y2: par ? 56 : entero ? 52 : 47, stroke: '#4a2f14', 'stroke-width': par ? 1.6 : 1 });
    if (par) {
      const t = el('text', { x: x(f), y: 70, 'text-anchor': 'middle', 'font-size': 11, fill: '#4a2f14', 'font-family': 'Georgia,serif', 'font-weight': 700 });
      t.textContent = Math.round(f);
    }
  }
  const mhz = el('text', { x: 150, y: 24, 'text-anchor': 'middle', 'font-size': 11, fill: '#4a2f14', 'font-family': 'Georgia,serif', 'font-style': 'italic' });
  mhz.textContent = 'ONDA CORTA · MHz';
  const aguja = el('line', { x1: 150, x2: 150, y1: 8, y2: 62, stroke: '#c8281a', 'stroke-width': 2.4, 'stroke-linecap': 'round' });
  el('circle', { cx: 150, cy: 8, r: 3, fill: '#c8281a' }).setAttribute('id', 'farAgujaPunta');

  // ---- panel: lectura + señal ----
  const panel = document.createElement('div');
  panel.className = 'far-panel';
  const lectura = document.createElement('div');
  lectura.className = 'far-lectura';
  lectura.id = 'farReadout';
  lectura.setAttribute('aria-live', 'off');
  panel.append(lectura);

  // ---- ruedas ----
  const ruedas = document.createElement('div');
  ruedas.className = 'far-ruedas';

  function crearRueda(clase, etiqueta, nombreAria, inicial) {
    const wrap = document.createElement('div');
    wrap.className = 'far-rueda';
    const knob = document.createElement('div');
    knob.className = 'far-knob ' + clase;
    knob.tabIndex = 0;
    knob.setAttribute('role', 'slider');
    knob.setAttribute('aria-label', nombreAria);
    knob.setAttribute('aria-valuemin', '-135');
    knob.setAttribute('aria-valuemax', '135');
    const nota = document.createElement('div');
    nota.className = 'nota';
    knob.appendChild(nota);
    const lab = document.createElement('span');
    lab.textContent = etiqueta;
    wrap.append(knob, lab);
    ruedas.appendChild(wrap);

    const estado = { ang: inicial, activa: true, alCambiar: () => {} };
    const limitar = a => Math.max(-135, Math.min(135, a));
    function poner(a) {
      estado.ang = limitar(a);
      knob.style.transform = 'rotate(' + estado.ang + 'deg)';
      knob.setAttribute('aria-valuenow', String(Math.round(estado.ang)));
      estado.alCambiar();
    }
    let arrastrando = false;
    let ultimo = 0;
    const angulo = e => {
      const r = knob.getBoundingClientRect();
      return Math.atan2(e.clientY - (r.top + r.height / 2), e.clientX - (r.left + r.width / 2)) * 180 / Math.PI;
    };
    knob.addEventListener('pointerdown', e => {
      if (!estado.activa) return;
      arrastrando = true;
      ultimo = angulo(e);
      try { knob.setPointerCapture(e.pointerId); } catch (err) { /* sin captura */ }
      e.preventDefault();
    });
    knob.addEventListener('pointermove', e => {
      if (!arrastrando || !estado.activa) return;
      const a = angulo(e);
      let d = a - ultimo;
      while (d > 180) d -= 360;
      while (d < -180) d += 360;
      ultimo = a;
      poner(estado.ang + d);
    });
    const soltar = () => { arrastrando = false; };
    knob.addEventListener('pointerup', soltar);
    knob.addEventListener('pointercancel', soltar);
    knob.addEventListener('wheel', e => {
      if (!estado.activa) return;
      e.preventDefault();
      poner(estado.ang + (e.deltaY < 0 ? 4 : -4));
    }, { passive: false });
    knob.addEventListener('keydown', e => {
      if (!estado.activa) return;
      const paso = e.shiftKey ? 15 : 3;
      if (e.key === 'ArrowRight' || e.key === 'ArrowUp') { poner(estado.ang + paso); e.preventDefault(); }
      if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') { poner(estado.ang - paso); e.preventDefault(); }
    });
    estado.poner = poner;
    estado.knob = knob;
    return estado;
  }

  const grande = crearRueda('grande', 'Sintonía', 'Rueda de sintonía', 13.5);   // 99,0 MHz
  const fina = crearRueda('fino', 'Ajuste fino', 'Rueda de ajuste fino', 0);
  radio.append(escala, panel, ruedas);
  const msg = document.createElement('div');
  msg.className = 'far-msg';
  ui.body.append(radio, msg);

  // ---- sonido ----
  // Sonido: estática que baja al acercarte a una emisora, tono limpio en la del faro y otro tono en las falsas.
  let ctx = null, noiseGain = null, toneGain = null, decoyGain = null, decoyOsc = null, nodes = [], muted = false, solved = false, holdTimer = null;
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
      decoyOsc = ctx.createOscillator();
      decoyOsc.type = 'triangle';
      decoyOsc.frequency.value = 260;
      decoyGain = ctx.createGain();
      decoyGain.gain.value = 0;
      decoyOsc.connect(decoyGain).connect(ctx.destination);
      noise.start();
      osc.start();
      decoyOsc.start();
      nodes = [noise, osc, decoyOsc];
    } catch (e) { ctx = null; }
  }
  function despertarAudio() {
    if (ctx && ctx.state === 'suspended') { try { ctx.resume(); } catch (e) { /* ignore */ } }
  }
  ['pointerdown', 'keydown', 'wheel'].forEach(t => radio.addEventListener(t, despertarAudio, { passive: true }));
  function stopAudio() {
    nodes.forEach(n => { try { n.stop(); } catch (e) { /* ignore */ } });
    if (ctx) { try { ctx.close(); } catch (e) { /* ignore */ } }
  }
  ui.onClose(() => { stopAudio(); clearTimeout(holdTimer); });

  // ---- frecuencia ----
  const frecuencia = () => {
    const f = MIN_F + (grande.ang + 135) / 270 * (MAX_F - MIN_F) + fina.ang / 135;
    return Math.max(MIN_F, Math.min(MAX_F, f));
  };
  const fuerza = f => Math.max(0, 1 - Math.abs(f - TARGET) / 1.5);

  function actualizar() {
    const f = frecuencia();
    aguja.setAttribute('x1', x(f));
    aguja.setAttribute('x2', x(f));
    document.getElementById('farAgujaPunta').setAttribute('cx', x(f));
    lectura.textContent = f.toFixed(1) + ' MHz';
    const s = fuerza(f);
    const dd = Math.min(...DECOYS.map(d => Math.abs(d.f - f)));
    const sd = Math.max(0, 1 - dd / 0.8);
    if (ctx && noiseGain && toneGain && decoyGain) {
      const apagado = muted || solved;
      noiseGain.gain.value = apagado ? 0 : 0.2 * (1 - Math.max(s, sd * 0.7));
      toneGain.gain.value = apagado ? 0 : 0.07 * s * s;
      decoyGain.gain.value = apagado ? 0 : 0.05 * sd * sd;
    }
    if (solved) return;
    clearTimeout(holdTimer);
    if (Math.abs(f - TARGET) <= TOLERANCIA) {
      holdTimer = setTimeout(() => {
        solved = true;
        grande.activa = false;
        fina.activa = false;
        msg.textContent = MESSAGE;
        ui.say('¡Sintonizado! Responde la guardia costera. Cifra de la radio: ' + D.cifra + '. Coged la carta 30.', 'ok');
        actualizar();
      }, 700);
      return;
    }
    const decoy = DECOYS.find(d => Math.abs(d.f - f) <= 0.3);
    msg.textContent = decoy ? decoy.msg : '';
  }

  grande.alCambiar = actualizar;
  fina.alCambiar = actualizar;
  ui.button('Silenciar / activar sonido', 'ghost', () => { muted = !muted; actualizar(); });
  startAudio();
  fina.poner(fina.ang);
  grande.poner(grande.ang);
  return { close: ui.close };
}

// musica.js — música de fondo generativa (WebAudio, sin archivos): cada juego tiene su ambientación.
// Común a todos los juegos: se edita en juegos/el-faro y se propaga con herramientas/regenerar_index.py.
//
// Uso:  const m = crearMusica('faro');  m.iniciar();  m.duck(true);  m.parar();
// Todo es opcional y a prueba de fallos: si no hay audio, no pasa nada.

const mtof = (m) => 440 * Math.pow(2, (m - 69) / 12);
const azar = (a, b) => a + Math.random() * (b - a);
const elige = (lista) => lista[Math.floor(Math.random() * lista.length)];

// escalas (semitonos desde la raíz)
const ESC = {
  menor: [0, 2, 3, 5, 7, 8, 10],
  dorica: [0, 2, 3, 5, 7, 9, 10],
  frigia: [0, 1, 4, 5, 7, 8, 10], // frigia dominante (egipcia/árabe)
  pentatonica: [0, 3, 5, 7, 10],
  mayorPent: [0, 2, 4, 7, 9],
  lidia: [0, 2, 4, 6, 7, 9, 11]
};

/*  Cada preset describe capas: pad (acordes largos), melodia (notas sueltas), arpegio (patrón regular), ritmo (golpes) y ruido (ambiente).
    - raiz: nota MIDI base; bpm; acordes: lista de acordes en grados de la escala (0 = raíz) que cambian cada `compases`.
    - onda: forma de onda; filtro: frecuencia del paso bajo; vol: volumen relativo de la capa. */
const PRESETS = {
  // Faro: tormenta, niebla y una campana lejana. La Menor, muy lento.
  faro: {
    bpm: 52, raiz: 45, escala: ESC.menor, compases: 2, reverb: 3.2,
    acordes: [[0, 2, 4], [5, 0, 2], [3, 5, 0], [4, 6, 1]],
    pad: { onda: 'sawtooth', filtro: 520, vol: 0.16, octava: 0, ataque: 2.4 },
    melodia: { onda: 'sine', vol: 0.26, octava: 2, prob: 0.26, dur: 2.6, ataque: 0.01, filtro: 2800, vibrato: 0, campana: true },
    ruido: { tipo: 'lluvia', vol: 0.12 },
    extras: { sirena: { nota: 33, cada: [26, 44], vol: 0.2 } }
  },
  // Egipto: modo frigio dominante, tambor de marco y laúd.
  egipto: {
    bpm: 76, raiz: 50, escala: ESC.frigia, compases: 2, reverb: 2.2,
    acordes: [[0, 4], [0, 4], [3, 0], [0, 4]],
    pad: { onda: 'triangle', filtro: 700, vol: 0.14, octava: 0, ataque: 1.6 },
    melodia: { onda: 'sawtooth', vol: 0.12, octava: 1, prob: 0.42, dur: 0.7, ataque: 0.005, filtro: 1900, vibrato: 0, pulsada: true },
    ritmo: { tipo: 'tambor', patron: [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0], vol: 0.34, tono: 90 },
    ruido: { tipo: 'viento', vol: 0.05 }
  },
  // Marte: sintetizadores fríos, pulso grave y viento de polvo.
  marte: {
    bpm: 92, raiz: 40, escala: ESC.pentatonica, compases: 4, reverb: 2.6,
    acordes: [[0, 2, 4], [3, 0, 2], [4, 1, 3], [2, 4, 0]],
    pad: { onda: 'sawtooth', filtro: 900, vol: 0.13, octava: 0, ataque: 3.2, lfo: 0.07 },
    arpegio: { onda: 'square', vol: 0.06, paso: 2, octava: 2, patron: [0, 2, 4, 2, 1, 3, 4, 3], filtro: 2400 },
    ritmo: { tipo: 'pulso', patron: [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0], vol: 0.3, tono: 52 },
    ruido: { tipo: 'viento', vol: 0.1 }
  },
  // Florencia: modo dórico, laúd arpegiado y flauta suave.
  florencia: {
    bpm: 84, raiz: 50, escala: ESC.dorica, compases: 2, reverb: 2.4,
    acordes: [[0, 2, 4], [3, 5, 0], [4, 6, 1], [0, 2, 4]],
    pad: { onda: 'sine', filtro: 1200, vol: 0.11, octava: 0, ataque: 1.8 },
    arpegio: { onda: 'triangle', vol: 0.15, paso: 2, octava: 1, patron: [0, 1, 2, 1, 2, 3, 2, 1], filtro: 3200, pulsada: true },
    melodia: { onda: 'sine', vol: 0.12, octava: 2, prob: 0.2, dur: 2.2, ataque: 0.25, filtro: 3000, vibrato: 5.2 },
    ruido: null
  },
  // Dinosaurios: tambores tribales, selva con insectos y cuerno grave.
  dinosaurios: {
    bpm: 84, raiz: 40, escala: ESC.pentatonica, compases: 4, reverb: 2.0,
    acordes: [[0, 2], [0, 3], [2, 4], [0, 2]],
    pad: { onda: 'sawtooth', filtro: 380, vol: 0.14, octava: 0, ataque: 2.8 },
    melodia: { onda: 'triangle', vol: 0.16, octava: 2, prob: 0.22, dur: 1.6, ataque: 0.08, filtro: 2200, vibrato: 4.5 },
    ritmo: { tipo: 'tom', patron: [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1], vol: 0.4, tono: 110 },
    ruido: { tipo: 'insectos', vol: 0.07 }
  },
  // Cuento: caja de música y arpa, tono de vals luminoso (lidio).
  cuento: {
    bpm: 108, raiz: 60, escala: ESC.lidia, compases: 2, reverb: 2.8, compas: 3,
    acordes: [[0, 2, 4], [3, 5, 0], [4, 6, 1], [0, 2, 4]],
    pad: { onda: 'sine', filtro: 1800, vol: 0.1, octava: -1, ataque: 1.4 },
    arpegio: { onda: 'sine', vol: 0.16, paso: 2, octava: 1, patron: [0, 1, 2, 1, 2, 4, 2, 1], filtro: 5200, pulsada: true, campana: true },
    melodia: { onda: 'triangle', vol: 0.15, octava: 2, prob: 0.3, dur: 0.9, ataque: 0.01, filtro: 4200, vibrato: 0, campana: true },
    ruido: null
  },
  // Trono: cuerdas graves, golpes de tambor de guerra y viento helado.
  trono: {
    bpm: 62, raiz: 38, escala: ESC.menor, compases: 2, reverb: 3.4,
    acordes: [[0, 2, 4], [5, 0, 2], [3, 5, 0], [4, 6, 1]],
    pad: { onda: 'sawtooth', filtro: 650, vol: 0.2, octava: 0, ataque: 2.6, lfo: 0.05 },
    melodia: { onda: 'sawtooth', vol: 0.1, octava: 1, prob: 0.16, dur: 3.4, ataque: 0.5, filtro: 1100, vibrato: 4 },
    arpegio: { onda: 'sine', vol: 0.06, paso: 4, octava: 3, patron: [4, 2, 0, 2], filtro: 6000, pulsada: true, campana: true },
    ritmo: { tipo: 'taiko', patron: [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0], vol: 0.46, tono: 62 },
    ruido: { tipo: 'viento', vol: 0.13 }
  },
  // Pompeya: lira arpegiada y flauta en modo dórico, tambor suave y un viento con ceniza.
  pompeya: {
    bpm: 72, raiz: 50, escala: ESC.dorica, compases: 2, reverb: 2.4,
    acordes: [[0, 2, 4], [3, 5, 0], [4, 6, 1], [0, 2, 4]],
    pad: { onda: 'triangle', filtro: 900, vol: 0.13, octava: -1, ataque: 2.2 },
    arpegio: { onda: 'triangle', vol: 0.15, paso: 2, octava: 1, patron: [0, 2, 1, 3, 2, 4, 3, 2], filtro: 4200, pulsada: true, campana: true },
    melodia: { onda: 'sine', vol: 0.13, octava: 2, prob: 0.24, dur: 1.5, ataque: 0.1, filtro: 3000, vibrato: 4 },
    ritmo: { tipo: 'tambor', patron: [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0], vol: 0.26, tono: 80 },
    ruido: { tipo: 'viento', vol: 0.08 }
  },
  // Arcade: chiptune de ocho bits, arpegio de onda cuadrada rápido y bombo constante.
  arcade: {
    bpm: 132, raiz: 57, escala: ESC.menor, compases: 2, reverb: 0.5,
    acordes: [[0, 2, 4], [5, 0, 2], [3, 5, 0], [4, 6, 1]],
    pad: { onda: 'square', filtro: 1400, vol: 0.05, octava: -1, ataque: 0.05 },
    arpegio: { onda: 'square', vol: 0.09, paso: 2, octava: 1, patron: [0, 2, 4, 2, 5, 4, 2, 0], filtro: 4800, pulsada: true, campana: false },
    melodia: { onda: 'square', vol: 0.07, octava: 2, prob: 0.3, dur: 0.3, ataque: 0.005, filtro: 4200, vibrato: 0 },
    ritmo: { tipo: 'pulso', patron: [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0], vol: 0.3, tono: 60 },
    ruido: null
  },
  // Oeste: guitarra pulsada, armónica lejana, galope de caballos y viento seco.
  oeste: {
    bpm: 92, raiz: 45, escala: ESC.pentatonica, compases: 2, reverb: 1.8,
    acordes: [[0, 2], [0, 3], [2, 4], [0, 2]],
    pad: { onda: 'triangle', filtro: 700, vol: 0.1, octava: -1, ataque: 1.8 },
    arpegio: { onda: 'triangle', vol: 0.12, paso: 2, octava: 1, patron: [0, 2, 1, 3, 2, 1], filtro: 3600, pulsada: true, campana: true },
    melodia: { onda: 'sine', vol: 0.12, octava: 2, prob: 0.2, dur: 2.2, ataque: 0.15, filtro: 2400, vibrato: 5 },
    ritmo: { tipo: 'tambor', patron: [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0], vol: 0.22, tono: 85 },
    ruido: { tipo: 'viento', vol: 0.1 }
  },
  // Espía: bajo de big band, vibráfono pulsado y melodía de misterio en modo menor armónico aproximado (menor).
  espia: {
    bpm: 112, raiz: 40, escala: ESC.menor, compases: 2, reverb: 1.2,
    acordes: [[0, 2, 4], [0, 2, 5], [3, 5, 0], [4, 6, 1]],
    pad: { onda: 'triangle', filtro: 800, vol: 0.09, octava: -1, ataque: 0.6 },
    arpegio: { onda: 'sine', vol: 0.12, paso: 2, octava: 2, patron: [0, 2, 4, 2, 0, 3, 5, 3], filtro: 5200, pulsada: true, campana: true },
    melodia: { onda: 'triangle', vol: 0.1, octava: 1, prob: 0.3, dur: 0.5, ataque: 0.02, filtro: 2600, vibrato: 4 },
    ritmo: { tipo: 'pulso', patron: [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0], vol: 0.26, tono: 55 },
    ruido: null
  }
};

function impulso(ctx, seg) {
  const n = Math.floor(ctx.sampleRate * seg);
  const b = ctx.createBuffer(2, n, ctx.sampleRate);
  for (let c = 0; c < 2; c++) {
    const d = b.getChannelData(c);
    for (let i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / n, 2.6);
  }
  return b;
}

function ruidoBuffer(ctx, color) {
  const n = ctx.sampleRate * 4;
  const b = ctx.createBuffer(1, n, ctx.sampleRate);
  const d = b.getChannelData(0);
  let ult = 0;
  for (let i = 0; i < n; i++) {
    const w = Math.random() * 2 - 1;
    if (color === 'marron') { ult = (ult + 0.02 * w) / 1.02; d[i] = ult * 3.2; } else d[i] = w;
  }
  return b;
}

export function crearMusica(tema, { contexto = null, destino = null } = {}) {
  const P = PRESETS[tema] || PRESETS.faro;
  let ctx = contexto;
  let master = null, bus = null, reverbIn = null;
  let timer = null, activo = false, siguiente = 0, paso = 0, volumen = 0.5, bajo = false;
  const fuentesContinuas = [];
  let proximaSirena = 0;
  let notaMelodia = 2;

  const grado = (g, octava = 0) => {
    const n = P.escala.length;
    const o = Math.floor(g / n);
    return P.raiz + 12 * (octava + o) + P.escala[((g % n) + n) % n];
  };
  const seg16 = () => 60 / P.bpm / 4;

  function montar() {
    if (ctx) { /* contexto prestado */ } else {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return false;
      ctx = new AC();
    }
    master = ctx.createGain();
    master.gain.value = 0.0001;
    const comp = ctx.createDynamicsCompressor();
    comp.threshold.value = -20; comp.ratio.value = 4;
    bus = ctx.createGain();
    const seco = ctx.createGain(); seco.gain.value = 0.8;
    const conv = ctx.createConvolver(); conv.buffer = impulso(ctx, P.reverb || 2.5);
    const hum = ctx.createGain(); hum.gain.value = 0.5;
    reverbIn = ctx.createGain();
    bus.connect(seco); seco.connect(master);
    bus.connect(reverbIn); reverbIn.connect(conv); conv.connect(hum); hum.connect(master);
    master.connect(comp); comp.connect(destino || ctx.destination);
    // capas continuas
    if (P.ruido) fuentesContinuas.push(ruidoCapa(P.ruido));
    return true;
  }

  function ruidoCapa(r) {
    const src = ctx.createBufferSource();
    src.buffer = ruidoBuffer(ctx, r.tipo === 'insectos' ? 'blanco' : 'marron');
    src.loop = true;
    const f = ctx.createBiquadFilter();
    const g = ctx.createGain();
    const lfo = ctx.createOscillator();
    const lfoG = ctx.createGain();
    lfo.type = 'sine';
    if (r.tipo === 'lluvia') { f.type = 'highpass'; f.frequency.value = 1800; g.gain.value = r.vol * 0.8; lfo.frequency.value = 0.1; lfoG.gain.value = r.vol * 0.25; }
    else if (r.tipo === 'insectos') { f.type = 'bandpass'; f.frequency.value = 4600; f.Q.value = 6; g.gain.value = r.vol * 0.5; lfo.frequency.value = 7; lfoG.gain.value = r.vol * 0.45; }
    else { f.type = 'lowpass'; f.frequency.value = 520; g.gain.value = r.vol; lfo.frequency.value = 0.08; lfoG.gain.value = r.vol * 0.6; }
    lfo.connect(lfoG); lfoG.connect(g.gain);
    src.connect(f); f.connect(g); g.connect(bus);
    src.start(); lfo.start();
    return [src, lfo];
  }

  // ---- voces
  function nota(freq, t, dur, { onda = 'sine', vol = 0.1, ataque = 0.01, filtro = 3000, vibrato = 0, pulsada = false, campana = false } = {}) {
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    const f = ctx.createBiquadFilter();
    o.type = onda; o.frequency.setValueAtTime(freq, t);
    f.type = 'lowpass';
    f.frequency.setValueAtTime(pulsada ? filtro * 1.4 : filtro, t);
    if (pulsada) f.frequency.exponentialRampToValueAtTime(Math.max(300, filtro * 0.35), t + Math.min(dur, 0.9));
    if (vibrato) { const l = ctx.createOscillator(); const lg = ctx.createGain(); l.frequency.value = vibrato; lg.gain.value = freq * 0.006; l.connect(lg); lg.connect(o.frequency); l.start(t); l.stop(t + dur + 0.5); }
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + Math.max(0.004, ataque));
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(f); f.connect(g); g.connect(bus);
    o.start(t); o.stop(t + dur + 0.1);
    if (campana) { // armónico inarmónico: sonido de campana / caja de música
      const o2 = ctx.createOscillator(); const g2 = ctx.createGain();
      o2.type = 'sine'; o2.frequency.value = freq * 2.76;
      g2.gain.setValueAtTime(0.0001, t); g2.gain.exponentialRampToValueAtTime(vol * 0.35, t + 0.005); g2.gain.exponentialRampToValueAtTime(0.0001, t + dur * 0.5);
      o2.connect(g2); g2.connect(bus); o2.start(t); o2.stop(t + dur * 0.5 + 0.1);
    }
  }

  function acordeLargo(t, acorde, dur) {
    const p = P.pad;
    acorde.forEach((g, i) => {
      [-6, 6].forEach((cents) => {
        const o = ctx.createOscillator(); const gn = ctx.createGain(); const f = ctx.createBiquadFilter();
        o.type = p.onda; o.frequency.setValueAtTime(mtof(grado(g, p.octava + (i === 0 ? 0 : 1))), t); o.detune.value = cents;
        f.type = 'lowpass'; f.frequency.setValueAtTime(p.filtro, t);
        if (p.lfo) { const l = ctx.createOscillator(); const lg = ctx.createGain(); l.frequency.value = p.lfo; lg.gain.value = p.filtro * 0.45; l.connect(lg); lg.connect(f.frequency); l.start(t); l.stop(t + dur + p.ataque * 2); }
        gn.gain.setValueAtTime(0.0001, t);
        gn.gain.exponentialRampToValueAtTime(p.vol / (acorde.length * 1.6), t + p.ataque);
        gn.gain.setValueAtTime(p.vol / (acorde.length * 1.6), t + dur);
        gn.gain.exponentialRampToValueAtTime(0.0001, t + dur + p.ataque * 1.2);
        o.connect(f); f.connect(gn); gn.connect(bus);
        o.start(t); o.stop(t + dur + p.ataque * 1.3);
      });
    });
  }

  function golpe(t, tipo, tono, vol) {
    const o = ctx.createOscillator(); const g = ctx.createGain();
    o.type = 'sine';
    const caida = tipo === 'taiko' ? 0.55 : tipo === 'pulso' ? 0.8 : 0.45;
    o.frequency.setValueAtTime(tono * 2.2, t); o.frequency.exponentialRampToValueAtTime(tono * caida, t + 0.16);
    const largo = tipo === 'taiko' ? 0.7 : tipo === 'pulso' ? 0.22 : 0.32;
    g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.0001, t + largo);
    o.connect(g); g.connect(bus); o.start(t); o.stop(t + largo + 0.05);
    if (tipo !== 'pulso') { // golpe de parche: ráfaga de ruido corta
      const n = ctx.createBufferSource(); n.buffer = ruidoBuffer(ctx, 'blanco');
      const f = ctx.createBiquadFilter(); f.type = 'bandpass'; f.frequency.value = tipo === 'tambor' ? 1400 : 700; f.Q.value = 0.9;
      const gn = ctx.createGain(); gn.gain.setValueAtTime(vol * 0.35, t); gn.gain.exponentialRampToValueAtTime(0.0001, t + 0.09);
      n.connect(f); f.connect(gn); gn.connect(bus); n.start(t, Math.random() * 2); n.stop(t + 0.12);
    }
  }

  function sirena(t, e) {
    const o = ctx.createOscillator(); const g = ctx.createGain(); const f = ctx.createBiquadFilter();
    o.type = 'sawtooth'; o.frequency.setValueAtTime(mtof(e.nota), t); o.frequency.linearRampToValueAtTime(mtof(e.nota) * 0.985, t + 4.5);
    f.type = 'lowpass'; f.frequency.value = 280;
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(e.vol * 0.4, t + 1.2); g.gain.exponentialRampToValueAtTime(0.0001, t + 5);
    o.connect(f); f.connect(g); g.connect(bus); o.start(t); o.stop(t + 5.2);
  }

  // ---- planificador (cada 16.º de pulso)
  function programar(t) {
    const por16 = P.compas ? P.compas * 4 : 16;
    const paso16 = paso % por16;
    const barra = Math.floor(paso / por16);
    const largoAcorde = P.compases;
    if (paso16 === 0 && barra % largoAcorde === 0) {
      const ac = P.acordes[Math.floor(barra / largoAcorde) % P.acordes.length];
      acordeLargo(t, ac, seg16() * por16 * largoAcorde);
      notaMelodia = ac[0] + 2;
    }
    const ac = P.acordes[Math.floor(barra / largoAcorde) % P.acordes.length];
    if (P.arpegio && paso16 % P.arpegio.paso === 0) {
      const a = P.arpegio;
      const idx = a.patron[(paso16 / a.paso) % a.patron.length];
      const g = ac[idx % ac.length] + (idx >= ac.length ? P.escala.length : 0);
      nota(mtof(grado(g, a.octava)), t, seg16() * a.paso * 1.8, { onda: a.onda, vol: a.vol, filtro: a.filtro, pulsada: a.pulsada, campana: a.campana, ataque: 0.004 });
    }
    if (P.melodia && paso16 % 4 === 0 && Math.random() < P.melodia.prob) {
      const m = P.melodia;
      notaMelodia = Math.max(0, Math.min(P.escala.length + 3, notaMelodia + elige([-2, -1, -1, 0, 1, 1, 2])));
      nota(mtof(grado(notaMelodia, m.octava)), t + azar(0, 0.06), m.dur, { onda: m.onda, vol: m.vol, ataque: m.ataque, filtro: m.filtro, vibrato: m.vibrato, pulsada: m.pulsada, campana: m.campana });
    }
    if (P.ritmo && P.ritmo.patron[paso % P.ritmo.patron.length]) {
      golpe(t, P.ritmo.tipo, P.ritmo.tono, P.ritmo.vol * (paso16 === 0 ? 1 : 0.7));
    }
    if (P.extras && P.extras.sirena && t >= proximaSirena) {
      if (proximaSirena > 0) sirena(t, P.extras.sirena);
      proximaSirena = t + azar(P.extras.sirena.cada[0], P.extras.sirena.cada[1]);
    }
    paso++;
  }

  function reloj() {
    if (!activo || !ctx) return;
    while (siguiente < ctx.currentTime + 0.5) { programar(siguiente); siguiente += seg16(); }
  }

  function aplicarVolumen(rapido) {
    if (!master) return;
    const v = Math.max(0.0001, volumen * (bajo ? 0.35 : 1));
    master.gain.cancelScheduledValues(ctx.currentTime);
    master.gain.setTargetAtTime(v, ctx.currentTime, rapido ? 0.05 : 0.8);
  }

  return {
    get activo() { return activo; },
    iniciar() {
      try {
        if (activo) return true;
        if (!master && !montar()) return false;
        if (ctx.state === 'suspended') ctx.resume();
        activo = true;
        siguiente = ctx.currentTime + 0.15;
        paso = 0;
        proximaSirena = ctx.currentTime + 12;
        reloj();
        timer = setInterval(reloj, 120);
        aplicarVolumen(false);
        return true;
      } catch (e) { activo = false; return false; }
    },
    parar() {
      try {
        activo = false;
        if (timer) { clearInterval(timer); timer = null; }
        if (master && ctx) master.gain.setTargetAtTime(0.0001, ctx.currentTime, 0.4);
      } catch (e) { /* nada */ }
    },
    /** Solo para pruebas con OfflineAudioContext: programa de golpe `seg` segundos de música y abre el volumen. */
    renderizarPrueba(seg) {
      if (!master && !montar()) return false;
      activo = true; siguiente = 0.05; paso = 0; proximaSirena = 8;
      while (siguiente < seg) { programar(siguiente); siguiente += seg16(); }
      master.gain.setValueAtTime(volumen, 0);
      activo = false;
      return true;
    },
    /** Baja el volumen mientras hay un minijuego o una pausa. */
    duck(si) { bajo = !!si; try { aplicarVolumen(true); } catch (e) { /* nada */ } },
    volumen(v) { volumen = Math.max(0, Math.min(1, v)); try { aplicarVolumen(true); } catch (e) { /* nada */ } },
    suspender() { try { if (ctx && ctx.state === 'running') ctx.suspend(); } catch (e) { /* nada */ } },
    reanudar() { try { if (ctx && activo && ctx.state === 'suspended') ctx.resume(); } catch (e) { /* nada */ } },
    get contexto() { return ctx; },
    temas: Object.keys(PRESETS)
  };
}

export const TEMAS_MUSICA = Object.keys(PRESETS);

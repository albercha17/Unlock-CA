// Base común de los minijuegos: overlay, título, feedback, botones y cierre.
// Ambientación visual: cada juego tiene su tema (`data-tema` en <html> o, si falta, se deduce de la ruta):
// fondo con la ilustración de la carta, cabecera con imagen, marco, tipografía, partículas ambientales,
// destello al ganar y sacudida al fallar. Los minijuegos solo usan: body, button, close, onClose, say.

const STYLE_ID = 'far-ui-style';
const FONT_ID = 'far-ui-fonts';

const TEMAS = {
  faro: {
    fuente: "'Playfair Display', Georgia, 'Times New Roman', serif", mayus: false, trazo: '.02em',
    tinte: '4,16,28', panel: 'rgba(8,24,38,.90)', panel2: 'rgba(4,12,22,.94)',
    borde: '#c9a45a', acento: '#ffd27a', brillo: '255,210,122', boton: 'linear-gradient(180deg,#ffd27a,#d79a2a)', botonTxt: '#2a1600',
    particulas: 'lluvia', simbolo: '✦', textura: 'panel.jpg', papel: 'papel.jpg'
  },
  egipto: {
    fuente: "'Cinzel', Georgia, 'Times New Roman', serif", mayus: true, trazo: '.1em',
    tinte: '34,22,6', panel: 'rgba(40,26,10,.90)', panel2: 'rgba(18,11,4,.94)',
    borde: '#d9a441', acento: '#f2d27a', brillo: '242,210,122', boton: 'linear-gradient(180deg,#f2d27a,#c98a1f)', botonTxt: '#2a1600',
    particulas: 'polvo', simbolo: '☥', textura: 'panel.jpg', papel: 'papiro.jpg'
  },
  marte: {
    fuente: "'Orbitron', 'Poppins', system-ui, sans-serif", mayus: true, trazo: '.12em',
    tinte: '30,8,4', panel: 'rgba(34,12,8,.90)', panel2: 'rgba(14,5,4,.94)',
    borde: '#ff8a50', acento: '#ffb085', brillo: '255,138,80', boton: 'linear-gradient(180deg,#ff9a60,#d8561e)', botonTxt: '#1c0a04',
    particulas: 'racha', simbolo: '✧', textura: 'panel.jpg', escaneo: true
  },
  florencia: {
    fuente: "'Cormorant Garamond', Georgia, 'Times New Roman', serif", mayus: false, trazo: '.01em',
    tinte: '28,16,6', panel: 'rgba(42,26,12,.90)', panel2: 'rgba(20,11,5,.94)',
    borde: '#d9a441', acento: '#f0c773', brillo: '240,199,115', boton: 'linear-gradient(180deg,#f0c773,#c9892a)', botonTxt: '#2a1600',
    particulas: 'chispa', simbolo: '✦', textura: 'panel.jpg', vela: true
  },
  dinosaurios: {
    fuente: "'Bevan', Georgia, 'Times New Roman', serif", mayus: false, trazo: '.02em',
    tinte: '6,22,10', panel: 'rgba(14,38,20,.90)', panel2: 'rgba(6,18,10,.94)',
    borde: '#9bc94a', acento: '#b5e35b', brillo: '181,227,91', boton: 'linear-gradient(180deg,#c7ef6a,#6fae2a)', botonTxt: '#0c1f06',
    particulas: 'polvo', simbolo: '✧', textura: 'panel.jpg', papel: 'papel.jpg'
  },
  cuento: {
    fuente: "'Fredoka', 'Poppins', system-ui, sans-serif", mayus: false, trazo: '.02em',
    tinte: '16,8,40', panel: 'rgba(44,26,92,.90)', panel2: 'rgba(22,12,52,.94)',
    borde: '#f6c453', acento: '#ffe08a', brillo: '255,224,138', boton: 'linear-gradient(180deg,#ffe08a,#f2a93a)', botonTxt: '#2a1450',
    particulas: 'chispa', simbolo: '✦', textura: 'panel.jpg', papel: 'papel.jpg'
  },
  trono: {
    fuente: "'MedievalSharp', 'Cinzel', Georgia, serif", mayus: false, trazo: '.03em',
    tinte: '8,12,18', panel: 'rgba(22,28,36,.92)', panel2: 'rgba(10,14,20,.95)',
    borde: '#9fb8cc', acento: '#d6e8f5', brillo: '159,200,230', boton: 'linear-gradient(180deg,#d6e8f5,#8aa6bc)', botonTxt: '#0d1822',
    particulas: 'nieve', simbolo: '❖', textura: 'panel.jpg', papel: 'papel.jpg'
  }
};

function detectarTema() {
  const t = document.documentElement.dataset.tema;
  if (t && TEMAS[t]) return t;
  const p = location.pathname;
  if (/dinosaurios/.test(p)) return 'dinosaurios';
  if (/cuento/.test(p)) return 'cuento';
  if (/trono/.test(p)) return 'trono';
  if (/florencia/.test(p)) return 'florencia';
  if (/egipto/.test(p)) return 'egipto';
  if (/marte/.test(p)) return 'marte';
  return 'faro';
}

function sinMovimiento() {
  return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
}

function injectFonts() {
  if (document.getElementById(FONT_ID)) return;
  const l = document.createElement('link');
  l.id = FONT_ID;
  l.rel = 'stylesheet';
  l.href = 'https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Cormorant+Garamond:ital,wght@0,600;1,600;1,700&family=Orbitron:wght@600;800&family=Playfair+Display:wght@600;800&family=Bevan&family=Fredoka:wght@500;700&family=MedievalSharp&display=swap';
  document.head.appendChild(l);
}

function injectStyle() {
  if (document.getElementById(STYLE_ID)) return;
  const s = document.createElement('style');
  s.id = STYLE_ID;
  s.textContent = `
    .far-overlay{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(var(--far-tinte,2,6,12),.86);z-index:2500;padding:max(12px,env(safe-area-inset-top)) max(12px,env(safe-area-inset-right)) max(12px,env(safe-area-inset-bottom)) max(12px,env(safe-area-inset-left));font-family:"Poppins",system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;overflow:hidden;animation:far-entra .25s ease-out}
    .far-bg{position:absolute;inset:-24px;background-size:cover;background-position:center;filter:blur(8px) brightness(.55) saturate(1.2);transform:scale(1.08);pointer-events:none}
    .far-bg::after{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 50% 40%,rgba(var(--far-tinte),0) 0%,rgba(var(--far-tinte),.82) 100%)}
    .far-ambiente{position:absolute;inset:0;pointer-events:none;overflow:hidden}
    .far-box{position:relative;z-index:2;width:min(480px,94vw);max-height:94vh;overflow:auto;background:var(--far-panel,linear-gradient(180deg,#14202c,#0c141d));border:1px solid var(--far-borde,rgba(255,255,255,.1));border-radius:16px;padding:20px;color:#fff;box-shadow:0 22px 70px rgba(0,0,0,.65),0 0 46px rgba(var(--far-brillo,255,210,122),.14),inset 0 0 0 4px rgba(0,0,0,.28),inset 0 0 0 5px rgba(var(--far-brillo,255,255,255),.22);text-align:center;animation:far-sube .38s cubic-bezier(.2,.85,.25,1);backdrop-filter:blur(3px)}
    .far-box::-webkit-scrollbar{width:6px}.far-box::-webkit-scrollbar-thumb{background:rgba(255,255,255,.18);border-radius:6px}
    .far-textura{position:absolute;inset:0;border-radius:16px;background-size:cover;background-position:center;opacity:.2;mix-blend-mode:screen;pointer-events:none}
    .far-esq{position:absolute;width:16px;height:16px;border:2px solid var(--far-acento,#ffd27a);opacity:.85;pointer-events:none;z-index:3}
    .far-esq.a{top:8px;left:8px;border-right:none;border-bottom:none;border-top-left-radius:5px}
    .far-esq.b{top:8px;right:8px;border-left:none;border-bottom:none;border-top-right-radius:5px}
    .far-esq.c{bottom:8px;left:8px;border-right:none;border-top:none;border-bottom-left-radius:5px}
    .far-esq.d{bottom:8px;right:8px;border-left:none;border-top:none;border-bottom-right-radius:5px}
    .far-banner{position:relative;height:112px;margin:-20px -20px 6px;border-radius:15px 15px 0 0;overflow:hidden}
    .far-banner img{width:100%;height:100%;object-fit:cover;object-position:center 35%;display:block;transform:scale(1.04);animation:far-lento 14s ease-in-out infinite alternate}
    .far-banner::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.05) 25%,var(--far-panel2,#0c141d) 100%)}
    .far-title{position:relative;margin:0 0 4px;font-size:1.15rem;line-height:1.2;font-family:var(--far-fuente,inherit);font-weight:700;color:var(--far-acento,#fff);letter-spacing:var(--far-trazo,0);text-shadow:0 2px 10px rgba(0,0,0,.7),0 0 18px rgba(var(--far-brillo,255,210,122),.28)}
    .far-box.sinbanner .far-title{margin-top:2px}
    .far-banner + .far-title{margin-top:-30px}
    .far-divisor{display:flex;align-items:center;gap:8px;margin:2px auto 8px;max-width:260px;color:var(--far-acento,#ffd27a);opacity:.9}
    .far-divisor::before,.far-divisor::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,transparent,var(--far-acento,#ffd27a))}
    .far-divisor::after{background:linear-gradient(270deg,transparent,var(--far-acento,#ffd27a))}
    .far-divisor i{font-style:normal;font-size:.7rem;line-height:1}
    .far-instr{position:relative;margin:0 0 14px;color:#d8e2ee;font-size:.9rem}
    .far-body,.far-feedback,.far-actions{position:relative}
    .far-feedback{min-height:1.4em;margin:10px 0;font-weight:700}
    .far-feedback.ok{color:#9dffb0;text-shadow:0 0 14px rgba(120,255,160,.35)}
    .far-feedback.bad{color:#ffb3b3}
    .far-actions{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
    .far-btn{padding:10px 16px;border-radius:10px;border:none;font-weight:700;cursor:pointer;font-family:inherit;transition:transform .12s,filter .12s}
    .far-btn:hover:not(:disabled){filter:brightness(1.08)}.far-btn:active:not(:disabled){transform:translateY(1px) scale(.98)}
    .far-btn.primary{background:var(--far-boton,linear-gradient(180deg,#ffd27a,#f0a020));color:var(--far-botontxt,#2a1600);box-shadow:0 4px 14px rgba(var(--far-brillo,255,210,122),.25)}
    .far-btn.ghost{background:rgba(255,255,255,.07);color:#fff;border:1px solid rgba(var(--far-brillo,255,255,255),.28)}
    .far-btn:disabled{opacity:.5;cursor:not-allowed}
    .far-btn:focus-visible,.far-key:focus-visible{outline:2px solid var(--far-acento,#ffd27a);outline-offset:2px}
    .far-display{font-size:1.8rem;font-weight:800;letter-spacing:6px;background:rgba(0,0,0,.32);border:1px solid rgba(var(--far-brillo,255,255,255),.22);border-radius:10px;padding:10px 0;margin-bottom:14px;min-height:3.1rem;box-shadow:inset 0 2px 12px rgba(0,0,0,.5)}
    .far-keypad{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px}
    .far-keyboard{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;margin-bottom:12px}
    .far-key{background:linear-gradient(180deg,rgba(255,255,255,.12),rgba(255,255,255,.03));border:1px solid rgba(var(--far-brillo,255,255,255),.2);color:#fff;padding:12px 0;border-radius:9px;font-size:1.05rem;font-weight:700;cursor:pointer;font-family:inherit;transition:transform .1s,background .15s}
    .far-key:active{transform:translateY(1px) scale(.97)}
    .far-key:hover:not(:disabled){background:linear-gradient(180deg,rgba(var(--far-brillo,255,255,255),.2),rgba(255,255,255,.04))}
    .far-key:disabled{opacity:.45;cursor:not-allowed}
    .far-overlay .far-hoja.papiro,.far-overlay[data-tema="faro"] .far-hoja{background-image:linear-gradient(rgba(246,232,190,.62),rgba(246,232,190,.62)),var(--far-papel);background-size:cover;background-position:center;background-blend-mode:multiply}
    .far-overlay[data-mayus="1"] .far-title{text-transform:uppercase;font-size:1.02rem}
    .far-overlay[data-tema="florencia"] .far-title{font-size:1.5rem;font-style:italic}
    .far-overlay[data-tema="marte"] .far-display{font-family:"Orbitron","IBM Plex Mono",ui-monospace,monospace;color:#ffb085}
    .far-overlay[data-tema="faro"] .far-key{background:linear-gradient(180deg,rgba(255,255,255,.11),rgba(0,0,0,.18));border:1.5px solid rgba(201,164,90,.55);box-shadow:inset 0 1px 0 rgba(255,255,255,.18),0 3px 0 rgba(0,0,0,.45)}
    .far-overlay[data-tema="egipto"] .far-key{background:linear-gradient(180deg,#76603a,#4d3c20);border:1px solid #d9a441;color:#f6e7bf;box-shadow:inset 0 1px 0 rgba(255,235,180,.3),0 3px 0 #2a1f0c;text-shadow:0 1px 0 rgba(0,0,0,.5)}
    .far-overlay[data-tema="marte"] .far-key{border-radius:0;clip-path:polygon(9px 0,100% 0,100% calc(100% - 9px),calc(100% - 9px) 100%,0 100%,0 9px);background:linear-gradient(180deg,rgba(255,138,80,.24),rgba(255,138,80,.06));border:1px solid rgba(255,138,80,.7);font-family:"Orbitron","Poppins",sans-serif;font-size:.95rem;color:#ffd3b8}
    .far-overlay[data-tema="florencia"] .far-key{background:radial-gradient(circle at 30% 22%,#f7e2a4,#c79a3a 72%);border:1px solid #7a5a1e;color:#2a1600;box-shadow:inset 0 1px 0 rgba(255,255,255,.55),0 3px 0 #5a3f10;text-shadow:0 1px 0 rgba(255,255,255,.35)}
    .far-overlay[data-tema="florencia"] .far-key:disabled{filter:grayscale(.5)}
    .far-overlay[data-tema="dinosaurios"] .far-key{background:linear-gradient(180deg,#6f8d45,#3d5a24);border:1px solid #b5e35b;color:#f2ffd6;box-shadow:inset 0 1px 0 rgba(235,255,190,.35),0 3px 0 #1f3410;text-shadow:0 1px 0 rgba(0,0,0,.5)}
    .far-overlay[data-tema="dinosaurios"] .far-title{font-size:1.25rem}
    .far-overlay[data-tema="cuento"] .far-title{font-size:1.3rem}
    .far-overlay[data-tema="cuento"] .far-key{background:linear-gradient(180deg,#8a63d8,#5a3aa8);border:1px solid #ffe08a;color:#fff7d6;box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 3px 0 #2c1a66;text-shadow:0 1px 0 rgba(0,0,0,.4);border-radius:14px}
    .far-overlay[data-tema="trono"] .far-title{font-size:1.2rem;letter-spacing:.05em}
    .far-overlay[data-tema="trono"] .far-key{background:linear-gradient(180deg,#56626e,#2c343c);border:1px solid #9fb8cc;color:#e6f1f9;box-shadow:inset 0 1px 0 rgba(255,255,255,.25),0 3px 0 #0f1318;text-shadow:0 1px 0 rgba(0,0,0,.55);border-radius:4px}
    .far-copo{position:absolute;top:-10px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.95),rgba(255,255,255,0));animation:far-nieve linear infinite}
    @keyframes far-nieve{0%{transform:translate(0,0);opacity:0}10%{opacity:.9}100%{transform:translate(-40px,112vh);opacity:.3}}
    .far-sonido{position:absolute;top:10px;right:34px;z-index:6;width:30px;height:30px;border-radius:50%;border:1px solid rgba(255,255,255,.35);background:rgba(0,0,0,.45);color:#fff;font-size:.95rem;line-height:1;cursor:pointer;padding:0}
    .far-sonido:hover{background:rgba(0,0,0,.65)}
    .far-overlay[data-escaneo="1"] .far-box::after{content:"";position:absolute;inset:0;border-radius:16px;background:repeating-linear-gradient(0deg,rgba(255,255,255,.035) 0 1px,transparent 1px 3px);pointer-events:none;z-index:4;animation:far-parpadeo 5s steps(1) infinite}
    .far-vela{position:absolute;left:-60px;bottom:-60px;width:340px;height:340px;border-radius:50%;background:radial-gradient(circle,rgba(255,170,70,.34),transparent 65%);animation:far-llama 2.8s ease-in-out infinite alternate;pointer-events:none}
    /* partículas */
    .far-gota{position:absolute;top:-30px;width:1px;height:22px;background:linear-gradient(180deg,transparent,rgba(190,215,255,.55));transform:rotate(12deg);animation:far-caer linear infinite}
    .far-niebla{position:absolute;width:70%;height:34%;border-radius:50%;background:radial-gradient(ellipse,rgba(180,205,225,.14),transparent 70%);animation:far-deriva 22s ease-in-out infinite alternate}
    .far-mota{position:absolute;bottom:-10px;border-radius:50%;background:radial-gradient(circle,rgba(255,230,150,.95),rgba(255,200,90,0));animation:far-flota ease-in-out infinite}
    .far-racha{position:absolute;left:-60px;height:1.5px;width:44px;background:linear-gradient(90deg,transparent,rgba(255,150,100,.7));animation:far-viento linear infinite}
    .far-chispa{position:absolute;bottom:-8px;border-radius:50%;background:radial-gradient(circle,#ffcf7a,rgba(255,120,30,0));animation:far-sube-chispa ease-out infinite}
    .far-burst{position:absolute;left:50%;top:38%;width:0;height:0;pointer-events:none;z-index:6}
    .far-burst span{position:absolute;color:var(--far-acento,#ffd27a);font-size:1.1rem;text-shadow:0 0 12px rgba(var(--far-brillo,255,210,122),1),0 0 26px rgba(var(--far-brillo,255,210,122),.7);animation:far-estalla 1.3s ease-out forwards}
    .far-box.far-ganado{animation:far-glow 1.6s ease-out}
    .far-box.far-error{animation:far-sacude .4s}
    @keyframes far-entra{from{opacity:0}to{opacity:1}}
    @keyframes far-sube{from{opacity:0;transform:translateY(22px) scale(.97)}to{opacity:1;transform:none}}
    @keyframes far-lento{from{transform:scale(1.04) translate(0,0)}to{transform:scale(1.14) translate(-6px,-3px)}}
    @keyframes far-caer{to{transform:translate(40px,115vh) rotate(12deg)}}
    @keyframes far-deriva{from{transform:translateX(-14%)}to{transform:translateX(30%)}}
    @keyframes far-flota{0%{transform:translate(0,0);opacity:0}15%{opacity:.9}60%{transform:translate(18px,-55vh);opacity:.7}100%{transform:translate(-14px,-110vh);opacity:0}}
    @keyframes far-viento{to{transform:translateX(120vw)}}
    @keyframes far-sube-chispa{0%{transform:translate(0,0);opacity:0}12%{opacity:1}100%{transform:translate(22px,-92vh);opacity:0}}
    @keyframes far-llama{from{opacity:.55;transform:scale(.94)}to{opacity:1;transform:scale(1.06)}}
    @keyframes far-parpadeo{0%,92%,100%{opacity:1}94%{opacity:.4}96%{opacity:.9}}
    @keyframes far-estalla{from{transform:translate(0,0) scale(.4);opacity:1}to{transform:translate(var(--dx),var(--dy)) scale(1.2) rotate(120deg);opacity:0}}
    @keyframes far-glow{0%{box-shadow:0 22px 70px rgba(0,0,0,.65),0 0 0 rgba(var(--far-brillo),0)}35%{box-shadow:0 22px 70px rgba(0,0,0,.65),0 0 90px rgba(var(--far-brillo),.7),inset 0 0 40px rgba(var(--far-brillo),.25)}100%{box-shadow:0 22px 70px rgba(0,0,0,.65),0 0 46px rgba(var(--far-brillo),.14),inset 0 0 0 4px rgba(0,0,0,.28),inset 0 0 0 5px rgba(var(--far-brillo),.22)}}
    @keyframes far-sacude{0%,100%{transform:translateX(0)}20%{transform:translateX(-7px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(3px)}}
    @media (prefers-reduced-motion:reduce){.far-overlay,.far-box,.far-banner img,.far-vela{animation:none!important}}
    @media (max-height:640px){.far-banner{height:84px}}
  `;
  document.head.appendChild(s);
}

// ---- sonido: acordes breves de acierto y fallo (WebAudio), con interruptor persistente ----
let ctxAudio = null;
function sonidoActivo() {
  try { return localStorage.getItem('far-sonido') !== '0'; } catch (e) { return true; }
}
function guardarSonido(v) {
  try { localStorage.setItem('far-sonido', v ? '1' : '0'); } catch (e) { /* ignore */ }
}
const SONIDO = {
  faro: { onda: 'triangle', base: 392 },
  egipto: { onda: 'sine', base: 440 },
  marte: { onda: 'square', base: 330 },
  florencia: { onda: 'sine', base: 392 },
  dinosaurios: { onda: 'triangle', base: 349 },
  cuento: { onda: 'sine', base: 523 },
  trono: { onda: 'sawtooth', base: 294 }
};
function sonar(tipo, tema) {
  if (!sonidoActivo()) return;
  try {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    ctxAudio = ctxAudio || new AC();
    if (ctxAudio.state === 'suspended') ctxAudio.resume();
    const cfg = SONIDO[tema] || SONIDO.faro;
    const notas = tipo === 'ok' ? [1, 1.25, 1.5, 2] : [0.5, 0.375];
    const onda = tipo === 'ok' ? cfg.onda : 'sawtooth';
    const dur = tipo === 'ok' ? 0.16 : 0.18;
    const t0 = ctxAudio.currentTime + 0.02;
    notas.forEach((m, i) => {
      const o = ctxAudio.createOscillator();
      const g = ctxAudio.createGain();
      const f = ctxAudio.createBiquadFilter();
      o.type = onda;
      o.frequency.value = cfg.base * m;
      f.type = 'lowpass';
      f.frequency.value = tipo === 'ok' ? 3200 : 900;
      const ini = t0 + i * (tipo === 'ok' ? 0.11 : 0.14);
      g.gain.setValueAtTime(0.0001, ini);
      g.gain.exponentialRampToValueAtTime(tipo === 'ok' ? 0.12 : 0.07, ini + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, ini + dur + (i === notas.length - 1 ? 0.35 : 0));
      o.connect(f); f.connect(g); g.connect(ctxAudio.destination);
      o.start(ini);
      o.stop(ini + dur + 0.45);
    });
  } catch (e) { /* sin audio: no pasa nada */ }
}

function aleatorio(a, b) { return a + Math.random() * (b - a); }

function particulas(cont, tipo) {
  if (sinMovimiento()) return;
  const crea = (clase, estilo) => { const e = document.createElement('span'); e.className = clase; Object.assign(e.style, estilo); cont.appendChild(e); return e; };
  if (tipo === 'lluvia') {
    for (let i = 0; i < 34; i++) crea('far-gota', { left: aleatorio(-5, 105) + '%', animationDuration: aleatorio(0.7, 1.5) + 's', animationDelay: -aleatorio(0, 1.5) + 's', opacity: String(aleatorio(0.3, 0.9)) });
    for (let i = 0; i < 3; i++) crea('far-niebla', { left: aleatorio(-20, 60) + '%', top: aleatorio(10, 70) + '%', animationDuration: aleatorio(18, 30) + 's', animationDelay: -aleatorio(0, 18) + 's' });
  } else if (tipo === 'polvo') {
    for (let i = 0; i < 24; i++) { const t = aleatorio(2, 5); crea('far-mota', { left: aleatorio(0, 100) + '%', width: t + 'px', height: t + 'px', animationDuration: aleatorio(9, 18) + 's', animationDelay: -aleatorio(0, 18) + 's' }); }
  } else if (tipo === 'racha') {
    for (let i = 0; i < 18; i++) crea('far-racha', { top: aleatorio(0, 100) + '%', width: aleatorio(28, 90) + 'px', animationDuration: aleatorio(2.2, 5) + 's', animationDelay: -aleatorio(0, 5) + 's', opacity: String(aleatorio(0.25, 0.8)) });
  } else if (tipo === 'nieve') {
    for (let i = 0; i < 40; i++) { const t = aleatorio(2, 5); crea('far-copo', { left: aleatorio(0, 105) + '%', width: t + 'px', height: t + 'px', animationDuration: aleatorio(6, 14) + 's', animationDelay: -aleatorio(0, 14) + 's' }); }
  } else if (tipo === 'chispa') {
    for (let i = 0; i < 22; i++) { const t = aleatorio(2, 4); crea('far-chispa', { left: aleatorio(0, 100) + '%', width: t + 'px', height: t + 'px', animationDuration: aleatorio(5, 11) + 's', animationDelay: -aleatorio(0, 11) + 's' }); }
  }
}

export function openGame({ title, instr, pauseGameTimer, resumeGameTimer, onClose }) {
  injectStyle();
  injectFonts();
  if (typeof pauseGameTimer === 'function') pauseGameTimer();

  const tema = detectarTema();
  const T = TEMAS[tema];

  const overlay = document.createElement('div');
  overlay.className = 'far-overlay';
  overlay.dataset.tema = tema;
  overlay.dataset.mayus = T.mayus ? '1' : '0';
  overlay.dataset.escaneo = T.escaneo ? '1' : '0';
  const vars = {
    '--far-tinte': T.tinte, '--far-panel': 'linear-gradient(180deg,' + T.panel + ',' + T.panel2 + ')', '--far-panel2': T.panel2,
    '--far-borde': T.borde, '--far-acento': T.acento, '--far-brillo': T.brillo, '--far-boton': T.boton, '--far-botontxt': T.botonTxt,
    '--far-fuente': T.fuente, '--far-trazo': T.trazo
  };
  if (T.papel) vars['--far-papel'] = 'url("./img/ui/' + T.papel + '")';
  Object.keys(vars).forEach(k => overlay.style.setProperty(k, vars[k]));

  const num = (String(title).match(/Carta\s+([0-9P]+)/) || [])[1];
  overlay.innerHTML =
    '<div class="far-bg"></div><div class="far-ambiente"></div>' +
    '<div class="far-box" role="dialog" aria-modal="true">' +
    '<button type="button" class="far-sonido" aria-label="Sonido"></button><div class="far-textura"></div><i class="far-esq a"></i><i class="far-esq b"></i><i class="far-esq c"></i><i class="far-esq d"></i>' +
    (num ? '<div class="far-banner"><img alt="" src="./img/' + num + '.jpg"></div>' : '') +
    '<h3 class="far-title"></h3><div class="far-divisor"><i>' + T.simbolo + '</i></div><p class="far-instr"></p>' +
    '<div class="far-body"></div><div class="far-feedback" aria-live="polite"></div><div class="far-actions"></div></div>';
  overlay.querySelector('.far-title').textContent = title;
  overlay.querySelector('.far-instr').textContent = instr;
  const box = overlay.querySelector('.far-box');
  if (!num) box.classList.add('sinbanner');
  if (num) {
    const bg = overlay.querySelector('.far-bg');
    bg.style.backgroundImage = 'url("./img/' + num + '.jpg")';
    const img = overlay.querySelector('.far-banner img');
    img.addEventListener('error', () => { const b = overlay.querySelector('.far-banner'); if (b) b.remove(); bg.style.backgroundImage = 'none'; box.classList.add('sinbanner'); });
  }
  const btnSonido = overlay.querySelector('.far-sonido');
  const pintarSonido = () => { btnSonido.textContent = sonidoActivo() ? '🔊' : '🔇'; btnSonido.title = sonidoActivo() ? 'Silenciar' : 'Activar sonido'; };
  btnSonido.addEventListener('click', () => { guardarSonido(!sonidoActivo()); pintarSonido(); if (sonidoActivo()) sonar('ok', tema); });
  pintarSonido();
  overlay.querySelector('.far-textura').style.backgroundImage = 'url("./img/ui/' + T.textura + '")';
  const ambiente = overlay.querySelector('.far-ambiente');
  if (T.vela && !sinMovimiento()) { const v = document.createElement('div'); v.className = 'far-vela'; ambiente.appendChild(v); }
  particulas(ambiente, T.particulas);
  document.body.appendChild(overlay);

  const body = overlay.querySelector('.far-body');
  const feedback = overlay.querySelector('.far-feedback');
  const actions = overlay.querySelector('.far-actions');
  const closers = [];
  let closed = false;
  let celebrado = false;

  function close() {
    if (closed) return;
    closed = true;
    closers.forEach(fn => { try { fn(); } catch (e) { /* ignore */ } });
    document.removeEventListener('keydown', onKey);
    overlay.remove();
    if (typeof resumeGameTimer === 'function') resumeGameTimer();
    if (typeof onClose === 'function') onClose();
  }
  function onKey(e) { if (e.key === 'Escape') close(); }
  document.addEventListener('keydown', onKey);

  function button(label, kind, fn) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-btn ' + kind;
    b.textContent = label;
    b.addEventListener('click', fn);
    actions.appendChild(b);
    return b;
  }
  button('Cerrar', 'ghost', close);

  function celebrar() {
    if (celebrado) return;
    celebrado = true;
    box.classList.remove('far-error');
    box.classList.add('far-ganado');
    sonar('ok', tema);
    try { if (navigator.vibrate) navigator.vibrate([40, 30, 60]); } catch (e) { /* ignore */ }
    if (sinMovimiento()) return;
    const r = document.createElement('div');
    r.className = 'far-burst';
    for (let i = 0; i < 38; i++) {
      const p = document.createElement('span');
      p.textContent = T.simbolo;
      const a = Math.random() * Math.PI * 2;
      const d = aleatorio(80, 230);
      p.style.setProperty('--dx', Math.cos(a) * d + 'px');
      p.style.setProperty('--dy', Math.sin(a) * d - 30 + 'px');
      p.style.animationDelay = aleatorio(0, 0.25) + 's';
      p.style.fontSize = aleatorio(0.9, 2.1) + 'rem';
      r.appendChild(p);
    }
    box.appendChild(r);
    setTimeout(() => r.remove(), 1900);
  }

  function fallar() {
    sonar('bad', tema);
    box.classList.remove('far-error');
    void box.offsetWidth;
    box.classList.add('far-error');
    setTimeout(() => box.classList.remove('far-error'), 450);
  }

  return {
    body,
    button,
    close,
    onClose(fn) { closers.push(fn); },
    /** Cambia la textura del panel por una propia del minijuego (./img/ui/<nombre>). */
    textura(nombre, { opacidad = 0.45, mezcla = 'normal' } = {}) {
      const tx = overlay.querySelector('.far-textura');
      tx.style.backgroundImage = 'url("./img/ui/' + nombre + '")';
      tx.style.opacity = String(opacidad);
      tx.style.mixBlendMode = mezcla;
    },
    say(text, kind) {
      feedback.textContent = text;
      feedback.className = 'far-feedback' + (kind ? ' ' + kind : '');
      if (text && kind === 'ok') celebrar();
      else if (text && kind === 'bad') fallar();
    }
  };
}

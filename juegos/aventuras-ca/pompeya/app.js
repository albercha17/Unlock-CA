// app.js — lógica de la app de Unlock C&A / Aventuras C&A. Común a todos los juegos: se edita en juegos/el-faro y se propaga con
// herramientas/regenerar_index.py. La configuración de cada juego (segundos, carta final, minijuegos) está en window.APP_CONFIG (index.html).

import { crearMusica } from './musica.js';

const CFG = Object.assign({ juego: '', assets: '../../assets/', segundos: 3600, dificultad: 0, final: '99', volver: '../index.html', minijuegos: {} }, window.APP_CONFIG || {});
const NIVELES = ['', 'Muy fácil', 'Fácil', 'Media', 'Difícil', 'Muy difícil'];
const $ = (id) => document.getElementById(id);
const TEMA = document.documentElement.dataset.tema || 'faro';
const TITULO = (document.querySelector('[data-juego-titulo]') || {}).textContent || document.title;
const CLAVE_GUARDADO = 'ca-partida:' + location.pathname.replace(/index\.html$/, '');
const CLAVE_RELOJ = 'ca-reloj-oculto';
const CLAVE_MUSICA = 'ca-musica';
const musica = crearMusica(TEMA);
const volumenAjustado = () => { try { return window.CA_AJUSTES ? window.CA_AJUSTES.leer().volMusica : 0.5; } catch (e) { return 0.5; } };
musica.volumen(volumenAjustado());
window.addEventListener('ca-ajustes', () => musica.volumen(volumenAjustado()));
let musicaOn = true;
try { musicaOn = localStorage.getItem(CLAVE_MUSICA) !== '0'; } catch (e) { /* por defecto, con música */ }

// texto del reloj según la historia (el reloj es parte del juego, no solo un número)
const ETIQUETA_RELOJ = {
  faro: 'El carguero se acerca a las rocas',
  egipto: 'Los sacerdotes se acercan al templo',
  marte: 'El oxígeno de la cúpula se agota',
  florencia: 'El alba se acerca',
  dinosaurios: 'El asteroide se acerca',
  pompeya: 'La ceniza se acerca'
};

const REGLAS = [
  '<p><b>Cartas:</b> cada carta tiene un número. Se leen entre los dos y se ponen en la mesa.</p>',
  '<p><b>Coge / Descarta:</b> cuando una carta dice «Coge», buscad esas cartas en el mazo y ponedlas en la mesa; «Descarta» significa apartarlas.</p>',
  '<p><b>Combinar:</b> si dos cartas se pueden combinar, <b>sumad sus números</b>: el resultado es la carta que debéis coger.</p>',
  '<p><b>Acción:</b> si una carta tiene puzle, código o minijuego en la app, escribid su número en Acción.</p>',
  '<p><b>Pista:</b> escribid el número de la carta en la que estáis atascados. Las pistas van de menos a más reveladoras; la última lo resuelve.</p>',
  '<p><b>Cuaderno:</b> la app apunta lo que abrís y tiene un bloc para vuestras notas. La partida se guarda sola.</p>'
].join('');

// ---------------------------------------------------------------- utilidades
function leerGuardado() {
  try { return JSON.parse(localStorage.getItem(CLAVE_GUARDADO) || 'null'); } catch (e) { return null; }
}
function escribirGuardado(valor) {
  try {
    if (valor === null) localStorage.removeItem(CLAVE_GUARDADO);
    else localStorage.setItem(CLAVE_GUARDADO, JSON.stringify(valor));
  } catch (e) { /* sin almacenamiento: la partida sigue, solo no se guarda */ }
}
function prefiereMenosMovimiento() {
  if (document.documentElement.getAttribute('data-movimiento') === 'reducido') return true; // ajuste de la app
  return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
}
function pitido(freq, ms, tipo = 'sine', vol = 0.06) {
  try {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    pitido.ctx = pitido.ctx || new AC();
    const ctx = pitido.ctx;
    if (ctx.state === 'suspended') ctx.resume();
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = tipo;
    osc.frequency.value = freq;
    g.gain.setValueAtTime(vol, ctx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + ms / 1000);
    osc.connect(g).connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + ms / 1000);
  } catch (e) { /* sin audio */ }
}
function vibrar(patron) {
  try { if (navigator.vibrate) navigator.vibrate(patron); } catch (e) { /* iOS no lo tiene */ }
}
function textoDuracion(seg) {
  const m = Math.round(seg / 60);
  if (m === 60) return '1 hora';
  if (m % 60 === 0) return (m / 60) + ' horas';
  return m + ' minutos';
}
function formatTime(s) {
  const neg = s < 0;
  const n = Math.ceil(Math.abs(s));
  const h = Math.floor(n / 3600).toString().padStart(2, '0');
  const m = Math.floor((n % 3600) / 60).toString().padStart(2, '0');
  const sec = Math.floor(n % 60).toString().padStart(2, '0');
  return `${neg ? '+' : ''}${h}:${m}:${sec}`;
}
function mmss(s) {
  const n = Math.max(0, Math.round(s));
  return `${Math.floor(n / 60)}:${String(n % 60).padStart(2, '0')}`;
}

// ---------------------------------------------------------------- elementos
const introPanel = $('introPanel');
const gamePanel = $('gamePanel');
const finalPanel = $('finalPanel');
const startBtn = $('startBtn');
const continueBtn = $('continueBtn');
const gameTimerEl = $('gameTimer');
const relojEl = $('reloj');
const actionBtn = $('actionBtn');
const hintBtn = $('hintBtn');
const pauseBtn = $('pauseBtn');
const resumeBtn = $('resumeBtn');
const stopBtn = $('stopBtn');
const numModal = $('numModal');
const numDisplay = $('numDisplay');
const numTitulo = $('numTitulo');
const numMessage = $('numMessage');
const numKeys = Array.from(document.querySelectorAll('.num-key'));
const numOk = $('numOk');
const numCancel = $('numCancel');
const numClear = $('numClear');
const openAnywayWrap = $('openAnywayWrap');
const sysDialog = $('sysDialog');
const sysDialogMsg = $('sysDialogMsg');
const sysOkBtn = $('sysOkBtn');
const sysCancelBtn = $('sysCancelBtn');

// ---------------------------------------------------------------- estado de la partida
const TOTAL = CFG.segundos;
let estado = nuevoEstado();
let intervalId = null;
let isPaused = false;
let ultimoTick = 0;
let ticksDesdeGuardado = 0;
let avisoTiempoMostrado = false;
let partidaIniciada = false;
let entered = '';
let pendingUse = null;
let cartas = null; // cartas.json (títulos para el teclado y el registro)

function nuevoEstado() {
  return { v: 1, restante: TOTAL, log: [], pistas: {}, sinEfecto: 0, notas: '', empezada: Date.now(), fin: null };
}
function guardar() {
  if (!estado || estado.fin) return;
  escribirGuardado(estado);
}
async function cargarCartas() {
  if (cartas) return cartas;
  try {
    const r = await fetch('./cartas.json', { cache: 'no-store' });
    cartas = r.ok ? await r.json() : {};
  } catch (e) {
    cartas = {};
  }
  return cartas;
}
function tituloCarta(num) {
  const c = cartas && cartas[String(num)];
  return c && c.titulo ? c.titulo : `Carta ${num}`;
}
function soloNombre(titulo) {
  const partes = String(titulo).split('—');
  return (partes.length > 1 ? partes.slice(1).join('—') : titulo).replace(/\s*\(FIN\)\s*/i, '').trim();
}

// ---------------------------------------------------------------- reloj
function actualizarReloj() {
  const gastado = TOTAL - estado.restante;
  gameTimerEl.textContent = formatTime(estado.restante);
  const frac = Math.max(0, Math.min(1, gastado / TOTAL));
  $('relojBarra').style.width = (frac * 100) + '%';
  $('relojMarca').style.left = (frac * 100) + '%';
  const urgente = estado.restante > 0 && (estado.restante <= 300 || frac >= 0.9);
  relojEl.classList.toggle('urgente', urgente && !prefiereMenosMovimiento());
  if (prefiereMenosMovimiento()) gameTimerEl.style.color = urgente ? '#ff9d9d' : '#fff';
  relojEl.classList.toggle('tarde', estado.restante <= 0);
  const abiertas = estado.log.filter((e) => e.uso === 'accion' && e.card !== String(CFG.final)).length;
  const pistas = Object.values(estado.pistas).reduce((a, b) => a + b, 0);
  $('resumen').textContent = `Cartas abiertas: ${abiertas} · Pistas pedidas: ${pistas}`;
}
function tick() {
  const ahora = Date.now();
  const dt = (ahora - ultimoTick) / 1000;
  ultimoTick = ahora;
  if (isPaused || estado.fin) return;
  estado.restante -= dt;
  if (estado.restante <= 0 && !avisoTiempoMostrado) {
    avisoTiempoMostrado = true;
    pitido(220, 600, 'sawtooth');
    vibrar([200, 100, 200]);
    showSysDialog('Se acabó el tiempo. Podéis seguir jugando: el reloj cuenta el tiempo de más y quedará anotado en el informe.', { okText: 'Seguir jugando' });
  }
  actualizarReloj();
  if (++ticksDesdeGuardado >= 5) { ticksDesdeGuardado = 0; guardar(); }
}
function arrancarReloj() {
  if (intervalId) clearInterval(intervalId);
  ultimoTick = Date.now();
  intervalId = setInterval(tick, 1000);
}

// ---------------------------------------------------------------- pantalla encendida
let wakeLock = null;
async function pedirPantallaEncendida() {
  try {
    if (!('wakeLock' in navigator) || estado.fin) return;
    wakeLock = await navigator.wakeLock.request('screen');
    wakeLock.addEventListener('release', () => { wakeLock = null; });
  } catch (e) { /* batería baja o sin permiso: no pasa nada */ }
}
function soltarPantalla() {
  try { if (wakeLock) wakeLock.release(); } catch (e) { /* nada */ }
  wakeLock = null;
}
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible' && partidaIniciada && !estado.fin) { pedirPantallaEncendida(); musica.reanudar(); }
  else if (document.visibilityState === 'hidden') musica.suspender();
});

// ---------------------------------------------------------------- inicio de partida
function prepararPantallaJuego() {
  introPanel.style.display = 'none';
  finalPanel.style.display = 'none';
  gamePanel.style.display = 'block';
  pauseBtn.style.display = 'inline-flex';
  resumeBtn.style.display = 'none';
  isPaused = false;
  avisoTiempoMostrado = estado.restante <= 0;
  $('notasTexto').value = estado.notas || '';
  actualizarReloj();
  arrancarReloj();
  pedirPantallaEncendida();
  if (musicaOn) musica.iniciar();
  guardar();
  window.scrollTo(0, 0);
}
function empezarPartida() {
  if (partidaIniciada) return;
  partidaIniciada = true;
  try { introVideo.pause(); } catch (e) { /* ignore */ }
  videoOverlay.style.display = 'none';
  estado = nuevoEstado();
  prepararPantallaJuego();
}

const videoOverlay = $('videoOverlay');
const introVideo = $('introVideo');
const skipVideoBtn = $('skipVideoBtn');

// El vídeo de introducción va en ./video/videoInicial.mp4. Si no existe o falla, la partida empieza igual.
startBtn.addEventListener('click', () => {
  pitido(660, 90);
  partidaIniciada = false;
  videoOverlay.style.display = 'flex';
  try {
    introVideo.currentTime = 0;
    const p = introVideo.play();
    if (p && typeof p.catch === 'function') {
      p.catch(() => {
        if (introVideo.error) empezarPartida();
        else introVideo.setAttribute('controls', 'controls');
      });
    }
  } catch (e) {
    empezarPartida();
  }
});
introVideo.addEventListener('ended', empezarPartida);
introVideo.addEventListener('error', () => {
  if (videoOverlay.style.display === 'flex') empezarPartida();
});
skipVideoBtn.addEventListener('click', empezarPartida);

continueBtn.addEventListener('click', () => {
  const g = leerGuardado();
  if (!g || !Array.isArray(g.log)) return;
  pitido(660, 90);
  estado = g;
  partidaIniciada = true;
  prepararPantallaJuego();
});

// ---------------------------------------------------------------- gestos: deslizar hacia abajo para cerrar una hoja
function gestoCerrar(caja, cerrar) {
  let y0 = null, dy = 0, t0 = 0;
  caja.addEventListener('touchstart', (e) => {
    const r = caja.getBoundingClientRect();
    const t = e.touches[0];
    if (t.clientY - r.top > 64 || caja.scrollTop > 0) { y0 = null; return; }
    y0 = t.clientY; dy = 0; t0 = Date.now(); caja.style.transition = 'none';
  }, { passive: true });
  caja.addEventListener('touchmove', (e) => {
    if (y0 === null) return;
    dy = Math.max(0, e.touches[0].clientY - y0);
    caja.style.transform = 'translateY(' + dy + 'px)';
  }, { passive: true });
  const fin = () => {
    if (y0 === null) return;
    caja.style.transition = 'transform .2s ease';
    const rapido = dy / Math.max(1, Date.now() - t0) > 0.6;
    const cierra = dy > 90 || (dy > 30 && rapido);
    caja.style.transform = '';
    y0 = null; dy = 0;
    if (cierra) cerrar();
  };
  caja.addEventListener('touchend', fin);
  caja.addEventListener('touchcancel', fin);
}
function toquecito() { try { if (navigator.vibrate) navigator.vibrate(6); } catch (e) { /* iPhone no vibra */ } }

// ---------------------------------------------------------------- teclado de cartas
function renderNum() {
  numDisplay.textContent = entered === '' ? '—' : entered;
  numTitulo.textContent = '';
  const c = entered && cartas ? cartas[entered.toUpperCase() === 'P' ? 'P' : String(Number(entered))] : null;
  if (!c || !c.titulo || !/^(P|\d+)$/i.test(entered)) return;
  if (String(Number(entered)) === String(CFG.final) && pendingUse === 'pista') return; // sin destripar el final
  if (pendingUse === 'accion' && !CFG.minijuegos[String(Number(entered))]) return; // solo confirma las cartas con app
  numTitulo.textContent = soloNombre(c.titulo);
}
function openNumModal() {
  entered = '';
  numMessage.textContent = '';
  renderNum();
  numModal.classList.remove('closing');
  numModal.style.display = 'flex';
  numModal.setAttribute('aria-hidden', 'false');
  openAnywayWrap.style.display = location.protocol === 'file:' ? 'block' : 'none';
  const first = numKeys.find((k) => !k.classList.contains('action'));
  if (first) first.focus();
}
function closeNumModalImmediate() {
  numModal.style.display = 'none';
  numModal.classList.remove('closing');
  numModal.setAttribute('aria-hidden', 'true');
  actionBtn.focus();
}
function closeNumModal() {
  numModal.classList.add('closing');
  numModal.setAttribute('aria-hidden', 'true');
  setTimeout(closeNumModalImmediate, 150);
}
function cancelNumModal() {
  pendingUse = null;
  closeNumModal();
}
function mostrarErrorNum(texto) {
  numMessage.textContent = texto;
  numModal.style.display = 'flex';
  numModal.setAttribute('aria-hidden', 'false');
  pitido(180, 160, 'square', 0.04);
  vibrar(60);
}

numKeys.forEach((k) => {
  k.addEventListener('click', () => {
    const key = k.dataset.key;
    if (!key || entered.length >= 4) return;
    toquecito();
    entered += key;
    renderNum();
  });
});
numClear.addEventListener('click', () => { entered = entered.slice(0, -1); renderNum(); });
numCancel.addEventListener('click', cancelNumModal);
gestoCerrar(document.querySelector('.num-modal-box'), cancelNumModal);

// escáner de cartas (QR de la esquina de cada carta impresa); el teclado sigue siendo la alternativa
const scanBtn = $('scanBtn');
if (scanBtn && navigator.mediaDevices && navigator.mediaDevices.getUserMedia && location.protocol !== 'file:') {
  scanBtn.hidden = false;
  scanBtn.addEventListener('click', async () => {
    numMessage.textContent = '';
    try {
      const mod = await import(new URL(CFG.assets + 'js/escaner.js', import.meta.url).href);
      const r = await mod.escanear({ juego: CFG.juego || TEMA });
      if (r.id) { entered = r.id; renderNum(); } else if (r.error) { numMessage.textContent = r.error; }
    } catch (e) { numMessage.textContent = 'No se pudo abrir el escáner. Escribe el número de la carta.'; }
  });
}

actionBtn.addEventListener('click', async () => { pendingUse = 'accion'; await cargarCartas(); openNumModal(); });
hintBtn.addEventListener('click', async () => { pendingUse = 'pista'; await cargarCartas(); openNumModal(); });

// ---------------------------------------------------------------- diálogos
function showSysDialog(message, { showCancel = false, okText = 'Aceptar', cancelText = 'Cancelar' } = {}) {
  return new Promise((resolve) => {
    sysDialogMsg.textContent = message;
    sysOkBtn.textContent = okText;
    sysCancelBtn.textContent = cancelText;
    sysCancelBtn.style.display = showCancel ? 'inline-block' : 'none';
    sysDialog.style.display = 'flex';
    sysDialog.setAttribute('aria-hidden', 'false');
    sysOkBtn.focus();
    function cleanup() {
      sysDialog.style.display = 'none';
      sysDialog.setAttribute('aria-hidden', 'true');
      sysOkBtn.removeEventListener('click', onOk);
      sysCancelBtn.removeEventListener('click', onCancel);
    }
    function onOk() { cleanup(); resolve({ ok: true }); }
    function onCancel() { cleanup(); resolve({ ok: false }); }
    sysOkBtn.addEventListener('click', onOk);
    sysCancelBtn.addEventListener('click', onCancel);
  });
}
function showAlert(message) {
  try { showSysDialog(message, { showCancel: false, okText: 'Aceptar' }); } catch (e) { console.log(message); }
}
function showConfirm(message) {
  return showSysDialog(message, { showCancel: true, okText: 'Sí', cancelText: 'No' }).then((r) => !!r.ok);
}
window.alert = function (msg) { showAlert(String(msg)); };

// ---------------------------------------------------------------- aceptar carta
function registrar(card, uso) {
  estado.log.push({ card: String(card), uso, t: Math.round(TOTAL - estado.restante) });
  if (uso === 'pista') estado.pistas[card] = (estado.pistas[card] || 0) + 1;
  actualizarReloj();
  guardar();
}

numOk.addEventListener('click', async () => {
  if (!entered || entered.trim() === '') {
    numMessage.textContent = 'Introduce un número.';
    return;
  }
  const card = entered.trim();

  if (pendingUse === 'pista') {
    numMessage.textContent = '';
    try {
      const module = await import('./pistas.js');
      if (module && typeof module.openPistas === 'function') {
        closeNumModal();
        const clave = card.toUpperCase() === 'P' ? 'P' : String(Number(card));
        registrar(clave, 'pista');
        module.openPistas(clave, { onClose: () => { pendingUse = null; hintBtn.focus(); } });
      } else {
        numMessage.textContent = 'No se pudo cargar el sistema de pistas.';
      }
    } catch (err) {
      console.warn('No se pudo cargar el módulo de pistas:', err);
      mostrarErrorNum('No hay pistas para esta carta. Prueba con otra.');
    }
    return;
  }

  await checkAndOpen(card);
  pendingUse = null;
});

async function tryImportModule(modulePath) {
  try {
    const resolvedPath = new URL(modulePath, import.meta.url).href;
    const module = await import(resolvedPath);
    return { ok: true, module };
  } catch (err) {
    return { ok: false, err };
  }
}

async function checkAndOpen(code) {
  numMessage.textContent = '';
  if (code.trim() === '') { mostrarErrorNum('Introduce un número.'); return; }
  if (code.trim().toUpperCase() === 'P') {
    estado.sinEfecto++;
    mostrarErrorNum('La carta P no es de acción. Pide su pista con el botón Pista.');
    return;
  }
  if (!/^\d+$/.test(code)) { mostrarErrorNum('Solo se permiten dígitos.'); return; }
  const c = String(Number(code)); // normaliza '02' -> '2', etc.

  if (c === String(CFG.final)) {
    closeNumModal();
    registrar(c, 'accion');
    mostrarFinal(true);
    return;
  }

  const modulePath = CFG.minijuegos[c];
  if (modulePath) {
    const res = await tryImportModule(modulePath);
    if (!res.ok) {
      console.error(`Error cargando minijuego ${c}:`, res.err);
      mostrarErrorNum(`No se pudo cargar el minijuego (${c}). Comprueba que el archivo exista y usa un servidor local.`);
      return;
    }
    const module = res.module;
    if (typeof module.startMinigame === 'function') {
      closeNumModal();
      registrar(c, 'accion');
      module.startMinigame({
        onClose: () => actionBtn.focus(),
        pauseGameTimer: () => { isPaused = true; musica.duck(true); },
        resumeGameTimer: () => { isPaused = false; musica.duck(false); }
      });
    } else {
      mostrarErrorNum(`Módulo ${c} cargado, pero no exporta startMinigame.`);
    }
    return;
  }

  estado.sinEfecto++;
  guardar();
  mostrarErrorNum('Esa carta no es de acción. Prueba con otra.');
}

document.addEventListener('keydown', (e) => {
  if (numModal.style.display === 'flex') {
    if (e.key === 'Escape') { cancelNumModal(); e.preventDefault(); return; }
    if (e.key === 'Enter') { numOk.click(); e.preventDefault(); return; }
    if (e.key === 'Backspace') { entered = entered.slice(0, -1); renderNum(); e.preventDefault(); return; }
    if (/^[0-9pP]$/.test(e.key) && entered.length < 4) { entered += e.key.toUpperCase(); renderNum(); e.preventDefault(); }
  }
  if (sysDialog.style.display === 'flex' && e.key === 'Escape') {
    if (sysCancelBtn.style.display !== 'none') sysCancelBtn.click();
    else sysOkBtn.click();
  }
});

// ---------------------------------------------------------------- pausa y salida
pauseBtn.addEventListener('click', () => {
  isPaused = true;
  musica.duck(true);
  pauseBtn.style.display = 'none';
  resumeBtn.style.display = 'inline-flex';
});
resumeBtn.addEventListener('click', () => {
  isPaused = false;
  musica.duck(false);
  pauseBtn.style.display = 'inline-flex';
  resumeBtn.style.display = 'none';
});
stopBtn.addEventListener('click', async () => {
  const ok = await showConfirm('¿Salir al inicio? La partida queda guardada y podréis continuarla desde el botón «Continuar partida».');
  if (!ok) return;
  guardar();
  if (intervalId) clearInterval(intervalId);
  soltarPantalla();
  musica.parar();
  partidaIniciada = false;
  introPanel.style.display = 'block';
  gamePanel.style.display = 'none';
  mostrarContinuar();
});

// ---------------------------------------------------------------- reloj oculto
const clockToggle = $('clockToggle');
function aplicarRelojOculto(oculto) {
  relojEl.classList.toggle('oculto', oculto);
  clockToggle.setAttribute('aria-pressed', String(oculto));
  clockToggle.setAttribute('aria-label', oculto ? 'Mostrar el número del reloj' : 'Ocultar el número del reloj');
  try { localStorage.setItem(CLAVE_RELOJ, oculto ? '1' : '0'); } catch (e) { /* nada */ }
}
clockToggle.addEventListener('click', () => aplicarRelojOculto(!relojEl.classList.contains('oculto')));
try { if (localStorage.getItem(CLAVE_RELOJ) === '1') aplicarRelojOculto(true); } catch (e) { /* nada */ }

// ---------------------------------------------------------------- música
const musicBtn = $('musicBtn');
function pintarMusica() {
  musicBtn.setAttribute('aria-pressed', String(musicaOn));
  musicBtn.classList.toggle('apagado', !musicaOn);
  musicBtn.setAttribute('aria-label', musicaOn ? 'Quitar la música de fondo' : 'Poner la música de fondo');
}
musicBtn.addEventListener('click', () => {
  musicaOn = !musicaOn;
  try { localStorage.setItem(CLAVE_MUSICA, musicaOn ? '1' : '0'); } catch (e) { /* nada */ }
  if (musicaOn && partidaIniciada && !estado.fin) musica.iniciar(); else musica.parar();
  pintarMusica();
});
pintarMusica();

// ---------------------------------------------------------------- cuaderno
const cuaderno = $('cuaderno');
function abrirCuaderno(tab) {
  pintarRegistro();
  cuaderno.classList.add('abierto');
  cuaderno.setAttribute('aria-hidden', 'false');
  elegirPestana(tab || 'registro');
}
function cerrarCuaderno() {
  cuaderno.classList.remove('abierto');
  cuaderno.setAttribute('aria-hidden', 'true');
  $('notebookBtn').focus();
}
function elegirPestana(nombre) {
  ['registro', 'notas', 'reglas'].forEach((t) => {
    $('tab' + t[0].toUpperCase() + t.slice(1)).setAttribute('aria-selected', String(t === nombre));
    $('panel' + t[0].toUpperCase() + t.slice(1)).hidden = t !== nombre;
  });
  if (nombre === 'notas') $('notasTexto').focus();
}
async function pintarRegistro() {
  await cargarCartas();
  const cont = $('panelRegistro');
  if (!estado.log.length) {
    cont.innerHTML = '<p class="registro-vacio">Todavía no habéis abierto ninguna carta con la app. Aquí quedará anotado lo que hagáis.</p>';
    return;
  }
  const ol = document.createElement('ol');
  ol.className = 'registro';
  estado.log.slice().reverse().forEach((e) => {
    const li = document.createElement('li');
    const nombre = document.createElement('span');
    nombre.textContent = (e.uso === 'pista' ? 'Pista · ' : '') + tituloCarta(e.card);
    const t = document.createElement('small');
    t.textContent = mmss(e.t);
    li.append(nombre, t);
    ol.appendChild(li);
  });
  cont.replaceChildren(ol);
}
$('notebookBtn').addEventListener('click', () => abrirCuaderno('registro'));
$('cuadernoCerrar').addEventListener('click', cerrarCuaderno);
gestoCerrar(document.querySelector('.cuaderno-caja'), cerrarCuaderno);
cuaderno.addEventListener('click', (e) => { if (e.target === cuaderno) cerrarCuaderno(); });
document.querySelectorAll('.pestanas button').forEach((b) => b.addEventListener('click', () => elegirPestana(b.dataset.tab)));
$('notasTexto').addEventListener('input', (e) => { estado.notas = e.target.value; guardar(); });
document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && cuaderno.classList.contains('abierto')) cerrarCuaderno(); });

// ---------------------------------------------------------------- final e informe
function construirInforme(exito) {
  const usado = TOTAL - estado.restante;
  const pistas = Object.entries(estado.pistas).map(([c, n]) => `${c}×${n}`).join(', ') || 'ninguna';
  const abiertas = estado.log.filter((e) => e.uso === 'accion').map((e) => e.card).join(', ') || 'ninguna';
  const extra = estado.restante < 0 ? ` (${mmss(-estado.restante)} de más)` : '';
  const lineas = [
    `Informe de partida — ${TITULO}`,
    `Fecha: ${new Date().toLocaleString('es-ES')}`,
    `Resultado: ${exito ? 'aventura completada' : 'partida sin terminar'}`,
    `Tiempo usado: ${mmss(usado)} de ${mmss(TOTAL)}${extra}`,
    `Pistas pedidas (carta×veces): ${pistas}`,
    `Cartas abiertas con la app (en orden): ${abiertas}`,
    `Intentos sin efecto en el teclado: ${estado.sinEfecto}`
  ];
  const tiempos = estado.log.map((e) => `${e.uso === 'pista' ? 'pista ' : ''}${e.card} a los ${mmss(e.t)}`).join('; ');
  if (tiempos) lineas.push(`Línea de tiempo: ${tiempos}`);
  if (estado.notas && estado.notas.trim()) lineas.push(`Notas: ${estado.notas.trim()}`);
  return lineas.join('\n');
}
function mostrarFinal(exito) {
  estado.fin = Date.now();
  escribirGuardado(null);
  if (intervalId) clearInterval(intervalId);
  soltarPantalla();
  musica.parar();
  gamePanel.style.display = 'none';
  introPanel.style.display = 'none';
  finalPanel.style.display = 'block';
  const usado = TOTAL - estado.restante;
  const pistas = Object.values(estado.pistas).reduce((a, b) => a + b, 0);
  $('finTiempo').textContent = mmss(usado);
  $('finPistas').textContent = String(pistas);
  $('finCartas').textContent = String(estado.log.filter((e) => e.uso === 'accion' && e.card !== String(CFG.final)).length);
  $('finalTitulo').textContent = exito ? '¡Misión cumplida!' : 'Partida terminada';
  $('finalSub').textContent = estado.restante >= 0
    ? `Lo habéis conseguido con ${mmss(estado.restante)} de margen.`
    : `Lo habéis conseguido, con ${mmss(-estado.restante)} de más sobre el tiempo previsto.`;
  $('informeTexto').textContent = construirInforme(exito);
  if (exito) registrarPartida();
  [440, 554, 659, 880].forEach((f, i) => setTimeout(() => pitido(f, 220, 'triangle', 0.07), i * 160));
  window.scrollTo(0, 0);
}
// ---------------------------------------------------------------- registro de la partida (cuenta y dispositivo)
function guardarLocalDeEmergencia(reg) {
  try {
    const l = JSON.parse(localStorage.getItem('ca-hechas') || '[]');
    l.push(Object.assign({ cliente_id: Date.now().toString(36) + Math.random().toString(36).slice(2, 8), fin: new Date().toISOString(), sync: false }, reg));
    localStorage.setItem('ca-hechas', JSON.stringify(l.slice(-300)));
  } catch (e) { /* sin almacenamiento */ }
}
async function registrarPartida() {
  const estadoEl = $('guardadoEstado');
  const btn = $('guardarCuentaBtn');
  const usado = TOTAL - estado.restante;
  const reg = {
    juego: CFG.juego || TEMA, tiempo_seg: Math.round(usado), pistas: Object.values(estado.pistas).reduce((a, b) => a + b, 0),
    cartas: estado.log.filter((e) => e.uso === 'accion' && e.card !== String(CFG.final)).length, informe: construirInforme(true)
  };
  estadoEl.textContent = 'Guardando la partida…';
  try {
    const url = (f) => new URL(CFG.assets + 'js/' + f, import.meta.url).href;
    const cuenta = await import(url('cuenta.js'));
    const antes = cuenta.resumenLocal()[reg.juego];
    const r = await cuenta.guardarPartida(reg);
    const mejor = !antes || reg.tiempo_seg < antes.mejor;
    estadoEl.textContent = r.mensaje + (mejor && antes ? ' ¡Nuevo mejor tiempo!' : '');
    if (!r.nube) {
      btn.hidden = false;
      btn.onclick = async () => {
        const ui = await import(url('cuenta-ui.js'));
        const u = await ui.abrirLogin({ motivo: 'Entra para guardar esta partida (' + cuenta.formatoTiempo(reg.tiempo_seg) + ') en tu cuenta.' });
        if (u) { const s = await cuenta.sincronizar(); estadoEl.textContent = s.ok ? 'Partida guardada en tu cuenta.' : (s.mensaje || 'Se guardará en cuanto haya conexión.'); btn.hidden = s.ok; }
      };
    }
  } catch (e) {
    guardarLocalDeEmergencia(reg);
    estadoEl.textContent = 'Partida guardada en este dispositivo.';
  }
}

$('copyReportBtn').addEventListener('click', async () => {
  const texto = $('informeTexto').textContent;
  const pre = $('informeTexto');
  let copiado = false;
  try { await navigator.clipboard.writeText(texto); copiado = true; } catch (e) { /* respaldo abajo */ }
  if (!copiado) {
    try {
      const ta = document.createElement('textarea');
      ta.value = texto;
      document.body.appendChild(ta);
      ta.select();
      copiado = document.execCommand('copy');
      document.body.removeChild(ta);
    } catch (e) { copiado = false; }
  }
  pre.hidden = false;
  $('copyReportBtn').textContent = copiado ? 'Informe copiado' : 'Seleccionad y copiad el informe';
});
$('replayBtn').addEventListener('click', () => { escribirGuardado(null); location.reload(); });

// ---------------------------------------------------------------- inicio
function mostrarContinuar() {
  const g = leerGuardado();
  const hay = !!(g && !g.fin && Array.isArray(g.log) && typeof g.restante === 'number' && (g.log.length || g.restante < TOTAL - 5));
  continueBtn.hidden = !hay;
  if (hay) continueBtn.textContent = `Continuar partida (${mmss(Math.max(0, g.restante))} restantes)`;
}
function volver() { window.location.href = CFG.volver; }
window.volver = volver;

// ---------------------------------------------------------------- modo sin conexión (PWA)
function iniciarOffline() {
  const btn = $('offlineBtn'), est = $('offlineEstado');
  if (!btn || !window.CA_PWA || !window.CA_PWA.soportado || location.protocol === 'file:') return;
  const clave = 'ca-offline:' + (CFG.juego || TEMA);
  let hecho = false;
  try { hecho = localStorage.getItem(clave) === '1'; } catch (e) { /* nada */ }
  btn.hidden = false;
  if (hecho) { btn.textContent = 'Actualizar la descarga sin conexión'; est.hidden = false; est.textContent = 'Este juego ya funciona sin conexión.'; }
  btn.onclick = async () => {
    btn.disabled = true; est.hidden = false; est.textContent = 'Descargando…';
    try {
      const lista = await (await fetch('./precache.json', { cache: 'no-store' })).json();
      const r = await window.CA_PWA.descargar(lista, (p) => { est.textContent = 'Descargando… ' + Math.round((100 * p.hechos) / Math.max(1, p.total)) + ' %'; });
      if (r.fallos > 0) est.textContent = 'Se descargó casi todo, pero ' + r.fallos + ' ficheros fallaron: vuelve a intentarlo con buena conexión.';
      else { est.textContent = 'Listo: este juego funciona sin conexión.'; try { localStorage.setItem(clave, '1'); } catch (e) { /* nada */ } }
    } catch (e) { est.textContent = (e && e.message) || 'No se pudo descargar.'; }
    btn.disabled = false;
  };
}
(function cargarPwa() {
  if (!('serviceWorker' in navigator) || location.protocol === 'file:') return;
  const s = document.createElement('script');
  s.src = new URL(CFG.assets + 'js/pwa.js', import.meta.url).href;
  s.onload = iniciarOffline;
  document.head.appendChild(s);
})();

$('introMin').textContent = textoDuracion(TOTAL);
$('reglasTexto').innerHTML = REGLAS;
$('panelReglas').innerHTML = REGLAS;
$('relojEtiqueta').textContent = ETIQUETA_RELOJ[TEMA] || 'El tiempo corre';
(function pintarDificultad() {
  const el = $('dificultad');
  const n = Math.max(0, Math.min(5, Math.round(CFG.dificultad || 0)));
  if (!el || !n) { if (el) el.hidden = true; return; }
  el.setAttribute('aria-label', 'Dificultad: ' + NIVELES[n] + ' (' + n + ' de 5)');
  el.innerHTML = '<span>Dificultad</span><span class="puntos" aria-hidden="true">' +
    [1, 2, 3, 4, 5].map((k) => '<i class="' + (k <= n ? 'on' : '') + '"></i>').join('') + '</span><span>' + NIVELES[n] + '</span>';
})();
gameTimerEl.textContent = formatTime(TOTAL);
mostrarContinuar();
cargarCartas();

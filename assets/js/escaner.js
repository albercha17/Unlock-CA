// escaner.js — escanea con la cámara el QR de una carta (imprimir.html lo dibuja en cada carta: «CA:<juego>:<número>»).
// Usa jsQR (assets/js/vendor/jsQR.js), que funciona también en iPhone (Safari no tiene BarcodeDetector). Siempre queda el teclado como alternativa.

const FORMATO = /^CA:([a-z0-9-]+):([0-9P]{1,4})$/i;

/** Interpreta el texto de un QR. Devuelve { id } si es una carta de este juego o { error } con un mensaje claro. */
export function interpretar(texto, juego) {
  const m = FORMATO.exec(String(texto || '').trim());
  if (!m) return { error: 'Ese código no es de una carta de Unlock C&A.' };
  if (juego && m[1].toLowerCase() !== String(juego).toLowerCase()) return { error: 'Esa carta es de otro juego (' + m[1] + ').' };
  return { id: m[2].toUpperCase() };
}

function cargarJsQR() {
  return new Promise((ok, mal) => {
    if (window.jsQR) { ok(window.jsQR); return; }
    const s = document.createElement('script');
    s.src = new URL('./vendor/jsQR.js', import.meta.url).href;
    s.onload = () => (window.jsQR ? ok(window.jsQR) : mal(new Error('sin lector')));
    s.onerror = () => mal(new Error('No se pudo cargar el lector de códigos.'));
    document.head.appendChild(s);
  });
}

/** Decodifica un fotograma (ImageData). Útil también para pruebas sin cámara. */
export function decodificar(imagen) {
  const r = window.jsQR && window.jsQR(imagen.data, imagen.width, imagen.height, { inversionAttempts: 'attemptBoth' });
  return r ? r.data : null;
}

/** Abre la cámara a pantalla completa. Devuelve { id } al leer una carta, { error } si falla, o { cancelado: true }. */
export async function escanear({ juego } = {}) {
  try { await cargarJsQR(); } catch (e) { return { error: e.message }; }
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) return { error: 'Este navegador no permite usar la cámara aquí. Escribe el número de la carta.' };
  let flujo;
  try {
    flujo = await navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: 'environment' }, width: { ideal: 1280 } }, audio: false });
  } catch (e) {
    return { error: /denied|NotAllowed|Permission/i.test(String(e && (e.name + e.message))) ? 'No hay permiso para la cámara. Puedes activarlo en los ajustes del navegador o escribir el número.' : 'No se pudo abrir la cámara. Escribe el número de la carta.' };
  }
  return new Promise((resolve) => {
    const caja = document.createElement('div');
    caja.setAttribute('role', 'dialog');
    caja.setAttribute('aria-modal', 'true');
    caja.setAttribute('aria-label', 'Escanear una carta');
    caja.style.cssText = 'position:fixed;inset:0;z-index:30000;background:#000;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Poppins,system-ui,sans-serif;color:#fff';
    const video = document.createElement('video');
    video.setAttribute('playsinline', '');
    video.muted = true;
    video.srcObject = flujo;
    video.style.cssText = 'width:100%;flex:1;object-fit:cover;min-height:0';
    const marco = document.createElement('div');
    marco.style.cssText = 'position:absolute;left:50%;top:42%;width:min(62vw,300px);aspect-ratio:1;transform:translate(-50%,-50%);border:3px solid #ffd27a;border-radius:18px;box-shadow:0 0 0 100vmax rgba(0,0,0,.45);pointer-events:none';
    const msg = document.createElement('p');
    msg.style.cssText = 'margin:0;padding:12px 16px;text-align:center;font-size:.92rem;min-height:3.2em';
    msg.textContent = 'Apunta al código QR de la esquina de la carta.';
    msg.setAttribute('aria-live', 'polite');
    const cancelar = document.createElement('button');
    cancelar.type = 'button';
    cancelar.textContent = 'Escribir el número';
    cancelar.style.cssText = 'min-height:52px;margin:0 16px max(16px,env(safe-area-inset-bottom));padding:0 22px;border:0;border-radius:14px;background:#ffd27a;color:#2a1600;font:800 1rem Poppins,system-ui,sans-serif;cursor:pointer';
    caja.append(video, marco, msg, cancelar);
    document.body.appendChild(caja);
    const lienzo = document.createElement('canvas');
    const cx = lienzo.getContext('2d', { willReadFrequently: true });
    let activo = true, ultimo = 0, avisoHasta = 0;
    function fin(r) {
      if (!activo) return;
      activo = false;
      flujo.getTracks().forEach((t) => t.stop());
      caja.remove();
      resolve(r);
    }
    cancelar.addEventListener('click', () => fin({ cancelado: true }));
    function bucle(t) {
      if (!activo) return;
      requestAnimationFrame(bucle);
      if (t - ultimo < 140 || video.readyState < 2 || !video.videoWidth) return;
      ultimo = t;
      const w = Math.min(640, video.videoWidth), h = Math.round(w * video.videoHeight / video.videoWidth);
      lienzo.width = w; lienzo.height = h;
      cx.drawImage(video, 0, 0, w, h);
      const texto = decodificar(cx.getImageData(0, 0, w, h));
      if (!texto) { if (t > avisoHasta && msg.dataset.err) { msg.textContent = 'Apunta al código QR de la esquina de la carta.'; delete msg.dataset.err; } return; }
      const r = interpretar(texto, juego);
      if (r.id) { try { if (navigator.vibrate) navigator.vibrate(40); } catch (e) { /* iPhone no vibra */ } fin(r); return; }
      msg.textContent = r.error; msg.dataset.err = '1'; avisoHasta = t + 2500;
    }
    video.play().catch(() => {});
    requestAnimationFrame(bucle);
  });
}

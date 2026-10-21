/* sw.js — service worker de Unlock C&A (GENERADO por herramientas/generar_pwa.py a partir de herramientas/sw_plantilla.js: no editar a mano).
   - Instala el «cascarón» (menús, cuentas, iconos) para que la app abra sin conexión.
   - Páginas y datos (HTML/JSON): red primero (para recibir las actualizaciones) y, sin red, la copia guardada.
   - Resto (imágenes, JS, CSS): copia guardada y se refresca en segundo plano.
   - Mensaje {tipo:'cachear', urls:[...]}: descarga un juego entero para jugarlo sin conexión (responde con el progreso).
   - No toca vídeo (los rangos de vídeo de iOS no se pueden servir bien desde la caché) ni las llamadas a Supabase.
   La versión cambia sola cuando cambia el cascarón: así los móviles reciben los ficheros nuevos. */
const VERSION = '9ce19212d8';
const CACHE = 'unlock-ca-' + VERSION;
const CASCARON = ["./", "index.html", "perfil.html", "instalar.html", "ajustes.html", "manifest.webmanifest", "assets/css/style.css", "assets/css/menu.css", "assets/css/cuenta.css", "assets/css/barra.css", "assets/js/menu.js", "assets/js/ajustes.js", "assets/js/barra.js", "assets/js/splash.js", "assets/js/cuenta.js", "assets/js/cuenta-ui.js", "assets/js/accesos.js", "assets/js/filtro-juegos.js", "assets/js/pwa.js", "assets/js/vendor/supabase.js", "assets/images/logo.png", "assets/images/faro.jpg", "assets/icons/icon-192.png", "assets/icons/icon-512.png", "assets/icons/apple-touch-icon.png", "assets/icons/favicon.png", "juegos/catalogo.json", "juegos/aventuras-ca/index.html"];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => Promise.all(CASCARON.map((u) => c.add(new Request(u, { cache: 'reload' })).catch(() => null)))).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k.startsWith('unlock-ca-') && k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

function conTiempo(promesa, ms) {
  return new Promise((ok, mal) => { const t = setTimeout(() => mal(new Error('tiempo')), ms); promesa.then((r) => { clearTimeout(t); ok(r); }, (er) => { clearTimeout(t); mal(er); }); });
}

async function redPrimero(req) {
  const cache = await caches.open(CACHE);
  try {
    const r = await conTiempo(fetch(req), 4500);
    if (r && r.ok) cache.put(req, r.clone());
    return r;
  } catch (e) {
    const guardada = await cache.match(req, { ignoreSearch: true });
    if (guardada) return guardada;
    if (req.mode === 'navigate') {
      const inicio = await cache.match(new URL('index.html', self.registration.scope).href);
      if (inicio) return inicio;
    }
    return new Response('Sin conexión', { status: 503, statusText: 'Sin conexión', headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
  }
}

async function guardadaYRefresca(req) {
  const cache = await caches.open(CACHE);
  const guardada = await cache.match(req, { ignoreSearch: true });
  const red = fetch(req).then((r) => { if (r && (r.ok || r.type === 'opaque')) cache.put(req, r.clone()); return r; }).catch(() => null);
  if (guardada) { red.catch(() => {}); return guardada; }
  const r = await red;
  return r || new Response('', { status: 504 });
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET' || req.headers.has('range')) return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) {
    if (/(^|\.)fonts\.(googleapis|gstatic)\.com$/.test(url.hostname)) e.respondWith(guardadaYRefresca(req));
    return;
  }
  if (/\.(mp4|webm|mov|m4v)$/i.test(url.pathname)) return;
  const esPagina = req.mode === 'navigate' || /\.(html|json|webmanifest)$/i.test(url.pathname) || url.pathname.endsWith('/');
  e.respondWith(esPagina ? redPrimero(req) : guardadaYRefresca(req));
});

self.addEventListener('message', (e) => {
  const d = e.data || {};
  if (d.tipo === 'saltar') { self.skipWaiting(); return; }
  if (d.tipo !== 'cachear' || !Array.isArray(d.urls)) return;
  const origen = e.source;
  const total = d.urls.length;
  let hechos = 0, fallos = 0;
  const avisar = (fin) => { try { if (origen) origen.postMessage({ tipo: 'progreso', id: d.id || '', hechos, fallos, total, fin: !!fin }); } catch (er) { /* nada */ } };
  e.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    const cola = d.urls.slice();
    async function obrero() {
      while (cola.length) {
        const u = cola.shift();
        try {
          const r = await fetch(new Request(u, { cache: 'reload' }));
          if (r.ok) await cache.put(u, r); else fallos++;
        } catch (er) { fallos++; }
        hechos++;
        if (hechos % 4 === 0 || hechos === total) avisar(false);
      }
    }
    await Promise.all([obrero(), obrero(), obrero(), obrero(), obrero(), obrero()]);
    avisar(true);
  })());
});

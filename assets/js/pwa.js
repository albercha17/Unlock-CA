/* pwa.js — registra el service worker (sw.js en la raíz del sitio) y ofrece window.CA_PWA para instalar y descargar juegos sin conexión.
   Script clásico (no módulo): calcula la raíz del sitio a partir de su propia dirección, así funciona igual desde cualquier página. */
(function () {
  var script = document.currentScript;
  var base = new URL('../../', script ? script.src : location.href);
  var API = (window.CA_PWA = {
    base: base.href,
    soportado: 'serviceWorker' in navigator,
    instalada: function () {
      return (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) || window.navigator.standalone === true;
    },
    esIOS: function () {
      return /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    },
    /** Descarga una lista de rutas (relativas a la raíz del sitio) en la caché del service worker. onProgreso({hechos,total,fin,fallos}). */
    descargar: function (rutas, onProgreso) {
      if (!API.soportado) return Promise.reject(new Error('Este navegador no permite el modo sin conexión.'));
      return navigator.serviceWorker.ready.then(function (reg) {
        var sw = reg.active || navigator.serviceWorker.controller;
        if (!sw) throw new Error('El modo sin conexión aún no está activo: recarga la página y vuelve a intentarlo.');
        var id = 'd' + Date.now();
        var urls = rutas.map(function (r) { return new URL(r, base).href; });
        return new Promise(function (ok) {
          function alMensaje(e) {
            var d = e.data || {};
            if (d.tipo !== 'progreso' || d.id !== id) return;
            if (onProgreso) onProgreso(d);
            if (d.fin) { navigator.serviceWorker.removeEventListener('message', alMensaje); ok(d); }
          }
          navigator.serviceWorker.addEventListener('message', alMensaje);
          sw.postMessage({ tipo: 'cachear', urls: urls, id: id });
        });
      });
    }
  });
  if (!API.soportado) return;
  // Aviso «versión nueva»: solo cuando la app ya estaba controlada por un service worker y llega otro (no en la primera instalación)
  var yaControlada = !!navigator.serviceWorker.controller;
  var avisado = false;
  navigator.serviceWorker.addEventListener('controllerchange', function () {
    if (!yaControlada || avisado) return;
    avisado = true;
    var b = document.createElement('div');
    b.setAttribute('role', 'status');
    b.style.cssText = 'position:fixed;left:12px;right:12px;bottom:max(12px,env(safe-area-inset-bottom));z-index:30000;display:flex;gap:10px;align-items:center;justify-content:space-between;' +
      'background:#101a24;color:#eef3f8;border:1px solid #ffd27a;border-radius:14px;padding:12px 14px;font:600 .88rem Poppins,system-ui,sans-serif;box-shadow:0 12px 40px rgba(0,0,0,.6)';
    b.innerHTML = '<span>Hay una versión nueva de Unlock C&amp;A.</span>';
    var act = document.createElement('button');
    act.textContent = 'Actualizar';
    act.style.cssText = 'min-height:44px;padding:0 16px;border:0;border-radius:10px;background:#ffd27a;color:#2a1600;font:800 .9rem Poppins,system-ui,sans-serif;cursor:pointer';
    act.onclick = function () { location.reload(); };
    var luego = document.createElement('button');
    luego.textContent = 'Luego';
    luego.style.cssText = 'min-height:44px;padding:0 10px;border:0;background:transparent;color:#b6c4d2;font:700 .85rem Poppins,system-ui,sans-serif;cursor:pointer';
    luego.onclick = function () { b.remove(); };
    var fila = document.createElement('span');
    fila.style.cssText = 'display:flex;gap:6px';
    fila.append(luego, act);
    b.appendChild(fila);
    document.body.appendChild(b);
  });
  window.addEventListener('load', function () {
    navigator.serviceWorker.register(new URL('sw.js', base).href, { scope: base.href }).then(function (reg) {
      // si hay una versión nueva esperando, activarla en cuanto se pueda
      reg.addEventListener('updatefound', function () {
        var nuevo = reg.installing;
        if (!nuevo) return;
        nuevo.addEventListener('statechange', function () {
          if (nuevo.state === 'installed' && navigator.serviceWorker.controller) nuevo.postMessage({ tipo: 'saltar' });
        });
      });
    }).catch(function () { /* sin service worker: la web funciona igual, solo con conexión */ });
  });
})();

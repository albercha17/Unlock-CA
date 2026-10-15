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

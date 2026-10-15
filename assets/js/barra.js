/* barra.js — barra de navegación inferior (Inicio · Aventuras · Mis partidas · Ajustes) para los menús de la app.
   Script clásico: calcula la raíz del sitio a partir de su propia dirección. No se usa dentro de las partidas (pantalla inmersiva). */
(function () {
  var script = document.currentScript;
  var base = new URL('../../', script ? script.src : location.href);
  var css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = new URL('assets/css/barra.css', base).href;
  document.head.appendChild(css);

  var ICON = {
    inicio: '<path d="M3 11.5 12 4l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    aventuras: '<circle cx="12" cy="12" r="8"/><path d="M12 4v3M12 17v3M4 12h3M17 12h3"/><circle cx="12" cy="12" r="2.4"/>',
    partidas: '<path d="M7 4h10v4a5 5 0 0 1-10 0z"/><path d="M7 6H4a3 3 0 0 0 3 4M17 6h3a3 3 0 0 1-3 4M12 13v4M8 21h8M10 17h4"/>',
    ajustes: '<circle cx="12" cy="12" r="3"/><path d="M12 3v2.4M12 18.6V21M3 12h2.4M18.6 12H21M5.6 5.6l1.7 1.7M16.7 16.7l1.7 1.7M5.6 18.4l1.7-1.7M16.7 7.3l1.7-1.7"/>'
  };
  var TABS = [
    ['inicio', 'Inicio', 'index.html', /^\/(index\.html)?$/],
    ['aventuras', 'Aventuras', 'juegos/aventuras-ca/index.html', /\/juegos\/aventuras-ca\/(index\.html)?$/],
    ['partidas', 'Partidas', 'perfil.html', /\/perfil\.html$/],
    ['ajustes', 'Ajustes', 'ajustes.html', /\/ajustes\.html$/]
  ];

  function pintar() {
    var nav = document.createElement('nav');
    nav.className = 'ca-barra';
    nav.setAttribute('aria-label', 'Navegación principal');
    var ruta = location.pathname;
    var raizRuta = new URL('./', base).pathname;
    var relativa = ruta.indexOf(raizRuta) === 0 ? '/' + ruta.slice(raizRuta.length) : ruta;
    TABS.forEach(function (t) {
      var a = document.createElement('a');
      a.className = 'ca-tab';
      a.href = new URL(t[2], base).href;
      var activa = t[3].test(relativa);
      if (activa) { a.setAttribute('aria-current', 'page'); a.classList.add('activa'); }
      a.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true">' + ICON[t[0]] + '</svg><span>' + t[1] + '</span>';
      a.addEventListener('click', function () { try { if (navigator.vibrate) navigator.vibrate(8); } catch (e) { /* iPhone no vibra */ } });
      nav.appendChild(a);
    });
    document.body.appendChild(nav);
    document.body.classList.add('con-barra');
  }
  if (document.body) pintar(); else document.addEventListener('DOMContentLoaded', pintar);
})();

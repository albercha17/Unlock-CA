/* ajustes.js — ajustes de la app (texto, contraste, movimiento, música, sonido). Script clásico, se carga al principio de cada página para aplicarlos
   sin parpadeos. Las claves antiguas se conservan: `ca-musica` (música de fondo) y `far-sonido` (sonidos de los minijuegos). */
(function () {
  var K = 'ca-ajustes';
  var DEF = { volMusica: 0.5, texto: 1, contraste: false, movimiento: false };

  function lee(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function escribe(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* sin almacenamiento */ } }

  function leer() {
    var o = {};
    try { o = JSON.parse(lee(K) || '{}'); } catch (e) { o = {}; }
    var r = {};
    for (var k in DEF) r[k] = o[k] === undefined ? DEF[k] : o[k];
    r.musica = lee('ca-musica') !== '0';
    r.efectos = lee('far-sonido') !== '0';
    return r;
  }

  var ESTILO = 'html[data-movimiento="reducido"] *,html[data-movimiento="reducido"] *::before,html[data-movimiento="reducido"] *::after{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important;scroll-behavior:auto!important}' +
    'html[data-contraste="alto"]{--linea:rgba(255,255,255,.75)!important;--texto-suave:#fff!important;--mut:#fff!important;--muted:#fff!important}' +
    'html[data-contraste="alto"] body{background:#000!important}' +
    'html[data-contraste="alto"] p,html[data-contraste="alto"] small,html[data-contraste="alto"] .sub,html[data-contraste="alto"] .lede,html[data-contraste="alto"] .dif-fila{color:#fff!important}' +
    'html[data-contraste="alto"] .panel-card,html[data-contraste="alto"] .option,html[data-contraste="alto"] .salto,html[data-contraste="alto"] .tarj,html[data-contraste="alto"] .logro,html[data-contraste="alto"] .fila-aj,html[data-contraste="alto"] .pasos li{border:2px solid #fff!important;background:#0a0a0a!important}' +
    'html[data-contraste="alto"] button,html[data-contraste="alto"] .boton,html[data-contraste="alto"] .btn{border:2px solid #fff!important}';

  function aplicar() {
    var a = leer(), h = document.documentElement;
    if (a.contraste) h.setAttribute('data-contraste', 'alto'); else h.removeAttribute('data-contraste');
    if (a.movimiento) h.setAttribute('data-movimiento', 'reducido'); else h.removeAttribute('data-movimiento');
    h.style.zoom = a.texto && a.texto !== 1 ? String(a.texto) : '';
    return a;
  }

  function guardar(clave, valor) {
    if (clave === 'musica') escribe('ca-musica', valor ? '1' : '0');
    else if (clave === 'efectos') escribe('far-sonido', valor ? '1' : '0');
    else {
      var o = {};
      try { o = JSON.parse(lee(K) || '{}'); } catch (e) { o = {}; }
      o[clave] = valor;
      escribe(K, JSON.stringify(o));
    }
    var a = aplicar();
    try { window.dispatchEvent(new CustomEvent('ca-ajustes', { detail: a })); } catch (e) { /* nada */ }
    return a;
  }

  var st = document.createElement('style');
  st.id = 'ca-ajustes-css';
  st.textContent = ESTILO;
  (document.head || document.documentElement).appendChild(st);
  window.CA_AJUSTES = { leer: leer, guardar: guardar, aplicar: aplicar, DEF: DEF };
  aplicar();
  window.addEventListener('storage', aplicar);
})();

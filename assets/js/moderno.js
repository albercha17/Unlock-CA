/* moderno.js — animaciones de los menús (aparición escalonada, ondas al tocar, inclinación de tarjetas con el ratón, pastilla de la barra inferior y fondo vivo).
   Script clásico, sin dependencias. No hace nada con «reducir movimiento». En las pruebas automáticas (navigator.webdriver) no oculta ningún elemento. */
(function () {
  if (window.__moderno) return;
  window.__moderno = true;
  var reducir = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reducir) return;
  var auto = !!navigator.webdriver;
  var raiz = document.documentElement;
  raiz.classList.add('moderno');

  function inicio() {
    // fondo vivo
    var au = document.createElement('div');
    au.className = 'ca-aurora';
    au.setAttribute('aria-hidden', 'true');
    au.innerHTML = '<i></i><i></i><i></i>';
    document.body.insertBefore(au, document.body.firstChild);

    // aparición escalonada de lo que va entrando en pantalla
    var SEL = '.option, .salto, [data-juego], .portal, .seccion, .grupo, .header, .fj, .mis-vacio, .tarjeta, .panel-card > section, .panel-card > h2';
    var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        io.unobserve(el);
        el.classList.add('rv-in');
        if (el.classList.contains('option') || el.classList.contains('salto')) el.classList.add('brillo');
        setTimeout(function () { el.classList.remove('rv', 'rv-in', 'brillo'); el.style.removeProperty('--d'); }, 1500);
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -4% 0px' }) : null;
    var n = 0;
    function registrar(el) {
      if (el.__rv) return;
      el.__rv = true;
      if (auto || !io) return;
      el.classList.add('rv');
      el.style.setProperty('--d', Math.min(n++ % 8, 7) * 70 + 'ms');
      io.observe(el);
    }
    function barrer(raizNodo) {
      if (raizNodo.matches && raizNodo.matches(SEL)) registrar(raizNodo);
      if (raizNodo.querySelectorAll) Array.prototype.forEach.call(raizNodo.querySelectorAll(SEL), registrar);
    }
    barrer(document.body);
    new MutationObserver(function (ms) {
      ms.forEach(function (m) { Array.prototype.forEach.call(m.addedNodes, function (x) { if (x.nodeType === 1 && !x.classList.contains('ca-aurora') && !x.classList.contains('rip')) barrer(x); }); });
    }).observe(document.body, { childList: true, subtree: true });

    // onda al tocar
    var HOST = '.option, .salto, .btn, .boton, .mis-btn, .ca-tab, .fj-dif button, .icono';
    document.addEventListener('pointerdown', function (e) {
      var el = e.target.closest && e.target.closest(HOST);
      if (!el || el.disabled) return;
      var r = el.getBoundingClientRect();
      var d = Math.max(r.width, r.height) * 2;
      var s = document.createElement('span');
      s.className = 'rip';
      s.style.cssText = 'width:' + d + 'px;height:' + d + 'px;left:' + (e.clientX - r.left - d / 2) + 'px;top:' + (e.clientY - r.top - d / 2) + 'px';
      el.classList.add('rip-host');
      el.appendChild(s);
      setTimeout(function () { if (s.parentNode) s.parentNode.removeChild(s); }, 700);
    }, { passive: true });

    // inclinación suave de las tarjetas con el ratón (solo con puntero fino)
    if (window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches) {
      document.addEventListener('pointermove', function (e) {
        var el = e.target.closest && e.target.closest('.option, .salto');
        if (!el) return;
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5;
        var y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = 'perspective(700px) translateY(-5px) scale(1.012) rotateX(' + (-y * 5).toFixed(2) + 'deg) rotateY(' + (x * 6).toFixed(2) + 'deg)';
      }, { passive: true });
      document.addEventListener('pointerout', function (e) {
        var el = e.target.closest && e.target.closest('.option, .salto');
        if (el && !el.contains(e.relatedTarget)) el.style.transform = '';
      }, { passive: true });
    }

    // pastilla de la barra inferior
    function pastilla() {
      var nav = document.querySelector('.ca-barra');
      if (!nav) return false;
      var ind = nav.querySelector('.ca-ind');
      if (!ind) { ind = document.createElement('span'); ind.className = 'ca-ind'; nav.insertBefore(ind, nav.firstChild); }
      function mover() {
        var a = nav.querySelector('.ca-tab.activa');
        if (!a) { ind.style.width = '0'; return; }
        ind.style.width = a.offsetWidth + 'px';
        ind.style.transform = 'translateX(' + a.offsetLeft + 'px)';
      }
      mover();
      window.addEventListener('resize', mover);
      return true;
    }
    if (!pastilla()) {
      var o = new MutationObserver(function () { if (pastilla()) o.disconnect(); });
      o.observe(document.body, { childList: true });
    }
  }
  if (document.body) inicio(); else document.addEventListener('DOMContentLoaded', inicio);
})();

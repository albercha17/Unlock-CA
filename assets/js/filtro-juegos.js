/* filtro-juegos.js — buscador por nombre y filtro por dificultad para listas de juegos (tienda, menú, hub de aventuras).
   Script clásico: deja window.FiltroJuegos.montar(lista, opciones). Cada elemento de la lista que se quiera filtrar
   lleva data-dif (1-5); se busca en todo su texto (sin tildes ni mayúsculas), así que también encuentra época y puzles.
     FiltroJuegos.montar(document.getElementById('lista'), { items: '.aventura', nombre: 'aventura', antes: elemento })
   Devuelve { aplicar() } para volver a filtrar si la lista se repinta. */
(function () {
  var NIVELES = [
    ['todas', 'Todas', function () { return true; }],
    ['facil', 'Fácil', function (n) { return n <= 2; }],
    ['media', 'Media', function (n) { return n === 3; }],
    ['dificil', 'Difícil', function (n) { return n >= 4; }]
  ];
  var css = '' +
    '.fj{display:flex;flex-wrap:wrap;gap:8px 10px;align-items:center;margin:14px 0 16px}' +
    '.fj input{flex:1 1 200px;min-width:0;min-height:42px;padding:0 14px;border-radius:999px;border:1px solid rgba(255,255,255,.2);' +
      'background:rgba(0,0,0,.28);color:inherit;font:inherit;font-size:.92rem}' +
    '.fj input:focus-visible{outline:3px solid #ffd27a;outline-offset:1px}' +
    '.fj-dif{display:flex;flex-wrap:wrap;gap:6px}' +
    '.fj-dif button{min-height:38px;padding:0 13px;border-radius:999px;border:1px solid rgba(255,255,255,.2);background:transparent;' +
      'color:inherit;opacity:.78;font:inherit;font-size:.84rem;font-weight:600;cursor:pointer}' +
    '.fj-dif button[aria-pressed="true"]{opacity:1;background:rgba(255,210,122,.16);border-color:#e9b65c;color:#ffd88f}' +
    '.fj-n{font-size:.8rem;opacity:.7;white-space:nowrap}' +
    '.fj-vacio{opacity:.75;font-size:.92rem;padding:18px 4px}' +
    '[data-fj-oculto]{display:none!important}';

  function quitarTildes(t) { return String(t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }

  function montar(lista, op) {
    if (!lista) return null;
    op = op || {};
    if (!document.getElementById('fj-css')) {
      var st = document.createElement('style');
      st.id = 'fj-css';
      st.textContent = css;
      document.head.appendChild(st);
    }
    var nombre = op.nombre || 'juego';
    var plural = op.plural || nombre + 's';
    var barra = document.createElement('div');
    barra.className = 'fj';
    barra.innerHTML = '<input type="search" placeholder="Buscar ' + nombre + ' por nombre, época…" aria-label="Buscar ' + nombre + '">' +
      '<div class="fj-dif" role="group" aria-label="Dificultad">' +
      NIVELES.map(function (n, i) { return '<button type="button" data-nivel="' + n[0] + '" aria-pressed="' + (i === 0) + '">' + n[1] + '</button>'; }).join('') +
      '</div><span class="fj-n" aria-live="polite"></span>';
    var antes = op.antes || lista;
    antes.parentNode.insertBefore(barra, antes);
    var vacio = document.createElement('p');
    vacio.className = 'fj-vacio';
    vacio.hidden = true;
    vacio.textContent = 'Ninguna ' + nombre + ' coincide. Prueba con otra palabra o dificultad.';
    lista.parentNode.insertBefore(vacio, lista.nextSibling);
    var input = barra.querySelector('input');
    var nivel = 'todas';

    function aplicar() {
      var q = quitarTildes(input.value.trim());
      var f = NIVELES.filter(function (n) { return n[0] === nivel; })[0][2];
      var items = lista.querySelectorAll(op.items || ':scope > *');
      var vistos = 0;
      Array.prototype.forEach.call(items, function (el) {
        var dif = parseInt(el.getAttribute('data-dif'), 10) || 3;
        var si = f(dif) && (!q || quitarTildes(el.textContent + ' ' + (el.getAttribute('data-buscar') || '')).indexOf(q) >= 0);
        if (si) { el.removeAttribute('data-fj-oculto'); vistos++; } else el.setAttribute('data-fj-oculto', '');
      });
      var filtrando = q || nivel !== 'todas';
      barra.querySelector('.fj-n').textContent = filtrando ? vistos + ' de ' + items.length : items.length + ' ' + (items.length === 1 ? nombre : plural);
      vacio.hidden = vistos > 0 || !items.length;
    }
    input.addEventListener('input', aplicar);
    barra.querySelector('.fj-dif').addEventListener('click', function (e) {
      var b = e.target.closest('[data-nivel]');
      if (!b) return;
      nivel = b.getAttribute('data-nivel');
      barra.querySelectorAll('[data-nivel]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      aplicar();
    });
    aplicar();
    return { aplicar: aplicar, barra: barra, quitar: function () { barra.remove(); vacio.remove(); } };
  }

  window.FiltroJuegos = { montar: montar };
})();

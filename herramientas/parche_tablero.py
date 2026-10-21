"""Añade a todos los pc.html (Modo PC) dos mejoras de la mesa:

1. TABLERO LIBRE: las cartas de la mesa se arrastran (ratón o dedo) y se dejan donde se quiera; la posición se guarda con la partida. Las cartas
   nuevas se colocan solas en un hueco libre. El botón «Ordenar la mesa» las recoloca por número.
2. AUTOMÁTICO: cada carta que manda coger o descartar otras tiene un botón «Hacer lo que dice la carta» (en la mesa y en la carta ampliada) que
   coge y descarta todas de una vez; y las cartas combinables con su pareja ya en mesa tienen «Combinar con la N», que coge la carta resultado.

Idempotente. Uso (desde la raíz del repo):  python herramientas/parche_tablero.py
"""
import glob

CSS = """  /* ===== Tablero libre: las cartas se colocan arrastrándolas ===== */
  #mesa.tablero{display:block;position:relative;min-height:340px;border:1px dashed var(--line);border-radius:12px;background:rgba(255,255,255,.015)}
  #mesa.tablero .item{position:absolute;touch-action:none;user-select:none;-webkit-user-select:none}
  #mesa.tablero .item .carta-btn{cursor:grab;touch-action:none}
  #mesa.tablero .item.arrastrando{z-index:2000 !important}
  #mesa.tablero .item.arrastrando .carta-btn{cursor:grabbing}
  #mesa.tablero .item.arrastrando .carta{transform:scale(1.03);box-shadow:0 16px 34px rgba(0,0,0,.7)}
  .item .auto{padding:5px 12px;font-size:.8rem;border-color:#7be495;color:#b9f5cb}
  #zAuto[hidden]{display:none}
"""

JS = """  // ----- Tablero libre: arrastrar las cartas de la mesa y dejarlas donde se quiera (la posición se guarda con la partida) -----
  var arrastre = null, huboArrastre = false;
  function colocarTablero(){
    var mesa = $('mesa'), items = [].slice.call(mesa.querySelectorAll('.item'));
    if (!items.length) { mesa.style.height = ''; return; }
    var W = mesa.clientWidth || 800, M = 12, pos = estado.pos || (estado.pos = {}), rects = [], fijos = [], nuevos = [];
    items.forEach(function(it){ it.style.left = '0px'; it.style.top = '0px'; (pos[it.dataset.id] ? fijos : nuevos).push(it); });
    fijos.forEach(function(it){
      var p = pos[it.dataset.id], w = it.offsetWidth, h = it.offsetHeight;
      p.x = Math.max(0, Math.min(p.x, Math.max(0, W - w))); p.y = Math.max(0, p.y);
      it.style.left = p.x + 'px'; it.style.top = p.y + 'px';
      rects.push({x: p.x, y: p.y, w: w, h: h});
    });
    nuevos.forEach(function(it){
      var w = it.offsetWidth, h = it.offsetHeight, pp = null;
      for (var y = M; !pp; y += 24) {
        for (var x = M; (x === M || x + w <= W - M) && !pp; x += 24) {
          if (!rects.some(function(r){ return x < r.x + r.w + 10 && r.x < x + w + 10 && y < r.y + r.h + 10 && r.y < y + h + 10; })) pp = {x: x, y: y};
        }
      }
      pos[it.dataset.id] = pp; it.style.left = pp.x + 'px'; it.style.top = pp.y + 'px';
      rects.push({x: pp.x, y: pp.y, w: w, h: h});
    });
    ajustarAlto();
    if (nuevos.length) guardar();
  }
  function ajustarAlto(){
    var mesa = $('mesa'), alto = 340;
    [].slice.call(mesa.querySelectorAll('.item')).forEach(function(it){ alto = Math.max(alto, parseFloat(it.style.top || 0) + it.offsetHeight + 12); });
    mesa.style.height = alto + 'px';
    [].slice.call(mesa.querySelectorAll('.item')).forEach(function(it){ it.style.zIndex = String(estado.mesa.indexOf(it.dataset.id) + 1); });
  }
  function iniciarArrastre(e){
    var it = e.target.closest ? e.target.closest('#mesa .item') : null;
    if (!it || (e.button !== undefined && e.button > 0)) return;
    if (e.target.closest('button') && !e.target.closest('.carta-btn')) return;
    var p = estado.pos && estado.pos[it.dataset.id];
    if (!p) return;
    arrastre = {it: it, id: it.dataset.id, x0: e.clientX, y0: e.clientY, px: p.x, py: p.y, mov: false, pid: e.pointerId};
  }
  function moverArrastre(e){
    if (!arrastre || e.pointerId !== arrastre.pid) return;
    var dx = e.clientX - arrastre.x0, dy = e.clientY - arrastre.y0;
    if (!arrastre.mov) {
      if (Math.abs(dx) + Math.abs(dy) < 6) return;
      arrastre.mov = true; arrastre.it.classList.add('arrastrando');
      try { arrastre.it.setPointerCapture(e.pointerId); } catch (_) {}
    }
    var it = arrastre.it, W = $('mesa').clientWidth;
    it.style.left = Math.max(0, Math.min(arrastre.px + dx, Math.max(0, W - it.offsetWidth))) + 'px';
    it.style.top = Math.max(0, arrastre.py + dy) + 'px';
    e.preventDefault();
  }
  function finArrastre(e){
    if (!arrastre || e.pointerId !== arrastre.pid) return;
    var a = arrastre; arrastre = null;
    a.it.classList.remove('arrastrando');
    if (!a.mov) return;
    huboArrastre = true; setTimeout(function(){ huboArrastre = false; }, 60);
    estado.pos[a.id] = {x: parseFloat(a.it.style.left) || 0, y: parseFloat(a.it.style.top) || 0};
    quitar(estado.mesa, a.id); estado.mesa.push(a.id);        // la última carta tocada queda encima
    ajustarAlto(); guardar();
  }
  $('mesa').addEventListener('pointerdown', iniciarArrastre);
  document.addEventListener('pointermove', moverArrastre, {passive: false});
  document.addEventListener('pointerup', finArrastre);
  document.addEventListener('pointercancel', finArrastre);
  $('mesa').addEventListener('click', function(e){ if (huboArrastre) { e.stopPropagation(); e.preventDefault(); } }, true);
  var tRedim = null;
  window.addEventListener('resize', function(){ clearTimeout(tRedim); tRedim = setTimeout(function(){ if (estado) colocarTablero(); }, 150); });
  function ordenarMesa(){
    estado.mesa.sort(orden); estado.pos = {};
    mensaje('Cartas ordenadas por número.'); guardar(); pintar();
  }

  // ----- Automático: coger y descartar de una vez lo que manda la carta, y combinar con la pareja que ya está en mesa -----
  function tieneAuto(id){ var c = DATA[id]; return !!(c && ((c.coge && c.coge.length) || (c.descarta && c.descarta.length))); }
  function parejaCombinable(id){
    var c = DATA[id];
    if (!c || !c.combina || String(c.combina[0]).charAt(0) === '+') return null;
    var con = String(c.combina[0]), da = String(c.combina[1]);
    if (!DATA[da] || estado.mesa.indexOf(con) < 0 || estado.mesa.indexOf(da) >= 0 || estado.descartes.indexOf(da) >= 0) return null;
    return {con: con, da: da};
  }
  function aplicarCarta(id){
    var c = DATA[id], cogidas = [], descartadas = [];
    (c.coge || []).forEach(function(x){
      x = String(x);
      if (!DATA[x] || estado.mesa.indexOf(x) >= 0) return;
      quitar(estado.descartes, x); estado.mesa.push(x); cogidas.push(x);
    });
    (c.descarta || []).forEach(function(x){
      x = String(x);
      if (estado.mesa.indexOf(x) < 0) return;
      quitar(estado.mesa, x); delete estado.pos[x];
      if (estado.descartes.indexOf(x) < 0) estado.descartes.push(x);
      descartadas.push(x);
    });
    var t = [];
    if (cogidas.length) t.push((cogidas.length > 1 ? 'Has cogido las cartas ' : 'Has cogido la carta ') + cogidas.join(', '));
    if (descartadas.length) t.push((descartadas.length > 1 ? 'has descartado las cartas ' : 'has descartado la carta ') + descartadas.join(', '));
    mensaje(t.length ? t.join(' y ').replace(/^h/, 'H') + '.' : 'Ya está todo hecho: no hay nada más que coger ni descartar.');
    recienTomada = cogidas[0] || null; cerrarZoom(); guardar(); pintar();
  }
  function combinarCarta(id){
    var p = parejaCombinable(id);
    if (!p) return;
    estado.mesa.push(p.da); recienTomada = p.da;
    mensaje('Has combinado la carta ' + id + ' con la ' + p.con + ': coges la carta ' + p.da + '.');
    guardar(); pintar();
  }
  function botonesAuto(id){
    var bs = [];
    if (tieneAuto(id)) {
      var a = document.createElement('button'); a.type = 'button'; a.className = 'mini auto'; a.textContent = 'Hacer lo que dice';
      a.title = 'Coge y descarta de una vez las cartas que indica la carta ' + id;
      a.addEventListener('click', function(){ aplicarCarta(id); });
      bs.push(a);
    }
    var p = parejaCombinable(id);
    if (p) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'mini auto'; b.textContent = 'Combinar con la ' + p.con;
      b.title = 'Suma los números y coge la carta ' + p.da;
      b.addEventListener('click', function(){ combinarCarta(id); });
      bs.push(b);
    }
    return bs;
  }

"""

CAMBIOS = [
    ("  #zVoltear[hidden]{display:none}\n", "  #zVoltear[hidden]{display:none}\n" + CSS),
    ("""      <button type="button" id="reset">Reiniciar</button>\n""",
     """      <button type="button" id="ordenar" title="Recoloca las cartas de la mesa por número">Ordenar la mesa</button>\n      <button type="button" id="reset">Reiniciar</button>\n"""),
    ("""  <div id="msg" role="status" aria-live="polite"></div>\n""",
     """  <p class="aviso">Arrastra las cartas por la mesa para colocarlas como quieras. Las que mandan coger o descartar otras tienen un botón para hacerlo de una vez.</p>\n  <div id="msg" role="status" aria-live="polite"></div>\n"""),
    ("""    <button type="button" id="zDescartar" class="primario">Descartar</button>\n""",
     """    <button type="button" id="zAuto" class="primario" hidden>Hacer lo que dice la carta</button>\n    <button type="button" id="zDescartar" class="primario">Descartar</button>\n"""),
    ("function nuevoEstado(){ return {mesa:['P'], descartes:[]}; }", "function nuevoEstado(){ return {mesa:['P'], descartes:[], pos:{}}; }"),
    ("    if (!vistos.P) s.mesa.unshift('P');\n    return s;",
     "    if (!vistos.P) s.mesa.unshift('P');\n    s.pos = s.pos || {};\n    Object.keys(s.pos).forEach(function(k){ if (s.mesa.indexOf(k) < 0) delete s.pos[k]; });\n    return s;"),
    ("    var mesa = $('mesa'); mesa.innerHTML = '';\n", "    var mesa = $('mesa'); mesa.innerHTML = ''; mesa.className = 'fila tablero';\n"),
    ("      mesa.appendChild(it);\n    });\n    recienTomada = null;",
     "      botonesAuto(id).forEach(function(x){ it.appendChild(x); });\n      it.dataset.id = id;\n      mesa.appendChild(it);\n    });\n    colocarTablero();\n    recienTomada = null;"),
    ("  function quitar(arr, id){", JS + "  function quitar(arr, id){"),
    ("function descartar(id){ quitar(estado.mesa, id);", "function descartar(id){ quitar(estado.mesa, id); delete estado.pos[id];"),
    ("zoomId = id; $('zoomCarta').innerHTML = frente(id); $('zVoltear').hidden", "zoomId = id; $('zoomCarta').innerHTML = frente(id); $('zAuto').hidden = !tieneAuto(id); $('zVoltear').hidden"),
    ("  $('zVoltear').addEventListener('click', function(){ if (zoomId)",
     "  $('zAuto').addEventListener('click', function(){ if (zoomId) aplicarCarta(zoomId); });\n  $('ordenar').addEventListener('click', ordenarMesa);\n  $('zVoltear').addEventListener('click', function(){ if (zoomId)"),
]


def main():
    for ruta in sorted(glob.glob("juegos/el-faro/pc.html") + glob.glob("juegos/aventuras-ca/*/pc.html")):
        txt = open(ruta, encoding="utf-8").read()
        if "colocarTablero" in txt:
            print("ya estaba:", ruta)
            continue
        for viejo, nuevo in CAMBIOS:
            assert txt.count(viejo) == 1, f"{ruta}: no encuentro {viejo[:70]!r} ({txt.count(viejo)})"
            txt = txt.replace(viejo, nuevo)
        open(ruta, "w", encoding="utf-8", newline="\n").write(txt)
        print("parcheado:", ruta)


if __name__ == "__main__":
    main()

"""Añade a pc.html e imprimir.html el soporte de cartas-mosaico (piezas que se juntan para formar un dibujo) y la «Mesa de montaje» del Modo PC.
Es idempotente y no cambia nada en los juegos sin campo `mosaico` en sus cartas. Uso: python herramientas/parche_mosaicos.py"""
import glob
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def una(txt, viejo, nuevo):
    assert txt.count(viejo) == 1, f"se esperaba 1 aparición de {viejo[:70]!r} y hay {txt.count(viejo)}"
    return txt.replace(viejo, nuevo)


PC_CSS = """  /* ===== Cartas-mosaico: piezas sin borde que se juntan; el número va en la esquina exterior del mosaico ===== */
  .carta.mosaico{border:0}
  .carta.mosaico.mz-r .num{left:auto;right:calc(1.4 * var(--mm))}
  .carta.mosaico.mz-b .num{top:auto;bottom:calc(1.4 * var(--mm))}
  .montajes{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
  .montajes:empty{display:none}
  #montaje{position:fixed;inset:0;z-index:60;background:rgba(2,6,12,.93);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:16px;overflow:auto}
  #montaje[hidden]{display:none}
  #montaje h3{margin:0;font-size:1.1rem}
  #montaje .aviso{margin:0;text-align:center;max-width:520px}
  .mt-grid{--cw:min(38vw,230px,calc(33vh * 63 / 88));display:grid;grid-template-columns:repeat(var(--cols),var(--cw));grid-auto-rows:calc(var(--cw) * 88 / 63);gap:0;border:2px solid var(--line);border-radius:6px;overflow:hidden;background:#000}
  .mt-grid.una{--cw:min(60vw,300px,calc(33vh * 63 / 88))}
  .mt-tile{padding:0;border:0;border-radius:0;background:#1b2733 center/cover no-repeat;cursor:pointer;outline:1px solid rgba(255,255,255,.22);outline-offset:-1px}
  .mt-tile.sel{outline:3px solid var(--acc);outline-offset:-3px;filter:brightness(1.18)}
  .mt-grid.hecho{border-color:#7be495;box-shadow:0 0 30px rgba(123,228,149,.55)}
  .mt-grid.hecho .mt-tile{outline:0;cursor:default}
  #mMsg{min-height:1.5em;margin:0;font-weight:600;color:#7be495;text-align:center}

"""

PC_FUNCS = """  function frenteMosaico(id, c){
    var m = c.mosaico;
    var cls = 'carta mosaico' + (m.filas > 1 && m.fila >= m.filas - 1 ? ' mz-b' : '') + (m.cols > 1 && m.col >= m.cols - 1 ? ' mz-r' : '');
    return '<div class="' + cls + '" style="--c:#8a94a3"><div class="arte" style="background-image:url(\\'img/' + esc(id) + '.jpg\\')"></div><div class="num">' + esc(id) + '</div></div>';
  }

  // ----- Mesa de montaje: se tocan dos piezas para cambiarlas de sitio hasta que el dibujo encaje -----
  var MONT = {}, montActual = null, montSel = null;
  function mosaicos(){ return (DATA._meta && DATA._meta.mosaicos) || {}; }
  function pintarMontajes(){
    var cont = $('montajes'); cont.innerHTML = '';
    var ms = mosaicos();
    Object.keys(ms).forEach(function(k){
      var m = ms[k];
      if (!m.cartas.every(function(id){ return estado.mesa.indexOf(id) >= 0; })) return;
      var b = document.createElement('button'); b.type = 'button'; b.className = 'montar primario'; b.dataset.mosaico = k;
      b.textContent = (MONT[k] && MONT[k].hecho ? '✔ ' : '') + 'Mesa de montaje: ' + m.titulo;
      b.addEventListener('click', function(){ abrirMontaje(k); });
      cont.appendChild(b);
    });
  }
  function barajaInicial(c){
    // permutación fija en la que ninguna pieza empieza en su sitio
    if (c.length === 2) return [c[1], c[0]];
    return [c[1], c[3], c[0], c[2]];
  }
  function abrirMontaje(k){
    var m = mosaicos()[k];
    if (!MONT[k]) MONT[k] = {perm: barajaInicial(m.cartas), hecho: false};
    montActual = k; montSel = null;
    $('mTitulo').textContent = m.titulo;
    pintarMontaje();
    $('montaje').hidden = false; $('mCerrar').focus();
  }
  function pintarMontaje(){
    var m = mosaicos()[montActual], s = MONT[montActual], g = $('mGrid');
    g.className = 'mt-grid' + (m.cols === 1 ? ' una' : '') + (s.hecho ? ' hecho' : '');
    g.style.setProperty('--cols', m.cols);
    g.innerHTML = '';
    s.perm.forEach(function(id, i){
      var b = document.createElement('button'); b.type = 'button'; b.className = 'mt-tile' + (montSel === i ? ' sel' : '');
      b.dataset.pos = i; b.dataset.id = id; b.style.backgroundImage = "url('img/" + id + ".jpg')";
      b.setAttribute('aria-label', 'Pieza de la posición ' + (i + 1) + (montSel === i ? ' (elegida)' : ''));
      b.addEventListener('click', function(){ tocarPieza(i); });
      g.appendChild(b);
    });
    $('mMsg').textContent = s.hecho ? '¡Encajan! Ya se ve el dibujo entero.' : '';
  }
  function tocarPieza(i){
    var s = MONT[montActual], m = mosaicos()[montActual];
    if (s.hecho) return;
    if (montSel === null) montSel = i;
    else if (montSel === i) montSel = null;
    else { var t = s.perm[i]; s.perm[i] = s.perm[montSel]; s.perm[montSel] = t; montSel = null; }
    s.hecho = s.perm.every(function(id, j){ return id === m.cartas[j]; });
    pintarMontaje();
    if (s.hecho) pintarMontajes();
  }
  function cerrarMontaje(){ montActual = null; $('montaje').hidden = true; }
  $('mCerrar').addEventListener('click', cerrarMontaje);
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && !$('montaje').hidden) cerrarMontaje(); });

"""

PC_MODAL = """<div id="montaje" hidden role="dialog" aria-modal="true" aria-label="Mesa de montaje">
  <h3 id="mTitulo"></h3>
  <p class="aviso">Toca una pieza y luego otra para cambiarlas de sitio, hasta que los bordes del dibujo continúen de una a otra.</p>
  <div id="mGrid" class="mt-grid"></div>
  <p id="mMsg" role="status" aria-live="polite"></p>
  <button type="button" id="mCerrar">Cerrar</button>
</div>

"""


def parchear_pc(p):
    t = open(p, encoding="utf-8").read()
    if "frenteMosaico" in t:
        return False
    t = una(t, "  .dorso{--c:#ffd27a;background:radial-gradient(circle at 50% 36%", PC_CSS + "  .dorso{--c:#ffd27a;background:radial-gradient(circle at 50% 36%")
    t = una(t, '  <section class="mesa" aria-label="Cartas en mesa">', '  <div id="montajes" class="montajes"></div>\n\n  <section class="mesa" aria-label="Cartas en mesa">')
    t = una(t, '<div id="zoom" hidden role="dialog"', PC_MODAL + '<div id="zoom" hidden role="dialog"')
    t = una(t, "  function frente(id){\n    var c = DATA[id], color = COLORES[c.tipo] || COLORES.gris;\n",
            "  function frente(id){\n    var c = DATA[id], color = COLORES[c.tipo] || COLORES.gris;\n    if (c.mosaico) return frenteMosaico(id, c);\n")
    t = una(t, "    recienTomada = null;\n\n    var mz", "    recienTomada = null;\n    pintarMontajes();\n\n    var mz")
    t = una(t, "  fetchCartas().then(function(r){ if (!r.ok)", PC_FUNCS + "  fetchCartas().then(function(r){ if (!r.ok)")
    open(p, "w", encoding="utf-8", newline="\n").write(t)
    return True


IMP_CSS = """  /* cartas-mosaico: sin borde, para que al juntarlas el dibujo continúe; número y QR en la esquina exterior */
  .carta.mosaico{border:0}
  .carta.mosaico .num{top:1.4mm;left:1.4mm}
  .carta.mosaico.mz-r .num{left:auto;right:1.4mm}
  .carta.mosaico.mz-b .num{top:auto;bottom:1.4mm}
  .carta.mosaico .qr{top:auto;bottom:1.4mm;left:1.4mm;right:auto}
  .carta.mosaico.mz-r .qr{left:auto;right:1.4mm}
  .carta.mosaico.mz-b .qr{bottom:auto;top:1.4mm}

"""

IMP_JS = """    if (c.mosaico) {
      var mz = c.mosaico;
      return '<div class="carta mosaico' + (mz.filas > 1 && mz.fila >= mz.filas - 1 ? ' mz-b' : '') + (mz.cols > 1 && mz.col >= mz.cols - 1 ? ' mz-r' : '') + '" style="--c:#8a94a3"><div class="arte" data-id="' + esc(id) + '"></div>' +
        '<div class="num">' + esc(id) + '</div><div class="qr" data-qr="CA:' + CLAVE_JUEGO + ':' + esc(id) + '" aria-hidden="true"></div></div>';
    }
"""


def parchear_imprimir(p):
    t = open(p, encoding="utf-8").read()
    if "carta mosaico" in t:
        return False
    t = una(t, "  @page{size:A4;margin:0}", IMP_CSS + "  @page{size:A4;margin:0}")
    t = una(t, "    var c = J[id], color = COLORES[c.tipo] || COLORES.gris;\n", "    var c = J[id], color = COLORES[c.tipo] || COLORES.gris;\n" + IMP_JS)
    open(p, "w", encoding="utf-8", newline="\n").write(t)
    return True


if __name__ == "__main__":
    carpetas = ["juegos/el-faro"] + [os.path.dirname(f).replace("\\", "/").replace(RAIZ.replace("\\", "/") + "/", "") for f in glob.glob(os.path.join(RAIZ, "juegos", "aventuras-ca", "*", "pc.html"))]
    for c in sorted(set(carpetas)):
        for nombre, fn in (("pc.html", parchear_pc), ("imprimir.html", parchear_imprimir)):
            ruta = os.path.join(RAIZ, c, nombre)
            if os.path.exists(ruta):
                print(("parcheado " if fn(ruta) else "al dia    ") + os.path.join(c, nombre))

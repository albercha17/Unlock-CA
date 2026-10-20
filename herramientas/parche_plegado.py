"""Añade a todos los pc.html el soporte de CARTAS QUE SE PLIEGAN (campo `plegado` de cartas.json, «Mar de las Brumas, 1715»).

`plegado` = {"x": [a, b], "y": [c, d]} en fracciones del ancho/alto de la ilustración: al plegar la carta en acordeón, la franja [a, b) (y la
[c, d)) queda escondida detrás y los trozos de los lados se juntan. En la mesa y en la carta ampliada sale el botón «Plegar», que enseña la
carta plegada (más estrecha, centrada). En papel, la propia ilustración trae las líneas A, B, C y D. Idempotente.
Uso (desde la raíz del repo):  python herramientas/parche_plegado.py
"""
import glob

CSS = """  #zPlegar[hidden]{display:none}
  /* ===== Cartas que se pliegan: los trozos visibles se juntan y la carta se estrecha ===== */
  .arte.plegada{background:#0b1218}
  .pl-trozo{position:absolute;overflow:hidden}
  .pl-trozo i{position:absolute;display:block;background:center / 100% 100% no-repeat}
"""

JS = """  function artePlegada(id, p){
    // trozos que quedan a la vista (fracciones de la ilustración) y su sitio en la carta plegada, centrada
    var xs = p.x ? [[0, p.x[0]], [p.x[1], 1]] : [[0, 1]], ys = p.y ? [[0, p.y[0]], [p.y[1], 1]] : [[0, 1]];
    function total(r){ return r.reduce(function(s, a){ return s + a[1] - a[0]; }, 0); }
    var h = '<div class="arte plegada">', oy = (1 - total(ys)) / 2;
    ys.forEach(function(ry){
      var ox = (1 - total(xs)) / 2, hh = ry[1] - ry[0];
      xs.forEach(function(rx){
        var w = rx[1] - rx[0];
        h += '<div class="pl-trozo" style="left:' + ox * 100 + '%;top:' + oy * 100 + '%;width:' + w * 100 + '%;height:' + hh * 100 + '%">' +
             '<i style="background-image:url(\\'img/' + esc(id) + '.jpg\\');left:' + (-rx[0] / w * 100) + '%;top:' + (-ry[0] / hh * 100) + '%;width:' + (100 / w) + '%;height:' + (100 / hh) + '%"></i></div>';
        ox += w;
      });
      oy += hh;
    });
    return h + '</div>';
  }
"""

CAMBIOS = [
    ("  #zVoltear[hidden]{display:none}\n", "  #zVoltear[hidden]{display:none}\n" + CSS),
    ("""    <button type="button" id="zVoltear" class="voltear" hidden>Dar la vuelta</button>\n""",
     """    <button type="button" id="zVoltear" class="voltear" hidden>Dar la vuelta</button>\n    <button type="button" id="zPlegar" class="plegar" hidden>Plegar</button>\n"""),
    ("var DATA = null, estado = null, zoomId = null, VOLT = {};", "var DATA = null, estado = null, zoomId = null, VOLT = {}, PLEG = {};"),
    ("""    var h = '<div class="carta' + (conacc ? ' conacc' : '') + '" style="--c:' + color + '"><div class="arte" style="background-image:url(\\'img/' + esc(id) + (c.reverso && VOLT[id] ? 'r' : '') + '.jpg\\')"></div><div class="num">' + esc(id) + '</div>';""",
     """    var arte = c.plegado && PLEG[id] ? artePlegada(id, c.plegado) : '<div class="arte" style="background-image:url(\\'img/' + esc(id) + (c.reverso && VOLT[id] ? 'r' : '') + '.jpg\\')"></div>';
    var h = '<div class="carta' + (conacc ? ' conacc' : '') + '" style="--c:' + color + '">' + arte + '<div class="num">' + esc(id) + '</div>';"""),
    ("  function dorso(id){", JS + "  function dorso(id){"),
    ("""      if (DATA[id].reverso) { var v = document.createElement('button');""",
     """      if (DATA[id].plegado) { var pg = document.createElement('button'); pg.type = 'button'; pg.className = 'voltear plegar'; pg.textContent = PLEG[id] ? 'Desplegar' : 'Plegar'; pg.addEventListener('click', function(){ PLEG[id] = !PLEG[id]; pintar(); }); it.appendChild(pg); }
      if (DATA[id].reverso) { var v = document.createElement('button');"""),
    ("$('zVoltear').hidden = !DATA[id].reverso; $('zoom').hidden = false;",
     "$('zVoltear').hidden = !DATA[id].reverso; $('zPlegar').hidden = !DATA[id].plegado; $('zPlegar').textContent = PLEG[id] ? 'Desplegar' : 'Plegar'; $('zoom').hidden = false;"),
    ("""  $('zoom').addEventListener('click', function(e){""",
     """  $('zPlegar').addEventListener('click', function(){ if (zoomId) { PLEG[zoomId] = !PLEG[zoomId]; $('zoomCarta').innerHTML = frente(zoomId); $('zPlegar').textContent = PLEG[zoomId] ? 'Desplegar' : 'Plegar'; pintar(); } });
  $('zoom').addEventListener('click', function(e){"""),
]


def main():
    for ruta in sorted(glob.glob("juegos/el-faro/pc.html") + glob.glob("juegos/aventuras-ca/*/pc.html")):
        txt = open(ruta, encoding="utf-8").read()
        if "artePlegada" in txt:
            print("ya estaba:", ruta)
            continue
        for viejo, nuevo in CAMBIOS:
            assert txt.count(viejo) == 1, f"{ruta}: no encuentro {viejo[:70]!r}"
            txt = txt.replace(viejo, nuevo)
        open(ruta, "w", encoding="utf-8", newline="\n").write(txt)
        print("parcheado:", ruta)


if __name__ == "__main__":
    main()

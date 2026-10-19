"""Reversos ambientados para imprimir a doble cara (imprimir.html de todos los juegos).

Cada hoja de 9 cartas va seguida de su hoja de REVERSOS, con las columnas invertidas para que cada reverso quede detrás de su carta al imprimir a doble cara
(volteando por el lado largo). El reverso de cada carta lleva su NÚMERO en grande y el diseño propio del juego (colores, dibujo repetido, emoji y título);
las cartas con dos caras de verdad (campo `reverso`) llevan su reverso ilustrado en vez del genérico. Ya no hay una hoja final de dorsos iguales.

El diseño de cada juego está en la tabla TABLA (clave = la `CLAVE_JUEGO` de su imprimir.html, que es el tema del juego). Al crear un juego nuevo:
añade su entrada a TABLA y ejecuta  python herramientas/parche_dorsos.py  (es idempotente: la primera vez cambia la estructura y después solo refresca la tabla).
"""
import glob
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATRONES = {
    "faro": "repeating-linear-gradient(115deg,rgba(255,255,255,.06) 0 6mm,transparent 6mm 12mm)",
    "egipto": "repeating-linear-gradient(45deg,rgba(0,0,0,.2) 0 3mm,transparent 3mm 6mm),repeating-linear-gradient(-45deg,rgba(255,255,255,.08) 0 3mm,transparent 3mm 6mm)",
    "marte": "radial-gradient(circle,rgba(255,255,255,.12) .6mm,transparent .7mm) 0 0/4mm 4mm",
    "florencia": "repeating-linear-gradient(60deg,rgba(255,220,140,.14) 0 .5mm,transparent .5mm 5mm),repeating-linear-gradient(-60deg,rgba(255,220,140,.14) 0 .5mm,transparent .5mm 5mm)",
    "dinosaurios": "radial-gradient(circle at 50% 100%,rgba(255,255,255,.12) 0 2.2mm,transparent 2.3mm) 0 0/5mm 4mm",
    "cuento": "radial-gradient(circle,rgba(255,240,170,.4) .5mm,transparent .6mm) 0 0/7mm 7mm",
    "trono": "repeating-linear-gradient(0deg,rgba(255,255,255,.07) 0 .4mm,transparent .4mm 4mm),repeating-linear-gradient(90deg,rgba(255,255,255,.07) 0 .4mm,transparent .4mm 4mm)",
    "pompeya": "conic-gradient(rgba(0,0,0,.2) 25%,transparent 0 50%,rgba(0,0,0,.2) 0 75%,transparent 0) 0 0/6mm 6mm",
    "arcade": "repeating-linear-gradient(0deg,rgba(255,80,220,.28) 0 .3mm,transparent .3mm 5mm),repeating-linear-gradient(90deg,rgba(80,230,255,.28) 0 .3mm,transparent .3mm 5mm)",
    "oeste": "repeating-linear-gradient(90deg,rgba(0,0,0,.24) 0 .4mm,transparent .4mm 8mm)",
    "espia": "radial-gradient(circle,rgba(255,255,255,.16) .7mm,transparent .8mm) 0 0/3mm 3mm",
    "futbol": "repeating-linear-gradient(90deg,rgba(255,255,255,.08) 0 8mm,transparent 8mm 16mm)",
}

# tema -> (título corto, emoji, [color de arriba, color de abajo], color de realce, color claro)
TABLA = {
    "faro": ("El Faro de Cabo Niebla", "🌊", ["#0e3a52", "#04101a"], "#c9a45a", "#f0d9a0"),
    "egipto": ("Egipto, 1274 a.C.", "🏺", ["#4a3512", "#150f05"], "#e0b04a", "#f2d27a"),
    "marte": ("Marte, 2157", "🚀", ["#5a2a14", "#12060a"], "#ff8a50", "#ffb085"),
    "florencia": ("Florencia, 1503", "🪞", ["#5a3a1a", "#140c06"], "#d9a441", "#f0c773"),
    "dinosaurios": ("Cretácico", "🦖", ["#2f5a22", "#07120a"], "#b5e35b", "#d9f59a"),
    "cuento": ("Érase una vez", "📖", ["#4a2a8a", "#120a2a"], "#f6c453", "#ffe08a"),
    "trono": ("Hielo y Fuego", "🐉", ["#2c3a4a", "#0a0f16"], "#8fc7ee", "#cfe8fb"),
    "pompeya": ("Pompeya, 79 d.C.", "🌋", ["#6a3418", "#150a06"], "#e08a4a", "#f5c08a"),
    "arcade": ("Game Over, 1985", "🕹️", ["#4a1a7a", "#07040f"], "#ff5ad8", "#8ffcff"),
    "oeste": ("Dry Gulch, 1878", "🤠", ["#7a4a1e", "#160d06"], "#e0a040", "#f5d48a"),
    "espia": ("Montecarlo, 1965", "🕵️", ["#0e5a6a", "#07121a"], "#ff6fa8", "#7fe8f0"),
    "futbol": ("La Final del Siglo", "⚽", ["#1f6a30", "#06140a"], "#f2c230", "#a8ec96"),
}


def tabla_js():
    d = {k: {"titulo": t, "emoji": e, "c": c, "ac": a, "ac2": a2, "patron": PATRONES[k]} for k, (t, e, c, a, a2) in TABLA.items()}
    return "/*DORSOS*/ var DORSOS = " + json.dumps(d, ensure_ascii=False) + "; /*FIN-DORSOS*/"


CSS = """  /* reversos ambientados (uno por carta, con su número); van en una hoja detrás de cada hoja de cartas, con las columnas invertidas */
  .guias .dorsoN{outline:.2mm dashed #888;outline-offset:.6mm}
  .dorsoN{position:relative;width:63mm;height:88mm;border-radius:3mm;overflow:hidden;border:1.6mm solid var(--ac);color:#fff;display:flex;align-items:center;justify-content:center;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .dorsoN::after{content:"";position:absolute;inset:2.4mm;border:.4mm solid var(--ac);border-radius:1.6mm;opacity:.75}
  .dorsoN .dn-emoji{position:absolute;font-size:44mm;line-height:1;opacity:.17}
  .dorsoN .dn-num{position:relative;min-width:30mm;height:30mm;padding:0 4mm;border-radius:15mm;background:rgba(0,0,0,.55);border:.8mm solid var(--ac);display:flex;align-items:center;justify-content:center;font:800 34pt/1 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#fff}
  .dorsoN .dn-t{position:absolute;left:0;right:0;top:6mm;text-align:center;font:800 6.5pt system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;letter-spacing:.16em;color:var(--ac2);text-transform:uppercase;padding:0 5mm}
  .dorsoN .dn-b{position:absolute;left:0;right:0;bottom:6mm;text-align:center;font:700 5.5pt system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;letter-spacing:.22em;color:var(--ac2);opacity:.9}
"""

JS = """  """ + "{TABLA}" + """
  var D = DORSOS[CLAVE_JUEGO] || DORSOS.faro;
  var hayReversos = ids.some(function(k){ return J[k].reverso; });
  function dorsoCarta(k){
    return '<div class="dorsoN" style="--ac:' + D.ac + ';--ac2:' + D.ac2 + ';background:' + D.patron + ',radial-gradient(circle at 50% 42%,' + D.c[0] + ',' + D.c[1] + ' 78%)">' +
      '<div class="dn-t">' + esc(D.titulo) + '</div><div class="dn-emoji">' + D.emoji + '</div><div class="dn-num">' + esc(k) + '</div><div class="dn-b">UNLOCK C&amp;A</div></div>';
  }
  function hojaReverso(grupo){
    var celdas = [];
    for (var f = 0; f < 3; f++) for (var c = 2; c >= 0; c--) {
      var k = grupo[f * 3 + c];
      if (!k) celdas.push('<div></div>');
      else if (J[k].reverso) celdas.push('<div class="rev"><div class="arte-rev" data-rev="' + esc(k) + '"></div><div class="nr">R' + esc(k) + '</div></div>');
      else celdas.push(dorsoCarta(k));
    }
    return '<div class="hoja guias hoja-reverso">' + celdas.join('') + '</div>';
  }
"""

TEXTO_BARRA = "Consejo: imprime en A4 al 100 % (sin «ajustar a página») y a DOBLE CARA, volteando por el lado largo: cada hoja de cartas va seguida de su hoja de reversos, con el número de cada carta, ya colocada para que cuadre."


def parchear(p):
    t = open(p, encoding="utf-8").read()
    if "/*DORSOS*/" in t:
        nuevo = re.sub(r"/\*DORSOS\*/.*?/\*FIN-DORSOS\*/", lambda m: tabla_js(), t, flags=re.S)
        if nuevo == t:
            return False
        open(p, "w", encoding="utf-8", newline="\n").write(nuevo)
        return True
    # estructura (primera vez)
    a = t.index("  var hayReversos = ")
    b = t.index("  var tarjetas = ids.map(cartaHTML);")
    t = t[:a] + JS.replace("{TABLA}", tabla_js()) + t[b:]
    ini = t.index("  var dorsos = '';")
    fin = t.index("\n", t.index("for (var k = 0; k < 9; k++) dorsos +=")) + 1
    t = t[:ini] + t[fin:]
    viejo = ".join('') +\n    '<div class=\"hoja guias\">' + dorsos + '</div>';"
    assert t.count(viejo) == 1, "no encuentro la hoja final de dorsos"
    t = t.replace(viejo, ".join('');")
    m = re.search(r"  if \(hayReversos\) document\.querySelector\('\.barra'\)\.insertAdjacentHTML\(.*?\);\n", t)
    assert m, "no encuentro el aviso de reversos"
    t = t.replace(m.group(0), "")
    m = re.search(r'<span class="n">Consejo: imprime en A4.*?</span>', t)
    assert m, "no encuentro el consejo de impresión"
    t = t.replace(m.group(0), '<span class="n">' + TEXTO_BARRA + "</span>")
    assert t.count("  @page{size:A4;margin:0}") == 1
    t = t.replace("  @page{size:A4;margin:0}", CSS + "  @page{size:A4;margin:0}")
    open(p, "w", encoding="utf-8", newline="\n").write(t)
    return True


if __name__ == "__main__":
    carpetas = ["juegos/el-faro"] + sorted(os.path.dirname(f).replace("\\", "/").replace(RAIZ.replace("\\", "/") + "/", "") for f in glob.glob(os.path.join(RAIZ, "juegos", "aventuras-ca", "*", "imprimir.html")))
    for c in carpetas:
        ruta = os.path.join(RAIZ, c, "imprimir.html")
        print(("parcheado " if parchear(ruta) else "al dia    ") + c)

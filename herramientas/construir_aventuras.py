"""Construye las carpetas de juego de Aventuras-CA a partir de la plantilla del Faro. Ejecutar desde la raiz del repo."""
import json, os, shutil, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
import datos_egipto as E
import datos_marte as M

FARO = "Unlock-El-Faro"
TMP = os.path.dirname(os.path.abspath(__file__))


def leer(p):
    return open(p, encoding="utf-8").read()


def escribir(p, txt):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write(txt)


def sustituir(txt, viejo, nuevo, veces=1):
    assert txt.count(viejo) == veces, f"se esperaban {veces} apariciones de {viejo[:60]!r} y hay {txt.count(viejo)}"
    return txt.replace(viejo, nuevo)


JUEGOS = {
    "Egipto": dict(
        datos=E, titulo="Egipto, 1274 a.C.: El Ojo de Horus", emoji="🏺",
        grad="#4a3512,#150f05", acento="#e0b04a", acento2="#f2d27a", bg1="#120d05", bg2="#2a1d0a",
        sinopsis="Cristina y Alberto estrenan su Cronoportal y aterrizan en una cámara secreta bajo un templo de Tebas, en el año 1274 a.C. Con el aparato sin energía y solo una hora antes de que lleguen los sacerdotes, tienen que encontrar el Ojo de Horus.",
        minigames={"15": "15-papiro.js", "23": "23-muro.js", "47": "47-balanza.js", "71": "71-anillos.js", "95": "95-cristales.js"},
        pal=("#7a5a1e", "#2a1d0a")),
    "Marte": dict(
        datos=M, titulo="Marte, 2157: Cúpula Aurora", emoji="🚀",
        grad="#5a2a14,#12060a", acento="#ff8a50", acento2="#ffb085", bg1="#12070a", bg2="#2a120c",
        sinopsis="Segundo salto del Cronoportal: Marte, año 2157. La cúpula Aurora está a oscuras por una tormenta de polvo y el soporte vital se apaga. Cristina y Alberto tienen una hora para encontrar el núcleo de fusión y volver a casa.",
        minigames={"21": "21-terminal.js", "52": "52-tuberias.js", "66": "66-esclusa.js", "88": "88-calibrador.js", "33": "33-diario.js"},
        pal=("#8a3a1a", "#1c0c10")),
}

index_faro = leer(f"{FARO}/index.html")
pc_faro = leer(f"{FARO}/pc.html")
imprimir_faro = leer(f"{FARO}/imprimir.html")
prompts_tpl = leer(os.path.join(TMP, "prompts_plantilla.html"))

ORDEN_CAMPOS = ["titulo", "tipo", "coge", "descarta", "combina", "descripcion", "pistas", "textoCarta", "arte"]


def fuente(tam):
    for f in (r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, tam)
    return ImageFont.load_default()


def placeholder(ruta, titulo, c1, c2):
    w, h = 520, 726
    im = Image.new("RGB", (w, h), c1)
    px = im.load()
    a = tuple(int(c1[i:i + 2], 16) for i in (1, 3, 5))
    b = tuple(int(c2[i:i + 2], 16) for i in (1, 3, 5))
    for y in range(h):
        t = y / (h - 1)
        col = tuple(int(a[k] * (1 - t) + b[k] * t) for k in range(3))
        for x in range(w):
            px[x, y] = col
    d = ImageDraw.Draw(im)
    f = fuente(34)
    palabras, lineas, actual = titulo.split(), [], ""
    for p in palabras:
        prueba = (actual + " " + p).strip()
        if d.textlength(prueba, font=f) > w - 90:
            lineas.append(actual)
            actual = p
        else:
            actual = prueba
    lineas.append(actual)
    y = h // 2 - 20 * len(lineas)
    for l in lineas:
        d.text(((w - d.textlength(l, font=f)) / 2, y), l, font=f, fill=(255, 255, 255))
        y += 44
    f2 = fuente(18)
    t2 = "ilustración pendiente"
    d.text(((w - d.textlength(t2, font=f2)) / 2, h - 150), t2, font=f2, fill=(255, 255, 255, 180))
    im.save(ruta, quality=82)


for nombre, cfg in JUEGOS.items():
    base = f"Aventuras-CA/{nombre}"
    if os.path.exists(f"{base}/cartas.json") and "--forzar" not in sys.argv:
        sys.exit(f"{base} ya existe: no lo sobrescribo (los juegos se retocan a mano; usa --forzar solo si de verdad quieres regenerarlo).")
    datos = cfg["datos"]
    os.makedirs(f"{base}/juegos", exist_ok=True)
    os.makedirs(f"{base}/img", exist_ok=True)
    os.makedirs(f"{base}/video", exist_ok=True)

    # ficheros genericos
    shutil.copy(f"{FARO}/pistas.js", f"{base}/pistas.js")
    shutil.copy(f"{FARO}/juegos/ui.js", f"{base}/juegos/ui.js")
    if nombre != "Egipto":
        shutil.copy("Aventuras-CA/Egipto/juegos/lector.js", f"{base}/juegos/lector.js")
    css = leer(f"{FARO}/style.css")
    css += f"\n/* Aventuras C&A: {nombre} */\n:root{{ --accent:{cfg['acento']}; --accent-2:{cfg['acento2']}; --bg1:{cfg['bg1']}; --bg2:{cfg['bg2']}; }}\n"
    escribir(f"{base}/style.css", css)
    escribir(f"{base}/video/LEEME.txt", "Pon aqui el video de introduccion como videoInicial.mp4 (MP4 H.264, vertical 9:16, idealmente menos de 25 MB).\n")

    # index.html
    ix = index_faro
    ix = sustituir(ix, "<title>Unlock C&amp;A - El Faro de Cabo Niebla</title>", f"<title>Aventuras C&amp;A - {cfg['titulo']}</title>")
    g1, g2 = cfg["grad"].split(",")
    ix = sustituir(ix, 'background:radial-gradient(circle at 50% 30%,#1c3a4d,#0a1218);border:2px solid rgba(255,255,255,0.06)">🌊</div>',
                   f'background:radial-gradient(circle at 50% 30%,{g1},{g2});border:2px solid rgba(255,255,255,0.06)">{cfg["emoji"]}</div>')
    ix = sustituir(ix, '<h1 style="margin:0;font-size:20px">El Faro de Cabo Niebla</h1>', f'<h1 style="margin:0;font-size:20px">{cfg["titulo"]}</h1>')
    ix = sustituir(ix, "Tormenta, la gran lámpara apagada y un carguero a ciegas rumbo a las rocas. Inés y Marcos tienen una hora para encender el faro... y encontrar al abuelo Anselmo.", cfg["sinopsis"])
    ix = sustituir(ix, '<div class="game-logo-circle" aria-hidden="true">🌊</div>', f'<div class="game-logo-circle" aria-hidden="true">{cfg["emoji"]}</div>')
    ix = sustituir(ix, "<h2>El Faro de Cabo Niebla</h2>", f'<h2>{cfg["titulo"]}</h2>')
    ix = sustituir(ix, "← Volver al menú", "← Volver a Aventuras C&amp;A")
    mapa = ",\n".join(f"      '{k}': './juegos/{v}'" for k, v in cfg["minigames"].items())
    viejo_mapa = re.search(r"    const MINIGAMES = \{.*?\n    \};", ix, re.S).group(0)
    ix = ix.replace(viejo_mapa, "    const MINIGAMES = {\n" + mapa + "\n    };")
    escribir(f"{base}/index.html", ix)

    # pc.html
    pc = pc_faro
    pc = sustituir(pc, "<title>El Faro de Cabo Niebla — Modo PC</title>", f"<title>{cfg['titulo']} — Modo PC</title>")
    pc = sustituir(pc, "<h1>El Faro de Cabo Niebla<small>", f"<h1>{cfg['titulo']}<small>")
    escribir(f"{base}/pc.html", pc)

    # cartas.json
    out = {"_meta": datos.META}
    for k, c in datos.J.items():
        out[k] = {campo: c[campo] for campo in ORDEN_CAMPOS if campo in c}
    json.dump(out, open(f"{base}/cartas.json", "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    open(f"{base}/cartas.json", "a", encoding="utf-8").write("\n")

    # imagenes de relleno
    for k, c in datos.J.items():
        placeholder(f"{base}/img/{k}.jpg", c["titulo"].split("—", 1)[1].strip(), *cfg["pal"])

    # prompts.html e imprimir.html (en linea: leen cartas.json)
    escribir(f"{base}/prompts.html", prompts_tpl.replace("{{TITULO}}", cfg["titulo"]).replace("{{KEY}}", f"prompts-{nombre.lower()}"))
    im = imprimir_faro
    im = sustituir(im, "<title>Imprimir cartas — El Faro de Cabo Niebla</title>", f"<title>Imprimir cartas — {cfg['titulo']}</title>")
    im = sustituir(im, '<script src="cartas-data.js"></script>\n<script>\n(function(){',
                   "<script>\nfetch('cartas.json?v=' + Date.now(), {cache: 'no-store'}).then(function(r){ return r.json(); }).then(function(datos){\nwindow.JUEGO = datos;\n(function(){")
    im = sustituir(im, "})();\n</script>\n</body>", "})();\n}).catch(function(){ document.body.insertAdjacentHTML('beforeend', '<p style=\"padding:20px\">No se pudo cargar cartas.json. Abre esta página desde el sitio web publicado.</p>'); });\n</script>\n</body>")
    im = im.replace("'arte/'", "'img/'").replace("url(\"arte/", "url(\"img/")
    im = sustituir(im, "exts = ['png','jpg','jpeg','webp']", "exts = ['jpg']")
    im = sustituir(im, """      document.getElementById('resumen').textContent = faltan.length
        ? 'Faltan ilustraciones: ' + faltan.join(', ')
        : 'Todas las ilustraciones están listas.';""",
                   """      fetch('img/pendientes.json?v=' + Date.now(), {cache: 'no-store'}).then(function(r){ return r.ok ? r.json() : []; }).catch(function(){ return []; }).then(function(pend){
        var r = document.getElementById('resumen');
        if (faltan.length) r.textContent = 'Faltan ilustraciones: ' + faltan.join(', ');
        else if (pend.length) r.textContent = 'Ilustraciones de relleno (aún sin hacer): ' + pend.join(', ');
        else r.textContent = 'Todas las ilustraciones están listas.';
      });""")
    json.dump(sorted(datos.J.keys(), key=lambda k: (k != "P", int(k) if k != "P" else 0)), open(f"{base}/img/pendientes.json", "w", encoding="utf-8"))
    escribir(f"{base}/imprimir.html", im)

    print(nombre, "->", len(datos.J), "cartas")

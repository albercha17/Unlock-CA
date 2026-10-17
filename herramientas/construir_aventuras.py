"""Construye las carpetas de juego de juegos/aventuras-ca a partir de la plantilla del Faro. Ejecutar desde la raiz del repo."""
import json, os, shutil, subprocess, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
from juegos_config import FARO, JUEGOS, generar_index, leer, escribir, sustituir

TMP = os.path.dirname(os.path.abspath(__file__))


SOLO = [a.lower() for a in sys.argv[1:] if not a.startswith("--")]

index_faro = leer(f"{FARO}/index.html")
pc_faro = leer(f"{FARO}/pc.html")
imprimir_faro = leer(f"{FARO}/imprimir.html")
prompts_tpl = leer(os.path.join(TMP, "prompts_plantilla.html"))

ORDEN_CAMPOS = ["titulo", "tipo", "coge", "descarta", "combina", "descripcion", "pistas", "textoCarta", "textoEspejo", "mosaico", "arte"]


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
    if SOLO and nombre.lower() not in SOLO:
        continue
    base = f"juegos/aventuras-ca/{nombre.lower()}"
    if os.path.exists(f"{base}/cartas.json") and "--forzar" not in sys.argv:
        sys.exit(f"{base} ya existe: no lo sobrescribo (los juegos se retocan a mano; usa --forzar solo si de verdad quieres regenerarlo).")
    datos = cfg["datos"]
    os.makedirs(f"{base}/minijuegos", exist_ok=True)
    os.makedirs(f"{base}/img", exist_ok=True)
    os.makedirs(f"{base}/video", exist_ok=True)

    # ficheros genericos
    shutil.copy(f"{FARO}/pistas.js", f"{base}/pistas.js")
    shutil.copy(f"{FARO}/minijuegos/ui.js", f"{base}/minijuegos/ui.js")
    shutil.copy(f"{FARO}/app.css", f"{base}/app.css")
    shutil.copy(f"{FARO}/app.js", f"{base}/app.js")
    shutil.copy(f"{FARO}/musica.js", f"{base}/musica.js")
    if nombre != "Egipto":
        shutil.copy("juegos/aventuras-ca/egipto/minijuegos/lector.js", f"{base}/minijuegos/lector.js")
    css = leer(f"{FARO}/style.css")
    css += f"\n/* Aventuras C&A: {nombre} */\n:root{{ --accent:{cfg['acento']}; --accent-2:{cfg['acento2']}; --bg1:{cfg['bg1']}; --bg2:{cfg['bg2']}; }}\n"
    escribir(f"{base}/style.css", css)
    escribir(f"{base}/video/LEEME.txt", "Pon aqui el video de introduccion como videoInicial.mp4 (MP4 H.264, vertical 9:16, idealmente menos de 25 MB).\n")

    # index.html
    escribir(f"{base}/index.html", generar_index(index_faro, cfg))

    # pc.html
    pc = pc_faro
    pc = sustituir(pc, "<title>El Faro de Cabo Niebla — Modo PC</title>", f"<title>{cfg['titulo']} — Modo PC</title>")
    pc = sustituir(pc, "<h1>El Faro de Cabo Niebla<small>", f"<h1>{cfg['titulo']}<small>")
    # textos con simbolos (emojis): letra mas grande para que se lean al imprimir
    pc = sustituir(pc, "  .acc{position:absolute;", "  .texto.emoji{font-size:calc(4.4 * var(--mm));line-height:1.35;letter-spacing:.12em}\n  .acc{position:absolute;")
    pc = sustituir(pc, """h += '<div class="texto' + (c.textoEspejo ? ' espejo' : '') + '">' + c.textoCarta""", """h += '<div class="texto' + (/\\p{Extended_Pictographic}/u.test(c.textoCarta.join('')) ? ' emoji' : '') + (c.textoEspejo ? ' espejo' : '') + '">' + c.textoCarta""")
    escribir(f"{base}/pc.html", pc)

    # cartas.json
    out = {"_meta": datos.META}
    for k, c in datos.J.items():
        out[k] = {campo: c[campo] for campo in ORDEN_CAMPOS if campo in c}
    json.dump(out, open(f"{base}/cartas.json", "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    open(f"{base}/cartas.json", "a", encoding="utf-8").write("\n")

    # imagenes de relleno
    for k, c in datos.J.items():
        if os.path.exists(f"{base}/arte/{k}.png"):
            continue  # ya hay ilustracion real: no la pises con el relleno
        placeholder(f"{base}/img/{k}.jpg", c["titulo"].split("—", 1)[1].strip(), *cfg["pal"])

    # textura provisional del panel de los minijuegos (degradado); chatgpt_fondos.py la sustituye por una real
    ui_dir = f"{base}/img/ui"
    os.makedirs(ui_dir, exist_ok=True)
    if not os.path.exists(f"{ui_dir}/panel.jpg"):
        a = tuple(int(cfg["pal"][0][i:i + 2], 16) for i in (1, 3, 5))
        b = tuple(int(cfg["pal"][1][i:i + 2], 16) for i in (1, 3, 5))
        g = Image.new("RGB", (64, 96))
        px = g.load()
        for y in range(96):
            for x in range(64):
                px[x, y] = tuple(int(a[k] * (1 - y / 95) + b[k] * y / 95) for k in range(3))
        g.save(f"{ui_dir}/panel.jpg", quality=70)

    # prompts.html e imprimir.html (en linea: leen cartas.json)
    escribir(f"{base}/prompts.html", prompts_tpl.replace("{{TITULO}}", cfg["titulo"]).replace("{{KEY}}", f"prompts-{nombre.lower()}"))
    im = imprimir_faro
    im = sustituir(im, "<title>Imprimir cartas — El Faro de Cabo Niebla</title>", f"<title>Imprimir cartas — {cfg['titulo']}</title>")
    im = sustituir(im, "var CLAVE_JUEGO = 'faro';", f"var CLAVE_JUEGO = '{cfg['tema']}';")
    im = sustituir(im, "  .texto.chico{","  .texto.emoji{font-size:4.4mm;line-height:1.35;letter-spacing:.12em}\n  .texto.chico{")
    im = sustituir(im, "var clase = (c.textoCarta.length <= 3 ? ' chico' : ' largo') + (c.textoEspejo ? ' espejo' : '');",
                   "var clase = (c.textoCarta.length <= 3 ? ' chico' : ' largo') + (/\\p{Extended_Pictographic}/u.test(c.textoCarta.join('')) ? ' emoji' : '') + (c.textoEspejo ? ' espejo' : '');")
    im = sustituir(im, """      document.getElementById('resumen').textContent = faltan.length
        ? 'Faltan ilustraciones: ' + faltan.join(', ')
        : 'Todas las ilustraciones están listas.';""",
                   """      fetch('img/pendientes.json?v=' + Date.now(), {cache: 'no-store'}).then(function(r){ return r.ok ? r.json() : []; }).catch(function(){ return []; }).then(function(pend){
        var r = document.getElementById('resumen');
        if (faltan.length) r.textContent = 'Faltan ilustraciones: ' + faltan.join(', ');
        else if (pend.length) r.textContent = 'Ilustraciones de relleno (aún sin hacer): ' + pend.join(', ');
        else r.textContent = 'Todas las ilustraciones están listas.';
      });""")
    json.dump(sorted((k for k in datos.J if not os.path.exists(f"{base}/arte/{k}.png")), key=lambda k: (k != "P", int(k) if k != "P" else 0)), open(f"{base}/img/pendientes.json", "w", encoding="utf-8"))
    escribir(f"{base}/imprimir.html", im)

    json.dump(datos.SPEC, open(os.path.join(TMP, f"spec_{nombre.lower()}.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    subprocess.run([sys.executable, os.path.join(TMP, "sincronizar_cartas.py")], check=True)
    print(nombre, "->", len(datos.J), "cartas")

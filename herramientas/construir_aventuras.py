"""Construye las carpetas de juego de juegos/aventuras-ca a partir de la plantilla del Faro. Ejecutar desde la raiz del repo."""
import json, os, shutil, subprocess, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
import datos_egipto as E
import datos_marte as M
import datos_florencia as F
import datos_dinosaurios as D

FARO = "juegos/el-faro"
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
        datos=E, tema="egipto", titulo="Egipto, 1274 a.C.: El Ojo de Horus", emoji="🏺",
        grad="#4a3512,#150f05", acento="#e0b04a", acento2="#f2d27a", bg1="#120d05", bg2="#2a1d0a",
        sinopsis="Cristina y Alberto estrenan su Cronoportal y aterrizan en una cámara secreta bajo un templo de Tebas, en el año 1274 a.C. Con el aparato sin energía y solo una hora antes de que lleguen los sacerdotes, tienen que encontrar el Ojo de Horus.",
        minigames={"15": "15-papiro.js", "23": "23-muro.js", "47": "47-balanza.js", "71": "71-anillos.js", "95": "95-cristales.js", "37": "37-tablilla.js", "34": "34-sarcofago.js"},
        pal=("#7a5a1e", "#2a1d0a")),
    "Marte": dict(
        datos=M, tema="marte", titulo="Marte, 2157: Cúpula Aurora", emoji="🚀",
        grad="#5a2a14,#12060a", acento="#ff8a50", acento2="#ffb085", bg1="#12070a", bg2="#2a120c",
        sinopsis="Segundo salto del Cronoportal: Marte, año 2157. La cúpula Aurora está a oscuras por una tormenta de polvo y el soporte vital se apaga. Cristina y Alberto tienen una hora para encontrar el núcleo de fusión y volver a casa.",
        minigames={"21": "21-terminal.js", "52": "52-tuberias.js", "66": "66-esclusa.js", "88": "88-calibrador.js", "35": "35-diario.js", "48": "48-rover.js", "62": "62-energia.js"},
        pal=("#8a3a1a", "#1c0c10")),
    "Florencia": dict(
        datos=F, tema="florencia", titulo="Florencia, 1503: El Taller de Leonardo", emoji="🪞",
        grad="#5a3a1a,#140c06", acento="#d9a441", acento2="#f0c773", bg1="#120c07", bg2="#2a1c0e",
        sinopsis="Tercer salto del Cronoportal: Florencia, año 1503. Cristina y Alberto aterrizan de noche en el taller de Leonardo da Vinci, sin energía y con una hora hasta el amanecer. Solo la luz del alba, concentrada por la lente del maestro, puede recargar el aparato.",
        minigames={"24": "24-cofre.js", "32": "32-disco.js", "38": "38-engranajes.js", "54": "54-cuadrado.js", "58": "58-cisterna.js", "66": "66-ornitoptero.js", "92": "92-espejos.js"},
        pal=("#6a4a22", "#1a1008")),
    "Dinosaurios": dict(
        datos=D, tema="dinosaurios", titulo="Cretácico, hace 66 millones de años: El Valle de los Gigantes", emoji="🦖", minutos=90,
        grad="#2f5a22,#07120a", acento="#b5e35b", acento2="#d9f59a", bg1="#07120a", bg2="#12281a",
        sinopsis="Cuarto salto del Cronoportal: el Cretácico, hace sesenta y seis millones de años. Cristina y Alberto aterrizan en un valle de dinosaurios, pero el núcleo de energía del aparato sale rodando y en el cielo brilla un asteroide. Tienen hora y media para recuperarlo antes de que el cielo se incendie.",
        minigames={"14": "14-huellas.js", "20": "20-excavacion.js", "42": "42-diario.js", "40": "40-balsa.js", "46": "46-adn.js",
                   "51": "51-estratos.js", "64": "64-cristales.js", "69": "69-nidos.js", "72": "72-geiser.js", "84": "84-esqueleto.js"},
        pal=("#2f5a22", "#0a160c")),
}

SOLO = [a.lower() for a in sys.argv[1:] if not a.startswith("--")]

index_faro = leer(f"{FARO}/index.html")
pc_faro = leer(f"{FARO}/pc.html")
imprimir_faro = leer(f"{FARO}/imprimir.html")
prompts_tpl = leer(os.path.join(TMP, "prompts_plantilla.html"))

ORDEN_CAMPOS = ["titulo", "tipo", "coge", "descarta", "combina", "descripcion", "pistas", "textoCarta", "textoEspejo", "arte"]


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
    if nombre != "Egipto":
        shutil.copy("juegos/aventuras-ca/egipto/minijuegos/lector.js", f"{base}/minijuegos/lector.js")
    css = leer(f"{FARO}/style.css")
    css += f"\n/* Aventuras C&A: {nombre} */\n:root{{ --accent:{cfg['acento']}; --accent-2:{cfg['acento2']}; --bg1:{cfg['bg1']}; --bg2:{cfg['bg2']}; }}\n"
    escribir(f"{base}/style.css", css)
    escribir(f"{base}/video/LEEME.txt", "Pon aqui el video de introduccion como videoInicial.mp4 (MP4 H.264, vertical 9:16, idealmente menos de 25 MB).\n")

    # index.html
    ix = index_faro
    ix = sustituir(ix, '<html lang="es" data-tema="faro">', f'<html lang="es" data-tema="{cfg["tema"]}">')
    ix = sustituir(ix, "<title>Unlock C&amp;A - El Faro de Cabo Niebla</title>", f"<title>Aventuras C&amp;A - {cfg['titulo']}</title>")
    ix = sustituir(ix, '<h1 style="margin:0;font-size:20px">El Faro de Cabo Niebla</h1>', f'<h1 style="margin:0;font-size:20px">{cfg["titulo"]}</h1>')
    ix = sustituir(ix, "Tormenta, la gran lámpara apagada y un carguero a ciegas rumbo a las rocas. Inés y Marcos tienen una hora para encender el faro... y encontrar al abuelo Anselmo.", cfg["sinopsis"])
    ix = sustituir(ix, "<h2>El Faro de Cabo Niebla</h2>", f'<h2>{cfg["titulo"]}</h2>')
    ix = sustituir(ix, "const DEFAULT_SECONDS = 60 * 60;", f"const DEFAULT_SECONDS = {cfg.get('minutos', 60)} * 60;")
    ix = sustituir(ix, "← Volver al menú", "← Volver a Aventuras C&amp;A")
    ix = sustituir(ix, "window.location.href = '../../index.html';", "window.location.href = '../index.html';")
    mapa = ",\n".join(f"      '{k}': './minijuegos/{v}'" for k, v in cfg["minigames"].items())
    viejo_mapa = re.search(r"    const MINIGAMES = \{.*?\n    \};", ix, re.S).group(0)
    ix = ix.replace(viejo_mapa, "    const MINIGAMES = {\n" + mapa + "\n    };")
    escribir(f"{base}/index.html", ix)

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
    im = sustituir(im, "  .texto.chico{", "  .texto.emoji{font-size:4.4mm;line-height:1.35;letter-spacing:.12em}\n  .texto.chico{")
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

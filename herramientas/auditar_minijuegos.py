"""Auditoría estática de los minijuegos y de sus pistas contra las reglas de diseño (GUIA-DE-PUZLES.md §7.1).

Uso (desde la raíz del repo):
    python herramientas/auditar_minijuegos.py                  # todos los juegos
    python herramientas/auditar_minijuegos.py juegos/aventuras-ca/dinosaurios

Comprueba, por minijuego (.js):
  - exporta startMinigame y se abre con openGame / abrirLector;
  - tiene mensaje de ACIERTO (say(..., 'ok')) con «Coged la carta N» o «Descartad…» y, si hay botón de comprobar, de FALLO (say(..., 'bad'));
  - no usa emojis ni símbolos pictográficos como dibujo (reglas de aspecto: imágenes reales);
  - no depende de colores sin otra señal (aviso si define colores pero no hay ni texto ni aria-label);
  - los botones llevan aria-label o texto; las imágenes tienen alt;
  - sin tamaños fijos de más de 400 px de ancho (móvil).
Y, por carta de app (verde) en cartas.json:
  - al menos 3 pistas progresivas y la última da la solución (no vacía);
  - su descripción nombra la carta que se coge al acertar.
Sale con código 1 si hay errores graves (los avisos no cuentan).
"""
import glob
import json
import os
import re
import sys

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿️]")
PERMITIDOS = set("✓✔✕✖✦✧☥▲▼◀▶●○◆◇←→↑↓↘↙⌫−+×·–—…«»¡¿€")


def emojis(texto):
    # se ignoran símbolos tipográficos de uso normal (flechas, viñetas, ✓)
    return [c for c in EMOJI.findall(texto) if c not in PERMITIDOS]


def auditar_js(ruta):
    t = open(ruta, encoding="utf-8").read()
    nombre = os.path.basename(ruta)
    graves, avisos = [], []
    lector = "abrirLector" in t or "say(" not in t      # sin mensajes = solo lectura (cuaderno, diario)
    if "export function startMinigame" not in t:
        graves.append("no exporta startMinigame")
    if not lector and "openGame" not in t:
        graves.append("no usa openGame")
    if not lector:
        if not re.search(r"say\([^;]*'ok'\)", t):
            graves.append("no tiene mensaje de acierto (say(..., 'ok'))")
        elif not re.search(r"say\([^;]*(Coged la carta|Descartad)[^;]*'ok'\)", t):
            avisos.append("el mensaje de acierto no dice «Coged la carta N» ni «Descartad…»")
        if not re.search(r"say\([^;]*'bad'\)", t):
            avisos.append("sin mensaje de fallo (say(..., 'bad')): vale si el fallo es evidente al jugar (deslizante, tuberías); si hay botón de comprobar, añádelo")
    e = emojis(t)
    if e:
        graves.append("usa emojis/símbolos pictográficos: " + "".join(sorted(set(e))))
    if "createElementNS" in t and "<image" not in t and "'image'" not in t:
        avisos.append("dibuja con SVG plano (¿falta imagen real?)")
    for m in re.finditer(r"<img(?![^>]*\balt=)[^>]*>", t):
        avisos.append("imagen sin atributo alt: " + m.group(0)[:60])
        break
    for m in re.finditer(r"width:\s*(\d{3,4})px", t):
        if int(m.group(1)) > 400 and "max-width" not in t[max(0, m.start() - 12):m.start()]:
            avisos.append(f"ancho fijo de {m.group(1)} px (¿cabe en el móvil?)")
            break
    if re.search(r"#[0-9a-fA-F]{6}", t) and "aria-label" not in t and not lector:
        avisos.append("define colores pero no hay aria-label ni texto alternativo")
    return nombre, graves, avisos


def auditar_cartas(carpeta):
    graves, avisos = [], []
    ruta = os.path.join(carpeta, "cartas.json")
    if not os.path.exists(ruta):
        return graves, avisos
    datos = json.load(open(ruta, encoding="utf-8"))
    for k, c in datos.items():
        if k == "_meta" or c.get("tipo") != "verde":
            continue
        p = c.get("pistas", [])
        if len(p) < 2:
            graves.append(f"carta {k}: tiene menos de 2 pistas")
        elif len(p) < 3:
            avisos.append(f"carta {k}: solo {len(p)} pistas (mejor 3 niveles: dónde mirar / método / solución)")
        if p and not p[-1].strip():
            graves.append(f"carta {k}: la última pista está vacía")
        desc = " ".join(c.get("descripcion", []))
        if not re.search(r"[Cc]oged la carta|[Cc]oged las cartas|termina|se abre|Descartad", desc) and k not in ("42", "15", "35"):
            avisos.append(f"carta {k}: la descripción no dice qué se coge al acertar")
    return graves, avisos


def main():
    carpetas = sys.argv[1:] or ["juegos/el-faro"] + sorted(os.path.dirname(p).replace("\\", "/") for p in glob.glob("juegos/aventuras-ca/*/cartas.json"))
    total_graves = 0
    for carpeta in carpetas:
        print(f"== {carpeta}")
        for ruta in sorted(glob.glob(os.path.join(carpeta, "minijuegos", "*.js"))):
            if os.path.basename(ruta) in ("ui.js", "lector.js", "libro.js", "comun.js"):  # módulos de apoyo, no minijuegos
                continue
            nombre, graves, avisos = auditar_js(ruta)
            marca = "ERROR" if graves else ("aviso" if avisos else "ok")
            print(f"  {marca:5} {nombre}")
            for g in graves:
                print("        ✗", g)
            for a in avisos:
                print("        ·", a)
            total_graves += len(graves)
        g, a = auditar_cartas(carpeta)
        for x in g:
            print("  ✗", x)
        for x in a:
            print("  ·", x)
        total_graves += len(g)
    print("RESULTADO:", "OK" if not total_graves else f"{total_graves} errores graves")
    sys.exit(1 if total_graves else 0)


if __name__ == "__main__":
    main()

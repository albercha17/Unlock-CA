"""Láminas de «El primer salto» (nivel de prueba): la pizarra de engranajes (16), la nota del plano (18), el plano del Umbral en dos mitades (19 y 21) y la nota del
orden (86), dibujadas por código con los sprites de ChatGPT (herramientas/sprites_chatgpt.py + pedidos_sprites/cronoportal.py).
Además copia en cada minijuego (entre /*DATOS*/ y /*FIN*/) los datos de su instancia.
Uso (desde la raíz del repo):  python herramientas/cronoportal.py [carpeta_juego]"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oeste import Hoja  # noqa: E402
from mosaicos import cortar  # noqa: E402

W, H = 630, 882
PAPEL = (236, 242, 248)
TINTA = (20, 40, 70)
ORO = (222, 170, 60)
AZUL = (40, 100, 170)


def _inst():
    return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_cronoportal.json"), encoding="utf-8"))


def ruido(im, semilla, fuerza=2.5):
    a = np.asarray(im).astype(np.int16)
    rng = np.random.default_rng(semilla)
    return Image.fromarray(np.clip(a + rng.normal(0, fuerza, a.shape[:2])[:, :, None], 0, 255).astype(np.uint8))


def papel(titulo, sub=None, w=W, h=H, fondo=PAPEL):
    p = Hoja(w, h, fondo)
    p.rect(16, 16, w - 16, h - 16, None, TINTA, 4)
    p.texto((w / 2 + 30, 60), titulo, "cartel", 34, TINTA)
    if sub:
        p.texto((w / 2 + 30, 98), sub, "texto2", 22, TINTA)
    return p


def sprite(carpeta, nombre):
    ruta = os.path.join(carpeta, "img", "ui", nombre + ".png")
    return Image.open(ruta).convert("RGBA") if os.path.exists(ruta) else None


def pegar(h, spr, cx, cy, alto):
    S = 2
    hp = max(2, round(alto * S))
    wp = max(2, round(spr.width * hp / spr.height))
    r = spr.resize((wp, hp), Image.LANCZOS)
    h.im.paste(r.convert("RGB"), (int(cx * S - wp / 2), int(cy * S - hp / 2)), r.getchannel("A"))


# ------------------------------------------------------------------ 16: la pizarra de Alberto
def pizarra(inst, carpeta):
    ce = inst["cerradura"]
    h = papel("LA PIZARRA DE ALBERTO", "Todo lo que sobró al montar el portal", fondo=(48, 66, 58))
    h.rect(16, 16, W - 16, H - 16, None, (210, 180, 120), 6)
    h.texto((W / 2 + 30, 60), "LA PIZARRA DE ALBERTO", "cartel", 34, (250, 246, 220))
    h.texto((W / 2 + 30, 98), "Todo lo que sobró al montar el portal", "texto2", 22, (230, 230, 210))
    h.rect(50, 150, W - 50, 700, (36, 52, 46), (180, 140, 80), 8)
    ancho_c, alto_c = (W - 140) / 5, 250
    for g in ce["gears"]:
        spr = sprite(carpeta, "eng-" + g["col"])
        cx = 70 + ancho_c * (g["x"] + 0.5) + g["dx"]
        cy = 190 + alto_c * (g["y"] + 0.5) + g["dy"]
        if spr is not None:
            pegar(h, spr, cx, cy, 98)
        else:
            col = {"rojo": (210, 50, 50), "azul": (50, 100, 200), "amarillo": (240, 200, 40)}[g["col"]]
            h.disco(cx, cy, 44, col, (20, 20, 20), 3)
            h.disco(cx, cy, 12, (220, 200, 140))
    h.texto((W / 2, 760), "Rojo · Azul · Amarillo", "texto", 26, (250, 246, 220))
    h.texto((W / 2, 806), "El candado de la vitrina pide tres cifras:", "texto2", 21, (230, 230, 210))
    h.texto((W / 2, 838), "en ese orden.", "texto2", 21, (230, 230, 210))
    return ruido(h.final(), 16)


# ------------------------------------------------------------------ 18: la nota del plano
def nota_plano(inst):
    h = papel("LA NOTA DE CRISTINA", "Pegada en el plano", fondo=(250, 244, 222))
    L = ["Entras por el borde de abajo.", "El camino avanza casilla a casilla", "sin saltarse ninguna ni pisar dos veces",
         "la misma, y sale a la sexta.", "", "Al abrirse, el portal solo deja pasar", "por los cuatro símbolos de en medio,",
         "en el orden en que los pisas.", "", "El primero y el último no cuentan."]
    for k, t in enumerate(L):
        h.texto((W / 2, 190 + k * 46), t, "texto2", 23, TINTA)
    return h.final()


# ------------------------------------------------------------------ 19 y 21: el plano del Umbral (dos mitades)
def plano(inst, carpeta):
    ma = inst["mapa"]
    h = Hoja(W, H * 2, (210, 224, 240))
    h.rect(16, 16, W - 16, H * 2 - 16, None, TINTA, 4)
    h.texto((W / 2 + 30, 60), "EL PLANO DEL UMBRAL", "cartel", 34, TINTA)
    h.texto((W / 2 + 30, 98), "Dibujado por Cristina en dos hojas", "texto2", 22, TINTA)
    lado = 128
    x0 = (W - ma["cols"] * lado) / 2
    y_sup = H - 3 * lado - 90
    y_inf = H + 80
    def cy(f):
        return y_sup + f * lado if f < 3 else y_inf + (f - 3) * lado
    for f in range(ma["filas"]):
        for c in range(ma["cols"]):
            x, y = x0 + c * lado, cy(f)
            h.rect(x + 4, y + 4, x + lado - 4, y + lado - 4, (236, 244, 252), (120, 150, 190), 2)
            spr = sprite(carpeta, "sim-" + ma["celdas"][f][c])
            if spr is not None:
                pegar(h, spr, x + lado / 2, y + lado / 2, lado - 30)
            else:
                h.texto((x + lado / 2, y + lado / 2), ma["celdas"][f][c][:3], "cartel", 28, TINTA)
    # camino con flechas
    pts = [(x0 + c * lado + lado / 2, cy(f) + lado / 2) for c, f in ma["camino"]]
    for a, b in zip(pts, pts[1:]):
        if abs(a[1] - b[1]) > lado * 2:           # cruza el corte entre hojas: no se dibuja el tramo largo, se dibujan puntas en los bordes
            continue
        h.linea([a, b], (230, 60, 60), 7)
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        h.poli([(m[0] + 16 * math.cos(ang), m[1] + 16 * math.sin(ang)), (m[0] + 16 * math.cos(ang + 2.5), m[1] + 16 * math.sin(ang + 2.5)),
                (m[0] + 16 * math.cos(ang - 2.5), m[1] + 16 * math.sin(ang - 2.5))], (230, 60, 60))
    h.disco(pts[0][0], pts[0][1], 12, (60, 170, 80), TINTA, 3)
    h.texto((pts[0][0], pts[0][1] + 52), "ENTRADA", "texto", 20, (30, 110, 50))
    h.disco(pts[-1][0], pts[-1][1], 12, (250, 210, 60), TINTA, 3)
    h.texto((pts[-1][0], pts[-1][1] - 52), "SALIDA", "texto", 20, (150, 40, 30))
    # tramo que cruza el corte entre hojas: una flecha de salida en una hoja y otra de entrada en la otra
    for a, b in zip(pts, pts[1:]):
        if abs(a[1] - b[1]) > lado * 2:
            arriba = a[1] > b[1]                 # el camino sube (de la hoja de abajo a la de arriba)
            for (p, sube) in ((a, arriba), (b, not arriba)):
                q = (p[0], p[1] - 80 if sube else p[1] + 80)
                h.linea([p, q], (230, 60, 60), 7)
                ang = -math.pi / 2 if sube else math.pi / 2
                h.poli([(q[0] + 18 * math.cos(ang), q[1] + 18 * math.sin(ang)), (q[0] + 16 * math.cos(ang + 2.5), q[1] + 16 * math.sin(ang + 2.5)),
                        (q[0] + 16 * math.cos(ang - 2.5), q[1] + 16 * math.sin(ang - 2.5))], (230, 60, 60)) if p is a else None
    return h.final()


# ------------------------------------------------------------------ 86: el orden
def nota_orden(inst):
    h = papel("EL ORDEN DEL PANEL", "Escrito por Alberto en el portal", fondo=(250, 244, 222))
    L = ["El panel de vuelta pide dos cifras.", "", "Primero, la que dejó el camino:", "el plano, el que se abre con símbolos.",
         "", "Después, la que dejó el candado:", "el de la vitrina, el de los engranajes.", "", "Teclea las dos, una tras otra,", "y el portal te llevará a casa."]
    for k, t in enumerate(L):
        h.texto((W / 2, 190 + k * 46), t, "texto2", 23, TINTA)
    return h.final()


DATOS_MINIJUEGOS = {
    "14-cerradura.js": lambda i: {"codigo": i["cerradura"]["codigo"], "cifra": i["cerradura"]["cifra"]},
    "20-mapa.js": lambda i: {"simbolos": ["sol", "luna", "estrella", "llave", "reloj", "flor"], "solucion": i["mapa"]["solucion"], "cifra": i["mapa"]["cifra"]},
    "85-panel.js": lambda i: {"codigo": i["meta"]["codigo"]},
}


def inyectar_datos(carpeta, inst):
    for nombre, f in DATOS_MINIJUEGOS.items():
        ruta = os.path.join(carpeta, "minijuegos", nombre)
        if not os.path.exists(ruta):
            continue
        js = open(ruta, encoding="utf-8").read()
        if "/*DATOS*/" not in js:
            continue
        a, b = js.index("/*DATOS*/") + len("/*DATOS*/"), js.index("/*FIN*/")
        js = js[:a] + json.dumps(f(inst), ensure_ascii=False, separators=(", ", ": ")) + js[b:]
        open(ruta, "w", encoding="utf-8", newline="\n").write(js)


def main(carpeta="juegos/aventuras-ca/cronoportal"):
    inst = _inst()
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    for k, im in {"16": pizarra(inst, carpeta), "18": ruido(nota_plano(inst), 18), "86": ruido(nota_orden(inst), 86)}.items():
        im.save(os.path.join(arte, f"{k}.png"))
    im = plano(inst, carpeta)
    im.save(os.path.join(arte, "mosaico-plano.png"))
    for pieza, k in zip(cortar(im, 2, 1), ("19", "21")):
        pieza.save(os.path.join(arte, f"{k}.png"))
    inyectar_datos(carpeta, inst)
    print("láminas escritas en", arte)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

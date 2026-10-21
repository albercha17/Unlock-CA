"""Láminas de «Egipto, 1274 a.C.: El Ojo de Horus» (versión de 60 cartas, 21 oct 2026). Todas las pistas son dibujos o acertijos:
ninguna carta escribe la respuesta ni explica cómo se resuelve su puzle. Datos de herramientas/instancias_egipto.py.

  16 el montón del granero · 18 el acertijo de la pirámide · 19 y 21 la pirámide del escriba (dos mitades)
  41 y 43 los registros de crecidas del Nilo · 45 la vara de medir · 42 y 49 el friso de animales (dos mitades) · 53 el guardián del friso
  54 las seis partes del ojo · 55 y 59 los pagos de la mañana y de la tarde · 37 la suma de los signos · 39 y 33 las pistas del escriba
  26 el papiro de la sacerdotisa · 61 y 63 el plano de las cámaras (dos mitades) · 70 el mapa de los campos · 71 la nota del visir
  66 y 67 el friso de azulejos (dos mitades) · 75 y 79 el campo por repartir (dos mitades) · 86 y 87 los acertijos de los sellos
Uso (desde la raíz del repo):  python herramientas/egipto.py [carpeta_juego]
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oeste import Hoja  # noqa: E402
from mosaicos import cortar  # noqa: E402
import instancias_egipto as I  # noqa: E402

W, H = 630, 882
PAPEL = (240, 224, 182)
ARENA = (226, 200, 150)
TINTA = (70, 44, 20)
OCRE = (200, 140, 60)
TURQ = (50, 150, 150)
LAPIS = (40, 70, 150)
ORO = (220, 170, 50)
TERRA = (190, 90, 55)
BLANCO = (252, 246, 232)
ROJO = (176, 50, 40)
COL3 = {"terracota": TERRA, "turquesa": TURQ, "oro": ORO}
COLCAM = [OCRE, TURQ, LAPIS]


def ruido(im, s, f=2.5):
    a = np.asarray(im).astype(np.int16)
    a = a + np.random.default_rng(s).normal(0, f, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def pagina(titulo, sub=None, fondo=PAPEL, borde=OCRE, w=W, h=H):
    p = Hoja(w, h, fondo)
    p.rect(16, 16, w - 16, h - 16, None, borde, 6)
    p.rect(28, 28, w - 28, h - 28, None, borde, 2)
    p.texto((w / 2 + 26, 70), titulo, "cartel", 32, TINTA)
    if sub:
        p.texto((w / 2 + 26, 108), sub, "texto2", 21, TINTA)
    return p


def versos(p, lineas, y0=220, paso=56, tam=27, x=W / 2):
    for k, v in enumerate(lineas):
        p.texto((x, y0 + k * paso), v, "texto2", tam, TINTA)


def figura(p, nombre, cx, cy, tam, color=TINTA, espejo=False, fondo=PAPEL):
    """Dibuja una figura de instancias_egipto.FIGURAS en una caja de `tam` px centrada en (cx, cy)."""
    s = tam / 100
    pt = lambda q: (cx + ((50 - q[0]) if espejo else (q[0] - 50)) * s, cy + (q[1] - 50) * s)
    for e in I.FIGURAS[nombre]:
        col = fondo if e.get("f") == "fondo" else color
        if e["t"] == "p":
            p.poli([pt(q) for q in e["p"]], col)
        elif e["t"] == "l":
            p.linea([pt(q) for q in e["p"]], col, e["w"] * s)
            for q in (e["p"][0], e["p"][-1]):
                x, y = pt(q)
                p.disco(x, y, e["w"] * s / 2, col)
        else:
            x, y = pt(e["c"])
            if "w" in e:
                p.disco(x, y, e["r"] * s, None, col, e["w"] * s)
            else:
                p.disco(x, y, e["r"] * s, col)


def numero_egipcio(p, n, x, y, tam=30, color=TINTA):
    """Número egipcio: arcos (decenas) y trazos verticales (unidades)."""
    d, u = divmod(n, 10)
    for k in range(d):
        px = x + k * tam * 0.9
        p.linea([(px, y + tam * 0.5), (px, y - tam * 0.1), (px + tam * 0.5, y - tam * 0.4), (px + tam * 0.8, y - tam * 0.1), (px + tam * 0.8, y + tam * 0.5)], color, 5)
    for k in range(u):
        px = x + d * tam * 0.9 + 12 + (k % 5) * tam * 0.4
        py = y + (k // 5) * tam * 1.1
        p.linea([(px, py - tam * 0.4), (px, py + tam * 0.5)], color, 5)


def saco(p, x, y, r=34, color=OCRE):
    p.elip(x - r, y - r * 0.8, x + r, y + r, color, TINTA, 3)
    p.poli([(x - r * 0.4, y - r * 0.75), (x + r * 0.4, y - r * 0.75), (x + r * 0.28, y - r * 1.15), (x - r * 0.28, y - r * 1.15)], color, TINTA, 3)


# ------------------------------------------------------------------ 16: el montón del granero
def monton():
    p = pagina("EL GRANERO CERRADO", "grabado en la puerta", PAPEL, OCRE)
    filas = [("un montón", "", 1), ("su mitad", "1/2", 0.5), ("su cuarto", "1/4", 0.25)]
    for k, (txt, frac, esc) in enumerate(filas):
        y = 250 + k * 150
        r = 52 * (0.6 + 0.4 * esc)
        p.poli([(150 - 70 * (0.6 + 0.4 * esc), y + 40), (150, y - 60 * (0.6 + 0.4 * esc)), (150 + 70 * (0.6 + 0.4 * esc), y + 40)], OCRE, TINTA, 3)
        for j in range(3):
            saco(p, 120 + j * 30, y + 14, 17, ARENA)
        p.texto((330, y), txt, "texto", 26, TINTA, "lm")
        if frac:
            p.texto((500, y), frac, "cartel", 34, TERRA)
        if k < 2:
            p.texto((60, y + 76), "+", "cartel", 34, TINTA)
    p.linea([(70, 690), (W - 70, 690)], TINTA, 5)
    p.texto((70, 745), "=", "cartel", 40, TINTA, "lm")
    numero_egipcio(p, 28, 150, 740, 44)
    p.texto((460, 745), "sacos", "texto", 26, TINTA, "lm")
    return p.final()


# ------------------------------------------------------------------ 18, 19/21: la pirámide
def acertijo_piramide():
    p = pagina("EL ACERTIJO DEL CANTERO", "cincelado en el muro", PAPEL, OCRE)
    versos(p, ["«Piedra sobre piedra,", "cada una carga con las dos", "que tiene debajo.", "", "Lo que pesa la de arriba",
               "es lo que pesan juntas", "las dos que la sostienen.»"], 220, 58, 27)
    return p.final()


def piramide():
    d = I.PIRAMIDE
    n = d["n"]
    p = Hoja(W, H * 2, PAPEL)
    p.rect(16, 16, W - 16, H * 2 - 16, None, OCRE, 6)
    p.rect(28, 28, W - 28, H * 2 - 28, None, OCRE, 2)
    p.texto((W / 2 + 26, 70), "LA PIRÁMIDE DEL ESCRIBA", "cartel", 32, TINTA)
    p.texto((W / 2 + 26, 108), "las piedras que ya tienen su peso", "texto2", 20, TINTA)
    ancho, alto = 112, 168
    corte = H
    dados = {tuple(x) for x in d["dados"]}
    for f in range(n - 1, -1, -1):
        fila = n - 1 - f                          # 0 = cima
        y0 = corte - 3 * alto + fila * alto
        for i in range(n - f):
            x0 = W / 2 - (n - f) * ancho / 2 + i * ancho
            hay = (f, i) in dados
            p.rect(x0 + 3, y0 + 4, x0 + ancho - 3, y0 + alto - 4, (232, 206, 150) if hay else (212, 184, 130), TINTA, 3)
            if hay:
                p.texto((x0 + ancho / 2, y0 + alto / 2), str(d["filas"][f][i]), "cartel", 38, TINTA)
    return p.final()


# ------------------------------------------------------------------ 41/43/45: el nilómetro
def columna_crecida(p, x, base, palmos, año):
    top = base - palmos * 11
    p.rect(x - 24, top - 12, x + 24, base, (200, 220, 230), TINTA, 3)
    p.rect(x - 24, top, x + 24, base, (120, 170, 200))
    for k in range(0, palmos + 4):
        y = base - k * 11
        largo = 22 if k % 7 == 0 else 10
        p.linea([(x + 24, y), (x + 24 + largo, y)], TINTA, 3 if k % 7 == 0 else 2)
    p.linea([(x - 30, top), (x + 30, top)], ROJO, 5)
    for k in range(año):
        p.disco(x - 18 + k * 12, base + 36, 4, TINTA)


def registro(años, titulo, vacio=False):
    p = pagina(titulo, "marcas del Nilo, año tras año", PAPEL, TURQ)
    xs = [150 + k * 170 for k in range(len(años) + (1 if vacio else 0))]
    base = 780
    for x, (n, alt) in zip(xs, años):
        columna_crecida(p, x, base, alt, n)
    if vacio:
        x = xs[-1]
        p.rect(x - 24, base - 120 * 4.5, x + 24, base, None, TINTA, 3)
        p.texto((x, base - 300), "?", "cartel", 60, TERRA)
        for k in range(6):
            p.disco(x - 30 + k * 12, base + 36, 4, TINTA)
    return p.final()


def registro1():
    a = I.NILOMETRO["alturas_palmos"]
    return registro([(k + 1, a[k]) for k in range(3)], "REGISTRO DE CRECIDAS (I)")


def registro2():
    a = I.NILOMETRO["alturas_palmos"]
    return registro([(k + 1, a[k]) for k in (3, 4)], "REGISTRO DE CRECIDAS (II)", vacio=True)


def vara():
    p = pagina("LA VARA DEL AGRIMENSOR", "un codo, partido en palmos", PAPEL, TURQ)
    x0, x1, y = 70, W - 70, 380
    p.rect(x0, y - 36, x1, y + 36, ORO, TINTA, 4)
    paso = (x1 - x0) / 7
    for k in range(8):
        p.linea([(x0 + k * paso, y - 36), (x0 + k * paso, y + 36)], TINTA, 3)
    p.texto((W / 2, y + 90), "un codo", "texto", 28, TINTA)
    versos(p, ["«Lo que mide la vara entera", "es un codo.", "Lo que mide cada partida", "es un palmo.»"], 540, 52, 25)
    return p.final()


# ------------------------------------------------------------------ 42/49: el friso, 53: el guardián
def friso_animales():
    d = I.CONTAR
    p = Hoja(W * 2, H, ARENA)
    p.rect(16, 16, W * 2 - 16, H - 16, None, OCRE, 6)
    p.rect(28, 28, W * 2 - 28, H - 28, None, OCRE, 2)
    p.texto((W, 70), "EL FRISO DE LOS ANIMALES", "cartel", 34, TINTA)
    x0, y0 = 90, 130
    dx, dy = (W * 2 - 180) / d["cols"], (H - 190) / d["filas"]
    for e in d["puestos"]:
        cx, cy = x0 + e["x"] * dx + dx / 2, y0 + e["y"] * dy + dy / 2
        col = (96, 70, 40) if e["animal"] in d["animales"] else (140, 110, 70)
        figura(p, e["animal"], cx, cy, 70 if e["animal"] in d["animales"] else 46, col, espejo=(e["mira"] == "i"), fondo=ARENA)
    return p.final()


def guardian():
    p = pagina("EL GUARDIÁN DEL FRISO", "su cerradura, labrada en piedra", PAPEL, OCRE)
    p.disco(W / 2, 210, 56, ORO, TINTA, 4)
    for k in range(12):
        a = k * math.pi / 6
        p.linea([(W / 2 + math.cos(a) * 66, 210 + math.sin(a) * 66), (W / 2 + math.cos(a) * 92, 210 + math.sin(a) * 92)], ORO, 6)
    p.texto((W / 2, 340), "Solo cuentan los que miran", "texto2", 24, TINTA)
    p.texto((W / 2, 376), "hacia el sol naciente.", "texto2", 24, TINTA)
    for k, a in enumerate(I.ANIMALES):
        x = 130 + k * 123
        p.rect(x - 52, 470, x + 52, 600, BLANCO, TINTA, 3)
        figura(p, a, x, 530, 76, TINTA)
        p.rect(x - 32, 640, x + 32, 720, None, TINTA, 3)
    p.texto((W / 2, 780), "contados de izquierda a derecha", "texto2", 18, TINTA)
    return p.final()


# ------------------------------------------------------------------ 54/55/59: el ojo y los pagos
def partes_ojo():
    p = pagina("LAS PARTES DEL OJO", "grabadas en el amuleto", PAPEL, TURQ)
    d = I.HEQAT
    for k, (forma, (a, b)) in enumerate(zip(d["formas"], d["partes"])):
        y = 200 + k * 108
        pieza_forma(p, forma, 160, y, 34)
        p.texto((340, y), f"{a}/{b}", "cartel", 40, TINTA, "lm")
    return p.final()


def pieza_forma(p, forma, cx, cy, r, color=TURQ):
    if forma == "circulo":
        p.disco(cx, cy, r, color, TINTA, 3)
    elif forma == "cuadrado":
        p.rect(cx - r, cy - r, cx + r, cy + r, color, TINTA, 3)
    elif forma == "triangulo":
        p.poli([(cx, cy - r), (cx + r, cy + r * 0.8), (cx - r, cy + r * 0.8)], color, TINTA, 3)
    elif forma == "rombo":
        p.poli([(cx, cy - r * 1.15), (cx + r, cy), (cx, cy + r * 1.15), (cx - r, cy)], color, TINTA, 3)
    elif forma == "estrella":
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            rr = r * (1.15 if k % 2 == 0 else 0.5)
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        p.poli(pts, color, TINTA, 3)
    else:
        p.poli([(cx + math.cos(k * math.pi / 3) * r * 1.1, cy + math.sin(k * math.pi / 3) * r * 1.1) for k in range(6)], color, TINTA, 3)


def pagos(titulo, sub, lista):
    p = pagina(titulo, sub, PAPEL, OCRE)
    for k, (a, b) in enumerate(lista):
        y = 230 + k * 170
        saco(p, 200, y, 52, ARENA)
        p.texto((380, y + 10), f"{a}/{b}", "cartel", 50, TERRA, "lm")
    p.texto((W / 2, 780), "de heqat de cebada", "texto2", 22, TINTA)
    return p.final()


# ------------------------------------------------------------------ 37/39/33: el criptograma
def suma_signos():
    d = I.CRIPTO
    p = pagina("LA SUMA DEL ESCRIBA", "los signos esconden cifras", PAPEL, LAPIS)
    sg = d["signos"]
    sumandos = d["suma"]
    x0, paso = 110, 90
    for fila, (pat, y) in enumerate(zip(sumandos, (300, 430, 600))):
        ancho = len(pat)
        for k, ch in enumerate(pat):
            figura(p, sg[ch], x0 + (4 - ancho + k) * paso + 90, y, 66, TINTA)
        if fila == 1:
            p.texto((60, y), "+", "cartel", 50, TINTA, "lm")
    p.linea([(60, 500), (W - 60, 500)], TINTA, 6)
    p.texto((W / 2, 780), "Cada signo, una cifra distinta.", "texto2", 21, TINTA)
    return p.final()


def pista_signos(titulo, texto_pista):
    d = I.CRIPTO
    p = pagina(titulo, "anotado al margen por el escriba", PAPEL, LAPIS)
    sg = d["signos"]
    x, y = 160, 360
    if " > " in texto_pista:
        a, b = texto_pista.split(" > ")
        figura(p, sg[a], 170, 380, 100, TINTA)
        p.texto((W / 2, 380), "vale más que", "texto2", 24, TINTA)
        figura(p, sg[b], 460, 380, 100, TINTA)
    else:
        a, resto = texto_pista.split(" es ")
        figura(p, sg[a], 190, 380, 110, TINTA)
        p.texto((380, 380), "es " + resto, "texto", 34, TINTA, "lm")
    return p.final()


# ------------------------------------------------------------------ 26, 61/63: las cámaras
def papiro_camaras():
    p = pagina("EL PAPIRO DE LA SACERDOTISA", None, PAPEL, LAPIS)
    versos(p, ["«Tres pinturas hay en el templo:", "ocre, turquesa y lapislázuli.", "", "Si dos cámaras comparten puerta,",
               "no pueden llevar la misma.", "", "En el plano, las puertas son líneas", "y las cámaras ya pintadas, llenas.»"], 210, 54, 25)
    return p.final()


def plano_camaras():
    d = I.CAMARAS
    p = Hoja(W * 2, H, PAPEL)
    p.rect(16, 16, W * 2 - 16, H - 16, None, LAPIS, 6)
    p.rect(28, 28, W * 2 - 28, H - 28, None, LAPIS, 2)
    p.texto((W, 70), "EL PLANO DEL TEMPLO", "cartel", 34, TINTA)
    cols, filas = d["cols"], d["filas"]
    pos = lambda i: (180 + (i % cols) * 300, 260 + (i // cols) * 240)
    for a, b in d["aristas"]:
        p.linea([pos(a), pos(b)], TINTA, 6)
    for i in range(cols * filas):
        x, y = pos(i)
        col = COLCAM[d["fijos"][str(i)]] if str(i) in d["fijos"] else BLANCO
        p.disco(x, y, 58, col, TINTA, 5)
        p.texto((x, y), "ABCDEFGHIJKL"[i], "cartel", 40, BLANCO if str(i) in d["fijos"] else TINTA)
    return p.final()


# ------------------------------------------------------------------ 70/71: los canales
def mapa_canales():
    d = I.CANALES
    p = pagina("LOS CAMPOS DEL VALLE", "y lo que costaría un canal entre cada dos", PAPEL, TURQ)
    X = lambda v: 60 + v[0] / 100 * (W - 120)
    Y = lambda v: 170 + v[1] / 100 * 560
    for a, b, c in d["canales"]:
        pa, pb = d["campos"][a], d["campos"][b]
        p.linea([(X(pa), Y(pa)), (X(pb), Y(pb))], (110, 160, 190), 7)
    for a, b, c in d["canales"]:
        pa, pb = d["campos"][a], d["campos"][b]
        mx, my = (X(pa) + X(pb)) / 2, (Y(pa) + Y(pb)) / 2
        p.disco(mx, my, 20, BLANCO, TINTA, 2)
        p.texto((mx, my), str(c), "texto", 22, TINTA)
    for k, v in d["campos"].items():
        p.disco(X(v), Y(v), 36, ORO, TINTA, 4)
        p.texto((X(v), Y(v)), k, "cartel", 32, TINTA)
    p.texto((W / 2, 800), "costes en codos de zanja", "texto2", 19, TINTA)
    return p.final()


def nota_visir():
    p = pagina("LA NOTA DEL VISIR", None, PAPEL, TURQ)
    versos(p, ["«Que el agua llegue a todos los campos,", "pero no más zanjas de las precisas:", "cada codo cavado de más",
               "es un codo robado al faraón.", "", "Y que ningún campo quede", "sin camino de agua hasta los demás.»"], 210, 54, 25)
    return p.final()


# ------------------------------------------------------------------ 66/67: el friso de azulejos
def azulejo(p, cx, cy, t, fig, color, tam):
    p.rect(cx - t / 2, cy - t / 2, cx + t / 2, cy + t / 2, BLANCO, TINTA, 3)
    figura(p, I.FIG3[fig], cx, cy, t * (0.34 + 0.22 * tam), COL3[I.COL3[color]], fondo=BLANCO)


def friso_azulejos():
    d = I.FRISO
    p = Hoja(W, H * 2, PAPEL)
    p.rect(16, 16, W - 16, H * 2 - 16, None, OCRE, 6)
    p.rect(28, 28, W - 28, H * 2 - 28, None, OCRE, 2)
    p.texto((W / 2 + 26, 70), "EL FRISO DE AZULEJOS", "cartel", 32, TINTA)
    p.texto((W / 2 + 26, 108), "de la cripta", "texto2", 20, TINTA)
    t = 170
    for r in range(3):
        y = 330 + r * 240 if r < 2 else H + 200
        for c in range(3):
            x = W / 2 + (c - 1) * (t + 20)
            if r == 2 and c == 2:
                p.rect(x - t / 2, y - t / 2, x + t / 2, y + t / 2, (200, 180, 140), TINTA, 3)
                p.texto((x, y), "?", "cartel", 80, TERRA)
            else:
                e = d["celdas"][r][c]
                azulejo(p, x, y, t, e["fig"], e["color"], e["tam"])
    return p.final()


# ------------------------------------------------------------------ 75/79: el campo por repartir
def campo():
    d = I.TIERRAS
    n = d["n"]
    p = Hoja(W * 2, H, (206, 190, 130))
    p.rect(16, 16, W * 2 - 16, H - 16, None, TURQ, 6)
    p.rect(28, 28, W * 2 - 28, H - 28, None, TURQ, 2)
    p.texto((W, 66), "EL CAMPO POR REPARTIR", "cartel", 34, TINTA)
    lado = 90
    x0, y0 = (W * 2 - n * lado) / 2, 118
    for y in range(n):
        for x in range(n):
            p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, (230, 214, 160), (150, 130, 80), 2)
    for x, y, a in d["pistas"]:
        p.texto((x0 + x * lado + lado / 2, y0 + y * lado + lado / 2), str(a), "cartel", 38, TINTA)
    return p.final()


# ------------------------------------------------------------------ 86/87: los sellos
def sellos_acertijo(titulo, versos_l):
    p = pagina(titulo, "dictado por la sacerdotisa", PAPEL, OCRE)
    versos(p, versos_l, 230, 58, 25)
    return p.final()


def inyectar(carpeta):
    """Mete los datos de las instancias en las apps (bloque /*DATOS*/.../*FIN*/)."""
    figs = lambda *n: {k: I.FIGURAS[k] for k in n}
    datos = {
        "14-monton.js": I.MONTON, "20-piramide.js": I.PIRAMIDE, "40-nilometro.js": I.NILOMETRO,
        "48-friso.js": {"animales": I.ANIMALES, "solucion": I.CONTAR["solucion"], "figuras": figs(*I.ANIMALES)},
        "52-heqat.js": I.HEQAT,
        "46-cripto.js": {"suma": I.CRIPTO["suma"], "signos": I.CRIPTO["signos"], "solucion": I.CRIPTO["solucion"], "figuras": figs(*I.SIGNOS)},
        "51-camaras.js": I.CAMARAS, "69-canales.js": I.CANALES,
        "64-azulejos.js": {"opciones": I.FRISO["opciones"], "solucion": I.FRISO["solucion"], "figuras": figs(*I.FIG3), "colores": I.COL3},
        "72-tierras.js": {"n": I.TIERRAS["n"], "solucion": I.TIERRAS["solucion"]},
        "85-sellos.js": {"sellos": I.SELLOS, "orden": I.ORDEN_SELLOS, "figuras": I.FIGURAS},
    }
    for app, d in datos.items():
        ruta = os.path.join(carpeta, "minijuegos", app)
        txt = open(ruta, encoding="utf-8").read() if os.path.exists(ruta) else ""
        if "/*DATOS*/" not in txt:
            continue
        a, b = txt.index("/*DATOS*/") + len("/*DATOS*/"), txt.index("/*FIN*/")
        open(ruta, "w", encoding="utf-8", newline="\n").write(txt[:a] + json.dumps(d, ensure_ascii=False) + txt[b:])


def main(carpeta="juegos/aventuras-ca/egipto"):
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    g = lambda k, im: ruido(im, int(k)).save(os.path.join(arte, f"{k}.png"))

    def mosaico(nombre, im, filas, cols, cartas):
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))
        for pieza, k in zip(cortar(im, filas, cols), cartas):
            pieza.save(os.path.join(arte, f"{k}.png"))
    g("16", monton())
    g("18", acertijo_piramide())
    mosaico("piramide", piramide(), 2, 1, ("19", "21"))
    g("41", registro1())
    g("43", registro2())
    g("45", vara())
    mosaico("friso", friso_animales(), 1, 2, ("42", "49"))
    g("53", guardian())
    g("54", partes_ojo())
    g("55", pagos("PAGO DE LA MAÑANA", "tres sacos de cebada", I.HEQAT["manana"]))
    g("59", pagos("PAGO DE LA TARDE", "tres sacos más", I.HEQAT["tarde"]))
    g("37", suma_signos())
    g("39", pista_signos("PRIMERA NOTA", I.CRIPTO["pistas"][0]))
    g("33", pista_signos("SEGUNDA NOTA", I.CRIPTO["pistas"][1]))
    g("26", papiro_camaras())
    mosaico("camaras", plano_camaras(), 1, 2, ("61", "63"))
    g("70", mapa_canales())
    g("71", nota_visir())
    mosaico("azulejos", friso_azulejos(), 2, 1, ("66", "67"))
    mosaico("tierras", campo(), 1, 2, ("75", "79"))
    g("86", sellos_acertijo("PRIMERA PARTE DEL ORDEN", ["«Primero, el sello de lo que", "sube y baja con el año.", "", "Segundo, el de lo que", "se reparte con cordel.", "",
                                                       "Tercero, el de lo que se amasa", "y se come.»"]))
    g("87", sellos_acertijo("SEGUNDA PARTE DEL ORDEN", ["«Cuarto, el sello del que mide", "con sus seis partes", "al dios halcón.", "", "Quinto, el del que empuja",
                                                       "el sol por el cielo", "cada mañana.»"]))
    inyectar(carpeta)
    print("láminas de Egipto escritas en", arte)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

"""Láminas de «Pompeya, 79 d.C.» (versión de 60 cartas): todas las cartas-pista se dibujan por código a partir de instancias_pompeya.json,
así que lo que enseñan es exacto. Las pistas son dibujos o acertijos: ninguna carta explica cómo se resuelve su puzle.

  14-17 mosaico laberinto del atrio (2 x 2) · 18 acertijo de Lucio · 21, 23, 24 tablillas de cuentas · 25 la regla del escriba
  27 y 29 la impronta del sello (dos mitades) · 36 el acueducto · 37 el plano del jardín · 41 el muro del cuadrado · 42 el acertijo del sembrador
  43 las pesadas · 45 el recibo · 51, 52, 53 grafitis · 54 plano de la manzana · 61 y 63 el calendario de piedra (dos mitades) · 65 el acertijo de Plinio
  67 el mapa de la huida · 75 el vigía · 71 el manifiesto · 72 el barquero · 76 la tablilla de Lucrecia
Imágenes de los minijuegos (img/ui): figuras del panel, anillos, ánforas y bultos de la barca. Copia en cada minijuego sus datos (/*DATOS*/).
Uso (desde la raíz del repo):  python herramientas/pompeya.py [carpeta_juego]
"""
import json
import math
import os
import random
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oeste import Hoja  # noqa: E402
from mosaicos import cortar  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
W, H = 630, 882
CERA = (226, 200, 140)
MADERA = (120, 80, 44)
TINTA = (46, 32, 22)
ROJO = (156, 40, 30)
OCRE = (196, 140, 60)
TERRA = (176, 92, 56)
MARMOL = (236, 230, 216)
BLANCO = (250, 246, 236)
NEGRO = (28, 24, 22)
AZUL = (40, 80, 140)
VERDE = (70, 120, 70)
ORO = (214, 170, 60)
GRIS = (130, 126, 120)


def inst():
    return json.load(open(os.path.join(AQUI, "instancias_pompeya.json"), encoding="utf-8"))


def ruido(im, semilla, fuerza=3):
    a = np.asarray(im).astype(np.int16)
    a = a + np.random.default_rng(semilla).normal(0, fuerza, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def tablilla(titulo, sub=None, fondo=CERA):
    h = Hoja(W, H, MADERA)
    h.rect(14, 14, W - 14, H - 14, MADERA, (70, 44, 22), 6)
    h.rect(40, 40, W - 40, H - 40, fondo, (90, 60, 30), 3)
    h.texto((W / 2 + 26, 84), titulo, "cartel", 32, TINTA)
    if sub:
        h.texto((W / 2 + 26, 120), sub, "texto2", 20, TINTA)
    return h


# ================================================================== figuras (panel del tablinum, mosaico y anillos)
def figura(h, nombre, cx, cy, r, col, fondo):
    if nombre == "delfin":
        h.elip(cx - r, cy - r * 0.35, cx + r * 0.6, cy + r * 0.35, col)
        h.poli([(cx + r * 0.5, cy), (cx + r, cy - r * 0.5), (cx + r * 0.85, cy), (cx + r, cy + r * 0.5)], col)
        h.poli([(cx - r * 0.2, cy - r * 0.3), (cx, cy - r * 0.75), (cx + r * 0.15, cy - r * 0.3)], col)
        h.disco(cx - r * 0.6, cy - r * 0.08, r * 0.09, fondo)
    elif nombre == "anfora":
        h.elip(cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.55, col)
        h.poli([(cx - r * 0.2, cy - r * 0.4), (cx + r * 0.2, cy - r * 0.4), (cx + r * 0.12, cy - r * 0.95), (cx - r * 0.12, cy - r * 0.95)], col)
        h.poli([(cx - r * 0.1, cy + r * 0.5), (cx + r * 0.1, cy + r * 0.5), (cx, cy + r)], col)
        for s in (-1, 1):
            h.d.arc([(cx + s * r * 0.15 - r * 0.25) * 2, (cy - r * 0.85) * 2, (cx + s * r * 0.15 + r * 0.25) * 2, (cy - r * 0.25) * 2],
                    -90 if s > 0 else 90, 90 if s > 0 else 270, fill=col, width=int(r * 0.2))
    elif nombre == "laurel":
        for k in range(6):
            a = math.radians(200 + k * 28)
            x, y = cx + r * 0.75 * math.cos(a), cy + r * 0.75 * math.sin(a)
            h.elip(x - r * 0.18, y - r * 0.32, x + r * 0.18, y + r * 0.32, col)
        h.d.arc([(cx - r * 0.8) * 2, (cy - r * 0.8) * 2, (cx + r * 0.8) * 2, (cy + r * 0.8) * 2], 190, 350, fill=col, width=int(r * 0.12))
    elif nombre == "lechuza":
        h.elip(cx - r * 0.55, cy - r * 0.4, cx + r * 0.55, cy + r * 0.9, col)
        h.disco(cx, cy - r * 0.45, r * 0.5, col)
        h.disco(cx - r * 0.2, cy - r * 0.48, r * 0.15, fondo)
        h.disco(cx + r * 0.2, cy - r * 0.48, r * 0.15, fondo)
        h.poli([(cx - r * 0.45, cy - r * 0.8), (cx - r * 0.3, cy - r * 1.05), (cx - r * 0.15, cy - r * 0.85)], col)
        h.poli([(cx + r * 0.45, cy - r * 0.8), (cx + r * 0.3, cy - r * 1.05), (cx + r * 0.15, cy - r * 0.85)], col)
    elif nombre == "racimo":
        for fila, n in enumerate((4, 3, 2, 1)):
            for k in range(n):
                h.disco(cx + (k - (n - 1) / 2) * r * 0.36, cy - r * 0.35 + fila * r * 0.32, r * 0.19, col)
        h.linea([(cx, cy - r * 0.55), (cx + r * 0.2, cy - r * 0.95)], col, r * 0.1)
    elif nombre == "concha":
        h.poli([(cx, cy + r * 0.7)] + [(cx + r * 0.9 * math.cos(math.radians(a)), cy + r * 0.1 - r * 0.8 * math.sin(math.radians(a))) for a in range(0, 181, 15)], col)
        for k in range(1, 6):
            a = math.radians(k * 30)
            h.linea([(cx, cy + r * 0.7), (cx + r * 0.85 * math.cos(a), cy + r * 0.1 - r * 0.75 * math.sin(a))], fondo, r * 0.06)
    elif nombre == "lucerna":
        h.elip(cx - r * 0.8, cy - r * 0.2, cx + r * 0.5, cy + r * 0.4, col)
        h.poli([(cx + r * 0.4, cy - r * 0.05), (cx + r * 0.95, cy + r * 0.05), (cx + r * 0.4, cy + r * 0.25)], col)
        h.poli([(cx + r * 0.9, cy), (cx + r * 0.8, cy - r * 0.5), (cx + r, cy - r * 0.2)], (240, 160, 40))
        h.d.arc([(cx - r * 1.05) * 2, (cy - r * 0.35) * 2, (cx - r * 0.55) * 2, (cy + r * 0.3) * 2], 90, 270, fill=col, width=int(r * 0.14))
    else:  # escudo
        h.elip(cx - r * 0.75, cy - r * 0.9, cx + r * 0.75, cy + r * 0.9, col)
        h.elip(cx - r * 0.5, cy - r * 0.65, cx + r * 0.5, cy + r * 0.65, fondo)
        h.disco(cx, cy, r * 0.25, col)


# ================================================================== 14-17: mosaico laberinto
def mosaico_laberinto(lab):
    n = lab["n"]
    W2, H2 = 2 * W, 2 * H
    h = Hoja(W2, H2, (150, 70, 46))
    rng = random.Random(14)
    tes = 14
    for y in range(0, H2, tes):
        for x in range(0, W2, tes):
            c = (150 + rng.randint(-14, 14), 70 + rng.randint(-10, 10), 46 + rng.randint(-8, 8))
            h.rect(x + 1, y + 1, x + tes - 1, y + tes - 1, c)
    celx, cely = (W2 - 200) / n, (H2 - 220) / n
    x0, y0 = (W2 - n * celx) / 2, (H2 - n * cely) / 2
    abiertos = {frozenset(tuple(p) for p in par) for par in lab["pasos"]}
    blanco = lambda: (236 + rng.randint(-10, 8), 228 + rng.randint(-10, 8), 210 + rng.randint(-10, 8))

    def pinta_tes(px0, py0, px1, py1):
        for y in range(int(py0), int(py1), tes):
            for x in range(int(px0), int(px1), tes):
                h.rect(x + 1, y + 1, min(x + tes, px1) - 1, min(y + tes, py1) - 1, blanco())
    ancho = 42
    for y in range(n):
        for x in range(n):
            cx, cy = x0 + x * celx + celx / 2, y0 + y * cely + cely / 2
            pinta_tes(cx - ancho / 2, cy - ancho / 2, cx + ancho / 2, cy + ancho / 2)
            if frozenset({(x, y), (x + 1, y)}) in abiertos:
                pinta_tes(cx, cy - ancho / 2, cx + celx, cy + ancho / 2)
            if frozenset({(x, y), (x, y + 1)}) in abiertos:
                pinta_tes(cx - ancho / 2, cy, cx + ancho / 2, cy + cely)
    # el sol (este) y la puerta (oeste)
    sx, sy = lab["inicio"]
    cx, cy = x0 + sx * celx + celx / 2, y0 + sy * cely + cely / 2
    pinta_tes(cx, cy - ancho / 2, W2 - 40, cy + ancho / 2)
    h.disco(W2 - 70, cy, 46, ORO, TINTA, 4)
    for k in range(12):
        a = k * math.pi / 6
        h.linea([(W2 - 70 + 54 * math.cos(a), cy + 54 * math.sin(a)), (W2 - 70 + 70 * math.cos(a), cy + 70 * math.sin(a))], ORO, 7)
    fx, fy = lab["fin"]
    cx, cy = x0 + fx * celx + celx / 2, y0 + fy * cely + cely / 2
    pinta_tes(40, cy - ancho / 2, cx, cy + ancho / 2)
    h.rect(20, cy - 60, 70, cy + 60, (90, 56, 30), TINTA, 4)
    h.disco(58, cy, 6, ORO)
    for (fx, fy), nombre in lab["figuras"]:
        cx, cy = x0 + fx * celx + celx / 2, y0 + fy * cely + cely / 2
        h.disco(cx, cy, 40, (30, 60, 110), ORO, 5)
        figura(h, nombre, cx, cy, 26, (236, 220, 170), (30, 60, 110))
    h.rect(10, 10, W2 - 10, H2 - 10, None, (60, 30, 20), 12)
    return h.final()


def acertijo_lucio():
    h = tablilla("TABLILLA DE LUCIO", "el mosaiquista")
    versos = ["Nazco donde nace el sol", "y muero donde se pone.", "Solo piso la piedra blanca,", "nunca vuelvo sobre mis pasos",
              "y saludo, por orden,", "a quien me sale al paso.", "Quien sepa a quién saludé", "tiene la llave del despacho."]
    for k, v in enumerate(versos):
        h.texto((W / 2, 220 + k * 56), v, "texto2", 28, TINTA)
    return h.final()


# ================================================================== 21-25: cuentas
def tablilla_cuentas(cu, d):
    dia = cu["dias"][d]
    h = tablilla("CUENTAS DE LUCRECIA", f"Día {['I', 'II', 'III'][d]} · ventas en sestercios")
    for k, (item, num) in enumerate(zip(dia["items"], dia["romanos"])):
        y = 230 + k * 92
        figura_producto(h, item, 120, y)
        h.texto((200, y), item, "texto2", 26, TINTA, "lm")
        h.texto((W - 80, y), num, "cartel", 40, TINTA, "rm")
        h.linea([(90, y + 40), (W - 80, y + 40)], (150, 110, 60), 1)
    h.linea([(90, 640), (W - 80, 640)], TINTA, 4)
    h.texto((120, 690), "SVMMA", "cartel", 34, ROJO, "lm")
    h.texto((W - 80, 690), dia["escrito_romano"], "cartel", 42, ROJO, "rm")
    h.texto((W / 2, 770), "escrito por Tiro, el esclavo", "texto2", 21, TINTA)
    return h.final()


def figura_producto(h, item, cx, cy):
    col = {"aceite": (190, 170, 60), "vino": (130, 30, 50), "garum": (150, 110, 70), "higos": (110, 60, 90), "trigo": (210, 170, 80),
           "miel": (220, 160, 40), "sal": (230, 230, 230), "lana": (240, 236, 220)}[item]
    h.elip(cx - 22, cy - 20, cx + 22, cy + 30, col, TINTA, 2)
    h.rect(cx - 8, cy - 34, cx + 8, cy - 18, col, TINTA, 2)


def regla_escriba():
    h = tablilla("LA REGLA DEL ESCRIBA", "para leer las cuentas")
    vals = [("I", 1), ("V", 5), ("X", 10), ("L", 50), ("C", 100), ("D", 500), ("M", 1000)]
    for k, (s, v) in enumerate(vals):
        x = 92 + k * 74
        h.rect(x - 32, 170, x + 32, 250, BLANCO, TINTA, 2)
        h.texto((x, 210), s, "cartel", 40, TINTA)
        h.texto((x, 280), str(v), "texto", 22, TINTA)
    ejemplos = [("VI", "5 + 1"), ("IV", "5 − 1"), ("XC", "100 − 10"), ("CX", "100 + 10"), ("MCD", "1000 + 500 − 100")]
    for k, (a, b) in enumerate(ejemplos):
        y = 360 + k * 66
        h.texto((180, y), a, "cartel", 34, ROJO, "rm")
        h.texto((210, y), "=", "texto", 28, TINTA, "mm")
        h.texto((240, y), b, "texto2", 28, TINTA, "lm")
    h.texto((W / 2, 720), "«Tiro suma mal cuando tiene prisa.»", "texto2", 24, TINTA)
    h.texto((W / 2, 760), "— Lucrecia", "texto2", 22, TINTA)
    return h.final()


# ================================================================== 27/29: la impronta del sello
def motivo(simbolo, letras, voltea_simbolo, voltea_letras, fondo, col, lado=600):
    """El dibujo de un sello: el símbolo arriba y las letras abajo, cada parte volteada o no."""
    a = Hoja(lado, lado * 2 // 3, fondo)
    figura(a, simbolo, lado / 2, lado / 3, lado * 0.28, col, fondo)
    sim = a.final()
    b = Hoja(lado, lado // 3, fondo)
    b.texto((lado / 2, lado / 6), letras, "cartel", int(lado * 0.18), col)
    let = b.final()
    if voltea_simbolo:
        sim = sim.transpose(Image.FLIP_LEFT_RIGHT)
    if voltea_letras:
        let = let.transpose(Image.FLIP_LEFT_RIGHT)
    m = Image.new("RGB", (lado, lado), fondo)
    m.paste(sim, (0, 0))
    m.paste(let, (0, lado * 2 // 3))
    return m


def impronta(se):
    h = Hoja(W * 2, H, (232, 220, 190))
    cx, cy, r = W, H / 2, 300
    h.disco(cx, cy, r, (176, 34, 30), (120, 20, 18), 10)
    h.disco(cx, cy, r * 0.8, (160, 28, 26), (130, 22, 20), 6)
    im = h.final()
    m = motivo(se["impronta"]["simbolo"], se["impronta"]["letras"], True, True, (160, 28, 26), (210, 80, 70), 420)
    fondo = np.array((160, 28, 26))
    mascara = Image.fromarray((np.abs(np.asarray(m).astype(np.int16) - fondo).sum(axis=2) > 40).astype(np.uint8) * 255)
    im.paste(m, (int(cx - 210), int(cy - 200)), mascara)
    hh = Hoja(W * 2, H)
    hh.im = im.resize((W * 4, H * 2))
    from PIL import ImageDraw
    hh.d = ImageDraw.Draw(hh.im)
    hh.linea([(W, 60), (W - 10, 300), (W + 12, 520), (W - 6, H - 60)], (232, 220, 190), 6)
    return hh.final()


def anillo_png(an, ruta):
    h = Hoja(240, 240, (255, 0, 255))
    h.disco(120, 120, 110, ORO, (140, 100, 30), 6)
    h.disco(120, 120, 80, (60, 30, 30), (140, 100, 30), 4)
    im = h.final()
    m = motivo(an["simbolo"], an["letras"], an["voltea_simbolo"], an["voltea_letras"], (60, 30, 30), (230, 200, 120), 300).resize((130, 130))
    im.paste(m, (55, 55))
    a = np.asarray(im).astype(np.int16)
    alfa = np.clip(np.abs(a - np.array((255, 0, 255))).sum(axis=2) * 3, 0, 255).astype(np.uint8)
    Image.fromarray(np.dstack([np.asarray(im), alfa])).save(ruta)


# ================================================================== 36/37: la fuente
def acueducto(fu):
    h = Hoja(W, H, MARMOL)
    h.rect(16, 16, W - 16, H - 16, None, TINTA, 4)
    h.texto((W / 2 + 26, 62), "EL ACUEDUCTO DE LA VILLA", "cartel", 30, TINTA)
    h.texto((W / 2 + 26, 98), "Plano del fontanero", "texto2", 21, TINTA)
    pos = {"acueducto": (315, 170), "A": (150, 340), "B": (315, 470), "C": (480, 340),
           "rosas": (90, 640), "laureles": (240, 700), "vina": (420, 700), "lirios": (560, 560)}
    for nudo, sal in fu["red"].items():
        for comp, dest in sal:
            (x0, y0), (x1, y1) = pos[nudo], pos[dest]
            h.linea([(x0, y0), (x1, y1)], (90, 130, 170), 10)
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            h.rect(mx - 30, my - 18, mx + 30, my + 18, (110, 80, 50), TINTA, 3)
            h.texto((mx, my + 1), comp, "cartel", 22, BLANCO)
    for nudo, (x, y) in pos.items():
        if nudo in fu["pide"]:
            h.elip(x - 52, y - 30, x + 52, y + 30, (110, 160, 90), TINTA, 3)
            h.texto((x, y), {"rosas": "rosas", "laureles": "laureles", "vina": "viña", "lirios": "lirios"}[nudo], "texto", 20, TINTA)
        else:
            h.disco(x, y, 34, (200, 210, 220), TINTA, 3)
            h.texto((x, y), "XXXVI" if nudo == "acueducto" else nudo, "cartel", 20 if nudo == "acueducto" else 26, TINTA)
    h.texto((W / 2, 800), "Cada arqueta reparte el agua por igual entre sus compuertas abiertas.", "texto2", 18, TINTA)
    h.texto((W / 2, 828), "Lo que llega a una arqueta sin salida, se pierde.", "texto2", 18, TINTA)
    return h.final()


def anfora_peq(h, cx, cy, s=1.0, col=TERRA):
    h.elip(cx - 9 * s, cy - 10 * s, cx + 9 * s, cy + 12 * s, col, TINTA, 1.5)
    h.rect(cx - 3 * s, cy - 18 * s, cx + 3 * s, cy - 9 * s, col)
    h.poli([(cx - 3 * s, cy + 11 * s), (cx + 3 * s, cy + 11 * s), (cx, cy + 18 * s)], col)


def plano_jardin(fu):
    h = Hoja(W, H, (196, 186, 150))
    h.rect(16, 16, W - 16, H - 16, None, TINTA, 4)
    h.texto((W / 2 + 26, 62), "EL JARDÍN DE LUCRECIA", "cartel", 30, TINTA)
    h.texto((W / 2 + 26, 98), "Lo que bebe cada parterre al día", "texto2", 21, TINTA)
    zonas = {"rosas": (60, 150, 300, 420), "laureles": (330, 150, 570, 420), "vina": (60, 450, 300, 720), "lirios": (330, 450, 570, 720)}
    nombres = {"rosas": "ROSAS", "laureles": "LAURELES", "vina": "VIÑA", "lirios": "LIRIOS"}
    for p, (x0, y0, x1, y1) in zonas.items():
        h.rect(x0, y0, x1, y1, (120, 150, 90), TINTA, 3)
        h.texto(((x0 + x1) / 2, y0 + 26), nombres[p], "texto", 22, BLANCO)
        n = fu["pide"][p]
        for k in range(n):
            fila, col = divmod(k, 6)
            anfora_peq(h, x0 + 36 + col * 34, y0 + 90 + fila * 56, 1.2)
    h.texto((W / 2, 780), "Ni una gota más, ni una menos:", "texto2", 22, TINTA)
    h.texto((W / 2, 812), "el jardinero lo apunta con ánforas.", "texto2", 22, TINTA)
    return h.final()


# ================================================================== 41/42: el cuadrado
def muro_cuadrado(sa):
    h = Hoja(W, H, (200, 80, 60))
    for y in range(0, H, 6):
        h.linea([(0, y), (W, y)], (196, 76, 58), 2)
    h.rect(16, 16, W - 16, H - 16, None, (90, 30, 20), 5)
    h.texto((W / 2 + 26, 64), "UN GRAFITO EN LA COLUMNA", "cartel", 30, BLANCO)
    h.texto((W / 2 + 26, 100), "del triclinio, medio borrado", "texto2", 21, BLANCO)
    lado, x0, y0 = 96, 75, 190
    borr = {tuple(x) for x in sa["borradas"]}
    for f in range(5):
        for c in range(5):
            x, y = x0 + c * lado, y0 + f * lado
            if (f, c) in borr:
                h.rect(x + 6, y + 6, x + lado - 6, y + lado - 6, (214, 120, 96))
                for k in range(5):
                    h.linea([(x + 12 + k * 14, y + 12), (x + 4 + k * 14, y + lado - 12)], (230, 150, 120), 3)
            else:
                h.texto((x + lado / 2, y + lado / 2), sa["filas"][f][c], "cartel", 56, (250, 236, 210))
    return h.final()


def acertijo_sembrador():
    h = tablilla("EL ACERTIJO DEL SEMBRADOR", "escrito bajo el grafito", (232, 214, 170))
    versos = ["Léeme de arriba abajo", "o de abajo arriba,", "de izquierda a derecha", "o al revés, como gustes:",
              "siempre digo lo mismo.", "La puerta del jardín se abre", "con la palabra de mi cruz."]
    for k, v in enumerate(versos):
        h.texto((W / 2, 230 + k * 60), v, "texto2", 30, TINTA)
    return h.final()


# ================================================================== 43/45: la balanza
def bulto(h, cosa, cx, cy):
    if cosa == "aceite":
        anfora_peq(h, cx, cy, 2.2, (190, 170, 70))
    elif cosa == "vino":
        anfora_peq(h, cx, cy, 2.2, (130, 30, 50))
    elif cosa == "higos":
        h.elip(cx - 22, cy - 6, cx + 22, cy + 26, (150, 110, 60), TINTA, 2)
        for k in range(3):
            h.disco(cx - 10 + k * 10, cy - 6, 7, (110, 60, 90))
    else:
        h.rect(cx - 12, cy - 6, cx + 12, cy + 18, GRIS, TINTA, 2)
        h.disco(cx, cy - 10, 5, None, TINTA, 2)


def balanza_dibujo(h, cx, y, izq, der):
    h.rect(cx - 5, y, cx + 5, y + 150, MADERA, TINTA, 2)
    h.poli([(cx - 40, y + 160), (cx + 40, y + 160), (cx + 10, y + 145), (cx - 10, y + 145)], MADERA, TINTA, 2)
    h.rect(cx - 180, y - 4, cx + 180, y + 4, MADERA, TINTA, 2)
    for lado, cosas in ((-1, izq), (1, der)):
        px = cx + lado * 150
        h.linea([(px, y), (px - 50, y + 90)], TINTA, 2)
        h.linea([(px, y), (px + 50, y + 90)], TINTA, 2)
        h.rect(px - 62, y + 90, px + 62, y + 98, ORO, TINTA, 2)
        for k, c in enumerate(cosas):
            bulto(h, c, px - (len(cosas) - 1) * 13 + k * 26, y + 62)


def pesadas(st):
    h = Hoja(W, H, MARMOL)
    h.rect(16, 16, W - 16, H - 16, None, TINTA, 4)
    h.texto((W / 2 + 26, 62), "LAS PESADAS DEL MERCADER", "cartel", 30, TINTA)
    h.texto((W / 2 + 26, 98), "Tres pruebas que salieron justas", "texto2", 21, TINTA)
    for k, (a, b) in enumerate(st["pesadas"]):
        balanza_dibujo(h, W / 2, 150 + k * 205, a, b)
    bulto(h, "pesa", 230, 790)
    h.texto((260, 794), "= una libra", "texto", 24, TINTA, "lm")
    return h.final()


def recibo(st):
    h = tablilla("RECIBO DEL MERCADER", "Lo que contiene el cofre de Lucrecia", (236, 220, 180))
    y = 240
    for cosa, n in st["cofre"].items():
        for k in range(n):
            bulto(h, cosa, 150 + k * 80, y)
        y += 120
    h.rect(110, y - 10, 520, y + 70, (210, 180, 120), TINTA, 3)
    for k in range(st["tara"]):
        bulto(h, "pesa", 190 + k * 40, y + 30)
    h.texto((340, y + 30), "el cofre, vacío", "texto2", 22, TINTA, "lm")
    h.texto((W / 2, 760), "«El contrapeso de la balanza pesa", "texto2", 22, TINTA)
    h.texto((W / 2, 792), "lo mismo que el cofre vacío.»", "texto2", 22, TINTA)
    return h.final()


# ================================================================== 51-54: grafitis y plano de la manzana
GRAFITIS = {
    "51": ["«Lucrecia vive donde", "no se vende nada:", "en su puerta solo hay casa.»"],
    "52": ["«Huele a pan recién hecho", "pegado a su pared,", "a un lado o al otro.»"],
    "53": ["«Su puerta mira al mar", "y la pintó de rojo", "para que la viera su marido.»"],
}


def grafito(texto, sem):
    rng = random.Random(sem)
    h = Hoja(W, H, (226, 214, 190))
    for _ in range(400):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        h.disco(x, y, rng.uniform(1, 3), (210, 196, 170))
    h.rect(16, 16, W - 16, H - 16, None, (140, 120, 90), 4)
    h.texto((W / 2 + 26, 64), "GRAFITO EN UNA PARED", "cartel", 30, (90, 70, 50))
    for k, t in enumerate(texto):
        h.texto((W / 2 + rng.uniform(-8, 8), 300 + k * 74), t, "texto2", 32, (60, 50, 70))
    return h.final()


ICONO = {"panaderia": "pan", "taberna": "vino", "fuente": "agua", "templo": "templo", "termas": "termas", "lavanderia": "telas",
         "barbero": "navaja", "taller": "martillo", "casa": ""}


def plano_manzana(ca):
    h = Hoja(W, H, (210, 196, 160))
    h.rect(16, 16, W - 16, H - 16, None, TINTA, 4)
    h.texto((W / 2 + 26, 62), "PLANO DE LA MANZANA", "cartel", 30, TINTA)
    h.texto((W / 2 + 26, 98), "Copiado de la pared del foro", "texto2", 21, TINTA)
    filas, cols = ca["filas"], ca["cols"]
    lado = 108
    x0, y0 = (W - cols * lado) / 2, 170
    h.texto((W / 2, y0 - 22), "NORTE · calle del foro", "texto2", 18, TINTA)
    COL = {"roja": (190, 70, 50), "ocre": (210, 160, 70), "blanca": (238, 232, 220)}
    for c in ca["casas"]:
        x, y = x0 + c["c"] * lado, y0 + c["f"] * (lado + 26)
        h.rect(x + 4, y + 4, x + lado - 4, y + lado - 4, COL[c["pintada"]], TINTA, 3)
        py = y + lado - 6 if c["puerta"] == "sur" else y + 6
        h.rect(x + lado / 2 - 12, py - 6, x + lado / 2 + 12, py + 6, (70, 44, 24))
        if c["rasgo"] != "casa":
            h.texto((x + lado / 2, y + lado / 2), ICONO[c["rasgo"]], "texto", 18, TINTA)
    h.texto((W / 2, y0 + filas * (lado + 26) + 6), "SUR · calle del mar", "texto2", 18, TINTA)
    h.texto((W / 2, 820), "La mancha oscura es la puerta de cada casa.", "texto2", 18, TINTA)
    return h.final()


# ================================================================== 61/63/65: el calendario
def calendario(cal):
    h = Hoja(W * 2, H, (200, 196, 186))
    rng = random.Random(61)
    for _ in range(900):
        h.disco(rng.uniform(0, W * 2), rng.uniform(0, H), rng.uniform(1, 3), (186, 180, 170))
    h.texto((W, 70), "AVGVSTVS", "cartel", 50, TINTA)
    lado = 120
    x0, y0 = 60, 150
    for d in range(1, 33):
        k = d - 1
        f, c = divmod(k, 10)
        x, y = x0 + c * lado, y0 + f * 150
        h.rect(x + 6, y, x + lado - 6, y + 120, (214, 210, 200), TINTA, 2)
        etiqueta = str(d) if d <= 31 else "1"
        h.texto((x + lado / 2, y + 40), etiqueta, "cartel", 40, TINTA if d <= 31 else ROJO)
        if d == 1:
            h.texto((x + lado / 2, y + 90), "KAL.", "texto", 22, ROJO)
        elif d == 5:
            h.texto((x + lado / 2, y + 90), "NON.", "texto", 22, ROJO)
        elif d == 13:
            h.texto((x + lado / 2, y + 90), "EID.", "texto", 22, ROJO)
        elif d == 32:
            h.texto((x + lado / 2, y + 90), "KAL. SEPT.", "texto", 18, ROJO)
        elif d == cal["ejemplo"]["dia"]:
            h.texto((x + lado / 2, y + 90), "a.d. IV", "texto", 20, AZUL)
    h.texto((W, H - 70), "Así cuentan los días los sacerdotes de Isis.", "texto2", 26, TINTA)
    return h.final()


def acertijo_plinio(cal):
    h = tablilla("CARTA DE PLINIO", "al sacerdote de Isis", (232, 220, 190))
    versos = ["«Anota bien el día:", "el monte despertó", "nueve días antes", "de las calendas de septiembre.", "Que lo recuerden",
              "los que vengan detrás.»"]
    for k, v in enumerate(versos):
        h.texto((W / 2, 240 + k * 60), v, "texto2", 30, TINTA)
    return h.final()


# ================================================================== 67/75: la huida
POS_H = {"F": (90, 240), "A": (250, 170), "B": (220, 400), "C": (400, 320), "D": (420, 160), "E": (560, 260), "G": (380, 560), "P": (540, 640)}
NOM_H = {"F": "foro", "A": "templo", "B": "termas", "C": "teatro", "D": "mercado", "E": "lupanar", "G": "anfiteatro", "P": "puerto"}


def mapa_huida(hu):
    from instancias_pompeya import romano
    h = Hoja(W, H, (216, 204, 176))
    h.rect(16, 16, W - 16, H - 16, None, TINTA, 4)
    h.texto((W / 2 + 26, 62), "LAS CALLES HASTA EL PUERTO", "cartel", 30, TINTA)
    h.texto((W / 2 + 26, 98), "En pasos de ceniza (cada uno, un minuto)", "texto2", 20, TINTA)
    for a, b, t in hu["calles"]:
        (x0, y0), (x1, y1) = POS_H[a], POS_H[b]
        h.linea([(x0, y0), (x1, y1)], (150, 130, 100), 12)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        h.rect(mx - 26, my - 16, mx + 26, my + 16, (240, 230, 206), TINTA, 2)
        h.texto((mx, my + 1), romano(t), "cartel", 20, TINTA)
    for n, (x, y) in POS_H.items():
        h.disco(x, y, 30, ROJO if n in "FP" else (90, 70, 50), TINTA, 3)
        h.texto((x, y + 48), NOM_H[n], "texto", 18, TINTA)
    h.texto((W / 2, 780), "Salís del foro.", "texto2", 22, TINTA)
    return h.final()


def vigia(hu):
    from instancias_pompeya import romano
    h = tablilla("EL VIGÍA DE LA TORRE", "lo que grita desde arriba", (232, 220, 190))
    corta = {frozenset(c) for c in map(tuple, hu["cortadas"])}
    y = 220
    for a, b in hu["cortadas"]:
        h.texto((W / 2, y), f"«¡Entre el {NOM_H[a]} y el {NOM_H[b]}", "texto2", 26, TINTA)
        h.texto((W / 2, y + 36), "han caído las columnas!»", "texto2", 26, TINTA)
        y += 100
    h.texto((W / 2, y + 40), f"«En {romano(hu['limite'])} pasos la ceniza", "texto", 26, ROJO)
    h.texto((W / 2, y + 78), "tapará la puerta del puerto.»", "texto", 26, ROJO)
    return h.final()


# ================================================================== 71/72/76: la barca
NOM_B = {"anfora_aceite": "ánfora de aceite", "anfora_vino": "ánfora de vino", "fardo_lana": "fardo de lana", "cofre_monedas": "cofre de monedas",
         "estatua_lar": "estatua del lar", "saco_trigo": "saco de trigo"}


def manifiesto(ba):
    h = tablilla("LA CARGA DEL MUELLE", "lo que Lucrecia quiere salvar", (236, 222, 186))
    for k, (cosa, (peso, valor)) in enumerate(ba["carga"].items()):
        y = 200 + k * 96
        h.texto((70, y), NOM_B[cosa], "texto", 22, TINTA, "lm")
        for i in range(peso):
            bulto(h, "pesa", 330 + i * 24, y - 6)
        for i in range(valor):
            h.disco(80 + i * 22, y + 34, 9, ORO, TINTA, 1.5)
    h.texto((W / 2, 800), "pesas: lo que pesa · monedas: lo que vale", "texto2", 20, TINTA)
    return h.final()


def barquero(ba):
    from instancias_pompeya import romano
    h = Hoja(W, H, (120, 170, 200))
    h.rect(16, 16, W - 16, H - 16, None, TINTA, 4)
    h.texto((W / 2 + 26, 62), "EL BARQUERO", "cartel", 34, TINTA)
    h.poli([(110, 470), (520, 470), (470, 560), (160, 560)], MADERA, TINTA, 4)
    h.linea([(80, 520), (550, 520)], (40, 90, 150), 6)
    h.texto((W / 2, 640), f"«Con más de {romano(ba['maximo'])} pesas,", "texto2", 28, TINTA)
    h.texto((W / 2, 680), "mi barca se va al fondo.»", "texto2", 28, TINTA)
    return h.final()


def tablilla_lucrecia():
    h = tablilla("TABLILLA DE LUCRECIA", None, (232, 216, 176))
    versos = ["«Que no se quede atrás", "lo que más vale.", "Lo demás, que lo cubra", "la ceniza.»"]
    for k, v in enumerate(versos):
        h.texto((W / 2, 260 + k * 64), v, "texto2", 32, TINTA)
    return h.final()


# ================================================================== imágenes de los minijuegos
def ui(carpeta, I):
    d = os.path.join(carpeta, "img", "ui")
    os.makedirs(d, exist_ok=True)
    for f in I["laberinto"]["todas"]:
        h = Hoja(140, 140, (30, 60, 110))
        h.disco(70, 70, 66, (30, 60, 110), ORO, 4)
        figura(h, f, 70, 70, 44, (236, 220, 170), (30, 60, 110))
        h.final().save(os.path.join(d, f"fig-{f}.png"))
    for an in I["sello"]["anillos"]:
        anillo_png(an, os.path.join(d, f"anillo-{an['id']}.png"))
    for cosa in I["barca"]["carga"]:
        h = Hoja(120, 120, (255, 0, 255))
        if cosa.startswith("anfora"):
            anfora_peq(h, 60, 60, 3, (190, 170, 70) if "aceite" in cosa else (130, 30, 50))
        elif cosa == "fardo_lana":
            h.elip(20, 40, 100, 100, (240, 236, 220), TINTA, 3)
        elif cosa == "cofre_monedas":
            h.rect(20, 50, 100, 100, MADERA, TINTA, 3)
            for k in range(5):
                h.disco(32 + k * 14, 46, 8, ORO, TINTA, 1)
        elif cosa == "estatua_lar":
            h.disco(60, 34, 14, (160, 120, 60), TINTA, 2)
            h.rect(46, 48, 74, 100, (160, 120, 60), TINTA, 2)
        else:
            h.elip(24, 40, 96, 104, (210, 170, 90), TINTA, 3)
        im = h.final()
        a = np.asarray(im).astype(np.int16)
        alfa = np.clip(np.abs(a - np.array((255, 0, 255))).sum(axis=2) * 3, 0, 255).astype(np.uint8)
        Image.fromarray(np.dstack([np.asarray(im), alfa])).save(os.path.join(d, f"carga-{cosa}.png"))


DATOS = {
    "13-panel.js": lambda I: {"todas": I["laberinto"]["todas"], "solucion": I["laberinto"]["solucion"]},
    "20-abaco.js": lambda I: {"total": I["cuentas"]["total"]},
    "28-anillos.js": lambda I: {"orden": I["sello"]["orden"], "solucion": I["sello"]["solucion"]},
    "33-compuertas.js": lambda I: {k: I["fuente"][k] for k in ("red", "orden", "caudal", "pide", "compuertas")},
    "40-tablilla.js": lambda I: {"solucion": I["sator"]["solucion"]},
    "46-statera.js": lambda I: {"muesca": I["statera"]["muesca"]},
    "55-calles.js": lambda I: {"filas": I["calles"]["filas"], "cols": I["calles"]["cols"], "solucion": I["calles"]["solucion"]},
    "59-calendario.js": lambda I: {"dia": I["calendario"]["dia"]},
    "66-huida.js": lambda I: {k: I["huida"][k] for k in ("calles", "cortadas", "limite")},
    "70-barca.js": lambda I: {k: I["barca"][k] for k in ("carga", "maximo", "solucion")},
}


def inyectar(carpeta, I):
    for js, f in DATOS.items():
        ruta = os.path.join(carpeta, "minijuegos", js)
        if not os.path.exists(ruta):
            continue
        s = open(ruta, encoding="utf-8").read()
        a, b = s.index("/*DATOS*/") + len("/*DATOS*/"), s.index("/*FIN*/")
        open(ruta, "w", encoding="utf-8", newline="\n").write(s[:a] + json.dumps(f(I), ensure_ascii=False, separators=(", ", ": ")) + s[b:])


MOSAICOS = {"atrio": ["16", "14", "17", "15"], "sello": ["27", "29"], "calendario": ["61", "63"]}


def main(carpeta="juegos/aventuras-ca/pompeya"):
    I = inst()
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    g = lambda k, im, s: ruido(im, s).save(os.path.join(arte, f"{k}.png"))
    for nombre, im, filas, cols in (("atrio", mosaico_laberinto(I["laberinto"]), 2, 2), ("sello", impronta(I["sello"]), 1, 2),
                                    ("calendario", calendario(I["calendario"]), 1, 2)):
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))          # el dibujo entero, para probar_mosaicos.py
        for pieza, k in zip(cortar(im, filas, cols), MOSAICOS[nombre]):
            pieza.save(os.path.join(arte, f"{k}.png"))
    g("18", acertijo_lucio(), 18)
    for d, k in enumerate(("21", "23", "24")):
        g(k, tablilla_cuentas(I["cuentas"], d), int(k))
    g("25", regla_escriba(), 25)
    g("36", acueducto(I["fuente"]), 36)
    g("37", plano_jardin(I["fuente"]), 37)
    g("41", muro_cuadrado(I["sator"]), 41)
    g("42", acertijo_sembrador(), 42)
    g("43", pesadas(I["statera"]), 43)
    g("45", recibo(I["statera"]), 45)
    for k, t in GRAFITIS.items():
        g(k, grafito(t, int(k)), int(k))
    g("54", plano_manzana(I["calles"]), 54)
    g("65", acertijo_plinio(I["calendario"]), 65)
    g("67", mapa_huida(I["huida"]), 67)
    g("75", vigia(I["huida"]), 75)
    g("71", manifiesto(I["barca"]), 71)
    g("72", barquero(I["barca"]), 72)
    g("76", tablilla_lucrecia(), 76)
    ui(carpeta, I)
    inyectar(carpeta, I)
    print("láminas de Pompeya escritas en", arte)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

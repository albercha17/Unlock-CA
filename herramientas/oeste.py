"""Láminas del Lejano Oeste para «Dry Gulch, 1878: El Tren del Oro» (cartas que se juntan en fila, en columna y en cuadrícula).

Igual que mosaicos.py y pixeles.py, todo se dibuja por código y se corta en las piezas que son las ilustraciones de las cartas, así que los códigos
de los puzles son exactos y se guardan en herramientas/codigos_oeste.json (los leen los solucionadores):
  - tren:   5 cartas EN FILA (3150x882): cinco vagones con enganches de símbolos; solo hay un orden en que los enganches coinciden y las letras
            pintadas en los vagones, leídas de atrás hacia delante, dicen TEXAS.
  - cartel: 3 cartas EN COLUMNA (630x2646): el retrato de «Se busca»; cada rasgo (sombrero, cicatriz, bigote) está en una carta distinta.
  - mapa:   4 cartas 2x2: camino con tres hitos y rayitas contadas en grupos de cinco (14, 7 y 29) que cruzan las juntas entre cartas.
  - cartas sueltas: 36 (libro del sheriff con los seis sospechosos), 52 (reloj del capataz) y 70 (informe del orfebre).
Uso (desde la raíz del repo):  python herramientas/oeste.py [carpeta_juego]
"""
import json
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mosaicos import cortar  # noqa: E402

S = 2                                   # supersampling para que el dibujo salga suave
PAPEL = (236, 214, 168)
TINTA = (54, 36, 24)
ROJO = (170, 52, 40)
OCRE = (214, 160, 70)
ARENA = (224, 186, 124)
ARENA2 = (198, 154, 98)
MADERA = (146, 94, 58)
MADERA2 = (110, 72, 44)
HIERRO = (86, 88, 96)
NEGRO = (38, 32, 30)
BLANCO = (248, 242, 226)
PIEL = (216, 172, 126)
SOMBRERO = (96, 66, 42)

FUENTES = {"cartel": "C:/Windows/Fonts/impact.ttf", "texto": "C:/Windows/Fonts/georgiab.ttf", "texto2": "C:/Windows/Fonts/georgia.ttf"}
_cache = {}


def fuente(nombre, tam):
    k = (nombre, tam)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(FUENTES[nombre], int(tam * S))
    return _cache[k]


class Hoja:
    def __init__(self, w, h, fondo=PAPEL):
        self.w, self.h = w, h
        self.im = Image.new("RGB", (w * S, h * S), fondo)
        self.d = ImageDraw.Draw(self.im)

    def _p(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def poli(self, pts, fill, borde=None, ancho=3):
        self.d.polygon(self._p(pts), fill=fill)
        if borde:
            self.d.line(self._p(list(pts) + [pts[0]]), fill=borde, width=int(ancho * S), joint="curve")

    def rect(self, x0, y0, x1, y1, fill, borde=None, ancho=3):
        self.d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill, outline=borde, width=int(ancho * S) if borde else 0)

    def elip(self, x0, y0, x1, y1, fill, borde=None, ancho=3):
        self.d.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill, outline=borde, width=int(ancho * S) if borde else 0)

    def disco(self, cx, cy, r, fill, borde=None, ancho=3):
        self.elip(cx - r, cy - r, cx + r, cy + r, fill, borde, ancho)

    def linea(self, pts, color, ancho):
        self.d.line(self._p(pts), fill=color, width=int(ancho * S), joint="curve")

    def texto(self, xy, s, tipo, tam, color, ancla="mm", borde=None, ancho_borde=0):
        self.d.text((xy[0] * S, xy[1] * S), s, font=fuente(tipo, tam), fill=color, anchor=ancla,
                    stroke_width=int(ancho_borde * S), stroke_fill=borde)

    def degradado(self, y0, y1, c0, c1):
        for y in range(int(y0), int(y1)):
            t = (y - y0) / max(1, (y1 - y0 - 1))
            c = tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))
            self.d.rectangle([0, y * S, self.w * S, (y + 1) * S], fill=c)

    def final(self, ruido=0, semilla=1):
        im = self.im.resize((self.w, self.h), Image.LANCZOS)
        if ruido:
            a = np.asarray(im).astype(np.int16)
            rng = np.random.default_rng(semilla)
            a = a + rng.normal(0, ruido, a.shape[:2])[:, :, None]
            im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
        return im


def simbolo(h, nombre, cx, cy, r, col, borde=TINTA):
    if nombre == "circulo":
        h.disco(cx, cy, r, col, borde, 4)
    elif nombre == "cuadrado":
        h.rect(cx - r * 0.85, cy - r * 0.85, cx + r * 0.85, cy + r * 0.85, col, borde, 4)
    elif nombre == "triangulo":
        h.poli([(cx, cy - r), (cx + r * 1.05, cy + r * 0.8), (cx - r * 1.05, cy + r * 0.8)], col, borde, 4)
    elif nombre == "rombo":
        h.poli([(cx, cy - r * 1.1), (cx + r * 0.85, cy), (cx, cy + r * 1.1), (cx - r * 0.85, cy)], col, borde, 4)
    elif nombre == "estrella":
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rad = r * (1.15 if i % 2 == 0 else 0.5)
            pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
        h.poli(pts, col, borde, 4)
    elif nombre == "cruz":
        a = r * 0.36
        h.poli([(cx - a, cy - r), (cx + a, cy - r), (cx + a, cy - a), (cx + r, cy - a), (cx + r, cy + a), (cx + a, cy + a), (cx + a, cy + r),
                (cx - a, cy + r), (cx - a, cy + a), (cx - r, cy + a), (cx - r, cy - a), (cx - a, cy - a)], col, borde, 4)


# ------------------------------------------------------------------ códigos
SOSPECHOSOS = [
    {"nombre": "Pete Cuchillo", "sombrero": "ancho", "cicatriz": "izq", "bigote": "manillar"},
    {"nombre": "Jack Botas", "sombrero": "alto", "cicatriz": "izq", "bigote": "manillar"},
    {"nombre": "Slim Sombra", "sombrero": "ancho", "cicatriz": "der", "bigote": "manillar"},
    {"nombre": "Doc Pólvora", "sombrero": "ancho", "cicatriz": "izq", "bigote": "grueso"},
    {"nombre": "La Zorra Roja", "sombrero": "bombin", "cicatriz": "ninguna", "bigote": "perilla"},
    {"nombre": "Tom Barro", "sombrero": "alto", "cicatriz": "der", "bigote": "grueso"},
]
JUNTAS = [("triangulo", (70, 150, 84)), ("estrella", (240, 196, 60)), ("cuadrado", (70, 110, 190)), ("rombo", (196, 60, 52))]
CODIGOS = {
    "tren": {"palabra": "TEXAS"},
    "cartel": {"sospechoso": SOSPECHOSOS[0]["nombre"], "sospechosos": [s["nombre"] for s in SOSPECHOSOS]},
    "mapa": {"combinacion": [14, 7, 29], "giros": ["derecha", "izquierda", "derecha"]},
    "mechas": {"minutos": 45},
}


# ------------------------------------------------------------------ el tren (5 cartas en fila: 3150 x 882)
def _ruedas(h, x0, ys, pos, r=32):
    for dx in pos:
        h.disco(x0 + dx, ys, r, NEGRO)
        h.disco(x0 + dx, ys, r * 0.55, HIERRO)
        h.disco(x0 + dx, ys, r * 0.15, NEGRO)


def _letra(h, x, y, letra, tam=170):
    h.texto((x, y), letra, "cartel", tam, BLANCO, "mm", TINTA, 5)


def _enganche(h, x0, y, lado, simb):
    """Barra de enganche que llega hasta el borde de la carta; lleva un disco con un símbolo si el extremo se une a otro vagón."""
    if lado == "izq":
        h.rect(x0, y - 9, x0 + 78, y + 9, HIERRO, TINTA, 3)
        if simb:
            cx = x0 + 34
    else:
        h.rect(x0 + 552, y - 9, x0 + 630, y + 9, HIERRO, TINTA, 3)
        if simb:
            cx = x0 + 596
    if simb:
        nombre, col = simb
        h.disco(cx, y, 36, BLANCO, TINTA, 4)
        simbolo(h, nombre, cx, y + (3 if nombre == "triangulo" else 0), 22, col)


def _vagon(h, i, x0):
    y_base = 748
    h.rect(x0 + 70, 700, x0 + 560, 722, NEGRO)
    if i == 0:                                    # furgón de cola
        h.rect(x0 + 90, 470, x0 + 540, 700, (156, 50, 40), TINTA, 4)
        for k in range(1, 15):
            h.linea([(x0 + 90 + k * 30, 470), (x0 + 90 + k * 30, 700)], (120, 36, 30), 2)
        h.rect(x0 + 80, 452, x0 + 550, 474, (96, 30, 26), TINTA, 4)
        h.rect(x0 + 240, 396, x0 + 392, 454, (156, 50, 40), TINTA, 4)
        h.rect(x0 + 262, 414, x0 + 370, 440, (250, 224, 150), TINTA, 3)
        for a in (130, 420):
            h.rect(x0 + a, 500, x0 + a + 70, 566, (250, 224, 150), TINTA, 3)
        h.rect(x0 + 70, 640, x0 + 94, 700, MADERA2, TINTA, 3)
        _letra(h, x0 + 315, 620, "T")
    elif i == 1:                                  # vagón de ganado
        h.rect(x0 + 80, 450, x0 + 550, 700, MADERA, TINTA, 4)
        for k in range(0, 9):
            h.rect(x0 + 108 + k * 50, 478, x0 + 124 + k * 50, 672, NEGRO)
        h.rect(x0 + 70, 436, x0 + 560, 458, MADERA2, TINTA, 4)
        h.linea([(x0 + 80, 575), (x0 + 550, 575)], MADERA2, 14)
        h.rect(x0 + 230, 535, x0 + 400, 650, MADERA, None)
        _letra(h, x0 + 315, 595, "E")
    elif i == 2:                                  # vagón cerrado
        h.rect(x0 + 80, 440, x0 + 550, 700, (104, 120, 76), TINTA, 4)
        for k in range(1, 16):
            h.linea([(x0 + 80 + k * 30, 440), (x0 + 80 + k * 30, 700)], (84, 98, 60), 2)
        h.rect(x0 + 70, 426, x0 + 560, 448, (70, 82, 52), TINTA, 4)
        h.rect(x0 + 180, 476, x0 + 450, 690, (118, 136, 86), TINTA, 4)
        h.linea([(x0 + 180, 690), (x0 + 450, 476)], (84, 98, 60), 6)
        h.rect(x0 + 440, 560, x0 + 456, 610, HIERRO, TINTA, 2)
        _letra(h, x0 + 315, 590, "X")
    elif i == 3:                                  # carbonero
        h.poli([(x0 + 90, 520), (x0 + 540, 520), (x0 + 520, 700), (x0 + 110, 700)], HIERRO, TINTA, 4)
        h.poli([(x0 + 100, 524), (x0 + 150, 470), (x0 + 230, 492), (x0 + 310, 450), (x0 + 400, 488), (x0 + 470, 462), (x0 + 535, 524)], NEGRO, TINTA, 3)
        for k in range(1, 6):
            h.linea([(x0 + 90 + k * 75, 524), (x0 + 108 + k * 70, 700)], (66, 68, 76), 3)
        _letra(h, x0 + 315, 622, "A")
    else:                                         # locomotora
        h.rect(x0 + 250, 520, x0 + 560, 660, NEGRO, TINTA, 4)
        h.elip(x0 + 520, 520, x0 + 604, 660, NEGRO, TINTA, 4)
        h.poli([(x0 + 462, 520), (x0 + 480, 436), (x0 + 520, 436), (x0 + 540, 520)], NEGRO, TINTA, 4)
        h.poli([(x0 + 452, 436), (x0 + 548, 436), (x0 + 536, 408), (x0 + 464, 408)], HIERRO, TINTA, 4)
        h.elip(x0 + 340, 480, x0 + 420, 534, (214, 160, 56), TINTA, 4)
        h.rect(x0 + 70, 424, x0 + 262, 700, (140, 40, 34), TINTA, 4)
        h.rect(x0 + 56, 408, x0 + 276, 432, NEGRO, TINTA, 4)
        h.rect(x0 + 100, 470, x0 + 176, 540, (250, 224, 150), TINTA, 3)
        h.linea([(x0 + 262, 640), (x0 + 600, 640)], (214, 160, 56), 8)
        _letra(h, x0 + 166, 625, "S", 150)
        for dx, r in ((190, 60), (320, 60), (440, 34), (520, 34)):
            h.disco(x0 + dx, 740 if r > 40 else y_base, r, NEGRO)
            h.disco(x0 + dx, 740 if r > 40 else y_base, r * 0.55, (170, 52, 40) if r > 40 else HIERRO)
            h.disco(x0 + dx, 740 if r > 40 else y_base, r * 0.14, NEGRO)
    if i != 4:
        _ruedas(h, x0, y_base, (170, 250, 390, 470))
    # enganches: el de la izquierda y el de la derecha llevan símbolo si se unen con otro vagón
    _enganche(h, x0, 690, "izq", JUNTAS[i - 1] if i > 0 else None)
    _enganche(h, x0, 690, "der", JUNTAS[i] if i < 4 else None)


def lamina_tren():
    h = Hoja(3150, 882)
    h.degradado(0, 560, (112, 164, 200), (246, 208, 144))
    h.disco(2380, 430, 120, (255, 232, 168))
    h.disco(2380, 430, 80, (255, 244, 206))
    h.rect(0, 556, 3150, 882, ARENA)
    h.rect(0, 556, 3150, 570, ARENA2)
    rng = random.Random(7)
    for x in range(-60, 3150, 260):                # mesetas lejanas
        a = rng.randint(70, 140)
        h.poli([(x, 560), (x + 30, 560 - a), (x + 170, 560 - a), (x + 210, 560)], (178, 112, 82))
    for k in range(0, 3150, 46):                    # traviesas y raíles
        h.rect(k, 786, k + 28, 806, MADERA2)
    h.rect(0, 772, 3150, 784, (116, 116, 126), TINTA, 2)
    for i in range(5):
        _vagon(h, i, i * 630)
    return h.final(ruido=3)


# ------------------------------------------------------------------ el cartel de «Se busca» (3 cartas en columna: 630 x 2646)
def _x(cx, k, x):
    return cx + k * (x - 315)


def sombrero(h, estilo, cx, by, k):
    """Sombrero con el borde en la línea `by` y la escala k (1 = cartel, 0.2 = icono)."""
    X = lambda x: cx + k * (x - 315)
    Y = lambda y: by + k * (y - 640)
    ink = max(2, 4 * k)
    if estilo == "ancho":
        h.rect(X(190), Y(470), X(440), Y(640), SOMBRERO, TINTA, ink)
        h.elip(X(190), Y(440), X(440), Y(500), SOMBRERO, TINTA, ink)
        h.elip(X(-15), Y(594), X(645), Y(690), SOMBRERO, TINTA, ink)
        h.rect(X(190), Y(596), X(440), Y(632), (58, 38, 24))
    elif estilo == "alto":
        h.poli([(X(205), Y(640)), (X(228), Y(420)), (X(270), Y(392)), (X(315), Y(430)), (X(360), Y(392)), (X(402), Y(420)), (X(425), Y(640))], SOMBRERO, TINTA, ink)
        h.poli([(X(10), Y(630)), (X(70), Y(660)), (X(315), Y(676)), (X(560), Y(660)), (X(620), Y(630)), (X(560), Y(600)), (X(70), Y(600))], SOMBRERO, TINTA, ink)
        h.rect(X(212), Y(580), X(418), Y(612), (58, 38, 24))
    else:                                           # bombín
        h.elip(X(135), Y(420), X(495), Y(660), SOMBRERO, TINTA, ink)
        h.elip(X(75), Y(606), X(555), Y(676), SOMBRERO, TINTA, ink)
        h.rect(X(150), Y(590), X(480), Y(626), (58, 38, 24))


def cicatriz(h, lado, cx, cy, k):
    X = lambda x: cx + k * (x - 315)
    Y = lambda y: cy + k * (y - 1200)
    if lado == "ninguna":
        return
    s = -1 if lado == "izq" else 1
    p = [(315 + s * 105, 1110), (315 + s * 70, 1300)]
    h.linea([(X(p[0][0]), Y(p[0][1])), (X(p[1][0]), Y(p[1][1]))], (140, 44, 36), max(3, 12 * k))
    for t in (0.2, 0.45, 0.7):
        px = p[0][0] + (p[1][0] - p[0][0]) * t
        py = p[0][1] + (p[1][1] - p[0][1]) * t
        h.linea([(X(px - 26), Y(py - 8)), (X(px + 26), Y(py + 8))], (140, 44, 36), max(2, 8 * k))


def bigote(h, estilo, cx, cy, k):
    X = lambda x: cx + k * (x - 315)
    Y = lambda y: cy + k * (y - 1900)
    oscuro = (60, 40, 28)
    if estilo == "manillar":
        h.elip(X(185), Y(1802), X(445), Y(1862), oscuro, None)
        for s in (-1, 1):
            pts = [(315 + s * 120, 1832), (315 + s * 175, 1826), (315 + s * 200, 1790), (315 + s * 178, 1760), (315 + s * 150, 1776)]
            h.linea([(X(x), Y(y)) for x, y in pts], oscuro, max(3, 26 * k))
    elif estilo == "grueso":
        h.poli([(X(170), Y(1800)), (X(460), Y(1800)), (X(488), Y(1856)), (X(315), Y(1880)), (X(142), Y(1856))], oscuro, None)
    else:                                           # perilla: bigote fino y barba en la barbilla
        h.poli([(X(215), Y(1814)), (X(415), Y(1814)), (X(395), Y(1840)), (X(235), Y(1840))], oscuro, None)
        h.poli([(X(262), Y(1980)), (X(368), Y(1980)), (X(332), Y(2120)), (X(298), Y(2120))], oscuro, None)


def lamina_cartel(sospechoso=None):
    s = sospechoso or SOSPECHOSOS[0]
    h = Hoja(630, 2646)
    h.rect(28, 28, 602, 2618, PAPEL, TINTA, 6)
    h.rect(46, 46, 584, 2600, PAPEL, TINTA, 2)
    h.texto((315, 150), "SE BUSCA", "cartel", 128, TINTA)
    h.texto((315, 300), "POR ASALTAR EL TREN", "texto", 38, TINTA)
    cx = 315
    h.rect(255, 2050, 375, 2330, PIEL, TINTA, 4)                                  # cuello
    h.poli([(40, 2646), (110, 2330), (520, 2330), (590, 2646)], (96, 90, 82), TINTA, 4)   # hombros
    h.poli([(215, 2300), (415, 2300), (315, 2450)], (170, 52, 40), TINTA, 4)             # pañuelo
    h.elip(cx - 60 - 250, 1180, cx - 250 + 40, 1400, PIEL, TINTA, 4)             # orejas
    h.elip(cx + 250 - 40, 1180, cx + 250 + 60, 1400, PIEL, TINTA, 4)
    h.elip(cx - 250, 520, cx + 250, 2140, PIEL, TINTA, 5)                         # cara
    for ex in (-90, 90):                                                           # ojos y cejas
        h.elip(cx + ex - 38, 975, cx + ex + 38, 1030, BLANCO, TINTA, 3)
        h.disco(cx + ex + (6 if ex > 0 else -6), 1002, 14, TINTA)
        h.linea([(cx + ex - 52 * (1 if ex < 0 else -1), 930 + (0 if ex < 0 else 26) ), (cx + ex + 44 * (1 if ex < 0 else -1), 956 - (0 if ex < 0 else 26) + 26)], TINTA, 14)
    h.poli([(cx, 1030), (cx - 36, 1240), (cx + 36, 1240)], (194, 146, 102), TINTA, 3)  # nariz
    cicatriz(h, s["cicatriz"], cx, 1200, 1)
    h.linea([(cx - 60, 1960), (cx + 60, 1960)], TINTA, 7)                          # boca
    bigote(h, s["bigote"], cx, 1900, 1)
    sombrero(h, s["sombrero"], cx, 640, 1)
    h.texto((315, 2490), "$500", "cartel", 130, ROJO)
    h.texto((315, 2578), "VIVO O MUERTO", "texto", 36, TINTA)
    return h.final(ruido=4, semilla=3)


def carta_libro():
    """Carta 36: el libro del sheriff con los seis sospechosos (sombrero, cicatriz, bigote y nombre)."""
    h = Hoja(630, 882)
    h.rect(24, 24, 606, 858, (206, 172, 120), TINTA, 6)
    h.rect(40, 40, 590, 842, PAPEL, TINTA, 2)
    h.texto((315, 92), "LIBRO DEL SHERIFF", "cartel", 62, TINTA)
    for i, s in enumerate(SOSPECHOSOS):
        y = 130 + i * 118
        h.rect(58, y, 572, y + 104, (226, 200, 150), TINTA, 2)
        for j, tipo in enumerate(("sombrero", "cicatriz", "bigote")):
            cx = 104 + j * 84
            h.disco(cx, y + 56, 32, PIEL, TINTA, 3)
            if tipo == "sombrero":
                sombrero(h, s["sombrero"], cx, y + 44, 0.12)
            elif tipo == "cicatriz":
                cicatriz(h, s["cicatriz"], cx, y + 54, 0.2)
            else:
                bigote(h, s["bigote"], cx, y + 54, 0.17)
        h.texto((340, y + 52), s["nombre"], "texto", 27, TINTA, "lm")
    return h.final(ruido=4, semilla=5)


# ------------------------------------------------------------------ el mapa del arroyo seco (4 cartas 2x2: 1260 x 1764)
def _rayitas(h, x, y, n):
    """n rayitas en grupos de cinco (cuatro verticales y una cruzada)."""
    for g in range((n + 4) // 5):
        cuantas = min(5, n - g * 5)
        gx = x + (g % 3) * 96
        gy = y + (g // 3) * 84
        for k in range(min(cuantas, 4)):
            h.linea([(gx + k * 16, gy), (gx + k * 16, gy + 62)], TINTA, 7)
        if cuantas == 5:
            h.linea([(gx - 10, gy + 52), (gx + 70, gy + 10)], TINTA, 7)


def _discontinua(h, pts, col, ancho, trazo=28, hueco=20):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        n = int(L // (trazo + hueco)) + 1
        for k in range(n):
            a = k * (trazo + hueco) / L
            b = min(1, (k * (trazo + hueco) + trazo) / L)
            h.linea([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)], col, ancho)


def _flecha(h, x0, y0, x1, y1, col):
    a = math.atan2(y1 - y0, x1 - x0)
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    p = [(mx + 26 * math.cos(a), my + 26 * math.sin(a)), (mx + 26 * math.cos(a + 2.5), my + 26 * math.sin(a + 2.5)), (mx + 26 * math.cos(a - 2.5), my + 26 * math.sin(a - 2.5))]
    h.poli(p, col)


def lamina_mapa():
    h = Hoja(1260, 1764)
    h.rect(0, 0, 1260, 1764, (120, 82, 50))
    h.rect(30, 30, 1230, 1734, PAPEL)
    rng = random.Random(11)
    for _ in range(90):                                       # manchas del papel
        x, y, r = rng.randint(60, 1200), rng.randint(60, 1700), rng.randint(10, 46)
        h.disco(x, y, r, (228, 204, 154))
    for k in range(40):
        h.disco(rng.randint(0, 1260), rng.choice([rng.randint(0, 40), rng.randint(1724, 1764)]), rng.randint(18, 40), (110, 72, 44))
    hoguera, roca, cactus, cala = (240, 1560), (430, 1030), (640, 860), (960, 400)
    ruta = [hoguera, roca, cactus, cala]
    _discontinua(h, ruta, (150, 60, 44), 8)
    for (a, b) in zip(ruta, ruta[1:]):
        _flecha(h, a[0], a[1], b[0], b[1], (150, 60, 44))
    # hoguera
    h.poli([(hoguera[0] - 44, hoguera[1] + 30), (hoguera[0] + 44, hoguera[1] - 4)], TINTA)
    h.linea([(hoguera[0] - 46, hoguera[1] + 34), (hoguera[0] + 46, hoguera[1] - 6)], MADERA2, 14)
    h.linea([(hoguera[0] - 46, hoguera[1] - 6), (hoguera[0] + 46, hoguera[1] + 34)], MADERA2, 14)
    h.poli([(hoguera[0], hoguera[1] - 84), (hoguera[0] + 34, hoguera[1] - 10), (hoguera[0] - 34, hoguera[1] - 10)], (226, 110, 38), TINTA, 3)
    h.poli([(hoguera[0], hoguera[1] - 50), (hoguera[0] + 16, hoguera[1] - 10), (hoguera[0] - 16, hoguera[1] - 10)], (250, 210, 80))
    h.texto((hoguera[0], hoguera[1] + 80), "SALIDA", "texto", 30, TINTA)
    # roca
    rx, ry = roca
    h.poli([(rx - 90, ry + 50), (rx - 60, ry - 40), (rx - 10, ry - 70), (rx + 50, ry - 50), (rx + 90, ry + 50)], (150, 132, 118), TINTA, 4)
    h.poli([(rx - 20, ry + 50), (rx + 10, ry - 10), (rx + 40, ry - 30), (rx + 90, ry + 50)], (128, 112, 100), TINTA, 3)
    # cactus (a caballo entre las cuatro cartas)
    kx, ky = cactus
    h.rect(kx - 22, ky - 120, kx + 22, ky + 70, (84, 130, 70), TINTA, 4)
    h.rect(kx - 80, ky - 60, kx - 22, ky - 30, (84, 130, 70), TINTA, 4)
    h.rect(kx - 80, ky - 100, kx - 52, ky - 30, (84, 130, 70), TINTA, 4)
    h.rect(kx + 22, ky - 20, kx + 80, ky + 8, (84, 130, 70), TINTA, 4)
    h.rect(kx + 52, ky - 60, kx + 80, ky + 8, (84, 130, 70), TINTA, 4)
    # calavera de vaca
    cx, cy = cala
    h.elip(cx - 62, cy - 52, cx + 62, cy + 40, BLANCO, TINTA, 4)
    h.poli([(cx - 40, cy + 30), (cx + 40, cy + 30), (cx + 30, cy + 90), (cx - 30, cy + 90)], BLANCO, TINTA, 4)
    h.disco(cx - 24, cy - 8, 14, TINTA)
    h.disco(cx + 24, cy - 8, 14, TINTA)
    h.poli([(cx - 62, cy - 30), (cx - 130, cy - 70), (cx - 112, cy - 20)], BLANCO, TINTA, 3)
    h.poli([(cx + 62, cy - 30), (cx + 130, cy - 70), (cx + 112, cy - 20)], BLANCO, TINTA, 3)
    # rayitas contadas en grupos de cinco, debajo de cada hito
    n1, n2, n3 = CODIGOS["mapa"]["combinacion"]
    _rayitas(h, rx - 130, ry + 140, n1)
    _rayitas(h, kx + 120, ky - 40, n2)
    _rayitas(h, cx - 130, cy + 150, n3)
    # rosa de los vientos y título
    rx0, ry0 = 1090, 1560
    h.poli([(rx0, ry0 - 110), (rx0 + 22, ry0), (rx0, ry0 + 110), (rx0 - 22, ry0)], TINTA)
    h.poli([(rx0 - 110, ry0), (rx0, ry0 - 22), (rx0 + 110, ry0), (rx0, ry0 + 22)], (150, 60, 44))
    h.texto((rx0, ry0 - 138), "N", "cartel", 44, TINTA)
    h.texto((150, 120), "ARROYO SECO", "cartel", 76, TINTA, "lm")
    return h.final(ruido=5, semilla=9)


# ------------------------------------------------------------------ cartas sueltas
def carta_reloj():
    """Carta 52: el reloj del capataz; la aguja marca los minutos que tiene que esperar la dinamita."""
    h = Hoja(630, 882)
    h.rect(0, 0, 630, 882, MADERA)
    rng = random.Random(3)
    for k in range(0, 882, 14):
        h.linea([(0, k), (630, k + rng.randint(-3, 3))], MADERA2, 2)
    h.rect(24, 24, 606, 858, None or MADERA, TINTA, 6)
    h.texto((315, 92), "EL RELOJ DEL CAPATAZ", "texto", 38, BLANCO, "mm", TINTA, 3)
    cx, cy, R = 315, 440, 250
    h.disco(cx, cy, R + 22, (196, 150, 56), TINTA, 6)
    h.disco(cx, cy, R, BLANCO, TINTA, 5)
    for m in range(60):
        a = math.radians(m * 6 - 90)
        r0 = R - (40 if m % 5 == 0 else 22)
        h.linea([(cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + (R - 8) * math.cos(a), cy + (R - 8) * math.sin(a))], TINTA, 7 if m % 5 == 0 else 3)
    for m, t in ((0, "60"), (15, "15"), (30, "30"), (45, "45")):
        a = math.radians(m * 6 - 90)
        h.texto((cx + (R - 84) * math.cos(a), cy + (R - 84) * math.sin(a)), t, "cartel", 46, TINTA)
    minutos = CODIGOS["mechas"]["minutos"]
    a = math.radians(minutos * 6 - 90)
    h.linea([(cx, cy), (cx + 118 * math.cos(a), cy + 118 * math.sin(a))], ROJO, 14)
    h.poli([(cx + 150 * math.cos(a), cy + 150 * math.sin(a)), (cx + 100 * math.cos(a + 0.18), cy + 100 * math.sin(a + 0.18)), (cx + 100 * math.cos(a - 0.18), cy + 100 * math.sin(a - 0.18))], ROJO)
    h.disco(cx, cy, 20, ROJO, TINTA, 3)
    h.rect(286, 136, 344, 166, (196, 150, 56), TINTA, 4)
    h.texto((315, 770), "La dinamita debe saltar", "texto2", 36, BLANCO, "mm", TINTA, 2)
    h.texto((315, 818), "cuando la aguja llegue aquí", "texto2", 36, BLANCO, "mm", TINTA, 2)
    return h.final(ruido=4, semilla=2)


def carta_informe():
    """Carta 70: el informe del orfebre sobre las nueve barras de oro."""
    h = Hoja(630, 882)
    h.rect(24, 24, 606, 858, (206, 172, 120), TINTA, 6)
    h.rect(40, 40, 590, 842, PAPEL, TINTA, 2)
    h.texto((315, 96), "INFORME DEL ORFEBRE", "cartel", 56, TINTA)
    for i in range(9):
        x = 110 + (i % 3) * 144
        y = 190 + (i // 3) * 96
        h.poli([(x, y + 62), (x + 22, y), (x + 100, y), (x + 122, y + 62)], (236, 190, 56), TINTA, 4)
        h.poli([(x + 22, y), (x + 100, y), (x + 92, y + 16), (x + 30, y + 16)], (255, 226, 120), None)
    h.texto((315, 520), "Nueve barras de oro.", "texto", 36, TINTA)
    h.texto((315, 570), "Una de ellas es FALSA:", "texto", 36, TINTA)
    h.texto((315, 620), "pesa MENOS que las otras.", "texto", 36, ROJO)
    h.texto((315, 700), "La balanza solo se puede", "texto", 36, TINTA)
    h.texto((315, 750), "usar DOS veces.", "texto", 36, TINTA)
    h.linea([(150, 800), (480, 800)], TINTA, 3)
    return h.final(ruido=4, semilla=4)


# ------------------------------------------------------------------ registro y salida
# nombre -> (función, [ids de las piezas en orden de lectura: izq→dcha, arriba→abajo], filas, cols); los números no siguen el orden de lectura
MOSAICOS = {
    "tren": (lamina_tren, ["16", "18", "14", "17", "15"], 1, 5),
    "cartel": (lamina_cartel, ["31", "32", "30"], 3, 1),
    "mapa": (lamina_mapa, ["42", "40", "43", "41"], 2, 2),
}
SUELTAS = {"36": carta_libro, "52": carta_reloj, "70": carta_informe}


def main(carpeta="juegos/aventuras-ca/oeste"):
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    for nombre, (fn, ids, filas, cols) in MOSAICOS.items():
        im = fn()
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))
        for pieza, i in zip(cortar(im, filas, cols), ids):
            pieza.save(os.path.join(arte, f"{i}.png"))
        print(f"{nombre}: {len(ids)} piezas {', '.join(ids)}")
    for i, fn in SUELTAS.items():
        fn().save(os.path.join(arte, f"{i}.png"))
        print(f"carta suelta {i}")
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "codigos_oeste.json")
    json.dump(CODIGOS, open(ruta, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print("códigos en", ruta)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

"""Láminas de «Mar de las Brumas, 1715» (piratas): CARTAS QUE SE PLIEGAN, como los «fold-in» de la revista MAD.

Una carta plegable se pliega en acordeón hasta que la línea A toque la B (y la C, la D): la franja de en medio queda escondida detrás y lo que
estaba a los dos lados se junta en un dibujo nuevo. Se dibuja primero la carta PLEGADA (la «composición»); después se abre metiendo las franjas,
que se rellenan con el fondo estirado y con señuelos (mitades falsas, pasos de más). Así, plegar la lámina devuelve la composición píxel a
píxel (se comprueba aquí mismo) y el Modo PC, que pliega la imagen con el campo `plegado` de cartas.json, enseña exactamente lo mismo.

  - carta 30: carta náutica; plegada, dos cifras de arrecifes dan el rumbo; desplegada, cada mitad forma otra cifra con su mitad falsa.
  - carta 76: testamento del capitán Calavera; plegado, cuatro símbolos en columna; desplegado, quimeras de dos símbolos.
  - carta 70: mapa de la isla, plegado por los dos lados; plegado, el camino de la palmera a la X; desplegado, el camino tiene pasos de más.
  - cartas sueltas: 31 (cuaderno del piloto: el desvío de la aguja), 40 (plano de estiba), 52 (ordenanza de la fragata) y 64 (carta celeste).
  - imágenes de la interfaz de los minijuegos (img/ui): La Gaviota, la fragata, símbolos de las losas, barril y rosa de los vientos.
Todo sale de herramientas/instancias_piratas.json. En arte/comprobar/ quedan las cartas plegadas para revisarlas a ojo.
Uso (desde la raíz del repo):  python herramientas/piratas.py [carpeta_juego]
"""
import json
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oeste import S, Hoja, fuente  # noqa: E402
from mosaicos import cortar  # noqa: E402


def _discontinua(h, pts, col, ancho, trazo=28, hueco=20):
    """Línea de trazos a lo largo de los puntos `pts`."""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        n = int(L // (trazo + hueco)) + 1
        for k in range(n):
            a = k * (trazo + hueco) / L
            b = min(1, (k * (trazo + hueco) + trazo) / L)
            h.linea([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)], col, ancho)

W, H = 630, 882
PERG = (236, 218, 174)
PERG2 = (214, 188, 136)
TINTA = (52, 36, 24)
ROJO = (172, 38, 32)
MAR = (58, 122, 146)
MAR2 = (30, 78, 104)
ARENA = (230, 200, 136)
ARENA2 = (206, 170, 104)
ROCA = (84, 74, 66)
ROCA2 = (132, 118, 102)
ESPUMA = (214, 236, 236)
ORO = (228, 180, 56)
ORO2 = (168, 120, 30)
HUESO = (234, 226, 204)
VERDE = (58, 116, 62)
VERDE2 = (36, 82, 42)
MADERA = (138, 92, 52)
MADERA2 = (98, 62, 34)
AZUL = (36, 76, 160)
AMARILLO = (240, 200, 40)
BLANCO = (248, 244, 232)
NEGRO = (26, 22, 20)


def _inst():
    return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_piratas.json"), encoding="utf-8"))


# ================================================================== pliegue
def expandir(bg, comp, xs=None, sv=0, ys=None, sh=0):
    """Abre la composición `comp` (la carta plegada) metiendo una franja de `sv` columnas en x = xs y otra de `sh` filas en y = ys.
    Las franjas se rellenan con la columna (fila) del pliegue de `bg` estirada. Devuelve la lámina y las máscaras de las franjas."""
    g, c = np.asarray(bg), np.asarray(comp)
    mx, my = np.arange(W), np.arange(H)
    tx, ty = np.zeros(W, bool), np.zeros(H, bool)
    if sv:
        tx = (mx >= xs) & (mx < xs + sv)
        mx = np.where(mx >= xs + sv, mx - sv, np.minimum(mx, xs))
    if sh:
        ty = (my >= ys) & (my < ys + sh)
        my = np.where(my >= ys + sh, my - sh, np.minimum(my, ys))
    full = c[my][:, mx].copy()
    fondo = g[my][:, mx]
    full[:, tx] = fondo[:, tx]
    full[ty, :] = fondo[ty, :]
    return Image.fromarray(full), tx, ty


def plegar(img, pl):
    """Lo que se ve con la carta plegada: se quitan las franjas escondidas (lo mismo que hace el Modo PC)."""
    a = np.asarray(img)
    keep_x = np.ones(a.shape[1], bool)
    keep_y = np.ones(a.shape[0], bool)
    if "x" in pl:
        keep_x[pl["x"][0]:pl["x"][1]] = False
    if "y" in pl:
        keep_y[pl["y"][0]:pl["y"][1]] = False
    return Image.fromarray(a[keep_y][:, keep_x])


def nueva(img):
    """Hoja cuyo lienzo es `img` (para seguir dibujando encima con suavizado)."""
    h = Hoja(img.width, img.height)
    h.im = img.resize((img.width * S, img.height * S), Image.LANCZOS)
    h.d = ImageDraw.Draw(h.im)
    return h


def carta_plegable(pl, fondo, objetos, extras, marcas, semilla):
    sv = pl["x"][1] - pl["x"][0] if "x" in pl else 0
    sh = pl["y"][1] - pl["y"][0] if "y" in pl else 0
    xs = pl["x"][0] if "x" in pl else None
    ys = pl["y"][0] if "y" in pl else None
    wc, hc = W - sv, H - sh
    hb = Hoja(wc, hc)
    fondo(hb, wc, hc)
    bg = hb.final()
    hf = Hoja(wc, hc)
    fondo(hf, wc, hc)
    objetos(hf, wc, hc)
    comp = hf.final()
    full, tx, ty = expandir(bg, comp, xs, sv, ys, sh)
    he = nueva(full)
    extras(he)
    a = np.asarray(he.final()).copy()
    keep = ~(tx[None, :] | ty[:, None])
    a[keep] = np.asarray(full)[keep]                      # lo que no es franja vuelve a ser exactamente la composición
    img = Image.fromarray(a)
    assert np.array_equal(np.asarray(plegar(img, pl)), np.asarray(comp)), "la lámina plegada no coincide con la composición"
    hm = nueva(img)
    marcas(hm)
    return ruido(hm.final(), semilla)


def ruido(im, semilla, fuerza=3):
    a = np.asarray(im).astype(np.int16)
    rng = np.random.default_rng(semilla)
    a = a + rng.normal(0, fuerza, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def linea_pliegue(h, x0, y0, x1, y1, letra1, letra2, pos1, pos2, col=TINTA):
    """Línea de puntos de un pliegue con su letra en los dos extremos."""
    _discontinua(h, [(x0, y0), (x1, y1)], col, 2, trazo=9, hueco=7)
    for letra, (lx, ly) in ((letra1, pos1), (letra2, pos2)):
        h.disco(lx, ly, 13, PERG, col, 2)
        h.texto((lx, ly + 1), letra, "texto", 17, col)


# ================================================================== dibujos comunes
def roca(h, cx, cy, r, rng, col=ROCA, luz=ROCA2):
    pts = []
    for k in range(8):
        a = k * math.pi / 4 + rng.uniform(-0.25, 0.25)
        rr = r * rng.uniform(0.75, 1.1)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    h.poli(pts, col, NEGRO, 2)
    h.disco(cx - r * 0.3, cy - r * 0.3, r * 0.32, luz)


def rocas_segmento(h, p0, p1, semilla, espuma=True):
    rng = random.Random(semilla)
    L = math.dist(p0, p1)
    n = max(2, int(L / 12))
    centros = [(p0[0] + (p1[0] - p0[0]) * k / n, p0[1] + (p1[1] - p0[1]) * k / n, rng.uniform(9, 12.5)) for k in range(n + 1)]
    if espuma:
        for cx, cy, r in centros:
            h.disco(cx, cy, r + 6, ESPUMA)
    for cx, cy, r in centros:
        roca(h, cx + rng.uniform(-2, 2), cy + rng.uniform(-2, 2), r, rng)


SEG = {"a": ((-1, 0), (1, 0)), "b": ((1, 0), (1, 1)), "c": ((1, 1), (1, 2)), "d": ((-1, 2), (1, 2)),
       "e": ((-1, 1), (-1, 2)), "f": ((-1, 0), (-1, 1)), "g": ((-1, 1), (1, 1))}
SEGMENTOS = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcdfg"}


def cifra_arrecife(h, xc, ytop, cifra, hw=52, alto=100, semilla=0):
    """Una cifra de siete segmentos hecha de arrecifes. Primero la espuma de todos los segmentos y luego las rocas."""
    segs = SEGMENTOS[cifra]
    tramos = [((xc + SEG[s][0][0] * hw, ytop + SEG[s][0][1] * alto), (xc + SEG[s][1][0] * hw, ytop + SEG[s][1][1] * alto)) for s in segs]
    for p0, p1 in tramos:
        L = math.dist(p0, p1)
        n = max(2, int(L / 12))
        for k in range(n + 1):
            h.disco(p0[0] + (p1[0] - p0[0]) * k / n, p0[1] + (p1[1] - p0[1]) * k / n, 18, ESPUMA)
    for i, (p0, p1) in enumerate(tramos):
        rocas_segmento(h, p0, p1, semilla * 100 + i, espuma=False)


def olas(h, x0, y0, x1, y1, semilla, n=14, col=(150, 196, 210)):
    rng = random.Random(semilla)
    for _ in range(n):
        x, y = rng.uniform(x0, x1 - 30), rng.uniform(y0, y1)
        h.linea([(x, y), (x + 8, y - 4), (x + 16, y), (x + 24, y - 4)], col, 2)


def rosa(h, cx, cy, r, col1=TINTA, col2=ROJO, fondo=PERG, norte=0.0):
    """Rosa de los vientos de 16 puntas; `norte` gira la rosa (grados, positivo = hacia el este)."""
    h.disco(cx, cy, r * 1.04, fondo, col1, 2)
    h.disco(cx, cy, r * 0.82, None or fondo, col1, 1)
    for k in range(16):
        a = math.radians(k * 22.5 + norte) - math.pi / 2
        largo = r * (0.98 if k % 4 == 0 else 0.7 if k % 2 == 0 else 0.5)
        ancho = r * (0.13 if k % 4 == 0 else 0.09)
        punta = (cx + largo * math.cos(a), cy + largo * math.sin(a))
        izq = (cx + ancho * math.cos(a - math.pi / 2), cy + ancho * math.sin(a - math.pi / 2))
        der = (cx + ancho * math.cos(a + math.pi / 2), cy + ancho * math.sin(a + math.pi / 2))
        h.poli([izq, punta, (cx, cy)], col2 if k % 4 == 0 else col1, col1, 1)
        h.poli([(cx, cy), punta, der], fondo, col1, 1)
    h.disco(cx, cy, r * 0.08, col2, col1, 1)
    a = math.radians(norte) - math.pi / 2
    h.texto((cx + r * 1.22 * math.cos(a), cy + r * 1.22 * math.sin(a)), "N", "texto", max(14, int(r * 0.32)), col1)


def palmera(h, x, y, k=1.0):
    tronco = [(x, y), (x + 4 * k, y - 18 * k), (x + 6 * k, y - 36 * k), (x + 4 * k, y - 52 * k)]
    h.linea(tronco, MADERA2, 7 * k)
    tx, ty = tronco[-1]
    for ang in (-160, -120, -60, -20, 30, 200):
        a = math.radians(ang)
        h.poli([(tx, ty), (tx + 30 * k * math.cos(a - 0.2), ty + 30 * k * math.sin(a - 0.2) + 6 * k),
                (tx + 34 * k * math.cos(a), ty + 34 * k * math.sin(a) + 10 * k), (tx + 26 * k * math.cos(a + 0.25), ty + 26 * k * math.sin(a + 0.25) + 8 * k)],
               VERDE, VERDE2, 2)
    h.disco(tx - 2 * k, ty + 4 * k, 4 * k, MADERA2)
    h.disco(tx + 4 * k, ty + 5 * k, 4 * k, MADERA2)


def arbusto(h, x, y, k=1.0):
    for dx, dy, r in ((-10, 0, 11), (8, -2, 12), (0, -10, 12)):
        h.disco(x + dx * k, y + dy * k, r * k, VERDE, VERDE2, 2)


def barco(h, x, y, k=1.0):
    h.poli([(x - 40 * k, y), (x + 40 * k, y), (x + 28 * k, y + 16 * k), (x - 30 * k, y + 16 * k)], MADERA, NEGRO, 2)
    h.linea([(x, y), (x, y - 60 * k)], NEGRO, 3)
    h.poli([(x - 2 * k, y - 56 * k), (x - 30 * k, y - 10 * k), (x - 2 * k, y - 8 * k)], BLANCO, NEGRO, 2)
    h.poli([(x + 3 * k, y - 50 * k), (x + 30 * k, y - 12 * k), (x + 3 * k, y - 10 * k)], BLANCO, NEGRO, 2)
    h.poli([(x, y - 60 * k), (x + 14 * k, y - 56 * k), (x, y - 52 * k)], NEGRO)


# ------------------------------------------------------------------ símbolos de las losas
def simbolo(h, nombre, cx, cy, r, col, hueco):
    t = r * 0.15
    if nombre == "estrella":
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rad = r * (0.95 if i % 2 == 0 else 0.4)
            pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
        h.poli(pts, col)
    elif nombre == "luna":
        h.disco(cx - r * 0.08, cy, r * 0.8, col)
        h.disco(cx + r * 0.3, cy - r * 0.12, r * 0.66, hueco)
    elif nombre == "calavera":
        h.disco(cx, cy - r * 0.18, r * 0.66, col)
        h.rect(cx - r * 0.38, cy + r * 0.2, cx + r * 0.38, cy + r * 0.72, col)
        h.disco(cx - r * 0.27, cy - r * 0.16, r * 0.19, hueco)
        h.disco(cx + r * 0.27, cy - r * 0.16, r * 0.19, hueco)
        h.poli([(cx, cy + r * 0.04), (cx - r * 0.09, cy + r * 0.22), (cx + r * 0.09, cy + r * 0.22)], hueco)
        for dx in (-0.19, 0, 0.19):
            h.linea([(cx + r * dx, cy + r * 0.44), (cx + r * dx, cy + r * 0.72)], hueco, max(2, r * 0.06))
    elif nombre == "ancla":
        h.elip(cx - r * 0.2, cy - r * 0.95, cx + r * 0.2, cy - r * 0.55, None, col, t * 0.8)
        h.linea([(cx, cy - r * 0.58), (cx, cy + r * 0.82)], col, t)
        h.linea([(cx - r * 0.45, cy - r * 0.36), (cx + r * 0.45, cy - r * 0.36)], col, t)
        pts = [(cx + r * 0.66 * math.cos(math.radians(a)), cy + r * 0.2 + r * 0.62 * math.sin(math.radians(a))) for a in range(10, 171, 10)]
        h.linea(pts, col, t)
        for (px, py), s in ((pts[0], 1), (pts[-1], -1)):
            h.poli([(px + s * r * 0.16, py - r * 0.02), (px - s * r * 0.06, py - r * 0.2), (px - s * r * 0.02, py + r * 0.06)], col)
    elif nombre == "llave":
        h.elip(cx - r * 0.32, cy - r * 0.92, cx + r * 0.32, cy - r * 0.28, None, col, t)
        h.linea([(cx, cy - r * 0.3), (cx, cy + r * 0.9)], col, t)
        h.rect(cx, cy + r * 0.48, cx + r * 0.36, cy + r * 0.6, col)
        h.rect(cx, cy + r * 0.74, cx + r * 0.28, cy + r * 0.88, col)
    elif nombre == "corona":
        base = [(cx - r * 0.75, cy + r * 0.55), (cx + r * 0.75, cy + r * 0.55), (cx + r * 0.75, cy - r * 0.35), (cx + r * 0.38, cy + r * 0.02),
                (cx, cy - r * 0.6), (cx - r * 0.38, cy + r * 0.02), (cx - r * 0.75, cy - r * 0.35)]
        h.poli(base, col)
        for px, py in ((cx - r * 0.75, cy - r * 0.42), (cx, cy - r * 0.68), (cx + r * 0.75, cy - r * 0.42)):
            h.disco(px, py, r * 0.12, col)
        h.rect(cx - r * 0.6, cy + r * 0.28, cx + r * 0.6, cy + r * 0.38, hueco)
    elif nombre == "pez":
        h.elip(cx - r * 0.8, cy - r * 0.4, cx + r * 0.38, cy + r * 0.4, col)
        h.poli([(cx + r * 0.28, cy), (cx + r * 0.85, cy - r * 0.48), (cx + r * 0.85, cy + r * 0.48)], col)
        h.disco(cx - r * 0.48, cy - r * 0.08, r * 0.09, hueco)
    elif nombre == "campana":
        pts = [(cx - r * 0.32, cy - r * 0.6), (cx + r * 0.32, cy - r * 0.6), (cx + r * 0.46, cy - r * 0.1), (cx + r * 0.52, cy + r * 0.32),
               (cx + r * 0.8, cy + r * 0.5), (cx - r * 0.8, cy + r * 0.5), (cx - r * 0.52, cy + r * 0.32), (cx - r * 0.46, cy - r * 0.1)]
        h.poli(pts, col)
        h.disco(cx, cy - r * 0.62, r * 0.3, col)
        h.disco(cx, cy - r * 0.68, r * 0.13, hueco)
        h.disco(cx, cy + r * 0.68, r * 0.16, col)
    elif nombre == "espada":
        h.poli([(cx, cy - r * 0.95), (cx + r * 0.11, cy - r * 0.75), (cx + r * 0.11, cy + r * 0.3), (cx - r * 0.11, cy + r * 0.3), (cx - r * 0.11, cy - r * 0.75)], col)
        h.rect(cx - r * 0.45, cy + r * 0.3, cx + r * 0.45, cy + r * 0.42, col)
        h.rect(cx - r * 0.08, cy + r * 0.42, cx + r * 0.08, cy + r * 0.76, col)
        h.disco(cx, cy + r * 0.84, r * 0.12, col)
    else:
        raise ValueError(nombre)


# ------------------------------------------------------------------ banderas de señales
def bandera(h, nombre, x0, y0, w, hh):
    x1, y1 = x0 + w, y0 + hh
    if nombre == "repetidor":
        h.poli([(x0, y0), (x1, (y0 + y1) / 2), (x0, y1)], AMARILLO, NEGRO, 3)
        h.poli([(x0 + w * 0.08, y0 + hh * 0.14), (x1 - w * 0.2, (y0 + y1) / 2), (x0 + w * 0.08, y1 - hh * 0.14)], ROJO)
        return
    if nombre == "diagonal":
        h.rect(x0, y0, x1, y1, BLANCO)
        h.poli([(x0, y0), (x0, y1), (x1, y1)], ROJO)
    elif nombre == "cruz":
        h.rect(x0, y0, x1, y1, AZUL)
        t = hh * 0.11
        h.rect(x0, (y0 + y1) / 2 - t, x1, (y0 + y1) / 2 + t, BLANCO)
        h.rect((x0 + x1) / 2 - t, y0, (x0 + x1) / 2 + t, y1, BLANCO)
    elif nombre == "sol":
        h.rect(x0, y0, x1, y1, AMARILLO)
        h.disco((x0 + x1) / 2, (y0 + y1) / 2, hh * 0.28, NEGRO)
    elif nombre == "damero":
        for i in range(4):
            for j in range(3):
                h.rect(x0 + w * i / 4, y0 + hh * j / 3, x0 + w * (i + 1) / 4, y0 + hh * (j + 1) / 3, NEGRO if (i + j) % 2 == 0 else BLANCO)
    elif nombre == "franjas":
        h.rect(x0, y0, x1, y1, AZUL)
        h.rect(x0, y0 + hh / 3, x1, y0 + 2 * hh / 3, AMARILLO)
    elif nombre == "cuna":
        h.rect(x0, y0, x1, y1, VERDE)
        h.poli([(x0, y0), (x0 + w * 0.62, (y0 + y1) / 2), (x0, y1)], BLANCO)
    else:
        raise ValueError(nombre)
    h.rect(x0, y0, x1, y1, None, NEGRO, 3)


# ------------------------------------------------------------------ bolsas, doblones y balanzas
def doblon(h, cx, cy, r):
    h.disco(cx, cy, r, ORO, ORO2, 2)
    h.disco(cx, cy, r * 0.66, None, ORO2, 1.5)
    h.linea([(cx, cy - r * 0.45), (cx, cy + r * 0.45)], ORO2, 2)
    h.linea([(cx - r * 0.45, cy), (cx + r * 0.45, cy)], ORO2, 2)


def bolsa(h, sim, cx, cy, r, fondo=(196, 160, 112)):
    """Saco de tela cerrado con un cordel y el símbolo pintado."""
    pts = [(cx - r * 0.25, cy - r * 0.62), (cx + r * 0.25, cy - r * 0.62), (cx + r * 0.2, cy - r * 0.45), (cx + r * 0.72, cy - r * 0.05),
           (cx + r * 0.8, cy + r * 0.55), (cx + r * 0.5, cy + r * 0.85), (cx - r * 0.5, cy + r * 0.85), (cx - r * 0.8, cy + r * 0.55),
           (cx - r * 0.72, cy - r * 0.05), (cx - r * 0.2, cy - r * 0.45)]
    h.poli(pts, fondo, MADERA2, 2.5)
    h.linea([(cx - r * 0.3, cy - r * 0.48), (cx + r * 0.3, cy - r * 0.48)], MADERA2, 3)
    h.poli([(cx - r * 0.25, cy - r * 0.62), (cx - r * 0.42, cy - r * 0.9), (cx, cy - r * 0.68), (cx + r * 0.42, cy - r * 0.9), (cx + r * 0.25, cy - r * 0.62)],
           fondo, MADERA2, 2)
    simbolo(h, sim, cx, cy + r * 0.25, r * 0.48, TINTA, fondo)


def objeto(h, cosa, cx, cy, r):
    if cosa == "doblon":
        doblon(h, cx, cy + r * 0.45, r * 0.42)
    else:
        bolsa(h, cosa, cx, cy, r * 0.8)


def balanza(h, cx, y, izq, der, ancho=230):
    """Balanza de platillos en equilibrio; `izq` y `der` son listas de cosas (bolsas por símbolo o «doblon»)."""
    h.poli([(cx - 34, y + 150), (cx + 34, y + 150), (cx + 8, y + 132), (cx - 8, y + 132)], MADERA2, NEGRO, 2)
    h.rect(cx - 5, y + 8, cx + 5, y + 136, MADERA, NEGRO, 2)
    h.poli([(cx, y - 4), (cx - 9, y + 12), (cx + 9, y + 12)], ORO, NEGRO, 2)
    h.rect(cx - ancho / 2, y + 2, cx + ancho / 2, y + 10, MADERA, NEGRO, 2)
    for lado, cosas in ((-1, izq), (1, der)):
        px = cx + lado * (ancho / 2 - 22)
        h.linea([(px, y + 10), (px - 40, y + 92)], TINTA, 2)
        h.linea([(px, y + 10), (px + 40, y + 92)], TINTA, 2)
        h.poli([(px - 50, y + 92), (px + 50, y + 92), (px + 34, y + 104), (px - 34, y + 104)], ORO, ORO2, 2)
        n = len(cosas)
        paso = min(32, 88 / max(1, n))
        for i, c in enumerate(cosas):
            ox = px + (i - (n - 1) / 2) * paso
            objeto(h, c, ox, y + 70, 30 if c != "doblon" else 26)


# ================================================================== carta 30: carta náutica (plegable)
def carta_nautica(inst):
    pl = inst["pliegues"]["66"]
    A, B = pl["x"]
    r = inst["rumbo"]
    xs = A                                                       # el pliegue, en coordenadas de la composición
    Y1, Y2 = 210, 470                                            # arriba de cada cifra

    def fondo(h, wc, hc):
        h.rect(0, 0, wc, hc, PERG)
        h.degradado(28, hc - 28, (78, 140, 160), MAR2)
        for y in range(80, hc - 40, 110):                        # paralelos (horizontales: siguen igual en la franja)
            h.linea([(0, y), (wc, y)], (110, 160, 176), 1)
        h.rect(0, 0, wc, 28, PERG)
        h.rect(0, hc - 28, wc, hc, PERG)
        h.linea([(0, 28), (wc, 28)], TINTA, 3)
        h.linea([(0, hc - 28), (wc, hc - 28)], TINTA, 3)
        for x in range(0, wc, 18):
            h.rect(x, 10, x + 9, 18, TINTA if (x // 18) % 2 == 0 else PERG)

    def objetos(h, wc, hc):
        h.linea([(14, 28), (14, hc - 28)], TINTA, 3)
        h.linea([(wc - 14, 28), (wc - 14, hc - 28)], TINTA, 3)
        for x in (110, 360):
            h.linea([(x, 28), (x, hc - 28)], (110, 160, 176), 1)
        olas(h, 30, 60, xs - 70, hc - 120, 3)
        olas(h, xs + 70, 300, wc - 30, hc - 120, 4)
        # isla grande a la izquierda y otra pequeña a la derecha
        h.poli([(26, 700), (60, 640), (120, 630), (160, 660), (170, 720), (130, 770), (60, 770)], ARENA, ARENA2, 3)
        palmera(h, 90, 700, 0.9)
        palmera(h, 130, 720, 0.7)
        h.poli([(wc - 120, 640), (wc - 70, 620), (wc - 34, 660), (wc - 60, 700), (wc - 116, 690)], ARENA, ARENA2, 3)
        palmera(h, wc - 80, 670, 0.6)
        barco(h, 70, 400, 0.8)
        # rumbo en arrecifes: dos cifras partidas por el pliegue
        cifra_arrecife(h, xs, Y1, r["carta"][0], semilla=1)
        cifra_arrecife(h, xs, Y2, r["carta"][1], semilla=2)
        # cartela y rosa a la derecha
        cx = xs + (wc - xs) / 2 + 6
        h.rect(cx - 104, 44, cx + 104, 132, PERG, TINTA, 3)
        h.texto((cx, 72), "CARTA NÁUTICA", "cartel", 30, TINTA)
        h.texto((cx, 108), "Mar de las Brumas", "texto2", 20, TINTA)
        rosa(h, cx, 216, 58)

    def extras(h):
        rng = random.Random(30)
        for x in (A + 40, B - 40):
            h.linea([(x, 28), (x, H - 28)], (110, 160, 176), 1)
        olas(h, A + 10, 60, B - 10, H - 120, 31, n=8)
        for k, y in enumerate((Y1, Y2)):
            cifra_arrecife(h, A, y, r["senuelos"][0][k], semilla=10 + k)       # su mitad derecha cae en la franja, junto a la A
            cifra_arrecife(h, B, y, r["senuelos"][1][k], semilla=20 + k)       # su mitad izquierda, junto a la B
        for _ in range(3):
            roca(h, rng.uniform(A + 20, B - 20), rng.uniform(720, 780), 9, rng)

    def marcas(h):
        linea_pliegue(h, A, 34, A, H - 34, "A", "A", (A, 46), (A, H - 46))
        linea_pliegue(h, B, 34, B, H - 34, "B", "B", (B, 46), (B, H - 46))
        _discontinua(h, [((A + B) / 2, 60), ((A + B) / 2, H - 60)], (40, 60, 70), 1, trazo=3, hueco=6)
        cx = B + (W - B) / 2 + 6
        h.rect(cx - 104, 728, cx + 104, 792, PERG, TINTA, 2)
        h.texto((cx, 746), "Pliégala en acordeón", "texto", 18, TINTA)
        h.texto((cx, 772), "hasta que A toque B", "texto", 18, TINTA)

    return carta_plegable(pl, fondo, objetos, extras, marcas, 30)


# ================================================================== carta 31: cuaderno del piloto (desvío de la aguja)
def carta_piloto(inst):
    r = inst["rumbo"]
    desvio = r["desvio"]
    h = Hoja(W, H, PERG)
    h.rect(16, 16, W - 16, H - 16, PERG, TINTA, 4)
    h.texto((W / 2, 70), "CUADERNO DEL PILOTO", "cartel", 40, TINTA)
    h.texto((W / 2, 112), "La aguja de este mar no señala al norte", "texto2", 22, TINTA)
    cx, cy, R = W / 2, 370, 190
    h.disco(cx, cy, R, (244, 230, 194), TINTA, 3)
    for k in range(72):                                        # marcas de 5 grados en el borde
        a = math.radians(k * 5) - math.pi / 2
        l = 16 if k % 18 == 0 else 8
        h.linea([(cx + (R - l) * math.cos(a), cy + (R - l) * math.sin(a)), (cx + R * math.cos(a), cy + R * math.sin(a))], TINTA, 2)
    # estrella polar: el norte verdadero
    h.linea([(cx, cy), (cx, cy - R + 6)], (90, 80, 70), 2)
    est = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rad = 22 if i % 2 == 0 else 9
        est.append((cx + rad * math.cos(a), cy - R - 34 + rad * math.sin(a)))
    h.poli(est, AMARILLO, TINTA, 2)
    h.texto((cx + 120, cy - R - 34), "estrella polar", "texto2", 20, TINTA)
    # la aguja magnética, desviada al oeste
    a = math.radians(-desvio) - math.pi / 2
    punta = (cx + (R - 24) * math.cos(a), cy + (R - 24) * math.sin(a))
    cola = (cx - (R - 60) * math.cos(a), cy - (R - 60) * math.sin(a))
    perp = (math.cos(a + math.pi / 2) * 12, math.sin(a + math.pi / 2) * 12)
    h.poli([punta, (cx + perp[0], cy + perp[1]), (cx - perp[0], cy - perp[1])], ROJO, TINTA, 2)
    h.poli([cola, (cx + perp[0], cy + perp[1]), (cx - perp[0], cy - perp[1])], (60, 60, 70), TINTA, 2)
    h.disco(cx, cy, 10, ORO, TINTA, 2)
    h.texto((cx - 50, cy - 40), "la aguja", "texto", 20, ROJO, "rm")
    # arco con rayitas entre la estrella y la aguja (una cada 5 grados)
    ra = R + 22
    arco = [(cx + ra * math.cos(math.radians(-90 - t)), cy + ra * math.sin(math.radians(-90 - t))) for t in range(0, desvio + 1, 1)]
    h.linea(arco, TINTA, 3)
    for t in range(0, desvio + 1, 5):
        ang = math.radians(-90 - t)
        h.linea([(cx + (ra - 9) * math.cos(ang), cy + (ra - 9) * math.sin(ang)), (cx + (ra + 9) * math.cos(ang), cy + (ra + 9) * math.sin(ang))], TINTA, 3)
    h.texto((cx - R - 10, cy), "OESTE", "texto", 20, TINTA, "rm")
    h.texto((cx + R + 10, cy), "ESTE", "texto", 20, TINTA, "lm")
    lineas = ["Cada rayita del arco: 5 grados.",
              "La aguja de este mar se tuerce",
              "hacia el oeste, tantas rayitas",
              "como marca el arco; y el timón",
              "obedece a la aguja."]
    for k, t in enumerate(lineas):
        h.texto((W / 2, 650 + k * 36), t, "texto", 24 if k else 22, TINTA)
    return ruido(h.final(), 31)


# ================================================================== carta 52: ordenanza de la fragata (la persecución)
def carta_ordenanza(inst):
    h = Hoja(W, H, PERG)
    h.rect(16, 16, W - 16, H - 16, PERG, TINTA, 4)
    h.texto((W / 2 + 30, 60), "ORDENANZA DE LA ARMADA", "cartel", 34, TINTA)
    h.texto((W / 2 + 30, 98), "Cómo persigue una fragata", "texto2", 22, TINTA)
    lineas = ["Por cada casilla que avanza el pirata", "(o cada turno que se queda quieto),", "la fragata da DOS pasos hacia él.",
              "En cada paso, primero se acerca", "en HORIZONTAL; si no puede", "(una roca, o ya está en su columna),",
              "se acerca en VERTICAL. Si tampoco,", "se queda quieta. No cruza las rocas."]
    for k, t in enumerate(lineas):
        h.texto((W / 2, 150 + k * 34), t, "texto" if k in (2, 4, 6) else "texto2", 22, TINTA)
    # ejemplo dibujado: 4 x 3 casillas; la fragata no puede ir a la izquierda por una roca y baja
    c, x0, y0 = 74, 167, 450
    h.texto((W / 2, y0 - 22), "Ejemplo: la roca le corta el paso", "texto", 21, ROJO)
    for yy in range(3):
        for xx in range(4):
            h.rect(x0 + xx * c, y0 + yy * c, x0 + (xx + 1) * c, y0 + (yy + 1) * c, (120, 170, 186), (70, 120, 140), 2)
    roca(h, x0 + 2 * c + c / 2, y0 + c / 2, 22, random.Random(5))
    barco(h, x0 + c / 2, y0 + 2 * c + c * 0.7, 0.55)
    fx, fy = x0 + 3 * c + c / 2, y0 + c / 2
    h.poli([(fx - 24, fy + 10), (fx + 24, fy + 10), (fx + 16, fy + 22), (fx - 18, fy + 22)], (60, 70, 90), NEGRO, 2)
    h.linea([(fx, fy + 10), (fx, fy - 26)], NEGRO, 3)
    h.poli([(fx - 2, fy - 22), (fx - 20, fy + 4), (fx - 2, fy + 6)], BLANCO, NEGRO, 2)
    h.poli([(fx + 2, fy - 20), (fx + 18, fy + 4), (fx + 2, fy + 6)], BLANCO, NEGRO, 2)
    h.texto((fx, y0 - 0 + c - 6), "fragata", "texto2", 15, TINTA, "mb")
    h.texto((x0 + c / 2, y0 + 3 * c - 4), "pirata", "texto2", 15, TINTA, "mb")
    # flechas de los dos pasos: abajo (la roca impide ir a la izquierda) y luego a la izquierda
    for (ax, ay), (bx, by) in (((fx, fy + 26), (fx, fy + c - 10)), ((fx - 12, fy + c + 10), (fx - c + 14, fy + c + 10))):
        h.linea([(ax, ay), (bx, by)], ROJO, 5)
        ang = math.atan2(by - ay, bx - ax)
        h.poli([(bx + 10 * math.cos(ang), by + 10 * math.sin(ang)), (bx + 9 * math.cos(ang + 2.4), by + 9 * math.sin(ang + 2.4)),
                (bx + 9 * math.cos(ang - 2.4), by + 9 * math.sin(ang - 2.4))], ROJO)
    h.texto((fx + 6, fy + c / 2 + 12), "1", "texto", 20, ROJO, "lm")
    h.texto((fx - c / 2, fy + c + 34), "2", "texto", 20, ROJO)
    h.rect(50, 700, W - 50, 790, (244, 230, 194), ROJO, 3)
    h.texto((W / 2, 728), "Si la fragata os alcanza, os apresa.", "texto", 21, TINTA)
    h.texto((W / 2, 762), "En la niebla no os puede ver.", "texto", 21, TINTA)
    return ruido(h.final(), 52)


# ================================================================== carta 64: carta celeste del capitán Calavera (la constelación)
def carta_celeste(inst):
    ci = inst["cielo"]
    h = Hoja(W, H, (18, 26, 52))
    h.degradado(0, H, (28, 40, 78), (10, 14, 32))
    h.rect(16, 16, W - 16, H - 16, None, ORO, 4)
    h.texto((W / 2 + 30, 64), "CARTA CELESTE", "cartel", 40, (240, 226, 180))
    h.texto((W / 2 + 30, 104), "del capitán Calavera", "texto2", 22, (220, 210, 170))
    rng = random.Random(64)
    for _ in range(140):
        x, y = rng.uniform(30, W - 30), rng.uniform(140, H - 120)
        h.disco(x, y, rng.choice((1, 1, 1.5, 2)), (150, 160, 200))
    cx, cy, k = W / 2, 400, 3.0
    pts = [(cx + x * k, cy + y * k) for x, y in ci["figura"]]
    for a, b in ((0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5), (1, 2)):
        _discontinua(h, [pts[a], pts[b]], (200, 190, 140), 2, trazo=8, hueco=7)
    for x, y in pts:
        h.disco(x, y, 13, (255, 236, 170))
        h.disco(x, y, 7, BLANCO)
    h.texto((W / 2, 610), "LA CALAVERA: seis estrellas", "texto", 26, (240, 226, 180))
    h.texto((W / 2, 652), "En la tapa de mi cofre está la Calavera,", "texto2", 21, (220, 210, 170))
    h.texto((W / 2, 684), "más pequeña y girada: buscad su forma.", "texto2", 21, (220, 210, 170))
    return ruido(h.final(), 64)


# ================================================================== carta 76: testamento (plegable)
def carta_testamento(inst):
    pl = inst["pliegues"]["53"]
    A, B = pl["x"]
    lo = inst["losas"]
    xs = A
    YS = [190, 330, 470, 610]

    def fondo(h, wc, hc):
        h.rect(0, 0, wc, hc, PERG)
        h.degradado(40, hc - 40, (238, 220, 176), (226, 204, 156))
        h.linea([(0, 30), (wc, 30)], TINTA, 3)
        h.linea([(0, 40), (wc, 40)], TINTA, 1)
        h.linea([(0, hc - 30), (wc, hc - 30)], TINTA, 3)
        h.linea([(0, hc - 40), (wc, hc - 40)], TINTA, 1)

    def objetos(h, wc, hc):
        h.linea([(20, 30), (20, hc - 30)], TINTA, 3)
        h.linea([(wc - 20, 30), (wc - 20, hc - 30)], TINTA, 3)
        for y, sim in zip(YS, lo["ciclo"]):
            simbolo(h, sim, xs, y, 56, TINTA, (236, 216, 168))
        izq = ["Yo, el capitán", "Calavera, dejo", "mi tesoro a", "quien sepa", "pisar donde", "yo pisé."]
        der = ["Mis cuatro", "señales, de", "arriba abajo,", "una y otra vez,", "de losa en losa", "vecina, hasta", "el fondo de", "la cueva."]
        for k, t in enumerate(izq):
            h.texto((xs - 76, 330 + k * 34), t, "texto2", 21, TINTA, "rm")
        for k, t in enumerate(der):
            h.texto((xs + 76, 250 + k * 34), t, "texto2", 21, TINTA, "lm")
        h.texto((xs + 120, 90), "TESTAMENTO", "cartel", 34, TINTA)
        h.texto((xs + 120, 126), "del capitán Calavera", "texto2", 20, TINTA)
        simbolo(h, "calavera", 70, 700, 28, ROJO, (236, 216, 168))
        h.linea([(52, 742), (88, 742)], ROJO, 2)

    def extras(h):
        for k, y in enumerate(YS):
            simbolo(h, lo["falsas_der"][k], A, y, 56, TINTA, (236, 216, 168))
            simbolo(h, lo["falsas_izq"][k], B, y, 56, TINTA, (236, 216, 168))
        for x in range(A + 14, B - 10, 26):
            h.linea([(x, 70), (x + 12, 70)], (190, 160, 110), 2)
            h.linea([(x, 760), (x + 12, 760)], (190, 160, 110), 2)

    def marcas(h):
        linea_pliegue(h, A, 46, A, H - 46, "A", "A", (A, 58), (A, H - 58))
        linea_pliegue(h, B, 46, B, H - 46, "B", "B", (B, 58), (B, H - 58))
        _discontinua(h, [((A + B) / 2, 80), ((A + B) / 2, H - 80)], (120, 100, 70), 1, trazo=3, hueco=6)
        h.texto((B + 120, 720), "Pliégalo en acordeón", "texto", 17, TINTA)
        h.texto((B + 120, 744), "hasta que A toque B", "texto", 17, TINTA)

    return carta_plegable(pl, fondo, objetos, extras, marcas, 76)


# ================================================================== carta 70: mapa de la isla (plegable por los dos lados)
def carta_mapa(inst):
    pl = inst["pliegues"]["75"]
    A, B = pl["x"]
    C, D = pl["y"]
    ru = inst["ruta"]
    celda, x0, y0 = 64, 59, 116
    xs, ys = A, C
    assert xs == x0 + ru["corte_col"] * celda and ys == y0 + ru["corte_fila"] * celda and B - A == ru["ocultas"] * celda == D - C
    centro = lambda c, f: (x0 + c * celda + celda / 2, y0 + f * celda + celda / 2)

    def fondo(h, wc, hc):
        h.rect(0, 0, wc, hc, MAR)
        h.degradado(0, hc, (80, 146, 168), (46, 104, 130))
        h.poli([(36, 150), (60, 100), (wc - 70, 96), (wc - 30, 140), (wc - 26, hc - 120), (wc - 70, hc - 70), (70, hc - 66), (34, hc - 130)],
               ARENA, ARENA2, 4)

    def objetos(h, wc, hc):
        olas(h, 10, 20, wc - 40, 80, 7, n=6)
        olas(h, 10, hc - 60, wc - 40, hc - 20, 8, n=6)
        for c in range(ru["cols"]):
            for f in range(ru["filas"]):
                cx0, cy0 = x0 + c * celda, y0 + f * celda
                h.rect(cx0 + 3, cy0 + 3, cx0 + celda - 3, cy0 + celda - 3, None, (196, 160, 100), 1)
        # la roca calavera, justo en el cruce de los dos pliegues
        sx, sy = xs, ys
        h.disco(sx, sy - 6, 46, HUESO, NEGRO, 3)
        h.rect(sx - 26, sy + 22, sx + 26, sy + 52, HUESO, NEGRO, 3)
        h.disco(sx - 18, sy - 8, 13, NEGRO)
        h.disco(sx + 18, sy - 8, 13, NEGRO)
        h.poli([(sx, sy + 6), (sx - 7, sy + 20), (sx + 7, sy + 20)], NEGRO)
        for dx in (-12, 0, 12):
            h.linea([(sx + dx, sy + 34), (sx + dx, sy + 52)], NEGRO, 2)
        # decorado que no pisa el camino
        celdas = {tuple(c) for c in ru["celdas"]}
        rng = random.Random(70)
        libres = [(c, f) for c in range(ru["cols"]) for f in range(ru["filas"]) if (c, f) not in celdas
                  and abs(x0 + c * celda + 32 - xs) > 70 and abs(y0 + f * celda + 32 - ys) > 70]
        rng.shuffle(libres)
        for c, f in libres[:6]:
            px, py = centro(c, f)
            (arbusto if rng.random() < 0.5 else (lambda hh, x, y, k: palmera(hh, x, y + 22, 0.55)))(h, px, py + 6, 0.9)
        # el camino: de la palmera a la X
        pts = [centro(*c) for c in ru["celdas"]]
        _discontinua(h, pts, ROJO, 5, trazo=14, hueco=10)
        px, py = pts[0]
        h.disco(px, py + 18, 20, ARENA2)
        palmera(h, px, py + 20, 0.75)
        qx, qy = pts[-1]
        h.linea([(qx - 18, qy - 18), (qx + 18, qy + 18)], ROJO, 9)
        h.linea([(qx + 18, qy - 18), (qx - 18, qy + 18)], ROJO, 9)
        # cartela
        h.texto((xs + 120, 28), "ISLA CALAVERA", "cartel", 28, TINTA)
        h.texto((xs + 120, 56), "Cada casilla, un paso.", "texto2", 17, TINTA)
        h.texto((xs + 120, 76), "Se sale de la palmera.", "texto2", 17, TINTA)
        rosa(h, wc - 52, hc - 170, 24, fondo=ARENA)

    def extras(h):
        # la rejilla sigue en las franjas
        for c in range(ru["cols"] + ru["ocultas"]):
            for f in range(ru["filas"] + ru["ocultas"]):
                cx0, cy0 = x0 + c * celda, y0 + f * celda
                if A <= cx0 < B or C <= cy0 < D:
                    h.rect(cx0 + 3, cy0 + 3, cx0 + celda - 3, cy0 + celda - 3, None, (196, 160, 100), 1)
        # el camino también cruza las franjas: desplegado, tiene pasos de más
        celdas = ru["celdas"]
        for (c1, f1), (c2, f2) in zip(celdas, celdas[1:]):
            cruza_v = {c1, c2} == {ru["corte_col"] - 1, ru["corte_col"]}
            cruza_h = {f1, f2} == {ru["corte_fila"] - 1, ru["corte_fila"]}
            if cruza_v and f1 == f2:
                y = y0 + f1 * celda + celda / 2 + (D - C if f1 >= ru["corte_fila"] else 0)
                _discontinua(h, [(A - 4, y), (B + 4, y)], ROJO, 5, trazo=14, hueco=10)
            if cruza_h and c1 == c2:
                x = x0 + c1 * celda + celda / 2 + (B - A if c1 >= ru["corte_col"] else 0)
                _discontinua(h, [(x, C - 4), (x, D + 4)], ROJO, 5, trazo=14, hueco=10)
        rng = random.Random(71)
        for _ in range(3):
            arbusto(h, rng.uniform(A + 20, B - 20), rng.choice((y0 + 290, D + 230)), 0.8)
        palmera(h, (A + B) / 2 + 30, C + 100, 0.55)
        roca(h, B + 120, (C + D) / 2, 14, rng)
        roca(h, A - 150, (C + D) / 2 + 10, 12, rng)

    def marcas(h):
        linea_pliegue(h, A, 112, A, H - 92, "A", "A", (A, 112), (A, H - 92))
        linea_pliegue(h, B, 112, B, H - 92, "B", "B", (B, 112), (B, H - 92))
        linea_pliegue(h, 20, C, W - 20, C, "C", "C", (20, C), (W - 20, C))
        linea_pliegue(h, 20, D, W - 20, D, "D", "D", (20, D), (W - 20, D))
        h.texto((B + 120, 97), "Pliégalo: A sobre B, C sobre D", "texto", 15, TINTA)

    return carta_plegable(pl, fondo, objetos, extras, marcas, 70)


HIERRO = (86, 88, 96)
MADERA2 = globals().get('MADERA2', (110, 72, 44))


# ================================================================== láminas nuevas de la versión de 60 cartas
def pagina(titulo, sub=None, w=W, h=H, fondo=PERG):
    p = Hoja(w, h, fondo)
    p.rect(16, 16, w - 16, h - 16, fondo, TINTA, 4)
    p.rect(30, 30, w - 30, h - 30, None, ORO2, 2)
    p.texto((w / 2, 74), titulo, "cartel", 32, TINTA)
    if sub:
        p.texto((w / 2, 112), sub, "texto2", 20, TINTA)
    return p


def versos(p, lineas, y0=210, paso=44, tam=22, x=W / 2, color=TINTA, tipo="texto2"):
    for k, v in enumerate(lineas):
        p.texto((x, y0 + k * paso), v, tipo, tam, color)


def flecha_p(p, a, b, color, ancho=4, punta=14):
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p.linea([a, (b[0] - math.cos(ang) * punta * 0.6, b[1] - math.sin(ang) * punta * 0.6)], color, ancho)
    p.poli([b, (b[0] - punta * math.cos(ang - 0.45), b[1] - punta * math.sin(ang - 0.45)), (b[0] - punta * math.cos(ang + 0.45), b[1] - punta * math.sin(ang + 0.45))], color)


def campana(h, cx, cy, r):
    pts = [(cx - r * 0.3, cy - r * 0.6), (cx + r * 0.3, cy - r * 0.6), (cx + r * 0.46, cy - r * 0.1), (cx + r * 0.52, cy + r * 0.32),
           (cx + r * 0.8, cy + r * 0.5), (cx - r * 0.8, cy + r * 0.5), (cx - r * 0.52, cy + r * 0.32), (cx - r * 0.46, cy - r * 0.1)]
    h.poli(pts, ORO, TINTA, 2)
    h.disco(cx, cy + r * 0.68, r * 0.16, ORO2, TINTA, 1)


# ------------------------------------------------------------------ 16: la bitácora
def carta_bitacora(inst):
    b = inst["bitacora"]
    p = pagina("LA BITÁCORA", "de La Gaviota")
    p.rect(60, 150, W - 60, 440, (244, 230, 194), TINTA, 3)
    p.texto((90, 176), "GUARDIA", "cartel", 20, ROJO, "lm")
    p.texto((W - 90, 176), "EMPIEZA A LAS", "cartel", 20, ROJO, "rm")
    for k, (nombre, h) in enumerate(b["guardias"]):
        y = 212 + k * 38
        p.texto((90, y), nombre, "texto", 22, TINTA, "lm")
        p.texto((W - 90, y), f"{h}:00", "texto", 22, TINTA, "rm")
        p.linea([(80, y + 18), (W - 80, y + 18)], (200, 176, 130), 1)
    versos(p, ["Cada guardia dura cuatro horas.", "Cada media hora suena una campanada más:", "una, dos, tres... hasta ocho."], 470, 30, 19)
    for k, (que, g, c) in enumerate(b["anotaciones"]):
        y = 595 + k * 76
        p.disco(80, y, 20, ROJO, TINTA, 2)
        p.texto((80, y), str(k + 1), "cartel", 24, BLANCO)
        p.texto((116, y - 14), que + ":", "texto", 21, TINTA, "lm")
        p.texto((116, y + 14), f"{c} campanadas de la guardia de {g}", "texto2", 19, TINTA, "lm")
    p.rect(60, 826, W - 60, 846, (244, 230, 194), ROJO, 2)
    p.texto((W / 2, 836), "¿Cuánto pasó entre el aviso 1 y el aviso 3?", "texto", 17, ROJO)
    return ruido(p.final(), 16)


# ------------------------------------------------------------------ 19 y 21: la carta de aguas (la persecución)
def aguas(inst):
    d = inst["persecucion"]
    celda = 88
    x0, y0 = 7, 530
    h = Hoja(W, H * 2, MAR)
    h.degradado(0, H * 2, (80, 146, 168), (46, 104, 130))
    h.rect(16, 16, W - 16, H * 2 - 16, None, ORO2, 4)
    h.texto((W / 2, 74), "CARTA DE AGUAS DE LA BAHÍA", "cartel", 30, BLANCO, "mm", NEGRO, 3)
    rosa(h, W / 2, 270, 90, fondo=(244, 230, 194))
    for yy in range(d["alto"]):
        for xx in range(d["ancho"]):
            h.rect(x0 + xx * celda, y0 + yy * celda, x0 + (xx + 1) * celda, y0 + (yy + 1) * celda, None, (190, 226, 236), 2)
    rng = random.Random(21)
    for rx, ry in d["rocas"]:
        roca(h, x0 + rx * celda + celda / 2, y0 + ry * celda + celda / 2, 30, rng)
    bx, by = d["barco"]
    barco(h, x0 + bx * celda + celda / 2, y0 + by * celda + celda / 2 + 14, 0.9)
    fx, fy = d["fragata"]
    cx, cy = x0 + fx * celda + celda / 2, y0 + fy * celda + celda / 2
    h.poli([(cx - 34, cy + 12), (cx + 34, cy + 12), (cx + 24, cy + 28), (cx - 26, cy + 28)], (60, 70, 90), NEGRO, 2)
    for dx in (-14, 14):
        h.linea([(cx + dx, cy + 12), (cx + dx, cy - 28)], NEGRO, 3)
        h.poli([(cx + dx - 2, cy - 24), (cx + dx - 20, cy + 6), (cx + dx - 2, cy + 8)], BLANCO, NEGRO, 2)
    nx, ny = d["niebla"]
    for k in range(6):
        h.disco(x0 + nx * celda + celda / 2 + rng.uniform(-18, 18), y0 + ny * celda + celda / 2 + rng.uniform(-14, 14), rng.uniform(18, 28), (246, 250, 252))
    yb = y0 + d["alto"] * celda
    h.rect(50, yb + 40, W - 50, yb + 200, (244, 230, 194), TINTA, 3)
    h.texto((W / 2, yb + 70), "LEYENDA", "cartel", 22, TINTA)
    barco(h, 110, yb + 150, 0.5)
    h.texto((150, yb + 130), "La Gaviota", "texto2", 18, TINTA, "lm")
    h.poli([(300, yb + 160), (350, yb + 160), (342, yb + 172), (308, yb + 172)], (60, 70, 90), NEGRO, 2)
    h.linea([(325, yb + 160), (325, yb + 126)], NEGRO, 3)
    h.texto((362, yb + 140), "la fragata", "texto2", 18, TINTA, "lm")
    for k in range(3):
        h.disco(470 + k * 16, yb + 150, 13, (246, 250, 252), (150, 170, 176), 1)
    h.texto((520, yb + 130), "niebla", "texto2", 18, TINTA, "lm")
    return ruido(h.final(), 19)


# ------------------------------------------------------------------ 41 y 43: el cielo del cofre (la constelación)
def cielo_cofre(inst):
    c = inst["cielo"]
    h = Hoja(W * 2, H, (18, 26, 52))
    h.degradado(0, H, (28, 40, 78), (10, 14, 32))
    h.rect(16, 16, W * 2 - 16, H - 16, None, ORO, 4)
    h.texto((W, 74), "EL CIELO DE LA TAPA", "cartel", 36, (240, 226, 180))
    rng = random.Random(41)
    for _ in range(220):
        x, y = rng.uniform(40, W * 2 - 40), rng.uniform(130, H - 40)
        h.disco(x, y, rng.choice((1, 1, 1.5)), (120, 130, 170))
    for k, (x, y) in enumerate(c["estrellas"]):
        h.disco(x, y, 16, (255, 236, 170))
        h.disco(x, y, 9, BLANCO)
        h.texto((x + 22, y - 18), str(k + 1), "texto", 17, (240, 226, 180), "lm")
    return ruido(h.final(), 41)


# ------------------------------------------------------------------ 42 y 49: el suelo de la cueva (las losas)
def suelo_cueva(inst):
    s = inst["losas"]
    n = s["n"]
    lado = 110
    x0, y0 = 300, 150
    h = Hoja(W * 2, H, (60, 52, 44))
    h.rect(16, 16, W * 2 - 16, H - 16, None, ORO2, 4)
    h.texto((W, 66), "EL SUELO DE LA CUEVA", "cartel", 34, (240, 226, 180))
    h.texto((W, 98), "visto desde la entrada", "texto2", 19, (240, 226, 180))
    for y in range(n):
        for x in range(n):
            cx0, cy0 = x0 + x * lado, y0 + y * lado
            h.rect(cx0 + 3, cy0 + 3, cx0 + lado - 3, cy0 + lado - 3, (136, 130, 116), (30, 26, 22), 3)
            h.rect(cx0 + 8, cy0 + 8, cx0 + lado - 8, cy0 + lado - 8, (148, 142, 128))
            simbolo(h, s["suelo"][y][x], cx0 + lado / 2, cy0 + lado / 2, 40, (40, 34, 28), (148, 142, 128))
    h.texto((W, y0 - 14), "FONDO", "texto", 17, (240, 226, 180))
    h.texto((W, y0 + n * lado + 22), "ENTRADA", "texto", 17, (240, 226, 180))
    return ruido(h.final(), 42)


# ------------------------------------------------------------------ 54, 55 y 59: la tabla de tiro
def sacos(h, cx, cy, k):
    for i in range(k):
        x = cx + (i % 3) * 30 - (min(k, 3) - 1) * 15
        y = cy + (i // 3) * 26
        h.disco(x, y, 12, (150, 112, 70), MADERA2, 2)
        h.linea([(x - 5, y - 11), (x + 5, y - 11)], MADERA2, 2)


def carta_cargas(inst):
    c = inst["canon"]
    p = pagina("LA TABLA DE TIRO (I)", "por la carga de pólvora")
    for k in range(6):
        y = 190 + k * 110
        p.rect(50, y - 46, W - 50, y + 46, (244, 230, 194), TINTA, 3)
        sacos(p, 130, y - 12, k + 1)
        flecha_p(p, (240, y), (330, y), TINTA, 4)
        p.texto((440, y), f"{c['base'][k]}", "cartel", 50, ROJO)
        p.texto((490, y + 10), "cables", "texto2", 17, TINTA, "lm")
    return ruido(p.final(), 54)


def carta_elevaciones(inst):
    c = inst["canon"]
    p = pagina("LA TABLA DE TIRO (II)", "por la elevación del cañón")
    for k, (ang, cor) in enumerate(zip(c["elevaciones"], c["corr"])):
        y = 190 + k * 130
        p.rect(50, y - 54, W - 50, y + 54, (244, 230, 194), TINTA, 3)
        bx, by = 120, y + 26
        p.linea([(bx - 60, by), (bx + 90, by)], TINTA, 3)
        a = math.radians(ang)
        p.linea([(bx, by), (bx + 110 * math.cos(a), by - 110 * math.sin(a))], ROJO, 8)
        p.disco(bx, by, 10, NEGRO)
        p.texto((300, y), f"{ang}°", "cartel", 36, TINTA)
        col = VERDE if cor >= 0 else ROJO
        p.texto((440, y), ("+" if cor >= 0 else "−") + str(abs(cor)), "cartel", 50, col)
        p.texto((490, y + 10), "cables", "texto2", 17, TINTA, "lm")
    return ruido(p.final(), 55)


def carta_presas(inst):
    c = inst["canon"]
    p = pagina("LAS TRES PRESAS", "tres barcos a tiro")
    for k, b in enumerate(c["barcos"]):
        y = 210 + k * 140
        p.rect(60, y - 54, W - 60, y + 54, (244, 230, 194), TINTA, 3)
        p.texto((100, y - 20), f"Barco {k + 1}", "cartel", 24, TINTA, "lm")
        p.texto((100, y + 18), f"a {b['dist']} cables", "texto", 22, ROJO, "lm")
        v = b["viento"]
        if v:
            for m in range(abs(v)):
                x = 330 + m * 44
                col = VERDE if v > 0 else ROJO
                if v > 0:
                    p.poli([(x, y - 22), (x + 30, y), (x, y + 22), (x + 10, y)], col, NEGRO, 2)
                else:
                    p.poli([(x + 30, y - 22), (x, y), (x + 30, y + 22), (x + 20, y)], col, NEGRO, 2)
        else:
            p.texto((380, y), "sin viento", "texto2", 20, TINTA)
    p.rect(60, 640, W - 60, 800, (244, 230, 194), ROJO, 3)
    p.texto((W / 2, 672), f"Quedan {c['limite']} sacos de pólvora", "cartel", 26, ROJO)
    versos(p, ["Cada barco, una carga distinta.", "El alcance es la suma de lo que da", "la carga, la elevación y el viento."], 706, 28, 19)
    return ruido(p.final(), 59)


# ------------------------------------------------------------------ 37, 39 y 33: el reparto del botín
def pirata_cara(h, cx, cy, k, rango):
    cols = [(172, 38, 32), (36, 76, 160), (58, 116, 62), (228, 180, 56), (140, 80, 150), (230, 120, 40), (60, 60, 70)]
    h.disco(cx, cy, 36, (222, 176, 130), NEGRO, 3)
    h.poli([(cx - 40, cy - 14), (cx + 40, cy - 14), (cx + 28, cy - 44), (cx - 28, cy - 44)], cols[k % 7], NEGRO, 3)
    h.disco(cx + (10 if k % 2 else -10), cy - 4, 10, NEGRO)
    h.disco(cx + (-12 if k % 2 else 12), cy - 6, 4, BLANCO)
    h.linea([(cx - 16, cy + 18), (cx + 16, cy + 18)], NEGRO, 3)
    h.disco(cx, cy + 56, 16, ROJO, TINTA, 2)
    h.texto((cx, cy + 56), str(rango), "cartel", 20, BLANCO)


def carta_tripulacion(inst):
    b = inst["botin"]
    p = pagina("LA TRIPULACIÓN", "por orden de antigüedad")
    for k in range(b["piratas"]):
        cx = 120 + (k % 3) * 195 if k < 6 else 315
        cy = 220 + (k // 3) * 190 if k < 6 else 600
        pirata_cara(p, cx, cy, k, k + 1)
    p.texto((W / 2, 740), "El 1 es el capitán.", "texto", 22, TINTA)
    return ruido(p.final(), 37)


def carta_codigo(inst):
    p = pagina("EL CÓDIGO DE LA HERMANDAD", "colgado en el palo mayor")
    versos(p, ["«Manda el más antiguo, y reparte.", "", "Todos votan: sí o no.", "Con la mitad de síes, por lo menos,", "se reparte como dijo el capitán.", "",
               "Si no, al capitán, por la borda,", "y reparte el que sigue.", "", "Cada pirata quiere vivir;", "luego, tener más doblones;", "y, a igual botín, ver caer al capitán.»"], 175, 44, 21)
    return ruido(p.final(), 39)


def carta_botin(inst):
    b = inst["botin"]
    p = pagina("EL BOTÍN", "de la Isla Calavera")
    for k in range(12):
        x = 110 + (k % 6) * 85
        y = 240 + (k // 6) * 110
        for j in range(5):
            doblon(p, x, y - j * 7, 30)
    p.texto((W / 2, 480), f"{b['monedas']} doblones", "cartel", 50, ROJO)
    p.texto((W / 2, 560), f"{b['piratas']} piratas a bordo", "cartel", 30, TINTA)
    p.texto((W / 2, 640), "Todos votan, también el capitán.", "texto", 22, TINTA)
    return ruido(p.final(), 33)


# ------------------------------------------------------------------ 26, 61 y 63: las mareas
def carta_calado(inst):
    m = inst["mareas"]
    p = pagina("EL PASO DE LAS BARRAS", "con La Gaviota cargada")
    p.rect(60, 150, W - 60, 260, (244, 230, 194), TINTA, 3)
    barco(p, 140, 230, 0.8)
    p.texto((420, 190), "CALADO", "cartel", 26, TINTA)
    p.texto((420, 232), f"{m['calado']} decímetros", "cartel", 30, ROJO)
    nombres = ["Barra del Cangrejo", "Barra del Faro", "Barra Seca"]
    for k, b in enumerate(m["barras"]):
        y = 340 + k * 150
        p.rect(60, y - 56, W - 60, y + 56, (244, 230, 194), TINTA, 3)
        p.texto((90, y - 26), nombres[k], "texto", 22, TINTA, "lm")
        p.texto((90, y + 12), "se cruza " + ("al salir" if b["tras"] == 0 else f"{b['tras']} horas después"), "texto2", 20, TINTA, "lm")
        p.texto((W - 90, y + 8), f"+{b['fondo']} dm", "cartel", 32, ROJO, "rm")
    versos(p, ["El agua sobre cada barra es lo que marca", "la tabla de la marea más su fondo propio."], 800, 28, 18)
    return ruido(p.final(), 26)


def tabla_mareas(inst):
    m = inst["mareas"]
    h = Hoja(W, H * 2, PERG)
    h.rect(16, 16, W - 16, H * 2 - 16, PERG, TINTA, 4)
    h.rect(30, 30, W - 30, H * 2 - 30, None, ORO2, 2)
    h.texto((W / 2, 74), "LA TABLA DE LA MAREA", "cartel", 32, TINTA)
    h.texto((W / 2, 110), "altura del agua, en decímetros, hora por hora", "texto2", 19, TINTA)
    paso = 62
    y0 = [150, 150 + 12 * paso + 60]
    # las doce primeras horas arriba (hasta la mitad) y las otras doce abajo; el corte está entre las dos tandas
    for t in range(24):
        bloque = 0 if t < 12 else 1
        y = (150 + t * paso) if bloque == 0 else (H + 36 + (t - 12) * paso)
        h.texto((84, y + 24), f"{t:02d}", "cartel", 24, TINTA)
        h.rect(120, y + 6, 120 + m["alturas"][t] * 9, y + 42, MAR, TINTA, 2)
        h.texto((120 + m["alturas"][t] * 9 + 14, y + 24), str(m["alturas"][t]), "cartel", 22, ROJO, "lm")
    return ruido(h.final(), 61)


# ------------------------------------------------------------------ 70 y 71: las pesas
def carta_cofres(inst):
    d = inst["pesas"]
    p = pagina("LOS COFRES DEL BOTÍN", "pesados uno a uno")
    for k, w in enumerate(d["objetos"]):
        y = 250 + k * 190
        p.rect(60, y - 80, W - 60, y + 80, (244, 230, 194), TINTA, 3)
        p.rect(100, y - 40, 250, y + 40, MADERA, NEGRO, 3)
        p.rect(100, y - 40, 250, y - 14, MADERA2, NEGRO, 3)
        p.disco(175, y + 4, 9, ORO, NEGRO, 2)
        p.texto((430, y - 10), f"{w}", "cartel", 64, ROJO)
        p.texto((430, y + 44), "libras", "texto2", 20, TINTA)
    return ruido(p.final(), 70)


def carta_pesas(inst):
    d = inst["pesas"]
    p = pagina("LAS PESAS DE HIERRO", "una de cada")
    for k, w in enumerate(d["pesas"]):
        x = 120 + k * 130
        r = 22 + k * 8
        p.poli([(x - r, 330), (x + r, 330), (x + r * 0.7, 330 - r * 1.2), (x - r * 0.7, 330 - r * 1.2)], HIERRO, NEGRO, 3)
        p.disco(x, 330 - r * 1.3, 8, HIERRO, NEGRO, 2)
        p.texto((x, 330 - 6), str(w), "cartel", 20 + k * 3, BLANCO)
    p.rect(60, 420, W - 60, 530, (244, 230, 194), TINTA, 3)
    balanza(p, W / 2, 440, ["doblon"], ["doblon"], ancho=300)
    versos(p, ["«Cada pesa, en un solo platillo:", "con el cofre, o enfrente.", "Todas pueden quedarse fuera.»"], 700, 44, 21)
    return ruido(p.final(), 71)


# ------------------------------------------------------------------ 79: la entrada de la gruta
def carta_gruta(inst):
    r = inst["ruta"]
    p = pagina("LA ENTRADA DE LA GRUTA", "por el lado del este")
    ancho, alto = r["filas"], r["cols"]
    lado = 50
    x0, y0 = 60, 210
    p.rect(x0 - 8, y0 - 8, x0 + ancho * lado + 8, y0 + alto * lado + 8, (200, 160, 100), TINTA, 4)
    for y in range(alto):
        for x in range(ancho):
            p.rect(x0 + x * lado + 2, y0 + y * lado + 2, x0 + (x + 1) * lado - 2, y0 + (y + 1) * lado - 2, (230, 200, 136), (170, 130, 80), 1)
    flecha_p(p, (540, y0 + alto * lado + 30), (540, y0 + alto * lado - 60), ROJO, 5, 18)
    p.texto((540, y0 + alto * lado + 56), "ENTRADA", "texto", 15, ROJO)
    flecha_p(p, (480, y0 - 10), (580, y0 - 10), TINTA, 4, 14)
    p.texto((530, y0 - 34), "NORTE", "texto", 15, TINTA)
    versos(p, ["«Se entra por el este,", "y quien entra mira a poniente:", "el norte le cae a la derecha.", "", "Es el mismo suelo del mapa,", "visto de otro lado.»"], 600, 38, 20)
    return ruido(p.final(), 79)


# ------------------------------------------------------------------ 86 y 87: la isla
def icono_isla(h, k, cx, cy):
    if k == "14":                                               # la bitácora
        h.rect(cx - 28, cy - 30, cx + 28, cy + 30, (160, 100, 60), NEGRO, 3)
        for a in range(3):
            h.linea([(cx - 18, cy - 14 + a * 14), (cx + 18, cy - 14 + a * 14)], PERG, 3)
    elif k == "40":                                             # el cielo
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rad = 32 if i % 2 == 0 else 13
            pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
        h.poli(pts, AMARILLO, NEGRO, 2)
    elif k == "52":                                             # el cañón
        h.rect(cx - 34, cy - 10, cx + 20, cy + 14, HIERRO, NEGRO, 3)
        h.disco(cx - 14, cy + 22, 14, MADERA2, NEGRO, 3)
    elif k == "69":                                             # la balanza
        h.linea([(cx, cy - 28), (cx, cy + 28)], NEGRO, 4)
        h.linea([(cx - 32, cy - 20), (cx + 32, cy - 20)], NEGRO, 4)
        h.poli([(cx - 40, cy + 4), (cx - 24, cy + 4), (cx - 32, cy - 20)], ORO, NEGRO, 2)
        h.poli([(cx + 24, cy + 4), (cx + 40, cy + 4), (cx + 32, cy - 20)], ORO, NEGRO, 2)
    else:                                                       # la gruta
        palmera(h, cx - 4, cy + 30, 0.7)


def carta_rumbos(inst):
    d = inst["isla"]
    p = pagina("LOS CINCO RUMBOS", "con el norte arriba")
    for n, k in enumerate(d["orden"]):
        y = 205 + n * 132
        p.rect(50, y - 54, W - 50, y + 54, (244, 230, 194), TINTA, 3)
        icono_isla(p, k, 120, y)
        cx, cy, r = 320, y, 40
        p.disco(cx, cy, r, PERG, TINTA, 2)
        dx, dy = RUMBOS_DIR[d["rumbos"][n]]
        flecha_p(p, (cx - dx * r * 0.7, cy - dy * r * 0.7), (cx + dx * r * 0.9, cy + dy * r * 0.9), ROJO, 6, 18)
        p.texto((cx, cy - r - 12), "N", "texto", 15, TINTA)
        p.linea([(480, y + 12), (580, y + 12)], TINTA, 3)
        p.texto((530, y - 18), "casillas", "texto2", 17, TINTA)
    return ruido(p.final(), 86)


RUMBOS_DIR = {"N": (0, -1), "NE": (0.7071, -0.7071), "E": (1, 0), "SE": (0.7071, 0.7071), "S": (0, 1), "SO": (-0.7071, 0.7071), "O": (-1, 0), "NO": (-0.7071, -0.7071)}


def carta_isla_mapa(inst):
    d = inst["isla"]
    n = d["n"]
    celda = 54
    x0, y0 = (W - n * celda) / 2, 170
    p = Hoja(W, H, MAR)
    p.degradado(0, H, (80, 146, 168), (46, 104, 130))
    p.rect(16, 16, W - 16, H - 16, None, ORO2, 4)
    p.texto((W / 2, 70), "LA CARTA DE LA ISLA CALAVERA", "cartel", 28, BLANCO, "mm", NEGRO, 3)
    for i in range(n):
        for j in range(n):
            p.rect(x0 + i * celda, y0 + j * celda, x0 + (i + 1) * celda, y0 + (j + 1) * celda, None, (190, 226, 236), 2)
    for i in range(n):
        p.texto((x0 + i * celda + celda / 2, y0 - 16), str(i + 1), "texto", 15, BLANCO)
        p.texto((x0 - 18, y0 + i * celda + celda / 2), str(i + 1), "texto", 15, BLANCO)
    rng = random.Random(87)
    ocupadas = {tuple(c) for c in d["camino"]}
    for _ in range(14):
        i, j = rng.randrange(n), rng.randrange(n)
        if (i, j) in ocupadas or abs(i - d["final"][0]) + abs(j - d["final"][1]) < 2:
            continue
        cx, cy = x0 + i * celda + celda / 2, y0 + j * celda + celda / 2
        p.poli([(cx - 20, cy + 8), (cx - 12, cy - 12), (cx + 14, cy - 14), (cx + 22, cy + 6), (cx + 4, cy + 20)], ARENA, ARENA2, 2)
        if rng.random() < 0.6:
            palmera(p, cx, cy + 14, 0.38)
    sx, sy = d["inicio"]
    barco(p, x0 + sx * celda + celda / 2, y0 + sy * celda + celda / 2 + 8, 0.45)
    p.texto((x0 + sx * celda + celda / 2, y0 + (sy + 1) * celda + 10), "SALIDA", "cartel", 13, BLANCO, "mm", NEGRO, 2)
    rosa(p, 540, 780, 40, fondo=(244, 230, 194))
    return ruido(p.final(), 87)


# ================================================================== imágenes de la interfaz (img/ui)
def ui_imagenes(carpeta, inst):
    ui = os.path.join(carpeta, "img", "ui")
    os.makedirs(ui, exist_ok=True)

    def guardar(h, nombre, transparente=None):
        im = h.final()
        if transparente is not None:
            a = np.asarray(im).astype(np.int16)
            d = np.abs(a - np.array(transparente)).sum(axis=2)
            alfa = np.clip(d * 3, 0, 255).astype(np.uint8)
            im = Image.fromarray(np.dstack([np.asarray(im), alfa]))
        im.save(os.path.join(ui, nombre))

    h = Hoja(120, 120, (255, 0, 255))
    barco(h, 60, 84, 1.1)
    guardar(h, "gaviota.png", (255, 0, 255))
    h = Hoja(120, 120, (255, 0, 255))
    h.poli([(14, 84), (106, 84), (92, 104), (24, 104)], (60, 70, 90), NEGRO, 3)
    for x, alto in ((40, 70), (78, 62)):
        h.linea([(x, 84), (x, 84 - alto)], NEGRO, 3)
        h.poli([(x - 2, 84 - alto + 6), (x - 26, 76), (x - 2, 78)], BLANCO, NEGRO, 2)
        h.poli([(x + 2, 84 - alto + 8), (x + 22, 76), (x + 2, 78)], BLANCO, NEGRO, 2)
    h.poli([(78, 22), (98, 26), (78, 30)], ROJO)
    guardar(h, "fragata.png", (255, 0, 255))
    h = Hoja(120, 120, (255, 0, 255))
    palmera(h, 56, 108, 1.5)
    guardar(h, "palmera.png", (255, 0, 255))
    for sim in ["ancla", "calavera", "estrella", "luna", "llave", "corona", "pez", "campana", "espada"]:
        h = Hoja(160, 160, (0, 0, 0))
        simbolo(h, sim, 80, 80, 66, (236, 214, 160), (0, 0, 0))
        guardar(h, f"sim-{sim}.png")
    h = Hoja(120, 120, (255, 0, 255))
    h.disco(60, 60, 54, MADERA, NEGRO, 3)
    h.disco(60, 60, 40, (160, 108, 62), MADERA2, 2)
    h.disco(60, 60, 54, None, (70, 70, 76), 6)
    h.disco(60, 60, 28, None, (70, 70, 76), 4)
    h.disco(60, 60, 8, MADERA2)
    guardar(h, "barril.png", (255, 0, 255))
    h = Hoja(420, 420, (255, 0, 255))
    rosa(h, 210, 210, 170, fondo=(244, 230, 194))
    for k in range(72):
        a = math.radians(k * 5) - math.pi / 2
        l = 14 if k % 9 == 0 else 7
        h.linea([(210 + (180 - l) * math.cos(a), 210 + (180 - l) * math.sin(a)), (210 + 180 * math.cos(a), 210 + 180 * math.sin(a))], TINTA, 2)
    guardar(h, "rosa.png", (255, 0, 255))


# ================================================================== datos de los minijuegos
def _dist(i, k):
    return i["isla"]["distancias"][i["isla"]["orden"].index(k)]


DATOS_MINIJUEGOS = {
    "14-bitacora.js": lambda i: {"entre_horas": i["bitacora"]["entre_horas"], "entre_min": i["bitacora"]["entre_min"], "distancia": _dist(i, "14")},
    "20-persecucion.js": lambda i: {k: i["persecucion"][k] for k in ("ancho", "alto", "rocas", "barco", "fragata", "niebla")},
    "40-cielo.js": lambda i: {"estrellas": i["cielo"]["estrellas"], "solucion": i["cielo"]["solucion"], "distancia": _dist(i, "40")},
    "48-suelo.js": lambda i: {k: i["losas"][k] for k in ("n", "ciclo", "suelo")},
    "52-canon.js": lambda i: dict({k: i["canon"][k] for k in ("base", "corr", "barcos", "limite", "solucion")}, distancia=_dist(i, "52")),
    "46-botin.js": lambda i: {k: i["botin"][k] for k in ("piratas", "monedas", "solucion", "necesarios", "previo")},
    "51-mareas.js": lambda i: {"salida": i["mareas"]["salida"], "alturas": i["mareas"]["alturas"], "calado": i["mareas"]["calado"], "barras": i["mareas"]["barras"]},
    "64-rumbo.js": lambda i: {"carta": i["rumbo"]["carta"], "aguja": i["rumbo"]["aguja"], "senuelos": i["rumbo"]["senuelos"]},
    "69-pesas.js": lambda i: dict({k: i["pesas"][k] for k in ("pesas", "objetos", "solucion")}, distancia=_dist(i, "69")),
    "72-gruta.js": lambda i: dict({k: i["ruta"][k] for k in ("cols", "filas", "inicio", "celdas")}, distancia=_dist(i, "72")),
    "85-isla.js": lambda i: {k: i["isla"][k] for k in ("n", "inicio", "final")},
}


def inyectar_datos(carpeta, inst):
    """Copia en cada minijuego (entre /*DATOS*/ y /*FIN*/) su instancia, para que la app y los solucionadores usen los mismos datos."""
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


# ================================================================== salida
def main(carpeta="juegos/aventuras-ca/piratas"):
    inst = _inst()
    arte = os.path.join(carpeta, "arte")
    comprobar = os.path.join(arte, "comprobar")
    os.makedirs(comprobar, exist_ok=True)
    laminas = {"16": carta_bitacora(inst), "18": carta_ordenanza(inst), "45": carta_celeste(inst), "67": carta_piloto(inst), "66": carta_nautica(inst),
               "53": carta_testamento(inst), "75": carta_mapa(inst), "54": carta_cargas(inst), "55": carta_elevaciones(inst), "59": carta_presas(inst),
               "37": carta_tripulacion(inst), "39": carta_codigo(inst), "33": carta_botin(inst), "26": carta_calado(inst), "70": carta_cofres(inst),
               "71": carta_pesas(inst), "79": carta_gruta(inst), "86": carta_rumbos(inst), "87": carta_isla_mapa(inst)}
    for k, im in laminas.items():
        im.save(os.path.join(arte, f"{k}.png"))
        if k in inst["pliegues"]:
            plegar(im, inst["pliegues"][k]).save(os.path.join(comprobar, f"{k}-plegada.png"))

    def mosaico(nombre, im, filas, cols, cartas):
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))
        for pieza, k in zip(cortar(im, filas, cols), cartas):
            pieza.save(os.path.join(arte, f"{k}.png"))
    mosaico("aguas", aguas(inst), 2, 1, ("19", "21"))
    mosaico("cielo", cielo_cofre(inst), 1, 2, ("41", "43"))
    mosaico("suelo", suelo_cueva(inst), 1, 2, ("42", "49"))
    mosaico("mareas", tabla_mareas(inst), 2, 1, ("61", "63"))
    ui_imagenes(carpeta, inst)
    inyectar_datos(carpeta, inst)
    print("láminas escritas en", arte, "y comprobaciones en", comprobar)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

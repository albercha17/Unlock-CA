"""Láminas de «Cretácico: El Valle de los Gigantes» (versión de 60 cartas, 21 oct 2026). Todas las pistas son dibujos o acertijos:
ninguna carta escribe la respuesta ni explica cómo se resuelve su puzle. Datos de herramientas/instancias_dinosaurios.py.

  16 el barro (huellas pisadas unas sobre otras) · 18 la guía de huellas, con la nota del barro
  19 y 21 la manada tras los helechos (cabezas arriba, patas abajo)
  41 y 43 la playa de los nidos vista desde el oeste y desde el sur · 45 la costumbre de las madres
  42 y 49 el mapa del valle (dos mitades) · 53 lo que vieron los tres vigías
  54 y 55 las alturas de la ladera (dos mitades) · 59 la canción de la lava
  37 y 39 el mapa de los senderos (dos mitades) · 33 la costumbre de la manada
  26 el árbol de la doctora · 61 y 63 las fichas de los animales
  70 quién se come a quién · 71 el plano del corral
  75 el cielo del acantilado (térmicas) · 79 cómo planea el pterosaurio
  66 la ciénaga (dónde está la cueva) · 67 la advertencia de la balsa
  86, 87 y 76 los tres troncos fósiles
Uso (desde la raíz del repo):  python herramientas/dinosaurios.py [carpeta_juego]
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
import instancias_dinosaurios as I  # noqa: E402

W, H = 630, 882
PAPEL = (238, 228, 200)
TINTA = (52, 44, 30)
VERDE = (70, 120, 60)
VERDE2 = (120, 170, 90)
BARRO = (150, 112, 74)
BARRO2 = (96, 66, 40)
OCRE = (200, 150, 70)
ROJO = (190, 60, 40)
AZUL = (70, 120, 180)
GRIS = (130, 126, 118)
BLANCO = (250, 246, 236)
NARANJA = (230, 120, 40)
LETRAS = "ABCDEFGH"


def ruido(im, s, f=2.5):
    a = np.asarray(im).astype(np.int16)
    a = a + np.random.default_rng(s).normal(0, f, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def pagina(titulo, sub=None, fondo=PAPEL, borde=VERDE, w=W, h=H):
    p = Hoja(w, h, fondo)
    p.rect(16, 16, w - 16, h - 16, None, borde, 6)
    p.rect(28, 28, w - 28, h - 28, None, borde, 2)
    p.texto((w / 2 + 26, 70), titulo, "cartel", 32, TINTA)
    if sub:
        p.texto((w / 2 + 26, 108), sub, "texto2", 21, TINTA)
    return p


def versos(p, lineas, y0=220, paso=56, tam=27):
    for k, v in enumerate(lineas):
        p.texto((W / 2, y0 + k * paso), v, "texto2", tam, TINTA)


# ------------------------------------------------------------------ huellas
def huella(p, especie, cx, cy, s=1.0, ang=0.0, fill=BARRO2, borde=(70, 46, 26), grosor=3):
    """Dibuja la huella de cada especie (forma propia); ang en radianes, la huella apunta hacia arriba."""
    def rot(pts):
        c, si = math.cos(ang), math.sin(ang)
        return [(cx + (x * c - y * si) * s, cy + (x * si + y * c) * s) for x, y in pts]

    def dedo(x, y, largo, ancho, a):
        pts = []
        for t in range(0, 360, 30):
            r = math.radians(t)
            px, py = math.cos(r) * ancho, math.sin(r) * largo
            pts.append((x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)))
        return rot(pts)
    if especie == "tiranosaurio":          # tres dedos largos y afilados, talón estrecho
        p.poli(dedo(0, 10, 26, 14, 0), fill, borde, grosor)
        for dx, a in ((-26, -0.45), (0, 0), (26, 0.45)):
            p.poli(dedo(dx * 0.8, -34, 40, 10, a), fill, borde, grosor)
    elif especie == "velociraptor":        # dos dedos (el tercero, la garra, no toca el suelo)
        p.poli(dedo(0, 14, 16, 10, 0), fill, borde, grosor)
        for dx, a in ((-9, -0.12), (10, 0.12)):
            p.poli(dedo(dx, -16, 26, 7, a), fill, borde, grosor)
        p.disco(*rot([(-20, -6)])[0], 4 * s, fill, borde, grosor)
    elif especie == "edmontosaurio":       # tres dedos anchos y romos, como un trébol
        p.poli(dedo(0, 14, 22, 22, 0), fill, borde, grosor)
        for dx, a in ((-24, -0.5), (0, 0), (24, 0.5)):
            p.poli(dedo(dx * 0.9, -26, 22, 15, a), fill, borde, grosor)
    elif especie == "triceratops":         # pata redonda con cinco deditos cortos delante
        p.poli(dedo(0, 6, 34, 36, 0), fill, borde, grosor)
        for k in range(5):
            a = -0.9 + k * 0.45
            p.poli(dedo(math.sin(a) * 34, -32 * math.cos(a) - 6, 9, 7, a), fill, borde, grosor)
    else:                                  # anquilosaurio: ancha, en media luna, con cuatro uñas
        p.poli(dedo(0, 0, 26, 42, 0), fill, borde, grosor)
        for k in range(4):
            a = -0.75 + k * 0.5
            p.poli(dedo(math.sin(a) * 40, -30 * math.cos(a) - 2, 8, 8, a), fill, borde, grosor)


def barro_huellas():
    h = I.HUELLAS
    p = pagina("EL BARRO DEL VADO", "tal como lo encontrasteis esta mañana", (200, 168, 124), BARRO2)
    p.rect(40, 140, W - 40, H - 60, (176, 138, 96), BARRO2, 3)
    # una pisada de cada especie, dibujadas en el orden en que pasaron: la de encima tapa a la de debajo.
    # Las posiciones se buscan para que se pisen justo las parejas de la instancia (y ninguna otra).
    tonos = [(112, 76, 46), (84, 58, 36), (126, 90, 56), (98, 64, 40), (74, 50, 30)]
    for k, ((x, y, ang), esp) in enumerate(zip(_sitios_huellas(), h["orden"])):
        huella(p, esp, x, y, 1.7, ang, tonos[k], (222, 190, 140))
    return p.final()


ANG_HUELLA = {"triceratops": 0.2, "tiranosaurio": -0.25, "anquilosaurio": 0.1, "edmontosaurio": -0.15, "velociraptor": 0.3}


def _mascara(esp):
    m = Hoja(W, H, (0, 0, 0))
    huella(m, esp, W / 2, H / 2, 1.7, ANG_HUELLA[esp], (255, 255, 255), (255, 255, 255))
    return np.asarray(m.final().convert("L").resize((W // 3, H // 3))) > 128


def _mueve(m, dx, dy):
    return np.roll(np.roll(m, int(dy // 3), axis=0), int(dx // 3), axis=1)


def _sitios_huellas():
    h = I.HUELLAS
    orden = h["orden"]
    quiero = {frozenset(par) for par in h["encima"]}
    base = {e: _mascara(e) for e in orden}
    rng = random.Random(7)
    area = lambda m: int(m.sum())

    def cabe(k, sit, mas):
        for i in range(k):
            solape = int((mas[i] & mas[k]).sum())
            if frozenset((orden[i], orden[k])) in quiero:
                if not 40 <= solape <= 0.18 * min(area(mas[i]), area(mas[k])):
                    return False
            elif solape:
                return False
        return True

    for _ in range(300):
        sit, mas = [], []
        for k, e in enumerate(orden):
            for _ in range(400):
                if k == 0:
                    x, y = rng.uniform(220, 410), rng.uniform(320, 640)
                else:
                    # cerca de una huella con la que tenga que tocarse
                    j = next(i for i in range(k) if frozenset((orden[i], e)) in quiero)
                    ang = rng.uniform(0, 2 * math.pi)
                    r = rng.uniform(85, 150)
                    x, y = sit[j][0] + math.cos(ang) * r, sit[j][1] + math.sin(ang) * r
                if not (150 <= x <= 480 and 260 <= y <= 700):
                    continue
                m = _mueve(base[e], x - W / 2, y - H / 2)
                if cabe(k, sit + [(x, y)], mas + [m]):
                    sit.append((x, y))
                    mas.append(m)
                    break
            else:
                break
        if len(sit) == len(orden):
            return [(x, y, ANG_HUELLA[e]) for e, (x, y) in zip(orden, sit)]
    raise SystemExit("sin sitio para las huellas")


def guia_huellas():
    p = pagina("GUÍA DE HUELLAS", "de la doctora Ibarra", PAPEL, BARRO2)
    nombres = {"triceratops": "Triceratops", "tiranosaurio": "Tiranosaurio", "anquilosaurio": "Anquilosaurio",
               "edmontosaurio": "Edmontosaurio", "velociraptor": "Velociraptor"}
    for k, esp in enumerate(I.ESPECIES):
        y = 190 + k * 108
        huella(p, esp, 170, y, 0.8)
        p.texto((300, y), nombres[esp], "texto", 26, TINTA, "lm")
    for k, v in enumerate(["«El barro no olvida: lo que pisa después se queda encima.",
                           "El último en cruzar el vado se llevó lo que buscáis pegado a la pata.»"]):
        p.texto((W / 2, 740 + k * 34), v, "texto2", 17, TINTA)
    return p.final()


# ------------------------------------------------------------------ manada (dos mitades: cabezas arriba, patas abajo)
def manada():
    m = I.MANADA
    p = Hoja(W, H * 2, (210, 226, 190))
    p.texto((W / 2, 70), "LA MANADA DEL ABREVADERO", "cartel", 32, TINTA)
    p.texto((W / 2, 108), "lo que asomaba por encima y por debajo de los helechos", "texto2", 19, TINTA)
    rng = random.Random(19)
    cab = m["cabezas"]
    # cabezas: siluetas iguales (cuello y cabeza) a distintas alturas; sin cuernos ni dientes que delaten la especie
    for k in range(cab):
        x = 60 + (k % 7) * 80 + rng.uniform(-10, 10)
        y = 300 + (k // 7) * 190 + rng.uniform(-30, 30)
        p.linea([(x, H - 20), (x + 6, y + 30)], (60, 80, 50), 16)
        p.elip(x - 6, y, x + 46, y + 34, (60, 80, 50))
        p.disco(x + 30, y + 12, 4, BLANCO)
    # helechos: franja que lo tapa todo en la junta
    for k in range(40):
        x = rng.uniform(0, W)
        for a in range(-3, 4):
            p.linea([(x, H + 120), (x + a * 26, H - 120 + abs(a) * 10)], VERDE, 8)
    p.rect(0, H - 110, W, H + 110, VERDE, None)
    for k in range(60):
        x = rng.uniform(0, W)
        y = rng.uniform(H - 120, H + 110)
        p.elip(x - 30, y - 10, x + 30, y + 10, VERDE2)
    # patas: columnas, sin cuerpo ni pies que distingan
    patas = m["patas"]
    xs = sorted(rng.sample(range(30, W - 30, 13), patas))
    for k, x in enumerate(xs):
        p.linea([(x, H + 110), (x + rng.uniform(-4, 4), H + 330 + rng.uniform(-25, 25))], (60, 80, 50), 9)
    p.rect(0, H + 340, W, H * 2, (170, 140, 100), None)
    return p.final()


# ------------------------------------------------------------------ nidos: vistas desde el oeste (filas) y desde el sur (columnas)
def nidos_vista(eje):
    n = I.NIDOS
    if eje == "filas":
        p = pagina("DESDE EL ACANTILADO OESTE", "huevos que se veían en cada fila de la playa", PAPEL, OCRE)
        cuentas = n["filas"]
    else:
        p = pagina("DESDE LA DUNA DEL SUR", "huevos que se veían en cada columna de la playa", PAPEL, OCRE)
        cuentas = n["cols"]
    for k, c in enumerate(cuentas):
        if eje == "filas":
            y = 200 + k * 100
            p.texto((90, y), str(k + 1), "cartel", 30, TINTA)
            p.linea([(120, y), (W - 60, y)], (190, 170, 130), 2)
            for j in range(c):
                p.elip(170 + j * 70, y - 30, 220 + j * 70, y + 30, BLANCO, TINTA, 2)
            if c == 0:
                p.texto((200, y), "—", "texto", 28, TINTA)
        else:
            x = 110 + k * 80
            p.texto((x, 200), LETRAS[k], "cartel", 30, TINTA)
            p.linea([(x, 230), (x, 760)], (190, 170, 130), 2)
            for j in range(c):
                p.elip(x - 25, 260 + j * 80, x + 25, 320 + j * 80, BLANCO, TINTA, 2)
            if c == 0:
                p.texto((x, 290), "—", "texto", 28, TINTA)
    return p.final()


def costumbre_nidos():
    p = pagina("LAS MADRES MAIASAURA", "lo que anotó la doctora", PAPEL, OCRE)
    versos(p, ["«Cada madre cava su nido", "pegado a su helecho,", "de lado, nunca en diagonal:", "un helecho, un nido.",
               "Y ninguna soporta a otra", "en las ocho casillas de alrededor.»"], 230, 60, 27)
    return p.final()


# ------------------------------------------------------------------ cráter: mapa del valle (dos mitades) y vigías
def mapa_valle():
    c = I.CRATER
    n = c["n"]
    p = Hoja(W * 2, H, (214, 222, 186))
    p.texto((W, 64), "EL VALLE, DE LADERA A LADERA", "cartel", 34, TINTA)
    lado = 84
    x0, y0 = (W * 2 - n * lado) / 2, 150
    for y in range(n):
        for x in range(n):
            p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, (200, 214, 170), (160, 176, 130), 1)
    for k in range(n):
        p.texto((x0 + k * lado + lado / 2, y0 - 22), LETRAS[k], "texto", 22, TINTA)
        p.texto((x0 - 24, y0 + k * lado + lado / 2), str(k + 1), "texto", 22, TINTA)
    icono = {"Roca del Cuerno": "roca", "Árbol Hueco": "arbol", "Colina Pelada": "colina"}
    for v in c["vigias"]:
        px, py = x0 + v["x"] * lado + lado / 2, y0 + v["y"] * lado + lado / 2
        if icono[v["nombre"]] == "roca":
            p.poli([(px - 34, py + 30), (px - 10, py - 30), (px + 6, py - 6), (px + 34, py + 30)], GRIS, TINTA, 2)
        elif icono[v["nombre"]] == "arbol":
            p.rect(px - 7, py, px + 7, py + 34, BARRO2)
            p.disco(px, py - 10, 28, VERDE, TINTA, 2)
            p.disco(px, py - 8, 8, BARRO2)
        else:
            p.elip(px - 40, py - 20, px + 40, py + 36, (190, 170, 120), TINTA, 2)
        p.texto((px, py + 40), v["nombre"], "texto2", 15, TINTA)
    # rosa de los vientos
    rx, ry = x0 + n * lado + 80, y0 + 90
    p.poli([(rx, ry - 50), (rx + 10, ry), (rx, ry + 50), (rx - 10, ry)], TINTA)
    p.texto((rx, ry - 66), "N", "cartel", 26, TINTA)
    return p.final()


FLECHA = {"N": 0, "NE": 45, "E": 90, "SE": 135, "S": 180, "SO": 225, "O": 270, "NO": 315}


def rosa(p, cx, cy, rumbo, r=110):
    p.disco(cx, cy, r, BLANCO, TINTA, 3)
    for k, l in enumerate(["N", "E", "S", "O"]):
        a = math.radians(k * 90)
        p.texto((cx + math.sin(a) * (r - 22), cy - math.cos(a) * (r - 22)), l, "texto", 20, TINTA)
    a = math.radians(FLECHA[rumbo])
    tip = (cx + math.sin(a) * (r - 40), cy - math.cos(a) * (r - 40))
    p.linea([(cx, cy), tip], ROJO, 8)
    b1 = (tip[0] - math.sin(a + 0.5) * 22, tip[1] + math.cos(a + 0.5) * 22)
    b2 = (tip[0] - math.sin(a - 0.5) * 22, tip[1] + math.cos(a - 0.5) * 22)
    p.poli([tip, b1, b2], ROJO)
    p.disco(cx, cy, 8, TINTA)


def vigias():
    p = pagina("LOS TRES VIGÍAS", "lo que vieron anoche, cada uno desde su sitio", PAPEL, AZUL)
    for k, v in enumerate(I.CRATER["vigias"]):
        cx, cy = (180, 300) if k == 0 else (450, 300) if k == 1 else (W / 2, 590)
        rosa(p, cx, cy, v["rumbo"], 105)
        p.texto((cx, cy + 128), "desde " + v["nombre"], "texto2", 20, TINTA)
    p.texto((W / 2, 800), "«Vi caer la piedra de fuego justo hacia donde apunta la flecha.»", "texto2", 17, TINTA)
    return p.final()


# ------------------------------------------------------------------ lava: alturas (dos mitades) y la canción
def mapa_alturas():
    lv = I.LAVA
    n = lv["n"]
    p = Hoja(W * 2, H, (226, 214, 190))
    p.texto((W, 64), "LA LADERA DEL VOLCÁN", "cartel", 34, TINTA)
    p.texto((W, 102), "metros sobre el mar, apuntados por la doctora", "texto2", 20, TINTA)
    lado = 116
    x0, y0 = (W * 2 - n * lado) / 2, 160
    alt = lv["alturas"]
    lo, hi = min(min(f) for f in alt), max(max(f) for f in alt)
    for y in range(n):
        for x in range(n):
            t = (alt[y][x] - lo) / (hi - lo)
            col = tuple(int(a + (b - a) * t) for a, b in zip((190, 210, 160), (150, 110, 80)))
            p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, col, TINTA, 2)
            p.texto((x0 + x * lado + lado / 2, y0 + y * lado + lado / 2), str(alt[y][x]), "texto", 26, TINTA)
    fx, fy = lv["fuente"]
    p.poli([(x0 + fx * lado + 40, y0 - 4), (x0 + fx * lado + lado / 2, y0 - 44), (x0 + fx * lado + lado - 40, y0 - 4)], NARANJA, TINTA, 2)
    nx, ny = lv["nido"]
    cx, cy = x0 + nx * lado + lado / 2, y0 + ny * lado + lado - 24
    for k in range(3):
        p.elip(cx - 40 + k * 26, cy - 14, cx - 20 + k * 26, cy + 12, BLANCO, TINTA, 2)
    return p.final()


def cancion_lava():
    p = pagina("LA CANCIÓN DE LOS VOLCANES", "que cantaba la doctora para no olvidarla", PAPEL, NARANJA)
    versos(p, ["«La lava no piensa: baja.", "De cada casilla, a la vecina", "más honda de las cuatro,", "nunca en diagonal.",
               "Cuando ya no hay nada más bajo,", "se para y se enfría.", "Y una roca no la deja pasar.»"], 220, 60, 26)
    return p.final()


# ------------------------------------------------------------------ senderos (dos mitades) y la costumbre de la manada
POS_CLAROS = {"N": (0.12, 0.30), "H": (0.32, 0.18), "L": (0.30, 0.62), "C": (0.55, 0.40), "V": (0.55, 0.82), "P": (0.80, 0.62),
              "R": (0.86, 0.22)}


def mapa_senderos():
    s = I.SENDEROS
    p = Hoja(W * 2, H, (206, 220, 176))
    p.texto((W, 64), "LOS SENDEROS DEL VALLE", "cartel", 34, TINTA)
    X = lambda k: 80 + POS_CLAROS[k][0] * (W * 2 - 160)
    Y = lambda k: 150 + POS_CLAROS[k][1] * (H - 220)
    for a, b in s["senderos"]:
        mx, my = (X(a) + X(b)) / 2, (Y(a) + Y(b)) / 2 + 30
        pts = [(X(a) + (mx - X(a)) * t * 2 if t < 0.5 else mx + (X(b) - mx) * (t - 0.5) * 2,
                Y(a) + (my - Y(a)) * t * 2 if t < 0.5 else my + (Y(b) - my) * (t - 0.5) * 2) for t in [k / 20 for k in range(21)]]
        p.linea(pts, (150, 120, 80), 9)
    for k, nom in s["claros"].items():
        p.disco(X(k), Y(k), 46, (236, 228, 196), TINTA, 3)
        p.texto((X(k), Y(k)), nom, "texto2", 17, TINTA)
    return p.final()


def costumbre_manada():
    p = pagina("LA RUTA DE LOS EDMONTOSAURIOS", "cuaderno de la doctora", PAPEL, VERDE)
    versos(p, ["«Salen de la Roca Alta al alba", "y no dejan un sendero sin pisar:", "los recorren todos, de claro en claro,",
               "pero ninguno dos veces.", "Quien les siga el paso", "llegará donde duermen.»"], 230, 60, 26)
    return p.final()


# ------------------------------------------------------------------ árbol de rasgos y fichas
def icono_rasgo(p, rasgo, cx, cy, r=26):
    if rasgo == "patas":                       # una pata con dedos
        p.linea([(cx, cy - r), (cx - 4, cy + r * 0.6)], TINTA, 6)
        for a in (-0.6, 0, 0.6):
            p.linea([(cx - 4, cy + r * 0.6), (cx - 4 + math.sin(a) * 16, cy + r * 0.6 + math.cos(a) * 12)], TINTA, 4)
    elif rasgo == "patas rectas bajo el cuerpo":   # cuerpo con las patas verticales debajo
        p.elip(cx - r, cy - r * 0.7, cx + r, cy, BLANCO, TINTA, 2)
        for dx in (-r * 0.5, r * 0.5):
            p.linea([(cx + dx, cy), (cx + dx, cy + r)], TINTA, 5)
    elif rasgo == "plumas":
        p.elip(cx - 8, cy - r, cx + 8, cy + r, OCRE, TINTA, 2)
        p.linea([(cx, cy - r), (cx, cy + r + 6)], TINTA, 2)
    elif rasgo == "alas":
        p.poli([(cx - r, cy + 8), (cx, cy - r), (cx + r, cy + 8), (cx, cy)], AZUL, TINTA, 2)


def arbol():
    a = I.ARBOL
    p = pagina("EL ÁRBOL DE LA DOCTORA", "quién es pariente de quién", PAPEL, VERDE)
    xs = [110 + k * 102 for k in range(5)]
    arriba, x0, y0 = 250, 110, 780
    nodo = [(x0 + (xs[4] - x0) * j / 4, y0 + (arriba - y0) * j / 4) for j in range(5)]
    p.linea([nodo[0], nodo[4]], TINTA, 6)
    for j in range(5):
        p.linea([nodo[j], (xs[j], arriba)], TINTA, 6)
        p.disco(xs[j], arriba - 30, 24, BLANCO, TINTA, 3)
        p.texto((xs[j], arriba - 30), str(j + 1), "texto", 22, TINTA)
    for i in range(4):
        mx, my = (nodo[i][0] + nodo[i + 1][0]) / 2, (nodo[i][1] + nodo[i + 1][1]) / 2
        p.linea([(mx - 14, my - 14), (mx + 14, my + 14)], ROJO, 5)
        icono_rasgo(p, a["rasgos"][i], mx + 58, my + 40, 22)
    return p.final()


def silueta(p, animal, cx, cy, s=1.0):
    def e(a, b, c, d, col=(90, 90, 80)):
        p.elip(cx + a * s, cy + b * s, cx + c * s, cy + d * s, col, TINTA, 2)
    if animal == "pez":
        e(-60, -22, 50, 22)
        p.poli([(cx + 46 * s, cy), (cx + 80 * s, cy - 24 * s), (cx + 80 * s, cy + 24 * s)], (90, 90, 80), TINTA, 2)
    elif animal == "cocodrilo":
        e(-70, -14, 60, 14)
        p.poli([(cx + 56 * s, cy - 6 * s), (cx + 96 * s, cy), (cx + 56 * s, cy + 6 * s)], (90, 90, 80), TINTA, 2)
        for dx in (-40, 30):
            p.linea([(cx + dx * s, cy + 10 * s), (cx + (dx - 8) * s, cy + 30 * s)], TINTA, 5)
    elif animal == "triceratops":
        e(-60, -30, 40, 26)
        e(30, -36, 76, 6)
        for a in (-26, -10):
            p.linea([(cx + 60 * s, cy + a * s), (cx + 92 * s, cy + (a - 14) * s)], TINTA, 4)
        for dx in (-40, -10, 10, 30):
            p.linea([(cx + dx * s, cy + 20 * s), (cx + dx * s, cy + 46 * s)], TINTA, 7)
    elif animal == "velociraptor":
        e(-30, -16, 30, 16)
        e(24, -34, 56, -14)
        p.linea([(cx - 28 * s, cy), (cx - 80 * s, cy - 10 * s)], TINTA, 5)
        for dx in (-6, 10):
            p.linea([(cx + dx * s, cy + 12 * s), (cx + (dx - 4) * s, cy + 48 * s)], TINTA, 5)
        for k in range(5):
            p.linea([(cx - 20 * s + k * 8 * s, cy - 14 * s), (cx - 26 * s + k * 8 * s, cy - 28 * s)], OCRE, 3)
    else:  # ave primitiva
        e(-24, -16, 24, 16)
        e(16, -30, 40, -12)
        p.poli([(cx - 10 * s, cy - 6 * s), (cx - 70 * s, cy - 50 * s), (cx - 50 * s, cy - 6 * s)], AZUL, TINTA, 2)
        p.linea([(cx - 22 * s, cy), (cx - 60 * s, cy + 10 * s)], TINTA, 4)
        for dx in (-4, 8):
            p.linea([(cx + dx * s, cy + 12 * s), (cx + dx * s, cy + 40 * s)], TINTA, 4)


def fichas(animales, titulo):
    a = I.ARBOL
    p = pagina(titulo, "dibujos y esqueletos de la doctora", PAPEL, VERDE)
    for k, an in enumerate(animales):
        y = 260 + k * 200 if len(animales) < 4 else 220 + k * 160
        silueta(p, an, 200, y, 1.0)
        for j, r in enumerate([r for r in a["rasgos"] if r in a["animales"][an]]):
            icono_rasgo(p, r, 360 + j * 62, y, 22)
        if not a["animales"][an]:
            p.texto((420, y), "—", "texto", 28, TINTA)
    return p.final()


# ------------------------------------------------------------------ corral
def red_comida():
    c = I.CORRAL
    p = pagina("QUIÉN SE COME A QUIÉN", "dibujado por la doctora en la puerta del corral", PAPEL, ROJO)
    pos = {"tiranosaurio": (W / 2, 230), "velociraptor": (W / 2, 470), "edmontosaurio": (150, 430), "protoceratops": (470, 650),
           "compsognato": (170, 690), "triceratops": (480, 300)}
    nom = {"tiranosaurio": "Tiranosaurio", "velociraptor": "Velociraptor", "edmontosaurio": "Edmontosaurio", "protoceratops": "Protoceratops",
           "compsognato": "Compsognato", "triceratops": "Triceratops"}
    for a, b in c["come"]:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        d = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        s, e = (x1 + ux * 70, y1 + uy * 40), (x2 - ux * 76, y2 - uy * 44)
        p.linea([s, e], ROJO, 5)
        p.poli([e, (e[0] - ux * 22 - uy * 12, e[1] - uy * 22 + ux * 12), (e[0] - ux * 22 + uy * 12, e[1] - uy * 22 - ux * 12)], ROJO)
    for k, (x, y) in pos.items():
        p.elip(x - 88, y - 34, x + 88, y + 34, BLANCO, TINTA, 2)
        p.texto((x, y), nom[k], "texto2", 20, TINTA)
    p.texto((W / 2, 800), "La flecha va del que come al que se come.", "texto2", 19, TINTA)
    return p.final()


def plano_corral():
    c = I.CORRAL
    p = pagina("EL CORRAL DE LA DOCTORA", "seis cercados, una cerca entre cada dos", PAPEL, ROJO)
    lado = 170
    x0, y0 = (W - 3 * lado) / 2, 260
    for y in range(c["filas"]):
        for x in range(c["cols"]):
            p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, (214, 196, 150), BARRO2, 6)
    for a, (x, y) in c["fijos"].items():
        silueta_corral(p, a, x0 + x * lado + lado / 2, y0 + y * lado + lado / 2)
    versos(p, ["«Que nadie duerma pared con pared", "con quien se lo quiere comer.»"], 700, 46, 24)
    return p.final()


def silueta_corral(p, animal, cx, cy):
    p.elip(cx - 30, cy - 12, cx + 20, cy + 12, (90, 90, 80), TINTA, 2)
    p.disco(cx + 26, cy - 14, 10, (90, 90, 80), TINTA, 2)
    p.linea([(cx - 28, cy), (cx - 56, cy - 8)], TINTA, 4)
    for dx in (-8, 6):
        p.linea([(cx + dx, cy + 10), (cx + dx - 2, cy + 34)], TINTA, 4)
    p.texto((cx, cy + 56), "compsognato", "texto2", 17, TINTA)


# ------------------------------------------------------------------ barro: la orilla y la advertencia
def orilla():
    b = I.BARRO
    n = b["n"]
    p = pagina("LA CIÉNAGA DESDE EL ÁRBOL", "dibujo de la doctora", PAPEL, BARRO2)
    lado = 72
    x0, y0 = (W - n * lado) / 2, 200
    rocas = {tuple(r) for r in b["rocas"]}
    for y in range(n):
        for x in range(n):
            p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, (160, 124, 86), (130, 96, 64), 1)
            if (x, y) in rocas:
                p.poli([(x0 + x * lado + 10, y0 + y * lado + lado - 8), (x0 + x * lado + 26, y0 + y * lado + 12),
                        (x0 + x * lado + 50, y0 + y * lado + 18), (x0 + x * lado + lado - 8, y0 + y * lado + lado - 8)], GRIS, TINTA, 2)
    cx, cy = b["cueva"]
    px, py = x0 + cx * lado, y0 + cy * lado
    p.elip(px + 10, py + 14, px + lado - 10, py + lado - 4, (30, 24, 20), TINTA, 2)
    sx, sy = b["inicio"]
    px, py = x0 + sx * lado, y0 + sy * lado
    p.rect(px + 10, py + 22, px + lado - 10, py + lado - 22, (170, 120, 60), TINTA, 2)
    p.texto((W / 2, y0 + n * lado + 50), "la balsa, en la orilla · la boca de la cueva, en el barro", "texto2", 19, TINTA)
    return p.final()


def advertencia_balsa():
    p = pagina("GRABADO EN LA BALSA", None, PAPEL, BARRO2)
    versos(p, ["«En este barro no hay remo que valga:", "empujad y la balsa resbala", "en línea recta, sin frenar,", "hasta que choca con una roca",
               "o con la orilla.", "Pasar por encima de la cueva no sirve:", "hay que pararse en su boca.»"], 220, 58, 25)
    return p.final()


# ------------------------------------------------------------------ planear: mapa de térmicas y la costumbre del pterosaurio
def mapa_termicas():
    pl = I.PLANEAR
    n = pl["n"]
    p = pagina("EL CIELO DEL ACANTILADO", "dibujado desde lo alto por la doctora", (214, 230, 240), AZUL)
    lado = 88
    x0, y0 = (W - n * lado) / 2, 190
    montes = {tuple(m) for m in pl["montes"]}
    term = {(x, y): k for x, y, k in pl["termicas"]}
    for y in range(n):
        for x in range(n):
            px, py = x0 + x * lado, y0 + y * lado
            p.rect(px, py, px + lado, py + lado, (200, 222, 236), (170, 196, 214), 1)
            if (x, y) in montes:
                p.poli([(px + 8, py + lado - 8), (px + lado / 2, py + 10), (px + lado - 8, py + lado - 8)], GRIS, TINTA, 2)
                p.poli([(px + lado / 2 - 12, py + 30), (px + lado / 2, py + 10), (px + lado / 2 + 12, py + 30)], BLANCO)
            if (x, y) in term:
                # una vuelta de remolino por cada palmo que sube
                for j in range(term[(x, y)]):
                    cx = px + lado / 2 + (j % 2) * 18 - 9
                    cy = py + 18 + j * 17
                    p.elip(cx - 14, cy - 7, cx + 14, cy + 7, None, NARANJA, 3)
    sx, sy = pl["inicio"]
    px, py = x0 + sx * lado, y0 + sy * lado
    p.poli([(px + 6, py + lado - 6), (px + 6, py + 20), (px + lado - 30, py + 20), (px + lado - 10, py + lado - 6)], BARRO2, TINTA, 2)
    fx, fy = pl["nido"]
    cx, cy = x0 + fx * lado + lado / 2, y0 + fy * lado + lado / 2
    p.elip(cx - 30, cy - 10, cx + 30, cy + 18, (150, 110, 60), TINTA, 2)
    for k in range(3):
        p.disco(cx - 14 + k * 14, cy - 2, 7, BLANCO, TINTA, 1)
    p.texto((W / 2, y0 + n * lado + 40), f"Al saltar del acantilado: {pl['altura']} palmos de altura.", "texto2", 21, TINTA)
    return p.final()


def costumbre_ptero():
    p = pagina("CÓMO PLANEA EL QUETZAL", "el pterosaurio de la doctora", PAPEL, AZUL)
    versos(p, ["«Cada casilla que avanza,", "un palmo que baja.", "Cada remolino de aire caliente", "lo sube un palmo por vuelta,",
               "pero solo la primera vez.", "Las montañas no se cruzan.", "Si llega al suelo, se acabó el vuelo.»"], 220, 58, 26)
    return p.final()


# ------------------------------------------------------------------ anillos
ANCHO = {"f": 6, "m": 14, "g": 26}


def tronco(i, titulo, sub):
    a = I.ANILLOS
    p = pagina(titulo, sub, PAPEL, BARRO2)
    t = a["troncos"][i]
    # testigo: una tira de madera con los anillos del más viejo (izquierda) al más nuevo (derecha)
    x = 70
    y0, y1 = 300, 420
    total = sum(ANCHO[c] + 6 for c in t)
    esc = (W - 140) / total
    p.rect(60, y0 - 10, W - 60, y1 + 10, (196, 160, 110), BARRO2, 3)
    for c in t:
        w = ANCHO[c] * esc
        p.rect(x, y0, x + w, y1, (226, 196, 140))
        x += w
        p.rect(x, y0, x + 6 * esc, y1, BARRO2)
        x += 6 * esc
    p.texto((90, y1 + 50), "corazón", "texto2", 18, TINTA)
    p.texto((W - 90, y1 + 50), "corteza", "texto2", 18, TINTA)
    if i == 0:
        versos(p, ["Murió quemado en la gran erupción,", "el día que llegué a este valle."], 560, 50, 24)
    elif i == 2:
        versos(p, ["Lo tumbó esta mañana", "la primera piedra de fuego."], 560, 50, 24)
    else:
        versos(p, ["Arrastrado por el río.", "Ni idea de cuándo vivió."], 560, 50, 24)
    return p.final()


def main(carpeta="juegos/aventuras-ca/dinosaurios"):
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    g = lambda k, im: ruido(im, int(k)).save(os.path.join(arte, f"{k}.png"))

    def mosaico(nombre, im, filas, cols, cartas):
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))
        for pieza, k in zip(cortar(im, filas, cols), cartas):
            pieza.save(os.path.join(arte, f"{k}.png"))
    g("16", barro_huellas())
    g("18", guia_huellas())
    mosaico("manada", manada(), 2, 1, ("19", "21"))
    g("41", nidos_vista("filas"))
    g("43", nidos_vista("cols"))
    g("45", costumbre_nidos())
    mosaico("valle", mapa_valle(), 1, 2, ("42", "49"))
    g("53", vigias())
    mosaico("ladera", mapa_alturas(), 1, 2, ("54", "55"))
    g("59", cancion_lava())
    mosaico("senderos", mapa_senderos(), 1, 2, ("37", "39"))
    g("33", costumbre_manada())
    g("26", arbol())
    g("61", fichas(["triceratops", "pez", "ave primitiva"], "FICHAS DE LA DOCTORA (I)"))
    g("63", fichas(["velociraptor", "cocodrilo"], "FICHAS DE LA DOCTORA (II)"))
    g("70", red_comida())
    g("71", plano_corral())
    g("75", mapa_termicas())
    g("79", costumbre_ptero())
    g("66", orilla())
    g("67", advertencia_balsa())
    g("86", tronco(0, "TRONCO FÓSIL DEL VOLCÁN", "corte del tronco quemado"))
    g("87", tronco(1, "TRONCO FÓSIL DEL RÍO", "corte de un tronco arrastrado"))
    g("76", tronco(2, "TRONCO DE LA ENTRADA", "corte del tronco caído esta mañana"))
    inyectar(carpeta)
    print("láminas de Dinosaurios escritas en", arte)


DATOS_APPS = {"14-huellas.js": "huellas", "20-manada.js": "manada", "40-nidos.js": "nidos", "48-crater.js": "crater", "52-lava.js": "lava",
              "46-senderos.js": "senderos", "51-arbol.js": "arbol", "69-corral.js": "corral", "72-planear.js": "planear", "64-barro.js": "barro",
              "85-anillos.js": "anillos"}


def inyectar(carpeta):
    """Mete los datos de las instancias en las apps (bloque /*DATOS*/.../*FIN*/)."""
    for app, clave in DATOS_APPS.items():
        ruta = os.path.join(carpeta, "minijuegos", app)
        txt = open(ruta, encoding="utf-8").read() if os.path.exists(ruta) else ""
        if "/*DATOS*/" not in txt:
            continue
        a, b = txt.index("/*DATOS*/") + len("/*DATOS*/"), txt.index("/*FIN*/")
        open(ruta, "w", encoding="utf-8", newline="\n").write(txt[:a] + json.dumps(I.TODO[clave], ensure_ascii=False) + txt[b:])


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

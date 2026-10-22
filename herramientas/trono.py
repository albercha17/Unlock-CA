"""Láminas de «Reino de Hielo y Fuego: La Corona del Dragón» (versión de 60 cartas, 21 oct 2026). Todas las pistas son dibujos o acertijos:
ninguna carta escribe la respuesta ni explica cómo se resuelve su puzle. Datos de herramientas/instancias_trono.py.

  16 el encargo del senescal (jarras) · 18 el acertijo de la muralla · 19 y 21 la muralla (dos mitades)
  41 el mapa del reino · 43 las leguas entre fortalezas · 45 el acertijo de los cuervos
  42 la carta de la prisionera · 49 el cuadrado de la clave · 53 la regla del cuadrado
  54 las reglas del juego de las piedras · 55 las partidas anteriores · 59 el dicho del carcelero
  37 y 39 los castillos (dos mitades) · 33 el acertijo de los puentes
  26 las leyes del reino · 61 y 63 el árbol del rey Aerion (dos mitades)
  70 y 71 el tablero de las casas (dos mitades) · 66 y 67 las pistas del tapiz (filas y columnas)
  75 las torres de hielo · 79 la regla del reloj de arena · 86 y 87 la profecía del maestre
Uso (desde la raíz del repo):  python herramientas/trono.py [carpeta_juego]
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
import instancias_trono as I  # noqa: E402

W, H = 630, 882
HIELO = (214, 228, 238)
ACERO = (64, 80, 96)
AZUL = (60, 110, 170)
FUEGO = (214, 100, 40)
NIEVE = (246, 250, 252)
OSCURO = (30, 40, 52)
ROJO = (176, 50, 40)
ORO = (214, 170, 60)
GRIS = (130, 142, 154)
CASAS = [(120, 120, 130), (200, 150, 40), (40, 110, 130), (180, 60, 80), (230, 130, 30), (70, 140, 170)]


def ruido(im, s, f=2.5):
    a = np.asarray(im).astype(np.int16)
    a = a + np.random.default_rng(s).normal(0, f, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def pagina(titulo, sub=None, fondo=HIELO, borde=ACERO, w=W, h=H):
    p = Hoja(w, h, fondo)
    p.rect(16, 16, w - 16, h - 16, None, borde, 6)
    p.rect(28, 28, w - 28, h - 28, None, borde, 2)
    p.texto((w / 2 + 26, 70), titulo, "cartel", 32, OSCURO)
    if sub:
        p.texto((w / 2 + 26, 108), sub, "texto2", 21, OSCURO)
    return p


def versos(p, lineas, y0=220, paso=56, tam=27, x=W / 2):
    for k, v in enumerate(lineas):
        p.texto((x, y0 + k * paso), v, "texto2", tam, OSCURO)


def ancha(titulo, borde=ACERO):
    p = Hoja(W * 2, H, HIELO)
    p.rect(16, 16, W * 2 - 16, H - 16, None, borde, 6)
    p.rect(28, 28, W * 2 - 28, H - 28, None, borde, 2)
    p.texto((W, 66), titulo, "cartel", 34, OSCURO)
    return p


def figura(p, nombre, cx, cy, tam, color=OSCURO, fondo=NIEVE):
    s = tam / 100
    pt = lambda q: (cx + (q[0] - 50) * s, cy + (q[1] - 50) * s)
    for e in I.CASAS_FIG[nombre]:
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


# ------------------------------------------------------------------ 16: las jarras
def jarra(p, x, y, cap, ancho):
    alto = cap * 30
    p.poli([(x - ancho / 2, y - alto), (x + ancho / 2, y - alto), (x + ancho / 2 - 6, y), (x - ancho / 2 + 6, y)], (200, 170, 110), OSCURO, 4)
    for k in range(1, cap):
        yy = y - k * 30
        p.linea([(x - ancho / 2, yy), (x - ancho / 2 + 18, yy)], OSCURO, 3)


def encargo_jarras():
    d = I.JARRAS
    p = pagina("EL ENCARGO DEL SENESCAL", "dos jarras y un cuenco", HIELO, ACERO)
    jarra(p, 150, 720, d["A"], 120)
    jarra(p, 330, 720, d["B"], 120)
    # el cuenco del rey, con la medida que se quiere
    p.poli([(480, 660), (590, 660), (572, 720), (498, 720)], (150, 110, 70), OSCURO, 4)
    for k in range(d["objetivo"]):
        p.linea([(487, 720 - (k + 1) * 6), (583, 720 - (k + 1) * 6)], FUEGO, 3)
    p.texto((150, 760), "jarra I", "texto", 22, OSCURO)
    p.texto((330, 760), "jarra II", "texto", 22, OSCURO)
    p.texto((535, 760), "el cuenco", "texto", 20, OSCURO)
    versos(p, ["«Cada raya de las jarras vale", "un cuenco pequeño de hidromiel.", "En el cuenco del rey, quiero", "justo lo que marca el fuego: ni más ni menos.»"], 160, 40, 20)
    return p.final()


# ------------------------------------------------------------------ 18, 19/21: la muralla
def acertijo_muralla():
    p = pagina("EL ACERTIJO DE LA MURALLA", "pintado en la puerta de la torre", HIELO, ACERO)
    versos(p, ["«Ocho centinelas, ocho torres,", "y ninguno ve a otro.", "", "Un centinela ve en línea recta:",
               "por su fila, por su columna", "y por las dos diagonales,", "hasta donde acaba el muro.", "", "Tres ya están puestos. Poned los demás.»"], 190, 52, 24)
    return p.final()


def muralla():
    d = I.CENTINELAS
    n = d["n"]
    p = Hoja(W, H * 2, HIELO)
    p.rect(16, 16, W - 16, H * 2 - 16, None, ACERO, 6)
    p.rect(28, 28, W - 28, H * 2 - 28, None, ACERO, 2)
    p.texto((W / 2 + 26, 70), "LA MURALLA DE PIEDRA NEGRA", "cartel", 30, OSCURO)
    lado = 70
    x0, y0 = (W - n * lado) / 2 + 12, 882 - 4 * lado
    for y in range(n):
        for x in range(n):
            col = (190, 205, 218) if (x + y) % 2 == 0 else (150, 170, 190)
            p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, col, ACERO, 2)
    for k in range(n):
        p.texto((x0 + k * lado + lado / 2, y0 - 14), "ABCDEFGH"[k], "texto", 20, OSCURO)
        p.texto((x0 - 20, y0 + k * lado + lado / 2), str(k + 1), "texto", 20, OSCURO)
    for x, y in d["fijas"]:
        cx, cy = x0 + x * lado + lado / 2, y0 + y * lado + lado / 2
        p.rect(cx - 18, cy - 4, cx + 18, cy + 28, OSCURO)
        p.poli([(cx - 22, cy - 4), (cx + 22, cy - 4), (cx + 14, cy - 22), (cx - 14, cy - 22)], ROJO, OSCURO, 2)
    return p.final()


# ------------------------------------------------------------------ 41/43/45: los cuervos
def mapa_reino():
    d = I.CUERVOS
    p = pagina("EL MAPA DE LOS SIETE REINOS", "las seis fortalezas", HIELO, ACERO)
    for k, (x, y) in enumerate(d["pos"]):
        p.rect(x - 22, y - 22, x + 22, y + 22, (96, 110, 124), OSCURO, 4)
        p.poli([(x - 22, y - 22), (x - 14, y - 36), (x - 4, y - 22)], (96, 110, 124), OSCURO, 3)
        p.poli([(x + 4, y - 22), (x + 14, y - 36), (x + 22, y - 22)], (96, 110, 124), OSCURO, 3)
        p.disco(x, y + 40, 13, NIEVE, OSCURO, 2)
        p.texto((x, y + 40), str(k + 1), "cartel", 18, OSCURO)
        p.texto((x, y + 66), d["fortalezas"][k], "texto2", 16, OSCURO)
    return p.final()


def leguas():
    d = I.CUERVOS
    p = pagina("LAS LEGUAS ENTRE FORTALEZAS", "del libro del maestre", HIELO, ACERO)
    n = 6
    x0, y0, c = 92, 200, 70
    for k in range(n):
        p.disco(x0 + (k + 1) * c, y0, 18, NIEVE, OSCURO, 2)
        p.texto((x0 + (k + 1) * c, y0), str(k + 1), "cartel", 18, OSCURO)
        p.disco(x0, y0 + (k + 1) * c, 18, NIEVE, OSCURO, 2)
        p.texto((x0, y0 + (k + 1) * c), str(k + 1), "cartel", 18, OSCURO)
    for (i, j), v in sorted(((tuple(map(int, k.split(","))), v) for k, v in d["distancias"].items())):
        x, y = x0 + (j + 1) * c, y0 + (i + 1) * c
        p.rect(x - 28, y - 26, x + 28, y + 26, NIEVE, GRIS, 2)
        p.texto((x, y), str(v), "cartel", 30, OSCURO)
    return p.final()


def acertijo_cuervos():
    p = pagina("EL ACERTIJO DE LOS CUERVOS", "grabado en el palomar", HIELO, ACERO)
    versos(p, ["«Un mensajero sale de Piedra Negra,", "visita cada fortaleza una vez", "y regresa a casa.", "",
               "Los cuervos cobran por legua:", "el maestre quiere la ruta", "que menos leguas gaste.»"], 210, 54, 25)
    return p.final()


# ------------------------------------------------------------------ 42/49/53: Playfair
def carta_prisionera():
    d = I.PLAYFAIR
    p = pagina("LA CARTA DE LA PRISIONERA", "escrita en pares de letras", HIELO, ACERO)
    for k in range(0, len(d["cifrado"]), 2):
        x = 100 + (k // 2) * 140
        p.rect(x - 56, 280, x + 56, 380, NIEVE, OSCURO, 4)
        p.texto((x - 26, 330), d["cifrado"][k], "cartel", 56, OSCURO)
        p.texto((x + 26, 330), d["cifrado"][k + 1], "cartel", 56, OSCURO)
    return p.final()


def cuadrado_clave():
    d = I.PLAYFAIR
    p = pagina("EL CUADRADO DE LA CLAVE", "la I y la J comparten casilla", HIELO, ACERO)
    lado = 90
    x0, y0 = (W - 5 * lado) / 2, 200
    for f in range(5):
        for c in range(5):
            p.rect(x0 + c * lado, y0 + f * lado, x0 + (c + 1) * lado, y0 + (f + 1) * lado, NIEVE, ACERO, 3)
            p.texto((x0 + c * lado + lado / 2, y0 + f * lado + lado / 2), d["cuadrado"][f][c], "cartel", 44, OSCURO)
    return p.final()


def regla_cuadrado():
    p = pagina("LA REGLA DEL CUADRADO", "para cifrar, de dos en dos", HIELO, ACERO)
    versos(p, ["«Las letras se cifran por parejas.", "", "Si están en la misma fila,", "cada una pasa a la de su derecha.", "",
               "Si están en la misma columna,", "cada una pasa a la de abajo.", "", "Si no, forman un rectángulo:",
               "cada una pasa a la esquina", "de su misma fila.»"], 190, 50, 24)
    return p.final()


# ------------------------------------------------------------------ 54/55/59: las piedras
def reglas_piedras():
    d = I.PIEDRAS
    p = pagina("EL JUEGO DE LAS PIEDRAS", "en la mesa del carcelero", HIELO, ACERO)
    for k in range(d["piedras"]):
        x = 70 + (k % 7) * 76
        y = 230 + (k // 7) * 70
        p.elip(x - 26, y - 20, x + 26, y + 20, GRIS, OSCURO, 3)
    versos(p, ["«Veintiuna piedras sobre la mesa.", "Cada uno toma una, dos o tres", "por turno. Quien se lleva la última,", "gana.", "El retador empieza.»"], 480, 46, 22)
    return p.final()


def partidas_piedras():
    d = I.PIEDRAS
    p = pagina("LAS PARTIDAS DEL CARCELERO", "contra otros tantos retadores", HIELO, ACERO)
    for g, pasos in enumerate(d["partidas"]):
        y = 230 + g * 190
        p.texto((60, y - 50), f"Partida {g + 1}", "texto", 22, OSCURO, "lm")
        x = 60
        for k, v in enumerate(pasos):
            rey = k % 2 == 0 and k > 0 or False
            quien = (k % 2 == 0)           # k pares (>0): tras el movimiento del Rey; impares: tras el del retador
            p.disco(x + 18, y + 20, 22, NIEVE, OSCURO, 3)
            p.texto((x + 18, y + 20), str(v), "cartel", 22 if v > 9 else 24, OSCURO)
            x += 46
    p.texto((W / 2, 800), "cada círculo, las piedras que quedan tras cada jugada;", "texto2", 15, OSCURO)
    p.texto((W / 2, 824), "el retador abre cada partida", "texto2", 15, OSCURO)
    return p.final()


def dicho_carcelero():
    p = pagina("EL DICHO DEL CARCELERO", "contado entre los guardias", HIELO, ACERO)
    versos(p, ["«Al Rey nunca le ganó nadie", "que le dejase cuatro, cuatro y cuatro.", "",
               "Quien cuenta de cuatro en cuatro", "se sienta a la mesa del Rey", "con las manos vacías.»"], 230, 56, 25)
    return p.final()


# ------------------------------------------------------------------ 37/39, 33: los castillos (Hashi)
def letras_islas():
    isl = [tuple(map(int, k.split(","))) for k in I.CAMINOS["islas"]]
    isl.sort(key=lambda t: (t[1], t[0]))
    return {isl_: "ABCDEFGHIJKLMNOP"[i] for i, isl_ in enumerate(isl)}


def mapa_castillos():
    d = I.CAMINOS
    n = d["n"]
    p = ancha("LOS CASTILLOS DEL REINO")
    lado = 84
    x0, y0 = 630 - 4 * lado, 100
    letras = letras_islas()
    for y in range(n):
        for x in range(n):
            p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, (222, 232, 240), (186, 200, 212), 1)
    for (x, y), L in letras.items():
        num = d["islas"][f"{x},{y}"]
        cx, cy = x0 + x * lado + lado / 2, y0 + y * lado + lado / 2
        p.disco(cx, cy, 30, (96, 110, 124), OSCURO, 4)
        p.texto((cx, cy - 2), str(num), "cartel", 34, NIEVE)
        p.texto((cx + 26, cy - 28), L, "cartel", 18, FUEGO)
    return p.final()


def acertijo_puentes():
    p = pagina("EL ACERTIJO DE LOS PUENTES", "grabado en el mapa del maestre", HIELO, ACERO)
    versos(p, ["«Cada castillo anota cuántos puentes", "salen de él.", "", "Los puentes van en línea recta,",
               "nunca se cruzan y no hay más", "de dos entre el mismo par.", "", "Y desde cualquier castillo se debe", "poder llegar a todos los demás.»"], 190, 52, 24)
    return p.final()


# ------------------------------------------------------------------ 26, 61/63: la sucesión
def leyes_reino():
    p = pagina("LAS LEYES DEL REINO", "copiadas por el maestre", HIELO, ACERO)
    versos(p, ["«Ni el muerto ni quien tomó los votos", "reciben la corona.", "", "Los hijos del primer hijo, aunque este",
               "haya muerto, van antes que los", "hijos de los demás hijos.", "", "Dentro de cada línea, el varón",
               "antes que la mujer y, entre iguales,", "el mayor antes que el menor.»"], 190, 50, 23)
    return p.final()


def arbol_rey():
    d = I.SUCESION["personas"]
    p = ancha("EL ÁRBOL DEL REY AERION")
    pos = {"Aerion": (330, 190), "Baelor": (210, 400), "Maegor": (480, 400), "Aemon": (860, 400), "Daenys": (1090, 400),
           "Rhaena": (110, 640), "Daemon": (310, 640), "Jaena": (1090, 640)}
    for k, v in d.items():
        if v["padre"]:
            a, b = pos[v["padre"]], pos[k]
            p.linea([(a[0], a[1] + 60), (b[0], b[1] - 60)], GRIS, 5)
    for k, v in d.items():
        x, y = pos[k]
        p.rect(x - 90, y - 60, x + 90, y + 60, NIEVE, OSCURO, 4)
        p.texto((x, y - 32), v["nombre"], "cartel", 24, OSCURO)
        p.texto((x, y - 4), f"{v['edad']} años", "texto2", 20, OSCURO)
        p.texto((x, y + 24), "varón" if v["sexo"] == "m" else "mujer", "texto2", 20, OSCURO)
        if v["estado"] == "muerto":
            p.rect(x - 90, y + 40, x + 90, y + 60, OSCURO)
            p.texto((x, y + 50), "muerto", "texto2", 15, NIEVE)
        elif v["estado"] == "septon":
            p.rect(x - 90, y + 40, x + 90, y + 60, ORO, OSCURO, 2)
            p.texto((x, y + 50), "septón (votos)", "texto2", 15, OSCURO)
    return p.final()


# ------------------------------------------------------------------ 70/71: el tablero de las casas (sudoku)
def tablero_casas():
    d = I.SUDOKU
    p = Hoja(W, H * 2, HIELO)
    p.rect(16, 16, W - 16, H * 2 - 16, None, ACERO, 6)
    p.rect(28, 28, W - 28, H * 2 - 28, None, ACERO, 2)
    p.texto((W / 2 + 26, 70), "EL TABLERO DE LAS SEIS CASAS", "cartel", 30, OSCURO)
    for k, v in enumerate(["Seis casas, seis escudos.", "En cada fila, en cada columna y en cada",
                           "recuadro de dos por tres, ningún escudo", "se repite. Los escudos de ahí abajo",
                           "ya están en su sitio."]):
        p.texto((W / 2, 150 + k * 34), v, "texto2", 20, OSCURO)
    # leyenda con los seis escudos
    for k, c in enumerate(d["casas"]):
        figura(p, c, 80 + k * 94, 360, 56, CASAS[k])
        p.texto((80 + k * 94, 410), c, "texto2", 15, OSCURO)
    lado = 90
    x0, y0 = (W - 6 * lado) / 2, H - 2 * lado
    for f in range(6):
        for c in range(6):
            p.rect(x0 + c * lado, y0 + f * lado, x0 + (c + 1) * lado, y0 + (f + 1) * lado, NIEVE, ACERO, 2)
            v = d["dados"][f][c]
            if v:
                figura(p, d["casas"][v - 1], x0 + c * lado + lado / 2, y0 + f * lado + lado / 2, 58, CASAS[v - 1])
    for k in range(7):
        p.linea([(x0 + k * lado * 1, y0), (x0 + k * lado, y0 + 6 * lado)], ACERO, 5 if k in (0, 3, 6) else 1)
    for k in range(7):
        p.linea([(x0, y0 + k * lado), (x0 + 6 * lado, y0 + k * lado)], ACERO, 5 if k in (0, 2, 4, 6) else 1)
    return p.final()


# ------------------------------------------------------------------ 66/67: el tapiz (nonograma)
def pistas_filas():
    d = I.TAPIZ
    p = pagina("EL TAPIZ DEL SIGILO", "lo que cuentan las tejedoras: las filas", HIELO, ACERO)
    for k, pist in enumerate(d["filas"]):
        y = 190 + k * 72
        p.texto((70, y), f"fila {k + 1}", "texto", 22, OSCURO, "lm")
        for j, v in enumerate(pist):
            p.disco(290 + j * 72, y, 26, NIEVE, OSCURO, 3)
            p.texto((290 + j * 72, y), str(v), "cartel", 28, OSCURO)
    return p.final()


def pistas_columnas():
    d = I.TAPIZ
    p = pagina("EL TAPIZ DEL SIGILO", "lo que cuentan las tejedoras: las columnas", HIELO, ACERO)
    for k, pist in enumerate(d["columnas"]):
        y = 190 + k * 72
        p.texto((70, y), f"columna {'ABCDEFGH'[k]}", "texto", 22, OSCURO, "lm")
        for j, v in enumerate(pist):
            p.disco(330 + j * 72, y, 26, NIEVE, OSCURO, 3)
            p.texto((330 + j * 72, y), str(v), "cartel", 28, OSCURO)
    return p.final()


# ------------------------------------------------------------------ 75/79: las torres de hielo
def torres_hielo():
    d = I.TORRES
    p = pagina("LAS TORRES DE HIELO", "las cuatro piezas de la corona", HIELO, ACERO)
    for t in range(3):
        x = 130 + t * 185
        p.rect(x - 8, 300, x + 8, 640, GRIS, OSCURO, 2)
        p.rect(x - 70, 640, x + 70, 664, ACERO)
    for k in range(d["discos"]):
        ancho = 130 - k * 26
        y = 640 - (d["discos"] - k) * 36
        p.rect(130 - ancho / 2, y, 130 + ancho / 2, y + 32, (190 - k * 20, 160 + k * 10, 90 + k * 30), OSCURO, 3)
    p.texto((130, 700), "I", "cartel", 30, OSCURO)
    p.texto((315, 700), "II", "cartel", 30, OSCURO)
    p.texto((500, 700), "III", "cartel", 30, OSCURO)
    return p.final()


def reloj_arena():
    d = I.TORRES
    p = pagina("EL RELOJ DE ARENA", "sobre la torre de hielo", HIELO, ACERO)
    versos(p, ["«Hay que llevar la corona entera", "de la torre I a la III.", "", "Un solo disco por vez, y nunca un disco",
               "sobre otro más pequeño.", "", f"El reloj de arena da {d['limite']} vueltas:", "cada movimiento es una vuelta.»"], 190, 52, 24)
    return p.final()


# ------------------------------------------------------------------ 86/87: la profecía
def profecia1():
    p = pagina("LA PROFECÍA DEL MAESTRE (I)", "dictada en voz baja", HIELO, ACERO)
    versos(p, ["«Cuatro cifras, cuatro pruebas:", "", "La primera, la del que lleva cartas", "con alas negras de torre en torre.",
               "", "La segunda, la del que reparte", "hidromiel en jarras sin marcas.»"], 200, 52, 24)
    return p.final()


def profecia2():
    p = pagina("LA PROFECÍA DEL MAESTRE (II)", "dictada en voz baja", HIELO, ACERO)
    versos(p, ["«La tercera, la del que quita", "piedras de una mesa por turnos.", "", "La cuarta, la de los ocho que vigilan",
               "la muralla sin verse entre sí.", "", "Y la puerta se abre con lo que sale de:", "", "primera por segunda,",
               "menos la tercera, más la cuarta.»"], 190, 50, 23)
    return p.final()


def inyectar(carpeta):
    """Mete los datos de las instancias en las apps (bloque /*DATOS*/.../*FIN*/)."""
    letras = letras_islas()
    isl = [{"x": x, "y": y, "letra": L} for (x, y), L in letras.items()]
    datos = {
        "14-jarras.js": {"A": I.JARRAS["A"], "B": I.JARRAS["B"], "objetivo": I.JARRAS["objetivo"], "dato": I.DATOS["14"]},
        "20-centinelas.js": {"n": I.CENTINELAS["n"], "fijas": I.CENTINELAS["fijas"], "solucion": I.CENTINELAS["solucion"], "dato": I.DATOS["20"]},
        "40-cuervos.js": {"fortalezas": I.CUERVOS["fortalezas"], "solucion": I.CUERVOS["solucion"], "minimo": I.CUERVOS["minimo"], "distancias": I.CUERVOS["distancias"],
                          "dato": I.DATOS["40"]},
        "48-playfair.js": {"claro": I.PLAYFAIR["claro"]},
        "52-piedras.js": {"piedras": I.PIEDRAS["piedras"], "dato": I.DATOS["52"]},
        "46-caminos.js": {"n": I.CAMINOS["n"], "islas": isl, "puentes": I.CAMINOS["puentes"]},
        "51-sucesion.js": {"opciones": ["Rhaena", "Daemon", "Maegor", "Aemon", "Daenys", "Jaena"], "solucion": I.SUCESION["solucion"]},
        "69-sudoku.js": {"dados": I.SUDOKU["dados"], "solucion": I.SUDOKU["solucion"], "casas": I.SUDOKU["casas"], "figuras": {c: I.CASAS_FIG[c] for c in I.SUDOKU["casas"]}},
        "64-tapiz.js": {"solucion": I.TAPIZ["solucion"]},
        "72-torres.js": I.TORRES,
        "85-profecia.js": {"resultado": I.RESULTADO},
    }
    for app, d in datos.items():
        ruta = os.path.join(carpeta, "minijuegos", app)
        txt = open(ruta, encoding="utf-8").read() if os.path.exists(ruta) else ""
        if "/*DATOS*/" not in txt:
            continue
        a, b = txt.index("/*DATOS*/") + len("/*DATOS*/"), txt.index("/*FIN*/")
        open(ruta, "w", encoding="utf-8", newline="\n").write(txt[:a] + json.dumps(d, ensure_ascii=False) + txt[b:])


def main(carpeta="juegos/aventuras-ca/trono"):
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    g = lambda k, im: ruido(im, int(k)).save(os.path.join(arte, f"{k}.png"))

    def mosaico(nombre, im, filas, cols, cartas):
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))
        for pieza, k in zip(cortar(im, filas, cols), cartas):
            pieza.save(os.path.join(arte, f"{k}.png"))
    g("16", encargo_jarras())
    g("18", acertijo_muralla())
    mosaico("muralla", muralla(), 2, 1, ("19", "21"))
    g("41", mapa_reino())
    g("43", leguas())
    g("45", acertijo_cuervos())
    g("42", carta_prisionera())
    g("49", cuadrado_clave())
    g("53", regla_cuadrado())
    g("54", reglas_piedras())
    g("55", partidas_piedras())
    g("59", dicho_carcelero())
    mosaico("castillos", mapa_castillos(), 1, 2, ("37", "39"))
    g("33", acertijo_puentes())
    g("26", leyes_reino())
    mosaico("arbol", arbol_rey(), 1, 2, ("61", "63"))
    mosaico("casas", tablero_casas(), 2, 1, ("70", "71"))
    g("66", pistas_filas())
    g("67", pistas_columnas())
    g("75", torres_hielo())
    g("79", reloj_arena())
    g("86", profecia1())
    g("87", profecia2())
    inyectar(carpeta)
    print("láminas de Trono escritas en", arte)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

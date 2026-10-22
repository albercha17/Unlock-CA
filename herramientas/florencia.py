"""Láminas de «Florencia, 1503: El Taller de Leonardo» (versión de 60 cartas, 21 oct 2026). Todas las pistas son dibujos o acertijos:
ninguna carta escribe la respuesta ni explica cómo se resuelve su puzle. Datos de herramientas/instancias_florencia.py.

  16 la tira de cuero y la vara · 18 el acertijo del perspectivo · 19 y 21 el suelo del taller (dos mitades)
  41 y 43 el tablero del león (dos mitades) · 45 el acertijo del tablero · 42 y 49 el patio de ajedrez (dos mitades) · 53 el acertijo del caballo
  54 los tres pigmentos · 55 el color de Leonardo · 59 el acertijo de la paleta
  37 el tren de engranajes · 39 la manivela · 33 el acertijo del reloj
  61 y 63 el plano de las plazas (dos mitades) · 26 el cuaderno de Leonardo · 70 los intentos de la caja · 71 los pigmentos y su norma
  66 y 67 la escalera de caracol (dos mitades) · 75 los cuatro sistemas de poleas · 79 el peso y el esfuerzo
  86 el mensaje del lucernario · 87 la tabla de Vigenère
Uso (desde la raíz del repo):  python herramientas/florencia.py [carpeta_juego]
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
import instancias_florencia as I  # noqa: E402

W, H = 630, 882
PERGAMINO = (238, 222, 188)
SEPIA = (70, 44, 24)
TERRA = (176, 84, 52)
OLIVA = (110, 120, 60)
AZUL = (48, 84, 150)
OCRE = (200, 150, 70)
BLANCO = (252, 246, 232)
GRIS = (130, 120, 108)
COL_MM = [(190, 50, 44), (50, 100, 200), (60, 150, 80), (232, 190, 60), (140, 80, 190), (246, 240, 228)]
COL_PIG = [(190, 50, 44), (232, 190, 60), (50, 100, 200)]


def ruido(im, s, f=2.5):
    a = np.asarray(im).astype(np.int16)
    a = a + np.random.default_rng(s).normal(0, f, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def pagina(titulo, sub=None, fondo=PERGAMINO, borde=OCRE, w=W, h=H):
    p = Hoja(w, h, fondo)
    p.rect(16, 16, w - 16, h - 16, None, borde, 6)
    p.rect(28, 28, w - 28, h - 28, None, borde, 2)
    p.texto((w / 2 + 26, 70), titulo, "cartel", 32, SEPIA)
    if sub:
        p.texto((w / 2 + 26, 108), sub, "texto2", 21, SEPIA)
    return p


def versos(p, lineas, y0=220, paso=56, tam=27, x=W / 2):
    for k, v in enumerate(lineas):
        p.texto((x, y0 + k * paso), v, "texto2", tam, SEPIA)


def ancha(titulo, borde=OCRE):
    p = Hoja(W * 2, H, PERGAMINO)
    p.rect(16, 16, W * 2 - 16, H - 16, None, borde, 6)
    p.rect(28, 28, W * 2 - 28, H - 28, None, borde, 2)
    p.texto((W, 66), titulo, "cartel", 34, SEPIA)
    return p


# ------------------------------------------------------------------ 16: la tira de cuero y la vara
def tira_escitala():
    d = I.ESCITALA
    p = pagina("LA TIRA DEL COFRE", "cuero cosido a la tapa", PERGAMINO, OCRE)
    letras = d["cifrado"]
    por_fila = 8
    for f in range(2):
        y = 250 + f * 130
        p.poli([(40, y - 44), (W - 40, y - 44), (W - 40, y + 44), (40, y + 44)], (196, 154, 98), SEPIA, 4)
        for k in range(por_fila):
            x = 76 + k * 68
            p.texto((x, y), letras[f * por_fila + k], "cartel", 44, SEPIA)
    p.texto((W / 2, 440), "▼ sigue la tira ▼" if False else "(la tira sigue en la línea de abajo)", "texto2", 16, SEPIA)
    # la vara: sección cuadrada con sus cuatro caras
    cx, cy, r = W / 2, 640, 70
    p.rect(cx - r, cy - r, cx + r, cy + r, (206, 170, 120), SEPIA, 5)
    for k in range(4):
        a = k * math.pi / 2
        p.disco(cx + math.cos(a) * (r - 22) * 0 + [0, r - 24, 0, -(r - 24)][k], cy + [-(r - 24), 0, r - 24, 0][k], 9, SEPIA)
    p.texto((cx, cy), "vara", "texto2", 22, SEPIA)
    p.texto((W / 2, 770), "la vara del maestro, vista de punta", "texto2", 18, SEPIA)
    return p.final()


# ------------------------------------------------------------------ 18, 19/21: el punto de fuga
def acertijo_fuga():
    p = pagina("EL ACERTIJO DEL PERSPECTIVO", "pegado en el bastidor", PERGAMINO, OCRE)
    versos(p, ["«Las losas del suelo parecen", "juntarse según se alejan.", "", "Todas las rectas que van", "hacia lo lejos, si las alargas,",
               "se encuentran en un solo punto.", "", "Hallalo y ya tienes el lugar", "donde acaba el mundo pintado.»"], 200, 52, 25)
    return p.final()


def suelo_taller():
    d = I.PERSPECTIVA
    p = Hoja(W, H * 2, PERGAMINO)
    p.rect(16, 16, W - 16, H * 2 - 16, None, OCRE, 6)
    p.rect(28, 28, W - 28, H * 2 - 28, None, OCRE, 2)
    p.texto((W / 2 + 26, 70), "EL SUELO DEL TALLER", "cartel", 32, SEPIA)
    p.texto((W / 2 + 26, 108), "dibujado por Leonardo, con su cuadrícula", "texto2", 18, SEPIA)
    lado, y0 = d["lado"], d["y0"]
    for c in range(d["cols"] + 1):
        p.linea([(c * lado, y0), (c * lado, y0 + d["filas"] * lado)], (206, 188, 150), 1.5)
    for f in range(d["filas"] + 1):
        p.linea([(0, y0 + f * lado), (W, y0 + f * lado)], (206, 188, 150), 1.5)
    for c in range(d["cols"]):
        p.texto((c * lado + lado / 2, y0 - 14), "ABCDEF"[c], "texto", 18, SEPIA)
    for f in range(d["filas"]):
        p.texto((16, y0 + f * lado + lado / 2), str(f + 1), "texto", 16, SEPIA, "lm")
    for a, b in d["lineas"]:
        p.linea([tuple(a), tuple(b)], SEPIA, 6)
    return p.final()


# ------------------------------------------------------------------ 41/43, 45: el tablero del león (futoshiki)
def tablero_leon():
    d = I.FUTOSHIKI
    n = d["n"]
    p = ancha("EL TABLERO DEL LEÓN")
    lado = 130
    x0, y0 = 630 - 3 * lado, 120
    dados = {(x, y): v for x, y, v in d["dados"]}
    for y in range(n):
        for x in range(n):
            px, py = x0 + x * lado + 18, y0 + y * lado + 18
            p.rect(px, py, px + lado - 36, py + lado - 36, BLANCO, SEPIA, 4)
            if (x, y) in dados:
                p.texto((px + (lado - 36) / 2, py + (lado - 36) / 2), str(dados[(x, y)]), "cartel", 52, SEPIA)
    for (ax, ay), (bx, by) in d["desigualdades"]:
        # signo entre las dos casillas, apuntando a la menor: a < b
        mx = x0 + (ax + bx) / 2 * lado + lado / 2
        my = y0 + (ay + by) / 2 * lado + lado / 2
        if ay == by:   # horizontal: a < b
            izq, der = (ax < bx), True
            sentido = 1 if ax < bx else -1       # 1: a a la izquierda (a<b) -> «<»; -1: a a la derecha -> «>»
            if sentido == 1:
                p.linea([(mx + 12, my - 20), (mx - 12, my), (mx + 12, my + 20)], TERRA, 7)
            else:
                p.linea([(mx - 12, my - 20), (mx + 12, my), (mx - 12, my + 20)], TERRA, 7)
        else:           # vertical
            sentido = 1 if ay < by else -1
            if sentido == 1:    # a arriba y menor: «∧»
                p.linea([(mx - 20, my + 12), (mx, my - 12), (mx + 20, my + 12)], TERRA, 7)
            else:
                p.linea([(mx - 20, my - 12), (mx, my + 12), (mx + 20, my - 12)], TERRA, 7)
    return p.final()


def acertijo_tablero():
    p = pagina("EL ACERTIJO DEL LEÓN", "grabado en la base", PERGAMINO, OCRE)
    versos(p, ["«Cada fila y cada columna", "guardan los números del uno al cinco,", "ninguno repetido.", "",
               "Y la boca abierta del signo", "mira siempre al número mayor:", "el pico del signo señala al menor.»"], 210, 54, 25)
    return p.final()


# ------------------------------------------------------------------ 42/49, 53: el patio de ajedrez
def patio_ajedrez():
    d = I.CABALLO
    n = d["n"]
    p = ancha("EL PATIO DEL TALLER")
    lado = 120
    x0, y0 = 630 - 3 * lado, 110
    huecos = {tuple(h) for h in d["huecos"]}
    for y in range(n):
        for x in range(n):
            if (x, y) in huecos:
                p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, (60, 44, 34), SEPIA, 2)
                p.linea([(x0 + x * lado + 24, y0 + y * lado + 24), (x0 + (x + 1) * lado - 24, y0 + (y + 1) * lado - 24)], (130, 100, 70), 8)
                p.linea([(x0 + (x + 1) * lado - 24, y0 + y * lado + 24), (x0 + x * lado + 24, y0 + (y + 1) * lado - 24)], (130, 100, 70), 8)
            else:
                p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, (236, 218, 180) if (x + y) % 2 == 0 else (186, 150, 108), SEPIA, 2)
    ix, iy = d["inicio"]
    cx, cy = x0 + ix * lado + lado / 2, y0 + iy * lado + lado / 2
    p.poli([(cx - 26, cy + 34), (cx - 22, cy - 6), (cx - 6, cy - 34), (cx + 14, cy - 28), (cx + 30, cy - 6), (cx + 22, cy + 34)], SEPIA)
    p.disco(cx + 8, cy - 18, 5, BLANCO)
    for k in range(n):
        p.texto((x0 + k * lado + lado / 2, y0 - 16), "ABCDEF"[k], "texto", 20, SEPIA)
        p.texto((x0 - 20, y0 + k * lado + lado / 2), str(k + 1), "texto", 20, SEPIA)
    return p.final()


def acertijo_caballo():
    p = pagina("EL ACERTIJO DEL CABALLO", "pintado en el muro del patio", PERGAMINO, OCRE)
    versos(p, ["«El caballo salta dos casillas", "en línea recta y una de lado,", "por encima de lo que haya.", "",
               "Sale de su casilla y debe pisar", "todas las casillas libres,", "una sola vez cada una.", "Las casillas tachadas no se pisan.»"], 200, 52, 25)
    return p.final()


# ------------------------------------------------------------------ 54/55/59: los pigmentos
def frasco(p, x, y, col, gotas):
    p.rect(x - 40, y - 50, x + 40, y + 60, (220, 232, 236), SEPIA, 4)
    p.rect(x - 28, y - 70, x + 28, y - 50, (150, 110, 70), SEPIA, 3)
    for k in range(gotas):
        p.disco(x - 20 + (k % 3) * 20, y + 40 - (k // 3) * 24, 9, col, SEPIA, 1.5)


def tres_pigmentos():
    d = I.PIGMENTOS
    p = pagina("LOS TRES PIGMENTOS", "lo que lleva cada cucharada", PERGAMINO, TERRA)
    nom = ["Pigmento I", "Pigmento II", "Pigmento III"]
    for j, fila in enumerate(d["pigmentos"]):
        y = 240 + j * 210
        p.texto((90, y - 10), nom[j], "texto", 22, SEPIA, "lm")
        for c, g in enumerate(fila):
            x = 250 + c * 120
            p.disco(x, y - 40, 14, COL_PIG[c], SEPIA, 2)
            for k in range(g):
                p.disco(x, y + k * 30, 12, COL_PIG[c], SEPIA, 2)
    return p.final()


def color_maestro():
    d = I.PIGMENTOS
    p = pagina("EL COLOR DEL MAESTRO", "la mezcla que quiere Leonardo", PERGAMINO, TERRA)
    for c in range(3):
        x = 150 + c * 165
        p.disco(x, 220, 20, COL_PIG[c], SEPIA, 2)
        for k in range(d["objetivo"][c]):
            p.disco(x - 30 + (k % 2) * 60, 280 + (k // 2) * 36, 13, COL_PIG[c], SEPIA, 2)
    return p.final()


def acertijo_paleta():
    p = pagina("EL ACERTIJO DE LA PALETA", "escrito en el cajón", PERGAMINO, TERRA)
    versos(p, ["«Cada cucharada de un pigmento", "lleva las gotas que ves.", "", "Echa cucharadas enteras de los tres",
               "hasta que las gotas sumadas", "sean justo las del color del maestro,", "ni una más, ni una menos.»"], 210, 54, 25)
    return p.final()


# ------------------------------------------------------------------ 37/39/33: el tren de engranajes
def engranaje(p, cx, cy, dientes, paso, color, nombre):
    r = dientes * paso / (2 * math.pi)
    pts = []
    for i in range(dientes):
        a0 = 2 * math.pi * i / dientes
        for da, rr in ((0.0, r - 7), (0.18, r + 7), (0.56, r + 7), (0.74, r - 7)):
            a = a0 + da * 2 * math.pi / dientes
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    p.poli(pts, color, SEPIA, 3)
    p.disco(cx, cy, 9, SEPIA)
    p.texto((cx, cy + r + 38), nombre, "cartel", 26, SEPIA)
    return r


def tren_engranajes():
    d = I.ENGRANAJES["dientes"]
    p = pagina("EL RELOJ DEL TALLER", "las ruedas, vistas de frente", PERGAMINO, OCRE)
    paso = 32
    rA, rB, rC, rD = (d[k] * paso / (2 * math.pi) for k in "ABCD")
    y = 430
    xA = 70
    xB = xA + rA + rB
    xC = xB + 230
    xD = xC + rC + rD
    p.linea([(xB, y), (xC, y)], (150, 110, 70), 16)
    engranaje(p, xA, y, d["A"], paso, (210, 170, 110), "A")
    engranaje(p, xB, y, d["B"], paso, (190, 140, 90), "B")
    engranaje(p, xC, y, d["C"], paso, (176, 100, 66), "C")
    engranaje(p, xD, y, d["D"], paso, (150, 120, 64), "D")
    return p.final()


def manivela():
    d = I.ENGRANAJES
    p = pagina("LA MANIVELA", "del reloj del taller", PERGAMINO, OCRE)
    p.disco(W / 2, 330, 110, (210, 170, 110), SEPIA, 6)
    p.linea([(W / 2, 330), (W / 2 + 110, 330 - 110)], SEPIA, 12)
    p.disco(W / 2 + 110, 220, 22, TERRA, SEPIA, 4)
    p.texto((W / 2, 330), "A", "cartel", 70, SEPIA)
    p.texto((W / 2, 520), f"{d['vueltas_a']} vueltas", "cartel", 50, SEPIA)
    p.texto((W / 2, 590), "y gira hacia la derecha", "texto2", 24, SEPIA)
    p.texto((W / 2, 630), "(como las agujas del reloj)", "texto2", 18, SEPIA)
    return p.final()


def acertijo_reloj():
    p = pagina("EL ACERTIJO DEL RELOJ", "grabado en el cárter", PERGAMINO, OCRE)
    versos(p, ["«Dos ruedas que se tocan", "giran en sentidos contrarios.", "", "Las que van en un mismo eje", "giran juntas y del mismo modo.", "",
               "Por cada diente que pasa de una,", "pasa un diente de la otra.»"], 200, 52, 25)
    return p.final()


# ------------------------------------------------------------------ 61/63, 26: las plazas de Florencia
def plano_plazas():
    d = I.VIGILANTES
    p = ancha("LAS PLAZAS DE LA CIUDAD")
    X = lambda v: 80 + (v[0] - 40) / 527 * 1100
    Y = lambda v: 160 + (v[1] - 90) / 420 * 560
    for a, b in d["aristas"]:
        pa, pb = d["pos"][str(a)], d["pos"][str(b)]
        p.linea([(X(pa), Y(pa)), (X(pb), Y(pb))], (150, 120, 90), 9)
    for k, v in d["pos"].items():
        p.disco(X(v), Y(v), 42, BLANCO, SEPIA, 5)
        p.texto((X(v), Y(v)), str(int(k) + 1), "cartel", 42, SEPIA)
    return p.final()


def cuaderno_leonardo():
    p = pagina("EL CUADERNO DE LEONARDO", "página escrita al revés", PERGAMINO, OCRE)
    versos(p, ["«Una torre de vigía ve su plaza", "y las plazas que tienen calle directa", "con la suya.", "",
               "La ciudad está a salvo si no queda", "ninguna plaza fuera de vista.", "", "El Gonfaloniere paga cada torre:", "que sean las menos posibles.»"], 200, 52, 24)
    return p.final()


# ------------------------------------------------------------------ 70/71: la caja de pigmentos
def intentos_caja():
    d = I.MASTERMIND
    p = pagina("LOS INTENTOS DEL APRENDIZ", "anotados en la tapa de la caja", PERGAMINO, TERRA)
    for k, it in enumerate(d["intentos"]):
        y = 190 + k * 105
        for j, c in enumerate(it["orden"]):
            p.disco(100 + j * 76, y, 28, COL_MM[c], SEPIA, 3)
        # los aciertos: negros primero, luego blancos
        for q in range(4):
            x = 450 + (q % 2) * 44
            yy = y - 16 + (q // 2) * 34
            if q < it["negros"]:
                p.disco(x, yy, 14, SEPIA, SEPIA, 2)
            elif q < it["negros"] + it["blancos"]:
                p.disco(x, yy, 14, BLANCO, SEPIA, 3)
            else:
                p.disco(x, yy, 14, None, (190, 170, 140), 2)
    return p.final()


def colores_caja():
    d = I.MASTERMIND
    p = pagina("LOS SEIS PIGMENTOS", "y lo que dicen los aciertos", PERGAMINO, TERRA)
    for k, c in enumerate(COL_MM):
        x = 120 + (k % 3) * 195
        y = 210 + (k // 3) * 110
        p.disco(x, y, 32, c, SEPIA, 3)
        p.texto((x, y + 52), d["colores"][k], "texto2", 19, SEPIA)
    p.disco(90, 480, 16, SEPIA, SEPIA, 2)
    p.texto((130, 480), "color bien puesto en su sitio", "texto2", 20, SEPIA, "lm")
    p.disco(90, 535, 16, BLANCO, SEPIA, 3)
    p.texto((130, 535), "color que está, pero en otro sitio", "texto2", 20, SEPIA, "lm")
    p.texto((W / 2, 640), "Los cuatro pigmentos de la clave", "texto2", 21, SEPIA)
    p.texto((W / 2, 675), "son todos distintos.", "texto2", 21, SEPIA)
    return p.final()


# ------------------------------------------------------------------ 66/67: la escalera de caracol (hidato)
def escalera_caracol():
    d = I.HIDATO
    n = d["n"]
    p = Hoja(W, H * 2, PERGAMINO)
    p.rect(16, 16, W - 16, H * 2 - 16, None, OCRE, 6)
    p.rect(28, 28, W - 28, H * 2 - 28, None, OCRE, 2)
    p.texto((W / 2 + 26, 70), "LA ESCALERA DE CARACOL", "cartel", 30, SEPIA)
    for k, v in enumerate(["Cada peldaño lleva un número del 1 al 25.", "Los peldaños seguidos están pegados,", "también en diagonal.",
                           "Faltan los números que no ves."]):
        p.texto((W / 2, 180 + k * 36), v, "texto2", 21, SEPIA)
    lado = 106
    x0, y0 = (W - n * lado) / 2, H - 3 * lado
    dados = {(x, y): v for x, y, v in d["dados"]}
    for y in range(n):
        for x in range(n):
            px, py = x0 + x * lado, y0 + y * lado
            p.rect(px, py, px + lado, py + lado, BLANCO if (x, y) in dados else (222, 204, 170), SEPIA, 3)
            if (x, y) in dados:
                p.texto((px + lado / 2, py + lado / 2), str(dados[(x, y)]), "cartel", 44, SEPIA)
    return p.final()


# ------------------------------------------------------------------ 75/79: las poleas
def sistemas_poleas():
    d = I.POLEAS
    p = pagina("LOS CUATRO APAREJOS", "del almacén del taller", PERGAMINO, OCRE)
    for k, seg in enumerate(d["sistemas"]):
        cx = 170 + (k % 2) * 300
        cy = 270 + (k // 2) * 330
        p.rect(cx - 90, cy - 100, cx + 90, cy - 80, (150, 110, 70), SEPIA, 3)
        bx0, bx1 = cx - 66, cx + 66
        p.rect(bx0, cy + 40, bx1, cy + 80, (196, 154, 98), SEPIA, 3)
        for j in range(seg):
            x = bx0 + (bx1 - bx0) * (j + 0.5) / seg
            p.linea([(x, cy - 80), (x, cy + 40)], SEPIA, 3)
        p.linea([(cx + 86, cy - 80), (cx + 86, cy + 20)], SEPIA, 3)
        p.poli([(cx + 74, cy + 8), (cx + 98, cy + 8), (cx + 86, cy + 30)], SEPIA)
        p.disco(cx - 100, cy - 60, 20, BLANCO, SEPIA, 3)
        p.texto((cx - 100, cy - 60), str(k + 1), "cartel", 26, SEPIA)
        p.poli([(cx - 40, cy + 80), (cx + 40, cy + 80), (cx + 30, cy + 130), (cx - 30, cy + 130)], (120, 100, 90), SEPIA, 3)
    return p.final()


def peso_esfuerzo():
    d = I.POLEAS
    p = pagina("LA CARGA Y LA MANO", "lo que hay que subir", PERGAMINO, OCRE)
    p.poli([(170, 260), (330, 260), (310, 380), (190, 380)], (120, 100, 90), SEPIA, 4)
    p.texto((250, 320), str(d["peso"]), "cartel", 52, BLANCO)
    p.texto((250, 410), "libras", "texto2", 22, SEPIA)
    p.disco(450, 300, 56, (236, 200, 160), SEPIA, 4)
    p.texto((450, 300), str(d["esfuerzo_max"]), "cartel", 52, SEPIA)
    p.texto((450, 410), "libras es lo que", "texto2", 18, SEPIA)
    p.texto((450, 436), "aguanta la mano", "texto2", 18, SEPIA)
    versos(p, ["«Se quiere el aparejo que alce", "la carga con lo que aguanta la mano", "y que gaste la menor cuerda.»"], 560, 50, 24)
    return p.final()


# ------------------------------------------------------------------ 86/87: el mensaje del lucernario y la tabla de Vigenère
def mensaje_lucernario():
    d = I.CIFRADO
    p = pagina("EL MENSAJE DEL LUCERNARIO", "escrito por Leonardo en el cristal", PERGAMINO, OCRE)
    for k, c in enumerate(d["cifrado"]):
        x = 85 + k * 67
        p.rect(x - 28, 240, x + 28, 320, BLANCO, SEPIA, 3)
        p.texto((x, 280), c, "cartel", 46, SEPIA)
    versos(p, ["«La palabra de la clave se forma", "con cuatro letras, una de cada puzle:", "", "primero la de lo que se mezcla en la paleta,",
               "luego la de lo que se alza con cuerdas,", "después la de lo que se adivina con colores,", "y al final la del salto del caballo.»"], 400, 48, 22)
    return p.final()


def tabla_vigenere():
    p = pagina("LA TABLA DEL CIFRADOR", "para quien sepa usarla", PERGAMINO, OCRE)
    c = 20
    x0, y0 = (W - 27 * c) / 2 + c, 140
    for i in range(26):
        p.texto((x0 + i * c, y0 - 14), I.ABC[i], "texto", 14, TERRA)
        p.texto((x0 - c, y0 + i * c + 10), I.ABC[i], "texto", 14, TERRA)
        for j in range(26):
            p.texto((x0 + j * c, y0 + i * c + 10), I.ABC[(i + j) % 26], "texto", 14, SEPIA)
    return p.final()


def inyectar(carpeta):
    """Mete los datos de las instancias en las apps (bloque /*DATOS*/.../*FIN*/)."""
    pers = I.PERSPECTIVA
    datos = {
        "14-escitala.js": {"caras": I.ESCITALA["caras"], "solucion": I.ESCITALA["solucion"], "letras": None},
        "20-perspectiva.js": {"cols": pers["cols"], "filas": pers["filas"], "solucion": pers["solucion"], "tolerancia": pers["tolerancia"]},
        "40-futoshiki.js": {"n": I.FUTOSHIKI["n"], "solucion": I.FUTOSHIKI["solucion"]},
        "48-caballo.js": {"n": I.CABALLO["n"], "huecos": I.CABALLO["huecos"], "inicio": I.CABALLO["inicio"], "letra": I.LETRAS_CLAVE["48"]},
        "52-pigmentos.js": {"pigmentos": I.PIGMENTOS["pigmentos"], "solucion": I.PIGMENTOS["solucion"], "letra": I.LETRAS_CLAVE["52"]},
        "46-engranajes.js": {"solucion": I.ENGRANAJES["solucion"]},
        "51-vigilantes.js": {"n": I.VIGILANTES["n"], "aristas": I.VIGILANTES["aristas"], "minimo": I.VIGILANTES["minimo"]},
        "69-mastermind.js": {"colores": I.MASTERMIND["colores"], "solucion": I.MASTERMIND["solucion"], "letra": I.LETRAS_CLAVE["69"]},
        "64-hidato.js": {"n": I.HIDATO["n"], "camino": I.HIDATO["camino"]},
        "72-poleas.js": {"sistemas": I.POLEAS["sistemas"], "solucion": I.POLEAS["solucion"], "letra": I.LETRAS_CLAVE["72"]},
        "85-cifrado.js": {"claro": I.CIFRADO["claro"]},
    }
    for app, d in datos.items():
        ruta = os.path.join(carpeta, "minijuegos", app)
        txt = open(ruta, encoding="utf-8").read() if os.path.exists(ruta) else ""
        if "/*DATOS*/" not in txt:
            continue
        a, b = txt.index("/*DATOS*/") + len("/*DATOS*/"), txt.index("/*FIN*/")
        open(ruta, "w", encoding="utf-8", newline="\n").write(txt[:a] + json.dumps(d, ensure_ascii=False) + txt[b:])


def main(carpeta="juegos/aventuras-ca/florencia"):
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    g = lambda k, im: ruido(im, int(k)).save(os.path.join(arte, f"{k}.png"))

    def mosaico(nombre, im, filas, cols, cartas):
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))
        for pieza, k in zip(cortar(im, filas, cols), cartas):
            pieza.save(os.path.join(arte, f"{k}.png"))
    g("16", tira_escitala())
    g("18", acertijo_fuga())
    mosaico("suelo", suelo_taller(), 2, 1, ("19", "21"))
    mosaico("leon", tablero_leon(), 1, 2, ("41", "43"))
    g("45", acertijo_tablero())
    mosaico("patio", patio_ajedrez(), 1, 2, ("42", "49"))
    g("53", acertijo_caballo())
    g("54", tres_pigmentos())
    g("55", color_maestro())
    g("59", acertijo_paleta())
    g("37", tren_engranajes())
    g("39", manivela())
    g("33", acertijo_reloj())
    mosaico("plazas", plano_plazas(), 1, 2, ("61", "63"))
    g("26", cuaderno_leonardo())
    g("70", intentos_caja())
    g("71", colores_caja())
    mosaico("escalera", escalera_caracol(), 2, 1, ("66", "67"))
    g("75", sistemas_poleas())
    g("79", peso_esfuerzo())
    g("86", mensaje_lucernario())
    g("87", tabla_vigenere())
    inyectar(carpeta)
    print("láminas de Florencia escritas en", arte)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

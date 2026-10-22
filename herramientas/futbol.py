"""Láminas de «La Final del Siglo, 1970: La Copa de Cristal» (versión de 60 cartas, 22 oct 2026). Todas las pistas son dibujos o acertijos: ninguna carta
escribe la respuesta ni explica cómo se resuelve su puzle. Datos de herramientas/instancias_futbol.py.

  16 la clasificación de la liguilla · 18 el acertijo del míster · 19 y 21 los seis cromos (dos caras: anverso 19.png / reverso 19r.png)
  41 y 43 las jugadas del VAR · 45 el reglamento del fuera de juego · 42 y 49 el campo con los jugadores (dos mitades) · 53 la regla del pase
  54 y 55 las notas del entrenador · 59 la regla de la alineación · 37 y 39 el informe de los once penaltis · 33 cómo se lee el informe
  26 los titulares de prensa · 61 y 63 el cuadro de eliminatorias (dos mitades) · 66 los cruces de la jornada 1 · 67 el método del calendario
  70 la alineación del míster · 71 las órdenes de cambios · 75 las filas de la grada · 79 la regla de las butacas · 86 los cinco aros · 87 el dial
Uso (desde la raíz del repo):  python herramientas/futbol.py [carpeta_juego]
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oeste  # noqa: E402
from oeste import Hoja  # noqa: E402
from mosaicos import cortar  # noqa: E402
import instancias_futbol as I  # noqa: E402

W, H = 630, 882
CREMA = (240, 236, 214)
TINTA = (30, 38, 30)
VERDE = (31, 106, 48)
VERDE2 = (60, 150, 70)
ROJO = (200, 40, 50)
AZUL = (40, 90, 190)
AMARILLO = (242, 194, 48)
BLANCO = (252, 252, 250)
NEGRO = (30, 30, 34)
GRIS = (120, 128, 120)
NARANJA = (235, 130, 40)


def ruido(im, s, f=2.5):
    a = np.asarray(im).astype(np.int16)
    a = a + np.random.default_rng(s).normal(0, f, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def marco(p, w, h):
    p.rect(16, 16, w - 16, h - 16, None, VERDE, 6)
    p.rect(28, 28, w - 28, h - 28, None, AMARILLO, 2)


def pagina(titulo, sub=None, w=W, h=H):
    p = Hoja(w, h, CREMA)
    marco(p, w, h)
    p.texto((w / 2, 72), titulo, "cartel", 30, VERDE)
    if sub:
        p.texto((w / 2, 108), sub, "texto2", 19, TINTA)
    return p


def versos(p, lineas, y0=220, paso=50, tam=23, x=W / 2, color=TINTA, tipo="texto2"):
    for k, v in enumerate(lineas):
        p.texto((x, y0 + k * paso), v, tipo, tam, color)


def flecha(p, a, b, color, ancho=4, punta=16, doble=False):
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p.linea([a, (b[0] - math.cos(ang) * punta * 0.6, b[1] - math.sin(ang) * punta * 0.6)], color, ancho)
    p.poli([b, (b[0] - punta * math.cos(ang - 0.45), b[1] - punta * math.sin(ang - 0.45)), (b[0] - punta * math.cos(ang + 0.45), b[1] - punta * math.sin(ang + 0.45))], color)
    if doble:
        flecha(p, b, a, color, ancho, punta)


def camiseta(p, cx, cy, tam, color, dorsal=None, color_num=BLANCO):
    s = tam / 2
    p.poli([(cx - s * 0.5, cy - s), (cx + s * 0.5, cy - s), (cx + s * 1.1, cy - s * 0.55), (cx + s * 0.78, cy - s * 0.25), (cx + s * 0.55, cy - s * 0.4), (cx + s * 0.55, cy + s),
            (cx - s * 0.55, cy + s), (cx - s * 0.55, cy - s * 0.4), (cx - s * 0.78, cy - s * 0.25), (cx - s * 1.1, cy - s * 0.55)], color, NEGRO, 3)
    if dorsal is not None:
        p.texto((cx, cy + s * 0.1), str(dorsal), "cartel", int(tam * 0.55), color_num)


# ------------------------------------------------------------------ 16: la clasificación de la liguilla
def clasificacion():
    d = I.LIGUILLA
    p = pagina("LA LIGUILLA DEL CLUB", "tras jugar todos contra todos")
    cols = [("EQUIPO", 70, "lm"), ("PJ", 270, "mm"), ("G", 320, "mm"), ("E", 365, "mm"), ("P", 410, "mm"), ("GF", 460, "mm"), ("GC", 510, "mm"), ("PTS", 570, "mm")]
    p.rect(40, 150, W - 40, 205, VERDE)
    for t, x, a in cols:
        p.texto((x, 178), t, "cartel", 22, BLANCO, a)
    for k, (eq, t) in enumerate(zip(d["equipos"], d["tabla"])):
        y = 235 + k * 62
        p.rect(40, y - 28, W - 40, y + 28, BLANCO if k % 2 == 0 else (226, 240, 222), GRIS, 1)
        vals = [eq, "3", t["g"], t["e"], t["p"], t["gf"], t["gc"], t["pts"]]
        for (_, x, a), v in zip(cols, vals):
            p.texto((x, y), str(v), "texto" if x == 70 else "cartel", 22 if x == 70 else 26, TINTA, a)
    p.texto((W / 2, 510), "RESULTADOS CONOCIDOS", "cartel", 24, VERDE)
    for k, i in enumerate(d["conocidos"]):
        a, b = d["partidos"][i]
        x, y = d["resultados"][i]
        yy = 565 + k * 58
        p.rect(60, yy - 24, W - 60, yy + 24, BLANCO, AMARILLO, 3)
        p.texto((90, yy), d["equipos"][a], "texto", 22, TINTA, "lm")
        p.texto((W / 2, yy), f"{x} - {y}", "cartel", 30, ROJO)
        p.texto((W - 90, yy), d["equipos"][b], "texto", 22, TINTA, "rm")
    p.texto((W / 2, 790), "Victoria: 2 puntos · Empate: 1 · Derrota: 0", "texto2", 19, GRIS)
    return p.final()


# ------------------------------------------------------------------ 18, 19 y 21: los cromos
def acertijo_cromos():
    d = I.CROMOS
    p = pagina("EL TABLÓN DEL MÍSTER", "la lista que se perdió")
    lineas = ["«Dos camisetas me faltan", "en la lista de salida.", ""] + _envolver("La primera es la de " + d["acertijo"][0] + ".", 30) + [""]         + _envolver("Y la segunda, la de " + d["acertijo"][1] + ".", 30) + ["", "Dadme sus dos dorsales.»"]
    versos(p, lineas, 190, 44, 21)
    return p.final()


def _envolver(texto, ancho):
    palabras, lin, lineas = texto.split(), "", []
    for w in palabras:
        if len(lin) + len(w) + 1 > ancho:
            lineas.append(lin)
            lin = w
        else:
            lin = (lin + " " + w).strip()
    lineas.append(lin)
    return lineas


def cromo_anverso(grupo):
    p = pagina("CROMOS DEL CLUB ESTRELLA", "dorsal y nombre")
    for k, i in enumerate(grupo):
        j = I.CROMOS["jugadores"][i]
        y0 = 150 + k * 235
        p.rect(60, y0, W - 60, y0 + 215, BLANCO, ROJO, 5)
        camiseta(p, 180, y0 + 108, 150, ROJO, j["dorsal"])
        p.texto((380, y0 + 80), j["nombre"].split()[0], "cartel", 34, TINTA)
        p.texto((380, y0 + 128), j["nombre"].split()[1], "cartel", 34, TINTA)
        p.texto((W / 2, y0 + 195), "CLUB ESTRELLA · 1970", "texto2", 14, GRIS)
    return p.final()


def cromo_reverso(grupo):
    p = pagina("FICHA TÉCNICA", "club estrella")
    for k, i in enumerate(grupo):
        j = I.CROMOS["jugadores"][i]
        y0 = 150 + k * 235
        p.rect(60, y0, W - 60, y0 + 215, (226, 240, 222), VERDE, 5)
        p.texto((90, y0 + 34), j["nombre"], "cartel", 26, VERDE, "lm")
        lin = [("Puesto", j["pos"]), ("Pie", j["pie"]), ("Altura", f"{j['altura']} cm"), ("Edad", f"{j['edad']} años")]
        for r, (a, b) in enumerate(lin):
            p.texto((90, y0 + 80 + r * 34), a + ":", "texto2", 20, GRIS, "lm")
            p.texto((220, y0 + 80 + r * 34), b, "texto", 21, TINTA, "lm")
    return p.final()


# ------------------------------------------------------------------ 41 y 43: las jugadas del VAR
def campo_var(p, x0, y0, w, h):
    ux, uy = w / 100, h / 60
    p.rect(x0, y0, x0 + w, y0 + h, (70, 150, 70), BLANCO, 4)
    for k in range(0, 100, 10):
        if (k // 10) % 2 == 0:
            p.rect(x0 + k * ux, y0, x0 + (k + 10) * ux, y0 + h, (80, 162, 80))
    for k in range(5, 100, 5):
        p.linea([(x0 + k * ux, y0), (x0 + k * ux, y0 + h)], (60, 130, 60), 1)
    p.linea([(x0 + 50 * ux, y0), (x0 + 50 * ux, y0 + h)], BLANCO, 4)
    p.disco(x0 + 50 * ux, y0 + h / 2, 22, None, BLANCO, 3)
    p.rect(x0 + 84 * ux, y0 + h * 0.25, x0 + w, y0 + h * 0.75, None, BLANCO, 3)
    p.rect(x0, y0 + h * 0.25, x0 + 16 * ux, y0 + h * 0.75, None, BLANCO, 3)
    return ux, uy


def dibujar_jugada(p, j, letra, y0):
    x0, w, h = 40, 550, 210
    ux, uy = campo_var(p, x0, y0, w, h)
    P = lambda x, y: (x0 + x * ux, y0 + 10 + y * (h - 20) / 60)
    for n, x, y in j["defensores"]:
        cx, cy = P(x, y)
        p.disco(cx, cy, 13, AMARILLO if n == "P" else ROJO, NEGRO, 2)
        p.texto((cx, cy), n, "cartel", 14, NEGRO if n == "P" else BLANCO)
    for k, (n, x, y) in enumerate(j["atacantes"]):
        cx, cy = P(x, y)
        p.disco(cx, cy, 13, AZUL, NEGRO, 2)
        p.texto((cx, cy), n, "cartel", 14, BLANCO)
    sx, sy = P(*j["atacantes"][j["pasador"]][1:])
    rx, ry = P(*j["atacantes"][j["receptor"]][1:])
    ang = math.atan2(ry - sy, rx - sx)
    flecha(p, (sx + 16 * math.cos(ang), sy + 16 * math.sin(ang)), (rx - 16 * math.cos(ang), ry - 16 * math.sin(ang)), BLANCO, 3, 14)
    p.disco(sx - 14, sy + 14, 6, BLANCO, NEGRO, 2)
    if j["saque"] == "banda":
        p.texto((sx + 24, sy + (-18 if sy > 30 else 22)), "SAQUE DE BANDA", "cartel", 17, BLANCO, "lm", NEGRO, 3)
    p.rect(x0, y0 - 28, x0 + 150, y0 - 2, VERDE)
    p.texto((x0 + 75, y0 - 15), f"JUGADA {letra}", "cartel", 17, BLANCO)


def jugadas_var(inicio, titulo):
    p = pagina(titulo)
    for k in range(3):
        j = I.VAR["jugadas"][inicio + k]
        dibujar_jugada(p, j, "ABCDEF"[inicio + k], 175 + k * 235)
    return p.final()


def regla_var():
    p = pagina("EL REGLAMENTO DEL FUERA DE JUEGO", "del libro del árbitro")
    versos(p, ["«Los azules atacan hacia la derecha.", "", "Cuando sale el pase, quien lo recibe", "está en fuera de juego si está más cerca",
               "de la línea de gol que el balón y que el", "penúltimo contrario. El portero cuenta", "como un contrario más.", "",
               "A la misma altura que ese contrario,", "no hay falta. En su propio campo,", "tampoco. Y en un saque de banda,", "nunca.»"], 175, 46, 20)
    return p.final()


# ------------------------------------------------------------------ 42, 49 y 53: el pase en cadena
ETIQUETA_PASE = ["P", "A", "B", "C", "D", "E", "Z"]


def campo_pase():
    d = I.PASE
    p = Hoja(W * 2, H, CREMA)
    marco(p, W * 2, H)
    p.texto((W, 72), "EL CAMPO DE ENTRENAMIENTO", "cartel", 30, VERDE)
    ux = 80
    x0, y0 = 70, 140
    p.rect(x0 - 20, y0 - 20, x0 + d["ancho"] * ux + 20, y0 + d["alto"] * ux + 20, (70, 150, 70), BLANCO, 4)
    for a in range(d["ancho"] + 1):
        for b in range(d["alto"] + 1):
            p.disco(x0 + a * ux, y0 + b * ux, 3, (50, 120, 50))
    for a in range(d["ancho"] + 1):
        p.linea([(x0 + a * ux, y0), (x0 + a * ux, y0 + d["alto"] * ux)], (60, 135, 60), 1)
    for b in range(d["alto"] + 1):
        p.linea([(x0, y0 + b * ux), (x0 + d["ancho"] * ux, y0 + b * ux)], (60, 135, 60), 1)
    for x, y in d["rivales"]:
        cx, cy = x0 + x * ux, y0 + y * ux
        p.disco(cx, cy, 24, ROJO, NEGRO, 3)
        p.texto((cx, cy), "X", "cartel", 22, BLANCO)
    for k, (x, y) in enumerate(d["jugadores"]):
        cx, cy = x0 + x * ux, y0 + y * ux
        p.disco(cx, cy, 26, AMARILLO if k == 0 else AZUL, NEGRO, 3)
        p.texto((cx, cy), ETIQUETA_PASE[k], "cartel", 24, NEGRO if k == 0 else BLANCO)
    return p.final()


def regla_pase():
    p = pagina("LA PIZARRA DEL ENTRENADOR", "el pase en cadena")
    versos(p, ["«El balón corre por el suelo,", "recto, de un jugador a otro.", "", "Si en su camino hay un rival,", "o un compañero, el pase se corta.", "",
               "Cada jugador lo toca una vez:", "salimos del portero, la P,", "y acabamos en el delantero, la Z,", "con todos los demás por el camino.»"], 190, 50, 21)
    return p.final()


# ------------------------------------------------------------------ 54, 55 y 59: las notas del entrenador
def notas(filas, titulo):
    d = I.ALINEACION
    p = pagina(titulo, "del 1 al 9, como las pone el míster")
    cab = ["POR", "DEF", "LAT", "MED", "DEL"]
    x0 = 210
    p.rect(40, 150, W - 40, 205, VERDE)
    p.texto((60, 178), "JUGADOR", "cartel", 20, BLANCO, "lm")
    for c, t in enumerate(cab):
        p.texto((x0 + c * 78, 178), t, "cartel", 20, BLANCO)
    for k, i in enumerate(filas):
        y = 255 + k * 110
        p.rect(40, y - 45, W - 40, y + 45, BLANCO if k % 2 == 0 else (226, 240, 222), GRIS, 1)
        p.texto((60, y), d["jugadores"][i], "texto", 24, TINTA, "lm")
        for c in range(5):
            p.texto((x0 + c * 78, y), str(d["notas"][i][c]), "cartel", 34, ROJO if d["notas"][i][c] >= 8 else TINTA)
    p.texto((W / 2, 780), "POR portero · DEF defensa · LAT lateral · MED medio · DEL delantero", "texto2", 15, GRIS)
    return p.final()


def regla_alineacion():
    p = pagina("EL MÍSTER SENTENCIA", "ante la plantilla")
    versos(p, ["«Cinco camisetas y cinco puestos:", "ni un hueco ni un repetido.", "", "Ninguna nota se discute,", "y la suma de las cinco", "debe ser la más alta posible.»"], 220, 56, 23)
    return p.final()


# ------------------------------------------------------------------ 37, 39 y 33: el informe de los penaltis
def evento_penalti(p, x0, y0, k, ev):
    w, h = 250, 160
    p.rect(x0, y0, x0 + w, y0 + h, (70, 150, 70), BLANCO, 3)
    p.rect(x0 + 25, y0 + 30, x0 + w - 25, y0 + 108, None, BLANCO, 6)           # portería
    for a in range(1, 3):
        p.linea([(x0 + 25 + a * (w - 50) / 3, y0 + 34), (x0 + 25 + a * (w - 50) / 3, y0 + 104)], (200, 220, 200), 1)
    zx = [x0 + 25 + (w - 50) * f for f in (1 / 6, 3 / 6, 5 / 6)]
    sx = zx[ev["salto"]]
    p.rect(sx - 20, y0 + 50, sx + 20, y0 + 106, NARANJA, NEGRO, 3)
    p.disco(sx, y0 + 43, 11, (240, 200, 160), NEGRO, 2)
    bx = zx[ev["tiro"]]
    p.disco(bx, y0 + 134, 14, BLANCO, NEGRO, 3)
    p.poli([(bx, y0 + 126), (bx + 8, y0 + 132), (bx + 5, y0 + 142), (bx - 5, y0 + 142), (bx - 8, y0 + 132)], NEGRO)
    p.texto((x0 + 14, y0 + 15), str(k), "cartel", 20, BLANCO, "lm")
    col, txt = (BLANCO, "GOL") if ev["gol"] else (AMARILLO, "PARADA")
    p.texto((x0 + w - 14, y0 + 15), txt, "cartel", 18, col, "rm")


def informe(inicio, fin, titulo):
    p = pagina(titulo, "tiros vistos desde el punto de penalti")
    for n, k in enumerate(range(inicio, fin)):
        x0 = 40 + (n % 2) * 290
        y0 = 150 + (n // 2) * 200
        evento_penalti(p, x0, y0, k + 1, I.PENALTIS["historial"][k])
    return p.final()


def leyenda_penaltis():
    p = pagina("CÓMO SE LEE EL INFORME", "notas del entrenador")
    evento_penalti(p, 190, 160, "", {"tiro": 0, "salto": 2, "gol": True})
    flecha(p, (150, 280), (230, 252), ROJO, 4)
    p.texto((140, 300), "el balón", "texto2", 18, ROJO, "rm")
    flecha(p, (480, 190), (440, 215), NARANJA, 4)
    p.texto((490, 175), "el portero", "texto2", 18, NARANJA, "lm")
    versos(p, ["«Los tres lados se miran", "desde el punto de penalti.", "", "El portero decide hacia dónde se lanza", "antes de que el balón salga,", "mirando solo los dos últimos tiros.", "",
               "Los tiros del informe están en orden.»"], 400, 48, 21)
    return p.final()


# ------------------------------------------------------------------ 26, 61 y 63: el cuadro de eliminatorias
def titulares():
    d = I.ELIMINATORIAS
    p = pagina("LOS TITULARES DE LA PRENSA", "de la última copa")
    eq = d["equipos"]
    for k, e in enumerate(d["enunciados"]):
        tipo = e[0]
        if tipo == "cae_cuartos":
            t = f"{eq[e[1]]} se despidió en cuartos"
        elif tipo == "cae_semis":
            t = f"{eq[e[1]]} cayó en semifinales"
        elif tipo == "campeon":
            t = f"{eq[e[1]]} se proclama campeón"
        elif tipo == "subcampeon":
            t = f"{eq[e[1]]} pierde la final"
        elif tipo == "vence":
            t = f"{eq[e[1]]} elimina a {eq[e[2]]}"
        else:
            t = f"{eq[e[1]]} no llegó a la final"
        y = 190 + k * 120
        p.rect(60, y - 42, W - 60, y + 42, BLANCO, GRIS, 3)
        p.rect(60, y - 42, 100, y + 42, VERDE)
        p.texto((80, y), str(k + 1), "cartel", 26, BLANCO)
        for r, l in enumerate(_envolver(t, 28)):
            p.texto((125, y - 14 + r * 32), l, "texto", 22, TINTA, "lm")
    return p.final()


def cuadro():
    d = I.ELIMINATORIAS
    p = Hoja(W, H * 2, CREMA)
    marco(p, W, H * 2)
    p.texto((W / 2, 72), "EL CUADRO DE LA COPA", "cartel", 30, VERDE)
    ys = [230, 430, 630, 830, 1000, 1200, 1400, 1600]
    for k, y in enumerate(ys):
        p.rect(36, y - 22, 196, y + 22, BLANCO, VERDE, 3)
        p.texto((116, y), d["equipos"][k], "texto", 19, TINTA)
    qf = [(ys[2 * i] + ys[2 * i + 1]) / 2 for i in range(4)]
    sf = [(qf[0] + qf[1]) / 2, (qf[2] + qf[3]) / 2]
    fy = (sf[0] + sf[1]) / 2
    for i in range(4):
        a, b = ys[2 * i], ys[2 * i + 1]
        p.linea([(196, a), (226, a), (226, b), (196, b)], TINTA, 4)
        p.linea([(226, qf[i]), (246, qf[i])], TINTA, 4)
        p.rect(246, qf[i] - 18, 316, qf[i] + 18, None, GRIS, 2)
        p.linea([(316, qf[i]), (336, qf[i])], TINTA, 4)
    for i in range(2):
        a, b = qf[2 * i], qf[2 * i + 1]
        p.linea([(336, a), (336, b)], TINTA, 4)
        p.linea([(336, sf[i]), (356, sf[i])], TINTA, 4)
        p.rect(356, sf[i] - 18, 426, sf[i] + 18, None, GRIS, 2)
        p.linea([(426, sf[i]), (446, sf[i])], TINTA, 4)
    p.linea([(446, sf[0]), (446, sf[1])], TINTA, 4)
    p.linea([(446, fy), (466, fy)], TINTA, 4)
    p.rect(466, fy - 22, 566, fy + 22, None, AMARILLO, 4)
    return p.final()


# ------------------------------------------------------------------ 66 y 67: el calendario
def cruces_jornada1():
    d = I.CALENDARIO
    p = pagina("EL CALENDARIO DE LA LIGA", "jornada 1")
    orden = d["orden"]
    arriba = orden[:4]
    abajo = [orden[7], orden[6], orden[5], orden[4]]
    for c in range(4):
        x = 78 + c * 128
        p.rect(x - 56, 230, x + 56, 290, BLANCO, VERDE, 4)
        p.texto((x, 260), d["clubes"][arriba[c]], "texto", 17, TINTA)
        p.rect(x - 56, 500, x + 56, 560, BLANCO, ROJO, 4)
        p.texto((x, 530), d["clubes"][abajo[c]], "texto", 17, TINTA)
        p.linea([(x, 290), (x, 500)], GRIS, 3)
        p.rect(x - 24, 378, x + 24, 412, CREMA)
        p.texto((x, 395), "vs", "cartel", 22, GRIS)
    p.disco(78, 205, 14, AMARILLO, NEGRO, 3)
    p.texto((78, 205), "1", "cartel", 16, NEGRO)
    return p.final()


def metodo_calendario():
    p = pagina("EL MÉTODO DEL CALENDARIO", "del secretario de la liga")
    versos(p, ["«En la primera jornada juegan", "los que están frente a frente.", "", "Luego, el primero de arriba, a la izquierda,",
               "se queda quieto; los demás avanzan un", "puesto en el sentido de las agujas", "del reloj, y vuelven a mirarse", "de frente.", "", "Así nadie repite rival en toda la liga.»"], 190, 50, 20)
    return p.final()


# ------------------------------------------------------------------ 70 y 71: las sustituciones
POS8 = [(110, 450), (260, 290), (260, 610), (400, 220), (400, 450), (400, 680), (530, 320), (530, 580)]


def alineacion_inicial():
    d = I.SUSTITUCIONES
    p = pagina("LA ALINEACIÓN DEL MÍSTER", "ocho puestos y ocho dorsales")
    p.rect(50, 150, W - 50, 780, (70, 150, 70), BLANCO, 4)
    p.linea([(W / 2 + 100, 150), (W / 2 + 100, 780)], BLANCO, 3)
    for k, (x, y) in enumerate(POS8):
        camiseta(p, x, y, 110, AZUL, d["dorsales"][k])
        p.disco(x - 42, y - 50, 17, AMARILLO, NEGRO, 2)
        p.texto((x - 42, y - 50), str(k + 1), "cartel", 20, NEGRO)
    return p.final()


def ordenes_cambios():
    d = I.SUSTITUCIONES
    p = pagina("LAS ÓRDENES DEL MÍSTER", "en cada ronda de cambios")
    y0 = 200
    for n, (tipo, ps) in enumerate(d["ops"]):
        cy = y0 + n * 195
        p.rect(50, cy - 80, W - 50, cy + 80, BLANCO, VERDE, 3)
        p.disco(85, cy - 55, 20, AMARILLO, NEGRO, 3)
        p.texto((85, cy - 55), str(n + 1), "cartel", 22, NEGRO)
        if tipo == "ciclo":
            pts = [(190, cy + 40), (330, cy - 30), (470, cy + 40)]
            nodos = [(190, cy + 40), (330, cy - 30), (470, cy + 40)]
            for k, (x, y) in enumerate(nodos):
                p.disco(x, y, 28, BLANCO, VERDE, 4)
                p.texto((x, y), str(ps[k]), "cartel", 28, TINTA)
            flecha(p, (222, cy + 6), (298, cy - 18), ROJO, 4)
            flecha(p, (362, cy - 18), (438, cy + 6), ROJO, 4)
            flecha(p, (440, cy + 54), (220, cy + 54), ROJO, 4)
        else:
            nodos = [(250, cy + 15), (410, cy + 15)]
            for k, (x, y) in enumerate(nodos):
                p.disco(x, y, 28, BLANCO, VERDE, 4)
                p.texto((x, y), str(ps[k]), "cartel", 28, TINTA)
            flecha(p, (284, cy + 15), (376, cy + 15), ROJO, 5, 16, True)
    p.texto((W / 2, 800), "Las tres órdenes, en este orden, " + ("tres" if d["repeticiones"] == 3 else str(d["repeticiones"])) + " veces seguidas.", "texto2", 19, TINTA)
    return p.final()


# ------------------------------------------------------------------ 75 y 79: la grada
def filas_grada():
    d = I.GRADA
    p = pagina("EL MOSAICO DE LA GRADA", "una vuelta entera de butacas")
    n = d["n"]
    lado = 40
    x0 = (W - n * lado) / 2
    for f in range(d["pasos"] + 1):
        y = 175 + f * 90
        p.texto((x0 - 12, y + lado / 2), str(f + 1), "cartel", 20, VERDE, "rm")
        for i in range(n):
            col = ROJO if (f == 0 and d["inicio"][i]) else BLANCO
            p.rect(x0 + i * lado, y, x0 + (i + 1) * lado - 3, y + lado, col, NEGRO if (f == 0 or f == d["pasos"]) else GRIS, 3 if (f == 0 or f == d["pasos"]) else 1)
    return p.final()


def regla_grada():
    p = pagina("LA REGLA DE LAS BUTACAS", "del encargado de la grada")
    versos(p, ["«Cada butaca mira a las dos vecinas", "de la fila de arriba: la de su izquierda", "y la de su derecha.", "",
               "La grada es un anillo: la última", "de un lado es vecina de la primera.", "", "Si las dos van del mismo color,",
               "la butaca queda en blanco.", "", "Si van de colores distintos,", "se pinta de rojo.»"], 175, 48, 21)
    return p.final()


# ------------------------------------------------------------------ 86 y 87: los cinco aros
def icono(p, k, cx, cy):
    if k == "14":                                         # la tabla de la liguilla
        p.rect(cx - 34, cy - 30, cx + 34, cy + 30, BLANCO, NEGRO, 3)
        for a in range(1, 4):
            p.linea([(cx - 34, cy - 30 + a * 15), (cx + 34, cy - 30 + a * 15)], NEGRO, 2)
        p.linea([(cx - 10, cy - 30), (cx - 10, cy + 30)], NEGRO, 2)
    elif k == "40":                                       # la banderola del VAR
        p.linea([(cx - 24, cy + 34), (cx - 24, cy - 34)], NEGRO, 5)
        p.poli([(cx - 24, cy - 34), (cx + 30, cy - 20), (cx - 24, cy - 6)], AMARILLO, NEGRO, 3)
    elif k == "52":                                       # la camiseta de la alineación
        camiseta(p, cx, cy, 70, ROJO)
    elif k == "69":                                       # las flechas de los cambios
        flecha(p, (cx - 30, cy - 14), (cx + 30, cy - 14), VERDE, 5, 14)
        flecha(p, (cx + 30, cy + 14), (cx - 30, cy + 14), ROJO, 5, 14)
    else:                                                 # la grada
        for f in range(3):
            for i in range(4):
                p.rect(cx - 36 + i * 19, cy - 30 + f * 21, cx - 21 + i * 19, cy - 14 + f * 21, [ROJO, BLANCO][(i + f) % 2], NEGRO, 2)


def aros():
    p = pagina("LOS CINCO AROS DE LA COPA", "cada uno con su giro")
    for n, k in enumerate(I.ORDEN_ARO):
        y = 215 + n * 125
        p.rect(50, y - 52, W - 50, y + 52, BLANCO, VERDE, 3)
        icono(p, k, 130, y)
        g = I.GIRO[k]
        for m in range(abs(g)):
            x = 280 + m * 52
            col = VERDE2 if g > 0 else ROJO
            if g > 0:
                p.poli([(x, y - 24), (x + 32, y), (x, y + 24), (x + 12, y)], col, NEGRO, 2)
            else:
                p.poli([(x + 32, y - 24), (x, y), (x + 32, y + 24), (x + 20, y)], col, NEGRO, 2)
    return p.final()


def dial():
    p = pagina("EL DIAL", "doce posiciones")
    cx, cy, r = W / 2, 440, 230
    p.disco(cx, cy, r + 26, BLANCO, VERDE, 6)
    p.disco(cx, cy, r - 70, CREMA, VERDE, 3)
    for k in range(12):
        ang = -math.pi / 2 + k * math.pi / 6
        p.linea([(cx + (r + 22) * math.cos(ang), cy + (r + 22) * math.sin(ang)), (cx + (r + 4) * math.cos(ang), cy + (r + 4) * math.sin(ang))], TINTA, 4)
        p.texto((cx + (r - 38) * math.cos(ang), cy + (r - 38) * math.sin(ang)), str(k + 1), "cartel", 36, ROJO if k == 0 else TINTA)
    flecha(p, (cx - 40, cy + 12), (cx + 40, cy + 12), VERDE2, 6, 20)
    p.texto((cx, cy + 56), "se cuenta hacia la derecha", "texto2", 15, GRIS)
    p.texto((W / 2, 780), "El uno, arriba del todo.", "texto2", 20, TINTA)
    return p.final()


# ------------------------------------------------------------------ datos de las apps
def inyectar(carpeta):
    d = I.LIGUILLA
    datos = {
        "14-liguilla.js": {"equipos": d["equipos"], "partidos": d["partidos"], "desconocidos": d["desconocidos"], "resultados": d["resultados"], "aro": I.ARO["14"]},
        "20-convocatoria.js": {"jugadores": [{"dorsal": j["dorsal"], "nombre": j["nombre"]} for j in I.CROMOS["jugadores"]], "solucion": I.CROMOS["solucion"]},
        "40-var.js": {"fuera": I.VAR["fuera"], "aro": I.ARO["40"]},
        "48-pase.js": {"jugadores": I.PASE["jugadores"], "rivales": I.PASE["rivales"], "etiquetas": ETIQUETA_PASE},
        "52-alineacion.js": {"jugadores": I.ALINEACION["jugadores"], "puestos": I.ALINEACION["puestos"], "notas": I.ALINEACION["notas"], "maximo": I.ALINEACION["maximo"], "aro": I.ARO["52"]},
        "46-penaltis.js": {"regla": I.PENALTIS["regla"], "ultimos": I.PENALTIS["ultimos"], "tanda": I.PENALTIS["tanda"]},
        "51-eliminatorias.js": {"equipos": I.ELIMINATORIAS["equipos"], "bits": I.ELIMINATORIAS["bits"]},
        "64-calendario.js": {"clubes": I.CALENDARIO["clubes"], "solucion": I.CALENDARIO["solucion"], "jornada": I.CALENDARIO["jornada"]},
        "69-sustituciones.js": {"dorsales": I.SUSTITUCIONES["dorsales"], "final": I.SUSTITUCIONES["final"], "aro": I.ARO["69"]},
        "72-grada.js": {"final": I.GRADA["final"], "n": I.GRADA["n"], "pasos": I.GRADA["pasos"], "aro": I.ARO["72"]},
        "85-aros.js": {"orden": I.ORDEN_ARO, "final": I.FINAL_ARO},
    }
    for app, dd in datos.items():
        ruta = os.path.join(carpeta, "minijuegos", app)
        txt = open(ruta, encoding="utf-8").read() if os.path.exists(ruta) else ""
        if "/*DATOS*/" not in txt:
            continue
        a, b = txt.index("/*DATOS*/") + len("/*DATOS*/"), txt.index("/*FIN*/")
        open(ruta, "w", encoding="utf-8", newline="\n").write(txt[:a] + json.dumps(dd, ensure_ascii=False) + txt[b:])


def main(carpeta="juegos/aventuras-ca/futbol"):
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)

    def g(k, im):
        ruido(im, sum(map(ord, k))).save(os.path.join(arte, f"{k}.png"))

    def mosaico(nombre, im, filas, cols, cartas):
        im = ruido(im, sum(map(ord, nombre)))
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))
        for pieza, k in zip(cortar(im, filas, cols), cartas):
            pieza.save(os.path.join(arte, f"{k}.png"))
    g("16", clasificacion())
    g("18", acertijo_cromos())
    for k, grupo in (("19", I.CROMOS["tarjetas"][0]), ("21", I.CROMOS["tarjetas"][1])):
        g(k, cromo_anverso(grupo))
        g(k + "r", cromo_reverso(grupo))
    g("41", jugadas_var(0, "LAS JUGADAS DEL VAR (I)"))
    g("43", jugadas_var(3, "LAS JUGADAS DEL VAR (II)"))
    g("45", regla_var())
    mosaico("campo", campo_pase(), 1, 2, ("42", "49"))
    g("53", regla_pase())
    g("54", notas([0, 1, 2], "LAS NOTAS DEL ENTRENADOR (I)"))
    g("55", notas([3, 4], "LAS NOTAS DEL ENTRENADOR (II)"))
    g("59", regla_alineacion())
    g("37", informe(0, 6, "EL INFORME DE PENALTIS (I)"))
    g("39", informe(6, len(I.PENALTIS["historial"]), "EL INFORME DE PENALTIS (II)"))
    g("33", leyenda_penaltis())
    g("26", titulares())
    mosaico("cuadro", cuadro(), 2, 1, ("61", "63"))
    g("66", cruces_jornada1())
    g("67", metodo_calendario())
    g("70", alineacion_inicial())
    g("71", ordenes_cambios())
    g("75", filas_grada())
    g("79", regla_grada())
    g("86", aros())
    g("87", dial())
    inyectar(carpeta)
    print("láminas de Fútbol escritas en", arte)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

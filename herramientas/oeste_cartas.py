"""Láminas de «Dry Gulch, 1878: El Tren del Oro» (versión de 60 cartas, 22 oct 2026). Todas las pistas son dibujos o acertijos: ninguna carta
escribe la respuesta ni explica cómo se resuelve su puzle. Datos de herramientas/instancias_oeste.py.

  16 el telegrama · 18 el acertijo del banco · 19 y 21 el cuadro del banco (dos mitades) · 41 y 43 la caja del carro (dos mitades) · 45 las piezas
  42 y 49 el cuadro de apuestas (dos mitades) · 53 la regla de las apuestas · 54 los pesos · 55 los valores · 59 el carro · 37 el corro de pistoleros
  39 y 33 el duelo · 26 la regla de la bodega · 61 y 63 el suelo de la bodega (dos mitades) · 66 y 67 el plano de la bomba (dos mitades)
  70 los vagones · 71 la maniobra · 75 los hierros sospechosos · 79 el hierro del ganadero · 86 el orden de las coordenadas · 87 el cuadrado de Polibio
Uso (desde la raíz del repo):  python herramientas/oeste_cartas.py [carpeta_juego]
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oeste import Hoja, PAPEL, TINTA, ROJO, OCRE, ARENA, ARENA2, MADERA, MADERA2, HIERRO, NEGRO, BLANCO  # noqa: E402
from mosaicos import cortar  # noqa: E402
import instancias_oeste as I  # noqa: E402

W, H = 630, 882
VERDE = (84, 110, 60)
AZUL = (60, 92, 128)
COLORES = [(176, 58, 46), (60, 92, 128), (84, 110, 60), (214, 160, 70), (140, 84, 120), (200, 110, 50), (90, 70, 50), (120, 128, 134)]
NOMBRES_COLOR = ["rojo", "azul", "verde", "amarillo", "violeta", "naranja", "marrón", "gris"]


def ruido(im, s, f=3.0):
    a = np.asarray(im).astype(np.int16)
    a = a + np.random.default_rng(s).normal(0, f, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def pagina(titulo, sub=None, w=W, h=H):
    p = Hoja(w, h, PAPEL)
    p.rect(16, 16, w - 16, h - 16, None, TINTA, 5)
    p.rect(28, 28, w - 28, h - 28, None, MADERA, 2)
    p.texto((w / 2, 72), titulo, "cartel", 32, ROJO)
    if sub:
        p.texto((w / 2, 110), sub, "texto2", 20, TINTA)
    return p


def versos(p, lineas, y0=220, paso=50, tam=24, x=W / 2, color=TINTA):
    for k, v in enumerate(lineas):
        p.texto((x, y0 + k * paso), v, "texto2", tam, color)


# ------------------------------------------------------------------ 16: el telegrama
def telegrama():
    d = I.VALLAS
    p = pagina("TELEGRAMA URGENTE", "recibido en la estafeta de Dry Gulch")
    grupos = [d["cifrado"][i:i + 5] for i in range(0, len(d["cifrado"]), 5)]
    for k, g in enumerate(grupos):
        x = 80 + (k % 4) * 125
        y = 200 + (k // 4) * 80
        p.rect(x - 52, y - 30, x + 52, y + 30, ARENA, TINTA, 3)
        p.texto((x, y), g, "texto", 25, TINTA)
    # el zigzag sin letras
    rieles = d["rieles"]
    y0, paso = 450, 62
    for r in range(rieles):
        p.linea([(60, y0 + r * paso), (W - 60, y0 + r * paso)], ARENA2, 2)
    n = 17
    pts = []
    for i in range(n):
        f = d["zigzag"][i]
        pts.append((80 + i * (W - 160) / (n - 1), y0 + f * paso))
    p.linea(pts, ROJO, 3)
    for (x, y) in pts:
        p.disco(x, y, 10, PAPEL, TINTA, 3)
    versos(p, ["«Escribo bajando y subiendo por la vía,", "y luego leo por pisos.»"], 760, 40, 21)
    return p.final()


# ------------------------------------------------------------------ 18: el acertijo del banco
def acertijo_banco():
    p = pagina("EL ACERTIJO DEL BANQUERO", "colgado en la ventanilla")
    versos(p, ["«Detesto las copias.", "En cada fila y en cada columna", "cada cifra ha de quedar sola.", "",
               "Tacha las que sobran, pero nunca", "dos manchas se tocan de lado,", "y lo que quede en blanco", "ha de estar todo unido.»"], 200, 52, 24)
    return p.final()


# ------------------------------------------------------------------ 19/21: el cuadro del banco
def cuadro_banco():
    d = I.HITORI
    n = d["n"]
    p = Hoja(W, H * 2, PAPEL)
    p.rect(16, 16, W - 16, H * 2 - 16, None, TINTA, 5)
    p.rect(28, 28, W - 28, H * 2 - 28, None, MADERA, 2)
    p.texto((W / 2, 72), "EL CUADRO DEL BANCO", "cartel", 32, ROJO)
    lado = 96
    x0, y0 = (W - n * lado) / 2, 882 - 2 * lado
    for r in range(n):
        for c in range(n):
            p.rect(x0 + c * lado, y0 + r * lado, x0 + (c + 1) * lado, y0 + (r + 1) * lado, ARENA, TINTA, 3)
            p.texto((x0 + c * lado + lado / 2, y0 + r * lado + lado / 2), str(d["cifras"][r][c]), "cartel", 52, TINTA)
    return p.final()


# ------------------------------------------------------------------ 41/43 y 45: la caja del carro
PAL_PIEZA = {"A": (176, 58, 46), "B": (60, 92, 128), "C": (84, 110, 60), "D": (214, 160, 70), "E": (140, 84, 120), "F": (200, 110, 50)}


def letra_pieza(i):
    return "ABCDEF"[i]


def caja_carro():
    d = I.PENTOMINO
    f, c = d["filas"], d["cols"]
    p = Hoja(W * 2, H, PAPEL)
    p.rect(16, 16, W * 2 - 16, H - 16, None, TINTA, 5)
    p.rect(28, 28, W * 2 - 28, H - 28, None, MADERA, 2)
    p.texto((W, 72), "LA CAJA DEL CARRO", "cartel", 32, ROJO)
    lado = 100
    x0, y0 = W - c * lado / 2, (H - f * lado) / 2 + 30
    for r in range(f):
        for q in range(c):
            p.rect(x0 + q * lado, y0 + r * lado, x0 + (q + 1) * lado, y0 + (r + 1) * lado, ARENA, TINTA, 3)
    for letra, cs in d["fijas"].items():
        col = PAL_PIEZA[letra_pieza(d["piezas"].index(letra))]
        for (r, q) in cs:
            p.rect(x0 + q * lado + 3, y0 + r * lado + 3, x0 + (q + 1) * lado - 3, y0 + (r + 1) * lado - 3, col, TINTA, 3)
            p.texto((x0 + q * lado + lado / 2, y0 + r * lado + lado / 2), letra_pieza(d["piezas"].index(letra)), "cartel", 44, BLANCO)
    return p.final()


def piezas_carro():
    d = I.PENTOMINO
    p = pagina("LAS SEIS PIEZAS", "de la carga del carro")
    for k, letra in enumerate(d["piezas"]):
        cx = 150 + (k % 2) * 330
        cy = 230 + (k // 2) * 190
        cs = I.PIEZAS[letra]
        mr, mc = max(r for r, q in cs), max(q for r, q in cs)
        lado = 36
        ox, oy = cx - (mc + 1) * lado / 2, cy - (mr + 1) * lado / 2
        for (r, q) in cs:
            p.rect(ox + q * lado, oy + r * lado, ox + (q + 1) * lado, oy + (r + 1) * lado, PAL_PIEZA[letra_pieza(k)], TINTA, 3)
        p.texto((cx - 110, cy), letra_pieza(k), "cartel", 40, TINTA)
    versos(p, ["«Piezas de cinco cuadros, ni una más.", "Se pueden girar y dar la vuelta.»"], 800, 36, 19)
    return p.final()


# ------------------------------------------------------------------ 42/49 y 53: el cuadro de apuestas
def cuadro_apuestas():
    d = I.KAKURO
    n = d["n"]
    p = Hoja(W * 2, H, PAPEL)
    p.rect(16, 16, W * 2 - 16, H - 16, None, TINTA, 5)
    p.rect(28, 28, W * 2 - 28, H - 28, None, MADERA, 2)
    p.texto((W, 72), "EL CUADRO DE APUESTAS", "cartel", 32, ROJO)
    lado = 100
    x0, y0 = W - n * lado / 2, (H - n * lado) / 2 + 30
    blancas = {tuple(q) for q in d["blancas"]}
    clues = {}
    for t in d["tandas"]:
        pos = (t["r"], t["c"] - 1) if t["tipo"] == "h" else (t["r"] - 1, t["c"])
        clues.setdefault(pos, {})["a" if t["tipo"] == "h" else "d"] = t["suma"]
    for r in range(n):
        for c in range(n):
            xa, ya = x0 + c * lado, y0 + r * lado
            if (r, c) in blancas:
                p.rect(xa, ya, xa + lado, ya + lado, ARENA, TINTA, 3)
            elif (r, c) in clues:
                p.rect(xa, ya, xa + lado, ya + lado, MADERA2, TINTA, 3)
                p.linea([(xa, ya), (xa + lado, ya + lado)], ARENA, 3)
                if "a" in clues[(r, c)]:
                    p.texto((xa + lado * 0.72, ya + lado * 0.28), str(clues[(r, c)]["a"]), "cartel", 26, BLANCO)
                if "d" in clues[(r, c)]:
                    p.texto((xa + lado * 0.28, ya + lado * 0.72), str(clues[(r, c)]["d"]), "cartel", 26, BLANCO)
            else:
                p.rect(xa, ya, xa + lado, ya + lado, NEGRO, TINTA, 3)
    return p.final()


def regla_apuestas():
    p = pagina("LA REGLA DEL TAHÚR", "escrita en el reverso de una baraja")
    versos(p, ["«En cada casilla va una cifra", "del uno al nueve.", "", "Lo que suman las de una racha,", "hacia la derecha o hacia abajo,",
               "es lo que el número manda.", "", "Y en una misma racha", "no se repite ninguna.»"], 190, 50, 24)
    return p.final()


# ------------------------------------------------------------------ 54, 55, 59: la carga del carro
ARTICULOS = ["barril de whisky", "saco de harina", "caja de herramientas", "fardo de pieles", "cajón de balas", "rollo de alambre", "bidón de petróleo", "baúl de plata"]


def lista_articulos(titulo, sub, valores, prefijo, sufijo):
    p = pagina(titulo, sub)
    for k, nombre in enumerate(ARTICULOS):
        y = 190 + k * 80
        p.rect(60, y - 30, W - 60, y + 30, ARENA, TINTA, 3)
        p.rect(78, y - 20, 118, y + 20, COLORES[k], TINTA, 3)
        p.texto((140, y), nombre, "texto", 22, TINTA, "lm")
        p.texto((W - 80, y), f"{prefijo}{valores[k]}{sufijo}", "cartel", 30, ROJO, "rm")
    return p.final()


def pesos():
    return lista_articulos("LO QUE PESA CADA COSA", "en arrobas, según el herrador", I.MOCHILA["pesos"], "", " ar.")


def valores():
    return lista_articulos("LO QUE VALE CADA COSA", "en dólares, según el tendero", I.MOCHILA["valores"], "", " $")


def carro():
    p = pagina("EL CARRO DEL ABUELO", "del cuaderno del carretero")
    versos(p, ["«Mi carro es viejo.", "", f"Pasadas las {I.MOCHILA['capacidad']} arrobas,", "cruje el eje y se acabó el viaje.", "",
               "Quiero la cartera más gorda", "sin romper nada.", "", "Una vez de cada cosa,", "que no hay dos iguales.»"], 190, 52, 24)
    return p.final()


# ------------------------------------------------------------------ 37, 39, 33: el duelo en corro
def corro():
    d = I.JOSEFO
    n = d["n"]
    p = pagina("EL CORRO DE PISTOLEROS", "alrededor de la mesa del saloon")
    cx, cy, R = W / 2, 480, 250
    p.disco(cx, cy, 150, MADERA, TINTA, 4)
    for k in range(n):
        ang = -math.pi / 2 + 2 * math.pi * k / n
        x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
        p.disco(x, y, 33, ARENA, TINTA, 3)
        p.texto((x, y), str(k + 1), "cartel", 26, TINTA)
        if k == 0:
            p.poli([(x - 22, y - 33), (x + 22, y - 33), (x + 12, y - 60), (x - 12, y - 60)], ROJO, TINTA, 3)
    p.texto((cx, cy), "mesa", "texto2", 26, ARENA)
    return p.final()


def regla_duelo():
    p = pagina("LA CUENTA DEL SHERIFF", "del libro de duelos")
    versos(p, ["«Empiezo a contar desde el sombrero rojo,", "con el uno, y sigo hacia la derecha,", "como las agujas del reloj.", "",
               "El que cae en cada cuarto número", "se va del corro, y se sigue", "desde el siguiente.»"], 200, 54, 24)
    return p.final()


def nota_duelo():
    p = pagina("LA NOTA DEL JUEZ", "clavada en la puerta")
    versos(p, ["«Se repite la cuenta, vuelta tras vuelta,", "hasta que solo queda uno en pie.", "", "Ese se lleva el botín.", "",
               "El que se siente donde no debe,", "para el duelo antes que yo.»"], 200, 54, 24)
    return p.final()


# ------------------------------------------------------------------ 26 y 61/63: la bodega
def regla_bodega():
    p = pagina("EL REFRÁN DEL TABERNERO", "grabado en un barril")
    versos(p, ["«Los barriles se empujan, no se tiran.", "", "Solo de a uno,", "siempre hacia delante,", "y nunca contra un muro", "o contra otro barril.", "",
               "Cada uno ha de acabar", "en su hueco del suelo.»"], 190, 50, 24)
    return p.final()


def suelo_bodega():
    d = I.SOKOBAN
    p = Hoja(W * 2, H, PAPEL)
    p.rect(16, 16, W * 2 - 16, H - 16, None, TINTA, 5)
    p.rect(28, 28, W * 2 - 28, H - 28, None, MADERA, 2)
    p.texto((W, 72), "EL SUELO DE LA BODEGA", "cartel", 32, ROJO)
    lado = 75
    f, c = d["filas"], d["cols"]
    x0, y0 = W - c * lado / 2, (H - f * lado) / 2 + 30
    muros = {tuple(q) for q in d["muros"]}
    metas = {tuple(q) for q in d["metas"]}
    for r in range(f):
        for q in range(c):
            xa, ya = x0 + q * lado, y0 + r * lado
            if (r, q) in muros:
                p.rect(xa, ya, xa + lado, ya + lado, MADERA2, TINTA, 3)
                p.linea([(xa, ya + lado / 2), (xa + lado, ya + lado / 2)], TINTA, 2)
            else:
                p.rect(xa, ya, xa + lado, ya + lado, ARENA, ARENA2, 2)
            if (r, q) in metas:
                p.disco(xa + lado / 2, ya + lado / 2, 24, NEGRO, TINTA, 3)
                p.linea([(xa + lado / 2 - 12, ya + lado / 2 - 12), (xa + lado / 2 + 12, ya + lado / 2 + 12)], ARENA, 3)
                p.linea([(xa + lado / 2 + 12, ya + lado / 2 - 12), (xa + lado / 2 - 12, ya + lado / 2 + 12)], ARENA, 3)
    return p.final()


# ------------------------------------------------------------------ 66/67: el plano de la bomba
def pintar_tubo(p, x, y, lado, m, color=TINTA):
    cx, cy = x + lado / 2, y + lado / 2
    for bit, dx, dy in ((1, 0, -1), (2, 1, 0), (4, 0, 1), (8, -1, 0)):
        if m & bit:
            p.linea([(cx, cy), (cx + dx * lado / 2, cy + dy * lado / 2)], color, 14)
    p.disco(cx, cy, 9, color)


def plano_bomba():
    d = I.TUBERIAS
    n = d["n"]
    p = Hoja(W, H * 2, PAPEL)
    p.rect(16, 16, W - 16, H * 2 - 16, None, TINTA, 5)
    p.rect(28, 28, W - 28, H * 2 - 28, None, MADERA, 2)
    p.texto((W / 2, 72), "EL PLANO DE LA BOMBA", "cartel", 32, ROJO)
    lado = 96
    x0, y0 = (W - n * lado) / 2, 882 - 2 * lado
    fijas = {(r, c): m for r, c, m in d["fijas"]}
    for r in range(n):
        for c in range(n):
            xa, ya = x0 + c * lado, y0 + r * lado
            p.rect(xa, ya, xa + lado, ya + lado, ARENA if (r, c) in fijas else PAPEL, TINTA if (r, c) in fijas else ARENA2, 3 if (r, c) in fijas else 1)
            if (r, c) in fijas:
                pintar_tubo(p, xa, ya, lado, fijas[(r, c)])
    return p.final()


# ------------------------------------------------------------------ 70/71: la maniobra de vagones
def vagon(p, x, y, color, peso):
    p.rect(x - 38, y - 30, x + 38, y + 24, color, TINTA, 4)
    p.disco(x - 22, y + 30, 11, NEGRO, TINTA, 2)
    p.disco(x + 22, y + 30, 11, NEGRO, TINTA, 2)
    p.texto((x, y - 3), str(peso), "cartel", 32, BLANCO)


def pesos_vagones():
    d = I.VAGONES
    p = pagina("LOS VAGONES DE LA ESTACIÓN", "pesados en toneladas")
    for k, peso in enumerate(d["pesos"]):
        x = 130 + (k % 3) * 185
        y = 240 + (k // 3) * 170
        vagon(p, x, y, COLORES[k], peso)
    versos(p, ["Los vagones, de color en color,", "tal y como esperan en la vía."], 700, 38, 20)
    return p.final()


def regla_maniobra():
    p = pagina("LA MANIOBRA", "del jefe de estación")
    versos(p, ["«Solo hay un apartadero ciego:", "el último que entra es el primero que sale.", "", "El tren ha de salir ordenado,",
               "del más ligero al más pesado,", "el ligero pegado a la locomotora.", "", "Y los vagones entran por orden de llegada,", "sin saltarse el turno.»"], 190, 50, 22)
    return p.final()


# ------------------------------------------------------------------ 75/79: los hierros
def hierro(p, g, x, y, lado, col=TINTA):
    n = len(g)
    for r in range(n):
        for c in range(n):
            p.rect(x + c * lado, y + r * lado, x + (c + 1) * lado, y + (r + 1) * lado, col if g[r][c] else ARENA, TINTA, 2)


def hierros_sospechosos():
    d = I.HIERROS
    p = pagina("LOS HIERROS DE LA SUBASTA", "ocho marcas en las reses")
    for k, (g, _) in enumerate(d["candidatos"]):
        x = 85 + (k % 2) * 290
        y = 170 + (k // 2) * 170
        p.texto((x - 10, y + 60), str(k + 1), "cartel", 40, ROJO, "rm")
        hierro(p, g, x + 10, y, 30)
    return p.final()


def hierro_ganadero():
    d = I.HIERROS
    p = pagina("EL HIERRO DE DON ABEL", "grabado a fuego en su puerta")
    hierro(p, d["maestro"], W / 2 - 110, 190, 55)
    versos(p, ["«Mis reses llevan mi hierro,", "lo mismo derecho que de lado,", "boca arriba o boca abajo,",
               "o visto en un espejo.", "", "Los ladrones se equivocan siempre", "en un solo cuadrito.»"], 500, 40, 21)
    return p.final()


# ------------------------------------------------------------------ 86/87: el cuadrado de Polibio
def orden_coordenadas():
    p = pagina("LAS CINCO COORDENADAS", "del libro del telegrafista")
    versos(p, ["«Cinco veces dio el telégrafo", "su pareja de cifras, y van así:", "",
               "primera, la del mensaje en zigzag;", "segunda, la de la caja que se llena;", "tercera, la del carro que aguanta;",
               "cuarta, la del tren que se ordena;", "y quinta, la que huele a barril.", "", "La primera cifra de cada pareja", "es el piso; la segunda, la puerta.»"], 175, 46, 21)
    return p.final()


def cuadrado_polibio():
    p = pagina("EL CUADRADO DE POLIBIO", "la J y la I comparten casilla")
    lado = 80
    x0, y0 = (W - 6 * lado) / 2, 190
    for c in range(5):
        p.texto((x0 + (c + 1.5) * lado, y0 + lado / 2), str(c + 1), "cartel", 34, ROJO)
    for r in range(5):
        p.texto((x0 + lado / 2, y0 + (r + 1.5) * lado), str(r + 1), "cartel", 34, ROJO)
        for c in range(5):
            xa, ya = x0 + (c + 1) * lado, y0 + (r + 1) * lado
            p.rect(xa, ya, xa + lado, ya + lado, ARENA, TINTA, 3)
            p.texto((xa + lado / 2, ya + lado / 2), I.POLIBIO[r][c], "cartel", 40, TINTA)
    return p.final()


# ------------------------------------------------------------------ datos de las apps
def inyectar(carpeta):
    datos = {
        "14-telegrama.js": {"claro": I.VALLAS["claro"], "rieles": I.VALLAS["rieles"], "coord": I.COORD["14"]},
        "20-banco.js": {"cifras": I.HITORI["cifras"], "tachones": I.HITORI["tachones"]},
        "40-caja.js": {"filas": I.PENTOMINO["filas"], "cols": I.PENTOMINO["cols"], "piezas": I.PENTOMINO["piezas"], "fijas": I.PENTOMINO["fijas"], "coord": I.COORD["40"]},
        "48-apuestas.js": {"n": I.KAKURO["n"], "blancas": I.KAKURO["blancas"], "tandas": I.KAKURO["tandas"]},
        "52-carga.js": {"articulos": I.ARTICULOS if hasattr(I, "ARTICULOS") else ARTICULOS, "pesos": I.MOCHILA["pesos"], "valores": I.MOCHILA["valores"],
                        "capacidad": I.MOCHILA["capacidad"], "optimo": I.MOCHILA["optimo"], "coord": I.COORD["52"]},
        "46-duelo.js": {"n": I.JOSEFO["n"], "sobrevive": I.JOSEFO["sobrevive"], "caen": I.JOSEFO["caen"]},
        "51-bodega.js": {"filas": I.SOKOBAN["filas"], "cols": I.SOKOBAN["cols"], "muros": I.SOKOBAN["muros"], "metas": I.SOKOBAN["metas"], "cajas": I.SOKOBAN["cajas"],
                         "jugador": I.SOKOBAN["jugador"], "coord": I.COORD["51"]},
        "64-bomba.js": {"n": I.TUBERIAS["n"], "tubos": I.TUBERIAS["tubos"], "inicio": I.TUBERIAS["inicio"], "fijas": I.TUBERIAS["fijas"]},
        "69-maniobra.js": {"pesos": I.VAGONES["pesos"], "coord": I.COORD["69"]},
        "72-hierros.js": {"candidatos": len(I.HIERROS["candidatos"]), "autenticos": [i + 1 for i in I.HIERROS["autenticos"]]},
        "85-polibio.js": {"palabra": I.PALABRA},
    }
    for app, d in datos.items():
        ruta = os.path.join(carpeta, "minijuegos", app)
        txt = open(ruta, encoding="utf-8").read() if os.path.exists(ruta) else ""
        if "/*DATOS*/" not in txt:
            continue
        a, b = txt.index("/*DATOS*/") + len("/*DATOS*/"), txt.index("/*FIN*/")
        open(ruta, "w", encoding="utf-8", newline="\n").write(txt[:a] + json.dumps(d, ensure_ascii=False) + txt[b:])


def main(carpeta="juegos/aventuras-ca/oeste"):
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)

    def g(k, im):
        ruido(im, int(k)).save(os.path.join(arte, f"{k}.png"))

    def mosaico(nombre, im, filas, cols, cartas):
        im = ruido(im, sum(map(ord, nombre)))
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))
        for pieza, k in zip(cortar(im, filas, cols), cartas):
            pieza.save(os.path.join(arte, f"{k}.png"))
    g("16", telegrama())
    g("18", acertijo_banco())
    mosaico("banco", cuadro_banco(), 2, 1, ("19", "21"))
    mosaico("caja", caja_carro(), 1, 2, ("41", "43"))
    g("45", piezas_carro())
    mosaico("apuestas", cuadro_apuestas(), 1, 2, ("42", "49"))
    g("53", regla_apuestas())
    g("54", pesos())
    g("55", valores())
    g("59", carro())
    g("37", corro())
    g("39", regla_duelo())
    g("33", nota_duelo())
    g("26", regla_bodega())
    mosaico("bodega", suelo_bodega(), 1, 2, ("61", "63"))
    mosaico("bomba", plano_bomba(), 2, 1, ("66", "67"))
    g("70", pesos_vagones())
    g("71", regla_maniobra())
    g("75", hierros_sospechosos())
    g("79", hierro_ganadero())
    g("86", orden_coordenadas())
    g("87", cuadrado_polibio())
    inyectar(carpeta)
    print("láminas de Oeste escritas en", arte)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

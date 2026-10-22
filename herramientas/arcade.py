"""Láminas de «Game Over, 1985: La Última Moneda» (versión de 60 cartas, 22 oct 2026). Todas las pistas son dibujos o acertijos:
ninguna carta escribe la respuesta ni explica cómo se resuelve su puzle. Datos de herramientas/instancias_arcade.py.

  16 el circuito de la placa · 18 el acertijo del aparcamiento · 19 y 21 el aparcamiento de naves (dos mitades)
  41 y 43 las tandas del sprite (filas 1-6 y 7-12) · 45 la regla de la compresión · 42 los bytes del mensaje · 49 la tabla de caracteres · 53 la regla de los bytes
  54 y 55 las pistas de los fantasmas · 59 el plano de los pasillos · 37 el marcador · 39 la regla del marcador · 33 las fichas de la bolsa
  26 la regla de la tabla de récords · 61 y 63 la tabla de récords (dos mitades) · 66 y 67 el dibujo del puzle deslizante (dos mitades)
  70 la autopista · 71 las velocidades de los carriles · 75 las monedas de la máquina · 79 el precio · 86 y 87 la clave del arranque
Uso (desde la raíz del repo):  python herramientas/arcade.py [carpeta_juego]
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
import instancias_arcade as I  # noqa: E402

W, H = 630, 882
FONDO = (16, 12, 38)
PANEL = (30, 24, 66)
CIAN = (0, 226, 255)
MAGENTA = (255, 70, 200)
AMARILLO = (255, 222, 70)
VERDE = (90, 255, 150)
BLANCO = (240, 240, 255)
GRIS = (120, 116, 160)
ROJO = (255, 80, 90)
NEON = [(255, 80, 90), (0, 226, 255), (90, 255, 150), (255, 222, 70), (255, 70, 200), (255, 150, 50), (150, 110, 255), (240, 240, 255)]


def ruido(im, s, f=2.0):
    a = np.asarray(im).astype(np.int16)
    a = a + np.random.default_rng(s).normal(0, f, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def pagina(titulo, sub=None, borde=MAGENTA, w=W, h=H):
    p = Hoja(w, h, FONDO)
    p.rect(16, 16, w - 16, h - 16, None, borde, 6)
    p.rect(28, 28, w - 28, h - 28, None, CIAN, 2)
    p.texto((w / 2 + 26, 70), titulo, "cartel", 30, AMARILLO)
    if sub:
        p.texto((w / 2 + 26, 108), sub, "texto2", 20, CIAN)
    return p


def versos(p, lineas, y0=220, paso=56, tam=26, x=W / 2, color=BLANCO):
    for k, v in enumerate(lineas):
        p.texto((x, y0 + k * paso), v, "texto2", tam, color)


def ancha(titulo, borde=MAGENTA):
    p = Hoja(W * 2, H, FONDO)
    p.rect(16, 16, W * 2 - 16, H - 16, None, borde, 6)
    p.rect(28, 28, W * 2 - 28, H - 28, None, CIAN, 2)
    p.texto((W, 66), titulo, "cartel", 32, AMARILLO)
    return p


# ------------------------------------------------------------------ 16: el circuito
def circuito():
    d = I.CIRCUITO
    p = pagina("EL CIRCUITO DE LA PLACA", "seis interruptores, dos lámparas", MAGENTA)
    pos = {}
    for k, c in enumerate("ABCDEF"):
        pos[c] = (80, 190 + k * 100)
    for g in d["puertas"]:
        pos[g[0]] = None
    # capas
    capas = [["P1", "P2", "P3"], ["P4", "P5"], ["P6", "P7"]]
    xs = [200, 340, 470]
    for cap, x in zip(capas, xs):
        ys = []
        for n in cap:
            g = next(q for q in d["puertas"] if q[0] == n)
            y = (pos[g[2]][1] + pos[g[3]][1]) / 2
            ys.append(y)
        # separarlas si se pisan
        for i in range(1, len(ys)):
            if ys[i] - ys[i - 1] < 120:
                ys[i] = ys[i - 1] + 120
        for n, y in zip(cap, ys):
            pos[n] = (x, y)
    ancho, alto = 90, 62
    # cables: un color por origen y un pasillo vertical propio para cada uno, para que se puedan seguir
    col = {n: NEON[k % 8] for k, n in enumerate(["A", "B", "C", "D", "E", "F", "P1", "P2", "P3", "P4", "P5"])}
    pasillo = {}
    for g in d["puertas"]:
        for k, src in enumerate((g[2], g[3])):
            if src not in "ABCDEF":
                pasillo.setdefault(src, len(pasillo))
    for g in d["puertas"]:
        for k, src in enumerate((g[2], g[3])):
            x0, y0 = pos[src]
            x0 += 22 if src in "ABCDEF" else ancho / 2
            x1, y1 = pos[g[0]][0] - ancho / 2, pos[g[0]][1] + (-14 if k == 0 else 14)
            if src in "ABCDEF":
                mx = (x0 + x1) / 2
            else:
                mx = x0 + 10 + 9 * list(pasillo).index(src)
            p.linea([(x0, y0), (mx, y0), (mx, y1), (x1, y1)], col[src], 3)
    for c in "ABCDEF":
        p.rect(pos[c][0] - 22, pos[c][1] - 22, pos[c][0] + 22, pos[c][1] + 22, PANEL, CIAN, 3)
        p.texto(pos[c], c, "cartel", 28, BLANCO)
    for g in d["puertas"]:
        x, y = pos[g[0]]
        p.rect(x - ancho / 2, y - alto / 2, x + ancho / 2, y + alto / 2, PANEL, MAGENTA, 4)
        p.texto((x, y - 6), g[1], "cartel", 22, AMARILLO)
        p.texto((x, y + 16), g[0].replace("P", "puerta "), "texto2", 13, GRIS)
    for nombre, g in d["salidas"].items():
        x0, y0 = pos[g]
        x1 = 565
        p.linea([(x0 + ancho / 2, y0), (x1 - 22, y0)], VERDE, 3)
        p.disco(x1, y0, 22, PANEL, VERDE, 4)
        p.texto((x1, y0), nombre, "cartel", 26, VERDE)
    p.texto((W / 2, 780), "Lámpara X encendida, lámpara Y apagada.", "texto2", 22, AMARILLO)
    p.texto((W / 2, 815), "Puertas: AND, OR, XOR, NAND y NOR.", "texto2", 17, GRIS)
    return p.final()


# ------------------------------------------------------------------ 18, 19/21: el atasco de naves
def acertijo_atasco():
    p = pagina("EL ACERTIJO DEL APARCAMIENTO", "pintado en el suelo", MAGENTA)
    versos(p, ["«Las naves solo avanzan y retroceden", "por donde apuntan: nunca de lado.", "", "Ninguna puede pisar a otra",
               "ni salirse del tablero.", "", "La nave roja quiere salir por la", "puerta de la derecha.»"], 200, 52, 24)
    return p.final()


def aparcamiento():
    d = I.ATASCO
    n = d["n"]
    p = Hoja(W, H * 2, FONDO)
    p.rect(16, 16, W - 16, H * 2 - 16, None, MAGENTA, 6)
    p.rect(28, 28, W - 28, H * 2 - 28, None, CIAN, 2)
    p.texto((W / 2 + 26, 70), "EL APARCAMIENTO DE NAVES", "cartel", 28, AMARILLO)
    lado = 88
    x0, y0 = (W - n * lado) / 2 - 10, 882 - 3 * lado
    for y in range(n):
        for x in range(n):
            p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, PANEL, (70, 60, 130), 2)
    for k, (f, c, largo, hor) in enumerate(d["naves"]):
        xa, ya = x0 + c * lado + 6, y0 + f * lado + 6
        xb, yb = (xa + largo * lado - 12, ya + lado - 12) if hor else (xa + lado - 12, ya + largo * lado - 12)
        col = ROJO if k == 0 else NEON[(k % 7) + 1]
        p.rect(xa, ya, xb, yb, col, BLANCO, 3)
        p.texto(((xa + xb) / 2, (ya + yb) / 2), str(k + 1), "cartel", 34, FONDO)
    # la puerta
    fy = y0 + d["naves"][0][0] * lado
    p.rect(x0 + n * lado + 4, fy + 20, x0 + n * lado + 24, fy + lado - 20, VERDE)
    p.texto((x0 + n * lado + 40, fy + lado / 2), "SALIDA", "texto", 14, VERDE, "lm")
    return p.final()


# ------------------------------------------------------------------ 41/43/45: el sprite comprimido
def tandas(f0, f1, titulo):
    d = I.SPRITE_D
    p = pagina(titulo, "una línea por fila del dibujo", MAGENTA)
    for k in range(f0, f1):
        y = 190 + (k - f0) * 100
        p.texto((60, y), f"fila {k + 1}", "texto", 22, CIAN, "lm")
        for j, v in enumerate(d["tandas"][k]):
            x = 210 + j * 62
            p.rect(x - 24, y - 24, x + 24, y + 24, PANEL, AMARILLO, 3)
            p.texto((x, y), str(v), "cartel", 28, BLANCO)
    return p.final()


def regla_sprite():
    p = pagina("LA REGLA DE LA COMPRESIÓN", "del manual de la máquina", MAGENTA)
    versos(p, ["«Cada fila del dibujo mide doce casillas.", "", "Se cuenta de izquierda a derecha:",
               "primero las casillas apagadas,", "luego las encendidas, y así", "alternando hasta el final.", "",
               "Si la fila empieza por encendidas,", "el primer número es un cero.»"], 190, 52, 24)
    return p.final()


# ------------------------------------------------------------------ 42/49/53: los bytes
def bytes_mensaje():
    d = I.ASCII
    p = pagina("EL MENSAJE DE LA PANTALLA", "ocho bytes en hexadecimal", MAGENTA)
    for k, b in enumerate(d["bytes"]):
        x = 100 + (k % 4) * 150
        y = 300 + (k // 4) * 200
        p.rect(x - 56, y - 50, x + 56, y + 50, PANEL, CIAN, 4)
        p.texto((x, y), b, "cartel", 52, AMARILLO)
    return p.final()


def tabla_caracteres():
    d = I.ASCII
    p = pagina("LA TABLA DE CARACTERES", "letra y byte", MAGENTA)
    for k, (c, h) in enumerate(d["tabla"].items()):
        col, fila = divmod(k, 13)
        x = 130 + col * 250
        y = 160 + fila * 50
        p.texto((x, y), c, "cartel", 32, VERDE, "rm")
        p.texto((x + 20, y), h, "cartel", 32, BLANCO, "lm")
    return p.final()


def regla_bytes():
    p = pagina("LA REGLA DE LOS BYTES", "del manual de la máquina", MAGENTA)
    versos(p, ["«Cada byte son dos cifras", "en base dieciséis:", "del 0 al 9 y de la A a la F.", "",
               "La tabla dice qué letra", "esconde cada byte.", "", "El mensaje se lee de izquierda", "a derecha y de arriba abajo.»"], 200, 52, 24)
    return p.final()


# ------------------------------------------------------------------ 54/55/59: los fantasmas
def pistas_fantasmas(ini, fin, titulo):
    d = I.FANTASMAS
    p = pagina(titulo, "lo que se sabe de los cuatro", MAGENTA)
    y = 200
    for k in range(ini, fin):
        texto = d["pistas"][k].replace(" de el ", " del ")
        # partir en líneas de unos 34 caracteres
        palabras, lin, lineas = texto.split(), "", []
        for w in palabras:
            if len(lin) + len(w) + 1 > 36:
                lineas.append(lin)
                lin = w
            else:
                lin = (lin + " " + w).strip()
        lineas.append(lin)
        p.texto((60, y - 8), f"{k + 1}.", "cartel", 24, CIAN, "lm")
        for j, l in enumerate(lineas):
            p.texto((100, y + j * 30), l, "texto2", 21, BLANCO, "lm")
        y += 30 * len(lineas) + 38
    return p.final()


def plano_pasillos():
    d = I.FANTASMAS
    p = pagina("EL PLANO DE LOS PASILLOS", "cuatro pasillos, de izquierda a derecha", MAGENTA)
    for k in range(4):
        x = 90 + k * 140
        p.rect(x - 40, 230, x + 40, 640, PANEL, CIAN, 3)
        p.disco(x, 280, 24, PANEL, AMARILLO, 3)
        p.texto((x, 280), str(k + 1), "cartel", 30, AMARILLO)
    for k, c in enumerate([(255, 80, 90), (255, 150, 200), (0, 226, 255), (255, 150, 50)]):
        p.disco(90 + k * 140, 720, 26, c, BLANCO, 3)
    p.texto((W / 2, 780), "los cuatro fantasmas: rojo, rosa, cian y naranja", "texto2", 19, GRIS)
    p.texto((W / 2, 810), "velocidades: lento, normal, rápido y loco", "texto2", 19, GRIS)
    p.texto((W / 2, 840), "frutas: cereza, fresa, naranja y manzana", "texto2", 19, GRIS)
    return p.final()


# ------------------------------------------------------------------ 37/39/33: el marcador (cuadrado mágico)
def marcador():
    d = I.MAGICO
    p = pagina("EL MARCADOR DEL JEFE", "dieciséis casillas, seis ya puestas", MAGENTA)
    lado = 120
    x0, y0 = (W - 4 * lado) / 2, 190
    dados = {(x, y): v for x, y, v in d["dados"]}
    for y in range(4):
        for x in range(4):
            p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, PANEL, CIAN, 3)
            if (x, y) in dados:
                p.texto((x0 + x * lado + lado / 2, y0 + y * lado + lado / 2), str(dados[(x, y)]), "cartel", 48, AMARILLO)
    return p.final()


def regla_marcador():
    p = pagina("LA REGLA DEL MARCADOR", "grabada en la carcasa", MAGENTA)
    versos(p, ["«Los dieciséis números van del 1 al 16,", "cada uno una sola vez.", "", "Todas las filas, todas las columnas",
               "y las dos diagonales largas", "suman lo mismo: treinta y cuatro.»"], 230, 56, 25)
    return p.final()


def fichas_bolsa():
    d = I.MAGICO
    puestos = {v for _, _, v in d["dados"]}
    p = pagina("LAS FICHAS DE LA BOLSA", "las que aún no están en el marcador", MAGENTA)
    resto = [n for n in range(1, 17) if n not in puestos]
    for k, n in enumerate(resto):
        x = 120 + (k % 4) * 125
        y = 230 + (k // 4) * 130
        p.disco(x, y, 46, PANEL, VERDE, 4)
        p.texto((x, y), str(n), "cartel", 40, BLANCO)
    return p.final()


# ------------------------------------------------------------------ 26, 61/63: la tabla de récords
def regla_record():
    p = pagina("LA REGLA DE LA TABLA", "nota del programador", MAGENTA)
    versos(p, ["«La tabla de récords se ordena", "de menos a más puntos, de arriba abajo.", "",
               "Solo se pueden cambiar de sitio", "dos entradas que están", "una justo encima de la otra.", "",
               "Y la máquina no tiene paciencia:", "hay un número máximo de cambios.»"], 200, 52, 24)
    return p.final()


def tabla_record():
    d = I.RANKING
    p = Hoja(W, H * 2, FONDO)
    p.rect(16, 16, W - 16, H * 2 - 16, None, MAGENTA, 6)
    p.rect(28, 28, W - 28, H * 2 - 28, None, CIAN, 2)
    p.texto((W / 2 + 26, 70), "LA TABLA DE RÉCORDS", "cartel", 30, AMARILLO)
    p.texto((W / 2 + 26, 108), "tal como la dejó la máquina", "texto2", 20, CIAN)
    alto = 160
    y0 = 882 - 4 * alto + 40
    for k, v in enumerate(d["puntos"]):
        y = y0 + k * alto
        p.rect(70, y - 56, W - 70, y + 56, PANEL, GRIS, 3)
        p.rect(100, y - 36, 172, y + 36, NEON[k], BLANCO, 3)
        p.texto((250, y), f"{v}", "cartel", 52, BLANCO, "lm")
        p.texto((W - 100, y), "puntos", "texto2", 22, GRIS, "rm")
    return p.final()


# ------------------------------------------------------------------ 66/67: el dibujo del puzle deslizante
def dibujo_deslizante():
    d = I.DESLIZANTE
    p = Hoja(W, H * 2, FONDO)
    p.rect(16, 16, W - 16, H * 2 - 16, None, MAGENTA, 6)
    p.rect(28, 28, W - 28, H * 2 - 28, None, CIAN, 2)
    p.texto((W / 2 + 26, 70), "EL DIBUJO FINAL", "cartel", 32, AMARILLO)
    p.texto((W / 2 + 26, 108), "las ocho fichas, ya ordenadas", "texto2", 20, CIAN)
    lado = 150
    x0, y0 = (W - 3 * lado) / 2, 882 - 2 * lado - 40
    for y in range(3):
        for x in range(3):
            v = d["objetivo"][y][x]
            if v:
                p.rect(x0 + x * lado + 4, y0 + y * lado + 4, x0 + (x + 1) * lado - 4, y0 + (y + 1) * lado - 4, PANEL, NEON[v - 1], 5)
                p.texto((x0 + x * lado + lado / 2, y0 + y * lado + lado / 2), str(v), "cartel", 64, NEON[v - 1])
            else:
                p.rect(x0 + x * lado + 4, y0 + y * lado + 4, x0 + (x + 1) * lado - 4, y0 + (y + 1) * lado - 4, FONDO, GRIS, 3)
    return p.final()


# ------------------------------------------------------------------ 70/71: la autopista
def autopista():
    d = I.RANA
    p = pagina("LA AUTOPISTA", "tal como está al empezar", MAGENTA)
    ancho, car = d["ancho"], len(d["carriles"])
    lado = 66
    x0, y0 = (W - ancho * lado) / 2, 170
    for f in range(car + 2):
        for c in range(ancho):
            col = (40, 120, 70) if f in (0, car + 1) else PANEL
            p.rect(x0 + c * lado, y0 + f * lado, x0 + (c + 1) * lado, y0 + (f + 1) * lado, col, (60, 54, 110), 1)
    p.texto((x0 + ancho * lado / 2, y0 + lado / 2), "META", "cartel", 24, VERDE)
    for i, L in enumerate(d["carriles"]):
        for pos in L["coches"]:
            p.rect(x0 + pos * lado + 8, y0 + (i + 1) * lado + 14, x0 + (pos + 1) * lado - 8, y0 + (i + 2) * lado - 14, NEON[(i + pos) % 7], BLANCO, 2)
        p.texto((x0 - 18, y0 + (i + 1.5) * lado), str(i + 1), "cartel", 22, AMARILLO)
    r, c = d["inicio"]
    p.disco(x0 + c * lado + lado / 2, y0 + r * lado + lado / 2, 22, VERDE, BLANCO, 3)
    p.texto((x0 + c * lado + lado / 2, y0 + r * lado + lado / 2), "R", "cartel", 24, FONDO)
    p.texto((x0 + 1.2 * lado, y0 + (car + 1.5) * lado), "SALIDA", "cartel", 24, VERDE)
    return p.final()


def velocidades():
    d = I.RANA
    p = pagina("LAS VELOCIDADES DEL TRÁFICO", "carril por carril", MAGENTA)
    for i, L in enumerate(d["carriles"]):
        y = 220 + i * 100
        p.texto((70, y), f"carril {i + 1}", "texto", 24, AMARILLO, "lm")
        flecha = 1 if L["dir"] > 0 else -1
        for k in range(L["vel"]):
            x = 280 + k * 80 * flecha
            p.poli([(x - 28 * flecha, y - 16), (x + 4 * flecha, y - 16), (x + 4 * flecha, y - 30), (x + 38 * flecha, y), (x + 4 * flecha, y + 30), (x + 4 * flecha, y + 16), (x - 28 * flecha, y + 16)], CIAN)
        p.texto((445, y), f"{L['vel']} casilla{'s' if L['vel'] > 1 else ''} por turno", "texto2", 17, BLANCO, "lm")
    versos(p, ["En cada turno, la rana se mueve primero", "y luego se mueven los coches.", "Los que se salen por un lado", "entran por el otro."], 712, 32, 19)
    return p.final()


# ------------------------------------------------------------------ 75/79: las monedas
def monedas_maquina():
    d = I.MONEDAS
    p = pagina("LAS MONEDAS DE LA MÁQUINA", "de las que hay cuantas se quiera", MAGENTA)
    for k, v in enumerate(d["monedas"]):
        x = 150 + (k % 2) * 330
        y = 280 + (k // 2) * 240
        p.disco(x, y, 80, AMARILLO, BLANCO, 5)
        p.disco(x, y, 62, None, (180, 150, 20), 3)
        p.texto((x, y), str(v), "cartel", 64, FONDO)
    return p.final()


def precio():
    d = I.MONEDAS
    p = pagina("EL PRECIO DE LA PARTIDA", "en la pantalla de continuar", MAGENTA)
    p.rect(120, 240, W - 120, 440, PANEL, CIAN, 5)
    p.texto((W / 2, 340), str(d["precio"]), "cartel", 120, AMARILLO)
    versos(p, ["«La máquina no da cambio:", "se paga justo, y con el menor", "número posible de monedas.»"], 540, 46, 23)
    return p.final()


# ------------------------------------------------------------------ 86/87: la clave del arranque
def clave1():
    p = pagina("LA CLAVE DEL ARRANQUE (I)", "escrita por el programador", MAGENTA)
    versos(p, ["«Cuatro bytes, cuatro pruebas:", "", "El primero, el del que deja pasar", "o corta la corriente.", "",
               "El segundo, el de los cuatro", "que se persiguen por los pasillos.»"], 200, 52, 24)
    return p.final()


def clave2():
    p = pagina("LA CLAVE DEL ARRANQUE (II)", "escrita por el programador", MAGENTA)
    versos(p, ["«El tercero, el que se dibuja", "con tandas de casillas.", "", "El cuarto, el del que cruza el tráfico",
               "contando turnos.", "", "Y la clave es lo que sale de aplicar", "la «o exclusiva» a los cuatro."], 190, 46, 23)
    # tabla de la «o exclusiva»
    y = 560
    for k, (a, b, r) in enumerate([(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]):
        p.texto((W / 2, y + k * 44), f"{a} y {b}  da  {r}", "texto", 28, VERDE)
    p.texto((W / 2, 760), "(cifra a cifra, con los números en binario)", "texto2", 18, GRIS)
    return p.final()


def inyectar(carpeta):
    """Mete los datos de las instancias en las apps (bloque /*DATOS*/.../*FIN*/)."""
    datos = {
        "14-circuito.js": {"puertas": I.CIRCUITO["puertas"], "salidas": I.CIRCUITO["salidas"], "solucion": I.CIRCUITO["solucion"], "dato": I.BYTES["14"]},
        "20-atasco.js": {"n": I.ATASCO["n"], "naves": I.ATASCO["naves"], "minimo": I.ATASCO["minimo"]},
        "40-sprite.js": {"pixeles": I.SPRITE_D["pixeles"], "dato": I.BYTES["40"]},
        "48-ascii.js": {"claro": I.ASCII["claro"]},
        "52-fantasmas.js": {"fantasmas": I.FANTASMAS["fantasmas"], "velocidades": I.FANTASMAS["velocidades"], "frutas": I.FANTASMAS["frutas"],
                            "solucion": I.FANTASMAS["solucion"], "dato": I.BYTES["52"]},
        "46-cuadrado.js": {"dados": I.MAGICO["dados"], "solucion": I.MAGICO["solucion"]},
        "51-ranking.js": {"puntos": I.RANKING["puntos"], "limite": I.RANKING["limite"]},
        "64-deslizante.js": {"inicio": I.DESLIZANTE["inicio"], "objetivo": I.DESLIZANTE["objetivo"]},
        "69-rana.js": {"ancho": I.RANA["ancho"], "carriles": I.RANA["carriles"], "inicio": I.RANA["inicio"], "dato": I.BYTES["69"]},
        "72-monedas.js": {"monedas": I.MONEDAS["monedas"], "precio": I.MONEDAS["precio"], "minimo": I.MONEDAS["minimo"], "solucion": I.MONEDAS["solucion"]},
        "85-xor.js": {"bytes": [I.BYTES[k] for k in I.ORDEN], "resultado": I.RESULTADO},
    }
    for app, d in datos.items():
        ruta = os.path.join(carpeta, "minijuegos", app)
        txt = open(ruta, encoding="utf-8").read() if os.path.exists(ruta) else ""
        if "/*DATOS*/" not in txt:
            continue
        a, b = txt.index("/*DATOS*/") + len("/*DATOS*/"), txt.index("/*FIN*/")
        open(ruta, "w", encoding="utf-8", newline="\n").write(txt[:a] + json.dumps(d, ensure_ascii=False) + txt[b:])


def main(carpeta="juegos/aventuras-ca/arcade"):
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    g = lambda k, im: ruido(im, int(k)).save(os.path.join(arte, f"{k}.png"))

    def mosaico(nombre, im, filas, cols, cartas):
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))
        for pieza, k in zip(cortar(im, filas, cols), cartas):
            pieza.save(os.path.join(arte, f"{k}.png"))
    g("16", circuito())
    g("18", acertijo_atasco())
    mosaico("aparcamiento", aparcamiento(), 2, 1, ("19", "21"))
    g("41", tandas(0, 6, "LAS TANDAS DEL SPRITE (I)"))
    g("43", tandas(6, 12, "LAS TANDAS DEL SPRITE (II)"))
    g("45", regla_sprite())
    g("42", bytes_mensaje())
    g("49", tabla_caracteres())
    g("53", regla_bytes())
    n = len(I.FANTASMAS["pistas"])
    g("54", pistas_fantasmas(0, (n + 1) // 2, "LAS PISTAS DE LOS FANTASMAS (I)"))
    g("55", pistas_fantasmas((n + 1) // 2, n, "LAS PISTAS DE LOS FANTASMAS (II)"))
    g("59", plano_pasillos())
    g("37", marcador())
    g("39", regla_marcador())
    g("33", fichas_bolsa())
    g("26", regla_record())
    mosaico("record", tabla_record(), 2, 1, ("61", "63"))
    mosaico("deslizante", dibujo_deslizante(), 2, 1, ("66", "67"))
    g("70", autopista())
    g("71", velocidades())
    g("75", monedas_maquina())
    g("79", precio())
    g("86", clave1())
    g("87", clave2())
    inyectar(carpeta)
    print("láminas de Arcade escritas en", arte)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

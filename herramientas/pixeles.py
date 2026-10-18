"""Pantallas de píxeles de neón para «Game Over, 1985» (el juego de la máquina recreativa).

Igual que mosaicos.py (Pompeya), cada dibujo se genera por código sobre una cuadrícula de celdas y se corta en las piezas que son las
ilustraciones de las cartas; así el código de cada puzle es exacto y se guarda en herramientas/codigos_arcade.json (lo leen los solucionadores).
Novedades respecto a Pompeya: mosaicos de 3 columnas (placa base, marquesina), letras y números con una fuente de píxeles 5x7 y
placas que se entregan BOCA ABAJO (giradas 180°) y hay que darles la vuelta para que encajen.

Uso (desde la raíz del repo):  python herramientas/pixeles.py [carpeta_juego]
Escribe  <juego>/arte/<id>.png (630x882) y <juego>/arte/mosaico-<nombre>.png (el dibujo entero, solo local).
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mosaicos import Lienzo, cortar, flecha  # noqa: E402

CELDA = 14
NEON = {
    "fondo": (9, 10, 34), "fondo2": (14, 16, 52), "rejilla": (26, 40, 92), "cian": (40, 230, 255), "magenta": (255, 52, 200),
    "amarillo": (255, 226, 60), "verde": (70, 255, 130), "naranja": (255, 142, 40), "rojo": (255, 66, 70), "blanco": (240, 240, 255),
    "gris": (96, 100, 140), "oscuro": (4, 4, 18), "cobre": (214, 150, 60), "placa": (10, 62, 52), "placa2": (14, 78, 64),
    "oro": (255, 200, 40), "azul": (60, 110, 255), "morado": (150, 80, 255), "apagado": (46, 48, 82),
}

# fuente 5x7 (mayúsculas y cifras)
FUENTE = {
    "A": "01110 10001 10001 11111 10001 10001 10001", "B": "11110 10001 10001 11110 10001 10001 11110",
    "C": "01110 10001 10000 10000 10000 10001 01110", "D": "11110 10001 10001 10001 10001 10001 11110",
    "E": "11111 10000 10000 11110 10000 10000 11111", "F": "11111 10000 10000 11110 10000 10000 10000",
    "G": "01110 10001 10000 10111 10001 10001 01111", "H": "10001 10001 10001 11111 10001 10001 10001",
    "I": "01110 00100 00100 00100 00100 00100 01110", "J": "00111 00010 00010 00010 00010 10010 01100",
    "K": "10001 10010 10100 11000 10100 10010 10001", "L": "10000 10000 10000 10000 10000 10000 11111",
    "M": "10001 11011 10101 10101 10001 10001 10001", "N": "10001 11001 10101 10011 10001 10001 10001",
    "O": "01110 10001 10001 10001 10001 10001 01110", "P": "11110 10001 10001 11110 10000 10000 10000",
    "Q": "01110 10001 10001 10001 10101 10010 01101", "R": "11110 10001 10001 11110 10100 10010 10001",
    "S": "01111 10000 10000 01110 00001 00001 11110", "T": "11111 00100 00100 00100 00100 00100 00100",
    "U": "10001 10001 10001 10001 10001 10001 01110", "V": "10001 10001 10001 10001 10001 01010 00100",
    "W": "10001 10001 10001 10101 10101 11011 10001", "X": "10001 10001 01010 00100 01010 10001 10001",
    "Y": "10001 10001 01010 00100 00100 00100 00100", "Z": "11111 00001 00010 00100 01000 10000 11111",
    "0": "01110 10001 10011 10101 11001 10001 01110", "1": "00100 01100 00100 00100 00100 00100 01110",
    "2": "01110 10001 00001 00010 00100 01000 11111", "3": "11110 00001 00001 01110 00001 00001 11110",
    "4": "00010 00110 01010 10010 11111 00010 00010", "5": "11111 10000 11110 00001 00001 10001 01110",
    "6": "00110 01000 10000 11110 10001 10001 01110", "7": "11111 00001 00010 00100 01000 01000 01000",
    "8": "01110 10001 10001 01110 10001 10001 01110", "9": "01110 10001 10001 01111 00001 00010 01100",
    " ": "00000 00000 00000 00000 00000 00000 00000",
}


class Pix(Lienzo):
    """Lienzo con aspecto de monitor de recreativa: píxeles planos con un borde de luz y rayas de barrido."""

    def a_imagen(self, semilla=1):
        im = Image.new("RGB", (self.cols * CELDA, self.filas * CELDA), NEON["oscuro"])
        d = ImageDraw.Draw(im)
        for r in range(self.filas):
            for c in range(self.cols):
                k = self.g[r][c] or "fondo"
                base = NEON[k]
                x0, y0 = c * CELDA, r * CELDA
                d.rectangle([x0, y0, x0 + CELDA - 1, y0 + CELDA - 1], fill=base)
                if k not in ("fondo", "fondo2", "rejilla", "oscuro", "placa", "placa2"):
                    claro = tuple(min(255, int(x * 1.18 + 12)) for x in base)
                    oscuro = tuple(int(x * 0.62) for x in base)
                    d.line([(x0, y0), (x0 + CELDA - 1, y0)], fill=claro)
                    d.line([(x0, y0), (x0, y0 + CELDA - 1)], fill=claro)
                    d.line([(x0, y0 + CELDA - 1), (x0 + CELDA - 1, y0 + CELDA - 1)], fill=oscuro)
                    d.line([(x0 + CELDA - 1, y0), (x0 + CELDA - 1, y0 + CELDA - 1)], fill=oscuro)
                # raya de barrido de monitor
                d.rectangle([x0, y0 + CELDA - 3, x0 + CELDA - 1, y0 + CELDA - 1], fill=tuple(int(x * 0.82) for x in base))
        return im


def texto(L, s, x, y, col, esc=1):
    """Escribe `s` con la fuente 5x7 a partir de la celda (x, y); `esc` amplía cada píxel."""
    for i, ch in enumerate(s.upper()):
        filas = FUENTE[ch].split()
        for r, fila in enumerate(filas):
            for c, bit in enumerate(fila):
                if bit == "1":
                    L.rect(x + (i * 6 + c) * esc, y + r * esc, x + (i * 6 + c) * esc + esc - 1, y + r * esc + esc - 1, col)


def ancho_texto(s, esc=1):
    return (len(s) * 6 - 1) * esc


def marco_neon(L, col="cian", grosor=2):
    for g in range(grosor):
        L.rect(g, g, L.cols - 1 - g, g, col)
        L.rect(g, L.filas - 1 - g, L.cols - 1 - g, L.filas - 1 - g, col)
        L.rect(g, g, g, L.filas - 1 - g, col)
        L.rect(L.cols - 1 - g, g, L.cols - 1 - g, L.filas - 1 - g, col)


# ------------------------------------------------------------------ elementos
def componente(L, cx, cy, letra, col_borde="amarillo", lado=13):
    """Componente cuadrado del circuito con una letra dentro."""
    h = lado // 2
    L.rect(cx - h, cy - h, cx + h, cy + h, col_borde)
    L.rect(cx - h + 1, cy - h + 1, cx + h - 1, cy + h - 1, "oscuro")
    texto(L, letra, cx - 2, cy - 3, "blanco")


def pila(L, x, y):
    """Pila: cuerpo rojo con borne dorado y un signo +."""
    L.rect(x, y, x + 14, y + 11, "rojo")
    L.rect(x + 15, y + 3, x + 17, y + 8, "oro")
    L.rect(x + 3, y + 5, x + 9, y + 6, "blanco")
    L.rect(x + 6, y + 2, x + 7, y + 9, "blanco")


def chip(L, cx, cy):
    L.rect(cx - 8, cy - 8, cx + 8, cy + 8, "gris")
    L.rect(cx - 6, cy - 6, cx + 6, cy + 6, "oscuro")
    for k in (-5, -2, 1, 4):
        L.rect(cx - 10, cy + k, cx - 9, cy + k + 1, "oro")
        L.rect(cx + 9, cy + k, cx + 10, cy + k + 1, "oro")
        L.rect(cx + k, cy - 10, cx + k + 1, cy - 9, "oro")
        L.rect(cx + k, cy + 9, cx + k + 1, cy + 10, "oro")
    L.rect(cx - 2, cy - 2, cx + 2, cy + 2, "verde")


def cofre(L, cx, cy):
    L.rect(cx - 5, cy - 3, cx + 5, cy + 4, "naranja")
    L.rect(cx - 5, cy - 3, cx + 5, cy - 1, "oro")
    L.rect(cx - 1, cy, cx + 1, cy + 2, "oscuro")


def boton(L, nombre, cx, cy, s, col):
    """Icono de mando: flechas o botones A / B."""
    if nombre in ("arriba", "abajo", "izquierda", "derecha"):
        flecha(L, nombre, cx, cy, s, col)
    else:
        L.disco(cx, cy, 5.3, col)
        texto(L, nombre.upper(), int(cx - 2), int(cy - 3), "oscuro")


# ------------------------------------------------------------------ puzles
CODIGOS = {
    "placa": {"palabra": "PIXEL"},
    "radar": {"columna": "F", "fila": 4},
    "marquesina": {"botones": ["arriba", "arriba", "abajo", "izquierda", "a", "b"]},
}


def pantalla_placa():
    """Placa base de 3x2 piezas (135x126 celdas): un cable lleva de la pila al chip y los componentes del cable, leídos en orden, forman la palabra."""
    L = Pix(135, 126)
    L.rell("placa")
    for r in range(0, 126, 6):
        for c in range(0, 135, 6):
            L.poner(c, r, "placa2")
    marco_neon(L, "cobre", 2)
    palabra = CODIGOS["placa"]["palabra"]
    cable = "cobre"
    # recorrido principal pila -> chip (ortogonal)
    ruta = [(13, 18), (13, 56), (58, 56), (58, 22), (104, 22), (104, 86), (122, 86), (122, 104)]
    L.trazo(ruta, 3, cable)
    # ramales sin salida (señuelos) con su componente y un extremo abierto
    L.trazo([(58, 56), (58, 100)], 3, cable)
    L.trazo([(13, 56), (13, 104), (40, 104)], 3, cable)
    L.trazo([(104, 86), (104, 112)], 3, cable)
    for (x, y) in [(58, 100), (40, 104), (104, 112)]:
        L.disco(x, y, 3, "apagado")
    # componentes sobre el recorrido, en orden: P I X E L (algunos a caballo entre dos cartas)
    puestos = [(13, 36), (35, 56), (58, 38), (90, 22), (104, 63)]
    for letra, (x, y) in zip(palabra, puestos):
        componente(L, x, y, letra, "amarillo")
    # componentes señuelo en los ramales
    for letra, (x, y) in zip("ARO", [(58, 84), (13, 88), (104, 100)]):
        componente(L, x, y, letra, "magenta")
    pila(L, 5, 4)
    chip(L, 122, 112)
    # unas pistas de soldadura de adorno, lejos del recorrido
    for (x, y) in [(40, 14), (80, 44), (30, 80), (80, 108), (125, 50), (125, 30)]:
        L.rect(x, y, x + 2, y + 2, "oro")
    return L


def pantalla_radar():
    """Radar de 2x2 piezas (90x126): rejilla de 8 columnas (A-H) y 6 filas (1-6) con las etiquetas en el borde; el cofre dorado está en F4."""
    L = Pix(90, 126)
    L.rell("fondo")
    marco_neon(L, "cian", 2)
    x0, y0, w, h = 14, 24, 9, 15
    for i in range(9):
        L.rect(x0 + i * w, y0, x0 + i * w, y0 + 6 * h, "rejilla")
    for j in range(7):
        L.rect(x0, y0 + j * h, x0 + 8 * w, y0 + j * h, "rejilla")
    for i, letra in enumerate("ABCDEFGH"):
        texto(L, letra, x0 + i * w + 2, 15, "cian")
    for j in range(6):
        texto(L, str(j + 1), 6, y0 + j * h + 4, "cian")
    # anillos de radar centrados en el cofre y barrido
    col_c, fila_c = CODIGOS["radar"]["columna"], CODIGOS["radar"]["fila"]
    cx = x0 + ("ABCDEFGH".index(col_c)) * w + w // 2
    cy = y0 + (fila_c - 1) * h + h // 2
    # señales falsas (rojas) en otras casillas
    for (c, f) in [("C", 2), ("E", 5), ("H", 3), ("B", 6), ("D", 1)]:
        sx = x0 + "ABCDEFGH".index(c) * w + w // 2
        sy = y0 + (f - 1) * h + h // 2
        L.rect(sx - 1, sy - 1, sx + 1, sy + 1, "rojo")
    cofre(L, cx, cy)
    L.anillo(cx, cy, 8, 8.5, "amarillo")
    texto(L, "RADAR", 33, 6, "verde")
    texto(L, "OK", 38, 117, "verde")
    return L


def pantalla_marquesina():
    """Marquesina de 3x1 piezas (135x63): nueve botones, seis encendidos (con LED) y tres apagados; se leen los encendidos, de izquierda a derecha."""
    L = Pix(135, 63)
    L.rell("fondo")
    marco_neon(L, "magenta", 2)
    for i in range(3, 132, 4):
        L.rect(i, 5, i + 1, 6, "amarillo" if (i // 4) % 2 == 0 else "rojo")
        L.rect(i, 56, i + 1, 57, "rojo" if (i // 4) % 2 == 0 else "amarillo")
    texto(L, "INSERT COIN", 33, 10, "amarillo")
    sec = CODIGOS["marquesina"]["botones"]
    encendidos = [0, 2, 3, 5, 7, 8]
    señuelos = {1: "b", 4: "izquierda", 6: "a"}
    it = iter(sec)
    for k in range(9):
        x = 12 + 13 * k
        if k in encendidos:
            nombre, col, led = next(it), "blanco", "amarillo"
            L.rect(x - 1, 27, x + 10, 40, "cian")
        else:
            nombre, col, led = señuelos[k], "apagado", "apagado"
            L.rect(x - 1, 27, x + 10, 40, "rejilla")
        L.rect(x, 28, x + 9, 39, "oscuro")
        boton(L, nombre, x + 4.5, 33.5, 4.2, col)
        L.rect(x + 3, 22, x + 6, 24, led)
    texto(L, "HI-SCORE 019850".replace("-", " "), 21, 46, "magenta")
    return L


def _instancias():
    return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_arcade.json"), encoding="utf-8"))


def triangulo_lado(L, x, y, h, derecha, col):
    """Punta de flecha de h celdas de alto apuntando a la derecha o a la izquierda."""
    mitad = h // 2
    for k in range(h):
        d = abs(k - mitad)
        ancho = mitad - d + 1
        if derecha:
            L.rect(x, y + k, x + ancho - 1, y + k, col)
        else:
            L.rect(x + mitad - ancho + 1, y + k, x + mitad, y + k, col)


def carta_trafico():
    """Carta 52 (una sola carta, 45x63): sentido y velocidad de cada carril de la autopista (una flecha = 1 casilla por turno, dos = 2)."""
    L = Pix(45, 63)
    L.rell("fondo")
    marco_neon(L, "amarillo", 1)
    ins = _instancias()["autopista"]
    texto(L, "META", 11, 4, "verde", 1)
    for k, car in enumerate(ins["carriles"]):
        y = 13 + k * 10
        L.rect(3, y - 1, 41, y + 7, "fondo2")
        L.rect(3, y - 1, 41, y - 1, "rejilla")
        L.rect(3, y + 7, 41, y + 7, "rejilla")
        texto(L, str(k + 1), 5, y, "cian", 1)
        for j in range(car["vel"]):
            x = 17 + j * 9
            triangulo_lado(L, x, y, 7, car["dir"] > 0, "amarillo")
    texto(L, "SALIDA", 5, 53, "magenta", 1)
    return L


COLOR_PIEZA = {"I": "cian", "O": "amarillo", "T": "morado", "S": "verde", "Z": "rojo", "J": "azul", "L": "naranja"}
BASE_PIEZAS = {"I": [(0, 0), (0, 1), (0, 2), (0, 3)], "O": [(0, 0), (0, 1), (1, 0), (1, 1)], "T": [(0, 0), (0, 1), (0, 2), (1, 1)],
               "S": [(0, 1), (0, 2), (1, 0), (1, 1)], "Z": [(0, 0), (0, 1), (1, 1), (1, 2)], "J": [(0, 0), (1, 0), (1, 1), (1, 2)],
               "L": [(0, 2), (1, 0), (1, 1), (1, 2)]}


def carta_piezas():
    """Carta 70 (una sola carta, 45x63): las piezas que hay que usar para llenar el pozo y cuántas de cada una."""
    L = Pix(45, 63)
    L.rell("fondo")
    marco_neon(L, "morado", 1)
    texto(L, "PIEZAS", 7, 4, "blanco", 1)
    for k, (tipo, n) in enumerate(sorted(_instancias()["pozo"]["piezas"].items())):
        y = 16 + k * 11
        for (r, c) in BASE_PIEZAS[tipo]:
            L.rect(5 + c * 3, y + r * 3, 5 + c * 3 + 2, y + r * 3 + 2, COLOR_PIEZA[tipo])
        texto(L, tipo, 24, y + 1, "blanco", 1)
        texto(L, "X" + str(n), 32, y + 1, "amarillo", 1)
    return L


SUELTAS = {"52": carta_trafico, "70": carta_piezas}

# nombre -> (función, [ids de las piezas en orden de lectura: izq→dcha, arriba→abajo], filas, cols, {id: giro en grados con que se entrega la pieza})
MOSAICOS = {
    "placa": (pantalla_placa, ["17", "14", "19", "16", "15", "18"], 2, 3, {"14": 180, "16": 180, "18": 180}),
    "radar": (pantalla_radar, ["32", "30", "33", "31"], 2, 2, {}),
    "marquesina": (pantalla_marquesina, ["41", "42", "40"], 1, 3, {}),
}


def main(carpeta="juegos/aventuras-ca/arcade"):
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    for nombre, (fn, ids, filas, cols, giros) in MOSAICOS.items():
        im = fn().a_imagen()
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))
        for pieza, i in zip(cortar(im, filas, cols), ids):
            if i in giros:
                pieza = pieza.rotate(-giros[i])   # entregada boca abajo: hay que girarla para que encaje
            pieza.save(os.path.join(arte, f"{i}.png"))
        print(f"{nombre}: {len(ids)} piezas {', '.join(ids)}")
    for i, fn in SUELTAS.items():
        fn().a_imagen().save(os.path.join(arte, f"{i}.png"))
        print(f"carta suelta {i}")
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "codigos_arcade.json")
    json.dump(CODIGOS, open(ruta, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print("códigos en", ruta)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

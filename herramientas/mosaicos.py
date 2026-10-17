"""Mosaicos romanos para los juegos en los que varias cartas se juntan para formar una figura (Pompeya).

Cada mosaico se dibuja con teselas (cuadraditos de color con junta) sobre una cuadrícula de celdas y se corta en las piezas que serán
las ilustraciones de las cartas: 2x2 = 4 cartas (las proporciones de la carta se conservan) o 1x2 = 2 cartas apiladas.
El dibujo contiene el CÓDIGO de un puzle (formas en un camino, flechas de estatuas, pétalos de rosetas, dígitos partidos, sombra de un
reloj de sol). Como se genera por código, la respuesta es exacta y se guarda en herramientas/codigos_pompeya.json (la leen los solucionadores).

Uso (desde la raíz del repo):  python herramientas/mosaicos.py [carpeta_juego]
Escribe  <juego>/arte/<id>.png  (630x882, cada pieza)  y  <juego>/arte/mosaico-<nombre>.png (el dibujo entero, solo local),
y luego conviene ejecutar  python herramientas/preparar_imagenes.py <juego>  para crear los img/<id>.jpg.
"""
import json
import math
import os
import random
import sys

from PIL import Image, ImageDraw

CELDA = 14
COLS, FILAS = 90, 126            # 2x2 piezas de 45x63 celdas = 630x882 px cada una
PALETA = {
    "azul": (30, 74, 112), "azul2": (22, 56, 88), "crema": (238, 224, 190), "marfil": (247, 241, 226), "ocre": (214, 160, 66),
    "oro": (236, 190, 70), "terracota": (176, 84, 58), "rojo": (150, 44, 38), "verde": (84, 124, 70), "verde2": (58, 96, 54),
    "negro": (30, 28, 28), "marron": (96, 66, 44), "gris": (140, 136, 128), "cian": (70, 150, 160),
}
JUNTA = (46, 40, 34)


class Lienzo:
    def __init__(self, cols=COLS, filas=FILAS):
        self.cols, self.filas = cols, filas
        self.g = [[None] * cols for _ in range(filas)]

    def poner(self, c, r, col):
        if 0 <= c < self.cols and 0 <= r < self.filas:
            self.g[r][c] = col

    def rell(self, col):
        for r in range(self.filas):
            for c in range(self.cols):
                self.g[r][c] = col

    def rect(self, c0, r0, c1, r1, col):
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                self.poner(c, r, col)

    def disco(self, cx, cy, rad, col):
        for r in range(int(cy - rad) - 1, int(cy + rad) + 2):
            for c in range(int(cx - rad) - 1, int(cx + rad) + 2):
                if (c - cx) ** 2 + (r - cy) ** 2 <= rad * rad:
                    self.poner(c, r, col)

    def anillo(self, cx, cy, r0, r1, col):
        for r in range(int(cy - r1) - 1, int(cy + r1) + 2):
            for c in range(int(cx - r1) - 1, int(cx + r1) + 2):
                d = (c - cx) ** 2 + (r - cy) ** 2
                if r0 * r0 <= d <= r1 * r1:
                    self.poner(c, r, col)

    def poligono(self, pts, col):
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        for r in range(int(min(ys)) - 1, int(max(ys)) + 2):
            for c in range(int(min(xs)) - 1, int(max(xs)) + 2):
                if dentro(c + 0.5, r + 0.5, pts):
                    self.poner(c, r, col)

    def trazo(self, puntos, ancho, col):
        """Línea quebrada de segmentos horizontales/verticales con `ancho` celdas."""
        h = ancho // 2
        for (x0, y0), (x1, y1) in zip(puntos, puntos[1:]):
            self.rect(min(x0, x1) - h, min(y0, y1) - h, max(x0, x1) + h - (1 if ancho % 2 == 0 else 0), max(y0, y1) + h - (1 if ancho % 2 == 0 else 0), col)

    # ---- imagen
    def a_imagen(self, semilla=1):
        rng = random.Random(semilla)
        im = Image.new("RGB", (self.cols * CELDA, self.filas * CELDA), JUNTA)
        d = ImageDraw.Draw(im)
        for r in range(self.filas):
            for c in range(self.cols):
                k = self.g[r][c]
                base = PALETA[k] if k else PALETA["azul2"]
                v = rng.randint(-10, 10)
                col = tuple(max(0, min(255, x + v)) for x in base)
                x0, y0 = c * CELDA, r * CELDA
                d.rectangle([x0 + 1, y0 + 1, x0 + CELDA - 2, y0 + CELDA - 2], fill=col)
                claro = tuple(min(255, x + 22) for x in col)
                d.line([(x0 + 1, y0 + 1), (x0 + CELDA - 2, y0 + 1)], fill=claro)
                d.line([(x0 + 1, y0 + 1), (x0 + 1, y0 + CELDA - 2)], fill=claro)
        return im


def dentro(x, y, pts):
    ok = False
    j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi:
            ok = not ok
        j = i
    return ok


# ------------------------------------------------------------------ elementos
def marco(L, ancho=5):
    c1, r1 = L.cols - 1, L.filas - 1
    L.rect(0, 0, c1, r1, "azul")
    # tira de ajedrez terracota/crema y filetes
    for r in range(L.filas):
        for c in range(L.cols):
            dist = min(c, r, c1 - c, r1 - r)
            if dist < ancho:
                L.poner(c, r, "azul2" if dist in (0, ancho - 1) else ("terracota" if (c + r) % 2 == 0 else "crema"))
            elif dist == ancho:
                L.poner(c, r, "oro")


def fondo_teselado(L, c0, r0, c1, r1, a="azul", b="azul2"):
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            L.poner(c, r, a if (c // 3 + r // 3) % 2 == 0 else b)


def forma(L, nombre, cx, cy, s, col):
    if nombre == "circulo":
        L.disco(cx, cy, s, col)
    elif nombre == "cuadrado":
        L.rect(int(cx - s * 0.85), int(cy - s * 0.85), int(cx + s * 0.85), int(cy + s * 0.85), col)
    elif nombre == "triangulo":
        L.poligono([(cx, cy - s), (cx + s * 1.05, cy + s * 0.8), (cx - s * 1.05, cy + s * 0.8)], col)
    elif nombre == "rombo":
        L.poligono([(cx, cy - s * 1.1), (cx + s * 0.85, cy), (cx, cy + s * 1.1), (cx - s * 0.85, cy)], col)
    elif nombre == "estrella":
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rad = s * (1.15 if i % 2 == 0 else 0.5)
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        L.poligono(pts, col)
    elif nombre == "cruz":
        a = s * 0.38
        L.rect(int(cx - a), int(cy - s), int(cx + a), int(cy + s), col)
        L.rect(int(cx - s), int(cy - a), int(cx + s), int(cy + a), col)
    else:
        raise ValueError(nombre)


def flecha(L, direccion, cx, cy, s, col):
    """Flecha gorda hacia arriba/abajo/izquierda/derecha."""
    base = [(-0.35, 0.9), (-0.35, -0.05), (-0.8, -0.05), (0, -0.95), (0.8, -0.05), (0.35, -0.05), (0.35, 0.9)]  # hacia arriba
    giro = {"arriba": 0, "derecha": 90, "abajo": 180, "izquierda": 270}[direccion]
    a = math.radians(giro)
    pts = [(cx + s * (x * math.cos(a) - y * math.sin(a)), cy + s * (x * math.sin(a) + y * math.cos(a))) for x, y in base]
    L.poligono(pts, col)


def estatua(L, cx, cy, h, cuerpo, antorcha=False):
    """Figura en hornacina: cabeza, torso en trapecio y plinto. Con antorcha (llama dorada) la figura de partida."""
    L.rect(int(cx - h * 0.5), int(cy - h * 0.62), int(cx + h * 0.5), int(cy + h * 0.62), "oro")          # marco de la hornacina
    L.rect(int(cx - h * 0.46), int(cy - h * 0.58), int(cx + h * 0.46), int(cy + h * 0.58), "azul2")
    L.disco(cx, cy - h * 0.34, h * 0.13, cuerpo)
    L.poligono([(cx - h * 0.12, cy - h * 0.2), (cx + h * 0.12, cy - h * 0.2), (cx + h * 0.3, cy + h * 0.38), (cx - h * 0.3, cy + h * 0.38)], cuerpo)
    L.rect(int(cx - h * 0.36), int(cy + h * 0.38), int(cx + h * 0.36), int(cy + h * 0.5), "gris")
    if antorcha:
        L.rect(int(cx + h * 0.28), int(cy - h * 0.36), int(cx + h * 0.33), int(cy - h * 0.05), "marron")
        L.poligono([(cx + h * 0.305, cy - h * 0.62), (cx + h * 0.42, cy - h * 0.34), (cx + h * 0.19, cy - h * 0.34)], "oro")
        L.poligono([(cx + h * 0.305, cy - h * 0.5), (cx + h * 0.36, cy - h * 0.36), (cx + h * 0.25, cy - h * 0.36)], "rojo")


def roseta(L, cx, cy, rad, petalos, col1, col2):
    for k in range(petalos):
        ang = -math.pi / 2 + k * 2 * math.pi / petalos
        ux, uy = math.cos(ang), math.sin(ang)
        px, py = -uy, ux
        ancho = rad * min(0.26, 0.9 * math.pi / max(petalos, 3) / 2.2)
        pts = []
        for t in range(0, 11):
            f = t / 10
            w = ancho * math.sin(math.pi * f) ** 0.8
            pts.append((cx + ux * rad * (0.24 + 0.76 * f) + px * w, cy + uy * rad * (0.24 + 0.76 * f) + py * w))
        for t in range(10, -1, -1):
            f = t / 10
            w = ancho * math.sin(math.pi * f) ** 0.8
            pts.append((cx + ux * rad * (0.24 + 0.76 * f) - px * w, cy + uy * rad * (0.24 + 0.76 * f) - py * w))
        L.poligono(pts, col1 if k % 2 == 0 else col2)
    L.disco(cx, cy, rad * 0.24, "oro")
    L.disco(cx, cy, rad * 0.11, "rojo")


SEGMENTOS = {0: "abcdef", 1: "bc", 2: "abdeg", 3: "abcdg", 4: "bcfg", 5: "acdfg", 6: "acdefg", 7: "abc", 8: "abcdefg", 9: "abcdfg"}


def digito(L, d, x0, y0, ancho, alto, grosor, col):
    """Dígito de siete segmentos en la caja (x0,y0)-(x0+ancho-1, y0+alto-1). El segmento central cae en la mitad exacta de la caja."""
    mid = y0 + alto // 2 - grosor // 2
    seg = {
        "a": (x0, y0, x0 + ancho - 1, y0 + grosor - 1), "d": (x0, y0 + alto - grosor, x0 + ancho - 1, y0 + alto - 1),
        "g": (x0, mid, x0 + ancho - 1, mid + grosor - 1),
        "f": (x0, y0, x0 + grosor - 1, y0 + alto // 2 + grosor // 2 - 1), "b": (x0 + ancho - grosor, y0, x0 + ancho - 1, y0 + alto // 2 + grosor // 2 - 1),
        "e": (x0, mid, x0 + grosor - 1, y0 + alto - 1), "c": (x0 + ancho - grosor, mid, x0 + ancho - 1, y0 + alto - 1),
    }
    for s in SEGMENTOS[d]:
        L.rect(*seg[s], col)


# ------------------------------------------------------------------ los mosaicos
CODIGOS = {
    "atrio": {"formas": ["triangulo", "estrella", "circulo", "cruz"]},
    "peristilo": {"flechas": ["abajo", "abajo", "derecha", "arriba"]},
    "rosetas": {"petalos": [5, 3, 7]},
    "digitos": {"digitos": [4, 7, 2]},
    "reloj": {"marca": 7},
}


def mosaico_atrio():
    L = Lienzo()
    marco(L)
    fondo_teselado(L, 6, 6, L.cols - 7, L.filas - 7, "azul", "azul2")
    nodos = [(14, 14), (66, 14), (66, 42), (24, 42), (24, 70), (70, 70), (70, 98), (20, 98), (20, 112)]
    L.trazo(nodos, 4, "crema")
    emblemas = [("triangulo", (66, 42), "terracota"), ("estrella", (24, 42), "ocre"), ("circulo", (70, 70), "verde"), ("cruz", (20, 98), "rojo")]
    señuelos = [("rombo", (45, 30), "cian"), ("cuadrado", (44, 84), "ocre")]
    for nombre, (x, y), col in emblemas + señuelos:
        L.disco(x, y, 10, "crema")
        L.anillo(x, y, 10, 11, "oro")
        forma(L, nombre, x, y, 6.5, col)
    forma(L, "estrella", 14, 14, 7, "oro")
    L.anillo(14, 14, 8, 9, "oro")
    L.disco(20, 112, 3, "oro")
    return L


def mosaico_peristilo():
    L = Lienzo()
    marco(L)
    fondo_teselado(L, 6, 6, L.cols - 7, L.filas - 7, "verde2", "verde")
    L.rect(14, 20, 75, 105, "crema")
    L.rect(16, 22, 73, 103, "verde2")
    estatuas = [((66, 28), "abajo", True), ((66, 98), "abajo", False), ((24, 98), "derecha", False), ((24, 28), "arriba", False)]  # sentido del reloj desde la antorcha
    for (x, y), dir_, antorcha in estatuas:
        estatua(L, x, y, 24, "marfil", antorcha)
        L.disco(x, y + 22 if y < 63 else y - 22, 8, "crema")
        flecha(L, dir_, x, y + 22 if y < 63 else y - 22, 6.5, "terracota")
    # fuente central (cruza las cuatro piezas)
    L.disco(45, 63, 12, "gris")
    L.disco(45, 63, 10, "cian")
    L.disco(45, 63, 3, "marfil")
    return L


def mosaico_rosetas():
    L = Lienzo()
    marco(L)
    for r in range(6, L.filas - 6):
        for c in range(6, L.cols - 6):
            L.poner(c, r, "crema" if (c + r) % 14 in (0, 1) or (c - r) % 14 in (0, 1) else "marfil")
    centros = [((45, 32), 20, 5, "terracota", "ocre"), ((22, 92), 16, 3, "azul", "cian"), ((68, 92), 16, 7, "verde", "rojo")]
    for (cx, cy), rad, n, c1, c2 in centros:
        L.disco(cx, cy, rad + 3, "negro")
        L.disco(cx, cy, rad + 2, "marfil")
        roseta(L, cx, cy, rad, n, c1, c2)
    return L


def mosaico_reloj():
    L = Lienzo()
    marco(L)
    fondo_teselado(L, 6, 6, L.cols - 7, L.filas - 7, "ocre", "crema")
    cx, cy = 45, 63
    L.disco(cx, cy, 36, "negro")
    L.disco(cx, cy, 35, "marfil")
    L.anillo(cx, cy, 31, 32, "oro")
    n = CODIGOS["reloj"]["marca"]
    for k in range(12):
        ang = -math.pi / 2 + k * math.pi / 6
        x, y = cx + 26 * math.cos(ang), cy + 26 * math.sin(ang)
        if k == 0:
            forma(L, "estrella", x, y, 6, "oro")
        else:
            L.disco(x, y, 2.6, "azul")
    # sombra del gnomon hacia la marca n (contando en el sentido del reloj desde la estrella)
    ang = -math.pi / 2 + n * math.pi / 6
    ux, uy = math.cos(ang), math.sin(ang)
    px, py = -uy, ux
    L.poligono([(cx + px * 3, cy + py * 3), (cx - px * 3, cy - py * 3), (cx + ux * 22 - px * 1.2, cy + uy * 22 - py * 1.2), (cx + ux * 22 + px * 1.2, cy + uy * 22 + py * 1.2)], "negro")
    L.disco(cx, cy, 5, "oro")
    L.disco(cx, cy, 2, "rojo")
    return L


def mosaico_digitos():
    L = Lienzo(cols=45, filas=126)
    marco(L)
    fondo_teselado(L, 6, 6, L.cols - 7, L.filas - 7, "azul", "azul2")
    digs = CODIGOS["digitos"]["digitos"]
    ancho, alto, gro = 7, 28, 3
    sep = 3
    total = len(digs) * ancho + (len(digs) - 1) * sep
    x0 = (L.cols - total) // 2
    for i, d in enumerate(digs):
        digito(L, d, x0 + i * (ancho + sep), 49, ancho, alto, gro, "ocre")
    return L


# nombre -> (función, [ids de las piezas en orden de lectura: izq→dcha, arriba→abajo], filas, cols)
MOSAICOS = {
    # los números de las placas no siguen el orden de lectura (así el número no delata el sitio); deben coincidir con MOSAICOS de datos_pompeya.py
    "atrio": (mosaico_atrio, ["16", "14", "17", "15"], 2, 2),
    "peristilo": (mosaico_peristilo, ["32", "30", "33", "31"], 2, 2),
    "rosetas": (mosaico_rosetas, ["42", "40", "43", "41"], 2, 2),
    "digitos": (mosaico_digitos, ["53", "52"], 2, 1),
    "reloj": (mosaico_reloj, ["65", "67", "64", "66"], 2, 2),
}


def cortar(im, filas, cols):
    w, h = im.size
    pw, ph = w // cols, h // filas
    return [im.crop((c * pw, f * ph, (c + 1) * pw, (f + 1) * ph)) for f in range(filas) for c in range(cols)]


def main(carpeta="juegos/aventuras-ca/pompeya"):
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    for nombre, (fn, ids, filas, cols) in MOSAICOS.items():
        im = fn().a_imagen(semilla=sum(map(ord, nombre)))
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))
        for pieza, i in zip(cortar(im, filas, cols), ids):
            pieza.save(os.path.join(arte, f"{i}.png"))
        print(f"{nombre}: {len(ids)} piezas {', '.join(ids)}")
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "codigos_pompeya.json")
    json.dump(CODIGOS, open(ruta, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print("códigos en", ruta)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

"""Láminas de «El Cuarto de Leo, 1995» (juguetes): todo se dibuja por código a partir de herramientas/instancias_juguetes.json.

  - carta 20: la foto Polaroid de la estantería (antes); la estantería de ahora es la imagen img/ui/estanteria.png del minijuego 24.
  - cartas 30 y 31: la torre de bloques vista de frente y desde la derecha, y desde arriba.
  - carta 52: los hilos enredados de la marioneta, de los cuatro mandos a los cuatro miembros; carta 53: el cartel con la postura.
  - cartas 41, 43, 45, 49 y 51: las páginas del FOLIOSCOPIO (el cuaderno de Leo); se ordenan por el sol que se pone en la ventana.
  - carta 70: las instrucciones de la pista de canicas con balancines.
  - imágenes de los minijuegos (img/ui): estantería, marioneta en sus 16 posturas, juguetes del tren y pista de canicas.
Además copia en cada minijuego (entre /*DATOS*/ y /*FIN*/) los datos de su instancia.
Uso (desde la raíz del repo):  python herramientas/juguetes.py [carpeta_juego]
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

W, H = 630, 882
PAPEL = (250, 244, 226)
TINTA = (48, 40, 60)
ROJO = (214, 52, 48)
AZUL = (44, 104, 196)
AMARILLO = (246, 196, 42)
VERDE = (58, 160, 84)
NARANJA = (238, 128, 40)
MORADO = (130, 76, 170)
MADERA = (196, 140, 86)
MADERA2 = (140, 92, 52)
BLANCO = (252, 250, 244)
NEGRO = (30, 26, 34)
CIELO = (120, 186, 236)
GRIS = (150, 150, 160)
COLOR_MANDO = {"rojo": ROJO, "azul": AZUL, "amarillo": AMARILLO, "verde": VERDE}
FORMA_MANDO = {"rojo": "circulo", "azul": "cuadrado", "amarillo": "triangulo", "verde": "estrella"}
NOMBRE_JUGUETE = {"patito": "patito", "pelota": "pelota", "tambor": "tambor", "cohete": "cohete", "cometa": "cometa"}


def _inst():
    return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_juguetes.json"), encoding="utf-8"))


def ruido(im, semilla, fuerza=2.5):
    a = np.asarray(im).astype(np.int16)
    rng = np.random.default_rng(semilla)
    a = a + rng.normal(0, fuerza, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def estrella(h, cx, cy, r, col, borde=NEGRO):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rad = r * (1 if i % 2 == 0 else 0.45)
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    h.poli(pts, col, borde, 2)


def forma(h, nombre, cx, cy, r, col):
    if nombre == "circulo":
        h.disco(cx, cy, r, col, NEGRO, 2)
    elif nombre == "cuadrado":
        h.rect(cx - r * 0.85, cy - r * 0.85, cx + r * 0.85, cy + r * 0.85, col, NEGRO, 2)
    elif nombre == "triangulo":
        h.poli([(cx, cy - r), (cx + r, cy + r * 0.8), (cx - r, cy + r * 0.8)], col, NEGRO, 2)
    else:
        estrella(h, cx, cy, r * 1.1, col)


# ================================================================== juguetes (base 0 = el suelo/balda donde se apoyan)
def juguete(h, nombre, cx, base, k=1.0, color=None, boca_abajo=False):
    s = k
    if nombre == "patito":
        h.elip(cx - 30 * s, base - 34 * s, cx + 26 * s, base, AMARILLO, NEGRO, 2)
        h.disco(cx + 16 * s, base - 44 * s, 15 * s, AMARILLO, NEGRO, 2)
        h.poli([(cx + 28 * s, base - 46 * s), (cx + 42 * s, base - 42 * s), (cx + 28 * s, base - 38 * s)], NARANJA, NEGRO, 1.5)
        h.disco(cx + 20 * s, base - 48 * s, 2.5 * s, NEGRO)
    elif nombre == "tambor":
        h.rect(cx - 30 * s, base - 46 * s, cx + 30 * s, base - 6 * s, ROJO, NEGRO, 2)
        h.elip(cx - 30 * s, base - 54 * s, cx + 30 * s, base - 38 * s, BLANCO, NEGRO, 2)
        for i in range(4):
            x = cx - 30 * s + i * 20 * s
            h.linea([(x, base - 44 * s), (x + 20 * s, base - 10 * s)], AMARILLO, 2.5 * s)
        h.elip(cx - 30 * s, base - 12 * s, cx + 30 * s, base, ROJO, NEGRO, 2)
    elif nombre == "cohete":
        def P(x, y):
            return (cx + x * s, base - 70 * s + (70 - y) * s) if boca_abajo else (cx + x * s, base - y * s)
        h.poli([P(-14, 10), P(14, 10), P(14, 52), P(0, 72), P(-14, 52)], BLANCO, NEGRO, 2)
        h.poli([P(-14, 10), P(-26, 0), P(-14, 30)], ROJO, NEGRO, 2)
        h.poli([P(14, 10), P(26, 0), P(14, 30)], ROJO, NEGRO, 2)
        cxv, cyv = P(0, 40)
        h.disco(cxv, cyv, 7 * s, CIELO, NEGRO, 2)
    elif nombre == "libro":
        h.rect(cx - 14 * s, base - 60 * s, cx + 14 * s, base, MORADO, NEGRO, 2)
        h.rect(cx - 10 * s, base - 50 * s, cx + 10 * s, base - 44 * s, AMARILLO)
    elif nombre == "pelota":
        c = color or ROJO
        h.disco(cx, base - 24 * s, 24 * s, c, NEGRO, 2)
        h.linea([(cx - 24 * s, base - 24 * s), (cx + 24 * s, base - 24 * s)], BLANCO, 4 * s)
        h.disco(cx - 8 * s, base - 34 * s, 5 * s, BLANCO)
    elif nombre == "coche":
        h.rect(cx - 34 * s, base - 26 * s, cx + 34 * s, base - 8 * s, AZUL, NEGRO, 2)
        h.poli([(cx - 18 * s, base - 26 * s), (cx - 10 * s, base - 40 * s), (cx + 14 * s, base - 40 * s), (cx + 22 * s, base - 26 * s)], AZUL, NEGRO, 2)
        h.rect(cx - 6 * s, base - 37 * s, cx + 10 * s, base - 28 * s, CIELO)
        for x in (-20, 20):
            h.disco(cx + x * s, base - 8 * s, 8 * s, NEGRO)
    elif nombre == "osito":
        h.disco(cx, base - 22 * s, 20 * s, MADERA, NEGRO, 2)
        h.disco(cx, base - 52 * s, 15 * s, MADERA, NEGRO, 2)
        for x in (-11, 11):
            h.disco(cx + x * s, base - 64 * s, 6 * s, MADERA, NEGRO, 2)
        h.disco(cx, base - 48 * s, 5 * s, (230, 200, 160))
        for x in (-5, 5):
            h.disco(cx + x * s, base - 55 * s, 2.2 * s, NEGRO)
    elif nombre == "barco":
        h.poli([(cx - 32 * s, base - 18 * s), (cx + 32 * s, base - 18 * s), (cx + 22 * s, base), (cx - 22 * s, base)], ROJO, NEGRO, 2)
        h.linea([(cx, base - 18 * s), (cx, base - 66 * s)], NEGRO, 2.5)
        h.poli([(cx + 2 * s, base - 64 * s), (cx + 26 * s, base - 24 * s), (cx + 2 * s, base - 24 * s)], BLANCO, NEGRO, 2)
    elif nombre == "cubos":
        for (x, y, c, l) in ((-22, 0, AZUL, "A"), (2, 0, VERDE, "B"), (-10, -24, AMARILLO, "C")):
            h.rect(cx + x * s, base - 24 * s + y * s, cx + (x + 24) * s, base + y * s, c, NEGRO, 2)
            h.texto((cx + (x + 12) * s, base - 12 * s + y * s), l, "cartel", int(16 * s), BLANCO)
    elif nombre == "cometa":
        h.poli([(cx, base - 76 * s), (cx + 22 * s, base - 46 * s), (cx, base - 14 * s), (cx - 22 * s, base - 46 * s)], NARANJA, NEGRO, 2)
        h.linea([(cx, base - 76 * s), (cx, base - 14 * s)], NEGRO, 1.5)
        h.linea([(cx - 22 * s, base - 46 * s), (cx + 22 * s, base - 46 * s)], NEGRO, 1.5)
        h.linea([(cx, base - 14 * s), (cx + 8 * s, base - 6 * s), (cx - 4 * s, base)], ROJO, 2)
    elif nombre == "trompo":
        h.poli([(cx - 24 * s, base - 40 * s), (cx + 24 * s, base - 40 * s), (cx, base)], VERDE, NEGRO, 2)
        h.elip(cx - 24 * s, base - 48 * s, cx + 24 * s, base - 34 * s, AMARILLO, NEGRO, 2)
        h.rect(cx - 3 * s, base - 60 * s, cx + 3 * s, base - 46 * s, MADERA2)
    elif nombre == "xilofono":
        for i, c in enumerate((ROJO, NARANJA, AMARILLO, VERDE, AZUL)):
            x = cx - 36 * s + i * 15 * s
            h.rect(x, base - 14 * s - (5 - i) * 6 * s, x + 12 * s, base - 4 * s, c, NEGRO, 1.5)
        h.rect(cx - 40 * s, base - 6 * s, cx + 40 * s, base, MADERA2)
    elif nombre == "dado":
        h.rect(cx - 22 * s, base - 44 * s, cx + 22 * s, base, BLANCO, NEGRO, 2)
        for (x, y) in ((-11, -33), (0, -22), (11, -11)):
            h.disco(cx + x * s, base + y * s, 4 * s, NEGRO)
    else:
        raise ValueError(nombre)


# ================================================================== estantería (antes en la Polaroid, ahora en la app)
def dibujar_estanteria(h, x0, y0, ancho, inst, despues):
    e = inst["estanteria"]
    alto_balda = 120
    k = ancho / 600
    h.rect(x0, y0, x0 + ancho, y0 + alto_balda * 3 * k + 14 * k, (230, 216, 190))
    baldas = {b: [list(t) for t in lista] for b, lista in e["antes"].items()}
    color_pelota = None
    girado = False
    if despues:
        for c in e["cambios"]:
            if c["tipo"] == "color":
                color_pelota = AZUL
            elif c["tipo"] == "falta":
                for b in baldas.values():
                    b[:] = [t for t in b if t[0] != c["juguete"]]
            elif c["tipo"] == "girado":
                girado = True
            elif c["tipo"] == "sobra":
                baldas[c["balda"]].append([c["juguete"], c["x"]])
            elif c["tipo"] == "movido":
                for b in baldas.values():
                    b[:] = [t for t in b if t[0] != c["juguete"]]
                baldas[c["a_balda"]].append([c["juguete"], c["x"]])
    for b in ("0", "1", "2"):
        base = y0 + (int(b) + 1) * alto_balda * k
        for nombre, x in baldas[b]:
            juguete(h, nombre, x0 + x * k, base - 2 * k, 1.1 * k, color=color_pelota if nombre == "pelota" else None,
                    boca_abajo=girado and nombre == "cohete")
        h.rect(x0, base, x0 + ancho, base + 14 * k, MADERA, MADERA2, 2)
    h.rect(x0 - 10 * k, y0 - 6 * k, x0, y0 + alto_balda * 3 * k + 14 * k, MADERA2)
    h.rect(x0 + ancho, y0 - 6 * k, x0 + ancho + 10 * k, y0 + alto_balda * 3 * k + 14 * k, MADERA2)


def zonas_diferencias(inst):
    """Rectángulos (en % de la imagen de la estantería de ahora, 620 x 400) de las cinco diferencias, para el minijuego: una lista por
    diferencia (el juguete que cambia de balda vale tocándolo en su sitio nuevo o en el hueco que ha dejado)."""
    e = inst["estanteria"]
    W2, H2, x0, y0, k = 620, 400, 10, 12, 1.0
    zonas = []

    def caja(x, balda, alto=80):
        base = y0 + (int(balda) + 1) * 120 * k
        return [round((x0 + (x - 46) * k) / W2 * 100, 2), round((base - alto * k) / H2 * 100, 2), round(92 * k / W2 * 100, 2), round(alto * k / H2 * 100, 2)]
    pos = {n: (b, x) for b, lista in e["antes"].items() for n, x in lista}
    for c in e["cambios"]:
        if c["tipo"] in ("color", "falta", "girado"):
            b, x = pos[c["juguete"]]
            zonas.append([caja(x, b)])
        elif c["tipo"] == "sobra":
            zonas.append([caja(c["x"], c["balda"])])
        elif c["tipo"] == "movido":
            b, x = pos[c["juguete"]]
            zonas.append([caja(c["x"], c["a_balda"]), caja(x, b)])
    return zonas


def carta_polaroid(inst):
    h = Hoja(W, H, (120, 170, 210))
    for y in range(0, H, 40):
        h.rect(0, y, W, y + 20, (126, 176, 216))
    h.poli([(70, 120), (580, 96), (594, 780), (84, 800)], BLANCO, (200, 196, 190), 3)
    h.rect(108, 150, 556, 470, (230, 216, 190))
    dibujar_estanteria(h, 120, 176, 420, inst, despues=False)
    h.texto((330, 580), "Mi estantería", "texto", 38, (60, 70, 140))
    h.texto((330, 630), "¡ordenada por fin!", "texto2", 28, (60, 70, 140))
    h.texto((330, 676), "Leo", "texto2", 28, (60, 70, 140))
    h.rect(268, 70, 392, 112, (240, 230, 160))
    return ruido(h.final(), 20)


def ui_estanteria(inst):
    h = Hoja(620, 400, (230, 216, 190))
    dibujar_estanteria(h, 10, 12, 600, inst, despues=True)
    return h.final()


# ================================================================== torre de bloques: vistas
COLORES_ALTURA = {1: VERDE, 2: AZUL, 3: ROJO}


def pila(h, x, base, n, lado, col_fn):
    for i in range(n):
        h.rect(x, base - (i + 1) * lado, x + lado, base - i * lado, col_fn(i), NEGRO, 3)
        h.rect(x + 6, base - (i + 1) * lado + 6, x + lado - 6, base - i * lado - 6, None, (255, 255, 255), 1)


def carta_vistas(inst):
    t = inst["torre"]
    h = Hoja(W, H, PAPEL)
    h.rect(16, 16, W - 16, H - 16, PAPEL, TINTA, 4)
    h.texto((W / 2 + 30, 60), "INSTRUCCIONES", "cartel", 40, TINTA)
    h.texto((W / 2 + 30, 98), "Torre de bloques de Leo (1 de 2)", "texto2", 22, TINTA)
    lado = 62
    for k, (titulo, valores, etiquetas) in enumerate((("VISTA DE FRENTE", t["frente"], ("izquierda", "derecha")),
                                                      ("VISTA DESDE LA DERECHA", t["lado"], ("delante", "detrás")))):
        y = 140 + k * 340
        h.texto((W / 2, y), titulo, "texto", 26, TINTA)
        base = y + 260
        x0 = W / 2 - lado * 1.5
        h.linea([(x0 - 30, base), (x0 + lado * 3 + 30, base)], TINTA, 4)
        for i, v in enumerate(valores):
            pila(h, x0 + i * lado, base, v, lado, lambda n: (AMARILLO, NARANJA, ROJO)[n])
        h.texto((x0 - 10, base + 24), etiquetas[0], "texto2", 19, TINTA, "lm")
        h.texto((x0 + lado * 3 + 10, base + 24), etiquetas[1], "texto2", 19, TINTA, "rm")
    h.texto((W / 2, 820), "La base es de 3 × 3. Nada puede flotar.", "texto2", 21, TINTA)
    return ruido(h.final(), 30)


def carta_planta(inst):
    t = inst["torre"]
    h = Hoja(W, H, PAPEL)
    h.rect(16, 16, W - 16, H - 16, PAPEL, TINTA, 4)
    h.texto((W / 2 + 30, 60), "INSTRUCCIONES", "cartel", 40, TINTA)
    h.texto((W / 2 + 30, 98), "Torre de bloques de Leo (2 de 2)", "texto2", 22, TINTA)
    h.texto((W / 2, 160), "VISTA DESDE ARRIBA", "texto", 26, TINTA)
    h.texto((W / 2, 196), "(las casillas con algún bloque)", "texto2", 20, TINTA)
    lado = 120
    x0, y0 = W / 2 - lado * 1.5, 250
    h.texto((W / 2, y0 - 18), "detrás", "texto2", 20, TINTA)
    for f in range(3):                      # f = 0 delante (abajo en el dibujo) ... 2 detrás (arriba)
        for c in range(3):
            y = y0 + (2 - f) * lado
            lleno = t["arriba"][f][c]
            h.rect(x0 + c * lado, y, x0 + (c + 1) * lado, y + lado, (232, 222, 200) if not lleno else (250, 210, 80), TINTA, 3)
            if lleno:
                h.rect(x0 + c * lado + 18, y + 18, x0 + (c + 1) * lado - 18, y + lado - 18, None, BLANCO, 2)
    h.texto((W / 2, y0 + 3 * lado + 30), "delante", "texto2", 20, TINTA)
    h.texto((x0 - 14, y0 + 1.5 * lado), "izq.", "texto2", 19, TINTA, "rm")
    h.texto((x0 + 3 * lado + 14, y0 + 1.5 * lado), "dcha.", "texto2", 19, TINTA, "lm")
    h.rect(60, 700, W - 60, 800, (244, 236, 214), ROJO, 3)
    h.texto((W / 2, 732), f"Con {t['bloques']} bloques en total,", "texto", 22, TINTA)
    h.texto((W / 2, 768), "ni uno más ni uno menos.", "texto", 22, TINTA)
    return ruido(h.final(), 31)


# ================================================================== marioneta
MIEMBRO_XY = {"brazo_izq": (-62, 40), "brazo_der": (62, 40), "pierna_izq": (-26, 170), "pierna_der": (26, 170)}   # «izq/der» del dibujo


def dibujar_marioneta(h, cx, top, arriba=(), k=1.0, hilos=True):
    """Marioneta de madera de frente; `arriba` = miembros levantados. top = altura de la cabeza."""
    S = k
    cuerpo_y = top + 50 * S
    h.rect(cx - 30 * S, cuerpo_y, cx + 30 * S, cuerpo_y + 80 * S, (220, 70, 70), NEGRO, 2)
    h.rect(cx - 30 * S, cuerpo_y + 60 * S, cx + 30 * S, cuerpo_y + 80 * S, (60, 90, 170), NEGRO, 2)
    h.disco(cx, top + 22 * S, 26 * S, (240, 200, 160), NEGRO, 2)
    h.disco(cx - 9 * S, top + 18 * S, 3 * S, NEGRO)
    h.disco(cx + 9 * S, top + 18 * S, 3 * S, NEGRO)
    h.linea([(cx - 9 * S, top + 32 * S), (cx, top + 36 * S), (cx + 9 * S, top + 32 * S)], NEGRO, 2)
    h.poli([(cx - 26 * S, top + 10 * S), (cx, top - 22 * S), (cx + 26 * S, top + 10 * S)], (60, 140, 80), NEGRO, 2)
    for nombre in ("brazo_izq", "brazo_der"):
        lado = -1 if nombre.endswith("izq") else 1
        hx, hy = cx + lado * 30 * S, cuerpo_y + 8 * S
        if nombre in arriba:
            mano = (hx + lado * 30 * S, hy - 52 * S)
        else:
            mano = (hx + lado * 26 * S, hy + 52 * S)
        h.linea([(hx, hy), mano], (240, 200, 160), 12 * S)
        h.disco(mano[0], mano[1], 8 * S, (240, 200, 160), NEGRO, 2)
    for nombre in ("pierna_izq", "pierna_der"):
        lado = -1 if nombre.endswith("izq") else 1
        px, py = cx + lado * 16 * S, cuerpo_y + 80 * S
        if nombre in arriba:
            pie = (px + lado * 40 * S, py + 26 * S)
        else:
            pie = (px + lado * 6 * S, py + 66 * S)
        h.linea([(px, py), pie], (60, 90, 170), 14 * S)
        h.elip(pie[0] - 12 * S, pie[1] - 6 * S, pie[0] + 12 * S, pie[1] + 8 * S, NEGRO)


def punto_miembro(cx, top, nombre, arriba, k=1.0):
    lado = -1 if nombre.endswith("izq") else 1
    cuerpo_y = top + 50 * k
    if nombre.startswith("brazo"):
        hx, hy = cx + lado * 30 * k, cuerpo_y + 8 * k
        return (hx + lado * 30 * k, hy - 52 * k) if nombre in arriba else (hx + lado * 26 * k, hy + 52 * k)
    px, py = cx + lado * 16 * k, cuerpo_y + 80 * k
    return (px + lado * 40 * k, py + 26 * k) if nombre in arriba else (px + lado * 6 * k, py + 66 * k)


def carta_hilos(inst):
    m = inst["marioneta"]
    h = Hoja(W, H, (60, 40, 70))
    h.degradado(0, H, (90, 50, 90), (40, 24, 50))
    h.rect(16, 16, W - 16, H - 16, None, AMARILLO, 4)
    h.texto((W / 2 + 30, 58), "LOS HILOS DE PIPO", "cartel", 38, (250, 230, 180))
    h.texto((W / 2 + 30, 96), "Se han enredado al guardarlo", "texto2", 22, (230, 210, 170))
    # cruceta con cuatro mandos
    barra_y = 160
    h.rect(110, barra_y - 10, 520, barra_y + 10, MADERA, NEGRO, 2)
    xs_mando = {"rojo": 140, "azul": 260, "amarillo": 380, "verde": 490}
    cx, top = W / 2, 520
    for nombre, x in xs_mando.items():
        forma(h, FORMA_MANDO[nombre], x, barra_y, 20, COLOR_MANDO[nombre])
    dibujar_marioneta(h, cx, top, ())                      # primero la marioneta: los hilos van por delante hasta cada mano y cada pie
    # hilos enredados: curvas con dos puntos de control que se cruzan
    rng = random.Random(52)
    orden_ctrl = [0, 1, 2, 3]
    rng.shuffle(orden_ctrl)
    ctrl_x = [70, 230, 400, 560]
    for i, (mando, miembro) in enumerate(m["hilos"].items()):
        x0 = xs_mando[mando]
        x1, y1 = punto_miembro(cx, top, miembro, ())
        c1 = (ctrl_x[orden_ctrl[i]], 280)
        c2 = (cx + (x1 - cx) * 2.6, 420)                   # cada hilo llega a su miembro desde fuera, sin taparse con los demás
        pts = []
        for t in [j / 60 for j in range(61)]:
            a = (1 - t) ** 3
            b = 3 * (1 - t) ** 2 * t
            c = 3 * (1 - t) * t ** 2
            d = t ** 3
            pts.append((a * x0 + b * c1[0] + c * c2[0] + d * x1, a * (barra_y + 20) + b * c1[1] + c * c2[1] + d * y1))
        h.linea(pts, (235, 228, 210), 3)
        h.disco(x1, y1, 5, (235, 228, 210))
    h.texto((W / 2, 820), "Seguid cada hilo con el dedo.", "texto2", 22, (230, 210, 170))
    return ruido(h.final(), 52)


def carta_cartel(inst):
    m = inst["marioneta"]
    h = Hoja(W, H, (250, 226, 160))
    h.rect(16, 16, W - 16, H - 16, (250, 226, 160), ROJO, 8)
    h.texto((W / 2 + 30, 66), "¡GRAN FUNCIÓN!", "cartel", 46, ROJO)
    h.texto((W / 2 + 30, 110), "Pipo saluda al público así:", "texto", 24, TINTA)
    for x in range(40, W - 40, 60):
        h.poli([(x, 140), (x + 60, 140), (x + 30, 176)], ROJO if (x // 60) % 2 == 0 else AMARILLO, None)
    h.rect(110, 210, 520, 760, (60, 40, 70), (130, 80, 40), 10)
    dibujar_marioneta(h, W / 2, 380, tuple(m["postura"]), k=1.25)
    h.texto((W / 2, 810), "Teatro de Leo · Entrada gratis", "texto2", 22, TINTA)
    return ruido(h.final(), 53)


# ================================================================== folioscopio (cuaderno de Leo)
def pagina(inst, pag):
    fo = inst["folioscopio"]
    paso = pag["paso"]
    h = Hoja(W, H, (252, 250, 240))
    for y in range(150, H - 40, 34):
        h.linea([(40, y), (W - 30, y)], (190, 210, 236), 2)
    h.linea([(90, 40), (90, H - 30)], (240, 160, 160), 2)
    for y in range(60, H - 40, 46):
        h.disco(36, y, 9, (220, 220, 224), (150, 150, 160), 2)
    # ventana con el sol que se pone
    vx0, vy0, vx1, vy1 = 170, 110, 540, 430
    t = paso / 4
    cielo = tuple(int(a + (b - a) * t) for a, b in zip((140, 200, 246), (246, 150, 90)))
    h.rect(vx0, vy0, vx1, vy1, cielo, MADERA2, 8)
    sy = vy0 + 62 + paso * 52
    h.disco(470, sy, 34, (255, 220, 80) if paso < 3 else (255, 160, 60), None)
    h.rect(vx0 + 4, 360, vx1 - 4, vy1 - 4, (90, 150, 90))
    for x in range(vx0 + 30, vx1, 70):
        h.poli([(x - 26, 362), (x, 330), (x + 26, 362)], (70, 130, 80))
    h.linea([((vx0 + vx1) / 2, vy0), ((vx0 + vx1) / 2, vy1)], MADERA2, 6)
    h.linea([(vx0, (vy0 + vy1) / 2 - 20), (vx1, (vy0 + vy1) / 2 - 20)], MADERA2, 6)
    # los cinco juguetes en el suelo, siempre en el mismo sitio; Leo rodea uno con su cera
    base = 640
    h.linea([(110, base), (W - 40, base)], MADERA2, 4)
    for i, nombre in enumerate(fo["juguetes"]):
        x = 150 + i * 98
        juguete(h, nombre, x, base, 0.9)
        if nombre == pag["juguete"]:
            pts = [(x + 52 * math.cos(a / 30 * math.pi * 2 + 0.3) * (1 + 0.05 * math.sin(a)), base - 34 + 52 * math.sin(a / 30 * math.pi * 2 + 0.3)) for a in range(33)]
            h.linea(pts, ROJO, 5)
    h.texto((W / 2 + 20, 720), "Mi cuaderno · Leo", "texto2", 24, (90, 100, 160))
    return ruido(h.final(), 40 + paso)


# ================================================================== pista de canicas: instrucciones
def balancin(h, cx, cy, lado, r=26, col=NARANJA):
    h.disco(cx, cy, 6, NEGRO)
    dx = 30 if lado == "der" else -30
    h.poli([(cx - 4, cy - 4), (cx + 4, cy - 4), (cx + dx + 4, cy + 30), (cx + dx - 4, cy + 30)], col, NEGRO, 2)


def carta_pista(inst):
    p = inst["pista"]
    h = Hoja(W, H, PAPEL)
    h.rect(16, 16, W - 16, H - 16, PAPEL, TINTA, 4)
    h.texto((W / 2 + 30, 58), "LA PISTA DE CANICAS", "cartel", 38, TINTA)
    h.texto((W / 2 + 30, 96), "Instrucciones de la caja", "texto2", 22, TINTA)
    # tablero
    tx0, ty0 = 120, 140
    h.rect(tx0, ty0, W - 120, 520, (232, 214, 170), MADERA2, 6)
    entrada = (W / 2, ty0 + 20)
    b1, b2, b3 = (W / 2, 220), (W / 2 - 110, 330), (W / 2 + 110, 330)
    salidas = {"A": (W / 2 - 160, 470), "B": (W / 2 - 60, 470), "C": (W / 2 + 60, 470), "D": (W / 2 + 160, 470)}
    for a, b in ((entrada, b1), (b1, b2), (b1, b3), (b2, salidas["A"]), (b2, salidas["B"]), (b3, salidas["C"]), (b3, salidas["D"])):
        h.linea([a, b], (180, 150, 110), 10)
    h.poli([(entrada[0] - 12, entrada[1] - 12), (entrada[0] + 12, entrada[1] - 12), (entrada[0], entrada[1] + 6)], TINTA)
    for (x, y), nombre in ((b1, "1"), (b2, "2"), (b3, "3")):
        h.disco(x, y, 30, (250, 240, 220), MADERA2, 3)
        h.texto((x + 44, y - 18), nombre, "texto", 22, TINTA)
    for letra, (x, y) in salidas.items():
        h.texto((x, y + 30), letra, "texto", 24, TINTA)
        if letra == p["tarro"]:
            h.rect(x - 22, y, x + 22, y + 10, None, None)
            h.poli([(x - 24, y - 6), (x + 24, y - 6), (x + 20, y + 22), (x - 20, y + 22)], (190, 230, 240), (60, 120, 140), 3)
            h.texto((x, y - 22), "tarro", "texto2", 16, TINTA)
    # regla con ejemplo
    h.rect(40, 545, W - 40, 830, (244, 236, 214), ROJO, 3)
    lineas = ["Cada balancín manda la canica hacia el lado",
              "al que apunta y, al pasar, CAMBIA DE LADO.",
              "Leo suelta las canicas de una en una;",
              "el cristal es la TERCERA. Tiene que caer",
              "en el tarro. Antes de soltar, colocad",
              "los tres balancines como haga falta."]
    for k, t in enumerate(lineas):
        h.texto((W / 2, 572 + k * 34), t, "texto2", 21, TINTA)
    balancin(h, 220, 770, "izq")
    h.texto((315, 760), "pasa una canica", "texto2", 18, TINTA)
    h.linea([(270, 784), (352, 784)], TINTA, 3)
    h.poli([(352, 776), (366, 784), (352, 792)], TINTA)
    balancin(h, 410, 770, "der")
    return ruido(h.final(), 70)


# ================================================================== imágenes de la interfaz
def ui_imagenes(carpeta, inst):
    ui = os.path.join(carpeta, "img", "ui")
    os.makedirs(ui, exist_ok=True)

    def transparente(h, nombre, clave=(255, 0, 255)):
        im = h.final()
        a = np.asarray(im).astype(np.int16)
        alfa = np.clip(np.abs(a - np.array(clave)).sum(axis=2) * 3, 0, 255).astype(np.uint8)
        Image.fromarray(np.dstack([np.asarray(im), alfa])).save(os.path.join(ui, nombre))

    ui_estanteria(inst).save(os.path.join(ui, "estanteria.jpg"), quality=88)
    miembros = inst["marioneta"]["miembros"]
    for bits in range(16):
        arriba = tuple(m for i, m in enumerate(miembros) if bits >> i & 1)
        h = Hoja(240, 320, (255, 0, 255))
        dibujar_marioneta(h, 120, 60, arriba, k=1.05)
        transparente(h, f"pipo-{bits}.png")
    for nombre in inst["folioscopio"]["juguetes"]:
        h = Hoja(110, 110, (255, 0, 255))
        juguete(h, nombre, 55, 96, 1.15)
        transparente(h, f"jug-{nombre}.png")


DATOS_MINIJUEGOS = {
    "24-estanteria.js": lambda i: {"zonas": zonas_diferencias(i), "textos": [c["texto"] for c in i["estanteria"]["cambios"]]},
    "46-torre.js": lambda i: {"alturas": i["torre"]["alturas"], "bloques": i["torre"]["bloques"]},
    "48-marioneta.js": lambda i: {k: i["marioneta"][k] for k in ("mandos", "miembros", "hilos", "postura")},
    "66-tren.js": lambda i: {"juguetes": i["folioscopio"]["juguetes"], "orden": i["folioscopio"]["orden"]},
    "69-canicas.js": lambda i: {k: i["pista"][k] for k in ("tarro", "solucion", "canicas")},
}


def inyectar_datos(carpeta, inst):
    for nombre, f in DATOS_MINIJUEGOS.items():
        ruta = os.path.join(carpeta, "minijuegos", nombre)
        if not os.path.exists(ruta):
            continue
        js = open(ruta, encoding="utf-8").read()
        a, b = js.index("/*DATOS*/") + len("/*DATOS*/"), js.index("/*FIN*/")
        js = js[:a] + json.dumps(f(inst), ensure_ascii=False, separators=(", ", ": ")) + js[b:]
        open(ruta, "w", encoding="utf-8", newline="\n").write(js)


def main(carpeta="juegos/aventuras-ca/juguetes"):
    inst = _inst()
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    laminas = {"20": carta_polaroid(inst), "30": carta_vistas(inst), "31": carta_planta(inst), "52": carta_hilos(inst),
               "53": carta_cartel(inst), "70": carta_pista(inst)}
    for pag in inst["folioscopio"]["paginas"]:
        laminas[pag["carta"]] = pagina(inst, pag)
    for k, im in laminas.items():
        im.save(os.path.join(arte, f"{k}.png"))
    ui_imagenes(carpeta, inst)
    inyectar_datos(carpeta, inst)
    print("láminas escritas en", arte)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

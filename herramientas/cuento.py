"""Láminas de «Érase una vez: El Libro de los Finales Felices» (versión de 60 cartas, 21 oct 2026). Todas las pistas son dibujos o acertijos:
ninguna carta escribe la respuesta ni explica cómo se resuelve su puzle. Datos de herramientas/instancias_cuento.py.

  16 el escaparate (precios en monedas) · 18 los duendes (minutos en granos de arena) · 19 y 21 la vela del troll (dos mitades)
  41, 43 y 45 «había una vez / y ahora» (qué hace cada salto en el tiempo, con ejemplos dibujados)
  42 y 49 el mapa del bosque (dos mitades) · 53 el acertijo de las botas · 54, 55 y 59 la habichuela, día a día
  37 la ventana · 39 los cristales · 33 la nota del vidriero · 26, 61 y 63 lo que dijeron las hadas
  66 y 67 el plano de la sala de los espejos (dos mitades) · 70 el tapiz de los estandartes · 71 la nota de la cocinera
  75 la partitura de animales · 79 el xilófono del bosque · 86 la nota del Búho
Uso (desde la raíz del repo):  python herramientas/cuento.py [carpeta_juego]
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
import instancias_cuento as I  # noqa: E402

W, H = 630, 882
PAPEL = (250, 240, 214)
TINTA = (60, 40, 70)
LILA = (120, 90, 190)
ROSA = (230, 120, 150)
ORO = (230, 180, 60)
TURQ = (60, 170, 170)
VERDE = (90, 160, 90)
MARRON = (140, 96, 60)
AZUL = (70, 110, 200)
ROJO = (200, 60, 60)
BLANCO = (255, 252, 244)
NEGRO = (30, 26, 34)


def ruido(im, s, f=2.5):
    a = np.asarray(im).astype(np.int16)
    a = a + np.random.default_rng(s).normal(0, f, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def pagina(titulo, sub=None, fondo=PAPEL, borde=LILA):
    h = Hoja(W, H, fondo)
    h.rect(16, 16, W - 16, H - 16, None, borde, 6)
    h.rect(28, 28, W - 28, H - 28, None, borde, 2)
    h.texto((W / 2 + 26, 70), titulo, "cartel", 32, TINTA)
    if sub:
        h.texto((W / 2 + 26, 108), sub, "texto2", 21, TINTA)
    return h


def versos(h, lineas, y0=220, paso=56, tam=28):
    for k, v in enumerate(lineas):
        h.texto((W / 2, y0 + k * paso), v, "texto2", tam, TINTA)


def moneda(h, x, y, r=13):
    h.disco(x, y, r, ORO, (160, 110, 30), 2)
    h.disco(x, y, r * 0.55, None, (160, 110, 30), 1.5)


# ------------------------------------------------------------------ 16: el escaparate
def escaparate():
    h = pagina("EL ESCAPARATE", "de Doña Hogaza")
    # hogaza: 5 monedas; bollo de nata: 4 monedas
    h.elip(90, 200, 290, 300, (200, 140, 70), MARRON, 3)
    for k in range(3):
        h.linea([(130 + k * 50, 225), (150 + k * 50, 275)], (230, 190, 120), 4)
    for k in range(5):
        moneda(h, 330 + k * 34, 250)
    h.elip(120, 360, 250, 440, (240, 220, 200), MARRON, 3)
    h.elip(130, 340, 240, 380, BLANCO, (220, 200, 180), 2)
    for k in range(4):
        moneda(h, 330 + k * 34, 400)
    h.rect(90, 500, 540, 620, (240, 226, 190), MARRON, 3)
    h.texto((W / 2, 530), "«Cada pan, su precio en monedas.", "texto2", 24, TINTA)
    h.texto((W / 2, 566), "Y mi cartel dice lo que cuestan", "texto2", 24, TINTA)
    h.texto((W / 2, 600), "los dos juntos.»", "texto2", 24, TINTA)
    return h.final()


# ------------------------------------------------------------------ 18: los duendes; 19/21: la vela
def reloj_arena(h, x, y, granos):
    h.poli([(x - 46, y - 56), (x + 46, y - 56), (x, y)], (240, 230, 200), TINTA, 3)
    h.poli([(x - 46, y + 56), (x + 46, y + 56), (x, y)], (240, 230, 200), TINTA, 3)
    for k in range(granos):
        fila, col = divmod(k, 6)
        h.disco(x - 30 + col * 12, y + 46 - fila * 11, 5, (200, 140, 40), TINTA, 1)


def duendes():
    h = pagina("LOS CUATRO DUENDES", "cuánta arena cae mientras cruza cada uno")
    nombres = ["Bigotes", "Pétalo", "Gruñón", "Abuela Musgo"]
    for k, (n, t) in enumerate(zip(nombres, I.PUENTE["tiempos"])):
        y = 220 + k * 140
        h.disco(110, y, 40, (150, 200, 140), TINTA, 3)
        h.poli([(80, y - 30), (110, y - 80), (140, y - 30)], ROJO, TINTA, 2)
        h.disco(98, y - 4, 5, NEGRO)
        h.disco(122, y - 4, 5, NEGRO)
        h.texto((170, y), n, "texto", 24, TINTA, "lm")
        reloj_arena(h, 470, y, t * 2)
    h.texto((W / 2, 790), "Cada dos granos, un minuto.", "texto2", 22, TINTA)
    return h.final()


def vela():
    h = Hoja(W, H * 2, (40, 40, 80))
    h.degradado(0, H * 2, (60, 60, 110), (20, 20, 50))
    h.texto((W / 2, 80), "LA VELA DEL TROLL", "cartel", 34, (240, 230, 200))
    h.texto((W / 2, 120), "«Cuando se apague, saldrá el sol»", "texto2", 22, (220, 210, 190))
    x0, x1, y0, y1 = W / 2 - 60, W / 2 + 60, 300, 300 + 15 * 80
    h.poli([(W / 2, 200), (W / 2 - 22, 260), (W / 2, 290), (W / 2 + 22, 260)], (255, 200, 80))
    h.rect(x0, y0, x1, y1, (240, 230, 210), (200, 190, 170), 3)
    for k in range(1, 15):
        y = y0 + k * 80
        h.linea([(x0, y), (x1, y)], ROJO, 4)
    h.rect(x0 - 60, y1, x1 + 60, y1 + 30, (150, 130, 100), TINTA, 3)
    h.texto((W / 2, y1 + 110), "Cada raya, un minuto de cera.", "texto2", 24, (220, 210, 190))
    return h.final()


# ------------------------------------------------------------------ 41/43/45: había una vez / y ahora
ICONOS = {"pradera": (140, 200, 110), "bosquecillo": (70, 130, 70), "charca": (90, 150, 210), "colina": (160, 140, 110),
          "libre": (220, 200, 150), "zarza": (110, 80, 60), "rio": (70, 120, 200), "roca": (130, 130, 140),
          "habichuela": (90, 180, 90), "puente": (170, 120, 70), "zarzal": (90, 60, 40), "foso": (60, 40, 30), "hueco": (40, 34, 30),
          "ceniza": (90, 90, 90)}
NOMBRE_T = {"pradera": "prado", "bosquecillo": "arbolitos", "charca": "charca", "colina": "colina", "libre": "camino", "zarza": "zarza",
            "rio": "río", "roca": "roca", "habichuela": "habichuela", "puente": "tronco caído", "zarzal": "zarzal enorme", "foso": "foso",
            "hueco": "túnel", "ceniza": "ceniza"}


def casilla(h, x, y, terreno, lado=110):
    h.rect(x, y, x + lado, y + lado, ICONOS[terreno], TINTA, 3)
    h.texto((x + lado / 2, y + lado + 22), NOMBRE_T[terreno], "texto2", 18, TINTA)


def antes_ahora(accion, ejemplos, sem):
    tit = {"plantar": "PLANTAR UNA SEMILLA", "cavar": "CAVAR", "fuego": "ENCENDER FUEGO"}[accion]
    h = pagina(tit, "Había una vez...  /  ...y ahora", PAPEL, VERDE)
    h.texto((180, 170), "si pasó esto encima de...", "texto2", 18, TINTA)
    h.texto((450, 170), "...hoy hay", "texto2", 18, TINTA)
    for k, ahora_antes in enumerate(ejemplos):
        y = 200 + k * 190
        casilla(h, 125, y, ahora_antes)
        h.poli([(275, y + 45), (330, y + 45), (330, y + 30), (360, y + 55), (330, y + 80), (330, y + 65), (275, y + 65)], TINTA)
        casilla(h, 395, y, I.efecto(accion, ahora_antes))
    h.texto((W / 2, 800), "(lo de la izquierda es lo que hay hoy en esa casilla)", "texto2", 18, TINTA)
    return h.final()


# ------------------------------------------------------------------ 42/49: el mapa de las botas; 53: el acertijo
def mapa_botas():
    b = I.BOTAS
    n = b["n"]
    h = Hoja(W * 2, H, (210, 230, 190))
    h.texto((W, 60), "EL BOSQUE DE LAS SIETE LEGUAS", "cartel", 36, TINTA)
    lado = 104
    x0, y0 = (W * 2 - n * lado) / 2, 120
    obst = {tuple(o) for o in b["obstaculos"]}
    rng = random.Random(42)
    for y in range(n):
        for x in range(n):
            px, py = x0 + x * lado, y0 + y * lado
            h.rect(px, py, px + lado, py + lado, (196, 222, 170), (160, 190, 140), 1)
            if (x, y) in obst:
                if rng.random() < 0.6:
                    h.disco(px + lado / 2, py + lado / 2 - 10, 34, (60, 120, 60), TINTA, 2)
                    h.rect(px + lado / 2 - 6, py + lado / 2 + 20, px + lado / 2 + 6, py + lado - 10, MARRON)
                else:
                    h.rect(px + 6, py + 6, px + lado - 6, py + lado - 6, (90, 150, 210), (60, 110, 170), 2)
    sx, sy = b["inicio"]
    h.texto((x0 + sx * lado + lado / 2, y0 + sy * lado + lado / 2), "TÚ", "cartel", 30, ROJO)
    fx, fy = b["fin"]
    px, py = x0 + fx * lado, y0 + fy * lado
    h.poli([(px + 20, py + 90), (px + 20, py + 40), (px + 52, py + 14), (px + 84, py + 40), (px + 84, py + 90)], (230, 210, 230), TINTA, 3)
    return h.final()


def acertijo_botas():
    h = pagina("LAS BOTAS DEL GIGANTE", "bordado en la lengüeta")
    versos(h, ["Con un pie salto dos,", "con el otro salto tres:", "primero el izquierdo, luego el derecho,", "y así hasta el final del mes.",
               "Salto por encima de todo,", "pero nunca caigo en el agua", "ni me estrello contra un árbol."], 220, 58, 26)
    return h.final()


# ------------------------------------------------------------------ 54/55/59: la habichuela
def habichuela(dias, sem):
    h = pagina("EL DIARIO DEL LEÑADOR", "lo que crece la habichuela cada mañana", PAPEL, VERDE)
    for k, dia in enumerate(dias):
        x = 170 + k * 290
        y0 = 720
        for luna in range(dia + 1):
            h.disco(x - 60 + luna * 22, 150, 8, (240, 230, 150), TINTA, 1.5)
        h.texto((x, 180), "lunas que pasaron", "texto2", 15, TINTA)
        hojas = I.HABICHUELA["dibujados"][dia]
        alto = 120 + hojas * 50
        h.linea([(x, y0), (x + 10, y0 - alto / 2), (x - 6, y0 - alto)], (60, 140, 60), 8)
        rng = random.Random(sem * 10 + k)
        for i in range(hojas):
            t = (i + 1) / (hojas + 1)
            yy = y0 - alto * t
            lado = -1 if i % 2 else 1
            h.elip(x + lado * 8 - 22 + lado * 18, yy - 12, x + lado * 8 + 22 + lado * 18, yy + 12, (90, 180, 90), (40, 110, 40), 2)
        h.rect(x - 60, y0, x + 60, y0 + 30, MARRON)
    return h.final()


# ------------------------------------------------------------------ 37/39/33: la vidriera
def ventana():
    h = pagina("LA VENTANA DE LA TORRE", "dibujo del vidriero", PAPEL, AZUL)
    dib = {(int(a), int(b)) for a, b in (k.split(",") for k in ["0,2", "1,2", "2,2", "3,2", "4,2", "1,3", "2,3", "3,3", "1,4", "2,4", "3,4", "4,4"])}
    lado, x0, y0 = 90, (W - 450) / 2, 250
    h.poli([(x0, y0), (x0 + 225, y0 - 90), (x0 + 450, y0)], (230, 220, 240), TINTA, 3)
    for y in range(5):
        for x in range(5):
            px, py = x0 + x * lado, y0 + y * lado
            h.rect(px, py, px + lado, py + lado, (255, 236, 150) if (x, y) in dib else (70, 60, 100), TINTA, 3)
    return h.final()


TETRA = {"palo": [(0, 0), (1, 0), (2, 0), (3, 0)], "ese": [(1, 0), (2, 0), (0, 1), (1, 1)], "te": [(0, 0), (1, 0), (2, 0), (1, 1)]}


def cristales():
    h = pagina("LOS TRES CRISTALES", "como salieron del horno", PAPEL, AZUL)
    cols = [(230, 90, 90), (90, 170, 230), (120, 200, 120)]
    for k, (nombre, celdas) in enumerate(TETRA.items()):
        y = 200 + k * 200
        for x, yy in celdas:
            h.rect(170 + x * 70, y + yy * 70, 240 + x * 70, y + 70 + yy * 70, cols[k], TINTA, 3)
    return h.final()


def nota_vidriero():
    h = pagina("NOTA DEL VIDRIERO", None, PAPEL, AZUL)
    versos(h, ["«Mis cristales salen del horno", "tal como los veis: si los giráis,", "se rajan.", "Si dos se pisan, la luz se apaga.",
               "Y si queda un hueco a oscuras,", "la torre no despierta.»"], 220, 60, 27)
    return h.final()


# ------------------------------------------------------------------ 26/61/63: las hadas
def hadas(titulo, sub, lineas, sem):
    h = pagina(titulo, sub, PAPEL, ROSA)
    versos(h, lineas, 230, 58, 26)
    return h.final()


# ------------------------------------------------------------------ 66/67: plano de la sala de los espejos
def plano_espejos():
    r = I.RAYOS
    n = r["n"]
    h = Hoja(W * 2, H, (30, 30, 60))
    h.texto((W, 60), "LA SALA DE LOS ESPEJOS", "cartel", 36, (230, 230, 250))
    lado = 140
    x0, y0 = (W * 2 - n * lado) / 2, 140
    for i in range(n * n):
        y, x = divmod(i, n)
        px, py = x0 + x * lado, y0 + y * lado
        h.rect(px, py, px + lado, py + lado, (60, 60, 100), (100, 100, 150), 2)
        if i in r["paredes"]:
            h.rect(px + 8, py + 8, px + lado - 8, py + lado - 8, (120, 110, 100), (80, 70, 60), 3)
        if i == r["objetivo"]:
            for k in range(6):
                a = k * math.pi / 3
                h.elip(px + lado / 2 + 30 * math.cos(a) - 18, py + lado / 2 + 30 * math.sin(a) - 18,
                       px + lado / 2 + 30 * math.cos(a) + 18, py + lado / 2 + 30 * math.sin(a) + 18, (230, 230, 255))
            h.disco(px + lado / 2, py + lado / 2, 14, (255, 240, 150))
    fy = r["fila"]
    py = y0 + fy * lado + lado / 2
    h.poli([(x0 - 70, py - 24), (x0 - 10, py), (x0 - 70, py + 24)], (255, 240, 150))
    return h.final()


# ------------------------------------------------------------------ 70/71: el tapiz y la cocinera
def tapiz():
    h = pagina("EL TAPIZ DEL SALÓN", "los estandartes del rey, en su pared", PAPEL, ORO)
    cols = {0: ROSA, 1: ORO, 2: TURQ}
    orden = I.POCIONES["orden"]
    for k, c in enumerate(orden):
        x = 140 + k * 175
        h.linea([(x - 40, 200), (x + 40, 200)], MARRON, 6)
        h.poli([(x - 36, 204), (x + 36, 204), (x + 36, 470), (x, 430), (x - 36, 470)], cols[c], TINTA, 3)
        h.disco(x, 300, 22, BLANCO, TINTA, 2)
    for k in range(2):
        x = 140 + (3 + k) * 175 - 525 + 87
    h.texto((W / 2, 560), "Dos huecos de la pared", "texto2", 24, TINTA)
    h.texto((W / 2, 594), "se quedaron sin estandarte.", "texto2", 24, TINTA)
    return h.final()


def cocinera():
    h = pagina("NOTA DE LA COCINERA REAL", None, PAPEL, ORO)
    versos(h, ["«Los colores del reino", "van en los tarros como en el salón:", "cada uno en el suyo, sin mezclar,", "de izquierda a derecha.",
               "Y lo que en la pared está vacío,", "vacío en la despensa.»"], 220, 60, 26)
    return h.final()


# ------------------------------------------------------------------ 75/79: la caja de música
def animal(h, nombre, cx, cy, r, col=TINTA):
    if nombre == "conejo":
        h.disco(cx, cy + r * 0.2, r * 0.55, col)
        h.elip(cx - r * 0.35, cy - r * 0.9, cx - r * 0.1, cy - r * 0.1, col)
        h.elip(cx + r * 0.1, cy - r * 0.9, cx + r * 0.35, cy - r * 0.1, col)
    elif nombre == "ciervo":
        h.elip(cx - r * 0.35, cy - r * 0.2, cx + r * 0.35, cy + r * 0.7, col)
        for s in (-1, 1):
            h.linea([(cx + s * r * 0.2, cy - r * 0.2), (cx + s * r * 0.6, cy - r * 0.9)], col, r * 0.1)
            h.linea([(cx + s * r * 0.45, cy - r * 0.6), (cx + s * r * 0.8, cy - r * 0.6)], col, r * 0.1)
    elif nombre == "búho":
        h.elip(cx - r * 0.5, cy - r * 0.6, cx + r * 0.5, cy + r * 0.8, col)
        h.disco(cx - r * 0.2, cy - r * 0.2, r * 0.17, BLANCO)
        h.disco(cx + r * 0.2, cy - r * 0.2, r * 0.17, BLANCO)
    elif nombre == "rana":
        h.elip(cx - r * 0.7, cy - r * 0.2, cx + r * 0.7, cy + r * 0.6, col)
        h.disco(cx - r * 0.4, cy - r * 0.3, r * 0.22, col)
        h.disco(cx + r * 0.4, cy - r * 0.3, r * 0.22, col)
    elif nombre == "ardilla":
        h.disco(cx - r * 0.1, cy + r * 0.2, r * 0.45, col)
        h.elip(cx + r * 0.2, cy - r * 0.8, cx + r * 0.8, cy + r * 0.6, col)
    else:  # zorro
        h.poli([(cx - r * 0.7, cy - r * 0.5), (cx + r * 0.7, cy - r * 0.5), (cx, cy + r * 0.7)], col)
        h.poli([(cx - r * 0.7, cy - r * 0.5), (cx - r * 0.5, cy - r * 1.0), (cx - r * 0.2, cy - r * 0.5)], col)
        h.poli([(cx + r * 0.7, cy - r * 0.5), (cx + r * 0.5, cy - r * 1.0), (cx + r * 0.2, cy - r * 0.5)], col)


def partitura():
    h = pagina("LA PARTITURA DE LA CAJA", "tal como la pintó el músico del rey", PAPEL, LILA)
    for k in range(5):
        h.linea([(50, 300 + k * 30), (W - 50, 300 + k * 30)], (180, 160, 200), 2)
    for k, a in enumerate(I.PARTITURA):
        animal(h, a, 90 + k * 75, 360, 36)
    h.texto((W / 2, 520), "De izquierda a derecha.", "texto2", 24, TINTA)
    return h.final()


def xilofono():
    h = pagina("EL XILÓFONO DEL BOSQUE", "cada animal, sentado en su tecla", PAPEL, LILA)
    notas = I.NOTAS
    cols = [(230, 90, 90), (240, 150, 70), (240, 210, 70), (120, 200, 100), (80, 170, 220), (110, 110, 220), (180, 110, 210)]
    inv = {v: k for k, v in I.TABLA.items()}
    for k, nota in enumerate(notas):
        x = 70 + k * 74
        alto = 420 - k * 32
        h.rect(x, 640 - alto, x + 60, 640, cols[k], TINTA, 3)
        h.texto((x + 30, 670), nota, "texto", 20, TINTA)
        if nota in inv:
            animal(h, inv[nota], x + 30, 640 - alto - 40, 26)
    return h.final()


def nota_buho():
    h = pagina("NOTA DEL BÚHO NARRADOR", None, PAPEL, LILA)
    versos(h, ["«Todo cuento que se precie", "acaba en un banquete:", "fueron felices y comieron...", "lo que veréis en la mesa.",
               "Cada puzle os dejó una letra;", "el libro las guarda todas.»"], 220, 60, 27)
    return h.final()


def inyectar(carpeta):
    """Mete los datos de las instancias en las apps que los necesitan (bloque /*DATOS*/.../*FIN*/)."""
    for app, datos in (("48-botas.js", I.BOTAS), ("52-habichuela.js", I.HABICHUELA)):
        ruta = os.path.join(carpeta, "minijuegos", app)
        txt = open(ruta, encoding="utf-8").read()
        a, b = txt.index("/*DATOS*/") + len("/*DATOS*/"), txt.index("/*FIN*/")
        open(ruta, "w", encoding="utf-8", newline="\n").write(txt[:a] + json.dumps(datos, ensure_ascii=False) + txt[b:])


def main(carpeta="juegos/aventuras-ca/cuento"):
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    g = lambda k, im: ruido(im, int(k)).save(os.path.join(arte, f"{k}.png"))
    g("16", escaparate())
    g("18", duendes())
    v = vela()
    v.save(os.path.join(arte, "mosaico-vela.png"))
    for pieza, k in zip(cortar(v, 2, 1), ("19", "21")):
        pieza.save(os.path.join(arte, f"{k}.png"))
    g("41", antes_ahora("plantar", ["rio", "libre", "zarza"], 41))
    g("43", antes_ahora("cavar", ["roca", "libre", "rio"], 43))
    g("45", antes_ahora("fuego", ["zarza", "libre", "roca"], 45))
    m = mapa_botas()
    m.save(os.path.join(arte, "mosaico-botas.png"))
    for pieza, k in zip(cortar(m, 1, 2), ("42", "49")):
        pieza.save(os.path.join(arte, f"{k}.png"))
    g("53", acertijo_botas())
    g("54", habichuela([0, 1], 54))
    g("55", habichuela([2, 3], 55))
    g("59", habichuela([4, 5], 59))
    g("37", ventana())
    g("39", cristales())
    g("33", nota_vidriero())
    g("26", hadas("LOS CHISMES DE DOÑA HOGAZA", "sobre las hadas de la torre",
                  ["«Las hadas de ala azul", "nunca mienten.", "Las de ala roja, siempre.", "Y Brisa me dijo:",
                   "Nube es de ala roja.»"], 26))
    g("61", hadas("UN PAPELITO", "con la letra de Lila", ["«Dalia es de ala roja.»", "", "— Lila"], 61))
    g("63", hadas("OTRO PAPELITO", "con la letra de Nube", ["«Brisa y Lila", "son de ala azul.»", "", "— Nube"], 63))
    p = plano_espejos()
    p.save(os.path.join(arte, "mosaico-espejos.png"))
    for pieza, k in zip(cortar(p, 1, 2), ("66", "67")):
        pieza.save(os.path.join(arte, f"{k}.png"))
    g("70", tapiz())
    g("71", cocinera())
    g("75", partitura())
    g("79", xilofono())
    g("86", nota_buho())
    inyectar(carpeta)
    print("láminas de Cuento escritas en", arte)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

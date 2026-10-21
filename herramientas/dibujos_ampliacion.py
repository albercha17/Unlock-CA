"""Láminas de las cartas-pista de la ampliación a 36 cartas (20 oct 2026), dibujadas por código a partir de instancias_ampliacion.json,
y las imágenes de los minijuegos nuevos. También copia en cada minijuego nuevo (entre /*DATOS*/ y /*FIN*/) los datos de su instancia.

  Marte:      75, 76 y 78 (las tres salidas del circuito), 81 (leyenda y estado pedido), 87, 89 y 90 (cuaderno de muestras).
  Egipto:     38 y 51 (las ofrendas: mitad de arriba y de abajo), 45, 48 y 49 (la losa de los números, en tres franjas).
  Florencia:  47, 48, 49 y 50 (las cuatro cajas del baúl).
  Montecarlo: 37, 39, 41 y 42 (las cuatro manos de póker).
  Piratas:    63 (las guardias), 65 (las campanadas) y 67 (el diario de la capitana).
  Juguetes:   67 (el dibujo de Leo que hay que formar con los cubos).
  El Faro:    46 y 47 (plano de la bahía), 56 (la sombra en la pared), 57 (el estante del farero), 66 (almanaque) y 67 (nota de Anselmo).
Uso (desde la raíz del repo):  python herramientas/dibujos_ampliacion.py
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

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
W, H = 630, 882
TINTA = (40, 34, 30)
BLANCO = (250, 248, 240)
NEGRO = (26, 24, 26)
ROJO = (196, 46, 40)
AZUL = (40, 90, 180)
VERDE = (52, 150, 80)
AMARILLO = (240, 196, 40)
GRIS = (140, 140, 150)


def inst():
    return json.load(open(os.path.join(AQUI, "instancias_ampliacion.json"), encoding="utf-8"))


def ruido(im, semilla, fuerza=2.5):
    a = np.asarray(im).astype(np.int16)
    a = a + np.random.default_rng(semilla).normal(0, fuerza, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def guardar(juego, carta, im, semilla):
    d = os.path.join(RAIZ, "juegos", "aventuras-ca", juego, "arte")
    os.makedirs(d, exist_ok=True)
    ruido(im, semilla).save(os.path.join(d, f"{carta}.png"))


def ui_dir(juego):
    d = os.path.join(RAIZ, "juegos", "aventuras-ca", juego, "img", "ui")
    os.makedirs(d, exist_ok=True)
    return d


def transparente(im, ruta, clave=(255, 0, 255)):
    a = np.asarray(im).astype(np.int16)
    alfa = np.clip(np.abs(a - np.array(clave)).sum(axis=2) * 3, 0, 255).astype(np.uint8)
    Image.fromarray(np.dstack([np.asarray(im), alfa])).save(ruta)


def cabecera(h, titulo, sub, col=TINTA, fondo=None):
    h.texto((W / 2 + 30, 60), titulo, "cartel", 36, col)
    if sub:
        h.texto((W / 2 + 30, 98), sub, "texto2", 21, col)


# ================================================================== MARTE: circuito
MARTE_FONDO = (18, 30, 40)
CIAN = (110, 230, 240)


def puerta(h, tipo, x, y, col=CIAN):
    """Dibuja una puerta lógica con la salida en (x + 70, y)."""
    if tipo == "Y":
        h.rect(x, y - 30, x + 34, y + 30, None, col, 4)
        h.d.arc([(x + 4) * 2, (y - 30) * 2, (x + 64) * 2, (y + 30) * 2], -90, 90, fill=col, width=8)
    elif tipo == "O":
        h.d.arc([(x - 20) * 2, (y - 30) * 2, (x + 20) * 2, (y + 30) * 2], -90, 90, fill=col, width=8)
        h.d.arc([(x - 30) * 2, (y - 30) * 2, (x + 70) * 2, (y + 70) * 2], -90, -20, fill=col, width=8)
        h.d.arc([(x - 30) * 2, (y - 70) * 2, (x + 70) * 2, (y + 30) * 2], 20, 90, fill=col, width=8)
    else:
        h.poli([(x, y - 22), (x + 52, y), (x, y + 22)], None, col, 4)
        h.disco(x + 60, y, 8, MARTE_FONDO, col, 4)
    h.texto((x + 30, y + 44), tipo, "cartel", 20, col)


def dibujar_arbol(h, nodo, x, y, alto, col=CIAN):
    """Dibuja el nodo con su salida en (x, y) hacia la derecha; las entradas, a la izquierda. Devuelve nada."""
    if nodo[0] == "in":
        h.disco(x - 16, y, 18, (40, 60, 70), col, 3)
        h.texto((x - 16, y + 1), nodo[1], "cartel", 22, BLANCO)
        return
    if nodo[0] == "NO":
        gx = x - 70
        puerta(h, "NO", gx, y, col)
        h.linea([(gx - 30, y), (gx, y)], col, 4)
        dibujar_arbol(h, nodo[1], gx - 30, y, alto, col)
        return
    gx = x - 70
    puerta(h, nodo[0], gx, y, col)
    for k, hijo in enumerate(nodo[1:]):
        hy = y - alto / 2 if k == 0 else y + alto / 2
        h.linea([(gx, y - 16 if k == 0 else y + 16), (gx - 30, y - 16 if k == 0 else y + 16), (gx - 30, hy), (gx - 60, hy)], col, 4)
        dibujar_arbol(h, hijo, gx - 60, hy, alto / 2.1, col)


NOMBRE_SALIDA = {"motor": "MOTOR DE LA PUERTA", "alarma": "ALARMA", "ventilacion": "VENTILACIÓN"}


def marte_salida(nombre, arbol):
    h = Hoja(W, H, MARTE_FONDO)
    for y in range(0, H, 24):
        h.linea([(0, y), (W, y)], (24, 40, 52), 1)
    for x in range(0, W, 24):
        h.linea([(x, 0), (x, H)], (24, 40, 52), 1)
    h.rect(16, 16, W - 16, H - 16, None, CIAN, 3)
    h.texto((W / 2 + 30, 64), "PLACA DEL ANEXO", "cartel", 34, CIAN)
    h.texto((W / 2 + 30, 102), "Salida: " + NOMBRE_SALIDA[nombre].lower(), "texto2", 22, (180, 230, 236))
    y = 440
    h.linea([(500, y), (560, y)], CIAN, 4)
    h.disco(568, y, 22, (255, 220, 90) if nombre != "alarma" else (255, 90, 90), BLANCO, 3)
    h.texto((568, y + 52), {"motor": "motor", "alarma": "alarma", "ventilacion": "aire"}[nombre], "texto", 18, BLANCO)
    dibujar_arbol(h, arbol, 500, y, 260)
    h.texto((W / 2, 780), "Los círculos con letra son los interruptores.", "texto2", 20, (180, 230, 236))
    return h.final()


def marte_leyenda(c):
    h = Hoja(W, H, MARTE_FONDO)
    h.rect(16, 16, W - 16, H - 16, None, CIAN, 3)
    h.texto((W / 2 + 30, 64), "PARTE DE AVERÍAS", "cartel", 34, CIAN)
    h.texto((W / 2 + 30, 102), "Dra. Reyes — anexo del reactor", "texto2", 21, (180, 230, 236))
    filas = [("Y", "se enciende si le llegan LAS DOS"), ("O", "se enciende si le llega ALGUNA"), ("NO", "hace lo contrario de lo que le llega")]
    for k, (t, txt) in enumerate(filas):
        y = 190 + k * 100
        puerta(h, t, 70, y)
        h.texto((190, y), txt, "texto2", 21, BLANCO, "lm")
    h.linea([(40, 500), (W - 40, 500)], CIAN, 2)
    h.texto((W / 2, 540), "Para abrir la puerta interior:", "texto", 24, BLANCO)
    est = [("motor", "ENCENDIDO", (255, 220, 90)), ("alarma", "APAGADA", (90, 90, 100)), ("aire", "ENCENDIDO", (255, 220, 90))]
    for k, (n, e, col) in enumerate(est):
        y = 610 + k * 64
        h.disco(130, y, 20, col, BLANCO, 3)
        h.texto((170, y), f"{n}: {e}", "texto", 24, BLANCO, "lm")
    return h.final()


# ------------------------------------------------------------------ Marte: muestras
COL_ROCA = {"rojo": (190, 70, 50), "gris": (150, 150, 156), "negro": (54, 52, 58)}


def roca(h, m, cx, cy, r, semilla):
    rng = random.Random(semilla)
    n = 14 if m["forma"] == "redonda" else 6
    pts = []
    for k in range(n):
        a = k * 2 * math.pi / n + (rng.uniform(-0.15, 0.15) if m["forma"] == "angulosa" else 0)
        rr = r * (rng.uniform(0.95, 1.05) if m["forma"] == "redonda" else rng.uniform(0.75, 1.05))
        pts.append((cx + rr * math.cos(a), cy + rr * 0.8 * math.sin(a)))
    h.poli(pts, COL_ROCA[m["color"]], NEGRO, 3)
    for k in range(m["vetas"]):
        yy = cy - r * 0.3 + k * r * 0.35
        h.linea([(cx - r * 0.6, yy), (cx - r * 0.2, yy + 6), (cx + r * 0.2, yy - 4), (cx + r * 0.6, yy + 4)], BLANCO, 4)
    if m["cristal"]:
        h.poli([(cx + r * 0.25, cy + r * 0.05), (cx + r * 0.42, cy - r * 0.32), (cx + r * 0.6, cy + r * 0.05), (cx + r * 0.42, cy + r * 0.3)],
               (150, 240, 255), BLANCO, 2)


def marte_cuaderno(ms, pagina):
    h = Hoja(W, H, (236, 232, 220))
    for y in range(140, H - 30, 30):
        h.linea([(30, y), (W - 30, y)], (190, 200, 220), 1)
    h.rect(16, 16, W - 16, H - 16, None, TINTA, 3)
    h.texto((W / 2 + 30, 60), "CUADERNO DE MUESTRAS", "cartel", 32, TINTA)
    h.texto((W / 2 + 30, 98), f"Dra. Reyes · página {pagina + 1} de 3", "texto2", 21, TINTA)
    for k, m in enumerate(ms["ejemplos"][pagina * 3:pagina * 3 + 3]):
        y = 220 + k * 210
        roca(h, m, 200, y, 74, 100 * pagina + k)
        if m["pasa"]:
            h.linea([(380, y), (420, y + 40), (500, y - 50)], VERDE, 14)
            h.texto((450, y + 80), "limpia", "texto", 22, VERDE)
        else:
            h.linea([(390, y - 40), (480, y + 40)], ROJO, 14)
            h.linea([(480, y - 40), (390, y + 40)], ROJO, 14)
            h.texto((435, y + 80), "contaminada", "texto", 22, ROJO)
    return h.final()


def marte_ui(ms):
    d = ui_dir("marte")
    for i, m in enumerate(ms["bandeja"]):
        h = Hoja(160, 140, (255, 0, 255))
        roca(h, m, 80, 70, 60, 900 + i)
        transparente(h.final(), os.path.join(d, f"muestra-{i}.png"))


# ================================================================== EGIPTO
PAPIRO = (232, 214, 168)
OCRE = (150, 100, 40)


def egipto_ofrendas(of, mitad):
    h = Hoja(W, H, PAPIRO)
    h.rect(16, 16, W - 16, H - 16, None, OCRE, 5)
    h.texto((W / 2 + 30, 60), "LA MESA DE OFRENDAS", "cartel", 34, TINTA)
    h.texto((W / 2 + 30, 98), "Mitad de " + ("arriba (filas 1 y 2)" if mitad == 0 else "abajo (filas 3 y 4)"), "texto2", 22, TINTA)
    lado, x0, y0 = 120, 75, 200
    filas = range(0, 2) if mitad == 0 else range(2, 4)
    jaula_de = {}
    for j, cel in enumerate(of["jaulas"]):
        for f, c in cel:
            jaula_de[(f, c)] = j
    for i, f in enumerate(filas):
        for c in range(4):
            x, y = x0 + c * lado, y0 + i * lado
            h.rect(x, y, x + lado, y + lado, (240, 226, 186), (190, 160, 110), 1)
    for i, f in enumerate(filas):
        for c in range(4):
            x, y = x0 + c * lado, y0 + i * lado
            j = jaula_de[(f, c)]
            for (df, dc), seg in (((-1, 0), [(x, y), (x + lado, y)]), ((1, 0), [(x, y + lado), (x + lado, y + lado)]),
                                  ((0, -1), [(x, y), (x, y + lado)]), ((0, 1), [(x + lado, y), (x + lado, y + lado)])):
                if jaula_de.get((f + df, c + dc)) != j:
                    h.linea(seg, TINTA, 6)
            if [f, c] == min(of["jaulas"][j]):
                h.texto((x + 10, y + 22), str(of["sumas"][j]), "texto", 30, ROJO, "lm")
                h.texto((x + 12 + 18 * len(str(of["sumas"][j])), y + 22), "+", "texto", 22, ROJO, "lm")
    y = y0 + 2 * lado + 70
    for k, t in enumerate(["En cada fila y en cada columna van", "las ofrendas 1, 2, 3 y 4, sin repetir.", "El número rojo es lo que suman", "las casillas de su recinto."]):
        h.texto((W / 2, y + k * 38), t, "texto2", 23, TINTA)
    return h.final()


def egipto_losa(ta, franja):
    filas = [(0, 1), (2, 3), (4,)][franja]
    h = Hoja(W, H, (196, 180, 150))
    h.rect(16, 16, W - 16, H - 16, None, (110, 90, 60), 5)
    h.texto((W / 2 + 30, 60), "LA LOSA DE LOS NÚMEROS", "cartel", 30, TINTA)
    h.texto((W / 2 + 30, 98), f"Franja {franja + 1} de 3 (filas {', '.join(str(f + 1) for f in filas)})", "texto2", 21, TINTA)
    lado, x0, y0 = 104, 55, 170
    for i, f in enumerate(filas):
        h.texto((x0 - 26, y0 + i * lado + lado / 2), str(f + 1), "texto", 22, TINTA)
        for c in range(5):
            x, y = x0 + c * lado, y0 + i * lado
            h.rect(x + 3, y + 3, x + lado - 3, y + lado - 3, (220, 206, 176), (110, 90, 60), 3)
            h.texto((x + lado / 2, y + lado / 2 + 2), str(ta["rejilla"][f][c]), "cartel", 46, TINTA)
    if franja == 2:
        y = y0 + lado + 80
        for k, t in enumerate(["Tapad con arena números repetidos", "hasta que en ninguna fila ni columna", "se repita un número.",
                               "Dos tapados no pueden tocarse por un lado", "y todo lo que queda a la vista sigue unido."]):
            h.texto((W / 2, y + k * 38), t, "texto2", 22, TINTA)
    return h.final()


# ================================================================== FLORENCIA: cajas del baúl
NOMBRE_PIEZA = {"ornitoptero": "Ornitóptero", "leon": "León mecánico", "laud": "Laúd de plata", "carro": "Carro blindado"}
COL_PIEZA = {"ornitoptero": (186, 120, 60), "leon": (200, 160, 60), "laud": (150, 90, 120), "carro": (90, 120, 90)}


def florencia_caja(bau, nombre):
    h = Hoja(W, H, (238, 222, 186))
    h.rect(16, 16, W - 16, H - 16, None, (120, 80, 40), 5)
    h.texto((W / 2 + 30, 60), "CAJA DE VIAJE", "cartel", 36, (90, 50, 20))
    h.texto((W / 2 + 30, 98), NOMBRE_PIEZA[nombre], "texto", 26, (90, 50, 20))
    lado = 90
    pts = bau["piezas"][nombre]
    w = max(x for x, _ in pts) + 1
    hh = max(y for _, y in pts) + 1
    x0, y0 = (W - w * lado) / 2, 200 + (4 - hh) * lado / 2
    for x, y in pts:
        h.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, COL_PIEZA[nombre], (60, 40, 20), 4)
        h.rect(x0 + x * lado + 10, y0 + y * lado + 10, x0 + (x + 1) * lado - 10, y0 + (y + 1) * lado - 10, None, (255, 240, 200), 1)
    h.texto((W / 2, 640), "Vista desde arriba. Cada cuadro,", "texto2", 22, (90, 50, 20))
    h.texto((W / 2, 676), "un palmo. Se puede girar, pero no", "texto2", 22, (90, 50, 20))
    h.texto((W / 2, 712), "poner del revés.", "texto2", 22, (90, 50, 20))
    return h.final()


# ================================================================== MONTECARLO: manos de póker
PALO = {"picas": ("♠", NEGRO), "corazones": ("♥", ROJO), "diamantes": ("♦", ROJO), "tréboles": ("♣", NEGRO)}
FIG = {11: "J", 12: "Q", 13: "K", 14: "A"}
SIMBOLO_PALO = {"picas": "picas", "corazones": "corazon", "diamantes": "diamante", "tréboles": "trebol"}


def palo(h, nombre, cx, cy, r, col):
    if nombre == "corazones":
        h.disco(cx - r * 0.45, cy - r * 0.2, r * 0.5, col)
        h.disco(cx + r * 0.45, cy - r * 0.2, r * 0.5, col)
        h.poli([(cx - r * 0.92, cy - r * 0.05), (cx + r * 0.92, cy - r * 0.05), (cx, cy + r)], col)
    elif nombre == "diamantes":
        h.poli([(cx, cy - r), (cx + r * 0.7, cy), (cx, cy + r), (cx - r * 0.7, cy)], col)
    elif nombre == "picas":
        h.disco(cx - r * 0.45, cy + r * 0.15, r * 0.5, col)
        h.disco(cx + r * 0.45, cy + r * 0.15, r * 0.5, col)
        h.poli([(cx - r * 0.92, cy + r * 0.05), (cx + r * 0.92, cy + r * 0.05), (cx, cy - r)], col)
        h.poli([(cx, cy + r * 0.2), (cx - r * 0.3, cy + r), (cx + r * 0.3, cy + r)], col)
    else:
        for dx, dy in ((0, -0.45), (-0.45, 0.15), (0.45, 0.15)):
            h.disco(cx + dx * r, cy + dy * r, r * 0.42, col)
        h.poli([(cx, cy), (cx - r * 0.3, cy + r), (cx + r * 0.3, cy + r)], col)


def espia_mano(po, jugador):
    h = Hoja(W, H, (20, 70, 50))
    for y in range(0, H, 6):
        h.linea([(0, y), (W, y)], (24, 78, 56), 2)
    h.rect(16, 16, W - 16, H - 16, None, (220, 190, 110), 4)
    h.texto((W / 2 + 30, 60), "MESA DE PÓKER", "cartel", 36, (240, 220, 160))
    h.texto((W / 2 + 30, 100), "La mano de " + jugador, "texto", 26, (240, 220, 160))
    mano = po["manos"][jugador]
    for k, (v, p) in enumerate(mano):
        x = 60 + k * 104
        y = 260 + (k % 2) * 30
        h.rect(x, y, x + 96, y + 140, BLANCO, NEGRO, 3)
        col = PALO[p][1]
        h.texto((x + 20, y + 24), FIG.get(v, str(v)), "cartel", 28, col)
        palo(h, p, x + 48, y + 86, 26, col)
    for k, t in enumerate(["En la mesa se juega a cinco cartas.", "Mirad bien los palos y los números."]):
        h.texto((W / 2, 560 + k * 40), t, "texto2", 23, (240, 220, 160))
    return h.final()


# ================================================================== PIRATAS: campanadas
PERG = (236, 218, 174)
TINTA_P = (52, 36, 24)


def campana(h, cx, cy, r, col=(200, 150, 50)):
    h.poli([(cx - r * 0.5, cy - r * 0.6), (cx + r * 0.5, cy - r * 0.6), (cx + r * 0.65, cy + r * 0.3), (cx + r, cy + r * 0.55),
            (cx - r, cy + r * 0.55), (cx - r * 0.65, cy + r * 0.3)], col, TINTA_P, 2)
    h.disco(cx, cy + r * 0.7, r * 0.18, col, TINTA_P, 2)
    h.disco(cx, cy - r * 0.68, r * 0.16, None, TINTA_P, 2)


def piratas_guardias(pc):
    h = Hoja(W, H, PERG)
    h.rect(16, 16, W - 16, H - 16, None, TINTA_P, 4)
    h.texto((W / 2 + 30, 60), "LAS GUARDIAS", "cartel", 38, TINTA_P)
    h.texto((W / 2 + 30, 98), "El día de a bordo, en seis guardias", "texto2", 22, TINTA_P)
    cx, cy, R = W / 2, 420, 220
    h.disco(cx, cy, R, (244, 230, 196), TINTA_P, 4)
    for k, (nombre, ini) in enumerate(pc["guardias"]):
        a0 = math.radians(ini * 15 - 90)
        h.linea([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0))], TINTA_P, 3)
        am = math.radians((ini + 2) * 15 - 90)
        h.texto((cx + R * 0.66 * math.cos(am), cy + R * 0.66 * math.sin(am) - 12), nombre, "texto", 22, TINTA_P)
        h.texto((cx + R * 0.66 * math.cos(am), cy + R * 0.66 * math.sin(am) + 14), f"{ini:02d}-{(ini + 4) % 24:02d} h", "texto2", 18, TINTA_P)
    for hh in (0, 6, 12, 18):
        a = math.radians(hh * 15 - 90)
        h.texto((cx + (R + 24) * math.cos(a), cy + (R + 24) * math.sin(a)), f"{hh}h", "texto", 18, TINTA_P)
    h.disco(cx, cy - R * 0.2, 0, None)
    h.texto((W / 2, 720), "Cada guardia dura cuatro horas.", "texto2", 24, TINTA_P)
    return h.final()


def piratas_campanadas():
    h = Hoja(W, H, PERG)
    h.rect(16, 16, W - 16, H - 16, None, TINTA_P, 4)
    h.texto((W / 2 + 30, 60), "LAS CAMPANADAS", "cartel", 38, TINTA_P)
    h.texto((W / 2 + 30, 98), "Así se cuenta el tiempo en cada guardia", "texto2", 22, TINTA_P)
    for k in range(8):
        y = 170 + k * 70
        n = k + 1
        h.texto((70, y), f"{(k + 1) * 30 // 60}h {(k + 1) * 30 % 60:02d}m" if (k + 1) * 30 % 60 else f"{(k + 1) // 2}h", "texto", 20, TINTA_P, "lm")
        for j in range(n):
            campana(h, 210 + j * 46 + (j // 2) * 10, y, 18)
    h.texto((W / 2, 760), "Cada media hora de guardia, una campanada más.", "texto2", 22, TINTA_P)
    h.texto((W / 2, 796), "(a la izquierda, lo que ha pasado desde que empezó)", "texto2", 18, TINTA_P)
    return h.final()


def piratas_diario(pc):
    h = Hoja(W, H, (226, 206, 160))
    for y in range(150, H - 40, 34):
        h.linea([(40, y), (W - 40, y)], (200, 176, 130), 1)
    h.rect(16, 16, W - 16, H - 16, None, TINTA_P, 4)
    h.texto((W / 2 + 30, 60), "DIARIO DE LA CAPITANA", "cartel", 34, TINTA_P)
    h.texto((W / 2 + 30, 98), "Bruma, de su puño y letra", "texto2", 22, TINTA_P)
    for k, t in enumerate(["Frente a la Isla Calavera la marea", "solo deja pasar el bote entre los", "arrecifes un rato. Lo apunté así:"]):
        h.texto((W / 2, 190 + k * 40), t, "texto2", 24, TINTA_P)
    # guardia de la tarde: sol alto
    h.disco(150, 420, 50, (250, 200, 60), TINTA_P, 3)
    for k in range(12):
        a = k * math.pi / 6
        h.linea([(150 + 62 * math.cos(a), 420 + 62 * math.sin(a)), (150 + 80 * math.cos(a), 420 + 80 * math.sin(a))], TINTA_P, 3)
    h.texto((150, 520), "guardia de la", "texto2", 20, TINTA_P)
    h.texto((150, 546), pc["guardia"].lower(), "texto", 24, TINTA_P)
    for j in range(pc["campanadas"]):
        campana(h, 300 + (j % 3) * 80 + (j // 3) * 40, 400 + (j // 3) * 80, 30)
    h.texto((W / 2, 660), "Poned en hora el reloj de bitácora", "texto", 24, TINTA_P)
    h.texto((W / 2, 698), "y la marea os abrirá el paso.", "texto", 24, TINTA_P)
    return h.final()


# ================================================================== JUGUETES: dibujos de los cubos
def dibujo(nombre, lado=300):
    h = Hoja(lado, lado, (250, 244, 226))
    k = lado / 300
    if nombre == "perro":
        h.rect(0, 0, lado, lado, (180, 220, 250))
        h.rect(0, 220 * k, lado, lado, (110, 190, 100))
        h.elip(70 * k, 140 * k, 230 * k, 230 * k, (200, 140, 80), (60, 40, 20), 3)
        h.disco(90 * k, 120 * k, 50 * k, (200, 140, 80), (60, 40, 20), 3)
        h.elip(40 * k, 90 * k, 70 * k, 160 * k, (130, 80, 40), (60, 40, 20), 3)
        h.disco(80 * k, 110 * k, 7 * k, (30, 20, 20))
        h.disco(54 * k, 132 * k, 9 * k, (30, 20, 20))
        for x in (100, 200):
            h.rect(x * k, 210 * k, (x + 20) * k, 250 * k, (200, 140, 80), (60, 40, 20), 3)
        h.linea([(230 * k, 170 * k), (270 * k, 130 * k)], (200, 140, 80), 12 * k)
        h.disco(230 * k, 60 * k, 30 * k, (255, 220, 60))
    elif nombre == "barco":
        h.rect(0, 0, lado, lado, (190, 226, 250))
        h.rect(0, 200 * k, lado, lado, (60, 120, 200))
        h.poli([(60 * k, 190 * k), (240 * k, 190 * k), (210 * k, 240 * k), (90 * k, 240 * k)], (200, 60, 50), (60, 20, 20), 3)
        h.linea([(150 * k, 190 * k), (150 * k, 50 * k)], (60, 40, 20), 6 * k)
        h.poli([(156 * k, 60 * k), (240 * k, 170 * k), (156 * k, 170 * k)], (250, 250, 250), (60, 60, 60), 3)
    elif nombre == "casa":
        h.rect(0, 0, lado, lado, (200, 230, 250))
        h.rect(0, 240 * k, lado, lado, (110, 190, 100))
        h.rect(70 * k, 140 * k, 230 * k, 250 * k, (240, 200, 120), (80, 50, 20), 3)
        h.poli([(50 * k, 145 * k), (150 * k, 60 * k), (250 * k, 145 * k)], (200, 60, 50), (80, 30, 20), 3)
        h.rect(130 * k, 190 * k, 170 * k, 250 * k, (120, 70, 40))
    elif nombre == "sol":
        h.rect(0, 0, lado, lado, (120, 190, 250))
        h.disco(150 * k, 150 * k, 70 * k, (255, 210, 50), (220, 140, 20), 4)
        for i in range(12):
            a = i * math.pi / 6
            h.linea([(150 * k + 85 * k * math.cos(a), 150 * k + 85 * k * math.sin(a)), (150 * k + 125 * k * math.cos(a), 150 * k + 125 * k * math.sin(a))], (255, 190, 40), 8 * k)
    elif nombre == "cohete":
        h.rect(0, 0, lado, lado, (30, 30, 70))
        for i in range(20):
            h.disco((i * 53 % 290) * k, (i * 97 % 290) * k, 3 * k, (255, 255, 230))
        h.poli([(130 * k, 220 * k), (170 * k, 220 * k), (170 * k, 110 * k), (150 * k, 50 * k), (130 * k, 110 * k)], (240, 240, 240), (60, 60, 60), 3)
        h.poli([(130 * k, 220 * k), (100 * k, 250 * k), (130 * k, 170 * k)], (220, 60, 50))
        h.poli([(170 * k, 220 * k), (200 * k, 250 * k), (170 * k, 170 * k)], (220, 60, 50))
        h.disco(150 * k, 140 * k, 14 * k, (120, 200, 250), (60, 60, 60), 3)
    else:
        h.rect(0, 0, lado, lado, (200, 236, 250))
        h.rect(0, 240 * k, lado, lado, (120, 200, 100))
        h.rect(135 * k, 160 * k, 165 * k, 250 * k, (120, 80, 40))
        h.disco(150 * k, 120 * k, 80 * k, (60, 160, 70), (30, 90, 40), 3)
        for x, y in ((120, 100), (180, 130), (150, 80)):
            h.disco(x * k, y * k, 9 * k, (220, 40, 40))
    return h.final()


def juguetes_carta(cu):
    h = Hoja(W, H, (250, 244, 226))
    h.rect(16, 16, W - 16, H - 16, None, (90, 100, 160), 4)
    h.texto((W / 2 + 30, 60), "EL DIBUJO DE LEO", "cartel", 36, (60, 70, 140))
    h.texto((W / 2 + 30, 98), "En la tapa de la caja de cubos", "texto2", 22, (60, 70, 140))
    d = dibujo(cu["objetivo"], 420)
    h.im.paste(d.resize((840, 840)), (int((W - 420) / 2 * 2), 300))
    h.texto((W / 2, 740), "¡Mi perro Trufo! Leo, 5 años", "texto", 26, (60, 70, 140))
    return h.final()


def juguetes_ui(cu):
    d = ui_dir("juguetes")
    for nombre in cu["dibujos"]:
        im = dibujo(nombre, 240)
        for q, (x, y) in enumerate(((0, 0), (120, 0), (0, 120), (120, 120))):
            im.crop((x, y, x + 120, y + 120)).save(os.path.join(d, f"cubo-{nombre}-{q}.png"))


# ================================================================== EL FARO: bahía, sombras y destellos
FARO_DIR = os.path.join(RAIZ, "juegos", "el-faro")
NIEBLA = (226, 228, 222)
TINTA_F = (30, 46, 60)


def guardar_faro(carta, im, semilla):
    d = os.path.join(FARO_DIR, "arte")
    os.makedirs(d, exist_ok=True)
    ruido(im, semilla).save(os.path.join(d, f"{carta}.png"))


def faro_bahia(ba, mitad):
    h = Hoja(W, H, NIEBLA)
    h.rect(16, 16, W - 16, H - 16, None, TINTA_F, 4)
    h.texto((W / 2 + 30, 60), "PLANO DE LA BAHÍA", "cartel", 36, TINTA_F)
    h.texto((W / 2 + 30, 98), "Hoja " + ("1 de 2 (filas A a C)" if mitad == 0 else "2 de 2 (filas D a F)"), "texto2", 22, TINTA_F)
    n, lado, x0, y0 = ba["n"], 84, 62, 170
    pistas = {(f, c): v for f, c, v in ba["pistas"]}
    filas = range(0, 3) if mitad == 0 else range(3, 6)
    for c in range(n):
        h.texto((x0 + c * lado + lado / 2, y0 - 20), str(c + 1), "texto", 20, TINTA_F)
    for i, f in enumerate(filas):
        h.texto((x0 - 22, y0 + i * lado + lado / 2), "ABCDEF"[f], "texto", 20, TINTA_F)
        for c in range(n):
            x, y = x0 + c * lado, y0 + i * lado
            h.rect(x, y, x + lado, y + lado, (196, 214, 222), (120, 150, 170), 2)
            if (f, c) in pistas:
                h.disco(x + lado / 2, y + lado / 2, 28, (230, 200, 140), TINTA_F, 3)
                h.texto((x + lado / 2, y + lado / 2 + 2), str(pistas[(f, c)]), "cartel", 30, TINTA_F)
    if mitad == 1:
        y = y0 + 3 * lado + 50
        for k, t in enumerate(["Cada islote tiene un número: cuántas casillas", "mide. Dos islotes no se tocan por un lado.",
                               "El mar va todo unido y no forma charcos", "de 2 × 2 casillas: por ahí pasa el barco."]):
            h.texto((W / 2, y + k * 36), t, "texto2", 21, TINTA_F)
    else:
        h.texto((W / 2, y0 + 3 * lado + 60), "(Anselmo dibujó la bahía en dos hojas)", "texto2", 21, TINTA_F)
    return h.final()


def faro_sombra(so):
    import instancias_ampliacion as IA
    h = Hoja(W, H, (60, 64, 70))
    h.rect(16, 16, W - 16, H - 16, None, (200, 180, 120), 4)
    h.texto((W / 2 + 30, 60), "LA SOMBRA EN LA PARED", "cartel", 32, (240, 226, 190))
    h.texto((W / 2 + 30, 98), "Cuarto de guardia del faro", "texto2", 22, (220, 210, 180))
    pared = Image.new("RGB", (360, 160), (232, 220, 186))
    m = IA.sombra(so["solucion"])
    a = np.asarray(pared).copy()
    a[m] = (40, 34, 30)
    pared = Image.fromarray(a).resize((540, 240))
    h.im.paste(pared.resize((1080, 480)), (90, 340))
    h.linea([(45, 410), (585, 410)], (40, 34, 30), 3)
    for k, t in enumerate(["Anselmo pintó en la pared la sombra", "de tres de sus cosas, puestas en fila", "delante de la lámpara de la mesa."]):
        h.texto((W / 2, 520 + k * 40), t, "texto2", 23, (240, 226, 190))
    return h.final()


def faro_estante(so):
    import instancias_ampliacion as IA
    h = Hoja(W, H, (120, 86, 56))
    h.rect(16, 16, W - 16, H - 16, None, (60, 40, 24), 5)
    h.texto((W / 2 + 30, 60), "EL ESTANTE DEL FARERO", "cartel", 32, (250, 236, 200))
    h.texto((W / 2 + 30, 98), "Las cosas de Anselmo", "texto2", 22, (240, 226, 190))
    cols = [(210, 160, 60), (90, 96, 110), (70, 140, 90), (200, 200, 210), (236, 236, 230), (180, 140, 60), (200, 150, 50), (150, 120, 60)]
    for k, nombre in enumerate(so["objetos"]):
        fila, col = divmod(k, 2)
        x, y = 70 + col * 270, 150 + fila * 165
        h.rect(x - 10, y + 128, x + 230, y + 140, (80, 54, 32))
        mask = IA.silueta(nombre, 0).crop((0, 0, 120, 160))
        capa = Image.new("RGB", mask.size, cols[k])
        h.im.paste(capa.resize((240, 320)), (int((x + 50) * 2), int((y - 30) * 2)), mask.resize((240, 320)))
        h.texto((x + 180, y + 60), str(k + 1), "cartel", 30, (250, 236, 200))
    return h.final()


def faro_almanaque(de):
    h = Hoja(W, H, (236, 232, 214))
    h.rect(16, 16, W - 16, H - 16, None, TINTA_F, 4)
    h.texto((W / 2 + 30, 60), "ALMANAQUE DE FAROS", "cartel", 34, TINTA_F)
    h.texto((W / 2 + 30, 98), "Costa norte · edición de 1923", "texto2", 22, TINTA_F)
    for k, (faro, elems) in enumerate(de["faros"].items()):
        y = 180 + k * 112
        h.texto((50, y), faro, "texto", 26, TINTA_F, "lm")
        cuenta = {e: elems.count(e) for e in ("destello", "largo")}
        txt = " y ".join(f"{n} {e}{'s' if n > 1 else ''}" for e, n in cuenta.items() if n)
        orden = ", ".join(elems)
        h.texto((50, y + 36), "en orden: " + orden, "texto2", 20, TINTA_F, "lm")
        h.linea([(40, y + 66), (W - 40, y + 66)], (190, 186, 170), 1)
    h.texto((W / 2, 780), "Cada grupo se repite cada 12 segundos.", "texto2", 22, TINTA_F)
    return h.final()


def faro_leyenda(de):
    h = Hoja(W, H, (244, 236, 210))
    h.rect(16, 16, W - 16, H - 16, None, TINTA_F, 4)
    h.texto((W / 2 + 30, 60), "NOTA DE ANSELMO", "cartel", 36, TINTA_F)
    h.texto((W / 2 + 30, 98), "Cómo se lee el almanaque", "texto2", 22, TINTA_F)
    lineas = ["Destello: 1 segundo de luz.", "Largo: 2 segundos de luz.", "Después de cada uno, 1 segundo oscuro.",
              "El grupo empieza en el segundo 1", "y el resto, hasta 12, va a oscuras."]
    for k, t in enumerate(lineas):
        h.texto((W / 2, 170 + k * 40), t, "texto", 23, TINTA_F)
    h.texto((W / 2, 420), "Ejemplo: Punta Gaviota (destello, destello)", "texto2", 21, TINTA_F)
    lado = 42
    x0 = (W - 12 * lado) / 2
    for s, v in enumerate(de["patrones"]["Punta Gaviota"]):
        h.rect(x0 + s * lado, 460, x0 + (s + 1) * lado, 520, (255, 220, 90) if v == "1" else (40, 46, 60), TINTA_F, 2)
        h.texto((x0 + s * lado + lado / 2, 540), str(s + 1), "texto2", 16, TINTA_F)
    h.texto((W / 2, 620), "«Si el capitán ve otra luz,", "texto", 24, TINTA_F)
    h.texto((W / 2, 656), "creerá que es otro faro.»", "texto", 24, TINTA_F)
    return h.final()


def faro_ui(so):
    import instancias_ampliacion as IA
    d = os.path.join(FARO_DIR, "img", "ui")
    os.makedirs(d, exist_ok=True)
    cols = [(210, 160, 60), (90, 96, 110), (70, 140, 90), (200, 200, 210), (236, 236, 230), (180, 140, 60), (200, 150, 50), (150, 120, 60)]
    for k, nombre in enumerate(so["objetos"]):
        mask = IA.silueta(nombre, 0).crop((0, 0, 120, 160))
        capa = Image.new("RGBA", mask.size, cols[k] + (255,))
        capa.putalpha(mask)
        capa.save(os.path.join(d, f"obj-{nombre}.png"))
        sm = Image.new("RGBA", mask.size, (20, 18, 16, 255))
        sm.putalpha(mask)
        sm.save(os.path.join(d, f"sombra-{nombre}.png"))


# ================================================================== datos de los minijuegos nuevos
DATOS = {
    ("marte", "74-circuito.js"): lambda i: {"interruptores": list("ABCDE"), "solucion": i["marte_circuito"]["solucion"],
                                            "salidas": i["marte_circuito"]["salidas"], "quiere": i["marte_circuito"]["quiere"]},
    ("marte", "86-analizador.js"): lambda i: {"n": len(i["marte_muestras"]["bandeja"]), "solucion": i["marte_muestras"]["solucion"]},
    ("egipto", "50-ofrendas.js"): lambda i: {"solucion": i["egipto_ofrendas"]["solucion"]},
    ("egipto", "42-losa.js"): lambda i: {"tachadas": i["egipto_tachar"]["tachadas"]},
    ("florencia", "46-baul.js"): lambda i: {"ancho": i["florencia_baul"]["ancho"], "alto": i["florencia_baul"]["alto"], "piezas": i["florencia_baul"]["piezas"]},
    ("espia", "36-poker.js"): lambda i: {"jugadores": i["espia_poker"]["jugadores"], "orden": i["espia_poker"]["orden"], "ranking": i["espia_poker"]["ranking"]},
    ("piratas", "61-reloj.js"): lambda i: {"hora": i["piratas_campanas"]["hora"]},
    ("juguetes", "64-cubos.js"): lambda i: {k: i["juguetes_cubos"][k] for k in ("dibujos", "caras", "objetivo", "inicial")},
    ("@faro", "45-bahia.js"): lambda i: {"n": i["faro_bahia"]["n"], "tierra": i["faro_bahia"]["tierra"]},
    ("@faro", "55-sombras.js"): lambda i: {k: i["faro_sombras"][k] for k in ("objetos", "solucion")},
    ("@faro", "65-destellos.js"): lambda i: {"solucion": i["faro_destellos"]["solucion"]},
}


def inyectar(i):
    for (juego, js), f in DATOS.items():
        ruta = os.path.join(FARO_DIR if juego == "@faro" else os.path.join(RAIZ, "juegos", "aventuras-ca", juego), "minijuegos", js)
        if not os.path.exists(ruta):
            continue
        s = open(ruta, encoding="utf-8").read()
        a, b = s.index("/*DATOS*/") + len("/*DATOS*/"), s.index("/*FIN*/")
        s = s[:a] + json.dumps(f(i), ensure_ascii=False, separators=(", ", ": ")) + s[b:]
        open(ruta, "w", encoding="utf-8", newline="\n").write(s)


def main():
    i = inst()
    c = i["marte_circuito"]
    for carta, nombre in (("75", "motor"), ("76", "alarma"), ("78", "ventilacion")):
        guardar("marte", carta, marte_salida(nombre, c["salidas"][nombre]), int(carta))
    guardar("marte", "81", marte_leyenda(c), 81)
    for k, carta in enumerate(("87", "89", "90")):
        guardar("marte", carta, marte_cuaderno(i["marte_muestras"], k), int(carta))
    marte_ui(i["marte_muestras"])
    guardar("egipto", "38", egipto_ofrendas(i["egipto_ofrendas"], 0), 38)
    guardar("egipto", "51", egipto_ofrendas(i["egipto_ofrendas"], 1), 51)
    for k, carta in enumerate(("45", "48", "49")):
        guardar("egipto", carta, egipto_losa(i["egipto_tachar"], k), int(carta))
    for carta, nombre in zip(("47", "48", "49", "50"), ("ornitoptero", "leon", "laud", "carro")):
        guardar("florencia", carta, florencia_caja(i["florencia_baul"], nombre), int(carta))
    for carta, jug in zip(("37", "39", "41", "42"), i["espia_poker"]["jugadores"]):
        guardar("espia", carta, espia_mano(i["espia_poker"], jug), int(carta))
    guardar("piratas", "63", piratas_guardias(i["piratas_campanas"]), 63)
    guardar("piratas", "65", piratas_campanadas(), 65)
    guardar("piratas", "67", piratas_diario(i["piratas_campanas"]), 67)
    guardar("juguetes", "67", juguetes_carta(i["juguetes_cubos"]), 67)
    juguetes_ui(i["juguetes_cubos"])
    guardar_faro("46", faro_bahia(i["faro_bahia"], 0), 46)
    guardar_faro("47", faro_bahia(i["faro_bahia"], 1), 47)
    guardar_faro("56", faro_sombra(i["faro_sombras"]), 56)
    guardar_faro("57", faro_estante(i["faro_sombras"]), 57)
    guardar_faro("66", faro_almanaque(i["faro_destellos"]), 66)
    guardar_faro("67", faro_leyenda(i["faro_destellos"]), 67)
    faro_ui(i["faro_sombras"])
    inyectar(i)
    print("láminas de la ampliación escritas")


if __name__ == "__main__":
    main()

"""Láminas de «El Faro de Cabo Niebla» (versión de 60 cartas): todo se dibuja por código a partir de herramientas/instancias_faro.json.

  - 16 reloj parado y su etiqueta · 18 mensaje de banderas · 19+21 tabla de banderas · 41 mapa náutico · 43 brújula · 45 versos del radioaficionado
  - 42+49 tabla morse · 53 aviso de la sirena · 54+55 plano de la bahía · 59 versos de Anselmo · 37 sombra · 39 estante · 33 nota de las sombras
  - 26 nota del almanaque · 61+63 almanaque de faros · 66 y 67 cuaderno de relevos · 70+71 plano del desván · 75 papel del nido · 79 cuaderno del óptico
  - 86 orden de arranque · 87 tabla de válvulas.
Además copia en cada minijuego (entre /*DATOS*/ y /*FIN*/) los datos de su instancia y escribe las imágenes de los objetos de las sombras.
Uso (desde la raíz del repo):  python herramientas/faro.py [carpeta_juego]
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oeste import Hoja, fuente  # noqa: E402
from mosaicos import cortar  # noqa: E402
import instancias_ampliacion as IA  # noqa: E402

W, H = 630, 882
NIEBLA = (226, 228, 222)
TINTA = (30, 46, 60)
PAPEL = (240, 234, 214)
AMBAR = (214, 150, 40)
AZUL = (52, 98, 140)
BORDE = (120, 150, 170)
COL_B = {"rojo": (204, 44, 44), "azul": (44, 92, 184), "amarillo": (244, 202, 44), "blanco": (250, 250, 244), "negro": (30, 30, 36)}
OBJ_COL = [(210, 160, 60), (90, 96, 110), (70, 140, 90), (200, 200, 210), (236, 236, 230), (180, 140, 60), (200, 150, 50), (150, 120, 60)]


def _inst():
    return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_faro.json"), encoding="utf-8"))


def ruido(im, semilla, fuerza=2.5):
    a = np.asarray(im).astype(np.int16)
    rng = np.random.default_rng(semilla)
    a = a + rng.normal(0, fuerza, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def papel(titulo, sub=None, col=TINTA, w=W, h=H, fondo=NIEBLA, alto_total=None):
    p = Hoja(w, alto_total or h, fondo)
    p.rect(16, 16, w - 16, (alto_total or h) - 16, None, col, 4)
    p.texto((w / 2 + 30, 60), titulo, "cartel", 34, col)
    if sub:
        p.texto((w / 2 + 30, 98), sub, "texto2", 22, col)
    return p


def parrafo(h, x, y, ancho, txt, tipo="texto2", tam=22, color=TINTA, inter=1.4, ancla="l"):
    """Escribe un párrafo con saltos de línea automáticos; devuelve la y siguiente."""
    f = fuente(tipo, tam)
    linea = ""
    for palabra in txt.split():
        prueba = (linea + " " + palabra).strip()
        if f.getlength(prueba) / 2 > ancho and linea:
            h.texto((x if ancla == "l" else x + ancho / 2, y), linea, tipo, tam, color, "lm" if ancla == "l" else "mm")
            y += tam * inter
            linea = palabra
        else:
            linea = prueba
    if linea:
        h.texto((x if ancla == "l" else x + ancho / 2, y), linea, tipo, tam, color, "lm" if ancla == "l" else "mm")
        y += tam * inter
    return y


def versos(p, lineas, y0=200, paso=44, tam=22, x=W / 2, color=TINTA, tipo="texto2"):
    for k, v in enumerate(lineas):
        p.texto((x, y0 + k * paso), v, tipo, tam, color)


def flecha(p, a, b, color, ancho=4, punta=14):
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p.linea([a, (b[0] - math.cos(ang) * punta * 0.6, b[1] - math.sin(ang) * punta * 0.6)], color, ancho)
    p.poli([b, (b[0] - punta * math.cos(ang - 0.45), b[1] - punta * math.sin(ang - 0.45)), (b[0] - punta * math.cos(ang + 0.45), b[1] - punta * math.sin(ang + 0.45))], color)


# ------------------------------------------------------------------ banderas
def bandera(h, x, y, w, hg, spec):
    c1, c2 = COL_B[spec["c1"]], COL_B[spec["c2"]]
    p = spec["patron"]
    o = (30, 30, 36)
    if p == "mitad_v":
        h.rect(x, y, x + w / 2, y + hg, c1)
        h.rect(x + w / 2, y, x + w, y + hg, c2)
    elif p == "mitad_h":
        h.rect(x, y, x + w, y + hg / 2, c1)
        h.rect(x, y + hg / 2, x + w, y + hg, c2)
    elif p == "diagonal":
        h.rect(x, y, x + w, y + hg, c2)
        h.poli([(x, y), (x + w, y), (x, y + hg)], c1)
    elif p == "cruz":
        h.rect(x, y, x + w, y + hg, c1)
        h.rect(x + w * 0.4, y, x + w * 0.6, y + hg, c2)
        h.rect(x, y + hg * 0.38, x + w, y + hg * 0.62, c2)
    elif p == "aspa":
        h.rect(x, y, x + w, y + hg, c1)
        k = 0.16
        h.poli([(x, y), (x + w * k, y), (x + w, y + hg), (x + w * (1 - k), y + hg)], c2)
        h.poli([(x + w, y), (x + w * (1 - k), y), (x, y + hg), (x + w * k, y + hg)], c2)
    elif p == "marco":
        h.rect(x, y, x + w, y + hg, c1)
        h.rect(x + w * 0.2, y + hg * 0.2, x + w * 0.8, y + hg * 0.8, c2)
    elif p == "disco":
        h.rect(x, y, x + w, y + hg, c1)
        h.disco(x + w / 2, y + hg / 2, hg * 0.3, c2)
    elif p == "franjas_v":
        for i in range(3):
            h.rect(x + i * w / 3, y, x + (i + 1) * w / 3, y + hg, c2 if i == 1 else c1)
    elif p == "franjas_h":
        for i in range(3):
            h.rect(x, y + i * hg / 3, x + w, y + (i + 1) * hg / 3, c2 if i == 1 else c1)
    elif p == "cuartos":
        h.rect(x, y, x + w, y + hg, c1)
        h.rect(x + w / 2, y, x + w, y + hg / 2, c2)
        h.rect(x, y + hg / 2, x + w / 2, y + hg, c2)
    else:  # triangulo
        h.rect(x, y, x + w, y + hg, c2)
        h.poli([(x, y), (x + w * 0.6, y + hg / 2), (x, y + hg)], c1)
    h.rect(x, y, x + w, y + hg, None, o, 3)


def carta_mensaje_banderas(inst):
    b = inst["banderas"]
    h = papel("EL MENSAJE DEL ARMARIO", "Seis banderas, de izquierda a derecha", fondo=(214, 226, 234))
    h.linea([(60, 220), (W - 60, 220)], (90, 70, 50), 5)
    cols = 2
    for k, ch in enumerate(b["palabra"]):
        fila, col = divmod(k, 3)
        x = 70 + col * 180
        y = 250 + fila * 230
        h.linea([(x + 4, y - 30), (x + 4, y + 150)], (110, 84, 56), 5)
        bandera(h, x + 6, y - 30, 130, 90, b["banderas"][ch])
        h.texto((x + 70, y + 100), str(k + 1), "cartel", 28, TINTA)
    h.texto((W / 2, 745), "Las colgó Anselmo en el armario del recibidor.", "texto2", 21, TINTA)
    h.texto((W / 2, 780), "Cada bandera es una letra.", "texto2", 21, TINTA)
    return h.final()


def tabla_banderas(inst):
    b = inst["banderas"]["banderas"]
    h = papel("TABLA DE BANDERAS", None, alto_total=H * 2, fondo=(232, 238, 240))
    h.texto((W / 2 + 30, 98), "Código de señales de Cabo Niebla", "texto2", 22, TINTA)
    letras = [chr(65 + i) for i in range(26)]
    for k, ch in enumerate(letras):
        mitad, i = divmod(k, 13)
        fila, col = divmod(i, 3)
        x = 56 + col * 190
        y = (150 if mitad == 0 else H + 80) + fila * 138
        bandera(h, x, y, 110, 74, b[ch])
        h.texto((x + 148, y + 38), ch, "cartel", 40, TINTA)
    h.texto((W / 2, H + 80 + 5 * 138 + 20), "(la tabla sigue en la otra hoja)" if False else "Anselmo la dibujó en dos hojas", "texto2", 20, TINTA)
    return h.final()


# ------------------------------------------------------------------ 16 reloj parado
def carta_reloj(inst):
    pu = inst["puerta"]
    h = papel("EL RELOJ DEL RECIBIDOR", "Se paró cuando se fue la luz", fondo=(228, 222, 204))
    cx, cy, r = W / 2, 330, 150
    h.disco(cx, cy, r + 14, (110, 76, 44), (50, 32, 20), 4)
    h.disco(cx, cy, r, (250, 246, 232), (50, 32, 20), 4)
    for i in range(60):
        a = math.radians(i * 6 - 90)
        L = 16 if i % 5 == 0 else 6
        h.linea([(cx + (r - 6) * math.cos(a), cy + (r - 6) * math.sin(a)), (cx + (r - 6 - L) * math.cos(a), cy + (r - 6 - L) * math.sin(a))], TINTA, 3 if i % 5 == 0 else 1.5)
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        h.texto((cx + (r - 38) * math.cos(a), cy + (r - 38) * math.sin(a)), str(n), "texto", 24, TINTA)
    hh, mm = pu["parado"]
    am = math.radians(mm * 6 - 90)
    ah = math.radians((hh % 12) * 30 + mm * 0.5 - 90)
    h.linea([(cx, cy), (cx + (r - 30) * math.cos(am), cy + (r - 30) * math.sin(am))], TINTA, 6)
    h.linea([(cx, cy), (cx + (r - 70) * math.cos(ah), cy + (r - 70) * math.sin(ah))], TINTA, 10)
    h.disco(cx, cy, 9, (160, 40, 30))
    h.rect(70, 535, W - 70, 790, (250, 244, 224), (140, 120, 90), 3)
    h.texto((W / 2, 566), "ETIQUETA DEL RELOJERO", "cartel", 24, (120, 50, 40))
    ini = pu["inicio"]
    parrafo(h, 96, 604, W - 192, f"Lo puse en hora a las {ini[0]}:{ini[1]:02d} del mediodía, en punto. Atrasa {pu['atraso']} minutos cada hora.", tam=21)
    e = pu["ejemplo"]
    parrafo(h, 96, 690, W - 192, f"Ejemplo: cuando marca las {e[0]}:{e[1]:02d}, son las {e[2]}:{e[3]:02d}.", "texto", 21, (90, 40, 30))
    parrafo(h, 96, 745, W - 192, "(Se paró de golpe: la hora real es otra.)", tam=19)
    return h.final()


# ------------------------------------------------------------------ 41 mapa, 43 brújula, 45 versos (radio)
def carta_mapa(inst):
    ra = inst["radio"]
    h = papel("CARTA NÁUTICA", "Canal de Cabo Niebla", fondo=(188, 214, 226))
    rng = np.random.default_rng(41)
    h.rect(40, 150, W - 40, 690, (172, 204, 220), (90, 120, 140), 3)
    for x0, y0, rx, ry in ((130, 250, 52, 34), (430, 220, 60, 38), (300, 420, 44, 30), (170, 560, 56, 40), (470, 560, 50, 34)):
        h.elip(x0 - rx, y0 - ry, x0 + rx, y0 + ry, (220, 200, 150), (120, 100, 60), 3)
    for k, y in enumerate(range(190, 680, 46)):
        h.linea([(60, y), (W - 60, y + 6)], (150, 186, 206), 1)
    pos_r = [(230, 330), (360, 300), (520, 460)]
    pos_v = [(110, 420), (350, 560)]
    for (x, y), n in zip(pos_r, ra["rojas"]):
        h.disco(x, y, 24, COL_B["rojo"], TINTA, 3)
        h.texto((x, y + 1), str(n), "cartel", 26, (255, 255, 255))
    for (x, y), n in zip(pos_v, ra["verdes"]):
        h.disco(x, y, 24, (60, 160, 84), TINTA, 3)
        h.texto((x, y + 1), str(n), "cartel", 26, (255, 255, 255))
    h.texto((W / 2, 730), "Boyas del canal. Cabo Niebla, al norte.", "texto2", 21, TINTA)
    h.texto((W / 2, 765), "Emisora del faro: ochenta y algo.", "texto2", 21, TINTA)
    return h.final()


def carta_brujula(inst):
    ra = inst["radio"]
    h = papel("LA BRÚJULA ROTA", "Sobre la mesa de la radio", fondo=(226, 218, 196))
    cx, cy, r = W / 2, 400, 200
    h.disco(cx, cy, r + 16, (170, 124, 60), (70, 46, 20), 4)
    h.disco(cx, cy, r, (246, 240, 222), (70, 46, 20), 3)
    for i, nombre in enumerate(ra["vientos"]):
        a = math.radians(i * 45 - 90)
        h.linea([(cx + (r - 28) * math.cos(a), cy + (r - 28) * math.sin(a)), (cx + r * math.cos(a), cy + r * math.sin(a))], TINTA, 4)
        h.texto((cx + (r - 54) * math.cos(a), cy + (r - 54) * math.sin(a)), nombre, "texto", 22, TINTA)
        h.disco(cx + (r - 98) * math.cos(a), cy + (r - 98) * math.sin(a), 20, (255, 224, 150), (150, 100, 30), 3)
        h.texto((cx + (r - 98) * math.cos(a), cy + (r - 98) * math.sin(a) + 1), str(i), "cartel", 22, (110, 50, 20))
    a = math.radians(ra["mostrado"] * 45 - 90)
    h.poli([(cx + 88 * math.cos(a), cy + 88 * math.sin(a)), (cx + 14 * math.cos(a + 1.57), cy + 14 * math.sin(a + 1.57)),
            (cx + 14 * math.cos(a - 1.57), cy + 14 * math.sin(a - 1.57))], (190, 40, 36), TINTA, 2)
    h.disco(cx, cy, 10, TINTA)
    h.texto((W / 2, 685), "«Siete vientos, siete décimas»", "texto", 25, TINTA)
    h.texto((W / 2, 725), "(rotulado por Anselmo en la tapa)", "texto2", 19, TINTA)
    return h.final()


def carta_versos_radio(inst):
    h = papel("EL RADIOAFICIONADO", "Versos pegados en la radio", fondo=(242, 236, 214))
    L = ["Ochenta marca la costa;", "al ochenta, suma lo que ves en rojo.", "Lo verde es de otro canal:", "no lo mires, no lo cuentes.", "",
         "Las décimas, en la brújula;", "pero su aguja se pasó:", "dos vientos a la derecha", "(como las agujas del reloj).", "Cuenta hacia atrás dos vientos",
         "y lee la décima que te dé."]
    versos(h, L, 190, 46, 23)
    return h.final()


# ------------------------------------------------------------------ morse
def tabla_morse(inst):
    from instancias_faro import MORSE
    h = papel("TABLA MORSE", None, alto_total=H * 2, fondo=(236, 236, 228))
    h.texto((W / 2 + 30, 98), "Punto = destello corto · Raya = destello largo", "texto2", 21, TINTA)
    for k in range(26):
        ch = chr(65 + k)
        mitad, i = divmod(k, 13)
        col, fila = divmod(i, 7)
        x = 70 + col * 290
        y = (180 if mitad == 0 else H + 90) + fila * 96
        h.texto((x, y), ch, "cartel", 46, TINTA, "lm")
        xx = x + 66
        for s in MORSE[ch]:
            if s == ".":
                h.disco(xx + 9, y, 9, AZUL)
                xx += 30
            else:
                h.rect(xx, y - 8, xx + 42, y + 8, AMBAR, TINTA, 2)
                xx += 56
    h.texto((W / 2, H + 90 + 7 * 96 + 5), "Anselmo la copió en dos hojas", "texto2", 20, TINTA)
    return h.final()


def carta_sirena(inst):
    h = papel("EL AVISO DE LA SIRENA", "Pegado en la ventana redonda", fondo=(240, 230, 212))
    L = ["El carguero tiene averiada", "la sirena de niebla,", "y la avisa con la lámpara roja.", "", "Lo rojo es una alarma,", "no es una letra.", "",
         "Solo lo blanco habla;", "lo rojo, en cambio, estorba.", "", "Y entre letra y letra", "se hace una pausa larga."]
    versos(h, L, 190, 44, 23)
    h.disco(W / 2 - 40, 760, 22, COL_B["rojo"], TINTA, 3)
    h.disco(W / 2 + 40, 760, 22, (252, 252, 244), TINTA, 3)
    return h.final()


# ------------------------------------------------------------------ bahía (Nurikabe)
def plano_bahia(inst):
    ba = inst["bahia"]
    n, lado = ba["n"], 78
    x0 = (W - n * lado) / 2 + 12
    h = papel("PLANO DE LA BAHÍA", None, alto_total=H * 2, fondo=NIEBLA)
    h.texto((W / 2 + 30, 98), "Los islotes de Cabo Niebla", "texto2", 22, TINTA)
    h.texto((W / 2, 175), "Anselmo dibujó la bahía en dos hojas.", "texto2", 21, TINTA)
    h.texto((W / 2, 215), "Cada círculo es una casilla de islote", "texto2", 21, TINTA)
    h.texto((W / 2, 250), "y el número, cuántas casillas mide.", "texto2", 21, TINTA)
    pistas = {(f, c): v for f, c, v in ba["pistas"]}
    y0 = 470
    for c in range(n):
        h.texto((x0 + c * lado + lado / 2, y0 - 18), str(c + 1), "texto", 20, TINTA)
    for f in range(n):
        y = y0 + f * lado if f < 4 else H + 70 + (f - 4) * lado
        h.texto((x0 - 22, y + lado / 2), "ABCDEFG"[f], "texto", 20, TINTA)
        for c in range(n):
            x = x0 + c * lado
            h.rect(x, y, x + lado, y + lado, (196, 214, 222), BORDE, 2)
            if (f, c) in pistas:
                h.disco(x + lado / 2, y + lado / 2, 27, (230, 200, 140), TINTA, 3)
                h.texto((x + lado / 2, y + lado / 2 + 2), str(pistas[(f, c)]), "cartel", 30, TINTA)
    return h.final()


def versos_bahia(inst):
    h = papel("LOS VERSOS DE ANSELMO", "Para trazar el canal", fondo=(242, 236, 214))
    L = ["Cada islote lleva un número:", "tantas casillas, y ni una más.", "Dos islotes no se tocan", "por ningún lado.", "",
         "El mar es todo un mismo mar:", "ninguna casilla de agua", "se queda sola, sin camino.", "", "Y donde el agua se junta",
         "en un cuadrado de cuatro,", "se forma un charco que atasca", "las quillas del carguero.", "Evítalo siempre."]
    versos(h, L, 180, 44, 22)
    return h.final()


# ------------------------------------------------------------------ sombras
def carta_sombra(inst):
    so = inst["sombras"]
    h = Hoja(W, H, (60, 64, 70))
    h.rect(16, 16, W - 16, H - 16, None, (200, 180, 120), 4)
    h.texto((W / 2 + 30, 60), "LA SOMBRA EN LA PARED", "cartel", 32, (240, 226, 190))
    h.texto((W / 2 + 30, 98), "Cuarto de guardia del faro", "texto2", 22, (220, 210, 180))
    from instancias_faro import sombra4
    m = sombra4(so["solucion"])
    a = np.full((160, 480, 3), (232, 220, 186), np.uint8)
    a[m] = (40, 34, 30)
    pared = Image.fromarray(a).resize((1056, 352))
    h.im.paste(pared, (102, 340))
    h.linea([(51, 410), (579, 410)], (40, 34, 30), 3)
    return h.final()


def carta_estante(inst):
    so = inst["sombras"]
    h = Hoja(W, H, (120, 86, 56))
    h.rect(16, 16, W - 16, H - 16, None, (60, 40, 24), 5)
    h.texto((W / 2 + 30, 60), "EL ESTANTE DEL FARERO", "cartel", 32, (250, 236, 200))
    h.texto((W / 2 + 30, 98), "Las cosas de Anselmo", "texto2", 22, (240, 226, 190))
    for k, nombre in enumerate(so["objetos"]):
        fila, col = divmod(k, 2)
        x, y = 70 + col * 270, 140 + fila * 175
        h.rect(x - 10, y + 138, x + 230, y + 150, (80, 54, 32))
        mask = IA.silueta(nombre, 0).crop((0, 0, 120, 160))
        capa = Image.new("RGB", mask.size, OBJ_COL[k])
        h.im.paste(capa.resize((240, 320)), (int((x + 50) * 2), int((y - 20) * 2)), mask.resize((240, 320)))
        h.texto((x + 180, y + 60), str(k + 1), "cartel", 30, (250, 236, 200))
    return h.final()


def nota_sombras(inst):
    h = papel("LA NOTA DE ANSELMO", "Pegada bajo la lámpara", fondo=(244, 236, 210))
    L = ["En la pared dejé pintada", "la sombra de cuatro de mis cosas.", "", "Las puse en fila, sobre la mesa,", "de izquierda a derecha,",
         "delante de la lámpara.", "", "Ninguna se repite.", "Y cada una ocupa su hueco,", "sin pisar el de la vecina."]
    versos(h, L, 190, 46, 23)
    return h.final()


# ------------------------------------------------------------------ destellos
def nota_almanaque(inst):
    de = inst["destellos"]
    h = papel("NOTA DE ANSELMO", "Cómo se lee el almanaque", fondo=(244, 236, 210))
    L = ["Fl(2+1) 15 s se lee: grupos de dos y de un destello,", "y el ciclo entero dura quince segundos.", "",
         "Un destello es un segundo de luz,", "y tras él, otro segundo a oscuras.", "Entre un grupo y el siguiente,", "tres segundos de sombra.",
         "Al terminar el último grupo,", "oscuro hasta cerrar el ciclo.", "Y el ciclo empieza con la luz encendida."]
    versos(h, L, 180, 42, 21)
    h.texto((W / 2, 640), "Ejemplo: Fl(2) 6 s", "texto", 22, TINTA)
    ej = [1, 0, 1, 0, 0, 0]
    lado = 52
    xx = (W - 6 * lado) / 2
    for s, v in enumerate(ej):
        h.rect(xx + s * lado, 670, xx + (s + 1) * lado, 740, (255, 220, 90) if v else (40, 46, 60), TINTA, 2)
        h.texto((xx + s * lado + lado / 2, 765), str(s + 1), "texto2", 16, TINTA)
    return h.final()


def almanaque(inst):
    de = inst["destellos"]
    h = papel("ALMANAQUE DE FAROS", None, alto_total=H * 2, fondo=(236, 232, 214))
    h.texto((W / 2 + 30, 98), "Costa norte · edición de 1923", "texto2", 22, TINTA)
    faros = list(de["faros"].items())
    for k, (nombre, d) in enumerate(faros):
        mitad, i = divmod(k, 4)
        y = (210 if mitad == 0 else H + 110) + i * 150
        h.texto((50, y), nombre, "texto", 28, TINTA, "lm")
        h.texto((50, y + 46), d["notacion"], "cartel", 30, AZUL, "lm")
        h.linea([(40, y + 88), (W - 40, y + 88)], (190, 186, 170), 1)
    h.texto((W / 2, H - 70), "(el almanaque sigue en la otra hoja)", "texto2", 20, TINTA)
    h.texto((W / 2, 2 * H - 70), "Costa norte, ediciones anteriores agotadas", "texto2", 20, TINTA)
    return h.final()


# ------------------------------------------------------------------ guardianes
def cuaderno_relevos(inst, mitad):
    g = inst["guardianes"]
    fr = g["frases"]
    corte = (len(fr) + 1) // 2
    sel = fr[:corte] if mitad == 0 else fr[corte:]
    ini = 0 if mitad == 0 else corte
    h = papel("CUADERNO DE RELEVOS", f"Hoja {mitad + 1} de 2", fondo=(240, 232, 208))
    y = 170
    if mitad == 0:
        y = parrafo(h, 56, y, W - 112, "Cinco guardianes, cinco literas en fila, de izquierda a derecha. Cada uno con su gorro; ninguno se repite.", "texto2", 21, TINTA)
        y += 20
    for k, t in enumerate(sel):
        h.disco(66, y, 17, AMBAR, TINTA, 2)
        h.texto((66, y + 1), str(ini + k + 1), "cartel", 22, TINTA)
        y = parrafo(h, 100, y, W - 160, t, "texto2", 22, TINTA) + 24
    if mitad == 1:
        h.texto((W / 2, 790), "Nombres: " + ", ".join(g["nombres"]), "texto2", 19, TINTA)
        h.texto((W / 2, 822), "Gorros: " + ", ".join(g["gorros"]), "texto2", 19, TINTA)
    return h.final()


# ------------------------------------------------------------------ desván (laberinto)
def plano_desvan(inst):
    lb = inst["laberinto"]
    n, lado = lb["n"], 66
    x0 = (W - n * lado) / 2
    h = papel("PLANO DEL DESVÁN", None, alto_total=H * 2, fondo=(232, 222, 198))
    h.texto((W / 2 + 30, 98), "Cajas apiladas del suelo al techo", "texto2", 22, TINTA)
    parrafo(h, 56, 160, W - 112, "Entras por la escalera, abajo a la izquierda. La trampilla de la lente está arriba a la derecha. En el desván no hay luz.", "texto2", 21)
    y_sup = H - 40 - 4 * lado - 14
    y_inf = H + 60
    def pos_y(f):
        return y_sup + f * lado if f < 4 else y_inf + (f - 4) * lado
    for f in range(n):
        for c in range(n):
            x, y = x0 + c * lado, pos_y(f)
            h.rect(x, y, x + lado, y + lado, (210, 196, 160))
    for f in range(n):
        for c in range(n):
            x, y = x0 + c * lado, pos_y(f)
            ab = lb["abierto"][f][c]
            for d, (a, b, e, g) in (("N", (x, y, x + lado, y)), ("S", (x, y + lado, x + lado, y + lado)), ("O", (x, y, x, y + lado)), ("E", (x + lado, y, x + lado, y + lado))):
                if d in ab:
                    continue
                if f == lb["meta"][0] and c == lb["meta"][1] and d == "N":
                    continue
                h.linea([(a, b), (e, g)], (96, 60, 30), 7)
    fi, ci = lb["inicio"]
    xi, yi = x0 + ci * lado + lado / 2, pos_y(fi) + lado / 2
    flecha(h, (xi, yi + 20), (xi, yi - 22), (30, 130, 60), 7, 18)
    h.texto((xi, pos_y(fi) + lado + 20), "ENTRADA", "texto", 18, (30, 110, 50))
    fm, cm = lb["meta"]
    xm, ym = x0 + cm * lado + lado / 2, pos_y(fm) + lado / 2
    h.disco(xm, ym, 18, (250, 210, 60), TINTA, 3)
    h.texto((xm, ym + 1), "★", "texto", 20, TINTA)
    h.texto((xm, pos_y(fm) - 16), "TRAMPILLA", "texto", 17, (150, 40, 30))
    h.texto((W / 2, y_inf + 4 * lado + 40), "Miras al norte (hacia arriba) al entrar.", "texto2", 20, TINTA)
    h.texto((W / 2, y_inf + 4 * lado + 72), "El plano está dibujado en dos hojas.", "texto2", 20, TINTA)
    return h.final()


# ------------------------------------------------------------------ espejos
def papel_nido(inst):
    h = papel("EL PAPEL DEL NIDO", "Escondido entre las plumas", fondo=(240, 232, 208))
    L = ["La luz del foco no sube", "si antes no cruza.", "", "Primero a la galería,", "arriba, donde sopla el viento.",
         "Luego a la lente,", "que lo mira todo.", "Y por último, a la lámpara,", "para que baje y se encienda.", "",
         "«La luz sube, cruza y baja.»"]
    versos(h, L, 180, 44, 22)
    return h.final()


def cuaderno_optico(inst):
    h = papel("EL CUADERNO DEL ÓPTICO", "Cómo trabajan los espejos", fondo=(232, 238, 240))
    # dos espejos con el rayo
    for k, (tipo, ent, sal) in enumerate((("/", "E", "N"), ("\\", "E", "S"))):
        cx, cy = 175 + k * 280, 270
        h.rect(cx - 70, cy - 70, cx + 70, cy + 70, (214, 224, 232), BORDE, 2)
        if tipo == "/":
            h.linea([(cx - 44, cy + 44), (cx + 44, cy - 44)], (176, 120, 40), 9)
        else:
            h.linea([(cx - 44, cy - 44), (cx + 44, cy + 44)], (176, 120, 40), 9)
        flecha(h, (cx - 110, cy), (cx - 8, cy), (214, 160, 40), 4, 13)
        flecha(h, (cx, cy), (cx, cy - 106) if sal == "N" else (cx, cy + 106), (214, 160, 40), 4, 13)
        h.texto((cx, cy + 108), "espejo «" + tipo + "»", "texto", 20, TINTA)
    parrafo(h, 56, 470, W - 112, "El espejo desvía el rayo. Un espejo «/» lo manda hacia arriba si viene de la izquierda; un espejo «\\» lo manda hacia abajo.", "texto2", 21)
    parrafo(h, 56, 580, W - 112, "Una roca para el rayo. Solo los espejos que toca el rayo importan: los demás no pintan nada.", "texto2", 21)
    parrafo(h, 56, 690, W - 112, "El foco está a la izquierda del tablero y su rayo sale hacia la derecha.", "texto2", 21)
    return h.final()


# ------------------------------------------------------------------ metapuzle
def orden_arranque(inst):
    m = inst["meta"]
    riddles = {"14": "El centinela de madera que guarda la entrada y pide la hora.",
               "20": "Lo que cuelga en el armario y habla sin voz.",
               "40": "La caja que crepita y canta con las ruedas.",
               "48": "El ojo que parpadea en la ventana redonda.",
               "52": "Los islotes que hay que contar sin que se toquen."}
    h = papel("EL ORDEN DE ARRANQUE", "Escrito a lápiz en la sala de máquinas", fondo=(240, 232, 208))
    y = 160
    for k, a in enumerate(m["orden"]):
        h.disco(66, y + 12, 20, AMBAR, TINTA, 2)
        h.texto((66, y + 13), str(k + 1), "cartel", 26, TINTA)
        y = parrafo(h, 106, y + 12, W - 160, riddles[a], "texto2", 22, TINTA) + 38
    h.texto((W / 2, 790), "De cada uno, la cifra que dejó al abrirse.", "texto2", 20, TINTA)
    return h.final()


def tabla_valvulas(inst):
    m = inst["meta"]
    h = papel("LAS VÁLVULAS", "Cada cifra pasa por una válvula", fondo=(226, 232, 236))
    h.texto((W / 2 + 30, 134), "entra → sale", "texto2", 21, TINTA)
    for d in range(10):
        fila, col = divmod(d, 5)
        x = 80 + col * 112
        y = 210 + fila * 210
        h.disco(x + 30, y, 30, (250, 244, 226), TINTA, 3)
        h.texto((x + 30, y + 2), str(d), "cartel", 32, TINTA)
        flecha(h, (x + 30, y + 38), (x + 30, y + 92), AMBAR, 6, 18)
        h.disco(x + 30, y + 130, 30, (214, 232, 244), AZUL, 3)
        h.texto((x + 30, y + 132), str(m["tabla"][d]), "cartel", 32, AZUL)
    h.texto((W / 2, 690), "La combinación del panel son", "texto2", 22, TINTA)
    h.texto((W / 2, 724), "las cifras que SALEN de las válvulas.", "texto2", 22, TINTA)
    return h.final()


# ------------------------------------------------------------------ imágenes de la interfaz
def ui_imagenes(carpeta):
    d = os.path.join(carpeta, "img", "ui")
    os.makedirs(d, exist_ok=True)
    so = _inst()["sombras"]
    for k, nombre in enumerate(so["objetos"]):
        mask = IA.silueta(nombre, 0).crop((0, 0, 120, 160))
        capa = Image.new("RGBA", mask.size, OBJ_COL[k] + (255,))
        capa.putalpha(mask)
        capa.save(os.path.join(d, f"obj-{nombre}.png"))
        sm = Image.new("RGBA", mask.size, (20, 18, 16, 255))
        sm.putalpha(mask)
        sm.save(os.path.join(d, f"sombra-{nombre}.png"))


DATOS_MINIJUEGOS = {
    "14-puerta.js": lambda i: {"codigo": i["puerta"]["codigo"], "cifra": i["meta"]["cifras"]["14"]},
    "20-banderas.js": lambda i: {"palabra": i["banderas"]["palabra"], "cifra": i["meta"]["cifras"]["20"]},
    "40-radio.js": lambda i: {"objetivo": i["radio"]["objetivo"], "falsas": i["radio"]["falsas"], "cifra": i["meta"]["cifras"]["40"]},
    "48-morse.js": lambda i: {"palabra": i["morse"]["palabra"], "letras": i["morse"]["letras"], "cifra": i["meta"]["cifras"]["48"]},
    "52-bahia.js": lambda i: {"n": i["bahia"]["n"], "tierra": i["bahia"]["tierra"], "cifra": i["meta"]["cifras"]["52"]},
    "46-sombras.js": lambda i: {"objetos": i["sombras"]["objetos"], "solucion": i["sombras"]["solucion"]},
    "51-destellos.js": lambda i: {"periodo": i["destellos"]["periodo"], "solucion": i["destellos"]["solucion"]},
    "64-guardianes.js": lambda i: {"nombres": i["guardianes"]["nombres"], "gorros": i["guardianes"]["gorros"], "solucion": i["guardianes"]["solucion"]},
    "69-desvan.js": lambda i: {"n": i["laberinto"]["n"], "abierto": i["laberinto"]["abierto"], "inicio": i["laberinto"]["inicio"], "meta": i["laberinto"]["meta"],
                               "mira": i["laberinto"]["mira"]},
    "85-panel.js": lambda i: {"codigo": i["meta"]["codigo"]},
}


def inyectar_datos(carpeta, inst):
    for nombre, f in DATOS_MINIJUEGOS.items():
        ruta = os.path.join(carpeta, "minijuegos", nombre)
        if not os.path.exists(ruta):
            continue
        js = open(ruta, encoding="utf-8").read()
        if "/*DATOS*/" not in js:
            continue
        a, b = js.index("/*DATOS*/") + len("/*DATOS*/"), js.index("/*FIN*/")
        js = js[:a] + json.dumps(f(inst), ensure_ascii=False, separators=(", ", ": ")) + js[b:]
        open(ruta, "w", encoding="utf-8", newline="\n").write(js)


def main(carpeta="juegos/el-faro"):
    inst = _inst()
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    laminas = {"16": carta_reloj(inst), "18": carta_mensaje_banderas(inst), "41": carta_mapa(inst), "43": carta_brujula(inst), "45": carta_versos_radio(inst),
               "53": carta_sirena(inst), "59": versos_bahia(inst), "37": carta_sombra(inst), "39": carta_estante(inst), "33": nota_sombras(inst),
               "26": nota_almanaque(inst), "66": cuaderno_relevos(inst, 0), "67": cuaderno_relevos(inst, 1), "75": papel_nido(inst),
               "79": cuaderno_optico(inst), "86": orden_arranque(inst), "87": tabla_valvulas(inst)}
    for k, im in laminas.items():
        ruido(im, int(k)).save(os.path.join(arte, f"{k}.png"))

    def mosaico(nombre, im, filas, cols, cartas):
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))
        for pieza, k in zip(cortar(im, filas, cols), cartas):
            pieza.save(os.path.join(arte, f"{k}.png"))
    mosaico("banderas", tabla_banderas(inst), 2, 1, ("19", "21"))
    mosaico("morse", tabla_morse(inst), 2, 1, ("42", "49"))
    mosaico("bahia", plano_bahia(inst), 2, 1, ("54", "55"))
    mosaico("almanaque", almanaque(inst), 2, 1, ("61", "63"))
    mosaico("desvan", plano_desvan(inst), 2, 1, ("70", "71"))
    ui_imagenes(carpeta)
    inyectar_datos(carpeta, inst)
    print("láminas escritas en", arte)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

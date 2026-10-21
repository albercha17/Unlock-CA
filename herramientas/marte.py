"""Láminas de «Marte, 2157: Cúpula Aurora» (versión de 60 cartas, 21 oct 2026). Todas las pistas son dibujos o acertijos:
ninguna carta escribe la respuesta ni explica cómo se resuelve su puzle. Datos de herramientas/instancias_marte.py.

  16 los pasos de los satélites · 18 las reglas del invernadero · 19 y 21 el invernadero (dos mitades)
  41 y 43 la placa de bornes (dos mitades) · 45 la norma de los cables · 42 y 49 el radar del campo de rocas (dos mitades) · 53 el aviso del radar
  54 el brazo de la antena · 55 los pesos de repuesto · 59 la norma del brazo · 37 los números de la cuenta · 39 el objetivo · 33 la norma de la cuenta
  61 y 63 el esquema del reactor (dos mitades) · 26 la nota de la doctora Reyes · 70 el mapa del rover · 71 los comandos del rover
  66 y 67 los paneles de refrigeración (dos mitades) · 75 y 79 la base de datos (dos mitades) · 86 y 87 los acertijos del lanzamiento
Uso (desde la raíz del repo):  python herramientas/marte.py [carpeta_juego]
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
import instancias_marte as I  # noqa: E402

W, H = 630, 882
FONDO = (236, 214, 196)
TINTA = (52, 26, 18)
NARANJA = (226, 108, 52)
CIAN = (40, 160, 184)
METAL = (124, 132, 144)
OSCURO = (46, 40, 44)
ROJO = (190, 50, 44)
VERDE = (70, 160, 90)
AMARILLO = (232, 190, 60)
VIOLETA = (140, 80, 190)
AZUL = (60, 100, 210)
BLANCO = (252, 246, 240)
CABLES = [ROJO, AZUL, VERDE, AMARILLO, VIOLETA]


def ruido(im, s, f=2.5):
    a = np.asarray(im).astype(np.int16)
    a = a + np.random.default_rng(s).normal(0, f, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def pagina(titulo, sub=None, fondo=FONDO, borde=NARANJA, w=W, h=H):
    p = Hoja(w, h, fondo)
    p.rect(16, 16, w - 16, h - 16, None, borde, 6)
    p.rect(28, 28, w - 28, h - 28, None, borde, 2)
    p.texto((w / 2 + 26, 70), titulo, "cartel", 32, TINTA)
    if sub:
        p.texto((w / 2 + 26, 108), sub, "texto2", 21, TINTA)
    return p


def versos(p, lineas, y0=220, paso=56, tam=27, x=W / 2):
    for k, v in enumerate(lineas):
        p.texto((x, y0 + k * paso), v, "texto2", tam, TINTA)


def ancha(titulo, fondo=FONDO, borde=NARANJA):
    p = Hoja(W * 2, H, fondo)
    p.rect(16, 16, W * 2 - 16, H - 16, None, borde, 6)
    p.rect(28, 28, W * 2 - 28, H - 28, None, borde, 2)
    p.texto((W, 66), titulo, "cartel", 34, TINTA)
    return p


# ------------------------------------------------------------------ 16: los pasos de los satélites
def pasos_satelites():
    d = I.SATELITES
    p = pagina("PASOS DE LOS SATÉLITES", "vistos por la antena de la cúpula", FONDO, CIAN)
    x0, x1 = 120, W - 50
    esc = (x1 - x0) / d["horas_vistas"]
    for k, s in enumerate(d["sats"]):
        y = 250 + k * 190
        p.texto((70, y - 60), s["nombre"], "texto", 24, TINTA, "lm")
        p.linea([(x0, y), (x1, y)], METAL, 4)
        for t in s["pasos_vistos"]:
            p.disco(x0 + t * esc, y, 13, CABLES[k], TINTA, 2)
    y = 790
    p.linea([(x0, y), (x1, y)], TINTA, 3)
    for t in range(0, d["horas_vistas"] + 1, 4):
        p.linea([(x0 + t * esc, y - 8), (x0 + t * esc, y + 8)], TINTA, 3)
        p.texto((x0 + t * esc, y + 30), str(t), "texto", 17, TINTA)
    p.texto((W - 40, y + 60), "horas desde ahora", "texto2", 15, TINTA, "rm")
    return p.final()


# ------------------------------------------------------------------ 18, 19/21: el invernadero
def reglas_vida():
    p = pagina("LAS REGLAS DEL INVERNADERO", "pegadas en la puerta", FONDO, VERDE)
    versos(p, ["«Cada planta vive de sus vecinas:", "las ocho casillas de alrededor.", "", "Con dos o tres, sigue viva.",
               "Con menos, se seca; con más, se ahoga.", "", "Y en un suelo vacío con tres vecinas", "nace una nueva.»"], 210, 56, 26)
    return p.final()


def invernadero():
    d = I.VIDA
    n = d["n"]
    p = Hoja(W, H * 2, FONDO)
    p.rect(16, 16, W - 16, H * 2 - 16, None, VERDE, 6)
    p.rect(28, 28, W - 28, H * 2 - 28, None, VERDE, 2)
    p.texto((W / 2 + 26, 70), "EL INVERNADERO", "cartel", 32, TINTA)
    p.texto((W / 2 + 26, 108), "así está hoy; mañana, otra cosa", "texto2", 20, TINTA)
    lado = 96
    x0, y0 = (W - n * lado) / 2, H - 3 * lado
    for y in range(n):
        for x in range(n):
            px, py = x0 + x * lado, y0 + y * lado
            p.rect(px, py, px + lado, py + lado, (92, 66, 52), (60, 40, 30), 2)
            if d["actual"][y][x]:
                p.disco(px + lado / 2, py + lado / 2 + 6, 30, VERDE, (30, 90, 50), 3)
                p.poli([(px + lado / 2, py + 12), (px + lado / 2 + 18, py + 40), (px + lado / 2 - 18, py + 40)], (110, 200, 120), (30, 90, 50), 2)
    return p.final()


# ------------------------------------------------------------------ 41/43, 45: el cableado
def placa_cables():
    d = I.CABLEADO
    n = d["n"]
    p = ancha("LA PLACA DE BORNES", FONDO, CIAN)
    lado = 112
    x0, y0 = 630 - 3 * lado, 120
    for y in range(n):
        for x in range(n):
            p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, (200, 214, 206), (140, 160, 150), 2)
    for c, (a, b) in d["extremos"].items():
        for (x, y) in (a, b):
            cx, cy = x0 + x * lado + lado / 2, y0 + y * lado + lado / 2
            p.disco(cx, cy, 38, CABLES[int(c)], TINTA, 4)
            p.texto((cx, cy), str(int(c) + 1), "cartel", 36, BLANCO)
    return p.final()


def norma_cables():
    p = pagina("LA NORMA DE LOS CABLES", "del manual de la cúpula", FONDO, CIAN)
    versos(p, ["«Cada borne tiene un gemelo", "del mismo color y número.", "", "Un cable los une, pasando", "por casillas contiguas.",
               "", "Dos cables nunca comparten casilla,", "y en una placa buena", "no queda ninguna vacía.»"], 205, 54, 26)
    return p.final()


# ------------------------------------------------------------------ 42/49, 53: el campo de rocas
def radar():
    d = I.ROCAS
    n = d["n"]
    p = ancha("EL RADAR DEL CAMPO DE ROCAS", FONDO, NARANJA)
    lado = 92
    x0, y0 = 630 - 4 * lado, 112
    num = {(x, y): k for x, y, k in d["numeros"]}
    for y in range(n):
        for x in range(n):
            if (x, y) in num:
                p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, BLANCO, (150, 130, 120), 2)
                p.texto((x0 + x * lado + lado / 2, y0 + y * lado + lado / 2), str(num[(x, y)]), "cartel", 40, CIAN if num[(x, y)] else (120, 120, 120))
            else:
                p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, (150, 128, 112), (110, 90, 78), 2)
    return p.final()


def aviso_radar():
    d = I.ROCAS
    p = pagina("EL AVISO DEL RADAR", "mensaje automático", FONDO, NARANJA)
    versos(p, ["«Las casillas con número", "están despejadas.", "", "Cada número cuenta las rocas",
               "escondidas en las ocho casillas", "que lo rodean.", "", f"En todo el campo hay {d['total']} rocas.»"], 210, 54, 26)
    return p.final()


# ------------------------------------------------------------------ 54/55/59: el brazo de la antena
FORMAS = ["circulo", "cuadrado", "triangulo"]


def peso(p, forma, cx, cy, r, valor=None, color=NARANJA):
    if forma == "circulo":
        p.disco(cx, cy, r, color, TINTA, 3)
    elif forma == "cuadrado":
        p.rect(cx - r, cy - r, cx + r, cy + r, color, TINTA, 3)
    else:
        p.poli([(cx, cy - r * 1.1), (cx + r * 1.1, cy + r * 0.9), (cx - r * 1.1, cy + r * 0.9)], color, TINTA, 3)
    if valor is not None:
        p.texto((cx, cy + 4), str(valor), "cartel", int(r * 1.1), BLANCO)


def brazo():
    d = I.BALANCIN
    p = pagina("EL BRAZO DE LA ANTENA", "marcas a cada lado del eje", FONDO, METAL)
    cx, y = W / 2, 520
    paso = 52
    p.rect(cx - 5 * paso - 40, y, cx + 5 * paso + 40, y + 22, METAL, TINTA, 3)
    p.poli([(cx, y + 22), (cx + 40, y + 120), (cx - 40, y + 120)], OSCURO, TINTA, 3)
    for pos in d["posiciones"]:
        x = cx + pos * paso
        p.linea([(x, y), (x, y + 22)], TINTA, 3)
        p.texto((x, y + 50), str(abs(pos)), "texto", 20, TINTA)
    for k, (v, s) in enumerate(d["fijos"]):
        peso(p, FORMAS[k % 3] if False else "cuadrado", cx + s * paso, y - 32, 24, v, METAL)
    p.texto((cx, y + 160), "eje", "texto2", 20, TINTA)
    return p.final()


def pesos_repuesto():
    d = I.BALANCIN
    p = pagina("LOS PESOS DE REPUESTO", "caja de herramientas", FONDO, METAL)
    for k, v in enumerate(d["libres"]):
        y = 250 + k * 170
        peso(p, FORMAS[k], 200, y, 50, v)
        p.texto((340, y), f"pesa {v}", "texto", 28, TINTA, "lm")
    return p.final()


def norma_brazo():
    p = pagina("LA NORMA DEL BRAZO", "del manual de la antena", FONDO, METAL)
    versos(p, ["«Cada peso empuja hacia abajo", "tanto como pesa,", "multiplicado por lo lejos", "que está del eje.", "",
               "Si lo de un lado empuja igual", "que lo del otro, el brazo", "no se inclina.", "", "En cada marca cabe un solo peso.»"], 190, 50, 25)
    return p.final()


# ------------------------------------------------------------------ 37/39/33: la cuenta de cifras
def numeros_cuenta():
    d = I.CIFRAS
    p = pagina("LAS PIEZAS DE LA CUENTA", "del ordenador de a bordo", FONDO, CIAN)
    for k, v in enumerate(d["numeros"]):
        x = 150 + (k % 3) * 165
        y = 300 + (k // 3) * 220
        p.rect(x - 60, y - 70, x + 60, y + 70, BLANCO, TINTA, 4)
        p.texto((x, y), str(v), "cartel", 56 if v < 100 else 48, TINTA)
    return p.final()


def objetivo_cuenta():
    d = I.CIFRAS
    p = pagina("EL OBJETIVO", "lo que pide la trayectoria", FONDO, CIAN)
    p.disco(W / 2, 400, 170, OSCURO, CIAN, 8)
    p.texto((W / 2, 400), str(d["objetivo"]), "cartel", 110, (150, 240, 255))
    return p.final()


def norma_cuenta():
    p = pagina("LA NORMA DE LA CUENTA", "del ordenador de a bordo", FONDO, CIAN)
    versos(p, ["«Cada pieza se usa", "una vez como mucho.", "", "Se puede sumar, restar,", "multiplicar y dividir,",
               "pero los resultados", "han de ser números enteros", "y mayores que cero.", "", "Un resultado vale como pieza nueva.»"], 190, 52, 25)
    return p.final()


# ------------------------------------------------------------------ 61/63, 26: el anillo del reactor
def esquema_reactor():
    d = I.ANILLO
    n = d["n"]
    p = ancha("EL ESQUEMA DEL REACTOR", FONDO, ROJO)
    lado = 110
    x0, y0 = 630 - 3 * lado, 120
    for y in range(n):
        for x in range(n):
            p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, (232, 220, 208), (190, 170, 156), 1)
    for x, y, k in d["pistas"]:
        p.texto((x0 + x * lado + lado / 2, y0 + y * lado + lado / 2), str(k), "cartel", 44, TINTA)
    for y in range(n + 1):
        for x in range(n + 1):
            p.disco(x0 + x * lado, y0 + y * lado, 7, TINTA)
    return p.final()


def nota_reyes():
    p = pagina("NOTA DE LA DOCTORA REYES", "garabateada en el borde del esquema", FONDO, ROJO)
    versos(p, ["«El circuito del reactor es un anillo:", "un solo bucle cerrado, sin cruces", "ni ramales, que pasa de punto en punto.",
               "", "Cada número dice por cuántos lados", "de su casilla pasa el anillo.", "Donde no hay número, vale cualquier cosa.»"], 210, 54, 25)
    return p.final()


# ------------------------------------------------------------------ 70/71: el programa del rover
def mapa_rover():
    d = I.PROGRAMA
    n = d["n"]
    p = pagina("EL TERRENO DEL ROVER", "visto desde el dron", FONDO, NARANJA)
    lado = 78
    x0, y0 = (W - n * lado) / 2, 170
    muros = {tuple(m) for m in d["muros"]}
    for y in range(n):
        for x in range(n):
            px, py = x0 + x * lado, y0 + y * lado
            if (x, y) in muros:
                p.rect(px, py, px + lado, py + lado, (130, 100, 84), (90, 66, 54), 2)
                p.poli([(px + 10, py + lado - 10), (px + lado / 2, py + 12), (px + lado - 10, py + lado - 10)], (104, 78, 64), (80, 58, 48), 2)
            else:
                p.rect(px, py, px + lado, py + lado, (240, 224, 206), (200, 180, 160), 2)
    sx, sy = d["inicio"]
    cx, cy = x0 + sx * lado + lado / 2, y0 + sy * lado + lado / 2
    p.rect(cx - 24, cy - 16, cx + 24, cy + 16, CIAN, TINTA, 3)
    p.poli([(cx + 24, cy - 12), (cx + 38, cy), (cx + 24, cy + 12)], TINTA)
    mx, my = d["meta"]
    cx, cy = x0 + mx * lado + lado / 2, y0 + my * lado + lado / 2
    p.linea([(cx - 12, cy + 26), (cx - 12, cy - 26)], TINTA, 5)
    p.poli([(cx - 12, cy - 26), (cx + 26, cy - 14), (cx - 12, cy - 2)], ROJO, TINTA, 2)
    return p.final()


def comandos_rover():
    d = I.PROGRAMA
    p = pagina("LOS COMANDOS DEL ROVER", "del manual de programación", FONDO, NARANJA)
    filas = [("a", "avanzar una casilla"), ("i", "girar a la izquierda"), ("d", "girar a la derecha"), ("r", "repetir varias veces lo de dentro")]
    for k, (c, txt) in enumerate(filas):
        y = 230 + k * 110
        p.rect(60, y - 36, 150, y + 36, BLANCO, TINTA, 3)
        if c == "a":
            p.poli([(80, y - 14), (110, y - 14), (110, y - 26), (136, y), (110, y + 26), (110, y + 14), (80, y + 14)], TINTA)
        elif c == "i":
            p.linea([(130, y + 18), (130, y - 12), (92, y - 12)], TINTA, 8)
            p.poli([(92, y - 30), (72, y - 12), (92, y + 6)], TINTA)
        elif c == "d":
            p.linea([(80, y + 18), (80, y - 12), (118, y - 12)], TINTA, 8)
            p.poli([(118, y - 30), (138, y - 12), (118, y + 6)], TINTA)
        else:
            p.linea([(84, y + 16), (84, y - 16), (126, y - 16), (126, y + 16), (96, y + 16)], TINTA, 7)
            p.poli([(96, y + 4), (96, y + 28), (74, y + 16)], TINTA)
        p.texto((180, y), txt, "texto2", 22, TINTA, "lm")
    p.texto((W / 2, 720), f"El programa cabe en {d['limite']} bloques.", "texto", 26, ROJO)
    p.texto((W / 2, 765), "«Repetir» cuenta como un bloque", "texto2", 19, TINTA)
    p.texto((W / 2, 795), "y cada comando de dentro, otro.", "texto2", 19, TINTA)
    return p.final()


# ------------------------------------------------------------------ 66/67: los paneles
def paneles_refrigeracion():
    d = I.PANELES
    n = d["n"]
    p = Hoja(W, H * 2, FONDO)
    p.rect(16, 16, W - 16, H * 2 - 16, None, CIAN, 6)
    p.rect(28, 28, W - 28, H * 2 - 28, None, CIAN, 2)
    p.texto((W / 2 + 26, 70), "LOS PANELES DE REFRIGERACIÓN", "cartel", 30, TINTA)
    for k, v in enumerate(["Tocar un panel cambia ese panel", "y los cuatro que lo rodean en cruz:", "encendido, apagado; apagado, encendido.",
                           "Se empieza con todos apagados."]):
        p.texto((W / 2, 200 + k * 36), v, "texto2", 21, TINTA)
    p.texto((W / 2, 400), "El patrón que hay que conseguir:", "texto", 22, TINTA)
    lado = 104
    x0, y0 = (W - n * lado) / 2, H - 2 * lado + 20 if False else 480
    y0 = H - 2 * lado - 0
    for y in range(n):
        for x in range(n):
            px, py = x0 + x * lado, y0 + y * lado
            p.rect(px, py, px + lado, py + lado, (72, 78, 90), (40, 44, 52), 3)
            if d["objetivo"][y][x]:
                p.disco(px + lado / 2, py + lado / 2, 34, (150, 240, 255), CIAN, 4)
    return p.final()


# ------------------------------------------------------------------ 75/79: la base de datos
def sopa_letras():
    d = I.SOPA
    n = d["n"]
    p = ancha("LA BASE DE DATOS DE LA COLONIA", FONDO, VIOLETA)
    lado = 90
    x0, y0 = 630 - 3 * lado, 110
    for y in range(n):
        for x in range(n):
            p.rect(x0 + x * lado, y0 + y * lado, x0 + (x + 1) * lado, y0 + (y + 1) * lado, (244, 232, 222), (200, 180, 170), 1)
            p.texto((x0 + x * lado + lado / 2, y0 + y * lado + lado / 2), d["rejilla"][y][x], "cartel", 44, TINTA)
    p.texto((190, 170), "Palabras de la base:", "texto", 22, TINTA)
    for k, w in enumerate(d["palabras"]):
        p.texto((190, 230 + k * 50), w, "texto", 24, TINTA)
    p.texto((190, 230 + len(d["palabras"]) * 50 + 50), "Las demás letras,", "texto2", 18, TINTA)
    p.texto((190, 230 + len(d["palabras"]) * 50 + 78), "leídas en orden, son", "texto2", 18, TINTA)
    p.texto((190, 230 + len(d["palabras"]) * 50 + 106), "la clave de acceso.", "texto2", 18, TINTA)
    return p.final()


# ------------------------------------------------------------------ 86/87: los acertijos del lanzamiento
def acertijo(titulo, lineas):
    p = pagina(titulo, "dictado por la doctora Reyes", FONDO, NARANJA)
    versos(p, lineas, 230, 58, 25)
    return p.final()


def inyectar(carpeta):
    """Mete los datos de las instancias en las apps (bloque /*DATOS*/.../*FIN*/)."""
    datos = {
        "14-satelites.js": {"sats": [{"nombre": s["nombre"]} for s in I.SATELITES["sats"]], "solucion": I.SATELITES["solucion"], "dato": I.DATOS_MISION["14"]},
        "20-invernadero.js": {"n": I.VIDA["n"], "solucion": I.VIDA["solucion"], "dato": I.DATOS_MISION["20"]},
        "40-cableado.js": {"n": I.CABLEADO["n"], "colores": I.CABLEADO["colores"], "solucion": I.CABLEADO["solucion"], "dato": I.DATOS_MISION["40"]},
        "48-rocas.js": {"n": I.ROCAS["n"], "solucion": I.ROCAS["solucion"]},
        "52-brazo.js": {"posiciones": I.BALANCIN["posiciones"], "libres": len(I.BALANCIN["libres"]), "solucion": I.BALANCIN["solucion"], "dato": I.DATOS_MISION["52"]},
        "46-cuenta.js": {"numeros": I.CIFRAS["numeros"], "objetivo": I.CIFRAS["objetivo"]},
        "51-anillo.js": {"n": I.ANILLO["n"], "solucion": I.ANILLO["solucion"]},
        "69-programa.js": I.PROGRAMA,
        "64-paneles.js": {"n": I.PANELES["n"], "objetivo": I.PANELES["objetivo"]},
        "72-sopa.js": {"secreta": I.SOPA["secreta"]},
        "85-consola.js": {"codigo": I.CODIGO},
    }
    for app, d in datos.items():
        ruta = os.path.join(carpeta, "minijuegos", app)
        txt = open(ruta, encoding="utf-8").read() if os.path.exists(ruta) else ""
        if "/*DATOS*/" not in txt:
            continue
        a, b = txt.index("/*DATOS*/") + len("/*DATOS*/"), txt.index("/*FIN*/")
        open(ruta, "w", encoding="utf-8", newline="\n").write(txt[:a] + json.dumps(d, ensure_ascii=False) + txt[b:])


def main(carpeta="juegos/aventuras-ca/marte"):
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    g = lambda k, im: ruido(im, int(k)).save(os.path.join(arte, f"{k}.png"))

    def mosaico(nombre, im, filas, cols, cartas):
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))
        for pieza, k in zip(cortar(im, filas, cols), cartas):
            pieza.save(os.path.join(arte, f"{k}.png"))
    g("16", pasos_satelites())
    g("18", reglas_vida())
    mosaico("invernadero", invernadero(), 2, 1, ("19", "21"))
    mosaico("cableado", placa_cables(), 1, 2, ("41", "43"))
    g("45", norma_cables())
    mosaico("rocas", radar(), 1, 2, ("42", "49"))
    g("53", aviso_radar())
    g("54", brazo())
    g("55", pesos_repuesto())
    g("59", norma_brazo())
    g("37", numeros_cuenta())
    g("39", objetivo_cuenta())
    g("33", norma_cuenta())
    mosaico("reactor", esquema_reactor(), 1, 2, ("61", "63"))
    g("26", nota_reyes())
    g("70", mapa_rover())
    g("71", comandos_rover())
    mosaico("paneles", paneles_refrigeracion(), 2, 1, ("66", "67"))
    mosaico("sopa", sopa_letras(), 1, 2, ("75", "79"))
    g("86", acertijo("PRIMERA PARTE DE LA CLAVE", ["«Primero, el dato de lo que une", "con cobre los bornes gemelos.", "", "Segundo, el de lo que da vueltas", "sobre nuestras cabezas",
                                                    "y pasa a ratos por la antena.»"]))
    g("87", acertijo("SEGUNDA PARTE DE LA CLAVE", ["«Tercero, el dato de lo que se", "equilibra con pesos.", "", "Cuarto, el de lo que crece", "o se seca en el invernadero.»"]))
    inyectar(carpeta)
    print("láminas de Marte escritas en", arte)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

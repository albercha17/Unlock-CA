"""Cartas de «Montecarlo, 1965: Operación Cristal»: espionaje con cartas que se SUPERPONEN (a contraluz en papel, con «Superponer» en el Modo PC).

Todo se dibuja por código, así que los códigos son exactos (herramientas/codigos_espia.json lo leen los solucionadores):
  - criptografía visual (cartas 14 y 15): dos hojas de ruido que, una encima de otra, dejan ver un número de tres cifras (esquema 2 de 2 de Naor y Shamir:
    cada punto del dibujo secreto son 2x2 subpuntos; si el punto es blanco las dos hojas llevan el mismo patrón y si es negro llevan patrones complementarios);
  - rejilla de Cardano (cartas 30 y 31): una carta negra con ventanas sobre una carta de letras; por las ventanas se lee una palabra;
  - plano del yate (carta 40): el laberinto del minijuego 46; rascacielos (cartas 52 y 53): las pistas del borde repartidas en dos cartas;
  - manual del desactivador (carta 70): las reglas de los cables.
Uso (desde la raíz del repo):  python herramientas/espia.py [carpeta_juego]
"""
import json
import os
import random
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oeste  # noqa: E402
from oeste import Hoja, TINTA, ROJO  # noqa: E402

oeste.FUENTES["cour"] = "C:/Windows/Fonts/cour.ttf"
oeste.FUENTES["courb"] = "C:/Windows/Fonts/courbd.ttf"

MANILA = (236, 220, 178)
NEGRO = (22, 22, 22)
AZUL = (36, 84, 170)

CODIGOS = {
    "cripto": {"digitos": [7, 2, 9], "desfase": [5, -4]},
    "rejilla": {"palabra": "NEPTUNO", "desfase": [-4, 6]},
}
VENTANAS = [(1, 2), (2, 7), (4, 4), (5, 8), (8, 1), (10, 6), (12, 3)]     # (fila, columna) en el orden en que se lee la palabra


def _instancias():
    return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_espia.json"), encoding="utf-8"))


# ------------------------------------------------------------------ criptografía visual
SEGMENTOS = {0: "abcdef", 1: "bc", 2: "abdeg", 3: "abcdg", 4: "bcfg", 5: "acdfg", 6: "acdefg", 7: "abc", 8: "abcdefg", 9: "abcdfg"}
FILAS_S, COLS_S = 34, 25            # puntos del dibujo secreto (cada uno es un bloque de 2x2 subpuntos de 10 px = 20 px)
X0, Y0 = 60, 120                    # esquina de la zona de dibujo en la carta (520 x 728: el ancho al que se convierte para publicar, así el ruido de 8 px llega intacto)
SUB = 8                             # lado de un subpunto en píxeles (≈ 1 mm en la carta impresa)


def secreto_digitos(digitos):
    s = np.zeros((FILAS_S, COLS_S), bool)
    s[0, :] = s[-1, :] = True
    s[:, 0] = s[:, -1] = True                     # marco: se ve entero cuando las hojas están bien alineadas
    ancho, alto, g = 6, 15, 2
    top = (FILAS_S - alto) // 2
    for i, d in enumerate(digitos):
        x = 2 + i * 7
        mid = top + alto // 2 - g // 2
        seg = {"a": (x, top, x + ancho - 1, top + g - 1), "d": (x, top + alto - g, x + ancho - 1, top + alto - 1), "g": (x, mid, x + ancho - 1, mid + g - 1),
               "f": (x, top, x + g - 1, top + alto // 2 + g // 2 - 1), "b": (x + ancho - g, top, x + ancho - 1, top + alto // 2 + g // 2 - 1),
               "e": (x, mid, x + g - 1, top + alto - 1), "c": (x + ancho - g, mid, x + ancho - 1, top + alto - 1)}
        for k in SEGMENTOS[d]:
            x0, y0, x1, y1 = seg[k]
            s[y0:y1 + 1, x0:x1 + 1] = True
    return s


PATRONES = [(0, 1), (2, 3), (0, 2), (1, 3), (0, 3), (1, 2)]      # 2 de los 4 subpuntos de un bloque 2x2 (0 = arriba izq., 1 = arriba dcha., 2 = abajo izq., 3 = abajo dcha.)


def compartir(secreto, semilla=1965):
    rng = np.random.default_rng(semilla)
    h, w = secreto.shape
    a = np.zeros((h * 2, w * 2), bool)
    b = np.zeros((h * 2, w * 2), bool)
    for y in range(h):
        for x in range(w):
            p = set(PATRONES[rng.integers(6)])
            pb = p if not secreto[y, x] else {0, 1, 2, 3} - p
            for i in p:
                a[2 * y + i // 2, 2 * x + i % 2] = True
            for i in pb:
                b[2 * y + i // 2, 2 * x + i % 2] = True
    return a, b


def _carta_hoja(mascara):
    """Hoja de 520 x 728 con el marco de registro y la máscara de subpuntos (8 px cada uno) en la zona de dibujo."""
    im = np.full((728, 520), 255, np.uint8)
    px = np.kron(mascara, np.ones((SUB, SUB), bool))
    im[Y0:Y0 + px.shape[0], X0:X0 + px.shape[1]][px] = 22
    for g in range(8):                                         # marco
        im[100 + g, 40:480] = 22
        im[676 + g, 40:480] = 22
        im[100:684, 40 + g] = 22
        im[100:684, 472 + g] = 22
    return Image.fromarray(im).convert("RGB")


def cartas_cripto():
    a, b = compartir(secreto_digitos(CODIGOS["cripto"]["digitos"]))
    return _carta_hoja(a), _carta_hoja(b)


# ------------------------------------------------------------------ rejilla de Cardano
def cartas_rejilla():
    rng = random.Random(77)
    palabra = CODIGOS["rejilla"]["palabra"]
    filas, cols, cw, ch = 13, 10, 40, 41
    letras = [[rng.choice("ABCDEFGHIJLMOPQRSTUVXYZ") for _ in range(cols)] for _ in range(filas)]
    for (r, c), l in zip(VENTANAS, palabra):
        letras[r][c] = l
    # la palabra no debe aparecer otra vez por casualidad: las letras sueltas se eligen sin repetir ninguna de la palabra en la misma fila
    h = Hoja(520, 728, (252, 250, 244))
    h.rect(44, 104, 476, 680, (252, 250, 244), NEGRO, 8)
    for r in range(filas):
        for c in range(cols):
            h.texto((X0 + c * cw + cw / 2, Y0 + r * ch + ch / 2 + 2), letras[r][c], "courb", 33, NEGRO)
    letras_img = h.final()
    g = Hoja(520, 728, (252, 250, 244))
    g.rect(40, 100, 480, 684, (0, 0, 0))
    for (r, c) in VENTANAS:
        g.rect(X0 + c * cw + 3, Y0 + r * ch + 3, X0 + (c + 1) * cw - 3, Y0 + (r + 1) * ch - 3, (252, 250, 244))
    return g.final(), letras_img


# ------------------------------------------------------------------ cartas «dossier»
def _fondo(titulo, sello=True):
    h = Hoja(630, 882, MANILA)
    h.rect(22, 22, 608, 860, MANILA, TINTA, 4)
    h.texto((315, 78), titulo, "courb", 38 if len(titulo) <= 22 else 29, TINTA)
    h.linea([(60, 112), (570, 112)], TINTA, 3)
    if sello:
        h.texto((470, 830), "ALTO SECRETO", "courb", 26, ROJO)
        h.rect(322, 806, 618, 852, None or MANILA, ROJO, 3) if False else None
    return h


def carta_plano():
    """Carta 40: el plano del yate (laberinto 7x7 con un solo camino); las paredes son invisibles en el minijuego."""
    L = _instancias()["laberinto"]
    n, cel = L["n"], 66
    x0, y0 = 84, 200
    h = _fondo("PLANO DEL YATE «NEPTUNO»")
    h.rect(x0 - 6, y0 - 6, x0 + n * cel + 6, y0 + n * cel + 6, (250, 244, 226), TINTA, 3)
    abiertos = {tuple(map(tuple, p)) for p in L["abiertos"]}
    for f in range(n):
        for c in range(n):
            # pared a la derecha y abajo si no hay pasillo
            if c < n - 1 and ((f, c), (f, c + 1)) not in abiertos:
                h.linea([(x0 + (c + 1) * cel, y0 + f * cel), (x0 + (c + 1) * cel, y0 + (f + 1) * cel)], TINTA, 8)
            if f < n - 1 and ((f, c), (f + 1, c)) not in abiertos:
                h.linea([(x0 + c * cel, y0 + (f + 1) * cel), (x0 + (c + 1) * cel, y0 + (f + 1) * cel)], TINTA, 8)
    h.linea([(x0, y0), (x0 + n * cel, y0), (x0 + n * cel, y0 + n * cel), (x0, y0 + n * cel), (x0, y0)], TINTA, 10)
    h.rect(x0 - 8, y0 + 4, x0 + 4, y0 + cel - 4, (250, 244, 226))                       # entrada
    h.rect(x0 + n * cel - 4, y0 + (n - 1) * cel + 4, x0 + n * cel + 8, y0 + n * cel - 4, (250, 244, 226))   # salida
    h.poli([(x0 - 50, y0 + cel / 2 - 16), (x0 - 18, y0 + cel / 2), (x0 - 50, y0 + cel / 2 + 16)], (40, 140, 70), TINTA, 3)
    h.poli([(x0 + n * cel + 18, y0 + (n - 0.5) * cel - 16), (x0 + n * cel + 50, y0 + (n - 0.5) * cel), (x0 + n * cel + 18, y0 + (n - 0.5) * cel + 16)], ROJO, TINTA, 3)
    h.texto((x0 - 70, y0 + cel / 2 + 38), "ENTRADA", "courb", 20, (40, 140, 70), "lm")
    h.texto((x0 + n * cel + 62, y0 + (n - 0.5) * cel + 34), "SALIDA", "courb", 20, ROJO, "rm")
    h.texto((315, 700), "Los guardias no ven los muros:", "cour", 26, TINTA)
    h.texto((315, 736), "solo el que lleva el plano.", "cour", 26, TINTA)
    return h.final(ruido=3, semilla=40)


def cartas_rascacielos():
    """Cartas 52 y 53: la misma cuadrícula 4x4 con las pistas de dos lados cada una (52: arriba e izquierda; 53: abajo y derecha)."""
    R = _instancias()["rascacielos"]["pistas"]
    out = []
    for lados, titulo in ((("arriba", "izquierda"), "SKYLINE: ARRIBA E IZQUIERDA"), (("abajo", "derecha"), "SKYLINE: ABAJO Y DERECHA")):
        h = _fondo(titulo)
        cell, gx, gy = 84, 147, 228
        for f in range(4):
            for c in range(4):
                h.rect(gx + c * cell, gy + f * cell, gx + (c + 1) * cell, gy + (f + 1) * cell, (250, 244, 226), TINTA, 3)
        for i in range(4):
            if "arriba" in lados and R["arriba"][i] is not None:
                h.texto((gx + i * cell + cell / 2, gy - 36), str(R["arriba"][i]), "courb", 46, AZUL)
            if "abajo" in lados and R["abajo"][i] is not None:
                h.texto((gx + i * cell + cell / 2, gy + 4 * cell + 38), str(R["abajo"][i]), "courb", 46, AZUL)
            if "izquierda" in lados and R["izquierda"][i] is not None:
                h.texto((gx - 38, gy + i * cell + cell / 2), str(R["izquierda"][i]), "courb", 46, AZUL)
            if "derecha" in lados and R["derecha"][i] is not None:
                h.texto((gx + 4 * cell + 38, gy + i * cell + cell / 2), str(R["derecha"][i]), "courb", 46, AZUL)
        if lados[0] == "arriba":
            for k, t in enumerate(("Alturas 1, 2, 3 y 4 en cada fila", "y en cada columna, sin repetir.", "El número del borde dice cuántos", "edificios se ven desde ahí:", "los altos tapan a los bajos.")):
                h.texto((315, 668 + k * 32), t, "cour", 25, TINTA)
        else:
            for k, t in enumerate(("Ejemplo: en una fila con alturas", "2, 1, 4 y 3, desde la izquierda", "se ven DOS edificios: el 2 y el 4", "(el 1 queda tapado por el 2 y", "el 3 por el 4).")):
                h.texto((315, 668 + k * 32), t, "cour", 25, TINTA)
        out.append(h.final(ruido=3, semilla=52))
    return out


def carta_manual():
    """Carta 70: el manual del desactivador con las cuatro reglas de los cables."""
    h = _fondo("MANUAL DEL DESACTIVADOR")
    h.texto((315, 150), "Cables contados de ARRIBA a ABAJO.", "cour", 25, TINTA)
    h.texto((315, 184), "Vale la PRIMERA regla que se cumpla.", "cour", 25, TINTA)
    reglas = [("1", "Si hay MÁS cables azules", "que rojos: corta el ÚLTIMO", "cable azul."),
              ("2", "Si no, y no hay ningún cable", "rojo y el último es amarillo:", "corta el PRIMER cable."),
              ("3", "Si no, y hay EXACTAMENTE UN", "cable blanco: corta el", "CUARTO cable."),
              ("4", "Si no: corta el ÚLTIMO cable", "negro (si no hay ninguno,", "el SEGUNDO cable).")]
    for i, (n, a, b, c) in enumerate(reglas):
        y = 250 + i * 138
        h.disco(84, y + 36, 30, ROJO, TINTA, 3)
        h.texto((84, y + 37), n, "courb", 40, (250, 244, 226))
        for k, t in enumerate((a, b, c)):
            h.texto((136, y + 8 + k * 32), t, "cour", 26, TINTA, "lm")
    return h.final(ruido=3, semilla=70)


MOSAICOS = {"cripto": ["15", "14"], "rejilla": ["31", "30"]}      # (la carta de abajo y la de encima; el orden no importa)
SUELTAS = {"40": carta_plano, "70": carta_manual}


def main(carpeta="juegos/aventuras-ca/espia"):
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    a, b = cartas_cripto()
    a.save(os.path.join(arte, "15.png"))
    b.save(os.path.join(arte, "14.png"))
    # imagen de comprobación: las dos hojas superpuestas (solo local)
    Image.fromarray(np.minimum(np.asarray(a), np.asarray(b))).save(os.path.join(arte, "superpuestas-cripto.png"))
    g, letras = cartas_rejilla()
    g.save(os.path.join(arte, "30.png"))
    letras.save(os.path.join(arte, "31.png"))
    Image.fromarray(np.minimum(np.asarray(g), np.asarray(letras))).save(os.path.join(arte, "superpuestas-rejilla.png"))
    for i, fn in SUELTAS.items():
        fn().save(os.path.join(arte, f"{i}.png"))
    c52, c53 = cartas_rascacielos()
    c52.save(os.path.join(arte, "52.png"))
    c53.save(os.path.join(arte, "53.png"))
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "codigos_espia.json")
    json.dump(CODIGOS, open(ruta, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print("láminas escritas en", arte, "y códigos en", ruta)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

"""Utilidades de dibujo por código compartidas por los dibujantes de láminas de los juegos (Hoja, colores y fuentes de estilo «papel»).

Nació para el Lejano Oeste y lo importan casi todos los dibujantes (arcade.py, cuento.py, dinosaurios.py, egipto.py, espia.py, futbol.py,
juguetes.py...). Las láminas del juego del Oeste las dibuja ahora herramientas/oeste_cartas.py."""
import json
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mosaicos import cortar  # noqa: E402

S = 2                                   # supersampling para que el dibujo salga suave
PAPEL = (236, 214, 168)
TINTA = (54, 36, 24)
ROJO = (170, 52, 40)
OCRE = (214, 160, 70)
ARENA = (224, 186, 124)
ARENA2 = (198, 154, 98)
MADERA = (146, 94, 58)
MADERA2 = (110, 72, 44)
HIERRO = (86, 88, 96)
NEGRO = (38, 32, 30)
BLANCO = (248, 242, 226)
PIEL = (216, 172, 126)
SOMBRERO = (96, 66, 42)

FUENTES = {"cartel": "C:/Windows/Fonts/impact.ttf", "texto": "C:/Windows/Fonts/georgiab.ttf", "texto2": "C:/Windows/Fonts/georgia.ttf"}
_cache = {}


def fuente(nombre, tam):
    k = (nombre, tam)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(FUENTES[nombre], int(tam * S))
    return _cache[k]


class Hoja:
    def __init__(self, w, h, fondo=PAPEL):
        self.w, self.h = w, h
        self.im = Image.new("RGB", (w * S, h * S), fondo)
        self.d = ImageDraw.Draw(self.im)

    def _p(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def poli(self, pts, fill, borde=None, ancho=3):
        self.d.polygon(self._p(pts), fill=fill)
        if borde:
            self.d.line(self._p(list(pts) + [pts[0]]), fill=borde, width=int(ancho * S), joint="curve")

    def rect(self, x0, y0, x1, y1, fill, borde=None, ancho=3):
        self.d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill, outline=borde, width=int(ancho * S) if borde else 0)

    def elip(self, x0, y0, x1, y1, fill, borde=None, ancho=3):
        self.d.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill, outline=borde, width=int(ancho * S) if borde else 0)

    def disco(self, cx, cy, r, fill, borde=None, ancho=3):
        self.elip(cx - r, cy - r, cx + r, cy + r, fill, borde, ancho)

    def linea(self, pts, color, ancho):
        self.d.line(self._p(pts), fill=color, width=int(ancho * S), joint="curve")

    def texto(self, xy, s, tipo, tam, color, ancla="mm", borde=None, ancho_borde=0):
        self.d.text((xy[0] * S, xy[1] * S), s, font=fuente(tipo, tam), fill=color, anchor=ancla,
                    stroke_width=int(ancho_borde * S), stroke_fill=borde)

    def degradado(self, y0, y1, c0, c1):
        for y in range(int(y0), int(y1)):
            t = (y - y0) / max(1, (y1 - y0 - 1))
            c = tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))
            self.d.rectangle([0, y * S, self.w * S, (y + 1) * S], fill=c)

    def final(self, ruido=0, semilla=1):
        im = self.im.resize((self.w, self.h), Image.LANCZOS)
        if ruido:
            a = np.asarray(im).astype(np.int16)
            rng = np.random.default_rng(semilla)
            a = a + rng.normal(0, ruido, a.shape[:2])[:, :, None]
            im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
        return im

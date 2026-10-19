"""Láminas de «La Final del Siglo, 1970» (fútbol): cromos con DOS CARAS, pizarra con pistas, jugadas del VAR, reglamento, clasificación e informe del entrenador.

Se dibujan por código con PIL a partir de herramientas/instancias_futbol.json (solución comprobada por fuerza bruta), así que los códigos son exactos:
  - cartas 14 a 19: cromos de jugadores; el anverso (14.png) solo enseña el dorsal y el nombre; el reverso (14r.png) tiene la ficha técnica;
  - cartas 30 y 31: la pizarra del rival (campo 1-2-2-1 y las pistas del espía repartidas en dos cartas);
  - cartas 40 y 41: cuatro jugadas del VAR; carta 42: el reglamento del fuera de juego;
  - cartas 52 y 53: la clasificación de la liguilla y los resultados conocidos; carta 70: el informe del entrenador sobre el portero rival.
Uso (desde la raíz del repo):  python herramientas/futbol.py [carpeta_juego]
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oeste  # noqa: E402
from oeste import Hoja  # noqa: E402

CREMA = (240, 230, 200)
TINTA = (40, 34, 30)
ROJO = (184, 36, 40)
AZUL = (30, 70, 160)
CESPED = (64, 132, 62)
CESPED2 = (58, 122, 56)
AMARILLO = (240, 200, 40)
BLANCO = (250, 248, 240)
PIZARRA = (28, 62, 48)


def _inst():
    return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_futbol.json"), encoding="utf-8"))


# ------------------------------------------------------------------ cromos
def _camiseta(h, cx, cy, s, col1, col2):
    """Camiseta de rayas verticales con cuello en V centrada en (cx, cy) y ancho s."""
    w = s / 2
    cuerpo = [(cx - w * 0.78, cy - s * 0.55), (cx + w * 0.78, cy - s * 0.55), (cx + w * 0.78, cy + s * 0.62), (cx - w * 0.78, cy + s * 0.62)]
    h.poli([(cx - w * 0.78, cy - s * 0.55), (cx - w * 1.5, cy - s * 0.2), (cx - w * 1.2, cy + s * 0.08), (cx - w * 0.78, cy - s * 0.1)], col1, TINTA, 4)
    h.poli([(cx + w * 0.78, cy - s * 0.55), (cx + w * 1.5, cy - s * 0.2), (cx + w * 1.2, cy + s * 0.08), (cx + w * 0.78, cy - s * 0.1)], col1, TINTA, 4)
    h.poli(cuerpo, col2, TINTA, 4)
    for k in range(-3, 4):
        x0 = cx + k * w * 0.22 - w * 0.11
        if k % 2 == 0:
            h.rect(x0, cy - s * 0.55 + 2, x0 + w * 0.22, cy + s * 0.62 - 2, col1)
    h.poli([(cx - w * 0.3, cy - s * 0.55), (cx + w * 0.3, cy - s * 0.55), (cx, cy - s * 0.3)], CREMA, TINTA, 4)


def cromo_anverso(c):
    h = Hoja(630, 882, CREMA)
    h.rect(24, 24, 606, 858, CREMA, ROJO, 8)
    h.rect(24, 24, 606, 150, ROJO)
    h.texto((315, 88), "CLUB ESTRELLA", "cartel", 64, CREMA)
    h.texto((315, 190), "CROMO OFICIAL", "texto", 26, ROJO)
    _camiseta(h, 315, 440, 420, ROJO, BLANCO)
    h.texto((315, 480), str(c["dorsal"]), "cartel", 230, TINTA, "mm", BLANCO, 6)
    h.rect(215, 650, 415, 720, (30, 50, 120), TINTA, 4)                      # pantalón
    h.texto((315, 770), c["nombre"].upper(), "cartel", 52, TINTA)
    return h.final(ruido=4, semilla=int(c["dorsal"]))


def cromo_reverso(c):
    h = Hoja(630, 882, (232, 222, 190))
    h.rect(24, 24, 606, 858, (232, 222, 190), TINTA, 6)
    h.rect(24, 24, 606, 130, AZUL)
    h.texto((315, 78), "FICHA TÉCNICA", "cartel", 58, CREMA)
    h.disco(96, 176, 32, ROJO, TINTA, 4)
    h.texto((96, 178), str(c["dorsal"]), "cartel", 36, CREMA)
    h.texto((350, 176), c["nombre"], "texto", 42, TINTA)
    filas = (("POSICIÓN", c["pos"]), ("PIE", c["pie"]), ("ALTURA", f"{c['altura'] // 100},{c['altura'] % 100:02d} m"), ("EDAD", f"{c['edad']} años"))
    for i, (k, v) in enumerate(filas):
        y = 296 + i * 124
        h.rect(54, y - 50, 576, y + 50, (244, 236, 212), TINTA, 3)
        h.texto((78, y - 22), k, "texto", 24, ROJO, "lm")
        h.texto((78, y + 18), v, "cartel", 46, TINTA, "lm")
    return h.final(ruido=4, semilla=int(c["dorsal"]) + 50)


def _envolver(txt, n):
    """Parte `txt` en líneas de como mucho n caracteres, cortando por espacios."""
    out, linea = [], ""
    for w in txt.split():
        if len(linea) + len(w) + (1 if linea else 0) > n:
            out.append(linea)
            linea = w
        else:
            linea = (linea + " " + w).strip()
    return out + [linea]


# ------------------------------------------------------------------ pizarra del rival
SLOT_XY = {"DEL": (315, 0.14), "MI": (190, 0.33), "MD": (440, 0.33), "DI": (190, 0.62), "DD": (440, 0.62), "P": (315, 0.86)}
SLOT_NOMBRE = {"DEL": "Delantero", "MI": "Medio izq.", "MD": "Medio dcha.", "DI": "Defensa izq.", "DD": "Defensa dcha.", "P": "Portero"}


def _campo_pizarra(h, x0, y0, ancho, alto):
    h.rect(x0, y0, x0 + ancho, y0 + alto, (40, 96, 62), BLANCO, 4)
    h.linea([(x0, y0 + alto / 2), (x0 + ancho, y0 + alto / 2)], BLANCO, 3)
    h.disco(x0 + ancho / 2, y0 + alto / 2, alto * 0.11, None or (40, 96, 62), BLANCO, 3)
    h.rect(x0 + ancho * 0.3, y0, x0 + ancho * 0.7, y0 + alto * 0.14, (40, 96, 62), BLANCO, 3)
    h.rect(x0 + ancho * 0.3, y0 + alto * 0.86, x0 + ancho * 0.7, y0 + alto, (40, 96, 62), BLANCO, 3)
    for s, (sx, sy) in SLOT_XY.items():
        px = x0 + ancho * (sx - 100) / 430 + (0)
        px = x0 + (sx - 160) / 310 * ancho * 0.8 + ancho * 0.1
        py = y0 + sy * alto
        h.disco(px, py, 22, (240, 240, 232), BLANCO, 3)
        h.texto((px, py + 36), SLOT_NOMBRE[s], "texto2", 17, BLANCO)


def carta_pizarra(n):
    I = _inst()
    pistas = I["alineacion"]["pistas"]
    mitad = (len(pistas) + 1) // 2
    mias = pistas[:mitad] if n == 1 else pistas[mitad:]
    h = Hoja(630, 882, PIZARRA)
    h.rect(22, 22, 608, 860, PIZARRA, (196, 150, 90), 12)
    h.texto((315, 76), "PIZARRA DEL RIVAL", "cartel", 50, (240, 240, 232))
    h.texto((315, 122), f"Pistas de nuestro espía ({n} de 2)", "texto2", 28, (222, 222, 210))
    _campo_pizarra(h, 130, 160, 370, 330)
    h.texto((315, 520), "Los Rayos atacan hacia arriba:", "texto2", 24, (222, 222, 210))
    h.texto((315, 550), "izquierda y derecha, mirando a la portería rival.", "texto2", 24, (222, 222, 210))
    y = 610
    for p in mias:
        lineas = _envolver(p, 34)
        h.texto((60, y), "•", "texto", 28, (240, 214, 120), "lm")
        for l in lineas:
            h.texto((88, y), l, "texto2", 26, (240, 240, 232), "lm")
            y += 34
        y += 18
    return h.final(ruido=3, semilla=30 + n)


# ------------------------------------------------------------------ VAR
ESC = 4.6                      # píxeles por metro
CAMPO_W, CAMPO_H = int(105 * ESC), int(68 * ESC)


def _campo(h, x0, y0):
    for k in range(7):
        h.rect(x0 + k * CAMPO_W / 7, y0, x0 + (k + 1) * CAMPO_W / 7, y0 + CAMPO_H, CESPED if k % 2 == 0 else CESPED2)
    h.rect(x0, y0, x0 + CAMPO_W, y0 + CAMPO_H, None or CESPED, BLANCO, 4)
    h.linea([(x0 + CAMPO_W / 2, y0), (x0 + CAMPO_W / 2, y0 + CAMPO_H)], BLANCO, 3)
    h.disco(x0 + CAMPO_W / 2, y0 + CAMPO_H / 2, 9.15 * ESC, None or CESPED, BLANCO, 3)
    for lado in (0, 1):
        ax = x0 if lado == 0 else x0 + CAMPO_W - 16.5 * ESC
        h.rect(ax, y0 + 13.84 * ESC, ax + 16.5 * ESC, y0 + 54.16 * ESC, None or CESPED, BLANCO, 3)
        gx = x0 if lado == 0 else x0 + CAMPO_W - 5.5 * ESC
        h.rect(gx, y0 + 24.84 * ESC, gx + 5.5 * ESC, y0 + 43.16 * ESC, None or CESPED, BLANCO, 3)
    h.rect(x0 + CAMPO_W, y0 + 30.34 * ESC, x0 + CAMPO_W + 10, y0 + 37.66 * ESC, BLANCO, TINTA, 2)      # portería rival


def _jugada(h, x0, y0, j):
    _campo(h, x0, y0)
    P = lambda x, y: (x0 + x * ESC, y0 + y * ESC)
    pase = next(a for a in j["ataca"] if a[0] == "pase")
    recibe = next(a for a in j["ataca"] if a[0] == "recibe")
    px, py = P(pase[1], pase[2])
    rx, ry = P(recibe[1], recibe[2])
    # flecha discontinua del pase
    L = math.hypot(rx - px, ry - py)
    ang = math.atan2(ry - py, rx - px)
    n = int(L // 18)
    for k in range(n):
        a, b = k * 18 / L, min(1, (k * 18 + 10) / L)
        h.linea([(px + (rx - px) * a, py + (ry - py) * a), (px + (rx - px) * b, py + (ry - py) * b)], BLANCO, 3)
    ex, ey = rx - 16 * math.cos(ang), ry - 16 * math.sin(ang)
    h.poli([(ex + 9 * math.cos(ang), ey + 9 * math.sin(ang)), (ex + 6 * math.cos(ang + 2.3), ey + 6 * math.sin(ang + 2.3)), (ex + 6 * math.cos(ang - 2.3), ey + 6 * math.sin(ang - 2.3))], BLANCO)
    for rol, x, y in j["defensas"]:
        cx, cy = P(x, y)
        h.disco(cx, cy, 10, AMARILLO if rol == "P" else ROJO, TINTA, 3)
    for rol, x, y in j["ataca"]:
        cx, cy = P(x, y)
        h.disco(cx, cy, 10, AZUL, BLANCO, 3)
    h.disco(px + 14, py + 10, 5, BLANCO, TINTA, 2)                       # el balón, junto a quien pasa
    h.texto((x0 + 12, y0 - 20), f"JUGADA {j['nombre']}", "cartel", 34, TINTA, "lm")


def carta_var(n):
    I = _inst()
    h = Hoja(630, 882, CREMA)
    h.rect(14, 14, 616, 868, CREMA, TINTA, 4)
    h.texto((315, 50), "VAR: REVISIÓN DE JUGADAS", "cartel", 36, TINTA)
    x0 = (630 - CAMPO_W) // 2
    for i, j in enumerate(I["var"][(n - 1) * 2:(n - 1) * 2 + 2]):
        _jugada(h, x0, 120 + i * 345, j)
    h.texto((315, 818), "Azul: atacan hacia la derecha · Rojo: defienden · Amarillo: portero", "texto2", 20, TINTA)
    return h.final(ruido=3, semilla=40 + n)


def carta_reglamento():
    h = Hoja(630, 882, CREMA)
    h.rect(14, 14, 616, 868, CREMA, TINTA, 4)
    h.texto((315, 56), "REGLAMENTO", "cartel", 46, ROJO)
    h.texto((315, 108), "EL FUERA DE JUEGO", "cartel", 36, TINTA)
    lineas = ["En el momento del pase, quien recibe", "está en FUERA DE JUEGO si está más cerca", "de la portería rival que el penúltimo", "defensor (el portero también cuenta)", "Y TAMBIÉN más cerca que el balón.", "Si no se cumplen las dos cosas,", "el gol es VÁLIDO."]
    for k, t in enumerate(lineas):
        h.texto((315, 170 + k * 38), t, "texto", 25, TINTA)
    # ejemplo
    esc, x0, y0, ancho, alto = 9.0, 55, 470, 520, 300
    h.rect(x0, y0, x0 + ancho, y0 + alto, CESPED, BLANCO, 4)
    h.texto((315, 450), "EJEMPLO (la portería está a la derecha)", "texto2", 22, TINTA)

    def X(m):
        return x0 + (m - 60) * esc
    h.rect(X(88.5), y0 + 40, X(105), y0 + alto - 40, CESPED, BLANCO, 3)
    for dx, dy, col in ((103, 150, AMARILLO), (86, 90, ROJO), (70, 210, ROJO)):
        h.disco(X(dx), y0 + dy, 12, col, TINTA, 3)
    h.linea([(X(86), y0 + 6), (X(86), y0 + alto - 6)], (250, 230, 120), 3)
    h.texto((X(86) - 6, y0 + 22), "penúltimo", "texto2", 20, (250, 230, 120), "rm")
    h.disco(X(95), y0 + 220, 12, AZUL, BLANCO, 3)
    h.texto((X(95), y0 + 252), "FUERA", "cartel", 24, BLANCO)
    h.disco(X(81), y0 + 40, 12, AZUL, BLANCO, 3)
    h.texto((X(81), y0 + 70), "VÁLIDO", "cartel", 24, BLANCO)
    h.disco(X(66), y0 + 120, 12, AZUL, BLANCO, 3)
    h.disco(X(66) + 16, y0 + 130, 5, BLANCO, TINTA, 2)
    h.texto((X(66) + 6, y0 + 152), "balón", "texto2", 20, BLANCO, "mm")
    h.texto((315, 815), "(los dos atacantes de la derecha reciben un pase del que lleva el balón)", "texto2", 19, TINTA)
    return h.final(ruido=3, semilla=42)


# ------------------------------------------------------------------ liguilla
def carta_tabla():
    I = _inst()["liguilla"]
    h = Hoja(630, 882, (26, 30, 36))
    h.rect(20, 20, 610, 862, (26, 30, 36), (196, 150, 90), 10)
    h.texto((315, 80), "CLASIFICACIÓN", "cartel", 56, CREMA)
    h.texto((315, 128), "Liguilla de cuatro equipos (todos contra todos)", "texto2", 26, (200, 200, 190))
    cols = (("EQUIPO", 70, "lm"), ("PJ", 330, "mm"), ("PTS", 410, "mm"), ("GF", 490, "mm"), ("GC", 565, "mm"))
    for k, x, a in cols:
        h.texto((x, 200), k, "cartel", 30, AMARILLO, a)
    h.linea([(46, 226), (584, 226)], (200, 200, 190), 3)
    for i, (nombre, (pts, gf, gc)) in enumerate(zip(I["equipos"], I["tabla"])):
        y = 290 + i * 100
        h.texto((70, y), nombre, "cartel", 42, CREMA, "lm")
        for (k, x, a), v in zip(cols[1:], (3, pts, gf, gc)):
            h.texto((x, y), str(v), "cartel", 46, (250, 250, 242), a)
        h.linea([(46, y + 46), (584, y + 46)], (90, 96, 104), 2)
    for k, t in enumerate(("PJ: partidos jugados · PTS: puntos", "GF: goles a favor · GC: goles en contra", "Victoria: 3 puntos · Empate: 1 · Derrota: 0")):
        h.texto((315, 700 + k * 40), t, "texto2", 26, (200, 200, 190))
    return h.final(ruido=3, semilla=52)


def carta_resultados():
    I = _inst()["liguilla"]
    eq, partidos, res = I["equipos"], I["partidos"], I["resultados"]
    h = Hoja(630, 882, CREMA)
    h.rect(16, 16, 614, 866, CREMA, TINTA, 4)
    h.texto((315, 66), "RESULTADOS CONOCIDOS", "cartel", 42, ROJO)
    for k, i in enumerate(I["conocidos"]):
        a, b = partidos[i]
        y = 170 + k * 70
        h.texto((315, y), f"{eq[a]}  {res[i][0]} - {res[i][1]}  {eq[b]}", "texto", 38, TINTA)
    h.linea([(60, 400), (570, 400)], TINTA, 3)
    h.texto((315, 450), "POR JUGAR (marcadores que faltan)", "cartel", 34, ROJO)
    for k, i in enumerate(I["desconocidos"]):
        a, b = partidos[i]
        y = 540 + k * 70
        h.texto((315, y), f"{eq[a]}  ? - ?  {eq[b]}", "texto", 38, TINTA)
    h.texto((315, 790), "El equipo de la izquierda es el local.", "texto2", 24, TINTA)
    return h.final(ruido=3, semilla=53)


# ------------------------------------------------------------------ informe del entrenador
def carta_informe():
    h = Hoja(630, 882, (232, 222, 190))
    h.rect(16, 16, 614, 866, (232, 222, 190), TINTA, 4)
    h.texto((315, 64), "INFORME DEL ENTRENADOR", "cartel", 42, ROJO)
    h.texto((315, 112), "El portero rival y sus manías", "texto", 28, TINTA)
    # portería con tres zonas
    gx0, gy0, gw, gh = 120, 150, 390, 150
    h.rect(gx0, gy0, gx0 + gw, gy0 + gh, (250, 250, 244), BLANCO, 4)
    for k in (1, 2):
        h.linea([(gx0 + gw * k / 3, gy0), (gx0 + gw * k / 3, gy0 + gh)], TINTA, 3)
    for k, t in enumerate(("IZQUIERDA", "CENTRO", "DERECHA")):
        h.texto((gx0 + gw * (k + 0.5) / 3, gy0 + gh / 2), t, "cartel", 28, TINTA)
    h.linea([(gx0 - 20, gy0 + gh), (gx0 + gw + 20, gy0 + gh)], TINTA, 6)
    h.texto((315, 335), "(vista desde el delantero que chuta)", "texto2", 22, TINTA)
    reglas = ["1. En el PRIMER penalti, el portero", "    se lanza a la IZQUIERDA.", "2. En los demás se lanza al lado al que", "    chutó el delantero en el penalti", "    ANTERIOR (si chutó al centro,", "    se queda en el centro).", "3. Es GOL si el delantero chuta a un", "    lado distinto del de la parada."]
    for k, tx in enumerate(reglas):
        h.texto((50, 385 + k * 40), tx, "texto", 25, TINTA, "lm")
    h.rect(50, 722, 580, 806, (244, 236, 212), ROJO, 4)
    h.texto((315, 748), "Hay que marcar los cinco penaltis y", "texto", 26, ROJO)
    h.texto((315, 782), "chutar al menos una vez al centro.", "texto", 26, ROJO)
    return h.final(ruido=3, semilla=70)


# ------------------------------------------------------------------ registro y salida
def main(carpeta="juegos/aventuras-ca/futbol"):
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    I = _inst()
    for carta, c in I["cromos"].items():
        cromo_anverso(c).save(os.path.join(arte, f"{carta}.png"))
        cromo_reverso(c).save(os.path.join(arte, f"{carta}r.png"))
    carta_pizarra(1).save(os.path.join(arte, "30.png"))
    carta_pizarra(2).save(os.path.join(arte, "31.png"))
    carta_var(1).save(os.path.join(arte, "40.png"))
    carta_var(2).save(os.path.join(arte, "41.png"))
    carta_reglamento().save(os.path.join(arte, "42.png"))
    carta_tabla().save(os.path.join(arte, "52.png"))
    carta_resultados().save(os.path.join(arte, "53.png"))
    carta_informe().save(os.path.join(arte, "70.png"))
    print("láminas escritas en", arte)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

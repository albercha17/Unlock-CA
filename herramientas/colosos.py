"""Láminas de «Altamuralla: El Valle de los Colosos» (60 cartas): todo se dibuja por código a partir de herramientas/instancias_colosos.json.

  - 16 plano de las torres · 18 nota del archivero · 19+21 crónica · 26 hoja de la sargento · 41 lista del intendente · 43 plano a medio hacer
  - 45 normas de los barracones · 42+49 piedra del viajero · 53 nota de la doctora · 54+55 tabla de dosis · 59 báscula y vara
  - 37 y 33 tejados · 39 paso del coloso · 61+63 cancionero · 70 ofrendas · 71 cuaderno · 75 y 79 placas · 66 baratijas · 67 cómo ordena
  - 86 inscripción · 87 placa de los cinco dibujos.
Además copia en cada minijuego (entre /*DATOS*/ y /*FIN*/) los datos de su instancia.
Uso (desde la raíz del repo):  python herramientas/colosos.py [carpeta_juego]
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oeste import Hoja, fuente  # noqa: E402
from mosaicos import cortar  # noqa: E402
from faro import parrafo, ruido  # noqa: E402
import instancias_colosos as IC  # noqa: E402

W, H = 630, 882
PERG = (238, 228, 204)
TINTA = (56, 38, 22)
AMBAR = (196, 126, 36)
ROJO = (150, 50, 36)
PIEDRA = (178, 174, 164)
PIEDRA2 = (120, 116, 108)
MURO = (88, 70, 54)
BLANCO = (252, 248, 238)
COL_PIEDRA = {"roja": (196, 60, 48), "azul": (52, 96, 176), "blanca": (244, 242, 232)}
COL_MAT = {"oro": (226, 178, 52), "plata": (192, 198, 206), "cobre": (190, 110, 60), "vidrio": (160, 222, 232)}
CARPETA = "juegos/aventuras-ca/colosos"


def _inst():
    return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_colosos.json"), encoding="utf-8"))


def papel(titulo, sub=None, col=TINTA, fondo=PERG, alto=H):
    p = Hoja(W, alto, fondo)
    p.rect(16, 16, W - 16, alto - 16, None, col, 4)
    p.rect(26, 26, W - 26, alto - 26, None, AMBAR, 1.5)
    p.texto((W / 2 + 30, 66), titulo, "cartel", 34, col)
    if sub:
        p.texto((W / 2 + 30, 104), sub, "texto2", 21, col)
    return p


def versos(p, lineas, y0, paso=40, tam=23, color=TINTA, tipo="texto2"):
    for k, v in enumerate(lineas):
        p.texto((W / 2, y0 + k * paso), v, tipo, tam, color)


def recuadro(p, x0, y0, x1, y1, titulo=None):
    p.rect(x0, y0, x1, y1, (250, 243, 226), AMBAR, 2.5)
    if titulo:
        p.texto(((x0 + x1) / 2, y0 + 26), titulo, "texto", 21, ROJO)


def flor(p, cx, cy, r, color=AMBAR):
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        p.disco(cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55, r * 0.45, color)
    p.disco(cx, cy, r * 0.3, (250, 230, 160))


def check(p, cx, cy, si, r=16):
    if si:
        p.disco(cx, cy, r, (60, 130, 70))
        p.linea([(cx - r * .5, cy), (cx - r * .1, cy + r * .45), (cx + r * .55, cy - r * .45)], BLANCO, 4)
    else:
        p.disco(cx, cy, r, (170, 50, 40))
        p.linea([(cx - r * .45, cy - r * .45), (cx + r * .45, cy + r * .45)], BLANCO, 4)
        p.linea([(cx + r * .45, cy - r * .45), (cx - r * .45, cy + r * .45)], BLANCO, 4)


# ------------------------------------------------------------------ 14 · faroles
def plano_torres(i):
    fa = i["faroles"]
    n = fa["n"]
    p = papel("EL PLANO DE LAS TORRES", "Camino de ronda de la muralla norte")
    t = 66
    x0, y0 = (W - n * t) / 2, 170
    muros = {tuple(m) for m in fa["muros"]}
    nums = {(f, c): k for f, c, k in fa["numeros"]}
    for f in range(n):
        p.texto((x0 - 18, y0 + f * t + t / 2), str(f + 1), "texto", 18, TINTA)
        for c in range(n):
            if f == 0:
                p.texto((x0 + c * t + t / 2, y0 - 16), IC.LET[c], "texto", 18, TINTA)
            x, y = x0 + c * t, y0 + f * t
            if (f, c) in muros:
                p.rect(x + 2, y + 2, x + t - 2, y + t - 2, MURO, (40, 30, 22), 2)
                if (f, c) in nums:
                    p.texto((x + t / 2, y + t / 2), str(nums[(f, c)]), "cartel", 34, BLANCO)
            else:
                p.rect(x + 2, y + 2, x + t - 2, y + t - 2, (236, 222, 190), (190, 170, 130), 1.5)
    y = y0 + n * t + 40
    recuadro(p, 60, y, W - 60, H - 50, "ORDEN DE LA SARGENTO")
    parrafo(p, 84, y + 66, 470, "Que no quede ni una losa a oscuras. Un farol alumbra en línea recta hasta la primera torre. Dos faroles que se ven "
            "se deslumbran: no los pongáis. El número de cada torre dice cuántos faroles tiene pegados a sus lados.", tam=19)
    return p.final()


# ------------------------------------------------------------------ 20 · crónica
def nota_archivero(i):
    cr = i["cronica"]
    p = papel("NOTA DEL ARCHIVERO", "Pegada en la tapa de la crónica")
    flor(p, W / 2, 190, 34, (200, 170, 120))
    y = 270
    parrafo(p, 70, y, 470, "La crónica se mojó y las hojas se mezclaron. De memoria recuerdo solo esto:", tam=22)
    y = 380
    for c in cr["nota"]:
        p.disco(80, y, 6, AMBAR)
        y = parrafo(p, 100, y, 470, IC.texto_pista_cronica(c), tipo="texto", tam=22) + 26
    recuadro(p, 60, H - 250, W - 60, H - 50, "LOS SEIS SUCESOS")
    for k, s in enumerate(IC.SUCESOS):
        p.texto((W / 2, H - 190 + k * 23), s, "texto2", 19, TINTA)
    return p.final()


def cronica(i):
    cr = i["cronica"]
    p = papel("LA CRÓNICA DE ALTAMURALLA", "Lo que se salvó de la tinta corrida", alto=2 * H)
    for mitad, lista in ((0, cr["cronica_arriba"]), (1, cr["cronica_abajo"])):
        y = (180 if mitad == 0 else H + 90)
        for c in lista:
            p.rect(60, y - 34, W - 60, y + 80, (246, 236, 212), (200, 170, 120), 1.5)
            parrafo(p, 80, y, 470, IC.texto_pista_cronica(c), tipo="texto", tam=23)
            y += 150
        flor(p, W / 2, (H - 110) if mitad == 0 else (2 * H - 110), 28, (210, 180, 130))
    return p.final()


# ------------------------------------------------------------------ 51 · hoja de la sargento y cancionero
def hoja_sargento(i):
    ca = i["canto"]
    s = ca["nota_sargento"][0]
    p = papel("LO QUE CANTAN LOS COLOSOS", "Escrito por Ruth, a los nueve años")
    versos(p, [f"Si el coloso canta {s},", f"tú contéstale «{ca['traduccion'][s]}»,", "y no tengas miedo, que él", "solo quiere conversar.",
               "", "Canta tres veces seguidas,", "cada vez un poco más;", "en la última, Ruth, recuerda:", "se contesta del final",
               "hacia el principio, al revés."], 230, paso=42, tam=24)
    flor(p, W / 2, H - 120, 34)
    return p.final()


def cancionero(i):
    ca = i["canto"]
    p = papel("EL CANCIONERO DE LA DOCTORA", "Sonidos de los colosos y su respuesta", alto=2 * H)
    sons = ca["cancionero"]
    pos = [(230, 0), (560, 0), (H + 200, 1)]
    for (y, _), s in zip(pos, sons):
        p.rect(70, y - 80, W - 70, y + 140, (246, 236, 212), (200, 170, 120), 2)
        p.texto((W / 2, y - 40), f"Cuando cantan {s.upper()}", "texto", 26, ROJO)
        # onda dibujada
        pts = []
        for k in range(120):
            x = 120 + k * 3.3
            a = {"grave": 22, "agudo": 10, "largo": 16, "doble": 18}[s]
            fq = {"grave": 0.08, "agudo": 0.45, "largo": 0.12, "doble": 0.25}[s]
            env = 1 if s != "doble" else (1 if (k // 30) % 2 == 0 else 0.15)
            pts.append((x, y + 20 + a * env * math.sin(k * fq)))
        p.linea(pts, TINTA, 3)
        p.texto((W / 2, y + 100), f"responded «{ca['traduccion'][s]}»", "texto2", 26, TINTA)
    parrafo(p, 80, H + 520, 470, "Apunte: el cuarto sonido me lo enseñó una niña de la guardia, hace años. Nunca lo apunté.", tam=21)
    flor(p, W / 2, 2 * H - 120, 30)
    return p.final()


# ------------------------------------------------------------------ 40 · barracones
def lista_intendente(i):
    ba = i["barracones"]
    p = papel("LISTA DEL INTENDENTE", "Camas que ya están asignadas")
    y = 200
    for f, c, k in ba["lista"]:
        p.linea([(80, y + 18), (W - 80, y + 18)], (200, 180, 140), 1)
        p.texto((90, y), f"Cama {IC.ref(f, c)}", "texto", 25, TINTA, "lm")
        p.texto((W - 90, y), f"barracón de {k}", "texto2", 25, TINTA, "rm")
        y += 66
    parrafo(p, 80, H - 120, 470, "(Columna con letra, fila con número, como en el plano)", tam=19)
    return p.final()


def plano_barracones(i):
    ba = i["barracones"]
    n = ba["n"]
    p = papel("PLANO A MEDIO HACER", "Barracones de la plaza")
    t = 80
    x0, y0 = (W - n * t) / 2, 170
    nums = {(f, c): k for f, c, k in ba["plano"]}
    for f in range(n):
        p.texto((x0 - 18, y0 + f * t + t / 2), str(f + 1), "texto", 20, TINTA)
        for c in range(n):
            if f == 0:
                p.texto((x0 + c * t + t / 2, y0 - 16), IC.LET[c], "texto", 20, TINTA)
            x, y = x0 + c * t, y0 + f * t
            p.rect(x, y, x + t, y + t, (244, 232, 206), (140, 110, 80), 1.5)
            if (f, c) in nums:
                p.texto((x + t / 2, y + t / 2), str(nums[(f, c)]), "cartel", 38, ROJO)
    parrafo(p, 80, y0 + n * t + 50, 470, "Lo demás lo tengo en la lista, que no sé dónde la he dejado.", tam=21)
    return p.final()


def normas_barracones(i):
    p = papel("LAS NORMAS DE SIEMPRE", "Del intendente, que las repite cada noche")
    versos(p, ["En cada cama, un número:", "el de camas de su barracón.", "Si el barracón es de cuatro,", "cuatro casillas, ni una más,",
               "pegadas lado con lado,", "y las cuatro dicen «cuatro».", "", "Dos barracones iguales", "no se tocan por un lado:",
               "de esquina, pase; de lado, no.", "Y todas las camas, llenas:", "no queda una sin barracón."], 210, paso=42, tam=24)
    return p.final()


# ------------------------------------------------------------------ 48 · piedra del viajero
def glifo(p, cx, cy, tam, g, color=TINTA, ancho=4):
    x0, y0 = cx - tam / 2, cy - tam / 2
    for t in g:
        if t[0] == "l":
            p.linea([(x0 + t[1] * tam, y0 + t[2] * tam), (x0 + t[3] * tam, y0 + t[4] * tam)], color, ancho)
        elif t[0] == "c":
            p.elip(x0 + (t[1] - t[3]) * tam, y0 + (t[2] - t[3]) * tam, x0 + (t[1] + t[3]) * tam, y0 + (t[2] + t[3]) * tam, None, color, ancho)
        else:
            p.disco(x0 + t[1] * tam, y0 + t[2] * tam, ancho * 1.1, color)


def frase(p, i, glifos, y, tam=56, color=(50, 46, 40)):
    ins = i["inscripcion"]
    n = len(glifos)
    paso = tam + 18
    x = W / 2 - (n - 1) * paso / 2
    for k, w in enumerate(glifos):
        glifo(p, x + k * paso, y, tam, i["glifos"][ins["forma"][w]], color)


def piedra(i):
    ins = i["inscripcion"]
    p = Hoja(W, 2 * H, (150, 146, 138))
    p.rect(16, 16, W - 16, 2 * H - 16, None, (70, 66, 60), 4)
    p.texto((W / 2 + 30, 66), "LA PIEDRA DEL VIAJERO", "cartel", 34, (40, 36, 32))
    p.texto((W / 2 + 30, 104), "Sótano de la doctora Marván", "texto2", 21, (40, 36, 32))
    ys = [260, 560, H + 160, H + 480]
    for y, e in zip(ys, ins["ejemplos"][:4]):
        p.rect(50, y - 70, W - 50, y + 140, (190, 186, 176), (100, 96, 88), 2)
        frase(p, i, e["glifos"], y)
        p.texto((W / 2, y + 95), e["es"], "texto", 24, (40, 36, 32))
        flor(p, W - 80, y - 46, 14, (110, 104, 92))
    return p.final()


def nota_doctora(i):
    ins = i["inscripcion"]
    p = papel("NOTA DE LA DOCTORA", "Lo que llevo traducido")
    e = ins["ejemplos"][4]
    recuadro(p, 50, 160, W - 50, 400, "ESTA YA LA TENGO")
    frase(p, i, e["glifos"], 270, tam=50)
    p.texto((W / 2, 360), e["es"], "texto", 23, TINTA)
    recuadro(p, 50, 450, W - 50, 700, "ESTA ME FALTA ESCRIBIRLA")
    p.texto((W / 2, 560), ins["objetivo"]["es"], "texto", 26, ROJO)
    p.texto((W / 2, 630), "(con los signos del viajero, en su orden)", "texto2", 19, TINTA)
    parrafo(p, 70, 760, 470, "Todas las frases las firma con la misma flor de cinco pétalos. ¿Quién era?", tam=20)
    return p.final()


# ------------------------------------------------------------------ 52 · dosis
def tabla_dosis(i):
    do = i["dosis"]
    p = papel("TABLA DE DOSIS DEL SUERO", "Mililitros para un coloso de quince metros", alto=2 * H)
    cw, rh = 88, 112
    x0 = W / 2 - (len(do["alturas"]) * cw + 110) / 2 + 110

    def cabecera(y):
        p.texto((x0 - 56, y), "kg / cm", "texto", 18, TINTA)
        for j, a in enumerate(do["alturas"]):
            p.rect(x0 + j * cw, y - 26, x0 + (j + 1) * cw, y + 26, (226, 196, 140), (140, 110, 70), 1.5)
            p.texto((x0 + j * cw + cw / 2, y), f"{a}-{a + 9}", "texto", 19, TINTA)

    for mitad in (0, 1):
        ytop = 190 if mitad == 0 else H + 90
        cabecera(ytop)
        filas = list(range(5)) if mitad == 0 else list(range(5, 10))
        for k, r in enumerate(filas):
            y = ytop + 60 + k * rh
            peso = do["pesos"][r]
            p.rect(x0 - 110, y - rh / 2 + 6, x0, y + rh / 2 - 6, (226, 196, 140), (140, 110, 70), 1.5)
            p.texto((x0 - 55, y), f"{peso}-{peso + 4}", "texto", 20, TINTA)
            for j in range(len(do["alturas"])):
                p.rect(x0 + j * cw, y - rh / 2 + 6, x0 + (j + 1) * cw, y + rh / 2 - 6, (250, 244, 228), (180, 150, 110), 1.2)
                p.texto((x0 + j * cw + cw / 2, y), str(do["tabla"][r][j]), "cartel", 30, ROJO)
    return p.final()


def bascula(i):
    do = i["dosis"]
    p = papel("LA BÁSCULA Y LA VARA", "Medidas tomadas por la doctora")
    # dos esferas de báscula
    for k, (nombre, d) in enumerate((("Cristina", do["cristina"]), ("Alberto", do["alberto"]))):
        cx, cy, r = 150, 270 + k * 300, 118
        p.disco(cx, cy, r + 10, (110, 80, 50))
        p.disco(cx, cy, r, (250, 246, 234), (60, 44, 30), 3)
        lo, hi = 40, 100
        for v in range(lo, hi + 1):
            a = math.radians(-225 + (v - lo) / (hi - lo) * 270)
            l = 18 if v % 10 == 0 else (12 if v % 5 == 0 else 7)
            p.linea([(cx + math.cos(a) * (r - 6), cy + math.sin(a) * (r - 6)), (cx + math.cos(a) * (r - 6 - l), cy + math.sin(a) * (r - 6 - l))],
                    TINTA, 2.4 if v % 10 == 0 else 1.2)
            if v % 10 == 0:
                p.texto((cx + math.cos(a) * (r - 40), cy + math.sin(a) * (r - 40)), str(v), "texto", 17, TINTA)
        a = math.radians(-225 + (d["peso"] - lo) / (hi - lo) * 270)
        p.linea([(cx, cy), (cx + math.cos(a) * (r - 10), cy + math.sin(a) * (r - 10))], ROJO, 3.5)
        p.disco(cx, cy, 8, ROJO)
        p.texto((cx, cy + r + 30), nombre, "texto", 22, TINTA)
        p.texto((cx, cy + 52), "kg", "texto2", 16, TINTA)
    # la vara de medir
    x, ytop, ybot = 440, 160, 790
    lo, hi = 145, 195
    escala = (ybot - ytop) / (hi - lo)
    p.rect(x - 22, ytop - 10, x + 22, ybot + 10, (214, 176, 116), (110, 80, 50), 2)
    for v in range(lo, hi + 1):
        y = ybot - (v - lo) * escala
        l = 20 if v % 10 == 0 else (13 if v % 5 == 0 else 7)
        p.linea([(x - 22, y), (x - 22 + l, y)], TINTA, 2 if v % 5 == 0 else 1)
        if v % 10 == 0:
            p.texto((x + 6, y), str(v), "texto", 15, TINTA, "lm")
    for nombre, d, dx in (("Cristina", do["cristina"], 1), ("Alberto", do["alberto"], 1)):
        y = ybot - (d["altura"] - lo) * escala
        p.linea([(x + 24, y), (x + 70, y)], ROJO, 3)
        p.poli([(x + 24, y), (x + 36, y - 7), (x + 36, y + 7)], ROJO)
        p.texto((x + 76, y), nombre, "texto", 18, ROJO, "lm")
    p.texto((x, ybot + 40), "cm", "texto2", 17, TINTA)
    return p.final()


# ------------------------------------------------------------------ 46 · pisadas
def tejados(i, filas, titulo, sub):
    pi = i["pisadas"]
    n = pi["n"]
    p = papel(titulo, sub)
    t = 86
    x0, y0 = (W - n * t) / 2, 200
    for k, f in enumerate(filas):
        p.texto((x0 - 18, y0 + k * t + t / 2), str(f + 1), "texto", 20, TINTA)
        for c in range(n):
            if k == 0:
                p.texto((x0 + c * t + t / 2, y0 - 16), IC.LET[c], "texto", 20, TINTA)
            x, y = x0 + c * t, y0 + k * t
            p.rect(x + 3, y + 3, x + t - 3, y + t - 3, (196, 84, 60), (110, 40, 28), 2)
            p.poli([(x + 3, y + 3), (x + t / 2, y + t * 0.32), (x + t - 3, y + 3)], (220, 110, 80))
            p.disco(x + t / 2, y + t * 0.62, 22, (250, 238, 214), (110, 40, 28), 2)
            p.texto((x + t / 2, y + t * 0.62), str(pi["numeros"][f][c]), "cartel", 28, TINTA)
    parrafo(p, 80, y0 + 3 * t + 60, 470, "Cada tejado lleva pintado el número de su familia. Desde arriba, un coloso los ve todos.", tam=21)
    return p.final()


def paso_coloso(i):
    p = papel("EL PASO DEL COLOSO", "De la libreta de la doctora")
    versos(p, ["Pisa solo cobertizos:", "donde no pisas, hay gente,", "y en una fila o columna", "ninguna familia se repite.", "",
               "No pises dos veces juntas,", "de lado no, que se hunde el suelo;", "de esquina, sí puedes.", "",
               "Y la ciudad que no pisas", "ha de quedar toda unida:", "que se pueda ir de casa en casa."], 210, paso=42, tam=24)
    return p.final()


# ------------------------------------------------------------------ 69 · ofrendas
def piedra_dib(p, cx, cy, color, forma, r=26):
    c = COL_PIEDRA[color]
    if forma == "redonda":
        p.disco(cx, cy, r, c, (40, 34, 28), 2.5)
    else:
        p.poli([(cx, cy - r * 1.15), (cx + r, cy + r * 0.8), (cx - r, cy + r * 0.8)], c, (40, 34, 28), 2.5)


def fila_ofrenda(p, y, piedras, acepta, etiqueta=None):
    p.rect(70, y - 42, W - 70, y + 42, (246, 236, 212), (200, 170, 120), 1.5)
    for k, (col, fo) in enumerate(piedras):
        piedra_dib(p, 200 + k * 90, y, col, fo)
    check(p, W - 130, y, acepta, 22)
    if etiqueta:
        p.texto((110, y), etiqueta, "texto", 20, TINTA)


def ofrendas_doctora(i):
    of = i["ofrendas"]
    p = papel("LAS OFRENDAS", "Lo que el Coloso Viejo aceptó y lo que no")
    y = 180
    for e in of["ejemplos_70"]:
        fila_ofrenda(p, y, e["piedras"], e["acepta"])
        y += 96
    return p.final()


def cuaderno_doctora(i):
    of = i["ofrendas"]
    p = papel("CUADERNO DE LA DOCTORA", "Tres ofrendas más, del último otoño")
    y = 230
    for e in of["ejemplos_71"]:
        fila_ofrenda(p, y, e["piedras"], e["acepta"])
        y += 110
    parrafo(p, 80, y + 40, 470, "Siempre las coloca en fila, de izquierda a derecha, y mira mucho la del centro. Las puntiagudas las llamo «picudas».",
            tam=21)
    recuadro(p, 80, H - 170, W - 80, H - 60)
    piedra_dib(p, 150, H - 115, "roja", "redonda", 20)
    p.texto((185, H - 115), "redonda", "texto2", 18, TINTA, "lm")
    piedra_dib(p, 360, H - 112, "azul", "picuda", 20)
    p.texto((395, H - 115), "picuda", "texto2", 18, TINTA, "lm")
    return p.final()


# ------------------------------------------------------------------ 72 · palancas
def placa(i, etapas, titulo):
    pa = i["palancas"]
    p = papel(titulo, "Maquinaria de la Torre del Reloj", fondo=(214, 186, 120), col=(60, 40, 18))
    y = 170
    for e in etapas:
        p.texto((W / 2, y), f"ETAPA {e + 1}", "cartel", 28, (100, 40, 20))
        y += 40
        for d, r in enumerate(pa["reglas"][e]):
            y = parrafo(p, 70, y, 470, f"Esfera en {d + 1}: {IC.texto_regla(r)}.", tam=20, color=(50, 32, 14), inter=1.25) + 6
        y += 26
    if len(etapas) == 2:
        parrafo(p, 70, y + 10, 470, "Las palancas se cuentan de izquierda a derecha. Si os equivocáis, la torre vuelve a la etapa 1.", tam=19,
                color=(50, 32, 14))
    return p.final()


# ------------------------------------------------------------------ 64 · tesoro
def baratija(p, cx, cy, tipo, material, muescas, r=34):
    c = COL_MAT[material]
    os_ = (60, 44, 30)
    if tipo == "anillo":
        p.elip(cx - r, cy - r * 0.8, cx + r, cy + r * 0.8, None, c, 9)
        p.elip(cx - r, cy - r * 0.8, cx + r, cy + r * 0.8, None, os_, 1.5)
        p.disco(cx, cy - r * 0.8, 9, (120, 200, 240), os_, 1.5)
    elif tipo == "moneda":
        p.disco(cx, cy, r, c, os_, 2.5)
        p.disco(cx, cy, r * 0.65, None, os_, 1.5)
    elif tipo == "llave":
        p.disco(cx - r * 0.55, cy, r * 0.42, c, os_, 2.5)
        p.disco(cx - r * 0.55, cy, r * 0.16, (246, 236, 212))
        p.rect(cx - r * 0.15, cy - 6, cx + r, cy + 6, c, os_, 2)
        p.rect(cx + r * 0.55, cy + 6, cx + r * 0.75, cy + 18, c, os_, 2)
    else:
        p.poli([(cx - r * 0.25, cy - r * 0.8), (cx + r * 0.25, cy - r * 0.8), (cx + r * 0.8, cy + r * 0.6), (cx - r * 0.8, cy + r * 0.6)], c, os_, 2.5)
        p.disco(cx, cy + r * 0.75, 7, c, os_, 2)
    for k in range(muescas):
        x = cx - (muescas - 1) * 9 + k * 18
        p.linea([(x, cy - r - 18), (x, cy - r - 4)], (40, 30, 22), 3.5)


def baratijas(i):
    te = i["tesoro"]
    p = papel("EL TESORO DEL COLOSO VIEJO", "Dieciséis baratijas brillantes")
    t = 132
    x0, y0 = (W - 4 * t) / 2, 150
    for k, o in enumerate(te["objetos"]):
        f, c = divmod(k, 4)
        x, y = x0 + c * t, y0 + f * t
        p.rect(x + 4, y + 4, x + t - 4, y + t - 4, (246, 236, 212), (200, 170, 120), 1.5)
        p.texto((x + 20, y + 22), o["letra"], "cartel", 22, ROJO)
        baratija(p, x + t / 2 + 6, y + t / 2 + 16, o["tipo"], o["material"], o["muescas"])
    y = y0 + 4 * t + 26
    for k, m in enumerate(IC.MATERIALES):
        x = 90 + k * 125
        p.disco(x, y + 10, 14, COL_MAT[m], (60, 44, 30), 2)
        p.texto((x + 22, y + 10), m, "texto2", 19, TINTA, "lm")
    p.texto((W / 2, y + 52), "Las rayitas de encima son las muescas.", "texto2", 19, TINTA)
    return p.final()


def como_ordena(i):
    te = i["tesoro"]
    p = papel("CÓMO ORDENA SU TESORO", "Lo que apuntó la doctora en tres veranos")
    parrafo(p, 70, 180, 470, "El Coloso Viejo hace siempre cuatro montones de cuatro, y en cada montón pone...", tam=22)
    y = 300
    for k, c in enumerate(te["condiciones"]):
        p.rect(60, y - 40, W - 60, y + 60, (246, 236, 212), (200, 170, 120), 1.5)
        p.texto((90, y + 10), str(k + 1), "cartel", 30, ROJO)
        parrafo(p, 125, y + 10, 420, c[0].upper() + c[1:] + ".", tipo="texto", tam=22)
        y += 120
    parrafo(p, 70, y + 20, 470, "Nunca pone una baratija en dos montones.", tam=21)
    return p.final()


# ------------------------------------------------------------------ 85 · meta
def inscripcion_camara(i):
    me = i["meta"]
    rej = me["rejilla"]
    p = papel("LA INSCRIPCIÓN DE LA CÁMARA", "Grabada alrededor de la flor")
    filas, cols = len(rej), len(rej[0])
    t = 58
    x0, y0 = (W - cols * t) / 2 + 10, 190
    for c in range(cols):
        p.texto((x0 + c * t + t / 2, y0 - 18), str(c + 1), "texto", 18, ROJO)
    for f in range(filas):
        p.texto((x0 - 20, y0 + f * t + t / 2), str(f + 1), "texto", 18, ROJO)
        for c in range(cols):
            x, y = x0 + c * t, y0 + f * t
            p.rect(x + 2, y + 2, x + t - 2, y + t - 2, (232, 220, 190), (170, 140, 100), 1.2)
            ch = rej[f][c]
            if ch == "·":
                flor(p, x + t / 2, y + t / 2, 12, (200, 170, 120))
            else:
                p.texto((x + t / 2, y + t / 2), ch, "cartel", 30, TINTA)
    return p.final()


def icono(p, nombre, cx, cy):
    if nombre == "52":    # jeringuilla
        p.rect(cx - 14, cy - 40, cx + 14, cy + 26, (230, 240, 240), TINTA, 2.5)
        p.rect(cx - 12, cy - 6, cx + 12, cy + 24, (230, 170, 60))
        p.linea([(cx, cy + 26), (cx, cy + 52)], TINTA, 2.5)
        p.rect(cx - 24, cy - 46, cx + 24, cy - 40, TINTA)
    elif nombre == "14":  # farol
        p.poli([(cx - 22, cy - 30), (cx + 22, cy - 30), (cx + 16, cy + 30), (cx - 16, cy + 30)], (250, 210, 110), TINTA, 3)
        p.rect(cx - 26, cy - 40, cx + 26, cy - 30, TINTA)
        p.rect(cx - 20, cy + 30, cx + 20, cy + 38, TINTA)
        p.disco(cx, cy, 8, (255, 160, 40))
    elif nombre == "48":  # piedra con signo
        p.poli([(cx - 34, cy + 36), (cx - 30, cy - 30), (cx, cy - 42), (cx + 30, cy - 30), (cx + 34, cy + 36)], PIEDRA, PIEDRA2, 3)
        flor(p, cx, cy, 16, PIEDRA2)
    elif nombre == "20":  # libro
        p.poli([(cx - 40, cy - 26), (cx, cy - 18), (cx, cy + 34), (cx - 40, cy + 26)], (246, 236, 212), TINTA, 3)
        p.poli([(cx + 40, cy - 26), (cx, cy - 18), (cx, cy + 34), (cx + 40, cy + 26)], (246, 236, 212), TINTA, 3)
        for k in range(3):
            p.linea([(cx - 32, cy - 10 + k * 11), (cx - 8, cy - 6 + k * 11)], TINTA, 1.5)
    else:                 # barracón
        p.poli([(cx - 40, cy - 4), (cx, cy - 40), (cx + 40, cy - 4)], (170, 70, 50), TINTA, 3)
        p.rect(cx - 32, cy - 4, cx + 32, cy + 36, (196, 150, 100), TINTA, 3)
        p.rect(cx - 9, cy + 10, cx + 9, cy + 36, (90, 60, 40))


def placa_dibujos(i):
    me = i["meta"]
    p = papel("LA PLACA DE LOS CINCO DIBUJOS", "Debajo del teclado del panel")
    t = 110
    x0 = (W - 5 * t) / 2
    for k, app in enumerate(me["orden"]):
        cx = x0 + k * t + t / 2
        p.rect(cx - 48, 230, cx + 48, 360, (246, 236, 212), (200, 170, 120), 2)
        icono(p, app, cx, 295)
    versos(p, ["Cada dibujo, un recuerdo;", "cada recuerdo, dos cifras:", "la primera, la fila;", "la segunda, la columna.", "",
               "Leed de izquierda a derecha", "y sabréis adónde vuelve", "quien sigue la flor."], 450, paso=42, tam=24)
    return p.final()


# ------------------------------------------------------------------ datos de los minijuegos
DATOS_MINIJUEGOS = {
    "14-faroles.js": lambda i: {"n": i["faroles"]["n"], "muros": i["faroles"]["muros"], "solucion": i["faroles"]["solucion"],
                                "marca": i["meta"]["marcas"]["14"]},
    "20-cronica.js": lambda i: {"sucesos": i["cronica"]["sucesos"], "solucion": i["cronica"]["solucion"], "marca": i["meta"]["marcas"]["20"]},
    "40-barracones.js": lambda i: {"n": i["barracones"]["n"], "solucion": i["barracones"]["solucion"], "marca": i["meta"]["marcas"]["40"]},
    "48-inscripcion.js": lambda i: {"glifos": i["glifos"], "forma": i["inscripcion"]["forma"], "objetivo": i["inscripcion"]["objetivo"]["glifos"],
                                    "marca": i["meta"]["marcas"]["48"]},
    "52-dosis.js": lambda i: {"dosis": i["dosis"]["dosis"], "marca": i["meta"]["marcas"]["52"]},
    "46-pisadas.js": lambda i: {"n": i["pisadas"]["n"], "solucion": i["pisadas"]["solucion"]},
    "51-canto.js": lambda i: {"rondas": i["canto"]["rondas"], "solucion": i["canto"]["solucion"], "respuestas": i["canto"]["respuestas"]},
    "69-ofrendas.js": lambda i: {"prueba": i["ofrendas"]["prueba"], "solucion": i["ofrendas"]["solucion"]},
    "72-palancas.js": lambda i: {"simbolos": i["palancas"]["simbolos"], "reglas": i["palancas"]["reglas"]},
    "64-tesoro.js": lambda i: {"objetos": [{"letra": o["letra"], "tipo": o["tipo"]} for o in i["tesoro"]["objetos"]], "grupos": i["tesoro"]["grupos"]},
    "85-panel.js": lambda i: {"palabra": i["meta"]["palabra"]},
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


def main(carpeta=CARPETA):
    inst = _inst()
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)
    laminas = {"16": plano_torres(inst), "18": nota_archivero(inst), "26": hoja_sargento(inst), "41": lista_intendente(inst),
               "43": plano_barracones(inst), "45": normas_barracones(inst), "53": nota_doctora(inst), "59": bascula(inst),
               "37": tejados(inst, [0, 1, 2], "LOS TEJADOS DEL NORTE", "Filas 1 a 3 de la plaza"),
               "33": tejados(inst, [3, 4, 5], "LOS TEJADOS DEL SUR", "Filas 4 a 6 de la plaza"), "39": paso_coloso(inst),
               "70": ofrendas_doctora(inst), "71": cuaderno_doctora(inst), "75": placa(inst, [0, 1, 2], "LA PRIMERA PLACA"),
               "79": placa(inst, [3, 4], "LA SEGUNDA PLACA"), "66": baratijas(inst), "67": como_ordena(inst), "86": inscripcion_camara(inst),
               "87": placa_dibujos(inst)}
    for k, im in laminas.items():
        ruido(im, int(k)).save(os.path.join(arte, f"{k}.png"))

    def mosaico(nombre, im, cartas):
        im = ruido(im, sum(map(ord, nombre)))
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))
        for pieza, k in zip(cortar(im, 2, 1), cartas):
            pieza.save(os.path.join(arte, f"{k}.png"))
    mosaico("cronica", cronica(inst), ("19", "21"))
    mosaico("piedra", piedra(inst), ("42", "49"))
    mosaico("dosis", tabla_dosis(inst), ("54", "55"))
    mosaico("cancionero", cancionero(inst), ("61", "63"))
    inyectar_datos(carpeta, inst)
    print("láminas escritas en", arte)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

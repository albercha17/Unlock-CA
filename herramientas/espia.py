"""Láminas de «Montecarlo, 1965: Operación Cristal» (versión de 60 cartas, 22 oct 2026). Todas las pistas son dibujos o acertijos: ninguna carta
escribe la respuesta ni explica cómo se resuelve su puzle. Datos de herramientas/instancias_espia.py.

  16 la nota de Zorro · 18 el desfile · 19 y 21 el plano de Montecarlo (dos mitades) · 41 y 43 las pistas del skyline (arriba e izquierda; abajo y derecha)
  45 la regla del skyline · 42 y 49 las páginas del libro · 53 los renglones del mensaje · 54 y 55 la caja fuerte (dos mitades) · 59 la regla de la caja
  37 y 39 las cartas del crupier (primera y segunda parte) · 33 la regla de la cuenta · 61 y 63 los pasaportes (dos mitades) · 26 la regla del pasaporte
  66 el itinerario · 67 los husos horarios · 70 y 71 el manual del desactivador · 75 los giros de la ruleta · 79 la regla de la martingala
  86 el orden de las pulsaciones · 87 el teclado del teléfono rojo
Uso (desde la raíz del repo):  python herramientas/espia.py [carpeta_juego]
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oeste  # noqa: E402
from oeste import Hoja  # noqa: E402
from mosaicos import cortar  # noqa: E402
import instancias_espia as I  # noqa: E402

oeste.FUENTES["cour"] = "C:/Windows/Fonts/cour.ttf"
oeste.FUENTES["courb"] = "C:/Windows/Fonts/courbd.ttf"

W, H = 630, 882
CREMA = (246, 238, 220)
TINTA = (28, 36, 48)
TURQ = (0, 150, 160)
ROSA = (226, 70, 130)
ORO = (200, 160, 50)
GRIS = (120, 128, 138)
BLANCO = (252, 252, 252)
NEGRO = (30, 30, 34)
ROJO = (200, 40, 50)
VERDE = (30, 130, 80)


def ruido(im, s, f=2.5):
    a = np.asarray(im).astype(np.int16)
    a = a + np.random.default_rng(s).normal(0, f, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def pagina(titulo, sub=None, w=W, h=H):
    p = Hoja(w, h, CREMA)
    p.rect(16, 16, w - 16, h - 16, None, TURQ, 6)
    p.rect(28, 28, w - 28, h - 28, None, ROSA, 2)
    p.texto((w / 2, 72), titulo, "cartel", 30, TURQ)
    if sub:
        p.texto((w / 2, 108), sub, "texto2", 19, TINTA)
    return p


def versos(p, lineas, y0=220, paso=50, tam=23, x=W / 2, color=TINTA, tipo="texto2"):
    for k, v in enumerate(lineas):
        p.texto((x, y0 + k * paso), v, tipo, tam, color)


# ------------------------------------------------------------------ 16: la nota de Zorro
def nota_zorro():
    d = I.CRIPTOGRAMA
    p = pagina("NOTA DE LA AGENTE ZORRO", "interceptada en el casino")
    palabras = d["cifrado"].split()
    lineas, cur = [], ""
    for w in palabras:
        if len(cur) + len(w) + 1 > 15:
            lineas.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lineas.append(cur)
    for k, l in enumerate(lineas):
        p.texto((W / 2, 220 + k * 70), l, "courb", 40, TINTA)
    p.rect(110, 650, W - 110, 760, BLANCO, ROSA, 3)
    p.texto((W / 2, 690), "Mi firma es mi cargo:", "texto2", 21, TINTA)
    p.texto((W / 2, 730), "la primera palabra es " + d["pista"], "texto", 24, ROSA)
    return p.final()


# ------------------------------------------------------------------ 18 y 19/21: la persecución
def acertijo_desfile():
    r = I.RUTA
    cerr = " y ".join(r["nodos"][k] for k in r["cerrados"])
    p = pagina("EL ACERTIJO DEL DESFILE", "del cartel de la policía")
    versos(p, ["«El Gran Premio pasa hoy por la ciudad:", f"las glorietas {cerr} están cortadas", "y nadie puede cruzarlas.", "",
               "Salid del Casino, la A,", "y llegad al Puerto, la I,", "en el menor tiempo posible,", "contando minutos por calle.»"], 200, 54, 23)
    return p.final()


def plano_montecarlo():
    r = I.RUTA
    p = Hoja(W, H * 2, CREMA)
    p.rect(16, 16, W - 16, H * 2 - 16, None, TURQ, 6)
    p.rect(28, 28, W - 28, H * 2 - 28, None, ROSA, 2)
    p.texto((W / 2, 72), "EL PLANO DE MONTECARLO", "cartel", 30, TURQ)
    xs = [130, 315, 500]
    ys = [420, 740, 1280]
    pos = {k: (xs[k % 3], ys[k // 3]) for k in range(9)}
    for a, b, w in r["aristas"]:
        (xa, ya), (xb, yb) = pos[a], pos[b]
        p.linea([(xa, ya), (xb, yb)], TINTA, 6)
    for a, b, w in r["aristas"]:
        (xa, ya), (xb, yb) = pos[a], pos[b]
        mx, my = (xa + xb) / 2, (ya + yb) / 2
        p.rect(mx - 22, my - 17, mx + 22, my + 17, BLANCO, ROSA, 3)
        p.texto((mx, my), str(w), "cartel", 24, TINTA)
    for k, (x, y) in pos.items():
        p.disco(x, y, 38, TURQ if k not in (0, 8) else ROSA, TINTA, 4)
        p.texto((x, y), r["nodos"][k], "cartel", 36, BLANCO)
    p.texto((pos[0][0], pos[0][1] - 62), "CASINO", "texto", 18, TINTA)
    p.texto((pos[8][0], pos[8][1] + 62), "PUERTO", "texto", 18, TINTA)
    return p.final()


# ------------------------------------------------------------------ 41/43 y 45: el skyline
def marco_skyline(titulo, lados):
    d = I.RASCACIELOS
    n = d["n"]
    p = pagina(titulo)
    lado = 90
    x0, y0 = (W - n * lado) / 2, 250
    for r in range(n):
        for c in range(n):
            p.rect(x0 + c * lado, y0 + r * lado, x0 + (c + 1) * lado, y0 + (r + 1) * lado, BLANCO, TINTA, 2)
    for l in lados:
        for i, v in enumerate(d["pistas"][l]):
            if not v:
                continue
            if l == "N":
                xy = (x0 + i * lado + lado / 2, y0 - 30)
            elif l == "S":
                xy = (x0 + i * lado + lado / 2, y0 + n * lado + 30)
            elif l == "O":
                xy = (x0 - 30, y0 + i * lado + lado / 2)
            else:
                xy = (x0 + n * lado + 30, y0 + i * lado + lado / 2)
            p.texto(xy, str(v), "cartel", 38, ROSA)
    return p.final()


def skyline_a():
    return marco_skyline("EL SKYLINE: ARRIBA E IZQUIERDA", ["N", "O"])


def skyline_b():
    return marco_skyline("EL SKYLINE: ABAJO Y DERECHA", ["S", "E"])


def regla_skyline():
    p = pagina("LA REGLA DEL ARQUITECTO", "del plano del casino")
    versos(p, ["«Cinco torres, de una a cinco plantas,", "en cada fila y en cada columna,", "ni una repetida.", "",
               "Cada número del borde cuenta cuántas", "torres se ven desde allí:", "las bajas se esconden", "detrás de las altas.»"], 200, 54, 23)
    return p.final()


# ------------------------------------------------------------------ 42 y 49: las páginas del libro; 53: los renglones
def pagina_libro(num):
    p = pagina(f"PÁGINA {num}", "de «La última carta», novela de bolsillo")
    for k, l in enumerate(I.PAGINAS[num]):
        p.texto((60, 200 + k * 62), l, "texto2", 23, TINTA, "lm")
    p.texto((W / 2, 800), str(num), "texto2", 22, GRIS)
    return p.final()


def renglones():
    d = I.LIBRO
    p = pagina("LOS RENGLONES DEL MENSAJE", "tres números por palabra")
    for k, (pg, ln, w) in enumerate(d["mensaje"]):
        p.rect(80, 190 + k * 100, W - 80, 260 + k * 100, BLANCO, ROSA, 3)
        p.texto((W / 2, 225 + k * 100), f"{pg} · {ln} · {w}", "cartel", 40, TINTA)
    versos(p, ["«Primero la página, luego el renglón,", "y al final, la palabra.»"], 650, 44, 21)
    return p.final()


# ------------------------------------------------------------------ 54/55 y 59: la caja fuerte (kenken)
def caja_fuerte():
    d = I.KENKEN
    n = d["n"]
    p = Hoja(W * 2, H, CREMA)
    p.rect(16, 16, W * 2 - 16, H - 16, None, TURQ, 6)
    p.rect(28, 28, W * 2 - 28, H - 28, None, ROSA, 2)
    p.texto((W, 72), "LA CAJA FUERTE", "cartel", 32, TURQ)
    lado = 110
    x0, y0 = W - 3 * lado, (H - n * lado) / 2 + 30
    jaula_de = {}
    for k, j in enumerate(d["jaulas"]):
        for r, c in j["celdas"]:
            jaula_de[(r, c)] = k
    for r in range(n):
        for c in range(n):
            p.rect(x0 + c * lado, y0 + r * lado, x0 + (c + 1) * lado, y0 + (r + 1) * lado, BLANCO, GRIS, 1)
    for r in range(n):
        for c in range(n):
            xa, ya = x0 + c * lado, y0 + r * lado
            if r == 0 or jaula_de[(r - 1, c)] != jaula_de[(r, c)]:
                p.linea([(xa, ya), (xa + lado, ya)], TINTA, 6)
            if r == n - 1 or jaula_de[(r + 1, c)] != jaula_de[(r, c)]:
                p.linea([(xa, ya + lado), (xa + lado, ya + lado)], TINTA, 6)
            if c == 0 or jaula_de[(r, c - 1)] != jaula_de[(r, c)]:
                p.linea([(xa, ya), (xa, ya + lado)], TINTA, 6)
            if c == n - 1 or jaula_de[(r, c + 1)] != jaula_de[(r, c)]:
                p.linea([(xa + lado, ya), (xa + lado, ya + lado)], TINTA, 6)
    simb = {"=": "", "+": "+", "x": "x", "-": "-", "/": "÷"}
    for j in d["jaulas"]:
        r, c = min(map(tuple, j["celdas"]))
        p.texto((x0 + c * lado + 8, y0 + r * lado + 8), f"{j['objetivo']}{simb[j['op']]}", "cartel", 24, ROSA, "lt")
    return p.final()


def regla_caja():
    p = pagina("LA REGLA DEL JOYERO", "grabada en la cerradura")
    versos(p, ["«Cinco cifras, del uno al cinco,", "sin repetir en filas ni columnas.", "",
               "Cada jaula de trazo grueso lleva un número", "y una operación: la cuenta que", "han de hacer sus cifras.", "",
               "En la resta y la división manda", "la mayor sobre la menor.»"], 190, 50, 22)
    return p.final()


# ------------------------------------------------------------------ 37/39 y 33: las cartas del crupier
def palo(p, x, y, r, tipo, col):
    if tipo == "diamantes":
        p.poli([(x, y - r), (x + r * 0.75, y), (x, y + r), (x - r * 0.75, y)], col)
    elif tipo == "corazones":
        p.disco(x - r * 0.4, y - r * 0.25, r * 0.5, col)
        p.disco(x + r * 0.4, y - r * 0.25, r * 0.5, col)
        p.poli([(x - r * 0.88, y - r * 0.05), (x + r * 0.88, y - r * 0.05), (x, y + r)], col)
    elif tipo == "picas":
        p.disco(x - r * 0.4, y + r * 0.05, r * 0.5, col)
        p.disco(x + r * 0.4, y + r * 0.05, r * 0.5, col)
        p.poli([(x - r * 0.88, y - r * 0.05), (x + r * 0.88, y - r * 0.05), (x, y - r)], col)
        p.poli([(x - r * 0.18, y), (x + r * 0.18, y), (x + r * 0.35, y + r), (x - r * 0.35, y + r)], col)
    else:
        p.disco(x, y - r * 0.45, r * 0.42, col)
        p.disco(x - r * 0.45, y + r * 0.15, r * 0.42, col)
        p.disco(x + r * 0.45, y + r * 0.15, r * 0.42, col)
        p.poli([(x - r * 0.18, y), (x + r * 0.18, y), (x + r * 0.35, y + r), (x - r * 0.35, y + r)], col)


def cartas_crupier(inicio, fin, titulo):
    d = I.CONTEO
    p = pagina(titulo, "en el orden en que salen")
    for k in range(inicio, fin):
        rango, pl = d["cartas"][k]
        i = k - inicio
        x = 80 + (i % 4) * 125
        y = 225 + (i // 4) * 160
        p.rect(x - 45, y - 62, x + 45, y + 62, BLANCO, TINTA, 3)
        col = ROJO if pl in ("corazones", "diamantes") else NEGRO
        p.texto((x - 28, y - 40), rango, "cartel", 28, col)
        palo(p, x, y + 12, 24, pl, col)
        p.texto((x + 34, y + 54), str(k + 1), "texto2", 13, GRIS, "rm")
    return p.final()


def regla_cuenta():
    p = pagina("LA CUENTA DEL CRUPIER", "susurrada en el casino")
    versos(p, ["«Las bajas, del dos al seis,", "suman uno cada vez que salen.", "", "Las medias, siete, ocho y nueve,", "ni suman ni restan.", "",
               "Las altas, diez, figuras y as,", "restan uno.», dice el crupier,", "«y se cuenta carta a carta,", "desde la primera.»"], 190, 50, 22)
    return p.final()


# ------------------------------------------------------------------ 61/63 y 26: los pasaportes
def pasaporte(p, y0, d):
    p.rect(50, y0, W - 50, y0 + 360, (236, 226, 196), TINTA, 4)
    p.rect(60, y0 + 10, W - 60, y0 + 50, TURQ)
    p.texto((W / 2, y0 + 30), "PASAPORTE", "cartel", 24, BLANCO)
    p.texto((70, y0 + 80), "Apellido: " + d["apellido"], "texto", 21, TINTA, "lm")
    p.texto((70, y0 + 112), "Nombre: " + d["nombre"], "texto", 21, TINTA, "lm")
    p.texto((70, y0 + 144), "Núm.: " + d["doc"], "texto", 21, TINTA, "lm")
    p.rect(450, y0 + 66, W - 70, y0 + 170, GRIS, TINTA, 3)
    p.disco(520, y0 + 106, 20, (200, 200, 210))
    mrz1 = ("P<ESP" + d["apellido"] + "<<" + d["nombre"]).ljust(30, "<")[:30]
    mrz2 = d["doc"] + "?" + "ESP" + d["nac"] + str(d["control_nac"]) + "<" + d["ven"] + str(d["control_ven"])
    p.rect(55, y0 + 210, W - 55, y0 + 350, (250, 248, 238), TINTA, 2)
    p.texto((70, y0 + 250), mrz1, "courb", 24, TINTA, "lm")
    p.texto((70, y0 + 310), mrz2, "courb", 24, TINTA, "lm")


def pasaportes():
    d = I.PASAPORTES
    p = Hoja(W, H * 2, CREMA)
    p.rect(16, 16, W - 16, H * 2 - 16, None, TURQ, 6)
    p.rect(28, 28, W - 28, H * 2 - 28, None, ROSA, 2)
    p.texto((W / 2, 72), "LOS PASAPORTES FALSOS", "cartel", 30, TURQ)
    for y0, doc in zip((120, 500, 940), d["pasaportes"]):
        pasaporte(p, y0, doc)
    return p.final()


def regla_pasaporte():
    d = I.PASAPORTES
    p = pagina("LA REGLA DEL ADUANERO", "sellada en la frontera")
    versos(p, ["«Cada letra vale lo que su puesto", "más nueve: la A, diez; la B, once...", "La flecha ‹ vale cero.", "",
               "Cada símbolo se multiplica por 7, 3 y 1,", "y vuelta a empezar.", "Se suma todo y de la suma", "solo vale la cifra de las unidades.", "",
               f"Ejemplo: {d['ejemplo']['doc']} da {d['ejemplo']['control']}.»"], 175, 48, 20)
    return p.final()


# ------------------------------------------------------------------ 66 y 67: el vuelo con escalas
def itinerario():
    d = I.HUSOS
    p = pagina("EL ITINERARIO DE ZORRO", "billete con tres vuelos")
    s = d["salida"]
    p.rect(60, 150, W - 60, 250, BLANCO, ROSA, 3)
    p.texto((W / 2, 185), f"Sale de {s['ciudad']}", "texto", 24, TINTA)
    p.texto((W / 2, 222), f"a las {s['hora']}:{s['min']:02d}, hora local", "texto2", 22, ROSA)
    y = 270
    for t in d["tramos"]:
        p.rect(60, y, W - 60, y + 130, BLANCO, TURQ, 3)
        p.texto((W / 2, y + 30), f"{t['de']} a {t['a']}", "texto", 22, TINTA)
        p.texto((W / 2, y + 66), f"Vuelo de {t['dur'][0]} h {t['dur'][1]} min", "texto2", 21, TINTA)
        if t["escala"] != [0, 0]:
            p.texto((W / 2, y + 100), f"Escala de {t['escala'][0]} h {t['escala'][1]} min", "texto2", 21, ROSA)
        else:
            p.texto((W / 2, y + 100), "Llegada final", "texto2", 21, ROSA)
        y += 150
    return p.final()


def husos():
    d = I.HUSOS
    p = pagina("LOS HUSOS HORARIOS", "respecto al meridiano de Greenwich")
    k = 0
    for ciudad, off in d["ciudades"].items():
        if ciudad not in ("Tokio", "Bombay", "El Cairo", "Montecarlo", "Londres"):
            continue
        y = 190 + k * 100
        p.rect(60, y - 36, W - 60, y + 36, BLANCO, TURQ, 3)
        p.texto((90, y), ciudad, "texto", 24, TINTA, "lm")
        txt = ("+" if off >= 0 else "") + (str(int(off)) if off == int(off) else f"{int(off)} y media")
        p.texto((W - 90, y), "UTC " + txt, "cartel", 26, ROSA, "rm")
        k += 1
    versos(p, ["Al este del meridiano, el sol sale antes", "y la hora local va por delante."], 740, 38, 19)
    return p.final()


# ------------------------------------------------------------------ 70 y 71: el manual del desactivador
def manual(parte):
    d = I.CABLES
    p = pagina("EL MANUAL DEL DESACTIVADOR", f"parte {parte} de 2")
    if parte == 1:
        p.texto((W / 2, 150), "Se aplica la primera regla que se cumpla.", "texto2", 19, ROSA)
    rs = d["reglas"][:3] if parte == 1 else d["reglas"][3:]
    base = 0 if parte == 1 else 3
    for k, r in enumerate(rs):
        y = 220 + k * 190
        p.disco(80, y + 14, 24, ROSA)
        p.texto((80, y + 14), str(base + k + 1), "cartel", 26, BLANCO)
        palabras, lin, lineas = r.split(), "", []
        for w in palabras:
            if len(lin) + len(w) + 1 > 30:
                lineas.append(lin)
                lin = w
            else:
                lin = (lin + " " + w).strip()
        lineas.append(lin)
        for j, l in enumerate(lineas):
            p.texto((130, y + j * 34), l, "texto2", 21, TINTA, "lm")
    return p.final()


# ------------------------------------------------------------------ 75 y 79: la ruleta
def giros():
    d = I.RULETA
    p = pagina("LOS GIROS DE LA RULETA", "anotados por el crupier")
    for k, x in enumerate(d["resultados"]):
        cx = 110 + (k % 4) * 140
        cy = 220 + (k // 4) * 150
        col = {"R": ROJO, "N": NEGRO, "V": VERDE}[x]
        p.disco(cx, cy, 48, col, TINTA, 3)
        p.texto((cx, cy), str(k + 1), "cartel", 34, BLANCO)
    return p.final()


def regla_ruleta():
    d = I.RULETA
    p = pagina("LA MARTINGALA", "el sistema del jugador")
    versos(p, [f"«Empiezo con {d['banco']} fichas y apuesto", f"{d['base']} al rojo.", "", "Si gano, cobro lo apostado", f"y vuelvo a apostar {d['base']}.", "",
               "Si pierdo, la próxima apuesta", "es el doble de la anterior.", "", "El verde, el cero, siempre pierde.»"], 185, 48, 22)
    return p.final()


# ------------------------------------------------------------------ 86 y 87: el teléfono rojo
def orden_pulsaciones():
    p = pagina("LAS CINCO PULSACIONES", "del cuaderno de la Agente Zorro")
    versos(p, ["«Cinco veces dio el teléfono su tono,", "y cada una dejó sus teclas:", "",
               "primera, la de la nota secreta;", "segunda, la del skyline;", "tercera, la de la caja fuerte;", "cuarta, la del desactivador;",
               "y quinta, la de los pasaportes.", "", "Se pulsa varias veces la misma tecla", "para llegar a la letra que toca.»"], 175, 46, 21)
    return p.final()


def teclado_telefono():
    p = pagina("EL TELÉFONO ROJO", "teclado de disco con letras")
    teclas = [("1", ""), ("2", "ABC"), ("3", "DEF"), ("4", "GHI"), ("5", "JKL"), ("6", "MNO"), ("7", "PQRS"), ("8", "TUV"), ("9", "WXYZ"), ("*", ""), ("0", ""), ("#", "")]
    for k, (t, ls) in enumerate(teclas):
        x = 150 + (k % 3) * 165
        y = 230 + (k // 3) * 140
        p.disco(x, y, 52, ROSA if k != 0 else GRIS, TINTA, 4)
        p.texto((x, y - 8), t, "cartel", 40, BLANCO)
        if ls:
            p.texto((x, y + 28), ls, "texto", 16, BLANCO)
    return p.final()


# ------------------------------------------------------------------ datos de las apps
def inyectar(carpeta):
    datos = {
        "14-criptograma.js": {"claro": I.CRIPTOGRAMA["claro"], "pulsa": I.PULSA["14"]},
        "20-ruta.js": {"nodos": I.RUTA["nodos"], "aristas": I.RUTA["aristas"], "cerrados": I.RUTA["cerrados"], "mejor": I.RUTA["mejor"]},
        "40-rascacielos.js": {"n": I.RASCACIELOS["n"], "pistas": I.RASCACIELOS["pistas"], "solucion": I.RASCACIELOS["solucion"], "pulsa": I.PULSA["40"]},
        "48-libro.js": {"claro": I.LIBRO["claro"]},
        "52-kenken.js": {"n": I.KENKEN["n"], "jaulas": I.KENKEN["jaulas"], "pulsa": I.PULSA["52"]},
        "46-conteo.js": {"corte": I.CONTEO["corte"], "cuenta_corte": I.CONTEO["cuenta_corte"], "cuenta_final": I.CONTEO["cuenta_final"]},
        "51-pasaporte.js": {"digitos": I.PASAPORTES["digitos"], "pulsa": I.PULSA["51"]},
        "64-husos.js": {"llegada": I.HUSOS["llegada"]},
        "69-cables.js": {"cargas": I.CABLES["cargas"], "pulsa": I.PULSA["69"]},
        "72-ruleta.js": {"final": I.RULETA["final"]},
        "85-teclado.js": {"palabra": I.PALABRA},
    }
    for app, d in datos.items():
        ruta = os.path.join(carpeta, "minijuegos", app)
        txt = open(ruta, encoding="utf-8").read() if os.path.exists(ruta) else ""
        if "/*DATOS*/" not in txt:
            continue
        a, b = txt.index("/*DATOS*/") + len("/*DATOS*/"), txt.index("/*FIN*/")
        open(ruta, "w", encoding="utf-8", newline="\n").write(txt[:a] + json.dumps(d, ensure_ascii=False) + txt[b:])


def main(carpeta="juegos/aventuras-ca/espia"):
    arte = os.path.join(carpeta, "arte")
    os.makedirs(arte, exist_ok=True)

    def g(k, im):
        ruido(im, int(k)).save(os.path.join(arte, f"{k}.png"))

    def mosaico(nombre, im, filas, cols, cartas):
        im = ruido(im, sum(map(ord, nombre)))
        im.save(os.path.join(arte, f"mosaico-{nombre}.png"))
        for pieza, k in zip(cortar(im, filas, cols), cartas):
            pieza.save(os.path.join(arte, f"{k}.png"))
    g("16", nota_zorro())
    g("18", acertijo_desfile())
    mosaico("plano", plano_montecarlo(), 2, 1, ("19", "21"))
    g("41", skyline_a())
    g("43", skyline_b())
    g("45", regla_skyline())
    g("42", pagina_libro(17))
    g("49", pagina_libro(18))
    g("53", renglones())
    mosaico("caja", caja_fuerte(), 1, 2, ("54", "55"))
    g("59", regla_caja())
    n = len(I.CONTEO["cartas"])
    g("37", cartas_crupier(0, n // 2, "LAS CARTAS DEL CRUPIER (I)"))
    g("39", cartas_crupier(n // 2, n, "LAS CARTAS DEL CRUPIER (II)"))
    g("33", regla_cuenta())
    mosaico("pasaportes", pasaportes(), 2, 1, ("61", "63"))
    g("26", regla_pasaporte())
    g("66", itinerario())
    g("67", husos())
    g("70", manual(1))
    g("71", manual(2))
    g("75", giros())
    g("79", regla_ruleta())
    g("86", orden_pulsaciones())
    g("87", teclado_telefono())
    inyectar(carpeta)
    print("láminas de Espía escritas en", arte)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))

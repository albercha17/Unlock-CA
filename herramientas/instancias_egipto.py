"""Instancias de los puzles de «Egipto, 1274 a.C.: El Ojo de Horus» (versión de 60 cartas, 21 oct 2026), con solución única comprobada.

Once puzles de tipos que no salen en ningún otro juego de la serie:
  monton       la «falsa posición» del papiro Rhind: un montón, su mitad y su cuarto suman 28
  piramide     pirámide de sumas: cada piedra es la suma de las dos que la sostienen
  nilometro    secuencia de crecidas del Nilo medidas en codos y palmos (7 palmos = 1 codo)
  contar       contar, en un friso, solo los animales que miran hacia donde nace el sol
  heqat        las seis partes del Ojo de Horus (1/2 ... 1/64) para medir un total de pagos
  cripto       criptoaritmética con jeroglíficos en lugar de letras
  camaras      colorear las cámaras de un templo: dos cámaras con puerta no pueden llevar la misma pintura
  canales      red de riego más barata (árbol de expansión mínimo)
  friso        matriz de figuras (3 reglas): qué azulejo falta en el friso
  tierras      reparto de tierras (Shikaku): dividir el campo en parcelas rectangulares
  sellos       metapuzle final: ordenar cinco sellos por acertijos
Uso: python herramientas/instancias_egipto.py   (comprueba todo y escribe instancias_egipto.json)
"""
import itertools
import json
import math
import os
import random

AQUI = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ montón (falsa posición)
def monton():
    x = 16
    assert x + x // 2 + x // 4 == 28
    return {"fracciones": [[1, 1], [1, 2], [1, 4]], "total": 28, "solucion": x}


# ------------------------------------------------------------------ heqat: las seis partes del ojo
PARTES = [[1, 2], [1, 4], [1, 8], [1, 16], [1, 32], [1, 64]]
FORMAS = ["circulo", "cuadrado", "triangulo", "rombo", "estrella", "hexagono"]


def heqat():
    manana = [[1, 4], [1, 8], [1, 8]]
    tarde = [[1, 32], [1, 32], [1, 64]]
    total = sum(64 // d for _, d in manana + tarde)       # en sesenta y cuatroavos
    sol = [i for i, (_, d) in enumerate(PARTES) if total & (64 // d)]
    assert sum(64 // PARTES[i][1] for i in sol) == total and total < 64
    return {"partes": PARTES, "formas": FORMAS, "manana": manana, "tarde": tarde, "total64": total, "solucion": sol}


# ------------------------------------------------------------------ pirámide de sumas
def _piramide_filas(base):
    filas = [list(base)]
    while len(filas[-1]) > 1:
        a = filas[-1]
        filas.append([a[i] + a[i + 1] for i in range(len(a) - 1)])
    return filas            # filas[0] = base, filas[-1] = [cima]


def piramide(semilla=3, n=5):
    rng = random.Random(semilla)
    for _ in range(5000):
        base = [rng.randint(1, 9) for _ in range(n)]
        filas = _piramide_filas(base)
        celdas = [(f, i) for f in range(n) for i in range(n - f)]
        dados = {(n - 1, 0)}
        rng.shuffle(celdas)

        def cuantas(dados):
            c = 0
            for b in itertools.product(range(1, 10), repeat=n):
                fb = _piramide_filas(b)
                if all(fb[f][i] == filas[f][i] for f, i in dados):
                    c += 1
                    if c > 1:
                        return c
            return c
        for c in celdas:
            if cuantas(dados) == 1:
                break
            if c[0] != 0:
                dados.add(c)
        if cuantas(dados) != 1 or len(dados) > 7:
            continue
        # al menos dos pistas a cada lado del corte (filas superiores / filas de abajo)
        arriba = [d for d in dados if d[0] >= 2]
        abajo = [d for d in dados if d[0] < 2]
        if len(arriba) >= 2 and len(abajo) >= 2:
            return {"n": n, "filas": filas, "dados": sorted([list(d) for d in dados]), "solucion": base}
    raise SystemExit("sin pirámide")


# ------------------------------------------------------------------ nilómetro
def nilometro():
    palmos = [20, 23, 28, 35, 44]
    sig = palmos[-1] + (palmos[-1] - palmos[-2]) + 2     # las diferencias suben de dos en dos: 3, 5, 7, 9, 11
    assert [b - a for a, b in zip(palmos, palmos[1:])] == [3, 5, 7, 9] and sig == 55
    return {"alturas_palmos": palmos, "siguiente_palmos": sig, "solucion": [sig // 7, sig % 7]}


# ------------------------------------------------------------------ figuras (polígonos y trazos en una caja de 100 x 100, mirando a la derecha)
def _elipse(cx, cy, rx, ry, n=28):
    return [[round(cx + rx * math.cos(2 * math.pi * k / n), 1), round(cy + ry * math.sin(2 * math.pi * k / n), 1)] for k in range(n)]


FIGURAS = {
    # azulejos del friso
    "anj": [{"t": "c", "c": [50, 30], "r": 20, "w": 9}, {"t": "l", "p": [[50, 50], [50, 94]], "w": 10}, {"t": "l", "p": [[26, 66], [74, 66]], "w": 10}],
    "ojo": [{"t": "p", "p": [[8, 50], [26, 34], [50, 28], [74, 34], [92, 50], [74, 62], [50, 68], [26, 62]]},
            {"t": "c", "c": [50, 48], "r": 11, "f": "fondo"}, {"t": "l", "p": [[50, 68], [42, 90], [60, 90]], "w": 7}],
    "escarabajo": [{"t": "p", "p": _elipse(50, 56, 26, 32)}, {"t": "c", "c": [50, 20], "r": 12},
                   {"t": "l", "p": [[50, 30], [50, 86]], "w": 4, "f": "fondo"}, {"t": "l", "p": [[28, 44], [10, 36]], "w": 6},
                   {"t": "l", "p": [[24, 62], [8, 64]], "w": 6}, {"t": "l", "p": [[28, 80], [12, 92]], "w": 6},
                   {"t": "l", "p": [[72, 44], [90, 36]], "w": 6}, {"t": "l", "p": [[76, 62], [92, 64]], "w": 6},
                   {"t": "l", "p": [[72, 80], [88, 92]], "w": 6}],
    # animales del friso (miran a la derecha)
    "ibis": [{"t": "p", "p": _elipse(40, 56, 24, 17)}, {"t": "l", "p": [[56, 50], [66, 28], [70, 22]], "w": 7},
             {"t": "c", "c": [72, 20], "r": 8}, {"t": "l", "p": [[78, 20], [96, 28], [92, 34]], "w": 4},
             {"t": "l", "p": [[38, 72], [36, 92]], "w": 4}, {"t": "l", "p": [[46, 72], [48, 92]], "w": 4},
             {"t": "l", "p": [[18, 54], [4, 64]], "w": 7}],
    "cobra": [{"t": "p", "p": [[18, 94], [30, 70], [46, 78], [58, 56], [48, 34], [54, 16], [66, 16], [72, 34], [66, 58], [78, 80], [92, 94]]},
              {"t": "p", "p": [[36, 16], [54, 16], [48, 4]]}, {"t": "c", "c": [62, 10], "r": 7},
              {"t": "l", "p": [[66, 10], [78, 12]], "w": 3}],
    "chacal": [{"t": "p", "p": _elipse(36, 58, 26, 14)}, {"t": "l", "p": [[18, 66], [14, 92]], "w": 6}, {"t": "l", "p": [[30, 68], [30, 92]], "w": 6},
               {"t": "l", "p": [[46, 68], [48, 92]], "w": 6}, {"t": "l", "p": [[58, 62], [64, 92]], "w": 6},
               {"t": "p", "p": [[56, 50], [66, 30], [88, 40], [96, 46], [90, 52], [70, 54]]},
               {"t": "p", "p": [[62, 32], [64, 4], [74, 30]]}, {"t": "p", "p": [[74, 32], [80, 8], [84, 36]]},
               {"t": "l", "p": [[10, 56], [2, 40]], "w": 5}],
    "halcon": [{"t": "p", "p": _elipse(46, 62, 22, 26)}, {"t": "c", "c": [58, 28], "r": 12}, {"t": "p", "p": [[66, 26], [86, 32], [66, 40]]},
               {"t": "p", "p": [[34, 50], [10, 28], [8, 62], [30, 76]]}, {"t": "l", "p": [[40, 86], [40, 98]], "w": 5},
               {"t": "l", "p": [[52, 86], [54, 98]], "w": 5}],
    # signos para el criptograma (y los sellos)
    "sol": [{"t": "c", "c": [50, 50], "r": 30, "w": 8}, {"t": "c", "c": [50, 50], "r": 7}],
    "loto": [{"t": "p", "p": [[50, 14], [62, 52], [50, 74], [38, 52]]}, {"t": "p", "p": [[30, 30], [46, 54], [40, 74], [20, 56]]},
             {"t": "p", "p": [[70, 30], [54, 54], [60, 74], [80, 56]]}, {"t": "l", "p": [[50, 74], [50, 96]], "w": 6}],
    "agua": [{"t": "l", "p": [[8, 30], [26, 20], [44, 30], [62, 20], [80, 30], [94, 22]], "w": 7},
             {"t": "l", "p": [[8, 56], [26, 46], [44, 56], [62, 46], [80, 56], [94, 48]], "w": 7},
             {"t": "l", "p": [[8, 82], [26, 72], [44, 82], [62, 72], [80, 82], [94, 74]], "w": 7}],
    "pluma": [{"t": "p", "p": _elipse(50, 44, 15, 38)}, {"t": "l", "p": [[50, 10], [50, 96]], "w": 5, "f": "fondo"}],
    "corona": [{"t": "p", "p": [[30, 90], [38, 30], [50, 6], [62, 30], [70, 90]]}, {"t": "c", "c": [50, 50], "r": 8, "f": "fondo"}],
    "cetro": [{"t": "l", "p": [[50, 94], [50, 20]], "w": 9}, {"t": "p", "p": [[34, 8], [66, 8], [58, 28], [42, 28]]}],
    "pan": [{"t": "p", "p": _elipse(50, 62, 38, 22)}, {"t": "l", "p": [[24, 56], [76, 56]], "w": 4, "f": "fondo"}],
    "tierra": [{"t": "p", "p": [[10, 70], [30, 30], [50, 62], [70, 24], [92, 70]]}],
}


# ------------------------------------------------------------------ friso (matriz de figuras con tres reglas)
FIG3 = ["anj", "ojo", "escarabajo"]
COL3 = ["terracota", "turquesa", "oro"]


def friso(semilla=2):
    rng = random.Random(semilla)
    s = rng.randrange(3)
    cel = [[{"fig": (r + c) % 3, "color": (r + 2 * c + s) % 3, "tam": r} for c in range(3)] for r in range(3)]
    correcta = dict(cel[2][2])
    var = []
    for atr, n in (("fig", 3), ("color", 3), ("tam", 3)):
        for v in range(n):
            if v != correcta[atr]:
                d = dict(correcta)
                d[atr] = v
                var.append(d)
    rng.shuffle(var)
    opciones = var[:5] + [correcta]
    rng.shuffle(opciones)
    return {"celdas": cel, "faltan": [2, 2], "opciones": opciones, "solucion": opciones.index(correcta), "figuras": FIG3, "colores": COL3}


# ------------------------------------------------------------------ contar el friso
ANIMALES = ["ibis", "cobra", "chacal", "halcon"]


def contar(semilla=5, cols=13, filas=7):
    rng = random.Random(semilla)
    derecha = [4, 6, 3, 5]
    izquierda = [5, 3, 6, 4]
    celdas = [(x, y) for y in range(filas) for x in range(cols)]
    rng.shuffle(celdas)
    puestos, k = [], 0
    for a in range(4):
        for lado, cant in (("d", derecha[a]), ("i", izquierda[a])):
            for _ in range(cant):
                x, y = celdas[k]
                k += 1
                puestos.append({"animal": ANIMALES[a], "mira": lado, "x": x, "y": y})
    # adornos que no se cuentan: lotos y signos de agua
    for _ in range(14):
        x, y = celdas[k]
        k += 1
        puestos.append({"animal": rng.choice(["loto", "agua", "sol"]), "mira": "d", "x": x, "y": y})
    return {"cols": cols, "filas": filas, "puestos": puestos, "animales": ANIMALES, "solucion": derecha}


# ------------------------------------------------------------------ criptograma de jeroglíficos
SIGNOS = ["sol", "loto", "agua", "pluma", "corona", "cetro"]


PATRON = ("CDC", "EAA", "CBBF")        # CDC + EAA = CBBF, cada letra un signo distinto


def _soluciones_cripto(restricciones=()):
    letras = sorted(set("".join(PATRON)))
    out = []
    for dig in itertools.permutations(range(10), 6):
        m = dict(zip(letras, dig))
        if any(m[p[0]] == 0 for p in PATRON):
            continue
        v = lambda p: int("".join(str(m[c]) for c in p))
        if v(PATRON[0]) + v(PATRON[1]) == v(PATRON[2]) and all(f(m) for _, f in restricciones):
            out.append(m)
    return out


def cripto():
    """Una suma con tres soluciones y dos pistas (una por carta) que, juntas, dejan una sola."""
    todas = _soluciones_cripto()
    assert len(todas) == 3, len(todas)
    letras = sorted(set("".join(PATRON)))
    cand = []
    for x in letras:
        cand.append((f"{x} es par", lambda m, x=x: m[x] % 2 == 0))
        cand.append((f"{x} es impar", lambda m, x=x: m[x] % 2 == 1))
        for y in letras:
            if x != y:
                cand.append((f"{x} > {y}", lambda m, x=x, y=y: m[x] > m[y]))
    util = []
    for t, f in cand:
        k = sum(1 for m in todas if f(m))
        if 1 <= k < 3:
            util.append((t, f, k))
    for (t1, f1, k1), (t2, f2, k2) in itertools.combinations(util, 2):
        if sum(1 for m in todas if f1(m) and f2(m)) == 1 and k1 == 2 and k2 == 2:
            sol = next(m for m in todas if f1(m) and f2(m))
            return {"suma": list(PATRON), "signos": dict(zip("ABCDEF", SIGNOS)), "pistas": [t1, t2], "solucion": sol, "soluciones_sin_pistas": len(todas)}
    raise SystemExit("sin cripto")


# ------------------------------------------------------------------ cámaras de colores
COLORES = ["ocre", "turquesa", "lapislazuli"]


def camaras(semilla=9, cols=4, filas=3):
    rng = random.Random(semilla)
    n = cols * filas
    pos = {i: (i % cols, i // cols) for i in range(n)}
    for _ in range(5000):
        aristas = set()
        for i in range(n):
            x, y = pos[i]
            if x + 1 < cols:
                aristas.add((i, i + 1))
            if y + 1 < filas:
                aristas.add((i, i + cols))
        diag = [(i, i + cols + 1) for i in range(n) if pos[i][0] + 1 < cols and pos[i][1] + 1 < filas] + \
               [(i + 1, i + cols) for i in range(n) if pos[i][0] + 1 < cols and pos[i][1] + 1 < filas]
        rng.shuffle(diag)
        for a, b in diag[:5]:
            aristas.add((a, b))

        def colorear(fijos, limite=2):
            sol = []
            col = [None] * n
            for k, v in fijos.items():
                col[k] = v
            ady = {i: [] for i in range(n)}
            for a, b in aristas:
                ady[a].append(b)
                ady[b].append(a)

            def rec(i):
                if len(sol) >= limite:
                    return
                if i == n:
                    sol.append(list(col))
                    return
                if col[i] is not None:
                    if all(col[j] != col[i] for j in ady[i] if j < i):
                        rec(i + 1)
                    return
                for v in range(3):
                    if all(col[j] != v for j in ady[i] if col[j] is not None):
                        col[i] = v
                        rec(i + 1)
                        col[i] = None
            rec(0)
            return sol
        todas = colorear({}, limite=5)
        if not todas:
            continue
        base = todas[0]
        fijos = {}
        orden = list(range(n))
        rng.shuffle(orden)
        for k in orden:
            fijos[k] = base[k]
            if len(colorear(fijos)) == 1:
                break
        if len(fijos) <= 5 and len(colorear(fijos)) == 1:
            sol = colorear(fijos)[0]
            return {"cols": cols, "filas": filas, "aristas": sorted([list(a) for a in aristas]), "fijos": {str(k): v for k, v in sorted(fijos.items())},
                    "colores": COLORES, "solucion": sol}
    raise SystemExit("sin cámaras")


# ------------------------------------------------------------------ canales de riego (árbol de expansión mínimo)
def canales(semilla=4):
    rng = random.Random(semilla)
    pos = {"A": (12, 24), "B": (40, 12), "C": (70, 22), "D": (88, 50), "E": (62, 70), "F": (30, 74), "G": (10, 52)}
    nombres = list(pos)
    for _ in range(5000):
        cand = [(a, b) for a, b in itertools.combinations(nombres, 2)
                if math.dist(pos[a], pos[b]) < 52]
        rng.shuffle(cand)
        aristas = cand[:12]
        pesos = rng.sample(range(2, 40), len(aristas))
        w = {a: p for a, p in zip(aristas, pesos)}
        # conexo
        padre = {n: n for n in nombres}

        def raiz(x):
            while padre[x] != x:
                padre[x] = padre[padre[x]]
                x = padre[x]
            return x
        arbol = []
        for (a, b), p in sorted(w.items(), key=lambda t: t[1]):
            ra, rb = raiz(a), raiz(b)
            if ra != rb:
                padre[ra] = rb
                arbol.append([a, b])
        if len(arbol) == len(nombres) - 1:
            return {"campos": {k: list(v) for k, v in pos.items()}, "canales": [[a, b, p] for (a, b), p in w.items()],
                    "solucion": sorted([sorted(e) for e in arbol]), "coste": sum(w[tuple(e)] if tuple(e) in w else w[(e[1], e[0])] for e in arbol)}
    raise SystemExit("sin canales")


# ------------------------------------------------------------------ reparto de tierras (Shikaku)
def _shikaku_soluciones(n, pistas, limite=2):
    cubierto = [[False] * n for _ in range(n)]
    pdict = {tuple(p[:2]): p[2] for p in pistas}
    sols, usadas, partes = [], set(), []

    def rec():
        if len(sols) >= limite:
            return
        hueco = next(((x, y) for y in range(n) for x in range(n) if not cubierto[y][x]), None)
        if hueco is None:
            sols.append(list(partes))
            return
        x0, y0 = hueco
        for (px, py), area in pdict.items():
            if (px, py) in usadas:
                continue
            for w in range(1, area + 1):
                if area % w:
                    continue
                h = area // w
                if x0 + w > n or y0 + h > n or not (x0 <= px < x0 + w and y0 <= py < y0 + h):
                    continue
                if any(cubierto[y][x] for y in range(y0, y0 + h) for x in range(x0, x0 + w)):
                    continue
                if any((qx, qy) != (px, py) and x0 <= qx < x0 + w and y0 <= qy < y0 + h for (qx, qy) in pdict):
                    continue
                for y in range(y0, y0 + h):
                    for x in range(x0, x0 + w):
                        cubierto[y][x] = True
                usadas.add((px, py))
                partes.append([x0, y0, w, h])
                rec()
                partes.pop()
                usadas.discard((px, py))
                for y in range(y0, y0 + h):
                    for x in range(x0, x0 + w):
                        cubierto[y][x] = False
    rec()
    return sols


def tierras(semilla=6, n=8):
    rng = random.Random(semilla)
    for _ in range(20000):
        cubierto = [[False] * n for _ in range(n)]
        rects = []
        while True:
            hueco = next(((x, y) for y in range(n) for x in range(n) if not cubierto[y][x]), None)
            if hueco is None:
                break
            x0, y0 = hueco
            opciones = [(w, h) for w in range(1, 5) for h in range(1, 5) if 2 <= w * h <= 8 and x0 + w <= n and y0 + h <= n
                        and not any(cubierto[y][x] for y in range(y0, y0 + h) for x in range(x0, x0 + w))]
            if not opciones:
                rects = []
                break
            w, h = rng.choice(opciones)
            for y in range(y0, y0 + h):
                for x in range(x0, x0 + w):
                    cubierto[y][x] = True
            rects.append([x0, y0, w, h])
        if not rects or not 9 <= len(rects) <= 14:
            continue
        pistas = []
        for x0, y0, w, h in rects:
            px, py = rng.randrange(x0, x0 + w), rng.randrange(y0, y0 + h)
            pistas.append([px, py, w * h])
        if len(_shikaku_soluciones(n, pistas)) == 1:
            return {"n": n, "pistas": pistas, "solucion": sorted(rects, key=lambda r: (r[1], r[0]))}
    raise SystemExit("sin tierras")


# ------------------------------------------------------------------ sellos finales
SELLOS = {"14": "pan", "20": "tierra", "40": "agua", "48": "ibis", "52": "ojo", "46": "pluma", "51": "loto", "69": "cetro", "64": "escarabajo",
          "72": "corona"}
ORDEN_SELLOS = ["40", "20", "14", "52", "64"]          # lo que mide el agua, lo que se reparte, el pan, el ojo y el escarabajo


MONTON = monton()
HEQAT = heqat()
PIRAMIDE = piramide()
CRIPTO = cripto()
NILOMETRO = nilometro()
FRISO = friso()
CONTAR = contar()
CAMARAS = camaras()
CANALES = canales()
TIERRAS = tierras()

TODO = {"monton": MONTON, "heqat": HEQAT, "piramide": PIRAMIDE, "nilometro": NILOMETRO, "friso": FRISO, "contar": CONTAR, "cripto": CRIPTO, "camaras": CAMARAS,
        "canales": CANALES, "tierras": TIERRAS, "figuras": FIGURAS, "sellos": SELLOS, "orden_sellos": ORDEN_SELLOS}

if __name__ == "__main__":
    for k, v in TODO.items():
        print(k, json.dumps(v, ensure_ascii=False)[:260])
    with open(os.path.join(AQUI, "instancias_egipto.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(TODO, f, ensure_ascii=False, indent=1)
    print("OK")

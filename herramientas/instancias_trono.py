"""Instancias de los puzles de «Reino de Hielo y Fuego: La Corona del Dragón» (versión de 60 cartas, 21 oct 2026), con solución comprobada.

Once puzles de tipos que no salen en ningún otro juego de la serie:
  jarras       medir una cantidad exacta de hidromiel con dos jarras de capacidad conocida (sin marcas)
  centinelas   ocho centinelas en una muralla de 8 x 8 sin que ninguno vea a otro (problema de las damas), con tres ya colocados
  cuervos      la ruta más corta para visitar seis fortalezas y volver (viajante), con las distancias en una tabla
  playfair     un mensaje cifrado con el cuadrado de Playfair y la clave en una carta
  piedras      el juego de las piedras contra el Rey (Nim): hay que descubrir la estrategia con partidas anteriores
  caminos      puentes entre castillos (Hashi) con los números en dos láminas
  sucesion     quién hereda el trono, deduciéndolo de un árbol de familia y unas leyes
  sudoku       Sudoku de 6 x 6 con los escudos de las seis casas
  torres       torres de hielo (Hanói) con un límite de movimientos
  tapiz        nonograma del tapiz del sigilo, con las pistas de filas y de columnas en dos cartas
  profecia     metapuzle: una cuenta con cuatro cifras que dejan otros puzles
Uso: python herramientas/instancias_trono.py   (comprueba todo y escribe instancias_trono.json)
"""
import itertools
import json
import math
import os
import random
from collections import deque

import generadores_puzles as G

AQUI = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ jarras
def _bfs_jarras(a, b, t):
    ini = (0, 0)
    dist = {ini: 0}
    cola = deque([ini])
    prev = {ini: None}
    while cola:
        s = cola.popleft()
        if t in s:
            ruta = []
            while prev[s]:
                s, m = prev[s]
                ruta.append(m)
            return len(ruta), ruta[::-1]
        x, y = s
        vec = [((a, y), "llenar A"), ((x, b), "llenar B"), ((0, y), "vaciar A"), ((x, 0), "vaciar B"),
               ((x - min(x, b - y), y + min(x, b - y)), "A a B"), ((x + min(y, a - x), y - min(y, a - x)), "B a A")]
        for n, m in vec:
            if n not in dist:
                dist[n] = dist[s] + 1
                prev[n] = (s, m)
                cola.append(n)
    return None, None


def jarras():
    mejor = None
    for a in range(3, 12):
        for b in range(a + 2, 14):
            if math.gcd(a, b) != 1:
                continue
            for t in range(1, b):
                if t in (a, b) or t > b:
                    continue
                n, ruta = _bfs_jarras(a, b, t)
                if n and n <= 12 and (mejor is None or n > mejor[0]):
                    mejor = (n, a, b, t, ruta)
    n, a, b, t, ruta = mejor
    return {"A": a, "B": b, "objetivo": t, "minimo": n, "ruta": ruta}


# ------------------------------------------------------------------ centinelas (ocho damas)
def _damas(n, fijas):
    sols = []
    cols, d1, d2 = set(), set(), set()
    fijas = dict(fijas)                       # fila -> columna
    col = [None] * n

    def rec(f):
        if len(sols) > 1:
            return
        if f == n:
            sols.append(list(col))
            return
        rango = [fijas[f]] if f in fijas else range(n)
        for c in rango:
            if c in cols or (f - c) in d1 or (f + c) in d2:
                continue
            cols.add(c)
            d1.add(f - c)
            d2.add(f + c)
            col[f] = c
            rec(f + 1)
            cols.discard(c)
            d1.discard(f - c)
            d2.discard(f + c)
    rec(0)
    return sols


def centinelas(semilla=4, n=8):
    rng = random.Random(semilla)
    todas = []
    for c in itertools.permutations(range(n)):
        if len({f - c[f] for f in range(n)}) == n and len({f + c[f] for f in range(n)}) == n:
            todas.append(c)
    for _ in range(500):
        sol = rng.choice(todas)
        filas = rng.sample(range(n), 3)
        fijas = {f: sol[f] for f in filas}
        if len(_damas(n, fijas)) == 1:
            return {"n": n, "fijas": [[sol[f], f] for f in sorted(filas)], "solucion": [[sol[f], f] for f in range(n)]}
    raise SystemExit("sin centinelas")


# ------------------------------------------------------------------ cuervos (viajante)
def cuervos(semilla=3):
    rng = random.Random(semilla)
    nombres = ["Piedra Negra", "Invernalia", "Altojardín", "Roca Casterly", "Dorne", "Aguasdulces"]
    for _ in range(2000):
        pos = [(rng.randint(40, 560), rng.randint(110, 500)) for _ in nombres]
        if any(math.dist(a, b) < 120 for a, b in itertools.combinations(pos, 2)):
            continue
        dist = {}
        for i, j in itertools.combinations(range(6), 2):
            dist[(i, j)] = round(math.dist(pos[i], pos[j]) / 10)
        d = lambda a, b: dist[(min(a, b), max(a, b))]
        res = []
        for perm in itertools.permutations(range(1, 6)):
            if perm[0] > perm[-1]:
                continue
            ruta = (0,) + perm + (0,)
            res.append((sum(d(a, b) for a, b in zip(ruta, ruta[1:])), ruta))
        res.sort()
        if res[0][0] < res[1][0] - 1 and res[1][0] - res[0][0] >= 2:
            return {"fortalezas": nombres, "pos": [list(p) for p in pos], "distancias": {f"{i},{j}": v for (i, j), v in dist.items()},
                    "minimo": res[0][0], "solucion": list(res[0][1][:-1]), "segundo": res[1][0]}
    raise SystemExit("sin cuervos")


# ------------------------------------------------------------------ Playfair
def cuadrado_playfair(clave):
    letras = []
    for c in (clave.upper() + "ABCDEFGHIKLMNOPQRSTUVWXYZ"):
        c = "I" if c == "J" else c
        if c not in letras and c.isalpha():
            letras.append(c)
    return [letras[i * 5:(i + 1) * 5] for i in range(5)]


def _pos(cuad, c):
    for f, fila in enumerate(cuad):
        if c in fila:
            return f, fila.index(c)


def playfair_cifra(cuad, claro):
    out = ""
    for i in range(0, len(claro), 2):
        a, b = claro[i], claro[i + 1]
        (fa, ca), (fb, cb) = _pos(cuad, a), _pos(cuad, b)
        if fa == fb:
            out += cuad[fa][(ca + 1) % 5] + cuad[fb][(cb + 1) % 5]
        elif ca == cb:
            out += cuad[(fa + 1) % 5][ca] + cuad[(fb + 1) % 5][cb]
        else:
            out += cuad[fa][cb] + cuad[fb][ca]
    return out


def playfair_descifra(cuad, cif):
    out = ""
    for i in range(0, len(cif), 2):
        a, b = cif[i], cif[i + 1]
        (fa, ca), (fb, cb) = _pos(cuad, a), _pos(cuad, b)
        if fa == fb:
            out += cuad[fa][(ca - 1) % 5] + cuad[fb][(cb - 1) % 5]
        elif ca == cb:
            out += cuad[(fa - 1) % 5][ca] + cuad[(fb - 1) % 5][cb]
        else:
            out += cuad[fa][cb] + cuad[fb][ca]
    return out


def playfair():
    clave, claro = "ESCARCHA", "DRAGONES"
    cuad = cuadrado_playfair(clave)
    cif = playfair_cifra(cuad, claro)
    assert playfair_descifra(cuad, cif) == claro
    assert all(claro[i] != claro[i + 1] for i in range(0, len(claro), 2))
    return {"clave": clave, "cuadrado": cuad, "cifrado": cif, "claro": claro}


# ------------------------------------------------------------------ piedras (Nim con tomas de 1 a 3)
def piedras(semilla=2, n=21):
    rng = random.Random(semilla)
    partidas = []
    for _ in range(3):
        resto = n
        pasos = [resto]
        # el retador empieza y el Rey siempre responde dejando un múltiplo de cuatro
        primera = True
        while resto > 0:
            toma = rng.randint(2, 3) if primera else rng.randint(1, min(3, resto))      # nadie de los retadores acertó con la primera toma
            primera = False
            toma = min(toma, resto)
            resto -= toma
            pasos.append(resto)
            if resto == 0:
                break
            rey = resto % 4 or rng.randint(1, 3)
            resto -= min(rey, resto)
            pasos.append(resto)
        partidas.append(pasos)
    return {"piedras": n, "toma_max": 3, "partidas": partidas, "solucion_primera_toma": n % 4}


# ------------------------------------------------------------------ caminos (Hashi) y tapiz (nonograma)
def caminos():
    return G.hashi(9, 11, 3)


def tapiz():
    return G.nonograma(8, 8, 5, 0.55)


# ------------------------------------------------------------------ sucesión al trono
def sucesion():
    personas = {
        "Aerion": {"nombre": "el rey Aerion", "edad": 70, "sexo": "m", "estado": "muerto", "padre": None},
        "Baelor": {"nombre": "Baelor", "edad": 44, "sexo": "m", "estado": "muerto", "padre": "Aerion"},
        "Maegor": {"nombre": "Maegor", "edad": 40, "sexo": "m", "estado": "septon", "padre": "Aerion"},
        "Aemon": {"nombre": "Aemon", "edad": 35, "sexo": "m", "estado": "vivo", "padre": "Aerion"},
        "Daenys": {"nombre": "Daenys", "edad": 42, "sexo": "f", "estado": "vivo", "padre": "Aerion"},
        "Rhaena": {"nombre": "Rhaena", "edad": 17, "sexo": "f", "estado": "vivo", "padre": "Baelor"},
        "Daemon": {"nombre": "Daemon", "edad": 9, "sexo": "m", "estado": "vivo", "padre": "Baelor"},
        "Jaena": {"nombre": "Jaena", "edad": 14, "sexo": "f", "estado": "vivo", "padre": "Daenys"},
    }
    return {"personas": personas, "solucion": heredero(personas), "rey": "Aerion"}


def heredero(personas, rey="Aerion"):
    """Reglas: 1) no hereda quien está muerto ni quien tiene votos (septón); 2) hereda la línea del hijo mayor antes que la de los menores,
    también cuando ese hijo ha muerto (sus hijos ocupan su lugar); 3) dentro de una línea, antes los varones que las mujeres y, entre iguales, el mayor."""
    def hijos(p):
        return [k for k, v in personas.items() if v["padre"] == p]

    def candidatos(p):
        # personas de la línea de p, en orden de derecho
        hs = sorted(hijos(p), key=lambda k: -personas[k]["edad"])
        varones = [k for k in hs if personas[k]["sexo"] == "m"]
        mujeres = [k for k in hs if personas[k]["sexo"] == "f"]
        orden = []
        for k in varones + mujeres:
            e = personas[k]["estado"]
            if e == "vivo":
                orden.append(k)
            if e in ("vivo", "muerto"):
                orden.extend(candidatos(k))
        return orden
    # primero la línea de los varones y sus descendientes
    for k in candidatos(rey):
        if personas[k]["estado"] == "vivo":
            return k
    return None


# ------------------------------------------------------------------ sudoku 6 x 6 con escudos
def _sudoku_llena(rng):
    g = [[0] * 6 for _ in range(6)]

    def ok(f, c, v):
        if v in g[f] or any(g[i][c] == v for i in range(6)):
            return False
        bf, bc = f // 2 * 2, c // 3 * 3
        return all(g[i][j] != v for i in range(bf, bf + 2) for j in range(bc, bc + 3))

    def rec(k):
        if k == 36:
            return True
        f, c = divmod(k, 6)
        vals = list(range(1, 7))
        rng.shuffle(vals)
        for v in vals:
            if ok(f, c, v):
                g[f][c] = v
                if rec(k + 1):
                    return True
                g[f][c] = 0
        return False
    rec(0)
    return g


def _cuenta_sudoku(g, limite=2):
    g = [f[:] for f in g]
    n = [0]

    def ok(f, c, v):
        if v in g[f] or any(g[i][c] == v for i in range(6)):
            return False
        bf, bc = f // 2 * 2, c // 3 * 3
        return all(g[i][j] != v for i in range(bf, bf + 2) for j in range(bc, bc + 3))

    def rec():
        if n[0] >= limite:
            return
        vac = next(((f, c) for f in range(6) for c in range(6) if not g[f][c]), None)
        if not vac:
            n[0] += 1
            return
        f, c = vac
        for v in range(1, 7):
            if ok(f, c, v):
                g[f][c] = v
                rec()
                g[f][c] = 0
    rec()
    return n[0]


def sudoku(semilla=9):
    rng = random.Random(semilla)
    sol = _sudoku_llena(rng)
    g = [f[:] for f in sol]
    celdas = [(f, c) for f in range(6) for c in range(6)]
    rng.shuffle(celdas)
    for f, c in celdas:
        if sum(1 for x in g for y in x if y) <= 14:
            break
        v = g[f][c]
        g[f][c] = 0
        if _cuenta_sudoku(g) != 1:
            g[f][c] = v
    return {"dados": g, "solucion": sol, "casas": ["lobo", "leon", "kraken", "rosa", "sol", "trucha"]}


# ------------------------------------------------------------------ escudos de las seis casas (figuras en una caja de 100 x 100)
def _elipse(cx, cy, rx, ry, n=24):
    return [[round(cx + rx * math.cos(2 * math.pi * k / n), 1), round(cy + ry * math.sin(2 * math.pi * k / n), 1)] for k in range(n)]


CASAS_FIG = {
    "lobo": [{"t": "p", "p": [[18, 74], [24, 20], [42, 42], [58, 42], [76, 20], [82, 74], [62, 92], [38, 92]]},
             {"t": "c", "c": [38, 62], "r": 5, "f": "fondo"}, {"t": "c", "c": [62, 62], "r": 5, "f": "fondo"}],
    "leon": [{"t": "c", "c": [50, 50], "r": 36, "w": 10}, {"t": "c", "c": [50, 50], "r": 22}, {"t": "c", "c": [42, 46], "r": 4, "f": "fondo"},
             {"t": "c", "c": [58, 46], "r": 4, "f": "fondo"}],
    "kraken": [{"t": "p", "p": _elipse(50, 38, 26, 24)}, {"t": "l", "p": [[28, 54], [18, 78], [28, 92]], "w": 7}, {"t": "l", "p": [[42, 60], [38, 80], [46, 94]], "w": 7},
               {"t": "l", "p": [[58, 60], [62, 80], [54, 94]], "w": 7}, {"t": "l", "p": [[72, 54], [82, 78], [72, 92]], "w": 7},
               {"t": "c", "c": [42, 36], "r": 4, "f": "fondo"}, {"t": "c", "c": [58, 36], "r": 4, "f": "fondo"}],
    "rosa": [{"t": "c", "c": [50, 24], "r": 16}, {"t": "c", "c": [24, 44], "r": 16}, {"t": "c", "c": [76, 44], "r": 16}, {"t": "c", "c": [34, 74], "r": 16},
             {"t": "c", "c": [66, 74], "r": 16}, {"t": "c", "c": [50, 52], "r": 12, "f": "fondo"}],
    "sol": [{"t": "c", "c": [50, 50], "r": 22}] + [{"t": "l", "p": [[50 + 30 * math.cos(k * math.pi / 4), 50 + 30 * math.sin(k * math.pi / 4)],
                                                                    [50 + 46 * math.cos(k * math.pi / 4), 50 + 46 * math.sin(k * math.pi / 4)]], "w": 7} for k in range(8)],
    "trucha": [{"t": "p", "p": _elipse(44, 50, 34, 20)}, {"t": "p", "p": [[74, 50], [96, 26], [96, 74]]}, {"t": "c", "c": [28, 44], "r": 4, "f": "fondo"}],
}


# ------------------------------------------------------------------ torres de hielo (Hanói)
def torres(discos=4):
    return {"discos": discos, "limite": 2 ** discos - 1}


# ------------------------------------------------------------------ la profecía final
DATOS = {"40": 7, "14": 6, "52": 3, "20": 4}           # la cifra que deja cada puzle al resolverse
ORDEN = ["40", "14", "52", "20"]                       # cuervos, jarras, piedras y centinelas
FORMULA = "a × b − c + d"
RESULTADO = DATOS[ORDEN[0]] * DATOS[ORDEN[1]] - DATOS[ORDEN[2]] + DATOS[ORDEN[3]]


_CACHE = os.path.join(AQUI, "instancias_trono.json")
if os.path.exists(_CACHE) and __name__ != "__main__":
    # los generadores tardan: al importar se leen las instancias ya comprobadas (se regeneran con `python herramientas/instancias_trono.py`)
    _C = json.load(open(_CACHE, encoding="utf-8"))
    JARRAS, CENTINELAS, CUERVOS, PLAYFAIR, PIEDRAS, CAMINOS, SUCESION, SUDOKU, TORRES, TAPIZ = (
        _C[k] for k in ("jarras", "centinelas", "cuervos", "playfair", "piedras", "caminos", "sucesion", "sudoku", "torres", "tapiz"))
else:
    JARRAS = jarras()
    CENTINELAS = centinelas()
    CUERVOS = cuervos()
    PLAYFAIR = playfair()
    PIEDRAS = piedras()
    CAMINOS = caminos()
    SUCESION = sucesion()
    SUDOKU = sudoku()
    TORRES = torres()
    TAPIZ = tapiz()

TODO = {"jarras": JARRAS, "centinelas": CENTINELAS, "cuervos": CUERVOS, "playfair": PLAYFAIR, "piedras": PIEDRAS, "caminos": CAMINOS,
        "sucesion": SUCESION, "sudoku": SUDOKU, "torres": TORRES, "tapiz": TAPIZ,
        "profecia": {"datos": DATOS, "orden": ORDEN, "formula": FORMULA, "resultado": RESULTADO}}

if __name__ == "__main__":
    for k, v in TODO.items():
        print(k, json.dumps(v)[:200])
    with open(_CACHE, "w", encoding="utf-8", newline="\n") as f:
        json.dump(TODO, f, ensure_ascii=False, indent=1)
    print("OK")

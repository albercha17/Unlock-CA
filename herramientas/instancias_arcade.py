"""Instancias de los puzles de «Game Over, 1985: La Última Moneda» (versión de 60 cartas, 22 oct 2026), con solución comprobada.

Once puzles de tipos que no salen en ningún otro juego de la serie:
  circuito     un circuito de puertas lógicas con seis interruptores: solo una combinación enciende una lámpara y apaga la otra
  atasco       un aparcamiento de naves (Rush Hour) con una nave que debe salir
  sprite       un sprite de 12 x 12 comprimido por tandas (RLE): hay que descomprimirlo pintando casillas
  ascii        un mensaje en bytes hexadecimales y la tabla de caracteres
  fantasmas    un problema lógico de cuatro fantasmas (pasillo, velocidad y fruta favorita) con pistas en dos cartas
  magico       un cuadrado mágico de 4 x 4 con algunos números ya puestos (suma 34)
  ranking      ordenar una tabla de puntuaciones solo con intercambios entre vecinos y con un máximo de intercambios
  deslizante   un puzle deslizante de 8 fichas con el dibujo final en una carta
  rana         cruzar siete carriles de tráfico programando los pasos antes de empezar (Frogger por turnos)
  monedas      pagar un precio exacto con el menor número de monedas de una máquina de cambio raro
  xor          metapuzle: el XOR de los bytes que dejan cuatro puzles
Uso: python herramientas/instancias_arcade.py   (comprueba todo y escribe instancias_arcade.json)
"""
import itertools
import json
import math
import os
import random
from collections import deque

import generadores_puzles as G

AQUI = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ circuito lógico
OPS = {"AND": lambda a, b: a & b, "OR": lambda a, b: a | b, "XOR": lambda a, b: a ^ b, "NAND": lambda a, b: 1 - (a & b), "NOR": lambda a, b: 1 - (a | b)}


def _eval(circ, ent):
    v = dict(ent)
    for nombre, op, a, b in circ["puertas"]:
        v[nombre] = OPS[op](v[a], v[b])
    return v


def circuito(semilla=4):
    rng = random.Random(semilla)
    ops = list(OPS)
    for _ in range(20000):
        p = [("P1", rng.choice(ops), "A", "B"), ("P2", rng.choice(ops), "C", "D"), ("P3", rng.choice(ops), "E", "F"),
             ("P4", rng.choice(ops), rng.choice(["P1", "P2"]), rng.choice(["P2", "P3"])), ("P5", rng.choice(ops), rng.choice(["P1", "P3"]), "P2"),
             ("P6", rng.choice(ops), "P4", "P5"), ("P7", rng.choice(ops), rng.choice(["P4", "P5"]), rng.choice(["P3", "P1"]))]
        if p[3][2] == p[3][3] or {p[3][2], p[3][3]} == {p[4][2], p[4][3]} or len({(g[2], g[3]) for g in p}) < 7:
            continue
        circ = {"puertas": p, "salidas": {"X": "P6", "Y": "P7"}}
        buenas = []
        for bits in itertools.product((0, 1), repeat=6):
            ent = dict(zip("ABCDEF", bits))
            v = _eval(circ, ent)
            if v["P6"] == 1 and v["P7"] == 0:
                buenas.append(bits)
                if len(buenas) > 1:
                    break
        if len(buenas) == 1 and 2 <= sum(buenas[0]) <= 4:
            return {"puertas": [list(g) for g in p], "salidas": circ["salidas"], "solucion": list(buenas[0])}
    raise SystemExit("sin circuito")


# ------------------------------------------------------------------ atasco de naves
def atasco():
    r = G.rush_hour(5, 6, 14)
    return {"n": r["n"], "naves": r["coches"], "minimo": r["movimientos_minimos"], "ruta": G.rush_hour_ruta(r)}


# ------------------------------------------------------------------ sprite RLE
def sprite():
    # un fantasmita de 12 x 12
    filas = ["....####....", "..########..", ".##########.", "###..##..###", "###..##..###", "############", "############", "############",
             "############", "##.##..##.##", "#...#..#...#", "............"]
    assert all(len(f) == 12 for f in filas) and len(filas) == 12
    g = [[1 if c == "#" else 0 for c in f] for f in filas]
    runs = []
    for fila in g:
        r, cur, n = [], 0, 0
        for v in fila:
            if v == cur:
                n += 1
            else:
                r.append(n)
                cur, n = v, 1
        r.append(n)
        runs.append(r)
    return {"filas": 12, "cols": 12, "pixeles": g, "tandas": runs}


# ------------------------------------------------------------------ ascii hexadecimal
def ascii_hex():
    claro = "CONTINUE"
    hexa = [f"{ord(c):02X}" for c in claro]
    tabla = {chr(c): f"{c:02X}" for c in range(ord("A"), ord("Z") + 1)}
    return {"claro": claro, "bytes": hexa, "tabla": tabla}


# ------------------------------------------------------------------ fantasmas (lógica)
GH = ["rojo", "rosa", "cian", "naranja"]
VEL = ["lento", "normal", "rápido", "loco"]
FRU = ["cereza", "fresa", "naranja", "manzana"]


def _desc_texto(d):
    k, v = d
    if k == "g":
        return f"el fantasma {v}"
    if k == "v":
        return f"el fantasma {v}" if v != "loco" else "el fantasma loco"
    return f"el que persigue la {v}" if v in ("cereza", "fresa", "manzana") else f"el que persigue la {v}"


def fantasmas(semilla=7):
    rng = random.Random(semilla)
    sol = {"pos": rng.sample(range(1, 5), 4), "vel": rng.sample(range(4), 4), "fru": rng.sample(range(4), 4)}

    def pos_de(s, d):
        k, v = d
        i = GH.index(v) if k == "g" else (s["vel"].index(VEL.index(v)) if k == "v" else s["fru"].index(FRU.index(v)))
        return s["pos"][i]

    def cumple(s, c):
        rel, a, b = c
        pa = pos_de(s, a)
        if rel == "extremo":
            return pa in (1, 4)
        pb = pos_de(s, b)
        return {"igual": pa == pb, "izq_inm": pa + 1 == pb, "izq": pa < pb, "distinto": pa != pb}[rel]

    todas = [s for s in ({"pos": list(p), "vel": list(v), "fru": list(f)} for p in itertools.permutations(range(1, 5))
                         for v in itertools.permutations(range(4)) for f in itertools.permutations(range(4)))]
    pool = []
    for _ in range(4000):
        k1, k2 = rng.sample(["g", "v", "f"], 2) if rng.random() < 0.8 else (rng.choice(["g", "v", "f"]),) * 2
        vals = {"g": GH, "v": VEL, "f": FRU}
        a, b = (k1, rng.choice(vals[k1])), (k2, rng.choice(vals[k2]))
        if a == b:
            continue
        rel = rng.choice(["igual", "izq_inm", "izq", "izq", "distinto", "extremo"])
        c = (rel, a, b if rel != "extremo" else a)
        if cumple(sol, c):
            pool.append(c)
    rng.shuffle(pool)
    cands = list(todas)
    clues = []
    for c in pool:
        nuevo = [s for s in cands if cumple(s, c)]
        if len(nuevo) < len(cands):
            clues.append(c)
            cands = nuevo
        if len(cands) == 1:
            break
    assert len(cands) == 1
    # quitar pistas que sobren
    i = 0
    while i < len(clues):
        resto = clues[:i] + clues[i + 1:]
        c2 = [s for s in todas if all(cumple(s, c) for c in resto)]
        if len(c2) == 1:
            clues = resto
        else:
            i += 1

    def texto(c):
        rel, a, b = c
        A, B = _desc_texto(a), _desc_texto(b)
        A, B = A[0].upper() + A[1:], B
        return {"igual": f"{A} es {B}.", "izq_inm": f"{A} está justo a la izquierda de {B}.", "izq": f"{A} está a la izquierda de {B}.",
                "distinto": f"{A} no es {B}.", "extremo": f"{A} está en un extremo del salón."}[rel]
    return {"fantasmas": GH, "velocidades": VEL, "frutas": FRU, "pistas": [texto(c) for c in clues],
            "solucion": [{"fantasma": GH[i], "pasillo": sol["pos"][i], "velocidad": VEL[sol["vel"][i]], "fruta": FRU[sol["fru"][i]]} for i in range(4)]}


# ------------------------------------------------------------------ cuadrado mágico 4 x 4
def _magicos():
    res = []
    usados = [False] * 18
    g = [[0] * 4 for _ in range(4)]

    def rec(k):
        if k == 16:
            if sum(g[i][i] for i in range(4)) == 34 and sum(g[i][3 - i] for i in range(4)) == 34:
                res.append([f[:] for f in g])
            return
        f, c = divmod(k, 4)
        for v in range(1, 17):
            if usados[v]:
                continue
            if c == 3 and sum(g[f][:3]) + v != 34:
                continue
            if f == 3 and sum(g[i][c] for i in range(3)) + v != 34:
                continue
            usados[v] = True
            g[f][c] = v
            ok = True
            if c == 2:                                   # la cuarta casilla de la fila queda decidida
                need = 34 - sum(g[f][:3])
                ok = 1 <= need <= 16 and not usados[need]
            if ok and f == 2:                            # y la cuarta de la columna
                need = 34 - sum(g[i][c] for i in range(3))
                ok = 1 <= need <= 16 and not usados[need] and (need != v)
            if ok:
                rec(k + 1)
            usados[v] = False
            g[f][c] = 0
    rec(0)
    return res


def magico(semilla=2):
    rng = random.Random(semilla)
    todos = _magicos()
    assert len(todos) == 7040
    for _ in range(2000):
        sol = rng.choice(todos)
        celdas = rng.sample([(x, y) for y in range(4) for x in range(4)], 6)
        enc = [s for s in todos if all(s[y][x] == sol[y][x] for x, y in celdas)]
        if len(enc) == 1:
            return {"dados": [[x, y, sol[y][x]] for x, y in sorted(celdas, key=lambda t: (t[1], t[0]))], "solucion": sol}
    raise SystemExit("sin mágico")


# ------------------------------------------------------------------ ranking (ordenar con intercambios entre vecinos)
def ranking(semilla=5, n=8):
    rng = random.Random(semilla)
    for _ in range(1000):
        puntos = rng.sample(range(100, 1000, 10), n)
        orden = puntos[:]
        rng.shuffle(orden)
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if orden[i] > orden[j])
        if 12 <= inv <= 17:
            return {"puntos": orden, "limite": inv, "solucion": sorted(orden)}
    raise SystemExit("sin ranking")


# ------------------------------------------------------------------ puzle deslizante de 8 fichas
OBJETIVO = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]


def deslizante(semilla=3):
    rng = random.Random(semilla)
    for _ in range(2000):
        g = [f[:] for f in OBJETIVO]
        ult = None
        for _ in range(60):
            y, x = next((i, f.index(0)) for i, f in enumerate(g) if 0 in f)
            opc = [(dx, dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < 3 and 0 <= y + dy < 3 and (dx, dy) != ult]
            dx, dy = rng.choice(opc)
            g[y][x], g[y + dy][x + dx] = g[y + dy][x + dx], 0
            ult = (-dx, -dy)
        ini = tuple(tuple(f) for f in g)
        meta = tuple(tuple(f) for f in OBJETIVO)
        dist = {ini: 0}
        cola = deque([ini])
        while cola:
            s = cola.popleft()
            if s == meta:
                break
            y, x = next((i, f.index(0)) for i, f in enumerate(s) if 0 in f)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if 0 <= x + dx < 3 and 0 <= y + dy < 3:
                    t = [list(f) for f in s]
                    t[y][x], t[y + dy][x + dx] = t[y + dy][x + dx], 0
                    t = tuple(tuple(f) for f in t)
                    if t not in dist:
                        dist[t] = dist[s] + 1
                        cola.append(t)
        if 18 <= dist[meta] <= 24:
            return {"inicio": [list(f) for f in ini], "objetivo": OBJETIVO, "minimo": dist[meta]}
    raise SystemExit("sin deslizante")


# ------------------------------------------------------------------ rana (Frogger por turnos)
def rana(semilla=6, ancho=8, carriles=5):
    rng = random.Random(semilla)
    for _ in range(5000):
        lanes = []
        for _ in range(carriles):
            vel = rng.choice([1, 1, 2])
            dir_ = rng.choice([-1, 1])
            n = rng.choice([2, 3])
            pos = sorted(rng.sample(range(ancho), n))
            lanes.append({"vel": vel, "dir": dir_, "coches": pos})

        def ocupado(carril, col, t):
            L = lanes[carril]
            return any((p + L["dir"] * L["vel"] * t) % ancho == col for p in L["coches"])
        ini = (carriles + 1, ancho // 2, 0)
        prev = {ini: None}
        cola = deque([ini])
        fin = None
        while cola:
            f, c, t = cola.popleft()
            if f == 0:
                fin = (f, c, t)
                break
            if t >= 16:
                continue
            for mv, (df, dc) in (("U", (-1, 0)), ("L", (0, -1)), ("R", (0, 1)), ("W", (0, 0))):
                nf, nc = f + df, c + dc
                if not (0 <= nc < ancho) or nf < 0:
                    continue
                if 1 <= nf <= carriles and ocupado(nf - 1, nc, t + 1):
                    continue
                e = (nf, nc, t + 1)
                if e not in prev:
                    prev[e] = ((f, c, t), mv)
                    cola.append(e)
        if fin and 11 <= fin[2] <= 14:
            ruta, e = [], fin
            while prev[e]:
                e, m = prev[e]
                ruta.append(m)
            return {"ancho": ancho, "carriles": lanes, "inicio": [carriles + 1, ancho // 2], "minimo": fin[2], "solucion": "".join(ruta[::-1])}
    raise SystemExit("sin rana")


# ------------------------------------------------------------------ monedas (cambio mínimo con un sistema raro)
def monedas():
    mejor = None
    for tipo in itertools.combinations([2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 16, 18, 20], 3):
        tipos = (1,) + tipo
        for precio in range(24, 48):
            best = {0: 0}
            for v in range(1, precio + 1):
                best[v] = min(best[v - c] + 1 for c in tipos if v - c >= 0)
            m = best[precio]
            if m < 4:
                continue
            r, voraz = precio, 0
            for t in sorted(tipos, reverse=True):
                voraz += r // t
                r %= t
            if voraz < m + 2:
                continue
            maneras = [c for c in itertools.product(*[range(min(m, precio // t) + 1) for t in tipos]) if sum(c) == m and sum(a * t for a, t in zip(c, tipos)) == precio]
            if len(maneras) == 1:
                cur = (voraz - m, m, tipos, precio, maneras[0])
                if mejor is None or cur[:2] > mejor[:2]:
                    mejor = cur
    d, m, tipos, precio, man = mejor
    return {"monedas": list(tipos), "precio": precio, "minimo": m, "voraz": m + d, "solucion": list(man)}


# ------------------------------------------------------------------ XOR final
BYTES = {"14": 6, "52": 9, "40": 11, "69": 12}          # el byte que deja cada puzle al resolverse
ORDEN = ["14", "52", "40", "69"]                        # circuito, fantasmas, sprite y rana
RESULTADO = BYTES[ORDEN[0]] ^ BYTES[ORDEN[1]] ^ BYTES[ORDEN[2]] ^ BYTES[ORDEN[3]]


_CACHE = os.path.join(AQUI, "instancias_arcade.json")
if os.path.exists(_CACHE) and __name__ != "__main__":
    # los generadores tardan: al importar se leen las instancias ya comprobadas (se regeneran con `python herramientas/instancias_arcade.py`)
    _C = json.load(open(_CACHE, encoding="utf-8"))
    CIRCUITO, ATASCO, SPRITE_D, ASCII, FANTASMAS, MAGICO, RANKING, DESLIZANTE, RANA, MONEDAS = (
        _C[k] for k in ("circuito", "atasco", "sprite", "ascii", "fantasmas", "magico", "ranking", "deslizante", "rana", "monedas"))
else:
    CIRCUITO = circuito()
    ATASCO = atasco()
    SPRITE_D = sprite()
    ASCII = ascii_hex()
    FANTASMAS = fantasmas()
    MAGICO = magico()
    RANKING = ranking()
    DESLIZANTE = deslizante()
    RANA = rana()
    MONEDAS = monedas()

TODO = {"circuito": CIRCUITO, "atasco": ATASCO, "sprite": SPRITE_D, "ascii": ASCII, "fantasmas": FANTASMAS, "magico": MAGICO, "ranking": RANKING,
        "deslizante": DESLIZANTE, "rana": RANA, "monedas": MONEDAS, "xor": {"bytes": BYTES, "orden": ORDEN, "resultado": RESULTADO}}

if __name__ == "__main__":
    for k, v in TODO.items():
        print(k, json.dumps(v)[:200])
    with open(_CACHE, "w", encoding="utf-8", newline="\n") as f:
        json.dump(TODO, f, ensure_ascii=False, indent=1)
    print("OK")

"""Instancias de los puzles de «Marte, 2157: Cúpula Aurora» (versión de 60 cartas, 21 oct 2026), con solución comprobada.

Once puzles de tipos que no salen en ningún otro juego de la serie:
  satelites   ventana de comunicaciones: cuándo coinciden por primera vez tres satélites (periodos y desfases en una carta)
  vida        invernadero: un paso del «juego de la vida» de Conway sobre una rejilla de plantas
  cableado    unir pares de bornes del mismo color con cables que no se cruzan y cubren toda la placa (Numberlink)
  rocas       campo de rocas: marcar las rocas ocultas con los números del radar (buscaminas con solución única)
  balancin    equilibrar el brazo de la antena: pesos a distintas distancias del eje (momentos)
  cifras      cuenta de cifras: llegar a un número con seis números y las cuatro operaciones
  anillo      el circuito del reactor: un solo bucle cerrado que rodea cada número tantas veces como dice (Slitherlink)
  programa    programar el rover con bucles y un límite de bloques
  paneles     paneles de refrigeración: encender un patrón sabiendo que cada panel cambia a sus vecinos (Lights Out)
  sopa        sopa de letras cuyas letras sobrantes forman la palabra de acceso
  consola     metapuzle: cuatro datos de otros puzles marcados en un orden dado por acertijos
Uso: python herramientas/instancias_marte.py   (comprueba todo y escribe instancias_marte.json)
"""
import itertools
import json
import os
import random
from collections import deque

AQUI = os.path.dirname(os.path.abspath(__file__))
V4 = [(0, -1), (1, 0), (0, 1), (-1, 0)]


# ------------------------------------------------------------------ satélites
def satelites():
    periodos = [5, 8, 12]
    t = 53
    pasos = [(t % p, p) for p in periodos]                       # (primer paso, periodo)
    # el primer instante positivo en que pasan los tres a la vez
    sol = next(x for x in range(1, 400) if all(x % p == a for a, p in pasos))
    assert sol == t
    nombres = ["Fobos-1", "Deimos-2", "Aurora-3"]
    return {"sats": [{"nombre": n, "primer": a, "periodo": p, "pasos_vistos": [a + p * k for k in range(0, 40) if a + p * k <= 28 and a + p * k > 0]}
                     for n, (a, p) in zip(nombres, pasos)], "horas_vistas": 28, "solucion": sol}


# ------------------------------------------------------------------ vida (un paso de Conway)
def _paso_vida(g):
    n = len(g)
    out = [[0] * n for _ in range(n)]
    for y in range(n):
        for x in range(n):
            v = sum(g[y + dy][x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dx or dy) and 0 <= y + dy < n and 0 <= x + dx < n)
            out[y][x] = 1 if (g[y][x] and v in (2, 3)) or (not g[y][x] and v == 3) else 0
    return out


def vida(semilla=4, n=6):
    rng = random.Random(semilla)
    for _ in range(5000):
        g = [[1 if rng.random() < 0.42 else 0 for _ in range(n)] for _ in range(n)]
        s = _paso_vida(g)
        vivas, nuevas = sum(map(sum, g)), sum(map(sum, s))
        cambia = sum(g[y][x] != s[y][x] for y in range(n) for x in range(n))
        if 12 <= vivas <= 18 and 8 <= nuevas <= 16 and cambia >= 14:
            return {"n": n, "actual": g, "solucion": s}
    raise SystemExit("sin vida")


# ------------------------------------------------------------------ cableado (Numberlink)
def _camino_hamilton(n, rng):
    camino = [(x, y) if y % 2 == 0 else (n - 1 - x, y) for y in range(n) for x in range(n)]
    for _ in range(3000):
        if rng.random() < 0.5:
            camino.reverse()
        fin = camino[-1]
        vec = [(fin[0] + dx, fin[1] + dy) for dx, dy in V4 if (fin[0] + dx, fin[1] + dy) in camino]
        v = rng.choice(vec)
        j = camino.index(v)
        if j >= len(camino) - 2:
            continue
        camino = camino[:j + 1] + camino[j + 1:][::-1]
    return camino


def _soluciones_cableado(n, extremos, limite=2):
    """Cuenta las formas de unir cada par con un camino, cubriendo todas las casillas."""
    colores = list(extremos)
    ocupada = {}
    for c, (a, b) in extremos.items():
        ocupada[a] = c
        ocupada[b] = c
    sols = []
    total = n * n

    def libres_validas():
        for y in range(n):
            for x in range(n):
                if (x, y) in ocupada:
                    continue
                vec = 0
                for dx, dy in V4:
                    q = (x + dx, y + dy)
                    if 0 <= q[0] < n and 0 <= q[1] < n and (q not in ocupada or q in fin_abierto):
                        vec += 1
                if vec < 2:
                    return False
        return True
    fin_abierto = set()

    def pinta(ci):
        if len(sols) >= limite:
            return
        if ci == len(colores):
            if len(ocupada) == total:
                sols.append(dict(ocupada))
            return
        c = colores[ci]
        a, b = extremos[c]

        def dfs(p):
            if len(sols) >= limite:
                return
            for dx, dy in V4:
                q = (p[0] + dx, p[1] + dy)
                if not (0 <= q[0] < n and 0 <= q[1] < n):
                    continue
                if q == b:
                    # camino completo para este color
                    fin_abierto.discard(b)
                    pinta(ci + 1)
                    fin_abierto.add(b)
                    continue
                if q in ocupada:
                    continue
                ocupada[q] = c
                dfs(q)
                del ocupada[q]
        # los extremos de los colores aún sin pintar siguen siendo «puertas» para las casillas libres
        for c2 in colores[ci:]:
            fin_abierto.update(extremos[c2])
        dfs(a)
        for c2 in colores[ci:]:
            fin_abierto.difference_update(extremos[c2])
    pinta(0)
    return sols


def cableado(semilla=5, n=6, k=5):
    rng = random.Random(semilla)
    for _ in range(400):
        camino = _camino_hamilton(n, rng)
        cortes = sorted(rng.sample(range(3, len(camino) - 3), k - 1))
        trozos, ini = [], 0
        for c in cortes + [len(camino)]:
            trozos.append(camino[ini:c])
            ini = c
        if any(len(t) < 4 for t in trozos):
            continue
        extremos = {i: (t[0], t[-1]) for i, t in enumerate(trozos)}
        sols = _soluciones_cableado(n, extremos)
        if len(sols) == 1:
            col = [[None] * n for _ in range(n)]
            for (x, y), c in sols[0].items():
                col[y][x] = c
            return {"n": n, "colores": k, "extremos": {str(c): [list(a), list(b)] for c, (a, b) in extremos.items()}, "solucion": col}
    raise SystemExit("sin cableado")


# ------------------------------------------------------------------ campo de rocas (buscaminas)
def _vecinas(x, y, n):
    return [(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx or dy) and 0 <= x + dx < n and 0 <= y + dy < n]


def _contar_rocas(n, reveladas, numeros, total, limite=2):
    celdas = [(x, y) for y in range(n) for x in range(n) if (x, y) not in reveladas]
    asign, sols = {}, []
    # para cada pista: casillas ocultas que la rodean
    ocultas_de = {p: [q for q in _vecinas(p[0], p[1], n) if q not in reveladas] for p in reveladas}
    pistas_de = {c: [p for p in reveladas if c in ocultas_de[p]] for c in celdas}
    cuenta = {p: 0 for p in reveladas}
    sin_asignar = {p: len(ocultas_de[p]) for p in reveladas}

    def rec(i, minas):
        if len(sols) >= limite:
            return
        if i == len(celdas):
            if minas == total and all(cuenta[p] == numeros[p] for p in reveladas):
                sols.append(dict(asign))
            return
        if minas > total or minas + (len(celdas) - i) < total:
            return
        c = celdas[i]
        for v in (0, 1):
            asign[c] = v
            ok = True
            for p in pistas_de[c]:
                cuenta[p] += v
                sin_asignar[p] -= 1
            for p in pistas_de[c]:
                if cuenta[p] > numeros[p] or cuenta[p] + sin_asignar[p] < numeros[p]:
                    ok = False
            if ok:
                rec(i + 1, minas + v)
            for p in pistas_de[c]:
                cuenta[p] -= v
                sin_asignar[p] += 1
            del asign[c]
    rec(0, 0)
    return sols


def rocas(semilla=7, n=8, total=11):
    rng = random.Random(semilla)
    for _ in range(300):
        minas = set()
        while len(minas) < total:
            minas.add((rng.randrange(n), rng.randrange(n)))
        reveladas = {(x, y) for y in range(n) for x in range(n) if (x, y) not in minas}
        numeros = {p: sum(1 for q in _vecinas(p[0], p[1], n) if q in minas) for p in reveladas}
        orden = list(reveladas)
        rng.shuffle(orden)
        for p in orden:
            if len(reveladas) <= 22:
                break
            r2 = set(reveladas)
            r2.discard(p)
            if len(_contar_rocas(n, r2, {q: numeros[q] for q in r2}, total)) == 1:
                reveladas = r2
        if len(reveladas) <= 24 and len(_contar_rocas(n, reveladas, numeros, total)) == 1:
            return {"n": n, "total": total, "numeros": [[x, y, numeros[(x, y)]] for (x, y) in sorted(reveladas, key=lambda t: (t[1], t[0]))],
                    "solucion": sorted([list(m) for m in minas], key=lambda t: (t[1], t[0]))}
    raise SystemExit("sin rocas")


# ------------------------------------------------------------------ balancín
def balancin(semilla=3):
    rng = random.Random(semilla)
    posiciones = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
    for _ in range(200000):
        pesos = rng.sample(range(1, 10), 6)
        sitios = rng.sample(posiciones, 6)
        if sum(p * s for p, s in zip(pesos, sitios)) != 0:
            continue
        fijos = list(zip(pesos[:3], sitios[:3]))
        libres = pesos[3:]
        pos_libres = [s for s in posiciones if s not in sitios[:3]]
        mom0 = sum(p * s for p, s in fijos)
        sols = []
        for perm in itertools.permutations(pos_libres, len(libres)):
            if mom0 + sum(p * s for p, s in zip(libres, perm)) == 0:
                sols.append(perm)
                if len(sols) > 1:
                    break
        if len(sols) == 1:
            return {"posiciones": posiciones, "fijos": [list(f) for f in fijos], "libres": libres, "solucion": list(sols[0])}
    raise SystemExit("sin balancín")


# ------------------------------------------------------------------ cifras
def _alcanzables(nums):
    """Número mínimo de operaciones para llegar a cada valor con operaciones exactas entre los números disponibles."""
    mejor = {}

    def rec(lista, pasos):
        for v in lista:
            if v not in mejor or mejor[v] > pasos:
                mejor[v] = pasos
        for i in range(len(lista)):
            for j in range(i + 1, len(lista)):
                a, b = lista[i], lista[j]
                resto = [lista[k] for k in range(len(lista)) if k not in (i, j)]
                res = {a + b, a * b}
                if a != b:
                    res.add(abs(a - b))
                if b and a % b == 0:
                    res.add(a // b)
                if a and b % a == 0:
                    res.add(b // a)
                for r in res:
                    if r > 0:
                        rec(resto + [r], pasos + 1)
    rec(list(nums), 0)
    return mejor


def solucion_cifras(nums, objetivo):
    """Una lista de operaciones [(a, op, b, r), ...] que lleva a `objetivo` (las mismas operaciones que permite la app)."""
    def rec(lista, pasos):
        if objetivo in lista:
            return pasos
        for i in range(len(lista)):
            for j in range(len(lista)):
                if i == j:
                    continue
                a, b = lista[i], lista[j]
                resto = [lista[k] for k in range(len(lista)) if k not in (i, j)]
                cand = [("+", a + b)] if i < j else []
                if i < j:
                    cand.append(("×", a * b))
                if a - b > 0:
                    cand.append(("−", a - b))
                if b and a % b == 0:
                    cand.append(("÷", a // b))
                for op, r in cand:
                    sol = rec(resto + [r], pasos + [(a, op, b, r)])
                    if sol:
                        return sol
        return None
    return rec(list(nums), [])


def cifras(semilla=2):
    rng = random.Random(semilla)
    for _ in range(300):
        nums = sorted(rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4) + [rng.choice([25, 50, 75]), rng.choice([100, 20, 30])])
        mejor = _alcanzables(nums)
        cand = [v for v, p in mejor.items() if p == 4 and 100 <= v <= 999 and v not in nums]
        if cand:
            return {"numeros": nums, "objetivo": rng.choice(sorted(cand)), "minimo": 4}
    raise SystemExit("sin cifras")


# ------------------------------------------------------------------ anillo del reactor (Slitherlink)
def _aristas_celda(x, y):
    return [("h", x, y), ("h", x, y + 1), ("v", x, y), ("v", x + 1, y)]


def _bucle_valido(aristas, n):
    """¿Las aristas forman un solo bucle cerrado?"""
    ady = {}
    for t, x, y in aristas:
        a, b = ((x, y), (x + 1, y)) if t == "h" else ((x, y), (x, y + 1))
        ady.setdefault(a, []).append(b)
        ady.setdefault(b, []).append(a)
    if not ady or any(len(v) != 2 for v in ady.values()):
        return False
    ini = next(iter(ady))
    vistos, cola = {ini}, deque([ini])
    while cola:
        p = cola.popleft()
        for q in ady[p]:
            if q not in vistos:
                vistos.add(q)
                cola.append(q)
    return len(vistos) == len(ady)


def _bucle_aleatorio(n, rng):
    for _ in range(2000):
        region = {(rng.randrange(n), rng.randrange(n))}
        objetivo = rng.randint(n * n // 2 - 2, n * n // 2 + 4)
        while len(region) < objetivo:
            x, y = rng.choice(sorted(region))
            dx, dy = rng.choice(V4)
            q = (x + dx, y + dy)
            if 0 <= q[0] < n and 0 <= q[1] < n:
                region.add(q)
        aristas = set()
        for x, y in region:
            for e in _aristas_celda(x, y):
                aristas ^= {e}
        if _bucle_valido(aristas, n):
            return aristas
    raise SystemExit("sin bucle")


def _soluciones_anillo(n, pistas, limite=2):
    """Cuenta bucles únicos con las pistas dadas {(x,y): k}."""
    todas = [("h", x, y) for y in range(n + 1) for x in range(n)] + [("v", x, y) for y in range(n) for x in range(n + 1)]
    # orden por puntos para podar en cuanto un punto queda decidido
    orden = []
    for y in range(n + 1):
        for x in range(n + 1):
            for e in (("h", x, y), ("v", x, y)):
                if e in todas:
                    orden.append(e)
    puntos = lambda e: ((e[1], e[2]), (e[1] + 1, e[2])) if e[0] == "h" else ((e[1], e[2]), (e[1], e[2] + 1))
    aristas_de_punto = {}
    for e in orden:
        for p in puntos(e):
            aristas_de_punto.setdefault(p, []).append(e)
    celdas_de = {e: [] for e in orden}
    for c in pistas:
        for e in _aristas_celda(*c):
            celdas_de[e].append(c)
    grado, sin_decidir, cuenta, falta = {}, {}, {c: 0 for c in pistas}, {c: 4 for c in pistas}
    for p, es in aristas_de_punto.items():
        grado[p] = 0
        sin_decidir[p] = len(es)
    elegidas, sols = set(), []

    def rec(i):
        if len(sols) >= limite:
            return
        if i == len(orden):
            if elegidas and _bucle_valido(elegidas, n) and all(cuenta[c] == pistas[c] for c in pistas):
                sols.append(set(elegidas))
            return
        e = orden[i]
        for v in (0, 1):
            ok = True
            for p in puntos(e):
                grado[p] += v
                sin_decidir[p] -= 1
            for c in celdas_de[e]:
                cuenta[c] += v
                falta[c] -= 1
            for p in puntos(e):
                if grado[p] > 2 or (sin_decidir[p] == 0 and grado[p] == 1) or grado[p] + sin_decidir[p] < (2 if grado[p] else 0):
                    ok = False
            for c in celdas_de[e]:
                if cuenta[c] > pistas[c] or cuenta[c] + falta[c] < pistas[c]:
                    ok = False
            if ok:
                if v:
                    elegidas.add(e)
                rec(i + 1)
                elegidas.discard(e)
            for p in puntos(e):
                grado[p] -= v
                sin_decidir[p] += 1
            for c in celdas_de[e]:
                cuenta[c] -= v
                falta[c] += 1
    rec(0)
    return sols


def anillo(semilla=3, n=6):
    rng = random.Random(semilla)
    for _ in range(60):
        bucle = _bucle_aleatorio(n, rng)
        pistas = {(x, y): sum(1 for e in _aristas_celda(x, y) if e in bucle) for y in range(n) for x in range(n)}
        celdas = list(pistas)
        rng.shuffle(celdas)
        for c in celdas:
            p2 = dict(pistas)
            del p2[c]
            if len(_soluciones_anillo(n, p2)) == 1:
                pistas = p2
        if len(_soluciones_anillo(n, pistas)) == 1 and len(pistas) <= 15:
            return {"n": n, "pistas": [[x, y, k] for (x, y), k in sorted(pistas.items(), key=lambda t: (t[0][1], t[0][0]))],
                    "solucion": sorted([list(e) for e in bucle])}
    raise SystemExit("sin anillo")


# ------------------------------------------------------------------ programa del rover
DIR = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}


def simular(prog, n, muros, ini, d0, meta, limite_pasos=400):
    """prog: lista de ('a',) avanzar, ('i',) izquierda, ('d',) derecha, ('r', veces, [sub]) repetir. Devuelve (llega, posicion)."""
    x, y = ini
    d = d0
    pasos = [0]

    def ejecuta(bloques):
        nonlocal x, y, d
        for b in bloques:
            pasos[0] += 1
            if pasos[0] > limite_pasos:
                return False
            if b[0] == "a":
                nx, ny = x + DIR[d][0], y + DIR[d][1]
                if not (0 <= nx < n and 0 <= ny < n) or (nx, ny) in muros:
                    return False
                x, y = nx, ny
            elif b[0] == "i":
                d = (d + 3) % 4
            elif b[0] == "d":
                d = (d + 1) % 4
            else:
                for _ in range(b[1]):
                    if not ejecuta(b[2]):
                        return False
        return True
    ok = ejecuta(prog)
    return ok and (x, y) == tuple(meta), (x, y)


def programa():
    n = 7
    # escalera: del suelo de la cúpula (abajo a la izquierda) hasta la salida (arriba a la derecha)
    camino = [(0, 6)]
    x, y = 0, 6
    for _ in range(3):
        x += 1
        camino.append((x, y))
        y -= 1
        camino.append((x, y))
        x += 1
        camino.append((x, y))
    # el rover mira al este; la escalera es: avanzar, girar izquierda, avanzar, girar derecha, avanzar...
    solucion = [("r", 3, [("a",), ("i",), ("a",), ("d",), ("a",)])]
    ok, pos = simular(solucion, n, set(), (0, 6), 1, camino[-1])
    muros = {(a, b) for a in range(n) for b in range(n) if (a, b) not in set(camino)}
    ok, pos = simular(solucion, n, muros, (0, 6), 1, camino[-1])
    assert ok, pos
    # no hay atajos: cualquier otro programa corto que llegue tiene que seguir el mismo camino
    return {"n": n, "muros": sorted([list(m) for m in muros]), "inicio": [0, 6], "mira": 1, "meta": list(camino[-1]), "limite": 7,
            "solucion": [["r", 3, [["a"], ["i"], ["a"], ["d"], ["a"]]]], "camino": [list(c) for c in camino]}


# ------------------------------------------------------------------ paneles (Lights Out)
def paneles(semilla=2, n=5):
    rng = random.Random(semilla)
    for _ in range(500):
        toques = [(x, y) for y in range(n) for x in range(n) if rng.random() < 0.4]
        g = [[0] * n for _ in range(n)]
        for x, y in toques:
            for dx, dy in [(0, 0)] + V4:
                if 0 <= x + dx < n and 0 <= y + dy < n:
                    g[y + dy][x + dx] ^= 1
        encendidos = sum(map(sum, g))
        if 8 <= encendidos <= 14 and len(toques) >= 6:
            return {"n": n, "objetivo": g, "toques": [list(t) for t in toques]}
    raise SystemExit("sin paneles")


def aplica_paneles(n, toques):
    g = [[0] * n for _ in range(n)]
    for x, y in toques:
        for dx, dy in [(0, 0)] + V4:
            if 0 <= x + dx < n and 0 <= y + dy < n:
                g[y + dy][x + dx] ^= 1
    return g


# ------------------------------------------------------------------ sopa de letras
PALABRAS = ["POLVO", "ROVER", "CRATER", "OLIMPO", "ESCLUSA", "CUPULA", "HIELO", "OXIGENO", "FOBOS", "DEIMOS", "ARENA", "BASALTO", "CAVERNA",
            "TORMENTA", "VIENTO", "SONDA", "ORBITA", "RADIO", "ANTENA", "CAMPO"]
SECRETA = "LANZADOR"


def sopa(semilla=11, n=7):
    rng = random.Random(semilla)
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    objetivo = n * n - len(SECRETA)
    for _ in range(3000):
        pal = rng.sample([p for p in PALABRAS if len(p) <= n], 8)
        total, escogidas = 0, []
        for p in pal:
            if total + len(p) <= objetivo:
                escogidas.append(p)
                total += len(p)
        if total != objetivo:
            continue
        g = [[None] * n for _ in range(n)]
        pos = {}
        ok = True
        for p in sorted(escogidas, key=len, reverse=True):
            colocada = False
            for _ in range(200):
                dx, dy = rng.choice(dirs)
                x0, y0 = rng.randrange(n), rng.randrange(n)
                xs = [(x0 + dx * k, y0 + dy * k) for k in range(len(p))]
                if all(0 <= a < n and 0 <= b < n and g[b][a] is None for a, b in xs):
                    for (a, b), ch in zip(xs, p):
                        g[b][a] = ch
                    pos[p] = [list(xs[0]), [dx, dy]]
                    colocada = True
                    break
            if not colocada:
                ok = False
                break
        if not ok:
            continue
        libres = [(x, y) for y in range(n) for x in range(n) if g[y][x] is None]
        if len(libres) != len(SECRETA):
            continue
        for (x, y), ch in zip(libres, SECRETA):
            g[y][x] = ch
        # las palabras de la lista no deben aparecer en otro sitio (ni aparecer la secreta como palabra de la lista)
        def apariciones(p):
            c = 0
            for y in range(n):
                for x in range(n):
                    for dx, dy in dirs:
                        xs = [(x + dx * k, y + dy * k) for k in range(len(p))]
                        if all(0 <= a < n and 0 <= b < n for a, b in xs) and all(g[b][a] == ch for (a, b), ch in zip(xs, p)):
                            c += 1
            return c
        if all(apariciones(p) == 1 for p in escogidas):
            return {"n": n, "rejilla": ["".join(f) for f in g], "palabras": sorted(escogidas), "secreta": SECRETA}
    raise SystemExit("sin sopa")


# ------------------------------------------------------------------ consola final
DATOS_MISION = {"14": 3, "20": 8, "40": 5, "52": 2}        # el dato que muestra el mensaje de éxito de cada puzle
ORDEN_DATOS = ["40", "14", "52", "20"]                     # cableado, satélites, balancín, invernadero
CODIGO = [DATOS_MISION[c] for c in ORDEN_DATOS]


SATELITES = satelites()
VIDA = vida()
CABLEADO = cableado()
ROCAS = rocas()
BALANCIN = balancin()
CIFRAS = cifras()
ANILLO = anillo()
PROGRAMA = programa()
PANELES = paneles()
SOPA = sopa()

TODO = {"satelites": SATELITES, "vida": VIDA, "cableado": CABLEADO, "rocas": ROCAS, "balancin": BALANCIN, "cifras": CIFRAS, "anillo": ANILLO,
        "programa": PROGRAMA, "paneles": PANELES, "sopa": SOPA, "datos_mision": DATOS_MISION, "orden_datos": ORDEN_DATOS, "codigo": CODIGO}

if __name__ == "__main__":
    for k, v in TODO.items():
        print(k, json.dumps(v, ensure_ascii=False)[:230])
    with open(os.path.join(AQUI, "instancias_marte.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(TODO, f, ensure_ascii=False, indent=1)
    print("OK")

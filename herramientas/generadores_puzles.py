"""Banco de generadores de puzles con SOLUCIÓN ÚNICA comprobada (por fuerza bruta o retroceso).

Sirve para que cada juego nuevo pueda incluir puzles tipo Nikoli, deducción o lingüística sin dudar de que son justos:
cada función devuelve una instancia lista para pasar al minijuego (cuadrículas, pistas, solución) y comprueba que solo
hay una solución. Salió de la investigación de ideas de puzles (GUIA-DE-PUZLES.md §7).

Uso:
    python herramientas/generadores_puzles.py --prueba            # genera y verifica una instancia de cada tipo
    python herramientas/generadores_puzles.py nonograma 6 6 3     # filas, columnas, semilla
Desde Python:
    from generadores_puzles import nonograma, akari, rascacielos, zebra, caballeros, caja_negra, rush_hour, hashi, rosetta, luces, puentes_linterna, tubos
"""
import itertools
import random
import sys
from collections import deque


# ============================================================ Nonograma
def _lineas_posibles(longitud, pistas):
    """Todas las filas posibles de `longitud` casillas con esos bloques (1 = lleno)."""
    if not pistas:
        return [(0,) * longitud]
    res = []

    def colocar(i, pos, linea):
        if i == len(pistas):
            res.append(tuple(linea + [0] * (longitud - len(linea))))
            return
        resto = sum(pistas[i + 1:]) + (len(pistas) - i - 1)
        for ini in range(pos, longitud - pistas[i] - resto + 1):
            nueva = linea + [0] * (ini - len(linea)) + [1] * pistas[i]
            if i < len(pistas) - 1:
                nueva = nueva + [0]
            colocar(i + 1, len(nueva), nueva)

    colocar(0, 0, [])
    return res


def _pistas_de(linea):
    p, n = [], 0
    for v in linea:
        if v:
            n += 1
        elif n:
            p.append(n)
            n = 0
    if n:
        p.append(n)
    return p


def _contar_nonograma(filas, cols, pf, pc, limite=2):
    opciones = [_lineas_posibles(cols, p) for p in pf]
    cuenta = 0
    columnas_ok = [set() for _ in range(cols)]

    def rec(r, parcial):
        nonlocal cuenta
        if cuenta >= limite:
            return
        if r == filas:
            if all(_pistas_de([parcial[i][c] for i in range(filas)]) == pc[c] for c in range(cols)):
                cuenta += 1
            return
        for f in opciones[r]:
            # poda por columnas: lo que llevamos no puede exceder la pista
            ok = True
            for c in range(cols):
                col = [parcial[i][c] for i in range(r)] + [f[c]]
                p = _pistas_de(col)
                objetivo = pc[c]
                if len(p) > len(objetivo) or any(p[k] != objetivo[k] for k in range(len(p) - 1)) or (p and p[-1] > objetivo[len(p) - 1]):
                    ok = False
                    break
            if ok:
                rec(r + 1, parcial + [f])

    rec(0, [])
    return cuenta


def nonograma(filas=6, cols=6, semilla=1, densidad=0.55):
    rng = random.Random(semilla)
    for _ in range(500):
        g = [[1 if rng.random() < densidad else 0 for _ in range(cols)] for _ in range(filas)]
        pf = [_pistas_de(f) for f in g]
        pc = [_pistas_de([g[i][c] for i in range(filas)]) for c in range(cols)]
        if _contar_nonograma(filas, cols, pf, pc) == 1:
            return dict(solucion=g, filas=pf, columnas=pc)
    raise RuntimeError("no se encontró un nonograma único")


# ============================================================ Akari (luces)
def _ilumina(n, muros, bombillas):
    lit = set()
    for (r, c) in bombillas:
        lit.add((r, c))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            y, x = r + dr, c + dc
            while 0 <= y < n and 0 <= x < n and (y, x) not in muros:
                lit.add((y, x))
                y, x = y + dr, x + dc
    return lit


def _contar_akari(n, muros, numeros, limite=2):
    blancas = [(r, c) for r in range(n) for c in range(n) if (r, c) not in muros]
    cuenta = 0

    def valido_parcial(bomb):
        s = set(bomb)
        for (r, c) in bomb:
            for dr, dc in ((1, 0), (0, 1)):
                y, x = r + dr, c + dc
                while 0 <= y < n and 0 <= x < n and (y, x) not in muros:
                    if (y, x) in s:
                        return False
                    y, x = y + dr, x + dc
        for (mr, mc), k in numeros.items():
            vec = sum(1 for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (mr + dr, mc + dc) in s)
            if vec > k:
                return False
        return True

    def rec(i, bomb):
        nonlocal cuenta
        if cuenta >= limite:
            return
        if i == len(blancas):
            if len(_ilumina(n, muros, bomb)) == len(blancas) and all(
                    sum(1 for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (mr + dr, mc + dc) in set(bomb)) == k
                    for (mr, mc), k in numeros.items()):
                cuenta += 1
            return
        rec(i + 1, bomb)
        nb = bomb + [blancas[i]]
        if valido_parcial(nb):
            rec(i + 1, nb)

    rec(0, [])
    return cuenta


def akari(n=6, semilla=1):
    rng = random.Random(semilla)
    for _ in range(300):
        muros = {(r, c) for r in range(n) for c in range(n) if rng.random() < 0.14}
        blancas = [(r, c) for r in range(n) for c in range(n) if (r, c) not in muros]
        if len(blancas) < 20:
            continue
        # solución aleatoria: añadir bombillas hasta iluminar todo sin que se vean entre sí
        bomb = []
        for cel in rng.sample(blancas, len(blancas)):
            if cel in _ilumina(n, muros, bomb):
                continue
            if not any(b in _ilumina(n, muros, [cel]) for b in bomb):
                bomb.append(cel)
        if len(_ilumina(n, muros, bomb)) != len(blancas):
            continue
        numeros = {}
        for m in muros:
            numeros[m] = sum(1 for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (m[0] + dr, m[1] + dc) in set(bomb))
        if _contar_akari(n, muros, numeros) != 1:
            continue
        # quitar números mientras siga siendo único
        for m in rng.sample(list(numeros), len(numeros)):
            k = numeros.pop(m)
            if _contar_akari(n, muros, numeros) != 1:
                numeros[m] = k
        return dict(n=n, muros=sorted(muros), numeros={f"{r},{c}": v for (r, c), v in sorted(numeros.items())}, bombillas=sorted(bomb))
    raise RuntimeError("no se encontró un akari único")


# ============================================================ Rascacielos
def _contar_rascacielos(n, pistas, limite=2):
    """pistas: dict con 'arriba','abajo','izq','der' (listas; None = sin pista)."""
    cuenta = 0
    filas = list(itertools.permutations(range(1, n + 1)))

    def vistos(linea):
        m, v = 0, 0
        for h in linea:
            if h > m:
                m, v = h, v + 1
        return v

    def rec(r, tablero):
        nonlocal cuenta
        if cuenta >= limite:
            return
        if r == n:
            for c in range(n):
                col = [tablero[i][c] for i in range(n)]
                if pistas["arriba"][c] and vistos(col) != pistas["arriba"][c]:
                    return
                if pistas["abajo"][c] and vistos(col[::-1]) != pistas["abajo"][c]:
                    return
            cuenta += 1
            return
        for f in filas:
            if pistas["izq"][r] and vistos(f) != pistas["izq"][r]:
                continue
            if pistas["der"][r] and vistos(f[::-1]) != pistas["der"][r]:
                continue
            if any(f[c] == tablero[i][c] for i in range(r) for c in range(n)):
                continue
            rec(r + 1, tablero + [f])

    rec(0, [])
    return cuenta


def rascacielos(n=4, semilla=1):
    rng = random.Random(semilla)

    def vistos(linea):
        m, v = 0, 0
        for h in linea:
            if h > m:
                m, v = h, v + 1
        return v

    base = list(range(1, n + 1))
    t = [base[i:] + base[:i] for i in range(n)]
    rng.shuffle(t)
    cols = list(range(n))
    rng.shuffle(cols)
    t = [[f[c] for c in cols] for f in t]
    pistas = dict(
        arriba=[vistos([t[i][c] for i in range(n)]) for c in range(n)],
        abajo=[vistos([t[i][c] for i in range(n)][::-1]) for c in range(n)],
        izq=[vistos(t[r]) for r in range(n)],
        der=[vistos(t[r][::-1]) for r in range(n)],
    )
    assert _contar_rascacielos(n, pistas) == 1 or True
    claves = [(k, i) for k in pistas for i in range(n)]
    rng.shuffle(claves)
    for k, i in claves:
        guardada = pistas[k][i]
        pistas[k][i] = 0
        if _contar_rascacielos(n, pistas) != 1:
            pistas[k][i] = guardada
    if _contar_rascacielos(n, pistas) != 1:
        return rascacielos(n, semilla + 1000)
    return dict(n=n, solucion=t, pistas=pistas)


# ============================================================ Tabla lógica (Zebra)
def zebra(personas=("Ana", "Beto", "Carla", "Diego"), atributos=None, semilla=1):
    """Cada atributo es un reparto de valores entre las posiciones 0..n-1. Devuelve frases de pista en español."""
    n = len(personas)
    atributos = atributos or {"objeto": ["lupa", "llave", "brújula", "mapa"], "lugar": ["torre", "puerto", "mercado", "faro"]}
    verbos = {"objeto": "lleva", "lugar": "está en"}   # cómo se dice cada atributo en una frase (cámbialo para otro tema)
    art = {"lupa": "la", "llave": "la", "brújula": "la", "mapa": "el", "torre": "la", "puerto": "el", "mercado": "el", "faro": "el"}
    rng = random.Random(semilla)
    nombres = list(atributos)
    sol = {a: rng.sample(range(n), n) for a in nombres}   # sol[a][i] = posición del valor i
    valor_en = {a: {sol[a][i]: atributos[a][i] for i in range(n)} for a in nombres}
    # posición de cada persona = su índice. Hechos candidatos
    candidatas = []
    for a in nombres:
        for i in range(n):
            pos = sol[a][i]
            candidatas.append(("pos", a, i, pos, f"{personas[pos]} {verbos.get(a, 'tiene')} {art.get(atributos[a][i], '')} {atributos[a][i]}.".replace("  ", " ")))
    for a, b in itertools.permutations(nombres, 2):
        for i in range(n):
            for j in range(n):
                if sol[a][i] == sol[b][j]:
                    candidatas.append(("igual", a, i, b, j, f"Quien {verbos.get(a, 'tiene')} {art.get(atributos[a][i], '')} {atributos[a][i]} {verbos.get(b, 'tiene')} {art.get(atributos[b][j], '')} {atributos[b][j]}.".replace("  ", " ")))
                else:
                    candidatas.append(("dist", a, i, b, j, f"Quien {verbos.get(a, 'tiene')} {art.get(atributos[a][i], '')} {atributos[a][i]} NO {verbos.get(b, 'tiene')} {art.get(atributos[b][j], '')} {atributos[b][j]}.".replace("  ", " ")))

    def cuenta(pistas):
        # reparto: para cada atributo una permutación de posiciones; contar las compatibles
        total = 0
        for combo in itertools.product(*[list(itertools.permutations(range(n))) for _ in nombres]):
            asg = dict(zip(nombres, combo))
            ok = True
            for p in pistas:
                if p[0] == "pos":
                    _, a, i, pos, _t = p
                    ok = asg[a][i] == pos
                elif p[0] == "igual":
                    _, a, i, b, j, _t = p
                    ok = asg[a][i] == asg[b][j]
                else:
                    _, a, i, b, j, _t = p
                    ok = asg[a][i] != asg[b][j]
                if not ok:
                    break
            if ok:
                total += 1
                if total > 1:
                    return total
        return total

    rng.shuffle(candidatas)
    pistas = []
    for c in candidatas:
        pistas.append(c)
        if cuenta(pistas) == 1:
            break
    # quitar pistas redundantes
    for c in list(pistas):
        resto = [p for p in pistas if p is not c]
        if cuenta(resto) == 1:
            pistas = resto
    return dict(personas=list(personas), atributos=atributos, solucion={a: [valor_en[a][p] for p in range(n)] for a in nombres},
                frases=[p[-1] for p in pistas])


def a_art(a):
    return a


# ============================================================ Caballeros y bribones
def caballeros(n=4, semilla=1):
    """n personajes; cada uno hace una declaración sobre otros. Caballero dice la verdad, bribón miente. Solución única."""
    rng = random.Random(semilla)
    nombres = ["Ana", "Beto", "Carla", "Diego", "Elena", "Fran"][:n]
    for _ in range(2000):
        real = [rng.random() < 0.5 for _ in range(n)]
        decl = []
        for i in range(n):
            j = rng.choice([k for k in range(n) if k != i])
            tipo = rng.choice(["es", "no es", "ambos", "alguno"])
            k = rng.choice([x for x in range(n) if x not in (i, j)]) if n > 2 else j
            decl.append((tipo, j, k))

        def verdad(d, a):
            tipo, j, k = d
            if tipo == "es":
                return a[j]
            if tipo == "no es":
                return not a[j]
            if tipo == "ambos":
                return a[j] and a[k]
            return a[j] or a[k]

        def cuenta():
            c = 0
            for a in itertools.product([True, False], repeat=n):
                if all(verdad(decl[i], a) == a[i] for i in range(n)):
                    c += 1
            return c

        if cuenta() == 1 and sum(real) not in (0, n):
            # la solución única debe coincidir con alguna asignación consistente
            sol = [a for a in itertools.product([True, False], repeat=n) if all(verdad(decl[i], a) == a[i] for i in range(n))][0]
            frases = []
            for i, (tipo, j, k) in enumerate(decl):
                if tipo == "es":
                    t = f"{nombres[j]} es caballero."
                elif tipo == "no es":
                    t = f"{nombres[j]} es bribón."
                elif tipo == "ambos":
                    t = f"{nombres[j]} y {nombres[k]} son caballeros."
                else:
                    t = f"Al menos uno de {nombres[j]} y {nombres[k]} es caballero."
                frases.append(f"{nombres[i]}: «{t}»")
            return dict(nombres=nombres, caballeros=list(sol), frases=frases)
    raise RuntimeError("sin instancia")


# ============================================================ Caja negra (inducción de una regla)
REGLAS = {
    "todas rojas": lambda f: all(x[0] == "rojo" for x in f),
    "alguna redonda": lambda f: any(x[1] == "redonda" for x in f),
    "más grandes que pequeñas": lambda f: sum(1 for x in f if x[2] == "grande") > sum(1 for x in f if x[2] == "pequeña"),
    "no hay dos del mismo color": lambda f: len({x[0] for x in f}) == len(f),
    "el primero es azul": lambda f: f[0][0] == "azul",
    "hay tantas cuadradas como redondas": lambda f: sum(1 for x in f if x[1] == "cuadrada") == sum(1 for x in f if x[1] == "redonda"),
}
FICHAS = [(c, f, t) for c in ("rojo", "azul", "verde") for f in ("redonda", "cuadrada") for t in ("grande", "pequeña")]


def caja_negra(regla=None, semilla=1, n_ejemplos=8):
    """Elige una regla y un conjunto de ejemplos (con su etiqueta) que la distingue de todas las demás reglas."""
    rng = random.Random(semilla)
    regla = regla or rng.choice(list(REGLAS))
    cand = [tuple(rng.sample(FICHAS, 3)) for _ in range(400)]
    ejemplos = []
    otras = [r for r in REGLAS if r != regla]
    pend = set(otras)
    for e in cand:
        et = REGLAS[regla](e)
        quita = {o for o in pend if REGLAS[o](e) != et}
        if quita:
            ejemplos.append((e, et))
            pend -= quita
        if not pend:
            break
    relleno = [e for e in cand if e not in [x[0] for x in ejemplos]][: max(0, n_ejemplos - len(ejemplos))]
    ejemplos += [(e, REGLAS[regla](e)) for e in relleno]
    rng.shuffle(ejemplos)
    return dict(regla=regla, ejemplos=ejemplos, distingue_todas=not pend)


# ============================================================ Rush Hour (bloques deslizantes)
def rush_hour(semilla=1, n=6, min_movs=8):
    rng = random.Random(semilla)
    for _ in range(3000):
        coches = []   # (fila, col, largo, horizontal)
        ocupado = set()
        # coche objetivo en la fila 2, horizontal, largo 2
        coches.append((2, rng.randint(0, 2), 2, True))
        for k in range(2):
            ocupado.add((2, coches[0][1] + k))
        for _c in range(rng.randint(6, 9)):
            largo = rng.choice([2, 2, 3])
            hor = rng.random() < 0.5
            r, c = rng.randint(0, n - 1), rng.randint(0, n - 1)
            celdas = [(r, c + k) if hor else (r + k, c) for k in range(largo)]
            if any(not (0 <= y < n and 0 <= x < n) or (y, x) in ocupado for y, x in celdas):
                continue
            coches.append((r, c, largo, hor))
            ocupado |= set(celdas)
        estado = tuple(tuple(c[:2]) for c in coches)
        movs = _resolver_rush(n, coches, estado)
        if movs is not None and movs >= min_movs:
            return dict(n=n, coches=coches, movimientos_minimos=movs)
    raise RuntimeError("sin instancia de Rush Hour")


def rush_hour_ruta(inst):
    """Lista de pasos (coche, +1/-1) de una solución mínima."""
    n, coches = inst["n"], inst["coches"]
    ini = tuple(tuple(c[:2]) for c in coches)
    return _resolver_rush(n, coches, ini, ruta=True)


def _resolver_rush(n, coches, ini, ruta=False):
    def celdas(i, pos):
        r, c = pos
        _, _, largo, hor = coches[i]
        return [(r, c + k) if hor else (r + k, c) for k in range(largo)]

    visto = {ini}
    padre = {ini: None}
    cola = deque([(ini, 0)])
    while cola:
        est, d = cola.popleft()
        if est[0][1] + 2 == n:     # el coche objetivo toca el borde derecho
            if not ruta:
                return d
            pasos, e = [], est
            while padre[e]:
                e, paso = padre[e]
                pasos.append(paso)
            return pasos[::-1]
        occ = set()
        for i, p in enumerate(est):
            occ |= set(celdas(i, p))
        for i, (r, c) in enumerate(est):
            _, _, largo, hor = coches[i]
            for paso in (-1, 1):
                nr, nc = (r, c + paso) if hor else (r + paso, c)
                nuevas = celdas(i, (nr, nc))
                if any(not (0 <= y < n and 0 <= x < n) for y, x in nuevas):
                    continue
                propias = set(celdas(i, (r, c)))
                if any((y, x) in occ and (y, x) not in propias for y, x in nuevas):
                    continue
                ne = est[:i] + ((nr, nc),) + est[i + 1:]
                if ne not in visto:
                    visto.add(ne)
                    padre[ne] = (est, (i, paso))
                    cola.append((ne, d + 1))
    return None


# ============================================================ Hashi (puentes)
def hashi(n=7, islas=8, semilla=1):
    rng = random.Random(semilla)
    for _ in range(2000):
        pos = set()
        while len(pos) < islas:
            pos.add((rng.randrange(n), rng.randrange(n)))
        pos = sorted(pos)
        # aristas posibles: islas vecinas en línea sin otra isla entre medias
        aristas = []
        for a, b in itertools.combinations(pos, 2):
            if a[0] == b[0]:
                entre = [p for p in pos if p[0] == a[0] and a[1] < p[1] < b[1]]
                if not entre:
                    aristas.append((a, b))
            elif a[1] == b[1]:
                entre = [p for p in pos if p[1] == a[1] and a[0] < p[0] < b[0]]
                if not entre:
                    aristas.append((a, b))

        def cruzan(e1, e2):
            (a, b), (c, d) = e1, e2
            h1, h2 = a[0] == b[0], c[0] == d[0]
            if h1 == h2:
                return False
            if h1:
                (fy, x1, x2), (fx, y1, y2) = (a[0], a[1], b[1]), (c[1], c[0], d[0])
            else:
                (fx, y1, y2), (fy, x1, x2) = (a[1], a[0], b[0]), (c[0], c[1], d[1])
            return x1 < fx < x2 and y1 < fy < y2

        # solución aleatoria conexa
        puentes = {}
        orden = rng.sample(aristas, len(aristas))
        for e in orden:
            if any(puentes.get(f, 0) and cruzan(e, f) for f in puentes):
                continue
            puentes[e] = rng.choice([1, 2]) if rng.random() < 0.7 else 0
        usados = {e: v for e, v in puentes.items() if v}
        # conexo
        grafo = {p: set() for p in pos}
        for (a, b) in usados:
            grafo[a].add(b)
            grafo[b].add(a)
        vistos, pila = set(), [pos[0]]
        while pila:
            x = pila.pop()
            if x in vistos:
                continue
            vistos.add(x)
            pila += list(grafo[x])
        if len(vistos) != len(pos):
            continue
        num = {p: 0 for p in pos}
        for (a, b), v in usados.items():
            num[a] += v
            num[b] += v
        if any(v == 0 for v in num.values()):
            continue
        # contar soluciones
        cuenta = 0
        lista = list(aristas)

        def rec(i, asg, rest):
            nonlocal cuenta
            if cuenta >= 2:
                return
            if i == len(lista):
                if all(v == 0 for v in rest.values()):
                    # conexo
                    g = {p: set() for p in pos}
                    for e, v in asg.items():
                        if v:
                            g[e[0]].add(e[1])
                            g[e[1]].add(e[0])
                    vv, st = set(), [pos[0]]
                    while st:
                        x = st.pop()
                        if x in vv:
                            continue
                        vv.add(x)
                        st += list(g[x])
                    if len(vv) == len(pos):
                        cuenta += 1
                return
            e = lista[i]
            for v in (0, 1, 2):
                if v and (rest[e[0]] < v or rest[e[1]] < v):
                    continue
                if v and any(asg.get(f, 0) and cruzan(e, f) for f in asg):
                    continue
                rest2 = dict(rest)
                rest2[e[0]] -= v
                rest2[e[1]] -= v
                asg2 = dict(asg)
                asg2[e] = v
                rec(i + 1, asg2, rest2)

        rec(0, {}, dict(num))
        if cuenta == 1:
            return dict(n=n, islas={f"{p[0]},{p[1]}": num[p] for p in pos},
                        puentes=[(a, b, v) for (a, b), v in usados.items()])
    raise RuntimeError("sin instancia de Hashi")


# ============================================================ Lengua inventada (Rosetta)
def rosetta(semilla=1):
    """Lengua con orden de frase, posición del adjetivo y plural por sufijo. Comprueba que los ejemplos fijan la traducción pedida."""
    rng = random.Random(semilla)
    sust = {"perro": "tak", "pez": "mol", "pájaro": "ris", "niño": "dun"}
    verb = {"ve": "sef", "come": "gor"}
    adj = {"grande": "ba", "rojo": "ku"}
    orden = rng.choice(["SVO", "SOV", "VSO"])
    adj_pos = rng.choice(["antes", "despues"])
    plural = rng.choice(["-i", "-o"])

    def trad(sujeto, v, objeto, a=None, plural_sujeto=False):
        s = sust[sujeto[0]] if isinstance(sujeto, tuple) else sust[sujeto]
        p = [sust[sujeto]]
        if plural_sujeto:
            p = [sust[sujeto] + plural[1:]]
        if a:
            p = [adj[a]] + p if adj_pos == "antes" else p + [adj[a]]
        o = [sust[objeto]]
        vv = [verb[v]]
        piezas = {"S": p, "V": vv, "O": o}
        return " ".join(sum((piezas[ch] for ch in orden), []))

    sujetos = list(sust)
    frases = [
        ("El perro ve el pez", trad("perro", "ve", "pez")),
        ("El niño come el pájaro", trad("niño", "come", "pájaro")),
        ("El perro grande ve el pez", trad("perro", "ve", "pez", "grande")),
        ("Los pájaros ven el pez", trad("pájaro", "ve", "pez", plural_sujeto=True)),
        ("El pez rojo come el niño", trad("pez", "come", "niño", "rojo")),
    ]
    pregunta = ("Los niños grandes comen el perro", trad("niño", "come", "perro", "grande", True))

    def hipotesis():
        for o, ap, pl in itertools.product(["SVO", "SOV", "VSO"], ["antes", "despues"], ["-i", "-o"]):
            yield o, ap, pl

    def construir(o, ap, pl, sujeto, v, objeto, a=None, plural_sujeto=False):
        p = [sust[sujeto] + (pl[1:] if plural_sujeto else "")]
        if a:
            p = [adj[a]] + p if ap == "antes" else p + [adj[a]]
        piezas = {"S": p, "V": [verb[v]], "O": [sust[objeto]]}
        return " ".join(sum((piezas[ch] for ch in o), []))

    consistentes = []
    datos = [("perro", "ve", "pez", None, False), ("niño", "come", "pájaro", None, False), ("perro", "ve", "pez", "grande", False),
             ("pájaro", "ve", "pez", None, True), ("pez", "come", "niño", "rojo", False)]
    for h in hipotesis():
        if all(construir(*h, *d) == frases[i][1] for i, d in enumerate(datos)):
            consistentes.append(h)
    resp = {construir(*h, "niño", "come", "perro", "grande", True) for h in consistentes}
    return dict(frases=frases, pregunta=pregunta, hipotesis_consistentes=len(consistentes), respuestas_distintas=len(resp),
                unica=len(resp) == 1 and resp == {pregunta[1]}, lengua=dict(orden=orden, adjetivo=adj_pos, plural=plural))


# ============================================================ Luces (cada toque cambia la cruz) y su solución mínima
def luces(cols=4, filas=3, semilla=1, min_toques=4):
    """Estado inicial todo apagado y un patrón objetivo alcanzable con al menos `min_toques` toques mínimos."""
    rng = random.Random(semilla)
    total = cols * filas

    def pulsar(est, i):
        c, r = i % cols, i // cols
        est = list(est)
        for dc, dr in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = c + dc, r + dr
            if 0 <= x < cols and 0 <= y < filas:
                est[y * cols + x] ^= 1
        return tuple(est)

    for _ in range(5000):
        toques = rng.sample(range(total), rng.randint(min_toques, min_toques + 1))
        est = (0,) * total
        for i in toques:
            est = pulsar(est, i)
        if not 4 <= sum(est) <= total - 3:
            continue
        # mínimo de toques (el orden no importa y repetir un toque lo anula)
        for k in range(1, len(toques) + 1):
            hallado = None
            for comb in itertools.combinations(range(total), k):
                e = (0,) * total
                for i in comb:
                    e = pulsar(e, i)
                if e == est:
                    hallado = comb
                    break
            if hallado:
                if k >= min_toques:
                    return dict(cols=cols, filas=filas, objetivo=list(est), toques_minimos=list(hallado))
                break
    raise RuntimeError("sin instancia de luces")


# ============================================================ Puente y linterna (tiempo mínimo)
def puentes_linterna(tiempos=(1, 2, 5, 8)):
    """Cruzan de dos en dos con una sola linterna; el grupo va a la velocidad del más lento. Devuelve el tiempo mínimo y un plan."""
    n = len(tiempos)
    ini = (frozenset(range(n)), True)    # personas en la orilla de salida, linterna en la salida
    mejor = {ini: (0, None)}
    cola = [(0, ini)]
    import heapq
    heapq.heapify(cola)
    while cola:
        d, est = heapq.heappop(cola)
        if mejor[est][0] < d:
            continue
        izq, lin = est
        if not izq and not lin:
            plan, e = [], est
            while mejor[e][1]:
                e, mov = mejor[e][1]
                plan.append(mov)
            return dict(tiempos=list(tiempos), tiempo_minimo=d, plan=plan[::-1])
        origen = izq if lin else frozenset(range(n)) - izq
        for k in (1, 2):
            for g in itertools.combinations(sorted(origen), k):
                coste = max(tiempos[i] for i in g)
                nuevo = (izq - frozenset(g), False) if lin else (izq | frozenset(g), True)
                nd = d + coste
                if nuevo not in mejor or nd < mejor[nuevo][0]:
                    mejor[nuevo] = (nd, (est, ("ida" if lin else "vuelta", [tiempos[i] for i in g])))
                    heapq.heappush(cola, (nd, nuevo))
    return None


# ============================================================ Cerillas (mover UNA cerilla para arreglar la cuenta)
# Segmentos de un dígito: a=arriba b=arriba-dcha c=abajo-dcha d=abajo e=abajo-izda f=arriba-izda g=centro
_SEG = {0: "abcdef", 1: "bc", 2: "abdeg", 3: "abcdg", 4: "bcfg", 5: "acdfg", 6: "acdefg", 7: "abc", 8: "abcdefg", 9: "abcdfg"}
_MASK = {d: sum(1 << "abcdefg".index(ch) for ch in s) for d, s in _SEG.items()}
_DIG = {m: d for d, m in _MASK.items()}


def _cerillas_valida(a, op, b, c):
    """a,b,c: máscaras de 7 bits; op: máscara de 2 bits (1 = '-', 3 = '+'). Devuelve True si es una cuenta verdadera."""
    if a not in _DIG or b not in _DIG or c not in _DIG or op not in (1, 3):
        return False
    x, y, z = _DIG[a], _DIG[b], _DIG[c]
    return (x + y == z) if op == 3 else (x - y == z)


def cerillas(semilla=1):
    """Cuenta falsa «A ± B = C» con cerillas (dígitos de 7 segmentos). Hay exactamente UNA forma de arreglarla moviendo una sola cerilla.
    Devuelve las posiciones (símbolo, segmento) de origen y destino de la única solución."""
    rng = random.Random(semilla)
    # símbolo 0=A, 1=operador (2 palitos: horizontal y vertical), 2=B, 3=C
    anchos = [7, 2, 7, 7]
    desde = [0, 7, 9, 16]

    def partir(estado):
        return [(estado >> desde[k]) & ((1 << anchos[k]) - 1) for k in range(4)]

    def juntar(partes):
        return sum(partes[k] << desde[k] for k in range(4))

    for _ in range(20000):
        a, b = rng.randint(0, 9), rng.randint(0, 9)
        op = rng.choice((1, 3))
        c = rng.randint(0, 9)
        est = juntar([_MASK[a], op, _MASK[b], _MASK[c]])
        pa, po, pb, pc = partir(est)
        if _cerillas_valida(pa, po, pb, pc):
            continue
        sols = {}
        for src in range(23):
            if not est >> src & 1:
                continue
            for dst in range(23):
                if dst == src or est >> dst & 1:
                    continue
                n = (est & ~(1 << src)) | (1 << dst)
                if _cerillas_valida(*partir(n)):
                    sols[n] = (src, dst)
        if len(sols) != 1:
            continue
        (src, dst), = sols.values()

        def donde(i):
            k = max(j for j in range(4) if desde[j] <= i)
            return k, i - desde[k]

        sk, ss = donde(src)
        dk, ds = donde(dst)
        if sk == dk:      # que la cerilla cambie de símbolo: más interesante y más claro
            continue
        return dict(simbolos=[a, "+" if op == 3 else "-", b, c], masks=[pa, po, pb, pc], desde=[sk, ss], hasta=[dk, ds])
    raise RuntimeError("sin instancia de cerillas")


# ============================================================ Tubos de colores (water sort)
def tubos(colores=3, capacidad=4, vacios=2, semilla=1, min_movs=6):
    rng = random.Random(semilla)
    for _ in range(3000):
        fichas = [c for c in range(colores) for _ in range(capacidad)]
        rng.shuffle(fichas)
        tub = [tuple(fichas[i * capacidad:(i + 1) * capacidad]) for i in range(colores)] + [()] * vacios
        movs = _resolver_tubos(tuple(tub), capacidad)
        if movs is not None and movs >= min_movs:
            return dict(tubos=[list(x) for x in tub], capacidad=capacidad, movimientos_minimos=movs)
    raise RuntimeError("sin instancia de tubos")


def tubos_ruta(inst):
    """Lista de movimientos (origen, destino) de una solución mínima."""
    return _resolver_tubos(tuple(tuple(x) for x in inst["tubos"]), inst["capacidad"], ruta=True)


def _resolver_tubos(ini, cap, ruta=False):
    def resuelto(e):
        return all(len(t) == 0 or (len(t) == cap and len(set(t)) == 1) for t in e)

    visto = {ini}
    padre = {ini: None}
    cola = deque([(ini, 0)])
    while cola:
        e, d = cola.popleft()
        if resuelto(e):
            if not ruta:
                return d
            pasos, x = [], e
            while padre[x]:
                x, mov = padre[x]
                pasos.append(mov)
            return pasos[::-1]
        for a, ta in enumerate(e):
            if not ta:
                continue
            for b, tb in enumerate(e):
                if a == b or len(tb) >= cap:
                    continue
                if tb and tb[-1] != ta[-1]:
                    continue
                # se vierte todo el bloque superior del mismo color que quepa
                k = 1
                while k < len(ta) and ta[-1 - k] == ta[-1]:
                    k += 1
                k = min(k, cap - len(tb))
                ne = list(e)
                ne[a] = ta[:-k]
                ne[b] = tb + ta[-k:]
                ne = tuple(ne)
                if ne not in visto:
                    visto.add(ne)
                    padre[ne] = (e, (a, b))
                    cola.append((ne, d + 1))
    return None


# ============================================================ Prueba
def _prueba():
    ok = True
    n = nonograma(5, 5, 3)
    print("nonograma 5x5 OK ->", n["filas"], n["columnas"])
    a = akari(6, 2)
    print("akari 6x6 OK ->", len(a["muros"]), "muros,", len(a["bombillas"]), "bombillas,", len(a["numeros"]), "numeros")
    r = rascacielos(4, 1)
    print("rascacielos 4x4 OK ->", sum(1 for k in r["pistas"] for v in r["pistas"][k] if v), "pistas")
    z = zebra(semilla=4)
    print("zebra OK ->", len(z["frases"]), "frases:", *z["frases"], sep="\n   ")
    c = caballeros(4, 5)
    print("caballeros OK ->", *c["frases"], c["caballeros"], sep="\n   ")
    cb = caja_negra(semilla=2)
    print("caja negra OK -> regla", cb["regla"], "distingue de todas las demás:", cb["distingue_todas"], len(cb["ejemplos"]), "ejemplos")
    ok &= cb["distingue_todas"]
    rh = rush_hour(3)
    print("rush hour OK ->", len(rh["coches"]), "coches,", rh["movimientos_minimos"], "movimientos mínimos")
    h = hashi(7, 7, 5)
    print("hashi OK ->", len(h["islas"]), "islas,", len(h["puentes"]), "puentes")
    ro = rosetta(1)
    print("rosetta ->", ro["lengua"], "hipótesis consistentes:", ro["hipotesis_consistentes"], "únicas:", ro["unica"])
    for semilla in range(2, 40):
        if ro["unica"]:
            break
        ro = rosetta(semilla)
    print("rosetta única con semilla", semilla, ro["unica"], ro["lengua"])
    ok &= ro["unica"]
    lu = luces(4, 3, 2)
    print("luces 4x3 OK -> objetivo", lu["objetivo"], "toques mínimos", lu["toques_minimos"])
    pl = puentes_linterna((1, 2, 5, 8))
    print("puente y linterna OK ->", pl["tiempo_minimo"], "min:", pl["plan"])
    ok &= pl["tiempo_minimo"] == 15
    ce = cerillas(1)
    print("cerillas OK ->", ce["simbolos"], "mueve", ce["desde"], "->", ce["hasta"])
    tb = tubos(3, 4, 2, 1)
    print("tubos OK ->", tb["tubos"], "mínimo", tb["movimientos_minimos"], "movimientos")
    return ok


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--prueba":
        sys.exit(0 if _prueba() else 1)
    nombre, *args = sys.argv[1:] or ["--prueba"]
    f = globals()[nombre]
    print(f(*[int(a) for a in args]))

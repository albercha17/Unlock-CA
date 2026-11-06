"""Instancias de «Altamuralla: El Valle de los Colosos» (decimocuarta parada, 60 cartas). Cada puzle se genera con semilla fija y se comprueba
por fuerza bruta que tiene una sola solución (y, cuando las pistas se reparten en varias cartas, que hacen falta todas).

  - faroles (14): Akari 7 x 7; los números de las torres solo están en la carta.
  - cronica (20): seis sucesos de la ciudad que se ordenan con pistas repartidas en tres cartas.
  - barracones (40): Fillomino 6 x 6; los números ya puestos, repartidos en dos cartas.
  - inscripcion (48): lengua inventada del viajero (orden objeto-verbo-sujeto, negación y plural).
  - dosis (52): báscula y vara de medir -> tabla de dosis -> llenar dos jeringuillas.
  - pisadas (46): Hitori 6 x 6 (el coloso pisa cobertizos sin repetir tejado y sin dejar la ciudad partida).
  - canto (51): Simon traducido: el canto de los colosos y la respuesta, en tres rondas.
  - ofrendas (69): caja negra: qué ofrendas de tres piedras acepta el Coloso Viejo.
  - palancas (72): memoria por etapas en la maquinaria de la Torre del Reloj.
  - tesoro (64): agrupar dieciséis baratijas en cuatro grupos de cuatro.
  - meta (85): cinco marcas (fila y columna) sobre la inscripción de la cámara -> HOGAR.
Uso:  python herramientas/instancias_colosos.py   (escribe instancias_colosos.json)
"""
import itertools
import json
import os
import random

AQUI = os.path.dirname(os.path.abspath(__file__))
RUTA = os.path.join(AQUI, "instancias_colosos.json")
LET = "ABCDEFGH"
V4 = ((-1, 0), (1, 0), (0, -1), (0, 1))


def ref(f, c):
    return LET[c] + str(f + 1)


# ================================================================== 14 · Faroles (Akari)
def _akari_vis(n, muro, f, c):
    vis = []
    for df, dc in V4:
        y, x = f + df, c + dc
        while 0 <= y < n and 0 <= x < n and (y, x) not in muro:
            vis.append((y, x))
            y, x = y + df, x + dc
    return vis


def akari_soluciones(n, muro, numeros, tope=2):
    libres = [(f, c) for f in range(n) for c in range(n) if (f, c) not in muro]
    vis = {p: _akari_vis(n, muro, *p) for p in libres}
    vecinos = {m: [(m[0] + a, m[1] + b) for a, b in V4 if (m[0] + a, m[1] + b) in vis] for m in numeros}
    sols = []

    def ok_num(luces, final):
        for m, k in numeros.items():
            t = sum(1 for v in vecinos[m] if v in luces)
            if t > k:
                return False
            if final and t != k:
                return False
        return True

    def rec(luces, prohibidas):
        if len(sols) >= tope:
            return
        lit = set(luces)
        for l in luces:
            lit.update(vis[l])
        pend = [p for p in libres if p not in lit]
        if not pend:
            if ok_num(luces, True):
                sols.append(sorted(luces))
            return
        p = pend[0]
        cands = [q for q in [p] + vis[p] if q not in lit and q not in prohibidas]
        nuevas = set(prohibidas)
        for q in cands:
            nl = luces | {q}
            if ok_num(nl, False):
                rec(nl, nuevas)
            nuevas.add(q)

    rec(frozenset(), frozenset())
    return sols


def faroles(rng):
    n = 7
    while True:
        muro = set()
        for _ in range(7):
            f, c = rng.randrange(n), rng.randrange(n)
            muro |= {(f, c), (n - 1 - f, n - 1 - c)}
        if len(muro) < 9 or len(muro) > 13:
            continue
        libres = [(f, c) for f in range(n) for c in range(n) if (f, c) not in muro]
        vis = {p: _akari_vis(n, muro, *p) for p in libres}
        # solución aleatoria: se colocan luces en celdas oscuras al azar
        luces, lit = [], set()
        orden = libres[:]
        rng.shuffle(orden)
        for p in orden:
            if p not in lit:
                luces.append(p)
                lit |= {p, *vis[p]}
        numeros = {m: sum(1 for a, b in V4 if (m[0] + a, m[1] + b) in luces) for m in muro}
        if akari_soluciones(n, muro, numeros) != [sorted(luces)]:
            continue
        # quitar números mientras siga habiendo una sola solución
        claves = list(numeros)
        rng.shuffle(claves)
        for m in claves:
            prueba = {k: v for k, v in numeros.items() if k != m}
            if len(akari_soluciones(n, muro, prueba)) == 1:
                numeros = prueba
        if len(numeros) >= 4 and len(luces) >= 8:
            return dict(n=n, muros=sorted(map(list, muro)), numeros=[[f, c, k] for (f, c), k in sorted(numeros.items())],
                        solucion=sorted(map(list, luces)))


# ================================================================== 20 · La crónica (línea de tiempo)
SUCESOS = ["La primera piedra", "El primer coloso", "El gran incendio", "La campana mayor", "La llegada de la doctora", "El elevador"]


def _cumple_cr(p, cl):
    pos = {s: i for i, s in enumerate(p)}
    t = cl[0]
    if t == "antes":
        return pos[cl[1]] < pos[cl[2]]
    if t == "justo":
        return pos[cl[1]] + 1 == pos[cl[2]]
    if t == "entre":                       # entre a y b pasaron exactamente k sucesos (en cualquier orden)
        return abs(pos[cl[1]] - pos[cl[2]]) - 1 == cl[3]
    if t == "puesto":
        return pos[cl[1]] == cl[2]
    if t == "no_extremos":
        return 0 < pos[cl[1]] < 5
    raise ValueError(t)


def _cr_sols(clues):
    return [p for p in itertools.permutations(range(6)) if all(_cumple_cr(p, c) for c in clues)]


def cronica(rng):
    while True:
        sol = list(range(6))
        rng.shuffle(sol)
        pos = {s: i for i, s in enumerate(sol)}
        pool = []
        for a, b in itertools.permutations(range(6), 2):
            if pos[a] < pos[b]:
                pool.append(("antes", a, b))
            if pos[a] + 1 == pos[b]:
                pool.append(("justo", a, b))
            if a < b and abs(pos[a] - pos[b]) > 1:
                pool.append(("entre", a, b, abs(pos[a] - pos[b]) - 1))
        for a in range(6):
            if 0 < pos[a] < 5:
                pool.append(("no_extremos", a))
        rng.shuffle(pool)
        clues = []
        for c in pool:
            if len(_cr_sols(clues)) == 1:
                break
            if len(_cr_sols(clues + [c])) < len(_cr_sols(clues)):
                clues.append(c)
        # minimizar
        for c in clues[:]:
            r = [x for x in clues if x != c]
            if len(_cr_sols(r)) == 1:
                clues = r
        if not 6 <= len(clues) <= 8 or any(c[0] == "puesto" for c in clues):
            continue
        tipos = {c[0] for c in clues}
        if len(tipos) < 3:
            continue
        rng.shuffle(clues)
        nota, cron = clues[:2], clues[2:]
        # todas las cartas hacen falta: sin la nota, o sin cada mitad de la crónica, hay más de una solución
        mitad = (len(cron) + 1) // 2
        partes = [nota, cron[:mitad], cron[mitad:]]
        if all(len(_cr_sols([c for j, p in enumerate(partes) if j != i for c in p])) > 1 for i in range(3)):
            return dict(sucesos=SUCESOS, solucion=list(_cr_sols(clues)[0]), nota=nota, cronica_arriba=cron[:mitad], cronica_abajo=cron[mitad:])


def texto_pista_cronica(c):
    S = SUCESOS
    if c[0] == "antes":
        return f"«{S[c[1]]}» ocurrió antes que «{S[c[2]]}»."
    if c[0] == "justo":
        return f"Justo después de «{S[c[1]]}» vino «{S[c[2]]}», sin nada en medio."
    if c[0] == "entre":
        k = c[3]
        n = {1: "un suceso", 2: "dos sucesos", 3: "tres sucesos", 4: "cuatro sucesos"}[k]
        return f"Entre «{S[c[1]]}» y «{S[c[2]]}» hubo {n}, ni más ni menos."
    if c[0] == "no_extremos":
        return f"«{S[c[1]]}» no fue ni lo primero ni lo último."
    raise ValueError(c)


# ================================================================== 40 · Barracones (Fillomino)
def _componentes(n, val):
    vis, comps = set(), []
    for f in range(n):
        for c in range(n):
            if (f, c) in vis or val.get((f, c)) is None:
                continue
            v = val[(f, c)]
            pila, comp = [(f, c)], []
            vis.add((f, c))
            while pila:
                p = pila.pop()
                comp.append(p)
                for a, b in V4:
                    q = (p[0] + a, p[1] + b)
                    if q not in vis and val.get(q) == v:
                        vis.add(q)
                        pila.append(q)
            comps.append((v, comp))
    return comps


def fillomino_soluciones(n, dados, tope=2, maxv=6):
    celdas = [(f, c) for f in range(n) for c in range(n)]
    val = dict(dados)
    sols = []

    def valido():
        for v, comp in _componentes(n, val):
            if len(comp) > v:
                return False
            if len(comp) < v:
                # tiene que poder crecer: algún vecino vacío
                if not any(0 <= p[0] + a < n and 0 <= p[1] + b < n and (p[0] + a, p[1] + b) not in val for p in comp for a, b in V4):
                    return False
        return True

    def rec(i):
        if len(sols) >= tope:
            return
        while i < len(celdas) and celdas[i] in val:
            i += 1
        if i == len(celdas):
            if all(len(comp) == v for v, comp in _componentes(n, val)):
                sols.append({f"{f},{c}": val[(f, c)] for f, c in celdas})
            return
        for v in range(1, maxv + 1):
            val[celdas[i]] = v
            if valido():
                rec(i + 1)
            del val[celdas[i]]

    if valido():
        rec(0)
    return sols


def barracones(rng):
    n = 6
    while True:
        # partición aleatoria en regiones de 1 a 6 casillas sin dos regiones del mismo tamaño tocándose
        reg = {}
        libres = [(f, c) for f in range(n) for c in range(n)]
        rng.shuffle(libres)
        ok = True
        rid = 0
        for p in libres:
            if p in reg:
                continue
            tam = rng.choice([1, 2, 2, 3, 3, 4, 4, 5, 5, 6])
            comp = [p]
            reg[p] = rid
            while len(comp) < tam:
                fr = [(q[0] + a, q[1] + b) for q in comp for a, b in V4
                      if 0 <= q[0] + a < n and 0 <= q[1] + b < n and (q[0] + a, q[1] + b) not in reg]
                if not fr:
                    break
                q = rng.choice(fr)
                reg[q] = rid
                comp.append(q)
            rid += 1
        tam_de = {}
        for p, r in reg.items():
            tam_de[r] = tam_de.get(r, 0) + 1
        val = {p: tam_de[r] for p, r in reg.items()}
        for p in val:
            for a, b in V4:
                q = (p[0] + a, p[1] + b)
                if q in val and reg[q] != reg[p] and val[q] == val[p]:
                    ok = False
        if not ok or len(set(val.values())) < 5:
            continue
        sol = {f"{f},{c}": val[(f, c)] for f, c in val}
        dados = dict(val)
        claves = list(dados)
        rng.shuffle(claves)
        for p in claves:
            prueba = {k: v for k, v in dados.items() if k != p}
            if len(fillomino_soluciones(n, prueba)) == 1:
                dados = prueba
        if not 9 <= len(dados) <= 14:
            continue
        # repartir los números ya puestos entre la lista del intendente (41) y el plano (43): hacen falta los dos
        ks = sorted(dados)
        for _ in range(40):
            rng.shuffle(ks)
            a, b = ks[:len(ks) // 2], ks[len(ks) // 2:]
            if len(fillomino_soluciones(n, {k: dados[k] for k in a})) > 1 and len(fillomino_soluciones(n, {k: dados[k] for k in b})) > 1:
                return dict(n=n, solucion=sol, lista=[[f, c, dados[(f, c)]] for f, c in sorted(a)],
                            plano=[[f, c, dados[(f, c)]] for f, c in sorted(b)])


# ================================================================== 48 · La inscripción del viajero (lengua inventada)
PALABRAS = ["FLOR", "MURO", "VIAJERO", "CRISTAL", "COLOSO", "BUSCAR", "GUARDAR", "ABRIR", "NO", "PLURAL", "CAMINO", "LUNA"]
EJEMPLOS = [  # (frase en castellano, sujeto, verbo, objeto, negado, sujeto plural, objeto plural)
    ("El viajero busca la flor.", "VIAJERO", "BUSCAR", "FLOR", False, False, False),
    ("Los colosos guardan el muro.", "COLOSO", "GUARDAR", "MURO", False, True, False),
    ("La flor no abre el muro.", "FLOR", "ABRIR", "MURO", True, False, False),
    ("El cristal busca a los colosos.", "CRISTAL", "BUSCAR", "COLOSO", False, False, True),
    ("Los viajeros abren el muro.", "VIAJERO", "ABRIR", "MURO", False, True, False),
]
OBJETIVO = ("Los colosos no buscan el cristal.", "COLOSO", "BUSCAR", "CRISTAL", True, True, False)


def frase_glifos(e):
    _, s, v, o, neg, spl, opl = e
    out = [o] + (["PLURAL"] if opl else []) + (["NO"] if neg else []) + [v] + [s] + (["PLURAL"] if spl else [])
    return out


def inscripcion(rng):
    glifos = PALABRAS[:]
    # cada palabra del objetivo se deduce: su patrón de apariciones en los ejemplos es único
    pat = {w: tuple(i for i, e in enumerate(EJEMPLOS) if w in frase_glifos(e)) for w in PALABRAS}
    usadas = {w for e in EJEMPLOS for w in frase_glifos(e)}
    for w in frase_glifos(OBJETIVO):
        assert w in usadas, w
        assert sum(1 for x in usadas if pat[x] == pat[w]) == 1, w
    # sin el ejemplo de la carta 53 (el último), PLURAL y COLOSO no se distinguen
    pat4 = {w: tuple(i for i, e in enumerate(EJEMPLOS[:4]) if w in frase_glifos(e)) for w in PALABRAS}
    assert pat4["PLURAL"] == pat4["COLOSO"]
    forma = list(range(len(glifos)))
    rng.shuffle(forma)
    return dict(palabras=PALABRAS, forma={w: forma[i] for i, w in enumerate(PALABRAS)},
                ejemplos=[dict(es=e[0], glifos=frase_glifos(e)) for e in EJEMPLOS],
                objetivo=dict(es=OBJETIVO[0], glifos=frase_glifos(OBJETIVO)))


# 12 glifos de trazos en un cuadrado de 0 a 1: ("l", x0, y0, x1, y1) línea · ("c", cx, cy, r) círculo · ("p", cx, cy) punto
GLIFOS = [
    [("l", .5, .1, .5, .9), ("c", .5, .3, .18)],
    [("l", .15, .85, .5, .15), ("l", .5, .15, .85, .85), ("l", .3, .55, .7, .55)],
    [("c", .5, .5, .32), ("p", .5, .5)],
    [("l", .15, .2, .85, .2), ("l", .5, .2, .5, .85), ("l", .25, .85, .75, .85)],
    [("l", .15, .15, .85, .85), ("l", .85, .15, .15, .85), ("c", .5, .5, .12)],
    [("l", .2, .5, .8, .5), ("l", .8, .5, .55, .25), ("l", .8, .5, .55, .75)],
    [("l", .2, .2, .2, .8), ("l", .2, .8, .8, .8), ("l", .8, .8, .8, .4), ("p", .55, .45)],
    [("c", .35, .5, .17), ("c", .65, .5, .17)],
    [("l", .5, .1, .9, .5), ("l", .9, .5, .5, .9), ("l", .5, .9, .1, .5), ("l", .1, .5, .5, .1)],
    [("l", .2, .3, .8, .3), ("l", .2, .7, .8, .7), ("p", .5, .5)],
    [("l", .3, .1, .3, .9), ("l", .7, .1, .7, .9), ("l", .3, .5, .7, .5)],
    [("c", .5, .62, .25), ("l", .5, .1, .5, .37), ("l", .35, .2, .65, .2)],
]


# ================================================================== 52 · La dosis
PESOS = list(range(50, 100, 5))          # filas de la tabla (kg, desde... hasta 4 más)
ALTURAS = [150, 160, 170, 180, 190]       # columnas (cm, desde... hasta 9 más)


def dosis(rng):
    tabla = []
    for i, p in enumerate(PESOS):
        fila = []
        for j, a in enumerate(ALTURAS):
            fila.append(4 + i + j + rng.choice([0, 0, 1]))
        tabla.append(fila)
    while True:
        cris = dict(peso=rng.randrange(52, 68), altura=rng.randrange(158, 172))
        alb = dict(peso=rng.randrange(72, 92), altura=rng.randrange(172, 186))
        idx = lambda v, xs, paso: max(k for k, x in enumerate(xs) if v >= x)
        dc = tabla[idx(cris["peso"], PESOS, 5)][idx(cris["altura"], ALTURAS, 10)]
        da = tabla[idx(alb["peso"], PESOS, 5)][idx(alb["altura"], ALTURAS, 10)]
        if dc != da and dc <= 15 and da <= 15:
            return dict(pesos=PESOS, alturas=ALTURAS, tabla=tabla, cristina=cris, alberto=alb, dosis=dict(Cristina=dc, Alberto=da))


# ================================================================== 46 · Pisadas (Hitori)
def hitori_soluciones(n, g, tope=2):
    sols = []
    marcadas = set()

    def conexo():
        libres = [(f, c) for f in range(n) for c in range(n) if (f, c) not in marcadas]
        vis, pila = {libres[0]}, [libres[0]]
        while pila:
            p = pila.pop()
            for a, b in V4:
                q = (p[0] + a, p[1] + b)
                if 0 <= q[0] < n and 0 <= q[1] < n and q not in marcadas and q not in vis:
                    vis.add(q)
                    pila.append(q)
        return len(vis) == len(libres)

    # solo pueden marcarse casillas con número repetido en su fila o columna
    cand = [(f, c) for f in range(n) for c in range(n)
            if sum(1 for x in range(n) if g[f][x] == g[f][c]) > 1 or sum(1 for y in range(n) if g[y][c] == g[f][c]) > 1]

    def sin_repes_hasta(f0):
        for f in range(n):
            vals = [g[f][c] for c in range(n) if (f, c) not in marcadas]
            if f < f0 and len(vals) != len(set(vals)):
                return False
        return True

    def final_ok():
        for i in range(n):
            fila = [g[i][c] for c in range(n) if (i, c) not in marcadas]
            col = [g[f][i] for f in range(n) if (f, i) not in marcadas]
            if len(fila) != len(set(fila)) or len(col) != len(set(col)):
                return False
        return conexo()

    def rec(k):
        if len(sols) >= tope:
            return
        if k == len(cand):
            if final_ok():
                sols.append(sorted(marcadas))
            return
        p = cand[k]
        # no marcar
        rec(k + 1)
        # marcar (si no toca otra marcada y no rompe la conexión)
        if not any((p[0] + a, p[1] + b) in marcadas for a, b in V4):
            marcadas.add(p)
            if conexo():
                rec(k + 1)
            marcadas.discard(p)

    rec(0)
    return sols


def pisadas(rng):
    n = 6
    while True:
        base = list(range(1, n + 1))
        filas = []
        for f in range(n):
            filas.append(base[f:] + base[:f])
        rng.shuffle(filas)
        cols = list(range(n))
        rng.shuffle(cols)
        sim = list(range(1, n + 1))
        rng.shuffle(sim)
        g = [[sim[filas[f][cols[c]] - 1] for c in range(n)] for f in range(n)]
        marc = set()
        orden = [(f, c) for f in range(n) for c in range(n)]
        rng.shuffle(orden)
        for p in orden:
            if len(marc) >= 9:
                break
            if any((p[0] + a, p[1] + b) in marc for a, b in V4):
                continue
            marc.add(p)
            libres = [(f, c) for f in range(n) for c in range(n) if (f, c) not in marc]
            vis, pila = {libres[0]}, [libres[0]]
            while pila:
                q = pila.pop()
                for a, b in V4:
                    r = (q[0] + a, q[1] + b)
                    if 0 <= r[0] < n and 0 <= r[1] < n and r not in marc and r not in vis:
                        vis.add(r)
                        pila.append(r)
            if len(vis) != len(libres):
                marc.discard(p)
        # cada casilla pisada copia el número de otra casilla de su fila o columna
        for f, c in marc:
            opciones = [g[f][x] for x in range(n) if x != c and (f, x) not in marc] + [g[y][c] for y in range(n) if y != f and (y, c) not in marc]
            g[f][c] = rng.choice(opciones)
        if hitori_soluciones(n, g) == [sorted(marc)] and len(marc) >= 7:
            return dict(n=n, numeros=g, solucion=sorted(map(list, marc)))


# ================================================================== 51 · El canto de los colosos (Simon traducido)
SONIDOS = ["grave", "agudo", "largo", "doble"]         # lo que canta el coloso
RESPUESTAS = ["piedra", "río", "luna", "flor"]         # los botones de la respuesta


def canto(rng):
    trad = RESPUESTAS[:]
    rng.shuffle(trad)
    traduccion = dict(zip(SONIDOS, trad))
    rondas = []
    for largo in (3, 4, 5):
        while True:
            r = [rng.choice(SONIDOS) for _ in range(largo)]
            if len(set(r)) >= 3:
                break
        rondas.append(r)
    # regla: en la última ronda se responde al revés (está en la carta de la sargento)
    respuesta = [[traduccion[s] for s in r] for r in rondas]
    respuesta[-1] = respuesta[-1][::-1]
    return dict(sonidos=SONIDOS, respuestas=RESPUESTAS, traduccion=traduccion, rondas=rondas, solucion=respuesta,
                nota_sargento=SONIDOS[:1], cancionero=SONIDOS[1:])


# ================================================================== 69 · Las ofrendas del Coloso Viejo (caja negra)
COLORES_P = ["roja", "azul", "blanca"]
FORMAS_P = ["redonda", "picuda"]
PIEDRAS = [(c, f) for c in COLORES_P for f in FORMAS_P]
OFRENDAS = list(itertools.product(range(6), repeat=3))


def _atomos():
    at = []
    for c in COLORES_P:
        at.append((f"hay alguna piedra {c}", lambda o, c=c: any(PIEDRAS[p][0] == c for p in o)))
        at.append((f"la piedra del centro es {c}", lambda o, c=c: PIEDRAS[o[1]][0] == c))
        at.append((f"hay dos o más piedras {c}s", lambda o, c=c: sum(PIEDRAS[p][0] == c for p in o) >= 2))
    for fo in FORMAS_P:
        at.append((f"la piedra del centro es {fo}", lambda o, fo=fo: PIEDRAS[o[1]][1] == fo))
        at.append((f"la primera piedra es {fo}", lambda o, fo=fo: PIEDRAS[o[0]][1] == fo))
        at.append((f"la última piedra es {fo}", lambda o, fo=fo: PIEDRAS[o[2]][1] == fo))
    at.append(("la primera y la última son del mismo color", lambda o: PIEDRAS[o[0]][0] == PIEDRAS[o[2]][0]))
    at.append(("las tres son de colores distintos", lambda o: len({PIEDRAS[p][0] for p in o}) == 3))
    at.append(("hay exactamente dos picudas", lambda o: sum(PIEDRAS[p][1] == "picuda" for p in o) == 2))
    at.append(("las tres tienen la misma forma", lambda o: len({PIEDRAS[p][1] for p in o}) == 1))
    return at


def ofrendas(rng):
    at = _atomos()
    hip = [(a[0], a[1]) for a in at] + [("no " + a[0], (lambda o, f=a[1]: not f(o))) for a in at]
    hip += [(f"{a[0]} y {b[0]}", (lambda o, f=a[1], g=b[1]: f(o) and g(o))) for a, b in itertools.combinations(at, 2)]
    hip += [(f"{a[0]} y no {b[0]}", (lambda o, f=a[1], g=b[1]: f(o) and not g(o))) for a, b in itertools.permutations(at, 2)]
    ext = {}
    for nombre, f in hip:
        e = frozenset(i for i, o in enumerate(OFRENDAS) if f(o))
        if 30 < len(e) < 150:
            ext.setdefault(e, nombre)
    exts = list(ext.items())
    while True:
        objetivo, nombre = rng.choice(exts)
        if " y " not in nombre:
            continue
        ejemplos = []
        vivos = [e for e, _ in exts]
        idx = list(range(len(OFRENDAS)))
        rng.shuffle(idx)
        for i in idx:
            if len(vivos) == 1 or len(ejemplos) >= 10:
                break
            si = i in objetivo
            quedan = [e for e in vivos if (i in e) == si]
            if len(quedan) <= len(vivos) * 0.7:
                ejemplos.append(i)
                vivos = quedan
        if len(vivos) != 1 or len(ejemplos) < 8:
            continue
        # sin las del cuaderno (71) queda más de una regla posible
        en70, en71 = ejemplos[:-3], ejemplos[-3:]
        vivos70 = [e for e, _ in exts if all((i in e) == (i in objetivo) for i in en70)]
        if len(vivos70) < 3:
            continue
        resto = [i for i in idx if i not in ejemplos]
        si_ = [i for i in resto if i in objetivo]
        no_ = [i for i in resto if i not in objetivo]
        k = rng.choice([2, 3])
        prueba = rng.sample(si_, k) + rng.sample(no_, 6 - k)
        rng.shuffle(prueba)
        # las reglas que sobreviven sin la carta 71 no aciertan todas las ofrendas nuevas
        if all(all((i in e) == (i in objetivo) for i in prueba) for e in vivos70 if e != objetivo):
            continue
        conv = lambda i: [list(PIEDRAS[p]) for p in OFRENDAS[i]]
        return dict(regla=nombre, ejemplos_70=[dict(piedras=conv(i), acepta=i in objetivo) for i in en70],
                    ejemplos_71=[dict(piedras=conv(i), acepta=i in objetivo) for i in en71],
                    prueba=[conv(i) for i in prueba], solucion=[j for j, i in enumerate(prueba) if i in objetivo])


# ================================================================== 72 · Las palancas de la Torre del Reloj (memoria por etapas)
SIMBOLOS = ["campana", "llave", "luna", "rueda"]


def palancas(rng):
    reglas = []
    for etapa in range(5):
        fila = []
        for d in range(4):
            tipos = ["pos", "sim"] + (["igual_pos", "igual_sim"] if etapa > 0 else [])
            t = rng.choice(tipos)
            if t == "pos":
                fila.append(["pos", rng.randrange(4)])
            elif t == "sim":
                fila.append(["sim", rng.choice(SIMBOLOS)])
            else:
                fila.append([t, rng.randrange(etapa)])
        reglas.append(fila)
    return dict(simbolos=SIMBOLOS, reglas=reglas)


def resolver_palancas(reglas, esferas, ordenes):
    """esferas[e] = número de la esfera (1-4) y ordenes[e] = símbolos de izquierda a derecha. Devuelve la posición pulsada en cada etapa."""
    pos, sim = [], []
    for e in range(5):
        t, x = reglas[e][esferas[e] - 1]
        if t == "pos":
            p = x
        elif t == "sim":
            p = ordenes[e].index(x)
        elif t == "igual_pos":
            p = pos[x]
        else:
            p = ordenes[e].index(sim[x])
        pos.append(p)
        sim.append(ordenes[e][p])
    return pos


def texto_regla(r):
    t, x = r
    nombres = ["la primera", "la segunda", "la tercera", "la cuarta"]
    if t == "pos":
        return f"tirad de {nombres[x]} palanca"
    if t == "sim":
        return f"tirad de la palanca de la {x}"
    if t == "igual_pos":
        return f"tirad de la palanca que esté en el mismo sitio que en la etapa {x + 1}"
    return f"tirad de la palanca del mismo dibujo que en la etapa {x + 1}"


# ================================================================== 64 · El tesoro del Coloso Viejo (agrupar)
MATERIALES = ["oro", "plata", "cobre", "vidrio"]
TIPOS = ["anillo", "moneda", "llave", "campanita"]


def _pred_lib():
    P = []
    for m in MATERIALES:
        P.append((f"todo lo de {m}", lambda o, m=m: o["material"] == m))
        for t in TIPOS:
            P.append((f"lo de {m} que no sea {('un ' if t in ('anillo',) else 'una ')}{t}", lambda o, m=m, t=t: o["material"] == m and o["tipo"] != t))
    for k in range(1, 5):
        P.append((f"lo que tenga {k} muesca{'s' if k > 1 else ''}", lambda o, k=k: o["muescas"] == k))
        P.append((f"lo que tenga más de {k} muesca{'s' if k > 1 else ''}", lambda o, k=k: o["muescas"] > k))
    for t in TIPOS:
        P.append((f"{'los' if t in ('anillo',) else 'las'} {t}s", lambda o, t=t: o["tipo"] == t))
        for t2 in TIPOS:
            if t < t2:
                P.append((f"{t}s y {t2}s con número par de muescas", lambda o, t=t, t2=t2: o["tipo"] in (t, t2) and o["muescas"] % 2 == 0))
    return P


def _asignaciones(objs, preds, tope=2):
    n = len(objs)
    cuenta = [0] * 4
    asig = [None] * n
    sols = []

    def rec(i):
        if len(sols) >= tope:
            return
        if i == n:
            sols.append(asig[:])
            return
        for g in range(4):
            if cuenta[g] < 4 and preds[g][1](objs[i]):
                cuenta[g] += 1
                asig[i] = g
                rec(i + 1)
                cuenta[g] -= 1
                asig[i] = None
    rec(0)
    return sols


def tesoro(rng):
    lib = _pred_lib()
    while True:
        combos = [(m, t) for m in MATERIALES for t in TIPOS]
        rng.shuffle(combos)
        objs = [dict(material=m, tipo=t, muescas=rng.randrange(1, 5)) for m, t in combos]
        preds = rng.sample(lib, 4)
        sols = _asignaciones(objs, preds)
        if len(sols) != 1:
            continue
        # tiene que haber trampas: objetos que cumplen dos condiciones
        dobles = sum(1 for o in objs if sum(p[1](o) for p in preds) > 1)
        if dobles < 4:
            continue
        grupos = [[i for i in range(16) if sols[0][i] == g] for g in range(4)]
        return dict(objetos=[dict(letra="ABCDEFGHIJKLMNOP"[i], **o) for i, o in enumerate(objs)],
                    condiciones=[p[0] for p in preds], grupos=grupos)


# ================================================================== 85 · Meta: las marcas sobre la inscripción
INSCRIPCION = "QUIEN SIGA LA FLOR DE CINCO PETALOS HALLARA SIEMPRE EL CAMINO DE VUELTA AL HOGAR"
ORDEN_META = ["52", "14", "48", "20", "40"]          # el orden en que se leen las marcas (carta 87): da H, O, G, A, R


def meta(rng):
    letras = [ch for ch in INSCRIPCION if ch.isalpha()]
    cols = 9
    while len(letras) % cols:
        letras.append("·")
    filas = len(letras) // cols
    rejilla = ["".join(letras[f * cols:(f + 1) * cols]) for f in range(filas)]
    marcas = {}
    usadas = set()
    for app, letra in zip(ORDEN_META, "HOGAR"):
        opciones = [(f, c) for f in range(filas) for c in range(cols) if rejilla[f][c] == letra and (f, c) not in usadas]
        f, c = rng.choice(opciones)
        usadas.add((f, c))
        marcas[app] = f"{f + 1}{c + 1}"
    return dict(rejilla=rejilla, marcas=marcas, orden=ORDEN_META, palabra="HOGAR")


def main():
    rng = random.Random(1914)
    inst = {}
    inst["faroles"] = faroles(rng)
    print("faroles:", len(inst["faroles"]["numeros"]), "números,", len(inst["faroles"]["solucion"]), "faroles")
    inst["cronica"] = cronica(rng)
    print("cronica:", [SUCESOS[i] for i in inst["cronica"]["solucion"]])
    inst["barracones"] = barracones(rng)
    print("barracones:", len(inst["barracones"]["lista"]), "+", len(inst["barracones"]["plano"]), "números")
    inst["inscripcion"] = inscripcion(rng)
    inst["glifos"] = [[list(t) for t in g] for g in GLIFOS]
    inst["dosis"] = dosis(rng)
    print("dosis:", inst["dosis"]["dosis"])
    inst["pisadas"] = pisadas(rng)
    print("pisadas:", len(inst["pisadas"]["solucion"]), "casillas")
    inst["canto"] = canto(rng)
    print("canto:", inst["canto"]["solucion"])
    inst["ofrendas"] = ofrendas(rng)
    print("ofrendas:", inst["ofrendas"]["regla"], inst["ofrendas"]["solucion"])
    inst["palancas"] = palancas(rng)
    inst["tesoro"] = tesoro(rng)
    print("tesoro:", inst["tesoro"]["condiciones"])
    inst["meta"] = meta(rng)
    print("meta:", inst["meta"]["marcas"])
    with open(RUTA, "w", encoding="utf-8", newline="\n") as f:
        json.dump(inst, f, ensure_ascii=False, indent=1)
    print("escrito", RUTA)


def _cargar():
    if not os.path.exists(RUTA):
        main()
    return json.load(open(RUTA, encoding="utf-8"))


if __name__ == "__main__":
    main()
else:
    INST = _cargar()

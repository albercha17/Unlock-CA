"""Instancias de los puzles NUEVOS con los que se amplían los juegos cortos hasta 36 cartas (20 oct 2026), con semilla fija y
solución única comprobada por fuerza bruta. Escribe instancias_ampliacion.json (lo leen dibujos_ampliacion.py, los datos de cada juego,
los minijuegos ―dibujos_ampliacion.py les copia sus datos― y los solucionadores).

  - marte_circuito: tres salidas (motor, alarma, ventilación) con puertas Y / O / NO y cinco interruptores; una sola combinación.
  - marte_muestras: «caja negra» del analizador: nueve muestras de ejemplo con su veredicto; todas las reglas compatibles clasifican
                    igual las ocho muestras de la bandeja.
  - egipto_ofrendas: KenKen de sumas 4 x 4 (jaulas que no cruzan la mitad, para partirlo en dos cartas); solución única.
  - egipto_tachar:  Hitori 5 x 5 (tachar repetidos sin juntar tachones y sin aislar casillas); solución única.
  - florencia_baul: cuatro piezas (cajas de inventos) que llenan un baúl de 5 x 4; se cuentan los encajes posibles (la app acepta cualquiera).
  - espia_poker:    cuatro manos de póker de categorías distintas; el orden de mejor a peor.
  - piratas_campanas: guardias y campanadas de a bordo; la hora del diario.
  - juguetes_cubos: cuatro cubos con seis dibujos partidos en cuartos.
  - faro_bahia:     islas de la bahía (Nurikabe 6 x 6, pistas partidas en dos cartas); solución única.
  - faro_sombras:   tres objetos que, puestos en orden ante la lámpara, dan la sombra de la pared; ninguna otra terna la da.
  - faro_destellos: la característica de la luz de Cabo Niebla en 12 segundos.
Uso (desde la raíz del repo):  python herramientas/instancias_ampliacion.py
"""
import itertools
import json
import os
import random

AQUI = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ Marte: circuito lógico
def evaluar(nodo, v):
    t = nodo[0]
    if t == "in":
        return v[nodo[1]]
    if t == "NO":
        return not evaluar(nodo[1], v)
    a, b = evaluar(nodo[1], v), evaluar(nodo[2], v)
    return (a and b) if t == "Y" else (a or b)


def marte_circuito():
    rng = random.Random(2157)
    ins = "ABCDE"

    def hoja():
        return ("in", rng.choice(ins))

    def arbol():
        g1 = rng.choice(["Y", "O"])
        sub = (g1, hoja(), hoja())
        if rng.random() < 0.4:
            sub = ("NO", sub)
        g2 = rng.choice(["Y", "O"])
        otro = hoja() if rng.random() < 0.6 else ("NO", hoja())
        return (g2, sub, otro)
    quiere = {"motor": True, "alarma": False, "ventilacion": True}
    for _ in range(20000):
        salidas = {k: arbol() for k in quiere}
        usadas = set()

        def recoger(n):
            if n[0] == "in":
                usadas.add(n[1])
            else:
                for h in n[1:]:
                    recoger(h)
        for s in salidas.values():
            recoger(s)
        if usadas != set(ins):
            continue
        sols = [c for c in itertools.product((False, True), repeat=5)
                if all(evaluar(salidas[k], dict(zip(ins, c))) == quiere[k] for k in quiere)]
        if len(sols) == 1 and 2 <= sum(sols[0]) <= 3:
            return {"salidas": salidas, "quiere": quiere, "solucion": dict(zip(ins, sols[0]))}
    raise SystemExit("sin circuito")


# ------------------------------------------------------------------ Marte: caja negra de muestras
ATRIB = {"color": ["rojo", "gris", "negro"], "forma": ["redonda", "angulosa"], "vetas": [0, 1, 2], "cristal": [False, True]}


def reglas():
    simples = []
    for a, vs in ATRIB.items():
        for v in vs:
            simples.append((f"{a}={v}", lambda m, a=a, v=v: m[a] == v))
            if len(vs) > 2:
                simples.append((f"{a}!={v}", lambda m, a=a, v=v: m[a] != v))
    out = list(simples)
    for (n1, f1), (n2, f2) in itertools.combinations(simples, 2):
        out.append((f"{n1} y {n2}", lambda m, f1=f1, f2=f2: f1(m) and f2(m)))
        out.append((f"{n1} o {n2}", lambda m, f1=f1, f2=f2: f1(m) or f2(m)))
    return out


def marte_muestras():
    rng = random.Random(88)
    todas = [dict(zip(ATRIB, c)) for c in itertools.product(*ATRIB.values())]
    R = reglas()
    verdad = next(r for r in R if r[0] == "color!=rojo y cristal=True")
    for _ in range(5000):
        rng.shuffle(todas)
        ejemplos, bandeja = todas[:9], todas[9:17]
        etiq = [verdad[1](m) for m in ejemplos]
        if not 3 <= sum(etiq) <= 5:
            continue
        compatibles = [r for r in R if all(r[1](m) == e for m, e in zip(ejemplos, etiq))]
        clas = {tuple(r[1](m) for m in bandeja) for r in compatibles}
        res = [verdad[1](m) for m in bandeja]
        if len(clas) == 1 and 2 <= sum(res) <= 4:
            return {"regla": verdad[0], "ejemplos": [dict(m, pasa=e) for m, e in zip(ejemplos, etiq)], "bandeja": bandeja,
                    "solucion": [i for i, r in enumerate(res) if r], "compatibles": len(compatibles)}
    raise SystemExit("sin caja negra")


# ------------------------------------------------------------------ Egipto: KenKen de sumas
def latinos(n):
    filas = list(itertools.permutations(range(1, n + 1)))
    out = []

    def rec(acum):
        if len(acum) == n:
            out.append([list(f) for f in acum])
            return
        for f in filas:
            if all(f[c] != a[c] for a in acum for c in range(n)):
                rec(acum + [f])
    rec([])
    return out


def egipto_ofrendas():
    rng = random.Random(1274)
    L = latinos(4)
    for _ in range(4000):
        sol = rng.choice(L)
        libres = {(f, c) for f in range(4) for c in range(4)}
        jaulas = []
        while libres:
            f, c = min(libres)
            j = [(f, c)]
            libres.discard((f, c))
            objetivo = rng.choice([1, 2, 2, 3, 3])
            while len(j) < objetivo:
                vec = [(a + df, b + dc) for a, b in j for df, dc in ((0, 1), (1, 0), (0, -1), (-1, 0))
                       if (a + df, b + dc) in libres and (a + df < 2) == (f < 2)]
                if not vec:
                    break
                x = rng.choice(vec)
                j.append(x)
                libres.discard(x)
            jaulas.append(j)
        if sum(len(j) == 1 for j in jaulas) > 2:
            continue
        sumas = [sum(sol[f][c] for f, c in j) for j in jaulas]
        n = sum(all(sum(m[f][c] for f, c in j) == s for j, s in zip(jaulas, sumas)) for m in L)
        if n == 1:
            return {"solucion": sol, "jaulas": [[list(x) for x in j] for j in jaulas], "sumas": sumas}
    raise SystemExit("sin kenken")


# ------------------------------------------------------------------ Egipto: Hitori
def hitori_soluciones(g, limite=2):
    n = len(g)
    out = []
    tach = [[False] * n for _ in range(n)]

    def conexo():
        libres = [(f, c) for f in range(n) for c in range(n) if not tach[f][c]]
        vis, pila = {libres[0]}, [libres[0]]
        while pila:
            f, c = pila.pop()
            for df, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                x = (f + df, c + dc)
                if 0 <= x[0] < n and 0 <= x[1] < n and not tach[x[0]][x[1]] and x not in vis:
                    vis.add(x)
                    pila.append(x)
        return len(vis) == len(libres)

    def ok_parcial(f, c):
        if tach[f][c]:
            if (f > 0 and tach[f - 1][c]) or (c > 0 and tach[f][c - 1]):
                return False
        else:
            for cc in range(c):
                if not tach[f][cc] and g[f][cc] == g[f][c]:
                    return False
            for ff in range(f):
                if not tach[ff][c] and g[ff][c] == g[f][c]:
                    return False
        return True

    def rec(i):
        if len(out) >= limite:
            return
        if i == n * n:
            if conexo():
                out.append([r[:] for r in tach])
            return
        f, c = divmod(i, n)
        for t in (False, True):
            tach[f][c] = t
            if ok_parcial(f, c):
                rec(i + 1)
        tach[f][c] = False
    rec(0)
    return out


def egipto_tachar():
    rng = random.Random(1275)
    n = 5
    for _ in range(20000):
        base = rng.choice(latinos(5)) if False else None
        # solución: un cuadrado latino al que se le tapan casillas con números repetidos
        perm = list(range(1, n + 1))
        filas = []
        for f in range(n):
            filas.append(perm[f:] + perm[:f])
        rng.shuffle(filas)
        cols = list(range(n))
        rng.shuffle(cols)
        g = [[filas[f][c] for c in cols] for f in range(n)]
        tachadas = set()
        for f in range(n):
            for c in range(n):
                if rng.random() < 0.3 and all((f + df, c + dc) not in tachadas for df, dc in ((0, 1), (1, 0), (0, -1), (-1, 0))):
                    tachadas.add((f, c))
        for f, c in tachadas:
            otras = [g[f][cc] for cc in range(n) if cc != c] + [g[ff][c] for ff in range(n) if ff != f]
            g[f][c] = rng.choice(otras)
        if not 5 <= len(tachadas) <= 8:
            continue
        sols = hitori_soluciones(g)
        if len(sols) == 1 and {(f, c) for f in range(n) for c in range(n) if sols[0][f][c]} == tachadas:
            return {"rejilla": g, "tachadas": sorted([list(x) for x in tachadas])}
    raise SystemExit("sin hitori")


# ------------------------------------------------------------------ Florencia: piezas en el baúl
PIEZAS = {                                                       # sale de partir el baúl de 5 x 4 en cuatro piezas
    "ornitoptero": [(0, 0), (1, 0), (2, 0), (3, 0), (1, 1)],
    "leon": [(1, 0), (1, 1), (1, 2), (0, 2), (1, 3)],
    "laud": [(0, 0), (0, 1), (1, 1), (0, 2)],
    "carro": [(1, 0), (2, 0), (1, 1), (0, 2), (1, 2), (2, 2)],
}


def orientaciones(p):
    out = set()
    pts = p
    for _ in range(4):
        pts = [(y, -x) for x, y in pts]
        for q in (pts, [(-x, y) for x, y in pts]):
            mx, my = min(x for x, _ in q), min(y for _, y in q)
            out.add(tuple(sorted((x - mx, y - my) for x, y in q)))
    return sorted(out)


def rotaciones(p):
    """Solo giros (sin darle la vuelta a la caja): es lo que permite la app."""
    out = []
    pts = p
    for _ in range(4):
        pts = [(y, -x) for x, y in pts]
        mx, my = min(x for x, _ in pts), min(y for _, y in pts)
        o = tuple(sorted((x - mx, y - my) for x, y in pts))
        if o not in out:
            out.append(o)
    return out


def encajes(ancho, alto, piezas):
    nombres = list(piezas)
    sols = []

    def rec(i, ocupado, colocadas):
        if i == len(nombres):
            if len(ocupado) == ancho * alto:
                sols.append(dict(colocadas))
            return
        for o in rotaciones(piezas[nombres[i]]):
            for x0 in range(ancho):
                for y0 in range(alto):
                    cel = [(x0 + x, y0 + y) for x, y in o]
                    if all(0 <= x < ancho and 0 <= y < alto and (x, y) not in ocupado for x, y in cel):
                        colocadas[nombres[i]] = sorted(cel)
                        rec(i + 1, ocupado | set(cel), colocadas)
                        del colocadas[nombres[i]]
    rec(0, frozenset(), {})
    return sols


def florencia_baul():
    ancho, alto = 5, 4
    sols = encajes(ancho, alto, PIEZAS)
    assert sum(len(v) for v in PIEZAS.values()) == ancho * alto
    assert sols, "las piezas no encajan"
    return {"ancho": ancho, "alto": alto, "piezas": {k: [list(p) for p in v] for k, v in PIEZAS.items()},
            "soluciones": [{k: [list(c) for c in v] for k, v in s.items()} for s in sols], "n_soluciones": len(sols)}


# ------------------------------------------------------------------ Montecarlo: póker
CATEGORIAS = ["escalera de color", "póker", "full", "color", "escalera", "trío", "dobles parejas", "pareja", "carta alta"]


def categoria(mano):
    vals = sorted((v for v, _ in mano), reverse=True)
    palos = {p for _, p in mano}
    cuenta = sorted((vals.count(v) for v in set(vals)), reverse=True)
    escalera = len(set(vals)) == 5 and vals[0] - vals[4] == 4
    if escalera and len(palos) == 1:
        return "escalera de color"
    if cuenta[0] == 4:
        return "póker"
    if cuenta[:2] == [3, 2]:
        return "full"
    if len(palos) == 1:
        return "color"
    if escalera:
        return "escalera"
    if cuenta[0] == 3:
        return "trío"
    if cuenta[:2] == [2, 2]:
        return "dobles parejas"
    if cuenta[0] == 2:
        return "pareja"
    return "carta alta"


def espia_poker():
    jugadores = ["La Condesa", "El Barón", "El Dr. Noche", "La Agente Zorro"]
    manos = {
        # parece color, pero hay un corazón entre los diamantes: es escalera
        "La Condesa": [(9, "diamantes"), (10, "diamantes"), (11, "corazones"), (12, "diamantes"), (13, "diamantes")],
        "El Barón": [(7, "picas"), (7, "corazones"), (7, "tréboles"), (2, "diamantes"), (2, "picas")],
        "El Dr. Noche": [(3, "tréboles"), (8, "tréboles"), (11, "tréboles"), (5, "tréboles"), (13, "tréboles")],
        "La Agente Zorro": [(12, "picas"), (12, "corazones"), (4, "tréboles"), (4, "diamantes"), (9, "picas")],
    }
    cats = {j: categoria(m) for j, m in manos.items()}
    assert len(set(cats.values())) == 4
    orden = sorted(jugadores, key=lambda j: CATEGORIAS.index(cats[j]))
    return {"jugadores": jugadores, "manos": {j: [list(c) for c in m] for j, m in manos.items()}, "categorias": cats, "orden": orden,
            "ranking": CATEGORIAS}


# ------------------------------------------------------------------ Piratas: campanadas
GUARDIAS = [("Primera", 20), ("Media", 0), ("Alba", 4), ("Mañana", 8), ("Tarde", 12), ("Perro", 16)]


def hora(guardia, campanadas):
    inicio = dict(GUARDIAS)[guardia]
    m = (inicio * 60 + campanadas * 30) % (24 * 60)
    return m // 60, m % 60


def piratas_campanas():
    g, c = "Tarde", 5
    h, m = hora(g, c)
    return {"guardias": GUARDIAS, "guardia": g, "campanadas": c, "hora": [h, m]}


# ------------------------------------------------------------------ Juguetes: cubos de imágenes
def juguetes_cubos():
    dibujos = ["perro", "barco", "casa", "sol", "cohete", "arbol"]
    rng = random.Random(1995)
    caras = []
    for _ in range(4):
        d = dibujos[:]
        rng.shuffle(d)
        caras.append(d)
    objetivo = "perro"
    inicial = [0, 0, 0, 0]
    while any(caras[i][inicial[i]] == objetivo for i in range(4)):
        inicial = [rng.randrange(6) for _ in range(4)]
    return {"dibujos": dibujos, "caras": caras, "objetivo": objetivo, "inicial": inicial,
            "solucion": [caras[i].index(objetivo) for i in range(4)]}


# ------------------------------------------------------------------ Faro: islas de la bahía (Nurikabe)
def poliominos(origen, tam, n):
    """Todos los poliominós de `tam` casillas que contienen `origen` en una rejilla n x n."""
    out = set()

    def crecer(actual):
        if len(actual) == tam:
            out.add(frozenset(actual))
            return
        for (f, c) in list(actual):
            for df, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                x = (f + df, c + dc)
                if 0 <= x[0] < n and 0 <= x[1] < n and x not in actual:
                    crecer(actual | {x})
    crecer(frozenset([origen]))
    return list(out)


def mar_valido(islas, n):
    tierra = set().union(*islas) if islas else set()
    mar = [(f, c) for f in range(n) for c in range(n) if (f, c) not in tierra]
    for f in range(n - 1):
        for c in range(n - 1):
            if all(x not in tierra for x in ((f, c), (f + 1, c), (f, c + 1), (f + 1, c + 1))):
                return False
    if not mar:
        return False
    vis, pila = {mar[0]}, [mar[0]]
    while pila:
        f, c = pila.pop()
        for df, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            x = (f + df, c + dc)
            if 0 <= x[0] < n and 0 <= x[1] < n and x not in tierra and x not in vis:
                vis.add(x)
                pila.append(x)
    return len(vis) == len(mar)


def nurikabe_soluciones(pistas, n, limite=2):
    claves = sorted(pistas, key=lambda p: pistas[p])
    opciones = {p: poliominos(p, pistas[p], n) for p in claves}
    sols = []

    def vecinas(cs):
        return {(f + df, c + dc) for f, c in cs for df, dc in ((0, 1), (1, 0), (0, -1), (-1, 0))}

    def rec(i, usadas, prohibidas, islas):
        if len(sols) >= limite:
            return
        if i == len(claves):
            if mar_valido(islas, n):
                sols.append(list(islas))
            return
        for pol in opciones[claves[i]]:
            if pol & usadas or pol & prohibidas or any(q in pol for q in claves if q != claves[i]):
                continue
            rec(i + 1, usadas | pol, prohibidas | vecinas(pol), islas + [pol])
    rec(0, frozenset(), frozenset(), [])
    return sols


def faro_bahia():
    rng = random.Random(1923)
    n = 6
    for _ in range(4000):
        k = rng.randint(5, 7)
        pistas = {}
        while len(pistas) < k:
            p = (rng.randrange(n), rng.randrange(n))
            if all(abs(p[0] - q[0]) + abs(p[1] - q[1]) > 1 for q in pistas):
                pistas[p] = rng.choice([1, 2, 2, 3, 3, 4])
        if not 12 <= sum(pistas.values()) <= 17:
            continue
        sols = nurikabe_soluciones(pistas, n)
        if len(sols) == 1:
            tierra = sorted(set().union(*sols[0]))
            return {"n": n, "pistas": [[f, c, v] for (f, c), v in sorted(pistas.items())], "tierra": [list(x) for x in tierra]}
    raise SystemExit("sin bahía")


# ------------------------------------------------------------------ Faro: sombras en la pared
OBJETOS_SOMBRA = ["farol", "ancla", "botella", "tetera", "gaviota", "catalejo", "campana", "llave"]


def silueta(nombre, x0, w=120, h=160):
    """Máscara (PIL, modo L) de un objeto apoyado en la mesa, en una franja de 120 px que empieza en x0, dentro de una pared de 360 x 160."""
    from PIL import Image, ImageDraw
    im = Image.new("L", (360, h), 0)
    d = ImageDraw.Draw(im)
    cx = x0 + w // 2
    b = h - 6
    if nombre == "farol":
        d.rectangle([cx - 22, b - 70, cx + 22, b], fill=255)
        d.polygon([(cx - 30, b - 70), (cx + 30, b - 70), (cx, b - 100)], fill=255)
        d.ellipse([cx - 8, b - 116, cx + 8, b - 100], fill=255)
    elif nombre == "ancla":
        d.rectangle([cx - 5, b - 110, cx + 5, b - 10], fill=255)
        d.rectangle([cx - 30, b - 96, cx + 30, b - 86], fill=255)
        d.arc([cx - 44, b - 70, cx + 44, b + 6], 0, 180, fill=255, width=10)
        d.ellipse([cx - 10, b - 126, cx + 10, b - 106], outline=255, width=6)
    elif nombre == "botella":
        d.rounded_rectangle([cx - 20, b - 80, cx + 20, b], 8, fill=255)
        d.rectangle([cx - 7, b - 120, cx + 7, b - 78], fill=255)
    elif nombre == "tetera":
        d.ellipse([cx - 36, b - 60, cx + 36, b], fill=255)
        d.polygon([(cx + 30, b - 30), (cx + 58, b - 58), (cx + 52, b - 22)], fill=255)
        d.arc([cx - 60, b - 50, cx - 24, b - 14], 90, 270, fill=255, width=8)
        d.ellipse([cx - 8, b - 74, cx + 8, b - 58], fill=255)
    elif nombre == "gaviota":
        d.ellipse([cx - 34, b - 56, cx + 26, b - 24], fill=255)
        d.ellipse([cx + 10, b - 76, cx + 36, b - 50], fill=255)
        d.polygon([(cx + 34, b - 66), (cx + 54, b - 62), (cx + 34, b - 58)], fill=255)
        d.rectangle([cx - 6, b - 26, cx - 2, b], fill=255)
        d.rectangle([cx + 6, b - 26, cx + 10, b], fill=255)
    elif nombre == "catalejo":
        d.polygon([(cx - 50, b - 10), (cx + 50, b - 40), (cx + 54, b - 26), (cx - 46, b + 2)], fill=255)
        d.polygon([(cx - 10, b - 22), (cx + 10, b - 22), (cx + 18, b), (cx - 18, b)], fill=255)
    elif nombre == "campana":
        d.polygon([(cx - 22, b - 90), (cx + 22, b - 90), (cx + 30, b - 40), (cx + 46, b - 14), (cx - 46, b - 14), (cx - 30, b - 40)], fill=255)
        d.ellipse([cx - 12, b - 106, cx + 12, b - 84], outline=255, width=6)
        d.ellipse([cx - 9, b - 16, cx + 9, b + 2], fill=255)
    else:
        d.ellipse([cx - 26, b - 120, cx + 6, b - 88], outline=255, width=9)
        d.rectangle([cx - 14, b - 90, cx - 6, b], fill=255)
        d.rectangle([cx - 6, b - 30, cx + 14, b - 22], fill=255)
        d.rectangle([cx - 6, b - 14, cx + 10, b - 6], fill=255)
    return im


def sombra(seq):
    import numpy as np
    m = np.zeros((160, 360), bool)
    for k, nombre in enumerate(seq):
        m |= np.asarray(silueta(nombre, 120 * k)) > 128
    return m


def faro_sombras():
    import numpy as np
    meta = ["catalejo", "tetera", "ancla"]
    objetivo = sombra(meta)
    iguales = []
    for seq in itertools.permutations(OBJETOS_SOMBRA, 3):
        if np.count_nonzero(sombra(seq) ^ objetivo) < 150:
            iguales.append(seq)
    assert iguales == [tuple(meta)], iguales
    return {"objetos": OBJETOS_SOMBRA, "solucion": meta}


# ------------------------------------------------------------------ Faro: la característica de la luz
ELEMENTO = {"destello": "10", "largo": "110"}          # cada elemento termina con 1 s de oscuridad
FAROS = {                                              # el grupo empieza en el segundo 1; lo que sobra hasta 12 s, oscuro
    "Punta Gaviota": ["destello", "destello"],
    "Isla del Moro": ["largo", "destello", "destello"],
    "Cabo Niebla": ["destello", "destello", "destello", "largo"],
    "Roca Negra": ["largo", "largo"],
    "Puerto Viejo": ["destello", "destello", "destello", "destello"],
}


def patron(elems):
    s = "".join(ELEMENTO[e] for e in elems)
    return s + "0" * (12 - len(s))


def faro_destellos():
    patrones = {f: patron(e) for f, e in FAROS.items()}
    assert len(set(patrones.values())) == len(patrones)
    return {"faros": FAROS, "patrones": patrones, "faro": "Cabo Niebla", "solucion": [int(x) for x in patrones["Cabo Niebla"]]}


def main():
    inst = {"marte_circuito": marte_circuito(), "marte_muestras": marte_muestras(), "egipto_ofrendas": egipto_ofrendas(),
            "egipto_tachar": egipto_tachar(), "florencia_baul": florencia_baul(), "espia_poker": espia_poker(),
            "piratas_campanas": piratas_campanas(), "juguetes_cubos": juguetes_cubos(),
            "faro_bahia": faro_bahia(), "faro_sombras": faro_sombras(), "faro_destellos": faro_destellos()}
    with open(os.path.join(AQUI, "instancias_ampliacion.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(inst, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("circuito:", inst["marte_circuito"]["solucion"])
    print("muestras:", inst["marte_muestras"]["solucion"], "reglas compatibles:", inst["marte_muestras"]["compatibles"])
    print("ofrendas:", inst["egipto_ofrendas"]["solucion"], len(inst["egipto_ofrendas"]["jaulas"]), "jaulas")
    print("tachar:", inst["egipto_tachar"]["tachadas"])
    print("baúl:", inst["florencia_baul"]["n_soluciones"], "encajes")
    print("póker:", inst["espia_poker"]["orden"], inst["espia_poker"]["categorias"])
    print("campanas:", inst["piratas_campanas"]["hora"])
    print("cubos:", inst["juguetes_cubos"]["solucion"])
    print("bahía:", inst["faro_bahia"]["pistas"], len(inst["faro_bahia"]["tierra"]), "casillas de tierra")
    print("sombras:", inst["faro_sombras"]["solucion"], "· destellos:", inst["faro_destellos"]["solucion"])


if __name__ == "__main__":
    main()

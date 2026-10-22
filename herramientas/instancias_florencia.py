"""Instancias de los puzles de «Florencia, 1503: El Taller de Leonardo» (versión de 60 cartas, 21 oct 2026), con solución comprobada.

Once puzles de tipos que no salen en ningún otro juego de la serie:
  escitala     mensaje en una tira de cuero enrollada en una vara de cuatro caras (cifrado por transposición)
  perspectiva  punto de fuga: las líneas de un suelo dibujado en dos láminas se juntan en una casilla del horizonte
  futoshiki    cuadrado latino 5 x 5 con signos de desigualdad entre casillas vecinas
  caballo      recorrer un tablero con saltos de caballo, pasando una vez por cada casilla libre
  pigmentos    mezclar tres pigmentos para obtener la composición de un color (sistema de tres ecuaciones)
  engranajes   tren de engranajes con un eje compartido: vueltas y sentido de giro de la última rueda
  vigilantes   poner el menor número de torres de vigía para que cada plaza esté vigilada (conjunto dominante)
  mastermind   deducir el orden de cuatro pigmentos con los intentos anteriores y sus aciertos
  hidato       escalera de caracol: numerar las casillas del 1 al 25 en un camino sin saltos
  poleas       elegir el sistema de poleas que alza el peso con el esfuerzo permitido gastando menos cuerda
  cifrado      metapuzle: cifrado de Vigenère cuya clave son cuatro letras que dejan otros puzles
Uso: python herramientas/instancias_florencia.py   (comprueba todo y escribe instancias_florencia.json)
"""
import itertools
import json
import math
import os
import random

AQUI = os.path.dirname(os.path.abspath(__file__))
V4 = [(0, -1), (1, 0), (0, 1), (-1, 0)]
V8 = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]


# ------------------------------------------------------------------ escítala
def escitala():
    caras = 4
    claro = "LACLAVEESALASXXX"
    k = len(claro) // caras
    cifrado = "".join(claro[f * caras + c] for c in range(caras) for f in range(k))
    # descifrar: se escribe el cifrado en columnas de k letras y se lee por filas
    descifrado = "".join(cifrado[c * k + f] for f in range(k) for c in range(caras))
    assert descifrado == claro
    return {"caras": caras, "cifrado": cifrado, "claro": claro, "solucion": "ALAS"}


# ------------------------------------------------------------------ perspectiva (punto de fuga)
def perspectiva():
    cols, filas, lado = 6, 15, 105
    vp = (3, 4)                                     # casilla (columna, fila) del punto de fuga
    cx, cy = vp[0] * lado + lado / 2, 130 + vp[1] * lado + lado / 2
    angulos = [68, 79, 90, 101, 112]
    lineas = []
    for a in angulos:
        r = math.radians(a)
        dx, dy = math.cos(r), math.sin(r)
        d0 = 380
        # recorte del rayo (desde d0) al rectángulo útil de la lámina
        lim = []
        for t in (1, 2, 3, 4):
            pass
        tmax = 4000.0
        if dx > 0:
            tmax = min(tmax, (600 - cx) / dx)
        elif dx < 0:
            tmax = min(tmax, (30 - cx) / dx)
        if dy > 0:
            tmax = min(tmax, (1720 - cy) / dy)
        p0 = (cx + dx * d0, cy + dy * d0)
        p1 = (cx + dx * tmax, cy + dy * tmax)
        assert math.dist(p0, p1) > 150, (a, math.dist(p0, p1))
        lineas.append([[round(p0[0], 1), round(p0[1], 1)], [round(p1[0], 1), round(p1[1], 1)]])
    return {"cols": cols, "filas": filas, "lado": lado, "y0": 130, "lineas": lineas, "centro": [round(cx, 1), round(cy, 1)], "solucion": list(vp), "tolerancia": 1}


# ------------------------------------------------------------------ futoshiki
def _latino(n, rng):
    base = [[(i + j) % n for j in range(n)] for i in range(n)]
    filas = list(range(n))
    cols = list(range(n))
    rng.shuffle(filas)
    rng.shuffle(cols)
    sim = list(range(n))
    rng.shuffle(sim)
    return [[sim[base[filas[i]][cols[j]]] + 1 for j in range(n)] for i in range(n)]


def _contar_futoshiki(n, dados, desig, limite=2):
    g = [[0] * n for _ in range(n)]
    for (x, y), v in dados.items():
        g[y][x] = v
    sols = []

    def ok(x, y, v):
        for k in range(n):
            if k != x and g[y][k] == v:
                return False
            if k != y and g[k][x] == v:
                return False
        for (a, b) in desig:             # a < b
            for (p, q, menor) in ((a, b, True),):
                pass
        return True

    def cumple(x, y):
        v = g[y][x]
        for (ax, ay), (bx, by) in desig:   # (a) < (b)
            va, vb = g[ay][ax], g[by][bx]
            if va and vb and not va < vb:
                return False
        return True

    def rec(i):
        if len(sols) >= limite:
            return
        if i == n * n:
            sols.append([f[:] for f in g])
            return
        x, y = i % n, i // n
        if g[y][x]:
            if cumple(x, y):
                rec(i + 1)
            return
        for v in range(1, n + 1):
            if ok(x, y, v):
                g[y][x] = v
                if cumple(x, y):
                    rec(i + 1)
                g[y][x] = 0
    rec(0)
    return sols


def futoshiki(semilla=4, n=5):
    rng = random.Random(semilla)
    for _ in range(100):
        sol = _latino(n, rng)
        pares = []
        for y in range(n):
            for x in range(n):
                if x + 1 < n:
                    pares.append(((x, y), (x + 1, y)))
                if y + 1 < n:
                    pares.append(((x, y), (x, y + 1)))
        desig = []
        for a, b in pares:
            va, vb = sol[a[1]][a[0]], sol[b[1]][b[0]]
            desig.append((a, b) if va < vb else (b, a))
        dados = {}
        casillas = [(x, y) for y in range(n) for x in range(n)]
        rng.shuffle(casillas)
        # añadir pistas hasta que haya una sola solución
        for c in casillas:
            if len(_contar_futoshiki(n, dados, desig)) == 1:
                break
            dados[c] = sol[c[1]][c[0]]
        if len(_contar_futoshiki(n, dados, desig)) != 1:
            continue
        # quitar lo que sobre
        for d in rng.sample(desig, len(desig)):
            d2 = [e for e in desig if e != d]
            if len(_contar_futoshiki(n, dados, d2)) == 1:
                desig = d2
        for c in rng.sample(list(dados), len(dados)):
            d2 = {k: v for k, v in dados.items() if k != c}
            if len(_contar_futoshiki(n, d2, desig)) == 1:
                dados = d2
        if len(desig) <= 11 and len(dados) <= 4:
            return {"n": n, "dados": [[x, y, v] for (x, y), v in sorted(dados.items(), key=lambda t: (t[0][1], t[0][0]))],
                    "desigualdades": [[list(a), list(b)] for a, b in desig], "solucion": sol}
    raise SystemExit("sin futoshiki")


# ------------------------------------------------------------------ caballo
SALTOS = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def _recorrido_caballo(n, huecos, ini):
    libres = {(x, y) for y in range(n) for x in range(n)} - huecos
    visitado = {ini}
    ruta = [ini]

    def vecinas(p):
        return [(p[0] + dx, p[1] + dy) for dx, dy in SALTOS if (p[0] + dx, p[1] + dy) in libres and (p[0] + dx, p[1] + dy) not in visitado]

    def rec(p):
        if len(ruta) == len(libres):
            return True
        cand = sorted(vecinas(p), key=lambda q: len(vecinas(q)))
        for q in cand:
            visitado.add(q)
            ruta.append(q)
            if rec(q):
                return True
            visitado.discard(q)
            ruta.pop()
        return False
    return ruta if rec(ini) else None


def caballo(semilla=6, n=6, k=5):
    rng = random.Random(semilla)
    ini = (0, 0)
    for _ in range(500):
        huecos = set()
        while len(huecos) < k:
            c = (rng.randrange(n), rng.randrange(n))
            if c != ini:
                huecos.add(c)
        ruta = _recorrido_caballo(n, huecos, ini)
        if ruta:
            return {"n": n, "huecos": sorted([list(h) for h in huecos]), "inicio": list(ini), "ruta": [list(r) for r in ruta]}
    raise SystemExit("sin caballo")


# ------------------------------------------------------------------ pigmentos
def pigmentos():
    p = [[2, 1, 0], [1, 3, 1], [0, 1, 3]]            # gotas de [rojo, amarillo, azul] por cucharada de cada pigmento
    cucharadas = [3, 2, 4]
    objetivo = [sum(cucharadas[j] * p[j][c] for j in range(3)) for c in range(3)]
    det = (p[0][0] * (p[1][1] * p[2][2] - p[1][2] * p[2][1]) - p[0][1] * (p[1][0] * p[2][2] - p[1][2] * p[2][0])
           + p[0][2] * (p[1][0] * p[2][1] - p[1][1] * p[2][0]))
    assert det != 0
    # comprobación por fuerza bruta de que es la única mezcla
    sols = [c for c in itertools.product(range(0, 11), repeat=3) if all(sum(c[j] * p[j][k] for j in range(3)) == objetivo[k] for k in range(3))]
    assert sols == [tuple(cucharadas)], sols
    return {"pigmentos": p, "componentes": ["rojo", "amarillo", "azul"], "objetivo": objetivo, "solucion": cucharadas}


# ------------------------------------------------------------------ engranajes
def engranajes():
    dientes = {"A": 6, "B": 18, "C": 4, "D": 12}       # A engrana con B; B y C comparten eje; C engrana con D
    vueltas_a = 18
    vueltas_d = vueltas_a * dientes["A"] / dientes["B"] * dientes["C"] / dientes["D"]
    assert vueltas_d == int(vueltas_d)
    # sentido: A derecha -> B izquierda -> C (mismo eje que B) izquierda -> D derecha
    return {"dientes": dientes, "vueltas_a": vueltas_a, "sentido_a": "derecha", "solucion": {"vueltas": int(vueltas_d), "sentido": "derecha"}}


# ------------------------------------------------------------------ vigilantes (conjunto dominante mínimo)
def vigilantes(semilla=5, n=9):
    rng = random.Random(semilla)
    pos = {i: (60 + (i % 3) * 240 + rng.randint(-40, 40), 120 + (i // 3) * 190 + rng.randint(-30, 30)) for i in range(n)}
    for _ in range(5000):
        cand = [(a, b) for a, b in itertools.combinations(range(n), 2) if math.dist(pos[a], pos[b]) < 330]
        rng.shuffle(cand)
        aristas = sorted(cand[:13])
        ady = {i: {i} for i in range(n)}
        for a, b in aristas:
            ady[a].add(b)
            ady[b].add(a)
        for k in range(1, 5):
            sols = [s for s in itertools.combinations(range(n), k) if set().union(*(ady[v] for v in s)) == set(range(n))]
            if sols:
                break
        if k == 3 and 1 <= len(sols) <= 3:
            return {"n": n, "pos": {str(i): list(p) for i, p in pos.items()}, "aristas": [list(a) for a in aristas], "minimo": k,
                    "soluciones": [list(s) for s in sols]}
    raise SystemExit("sin vigilantes")


# ------------------------------------------------------------------ mastermind
COLORES = ["rojo", "azul", "verde", "amarillo", "violeta", "blanco"]


def _respuesta(secreto, intento):
    negros = sum(a == b for a, b in zip(secreto, intento))
    blancos = len(set(secreto) & set(intento)) - negros
    return negros, blancos


def mastermind(semilla=3):
    rng = random.Random(semilla)
    todos = list(itertools.permutations(range(6), 4))
    for _ in range(2000):
        secreto = rng.choice(todos)
        cons = list(todos)
        intentos = []
        while len(cons) > 1 and len(intentos) < 7:
            g = rng.choice(todos)
            if g in [i[0] for i in intentos]:
                continue
            r = _respuesta(secreto, g)
            nuevo = [c for c in cons if _respuesta(c, g) == r]
            if len(nuevo) < len(cons):
                intentos.append((g, r))
                cons = nuevo
        if len(cons) == 1 and 5 <= len(intentos) <= 6:
            return {"colores": COLORES, "intentos": [{"orden": list(g), "negros": r[0], "blancos": r[1]} for g, r in intentos], "solucion": list(secreto)}
    raise SystemExit("sin mastermind")


# ------------------------------------------------------------------ hidato
def _camino_hamilton(n, rng):
    camino = [(x, y) if y % 2 == 0 else (n - 1 - x, y) for y in range(n) for x in range(n)]
    for _ in range(2000):
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


def _contar_hidato(n, dados, limite=2):
    pos_de = {v: c for c, v in dados.items()}
    total = n * n
    sols = []
    visit = {}

    def rec(k, cur):
        if len(sols) >= limite:
            return
        if k == total:
            sols.append(dict(visit))
            return
        sig = k + 1
        if sig in pos_de:
            q = pos_de[sig]
            if q not in visit and max(abs(q[0] - cur[0]), abs(q[1] - cur[1])) == 1:
                visit[q] = sig
                rec(sig, q)
                del visit[q]
            return
        for dx, dy in V8:
            q = (cur[0] + dx, cur[1] + dy)
            if 0 <= q[0] < n and 0 <= q[1] < n and q not in visit and q not in dados:
                visit[q] = sig
                rec(sig, q)
                del visit[q]
    ini = pos_de[1]
    visit[ini] = 1
    rec(1, ini)
    return sols


def hidato(semilla=8, n=5):
    rng = random.Random(semilla)
    for _ in range(200):
        camino = _camino_hamilton(n, rng)
        sol = {c: i + 1 for i, c in enumerate(camino)}
        dados = dict(sol)
        orden = [c for c in camino[1:-1]]
        rng.shuffle(orden)
        for c in orden:
            d2 = {k: v for k, v in dados.items() if k != c}
            if len(_contar_hidato(n, d2)) == 1:
                dados = d2
        if len(dados) <= 9:
            return {"n": n, "dados": [[x, y, v] for (x, y), v in sorted(dados.items(), key=lambda t: t[1])],
                    "camino": [list(c) for c in camino]}
    raise SystemExit("sin hidato")


# ------------------------------------------------------------------ poleas
def poleas():
    peso, esfuerzo_max = 120, 30
    segmentos = [2, 3, 4, 5]                            # cuerdas que sostienen el peso en cada sistema
    orden = [4, 2, 5, 3]                                # cómo salen dibujados (el 4 es el bueno: el que menos cuerda gasta de los que alcanzan)
    validos = [s for s in orden if peso / s <= esfuerzo_max]
    bueno = min(validos)
    assert bueno == 4
    return {"peso": peso, "esfuerzo_max": esfuerzo_max, "sistemas": orden, "solucion": orden.index(bueno)}


# ------------------------------------------------------------------ cifrado final (Vigenère)
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CLAVE = "SOLE"
CLARO = "AMANECER"
LETRAS_CLAVE = {"52": "S", "72": "O", "69": "L", "48": "E"}     # la letra que deja cada puzle al resolverse
ORDEN_CLAVE = ["52", "72", "69", "48"]                          # pigmentos, poleas, mastermind y caballo


def vigenere(claro, clave):
    return "".join(ABC[(ABC.index(c) + ABC.index(clave[i % len(clave)])) % 26] for i, c in enumerate(claro))


CIFRADO = {"cifrado": vigenere(CLARO, CLAVE), "claro": CLARO, "clave": CLAVE, "letras": LETRAS_CLAVE, "orden": ORDEN_CLAVE}
assert "".join(LETRAS_CLAVE[c] for c in ORDEN_CLAVE) == CLAVE


_CACHE = os.path.join(AQUI, "instancias_florencia.json")
if os.path.exists(_CACHE) and __name__ != "__main__":
    # los generadores tardan: al importar se leen las instancias ya comprobadas (se regeneran con `python herramientas/instancias_florencia.py`)
    _C = json.load(open(_CACHE, encoding="utf-8"))
    ESCITALA, PERSPECTIVA, FUTOSHIKI, CABALLO, PIGMENTOS, ENGRANAJES, VIGILANTES, MASTERMIND, HIDATO, POLEAS = (
        _C[k] for k in ("escitala", "perspectiva", "futoshiki", "caballo", "pigmentos", "engranajes", "vigilantes", "mastermind", "hidato", "poleas"))
else:
    ESCITALA = escitala()
    PERSPECTIVA = perspectiva()
    FUTOSHIKI = futoshiki()
    CABALLO = caballo()
    PIGMENTOS = pigmentos()
    ENGRANAJES = engranajes()
    VIGILANTES = vigilantes()
    MASTERMIND = mastermind()
    HIDATO = hidato()
    POLEAS = poleas()

TODO = {"escitala": ESCITALA, "perspectiva": PERSPECTIVA, "futoshiki": FUTOSHIKI, "caballo": CABALLO, "pigmentos": PIGMENTOS, "engranajes": ENGRANAJES,
        "vigilantes": VIGILANTES, "mastermind": MASTERMIND, "hidato": HIDATO, "poleas": POLEAS, "cifrado": CIFRADO}

if __name__ == "__main__":
    for k, v in TODO.items():
        print(k, json.dumps(v, ensure_ascii=False)[:230])
    with open(os.path.join(AQUI, "instancias_florencia.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(TODO, f, ensure_ascii=False, indent=1)
    print("OK")

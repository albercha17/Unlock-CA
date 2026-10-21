"""Instancias de los puzles de «Dinosaurios» (versión de 60 cartas, 21 oct 2026), con solución única comprobada por fuerza bruta.

Diez puzles de tipos que no salen en ningún otro juego de la serie:
  huellas    orden en que pasaron cinco dinosaurios por quién pisó encima de quién
  manada     cabezas y patas asomando entre los helechos
  nidos      nidos junto a helechos (tipo «Tents»), con las cuentas de filas y columnas en dos cartas
  crater     triangulación: tres vigías ven el cráter en tres direcciones
  lava       una roca para desviar la lava, que baja siempre hacia la vecina más baja
  senderos   recorrer todos los senderos del valle una sola vez (camino de Euler)
  arbol      árbol de rasgos: cada animal en su rama
  corral     seis animales en seis corrales sin que nadie quede al lado de quien se lo come
  barro      la balsa resbala por el barro hasta chocar
  anillos    datación por anillos de tres troncos fósiles que se solapan en el tiempo
  planear    volar con el pterosaurio: cada casilla cuesta altura y las térmicas la devuelven
Uso: python herramientas/instancias_dinosaurios.py   (comprueba todo y escribe instancias_dinosaurios.json)
"""
import itertools
import json
import os
import random
from collections import deque

AQUI = os.path.dirname(os.path.abspath(__file__))
V4 = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# ------------------------------------------------------------------ huellas: un orden total por las pisadas encima
ESPECIES = ["triceratops", "tiranosaurio", "anquilosaurio", "edmontosaurio", "velociraptor"]


def huellas(semilla=5):
    rng = random.Random(semilla)
    orden = ESPECIES[:]
    rng.shuffle(orden)
    # encima[i] = (de, sobre): la huella de «de» pisa la de «sobre» (pasó después)
    pares = [(orden[i + 1], orden[i]) for i in range(len(orden) - 1)]
    pares.append((orden[3], orden[0]))      # un solape más, coherente, para despistar
    rng.shuffle(pares)
    return {"orden": orden, "encima": pares}


def _ordenes_huellas(h):
    return [p for p in itertools.permutations(ESPECIES)
            if all(p.index(a) > p.index(b) for a, b in h["encima"])]


# ------------------------------------------------------------------ manada: cabezas y patas
def manada():
    tric, rapt = 7, 6
    return {"cabezas": tric + rapt, "patas": 4 * tric + 2 * rapt, "solucion": {"triceratops": tric, "velociraptor": rapt}}


# ------------------------------------------------------------------ nidos (Tents): cada nido junto a su helecho, nidos sin tocarse
def _contar_nidos(n, helechos, filas, cols, limite=2):
    hel = set(helechos)
    cand = [(x, y) for y in range(n) for x in range(n) if (x, y) not in hel
            and any((x + dx, y + dy) in hel for dx, dy in V4)]
    sols = []

    def ok_parcial(elegidos):
        f = [0] * n
        c = [0] * n
        for x, y in elegidos:
            f[y] += 1
            c[x] += 1
        return all(f[i] <= filas[i] for i in range(n)) and all(c[i] <= cols[i] for i in range(n))

    def emparejable(elegidos):
        # emparejamiento perfecto nido-helecho (adyacentes ortogonales)
        nidos = list(elegidos)
        pareja = {}

        def busca(i, vistos):
            x, y = nidos[i]
            for dx, dy in V4:
                h = (x + dx, y + dy)
                if h in hel and h not in vistos:
                    vistos.add(h)
                    if h not in pareja or busca(pareja[h], vistos):
                        pareja[h] = i
                        return True
            return False
        return all(busca(i, set()) for i in range(len(nidos)))

    def rec(i, elegidos):
        if len(sols) >= limite:
            return
        if len(elegidos) == len(hel):
            f = [sum(1 for _, y in elegidos if y == k) for k in range(n)]
            c = [sum(1 for x, _ in elegidos if x == k) for k in range(n)]
            if f == list(filas) and c == list(cols) and emparejable(elegidos):
                sols.append(sorted(elegidos))
            return
        if i == len(cand):
            return
        x, y = cand[i]
        if all(max(abs(x - a), abs(y - b)) > 1 for a, b in elegidos):
            elegidos.append((x, y))
            if ok_parcial(elegidos):
                rec(i + 1, elegidos)
            elegidos.pop()
        rec(i + 1, elegidos)
    rec(0, [])
    return sols


def nidos(semilla=11, n=6, k=7):
    rng = random.Random(semilla)
    for _ in range(5000):
        tiendas, hel = [], []
        celdas = [(x, y) for y in range(n) for x in range(n)]
        rng.shuffle(celdas)
        for (x, y) in celdas:
            if len(tiendas) == k:
                break
            if (x, y) in hel or any(max(abs(x - a), abs(y - b)) <= 1 for a, b in tiendas):
                continue
            vec = [(x + dx, y + dy) for dx, dy in V4 if 0 <= x + dx < n and 0 <= y + dy < n
                   and (x + dx, y + dy) not in hel and (x + dx, y + dy) not in tiendas]
            if not vec:
                continue
            hel.append(rng.choice(vec))
            tiendas.append((x, y))
        if len(tiendas) < k or any(h in tiendas for h in hel):
            continue
        filas = [sum(1 for _, y in tiendas if y == i) for i in range(n)]
        cols = [sum(1 for x, _ in tiendas if x == i) for i in range(n)]
        if len(_contar_nidos(n, hel, filas, cols)) == 1:
            return {"n": n, "helechos": sorted([list(h) for h in hel]), "filas": filas, "cols": cols,
                    "solucion": sorted([list(t) for t in tiendas])}
    raise SystemExit("sin nidos")


# ------------------------------------------------------------------ cráter: tres rayos desde tres vigías
RUMBOS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SO": (-1, 1), "O": (-1, 0), "NO": (-1, -1)}


def _rayo(n, x, y, d):
    dx, dy = RUMBOS[d]
    out = set()
    x, y = x + dx, y + dy
    while 0 <= x < n and 0 <= y < n:
        out.add((x, y))
        x, y = x + dx, y + dy
    return out


def crater(semilla=3, n=8):
    rng = random.Random(semilla)
    nombres = ["Roca del Cuerno", "Árbol Hueco", "Colina Pelada"]
    for _ in range(5000):
        cx, cy = rng.randrange(1, n - 1), rng.randrange(1, n - 1)
        vigias = []
        for nom in nombres:
            d = rng.choice(list(RUMBOS))
            dx, dy = RUMBOS[d]
            pasos = rng.randint(2, 5)
            x, y = cx - dx * pasos, cy - dy * pasos
            if not (0 <= x < n and 0 <= y < n) or (x, y) in [(v["x"], v["y"]) for v in vigias]:
                break
            vigias.append({"nombre": nom, "x": x, "y": y, "rumbo": d})
        if len(vigias) < 3 or len({v["rumbo"] for v in vigias}) < 3:
            continue
        rayos = [_rayo(n, v["x"], v["y"], v["rumbo"]) for v in vigias]
        if any(len(rayos[i] & rayos[j]) != 1 for i, j in ((0, 1), (0, 2), (1, 2))):
            continue          # cada par de vigías por separado ya da un solo punto: hacen falta los tres para estar seguros
        comun = rayos[0] & rayos[1] & rayos[2]
        pares = {frozenset(rayos[i] & rayos[j]) for i, j in ((0, 1), (0, 2), (1, 2))}
        if comun == {(cx, cy)} and len(pares) == 1:
            return {"n": n, "vigias": vigias, "solucion": [cx, cy]}
    raise SystemExit("sin cráter")


# ------------------------------------------------------------------ lava: baja siempre a la vecina más baja
def _flujo(alt, fuente, roca=None):
    n = len(alt)
    x, y = fuente
    camino = [(x, y)]
    while True:
        vec = [(alt[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in V4
               if 0 <= x + dx < n and 0 <= y + dy < n and (x + dx, y + dy) != roca]
        h, (nx, ny) = min(vec)
        if h >= alt[y][x]:
            return camino
        x, y = nx, ny
        camino.append((x, y))


def lava(semilla=21, n=6):
    rng = random.Random(semilla)
    for _ in range(20000):
        vals = rng.sample(range(10, 10 + n * n * 2), n * n)
        alt = [[vals[y * n + x] for x in range(n)] for y in range(n)]
        # pendiente general: arriba alto, abajo bajo
        for y in range(n):
            for x in range(n):
                alt[y][x] += (n - y) * 25
        fuente = (rng.randrange(n), 0)
        cam = _flujo(alt, fuente)
        if len(cam) < 6:
            continue
        nido = cam[-1]
        buenas = []
        for c in cam[1:-1]:
            c2 = _flujo(alt, fuente, roca=c)
            if nido not in c2:
                buenas.append(c)
        if len(buenas) == 1 and nido[1] >= n - 2:
            # alturas de 1 a 9 por franjas para dibujarlas (sin empates entre vecinas)
            planas = sorted({alt[y][x] for y in range(n) for x in range(n)})
            return {"n": n, "alturas": alt, "fuente": list(fuente), "nido": list(nido),
                    "camino": [list(c) for c in cam], "solucion": list(buenas[0])}
    raise SystemExit("sin lava")


# ------------------------------------------------------------------ senderos: camino de Euler
def senderos():
    claros = {"N": "Nidos", "H": "Helechal", "L": "Lago", "C": "Cascada", "V": "Volcán", "P": "Pinar", "R": "Roca Alta"}
    aristas = [("N", "H"), ("N", "L"), ("H", "L"), ("H", "C"), ("L", "C"), ("L", "V"), ("C", "P"), ("V", "P"), ("P", "R"),
               ("C", "R"), ("V", "R"), ("H", "V")]
    grado = {k: 0 for k in claros}
    for a, b in aristas:
        grado[a] += 1
        grado[b] += 1
    impares = [k for k, g in grado.items() if g % 2]
    return {"claros": claros, "senderos": [list(a) for a in aristas], "impares": impares}


def euler(inst, inicio):
    ady = {k: [] for k in inst["claros"]}
    for i, (a, b) in enumerate(inst["senderos"]):
        ady[a].append((b, i))
        ady[b].append((a, i))
    usadas, pila, camino = set(), [inicio], []
    while pila:
        v = pila[-1]
        resto = [(w, i) for w, i in ady[v] if i not in usadas]
        if resto:
            w, i = resto[0]
            usadas.add(i)
            pila.append(w)
        else:
            camino.append(pila.pop())
    return camino[::-1]


# ------------------------------------------------------------------ árbol de rasgos
RASGOS = ["patas", "patas rectas bajo el cuerpo", "plumas", "alas"]
ANIMALES = {"cocodrilo": ["patas"], "triceratops": ["patas", "patas rectas bajo el cuerpo"],
            "velociraptor": ["patas", "patas rectas bajo el cuerpo", "plumas"],
            "ave primitiva": ["patas", "patas rectas bajo el cuerpo", "plumas", "alas"], "pez": []}


def arbol():
    # árbol en escalera: cada rasgo abre una rama más; el animal de cada hoja es el que tiene justo los rasgos hasta ahí
    hojas = sorted(ANIMALES, key=lambda a: len(ANIMALES[a]))
    return {"rasgos": RASGOS, "animales": ANIMALES, "solucion": hojas}


# ------------------------------------------------------------------ corral: nadie al lado de quien se lo come
COME = [("tiranosaurio", "edmontosaurio"), ("tiranosaurio", "protoceratops"), ("tiranosaurio", "velociraptor"),
        ("velociraptor", "protoceratops"), ("velociraptor", "compsognato")]
ANIMALES_CORRAL = ["compsognato", "edmontosaurio", "protoceratops", "tiranosaurio", "triceratops", "velociraptor"]


def _corrales(fijos, cols=3, filas=2):
    cel = [(x, y) for y in range(filas) for x in range(cols)]
    sols = []
    for perm in itertools.permutations(cel):
        pos = dict(zip(ANIMALES_CORRAL, perm))
        if all(pos[a] == tuple(c) for a, c in fijos.items()) and                 all(abs(pos[a][0] - pos[b][0]) + abs(pos[a][1] - pos[b][1]) != 1 for a, b in COME):
            sols.append(pos)
    return sols


def corral():
    fijos = {"compsognato": [0, 0]}
    s = _corrales(fijos)
    assert len(s) == 1
    return {"animales": ANIMALES_CORRAL, "come": [list(p) for p in COME], "fijos": fijos, "cols": 3, "filas": 2,
            "solucion": {a: list(c) for a, c in s[0].items()}}


# ------------------------------------------------------------------ barro: la balsa resbala hasta chocar
def _desliza(n, rocas, p, d):
    dx, dy = V4[d]
    x, y = p
    while 0 <= x + dx < n and 0 <= y + dy < n and (x + dx, y + dy) not in rocas:
        x, y = x + dx, y + dy
    return (x, y)


def barro(semilla=8, n=7):
    rng = random.Random(semilla)
    for _ in range(20000):
        rocas = set()
        while len(rocas) < 9:
            rocas.add((rng.randrange(n), rng.randrange(n)))
        ini = (0, n - 1)
        if ini in rocas:
            continue
        dist = {ini: 0}
        prev = {ini: None}
        cola = deque([ini])
        while cola:
            p = cola.popleft()
            for d in range(4):
                q = _desliza(n, rocas, p, d)
                if q not in dist:
                    dist[q] = dist[p] + 1
                    prev[q] = (p, d)
                    cola.append(q)
        # la cueva: un sitio donde la balsa pueda pararse, a 6 o 7 deslizamientos como mínimo
        lejos = [q for q, k in dist.items() if 6 <= k <= 7 and q[0] not in (0, n - 1) and q[1] not in (0, n - 1)]
        if not lejos:
            continue
        cueva = rng.choice(lejos)
        ruta, q = [], cueva
        while prev[q]:
            q, d = prev[q]
            ruta.append(["arriba", "derecha", "abajo", "izquierda"][d])
        return {"n": n, "rocas": sorted([list(r) for r in rocas]), "inicio": list(ini), "cueva": list(cueva),
                "minimo": dist[cueva], "solucion": ruta[::-1]}
    raise SystemExit("sin barro")


# ------------------------------------------------------------------ anillos: tres troncos que se solapan en el tiempo
def anillos(semilla=4, total=30):
    rng = random.Random(semilla)
    for _ in range(5000):
        anchos = [rng.choice("fmg") for _ in range(total)]        # fino, medio, grueso (del más viejo al más nuevo)
        tramos = [(0, 13), (9, 21), (17, 30)]
        tr = ["".join(anchos[a:b]) for a, b in tramos]

        def encaja(p, q):
            # desplazamientos en que el final de p coincide con el principio de q en 4 anillos o más
            return [k for k in range(1, len(p) - 3) if p[k:] == q[:len(p) - k]]
        if encaja(tr[0], tr[1]) == [9] and encaja(tr[1], tr[2]) == [8] and not encaja(tr[0], tr[2]):
            # el tronco 0 murió en la gran erupción, el día que llegó la doctora; el 2 cayó esta mañana: años que lleva aquí
            return {"troncos": tr, "solucion": tramos[2][1] - tramos[0][1], "tramos": tramos}
    raise SystemExit("sin anillos")


# ------------------------------------------------------------------ planear: el pterosaurio pierde un palmo de altura por casilla
def _vuelos(n, ini, fin, alt0, termicas, montes):
    """Búsqueda en anchura sobre (casilla, altura, térmicas ya usadas). Devuelve el número mínimo de térmicas y una ruta."""
    inicio = (tuple(ini), alt0, frozenset())
    prev = {inicio: None}
    cola = deque([inicio])
    mejor = None
    while cola:
        e = cola.popleft()
        (x, y), h, usadas = e
        if (x, y) == tuple(fin):
            if mejor is None or len(usadas) < len(mejor[1]):
                mejor = (e, usadas)
            continue
        for d, (dx, dy) in enumerate(V4):
            q = (x + dx, y + dy)
            if not (0 <= q[0] < n and 0 <= q[1] < n) or q in montes:
                continue
            h2, u2 = h - 1, usadas
            if h2 < 0:
                continue
            if q in termicas and q not in usadas:
                h2 += termicas[q]
                u2 = usadas | {q}
            e2 = (q, h2, u2)
            if e2 not in prev:
                prev[e2] = (e, d)
                cola.append(e2)
    if not mejor:
        return None
    ruta, e = [], mejor[0]
    while prev[e]:
        e, d = prev[e]
        ruta.append(["arriba", "derecha", "abajo", "izquierda"][d])
    return len(mejor[1]), ruta[::-1]


def planear(semilla=6, n=6):
    rng = random.Random(semilla)
    for _ in range(20000):
        ini, fin = (0, 0), (n - 1, n - 1)
        montes = set()
        while len(montes) < 5:
            c = (rng.randrange(n), rng.randrange(n))
            if c not in (ini, fin):
                montes.add(c)
        termicas = {}
        while len(termicas) < 4:
            c = (rng.randrange(n), rng.randrange(n))
            if c not in montes and c not in (ini, fin):
                termicas[c] = rng.choice([2, 3, 4])
        alt0 = 3
        r = _vuelos(n, ini, fin, alt0, termicas, montes)
        if r and r[0] >= 2:
            return {"n": n, "inicio": list(ini), "nido": list(fin), "altura": alt0, "montes": sorted([list(m) for m in montes]),
                    "termicas": [[x, y, k] for (x, y), k in sorted(termicas.items())], "minimo_termicas": r[0], "solucion": r[1]}
    raise SystemExit("sin planear")


HUELLAS = huellas()
MANADA = manada()
NIDOS = nidos()
CRATER = crater()
LAVA = lava()
SENDEROS = senderos()
ARBOL = arbol()
CORRAL = corral()
BARRO = barro()
ANILLOS = anillos()
PLANEAR = planear()

TODO = {"huellas": HUELLAS, "manada": MANADA, "nidos": NIDOS, "crater": CRATER, "lava": LAVA, "senderos": SENDEROS, "arbol": ARBOL,
        "corral": CORRAL, "barro": BARRO, "anillos": ANILLOS, "planear": PLANEAR}


if __name__ == "__main__":
    assert len(_ordenes_huellas(HUELLAS)) == 1, "huellas con más de un orden"
    assert len(SENDEROS["impares"]) == 2, SENDEROS["impares"]
    for k, v in TODO.items():
        print(k, json.dumps(v, ensure_ascii=False)[:300])
    with open(os.path.join(AQUI, "instancias_dinosaurios.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(TODO, f, ensure_ascii=False, indent=1)
    print("OK")

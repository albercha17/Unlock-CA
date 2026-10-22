"""Instancias de «Mar de las Brumas, 1715» (piratas), versión de 60 cartas (22 oct 2026), buscadas con semilla fija y comprobadas por fuerza bruta.
Escribe instancias_piratas.json, que leen piratas.py (las láminas de las cartas), datos_piratas.py (pistas y manual), los minijuegos (copiados como
constantes) y solvers_piratas.py.

Once puzles; los tres primeros siguen siendo las cartas que se PLIEGAN (fold-in) y el resto no se parece a ningún otro juego de la serie:
  bitacora     las guardias y campanadas de a bordo: la hora de tres anotaciones y el tiempo entre dos
  persecucion  la fragata persigue a La Gaviota con una regla fija (mapa de aguas en dos láminas); BFS hasta el banco de niebla
  cielo        la constelación de la Calavera, girada y más pequeña entre treinta y seis estrellas numeradas (cielo en dos láminas); única
  suelo        el testamento plegado da cuatro símbolos; el suelo de la cueva (dos láminas) se cruza por losas vecinas que los siguen; camino único
  canon        la tabla de tiro: tres barcos enemigos, cargas de pólvora y elevaciones; alcance exacto con viento y pólvora limitada; solución única
  botin        el reparto del botín entre siete piratas (inducción hacia atrás, el Código de la Hermandad)
  mareas       el calado y las barras de arena: la hora de salida única para cruzar tres barras con la marea
  rumbo        la carta náutica plegada da el rumbo verdadero con arrecifes en forma de cifras; el cuaderno del piloto, el desvío de la aguja
  pesas        la balanza con cuatro pesas (1, 3, 9 y 27) que se pueden poner en los dos platillos (ternario equilibrado)
  gruta        el mapa de la isla plegado por los dos lados: camino de la palmera a la X; la gruta es la misma rejilla girada
  isla         metapuzle: cinco rumbos de rosa de los vientos con las distancias que dejan otros puzles; casilla final de la carta
Uso (desde la raíz del repo):  python herramientas/instancias_piratas.py
"""
import itertools
import json
import math
import os
import random
from collections import deque

AQUI = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ cifras de arrecife (siete segmentos partidos por el pliegue)
# Cada cifra se parte en dos mitades por el pliegue vertical: la izquierda lleva los verticales f y e y la mitad izquierda de a, g y d;
# la derecha, b y c y la otra mitad de a, g y d. Desplegada, junto a cada mitad verdadera hay una mitad falsa: se leen otras cifras.
SEGMENTOS = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcdfg"}


def mitades(c):
    s = set(SEGMENTOS[c])
    horiz = "".join(x for x in "agd" if x in s)
    return horiz, "".join(x for x in "fe" if x in s), "".join(x for x in "bc" if x in s)


def cifra_de(horiz, izq, der):
    for c, segs in SEGMENTOS.items():
        if mitades(c) == (horiz, izq, der):
            return c
    return None


def senuelos(c):
    """Cifras falsas que se leen desplegada: (mitad izquierda verdadera + derecha falsa, izquierda falsa + derecha verdadera)."""
    h, i, d = mitades(c)
    izq_falsas = [cifra_de(h, i, d2) for d2 in ("", "b", "c", "bc") if d2 != d and cifra_de(h, i, d2)]
    der_falsas = [cifra_de(h, i2, d) for i2 in ("", "f", "e", "fe") if i2 != i and cifra_de(h, i2, d)]
    return izq_falsas, der_falsas


def rumbo():
    verdadero, desvio = "86", 25
    col_izq, col_der = [], []
    for c in verdadero:
        iz, de = senuelos(c)
        assert iz and de, f"la cifra {c} no admite señuelos"
        col_izq.append(iz[0])
        col_der.append(de[-1])
    falsos = ["".join(col_izq), "".join(col_der)]
    aguja = int(verdadero) + desvio
    return {"carta": verdadero, "desvio": desvio, "aguja": aguja, "senuelos": falsos,
            "mitades_falsas": {"derechas": [mitades(c)[2] for c in col_izq], "izquierdas": [mitades(c)[1] for c in col_der]}}


# ------------------------------------------------------------------ la persecución (la fragata, como el Minotauro de «Teseo y el Minotauro»)
MOV = {"arriba": (0, -1), "abajo": (0, 1), "izquierda": (-1, 0), "derecha": (1, 0), "esperar": (0, 0)}


def paso_fragata(f, b, rocas, ancho, alto):
    """Un paso de la fragata (la ordenanza): si puede acercarse en horizontal, va en horizontal; si no, si puede acercarse en vertical, va en
    vertical; si no, se queda. Las rocas no se cruzan."""
    libre = lambda c: c not in rocas and 0 <= c[0] < ancho and 0 <= c[1] < alto
    if b[0] != f[0]:
        c = (f[0] + (1 if b[0] > f[0] else -1), f[1])
        if libre(c):
            return c
    if b[1] != f[1]:
        c = (f[0], f[1] + (1 if b[1] > f[1] else -1))
        if libre(c):
            return c
    return f


def turno(b, f, mov, rocas, ancho, alto):
    """Mueve La Gaviota y después la fragata dos pasos. Devuelve (barco, fragata, atrapados) o None si el movimiento no vale."""
    dx, dy = MOV[mov]
    nb = (b[0] + dx, b[1] + dy)
    if nb in rocas or not (0 <= nb[0] < ancho and 0 <= nb[1] < alto) or nb == f:
        return None
    for _ in range(2):
        f = paso_fragata(f, nb, rocas, ancho, alto)
        if f == nb:
            return nb, f, True
    return nb, f, False


def resolver_persecucion(rocas, barco, fragata, niebla, ancho, alto):
    """BFS: la lista de movimientos más corta que lleva La Gaviota a la niebla sin que la alcance la fragata."""
    inicio = (barco, fragata)
    previo = {inicio: None}
    cola = deque([inicio])
    while cola:
        e = cola.popleft()
        if e[0] == niebla:
            camino = []
            while previo[e]:
                e, m = previo[e]
                camino.append(m)
            return camino[::-1]
        for m in MOV:
            r = turno(e[0], e[1], m, rocas, ancho, alto)
            if not r or r[2]:
                continue
            n = (r[0], r[1])
            if n not in previo:
                previo[n] = (e, m)
                cola.append(n)
    return None


def persecucion():
    ancho, alto = 7, 7
    rng = random.Random(1716)
    mejor = None
    for _ in range(8000):
        celdas = [(x, y) for y in range(alto) for x in range(ancho)]
        rng.shuffle(celdas)
        rocas = set(celdas[:rng.randint(9, 11)])
        libres = [c for c in celdas if c not in rocas]
        barco, fragata, niebla = libres[0], libres[1], libres[2]
        if abs(barco[0] - niebla[0]) + abs(barco[1] - niebla[1]) < 7 or abs(barco[0] - fragata[0]) + abs(barco[1] - fragata[1]) < 3:
            continue
        sol = resolver_persecucion(rocas, barco, fragata, niebla, ancho, alto)
        if not sol or not 12 <= len(sol) <= 20:
            continue
        directo = resolver_persecucion(rocas, barco, (-9, -9), niebla, ancho, alto)
        if len(sol) - len(directo) < 4:                        # que no valga ir directo: hay que engañar a la fragata
            continue
        clave = (len(sol) - len(directo), "esperar" in sol, len(sol))
        if mejor is None or clave > mejor[0]:
            mejor = (clave, dict(ancho=ancho, alto=alto, rocas=sorted([list(c) for c in rocas]), barco=list(barco), fragata=list(fragata),
                                 niebla=list(niebla), solucion=sol, directo=len(directo)))
    assert mejor, "no se encontró una persecución"
    return mejor[1]


# ------------------------------------------------------------------ el cielo (constelación girada y más pequeña entre estrellas numeradas)
FIGURA = [(0, -46), (-34, -20), (34, -20), (-22, 26), (22, 26), (0, 56)]          # la Calavera de la carta celeste
ENLACES = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5), (1, 2)]


def _ocurrencias(estrellas, tol=7):
    """Cuántas veces aparece la figura (con cualquier giro y tamaño) entre las estrellas."""
    f0 = FIGURA[0]
    n = 0
    for i, a in enumerate(estrellas):
        for j, b in enumerate(estrellas):
            if i == j:
                continue
            fx, fy = FIGURA[1][0] - f0[0], FIGURA[1][1] - f0[1]
            esc = math.dist(a, b) / math.hypot(fx, fy)
            if not 0.4 <= esc <= 3.0:
                continue
            ang = math.atan2(b[1] - a[1], b[0] - a[0]) - math.atan2(fy, fx)
            ok = True
            for x, y in FIGURA:
                dx, dy = (x - f0[0]) * esc, (y - f0[1]) * esc
                p = (a[0] + dx * math.cos(ang) - dy * math.sin(ang), a[1] + dx * math.sin(ang) + dy * math.cos(ang))
                if min(math.dist(p, q) for q in estrellas) > tol:
                    ok = False
                    break
            n += ok
    return n


def cielo():
    """La Calavera aparece girada 120° y a escala 2 entre treinta y seis estrellas numeradas del cielo de la carta (1260 × 700 repartidas en
    las dos láminas). Se comprueba que no hay ninguna otra figura igual."""
    for sem in range(1, 4000):
        rng = random.Random(sem)
        giro = math.radians(120)
        cx, cy = rng.randint(200, 1060), rng.randint(280, 560)
        estrellas = [(round(cx + 2.0 * (x * math.cos(giro) - y * math.sin(giro))), round(cy + 2.0 * (x * math.sin(giro) + y * math.cos(giro)))) for x, y in FIGURA]
        if any(abs(x - 630) < 36 or not 50 <= x <= 1210 or not 150 <= y <= 780 for x, y in estrellas):
            continue
        while len(estrellas) < 36:
            p = (rng.randint(50, 1210), rng.randint(150, 780))
            if abs(p[0] - 630) >= 36 and all(math.dist(p, q) >= 70 for q in estrellas):
                estrellas.append(p)
        if _ocurrencias(estrellas) != 1:
            continue
        orden = list(range(len(estrellas)))
        rng.shuffle(orden)
        estrellas = [estrellas[k] for k in orden]
        solucion = sorted(orden.index(k) + 1 for k in range(6))         # los números de las seis estrellas (1 a 36)
        return {"figura": FIGURA, "enlaces": ENLACES, "giro": 120, "escala": 2.0, "estrellas": [list(e) for e in estrellas], "solucion": solucion}
    raise SystemExit("sin cielo")


# ------------------------------------------------------------------ el suelo de la cueva (camino que sigue en bucle los símbolos del testamento)
SIMBOLOS = ["ancla", "calavera", "estrella", "luna", "llave", "corona", "pez", "campana", "espada"]


def caminos_suelo(rej, ciclo, n):
    """Caminos que entran por la fila de abajo pisando ciclo[0], van a losas vecinas siguiendo el ciclo en bucle y llegan a la fila de arriba
    (se para al encontrar dos)."""
    sig = {ciclo[i]: ciclo[(i + 1) % len(ciclo)] for i in range(len(ciclo))}
    out = []

    def dfs(c, camino):
        x, y = c
        if y == 0:
            out.append(list(camino))
            return
        for dx, dy in ((0, -1), (1, 0), (-1, 0), (0, 1)):
            nx, ny = x + dx, y + dy
            if len(out) < 2 and 0 <= nx < n and 0 <= ny < n and (nx, ny) not in camino and rej[ny][nx] == sig[rej[y][x]]:
                camino.append((nx, ny))
                dfs((nx, ny), camino)
                camino.pop()
    for x in range(n):
        if rej[n - 1][x] == ciclo[0]:
            dfs((x, n - 1), [(x, n - 1)])
    return out


def suelo():
    n = 6
    ciclo = ["luna", "llave", "calavera", "corona"]
    otros = [s for s in SIMBOLOS if s not in ciclo]
    rng = random.Random(79)
    for _ in range(200000):
        x = rng.randrange(n)
        camino = [(x, n - 1)]
        while camino[-1][1] > 0 and len(camino) < 17:
            cx, cy = camino[-1]
            c = rng.choice([(cx, cy - 1), (cx, cy - 1)] + [(cx + d, cy) for d in (-1, 1) if 0 <= cx + d < n])
            if c in camino:
                if all(o in camino for o in [(cx, cy - 1)] + [(cx + d, cy) for d in (-1, 1) if 0 <= cx + d < n]):
                    break
                continue
            camino.append(c)
        if camino[-1][1] != 0 or len(camino) < 12:
            continue
        rej = [[None] * n for _ in range(n)]
        for k, (cx, cy) in enumerate(camino):
            rej[cy][cx] = ciclo[k % 4]
        for y in range(n):
            for xx in range(n):
                if rej[y][xx] is None:
                    rej[y][xx] = rng.choice(ciclo + ciclo + otros)
        sols = caminos_suelo(rej, ciclo, n)
        if len(sols) == 1 and sols[0] == camino:
            return {"n": n, "ciclo": ciclo, "suelo": rej, "camino": [list(c) for c in camino],
                    "falsas_der": ["ancla", "estrella", "pez", "campana"], "falsas_izq": ["pez", "campana", "espada", "ancla"]}
    raise SystemExit("no se encontró un suelo con camino único")


# ------------------------------------------------------------------ ruta del mapa (candado de flechas)
FLECHA = {"derecha": (1, 0), "izquierda": (-1, 0), "abajo": (0, 1), "arriba": (0, -1)}


def ruta():
    """Ruta en la rejilla PLEGADA (6 columnas x 8 filas). El pliegue vertical esconde 2 columnas entre las columnas 2 y 3 (índice 0) y el
    horizontal 2 filas entre las filas 3 y 4. Desplegado, cada cruce de un pliegue añade dos pasos de más."""
    cols, filas, corte_c, corte_f, oculto = 6, 8, 3, 4, 2
    inicio = (0, 1)
    movs = ["derecha", "derecha", "derecha", "derecha", "abajo", "abajo", "abajo", "abajo", "izquierda", "izquierda", "abajo"]
    p = inicio
    celdas = [p]
    for m in movs:
        p = (p[0] + FLECHA[m][0], p[1] + FLECHA[m][1])
        assert 0 <= p[0] < cols and 0 <= p[1] < filas
        celdas.append(p)
    assert len(set(celdas)) == len(celdas)
    desplegada = []
    for a, b, m in zip(celdas, celdas[1:], movs):
        cruza_v = m in ("derecha", "izquierda") and {a[0], b[0]} == {corte_c - 1, corte_c}
        cruza_h = m in ("abajo", "arriba") and {a[1], b[1]} == {corte_f - 1, corte_f}
        desplegada += [m] * (1 + (oculto if (cruza_v or cruza_h) else 0))
    return {"cols": cols, "filas": filas, "corte_col": corte_c, "corte_fila": corte_f, "ocultas": oculto, "inicio": list(inicio),
            "movimientos": movs, "celdas": [list(c) for c in celdas], "desplegada": desplegada}


# Pliegues de las cartas plegables, en píxeles de la lámina de 630 x 882: la franja [x0, x1) (o [y0, y1)) queda escondida detrás
# al plegar la carta en acordeón hasta que la línea A toque la B (y la C, la D). El Modo PC los usa como fracciones (campo `plegado`).
PLIEGUES = {
    "66": {"x": [235, 395]},            # la carta náutica
    "53": {"x": [240, 390]},            # el testamento
    "75": {"x": [251, 379], "y": [372, 500]},          # el mapa de la isla
}


# ------------------------------------------------------------------ la bitácora (guardias y campanadas)
GUARDIAS = [("Media", 0), ("Alba", 4), ("Mañana", 8), ("Tarde", 12), ("Vísperas", 16), ("Primera", 20)]


def hora_de(guardia, campanadas):
    """Hora (en minutos desde las 0:00) a la que suena la campanada número `campanadas` de la guardia dada: una cada media hora."""
    ini = dict(GUARDIAS)[guardia] * 60
    return ini + campanadas * 30


def bitacora():
    anotaciones = [("Avistamos la isla", "Alba", 5), ("Echamos el ancla", "Mañana", 3), ("La marea nos deja en seco", "Tarde", 6)]
    t = [hora_de(g, c) for _, g, c in anotaciones]
    return {"guardias": [list(g) for g in GUARDIAS], "anotaciones": [list(a) for a in anotaciones], "minutos": t,
            "pregunta": [0, 2], "entre": t[2] - t[0], "entre_horas": (t[2] - t[0]) // 60, "entre_min": (t[2] - t[0]) % 60}


# ------------------------------------------------------------------ la tabla de tiro del cañón
def canon(semilla=1):
    for sem in range(semilla, semilla + 20000):
        rng = random.Random(sem)
        base = sorted(rng.sample(range(2, 15), 6))                    # alcance, en cables, de cada carga (1 a 6 sacos)
        corr = [rng.randint(-3, 5) for _ in range(5)]                 # corrección de cada elevación (0° a 20°)
        if len(set(corr)) < 5:
            continue
        barcos = [{"dist": rng.randint(4, 18), "viento": rng.choice([-2, -1, 0, 1, 2])} for _ in range(3)]
        limite = rng.randint(8, 12)
        opciones = []
        for b in barcos:
            op = [(c, a) for c in range(6) for a in range(5) if base[c] + corr[a] + b["viento"] == b["dist"]]
            opciones.append(op)
        if any(len(o) == 0 for o in opciones):
            continue
        sols = []
        for combo in itertools.product(*opciones):
            cargas = [c for c, _ in combo]
            if len(set(cargas)) == 3 and sum(c + 1 for c in cargas) <= limite:
                sols.append(combo)
        if len(sols) == 1 and all(len(o) >= 2 for o in opciones):
            return {"base": base, "corr": corr, "barcos": barcos, "limite": limite, "elevaciones": [0, 5, 10, 15, 20],
                    "solucion": [list(x) for x in sols[0]]}
    raise SystemExit("sin cañón")


# ------------------------------------------------------------------ el botín (reparto entre piratas, inducción hacia atrás)
def reparto(n, monedas):
    """Reparto que propone el capitán entre n piratas: cada pirata (en orden de antigüedad, 0 es el capitán) vota que sí solo si recibe estrictamente
    más de lo que recibiría si el capitán fuera a la mar; para aprobarse hacen falta al menos la mitad de los votos (el empate se aprueba)."""
    sol = {1: [monedas]}
    for m in range(2, n + 1):
        necesarios = (m + 1) // 2
        previo = sol[m - 1]
        costes = sorted((previo[k - 1] + 1, k) for k in range(1, m))
        prop = [0] * m
        for c, k in costes[:necesarios - 1]:
            prop[k] = c
        prop[0] = monedas - sum(prop)
        sol[m] = prop
    return sol


def botin():
    n, monedas = 7, 120
    sol = reparto(n, monedas)
    return {"piratas": n, "monedas": monedas, "solucion": sol[n], "necesarios": (n + 1) // 2, "previo": sol[n - 1]}


# ------------------------------------------------------------------ las mareas y las barras de arena
def mareas(semilla=1):
    for sem in range(semilla, semilla + 20000):
        rng = random.Random(sem)
        fase = rng.uniform(0, 12.4)
        alt = [round(22 + 17 * math.sin(2 * math.pi * (t - fase) / 12.4)) for t in range(24)]
        calado = rng.randint(24, 32)
        barras = [{"fondo": rng.randint(0, 12), "tras": d} for d in (0, 2, 5)]
        # el agua sobre cada barra es la altura de la marea más el fondo propio de la barra; el barco necesita calado
        sol = [t0 for t0 in range(0, 24 - 5) if all(alt[t0 + b["tras"]] + b["fondo"] >= calado for b in barras)]
        if len(sol) == 1:
            return {"alturas": alt, "calado": calado, "barras": barras, "salida": sol[0]}
    raise SystemExit("sin mareas")


# ------------------------------------------------------------------ las pesas (ternario equilibrado)
PESAS = [1, 3, 9, 27]


def ternario(n):
    """Coeficientes (-1, 0 o 1) de las pesas 1, 3, 9, 27 para pesar n: +1 en el platillo contrario al objeto, -1 en el mismo platillo."""
    d = []
    for _ in PESAS:
        r = n % 3
        if r == 2:
            r = -1
        d.append(r)
        n = (n - r) // 3
    assert n == 0
    return d


def pesas():
    objetos = [22, 31, 17]
    sol = [ternario(o) for o in objetos]
    for o, s in zip(objetos, sol):
        assert sum(p * c for p, c in zip(PESAS, s)) == o
    return {"pesas": PESAS, "objetos": objetos, "solucion": sol}


# ------------------------------------------------------------------ la isla (cinco rumbos con las distancias de otros puzles)
RUMBOS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SO": (-1, 1), "O": (-1, 0), "NO": (-1, -1)}
ORDEN_ISLA = ["14", "40", "52", "69", "72"]               # bitácora, cielo, cañón, pesas y gruta
DISTANCIA = {"14": 3, "40": 2, "52": 4, "69": 1, "72": 2}
RUMBOS_ISLA = {"14": "E", "40": "SE", "52": "N", "69": "NE", "72": "O"}


def isla():
    n = 10
    inicio = (1, 7)
    p = inicio
    camino = [p]
    for k in ORDEN_ISLA:
        dx, dy = RUMBOS[RUMBOS_ISLA[k]]
        p = (p[0] + dx * DISTANCIA[k], p[1] + dy * DISTANCIA[k])
        assert 0 <= p[0] < n and 0 <= p[1] < n, p
        camino.append(p)
    return {"n": n, "inicio": list(inicio), "orden": ORDEN_ISLA, "rumbos": [RUMBOS_ISLA[k] for k in ORDEN_ISLA], "distancias": [DISTANCIA[k] for k in ORDEN_ISLA],
            "camino": [list(c) for c in camino], "final": list(camino[-1])}


_CACHE = os.path.join(AQUI, "instancias_piratas.json")
_CLAVES = ("bitacora", "persecucion", "cielo", "losas", "canon", "botin", "mareas", "rumbo", "pesas", "ruta", "isla")


def _funcs():
    return {"bitacora": bitacora, "persecucion": persecucion, "cielo": cielo, "losas": suelo, "canon": canon, "botin": botin, "mareas": mareas, "rumbo": rumbo,
            "pesas": pesas, "ruta": ruta, "isla": isla}


def _construir():
    f = _funcs()
    d = {k: f[k]() for k in _CLAVES}
    d["pliegues"] = PLIEGUES
    d["lamina"] = [630, 882]
    return d


if __name__ != "__main__" and os.path.exists(_CACHE):
    INST = json.load(open(_CACHE, encoding="utf-8"))

if __name__ == "__main__":
    import time
    t0 = time.time()
    res = {}
    for k, f in _funcs().items():
        t = time.time()
        res[k] = f()
        print(f"{k:12s} OK ({time.time() - t:.1f} s)")
    res["pliegues"] = PLIEGUES
    res["lamina"] = [630, 882]
    with open(_CACHE, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("OK", f"{time.time() - t0:.0f} s")

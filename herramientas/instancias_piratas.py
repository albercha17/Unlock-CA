"""Instancias de «Mar de las Brumas, 1715» (piratas), buscadas con semilla fija y comprobadas por fuerza bruta. Escribe instancias_piratas.json,
que leen piratas.py (las láminas de las cartas), datos_piratas.py (pistas y manual), los minijuegos (copiados como constantes) y solvers_piratas.py.

  - rumbo:       la carta náutica plegada (carta 30) enseña el rumbo verdadero con arrecifes en forma de cifras; desplegada, las mitades forman
                 otras cifras (señuelos). El cuaderno del piloto (carta 31) da el desvío de la aguja: rumbo de la aguja = rumbo de la carta + desvío.
  - bodega:      Sokoban de barriles de pólvora (carta 46) con las X en el plano de estiba (carta 40); BFS con la solución más corta.
  - persecucion: la fragata (carta 48) persigue a La Gaviota dos pasos por turno con la regla de la ordenanza (carta 52), como el Minotauro de
                 «Teseo y el Minotauro»; BFS sobre (barco, fragata) hasta el banco de niebla.
  - cielo:       la tapa del cofre (carta 66) con 30 tachuelas-estrella; la constelación de la Calavera (carta 64) aparece una sola vez, girada.
  - losas:       el testamento plegado (carta 76) da cuatro símbolos; el suelo de la cueva (carta 79) se cruza pisando losas vecinas que siguen
                 esos símbolos en bucle; camino único comprobado.
  - ruta:        el mapa de la isla plegado por los dos lados (carta 70): camino de la palmera a la X; la gruta (carta 69) es la misma rejilla girada.
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
    verdadero, desvio = "95", 20
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


# ------------------------------------------------------------------ bodega (Sokoban)
DIRS = {"arriba": (0, -1), "abajo": (0, 1), "izquierda": (-1, 0), "derecha": (1, 0)}


def resolver_sokoban(muros, cajas, metas, jugador, ancho, alto, limite=400000):
    """BFS por movimientos del jugador: devuelve la lista de movimientos más corta que deja las cajas en las metas (o None)."""
    metas = frozenset(metas)
    inicio = (jugador, frozenset(cajas))
    previo = {inicio: None}
    cola = deque([inicio])
    while cola:
        estado = cola.popleft()
        p, cs = estado
        if cs == metas:
            camino = []
            while previo[estado]:
                estado, mov = previo[estado]
                camino.append(mov)
            return camino[::-1]
        for nombre, (dx, dy) in DIRS.items():
            q = (p[0] + dx, p[1] + dy)
            if q in muros or not (0 <= q[0] < ancho and 0 <= q[1] < alto):
                continue
            ncs = cs
            if q in cs:
                r = (q[0] + dx, q[1] + dy)
                if r in muros or r in cs or not (0 <= r[0] < ancho and 0 <= r[1] < alto):
                    continue
                if r not in metas and _rincon(r, muros, ancho, alto):
                    continue
                ncs = (cs - {q}) | {r}
            nuevo = (q, ncs)
            if nuevo not in previo:
                previo[nuevo] = (estado, nombre)
                if len(previo) > limite:
                    return None
                cola.append(nuevo)
    return None


def _rincon(c, muros, ancho, alto):
    bloq = lambda x, y: (x, y) in muros or not (0 <= x < ancho and 0 <= y < alto)
    x, y = c
    return (bloq(x - 1, y) or bloq(x + 1, y)) and (bloq(x, y - 1) or bloq(x, y + 1))


def empujes(muros, cajas, jugador, movs):
    cs, p, n = set(cajas), jugador, 0
    for m in movs:
        dx, dy = DIRS[m]
        q = (p[0] + dx, p[1] + dy)
        if q in cs:
            cs.remove(q)
            cs.add((q[0] + dx, q[1] + dy))
            n += 1
        p = q
    return n, cs


def bodega():
    ancho, alto = 7, 6
    rng = random.Random(1715)
    mejor = None
    for intento in range(4000):
        celdas = [(x, y) for y in range(alto) for x in range(ancho)]
        rng.shuffle(celdas)
        muros = set(celdas[:rng.randint(5, 7)])
        libres = [c for c in celdas if c not in muros]
        cajas = set(libres[:3])
        metas = set(libres[3:6])
        jugador = libres[6]
        if any(_rincon(c, muros, ancho, alto) for c in cajas):
            continue
        sol = resolver_sokoban(muros, cajas, metas, jugador, ancho, alto)
        if not sol:
            continue
        n_emp, final = empujes(muros, cajas, jugador, sol)
        assert final == metas
        # que haga falta pensar: bastantes empujes, alguna caja empujada en dos direcciones y ninguna meta pegada a su caja
        if not 10 <= n_emp <= 13 or len(sol) > 40 or any(abs(c[0] - m[0]) + abs(c[1] - m[1]) <= 1 for c in cajas for m in metas):
            continue
        clave = (n_emp, len(sol))
        if mejor is None or clave > mejor[0]:
            mejor = (clave, dict(ancho=ancho, alto=alto, muros=sorted(muros), cajas=sorted(cajas), metas=sorted(metas), jugador=jugador,
                                 solucion=sol, empujes=n_emp))
        if intento > 1500 and mejor:
            break
    assert mejor, "no se encontró una bodega"
    b = mejor[1]
    b["muros"] = [list(c) for c in b["muros"]]
    b["cajas"] = [list(c) for c in b["cajas"]]
    b["metas"] = [list(c) for c in b["metas"]]
    b["jugador"] = list(b["jugador"])
    return b


# ------------------------------------------------------------------ la persecución (la fragata, como el Minotauro de «Teseo y el Minotauro»)
MOV = {"arriba": (0, -1), "abajo": (0, 1), "izquierda": (-1, 0), "derecha": (1, 0), "esperar": (0, 0)}


def paso_fragata(f, b, rocas, ancho, alto):
    """Un paso de la fragata (la ordenanza de la carta 52): si puede acercarse en horizontal, va en horizontal; si no, si puede acercarse
    en vertical, va en vertical; si no, se queda. Las rocas no se cruzan."""
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
    ancho, alto = 6, 6
    rng = random.Random(1716)
    mejor = None
    for _ in range(6000):
        celdas = [(x, y) for y in range(alto) for x in range(ancho)]
        rng.shuffle(celdas)
        rocas = set(celdas[:rng.randint(6, 8)])
        libres = [c for c in celdas if c not in rocas]
        barco, fragata, niebla = libres[0], libres[1], libres[2]
        if abs(barco[0] - niebla[0]) + abs(barco[1] - niebla[1]) < 6 or abs(barco[0] - fragata[0]) + abs(barco[1] - fragata[1]) < 3:
            continue
        sol = resolver_persecucion(rocas, barco, fragata, niebla, ancho, alto)
        if not sol or not 9 <= len(sol) <= 16:
            continue
        directo = resolver_persecucion(rocas, barco, (-9, -9), niebla, ancho, alto)
        if len(sol) - len(directo) < 3:                        # que no valga ir directo: hay que engañar a la fragata
            continue
        clave = (len(sol) - len(directo), "esperar" in sol, len(sol))
        if mejor is None or clave > mejor[0]:
            mejor = (clave, dict(ancho=ancho, alto=alto, rocas=sorted([list(c) for c in rocas]), barco=list(barco), fragata=list(fragata),
                                 niebla=list(niebla), solucion=sol, directo=len(directo)))
    assert mejor, "no se encontró una persecución"
    return mejor[1]


# ------------------------------------------------------------------ la tapa del cofre (constelación girada entre tachuelas)
def cielo():
    """La constelación de la Calavera (carta 64) aparece en la tapa del cofre girada 120 grados entre otras estrellas.
    Se comprueba que ninguna otra elección de estrellas forma la misma figura (con cualquier giro y el mismo tamaño)."""
    figura = [(0, -46), (-34, -20), (34, -20), (-22, 26), (22, 26), (0, 56)]          # en píxeles de la tapa de la app (300 x 300)
    rng = random.Random(64)
    giro = math.radians(120)
    cx, cy = 172, 140
    estrellas = [(round(cx + x * math.cos(giro) - y * math.sin(giro)), round(cy + x * math.sin(giro) + y * math.cos(giro))) for x, y in figura]
    while len(estrellas) < 30:
        p = (rng.randint(16, 284), rng.randint(16, 284))
        if all(math.dist(p, q) >= 26 for q in estrellas):
            estrellas.append(p)
    tol = 6
    encontradas = 0
    d01 = math.dist(figura[0], figura[1])
    for i, a in enumerate(estrellas):
        for j, b in enumerate(estrellas):
            if i == j or abs(math.dist(a, b) - d01) > tol:
                continue
            ang = math.atan2(b[1] - a[1], b[0] - a[0]) - math.atan2(figura[1][1] - figura[0][1], figura[1][0] - figura[0][0])
            ok = True
            for x, y in figura:
                dx, dy = x - figura[0][0], y - figura[0][1]
                p = (a[0] + dx * math.cos(ang) - dy * math.sin(ang), a[1] + dx * math.sin(ang) + dy * math.cos(ang))
                if min(math.dist(p, q) for q in estrellas) > tol:
                    ok = False
                    break
            encontradas += ok
    assert encontradas == 1, f"la constelación aparece {encontradas} veces"
    orden = list(range(len(estrellas)))
    rng.shuffle(orden)
    estrellas = [estrellas[k] for k in orden]
    solucion = sorted(orden.index(k) for k in range(6))
    return {"figura": figura, "giro": 120, "estrellas": [list(e) for e in estrellas], "solucion": solucion}


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
    n = 5
    ciclo = ["luna", "llave", "calavera", "corona"]
    otros = [s for s in SIMBOLOS if s not in ciclo]
    rng = random.Random(79)
    for _ in range(50000):
        x = rng.randrange(n)
        camino = [(x, n - 1)]
        while camino[-1][1] > 0 and len(camino) < 14:
            cx, cy = camino[-1]
            c = rng.choice([(cx, cy - 1), (cx, cy - 1)] + [(cx + d, cy) for d in (-1, 1) if 0 <= cx + d < n])
            if c in camino:
                if all(o in camino for o in [(cx, cy - 1)] + [(cx + d, cy) for d in (-1, 1) if 0 <= cx + d < n]):
                    break
                continue
            camino.append(c)
        if camino[-1][1] != 0 or len(camino) < 9:
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
    # desplegado: cada vez que la ruta cruza el pliegue vertical se dan 2 pasos más; el horizontal, igual
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
    "30": {"x": [235, 395]},
    "76": {"x": [240, 390]},
    "70": {"x": [251, 379], "y": [372, 500]},
}


def main():
    inst = {"rumbo": rumbo(), "bodega": bodega(), "persecucion": persecucion(), "cielo": cielo(), "losas": suelo(), "ruta": ruta(),
            "pliegues": PLIEGUES, "lamina": [630, 882]}
    with open(os.path.join(AQUI, "instancias_piratas.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(inst, f, ensure_ascii=False, indent=1)
        f.write("\n")
    r, b, pe = inst["rumbo"], inst["bodega"], inst["persecucion"]
    print(f"rumbo: carta {r['carta']} (desplegada se lee {r['senuelos']}), aguja {r['aguja']}")
    print(f"bodega: {len(b['solucion'])} movimientos, {b['empujes']} empujes; muros {b['muros']}")
    print(f"persecución: {len(pe['solucion'])} turnos ({pe['directo']} sin fragata): {pe['solucion']}")
    print(f"cielo: constelación en las estrellas {inst['cielo']['solucion']}")
    print(f"suelo: camino de {len(inst['losas']['camino'])} losas")
    print(f"ruta: {len(inst['ruta']['movimientos'])} flechas plegada, {len(inst['ruta']['desplegada'])} desplegada")


if __name__ == "__main__":
    main()

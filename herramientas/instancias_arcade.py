"""Instancias de los dos minijuegos por turnos de «Game Over, 1985» (autopista tipo Frogger y encaje de piezas tipo Tetris),
buscadas por fuerza bruta con semilla fija para que tengan solución y sea comprobable. Escribe herramientas/instancias_arcade.json
(lo leen pixeles.py, para dibujar las cartas 52 y 70, y los solucionadores) y muestra el JSON para pegarlo en los minijuegos.

Uso:  python herramientas/instancias_arcade.py
"""
import json
import os
import random
from collections import deque

# --------------------------------------------------------------- autopista
ANCHO = 7
FILAS = 6                 # fila 0 = meta, filas 1..4 = carriles, fila 5 = salida
SALIDA = (5, 3)


def avanzar(coches, carril):
    """Mueve los coches de un carril una vez y devuelve las casillas por las que pasan (incluida la final)."""
    d, v, _ = carril
    nuevas, pasos = [], []
    for c in coches:
        x = c
        for _ in range(v):
            x = (x + d) % ANCHO
            pasos.append(x)
        nuevas.append(x)
    return nuevas, pasos


def paso(estado, mov, carriles):
    """estado = (fila, col, posiciones de los coches por carril). mov: arriba, izquierda, derecha o quieto. Devuelve estado nuevo o None si hay choque."""
    f, c, coches = estado
    if mov == "arriba":
        f -= 1
    elif mov == "izquierda":
        c -= 1
    elif mov == "derecha":
        c += 1
    if f < 0 or c < 0 or c >= ANCHO:
        return None
    if 1 <= f <= 4 and c in coches[f - 1]:
        return None
    nuevos = []
    for i, cols in enumerate(coches):
        nueva, pasos = avanzar(cols, carriles[i])
        if f == i + 1 and c in pasos:
            return None
        nuevos.append(nueva)
    return (f, c, tuple(tuple(sorted(x)) for x in nuevos))


def resolver(carriles, limite=14):
    ini = (SALIDA[0], SALIDA[1], tuple(tuple(sorted(c[2])) for c in carriles))
    cola = deque([(ini, [])])
    vistos = {ini}
    while cola:
        e, camino = cola.popleft()
        if e[0] == 0:
            return camino
        if len(camino) >= limite:
            continue
        for m in ("arriba", "izquierda", "derecha", "quieto"):
            n = paso(e, m, carriles)
            if n and n not in vistos:
                vistos.add(n)
                cola.append((n, camino + [m]))
    return None


def buscar_autopista():
    rng = random.Random(1985)
    while True:
        carriles = []
        for _ in range(4):
            d = rng.choice([1, -1])
            v = rng.choice([1, 1, 2])
            n = rng.choice([2, 2, 3])
            cols = sorted(rng.sample(range(ANCHO), n))
            carriles.append((d, v, cols))
        # ningún coche en la columna de salida de los carriles de más abajo (para que el primer paso no sea un choque inmediato)
        sol = resolver(carriles)
        if sol and 8 <= len(sol) <= 10 and sol.count("quieto") >= 1:
            return carriles, sol


# --------------------------------------------------------------- piezas
BASE = {"I": [(0, 0), (0, 1), (0, 2), (0, 3)], "O": [(0, 0), (0, 1), (1, 0), (1, 1)], "T": [(0, 0), (0, 1), (0, 2), (1, 1)],
        "S": [(0, 1), (0, 2), (1, 0), (1, 1)], "Z": [(0, 0), (0, 1), (1, 1), (1, 2)], "J": [(0, 0), (1, 0), (1, 1), (1, 2)],
        "L": [(0, 2), (1, 0), (1, 1), (1, 2)]}
POZO_F, POZO_C = 4, 6


def normalizar(celdas):
    mr = min(r for r, c in celdas)
    mc = min(c for r, c in celdas)
    return sorted((r - mr, c - mc) for r, c in celdas)


def girar(celdas):
    """Giro de 90° en el sentido de las agujas del reloj."""
    return normalizar([(c, -r) for r, c in celdas])


def orientaciones(t):
    o, vistas, c = [], [], normalizar(BASE[t])
    for _ in range(4):
        if c not in vistas:
            vistas.append(c)
            o.append(c)
        c = girar(c)
    return o


def teselados(libres, usar, limite=2):
    """Cuenta (hasta `limite`) las formas distintas de cubrir las casillas libres con las piezas de `usar` (diccionario tipo -> cantidad)."""
    libres = frozenset(libres)
    res = []

    def rec(libre, resto, colocadas):
        if len(res) >= limite:
            return
        if not libre:
            if not any(resto.values()):
                res.append(sorted(colocadas))
            return
        r0, c0 = min(libre)
        for t, n in resto.items():
            if n == 0:
                continue
            for o in orientaciones(t):
                dr, dc = o[0]
                celdas = [(r0 - dr + r, c0 - dc + c) for r, c in o]
                if all(x in libre for x in celdas):
                    resto[t] -= 1
                    rec(libre - set(celdas), resto, colocadas + [(t, tuple(celdas))])
                    resto[t] += 1

    rec(libres, dict(usar), [])
    return res


def teselado_al_azar(libres, rng):
    """Un teselado cualquiera de las casillas libres con piezas al azar (o None si no sale)."""
    libres = frozenset(libres)

    def rec(libre, colocadas):
        if not libre:
            return colocadas
        r0, c0 = min(libre)
        opciones = [(t, o) for t in "IOTSZJL" for o in orientaciones(t)]
        rng.shuffle(opciones)
        for t, o in opciones:
            dr, dc = o[0]
            celdas = [(r0 - dr + r, c0 - dc + c) for r, c in o]
            if all(x in libre for x in celdas):
                res = rec(libre - set(celdas), colocadas + [(t, tuple(celdas))])
                if res:
                    return res
        return None

    return rec(libres, [])


def buscar_pozo():
    rng = random.Random(1986)
    todas = [(r, c) for r in range(POZO_F) for c in range(POZO_C)]
    while True:
        bloqueadas = rng.sample(todas, 4)
        libres = [x for x in todas if x not in bloqueadas]
        base = teselado_al_azar(libres, rng)
        if base is None:
            continue
        usar = {}
        for t, _ in base:
            usar[t] = usar.get(t, 0) + 1
        if len(usar) < 4:
            continue                      # que haya variedad de piezas
        sols = teselados(libres, usar, 2)
        if len(sols) == 1:
            return sorted(bloqueadas), usar, sols[0]


def main():
    carriles, camino = buscar_autopista()
    bloq, usar, sol = buscar_pozo()
    datos = {
        "autopista": {"ancho": ANCHO, "carriles": [{"dir": d, "vel": v, "coches": c} for d, v, c in carriles], "salida": list(SALIDA), "solucion": camino},
        "pozo": {"filas": POZO_F, "cols": POZO_C, "bloqueadas": bloq, "piezas": usar,
                 "solucion": [{"tipo": t, "celdas": [list(x) for x in celdas]} for t, celdas in sol]},
    }
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_arcade.json")
    json.dump(datos, open(ruta, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print(json.dumps(datos, ensure_ascii=False))
    print("autopista:", len(camino), "pasos:", camino)
    print("pozo: piezas", usar, "bloqueadas", bloq)


if __name__ == "__main__":
    main()

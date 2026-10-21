"""Instancias con solución única comprobada para los minijuegos de «Cuento» (vidriera, hadas, pociones, salto en el tiempo, caja de música).

Uso (desde la raíz del repo): python herramientas/instancias_cuento.py      -> imprime las instancias y comprueba su unicidad
Los minijuegos (juegos/aventuras-ca/cuento/minijuegos/*.js) llevan estas constantes copiadas; los solucionadores (solvers_cuento.py) las importan de aquí.
"""
import itertools
import os
import random
import sys
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generadores_puzles as G  # noqa: E402

# ------------------------------------------------------------------ Cerillas, puente, rayos: del generador común
CERILLAS = G.cerillas(7)                      # 9 + 4 = 5  -> mover una cerilla: 5 + 4 = 9
PUENTE = G.puentes_linterna((1, 2, 5, 8))     # mínimo 15 minutos
RAYOS = G.rayos(5, 3, 7)                      # gema en la casilla E5

# ------------------------------------------------------------------ Vidriera: tres cristales (tetraminós, sin girar) que cubren exactamente el dibujo
FORMAS = {
    "palo": [(0, 0), (1, 0), (2, 0), (3, 0)],
    "ele": [(0, 0), (0, 1), (0, 2), (1, 2)],
    "te": [(0, 0), (1, 0), (2, 0), (1, 1)],
    "ese": [(1, 0), (2, 0), (0, 1), (1, 1)],
}
N_VID = 5


def _colocaciones(celdas):
    """Todas las posiciones (dx, dy) en las que cabe una pieza en el tablero de 5x5."""
    res = []
    for dx in range(N_VID):
        for dy in range(N_VID):
            c = frozenset((x + dx, y + dy) for x, y in celdas)
            if all(0 <= x < N_VID and 0 <= y < N_VID for x, y in c):
                res.append(((dx, dy), c))
    return res


def vidriera(semilla=1):
    """Elige tres piezas y una colocación cuyo dibujo solo se puede cubrir de una manera (cada pieza se usa una vez, sin solapar ni girar)."""
    rng = random.Random(semilla)
    nombres = list(FORMAS)
    for _ in range(3000):
        piezas = rng.sample(nombres, 3)
        elegido = [rng.choice(_colocaciones(FORMAS[p])) for p in piezas]
        union = set()
        ok = True
        for _, c in elegido:
            if union & c:
                ok = False
                break
            union |= c
        if not ok or len(union) != 12:
            continue
        sols = []
        for combo in itertools.product(*[_colocaciones(FORMAS[p]) for p in piezas]):
            u = set()
            bien = True
            for _, c in combo:
                if u & c:
                    bien = False
                    break
                u |= c
            if bien and u == union:
                sols.append([pos for pos, _ in combo])
        if len(sols) == 1:
            return dict(piezas=piezas, dibujo=sorted(union), solucion=sols[0])
    raise RuntimeError("sin vidriera")


VIDRIERA = vidriera(4)

# ------------------------------------------------------------------ Hadas (caballeros y bribones)
HADAS = G.caballeros(4, 13)

# ------------------------------------------------------------------ Pociones de colores (tubos) con el orden final de la carta
def pociones(semilla=3, orden=(1, 2, 0)):
    """Tubos de 4 con tres colores y dos vacíos; hay que dejar en los tres primeros tubos los colores en `orden` y los dos últimos vacíos."""
    inst = G.tubos(3, 4, 2, semilla, min_movs=8)
    ini = tuple(tuple(t) for t in inst["tubos"])
    meta = tuple(tuple([c] * 4) for c in orden) + ((), ())
    visto = {ini: None}
    cola = deque([ini])
    while cola:
        e = cola.popleft()
        if e == meta:
            ruta, x = [], e
            while visto[x]:
                x, mov = visto[x]
                ruta.append(mov)
            return dict(tubos=inst["tubos"], orden=list(orden), movimientos_minimos=len(ruta), ruta=ruta[::-1])
        for a, ta in enumerate(e):
            if not ta:
                continue
            for b, tb in enumerate(e):
                if a == b or len(tb) >= 4 or (tb and tb[-1] != ta[-1]):
                    continue
                k = 1
                while k < len(ta) and ta[-1 - k] == ta[-1]:
                    k += 1
                k = min(k, 4 - len(tb))
                ne = list(e)
                ne[a] = ta[:-k]
                ne[b] = tb + ta[-k:]
                ne = tuple(ne)
                if ne not in visto:
                    visto[ne] = (e, (a, b))
                    cola.append(ne)
    raise RuntimeError("sin pociones")


POCIONES = pociones()

# ------------------------------------------------------------------ Había una vez / Y ahora (salto corto en el tiempo)
# Siete casillas del camino. Casilla 0 = aldea, 6 = castillo. Terreno del presente en cada casilla y reglas de cada acción (carta 42 = cuento del Búho).
PRESENTE = ["aldea", "libre", "zarza", "libre", "rio", "roca", "castillo"]
PASADO = ["aldea", "pradera", "bosquecillo", "pradera", "charca", "colina", "castillo"]
ACCIONES = ["plantar", "cavar", "fuego"]


def efecto(accion, terreno):
    """Terreno del presente en una casilla tras hacer la acción en el pasado."""
    if accion == "plantar":
        return {"rio": "puente", "zarza": "zarzal", "roca": "roca", "libre": "habichuela"}.get(terreno, terreno)
    if accion == "cavar":
        return {"roca": "hueco", "libre": "foso", "rio": "rio", "zarza": "zarza"}.get(terreno, terreno)
    if accion == "fuego":
        return {"zarza": "ceniza", "libre": "ceniza", "rio": "rio", "roca": "roca"}.get(terreno, terreno)
    return terreno


PASABLES = {"aldea", "castillo", "libre", "ceniza", "puente", "hueco", "habichuela"}


def salto(acciones):
    """acciones: dict casilla -> acción. Devuelve la lista de terrenos del presente."""
    return [efecto(acciones[i], t) if i in acciones else t for i, t in enumerate(PRESENTE)]


def salto_resuelve(acciones):
    return all(t in PASABLES for t in salto(acciones))


def soluciones_salto():
    sols = []
    for cas in itertools.combinations(range(1, 6), 3):
        for acc in itertools.product(ACCIONES, repeat=3):
            a = dict(zip(cas, acc))
            if salto_resuelve(a):
                sols.append(a)
    return sols


# ------------------------------------------------------------------ Caja de música: partitura de animales y tabla animal -> nota
TABLA = {"conejo": "Do", "ciervo": "Re", "búho": "Mi", "rana": "Fa", "ardilla": "Sol", "zorro": "La"}
PARTITURA = ["rana", "conejo", "ardilla", "búho", "ciervo", "zorro", "rana"]
NOTAS = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"]
FRECUENCIAS = {"Do": 261.63, "Re": 293.66, "Mi": 329.63, "Fa": 349.23, "Sol": 392.0, "La": 440.0, "Si": 493.88}
SOLUCION_MUSICA = [TABLA[a] for a in PARTITURA]

# ------------------------------------------------------------------ Botas de siete leguas (versión de 60 cartas): los pasos saltan, por turnos,
# DOS y TRES casillas en línea recta (por encima de lo que haya); no se puede caer en un árbol, en el agua ni fuera del mapa.
def botas(semilla=7, n=7, saltos=(2, 3)):
    rng = random.Random(semilla)
    dirs = {"arriba": (0, -1), "abajo": (0, 1), "izquierda": (-1, 0), "derecha": (1, 0)}
    for _ in range(20000):
        obst = set()
        while len(obst) < 14:
            obst.add((rng.randrange(n), rng.randrange(n)))
        ini, fin = (0, n - 1), (n - 1, 0)
        if ini in obst or fin in obst:
            continue
        inicio = (ini, 0)
        prev = {inicio: None}
        cola = deque([inicio])
        llegada = None
        while cola:
            c, k = cola.popleft()
            if c == fin:
                llegada = (c, k)
                break
            for d, (dx, dy) in dirs.items():
                v = (c[0] + dx * saltos[k], c[1] + dy * saltos[k])
                e = (v, 1 - k)
                if 0 <= v[0] < n and 0 <= v[1] < n and v not in obst and e not in prev:
                    prev[e] = ((c, k), d)
                    cola.append(e)
        if not llegada:
            continue
        camino, e = [], llegada
        while prev[e]:
            e, d = prev[e]
            camino.append(d)
        camino = camino[::-1]
        if 7 <= len(camino) <= 10:
            return {"n": n, "saltos": list(saltos), "obstaculos": sorted([list(o) for o in obst]), "inicio": list(ini), "fin": list(fin), "solucion": camino}
    raise SystemExit("sin botas")


BOTAS = botas()

# ------------------------------------------------------------------ La habichuela: hojas cada día (cada día, tantas hojas nuevas como tenía anteayer)
HOJAS = [1, 1]
while len(HOJAS) < 12:
    HOJAS.append(HOJAS[-1] + HOJAS[-2])
HABICHUELA = {"dibujados": HOJAS[:6], "pregunta_dia": 9, "solucion": HOJAS[8]}


# ------------------------------------------------------------------ Letras del libro: una por cada app que se resuelve (palabra PERDICES)
LETRAS = {"14": "C", "20": "E", "40": "S", "46": "D", "51": "I", "64": "P", "69": "E", "72": "R"}
PALABRA = "PERDICES"


if __name__ == "__main__":
    print("cerillas:", CERILLAS)
    print("puente:", PUENTE["tiempo_minimo"], PUENTE["plan"])
    print("rayos:", RAYOS)
    print("vidriera:", VIDRIERA)
    print("hadas:", HADAS)
    print("pociones:", POCIONES)
    s = soluciones_salto()
    print("salto: soluciones", s)
    assert len(s) == 1, "el salto debe tener una sola solución"
    assert sorted(LETRAS.values()) == sorted(PALABRA), "las letras no forman la palabra"
    assert len(set(PARTITURA)) <= len(TABLA) and all(a in TABLA for a in PARTITURA)
    print("botas:", BOTAS)
    print("habichuela:", HABICHUELA)
    print("OK")

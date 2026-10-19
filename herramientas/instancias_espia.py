"""Instancias de «Montecarlo, 1965: Operación Cristal», buscadas con semilla fija y comprobadas por fuerza bruta:
  - laberinto 7x7 perfecto (un solo camino de la entrada a la salida) para las paredes invisibles de la carta 40 y el minijuego 46;
  - rascacielos 4x4 con solución ÚNICA y pistas repartidas en dos cartas (52: arriba e izquierda; 53: abajo y derecha);
  - las cuatro cargas de la bomba (cables) con la regla que se cumple en cada una y el cable que hay que cortar.
Escribe herramientas/instancias_espia.json (lo leen espia.py, para dibujar las cartas, y los solucionadores).

Uso:  python herramientas/instancias_espia.py
"""
import itertools
import json
import os
import random

# ------------------------------------------------------------------ laberinto
N = 7


def laberinto(semilla=1965):
    """Laberinto perfecto por búsqueda en profundidad. Devuelve los pasillos abiertos como pares de celdas ((f,c),(f,c))."""
    rng = random.Random(semilla)
    vistos = {(0, 0)}
    pila = [(0, 0)]
    abiertos = set()
    while pila:
        f, c = pila[-1]
        vecinos = [(f + df, c + dc) for df, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= f + df < N and 0 <= c + dc < N and (f + df, c + dc) not in vistos]
        if not vecinos:
            pila.pop()
            continue
        v = rng.choice(vecinos)
        abiertos.add(tuple(sorted([(f, c), v])))
        vistos.add(v)
        pila.append(v)
    return abiertos


def camino(abiertos, ini, fin):
    ant = {ini: None}
    cola = [ini]
    for cel in cola:
        if cel == fin:
            break
        f, c = cel
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            v = (f + d[0], c + d[1])
            if v not in ant and tuple(sorted([cel, v])) in abiertos:
                ant[v] = cel
                cola.append(v)
    ruta = []
    x = fin
    while x:
        ruta.append(x)
        x = ant[x]
    return ruta[::-1]


# ------------------------------------------------------------------ rascacielos
def visibles(fila):
    m, n = 0, 0
    for h in fila:
        if h > m:
            m, n = h, n + 1
    return n


def pistas_completas(rejilla):
    cols = [[rejilla[f][c] for f in range(4)] for c in range(4)]
    return {"arriba": [visibles(cols[c]) for c in range(4)], "abajo": [visibles(cols[c][::-1]) for c in range(4)],
            "izquierda": [visibles(rejilla[f]) for f in range(4)], "derecha": [visibles(rejilla[f][::-1]) for f in range(4)]}


LATINOS = [p for p in itertools.permutations(range(1, 5))]


def contar_soluciones(pistas, limite=2):
    n = 0
    for f0 in LATINOS:
        if pistas["arriba"][0] is not None and False:
            pass
        for f1 in LATINOS:
            if any(a == b for a, b in zip(f0, f1)):
                continue
            for f2 in LATINOS:
                if any(a == b or a == c for a, b, c in zip(f0, f1, f2)):
                    continue
                for f3 in LATINOS:
                    if any(len({f0[c], f1[c], f2[c], f3[c]}) < 4 for c in range(4)):
                        continue
                    g = [f0, f1, f2, f3]
                    if _cumple(g, pistas):
                        n += 1
                        if n >= limite:
                            return n
    return n


def _cumple(g, pistas):
    for f in range(4):
        if pistas["izquierda"][f] is not None and visibles(g[f]) != pistas["izquierda"][f]:
            return False
        if pistas["derecha"][f] is not None and visibles(g[f][::-1]) != pistas["derecha"][f]:
            return False
    for c in range(4):
        col = [g[f][c] for f in range(4)]
        if pistas["arriba"][c] is not None and visibles(col) != pistas["arriba"][c]:
            return False
        if pistas["abajo"][c] is not None and visibles(col[::-1]) != pistas["abajo"][c]:
            return False
    return True


def buscar_rascacielos(semilla=1966):
    rng = random.Random(semilla)
    while True:
        filas = list(LATINOS)
        rng.shuffle(filas)
        g = None
        for f0 in filas:
            for f1 in filas:
                if any(a == b for a, b in zip(f0, f1)):
                    continue
                for f2 in filas:
                    if any(a == b or a == c for a, b, c in zip(f0, f1, f2)):
                        continue
                    for f3 in filas:
                        if all(len({f0[c], f1[c], f2[c], f3[c]}) == 4 for c in range(4)):
                            g = [f0, f1, f2, f3]
                            break
                    if g:
                        break
                if g:
                    break
            if g:
                break
        completas = pistas_completas(g)
        pistas = {k: list(v) for k, v in completas.items()}
        celdas = [(k, i) for k in pistas for i in range(4)]
        rng.shuffle(celdas)
        for k, i in celdas:                      # quitar pistas mientras la solución siga siendo única (se dejan 8 para no pasarse de difícil)
            if sum(v is not None for l in pistas.values() for v in l) <= 8:
                break
            guardada = pistas[k][i]
            pistas[k][i] = None
            if contar_soluciones(pistas) != 1:
                pistas[k][i] = guardada
        card1 = sum(v is not None for v in pistas["arriba"] + pistas["izquierda"])
        card2 = sum(v is not None for v in pistas["abajo"] + pistas["derecha"])
        if card1 >= 3 and card2 >= 3 and card1 + card2 <= 10 and contar_soluciones(pistas) == 1:
            return g, pistas


# ------------------------------------------------------------------ cables
COLORES = ["rojo", "azul", "amarillo", "blanco", "negro"]


def regla_cable(cables):
    """Devuelve (número de regla, índice 0-based del cable que hay que cortar) según las reglas de la carta 70."""
    rojos, azules = cables.count("rojo"), cables.count("azul")
    if azules > rojos:
        return 1, max(i for i, c in enumerate(cables) if c == "azul")
    if rojos == 0 and cables[-1] == "amarillo":
        return 2, 0
    if cables.count("blanco") == 1:
        return 3, 3
    negros = [i for i, c in enumerate(cables) if c == "negro"]
    return 4, (max(negros) if negros else 1)


CARGAS = [["rojo", "azul", "azul", "negro", "blanco"],           # regla 1: más azules que rojos -> último azul
          ["rojo", "amarillo", "blanco", "rojo", "negro"],       # regla 3: un solo blanco -> cuarto cable
          ["negro", "blanco", "negro", "blanco", "amarillo"],    # regla 2: sin rojos y último amarillo -> primero
          ["amarillo", "rojo", "negro", "blanco", "blanco"]]     # regla 4: último negro


def main():
    abiertos = laberinto()
    ruta = camino(abiertos, (0, 0), (N - 1, N - 1))
    g, pistas = buscar_rascacielos()
    reglas = [regla_cable(c) for c in CARGAS]
    assert [r[0] for r in reglas] == [1, 3, 2, 4], reglas
    datos = {
        "laberinto": {"n": N, "abiertos": sorted([list(map(list, p)) for p in abiertos]), "entrada": [0, 0], "salida": [N - 1, N - 1], "ruta": [list(x) for x in ruta]},
        "rascacielos": {"solucion": g, "pistas": pistas},
        "cables": {"cargas": CARGAS, "reglas": [r[0] for r in reglas], "cortes": [r[1] for r in reglas]},
    }
    ruta_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_espia.json")
    json.dump(datos, open(ruta_json, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print("laberinto: camino de", len(ruta), "celdas")
    print("rascacielos:", g, pistas)
    print("cables: reglas", [r[0] for r in reglas], "cortes", [r[1] + 1 for r in reglas])


if __name__ == "__main__":
    main()

"""Instancias de «El primer salto» (el nivel de prueba, gratuito): tres puzles muy sencillos que enseñan a jugar.

  - cerradura: la pizarra de Alberto dibuja engranajes rojos, azules y amarillos; el código son los que hay de cada color (3 cifras).
  - mapa:      un plano de 4 x 6 casillas con seis símbolos, partido en dos láminas; un camino de seis casillas cruza el corte y hay que tocar, en orden,
               los símbolos de las cuatro casillas de en medio (todos distintos).
  - meta:      cada puzle deja una cifra y la carta 86 dice en qué orden se teclean.
Escribe herramientas/instancias_cronoportal.json. Uso:  python herramientas/instancias_cronoportal.py"""
import json
import os
import random

AQUI = os.path.dirname(os.path.abspath(__file__))
SIMBOLOS = ["sol", "luna", "estrella", "llave", "reloj", "flor"]


def cerradura():
    rng = random.Random(14)
    cuentas = {"rojo": 3, "azul": 5, "amarillo": 2}
    pos = []
    # posiciones de los engranajes en la pizarra (sin solaparse): rejilla de 5 x 3 con holgura y orden barajado
    celdas = [(c, f) for c in range(5) for f in range(2)]
    rng.shuffle(celdas)
    colores = [c for c, n in cuentas.items() for _ in range(n)]
    rng.shuffle(colores)
    for (c, f), col in zip(celdas, colores):
        pos.append({"col": col, "x": c, "y": f, "dx": rng.randint(-8, 8), "dy": rng.randint(-8, 8)})
    return {"cuentas": cuentas, "gears": pos, "codigo": "".join(str(cuentas[c]) for c in ("rojo", "azul", "amarillo")), "cifra": 4}


def mapa():
    rng = random.Random(20)
    cols, filas = 4, 6
    for _ in range(5000):
        celdas = [[rng.choice(SIMBOLOS) for _ in range(cols)] for _ in range(filas)]
        p = [(rng.randrange(cols), 5)]                        # entra por abajo
        while len(p) < 6:
            x, y = p[-1]
            op = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, -1)) if 0 <= x + dx < cols and 0 <= y + dy < filas and (x + dx, y + dy) not in p]
            if not op:
                break
            p.append(rng.choice(op))
        if len(p) < 6:
            continue
        if not any(y <= 2 for _, y in p) or not any(y >= 3 for _, y in p):     # tiene que cruzar el corte entre las dos láminas
            continue
        medio = [celdas[y][x] for x, y in p[1:5]]
        if len(set(medio)) != 4 or sum(1 for _, y in p if y <= 2) < 2:
            continue
        # los símbolos de las casillas de en medio no se repiten en las dos casillas de los extremos (más fácil de leer)
        if celdas[p[0][1]][p[0][0]] in medio or celdas[p[5][1]][p[5][0]] in medio:
            continue
        return {"cols": cols, "filas": filas, "celdas": celdas, "camino": [list(c) for c in p], "solucion": medio, "cifra": 7}
    raise SystemExit("sin mapa")


def meta():
    return {"orden": ["20", "14"], "codigo": "74", "cifras": {"14": 4, "20": 7}}


def main():
    inst = {"cerradura": cerradura(), "mapa": mapa(), "meta": meta()}
    assert inst["cerradura"]["cifra"] == inst["meta"]["cifras"]["14"] and inst["mapa"]["cifra"] == inst["meta"]["cifras"]["20"]
    for k in inst:
        print(f"{k:10} OK")
    with open(os.path.join(AQUI, "instancias_cronoportal.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(inst, f, ensure_ascii=False, indent=1)
        f.write("\n")


def _cargar():
    ruta = os.path.join(AQUI, "instancias_cronoportal.json")
    return json.load(open(ruta, encoding="utf-8")) if os.path.exists(ruta) else {}


INST = _cargar()

if __name__ == "__main__":
    main()

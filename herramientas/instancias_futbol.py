"""Instancias de «La Final del Siglo, 1970»: los puzles de fútbol, buscados con semilla fija y comprobados por fuerza bruta.
  - los seis cromos (cartas 14 a 19) y la pregunta que solo tiene un jugador como respuesta;
  - la alineación de Los Rayos (1-2-2-1) con pistas lógicas repartidas en dos cartas (30 y 31), con solución única;
  - cuatro jugadas del VAR (cartas 40 y 41) con su decisión según el reglamento (carta 42);
  - la liguilla de cuatro equipos (cartas 52 y 53): tres resultados conocidos y tres por descubrir, con solución única.
Escribe herramientas/instancias_futbol.json (lo leen futbol.py, para dibujar las cartas, y los solucionadores).

Uso:  python herramientas/instancias_futbol.py
"""
import itertools
import json
import os
import random

# ------------------------------------------------------------------ cromos
# carta -> jugador; los números de carta no siguen ningún orden
CROMOS = {
    "14": dict(dorsal=4, nombre="Toni Roca", pos="Defensa", pie="Diestro", altura=182, edad=24),
    "15": dict(dorsal=10, nombre="Beto Pase", pos="Centrocampista", pie="Zurdo", altura=178, edad=29),
    "16": dict(dorsal=1, nombre="Paco Guante", pos="Portero", pie="Diestro", altura=188, edad=31),
    "17": dict(dorsal=9, nombre="Rafa Gol", pos="Delantero", pie="Zurdo", altura=184, edad=26),
    "18": dict(dorsal=3, nombre="Luis Muro", pos="Defensa", pie="Zurdo", altura=176, edad=27),
    "19": dict(dorsal=7, nombre="Nico Regate", pos="Centrocampista", pie="Diestro", altura=170, edad=22),
}


def convocatoria():
    """Zurdo, de más de 1,75 m, de menos de 1,80 m y que no juega de defensa."""
    return [c for c, j in CROMOS.items() if j["pie"] == "Zurdo" and 175 < j["altura"] < 180 and j["pos"] != "Defensa"]


# ------------------------------------------------------------------ alineación 1-2-2-1
DORSALES = [1, 2, 5, 6, 8, 11]
SLOTS = ["P", "DI", "DD", "MI", "MD", "DEL"]
LINEA = {"P": 0, "DI": 1, "DD": 1, "MI": 2, "MD": 2, "DEL": 3}
NOMBRE_LINEA = ["portero", "defensa", "centro del campo", "delantero"]
SOLUCION_ALINEACION = {"P": 1, "DI": 6, "DD": 2, "MI": 11, "MD": 5, "DEL": 8}
SLOT_TEXTO = {"P": "de portero", "DI": "de defensa por la izquierda", "DD": "de defensa por la derecha", "MI": "en el centro del campo por la izquierda",
              "MD": "en el centro del campo por la derecha", "DEL": "de delantero"}


def restricciones(sol):
    """Todas las pistas verdaderas sobre la alineación `sol` (slot -> dorsal)."""
    d2s = {d: s for s, d in sol.items()}
    out = []
    for d, s in d2s.items():
        out.append(("slot", d, s, f"El {d} juega {SLOT_TEXTO[s]}."))
        out.append(("linea", d, LINEA[s], f"El {d} juega en la línea de {NOMBRE_LINEA[LINEA[s]]}." if LINEA[s] in (1, 2) else f"El {d} es el {NOMBRE_LINEA[LINEA[s]]}."))
        if s not in ("P", "DEL"):
            lado = "izquierda" if s in ("DI", "MI") else "derecha"
            out.append(("lado", d, lado, f"El {d} juega por la {lado}."))
    for a in DORSALES:
        for b in DORSALES:
            if a == b:
                continue
            sa, sb = d2s[a], d2s[b]
            if (sa, sb) in (("DI", "DD"), ("MI", "MD")):
                out.append(("izq_de", a, b, f"El {a} juega justo a la izquierda del {b}."))
            if LINEA[sa] > LINEA[sb]:
                out.append(("delante", a, b, f"El {a} juega más adelantado que el {b}."))
    return out


def cumple(c, asign):
    """asign: slot -> dorsal."""
    d2s = {d: s for s, d in asign.items()}
    t = c[0]
    if t == "slot":
        return d2s[c[1]] == c[2]
    if t == "linea":
        return LINEA[d2s[c[1]]] == c[2]
    if t == "lado":
        s = d2s[c[1]]
        return (s in ("DI", "MI")) == (c[2] == "izquierda") and s not in ("P", "DEL")
    if t == "izq_de":
        return (d2s[c[1]], d2s[c[2]]) in (("DI", "DD"), ("MI", "MD"))
    return LINEA[d2s[c[1]]] > LINEA[d2s[c[2]]]


def soluciones(cl):
    return [dict(zip(SLOTS, p)) for p in itertools.permutations(DORSALES) if all(cumple(c, dict(zip(SLOTS, p))) for c in cl)]


def buscar_alineacion(semilla=1970):
    rng = random.Random(semilla)
    todas = restricciones(SOLUCION_ALINEACION)
    while True:
        rng.shuffle(todas)
        elegidas = []
        for c in todas:
            elegidas.append(c)
            if len(soluciones(elegidas)) == 1:
                break
        for c in list(elegidas):                       # quitar las pistas que sobran
            resto = [x for x in elegidas if x is not c]
            if len(soluciones(resto)) == 1:
                elegidas = resto
        if 5 <= len(elegidas) <= 7:
            rng.shuffle(elegidas)
            return elegidas


# ------------------------------------------------------------------ VAR
def jugadas():
    """Cuatro jugadas. x en metros (la portería rival está en x = 105). El receptor está en fuera de juego si, en el momento del pase, está
    más cerca de la portería que el balón Y que el penúltimo defensor (el portero cuenta como defensor)."""
    J = [
        dict(nombre="A", defensas=[("P", 103, 34), ("D", 62, 18), ("D", 70, 44), ("D", 58, 28)], ataca=[("pase", 60, 30), ("recibe", 78, 40), ("otro", 52, 12)]),
        dict(nombre="B", defensas=[("P", 103, 34), ("D", 66, 20), ("D", 72, 46), ("D", 59, 32)], ataca=[("pase", 88, 14), ("recibe", 80, 30), ("otro", 64, 54)]),
        dict(nombre="C", defensas=[("P", 103, 34), ("D", 70, 22), ("D", 77, 50), ("D", 64, 36)], ataca=[("pase", 55, 40), ("recibe", 70, 14), ("otro", 85, 28)]),
        dict(nombre="D", defensas=[("P", 103, 34), ("D", 52, 24), ("D", 85, 52), ("D", 60, 38)], ataca=[("pase", 70, 22), ("recibe", 91, 36), ("otro", 97, 10)]),
    ]
    for j in J:
        fuera = fuera_de_juego(j)
        j["fuera"] = fuera
    return J


def fuera_de_juego(j):
    xs = sorted(x for _, x, _ in j["defensas"])
    penultimo = xs[-2]
    xp = next(x for r, x, _ in j["ataca"] if r == "pase")
    xr = next(x for r, x, _ in j["ataca"] if r == "recibe")
    return xr > penultimo and xr > xp and xr > 52.5


# ------------------------------------------------------------------ liguilla
EQUIPOS = ["Rayos", "Leones", "Águilas", "Toros"]
PARTIDOS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def tabla(resultados):
    """resultados: lista de (golesLocal, golesVisitante) en el orden de PARTIDOS -> [(pts, gf, gc)] por equipo."""
    t = [[0, 0, 0] for _ in EQUIPOS]
    for (a, b), (ga, gb) in zip(PARTIDOS, resultados):
        t[a][1] += ga; t[a][2] += gb; t[b][1] += gb; t[b][2] += ga
        if ga > gb:
            t[a][0] += 3
        elif ga < gb:
            t[b][0] += 3
        else:
            t[a][0] += 1; t[b][0] += 1
    return [tuple(x) for x in t]


def buscar_liguilla(semilla=1971):
    rng = random.Random(semilla)
    while True:
        res = [(rng.randint(0, 3), rng.randint(0, 3)) for _ in PARTIDOS]
        if sum(1 for a, b in res if a == b) > 2 or sum(a + b for a, b in res) < 8:
            continue
        conocidos = sorted(rng.sample(range(6), 3))
        desconocidos = [i for i in range(6) if i not in conocidos]
        t = tabla(res)
        n = 0
        for comb in itertools.product(range(6), repeat=6):
            r = [None] * 6
            for i in conocidos:
                r[i] = res[i]
            for k, i in enumerate(desconocidos):
                r[i] = (comb[2 * k], comb[2 * k + 1])
            if tabla(r) == t:
                n += 1
                if n > 1:
                    break
        if n == 1:
            return res, conocidos, desconocidos, t


# ------------------------------------------------------------------ penaltis
def portero(tiros):
    """El portero se lanza a la izquierda en el primero y después al lado en que chutó el penalti anterior (si fue al centro, se queda)."""
    saltos = []
    for i in range(len(tiros)):
        saltos.append("izquierda" if i == 0 else tiros[i - 1])
    return saltos


def goles(tiros):
    return [t != s for t, s in zip(tiros, portero(tiros))]


def main():
    assert convocatoria() == ["15"], convocatoria()
    ali = buscar_alineacion()
    jug = jugadas()
    assert [j["fuera"] for j in jug] == [True, False, False, True], [j["fuera"] for j in jug]
    res, conocidos, desconocidos, t = buscar_liguilla()
    ejemplo = ["derecha", "izquierda", "centro", "derecha", "izquierda"]
    assert all(goles(ejemplo)) and len(set(ejemplo)) == 3
    datos = {
        "cromos": CROMOS, "convocatoria": convocatoria()[0],
        "alineacion": {"dorsales": DORSALES, "solucion": SOLUCION_ALINEACION, "pistas": [c[3] for c in ali]},
        "var": [dict(nombre=j["nombre"], defensas=j["defensas"], ataca=j["ataca"], fuera=j["fuera"]) for j in jug],
        "liguilla": {"equipos": EQUIPOS, "partidos": PARTIDOS, "resultados": res, "conocidos": conocidos, "desconocidos": desconocidos, "tabla": t},
        "penaltis": {"ejemplo": ejemplo},
    }
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_futbol.json")
    json.dump(datos, open(ruta, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print("alineación:", len(ali), "pistas:", [c[3] for c in ali])
    print("liguilla: resultados", res, "conocidos", conocidos, "tabla", t)
    print("VAR:", [j["fuera"] for j in jug])


if __name__ == "__main__":
    main()

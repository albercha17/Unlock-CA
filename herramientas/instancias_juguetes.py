"""Instancias de «El Cuarto de Leo, 1995» (juguetes, dificultad fácil), con semilla fija y comprobadas por fuerza bruta. Escribe
instancias_juguetes.json, que leen juguetes.py (láminas), datos_juguetes.py (pistas y manual), los minijuegos (juguetes.py les copia sus datos)
y solvers_juguetes.py.

  - estanteria: la foto Polaroid (carta 20) y la estantería de ahora (app, carta 24): cinco diferencias.
  - torre:      torre de bloques en una base de 3 x 3 con alturas de 0 a 3; vistas de frente y de lado (carta 30) y desde arriba (carta 31);
                solución única comprobada entre las 4^9 torres posibles.
  - marioneta:  cuatro mandos de colores con hilos enredados (carta 52) hasta cuatro miembros; el cartel (carta 53) pide una postura.
  - folioscopio: cinco páginas del cuaderno de Leo (cartas 41, 43, 45, 49 y 51); se ordenan por el sol que se pone en la ventana y en cada
                página Leo rodea un juguete: ese orden carga el tren (carta 66).
  - pista:      pista de canicas con tres balancines que cambian de lado cada vez que pasa una canica (carta 70); el cristal es la tercera
                canica y tiene que caer en el tarro; solo una de las 8 posiciones iniciales lo consigue.
Uso (desde la raíz del repo):  python herramientas/instancias_juguetes.py
"""
import itertools
import json
import os
import random

AQUI = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ estantería (diferencias)
def estanteria():
    # juguetes por balda: (nombre, x del centro en una lámina de 600 px de ancho), tres baldas
    antes = {
        "0": [["patito", 90], ["tambor", 230], ["cohete", 370], ["libro", 510]],
        "1": [["pelota", 90], ["coche", 240], ["osito", 390], ["barco", 520]],
        "2": [["cubos", 100], ["cometa", 250], ["trompo", 390], ["xilofono", 520]],
    }
    cambios = [
        {"tipo": "color", "juguete": "pelota", "texto": "la pelota era roja y ahora es azul"},
        {"tipo": "falta", "juguete": "libro", "texto": "falta el libro morado"},
        {"tipo": "girado", "juguete": "cohete", "texto": "el cohete está boca abajo"},
        {"tipo": "sobra", "juguete": "dado", "balda": "1", "x": 455, "texto": "hay un dado que no estaba"},
        {"tipo": "movido", "juguete": "patito", "a_balda": "2", "x": 175, "texto": "el patito ha bajado a la balda de abajo"},
    ]
    return {"antes": antes, "cambios": cambios}


# ------------------------------------------------------------------ torre de bloques (vistas)
def vistas(h):
    frente = [max(h[f][c] for f in range(3)) for c in range(3)]          # columnas de izquierda a derecha, mirando desde delante
    lado = [max(h[f][c] for c in range(3)) for f in range(3)]            # filas de delante (0) a detrás (2), mirando desde la derecha
    arriba = [[1 if h[f][c] else 0 for c in range(3)] for f in range(3)]
    return frente, lado, arriba


def torre():
    rng = random.Random(1995)
    todas = list(itertools.product(range(4), repeat=9))
    indice = {}
    for t in todas:
        h = [list(t[0:3]), list(t[3:6]), list(t[6:9])]
        fr, la, ar = vistas(h)
        indice.setdefault((tuple(fr), tuple(la), tuple(map(tuple, ar))), []).append(h)
    unicas = [v[0] for v in indice.values() if len(v) == 1 and 9 <= sum(map(sum, v[0])) <= 14 and sum(x > 0 for f in v[0] for x in f) >= 6
              and len({x for f in v[0] for x in f if x}) == 3]
    unicas.sort()
    h = unicas[rng.randrange(len(unicas))]
    fr, la, ar = vistas(h)
    return {"alturas": h, "frente": fr, "lado": la, "arriba": ar, "bloques": sum(map(sum, h)), "candidatas": len(unicas)}


# ------------------------------------------------------------------ marioneta
def marioneta():
    mandos = ["rojo", "azul", "amarillo", "verde"]
    miembros = ["brazo_izq", "brazo_der", "pierna_izq", "pierna_der"]
    rng = random.Random(52)
    while True:
        perm = miembros[:]
        rng.shuffle(perm)
        if all(a != b for a, b in zip(perm, miembros)):
            break
    hilos = dict(zip(mandos, perm))
    postura = ["brazo_der", "pierna_izq"]                               # lo que pide el cartel de la función
    solucion = sorted(m for m, x in hilos.items() if x in postura)
    return {"mandos": mandos, "miembros": miembros, "hilos": hilos, "postura": postura, "solucion": solucion}


# ------------------------------------------------------------------ folioscopio
def folioscopio():
    rng = random.Random(41)
    juguetes = ["patito", "pelota", "tambor", "cohete", "cometa"]
    orden = juguetes[:]
    rng.shuffle(orden)
    cartas = ["41", "43", "45", "49", "51"]
    asignadas = cartas[:]
    while asignadas == sorted(asignadas) or asignadas == sorted(asignadas, reverse=True):
        rng.shuffle(asignadas)
    paginas = [{"carta": c, "paso": i, "juguete": orden[i]} for i, c in enumerate(asignadas)]   # paso 0 = sol más alto
    return {"juguetes": juguetes, "orden": orden, "paginas": paginas, "cartas_en_orden": asignadas}


# ------------------------------------------------------------------ pista de canicas (balancines)
# Cada canica entra por arriba y cae en el balancín 1. Va al lado al que apunta y, al pasar, el balancín cambia de lado.
# Balancín 1 izquierda -> balancín 2; derecha -> balancín 3. Balancín 2: salidas A (izq) y B (der). Balancín 3: salidas C (izq) y D (der).
def soltar(estado, n):
    e = dict(estado)
    salidas = []
    for _ in range(n):
        lado1 = e["b1"]
        e["b1"] = "der" if lado1 == "izq" else "izq"
        b = "b2" if lado1 == "izq" else "b3"
        lado = e[b]
        e[b] = "der" if lado == "izq" else "izq"
        salidas.append({("b2", "izq"): "A", ("b2", "der"): "B", ("b3", "izq"): "C", ("b3", "der"): "D"}[(b, lado)])
    return salidas


def pista():
    configs = [dict(zip(("b1", "b2", "b3"), c)) for c in itertools.product(("izq", "der"), repeat=3)]
    for tarro in ("B", "C", "A", "D"):
        buenas = [c for c in configs if soltar(c, 3)[2] == tarro]
        if len(buenas) == 1:
            sol = buenas[0]
            return {"tarro": tarro, "solucion": sol, "recorrido": soltar(sol, 3), "canicas": 3}
    # con tres canicas cada salida admite dos configuraciones: se añade la condición de la carta (la primera canica no puede caer al suelo, salida A)
    for tarro in ("B", "C", "D"):
        buenas = [c for c in configs if soltar(c, 3)[2] == tarro and "A" not in soltar(c, 3)[:2]]
        if len(buenas) == 1:
            sol = buenas[0]
            return {"tarro": tarro, "suelo": "A", "solucion": sol, "recorrido": soltar(sol, 3), "canicas": 3}
    raise SystemExit("no hay pista con solución única")


def main():
    inst = {"estanteria": estanteria(), "torre": torre(), "marioneta": marioneta(), "folioscopio": folioscopio(), "pista": pista()}
    with open(os.path.join(AQUI, "instancias_juguetes.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(inst, f, ensure_ascii=False, indent=1)
        f.write("\n")
    t, m, fo, p = inst["torre"], inst["marioneta"], inst["folioscopio"], inst["pista"]
    print(f"torre: {t['alturas']} ({t['bloques']} bloques; {t['candidatas']} torres con vistas únicas)")
    print(f"marioneta: {m['hilos']} -> tirar de {m['solucion']}")
    print(f"folioscopio: cartas en orden {fo['cartas_en_orden']} -> {fo['orden']}")
    print(f"pista: tarro en {p['tarro']}, balancines {p['solucion']}, recorrido {p['recorrido']}")


if __name__ == "__main__":
    main()

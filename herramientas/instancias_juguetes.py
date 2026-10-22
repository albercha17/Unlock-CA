"""Instancias de «El Cuarto de Leo, 1995» (juguetes, dificultad fácil-media), versión de 62 cartas (22 oct 2026), con semilla fija y comprobadas por fuerza bruta.
Escribe instancias_juguetes.json, que leen juguetes.py (láminas), datos_juguetes.py (pistas y manual), los minijuegos (juguetes.py les copia sus datos) y
solvers_juguetes.py.

Once puzles; la mecánica de cartas propia sigue siendo el FOLIOSCOPIO (cinco páginas del cuaderno de Leo que se ordenan por el sol de la ventana):
  cubos        cuatro cubos de seis dibujos partidos en cuartos: formar el dibujo de la tapa de la caja
  diferencias  la foto Polaroid de la estantería (dos láminas) y la estantería de ahora (app): siete diferencias
  folioscopio  las cinco páginas del cuaderno de Leo ordenadas por el sol; en cada una Leo rodea un juguete: ese orden carga el tren
  marioneta    cuatro mandos con hilos enredados en dos láminas hasta cuatro miembros; el cartel pide una postura
  oca          el juego de la oca de Leo (60 casillas, escaleras y toboganes) y las diez tiradas de su hermana: casilla final
  clavijas     un solitario de clavijas en cruz de 33 agujeros con 9 clavijas; dejar una sola en el centro (solución construida al revés)
  collar       un collar de cuentas con un patrón que se repite: color de la cuenta 100 y cuántas azules hay en las 100 primeras
  torre        torre de bloques en una base de 3 x 3 con alturas de 0 a 3; vistas de frente y de lado y desde arriba; solución única
  canicas      pista de canicas con tres balancines que cambian de lado cada vez que pasa una canica; el cristal es la tercera
  memoria      un juego de memoria de 16 cartas: doce intentos de Leo enseñan 15 posiciones; hay que formar las 8 parejas
  xilofono     la nana final: cinco notas que dejan otros puzles, en el orden de los dibujos de una carta
Uso (desde la raíz del repo):  python herramientas/instancias_juguetes.py
"""
import itertools
import json
import os
import random

AQUI = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ cubos de imágenes
def cubos():
    dibujos = ["perro", "barco", "casa", "sol", "cohete", "arbol"]
    rng = random.Random(1995)
    caras = []
    for _ in range(4):
        d = dibujos[:]
        rng.shuffle(d)
        caras.append(d)
    objetivo = "perro"
    inicial = [0, 0, 0, 0]
    while any(caras[i][inicial[i]] == objetivo for i in range(4)):
        inicial = [rng.randrange(6) for _ in range(4)]
    return {"dibujos": dibujos, "caras": caras, "objetivo": objetivo, "inicial": inicial, "solucion": [caras[i].index(objetivo) for i in range(4)]}


# ------------------------------------------------------------------ estantería (diferencias)
def estanteria():
    # juguetes por balda: (nombre, x del centro en una lámina de 600 px de ancho), tres baldas
    antes = {
        "0": [["patito", 90], ["tambor", 230], ["cohete", 370], ["libro", 510]],
        "1": [["pelota", 90], ["coche", 240], ["osito", 390], ["barco", 520]],
        "2": [["cubos", 100], ["cometa", 250], ["trompo", 390], ["xilofono", 520]],
    }
    cambios = [
        {"tipo": "color", "juguete": "pelota", "hasta": "azul", "texto": "la pelota era roja y ahora es azul"},
        {"tipo": "color", "juguete": "coche", "hasta": "rojo", "texto": "el coche era azul y ahora es rojo"},
        {"tipo": "falta", "juguete": "libro", "texto": "falta el libro morado"},
        {"tipo": "falta", "juguete": "barco", "texto": "falta el barco rojo"},
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
    cartas = ["41", "43", "45", "27", "23"]
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
    for tarro in ("B", "C", "D"):
        buenas = [c for c in configs if soltar(c, 3)[2] == tarro and "A" not in soltar(c, 3)[:2]]
        if len(buenas) == 1:
            sol = buenas[0]
            return {"tarro": tarro, "suelo": "A", "solucion": sol, "recorrido": soltar(sol, 3), "canicas": 3}
    raise SystemExit("no hay pista con solución única")


# ------------------------------------------------------------------ solitario de clavijas (cruz de 33 agujeros)
CRUZ = [(r, c) for r in range(7) for c in range(7) if 2 <= r <= 4 or 2 <= c <= 4]
DIRS4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def clavijas(semilla=1, saltos=8):
    """Se parte de una sola clavija en el centro y se deshacen `saltos` saltos: así hay seguro una solución (los saltos al derecho, en orden inverso)."""
    agujeros = set(CRUZ)
    for sem in range(semilla, semilla + 10000):
        rng = random.Random(sem)
        pegs = {(3, 3)}
        inversos = []
        for _ in range(saltos):
            opc = []
            for c in sorted(pegs):
                for dr, dc in DIRS4:
                    b = (c[0] - dr, c[1] - dc)
                    a = (c[0] - 2 * dr, c[1] - 2 * dc)
                    if a in agujeros and b in agujeros and a not in pegs and b not in pegs:
                        opc.append((a, b, c))
            if not opc:
                break
            a, b, c = rng.choice(opc)
            pegs.discard(c)
            pegs.add(a)
            pegs.add(b)
            inversos.append((a, b, c))              # al derecho: la clavija en a salta sobre b y cae en c
        if len(inversos) == saltos and len(pegs) == saltos + 1 and (3, 3) not in pegs:
            # que no sea demasiado fácil: ninguna clavija está pegada a otras tres
            return {"agujeros": [list(a) for a in sorted(agujeros)], "clavijas": [list(p) for p in sorted(pegs)], "centro": [3, 3],
                    "solucion": [[list(a), list(c)] for a, b, c in reversed(inversos)]}
    raise SystemExit("sin clavijas")


# ------------------------------------------------------------------ el juego de la oca de Leo
def oca(semilla=3, casillas=60, tiradas=10):
    for sem in range(semilla, semilla + 20000):
        rng = random.Random(sem)
        usadas = set()
        escaleras, toboganes = {}, {}
        for _ in range(4):
            while True:
                a = rng.randint(3, 40)
                b = a + rng.randint(8, 18)
                if a not in usadas and b not in usadas and b < casillas:
                    usadas |= {a, b}
                    escaleras[a] = b
                    break
        for _ in range(4):
            while True:
                b = rng.randint(4, 40)
                a = b + rng.randint(8, 18)
                if a not in usadas and b not in usadas and a < casillas:
                    usadas |= {a, b}
                    toboganes[a] = b
                    break
        saltos = {**escaleras, **toboganes}
        dados = [rng.randint(1, 6) for _ in range(tiradas)]
        pos = 0
        ruta = []
        usos = {"escalera": 0, "tobogan": 0}
        for d in dados:
            pos += d
            if pos in escaleras:
                pos = escaleras[pos]
                usos["escalera"] += 1
            elif pos in toboganes:
                pos = toboganes[pos]
                usos["tobogan"] += 1
            ruta.append(pos)
        if usos["escalera"] >= 2 and usos["tobogan"] >= 1 and pos < casillas and 25 <= pos <= 55:
            return {"casillas": casillas, "escaleras": {str(k): v for k, v in escaleras.items()}, "toboganes": {str(k): v for k, v in toboganes.items()},
                    "dados": dados, "ruta": ruta, "final": pos}
    raise SystemExit("sin oca")


# ------------------------------------------------------------------ el collar de cuentas
COLORES_CUENTA = ["rojo", "azul", "verde", "amarillo", "morado"]


def collar(semilla=2, total=100, periodo=7):
    for sem in range(semilla, semilla + 20000):
        rng = random.Random(sem)
        patron = [rng.choice(COLORES_CUENTA) for _ in range(periodo)]
        if len(set(patron)) < 4:
            continue
        ultimo = patron[(total - 1) % periodo]
        azules = sum(1 for i in range(total) if patron[i % periodo] == "azul")
        # que haya que contar bien: la cuenta 100 no es igual a la 99 ni a la 98, y hay entre 2 y 3 azules por vuelta
        if patron[(total - 1) % periodo] == patron[(total - 2) % periodo] or not 2 <= patron.count("azul") <= 3:
            continue
        if periodo != 7 or len({patron[i] for i in range(periodo)}) < 4:
            continue
        return {"periodo": periodo, "patron": patron, "total": total, "ultimo": ultimo, "azules": azules, "mostradas": 40}
    raise SystemExit("sin collar")


# ------------------------------------------------------------------ memoria (16 cartas, 8 parejas)
IMAGENES = ["patito", "pelota", "tambor", "cohete", "coche", "osito", "barco", "cometa"]


def memoria(semilla=5):
    for sem in range(semilla, semilla + 20000):
        rng = random.Random(sem)
        cartas = IMAGENES * 2
        rng.shuffle(cartas)                       # cartas[i] es la imagen de la posición i (0 a 15; A1, B1, C1, D1, A2...)
        oculta = rng.randrange(16)
        vistas = [i for i in range(16) if i != oculta]
        apar = vistas[:] + rng.choices(vistas, k=24 - len(vistas))          # doce intentos de dos cartas: 24 apariciones sobre las 15 vistas
        rng.shuffle(apar)
        intentos = [[apar[2 * k], apar[2 * k + 1]] for k in range(12)]
        if any(a == b for a, b in intentos) or len({tuple(sorted(i)) for i in intentos}) < 12:
            continue
        parejas = {}
        for i, im in enumerate(cartas):
            parejas.setdefault(im, []).append(i)
        solucion = sorted(sorted(p) for p in parejas.values())
        return {"imagenes": IMAGENES, "cartas": cartas, "oculta": oculta, "intentos": intentos, "solucion": solucion}
    raise SystemExit("sin memoria")


# ------------------------------------------------------------------ el xilófono (la nana)
NOTAS = ["DO", "RE", "MI", "FA", "SOL", "LA", "SI"]
COLORES_NOTA = ["rojo", "naranja", "amarillo", "verde", "azul", "añil", "violeta"]
ORDEN_NANA = ["14", "20", "40", "48", "52"]               # cubos, diferencias, tren, marioneta y oca
NOTA = {"14": "MI", "20": "SOL", "40": "DO", "48": "RE", "52": "LA"}
NANA = [NOTA[k] for k in ORDEN_NANA]

_CACHE = os.path.join(AQUI, "instancias_juguetes.json")
_CLAVES = ("cubos", "estanteria", "torre", "marioneta", "folioscopio", "pista", "clavijas", "oca", "collar", "memoria")


def _funcs():
    return {"cubos": cubos, "estanteria": estanteria, "torre": torre, "marioneta": marioneta, "folioscopio": folioscopio, "pista": pista, "clavijas": clavijas,
            "oca": oca, "collar": collar, "memoria": memoria}


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
    res["nana"] = {"orden": ORDEN_NANA, "notas": NOTA, "melodia": NANA, "colores": dict(zip(NOTAS, COLORES_NOTA))}
    with open(_CACHE, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("OK", f"{time.time() - t0:.0f} s")

"""Instancias con solución comprobada de los 11 puzles de «El Faro de Cabo Niebla» (versión de 60 cartas, 22 oct 2026).

  - puerta:     reloj que atrasa 20 min por hora, puesto en hora a las 12:00 y parado en las 3:20 -> hora real 17:00 (código 1700).
  - banderas:   26 banderas de señales de dibujos inventados (pares casi iguales) y una palabra de seis letras.
  - radio:      frecuencia = 80 + suma de las boyas rojas + décima del viento verdadero (la aguja se pasó dos vientos).
  - morse:      palabra en destellos blancos con destellos rojos de la sirena (que no cuentan).
  - bahia:      Nurikabe 7 x 7 con solución única (islotes numerados; el mar va unido y sin charcos de 2 x 2).
  - sombras:    cuatro cosas del estante en fila para dar la sombra de la pared; ninguna otra cuaterna la da.
  - destellos:  característica de la luz en notación de almanaque, Fl(2+1) 15 s.
  - guardianes: cinco guardianes en cinco literas con nombre y gorro, doce pistas de solución única.
  - laberinto:  desván de 8 x 8 cajas apiladas (laberinto perfecto), se recorre con «avanzar / girar».
  - espejos:    el tablero fijo de 72-espejos.js (solución única comprobada cuando se escribió).
  - meta:       cinco cifras que dejan otros puzles, un orden de arranque en acertijos y una tabla de válvulas.
Escribe herramientas/instancias_faro.json. Uso:  python herramientas/instancias_faro.py"""
import itertools
import json
import os
import random
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import instancias_ampliacion as IA  # noqa: E402

MORSE = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
         "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
         "Y": "-.--", "Z": "--.."}


# ------------------------------------------------------------------ 14 puerta
def puerta():
    atraso, real_min, inicio = 20, 300, (12, 0)
    marca_min = real_min * (60 - atraso) // 60
    assert marca_min == 200 and real_min * (60 - atraso) % 60 == 0
    h = inicio[0] + real_min // 60
    return {"atraso": atraso, "inicio": list(inicio), "parado": [3, 20], "ejemplo": [1, 0, 1, 30 - 0], "real_min": real_min,
            "codigo": f"{h % 24:02d}{real_min % 60:02d}"}


# ------------------------------------------------------------------ 20 banderas
PATRONES = ["mitad_v", "mitad_h", "diagonal", "cruz", "aspa", "marco", "disco", "franjas_v", "franjas_h", "cuartos", "triangulo"]
COLORES_B = ["rojo", "azul", "amarillo", "blanco", "negro"]


def banderas():
    rng = random.Random(2026)
    usados = set()
    base = []
    while len(base) < 13:
        s = (rng.choice(PATRONES), *rng.sample(COLORES_B, 2))
        if s not in usados:
            usados.add(s)
            base.append(s)
    todas = list(base)
    for s in base:                             # una gemela casi igual: cambia el patrón o un color
        for _ in range(50):
            if rng.random() < 0.5:
                g = (rng.choice([p for p in PATRONES if p != s[0]]), s[1], s[2])
            else:
                g = (s[0], s[1], rng.choice([c for c in COLORES_B if c != s[1] and c != s[2]]))
            if g not in usados:
                usados.add(g)
                todas.append(g)
                break
    assert len(todas) == 26
    rng.shuffle(todas)
    letras = {chr(65 + i): {"patron": s[0], "c1": s[1], "c2": s[2]} for i, s in enumerate(todas)}
    return {"palabra": "NIEBLA", "banderas": letras}


# ------------------------------------------------------------------ 40 radio
VIENTOS = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]


def radio():
    rojas, verdes = [4, 3, 4], [2, 5]
    entero = 80 + sum(rojas)
    verdadero = 7
    desvio = 2
    mostrado = (verdadero + desvio) % 8
    return {"objetivo": round(entero + verdadero / 10, 1), "base": 80, "rojas": rojas, "verdes": verdes, "vientos": VIENTOS, "desvio": desvio,
            "mostrado": mostrado, "verdadero": verdadero, "falsas": [95.3, 101.9]}


# ------------------------------------------------------------------ 48 morse
def morse():
    rng = random.Random(48)
    palabra = "BALIZA"
    letras = []
    for ch in palabra:
        simbolos = list(MORSE[ch])
        toks = []
        for i, s in enumerate(simbolos):
            toks.append({"c": "b", "s": s})
            if 0 < i < len(simbolos) - 1 or (len(simbolos) == 2 and i == 0 and rng.random() < 0.3):
                pass
        letras.append(toks)
    # destellos rojos de la sirena: siempre entre dos destellos blancos de la misma letra, y uno al principio del mensaje
    for toks in letras:
        if len(toks) >= 3 and rng.random() < 0.9:
            pos = rng.randint(1, len(toks) - 1)
            toks.insert(pos, {"c": "r", "s": rng.choice([".", "-"])})
    letras[0].insert(0, {"c": "r", "s": "-"})
    assert sum(1 for l in letras for t in l if t["c"] == "r") >= 3
    return {"palabra": palabra, "letras": letras}


# ------------------------------------------------------------------ 52 bahía (Nurikabe 7 x 7)
def bahia():
    rng = random.Random(77)
    n = 7
    for _ in range(300):
        k = rng.randint(6, 8)
        pistas = {}
        while len(pistas) < k:
            p = (rng.randrange(n), rng.randrange(n))
            if all(abs(p[0] - q[0]) + abs(p[1] - q[1]) > 1 for q in pistas):
                pistas[p] = rng.choice([1, 2, 2, 3, 3, 4, 5])
        if not 16 <= sum(pistas.values()) <= 22:
            continue
        sols = IA.nurikabe_soluciones(pistas, n)
        if len(sols) == 1:
            tierra = sorted(set().union(*sols[0]))
            return {"n": n, "pistas": [[f, c, v] for (f, c), v in sorted(pistas.items())], "tierra": [list(x) for x in tierra]}
    raise SystemExit("sin bahía")


# ------------------------------------------------------------------ 46 sombras (cuatro objetos)
def _mascara(nombre):
    return np.asarray(IA.silueta(nombre, 0).crop((0, 0, 120, 160))) > 128


def sombra4(seq):
    m = np.zeros((160, 480), bool)
    for k, nombre in enumerate(seq):
        m[:, 120 * k:120 * k + 120] |= _mascara(nombre)
    return m


def sombras():
    meta = ["botella", "catalejo", "ancla", "campana"]
    obj = sombra4(meta)
    caches = {n: _mascara(n) for n in IA.OBJETOS_SOMBRA}
    iguales = []
    for seq in itertools.permutations(IA.OBJETOS_SOMBRA, 4):
        m = np.zeros((160, 480), bool)
        for k, nombre in enumerate(seq):
            m[:, 120 * k:120 * k + 120] |= caches[nombre]
        if np.count_nonzero(m ^ obj) < 250:
            iguales.append(list(seq))
    assert iguales == [meta], iguales
    return {"objetos": IA.OBJETOS_SOMBRA, "solucion": meta}


# ------------------------------------------------------------------ 51 destellos (característica de la luz)
FAROS = {                                   # grupos de destellos y periodo en segundos
    "Punta Gaviota": ([2], 10),
    "Isla del Moro": ([3], 12),
    "Cabo Niebla": ([2, 1], 15),
    "Roca Negra": ([1], 6),
    "Puerto Viejo": ([4], 15),
    "Cala Azul": ([1, 2], 12),
    "Punta Sal": ([3, 1], 15),
    "Faro del Norte": ([2, 2], 15),
}


def patron_luz(grupos, periodo):
    s = []
    for g, n in enumerate(grupos):
        for d in range(n):
            s += [1]
            if d < n - 1:
                s += [0]
        if g < len(grupos) - 1:
            s += [0, 0, 0]
    assert len(s) < periodo
    return s + [0] * (periodo - len(s))


def notacion(grupos, periodo):
    return "Fl(" + "+".join(str(g) for g in grupos) + ") " + str(periodo) + " s"


def destellos():
    pats = {f: patron_luz(*v) for f, v in FAROS.items()}
    assert len({(tuple(p)) for p in pats.values()}) == len(pats)
    faro = "Cabo Niebla"
    return {"faros": {f: {"grupos": v[0], "periodo": v[1], "notacion": notacion(*v)} for f, v in FAROS.items()}, "faro": faro, "periodo": FAROS[faro][1],
            "solucion": pats[faro]}


# ------------------------------------------------------------------ 64 guardianes (lógica)
NOMBRES = ["Elías", "Nora", "Teo", "Irene", "Bruno"]
GORROS = ["rojo", "azul", "verde", "amarillo", "blanco"]


def _pistas_verdaderas(sol):
    """Pistas (tipo, a, b) ciertas para la solución. Un elemento es ('n', i) nombre o ('g', i) gorro."""
    pos_n = {i: p for p, (i, _) in enumerate(sol)}
    pos_g = {j: p for p, (_, j) in enumerate(sol)}
    el = [("n", i) for i in range(5)] + [("g", j) for j in range(5)]

    def pos(e):
        return pos_n[e[1]] if e[0] == "n" else pos_g[e[1]]
    pistas = []
    for a in el:
        for b in el:
            if a >= b or a[0] == b[0]:
                continue
            if pos(a) == pos(b):
                pistas.append(("mismo", a, b))
    for a in el:
        for b in el:
            if a == b:
                continue
            if pos(a) + 1 == pos(b):
                pistas.append(("izq_inmediata", a, b))
            if pos(a) < pos(b) and pos(b) - pos(a) >= 2:
                pistas.append(("izq_lejos", a, b))
            if a < b and abs(pos(a) - pos(b)) == 1:
                pistas.append(("junto", a, b))
    for a in el:
        if pos(a) == 0:
            pistas.append(("extremo_izq", a, None))
        if pos(a) == 4:
            pistas.append(("extremo_der", a, None))
        if pos(a) == 2:
            pistas.append(("centro", a, None))
    return pistas


def _cumple(p, sol):
    t, a, b = p
    pos_n = {i: q for q, (i, _) in enumerate(sol)}
    pos_g = {j: q for q, (_, j) in enumerate(sol)}

    def pos(e):
        return pos_n[e[1]] if e[0] == "n" else pos_g[e[1]]
    if t == "mismo":
        return pos(a) == pos(b)
    if t == "izq_inmediata":
        return pos(a) + 1 == pos(b)
    if t == "izq_lejos":
        return pos(b) - pos(a) >= 2
    if t == "junto":
        return abs(pos(a) - pos(b)) == 1
    if t == "extremo_izq":
        return pos(a) == 0
    if t == "extremo_der":
        return pos(a) == 4
    return pos(a) == 2


def _soluciones(pistas):
    out = []
    for pn in itertools.permutations(range(5)):
        for pg in itertools.permutations(range(5)):
            sol = list(zip(pn, pg))
            if all(_cumple(p, sol) for p in pistas):
                out.append(sol)
                if len(out) > 1:
                    return out
    return out


def _texto_el(e):
    return NOMBRES[e[1]] if e[0] == "n" else "quien lleva el gorro " + GORROS[e[1]]


def _frase(p):
    t, a, b = p
    A, B = _texto_el(a), _texto_el(b) if b else None
    cap = lambda s: s[0].upper() + s[1:]
    if t == "mismo":
        return cap(A) + " lleva el gorro " + GORROS[b[1]] + "." if a[0] == "n" else cap(B) + " lleva el gorro " + GORROS[a[1]] + "."
    if t == "izq_inmediata":
        return cap(A) + " duerme justo a la izquierda de " + B + "."
    if t == "izq_lejos":
        return cap(A) + " duerme a la izquierda de " + B + ", con al menos una litera de por medio."
    if t == "junto":
        return cap(A) + " duerme en una litera pegada a la de " + B + "."
    if t == "extremo_izq":
        return cap(A) + " duerme en la litera del extremo izquierdo."
    if t == "extremo_der":
        return cap(A) + " duerme en la litera del extremo derecho."
    return cap(A) + " duerme en la litera del centro."


def guardianes():
    rng = random.Random(64)
    for _ in range(200):
        pn, pg = list(range(5)), list(range(5))
        rng.shuffle(pn)
        rng.shuffle(pg)
        sol = list(zip(pn, pg))
        todas = _pistas_verdaderas(sol)
        rng.shuffle(todas)
        elegidas = []
        for p in todas:
            elegidas.append(p)
            if len(_soluciones(elegidas)) == 1:
                break
        else:
            continue
        for p in list(elegidas):                         # quita lo que sobra
            resto = [q for q in elegidas if q != p]
            if len(_soluciones(resto)) == 1:
                elegidas = resto
        if 7 <= len(elegidas) <= 11 and len({t for t, _, _ in elegidas}) >= 3:
            frases = [_frase(p) for p in elegidas]
            return {"nombres": NOMBRES, "gorros": GORROS, "solucion": [[NOMBRES[i], GORROS[j]] for i, j in sol], "frases": frases}
    raise SystemExit("sin guardianes")


# ------------------------------------------------------------------ 69 laberinto del desván
DIRS = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "O": (0, -1)}
OPUESTA = {"N": "S", "S": "N", "E": "O", "O": "E"}


def laberinto():
    n = 8
    for semilla in range(1, 400):
        rng = random.Random(semilla)
        abierto = {(f, c): set() for f in range(n) for c in range(n)}
        vis, pila = {(n - 1, 0)}, [(n - 1, 0)]
        while pila:
            f, c = pila[-1]
            vec = [(d, (f + df, c + dc)) for d, (df, dc) in DIRS.items() if (f + df, c + dc) in abierto and (f + df, c + dc) not in vis]
            if not vec:
                pila.pop()
                continue
            d, q = rng.choice(vec)
            abierto[(f, c)].add(d)
            abierto[q].add(OPUESTA[d])
            vis.add(q)
            pila.append(q)
        meta = (0, n - 1)
        # camino único (laberinto perfecto) por búsqueda
        prev = {(n - 1, 0): None}
        cola = [(n - 1, 0)]
        for u in cola:
            for d in abierto[u]:
                v = (u[0] + DIRS[d][0], u[1] + DIRS[d][1])
                if v not in prev:
                    prev[v] = (u, d)
                    cola.append(v)
        camino, v = [], meta
        while prev[v]:
            u, d = prev[v]
            camino.append(d)
            v = u
        camino.reverse()
        giros = sum(1 for a, b in zip(["N"] + camino, camino) if a != b)
        if not (26 <= len(camino) <= 34 and 12 <= giros <= 18):
            continue
        # órdenes: A avanzar, I girar a la izquierda, D girar a la derecha; se empieza mirando al norte
        orden = "NESO"
        mira, prog = "N", []
        for d in camino:
            dif = (orden.index(d) - orden.index(mira)) % 4
            prog += {0: [], 1: ["D"], 2: ["D", "D"], 3: ["I"]}[dif]
            prog.append("A")
            mira = d
        return {"n": n, "abierto": [["".join(sorted(abierto[(f, c)])) for c in range(n)] for f in range(n)], "inicio": [n - 1, 0], "meta": list(meta),
                "mira": "N", "camino": camino, "solucion": "".join(prog), "semilla": semilla}
    raise SystemExit("sin laberinto")


# ------------------------------------------------------------------ 72 espejos (tablero fijo del minijuego)
def espejos():
    inicial = {"1,3": "\\", "1,2": "\\", "3,2": "\\", "3,1": "/", "6,1": "/", "6,2": "/", "5,2": "\\", "0,5": "/", "0,2": "\\", "7,1": "\\", "7,4": "/"}
    buena = {"1,3": "/", "1,2": "/", "3,2": "/", "3,1": "/", "6,1": "\\", "6,2": "/", "5,2": "/"}
    return {"inicial": inicial, "solucion": buena, "giran": [k for k in buena if buena[k] != inicial[k]], "orden": ["Galería", "Lente", "Lámpara"]}


# ------------------------------------------------------------------ 85 metapuzle
def meta():
    rng = random.Random(85)
    apps = ["14", "20", "40", "48", "52"]
    cifras = dict(zip(apps, rng.sample(range(10), 5)))
    orden = apps[:]
    while orden == apps:
        rng.shuffle(orden)
    tabla = list(range(10))
    rng.shuffle(tabla)
    code = [tabla[cifras[a]] for a in orden]
    assert len(set(code)) == 5
    return {"apps": apps, "cifras": cifras, "orden": orden, "tabla": tabla, "codigo": "".join(str(c) for c in code)}


def main():
    inst = {"puerta": puerta(), "banderas": banderas(), "radio": radio(), "morse": morse(), "bahia": bahia(), "sombras": sombras(), "destellos": destellos(),
            "guardianes": guardianes(), "laberinto": laberinto(), "espejos": espejos(), "meta": meta()}
    for k, v in inst.items():
        print(f"{k:11} OK")
    with open(os.path.join(AQUI, "instancias_faro.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(inst, f, ensure_ascii=False, indent=1)
        f.write("\n")


def _cargar():
    ruta = os.path.join(AQUI, "instancias_faro.json")
    if os.path.exists(ruta):
        return json.load(open(ruta, encoding="utf-8"))
    return {}


INST = _cargar()

if __name__ == "__main__":
    main()

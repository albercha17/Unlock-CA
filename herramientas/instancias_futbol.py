"""Instancias de «La Final del Siglo, 1970: La Copa de Cristal» (versión de 60 cartas, 22 oct 2026), con solución comprobada por código.

Once puzles de fútbol que no salen en ningún otro juego de la serie:
  liguilla      reconstruir cuatro marcadores de una liguilla con la clasificación y los resultados conocidos (2 puntos por victoria)
  cromos        seis cromos con dos caras (anverso: dorsal y nombre; reverso: ficha) y un acertijo del míster que señala a dos jugadores
  var           seis jugadas de fuera de juego dibujadas desde arriba y un reglamento con casos raros (nivel, campo propio, saque de banda, portero adelantado)
  pase          pase en cadena: recorrer siete jugadores, cada uno una vez, sin que un rival o un compañero corte la línea del pase
  alineacion    cinco jugadores, cinco puestos y una tabla de notas: la alineación de suma máxima (no vale lo voraz)
  penaltis      un portero que se lanza según los dos últimos tiros; la regla sale del informe de once penaltis (de Bruijn)
  grada         el mosaico de la grada: cada butaca se pinta según las dos vecinas de la fila anterior (anillo de doce, regla 90)
  calendario    el calendario de una liga de ocho equipos por el método del círculo: los cruces de la jornada 5
  eliminatorias un cuadro de ocho equipos que se reconstruye con titulares de prensa (solución única)
  sustituciones los cambios del míster aplicados tres veces a ocho jugadores (ciclos y permutaciones)
  aros          la cerradura de la Copa: cinco aros de doce posiciones, cada uno con un número que deja un puzle y un giro dibujado
Ejecutarlo comprueba todo y escribe instancias_futbol.json; al importarlo se lee de ahí.
"""
import itertools
import json
import math
import os
import random

AQUI = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ liguilla
EQUIPOS = ["Estrella", "Rayos", "Halcones", "Tigres"]
PARTIDOS = [(a, b) for a in range(4) for b in range(a + 1, 4)]


def clasificacion(res):
    t = [dict(g=0, e=0, p=0, gf=0, gc=0, pts=0) for _ in range(4)]
    for (a, b), (x, y) in zip(PARTIDOS, res):
        t[a]["gf"] += x
        t[a]["gc"] += y
        t[b]["gf"] += y
        t[b]["gc"] += x
        if x > y:
            t[a]["g"] += 1
            t[b]["p"] += 1
            t[a]["pts"] += 2
        elif x < y:
            t[b]["g"] += 1
            t[a]["p"] += 1
            t[b]["pts"] += 2
        else:
            t[a]["e"] += 1
            t[b]["e"] += 1
            t[a]["pts"] += 1
            t[b]["pts"] += 1
    return t


def _cuenta_liguilla(conocidos, tabla, limite=2):
    desconocidos = [i for i in range(6) if i not in conocidos]
    rgf = [tabla[i]["gf"] for i in range(4)]
    rgc = [tabla[i]["gc"] for i in range(4)]
    for i, (x, y) in conocidos.items():
        a, b = PARTIDOS[i]
        rgf[a] -= x
        rgc[b] -= x
        rgf[b] -= y
        rgc[a] -= y
    if min(rgf + rgc) < 0:
        return 0
    opciones = []
    for i in desconocidos:
        a, b = PARTIDOS[i]
        opciones.append([(x, y) for x in range(min(rgf[a], rgc[b]) + 1) for y in range(min(rgf[b], rgc[a]) + 1)])
    n = 0
    for combo in itertools.product(*opciones):
        res = [None] * 6
        for i, r in conocidos.items():
            res[i] = r
        for i, r in zip(desconocidos, combo):
            res[i] = r
        if clasificacion(res) == tabla:
            n += 1
            if n >= limite:
                break
    return n


def liguilla(semilla=1):
    for sem in range(semilla, semilla + 5000):
        rng = random.Random(sem)
        res = [(rng.randint(0, 4), rng.randint(0, 4)) for _ in PARTIDOS]
        tabla = clasificacion(res)
        if len({(r[0] > r[1]) - (r[0] < r[1]) for r in res}) < 3 or sum(x + y for x, y in res) < 9:
            continue
        for conocidos in itertools.combinations(range(6), 2):
            if len({e for i in conocidos for e in PARTIDOS[i]}) < 4:
                continue
            if _cuenta_liguilla({i: res[i] for i in conocidos}, tabla) == 1:
                return {"equipos": EQUIPOS, "partidos": [list(p) for p in PARTIDOS], "resultados": [list(r) for r in res],
                        "conocidos": list(conocidos), "desconocidos": [i for i in range(6) if i not in conocidos], "tabla": tabla}
    raise SystemExit("sin liguilla")


# ------------------------------------------------------------------ cromos de dos caras
POSICIONES = ["portero", "defensa", "medio", "delantero"]
NOMBRES = ["Toni Roca", "Beto Pase", "Paco Guante", "Rafa Gol", "Luis Muro", "Nico Regate", "Mario Eje", "Cesar Remate", "Pepe Banda", "Dani Cierre"]
ATRIBUTOS = {"altura": ("alto", "bajo"), "edad": ("veterano", "joven")}


def _filtros(rng):
    conds = []
    conds.append(rng.choice([("pie", "zurdo"), ("pie", "diestro")]))
    conds.append(rng.choice([("pos", rng.choice(POSICIONES)), ("npos", rng.choice(POSICIONES))]))
    return conds


def _cumple(j, conds):
    for tipo, v in conds:
        if tipo == "pie" and j["pie"] != v:
            return False
        if tipo == "pos" and j["pos"] != v:
            return False
        if tipo == "npos" and j["pos"] == v:
            return False
    return True


def _texto_filtro(conds):
    pie = [v for t, v in conds if t == "pie"]
    pos = [v for t, v in conds if t == "pos"]
    npos = [v for t, v in conds if t == "npos"]
    plural = {"portero": "porteros", "defensa": "defensas", "medio": "medios", "delantero": "delanteros", "zurdo": "zurdos", "diestro": "diestros"}
    if pos and pie:
        base = f"los {plural[pos[0]]} {plural[pie[0]]}"
    elif pos:
        base = f"los {plural[pos[0]]}"
    elif pie:
        base = f"los {plural[pie[0]]}"
    else:
        base = "los jugadores"
    if npos:
        base += (" " if pos or pie else " ") + "que no son " + plural[npos[0]]
        if not (pos or pie):
            base = "los que no son " + plural[npos[0]]
    return base


def cromos(semilla=4):
    for sem in range(semilla, semilla + 20000):
        rng = random.Random(sem)
        pos = ["portero", "defensa", "defensa", "medio", "medio", "delantero"]
        rng.shuffle(pos)
        alturas = rng.sample(range(168, 193), 6)
        edades = rng.sample(range(19, 37), 6)
        dorsales = rng.sample(range(2, 12), 6)
        nombres = rng.sample(NOMBRES, 6)
        jug = [dict(nombre=nombres[i], dorsal=dorsales[i], pos=pos[i], pie=rng.choice(["zurdo", "diestro"]), altura=alturas[i], edad=edades[i]) for i in range(6)]
        if sum(1 for j in jug if j["pie"] == "zurdo") not in (2, 3, 4):
            continue
        claus = []
        for _ in range(60):
            conds = _filtros(rng)
            attr = rng.choice(["altura", "edad"])
            sup = rng.choice([0, 1])
            grupo = [i for i, j in enumerate(jug) if _cumple(j, conds)]
            if len(grupo) < 3:
                continue
            if len({jug[i]['pos'] for i in grupo}) < 2:
                continue
            if attr == "altura":
                key = lambda i: jug[i]["altura"]
            else:
                key = lambda i: jug[i]["edad"]
            elegido = max(grupo, key=key) if sup == 0 else min(grupo, key=key)
            texto = f"el más {ATRIBUTOS[attr][sup]} de {_texto_filtro(conds)}"
            claus.append((elegido, texto, conds, attr, sup))
        distintos = {}
        for c in claus:
            distintos.setdefault(c[0], c)
        if len(distintos) < 2:
            continue
        a, b = rng.sample(sorted(distintos), 2)
        sel = sorted([a, b], key=lambda i: jug[i]["dorsal"])
        return {"jugadores": jug, "tarjetas": [[0, 1, 2], [3, 4, 5]],
                "acertijo": [distintos[a][1], distintos[b][1]], "solucion": [jug[i]["dorsal"] for i in sel]}
    raise SystemExit("sin cromos")


# ------------------------------------------------------------------ VAR: fuera de juego
def decide_var(j):
    """Reglas del reglamento (carta 45): fuera de juego si, en el momento del pase, quien recibe está más cerca de la línea de gol rival que el balón y
    que el penúltimo defensor (el portero cuenta); a la altura de uno no es fuera de juego; en el campo propio (x < 50) no hay; y desde un saque de banda
    tampoco."""
    if j["saque"] == "banda":
        return False
    rx = j["atacantes"][j["receptor"]][1]
    bx = j["atacantes"][j["pasador"]][1]
    xs = sorted([d[1] for d in j["defensores"]], reverse=True)         # el primero es el último defensor (el más cerca de su línea de gol)
    pen = xs[1]
    if rx < 50:
        return False
    return rx > pen and rx > bx


def jugadas():
    """Seis jugadas de 100 × 60 con atacantes (A a D), cuatro defensores (el primero, el portero) y un balón; atacan hacia la derecha."""
    def J(saque, atac, defe, pasador, receptor):
        return {"saque": saque, "atacantes": atac, "defensores": defe, "pasador": pasador, "receptor": receptor}
    js = [
        # A: portero adelantado (el penúltimo defensor es el portero, que ha salido) -> fuera de juego
        J("juego", [["A", 55, 30], ["B", 40, 15], ["C", 85, 40], ["D", 60, 50]],
          [["P", 80, 30], ["1", 90, 20], ["2", 65, 45], ["3", 60, 15]], 0, 2),
        # B: a la altura del penúltimo defensor -> válida
        J("juego", [["A", 50, 30], ["B", 35, 40], ["C", 75, 20], ["D", 60, 52]],
          [["P", 95, 30], ["1", 75, 45], ["2", 60, 12], ["3", 50, 28]], 0, 2),
        # C: por poco (5 unidades) -> fuera de juego
        J("juego", [["A", 45, 25], ["B", 30, 45], ["C", 70, 35], ["D", 85, 10]],
          [["P", 95, 30], ["1", 65, 40], ["2", 60, 20], ["3", 55, 50]], 0, 2),
        # D: campo propio (x < 50): los defensas están adelantados -> válida
        J("juego", [["A", 20, 30], ["B", 25, 50], ["C", 40, 20], ["D", 15, 10]],
          [["P", 95, 30], ["1", 30, 40], ["2", 25, 12], ["3", 20, 25]], 0, 2),
        # E: el balón va por delante de quien recibe -> válida
        J("juego", [["A", 85, 30], ["B", 50, 40], ["C", 78, 12], ["D", 60, 50]],
          [["P", 95, 30], ["1", 70, 45], ["2", 65, 20], ["3", 60, 38]], 0, 2),
        # F: saque de banda con quien recibe muy adelantado -> válida
        J("banda", [["A", 60, 0], ["B", 55, 35], ["C", 90, 25], ["D", 45, 15]],
          [["P", 95, 30], ["1", 75, 40], ["2", 70, 20], ["3", 65, 45]], 0, 2),
    ]
    for j in js:
        assert len({tuple(p[1:]) for p in j["atacantes"] + j["defensores"]}) == 8, "dos jugadores en el mismo sitio"
    return {"jugadas": js, "fuera": [decide_var(j) for j in js]}


# ------------------------------------------------------------------ pase en cadena
ANCHO_P, ALTO_P = 14, 8


def _entre(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    g = math.gcd(abs(dx), abs(dy))
    if g < 2:
        return []
    return [(p[0] + k * dx // g, p[1] + k * dy // g) for k in range(1, g)]


def _aristas(nodos, rivales):
    ocupados = set(rivales) | set(nodos)
    ar = set()
    bloqueadas = []
    for i in range(len(nodos)):
        for j in range(i + 1, len(nodos)):
            if any(q in ocupados for q in _entre(nodos[i], nodos[j])):
                bloqueadas.append((i, j))
            else:
                ar.add((i, j))
                ar.add((j, i))
    return ar, bloqueadas


def _caminos(n, ar, ini, fin):
    res = []
    for perm in itertools.permutations([k for k in range(n) if k not in (ini, fin)]):
        c = [ini] + list(perm) + [fin]
        if all((a, b) in ar for a, b in zip(c, c[1:])):
            res.append(c)
    return res


def pase(semilla=11):
    for sem in range(semilla, semilla + 200000):
        rng = random.Random(sem)
        nodos = [(rng.choice([0, 1, 2]), rng.randint(1, ALTO_P - 1))]
        for _ in range(5):
            nodos.append((rng.randint(1, ANCHO_P - 1), rng.randint(0, ALTO_P)))
        nodos.append((rng.choice([12, 13, 14]), rng.randint(1, ALTO_P - 1)))
        if len(set(nodos)) < 7 or any(x == 7 for x, _ in nodos):
            continue
        medios = []
        for i in range(7):
            for j in range(i + 1, 7):
                medios += _entre(nodos[i], nodos[j])
        medios = [m for m in set(medios) if m not in nodos and m[0] != 7]
        if len(medios) < 6:
            continue
        rivales = rng.sample(sorted(medios), 6)
        ar, bloq = _aristas(nodos, rivales)
        if len(bloq) < 8:
            continue
        cs = _caminos(7, ar, 0, 6)
        if len(cs) == 1:
            return {"ancho": ANCHO_P, "alto": ALTO_P, "jugadores": [list(n) for n in nodos], "rivales": [list(r) for r in rivales],
                    "camino": cs[0], "bloqueadas": [list(b) for b in bloq]}
    raise SystemExit("sin pase")


# ------------------------------------------------------------------ alineación óptima (asignación)
JUGADORES_ALI = ["Toni", "Beto", "Rafa", "Luis", "Nico"]
PUESTOS = ["Portero", "Defensa", "Lateral", "Medio", "Delantero"]


def _mejor(notas):
    n = len(notas)
    todas = sorted(((sum(notas[i][p[i]] for i in range(n)), p) for p in itertools.permutations(range(n))), reverse=True)
    return todas


def _voraz_puestos(notas):
    """El método de «el mejor para cada puesto, de izquierda a derecha»."""
    n = len(notas)
    libres = set(range(n))
    tot = 0
    for p in range(n):
        i = max(libres, key=lambda i: notas[i][p])
        libres.discard(i)
        tot += notas[i][p]
    return tot


def alineacion(semilla=5):
    for sem in range(semilla, semilla + 50000):
        rng = random.Random(sem)
        notas = [[rng.randint(2, 9) for _ in range(5)] for _ in range(5)]
        todas = _mejor(notas)
        mejor, perm = todas[0]
        if todas[1][0] == mejor:
            continue
        v = _voraz_puestos(notas)
        filas = sum(max(r) for r in notas)
        if mejor - v >= 2 and filas != mejor and mejor - todas[1][0] >= 1:
            return {"jugadores": JUGADORES_ALI, "puestos": PUESTOS, "notas": notas, "maximo": mejor, "solucion": list(perm), "voraz": v}
    raise SystemExit("sin alineación")


# ------------------------------------------------------------------ penaltis (regla de los dos últimos tiros)
BRUIJN = [0, 0, 1, 0, 2, 1, 1, 2, 2, 0]


def penaltis(semilla=2):
    rng = random.Random(semilla)
    for _ in range(10000):
        g = {(a, b): rng.randint(0, 2) for a in range(3) for b in range(3)}
        if len(set(g.values())) == 3 and sum(1 for k, v in g.items() if v == k[1]) <= 3:
            break
    kicks = BRUIJN + [rng.randint(0, 2)]
    dives = [rng.randint(0, 2), rng.randint(0, 2)]
    for t in range(2, len(kicks)):
        dives.append(g[(kicks[t - 2], kicks[t - 1])])
    historial = [{"tiro": k, "salto": d, "gol": k != d} for k, d in zip(kicks, dives)]
    return {"regla": {f"{a}{b}": v for (a, b), v in g.items()}, "historial": historial, "tanda": 5, "ultimos": [kicks[-2], kicks[-1]]}


# ------------------------------------------------------------------ mosaico de la grada (regla 90 en un anillo)
def paso_grada(fila):
    n = len(fila)
    return [fila[(i - 1) % n] ^ fila[(i + 1) % n] for i in range(n)]


def grada(semilla=3, n=12, pasos=6):
    for sem in range(semilla, semilla + 5000):
        rng = random.Random(sem)
        f = [rng.randint(0, 1) for _ in range(n)]
        filas = [f]
        for _ in range(pasos):
            filas.append(paso_grada(filas[-1]))
        if 4 <= sum(filas[-1]) <= 8 and 4 <= sum(f) <= 8 and filas[-1] != f and all(sum(r) > 0 for r in filas):
            return {"n": n, "filas": filas, "inicio": f, "final": filas[-1], "pasos": pasos}
    raise SystemExit("sin grada")


# ------------------------------------------------------------------ calendario (método del círculo)
CLUBES = ["Estrella", "Rayos", "Halcones", "Tigres", "Delfines", "Lobos", "Osos", "Cóndores"]


def jornada(orden, k):
    """Posiciones 0 a 3 en la fila de arriba (de izquierda a derecha) y 4 a 7 en la de abajo (de derecha a izquierda). Cada jornada todos giran un puesto en
    el sentido de las agujas del reloj, salvo el de la posición 0, que se queda."""
    pos = list(orden)
    for _ in range(k):
        pos = [pos[0]] + [pos[7]] + pos[1:7]
    return pos


def cruces(pos):
    return [[pos[i], pos[7 - i]] for i in range(4)]


def calendario(semilla=4, jornada_pedida=5):
    rng = random.Random(semilla)
    orden = list(range(8))
    rng.shuffle(orden)
    todas = [cruces(jornada(orden, k)) for k in range(7)]
    vistos = {tuple(sorted(tuple(sorted(c)) for c in cr)) for cr in todas}
    assert len(vistos) == 7
    # todos los cruces distintos entre sí (cada pareja se ve una sola vez)
    parejas = [tuple(sorted(c)) for cr in todas for c in cr]
    assert len(set(parejas)) == 28
    k = jornada_pedida - 1
    return {"clubes": CLUBES, "orden": orden, "jornada1": todas[0], "jornada": jornada_pedida, "solucion": todas[k]}


# ------------------------------------------------------------------ cuadro de eliminatorias
EQ8 = ["Estrella", "Rayos", "Halcones", "Tigres", "Delfines", "Lobos", "Osos", "Cóndores"]


def jugar_cuadro(bits):
    """bits: siete resultados (0 = gana el primero, 1 = el segundo) en el orden cuartos 1-4, semifinales 1-2, final. Devuelve ganadores y perdedores."""
    cuartos = [(2 * i, 2 * i + 1) for i in range(4)]
    ganq = [cuartos[i][bits[i]] for i in range(4)]
    perq = [cuartos[i][1 - bits[i]] for i in range(4)]
    semis = [(ganq[0], ganq[1]), (ganq[2], ganq[3])]
    gans = [semis[i][bits[4 + i]] for i in range(2)]
    pers = [semis[i][1 - bits[4 + i]] for i in range(2)]
    fin = (gans[0], gans[1])
    camp, sub = fin[bits[6]], fin[1 - bits[6]]
    return {"cuartos": cuartos, "semis": semis, "final": fin, "campeon": camp, "subcampeon": sub, "pierde_cuartos": perq, "pierde_semis": pers}


def verdades(bits):
    r = jugar_cuadro(bits)
    v = []
    for t in r["pierde_cuartos"]:
        v.append(("cae_cuartos", t))
    for t in r["pierde_semis"]:
        v.append(("cae_semis", t))
    v.append(("campeon", r["campeon"]))
    v.append(("subcampeon", r["subcampeon"]))
    for (a, b), g in zip(r["cuartos"], [r["cuartos"][i][bits[i]] for i in range(4)]):
        v.append(("vence", g, b if g == a else a))
    for (a, b), g in zip(r["semis"], [r["semis"][i][bits[4 + i]] for i in range(2)]):
        v.append(("vence", g, b if g == a else a))
    f = r["final"]
    v.append(("vence", r["campeon"], r["subcampeon"]))
    for t in range(8):
        if t not in (r["campeon"], r["subcampeon"]):
            v.append(("no_final", t))
    return v


def _consistente(bits, enunciados):
    vs = set(verdades(bits))
    return all(e in vs for e in enunciados)


def eliminatorias(semilla=6):
    todos = list(itertools.product([0, 1], repeat=7))
    for sem in range(semilla, semilla + 20000):
        rng = random.Random(sem)
        bits = tuple(rng.randint(0, 1) for _ in range(7))
        ver = verdades(bits)
        rng.shuffle(ver)
        elegidos = []
        for e in ver:
            elegidos.append(e)
            n = sum(1 for b in todos if _consistente(b, elegidos))
            if n == 1:
                break
        if len(elegidos) < 5 or len(elegidos) > 7:
            continue
        # sin enunciados redundantes
        mini = list(elegidos)
        for e in list(mini):
            resto = [x for x in mini if x != e]
            if sum(1 for b in todos if _consistente(b, resto)) == 1:
                mini = resto
        if len(mini) < 5:
            continue
        r = jugar_cuadro(bits)
        return {"equipos": EQ8, "bits": list(bits), "enunciados": [list(e) for e in mini], "campeon": r["campeon"]}
    raise SystemExit("sin cuadro")


# ------------------------------------------------------------------ sustituciones (permutaciones)
def sustituciones(semilla=8):
    rng = random.Random(semilla)
    for _ in range(100000):
        dorsales = rng.sample(range(1, 12), 8)
        ciclo3 = rng.sample(range(8), 3)
        par = rng.sample(range(8), 2)
        ciclo3b = rng.sample(range(8), 3)
        repeticiones = 3
        ops = [("ciclo", ciclo3), ("cambio", par), ("ciclo", ciclo3b)]
        sit = list(dorsales)
        pasos = [list(sit)]
        for _ in range(repeticiones):
            for tipo, p in ops:
                if tipo == "ciclo":
                    a, b, c = p
                    sit[a], sit[b], sit[c] = sit[c], sit[a], sit[b]       # el del puesto a pasa al b, el de b al c y el de c al a
                else:
                    a, b = p
                    sit[a], sit[b] = sit[b], sit[a]
            pasos.append(list(sit))
        mov = sum(1 for i in range(8) if sit[i] != dorsales[i])
        if mov >= 6 and len({tuple(s) for s in pasos}) == 4 and len(set(ciclo3) & set(ciclo3b)) >= 1:
            return {"dorsales": dorsales, "ops": [[t, [q + 1 for q in p]] for t, p in ops], "repeticiones": repeticiones, "final": sit}
    raise SystemExit("sin sustituciones")


# ------------------------------------------------------------------ aros de la Copa
ORDEN_ARO = ["14", "40", "52", "69", "72"]               # liguilla, VAR, alineación, sustituciones, grada
ARO = {"14": 7, "40": 11, "52": 4, "69": 9, "72": 2}
GIRO = {"14": 3, "40": -2, "52": 5, "69": -4, "72": 1}


def posicion_aro(k):
    return (ARO[k] + GIRO[k] - 1) % 12 + 1


FINAL_ARO = [posicion_aro(k) for k in ORDEN_ARO]

_CACHE = os.path.join(AQUI, "instancias_futbol.json")
_CLAVES = ("liguilla", "cromos", "var", "pase", "alineacion", "penaltis", "grada", "calendario", "eliminatorias", "sustituciones")


def _funcs():
    return {"liguilla": liguilla, "cromos": cromos, "var": jugadas, "pase": pase, "alineacion": alineacion, "penaltis": penaltis, "grada": grada,
            "calendario": calendario, "eliminatorias": eliminatorias, "sustituciones": sustituciones}


def _construir():
    f = _funcs()
    return {k: f[k]() for k in _CLAVES}


if __name__ != "__main__" and os.path.exists(_CACHE):
    _C = json.load(open(_CACHE, encoding="utf-8"))
    LIGUILLA, CROMOS, VAR, PASE, ALINEACION, PENALTIS, GRADA, CALENDARIO, ELIMINATORIAS, SUSTITUCIONES = (_C[k] for k in _CLAVES)
elif __name__ != "__main__" and not os.environ.get("INSTANCIAS_SIN_CACHE"):
    _C = _construir()
    LIGUILLA, CROMOS, VAR, PASE, ALINEACION, PENALTIS, GRADA, CALENDARIO, ELIMINATORIAS, SUSTITUCIONES = (_C[k] for k in _CLAVES)

if __name__ == "__main__":
    import time
    t0 = time.time()
    res = {}
    for k, f in _funcs().items():
        t = time.time()
        res[k] = f()
        print(f"{k:14s} OK ({time.time() - t:.1f} s)")
    json.dump(res, open(_CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    print("aros finales:", FINAL_ARO)
    print("OK", f"{time.time() - t0:.0f} s")

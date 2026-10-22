"""Instancias de «Montecarlo, 1965: Operación Cristal» (versión de 60 cartas, 22 oct 2026), con solución comprobada por código.

Once puzles que no salen en ningún otro juego de la serie:
  criptograma  la nota de la Agente Zorro: sustitución simple con las letras de AGENTE de pista
  ruta         la persecución: el camino más rápido por las calles de Montecarlo con dos cruces cortados por el desfile
  rascacielos  el skyline 5 x 5 con las pistas del borde repartidas en dos cartas
  libro        la cifra del libro: página, renglón y palabra en dos páginas de una novela
  kenken       la caja fuerte: cuadrado latino 5 x 5 con jaulas y operaciones
  conteo       el crupier: la cuenta de cartas del blackjack (alta-baja)
  pasaporte    los pasaportes falsos: el dígito de control de la zona de lectura mecánica (pesos 7-3-1)
  husos        el vuelo con escalas: hora de llegada a Montecarlo sumando husos horarios
  cables       el desactivador: tres cargas con un manual de reglas condicionales
  ruleta       la martingala: cuánto queda en el banco tras doce giros
  teclado      el teléfono rojo: la palabra final con las pulsaciones de cinco puzles (teclado multitoque)
Ejecutarlo comprueba todo y escribe instancias_espia.json; al importarlo se lee de ahí.
"""
import itertools
import json
import os
import random
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ criptograma (sustitución simple)
def criptograma(semilla=3, claro="AGENTE ZORRO ESPERA EN EL MUELLE DE LA RULETA AZUL"):
    rng = random.Random(semilla)
    letras = sorted(set(claro.replace(" ", "")))
    for _ in range(1000):
        perm = letras[:]
        rng.shuffle(perm)
        if all(a != b for a, b in zip(letras, perm)):
            break
    clave = dict(zip(letras, perm))
    cif = "".join(clave.get(c, c) for c in claro)
    assert "".join({v: k for k, v in clave.items()}.get(c, c) for c in cif) == claro
    return {"claro": claro, "cifrado": cif, "clave": clave, "pista": "AGENTE"}


# ------------------------------------------------------------------ kenken
def _latino(n, rng):
    # cuadrado latino por barajado de filas y columnas de uno cíclico
    base = [[(i + j) % n + 1 for j in range(n)] for i in range(n)]
    pf, pc, pv = list(range(n)), list(range(n)), list(range(1, n + 1))
    rng.shuffle(pf)
    rng.shuffle(pc)
    rng.shuffle(pv)
    return [[pv[base[pf[i]][pc[j]] - 1] for j in range(n)] for i in range(n)]


def _jaulas(n, rng):
    libres = {(r, c) for r in range(n) for c in range(n)}
    orden = list(libres)
    rng.shuffle(orden)
    jaulas = []
    for q in orden:
        if q not in libres:
            continue
        tam = rng.choice([1, 2, 2, 2, 3, 3])
        cage = [q]
        libres.discard(q)
        while len(cage) < tam:
            vec = [(r + dr, c + dc) for r, c in cage for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (r + dr, c + dc) in libres]
            if not vec:
                break
            nxt = rng.choice(vec)
            cage.append(nxt)
            libres.discard(nxt)
        jaulas.append(cage)
    return jaulas


def _eval_jaula(op, objetivo, vals):
    if op == "=":
        return vals[0] == objetivo
    if op == "+":
        return sum(vals) == objetivo
    if op == "x":
        p = 1
        for v in vals:
            p *= v
        return p == objetivo
    if op == "-":
        return abs(vals[0] - vals[1]) == objetivo
    if op == "/":
        a, b = max(vals), min(vals)
        return a % b == 0 and a // b == objetivo
    return False


def _kenken_cuenta(n, jaulas, limite=2):
    cell_jaula = {}
    for k, j in enumerate(jaulas):
        for q in j["celdas"]:
            cell_jaula[tuple(q)] = k
    g = [[0] * n for _ in range(n)]
    cuenta = [0]

    def ok(r, c):
        j = jaulas[cell_jaula[(r, c)]]
        vals = [g[a][b] for a, b in j["celdas"]]
        if 0 in vals:
            if j["op"] == "+" and sum(vals) >= j["objetivo"]:
                return False
            return True
        return _eval_jaula(j["op"], j["objetivo"], vals)

    def rec(i):
        if cuenta[0] >= limite:
            return
        if i == n * n:
            cuenta[0] += 1
            return
        r, c = divmod(i, n)
        for v in range(1, n + 1):
            if any(g[r][k] == v for k in range(c)) or any(g[k][c] == v for k in range(r)):
                continue
            g[r][c] = v
            if ok(r, c):
                rec(i + 1)
            g[r][c] = 0
    rec(0)
    return cuenta[0]


def kenken(n=5):
    for sem in range(2000):
        rng = random.Random(sem)
        sol = _latino(n, rng)
        jaulas = []
        for cage in _jaulas(n, rng):
            vals = [sol[r][c] for r, c in cage]
            if len(cage) == 1:
                op, obj = "=", vals[0]
            elif len(cage) == 2:
                a, b = max(vals), min(vals)
                cand = [("+", a + b), ("x", a * b), ("-", a - b)] + ([("/", a // b)] if a % b == 0 else [])
                op, obj = rng.choice(cand)
            else:
                p = 1
                for v in vals:
                    p *= v
                op, obj = rng.choice([("+", sum(vals)), ("x", p)])
            jaulas.append({"celdas": [list(q) for q in cage], "op": op, "objetivo": obj})
        if len(jaulas) < 9 or sum(1 for j in jaulas if j["op"] == "=") > 2:
            continue
        if _kenken_cuenta(n, jaulas) == 1:
            return {"n": n, "jaulas": jaulas, "solucion": sol}
    raise SystemExit("sin kenken")


# ------------------------------------------------------------------ conteo de cartas (alta-baja)
RANGOS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
PALOS = ["picas", "corazones", "diamantes", "treboles"]


def valor_cuenta(r):
    return 1 if r in ("2", "3", "4", "5", "6") else (0 if r in ("7", "8", "9") else -1)


def conteo(semilla=5, n=28, corte=14):
    for sem in range(semilla, semilla + 5000):
        rng = random.Random(sem)
        mazo = [(r, p) for r in RANGOS for p in PALOS]
        rng.shuffle(mazo)
        cartas = mazo[:n]
        c1 = sum(valor_cuenta(r) for r, _ in cartas[:corte])
        c2 = sum(valor_cuenta(r) for r, _ in cartas)
        if c1 != 0 and c2 != 0 and c1 != c2 and abs(c1) >= 2 and abs(c2) >= 2 and sum(1 for r, _ in cartas if valor_cuenta(r) == 0) >= 5:
            return {"cartas": [list(c) for c in cartas], "corte": corte, "cuenta_corte": c1, "cuenta_final": c2}
    raise SystemExit("sin conteo")


# ------------------------------------------------------------------ pasaporte (dígito de control de la zona de lectura mecánica)
def valor_mrz(ch):
    if ch.isdigit():
        return int(ch)
    if ch == "<":
        return 0
    return ord(ch) - 55


def digito_control(texto):
    return sum(valor_mrz(c) * (7, 3, 1)[i % 3] for i, c in enumerate(texto)) % 10


def pasaportes(semilla=9):
    rng = random.Random(semilla)
    nombres = [("PEREZ", "ELENA"), ("MOREAU", "LUCAS"), ("ROSSI", "CARLA")]
    docs = []
    for ap, no in nombres:
        while True:
            doc = "".join(rng.choice("ABCDEFGHJKLMNPRSTUVXYZ") if rng.random() < 0.45 else str(rng.randint(0, 9)) for _ in range(9))
            if sum(c.isalpha() for c in doc) >= 3 and sum(c.isdigit() for c in doc) >= 3:
                break
        nac = f"{rng.randint(40, 70):02d}{rng.randint(1, 12):02d}{rng.randint(1, 28):02d}"
        ven = f"{rng.randint(66, 75):02d}{rng.randint(1, 12):02d}{rng.randint(1, 28):02d}"
        docs.append({"apellido": ap, "nombre": no, "doc": doc, "nac": nac, "ven": ven, "control_doc": digito_control(doc),
                     "control_nac": digito_control(nac), "control_ven": digito_control(ven)})
    return {"pasaportes": docs, "digitos": [d["control_doc"] for d in docs], "ejemplo": {"doc": "AB123<<<<", "control": digito_control("AB123<<<<")}}


# ------------------------------------------------------------------ husos horarios
CIUDADES = {"Nueva York": -5, "Londres": 0, "Roma": 1, "El Cairo": 2, "Montecarlo": 1, "Tokio": 9, "Bombay": 5.5}


def husos(semilla=2):
    # Tokio -> Bombay -> El Cairo -> Montecarlo (de este a oeste, con escalas)
    salida = {"ciudad": "Tokio", "dia": 0, "hora": 21, "min": 40}
    tramos = [{"de": "Tokio", "a": "Bombay", "dur": [9, 25], "escala": [2, 50]},
              {"de": "Bombay", "a": "El Cairo", "dur": [5, 45], "escala": [3, 15]},
              {"de": "El Cairo", "a": "Montecarlo", "dur": [4, 35], "escala": [0, 0]}]
    t = salida["hora"] * 60 + salida["min"] - int(CIUDADES["Tokio"] * 60)        # minutos UTC desde el día 0
    for tr in tramos:
        t += tr["dur"][0] * 60 + tr["dur"][1] + tr["escala"][0] * 60 + tr["escala"][1]
    local = t + int(CIUDADES["Montecarlo"] * 60)
    dia, resto = divmod(local, 24 * 60)
    return {"ciudades": CIUDADES, "salida": salida, "tramos": tramos, "llegada": {"dia": dia, "hora": resto // 60, "min": resto % 60}}


# ------------------------------------------------------------------ ruta más rápida
def _dijkstra(adj, ini, fin, cerrados):
    import heapq
    dist = {ini: 0}
    cola = [(0, ini)]
    while cola:
        d, u = heapq.heappop(cola)
        if u == fin:
            return d
        if d > dist.get(u, 1e9):
            continue
        for v, w in adj[u]:
            if v in cerrados:
                continue
            nd = d + w
            if nd < dist.get(v, 1e9):
                dist[v] = nd
                heapq.heappush(cola, (nd, v))
    return None


def _caminos(adj, ini, fin, cerrados):
    res = []

    def rec(u, vis, coste):
        if u == fin:
            res.append((coste, list(vis)))
            return
        for v, w in adj[u]:
            if v not in vis and v not in cerrados:
                vis.append(v)
                rec(v, vis, coste + w)
                vis.pop()
    rec(ini, [ini], 0)
    return sorted(res)


def ruta(semilla=7):
    letras = "ABCDEFGHI"
    for sem in range(semilla, semilla + 20000):
        rng = random.Random(sem)
        aristas = {}
        for r in range(3):
            for c in range(3):
                k = r * 3 + c
                if c < 2:
                    aristas[(k, k + 1)] = rng.randint(2, 9)
                if r < 2:
                    aristas[(k, k + 3)] = rng.randint(2, 9)
                if r < 2 and c < 2 and rng.random() < 0.5:
                    aristas[(k, k + 4)] = rng.randint(3, 11)
                if r < 2 and c > 0 and rng.random() < 0.3:
                    aristas[(k, k + 2)] = rng.randint(3, 11)
        adj = {k: [] for k in range(9)}
        for (a, b), w in aristas.items():
            adj[a].append((b, w))
            adj[b].append((a, w))
        cerrados = set(rng.sample([1, 3, 4, 5, 7], 2))
        sin = _caminos(adj, 0, 8, set())
        con = _caminos(adj, 0, 8, cerrados)
        if not sin or not con:
            continue
        if sin[0][0] == con[0][0] or len(con) < 2 or con[0][0] == con[1][0] or len(con[0][1]) < 5:
            continue
        if len(sin) < 2 or sin[0][1] == con[0][1]:
            continue
        return {"nodos": list(letras), "aristas": [[a, b, w] for (a, b), w in sorted(aristas.items())], "cerrados": sorted(cerrados),
                "mejor": con[0][0], "camino": con[0][1], "sin_cierre": sin[0][0]}
    raise SystemExit("sin ruta")


# ------------------------------------------------------------------ rascacielos 5 x 5
def _pistas_lineas(g):
    n = len(g)

    def vis(linea):
        m = c = 0
        for v in linea:
            if v > m:
                m = v
                c += 1
        return c
    return {"N": [vis([g[r][c] for r in range(n)]) for c in range(n)], "S": [vis([g[r][c] for r in range(n - 1, -1, -1)]) for c in range(n)],
            "O": [vis(g[r]) for r in range(n)], "E": [vis(g[r][::-1]) for r in range(n)]}


def _rasc_cuenta(n, pistas, limite=2):
    g = [[0] * n for _ in range(n)]
    cuenta = [0]

    def vis(linea):
        m = c = 0
        for v in linea:
            if v > m:
                m = v
                c += 1
        return c

    def lineas_ok(r, c):
        if c == n - 1:                     # fila completa
            if pistas["O"][r] and vis(g[r]) != pistas["O"][r]:
                return False
            if pistas["E"][r] and vis(g[r][::-1]) != pistas["E"][r]:
                return False
        if r == n - 1:                     # columna completa
            col = [g[i][c] for i in range(n)]
            if pistas["N"][c] and vis(col) != pistas["N"][c]:
                return False
            if pistas["S"][c] and vis(col[::-1]) != pistas["S"][c]:
                return False
        return True

    def rec(i):
        if cuenta[0] >= limite:
            return
        if i == n * n:
            cuenta[0] += 1
            return
        r, c = divmod(i, n)
        for v in range(1, n + 1):
            if any(g[r][k] == v for k in range(c)) or any(g[k][c] == v for k in range(r)):
                continue
            g[r][c] = v
            if lineas_ok(r, c):
                rec(i + 1)
            g[r][c] = 0
    rec(0)
    return cuenta[0]


def rascacielos(semilla=6, n=5):
    rng = random.Random(semilla)
    for _ in range(200):
        sol = _latino(n, rng)
        pistas = _pistas_lineas(sol)
        if _rasc_cuenta(n, pistas) != 1:
            continue
        # quitar pistas mientras siga siendo única
        todas = [(lado, i) for lado in "NSOE" for i in range(n)]
        rng.shuffle(todas)
        for lado, i in todas:
            guardada = pistas[lado][i]
            pistas[lado][i] = 0
            if _rasc_cuenta(n, pistas) != 1:
                pistas[lado][i] = guardada
        total = sum(1 for lado in "NSOE" for v in pistas[lado] if v)
        if total <= 12:
            return {"n": n, "pistas": pistas, "solucion": sol}
    raise SystemExit("sin rascacielos")


# ------------------------------------------------------------------ cifra del libro
PAGINAS = {
    17: ["La noche caía sobre Montecarlo mientras", "el agente caminaba despacio por el puerto", "sin mirar atrás. En la esquina del muelle",
         "una mujer con gafas oscuras vendía flores", "y escondía un mensaje bajo cada ramo.", "Nadie en el casino sospechaba que la ruleta",
         "giraba para ocultar un secreto mucho mayor.", "Entre fichas y copas de champán, un reloj", "marcaba la hora exacta de la partida."],
    18: ["El capitán del yate esperaba en cubierta", "con la mirada fija en las luces del paseo.", "Su cargamento brillaba más que las estrellas:",
         "gemas robadas de museos de media Europa.", "Cuando sonó la sirena, el cristal azul", "desapareció dentro de una caja de caoba.",
         "Solo una llave dorada podía abrirla,", "y la llave dormía bajo la mesa del tahúr.", "Nadie volvió a verla antes del amanecer."],
}
MENSAJE = [(18, 5, 6), (17, 5, 5), (17, 6, 7), (17, 6, 8)]


def _limpio(t):
    import unicodedata
    t = unicodedata.normalize("NFD", t)
    return "".join(c for c in t if c.isalpha() and unicodedata.category(c) != "Mn").upper()


def libro():
    palabras = []
    for p, l, w in MENSAJE:
        palabras.append(_limpio(PAGINAS[p][l - 1].split()[w - 1]))
    return {"paginas": {str(k): v for k, v in PAGINAS.items()}, "mensaje": [list(m) for m in MENSAJE], "claro": " ".join(palabras)}


# ------------------------------------------------------------------ cables (el desactivador)
COLORES = ["rojo", "azul", "amarillo", "negro", "blanco"]
REGLAS_TXT = [
    "Si no hay ningún cable rojo, cortad el segundo cable.",
    "Si el último cable es blanco y hay más de un cable azul, cortad el último cable azul.",
    "Si hay exactamente un cable amarillo y más de un cable negro, cortad el primer cable.",
    "Si el primer cable es negro, cortad el último cable rojo.",
    "Si hay más de dos cables blancos, cortad el primer cable blanco.",
    "En cualquier otro caso, cortad el cuarto cable.",
]


def _ultimo(c, col):
    return max(i for i, x in enumerate(c) if x == col)


def regla_cables(c):
    """Devuelve (índice de la regla, índice del cable a cortar) para una carga de cables."""
    if "rojo" not in c:
        return 0, 1
    if c[-1] == "blanco" and c.count("azul") > 1:
        return 1, _ultimo(c, "azul")
    if c.count("amarillo") == 1 and c.count("negro") > 1:
        return 2, 0
    if c[0] == "negro":
        return 3, _ultimo(c, "rojo")
    if c.count("blanco") > 2:
        return 4, c.index("blanco")
    return 5, 3


def cables(semilla=4):
    rng = random.Random(semilla)
    for _ in range(100000):
        cargas = []
        usadas = set()
        for objetivo in rng.sample([1, 2, 3, 4, 5], 4):
            for _ in range(2000):
                c = [rng.choice(COLORES) for _ in range(6)]
                if regla_cables(c)[0] == objetivo:
                    cargas.append(c)
                    break
        if len(cargas) == 4:
            res = [regla_cables(c) for c in cargas]
            return {"reglas": REGLAS_TXT, "cargas": [{"cables": c, "regla": r, "corta": k} for c, (r, k) in zip(cargas, res)]}
    raise SystemExit("sin cables")


# ------------------------------------------------------------------ ruleta (la martingala)
def ruleta(semilla=3, giros=12, banco=100, base=5):
    for sem in range(semilla, semilla + 20000):
        rng = random.Random(sem)
        res = [rng.choice("RRNNNV") for _ in range(giros)]
        b, apuesta, ok, racha, maxracha = banco, base, True, 0, 0
        for x in res:
            if apuesta > b:
                ok = False
                break
            if x == "R":
                b += apuesta
                apuesta = base
                racha = 0
            else:
                b -= apuesta
                apuesta *= 2
                racha += 1
                maxracha = max(maxracha, racha)
        if ok and maxracha >= 3 and "V" in res and b != banco and b > 0:
            return {"resultados": res, "banco": banco, "base": base, "final": b}
    raise SystemExit("sin ruleta")


# ------------------------------------------------------------------ teléfono rojo (multitoque)
TECLADO = {"2": "ABC", "3": "DEF", "4": "GHI", "5": "JKL", "6": "MNO", "7": "PQRS", "8": "TUV", "9": "WXYZ"}
PALABRA = "ZARPA"
ORDEN = ["14", "40", "52", "69", "51"]                  # criptograma, rascacielos, kenken, cables y pasaporte


def pulsaciones(letra):
    for t, ls in TECLADO.items():
        if letra in ls:
            return t * (ls.index(letra) + 1)


PULSA = {p: pulsaciones(l) for p, l in zip(ORDEN, PALABRA)}

_CACHE = os.path.join(AQUI, "instancias_espia.json")
_CLAVES = ("criptograma", "ruta", "rascacielos", "libro", "kenken", "conteo", "pasaportes", "husos", "cables", "ruleta")


def _construir():
    return {k: globals()[k]() for k in _CLAVES}


if __name__ != "__main__" and os.path.exists(_CACHE):
    _C = json.load(open(_CACHE, encoding="utf-8"))
    CRIPTOGRAMA, RUTA, RASCACIELOS, LIBRO, KENKEN, CONTEO, PASAPORTES, HUSOS, CABLES, RULETA = (_C[k] for k in _CLAVES)
elif __name__ != "__main__" and not os.environ.get("INSTANCIAS_SIN_CACHE"):
    _C = _construir()
    CRIPTOGRAMA, RUTA, RASCACIELOS, LIBRO, KENKEN, CONTEO, PASAPORTES, HUSOS, CABLES, RULETA = (_C[k] for k in _CLAVES)

if __name__ == "__main__":
    import time
    t0 = time.time()
    res = {}
    for k in _CLAVES:
        t = time.time()
        res[k] = globals()[k]()
        print(f"{k:12s} OK ({time.time() - t:.1f} s)")
    json.dump(res, open(_CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    print("OK", f"{time.time() - t0:.0f} s")

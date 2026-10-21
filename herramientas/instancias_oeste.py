"""Instancias de «Dry Gulch, 1878: El Tren del Oro» (versión de 60 cartas, 22 oct 2026), con solución comprobada por código.

Once puzles que no salen en ningún otro juego de la serie:
  vallas      el telegrama en zigzag (cifrado de la valla con cuatro rieles)
  hitori      el cuadro del banco: tachar números repetidos sin tocar tachones ni partir la tabla
  pentomino   la caja del carro: llenar un tablero con seis piezas distintas de cinco cuadros, dos ya puestas
  kakuro      el cuadro de apuestas: sumas en filas y columnas sin repetir cifras
  mochila     la carga del carro: el mayor valor sin pasarse del peso
  josefo      el duelo en corro: quién queda en pie si cae cada cuarto
  sokoban     la bodega: empujar tres barriles a sus huecos (solo dibujados en la carta)
  tuberias    la bomba de agua: girar tubos hasta formar un solo árbol; cinco tubos ya están dibujados
  vagones     la maniobra: ordenar siete vagones con un apartadero (pila)
  hierros     los hierros del ganado: cuáles son del mismo ganadero aunque estén girados o de espejo
  polibio     el cuadrado de Polibio: la palabra final con cinco coordenadas que dejan otros puzles
Ejecutarlo comprueba todo y escribe instancias_oeste.json; al importarlo se lee de ahí.
"""
import itertools
import json
import os
import random
import sys
from collections import deque

AQUI = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ vallas (cifrado en zigzag)
def vallas(claro="ELORONOVIAJAENELTERCERVAGONDETRAS", rieles=4):
    def zigzag(n):
        f, d, out = 0, 1, []
        for _ in range(n):
            out.append(f)
            if f == 0:
                d = 1
            elif f == rieles - 1:
                d = -1
            f += d
        return out
    z = zigzag(len(claro))
    cif = "".join(c for r in range(rieles) for c, f in zip(claro, z) if f == r)
    # comprobación: descifrar
    orden = sorted(range(len(claro)), key=lambda i: (z[i], i))
    des = [""] * len(claro)
    for k, i in enumerate(orden):
        des[i] = cif[k]
    assert "".join(des) == claro
    return {"claro": claro, "cifrado": cif, "rieles": rieles, "zigzag": z}


# ------------------------------------------------------------------ hitori
def _masks_fila(n):
    return [m for m in range(1 << n) if not (m & (m >> 1))]


def _conexo(blancas, n):
    if not blancas:
        return False
    ini = next(iter(blancas))
    vis, cola = {ini}, [ini]
    while cola:
        r, c = cola.pop()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (r + dr, c + dc)
            if q in blancas and q not in vis:
                vis.add(q)
                cola.append(q)
    return len(vis) == len(blancas)


def _hitori_soluciones(g, limite=2):
    n = len(g)
    mks = _masks_fila(n)
    sols = []

    def valido_fila(r, m):
        vistos = set()
        for c in range(n):
            if not (m >> c) & 1:
                if g[r][c] in vistos:
                    return False
                vistos.add(g[r][c])
        return True
    filas_ok = [[m for m in mks if valido_fila(r, m)] for r in range(n)]

    def col_ok(ms):
        for c in range(n):
            vistos = set()
            for r, m in enumerate(ms):
                if not (m >> c) & 1:
                    if g[r][c] in vistos:
                        return False
                    vistos.add(g[r][c])
        return True

    def rec(r, ms):
        if len(sols) >= limite:
            return
        if r == n:
            if col_ok(ms):
                blancas = {(i, c) for i in range(n) for c in range(n) if not (ms[i] >> c) & 1}
                if _conexo(blancas, n):
                    sols.append(tuple(ms))
            return
        for m in filas_ok[r]:
            if r and (m & ms[-1]):
                continue
            # poda: columnas hasta ahora sin repetidos
            ok = True
            for c in range(n):
                if not (m >> c) & 1:
                    for rr in range(r):
                        if not (ms[rr] >> c) & 1 and g[rr][c] == g[r][c]:
                            ok = False
                            break
                if not ok:
                    break
            if ok:
                rec(r + 1, ms + [m])
    rec(0, [])
    return sols


def hitori(semilla=3, n=5):
    rng = random.Random(semilla)
    mks = _masks_fila(n)
    for _ in range(4000):
        # máscara de tachones sin vecinos, tablero blanco conexo
        ms = [rng.choice(mks) for _ in range(n)]
        if any(ms[i] & ms[i + 1] for i in range(n - 1)) or sum(bin(m).count("1") for m in ms) < 6:
            continue
        blancas = {(r, c) for r in range(n) for c in range(n) if not (ms[r] >> c) & 1}
        if not _conexo(blancas, n):
            continue
        # cuadrado latino aleatorio para las blancas (cifras 1..n) y duplicados en los tachones
        base = list(range(1, n + 1))
        rng.shuffle(base)
        g = [[base[(r + c) % n] for c in range(n)] for r in range(n)]
        pr, pc = list(range(n)), list(range(n))
        rng.shuffle(pr)
        rng.shuffle(pc)
        g = [[g[pr[r]][pc[c]] for c in range(n)] for r in range(n)]
        for r in range(n):
            for c in range(n):
                if (ms[r] >> c) & 1:
                    cand = [g[r][k] for k in range(n) if k != c and not (ms[r] >> k) & 1] + [g[k][c] for k in range(n) if k != r and not (ms[k] >> c) & 1]
                    g[r][c] = rng.choice(cand)
        sols = _hitori_soluciones(g)
        if len(sols) == 1:
            return {"n": n, "cifras": g, "tachones": [[(ms_r >> c) & 1 for c in range(n)] for ms_r in sols[0]]}
    raise SystemExit("sin hitori")


# ------------------------------------------------------------------ pentomino
PIEZAS = {
    "F": [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)], "I": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)], "L": [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)],
    "N": [(0, 1), (1, 1), (2, 0), (2, 1), (3, 0)], "P": [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], "T": [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    "U": [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)], "V": [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], "W": [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
    "X": [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)], "Y": [(0, 1), (1, 0), (1, 1), (2, 1), (3, 1)], "Z": [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
}


def _normal(celdas):
    mr = min(r for r, c in celdas)
    mc = min(c for r, c in celdas)
    return tuple(sorted((r - mr, c - mc) for r, c in celdas))


def orientaciones(celdas):
    res = set()
    cur = list(celdas)
    for _ in range(2):
        for _ in range(4):
            cur = [(c, -r) for r, c in cur]
            res.add(_normal(cur))
        cur = [(r, -c) for r, c in cur]
    return sorted(res)


ORI = {k: orientaciones(v) for k, v in PIEZAS.items()}


def _colocaciones(letra, libres):
    libres = set(libres)
    out = []
    for o in ORI[letra]:
        for (r0, c0) in libres:
            cs = [(r0 + r, c0 + c) for r, c in o]
            if all(q in libres for q in cs):
                out.append(frozenset(cs))
    return set(out)


def _teselados(libres, letras, limite=2):
    libres = frozenset(libres)
    res = []

    def rec(libres, letras, actual):
        if len(res) >= limite:
            return
        if not letras:
            if not libres:
                res.append(dict(actual))
            return
        # primera casilla libre: debe cubrirla alguna pieza
        p0 = min(libres)
        for l in letras:
            for pl in _colocaciones(l, libres):
                if p0 in pl:
                    actual[l] = pl
                    rec(libres - pl, [x for x in letras if x != l], actual)
                    del actual[l]
    rec(libres, list(letras), {})
    return res


def pentomino(semilla=5, filas=5, cols=6, n_fijas=2):
    rng = random.Random(semilla)
    todas = frozenset((r, c) for r in range(filas) for c in range(cols))
    for _ in range(3000):
        letras = rng.sample(sorted(PIEZAS), 6)
        t = _teselados(todas, letras, limite=40)
        if not t:
            continue
        sol = rng.choice(t)
        fijas = rng.sample(letras, n_fijas)
        libres = todas - frozenset().union(*[sol[f] for f in fijas])
        resto = [l for l in letras if l not in fijas]
        if len(_teselados(libres, resto, limite=2)) == 1:
            return {"filas": filas, "cols": cols, "piezas": letras, "fijas": {f: sorted(sol[f]) for f in fijas},
                    "solucion": {l: sorted(sol[l]) for l in letras}}
    raise SystemExit("sin pentomino")


# ------------------------------------------------------------------ kakuro
def _runs(blancas, n):
    """Devuelve las tandas (tipo, r, c, celdas) de longitud >= 2; None si hay una de longitud 1."""
    out = []
    for r in range(n):
        c = 0
        while c < n:
            if (r, c) in blancas:
                c0 = c
                while c < n and (r, c) in blancas:
                    c += 1
                if c - c0 == 1:
                    return None
                out.append(("h", r, c0, [(r, k) for k in range(c0, c)]))
            else:
                c += 1
    for c in range(n):
        r = 0
        while r < n:
            if (r, c) in blancas:
                r0 = r
                while r < n and (r, c) in blancas:
                    r += 1
                if r - r0 == 1:
                    return None
                out.append(("v", r0, c, [(k, c) for k in range(r0, r)]))
            else:
                r += 1
    return out


def _kakuro_cuenta(tandas, sumas, celdas, limite=2):
    # asigna cifras por orden de celdas comprobando las tandas ya completas y cotas
    idx = {c: i for i, c in enumerate(celdas)}
    por_celda = {c: [] for c in celdas}
    for t, (tp, r, c, cs) in enumerate(tandas):
        for q in cs:
            por_celda[q].append(t)
    val = {}
    cuenta = [0]

    def ok(t):
        cs = tandas[t][3]
        v = [val[q] for q in cs if q in val]
        if len(set(v)) < len(v):
            return False
        s = sum(v)
        faltan = len(cs) - len(v)
        if faltan == 0:
            return s == sumas[t]
        resto = sumas[t] - s
        mn = sum(range(1, faltan + 1))
        mx = sum(range(9, 9 - faltan, -1))
        return mn <= resto <= mx

    def rec(i):
        if cuenta[0] >= limite:
            return
        if i == len(celdas):
            cuenta[0] += 1
            return
        q = celdas[i]
        for d in range(1, 10):
            val[q] = d
            if all(ok(t) for t in por_celda[q]):
                rec(i + 1)
            del val[q]
    rec(0)
    return cuenta[0]


def _reparar(blancas):
    """Quita las blancas que quedarían en una tanda de una sola casilla."""
    cambiado = True
    while cambiado:
        cambiado = False
        for (r, c) in list(blancas):
            h = (r, c - 1) in blancas or (r, c + 1) in blancas
            v = (r - 1, c) in blancas or (r + 1, c) in blancas
            if not h or not v:
                blancas.discard((r, c))
                cambiado = True
    return blancas


def kakuro(n=6):
    pesos = [4, 3, 2, 1, 1, 1, 2, 3, 4]          # cifras de los extremos: dejan sumas con pocas descomposiciones
    for sem in range(60000):
        rng = random.Random(sem)
        blancas = _reparar({(r, c) for r in range(1, n) for c in range(1, n) if rng.random() > 0.3})
        tandas = _runs(blancas, n)
        if not tandas or len(tandas) < 8 or len(blancas) < 13:
            continue
        celdas = sorted(blancas)
        val = {}

        def rec(i):
            if i == len(celdas):
                return True
            q = celdas[i]
            for d in sorted(range(1, 10), key=lambda x: -rng.random() * pesos[x - 1]):
                val[q] = d
                if all(len({val[y] for y in cs if y in val}) == len([y for y in cs if y in val]) for _, _, _, cs in tandas):
                    if rec(i + 1):
                        return True
                del val[q]
            return False
        if not rec(0):
            continue
        sumas = [sum(val[q] for q in cs) for _, _, _, cs in tandas]
        if _kakuro_cuenta(tandas, sumas, celdas) == 1:
            return {"n": n, "blancas": [list(q) for q in celdas],
                    "tandas": [{"tipo": tp, "r": r, "c": c, "largo": len(cs), "suma": s} for (tp, r, c, cs), s in zip(tandas, sumas)],
                    "solucion": {f"{q[0]},{q[1]}": val[q] for q in celdas}}
    raise SystemExit("sin kakuro")


# ------------------------------------------------------------------ mochila (carga del carro)
def mochila(semilla=2):
    rng = random.Random(semilla)
    for _ in range(20000):
        n = 8
        pesos = [rng.randint(3, 14) for _ in range(n)]
        valores = [rng.randint(10, 60) for _ in range(n)]
        cap = rng.randint(30, 40)
        mejor, cuantos, mejor_c = -1, 0, None
        for m in range(1 << n):
            p = sum(pesos[i] for i in range(n) if m >> i & 1)
            if p > cap:
                continue
            v = sum(valores[i] for i in range(n) if m >> i & 1)
            if v > mejor:
                mejor, cuantos, mejor_c = v, 1, m
            elif v == mejor:
                cuantos += 1
        if cuantos != 1:
            continue
        # el método voraz por valor/peso no debe dar el óptimo
        orden = sorted(range(n), key=lambda i: -valores[i] / pesos[i])
        p = v = 0
        for i in orden:
            if p + pesos[i] <= cap:
                p += pesos[i]
                v += valores[i]
        orden2 = sorted(range(n), key=lambda i: -valores[i])
        p2 = v2 = 0
        for i in orden2:
            if p2 + pesos[i] <= cap:
                p2 += pesos[i]
                v2 += valores[i]
        if v == mejor or v2 == mejor or len({pesos[i] for i in range(n)}) < 6:
            continue
        if sum(1 for i in range(n) if mejor_c >> i & 1) < 3:
            continue
        return {"pesos": pesos, "valores": valores, "capacidad": cap, "optimo": mejor, "solucion": [i for i in range(n) if mejor_c >> i & 1],
                "voraz": max(v, v2)}
    raise SystemExit("sin mochila")


# ------------------------------------------------------------------ josefo (el duelo en corro)
def josefo(n=17, k=4):
    asientos = list(range(1, n + 1))
    i, orden = 0, []
    while len(asientos) > 1:
        i = (i + k - 1) % len(asientos)
        orden.append(asientos.pop(i))
    return {"n": n, "k": k, "empieza": 1, "caen": orden, "sobrevive": asientos[0]}


# ------------------------------------------------------------------ sokoban (la bodega)
def sokoban(semilla=4, w=8, h=6, cajas=3):
    rng = random.Random(semilla)
    for _ in range(3000):
        muros = {(r, c) for r in range(h) for c in range(w) if r in (0, h - 1) or c in (0, w - 1)}
        for _ in range(rng.randint(3, 6)):
            muros.add((rng.randint(1, h - 2), rng.randint(1, w - 2)))
        libres = [(r, c) for r in range(h) for c in range(w) if (r, c) not in muros]
        if len(libres) < 20:
            continue
        # el suelo debe ser conexo
        if not _conexo(set(libres), max(h, w)):
            continue
        metas = rng.sample(libres, cajas)
        resto = [q for q in libres if q not in metas]
        jug = rng.choice(resto)
        # marcha atrás: tirar de las cajas
        estado = (jug, frozenset(metas))
        vis = {estado}
        cola = deque([estado])
        lejano, lejos = estado, 0
        dist = {estado: 0}
        while cola and len(vis) < 60000:
            p, cs = cola.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                np_ = (p[0] + dr, p[1] + dc)
                if np_ in muros or np_ in cs:
                    continue
                nuevos = [(np_, cs)]
                # tirar de la caja que está detrás
                atras = (p[0] - dr, p[1] - dc)
                if atras in cs:
                    nuevos.append((np_, (cs - {atras}) | {p}))
                for e in nuevos:
                    if e not in vis:
                        vis.add(e)
                        dist[e] = dist[(p, cs)] + 1
                        cola.append(e)
        # el estado inicial elegido: el de mayor distancia con las cajas fuera de las metas
        cand = [(d, e) for e, d in dist.items() if not (e[1] & set(metas)) or len(e[1] & set(metas)) <= 1]
        if not cand:
            continue
        d, e = max(cand, key=lambda x: x[0])
        if d < 28:
            continue
        ini_p, ini_c = e
        # solución mínima directa (BFS hacia delante)
        sol = _sokoban_resolver(muros, ini_p, ini_c, frozenset(metas))
        if sol and 24 <= len(sol) <= 80:
            return {"filas": h, "cols": w, "muros": sorted(muros), "metas": sorted(metas), "cajas": sorted(ini_c), "jugador": list(ini_p), "minimo": len(sol), "solucion": sol}
    raise SystemExit("sin sokoban")


def _sokoban_resolver(muros, jug, cajas, metas):
    ini = (jug, cajas)
    prev = {ini: None}
    cola = deque([ini])
    mov = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
    while cola:
        e = cola.popleft()
        p, cs = e
        if cs == metas:
            ruta = []
            while prev[e]:
                e, m = prev[e]
                ruta.append(m)
            return "".join(ruta[::-1])
        for m, (dr, dc) in mov.items():
            q = (p[0] + dr, p[1] + dc)
            if q in muros:
                continue
            if q in cs:
                q2 = (q[0] + dr, q[1] + dc)
                if q2 in muros or q2 in cs:
                    continue
                ne = (q, (cs - {q}) | {q2})
            else:
                ne = (q, cs)
            if ne not in prev:
                prev[ne] = (e, m)
                cola.append(ne)
    return None


# ------------------------------------------------------------------ tuberías (la bomba de agua)
N_, E_, S_, W_ = 1, 2, 4, 8
DIR = [(N_, -1, 0, S_), (E_, 0, 1, W_), (S_, 1, 0, N_), (W_, 0, -1, E_)]


def _giro(m):
    return ((m << 1) | (m >> 3)) & 15


def _rotaciones(m):
    out, cur = [], m
    for _ in range(4):
        if cur not in out:
            out.append(cur)
        cur = _giro(cur)
    return out


def _tuberias_cuenta(masks, n, fijas, limite=2):
    opciones = [[(fijas[(r, c)],) if (r, c) in fijas else tuple(_rotaciones(masks[r][c])) for c in range(n)] for r in range(n)]
    sols = []
    asign = [[0] * n for _ in range(n)]

    def rec(i):
        if len(sols) >= limite:
            return
        if i == n * n:
            blancas = {(r, c) for r in range(n) for c in range(n)}
            ini = (0, 0)
            vis, cola = {ini}, [ini]
            while cola:
                r, c = cola.pop()
                for b, dr, dc, ob in DIR:
                    if asign[r][c] & b:
                        q = (r + dr, c + dc)
                        if q not in vis:
                            vis.add(q)
                            cola.append(q)
            if len(vis) == n * n:
                sols.append([row[:] for row in asign])
            return
        r, c = divmod(i, n)
        for m in opciones[r][c]:
            # borde y vecinos ya puestos
            if r == 0 and m & N_ or c == 0 and m & W_ or r == n - 1 and m & S_ or c == n - 1 and m & E_:
                continue
            if r and bool(asign[r - 1][c] & S_) != bool(m & N_):
                continue
            if c and bool(asign[r][c - 1] & E_) != bool(m & W_):
                continue
            asign[r][c] = m
            rec(i + 1)
        asign[r][c] = 0
    rec(0)
    return sols


def tuberias(semilla=6, n=5, n_fijas=6):
    rng = random.Random(semilla)
    for _ in range(3000):
        # árbol abarcador aleatorio
        masks = [[0] * n for _ in range(n)]
        vis = {(0, 0)}
        frontera = [(0, 0)]
        while len(vis) < n * n:
            r, c = rng.choice(frontera)
            opts = [(b, r + dr, c + dc, ob) for b, dr, dc, ob in DIR if 0 <= r + dr < n and 0 <= c + dc < n and (r + dr, c + dc) not in vis]
            if not opts:
                frontera.remove((r, c))
                continue
            b, r2, c2, ob = rng.choice(opts)
            masks[r][c] |= b
            masks[r2][c2] |= ob
            vis.add((r2, c2))
            frontera.append((r2, c2))
        grados = [bin(masks[r][c]).count("1") for r in range(n) for c in range(n)]
        if grados.count(4) > 1 or grados.count(3) < 3 or grados.count(1) < 3:
            continue
        # las casillas fijas: preferentemente las que tienen una sola orientación posible no simétrica
        cand = [(r, c) for r in range(n) for c in range(n) if len(_rotaciones(masks[r][c])) > 1]
        for _ in range(30):
            fijas = {q: masks[q[0]][q[1]] for q in rng.sample(cand, n_fijas)}
            sols = _tuberias_cuenta(masks, n, fijas)
            if len(sols) == 1:
                ini = [[rng.choice(_rotaciones(masks[r][c])) for c in range(n)] for r in range(n)]
                if any(ini[r][c] == sols[0][r][c] for r in range(n) for c in range(n) if len(_rotaciones(masks[r][c])) > 1 and (r, c) not in fijas and False):
                    continue
                return {"n": n, "tubos": masks, "inicio": ini, "fijas": [[r, c, m] for (r, c), m in sorted(fijas.items())], "solucion": sols[0]}
    raise SystemExit("sin tuberías")


# ------------------------------------------------------------------ vagones (la maniobra con apartadero)
def vagones(semilla=8, n=7):
    rng = random.Random(semilla)
    for _ in range(5000):
        perm = list(range(1, n + 1))
        rng.shuffle(perm)
        pila, sig, ops, prof, salida = [], 1, [], 0, []
        entrada = list(perm)
        ok = True
        while sig <= n:
            if pila and pila[-1] == sig:
                salida.append(pila.pop())
                ops.append("S")
                sig += 1
            elif entrada:
                pila.append(entrada.pop(0))
                ops.append("E")
                prof = max(prof, len(pila))
            else:
                ok = False
                break
        tandas_s = sum(1 for i, o in enumerate(ops) if o == "S" and (i == 0 or ops[i - 1] == "E"))
        if ok and 3 <= prof <= 5 and tandas_s >= 4 and ops.count("E") == n:
            return {"pesos": perm, "ops": "".join(ops), "profundidad": prof}
    raise SystemExit("sin vagones")


# ------------------------------------------------------------------ hierros (los hierros del ganado)
def _transformaciones(g):
    n = len(g)
    res = []
    cur = [row[:] for row in g]
    for _ in range(2):
        for _ in range(4):
            cur = [[cur[n - 1 - c][r] for c in range(n)] for r in range(n)]
            res.append(tuple(tuple(f) for f in cur))
        cur = [row[::-1] for row in cur]
    return res


def hierros(semilla=7, n=4):
    rng = random.Random(semilla)
    for _ in range(5000):
        m = [[rng.randint(0, 1) for _ in range(n)] for _ in range(n)]
        if not 6 <= sum(map(sum, m)) <= 10:
            continue
        tr = _transformaciones(m)
        if len(set(tr)) != 8:
            continue
        autenticos = rng.sample(tr, 3)
        bien = set(tr)
        falsos = []
        while len(falsos) < 5:
            base = rng.choice(tr)
            f = [list(r) for r in base]
            r, c = rng.randrange(n), rng.randrange(n)
            f[r][c] ^= 1
            ft = tuple(tuple(x) for x in f)
            if ft in bien or ft in falsos or any(ft in set(_transformaciones([list(x) for x in o])) for o in falsos):
                continue
            falsos.append(ft)
        todos = [(a, True) for a in autenticos] + [(f, False) for f in falsos]
        rng.shuffle(todos)
        return {"n": n, "maestro": m, "candidatos": [[list(map(list, g)), v] for g, v in todos],
                "autenticos": [i for i, (_, v) in enumerate(todos) if v]}
    raise SystemExit("sin hierros")


# ------------------------------------------------------------------ polibio (la palabra final)
POLIBIO = ["ABCDE", "FGHIK", "LMNOP", "QRSTU", "VWXYZ"]
PALABRA = "VAPOR"
ORDEN = ["14", "40", "52", "69", "51"]                  # vallas, pentomino, mochila, vagones y sokoban


def coordenada(letra):
    letra = "I" if letra == "J" else letra
    for r, fila in enumerate(POLIBIO):
        if letra in fila:
            return f"{r + 1}{fila.index(letra) + 1}"


COORD = {p: coordenada(l) for p, l in zip(ORDEN, PALABRA)}       # lo que dice el mensaje de acierto de cada puzle

_CACHE = os.path.join(AQUI, "instancias_oeste.json")
_CLAVES = ("vallas", "hitori", "pentomino", "kakuro", "mochila", "josefo", "sokoban", "tuberias", "vagones", "hierros")


def _construir():
    return {"vallas": vallas(), "hitori": hitori(), "pentomino": pentomino(), "kakuro": kakuro(), "mochila": mochila(), "josefo": josefo(),
            "sokoban": sokoban(), "tuberias": tuberias(), "vagones": vagones(), "hierros": hierros()}


if __name__ != "__main__" and os.path.exists(_CACHE):
    _C = json.load(open(_CACHE, encoding="utf-8"))
    VALLAS, HITORI, PENTOMINO, KAKURO, MOCHILA, JOSEFO, SOKOBAN, TUBERIAS, VAGONES, HIERROS = (_C[k] for k in _CLAVES)
elif __name__ != "__main__" and not os.environ.get("INSTANCIAS_SIN_CACHE"):
    _C = _construir()
    VALLAS, HITORI, PENTOMINO, KAKURO, MOCHILA, JOSEFO, SOKOBAN, TUBERIAS, VAGONES, HIERROS = (_C[k] for k in _CLAVES)

if __name__ == "__main__":
    import time
    t0 = time.time()
    res = {}
    for k in _CLAVES:
        t = time.time()
        res[k] = globals()[k]()
        print(f"{k:10s} OK ({time.time() - t:.1f} s)")
    json.dump(res, open(_CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    print("OK", f"{time.time() - t0:.0f} s")

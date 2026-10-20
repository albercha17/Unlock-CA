"""Instancias de «Pompeya, 79 d.C.» (versión de 60 cartas, 20 oct 2026), con semilla fija y solución única comprobada por fuerza bruta.
Escribe instancias_pompeya.json, que leen pompeya.py (láminas), datos_pompeya.py (pistas y manual), los minijuegos y solvers_pompeya.py.

  - laberinto: mosaico del atrio (12 x 12 teselas en 4 placas): laberinto perfecto del sol (este) a la puerta (oeste); 4 figuras en el camino
               y 4 en ramales sin salida. Respuesta: las figuras del camino, en orden.
  - cuentas:   tres tablillas de ventas en números romanos; una suma está mal. Respuesta: el total verdadero de los tres días.
  - sello:     la impronta de un sello partida en dos cartas; seis anillos (uno da la impronta tal cual, sin espejo: es la trampa).
  - fuente:    reparto de agua con cinco compuertas; cada nudo reparte a partes iguales; solo una combinación riega lo que pide cada parterre.
  - sator:     el cuadrado SATOR con letras borradas, recuperables por su simetría. Respuesta: la palabra de la cruz (TENET).
  - statera:   pesos deducidos de dos pesadas dibujadas; el cofre del recibo; muesca de la balanza romana.
  - calles:    plano de 4 x 5 casas con rasgos; tres grafitis (acertijos) dejan una sola casa.
  - calendario: la fecha romana del acertijo (cuenta inclusiva hacia las calendas), con un ejemplo en el calendario de piedra.
  - huida:     grafo de calles con tiempos, calles cortadas; una sola ruta llega al puerto a tiempo.
  - barca:     carga de la barca (mochila): el mejor valor sin pasar del peso; óptimo único.
Uso (desde la raíz del repo):  python herramientas/instancias_pompeya.py
"""
import itertools
import json
import os
import random
from collections import deque

AQUI = os.path.dirname(os.path.abspath(__file__))
FIGURAS = ["delfin", "anfora", "laurel", "lechuza", "racimo", "concha", "lucerna", "escudo"]


# ------------------------------------------------------------------ 1. laberinto del mosaico
def laberinto():
    n = 12
    rng = random.Random(79)
    for _ in range(500):
        vis = [[False] * n for _ in range(n)]
        pasos = {}
        pila = [(rng.randrange(n), rng.randrange(n))]
        vis[pila[0][1]][pila[0][0]] = True
        abiertos = set()
        while pila:
            x, y = pila[-1]
            vec = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < n and 0 <= y + dy < n and not vis[y + dy][x + dx]]
            if not vec:
                pila.pop()
                continue
            nx, ny = rng.choice(vec)
            vis[ny][nx] = True
            abiertos.add(frozenset({(x, y), (nx, ny)}))
            pila.append((nx, ny))
        ini, fin = (n - 1, rng.randrange(2, n - 2)), (0, rng.randrange(2, n - 2))
        # camino único (es un árbol)
        prev = {ini: None}
        cola = deque([ini])
        while cola:
            c = cola.popleft()
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                v = (c[0] + d[0], c[1] + d[1])
                if frozenset({c, v}) in abiertos and v not in prev:
                    prev[v] = c
                    cola.append(v)
        camino = []
        c = fin
        while c:
            camino.append(c)
            c = prev[c]
        camino = camino[::-1]
        if not 30 <= len(camino) <= 46:
            continue
        en = set(camino)
        fuera = [c for c in prev if c not in en]
        # que el camino cruce los cuatro cuartos (las cuatro placas)
        if len({(x >= n // 2, y >= n // 2) for x, y in camino}) < 4:
            continue
        figs = FIGURAS[:]
        rng.shuffle(figs)
        idx = sorted(rng.sample(range(4, len(camino) - 4), 4))
        if min(b - a for a, b in zip(idx, idx[1:])) < 5:
            continue
        en_camino = [(camino[i], figs[k]) for k, i in enumerate(idx)]
        rng.shuffle(fuera)
        cebos = [(c, figs[4 + k]) for k, c in enumerate(fuera[:4])]
        return {"n": n, "pasos": [sorted([list(a), list(b)]) for a, b in (tuple(p) for p in abiertos)], "inicio": list(ini), "fin": list(fin),
                "camino": [list(c) for c in camino], "figuras": [[list(c), f] for c, f in en_camino + cebos],
                "solucion": [f for _, f in en_camino], "todas": FIGURAS}
    raise SystemExit("sin laberinto")


# ------------------------------------------------------------------ 2. cuentas en números romanos
def romano(n):
    out = ""
    for v, s in ((1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= v:
            out += s
            n -= v
    return out


def cuentas():
    rng = random.Random(1979)
    productos = ["aceite", "vino", "garum", "higos", "trigo", "miel", "sal", "lana"]
    dias = []
    for d in range(3):
        items = rng.sample(productos, 4)
        importes = [rng.choice([14, 19, 24, 29, 34, 39, 44, 49, 94, 99, 140, 190, 240, 290, 340, 390, 440, 490, 940]) for _ in items]
        dias.append({"items": items, "importes": importes, "total": sum(importes), "escrito": sum(importes)})
    malo = 1
    dias[malo]["escrito"] = dias[malo]["total"] + 10            # el esclavo se equivocó en una X
    total = sum(d["total"] for d in dias)
    assert total < 4000
    for d in dias:
        d["romanos"] = [romano(x) for x in d["importes"]]
        d["escrito_romano"] = romano(d["escrito"])
    return {"dias": dias, "malo": malo, "total": total, "total_romano": romano(total)}


# ------------------------------------------------------------------ 3. el sello
def sello():
    """La impronta es el dibujo del anillo en espejo. El anillo bueno es el dibujo tal cual (delfín y letras sin voltear).
    Trampas: uno idéntico a la impronta (todo volteado), uno con solo el delfín volteado, uno con solo las letras volteadas,
    y dos con otro dibujo u otras letras."""
    anillos = [
        {"id": "a", "simbolo": "delfin", "letras": "LVC", "voltea_simbolo": False, "voltea_letras": False},
        {"id": "b", "simbolo": "delfin", "letras": "LVC", "voltea_simbolo": True, "voltea_letras": True},
        {"id": "c", "simbolo": "delfin", "letras": "LVG", "voltea_simbolo": False, "voltea_letras": False},
        {"id": "d", "simbolo": "anfora", "letras": "LVC", "voltea_simbolo": False, "voltea_letras": False},
        {"id": "e", "simbolo": "delfin", "letras": "LVC", "voltea_simbolo": True, "voltea_letras": False},
        {"id": "f", "simbolo": "delfin", "letras": "LVC", "voltea_simbolo": False, "voltea_letras": True},
    ]
    return {"impronta": {"simbolo": "delfin", "letras": "LVC"}, "anillos": anillos, "solucion": "a", "orden": ["d", "b", "f", "a", "c", "e"]}


# ------------------------------------------------------------------ 4. la fuente (reparto de agua)
RED = {   # nudo -> lista de (compuerta, destino). El agua de un nudo se reparte a partes iguales entre sus compuertas abiertas.
    "acueducto": [("I", "A"), ("II", "B"), ("III", "C")],
    "A": [("IV", "rosas"), ("V", "B")],
    "B": [("VI", "laureles"), ("VII", "vina")],
    "C": [("VIII", "vina"), ("IX", "lirios")],
}
ORDEN_NUDOS = ["acueducto", "A", "B", "C"]
PARTERRES = ["rosas", "laureles", "vina", "lirios"]


def regar(abiertas, caudal=36):
    agua = {"acueducto": caudal}
    llega = {p: 0 for p in PARTERRES}
    perdida = 0
    for nudo in ORDEN_NUDOS:
        q = agua.get(nudo, 0)
        salidas = [(c, d) for c, d in RED[nudo] if c in abiertas]
        if not salidas:
            perdida += q
            continue
        for c, d in salidas:
            if d in llega:
                llega[d] += q / len(salidas)
            else:
                agua[d] = agua.get(d, 0) + q / len(salidas)
    return llega, perdida


def fuente():
    comp = [c for v in RED.values() for c, _ in v]
    por_reparto = {}
    for k in range(len(comp) + 1):
        for ab in itertools.combinations(comp, k):
            llega, perdida = regar(set(ab))
            if perdida == 0 and all(v == int(v) and v > 0 for v in llega.values()):
                por_reparto.setdefault(tuple(int(llega[p]) for p in PARTERRES), []).append(sorted(ab))
    # un reparto que solo da una combinación y obliga a cerrar al menos dos compuertas
    buenos = sorted((r, s[0]) for r, s in por_reparto.items() if len(s) == 1 and len(comp) - len(s[0]) >= 2)
    assert buenos, "sin reparto"
    reparto, sol = buenos[len(buenos) // 2]
    return {"red": RED, "orden": ORDEN_NUDOS, "caudal": 36, "pide": dict(zip(PARTERRES, reparto)), "solucion": sol, "compuertas": comp}


# ------------------------------------------------------------------ 5. el cuadrado SATOR
def sator():
    filas = ["SATOR", "AREPO", "TENET", "OPERA", "ROTAS"]
    borradas = [(0, 2), (1, 0), (1, 3), (2, 1), (4, 4), (2, 4), (3, 3), (4, 1), (4, 2), (0, 4)]
    vis = {(f, c) for f in range(5) for c in range(5)} - set(borradas)
    # cada borrada se recupera por alguna de sus simétricas visibles (giro de 180°, trasposición y su combinación)
    for f, c in borradas:
        assert {(4 - f, 4 - c), (c, f), (4 - c, 4 - f)} & vis, (f, c)
    return {"filas": filas, "borradas": [list(x) for x in borradas], "solucion": "TENET"}


# ------------------------------------------------------------------ 6. la balanza romana
def statera():
    pesos = {"aceite": 6, "vino": 3, "higos": 2}           # libras
    pesadas = [(["aceite"], ["vino", "vino"]), (["vino", "higos"], ["pesa", "pesa", "pesa", "pesa", "pesa"]), (["higos", "pesa"], ["vino"])]   # pesa = 1 libra
    peso = lambda xs: sum(1 if x == "pesa" else pesos[x] for x in xs)
    assert all(peso(a) == peso(b) for a, b in pesadas)
    compatibles = [t for t in itertools.product(range(1, 13), repeat=3)
                   if all(sum(1 if x == "pesa" else t[["aceite", "vino", "higos"].index(x)] for x in a) ==
                          sum(1 if x == "pesa" else t[["aceite", "vino", "higos"].index(x)] for x in b) for a, b in pesadas)]
    assert compatibles == [(6, 3, 2)], compatibles
    cofre = {"aceite": 2, "vino": 3, "higos": 3}
    total = sum(pesos[k] * v for k, v in cofre.items()) + 3   # + el propio cofre (3 libras, viene en el recibo)
    pondus = 3
    assert total % pondus == 0 and total // pondus <= 12
    return {"pesos": pesos, "pesadas": pesadas, "cofre": cofre, "tara": 3, "total": total, "pondus": pondus, "muesca": total // pondus}


# ------------------------------------------------------------------ 7. el plano de las calles
def calles():
    rng = random.Random(24)
    tiendas = ["panaderia", "taberna", "fuente", "templo", "termas", "lavanderia", "barbero", "taller"]
    filas, cols = 4, 5
    for _ in range(20000):
        casas = []
        for f in range(filas):
            for c in range(cols):
                casas.append({"f": f, "c": c, "rasgo": rng.choice(tiendas + ["casa"] * 3), "puerta": rng.choice(["norte", "sur"]),
                              "pintada": rng.choice(["roja", "ocre", "blanca"])})
        R = {(h["f"], h["c"]): h for h in casas}

        def vecina(h, rasgo):
            return any(R.get((h["f"], h["c"] + d), {}).get("rasgo") == rasgo for d in (-1, 1))
        preds = [
            ("rasgo", lambda h: h["rasgo"] == "casa"),
            ("puerta", lambda h: h["puerta"] == "sur"),
            ("pan", lambda h: vecina(h, "panaderia")),
            ("roja", lambda h: h["pintada"] == "roja"),
        ]
        ok = [h for h in casas if all(p(h) for _, p in preds)]
        if len(ok) == 1 and all(len([h for h in casas if all(p(h) for k, p in preds if k != quita)]) > 1 for quita, _ in preds):
            return {"filas": filas, "cols": cols, "casas": casas, "solucion": [ok[0]["f"], ok[0]["c"]]}
    raise SystemExit("sin plano")


# ------------------------------------------------------------------ 8. el calendario romano
def calendario():
    # a. d. IX Kal. Sept. = 24 de agosto (agosto tiene 31 días; se cuenta incluyendo las calendas): 32 - 9 + 1 = 24
    ejemplo = {"romano": "a. d. IV Kal. Sept.", "dia": 29}
    dia = 32 - 9 + 1
    assert 32 - 4 + 1 == ejemplo["dia"]
    return {"acertijo": "IX", "dia": dia, "ejemplo": ejemplo, "mes": "Augustus"}


# ------------------------------------------------------------------ 9. la huida
def huida():
    calles_ = {("F", "A"): 4, ("F", "B"): 6, ("A", "C"): 5, ("B", "C"): 3, ("A", "D"): 7, ("C", "E"): 6, ("D", "E"): 3, ("B", "G"): 9,
               ("G", "P"): 4, ("E", "P"): 5, ("D", "P"): 9, ("C", "G"): 4}
    cortadas = [("C", "E"), ("D", "P"), ("A", "C")]
    limite = 17
    g = {}
    for (a, b), t in calles_.items():
        if (a, b) in cortadas:
            continue
        g.setdefault(a, []).append((b, t))
        g.setdefault(b, []).append((a, t))
    rutas = []

    def dfs(n, camino, t):
        if t > limite:
            return
        if n == "P":
            rutas.append((camino, t))
            return
        for v, w in g.get(n, []):
            if v not in camino:
                dfs(v, camino + [v], t + w)
    dfs("F", ["F"], 0)
    assert len(rutas) == 1, rutas
    return {"calles": [[a, b, t] for (a, b), t in calles_.items()], "cortadas": [list(x) for x in cortadas], "limite": limite,
            "solucion": rutas[0][0], "tiempo": rutas[0][1]}


# ------------------------------------------------------------------ 10. la barca
def barca():
    carga = {"anfora_aceite": (4, 9), "anfora_vino": (3, 6), "fardo_lana": (2, 3), "cofre_monedas": (5, 11), "estatua_lar": (1, 4), "saco_trigo": (3, 5)}
    maximo = 9
    mejor, opt = -1, []
    for k in range(len(carga) + 1):
        for comb in itertools.combinations(carga, k):
            p = sum(carga[x][0] for x in comb)
            v = sum(carga[x][1] for x in comb)
            if p <= maximo:
                if v > mejor:
                    mejor, opt = v, [comb]
                elif v == mejor:
                    opt.append(comb)
    assert len(opt) == 1, opt
    return {"carga": {k: list(v) for k, v in carga.items()}, "maximo": maximo, "solucion": sorted(opt[0]), "valor": mejor}


def main():
    inst = {"laberinto": laberinto(), "cuentas": cuentas(), "sello": sello(), "fuente": fuente(), "sator": sator(), "statera": statera(),
            "calles": calles(), "calendario": calendario(), "huida": huida(), "barca": barca()}
    with open(os.path.join(AQUI, "instancias_pompeya.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(inst, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("laberinto:", inst["laberinto"]["solucion"], len(inst["laberinto"]["camino"]), "casillas")
    print("cuentas:", inst["cuentas"]["total"], inst["cuentas"]["total_romano"])
    print("fuente:", inst["fuente"]["solucion"], "· statera muesca", inst["statera"]["muesca"], "(", inst["statera"]["total"], "libras )")
    print("calles:", inst["calles"]["solucion"], "· calendario:", inst["calendario"]["dia"])
    print("huida:", inst["huida"]["solucion"], inst["huida"]["tiempo"], "· barca:", inst["barca"]["solucion"], inst["barca"]["valor"])


if __name__ == "__main__":
    main()

"""Verificador de juegos Unlock.

Uso: python verificar.py <cartas.json> <spec.json>
spec.json: {"needs": {carta: [cartas que hay que TENER en la mano para obtenerla]},
            "eventos": {nombre: {"needs": [...], "descarta": [...]}},   # descartes que manda la app
            "final": "99"}
Las cartas que salen en el 'coge' de otra se cogen a la vez que ella (no llevan 'needs').
Comprueba: coherencia, fugas de numeros, descartes imposibles o prematuros, sumas al combinar,
utilidad de cada carta y 3000 partidas simuladas en orden aleatorio legal.
"""
import json, random, re, sys

cartas = json.load(open(sys.argv[1], encoding="utf-8"))
cartas.pop("_meta", None)
spec = json.load(open(sys.argv[2], encoding="utf-8"))
needs = {k: list(map(str, v)) for k, v in spec["needs"].items()}
eventos = {k: {"needs": list(map(str, v["needs"])), "descarta": list(map(str, v["descarta"]))} for k, v in spec.get("eventos", {}).items()}
final = spec["final"]
ids = set(cartas)
errores = []


def err(msg):
    errores.append(msg)
    print("  ERROR:", msg)


hijos = {c: [str(x) for x in d.get("coge", [])] for c, d in cartas.items()}
padre = {}
for c, hs in hijos.items():
    for h in hs:
        if h not in ids:
            err(f"{c}.coge nombra {h}, que no existe")
        if h in padre:
            err(f"{h} sale en el coge de {padre[h]} y de {c}")
        padre[h] = c

# 1 coherencia
for c in ids:
    if c == "P":
        continue
    if c in padre and c in needs:
        err(f"{c} sale en el coge de {padre[c]} y ademas tiene needs")
    if c not in padre and c not in needs:
        err(f"{c} no se obtiene de ningun modo (ni coge ni needs)")
for c, req in list(needs.items()) + [(k, v["needs"]) for k, v in eventos.items()]:
    for r in req:
        if r not in ids and r not in eventos:
            err(f"{c} necesita {r}, que no existe")
for c, d in cartas.items():
    for x in d.get("descarta", []):
        if str(x) not in ids:
            err(f"{c}.descarta nombra {x}, que no existe")


# ancestros: cartas que SIEMPRE se han obtenido antes de obtener c
def requisitos(c):
    if c in padre:
        return [padre[c]]
    if c in needs:
        return needs[c]
    if c in eventos:
        return eventos[c]["needs"]
    return []


cache = {}


def ancestros(c):
    if c in cache:
        return cache[c]
    s = set()
    for r in requisitos(c):
        s.add(r)
        s |= ancestros(r)
    cache[c] = s
    return s


def descartes_de(c):
    if c in eventos:
        return eventos[c]["descarta"]
    return [str(x) for x in cartas[c].get("descarta", [])]


# 2 fuga de numeros impresos
for c, d in cartas.items():
    texto = re.sub(r"\d{1,2}:\d{2}", "", " ".join(d.get("textoCarta", [])))
    for n in re.findall(r"\d+", texto):
        if n in ids:
            err(f"FUGA: la carta {c} imprime '{n}', que es el numero de otra carta")

# 5 sumas
for c, d in cartas.items():
    if d.get("combina"):
        pareja, res = map(str, d["combina"])
        if int(c) + int(pareja) != int(res):
            err(f"{c} + {pareja} != {res}")
        if not cartas[pareja].get("combina"):
            err(f"{pareja} deberia tener 'combina'")
        if c not in needs.get(res, []) or pareja not in needs.get(res, []):
            err(f"{res} deberia exigir {c} y {pareja}")

# 3 descartes
todos = list(ids) + list(eventos)
for c in todos:
    for d in descartes_de(c):
        anc_c = ancestros(c) | {c}
        if d not in ancestros(c) and not (c in hijos and False):
            # un hijo del coge tambien cuenta como obtenido tras su padre
            err(f"{c} manda descartar {d}, pero no siempre se tiene en ese momento")
        for e in todos:
            if e in (c, d):
                continue
            if d in (needs[e] if e in needs else eventos[e]["needs"] if e in eventos else []) and e not in ancestros(c):
                err(f"{c} descarta {d}, que aun necesita {e} (que se puede obtener despues)")

# 6 utilidad: cada carta es requisito de algo, o lleva pista impresa, o es de combinar/final
usadas = set()
for c in todos:
    usadas |= set(requisitos(c))
for c, d in cartas.items():
    if c == final:
        continue
    if c not in usadas and not d.get("textoCarta") and not d.get("combina"):
        err(f"la carta {c} no la necesita ningun paso (sin funcion)")


# 4 simulacion
def obtener(c, mano):
    for d in descartes_de(c):
        if d not in mano:
            return False
        mano.discard(d)
    mano.add(c)  # los eventos de la app tambien se anotan, para poder exigirlos despues
    for h in hijos.get(c, []):
        if not obtener(h, mano):
            return False
    return True


accidentales = set()


def revisar_combinaciones(mano):
    """Dos cartas combinables que coinciden en la mano no deben sumar el numero de OTRA carta aun no obtenida."""
    comb = [c for c in mano if c in cartas and cartas[c].get("combina")]
    for i, a in enumerate(comb):
        for b in comb[i + 1:]:
            s = str(int(a) + int(b))
            previsto = str(b) == str(cartas[a]["combina"][0])
            if not previsto and s in ids:
                accidentales.add((min(a, b, key=int), max(a, b, key=int), s))


def partida(rng):
    mano = set()
    obtener("P", mano)
    pend = [c for c in needs] + list(eventos)
    for _ in range(300):
        revisar_combinaciones(mano)
        if final in mano:
            return True, mano
        ops = [c for c in pend if all(r in mano for r in (needs[c] if c in needs else eventos[c]["needs"]))]
        if not ops:
            return False, mano
        c = rng.choice(ops)
        pend.remove(c)
        if not obtener(c, mano):
            return False, mano
    return False, mano


rng = random.Random(7)
fallos = 0
finales = set()
for _ in range(3000):
    ok, mano = partida(rng)
    if ok:
        finales.add(tuple(sorted(mano)))
    else:
        fallos += 1
        if fallos <= 3:
            err(f"partida atascada o con descarte invalido; mano: {sorted(mano)}")
for a, b, s in sorted(accidentales):
    err(f"COMBINACION ACCIDENTAL posible: {a} + {b} = {s}, que es otra carta del juego que aun no se tiene")
print(f"simulaciones: 3000, atascadas: {fallos}; manos finales: {sorted(finales)[:3]}")
# cartas-data.js (copia embebida para abrir pc/imprimir/prompts con doble clic) debe coincidir con cartas.json
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sincronizar_cartas import contenido
_cd = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), "cartas-data.js")
if os.path.exists(os.path.join(os.path.dirname(_cd), "pc.html")):
    if not os.path.exists(_cd) or open(_cd, encoding="utf-8", newline="").read().replace("\r\n", "\n") != contenido(sys.argv[1]):
        err("cartas-data.js falta o esta desfasado respecto a cartas.json: ejecuta python herramientas/sincronizar_cartas.py")
print("RESULTADO:", "OK" if not errores else f"{len(errores)} errores")
sys.exit(1 if errores else 0)

"""Instancias de los puzles de «Trono» con solución única comprobada por fuerza bruta.

Uso (desde la raíz): python herramientas/instancias_trono.py            # comprueba todo y escribe herramientas/instancias_trono.json
Los minijuegos (juegos/aventuras-ca/trono/minijuegos/*.js) llevan estas instancias como constantes y el solucionador
(solvers_trono.py) las lee del JSON, de modo que si se cambia una instancia hay que regenerar el JSON y actualizar el módulo.
"""
import itertools
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generadores_puzles as G  # noqa: E402

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_trono.json")
R = {}

# ------------------------------------------------------------------ 14 Mensaje del cuervo (César, desplazamiento 3)
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def cesar(texto, k):
    return "".join(ABC[(ABC.index(c) + k) % 26] if c in ABC else c for c in texto)


R["14"] = dict(desplazamiento=3, claro="BAJAD AL ARCHIVO", cifrado=cesar("BAJAD AL ARCHIVO", 3))
assert cesar(R["14"]["cifrado"], -3) == R["14"]["claro"]

# ------------------------------------------------------------------ 20 Banquete de las casas (tabla lógica)
CASAS = ["Lobo Gris", "León Dorado", "Halcón Plateado", "Oso Pardo"]
REGALOS = ["espada", "copa", "pieles", "cuerno"]
# solución: asiento i (0..3) -> (casa, regalo)
SOL_B = [("León Dorado", "copa"), ("Lobo Gris", "pieles"), ("Oso Pardo", "espada"), ("Halcón Plateado", "cuerno")]


def pistas_banquete():
    c = lambda x: CASAS.index(x)
    r = lambda x: REGALOS.index(x)
    # cada pista: (texto, predicado sobre (asiento_de_cada_casa[4], asiento_de_cada_regalo[4])); asientos 0..3 de izquierda a derecha
    return {
        "p1": ("El Halcón Plateado ocupa el último asiento.", lambda ac, ar: ac[c("Halcón Plateado")] == 3),
        "p2": ("Quien trae la espada no se sienta en ninguna de las dos puntas de la mesa.", lambda ac, ar: ar[r("espada")] in (1, 2)),
        "p3": ("El León Dorado y el Lobo Gris se sientan uno junto al otro.", lambda ac, ar: abs(ac[c("León Dorado")] - ac[c("Lobo Gris")]) == 1),
        "p4": ("El cuerno lo trae la casa sentada justo a la derecha del Oso Pardo.", lambda ac, ar: ar[r("cuerno")] == ac[c("Oso Pardo")] + 1),
        "p5": ("La casa del León Dorado trae la copa.", lambda ac, ar: ar[r("copa")] == ac[c("León Dorado")]),
        "p6": ("El Oso Pardo no trae las pieles.", lambda ac, ar: ar[r("pieles")] != ac[c("Oso Pardo")]),
        "p7": ("El Lobo Gris se sienta más a la derecha que el León Dorado.", lambda ac, ar: ac[c("Lobo Gris")] > ac[c("León Dorado")]),
        "p8": ("Las pieles no las trae ni el Halcón Plateado ni el León Dorado.", lambda ac, ar: ar[r("pieles")] not in (ac[c("Halcón Plateado")], ac[c("León Dorado")])),
        "p9": ("El Oso Pardo no se sienta en ninguna de las puntas.", lambda ac, ar: ac[c("Oso Pardo")] in (1, 2)),
        "p10": ("La espada está más a la izquierda que el cuerno.", lambda ac, ar: ar[r("espada")] < ar[r("cuerno")]),
    }


def contar_banquete(claves):
    P = pistas_banquete()
    n = 0
    for ac in itertools.permutations(range(4)):
        for ar in itertools.permutations(range(4)):
            if all(P[k][1](ac, ar) for k in claves):
                n += 1
    return n


sol_ac = [None] * 4
sol_ar = [None] * 4
for asiento, (casa, regalo) in enumerate(SOL_B):
    sol_ac[CASAS.index(casa)] = asiento
    sol_ar[REGALOS.index(regalo)] = asiento
P = pistas_banquete()
assert all(P[k][1](sol_ac, sol_ar) for k in P), [k for k in P if not P[k][1](sol_ac, sol_ar)]
# buscar 2 pistas para la carta y 3-4 para la app: juntas dan solución única, cada grupo por separado deja dudas y ninguna sobra
CARTA = APP = None
for n_app in (3, 4):
    for carta in itertools.combinations(P, 2):
        for app in itertools.combinations([k for k in P if k not in carta], n_app):
            todas = list(carta) + list(app)
            if contar_banquete(todas) != 1 or contar_banquete(list(app)) == 1 or contar_banquete(list(carta)) == 1:
                continue
            if any(contar_banquete([x for x in todas if x != k]) == 1 for k in todas):
                continue
            CARTA, APP = list(carta), list(app)
            break
        if CARTA:
            break
    if CARTA:
        break
assert CARTA, "no hay combinación de pistas para el banquete"
R["20"] = dict(casas=CASAS, regalos=REGALOS, solucion=SOL_B, carta=[P[k][0] for k in CARTA], app=[P[k][0] for k in APP])
print("banquete: carta", CARTA, "app", APP)

# ------------------------------------------------------------------ 40 Caminos entre castillos (puentes)
DEF_N = 7


def contar_hashi(islas, ocultas=()):
    """islas: {(r,c): grado}. Las ocultas aceptan cualquier grado >= 1. Cuenta soluciones (tope 2)."""
    pos = sorted(islas)
    aristas = []
    for a, b in itertools.combinations(pos, 2):
        if a[0] == b[0] and not [p for p in pos if p[0] == a[0] and a[1] < p[1] < b[1]]:
            aristas.append((a, b))
        elif a[1] == b[1] and not [p for p in pos if p[1] == a[1] and a[0] < p[0] < b[0]]:
            aristas.append((a, b))

    def cruzan(e1, e2):
        (a, b), (c, d) = e1, e2
        h1, h2 = a[0] == b[0], c[0] == d[0]
        if h1 == h2:
            return False
        if h1:
            (fy, x1, x2), (fx, y1, y2) = (a[0], a[1], b[1]), (c[1], c[0], d[0])
        else:
            (fx, y1, y2), (fy, x1, x2) = (a[1], a[0], b[0]), (c[0], c[1], d[1])
        return x1 < fx < x2 and y1 < fy < y2

    cuenta = [0]
    rest0 = {p: (islas[p] if p not in ocultas else 99) for p in pos}
    grado0 = {p: 0 for p in pos}

    def rec(i, asg, grado):
        if cuenta[0] >= 2:
            return
        if i == len(aristas):
            for p in pos:
                if p in ocultas:
                    if grado[p] < 1:
                        return
                elif grado[p] != islas[p]:
                    return
            g = {p: set() for p in pos}
            for e, v in asg.items():
                if v:
                    g[e[0]].add(e[1])
                    g[e[1]].add(e[0])
            vv, st = set(), [pos[0]]
            while st:
                x = st.pop()
                if x in vv:
                    continue
                vv.add(x)
                st += list(g[x])
            if len(vv) == len(pos):
                cuenta[0] += 1
            return
        e = aristas[i]
        for v in (0, 1, 2):
            if v:
                if any(asg.get(f, 0) and cruzan(e, f) for f in asg):
                    continue
                if grado[e[0]] + v > rest0[e[0]] or grado[e[1]] + v > rest0[e[1]]:
                    continue
            g2 = dict(grado)
            g2[e[0]] += v
            g2[e[1]] += v
            a2 = dict(asg)
            a2[e] = v
            rec(i + 1, a2, g2)

    rec(0, {}, grado0)
    return cuenta[0]


def elegir_hashi():
    for semilla in range(1, 60):
        h = G.hashi(DEF_N, 8, semilla)
        islas = {tuple(map(int, k.split(","))): v for k, v in h["islas"].items()}
        if max(islas.values()) < 3:
            continue  # que haya algún nodo gordo
        orden = sorted(islas, key=lambda p: -islas[p])
        ocultas = tuple(orden[:2])
        if contar_hashi(islas) == 1 and contar_hashi(islas, ocultas) > 1:
            return semilla, h, islas, ocultas
    raise RuntimeError("sin hashi adecuado")


semilla_h, H, ISLAS, OCULTAS = elegir_hashi()
letras = "ABCDEFGH"
lista = sorted(ISLAS)
R["40"] = dict(
    n=DEF_N,
    castillos=[dict(letra=letras[i], r=p[0], c=p[1], grado=ISLAS[p], oculto=p in OCULTAS) for i, p in enumerate(lista)],
    solucion=[[list(a), list(b), v] for a, b, v in H["puentes"]],
    semilla=semilla_h,
)

# ------------------------------------------------------------------ 46 Lengua del pueblo libre
SUST = {"lobo": "ur", "cuervo": "kra", "guerrero": "hod", "dragón": "zeh"}
VERB = {"ve": "sil", "teme": "ven"}
ADJ = {"grande": "mor", "negro": "ska"}
PLUR = "-i"


def traducir(h, sujeto, verbo, objeto, adj=None, plural=False):
    orden, adj_pos, suf, adj_plural = h
    s = SUST[sujeto] + (suf if plural else "")
    p = [s]
    if adj:
        a = ADJ[adj] + (suf if plural and adj_plural else "")
        p = [a] + p if adj_pos == "antes" else p + [a]
    piezas = {"S": p, "V": [VERB[verbo]], "O": [SUST[objeto]]}
    return " ".join(sum((piezas[ch] for ch in orden), []))


HIP = list(itertools.product(["SVO", "SOV", "VSO", "VOS", "OSV", "OVS"], ["antes", "despues"], ["i", "o", "u"], [True, False]))
VERDAD = ("SOV", "despues", "i", True)
EJEMPLOS = [
    # carta 48
    ("El lobo ve al cuervo", ("lobo", "ve", "cuervo", None, False)),
    ("El dragón negro ve al lobo", ("dragón", "ve", "lobo", "negro", False)),
    ("Los lobos grandes ven al cuervo", ("lobo", "ve", "cuervo", "grande", True)),
    # carta 37
    ("El cuervo teme al dragón", ("cuervo", "teme", "dragón", None, False)),
    ("El guerrero grande ve al lobo", ("guerrero", "ve", "lobo", "grande", False)),
    ("Los dragones temen al cuervo", ("dragón", "teme", "cuervo", None, True)),
]
PREGUNTA = ("Los cuervos negros temen al guerrero", ("cuervo", "teme", "guerrero", "negro", True))
frases = [(es, traducir(VERDAD, *d)) for es, d in EJEMPLOS]
consistentes = [h for h in HIP if all(traducir(h, *d) == frases[i][1] for i, (_, d) in enumerate(EJEMPLOS))]
respuestas = {traducir(h, *PREGUNTA[1]) for h in consistentes}
assert len(respuestas) == 1 and traducir(VERDAD, *PREGUNTA[1]) in respuestas, (len(consistentes), respuestas)
# ninguna carta sola da todo el vocabulario de la pregunta (negro solo está en la 48; temen y guerrero solo en la 37)
REPARTO = ([0, 1, 2], [3, 4, 5])
palabras_pregunta = {SUST["cuervo"], ADJ["negro"], VERB["teme"], SUST["guerrero"]}
for grupo in REPARTO:
    vistas = {w.rstrip("iou") if False else w for i in grupo for w in frases[i][1].split()}
    conocidas = {p for p in palabras_pregunta if any(w == p or w.startswith(p) for w in vistas)}
    assert conocidas != palabras_pregunta, "una sola carta ya trae todo el vocabulario"
R["46"] = dict(frases=frases, pregunta=[PREGUNTA[0], traducir(VERDAD, *PREGUNTA[1])],
               carta48=[list(frases[i]) for i in REPARTO[0]], carta37=[list(frases[i]) for i in REPARTO[1]], hipotesis=len(consistentes))

# ------------------------------------------------------------------ 51 Los consejeros (leales y traidores)
NOMBRES = ["Aldric", "Brenna", "Corvin", "Dalia"]


def contar_decl(decl, indices):
    """decl[i] = (tipo, j, k); cuenta asignaciones consistentes usando solo las declaraciones de `indices`."""
    cuenta = 0
    for a in itertools.product([True, False], repeat=4):
        def verdad(d):
            tipo, j, k = d
            if tipo == "es":
                return a[j]
            if tipo == "no es":
                return not a[j]
            if tipo == "ambos":
                return a[j] and a[k]
            return a[j] or a[k]
        if all(verdad(decl[i]) == a[i] for i in indices):
            cuenta += 1
    return cuenta


def reconstruir(frases):
    """Vuelve a leer las declaraciones de G.caballeros desde su texto."""
    nom = ["Ana", "Beto", "Carla", "Diego"]
    decl = []
    for t in frases:
        cuerpo = t.split("«")[1]
        if cuerpo.startswith("Al menos"):
            ks = [i for i, n in enumerate(nom) if n in cuerpo]
            decl.append(("alguno", ks[0], ks[1]))
        elif " y " in cuerpo and "son caballeros" in cuerpo:
            ks = [i for i, n in enumerate(nom) if n in cuerpo]
            decl.append(("ambos", ks[0], ks[1]))
        elif "es bribón" in cuerpo:
            decl.append(("no es", [i for i, n in enumerate(nom) if n in cuerpo][0], 0))
        else:
            decl.append(("es", [i for i, n in enumerate(nom) if n in cuerpo][0], 0))
    return decl


def elegir_c():
    for semilla in range(1, 600):
        c = G.caballeros(4, semilla)
        decl = reconstruir(c["frases"])
        if contar_decl(decl, [0, 1, 2, 3]) != 1:
            continue
        # cada mitad por separado debe dejar dudas (las cartas se necesitan las dos)
        if contar_decl(decl, [0, 1]) > 1 and contar_decl(decl, [2, 3]) > 1 and 1 <= sum(c["caballeros"]) <= 3:
            return semilla, c, decl
    raise RuntimeError("sin consejeros")


sem_c, C, DECL = elegir_c()
nom_vieja = ["Ana", "Beto", "Carla", "Diego"]


def traducir_frase(t):
    for a, b in zip(nom_vieja, NOMBRES):
        t = t.replace(a, b)
    t = (t.replace("son caballeros", "son leales").replace("es caballero", "es leal").replace("es bribón", "es un traidor")
         .replace("de " + NOMBRES[0] + " y", "de " + NOMBRES[0] + " y"))
    return t


FR_C = [traducir_frase(t) for t in C["frases"]]
R["51"] = dict(nombres=NOMBRES, leales=list(C["caballeros"]), frases=FR_C, semilla=sem_c, carta26=FR_C[:2], carta52=FR_C[2:])

# ------------------------------------------------------------------ 64 Antorchas de la cripta (Akari)


def elegir_akari():
    for semilla in range(1, 80):
        a = G.akari(6, semilla)
        muros = {tuple(m) for m in a["muros"]}
        numeros = {tuple(map(int, k.split(","))): v for k, v in a["numeros"].items()}
        if len(numeros) < 4 or len(muros) < 4:
            continue
        claves = sorted(numeros)
        mitad = claves[::2]  # los que irán en la carta
        en_app = {k: v for k, v in numeros.items() if k not in mitad}
        if G._contar_akari(6, muros, numeros) == 1 and G._contar_akari(6, muros, en_app) > 1:
            return semilla, a, muros, numeros, mitad
    raise RuntimeError("sin akari")


sem_a, A, MUROS, NUMS, EN_CARTA = elegir_akari()
R["64"] = dict(n=6, muros=A["muros"], numeros={f"{r},{c}": v for (r, c), v in sorted(NUMS.items())},
               en_carta=[f"{r},{c}" for (r, c) in EN_CARTA], bombillas=A["bombillas"], semilla=sem_a)

# ------------------------------------------------------------------ 69 Puerta atascada (bloques deslizantes)
for semilla in range(1, 200):
    B = G.rush_hour(semilla, 6, 9)
    if 9 <= B["movimientos_minimos"] <= 14:
        B["ruta"] = G.rush_hour_ruta(B)
        B["semilla"] = semilla
        break
R["69"] = B

# ------------------------------------------------------------------ 72 Tapiz de la batalla (nonograma: llama de dragón)
TAPIZ = [
    "..##..",
    ".####.",
    "######",
    "##..##",
    ".####.",
    "..##..",
]
sol = [[1 if ch == "#" else 0 for ch in fila] for fila in TAPIZ]
pf = [G._pistas_de(f) for f in sol]
pc = [G._pistas_de([sol[r][c] for r in range(6)]) for c in range(6)]
cuenta = G._contar_nonograma(6, 6, pf, pc)
if cuenta != 1:
    # probar variantes hasta dar con un dibujo de solución única
    raise RuntimeError(f"el tapiz tiene {cuenta} soluciones")
R["72"] = dict(solucion=sol, filas=pf, columnas=pc)

# ------------------------------------------------------------------ 84 La profecía (ordenar palabras)
FRASE = ["SOLO", "EL", "FUEGO", "VENCERÁ", "AL", "HIELO", "DEL", "NORTE"]
PALABRA_DE = {"14": "HIELO", "20": "SOLO", "40": "VENCERÁ", "46": "DEL", "51": "FUEGO", "64": "NORTE", "69": "AL", "72": "EL"}
assert sorted(PALABRA_DE.values()) == sorted(FRASE)
REGLAS_ORDEN = [
    ("La profecía empieza con SOLO.", lambda o: o[0] == "SOLO"),
    ("FUEGO va justo después de EL.", lambda o: o.index("FUEGO") == o.index("EL") + 1),
    ("VENCERÁ va justo después de FUEGO.", lambda o: o.index("VENCERÁ") == o.index("FUEGO") + 1),
    ("AL va justo antes de HIELO.", lambda o: o.index("AL") + 1 == o.index("HIELO")),
    ("VENCERÁ va antes que HIELO.", lambda o: o.index("VENCERÁ") < o.index("HIELO")),
    ("DEL va justo antes de NORTE.", lambda o: o.index("DEL") + 1 == o.index("NORTE")),
    ("NORTE es la última palabra.", lambda o: o[-1] == "NORTE"),
]
soluciones = [p for p in itertools.permutations(FRASE) if all(r[1](list(p)) for r in REGLAS_ORDEN)]
assert soluciones == [tuple(FRASE)], soluciones[:3]
# con la mitad de las reglas no basta
for k in range(len(REGLAS_ORDEN)):
    resto = [r for i, r in enumerate(REGLAS_ORDEN) if i != k]
    n = sum(1 for p in itertools.permutations(FRASE) if all(r[1](list(p)) for r in resto))
    print("sin la regla", k + 1, "->", n, "soluciones") if n > 1 else print("la regla", k + 1, "es redundante (", n, ")")
R["84"] = dict(frase=FRASE, palabra_de=PALABRA_DE, reglas=[r[0] for r in REGLAS_ORDEN])

json.dump(R, open(SALIDA, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print("instancias OK ->", SALIDA)

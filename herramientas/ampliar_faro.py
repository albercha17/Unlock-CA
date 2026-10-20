"""Amplía El Faro de Cabo Niebla a 36 cartas y cambia sus protagonistas por Cristina y Alberto (20 oct 2026). Idempotente.

  - Cambia Inés → Cristina y Marcos → Alberto en cartas.json, los minijuegos, la portada y el texto de la sinopsis; redefine su aspecto
    (la cara sale de personajes/hoja.png; la ropa es la de una noche de tormenta en un faro). Las ilustraciones antiguas, en las que salen
    Inés y Marcos, se tienen que volver a generar: se marcan como pendientes.
  - Añade tres puzles entre la radio y la sala de la lente: el plano de la bahía (islas tipo Nurikabe), la lámpara de la mesa (sombras)
    y el temporizador de la lente (la característica de la luz). Láminas e instancias: dibujos_ampliacion.py / instancias_ampliacion.py.
Uso (desde la raíz del repo):  python herramientas/ampliar_faro.py
"""
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FARO = os.path.join(RAIZ, "juegos", "el-faro")
sys.path.insert(0, AQUI)

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado, ojos azules. Viste un chubasquero amarillo con capucha, un jersey grueso de lana y botas de agua, y lleva una linterna.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Viste una chaqueta impermeable gris sobre un jersey azul marino de cuello alto y lleva una mochila con una antena de radio asomando.",
    "Anselmo": "Anselmo, hombre de unos 75 años, barba blanca, gorro de lana verde, jersey de punto grueso, mirada amable, siempre con un termo.",
}


def cambiar_nombres(s):
    s = s.replace("Inés Valcárcel", "Cristina").replace("Marcos Ibáñez", "Alberto")
    s = re.sub(r"\bInés\b", "Cristina", s)
    s = re.sub(r"\bMarcos\b", "Alberto", s)
    return s


def pieza(que):
    return f"Carta dibujada por código (herramientas/dibujos_ampliacion.py; no se pide a ChatGPT): {que}."


def cartas_nuevas(inst):
    ba, so = inst["faro_bahia"], inst["faro_sombras"]
    tierra = ", ".join(f"{'ABCDEF'[f]}{c + 1}" for f, c in ba["tierra"])
    orden = ", ".join(so["solucion"])
    luz = " ".join(str(s + 1) for s, v in enumerate(inst["faro_destellos"]["solucion"]) if v)
    return {
        "44": dict(
            titulo="Carta 44 — La guardia costera", tipo="gris", coge=[45, 46, 47],
            descripcion=[
                "La radio cruje y responde la guardia costera: el «Estrella del Norte» ha perdido el radar y no sabe por dónde pasa el canal entre los islotes de la bahía. Anselmo dibujó la bahía en dos hojas, con cuántas casillas mide cada islote (cartas 46 y 47). En el panel de la radio (carta 45) se marca el plano y se transmite.",
                "Coged las cartas 45, 46 y 47."],
            pistas=["Hay un puzle: el plano de la bahía.", "El plano está partido en dos hojas: filas A a C (46) y D a F (47); la 47 trae las reglas.", "Coged las cartas 45, 46 y 47."],
            arte="La sala de máquinas de un faro en una noche de tormenta, con una radio de onda corta antigua encendida y una luz verde en su escala; sobre la mesa, dos hojas con un plano de islotes dibujado a lápiz. Alberto sostiene el micrófono de la radio con cara de concentración y Cristina, con el chubasquero amarillo empapado, señala las hojas con gesto de urgencia."),
        "45": dict(
            titulo="Carta 45 — El plano de la bahía", tipo="verde",
            descripcion=[
                "Es un juego de la app: la bahía en una rejilla de 6 × 6. Tocando una casilla se marca como islote. Cada islote mide lo que dice su número en el plano de Anselmo (cartas 46 y 47); dos islotes no se tocan por un lado; el mar va todo unido y nunca forma un charco de 2 × 2.",
                "Al transmitir el plano bueno, el carguero toma el canal. Coged la carta 54."],
            pistas=["Hacen falta las dos hojas del plano (cartas 46 y 47).", "Empezad por los islotes de 1 casilla y por las casillas que tocan a dos números distintos (esas son mar). Después, evitad los charcos de 2 × 2.", f"Son islote: {tierra}."],
            arte="El panel de una radio antigua de faro con una rejilla de botones luminosos, unos azules y otros color arena, y una aguja temblando, a la luz de una lámpara. Cristina pulsa un botón con cuidado, mordiéndose el labio, y Alberto compara con un papel, muy serio."),
        "46": dict(titulo="Carta 46 — Plano de la bahía (1 de 2)", tipo="gris",
                   descripcion=["La primera hoja del plano de la bahía de Anselmo: las filas A, B y C, con el tamaño de cada islote."],
                   pistas=["Es la mitad de arriba del plano (carta 45).", "La otra mitad y las reglas están en la carta 47.", f"Son islote: {tierra}."],
                   arte=pieza("la primera hoja del plano")),
        "47": dict(titulo="Carta 47 — Plano de la bahía (2 de 2)", tipo="gris",
                   descripcion=["La segunda hoja del plano de la bahía de Anselmo: las filas D, E y F, con el tamaño de cada islote y las reglas del plano."],
                   pistas=["Es la mitad de abajo del plano (carta 45) y trae las reglas.", "La otra mitad está en la carta 46.", f"Son islote: {tierra}."],
                   arte=pieza("la segunda hoja del plano")),
        "54": dict(
            titulo="Carta 54 — El cuarto de guardia", tipo="gris", coge=[55, 56, 57], descarta=[44, 45, 46, 47],
            descripcion=[
                "El capitán toma el canal, pero necesita ver la luz del faro. La escalera de hierro hacia la lente tiene una trampilla con un capricho de Anselmo: en el cuarto de guardia hay una lámpara de mesa (carta 55), una sombra pintada en la pared (carta 56) y un estante con sus cosas (carta 57). La trampilla se abre si la sombra de tres cosas coincide con la pintura.",
                "Coged las cartas 55, 56 y 57. Descartad las cartas 44, 45, 46 y 47."],
            pistas=["Hay un puzle: la lámpara, la sombra pintada y el estante.", "La sombra (56) está hecha con tres cosas del estante (57), puestas en fila.", "Coged las cartas 55, 56 y 57. Descartad las cartas 44, 45, 46 y 47."],
            arte="El cuarto de guardia de un faro con una lámpara de mesa encendida, una pared con una extraña sombra pintada en negro, un estante con un farol, un ancla, una botella, una tetera, una gaviota de madera, un catalejo, una campana y una llave, y una trampilla de hierro en el techo. Alberto mira la sombra con la cabeza ladeada de curiosidad y Cristina coge la tetera con una sonrisa traviesa."),
        "55": dict(
            titulo="Carta 55 — La lámpara de la mesa", tipo="verde",
            descripcion=[
                "Es un juego de la app: la mesa de la lámpara y el estante del farero. Hay que poner tres cosas en fila, de izquierda a derecha, para que su sombra sea la que Anselmo pintó en la pared (carta 56). Las cosas del estante están dibujadas en la carta 57.",
                "Al acertar, se abre la trampilla. Coged la carta 64."],
            pistas=["Comparad la sombra de la pared (56) con las cosas del estante (57).", "Una cosa está tumbada, otra tiene asa y pitorro y la tercera es de hierro, con brazos curvos.", f"De izquierda a derecha: {orden}."],
            arte="Una lámpara de mesa de latón encendida sobre una mesa de madera en un faro, proyectando sombras de objetos en una pared encalada. Cristina coloca un catalejo en la mesa, conteniendo la risa, y Alberto, agachado, mira la sombra con un ojo cerrado."),
        "56": dict(titulo="Carta 56 — La sombra en la pared", tipo="gris",
                   descripcion=["La sombra que Anselmo pintó en la pared del cuarto de guardia: tres cosas suyas puestas en fila delante de la lámpara."],
                   pistas=["Es la sombra que hay que reproducir con la lámpara (carta 55).", "Son tres cosas del estante (carta 57), de izquierda a derecha.", f"De izquierda a derecha: {orden}."],
                   arte=pieza("la sombra en la pared")),
        "57": dict(titulo="Carta 57 — El estante del farero", tipo="gris",
                   descripcion=["El estante de Anselmo con ocho cosas suyas numeradas: farol, ancla, botella, tetera, gaviota, catalejo, campana y llave."],
                   pistas=["Son las cosas que se pueden poner ante la lámpara (carta 55).", "Comparad sus formas con la sombra de la pared (carta 56).", f"De izquierda a derecha: {orden}."],
                   arte=pieza("el estante del farero")),
        "64": dict(
            titulo="Carta 64 — La escalera de hierro", tipo="gris", coge=[65, 66, 67], descarta=[54, 55, 56, 57],
            descripcion=[
                "La trampilla se abre a la escalera de hierro. Antes de subir, Cristina se fija en el temporizador de la lente (carta 65): cada faro tiene su propia luz y, si el capitán ve otra, creerá que es otro faro y se estrellará. El almanaque de faros (carta 66) y una nota de Anselmo (carta 67) dicen cómo es la de Cabo Niebla.",
                "Coged las cartas 65, 66 y 67. Descartad las cartas 54, 55, 56 y 57."],
            pistas=["Hay un puzle: el temporizador, el almanaque y la nota.", "El almanaque (66) dice la luz de cada faro; la nota (67), cómo pasarla a segundos.", "Coged las cartas 65, 66 y 67. Descartad las cartas 54, 55, 56 y 57."],
            arte="Una escalera de caracol de hierro que sube hacia la cúpula de un faro, con un viejo temporizador de engranajes y doce botones junto a la barandilla y un almanaque abierto colgado de un clavo; la lluvia golpea los cristales. Cristina lee el almanaque a la luz de la linterna con los ojos entrecerrados y Alberto toca un botón del temporizador con cara de duda."),
        "65": dict(
            titulo="Carta 65 — El temporizador de la lente", tipo="verde",
            descripcion=[
                "Es un juego de la app: doce casillas, una por segundo del ciclo de la luz. Hay que encender las casillas de la luz de Cabo Niebla, que viene en el almanaque (carta 66) y se pasa a segundos con la nota de Anselmo (carta 67).",
                "Al programarla bien, la lente queda lista. Coged la carta 78."],
            pistas=["Hacen falta el almanaque (66) y la nota de Anselmo (67).", "Cabo Niebla: destello, destello, destello, largo. Un destello es 1 segundo de luz y uno oscuro; un largo, 2 de luz y uno oscuro.", f"Encended los segundos {luz}."],
            arte="Un temporizador de engranajes de latón con doce botones en fila, unos encendidos en amarillo, junto a la escalera de un faro. Alberto pulsa un botón con decisión y Cristina cuenta los segundos con los dedos, en voz alta."),
        "66": dict(titulo="Carta 66 — Almanaque de faros", tipo="gris",
                   descripcion=["El almanaque de faros de la costa norte de 1923: la luz de cada faro, escrita como una lista de destellos y largos."],
                   pistas=["Sirve para el temporizador de la lente (carta 65).", "Buscad Cabo Niebla y pasadlo a segundos con la nota de Anselmo (carta 67).", f"Encended los segundos {luz}."],
                   arte=pieza("el almanaque de faros")),
        "67": dict(titulo="Carta 67 — Nota de Anselmo", tipo="gris",
                   descripcion=["Una nota de Anselmo que explica cómo se lee el almanaque: cuánto dura un destello, un largo y la oscuridad, con un ejemplo dibujado."],
                   pistas=["Sirve para el temporizador de la lente (carta 65).", "Mirad el ejemplo de Punta Gaviota: cada elemento ocupa su luz y un segundo oscuro.", f"Encended los segundos {luz}."],
                   arte=pieza("la nota de Anselmo")),
    }


def main():
    import instancias_ampliacion  # noqa: F401  (solo para comprobar que existe)
    inst = json.load(open(os.path.join(AQUI, "instancias_ampliacion.json"), encoding="utf-8"))
    ruta = os.path.join(FARO, "cartas.json")
    d = json.loads(cambiar_nombres(open(ruta, encoding="utf-8").read()))
    d["_meta"]["personajes"] = PERSONAJES
    nuevas = cartas_nuevas(inst)
    out = {}
    for k, c in d.items():
        if k in nuevas:
            continue
        out[k] = c
        if k == "85":
            out.update(nuevas)
    if "44" not in out:
        out.update(nuevas)
    c85 = out["85"]
    c85["descripcion"] = [t.replace("Coged la carta 78", "Coged la carta 44") for t in c85["descripcion"]]
    c78 = out["78"]
    extra = [64, 65, 66, 67]
    c78["descarta"] = [x for x in c78.get("descarta", []) if x not in extra] + extra
    texto = ", ".join(str(x) for x in c78["descarta"][:-1]) + " y " + str(c78["descarta"][-1])
    c78["descripcion"] = [re.sub(r"Descartad las cartas [0-9, y]+\.", f"Descartad las cartas {texto}.", t) for t in c78["descripcion"]]
    c78["pistas"] = [re.sub(r"Descartad las cartas [0-9, y]+\.", f"Descartad las cartas {texto}.", t) for t in c78["pistas"]]
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    # textos fuera de cartas.json
    for rel in ("index.html", "prompts.html", "minijuegos/15-cuaderno.js", "minijuegos/85-radio.js"):
        p = os.path.join(FARO, rel)
        s = cambiar_nombres(open(p, encoding="utf-8").read())
        if rel == "minijuegos/85-radio.js":
            s = s.replace("¡Sintonizado! Coged la carta 78.", "¡Sintonizado! Responde la guardia costera. Coged la carta 44.")
        if rel == "index.html":
            s = s.replace("tienen una hora para encender el faro", "tienen hora y cuarto para encender el faro")
            s = s.replace("segundos: 3600,", "segundos: 4500,")
            s = s.replace("      '85': './minijuegos/85-radio.js',", "      '85': './minijuegos/85-radio.js',\n      '45': './minijuegos/45-bahia.js',\n      '55': './minijuegos/55-sombras.js',\n      '65': './minijuegos/65-destellos.js',") if "45-bahia" not in s else s
        open(p, "w", encoding="utf-8", newline="\n").write(s)
    # ilustraciones: todas las que tienen personas se rehacen; las nuevas sin imagen llevan relleno
    from construir_aventuras_util import placeholder
    pend = []
    for k, c in out.items():
        if k == "_meta":
            continue
        img = os.path.join(FARO, "img", f"{k}.jpg")
        if not c["arte"].startswith("Carta dibujada por código") and (re.search(r"Cristina|Alberto|Anselmo|anciano", c["arte"]) or not os.path.exists(img)):
            pend.append(k)
        if not os.path.exists(img):
            placeholder(img, c["titulo"].split("—", 1)[1].strip(), "#1c3a4d", "#0a1218")
    json.dump(sorted(pend, key=lambda k: (k != "P", int(k) if k != "P" else 0)), open(os.path.join(FARO, "img", "pendientes.json"), "w", encoding="utf-8"))
    subprocess.run([sys.executable, os.path.join(AQUI, "sincronizar_cartas.py")], check=True, stdout=subprocess.DEVNULL)
    print(f"El Faro: {len(out) - 1} cartas; ilustraciones por (re)hacer: {pend}")


if __name__ == "__main__":
    main()

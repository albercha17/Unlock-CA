"""La Final del Siglo, 1970: La Copa de Cristal — versión de 60 cartas (22 oct 2026), mucho más difícil y variada.

Once puzles de tipos que no salen en ningún otro juego de la serie, con las pistas dibujadas o en acertijo (ninguna carta explica cómo se resuelve su puzle):
una liguilla que se reconstruye con su clasificación, seis cromos con dos caras y un acertijo del míster, seis jugadas del VAR con un reglamento de casos raros,
un pase en cadena que cortan los rivales, una alineación de suma máxima, una tanda de penaltis contra un portero que mira los dos últimos tiros, el mosaico de
una grada que se pinta con una regla de vecinas, el calendario de una liga por el método del círculo, un cuadro de eliminatorias reconstruido con titulares,
unos cambios del míster que se repiten tres veces y la cerradura de la Copa con cinco aros. Solo 16 cartas tienen a Cristina y Alberto (escenas); el resto
son objetos y pistas sin personas; los cromos son las únicas cartas de dos caras. Las cartas-pista las dibuja herramientas/futbol.py (instancias_futbol.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402
import instancias_futbol as I  # noqa: E402

ESTILO = ("Ilustración pictórica semirrealista con aire de póster de fútbol de los años 70, colores saturados de césped verde, rojo, azul y amarillo, estadio con la grada llena de bufandas y banderines, "
          "luz dorada de tarde, balones de cuero con paneles blancos y negros, redes y porterías de madera, formato vertical 2:3. Sin texto, letras ni números legibles en la imagen; los carteles, "
          "marcadores y papeles solo muestran rayas decorativas. Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado recogido en una coleta alta, ojos azules. Viste ropa deportiva de los años 70: chándal retro rojo con rayas blancas en las mangas, un silbato colgado al cuello, un cronómetro en la muñeca y zapatillas blancas.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Viste ropa deportiva de los años 70: chándal retro azul con rayas blancas, una gorra de visera, una bufanda roja y blanca del club al cuello y una pizarra táctica bajo el brazo.",
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado recogido en una coleta alta, ojos azules, chándal retro rojo con rayas blancas en las mangas, silbato colgado al cuello, cronómetro en la muñeca y zapatillas blancas. "
        "Alberto: hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones, chándal retro azul con rayas blancas, gorra de visera, bufanda roja y blanca del club y una pizarra táctica bajo el brazo. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo cinematográfico de película deportiva de los años 70, luz dorada de tarde y colores saturados. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Cristina señala la foto de un estadio antiguo en un álbum de cromos. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul y dorada y los dos son absorbidos por un túnel de luz. "
         "Escena 3 (8-12 s): caen en el túnel de vestuarios de un estadio de 1970 con el rugido de la grada al fondo; el aparato golpea un carro de balones y su cristal sale rodando hacia el campo. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, con chándales retro, asombrados, mientras un entrenador con gabardina les da una pizarra táctica; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe sordo al aterrizar, rugido de una grada, silbato de árbitro y organillo, sin voz de narrador.")

SIN_GENTE = "Sin ninguna persona en la imagen. "

MOSAICOS = {
    "campo": dict(filas=1, cols=2, cartas=["42", "49"], titulo="El campo de entrenamiento"),
    "cuadro": dict(filas=2, cols=1, cartas=["61", "63"], titulo="El cuadro de la Copa"),
}
POS = {(2, 1): ["mitad de arriba", "mitad de abajo"], (1, 2): ["mitad izquierda", "mitad derecha"]}

LADOS = ["izquierda", "centro", "derecha"]
_LIG = I.LIGUILLA
_S_LIG = ", ".join(f"{_LIG['equipos'][_LIG['partidos'][i][0]]} {_LIG['resultados'][i][0]}-{_LIG['resultados'][i][1]} {_LIG['equipos'][_LIG['partidos'][i][1]]}" for i in _LIG["desconocidos"])
_S_CRO = " y ".join(str(d) for d in I.CROMOS["solucion"])
_S_VAR = ", ".join(f"{'ABCDEF'[i]} {'fuera de juego' if f else 'válida'}" for i, f in enumerate(I.VAR["fuera"]))
_S_PAS = " → ".join(I.PASE["camino"] and [["P", "A", "B", "C", "D", "E", "Z"][k] for k in I.PASE["camino"]])
_S_ALI = ", ".join(f"{I.ALINEACION['jugadores'][i]} de {I.ALINEACION['puestos'][p].lower()}" for i, p in enumerate(I.ALINEACION["solucion"]))


def _tanda():
    ult = list(I.PENALTIS["ultimos"])
    res = []
    for _ in range(I.PENALTIS["tanda"]):
        salto = I.PENALTIS["regla"][f"{ult[-2]}{ult[-1]}"]
        k = next(x for x in (0, 1, 2) if x != salto)
        res.append(k)
        ult.append(k)
    return res


_S_PEN = ", ".join(LADOS[k] for k in _tanda())


def _cuadro():
    bits = I.ELIMINATORIAS["bits"]
    eq = I.ELIMINATORIAS["equipos"]
    r = I.jugar_cuadro(bits)
    cuartos = [eq[r["cuartos"][i][bits[i]]] for i in range(4)]
    semis = [eq[r["semis"][i][bits[4 + i]]] for i in range(2)]
    return f"pasan a semifinales {', '.join(cuartos)}; a la final, {' y '.join(semis)}; campeón, {eq[r['campeon']]}"


_S_ELI = _cuadro()
_S_CAL = ", ".join(f"{I.CALENDARIO['clubes'][a]}-{I.CALENDARIO['clubes'][b]}" for a, b in I.CALENDARIO["solucion"])
_S_SUS = ", ".join(f"puesto {k + 1}: {d}" for k, d in enumerate(I.SUSTITUCIONES["final"]))
_S_GRA = "".join("#" if v else "·" for v in I.GRADA["final"])
_S_ARO = ", ".join(str(p) for p in I.FINAL_ARO)


def codigo(que):
    return f"Carta dibujada por código (herramientas/futbol.py; no se pide a ChatGPT): {que}."


def pieza(carta, mosaico, que, pistas):
    m = MOSAICOS[mosaico]
    i = m["cartas"].index(carta)
    pos = POS[(m["filas"], m["cols"])][i]
    return dict(titulo=f"Carta {carta} — {m['titulo']} ({pos})", tipo="gris",
                mosaico=dict(id=mosaico, filas=m["filas"], cols=m["cols"], fila=i // m["cols"], col=i % m["cols"]),
                descripcion=[que], pistas=pistas, arte=codigo(f"{pos} de «{m['titulo']}»"))


def gris(carta, titulo, que, pistas):
    return dict(titulo=f"Carta {carta} — {titulo}", tipo="gris", descripcion=[que], pistas=pistas, arte=codigo(titulo))


def app(carta, titulo, que, sale, pistas, arte):
    return dict(titulo=f"Carta {carta} — {titulo}", tipo="verde", descripcion=[que, f"Al resolverlo, coged la carta {sale}."], pistas=pistas, arte=arte)


def _lista(xs):
    xs = [str(x) for x in xs]
    return ", ".join(xs[:-1]) + " y " + xs[-1] if len(xs) > 1 else xs[0]


def escena(carta, titulo, coge, descarta, texto, pistas, arte):
    partes = []
    if coge:
        partes.append("Coged las cartas " + _lista(coge) + "." if len(coge) > 1 else f"Coged la carta {coge[0]}.")
    if descarta:
        partes.append("Descartad " + ("las cartas " + _lista(descarta) if len(descarta) > 1 else f"la carta {descarta[0]}") + ".")
    lineas = [texto, " ".join(partes)]
    c = dict(titulo=f"Carta {carta} — {titulo}", tipo="gris", descripcion=lineas, pistas=pistas + [lineas[-1]], arte=arte)
    if coge:
        c["coge"] = coge
    if descarta:
        c["descarta"] = descarta
    return c


def combinable(carta, titulo, color, con, da, que, arte):
    return dict(titulo=f"Carta {carta} — {titulo}", tipo=color, combina=[con, da],
                descripcion=[que, f"Combinadla con la carta {con}: sumad sus números ({carta} + {con} = {da}) y coged la carta {da}."],
                pistas=[que.split(".")[0] + ".", f"Se combina con la carta {con}.", f"{carta} + {con} = {da}."], arte=arte)


def cromo(carta, que, pistas, otra):
    return dict(titulo=f"Carta {carta} — Cromos del Club Estrella", tipo="gris", reverso=True,
                descripcion=[que + " Es una carta de dos caras: por delante solo se ve la camiseta con su dorsal y el nombre; dándole la vuelta (en el Modo PC, botón «Dar la vuelta»; en papel, hoja de reversos a doble cara), se ve la ficha técnica de cada jugador."],
                pistas=pistas, arte=codigo("el anverso (camisetas) y el reverso (fichas) de los cromos"))


J = {
    # ------------------------------------------------------------------ El vestuario
    "P": escena("P", "Llegada al estadio", [10, 12], [],
                "Undécima parada del Cronoportal: el estadio del Club Estrella, en 1970, una hora y media antes de la final del siglo. Aterrizáis en el túnel de vestuarios con el rugido de la grada al fondo, y el aparato golpea un carro de balones. Su cristal de energía sale rodando por el túnel hasta caer, de rebote, dentro de la Copa de cristal que un mozo lleva en ese momento al palco, donde quedará guardada bajo llave hasta que acabe la final. Un entrenador con gabardina os toma por su cuerpo técnico: «¡Por fin! Nos falta gente, venid al vestuario».",
                ["Mirad a vuestro alrededor y revisad el aparato."],
                "El túnel de vestuarios de un estadio de fútbol de 1970, con la luz del campo y el rugido de la grada al fondo; un carro de balones de cuero volcado y balones por el suelo. En primer plano, el Cronoportal, un aparato de latón y cristal, humea con la luz azul apagándose. Cristina, con la boca abierta y los ojos muy abiertos de asombro, y Alberto, con una ceja arqueada y la bufanda torcida de incredulidad, se levantan aturdidos con chándales retro."),
    "10": escena("10", "El vestuario del Estrella", [14, 16, 18, 19, 20, 21, 22], ["P"],
                 "En el vestuario del Estrella, Don Remigio, el míster, anda de cabeza: ha perdido la hoja de la liguilla clasificatoria y la lista de convocados. Sobre el banco, la clasificación de la liguilla con los resultados que recuerda (carta 16), un acertijo del míster clavado en el tablón (carta 18) y dos hojas de cromos de dos caras (cartas 19 y 21: por delante, el dorsal y el nombre; por detrás, la ficha). Entre las botas, Cristina encuentra la mitad de un pase de prensa (carta 22).",
                 ["Hay dos puzles: la liguilla y la convocatoria.", "Los cromos tienen dos caras: en el Modo PC, botón «Dar la vuelta»."],
                 "Un vestuario de fútbol de 1970: bancos de madera, camisetas rojas y blancas colgadas en perchas, botas de cuero y un tablón de corcho. Sobre el banco, seis cromos de jugadores boca arriba y boca abajo. Cristina da la vuelta a un cromo con curiosidad y los ojos entrecerrados y Alberto examina otro con la boca torcida de duda."),
    "12": combinable("12", "Cronoportal sin cristal", "azul", 62, 74,
                     "El Cronoportal: una consola de latón y cristal con un anillo central apagado y un hueco vacío en el pecho, donde iba el cristal de energía.",
                     SIN_GENTE + "Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo de cristal central apagado y un hueco circular vacío en el pecho del aparato, sobre un banco de madera de un vestuario, con una camiseta roja colgada al fondo."),
    "14": app("14", "La liguilla del club", "Es un juego de la app: cuatro equipos jugaron todos contra todos y falta la mitad de los marcadores. Hay que escribir los cuatro que faltan para que cuadre la clasificación.", 24,
              ["La clasificación y los resultados conocidos están en la carta 16.", "Cada victoria vale 2 puntos y cada empate, 1. Empezad por el equipo que no ha ganado ni empatado: todos sus partidos los perdió, y sus goles son los que ya conocéis.", f"Faltan: {_S_LIG}. Aro de la tabla: {I.ARO['14']}."],
              SIN_GENTE + "Un tablón de corcho de un vestuario con una hoja de papel cuadriculado clavada, un lápiz y una goma, bajo la luz de un fluorescente, en un estadio de 1970."),
    "16": gris("16", "La clasificación de la liguilla", "La clasificación de la liguilla clasificatoria, con los partidos jugados, ganados, empatados, perdidos, goles a favor y en contra y puntos de cada equipo, y dos resultados conocidos.",
               ["Es la clasificación de la liguilla (carta 14).", "Dos partidos de los seis se conocen.", "En 1970, una victoria valía 2 puntos."]),
    "18": gris("18", "El acertijo del míster", "Un acertijo del míster clavado en el tablón del vestuario, que describe a dos jugadores.",
               ["Dice a qué dos jugadores hay que elegir (carta 20).", "Cada jugador se describe comparando su altura o su edad con las de otros de un grupo.", "Los datos de cada jugador están por detrás de los cromos (cartas 19 y 21)."]),
    "19": cromo("19", "Tres cromos de la plantilla del Club Estrella.", ["Son tres jugadores de la plantilla (carta 20).", "Dad la vuelta a la carta para leer sus fichas técnicas.", "Los otros tres jugadores están en la carta 21."], "21"),
    "21": cromo("21", "Otros tres cromos de la plantilla del Club Estrella.", ["Son tres jugadores de la plantilla (carta 20).", "Dad la vuelta a la carta para leer sus fichas técnicas.", "Los otros tres jugadores están en la carta 19."], "19"),
    "20": app("20", "La convocatoria", "Es un juego de la app: el míster necesita a dos jugadores de la plantilla y los describe en un acertijo. Hay que elegir sus dos camisetas.", 28,
              ["El acertijo está en la carta 18 y las fichas, por detrás de los cromos de las cartas 19 y 21.", "Cada descripción tiene dos partes: primero, un grupo (por ejemplo, los zurdos que no son defensas); luego, el más alto, el más bajo, el más joven o el más veterano de ese grupo.", f"Son los dorsales {_S_CRO}."],
              SIN_GENTE + "Un tablón de corcho de un vestuario de fútbol con una hoja con una lista de nombres, chinchetas y una camiseta roja con un número en la espalda colgada de una percha."),
    "22": combinable("22", "Media pase de prensa", "azul", 35, 57, "Una mitad de un pase de prensa plastificado de un estadio, con la mitad de una foto en blanco y negro y el sello del club.",
                     SIN_GENTE + "La mitad izquierda de un pase de prensa plastificado de un estadio, con la mitad de una foto en blanco y negro y el sello rojo de un club, sobre unas botas de fútbol de cuero."),
    "24": escena("24", "El despacho del míster", [26], [14, 16],
                 "La tabla cuadra y Don Remigio respira: ya sabe quién ha ganado qué en la liguilla. En su despacho, un cuartito con una mesa llena de papeles y una taza de café frío, os enseña un recorte de periódico con los titulares de la última Copa y lo guarda en un sobre para después (carta 26).",
                 ["Mirad lo que os enseña Don Remigio."],
                 "El despacho de un entrenador de fútbol de 1970: una mesa llena de papeles, un cenicero, una taza de café y una pizarra táctica pegada a la pared; Don Remigio, con gabardina y sombrero, entrega un sobre con un recorte de periódico a Cristina y Alberto. Cristina lo coge con una sonrisa agradecida y el pulgar en alto; Alberto repasa el recorte con las cejas levantadas de sorpresa."),
    "26": gris("26", "Los titulares de la prensa", "Un recorte de periódico con cinco titulares sobre la última Copa, numerados.",
               ["Son los titulares del cuadro de la Copa (carta 51).", "Cada titular dice algo verdadero de un partido o de un equipo.", "El cuadro vacío está en las cartas 61 y 63."]),
    "28": escena("28", "La lista entregada", [35], [18, 19, 20, 21],
                 "Don Remigio entrega la lista al árbitro y, agradecido, os deja pasar a la zona de prensa, donde hay un sobre con la otra mitad del pase de prensa (carta 35).",
                 ["Mirad en la zona de prensa."],
                 "La zona de prensa de un estadio de 1970, con mesas de periodistas, máquinas de escribir y cámaras de fotos, y un sobre marrón sobre una mesa. Cristina abre el sobre con los ojos muy abiertos de emoción; Alberto, al lado, mira por encima de su hombro con una gran sonrisa."),
    "35": combinable("35", "Otra media pase de prensa", "roja", 22, 57, "La otra mitad del pase de prensa, con el resto de la foto y la firma del presidente del club.",
                     SIN_GENTE + "La mitad derecha de un pase de prensa plastificado de un estadio, con el resto de una foto en blanco y negro y una firma, sobre un sobre marrón en una mesa de periodistas."),
    "57": escena("57", "El palco de autoridades", [31, 32], [22, 35, 10, 28],
                 "Las dos mitades del pase de prensa encajan y abren la puerta del palco de autoridades, en lo alto del estadio. Desde allí se ve todo el campo y, sobre una mesa, la vitrina cerrada con la Copa de cristal, que alguien ha dejado allí. A la izquierda, la sala del VAR, donde los árbitros revisan jugadas (carta 31); a la derecha, la pizarra del entrenador (carta 32).",
                 ["Dos sitios: la sala del VAR y la pizarra del entrenador."],
                 "El palco de autoridades de un estadio de 1970, con butacas de madera, banderines y una gran vitrina de cristal con una copa dentro sobre una mesa con mantel rojo; por la ventana, el campo de césped lleno de gente. Cristina muestra el pase de prensa a un portero uniformado con una sonrisa de orgullo; Alberto mira la copa con las manos pegadas al cristal."),
    # ------------------------------------------------------------------ Rama 1: la sala del VAR
    "31": escena("31", "La sala del VAR", [40, 41, 43, 45], [],
                 "Una sala de vídeo-arbitraje con un gran televisor de tubo y una mesa con papeles. Los árbitros necesitan a alguien que decida seis jugadas de entrenamiento, dibujadas desde arriba en dos láminas (cartas 41 y 43) con el reglamento del fuera de juego (carta 45) y una pantalla (carta 40) donde dar el veredicto.",
                 ["Un único puzle: las seis jugadas del VAR."],
                 "Una sala de vídeo-arbitraje de los años 70 con un gran televisor de tubo, una consola con botones y cintas de vídeo, y dos árbitros con camiseta negra de espaldas, mirando un campo dibujado en la pantalla. Cristina, con las manos en la cabeza y los ojos muy abiertos de emoción, y Alberto, con el mando en la mano y una sonrisa de alivio, miran las jugadas."),
    "40": app("40", "La sala del VAR", "Es un juego de la app: seis jugadas dibujadas desde arriba. Hay que decidir si cada una es válida o fuera de juego, según el reglamento.", 30,
              ["Las jugadas están en las cartas 41 y 43 y el reglamento, en la 45.", "En cada jugada, mirad el momento del pase: dónde está quien recibe, dónde está el balón y cuáles son los dos contrarios más cercanos a su línea de gol (el portero cuenta). Después, repasad las excepciones del reglamento.", f"Son: {_S_VAR}. Aro de la bandera: {I.ARO['40']}."],
              SIN_GENTE + "Una pantalla de un televisor de tubo de los años 70 con un campo de fútbol dibujado visto desde arriba, con puntos azules y rojos, junto a una consola con botones y un cronómetro."),
    "41": gris("41", "Las jugadas del VAR (I)", "Tres jugadas de entrenamiento, A, B y C, dibujadas desde arriba: los azules atacan hacia la derecha.", ["Son las jugadas A, B y C del VAR (carta 40).", "Una flecha blanca marca el pase.", "Las jugadas D, E y F están en la carta 43."]),
    "43": gris("43", "Las jugadas del VAR (II)", "Tres jugadas de entrenamiento, D, E y F, dibujadas desde arriba: los azules atacan hacia la derecha.", ["Son las jugadas D, E y F del VAR (carta 40).", "Una flecha blanca marca el pase.", "Las jugadas A, B y C están en la carta 41."]),
    "45": gris("45", "El reglamento del fuera de juego", "El reglamento del fuera de juego, en el libro del árbitro, en versos.", ["Explica cuándo hay fuera de juego (carta 40).", "Hay que mirar el momento del pase, no el del gol.", "Tiene tres excepciones."]),
    "30": escena("30", "La tarjeta del árbitro", [38], [31, 40, 41, 43, 45],
                 "Las seis decisiones coinciden con el libro y el árbitro de campo, al verlo, os agradece la ayuda y os da, de su cartera, media llave pequeña con un llavero en forma de balón: es de la vitrina de la Copa de cristal (carta 38). Una pareja de cifras queda escrita en el cartel de la sala: ya la veréis más adelante.",
                 ["Mirad lo que os da el árbitro."],
                 "Un árbitro con camiseta negra entrega media llave pequeña con un llavero en forma de balón a Cristina y Alberto en la sala del VAR. Cristina la coge con una sonrisa triunfante y la ceja levantada; Alberto aplaude con los pulgares hacia arriba y los ojos brillantes."),
    "38": combinable("38", "Mitad de la llave de la vitrina", "roja", 56, 94, "Una mitad de una llave pequeña con un llavero en forma de balón, de las que abren la vitrina de la Copa.",
                     SIN_GENTE + "La mitad izquierda de una llave pequeña de latón con un llavero de cuero en forma de balón, de las de una vitrina de un museo, sobre una mesa de madera."),
    # ------------------------------------------------------------------ Rama 2: la pizarra del entrenador
    "32": escena("32", "La pizarra del entrenador", [42, 48, 49, 53],  [],
                 "En una sala del palco, la pizarra del entrenador con un campo de entrenamiento dibujado, en dos mitades: juntad la 42 a la izquierda y la 49 a la derecha. Sobre la mesa, la regla del entrenador (carta 53) y una pantalla (carta 48) para ensayar el pase en cadena.",
                 ["Un único puzle: el pase en cadena."],
                 "Una sala de entrenadores con una gran pizarra con un campo de fútbol dibujado con chinchetas de colores, una mesa con papeles y tazas de café. Cristina estudia la pizarra con el ceño fruncido y el dedo en la barbilla; Alberto da golpecitos a una chincheta azul con la mirada fija."),
    "48": app("48", "El pase en cadena", "Es un juego de la app: siete jugadores de un campo de entrenamiento y varios rivales. Hay que encadenar los pases desde el portero hasta el delantero, tocando a todos una vez, sin que nadie corte el balón.", 36,
              ["El campo está en las cartas 42 y 49 y la regla, en la 53.", "Un rival corta un pase solo si está en un punto de la rejilla justo en su camino. Buscad los pases que sí pueden hacerse, empezando por los del portero.", f"Un camino: {_S_PAS}."],
              SIN_GENTE + "Una pizarra con un campo de fútbol y chinchetas azules y rojas conectadas por hilos de lana, sobre una mesa con una taza de café, en una sala de entrenadores."),
    "42": pieza("42", "campo", "Media lámina del campo de entrenamiento.", ["Es la mitad de una lámina: juntadla con la carta 49.", "Es un campo con una rejilla de puntos.", "La regla del entrenador está en la carta 53."]),
    "49": pieza("49", "campo", "Media lámina del campo de entrenamiento.", ["Es la mitad de una lámina: juntadla con la carta 42.", "Es un campo con una rejilla de puntos.", "La regla del entrenador está en la carta 53."]),
    "53": gris("53", "La regla del entrenador", "Una nota del entrenador con la regla del pase en cadena, en versos.", ["Explica cómo viaja el balón (carta 48).", "Un jugador, o un rival, en el camino del pase lo corta.", "Se sale del portero y se acaba en el delantero."]),
    "36": escena("36", "El banquillo", [52, 54, 55, 59], [32, 42, 48, 49, 53],
                 "El pase sale redondo y el entrenador, contento, os lleva al banquillo, donde le queda una decisión: el once del partido. Cinco jugadores, cinco puestos (carta 52). Las notas de cada jugador en cada puesto están en dos hojas (cartas 54 y 55) y la sentencia del míster, en la carta 59.",
                 ["Un único puzle: el once ideal."],
                 "Un banquillo de fútbol de 1970 con un banco de madera, botellas de cristal, mantas y una pizarra táctica, y cinco jugadores con chándal sentados en fila. Cristina cuenta con los dedos las notas de cada uno con los labios apretados; Alberto sostiene una libreta con cara de tener una duda."),
    "52": app("52", "El once del míster", "Es un juego de la app: cinco jugadores y cinco puestos. Hay que poner a cada jugador en un puesto distinto para que la suma de sus notas sea la más alta posible.", 44,
              ["Las notas están en las cartas 54 y 55 y la sentencia del míster, en la 59.", "No sirve poner a cada jugador en su mejor puesto ni elegir el mejor de cada puesto: se estorban. Probad cambios de dos en dos y mirad cuánto sube o baja la suma.", f"El once: {_S_ALI}. Aro de la camiseta: {I.ARO['52']}."],
              SIN_GENTE + "Una pizarra táctica con cinco camisetas de colores colgadas en fila junto a cinco etiquetas de puestos, con una tiza y un borrador sobre un banco de madera."),
    "54": gris("54", "Las notas del entrenador (I)", "La hoja del entrenador con las notas de tres jugadores en los cinco puestos.", ["Son las notas de los tres primeros jugadores (carta 52).", "Cada nota va de 1 a 9.", "Los otros dos jugadores están en la carta 55."]),
    "55": gris("55", "Las notas del entrenador (II)", "La hoja del entrenador con las notas de los otros dos jugadores en los cinco puestos.", ["Son las notas de los dos últimos jugadores (carta 52).", "Cada nota va de 1 a 9.", "Los otros tres jugadores están en la carta 54."]),
    "59": gris("59", "La sentencia del míster", "Una nota del míster con lo que exige del once.", ["Explica cómo debe ser el once (carta 52).", "Cada jugador, un puesto distinto.", "La suma de las cinco notas ha de ser la mayor posible."]),
    # ------------------------------------------------------------------ El túnel y el vestuario visitante
    "44": escena("44", "El túnel de vestuarios", [33, 37, 39, 46, 51, 61, 63], [36, 52, 54, 55, 59],
                 "El míster anuncia su once y salís al túnel de vestuarios, donde dos cosas esperan. Un cartel avisa de que hay que ensayar la tanda de penaltis (carta 46): el informe del entrenador sobre el portero rival, de once penaltis, está en dos hojas (cartas 37 y 39) y la explicación de cómo se lee, en la 33. Y en el tablón de la sala de prensa, el cuadro de la Copa, en dos mitades: juntad la 61 arriba y la 63 abajo (carta 51).",
                 ["Hay dos puzles: la tanda de penaltis y el cuadro de la Copa."],
                 "El túnel de vestuarios de un estadio de 1970, con la luz del campo al fondo, un cartel de entrenamientos y un tablón de corcho con un cuadro de eliminatorias a lo lejos. Cristina mira el cartel con las manos en la cintura y los labios apretados; Alberto cuenta penaltis con los dedos con cara de agobio."),
    "46": app("46", "La tanda de penaltis", "Es un juego de la app: hay que marcar cinco penaltis seguidos. El portero rival decide su salto con una regla fija; si para uno, la tanda empieza de nuevo.", 56,
              ["El informe está en las cartas 37 y 39 y su explicación, en la 33.", "El portero decide su salto mirando solo los dos últimos tiros. Buscad en el informe cuándo hizo lo mismo que hará ahora.", f"Tirad: {_S_PEN}."],
              SIN_GENTE + "El punto de penalti de un estadio de fútbol de 1970 con un balón de cuero sobre la cal blanca y una portería con red de cuerda; una grada llena y borrosa al fondo."),
    "37": gris("37", "El informe de penaltis (I)", "Los seis primeros penaltis del informe del entrenador, con el tiro y el salto del portero.", ["Son los seis primeros penaltis (carta 46).", "El balón es el tiro y el guante naranja, el salto.", "Los demás penaltis están en la carta 39."]),
    "39": gris("39", "El informe de penaltis (II)", "Los cinco últimos penaltis del informe del entrenador, con el tiro y el salto del portero.", ["Son los cinco últimos penaltis (carta 46).", "El balón es el tiro y el guante naranja, el salto.", "Los demás penaltis están en la carta 37."]),
    "33": gris("33", "Cómo se lee el informe", "Una nota del entrenador que explica cómo se lee el informe de penaltis.", ["Explica el informe de los penaltis (carta 46).", "El portero decide antes del tiro.", "Mira solo los dos últimos tiros."]),
    "56": combinable("56", "Otra mitad de la llave", "roja", 38, 94, "La otra mitad de la llave de la vitrina, que el presidente del club os da al ver el ensayo.",
                     SIN_GENTE + "La mitad derecha de una llave pequeña de latón con un llavero de cuero en forma de balón, de las de una vitrina de un museo, entregada por una mano con un guante blanco."),
    "51": app("51", "El cuadro de la Copa", "Es un juego de la app: un cuadro de eliminatorias de ocho equipos, con cuartos, semifinales y final. Con los titulares de la prensa hay que reconstruir quién ganó cada partido.", 58,
              ["Los titulares están en la carta 26 y el cuadro vacío, en las cartas 61 y 63.", "Cada titular dice algo verdadero. Empezad por los que dicen una ronda exacta (en cuartos, en semifinales) y por los que dicen quién ganó a quién.", f"El cuadro: {_S_ELI}."],
              SIN_GENTE + "Un tablón de corcho de una sala de prensa con un cuadro de eliminatorias dibujado con rotulador, con nombres de equipos en tiras de papel y chinchetas, con luz de fluorescente."),
    "61": pieza("61", "cuadro", "Media lámina del cuadro de la Copa.", ["Es la mitad de una lámina: juntadla con la carta 63.", "Son los equipos de arriba, hasta las semifinales.", "Los titulares están en la carta 26."]),
    "63": pieza("63", "cuadro", "Media lámina del cuadro de la Copa.", ["Es la mitad de una lámina: juntadla con la carta 61.", "Son los equipos de abajo, hasta las semifinales.", "Los titulares están en la carta 26."]),
    "58": escena("58", "El vestuario visitante", [69, 70, 71], [51, 61, 63, 26, 24],
                 "El cuadro encaja y un empleado os abre el vestuario visitante, vacío porque el equipo ya está en el campo. Sobre la pizarra, la alineación inicial de Los Rayos con ocho puestos y ocho dorsales (carta 70) y las órdenes de cambios que su míster dará en el segundo tiempo (carta 71). Hay que saber cómo quedará el equipo cuando termine de cambiar (carta 69).",
                 ["Un único puzle: los cambios del míster."],
                 "Un vestuario visitante de un estadio de 1970, con perchas y camisetas azules colgadas, bancos de madera y una pizarra con unas formaciones dibujadas con tiza. Cristina señala la pizarra con un dedo y los ojos entrecerrados de concentración; Alberto, apoyado en un banco, copia las órdenes en una libreta con un bostezo."),
    "69": app("69", "Los cambios del míster", "Es un juego de la app: ocho jugadores en ocho puestos y tres órdenes de cambios que se repiten tres veces. Hay que decir qué dorsal acaba en cada puesto.", 80,
              ["La alineación inicial está en la carta 70 y las órdenes, en la 71.", "Aplicad las tres órdenes, una tras otra, y anotad cómo queda el equipo: es una ronda. Repetid la ronda tres veces, empezando cada vez desde donde acabó la anterior.", f"Queda así: {_S_SUS}. Aro de las flechas: {I.ARO['69']}."],
              SIN_GENTE + "Una pizarra de vestuario con un campo de fútbol dibujado con tiza y ocho fichas redondas con números colocadas en él, con flechas de tiza entre ellas, y un borrador."),
    "70": gris("70", "La alineación inicial", "La alineación inicial de Los Rayos, con ocho puestos numerados y el dorsal de cada jugador.", ["Es la alineación antes de los cambios (carta 69).", "El número en el círculo amarillo es el puesto y el de la camiseta, el dorsal.", "Las órdenes están en la carta 71."]),
    "71": gris("71", "Las órdenes del míster", "Las tres órdenes de cambios del míster, dibujadas con flechas entre puestos.", ["Son los cambios del segundo tiempo (carta 69).", "Se aplican en orden y se repiten.", "Cada flecha lleva al jugador de un puesto al siguiente."]),
    "80": escena("80", "La grada", [72, 75, 79], [58, 69, 70, 71],
                 "Cuando acaba el calentamiento, el equipo de animación de la grada os pide ayuda con el mosaico que los hinchas pintan cada partido, butaca a butaca, en una gran fila circular de la tribuna. Las primeras butacas de la fila 1 están pintadas (carta 75). El encargado de la grada anotó cómo se pinta cada butaca de las filas siguientes (carta 79). Hay que pintar la fila 7 (carta 72).",
                 ["Un único puzle: pintar la fila 7 de la grada."],
                 "La tribuna de un estadio de 1970 llena de aficionados con bufandas y banderines, con una gran fila circular de asientos de madera y un hincha con un megáfono. Cristina pinta un asiento de rojo con un pincel grande y una sonrisa traviesa; Alberto mira las filas desde arriba con una mano en la frente y cara de duda."),
    "72": app("72", "El mosaico de la grada", "Es un juego de la app: la primera fila de una grada circular está pintada. Cada butaca de las filas siguientes se pinta según las dos vecinas de la fila de arriba. Hay que pintar la fila 7.", 82,
              ["La primera fila está en la carta 75 y la regla, en la 79.", "Pintad fila a fila, de la 2 a la 7: cada butaca solo depende de dos vecinas de la fila anterior. No olvidéis que la grada es un anillo.", f"La fila 7 (# pintada, · blanca): {_S_GRA}. Aro de la grada: {I.ARO['72']}."],
              SIN_GENTE + "Una grada circular de un estadio de fútbol vista desde arriba con filas de asientos de madera pintados de rojo y de blanco formando un dibujo, con banderines al fondo y luz de tarde."),
    "75": gris("75", "Las filas de la grada", "Una vuelta entera de la grada, con la primera fila pintada y las demás por pintar.", ["Es la fila 1 de la grada (carta 72).", "Las butacas rojas están pintadas.", "La regla de las butacas está en la carta 79."]),
    "79": gris("79", "La regla de las butacas", "Una nota del encargado de la grada con la regla para pintar cada butaca, en versos.", ["Explica cómo se pinta cada butaca (carta 72).", "Cada butaca mira a dos vecinas de la fila de arriba.", "La grada es un anillo."]),
    "82": escena("82", "El estuche del silbato", [85, 86, 87], [80, 72, 75, 79],
                 "El mosaico queda perfecto y el delegado de la grada os lleva al palco, donde un estuche de madera guarda el silbato del árbitro para el pitido final. Se abre con una cerradura de cinco aros de doce posiciones (carta 85): cada aro parte de un número que os dejó un puzle y gira tantos puestos como flechas hay dibujadas, hacia la derecha las verdes y hacia la izquierda las rojas (cartas 86 y 87).",
                 ["Un único puzle: la cerradura de los cinco aros."],
                 "Un estuche de madera con una cerradura de cinco aros de latón sobre la mesa de un palco de un estadio de 1970, con el campo al fondo por una ventana. Cristina gira un aro con la lengua entre los dientes y los ojos muy abiertos; Alberto lleva la cuenta con los dedos y una mueca de esfuerzo."),
    "85": app("85", "La cerradura de la Copa", "Es un juego de la app: cinco aros de doce posiciones. Cada uno parte de un número que os dejó un puzle y gira tantos puestos como flechas hay dibujadas.", 99,
              ["Los aros y sus giros están en la carta 86 y el dial, en la 87.", "Los cinco números de partida los dejaron la tabla, la bandera, la camiseta, las flechas y la grada. Las flechas verdes avanzan a la derecha y las rojas, a la izquierda; las posiciones van de 1 a 12 y vuelven a empezar.", f"Las posiciones son: {_S_ARO}."],
              SIN_GENTE + "Una cerradura de cinco aros de latón con números, sobre un estuche de madera, con luz de tarde por una ventana."),
    "86": gris("86", "Los cinco aros", "Cinco aros con su dibujo y sus flechas de giro, verdes a la derecha y rojas a la izquierda.", ["Explica cuánto gira cada aro (carta 85).", "Cada aro lleva un dibujo.", "Las flechas verdes giran a la derecha y las rojas, a la izquierda."]),
    "87": gris("87", "El dial", "El dial de doce posiciones de un aro, con el uno arriba.", ["Sirve para colocar los aros (carta 85).", "Se cuenta hacia la derecha.", "Después del 12 viene el 1."]),
    # ------------------------------------------------------------------ La vitrina y el final
    "94": escena("94", "La vitrina de la Copa", [64, 66, 67], [38, 56, 30, 44, 33, 37, 39, 46],
                 "Las dos mitades de la llave encajan y abren la vitrina de la Copa de cristal. Dentro, la Copa y, en su base hueca, el brillo azul de vuestro cristal. Pero la base se cierra con un calendario: el secretario de la liga grabó los cruces de una jornada de la liga de ocho equipos (carta 64). Los cruces de la jornada 1 están en la carta 66 y el método, en la 67.",
                 ["Un único puzle: el calendario de la liga."],
                 "El interior de una vitrina de cristal con una gran copa de cristal sobre un cojín rojo, con una luz azul brillando en la base hueca, en un palco de un estadio de 1970. Cristina apoya las manos en el cristal con los ojos brillantes de emoción; Alberto sostiene una llave con una media sonrisa y la ceja levantada."),
    "64": app("64", "El calendario de la liga", "Es un juego de la app: una liga de ocho equipos que se cruzan con el método del círculo. Hay que formar los cuatro cruces de la jornada 5.", 62,
              ["Los cruces de la jornada 1 están en la carta 66 y el método, en la 67.", "Para pasar de una jornada a la siguiente, el primero se queda quieto y los demás avanzan un puesto en el sentido de las agujas del reloj. Hacedlo cuatro veces, anotando los cruces cada vez.", f"Los cruces: {_S_CAL}."],
              SIN_GENTE + "La base hueca de una copa de cristal con un calendario de ocho nombres grabado alrededor y una luz azul dentro, sobre un cojín rojo, en una vitrina."),
    "66": gris("66", "Los cruces de la jornada 1", "Los cruces de la primera jornada de una liga de ocho equipos, dibujados en dos filas de cuatro, cara a cara.", ["Son los cruces de la jornada 1 (carta 64).", "Cada equipo juega con el que tiene delante.", "El método está en la carta 67."]),
    "67": gris("67", "El método del calendario", "Una nota del secretario de la liga con el método para pasar de una jornada a la siguiente, en versos.", ["Explica cómo se pasa de una jornada a otra (carta 64).", "El primer equipo se queda quieto.", "Los demás avanzan un puesto en el sentido de las agujas del reloj."]),
    "62": combinable("62", "El cristal del Cronoportal", "roja", 12, 74, "El cristal del Cronoportal, que estaba escondido en la base de la Copa de cristal.",
                     SIN_GENTE + "Un cristal redondo de color azul brillante, del tamaño de una moneda grande, con destellos de luz, en la base hueca de una gran copa de cristal sobre un cojín rojo, en una vitrina abierta."),
    "74": escena("74", "Cronoportal con el cristal", [], [62, 12, 64, 66, 67, 94, 57],
                 "Encajáis el cristal en el pecho del Cronoportal y el anillo se enciende con un arco de luz azul. Fuera, la grada ruge: el partido está a punto de acabar y solo falta el pitido final, que el árbitro dará con el silbato del estuche (carta 85).",
                 ["Ya solo queda abrir el estuche del silbato."],
                 "Cristina y Alberto encajan un cristal azul brillante en el hueco del Cronoportal, un aparato de latón y cristal con un anillo que se enciende con un arco de luz azul, sobre una mesa de un palco de un estadio de 1970, con la grada al fondo. Cristina lo sostiene con las dos manos con una enorme sonrisa; Alberto contiene el aliento mirando el anillo con la boca abierta."),
    "99": escena("99", "De vuelta a casa (FIN)", [], [74, 82, 85, 86, 87],
                 "El silbato suena, el árbitro pita el final y la grada estalla en un rugido: el Estrella levanta la Copa. El anillo del Cronoportal se abre en un arco de luz justo cuando la multitud llega al túnel. Aterrizáis en vuestro salón. Alberto mira el aparato: «Mañana, otro destino». Cristina sonríe y guarda en el bolsillo un cromo del Club Estrella. FIN.",
                 [],
                 "La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ven un estadio de fútbol lleno, una grada que ruge y un balón en el aire. Llevan aún sus chándales retro de los años 70. Cristina ríe a carcajadas con un cromo en la mano y Alberto grita de euforia con los brazos en alto y la bufanda al viento. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(juego="La Final del Siglo, 1970 — La Copa de Cristal", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()})

SPEC = dict(final="99", needs={
    "24": ["14", "16"], "28": ["20", "18", "19", "21"], "57": ["22", "35"], "30": ["40", "41", "43", "45"], "36": ["48", "42", "49", "53"],
    "44": ["52", "54", "55", "59"], "56": ["46", "37", "39", "33"], "58": ["51", "26", "61", "63"], "80": ["69", "70", "71"], "94": ["38", "56"],
    "62": ["64", "66", "67"], "82": ["72", "75", "79"], "74": ["12", "62"], "99": ["85", "86", "87", "74"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_T = [
    ("leer", "P", "Llegada", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12."),
    ("leer", "10", "El vestuario del Estrella", "Lee la carta 10. Descarta la P y coge 14, 16, 18, 19, 20, 21 y 22. Los cromos (19 y 21) tienen dos caras: en el Modo PC, botón «Dar la vuelta»."),
    ("app", "14", "La liguilla del club", f"En el móvil: Acción, 14. Con la clasificación (16), los marcadores que faltan son: {_S_LIG}. El mensaje te dice que cojas la 24. Anota el aro de la tabla: {I.ARO['14']}.", "carta 24"),
    ("leer", "24", "El despacho del míster", "Lee la carta 24. Descarta 14 y 16 y coge la 26 (guárdala para el cuadro de la Copa)."),
    ("app", "20", "La convocatoria", f"En el móvil: Acción, 20. Con el acertijo (18) y las fichas de los cromos (19 y 21, dándoles la vuelta), los dorsales son {_S_CRO}. El mensaje te dice que cojas la 28.", "carta 28"),
    ("leer", "28", "La lista entregada", "Lee la carta 28. Descarta 18, 19, 20 y 21 y coge la 35."),
    ("combinar", "22", "35", "El pase de prensa", "Las dos mitades del pase de prensa (22 y 35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El palco de autoridades", "Lee la carta 57. Descarta 22, 35, 10 y 28 y coge 31 y 32."),
    ("leer", "31", "La sala del VAR", "Lee la carta 31. Coge 40, 41, 43 y 45."),
    ("app", "40", "La sala del VAR", f"En el móvil: Acción, 40. Con las jugadas (41 y 43) y el reglamento (45): {_S_VAR}. El mensaje te dice que cojas la 30. Anota el aro de la bandera: {I.ARO['40']}.", "carta 30"),
    ("leer", "30", "La tarjeta del árbitro", "Lee la carta 30. Descarta 31, 40, 41, 43 y 45 y coge la 38."),
    ("leer", "32", "La pizarra del entrenador", "Lee la carta 32. Coge 42, 48, 49 y 53. Junta el campo: 42 a la izquierda y 49 a la derecha."),
    ("app", "48", "El pase en cadena", f"En el móvil: Acción, 48. Con el campo (42 y 49) y la regla (53), una cadena de pases es {_S_PAS}. El mensaje te dice que cojas la 36.", "carta 36"),
    ("leer", "36", "El banquillo", "Lee la carta 36. Descarta 32, 42, 48, 49 y 53 y coge 52, 54, 55 y 59."),
    ("app", "52", "El once del míster", f"En el móvil: Acción, 52. Con las notas (54 y 55) y la sentencia (59), el once es: {_S_ALI}. El mensaje te dice que cojas la 44. Anota el aro de la camiseta: {I.ARO['52']}.", "carta 44"),
    ("leer", "44", "El túnel de vestuarios", "Lee la carta 44. Descarta 36, 52, 54, 55 y 59 y coge 33, 37, 39, 46, 51, 61 y 63. Junta el cuadro: 61 arriba y 63 abajo."),
    ("app", "46", "La tanda de penaltis", f"En el móvil: Acción, 46. Con el informe (37 y 39) y su explicación (33), una tanda que marca los cinco es: {_S_PEN}. El mensaje te dice que cojas la 56.", "carta 56"),
    ("app", "51", "El cuadro de la Copa", f"En el móvil: Acción, 51. Con los titulares (26) y el cuadro (61 y 63): {_S_ELI}. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "El vestuario visitante", "Lee la carta 58. Descarta 51, 61, 63, 26 y 24 y coge 69, 70 y 71."),
    ("app", "69", "Los cambios del míster", f"En el móvil: Acción, 69. Con la alineación (70) y las órdenes (71), tras los cambios queda: {_S_SUS}. El mensaje te dice que cojas la 80. Anota el aro de las flechas: {I.ARO['69']}.", "carta 80"),
    ("leer", "80", "La grada", "Lee la carta 80. Descarta 58, 69, 70 y 71 y coge 72, 75 y 79."),
    ("app", "72", "El mosaico de la grada", f"En el móvil: Acción, 72. Con la fila 1 (75) y la regla (79), la fila 7 es (# roja, · blanca): {_S_GRA}. El mensaje te dice que cojas la 82. Anota el aro de la grada: {I.ARO['72']}.", "carta 82"),
    ("leer", "82", "El estuche del silbato", "Lee la carta 82. Descarta 80, 72, 75 y 79 y coge 85, 86 y 87."),
    ("combinar", "38", "56", "La llave de la vitrina", "Las dos mitades de la llave (38 y 56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "La vitrina de la Copa", "Lee la carta 94. Descarta 38, 56, 30, 44, 33, 37, 39 y 46 y coge 64, 66 y 67."),
    ("app", "64", "El calendario de la liga", f"En el móvil: Acción, 64. Con la jornada 1 (66) y el método (67), los cruces de la jornada 5 son: {_S_CAL}. El mensaje te dice que cojas la 62.", "carta 62"),
    ("combinar", "12", "62", "El cristal", "El Cronoportal (12) y el cristal (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "Cronoportal con el cristal", "Lee la carta 74. Descarta 62, 12, 64, 66, 67, 94 y 57."),
    ("app", "85", "La cerradura de la Copa", f"En el móvil: Acción, 85. Con los aros (86) y el dial (87), las posiciones son {_S_ARO} (los cinco números de partida, uno por aro, los dejaron la tabla, la bandera, la camiseta, las flechas y la grada). El mensaje te dice que cojas la 99.", "carta 99"),
    ("leer", "99", "Final", "Lee la carta 99. Descarta 74, 82, 85, 86 y 87. En la mesa solo queda la 99. ¡Fin!"),
]
PASOS = []
for _p in _T:
    if _p[0] == "combinar":
        PASOS.append(dict(t=_p[3], que=_p[4], acciones=[("combinar", _p[1], _p[2])]))
    elif _p[0] == "app":
        PASOS.append(dict(t=_p[2], que=_p[3], acciones=[("app", _p[1], _p[4])]))
    else:
        PASOS.append(dict(t=_p[2], que=_p[3], acciones=[("leer", _p[1])]))
_amp.recalcular_mesas(PASOS, J)

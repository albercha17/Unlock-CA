"""El Faro de Cabo Niebla — versión de 60 cartas (22 oct 2026), de dificultad media.

Once puzles que no se parecen a los de ningún otro juego de la serie: un reloj que atrasa y una puerta con código, un armario de banderas de señales, una radio
con la frecuencia repartida en tres cartas, una ventana de señales en morse con destellos rojos que no cuentan, el plano de la bahía (islas tipo Nurikabe), la
sombra de cuatro cosas en la pared, la característica de la luz de un almanaque de faros, una barraca con cinco guardianes (lógica), un desván a oscuras
(laberinto con órdenes de avanzar y girar), la lente con sus espejos y un panel de arranque (metapuzle de cifras). Solo 16 cartas tienen a Cristina, Alberto y
Anselmo; el resto son objetos y pistas sin personas. Las cartas-pista las dibuja herramientas/faro.py (instancias_faro.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402
import instancias_faro as I  # noqa: E402

INST = I.INST

ESTILO = ("Ilustración pintada a mano en acuarela y gouache, estilo libro ilustrado de misterio (como un juego de escape room de mesa), texturas de papel, paleta azul petróleo, gris niebla y toques de luz ámbar cálida, iluminación dramática de tormenta nocturna, formato vertical 2:3. "
          "Sin texto, sin letras, sin números, sin marcos ni bordes. Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado, ojos azules. Viste un chubasquero amarillo con capucha, un jersey grueso de lana y botas de agua, y lleva una linterna.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Viste una chaqueta impermeable gris sobre un jersey azul marino de cuello alto y lleva una mochila con una antena de radio asomando.",
    "Anselmo": "Anselmo, hombre de unos 75 años, barba blanca, gorro de lana verde, jersey de punto grueso, mirada amable, siempre con un termo.",
}

HOJA = ("Crea una hoja de personajes (character sheet) con las tres personas descritas, de cuerpo entero y de frente, sobre fondo claro y neutro. Para Cristina y Alberto, mantén su parecido real con la foto adjunta en la cara. "
        + " ".join(PERSONAJES.values()) + " Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real en la cara y que los vista con el chubasquero amarillo y la chaqueta impermeable gris de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo de ilustración pintada en acuarela y gouache, noche de tormenta, tonos azul petróleo y luz ámbar. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): un faro blanco con una banda roja sobre un acantilado, la gran lámpara apagada, olas enormes y rayos; a lo lejos, las luces de un carguero. "
         "Escena 2 (4-8 s): Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules, chubasquero amarillo) y Alberto (hombre de 27 años, moreno con barba, chaqueta gris con una mochila con antena) corren hacia la puerta del faro con una linterna. "
         "Escena 3 (8-12 s): dentro, un recibidor circular a oscuras con un reloj parado y banderas colgadas; la linterna ilumina un cuaderno de cuero. "
         "Escena 4 (12-15 s): lo alto del faro, la lente apagada y, a lo lejos, el carguero acercándose a unas rocas; fundido a negro. "
         "Sonido: tormenta, olas, viento, un trueno y una radio con estática, sin voz de narrador.")

SIN_GENTE = "Sin ninguna persona en la imagen. "

MOSAICOS = {
    "banderas": dict(filas=2, cols=1, cartas=["19", "21"], titulo="La tabla de banderas"),
    "morse": dict(filas=2, cols=1, cartas=["42", "49"], titulo="La tabla morse"),
    "bahia": dict(filas=2, cols=1, cartas=["54", "55"], titulo="El plano de la bahía"),
    "almanaque": dict(filas=2, cols=1, cartas=["61", "63"], titulo="El almanaque de faros"),
    "desvan": dict(filas=2, cols=1, cartas=["70", "71"], titulo="El plano del desván"),
}
POS = {(2, 1): ["mitad de arriba", "mitad de abajo"], (1, 2): ["mitad izquierda", "mitad derecha"]}

_LET = "ABCDEFGH"
_PU, _BA, _RA, _MO, _BH, _SO, _DE, _GU, _LB, _ES, _ME = (INST[k] for k in ("puerta", "banderas", "radio", "morse", "bahia", "sombras", "destellos", "guardianes", "laberinto", "espejos", "meta"))
_S_BAH = ", ".join(_LET[f] + str(c + 1) for f, c in _BH["tierra"])
_S_SOM = ", ".join(_SO["solucion"])
_S_LUZ = ", ".join(str(i + 1) for i, v in enumerate(_DE["solucion"]) if v)
_S_GUA = "; ".join(f"litera {i + 1}: {n} ({g})" for i, (n, g) in enumerate(_GU["solucion"]))
_NOM = {"A": "avanzar", "I": "girar a la izquierda", "D": "girar a la derecha"}
_S_LAB = ", ".join(_NOM[c] for c in _LB["solucion"])
_S_ESP = ", ".join(_LET[int(k.split(",")[0])] + str(int(k.split(",")[1]) + 1) for k in _ES["giran"])
_S_PAN = " ".join(_ME["codigo"])
_S_CIF = ", ".join(f"{a}: {_ME['cifras'][a]}" for a in _ME["orden"])


def codigo(que):
    return f"Carta dibujada por código (herramientas/faro.py; no se pide a ChatGPT): {que}."


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


J = {
    # ------------------------------------------------------------------ El recibidor
    "P": escena("P", "Llegada al faro", [10, 12], [],
                "Noche de tormenta. Cristina y Alberto llegan al faro de Cabo Niebla. La gran lámpara está apagada y la sirena, muda. Por radio, la guardia costera avisa: el carguero «Estrella del Norte» navega a ciegas y llegará a las rocas en una hora. Anselmo, el viejo guardián y abuelo de Cristina, no responde. En el porche hay una lámpara de aceite de latón, vacía (carta 12).",
                ["Entrad en el faro."],
                "El faro de Cabo Niebla, torre blanca con una banda roja, sobre un acantilado en plena tormenta nocturna; la gran lámpara de la cima está apagada. En primer plano y de espaldas, Cristina y Alberto caminan hacia la puerta del faro con una linterna. En el mar, muy lejos, las luces de un carguero."),
    "10": escena("10", "El recibidor del faro", [14, 16, 18, 19, 20, 21, 22], ["P"],
                 "Recibidor circular y oscuro, iluminado solo con vuestras linternas. Al fondo, la puerta de la escalera, con un teclado numérico (carta 14); a su lado, el reloj de pared, parado, con una etiqueta (carta 16). De la pared cuelga un mensaje de banderas (carta 18) y en un rincón hay un armario de banderas con su cerradura (carta 20) y la tabla del código, en dos hojas: juntad la 19 arriba y la 21 abajo. En el suelo, una manivela de generador (carta 22).",
                 ["Hay dos puzles: la puerta de la escalera y el armario de banderas.", "La tabla de banderas son dos cartas: juntadlas, una encima de otra."],
                 "Interior del recibidor circular de un faro, a oscuras e iluminado solo por linternas: una puerta de madera con un panel metálico de teclado numérico al fondo, un reloj de pared grande parado, un mensaje de banderas de señales colgado de una pared, un armario de madera con banderas y una manivela de hierro en el suelo. Cristina señala el reloj con la boca abierta de asombro, y Alberto, con el ceño fruncido de concentración, examina las banderas."),
    "12": combinable("12", "Lámpara de aceite vacía", "azul", 62, 74,
                     "Una lámpara de aceite de latón con el depósito vacío: sin aceite no alumbrará.",
                     SIN_GENTE + "Una lámpara de aceite de latón, con el depósito de cristal vacío y la mecha seca, sobre un banco de madera junto a una ventana por la que se ve la tormenta."),
    "14": app("14", "La puerta de la escalera", "Es un juego de la app: una puerta con un teclado de cuatro cifras. El código es la hora real a la que se paró el reloj del recibidor, que atrasa.", 24,
              ["El reloj está en la carta 16.", "El reloj no marca la hora real: atrasa. Si lo pusieron en hora a las 12:00 y atrasa 20 minutos cada hora, por cada 40 minutos que marca pasan 60 de verdad.",
               f"Marca 3:20 y empezó a las 12:00: son 200 minutos de reloj y 300 reales, es decir, 5 horas. El código es {_PU['codigo']}."],
              SIN_GENTE + "Una puerta de madera oscura con un panel metálico de teclado numérico junto al marco, al fondo de un recibidor circular de un faro, con la luz de una linterna."),
    "16": gris("16", "El reloj del recibidor", "El reloj de pared del recibidor, parado, y una etiqueta del relojero pegada debajo.", ["Es el reloj de la carta 14.", "La etiqueta dice cómo atrasa y desde cuándo.", "Cuando marca la 1:00 son las 1:30."]),
    "18": gris("18", "El mensaje del armario", "Seis banderas de señales colgadas de una cuerda, que forman un mensaje.", ["Es el mensaje del armario de banderas (carta 20).", "Cada bandera es una letra; se leen de izquierda a derecha.", "La tabla del código está en las cartas 19 y 21."]),
    "19": pieza("19", "banderas", "Media lámina de la tabla de banderas.", ["Es la mitad de una lámina: juntadla con la carta 21.", "Son las letras de la A a la M.", "El mensaje está en la carta 18."]),
    "21": pieza("21", "banderas", "Media lámina de la tabla de banderas.", ["Es la mitad de una lámina: juntadla con la carta 19.", "Son las letras de la N a la Z.", "El mensaje está en la carta 18."]),
    "20": app("20", "El armario de banderas", "Es un juego de la app: un armario de banderas con una cerradura de letras. Hay que escribir la palabra que deletrean las banderas del mensaje.", 28,
              ["El mensaje está en la carta 18 y la tabla de banderas, en las cartas 19 y 21.", "Hay banderas casi gemelas: fijaos en el dibujo y en cada color.", f"La palabra es {_BA['palabra']}."],
              SIN_GENTE + "Un armario de madera con las puertas entreabiertas, lleno de banderas de señales de colores dobladas en estantes, en un rincón del recibidor de un faro."),
    "22": combinable("22", "Manivela del generador", "azul", 35, 57, "Una manivela de hierro de las de arrancar un generador diésel, con el mango desgastado.",
                     SIN_GENTE + "Una manivela de hierro con el mango de madera desgastado, apoyada en el suelo de piedra de un recibidor, con un charco de agua de lluvia cerca."),
    "24": escena("24", "La escalera de caracol", [26], [14, 16],
                 "La cerradura cede y la puerta se abre. Subís por una escalera de caracol de hierro, vuelta a vuelta, hasta un rellano con una ventana al mar y una puerta de máquinas. Clavada en la pared con una chincheta hay una nota de Anselmo sobre cómo leer las luces de los faros (carta 26).",
                 ["Mirad la nota del rellano."],
                 "Escalera de caracol de hierro forjado vista desde abajo, con un rellano que tiene una ventana redonda con vista al mar tormentoso, una puerta de hierro y una nota clavada en la pared con una chincheta. Cristina, con la linterna en alto, mira hacia arriba con cara de admiración y Alberto, un peldaño más abajo, resopla con las manos en las rodillas, cansado."),
    "26": gris("26", "La nota de Anselmo", "Una nota de Anselmo sobre cómo se leen las luces de los faros, con un ejemplo dibujado.", ["Es la nota de la característica de la luz (carta 51).", "Explica lo que son un destello, un grupo y el ciclo.", "El almanaque está en las cartas 61 y 63."]),
    "28": escena("28", "Detrás de las banderas", [35], [18, 19, 20, 21],
                 "Con la palabra puesta, el armario se abre y, detrás de las banderas, hay un hueco con una correa de cuero para el generador, de las que mueven una polea (carta 35).",
                 ["Mirad en el hueco del armario."],
                 "El hueco oscuro detrás de un armario de banderas abierto, con una correa de cuero enrollada y una hebilla de latón, visto de cerca. Cristina, con los ojos muy abiertos y una sonrisa de sorpresa, saca la correa con las dos manos; Alberto, con los puños en alto, celebra el hallazgo en silencio."),
    "35": combinable("35", "Correa de transmisión", "roja", 22, 57, "Una correa de cuero de las que mueven la polea de un generador, con la hebilla suelta.",
                     SIN_GENTE + "Una correa de cuero enrollada, con una hebilla de latón, sobre el suelo de piedra de un recibidor, con una linterna al lado."),
    "57": escena("57", "El generador arranca", [31, 32], [22, 35, 10, 28],
                 "Subís hasta la sala de máquinas. Con la correa puesta y la manivela en su sitio, el viejo generador diésel tose, escupe humo y arranca con un trueno: las bombillas parpadean. A un lado, la mesa de la radio (carta 31); al otro, la ventana redonda de señales (carta 32).",
                 ["Dos sitios: la mesa de la radio y la ventana de señales."],
                 "Sala de máquinas de un faro: un generador diésel antiguo arrancando entre humo, tuberías, cuadros de válvulas y bombillas que se encienden, con una radio de onda corta en una mesa y una ventana redonda al fondo. Cristina da vueltas a la manivela con cara de esfuerzo y los dientes apretados, y Alberto, con los brazos en jarras y una gran sonrisa, mira el generador funcionar."),
    # ------------------------------------------------------------------ Rama 1: la radio
    "31": escena("31", "La mesa de la radio", [40, 41, 43, 45], [],
                 "Sobre la mesa hay una radio de onda corta (carta 40), una carta náutica del canal con boyas rojas y verdes (carta 41), una brújula rota (carta 43) y unos versos que el radioaficionado que vendió la radio a Anselmo pegó en la tapa (carta 45).",
                 ["Un único puzle: la radio."],
                 "Una mesa de madera en la sala de máquinas de un faro, con una radio de onda corta antigua encendida con una luz verde en su escala, una carta náutica desplegada, una brújula de latón y un papel con versos pegado en la tapa. Alberto se inclina sobre la radio con el micrófono en la mano y cara de concentración, y Cristina, con el chubasquero empapado, señala la carta con gesto de urgencia."),
    "40": app("40", "La radio de onda corta", "Es un juego de la app: una radio con una rueda grande de sintonía y otra pequeña de ajuste fino. Hay que encontrar la emisora de Cabo Niebla.", 30,
              ["La frecuencia sale de tres cartas: el mapa (carta 41), la brújula (carta 43) y los versos (carta 45).", "Ochenta más la suma de las boyas rojas da la parte entera; la décima sale de la brújula, contando hacia atrás dos vientos desde donde marca la aguja.",
               f"80 + {' + '.join(str(x) for x in _RA['rojas'])} = {80 + sum(_RA['rojas'])}, y la décima es {_RA['verdadero']}: la frecuencia es {str(_RA['objetivo']).replace('.', ',')} MHz."],
              SIN_GENTE + "Una radio de onda corta antigua de madera, con una escala de frecuencias iluminada de ámbar, dos ruedas de sintonía de latón y un micrófono, sobre una mesa de un faro."),
    "41": gris("41", "La carta náutica", "Una carta náutica del canal de Cabo Niebla, con islotes y boyas rojas y verdes numeradas.", ["Es la carta del canal; las boyas llevan números.", "Hay boyas rojas y verdes.", "Los versos de la carta 45 dicen cuáles cuentan."]),
    "43": gris("43", "La brújula rota", "La brújula rota de la mesa de la radio, con los ocho vientos y un número de 0 a 7 junto a cada uno.", ["Cada viento lleva un número.", "La aguja no marca el viento verdadero.", "Los versos de la carta 45 dicen cuánto se pasó."]),
    "45": gris("45", "Los versos del radioaficionado", "Versos pegados en la tapa de la radio, escritos por el radioaficionado.", ["Explican cómo sacar la frecuencia.", "Hablan de ochenta, de las boyas rojas y de la brújula.", "Dos vientos hacia atrás."]),
    "30": escena("30", "La guardia costera", [38], [31, 40, 41, 43, 45],
                 "La radio cruje y responde la guardia costera: «Aquí Cabo Niebla Radio. El Estrella del Norte está a cuarenta minutos de Los Dientes. El abuelo Anselmo dejaba la llave de la sala de la lente partida en dos. Una mitad está dentro de la caja de la radio». En el fondo de la caja, media llave de bronce (carta 38).",
                 ["Mirad dentro de la caja de la radio."],
                 "La radio de onda corta de un faro con la tapa levantada y, en el fondo de su caja, media llave de bronce. Alberto, con el micrófono en la mano y los ojos muy abiertos de emoción, escucha la respuesta de la guardia costera, mientras Cristina, con una sonrisa de alivio, saca la media llave con dos dedos."),
    "38": combinable("38", "Mitad de la llave de bronce", "roja", 56, 94, "Una mitad de una llave de bronce, con las guardas talladas.",
                     SIN_GENTE + "La mitad de una llave de bronce con las guardas talladas, sobre el fondo de una caja de madera de una radio, con una luz ámbar."),
    # ------------------------------------------------------------------ Rama 2: la ventana de señales
    "32": escena("32", "La ventana de señales", [42, 48, 49, 53], [],
                 "La ventana redonda da al mar tormentoso, y en el alféizar hay una lámpara de señales con un teclado (carta 48). Pegados en el marco, la tabla morse de Anselmo, en dos hojas (juntad la 42 arriba y la 49 abajo), y un aviso (carta 53).",
                 ["Un único puzle: la ventana de señales.", "La tabla morse son dos cartas: juntadlas, una encima de otra."],
                 "Una ventana redonda de un faro con vista al mar tormentoso, una lámpara de señales con teclado en el alféizar y un aviso pegado en el marco. Se ve a lo lejos un carguero que parpadea con luces blancas y rojas. Cristina entrecierra los ojos para leer los destellos con una mano sobre la frente, y Alberto, con un lápiz tras la oreja y un papel en la mano, anota con cara de duda."),
    "48": app("48", "La ventana de señales", "Es un juego de la app: el carguero transmite una palabra en morse con una lámpara que parpadea. Hay que escribir la palabra.", 36,
              ["La tabla morse está en las cartas 42 y 49 y el aviso de la sirena, en la 53.", "Los destellos rojos no son letras: no los apuntéis. Entre una letra y otra hay una pausa larga.",
               f"Sin los destellos rojos, la palabra es {_MO['palabra']}."],
              SIN_GENTE + "Una ventana redonda de un faro con una lámpara de señales en el alféizar, que lanza un destello blanco hacia el mar tormentoso, y un destello rojo más abajo."),
    "42": pieza("42", "morse", "Media lámina de la tabla morse.", ["Es la mitad de una lámina: juntadla con la carta 49.", "Son las letras de la A a la M.", "El aviso de la sirena está en la carta 53."]),
    "49": pieza("49", "morse", "Media lámina de la tabla morse.", ["Es la mitad de una lámina: juntadla con la carta 42.", "Son las letras de la N a la Z.", "El aviso de la sirena está en la carta 53."]),
    "53": gris("53", "El aviso de la sirena", "Un aviso en verso pegado en la ventana, sobre la sirena averiada del carguero.", ["Es el aviso de la ventana de señales (carta 48).", "Habla de lo rojo y de lo blanco.", "Solo lo blanco habla."]),
    "36": escena("36", "El carguero contesta", [52, 54, 55, 59], [32, 42, 48, 49, 53],
                 "El carguero contesta con la lámpara: ha perdido el radar y no sabe por dónde pasa el canal entre los islotes de la bahía. Anselmo dibujó la bahía en dos hojas (juntad la 54 arriba y la 55 abajo) y dejó unos versos para trazar el canal (carta 59). En el panel de la radio se marca el plano y se transmite (carta 52).",
                 ["Un único puzle: el plano de la bahía.", "El plano son dos cartas: juntadlas, una encima de otra."],
                 "La sala de máquinas de un faro con un panel de radio con un mapa de islotes dibujado a lápiz sobre una mesa, y por la ventana, a lo lejos, las luces de un carguero. Alberto sostiene el micrófono con cara de preocupación y los labios apretados y Cristina, con el chubasquero amarillo empapado, señala las hojas con una gran ceja levantada de determinación."),
    "52": app("52", "El plano de la bahía", "Es un juego de la app: una rejilla de 7 × 7 casillas de mar. Hay que marcar los islotes de la bahía para que el carguero encuentre el canal.", 44,
              ["El plano está en las cartas 54 y 55 y las reglas, en los versos de la carta 59.", "Cada número es un islote de ese tamaño; dos islotes no se tocan por un lado; el mar va todo unido y sin charcos de 2 × 2.",
               f"Los islotes ocupan las casillas {_S_BAH}."],
              SIN_GENTE + "Una mesa con un mapa de islotes dibujado a lápiz de una bahía, un micrófono de radio antiguo y una luz verde, bajo la lámpara de un faro."),
    "54": pieza("54", "bahia", "Media lámina del plano de la bahía.", ["Es la mitad de una lámina: juntadla con la carta 55.", "Son las filas de la A a la D.", "Los versos están en la carta 59."]),
    "55": pieza("55", "bahia", "Media lámina del plano de la bahía.", ["Es la mitad de una lámina: juntadla con la carta 54.", "Son las filas de la E a la G.", "Los versos están en la carta 59."]),
    "59": gris("59", "Los versos de Anselmo", "Versos de Anselmo con las reglas para trazar el canal de la bahía.", ["Son las reglas del plano de la bahía (carta 52).", "Hablan de islotes, de mar y de charcos.", "El plano está en las cartas 54 y 55."]),
    # ------------------------------------------------------------------ El cuarto de guardia
    "44": escena("44", "El cuarto de guardia", [33, 37, 39, 46, 51, 61, 63], [36, 52, 54, 55, 59],
                 "El capitán da las gracias por el canal, pero necesita ver la luz del faro. Subís al cuarto de guardia. Sobre la mesa, una lámpara de aceite ante una pared pintada (carta 46), con la sombra de la pared (carta 37), el estante del farero (carta 39) y una nota (carta 33). Colgado de un clavo, el temporizador de la lente (carta 51), con el almanaque de faros en dos hojas: juntad la 61 arriba y la 63 abajo.",
                 ["Hay dos puzles: las sombras de la pared y el temporizador de la lente.", "El almanaque son dos cartas: juntadlas, una encima de otra."],
                 "El cuarto de guardia de un faro: una mesa de madera con una lámpara de aceite delante de una pared con una sombra pintada, un estante con objetos de marino (un farol, un ancla, una botella, una tetera, un catalejo) y un temporizador de latón colgado de un clavo. Cristina, con una mano en la barbilla y la ceja arqueada de duda, mira la pared, y Alberto, de puntillas y con una sonrisa traviesa, descuelga el temporizador."),
    "46": app("46", "La lámpara de la mesa", "Es un juego de la app: poner en fila, delante de la lámpara, cuatro cosas del estante de Anselmo para que su sombra sea la pintada en la pared.", 56,
              ["La sombra de la pared está en la carta 37, el estante en la 39 y la nota de Anselmo, en la 33.", "Cada cosa proyecta su sombra en su hueco, de izquierda a derecha, sin pisar el de al lado. Ninguna se repite.",
               f"De izquierda a derecha: {_S_SOM}."],
              SIN_GENTE + "Una mesa de madera con una lámpara de aceite encendida delante de una pared de piedra, con cuatro huecos para colocar objetos de marino y una pared que proyecta sombras alargadas."),
    "37": gris("37", "La sombra de la pared", "La sombra pintada en la pared del cuarto de guardia: cuatro formas en fila.", ["Es la sombra que hay que conseguir (carta 46).", "Son cuatro siluetas, una por hueco.", "El estante está en la carta 39 y la nota, en la 33."]),
    "39": gris("39", "El estante del farero", "El estante del farero, con ocho cosas numeradas.", ["Son los objetos que se pueden poner (carta 46).", "Hay ocho y solo se usan cuatro.", "La sombra de la pared está en la carta 37."]),
    "33": gris("33", "La nota de Anselmo", "Una nota de Anselmo sobre cómo pintó la sombra de la pared.", ["Explica cómo se colocan las cosas (carta 46).", "Hablan de la lámpara, de la mesa y de una fila.", "Ninguna se repite."]),
    "56": combinable("56", "Otra mitad de la llave de bronce", "roja", 38, 94, "La otra mitad de la llave de bronce, que estaba escondida en el cajoncito de la mesa.",
                     SIN_GENTE + "La otra mitad de una llave de bronce con la anilla, sobre el fondo de madera de un cajón de una mesa, con luz ámbar."),
    "51": app("51", "El temporizador de la lente", "Es un juego de la app: un temporizador con casillas, una por segundo del ciclo. Hay que programar la característica de la luz de Cabo Niebla.", 58,
              ["La nota está en la carta 26 y el almanaque, en las cartas 61 y 63.", "Cabo Niebla en el almanaque lleva una abreviatura: grupos de destellos y duración del ciclo. El ciclo empieza con la luz encendida.",
               f"Cabo Niebla es {_DE['faros']['Cabo Niebla']['notacion']}: la luz está encendida en los segundos {_S_LUZ}."],
              SIN_GENTE + "Un temporizador de latón con una rueda dentada y una tira de pequeñas bombillas, colgado de un clavo en la pared de un cuarto de un faro, con luz de linterna."),
    "61": pieza("61", "almanaque", "Media lámina del almanaque de faros.", ["Es la mitad de una lámina: juntadla con la carta 63.", "Cada faro lleva su característica abreviada.", "La nota de Anselmo está en la carta 26."]),
    "63": pieza("63", "almanaque", "Media lámina del almanaque de faros.", ["Es la mitad de una lámina: juntadla con la carta 61.", "Cada faro lleva su característica abreviada.", "La nota de Anselmo está en la carta 26."]),
    # ------------------------------------------------------------------ El desván
    "58": escena("58", "El desván", [69, 70, 71], [51, 61, 63, 26, 24],
                 "El temporizador queda programado y, arriba, se oye un crujido: una trampilla del techo se abre y cae una escalera hacia el desván. Está lleno de cajas apiladas, a oscuras, y solo se ve lo que alumbra la linterna. Anselmo dibujó un plano en dos hojas: juntad la 70 arriba y la 71 abajo (carta 69).",
                 ["Un único puzle: el desván a oscuras.", "El plano son dos cartas: juntadlas, una encima de otra."],
                 "Un desván oscuro de un faro, lleno de cajas y baúles apilados que forman pasillos estrechos, iluminado solo por el haz de una linterna que se pierde entre las cajas. Cristina, con la linterna en alto y los ojos entrecerrados por el miedo, avanza con cuidado, y Alberto, tras ella, se agarra a su chubasquero con cara de susto."),
    "69": app("69", "El desván a oscuras", "Es un juego de la app: un laberinto de cajas apiladas en el que solo se ve la linterna. Se avanza, se gira a la izquierda o a la derecha, empezando abajo a la izquierda y mirando al norte.", 80,
              ["El plano está en las cartas 70 y 71.", "Seguid el único camino del plano, de la entrada a la trampilla, y traducidlo a órdenes: avanzar, girar a la izquierda y girar a la derecha.",
               f"Las órdenes, en orden: {_S_LAB}."],
              SIN_GENTE + "Un desván oscuro con cajas y baúles apilados formando pasillos estrechos, iluminado solo por el haz de una linterna que se pierde entre ellos."),
    "70": pieza("70", "desvan", "Media lámina del plano del desván.", ["Es la mitad de una lámina: juntadla con la carta 71.", "Es la mitad de arriba: la trampilla de la lente.", "La entrada está en la otra mitad."]),
    "71": pieza("71", "desvan", "Media lámina del plano del desván.", ["Es la mitad de una lámina: juntadla con la carta 70.", "Es la mitad de abajo: la entrada, a la izquierda.", "La trampilla está en la otra mitad."]),
    "80": escena("80", "La sala de la lente", [72, 75, 79], [58, 69, 70, 71],
                 "La trampilla da a lo más alto del faro: la sala de la lente, con la enorme lente de Fresnel parada y un panel de espejos ajustables (carta 72). Entre las plumas de un nido, un papel de Anselmo (carta 75) y, en una repisa, el cuaderno del óptico (carta 79).",
                 ["Un único puzle: los espejos de la lente."],
                 "Sala de la lente en lo alto de un faro: una enorme lente de Fresnel de cristal, ventanales con una tormenta nocturna detrás y un panel de espejos de bronce ajustables a un lado, con un nido de gaviota en una repisa. Cristina, con las manos en las mejillas, mira la lente con una sonrisa de asombro, y Alberto, con la lengua entre los dientes, toca un espejo con un dedo con cara de duda."),
    "72": app("72", "Los espejos de la lente", "Es un juego de la app: un tablero de espejos que se giran. Hay que llevar el rayo del foco, por orden, a la galería, a la lente y a la lámpara.", 82,
              ["El orden lo dice el papel del nido (carta 75) y cómo desvía un espejo, el cuaderno del óptico (carta 79).", "Una roca para el rayo: solo importan los espejos que toca. El rayo sale del foco hacia la derecha.",
               f"Hay que girar los espejos {_S_ESP}."],
              SIN_GENTE + "Un panel de espejos de bronce ajustables frente a una lente de Fresnel, con un rayo de luz dorada rebotando entre ellos, en lo alto de un faro."),
    "75": gris("75", "El papel del nido", "Un papel de Anselmo escondido entre las plumas de un nido de gaviota, con versos.", ["Es el orden de los puntos de la carta 72.", "Habla de subir, cruzar y bajar.", "Galería, lente y lámpara."]),
    "79": gris("79", "El cuaderno del óptico", "El cuaderno del óptico, con un dibujo de cómo desvía el rayo cada tipo de espejo.", ["Es la explicación de los espejos (carta 72).", "Hay espejos «/» y «\\».", "Una roca detiene el rayo."]),
    "82": escena("82", "La lente gira", [85, 86, 87], [80, 72, 75, 79],
                 "Los espejos quedan alineados y la lente empieza a girar sola, pero sigue a oscuras: falta arrancar la lámpara. En la sala de control hay un panel de arranque con una combinación de cinco cifras (carta 85), un orden de arranque escrito a lápiz (carta 86) y la tabla de las válvulas del generador (carta 87).",
                 ["Un único puzle: el panel de arranque."],
                 "La sala de control de un faro con la lente de Fresnel girando despacio, un panel de latón con cinco ruedas de cifras y palancas, y un papel escrito a lápiz pegado al lado. Alberto, con las manos en el pelo y la boca abierta de sorpresa, mira el panel, y Cristina, con el dedo en el aire y una gran sonrisa de entendimiento, repasa el papel."),
    "85": app("85", "El panel de arranque", "Es un juego de la app: un panel con un teclado en el que hay que introducir la combinación de cinco cifras que arranca la lámpara.", 99,
              ["Cinco puzles dejaron cada uno una cifra: la puerta, las banderas, la radio, la ventana de señales y la bahía.", "El orden está en la carta 86 y cada cifra pasa por una válvula de la carta 87.",
               f"Las cifras en el orden de arranque son {_S_CIF}; la combinación, tras las válvulas, es {_S_PAN}."],
              SIN_GENTE + "Un panel de control de latón con cinco ruedas de cifras, palancas y válvulas, con indicadores ámbar, en la sala de control de un faro."),
    "86": gris("86", "El orden de arranque", "Cinco acertijos escritos a lápiz en la sala de máquinas, numerados del 1 al 5.", ["Es el orden de las cifras (carta 85).", "Cada acertijo es uno de los cinco primeros puzles.", "Las cifras pasan por las válvulas de la carta 87."]),
    "87": gris("87", "Las válvulas", "La tabla de las válvulas: cada cifra de 0 a 9 entra y sale como otra.", ["Es la tabla de las válvulas (carta 85).", "Cada cifra que entra sale como otra.", "La combinación son las cifras que salen."]),
    # ------------------------------------------------------------------ La barraca y el final
    "94": escena("94", "La puerta de la galería", [64, 66, 67], [38, 56, 30, 44, 33, 37, 39, 46],
                 "Las dos mitades de la llave de bronce encajan y abren la puerta de la galería exterior. Bajo la tormenta, un cobertizo, la barraca de los guardianes: cinco literas en fila y cinco gorros colgados. Anselmo dejó en el cuaderno de relevos, en dos hojas (cartas 66 y 67), las pistas de quién duerme dónde (carta 64).",
                 ["Un único puzle: los guardianes."],
                 "La galería exterior de un faro bajo la tormenta, con una puerta de hierro abierta y, al fondo, un cobertizo de madera con cinco literas en fila y cinco gorros de colores colgados, la lluvia cayendo de lado. Alberto, con una llave de bronce en la mano y una gran sonrisa de triunfo, abre la puerta, y Cristina, agarrándose la capucha del chubasquero contra el viento, mira las literas con curiosidad."),
    "64": app("64", "La barraca de los guardianes", "Es un juego de la app: cinco literas en fila, cinco nombres y cinco gorros. Hay que colocar a cada guardián con su gorro.", 62,
              ["Las pistas están en el cuaderno de relevos, en las cartas 66 y 67.", "Empezad por las pistas que fijan a alguien en un sitio o lo ligan a un gorro, y después ordenad al resto.",
               f"La solución: {_S_GUA}."],
              SIN_GENTE + "Una barraca de madera con cinco literas en fila, cada una con un gorro de lana de un color distinto colgado (rojo, azul, verde, amarillo y blanco), con luz de una linterna."),
    "66": gris("66", "El cuaderno de relevos (I)", "La primera hoja del cuaderno de relevos de Anselmo, con las pistas de quién duerme dónde.", ["Es la primera hoja de pistas (carta 64).", "Habla de literas, nombres y gorros.", "La otra hoja está en la carta 67."]),
    "67": gris("67", "El cuaderno de relevos (II)", "La segunda hoja del cuaderno de relevos de Anselmo, con las pistas de quién duerme dónde.", ["Es la segunda hoja de pistas (carta 64).", "Habla de literas, nombres y gorros.", "La otra hoja está en la carta 66."]),
    "62": combinable("62", "Bidón de aceite", "roja", 12, 74, "Un bidón de aceite de lámpara, de los de Anselmo, lleno hasta arriba.",
                     SIN_GENTE + "Un bidón metálico de aceite de lámpara con un tapón de corcho y una etiqueta sin texto, en el suelo de madera de una barraca, con luz de linterna."),
    "74": escena("74", "La lámpara llena", [], [62, 12, 64, 66, 67, 94, 57],
                 "El aceite llena la lámpara hasta el borde y la mecha prende con una chispa. Ya solo falta arrancar el generador con la combinación del panel (carta 85).",
                 ["Ya solo queda el panel de arranque."],
                 "Una lámpara de aceite de latón recién llenada, con la llama de la mecha prendiendo, en lo alto de un faro entre la tormenta. Cristina, con las manos juntas y una sonrisa de alivio, sostiene la lámpara con cuidado, y Alberto, apretando el puño con alegría, le acerca una cerilla."),
    "99": escena("99", "¡La luz del faro! (FIN)", [], [74, 82, 85, 86, 87],
                 "El panel acepta la combinación: el generador ruge, la lámpara prende y el faro enciende su luz, que barre el mar. El «Estrella del Norte» gira justo a tiempo y esquiva Los Dientes. Anselmo aparece por la escalera con su termo: se había quedado dormido en la despensa. «¿Qué han hecho con mi faro?», sonríe. FIN.",
                 [],
                 "El faro enciende su gran luz: un haz dorado barre el mar tormentoso e ilumina un carguero que gira lejos de las rocas. En primer plano, en la galería del faro, Cristina, Alberto y un anciano de barba blanca y gorro de lana con un termo, sonriendo."),
}

META = dict(juego="El Faro de Cabo Niebla", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()})

SPEC = dict(final="99", needs={
    "24": ["14", "16"], "28": ["20", "18", "19", "21"], "57": ["22", "35"], "30": ["40", "41", "43", "45"], "36": ["48", "42", "49", "53"],
    "44": ["52", "54", "55", "59"], "56": ["46", "37", "39", "33"], "58": ["51", "26", "61", "63"], "80": ["69", "70", "71"], "94": ["38", "56"],
    "62": ["64", "66", "67"], "82": ["72", "75", "79"], "74": ["12", "62"], "99": ["85", "86", "87", "74"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_T = [
    ("leer", "P", "Llegada", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12."),
    ("leer", "10", "El recibidor del faro", "Lee la carta 10. Descarta la P y coge 14, 16, 18, 19, 20, 21 y 22. Junta la tabla de banderas: 19 arriba y 21 abajo."),
    ("app", "14", "La puerta de la escalera", f"En el móvil: Acción, 14. El reloj (16) marca 3:20, lo pusieron en hora a las 12:00 y atrasa 20 minutos cada hora: la hora real es las 17:00. Código {_PU['codigo']}. El mensaje te dice que cojas la 24. Apunta la cifra de la puerta: {_ME['cifras']['14']}.", "carta 24"),
    ("leer", "24", "La escalera de caracol", "Lee la carta 24. Descarta 14 y 16 y coge la 26 (guárdala para el temporizador)."),
    ("app", "20", "El armario de banderas", f"En el móvil: Acción, 20. Con el mensaje (18) y la tabla (19 y 21), la palabra es {_BA['palabra']}. El mensaje te dice que cojas la 28. Apunta la cifra de las banderas: {_ME['cifras']['20']}.", "carta 28"),
    ("leer", "28", "Detrás de las banderas", "Lee la carta 28. Descarta 18, 19, 20 y 21 y coge la 35."),
    ("combinar", "22", "35", "El generador", "La manivela (22) y la correa (35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El generador arranca", "Lee la carta 57. Descarta 22, 35, 10 y 28 y coge 31 y 32."),
    ("leer", "31", "La mesa de la radio", "Lee la carta 31. Coge 40, 41, 43 y 45."),
    ("app", "40", "La radio", f"En el móvil: Acción, 40. Con el mapa (41), la brújula (43) y los versos (45): 80 + {' + '.join(str(x) for x in _RA['rojas'])} = {80 + sum(_RA['rojas'])} y la décima {_RA['verdadero']}: {str(_RA['objetivo']).replace('.', ',')} MHz. El mensaje te dice que cojas la 30. Apunta la cifra de la radio: {_ME['cifras']['40']}.", "carta 30"),
    ("leer", "30", "La guardia costera", "Lee la carta 30. Descarta 31, 40, 41, 43 y 45 y coge la 38."),
    ("leer", "32", "La ventana de señales", "Lee la carta 32. Coge 42, 48, 49 y 53. Junta la tabla morse: 42 arriba y 49 abajo."),
    ("app", "48", "La ventana de señales", f"En el móvil: Acción, 48. Con la tabla morse (42 y 49) y el aviso (53), sin contar los destellos rojos, la palabra es {_MO['palabra']}. El mensaje te dice que cojas la 36. Apunta la cifra de la ventana: {_ME['cifras']['48']}.", "carta 36"),
    ("leer", "36", "El carguero contesta", "Lee la carta 36. Descarta 32, 42, 48, 49 y 53 y coge 52, 54, 55 y 59. Junta el plano: 54 arriba y 55 abajo."),
    ("app", "52", "El plano de la bahía", f"En el móvil: Acción, 52. Con el plano (54 y 55) y los versos (59), los islotes ocupan las casillas {_S_BAH}. El mensaje te dice que cojas la 44. Apunta la cifra de la bahía: {_ME['cifras']['52']}.", "carta 44"),
    ("leer", "44", "El cuarto de guardia", "Lee la carta 44. Descarta 36, 52, 54, 55 y 59 y coge 33, 37, 39, 46, 51, 61 y 63. Junta el almanaque: 61 arriba y 63 abajo."),
    ("app", "46", "La lámpara de la mesa", f"En el móvil: Acción, 46. Con la sombra (37), el estante (39) y la nota (33), de izquierda a derecha: {_S_SOM}. El mensaje te dice que cojas la 56.", "carta 56"),
    ("app", "51", "El temporizador de la lente", f"En el móvil: Acción, 51. Con la nota (26) y el almanaque (61 y 63), Cabo Niebla es {_DE['faros']['Cabo Niebla']['notacion']}: luz encendida en los segundos {_S_LUZ}. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "El desván", "Lee la carta 58. Descarta 51, 61, 63, 26 y 24 y coge 69, 70 y 71. Junta el plano: 70 arriba y 71 abajo."),
    ("app", "69", "El desván a oscuras", f"En el móvil: Acción, 69. Con el plano (70 y 71), las órdenes son: {_S_LAB}. El mensaje te dice que cojas la 80.", "carta 80"),
    ("leer", "80", "La sala de la lente", "Lee la carta 80. Descarta 58, 69, 70 y 71 y coge 72, 75 y 79."),
    ("app", "72", "Los espejos de la lente", f"En el móvil: Acción, 72. Con el papel del nido (75) y el cuaderno del óptico (79), hay que girar los espejos {_S_ESP}. El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "La lente gira", "Lee la carta 82. Descarta 80, 72, 75 y 79 y coge 85, 86 y 87."),
    ("combinar", "38", "56", "La llave de bronce", "Las dos mitades de la llave (38 y 56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "La puerta de la galería", "Lee la carta 94. Descarta 38, 56, 30, 44, 33, 37, 39 y 46 y coge 64, 66 y 67."),
    ("app", "64", "La barraca de los guardianes", f"En el móvil: Acción, 64. Con el cuaderno de relevos (66 y 67): {_S_GUA}. El mensaje te dice que cojas la 62.", "carta 62"),
    ("combinar", "12", "62", "La lámpara", "La lámpara vacía (12) y el bidón (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "La lámpara llena", "Lee la carta 74. Descarta 62, 12, 64, 66, 67, 94 y 57."),
    ("app", "85", "El panel de arranque", f"En el móvil: Acción, 85. Con el orden (86) y las válvulas (87): las cifras en orden de arranque son {_S_CIF} y la combinación es {_S_PAN}. El mensaje te dice que cojas la 99.", "carta 99"),
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
_amp.separar_mosaicos(J, PASOS)
_amp.recalcular_mesas(PASOS, J)

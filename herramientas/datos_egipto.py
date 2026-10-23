"""Egipto, 1274 a.C.: El Ojo de Horus — versión de 60 cartas (21 oct 2026), mucho más difícil y variada.

Once puzles de tipos que no salen en ningún otro juego de la serie, con las pistas dibujadas o en acertijo (ninguna carta explica cómo se
resuelve su puzle): la falsa posición del papiro Rhind (el montón del granero), una pirámide de sumas, el nilómetro (una secuencia en codos
y palmos), el conteo de animales de un friso según hacia dónde miran, las partes del Ojo de Horus como medida, un criptograma de
jeroglíficos, las cámaras del templo (colorear un mapa), los canales de riego (árbol de expansión mínimo), un friso de azulejos con tres
reglas, el reparto de tierras (Shikaku) y la consola final con los sellos de todos los puzles.
Solo 15 cartas tienen a Cristina y Alberto (escenas); el resto son objetos y pistas sin personas.
Las cartas-pista las dibuja herramientas/egipto.py (instancias_egipto.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402
import instancias_egipto as I  # noqa: E402

ESTILO = ("Ilustración digital pintada con estética de película de aventuras, luz cálida de antorchas y rayos de sol dorados, "
          "paleta de ocres, turquesa y azul lapislázuli, formato vertical 2:3. Sin texto, letras ni números en la imagen; "
          "los jeroglíficos solo como decoración sin significado legible. Deja libre de detalles importantes la esquina "
          "superior izquierda y el 18 % inferior de la imagen.")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado, ojos azules. Lleva ropa actual y cómoda (vaqueros, zapatillas, camiseta y una chaqueta ligera).",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Lleva ropa actual (vaqueros, zapatillas, sudadera con capucha y una mochila)."
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado, ojos azules, vaqueros, zapatillas, camiseta y chaqueta ligera. "
        "Alberto: hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones, vaqueros, zapatillas, sudadera con capucha y mochila. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con animación de estilo ilustración pintada de película de aventuras, luz cálida y colores dorados y turquesa. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Alberto gira un dial con una sonrisa nerviosa. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul, el salón se deforma y los dos son absorbidos por un túnel de luz con destellos dorados. "
         "Escena 3 (8-12 s): caen sobre un suelo de piedra en una cámara oscura bajo un templo del antiguo Egipto, con jeroglíficos en las paredes y rayos de luz por una rendija; el aparato humea y se apaga. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, asombrados, mirando alrededor; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe sordo al aterrizar, eco de piedra y música de aventura con tambores suaves, sin voz de narrador.")

ESTILO += " Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes)."
SIN_GENTE = "Sin ninguna persona en la imagen. "

MOSAICOS = {
    "piramide": dict(filas=2, cols=1, cartas=["19", "21"], titulo="La pirámide del escriba"),
    "friso": dict(filas=1, cols=2, cartas=["42", "49"], titulo="El friso de los animales"),
    "camaras": dict(filas=1, cols=2, cartas=["61", "63"], titulo="El plano del templo"),
    "azulejos": dict(filas=2, cols=1, cartas=["66", "67"], titulo="El friso de azulejos"),
    "tierras": dict(filas=1, cols=2, cartas=["75", "79"], titulo="El campo por repartir"),
}
POS = {(2, 1): ["mitad de arriba", "mitad de abajo"], (1, 2): ["mitad izquierda", "mitad derecha"]}
_NOMCOL = ["ocre", "turquesa", "lapislázuli"]
_S_HEQAT = ", ".join(f"{I.PARTES[i][0]}/{I.PARTES[i][1]}" for i in I.HEQAT["solucion"])
_S_PIRA = ", ".join(str(x) for x in I.PIRAMIDE["solucion"])
_S_NILO = f"{I.NILOMETRO['solucion'][0]} codos y {I.NILOMETRO['solucion'][1]} palmos"
_S_FRISO = ", ".join(str(x) for x in I.CONTAR["solucion"])
_NOMSIG = {"sol": "el sol", "loto": "el loto", "agua": "el agua", "pluma": "la pluma", "corona": "la corona", "cetro": "el cetro"}
_S_CRIPTO = "; ".join(f"{_NOMSIG[I.CRIPTO['signos'][l]]} = {v}" for l, v in I.CRIPTO["solucion"].items())
_S_CAM = ", ".join(f"{'ABCDEFGHIJKL'[i]} {_NOMCOL[c]}" for i, c in enumerate(I.CAMARAS["solucion"]))
_S_CAN = ", ".join(f"{a}–{b}" for a, b in I.CANALES["solucion"])
_S_AZU = f"el azulejo n.º {I.FRISO['solucion'] + 1} de los seis"
_S_TIE = "; ".join(f"{w}×{h}" for _, _, w, h in I.TIERRAS["solucion"])
_NOMSEL = {"14": "el pan", "20": "la tierra", "40": "el agua", "48": "el ibis", "52": "el ojo", "46": "la pluma", "51": "el loto", "69": "el cetro",
           "64": "el escarabajo", "72": "la corona"}
_S_SEL = ", ".join(_NOMSEL[c] for c in I.ORDEN_SELLOS)


def codigo(que):
    return f"Carta dibujada por código (herramientas/egipto.py; no se pide a ChatGPT): {que}."


def pieza(carta, mosaico, que, pistas):
    m = MOSAICOS[mosaico]
    i = m["cartas"].index(carta)
    pos = POS[(m["filas"], m["cols"])][i]
    return dict(titulo=f"Carta {carta} — {m['titulo']} ({pos})", tipo="gris",
                mosaico=dict(id=mosaico, filas=m["filas"], cols=m["cols"], fila=i // m["cols"], col=i % m["cols"]),
                descripcion=[que], pistas=pistas, arte=codigo(f"{pos} de «{m['titulo']}»"))


def gris(carta, titulo, que, pistas, arte):
    return dict(titulo=f"Carta {carta} — {titulo}", tipo="gris", descripcion=[que], pistas=pistas, arte=arte)


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
    # ------------------------------------------------------------------ La cámara oculta
    "P": escena("P", "Llegada al templo", [10, 12], [],
                "Primer salto de vuestro Cronoportal: Tebas, el año 1274 a.C. Aterrizáis en una cámara secreta bajo un templo, con jeroglíficos en las paredes y un rayo de luz por una rendija. El aparato golpea el suelo y se apaga: su energía se ha agotado. Solo hay un sitio donde encontrar una fuente de poder tan antigua como esta ciudad: el Ojo de Horus, escondido en este mismo templo. Tenéis hora y media antes de que lleguen los sacerdotes.",
                ["Mirad a vuestro alrededor y revisad el aparato."],
                "Una cámara secreta de piedra bajo un templo del antiguo Egipto, con jeroglíficos decorativos en las paredes y un rayo de luz dorada entrando por una rendija. En el suelo, un aparato de latón y cristal retrofuturista (el Cronoportal) humea y se apaga. Cristina y Alberto, con ropa actual (vaqueros, camiseta, chaqueta ligera, sudadera y mochila), se levantan del suelo desconcertados: ella con los ojos muy abiertos y la boca entreabierta, él con una ceja arqueada y una media sonrisa de incredulidad."),
    "10": escena("10", "La cámara oculta", [14, 16, 18, 19, 20, 21, 22], ["P"],
                 "La cámara tiene dos salidas cerradas. Una puerta de bronce guarda un granero y lleva grabado un acertijo de sacos. La otra es un muro de bloques con una pirámide escrita encima, como si un cantero hubiera dejado un recado a medias: dos láminas de piedra con medio recado cada una y un acertijo. Y en el suelo, partido en dos, un medallón.",
                 ["Hay dos puzles: el granero y la pirámide del cantero.", "La pirámide son dos cartas: juntadlas, una encima de otra."],
                 "Una cámara secreta egipcia con una puerta de bronce con un relieve grabado a un lado y, al otro, un muro de bloques de piedra con una pirámide cincelada; en el suelo, medio medallón de oro. Cristina examina el relieve de la puerta con el ceño fruncido de concentración y Alberto toca los bloques del muro con la punta de los dedos, con gesto de duda."),
    "12": combinable("12", "Cronoportal sin energía", "azul", 62, 74,
                     "El Cronoportal con el anillo central apagado y el hueco de su fuente de energía vacío.",
                     SIN_GENTE + "Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo central apagado y un hueco circular vacío en el pecho del aparato, sobre un suelo de piedra con polvo dorado."),
    "14": app("14", "El granero cerrado", "Es un juego de la app: la puerta del granero solo se abre diciendo cuántos sacos hay en el montón.", 24,
              ["El grabado de la puerta está en la carta 16.", "Lo grabado habla de un montón, de su mitad y de su cuarto, y de lo que suman. Probad con montones de números sencillos.", f"Hay {I.MONTON['solucion']} sacos."],
              SIN_GENTE + "Una puerta de bronce de un granero egipcio con un relieve de sacos de cebada grabado."),
    "16": gris("16", "El granero cerrado", "El grabado de la puerta del granero.",
               ["Sirve para el granero (carta 14).", "Un montón, su mitad y su cuarto suman 28 sacos.", f"Hay {I.MONTON['solucion']} sacos."], codigo("el grabado del granero")),
    "18": gris("18", "El acertijo del cantero", "Un acertijo cincelado en el muro.",
               ["Sirve para la pirámide (carta 20).", "Cada piedra lleva la suma de las dos que tiene debajo.", f"Las cinco piedras de la base, de izquierda a derecha: {_S_PIRA}."], codigo("el acertijo del cantero")),
    "19": pieza("19", "piramide", "Media lámina de la pirámide del escriba.", ["Es la mitad de una lámina: juntadla con la carta 21.", "Hay piedras con su peso y piedras vacías.", f"Las cinco piedras de la base: {_S_PIRA}."]),
    "21": pieza("21", "piramide", "Media lámina de la pirámide del escriba.", ["Es la mitad de una lámina: juntadla con la carta 19.", "Hay piedras con su peso y piedras vacías.", f"Las cinco piedras de la base: {_S_PIRA}."]),
    "20": app("20", "La pirámide del escriba", "Es un juego de la app: el muro de bloques solo se abre si se pesa la base de la pirámide dibujada.", 28,
              ["La pirámide, partida en dos láminas, es lo de las cartas 19 y 21; el acertijo, en la carta 18.", "Empezad por una piedra cuyas dos de abajo conozcáis, o a la inversa: restad.", f"Las cinco piedras de la base: {_S_PIRA}."],
              SIN_GENTE + "Un muro de grandes bloques de piedra en una cámara egipcia con una pirámide de bloques cincelada y vacía."),
    "22": combinable("22", "Mitad de medallón", "azul", 35, 57, "Una mitad de un medallón de oro con el sol y un uraeus grabados.",
                     SIN_GENTE + "La mitad de un medallón de oro con un disco solar y una cobra grabados, sobre el suelo de piedra de una cámara egipcia."),
    "24": escena("24", "El granero abierto", [26], [14, 16],
                 "La puerta de bronce se abre con un chirrido y deja ver un granero lleno de cebada. Entre los sacos asoma un papiro enrollado con el sello de una sacerdotisa: Henut, la guardiana de las cámaras del templo, que escondió aquí instrucciones para quien llegara hasta aquí.",
                 ["El papiro de la sacerdotisa servirá más adelante."],
                 "Un granero egipcio abierto, lleno de sacos de cebada y vasijas, con un papiro enrollado entre los sacos. Alberto levanta el papiro con una sonrisa de triunfo y Cristina, a su lado, se tapa la nariz entre toses por el polvo, con los ojos llorosos."),
    "26": gris("26", "El papiro de la sacerdotisa", "Un papiro con el sello de la sacerdotisa Henut.",
               ["Sirve para las cámaras de colores (carta 51).", "Dos cámaras con una puerta entre ellas no pueden llevar la misma pintura.", f"Las doce cámaras: {_S_CAM}."], codigo("el papiro de la sacerdotisa")),
    "28": escena("28", "Tras el muro", [35], [18, 19, 20, 21],
                 "Los bloques se deslizan con un estruendo sordo. Detrás hay una cámara pequeña con un nicho, y en el nicho, la otra mitad del medallón. Los dos pedazos tienen los bordes irregulares y parecen hechos para encajar.",
                 ["Lo que habéis encontrado se puede juntar con algo que ya tenéis."],
                 "Una cámara pequeña de piedra tras un muro de bloques abierto, con un nicho en el que reposa la mitad de un medallón de oro. Alberto saca la mitad del medallón con mucho cuidado, la lengua entre los dientes, y Cristina lo ilumina con la linterna del móvil con gesto de asombro, boquiabierta."),
    "35": combinable("35", "Otra mitad de medallón", "roja", 22, 57, "La otra mitad del medallón, con los rayos de un sol y la cola de una cobra.",
                     SIN_GENTE + "La otra mitad de un medallón de oro con rayos de sol y la cola de una cobra grabados, en un nicho de piedra."),
    "57": escena("57", "El medallón de Tebas", [31, 32], [22, 35, 10, 28],
                 "Las dos mitades encajan con un clic y el medallón se pone a brillar. En la pared se abre un pasadizo con dos puertas: una lleva al río, a la sala donde los sacerdotes miden la crecida del Nilo; la otra, a una larga galería de frisos. «Hay que cruzar las dos —susurra una voz que sale del medallón—. Pero la luz no os ayudará hasta el final».",
                 ["Hay dos caminos: la sala del Nilo y la galería del friso. Podéis seguir los dos."],
                 "Una cámara egipcia con un pasadizo recién abierto con dos puertas; en el centro, un medallón de oro completo que brilla con luz dorada. Cristina sostiene el medallón en alto, deslumbrada, con una sonrisa de maravilla; Alberto mira las dos puertas alternativamente, con las cejas muy altas y la boca en una O."),
    # ------------------------------------------------------------------ Rama 1: el Nilo
    "31": escena("31", "La sala del Nilo", [40, 41, 43, 45], [],
                 "Una sala excavada junto al río. En la pared, una columna con muescas: el nilómetro. Los sacerdotes marcan en ella hasta dónde llega la crecida cada año, y hoy tienen que decidir si abren las compuertas de los canales. En una mesa, los registros de las últimas cinco crecidas y una vara de agrimensor.",
                 ["Los registros son dos cartas."],
                 SIN_GENTE + "Una sala excavada en la roca junto al Nilo, con una columna de piedra con muescas pegada a la pared (un nilómetro), una mesa con rollos y una vara de medir dorada, y al fondo el río visto por una abertura."),
    "40": app("40", "El nilómetro", "Es un juego de la app: los sacerdotes necesitan saber a qué altura llegará la crecida de este año.", 30,
              ["Las crecidas de los cinco años anteriores, dibujadas, están en las cartas 41 y 43; cuánto mide un codo y un palmo, en la 45.", "Pasad cada altura a palmos y mirad cuánto sube una a otra: las subidas también siguen una pauta.", f"La crecida de este año: {_S_NILO}."],
              SIN_GENTE + "Una columna de piedra con muescas, un nilómetro, con agua turbia subiendo en ella, en una sala excavada junto a un río."),
    "41": gris("41", "Registro de crecidas (I)", "Las marcas de las tres primeras crecidas.",
               ["Sirve para el nilómetro (carta 40).", "Contad los palmos de cada una y pasadlo a codos como dice la carta 45.", f"La crecida de este año: {_S_NILO}."], codigo("las crecidas de los años 1 a 3")),
    "43": gris("43", "Registro de crecidas (II)", "Las marcas de la cuarta y la quinta crecida, y un hueco para la de este año.",
               ["Sirve para el nilómetro (carta 40).", "Comparad lo que sube cada año con lo que subió el anterior.", f"La crecida de este año: {_S_NILO}."], codigo("las crecidas de los años 4 y 5")),
    "45": gris("45", "La vara del agrimensor", "Una vara dorada de un codo, partida en palmos.",
               ["Sirve para el nilómetro (carta 40).", "Contad los palmos de la vara: son los que hacen un codo.", f"La crecida de este año: {_S_NILO}."], codigo("la vara del agrimensor")),
    "30": escena("30", "Las compuertas", [38], [31, 40, 41, 43, 45],
                 "Los sacerdotes abren las compuertas justo a tiempo y el agua del Nilo llena los canales sin desbordarse. Agradecido, uno de ellos os entrega una lámpara de aceite de bronce... apagada, claro, y sin una gota de fuego para encenderla.",
                 ["La lámpara necesita llama: buscad algo que arda."],
                 "Una compuerta de piedra abierta junto al Nilo con el agua entrando a raudales en un canal de riego; un sacerdote con túnica blanca entrega una lámpara de bronce a Alberto. Cristina aplaude emocionada, con una gran sonrisa, mientras Alberto coge la lámpara con las dos manos, mirándola con respeto reverencial."),
    "38": combinable("38", "Lámpara apagada", "roja", 56, 94, "Una lámpara de aceite de bronce, con el depósito lleno pero sin llama.",
                     SIN_GENTE + "Una lámpara de aceite de bronce con la mecha seca y sin llama, sobre una mesa de piedra en una sala egipcia."),
    # ------------------------------------------------------------------ Rama 2: el friso
    "32": escena("32", "La galería del friso", [42, 48, 49, 53], [],
                 "Una larga galería con un friso de animales que recorre las dos paredes. Al fondo, un guardián de piedra con cabeza de chacal impide el paso: solo se aparta si se le dice la cuenta que él mismo grabó en su cerradura. El friso está partido en dos láminas que hay que juntar.",
                 ["El friso son dos cartas: juntadlas."],
                 "Una larga galería egipcia con un friso de animales pintado en la pared (ibis, cobras, chacales y halcones) y, al fondo, una estatua de piedra de un guardián con cabeza de chacal. Alberto mira el friso con los ojos entornados, contando con los dedos, y Cristina da un paso atrás ante el guardián con una ceja levantada y gesto de recelo."),
    "48": app("48", "El friso de los animales", "Es un juego de la app: el guardián de piedra solo deja pasar si se le dice cuántos animales de cada clase hay en el friso.", 36,
              ["El friso está en las cartas 42 y 49; la cerradura del guardián, en la carta 53.", "Solo cuentan los que miran hacia el sol naciente, a la derecha. Contad cada animal por separado, y sin olvidar ninguno.", f"Los animales de la cerradura, de izquierda a derecha: {_S_FRISO}."],
              SIN_GENTE + "Una estatua de piedra de un guardián con cabeza de chacal ante una puerta de piedra, con un panel de cuatro huecos en el pecho."),
    "42": pieza("42", "friso", "Media lámina del friso de los animales.", ["Es la mitad de una lámina: juntadla con la carta 49.", "Hay animales que miran a la derecha y otros a la izquierda, y adornos que no cuentan.", f"Los animales de la cerradura, de izquierda a derecha: {_S_FRISO}."]),
    "49": pieza("49", "friso", "Media lámina del friso de los animales.", ["Es la mitad de una lámina: juntadla con la carta 42.", "Hay animales que miran a la derecha y otros a la izquierda, y adornos que no cuentan.", f"Los animales de la cerradura, de izquierda a derecha: {_S_FRISO}."]),
    "53": gris("53", "El guardián del friso", "La cerradura del guardián de piedra: cuatro animales y cuatro huecos.",
               ["Sirve para el friso (carta 48).", "Solo cuentan los que miran hacia el sol naciente.", f"Los animales de la cerradura, de izquierda a derecha: {_S_FRISO}."], codigo("la cerradura del guardián")),
    "36": escena("36", "La casa de las medidas", [52, 54, 55, 59], [32, 42, 48, 49, 53],
                 "El guardián se aparta y entráis en una sala con balanzas, medidas de cebada y un escriba gordo y ceñudo, Ipi, que lleva las cuentas del templo. «Hoy me han cobrado dos pagos, uno por la mañana y otro por la tarde, con las partes del amuleto del Ojo de Horus... y no me cuadra». Solo si el escriba cuadra las cuentas os dejará ver el resto del templo.",
                 ["Los pagos son dos cartas."],
                 "Una sala de un templo egipcio con balanzas de bronce, sacos de cebada y un escriba rechoncho de gesto ceñudo sentado ante un papiro. Cristina le habla con las manos abiertas, en gesto conciliador, y Alberto se asoma al papiro por encima del hombro del escriba, con las cejas fruncidas de concentración."),
    "52": app("52", "La medida del heqat", "Es un juego de la app: el escriba cobra con las seis partes del Ojo de Horus; hay que decir cuáles suman lo cobrado hoy.", 44,
              ["Qué forma es cada parte, en la carta 54; los pagos de la mañana y de la tarde, en las 55 y 59.", "Sumad los dos pagos: algunos sacos se juntan en uno más grande. Cada parte, una vez o ninguna.", f"Las partes: {_S_HEQAT}."],
              SIN_GENTE + "Una balanza de bronce con un amuleto de seis piezas de colores (el Ojo de Horus) y un saco de cebada, en una sala del templo."),
    "54": gris("54", "Las partes del ojo", "Las seis partes del amuleto del Ojo de Horus, cada una con lo que mide.",
               ["Sirve para la medida (carta 52).", "Cada parte vale la mitad de la anterior.", f"Las partes: {_S_HEQAT}."], codigo("las seis partes del ojo")),
    "55": gris("55", "Pago de la mañana", "Los tres sacos que se pagaron por la mañana.",
               ["Sirve para la medida (carta 52).", "Sumad lo que hay en los tres sacos.", f"Las partes: {_S_HEQAT}."], codigo("los pagos de la mañana")),
    "59": gris("59", "Pago de la tarde", "Los tres sacos que se pagaron por la tarde.",
               ["Sirve para la medida (carta 52).", "Sumad lo que hay en los tres sacos y juntadlo con lo de la mañana.", f"Las partes: {_S_HEQAT}."], codigo("los pagos de la tarde")),
    # ------------------------------------------------------------------ La casa del escriba
    "44": escena("44", "La casa del escriba", [33, 37, 39, 46, 51, 61, 63], [36, 52, 54, 55, 59],
                 "Las cuentas cuadran y el escriba os agradece con un resoplido. «Pasad a mi casa. Tengo un cofre que lo cierra una suma de signos que no entiendo ni yo, y la sacerdotisa Henut necesita que alguien pinte las cámaras del templo antes de la fiesta de mañana». Tenéis delante dos encargos.",
                 ["Hay dos puzles: el cofre del escriba y las cámaras del templo. El papiro de la sacerdotisa sirve aquí."],
                 "El interior de la casa de un escriba egipcio, con papiros enrollados por todas partes, un cofre de madera con signos grabados y un plano pintado en la pared. El escriba, rechoncho, les señala el cofre con un dedo regordete, y Cristina mira el plano con la cabeza ladeada y una sonrisa curiosa mientras Alberto se rasca la barba, perplejo."),
    "46": app("46", "El cofre del escriba", "Es un juego de la app: el cofre se cierra con una suma de seis signos, cada uno una cifra distinta.", 56,
              ["La suma está en la carta 37; el escriba anotó dos cosas al margen, en las cartas 39 y 33.", "La suma sola admite tres soluciones: las notas dejan solo una. Los números no empiezan por cero.", f"Las cifras: {_S_CRIPTO}."],
              SIN_GENTE + "Un cofre de madera con la tapa grabada con seis signos jeroglíficos distintos, y seis ruedas de números en el frontal."),
    "37": gris("37", "La suma del escriba", "La suma que cierra el cofre, escrita con signos.",
               ["Sirve para el cofre (carta 46).", "Cada signo es una cifra distinta; todos los números empiezan por una cifra que no es cero.", f"Las cifras: {_S_CRIPTO}."], codigo("la suma de signos")),
    "39": gris("39", "Primera nota", "Una nota del escriba, al margen.",
               ["Sirve para el cofre (carta 46).", "Es una pista sobre un signo.", f"Las cifras: {_S_CRIPTO}."], codigo("la primera nota")),
    "33": gris("33", "Segunda nota", "Otra nota del escriba, al margen.",
               ["Sirve para el cofre (carta 46).", "Es una pista que compara dos signos.", f"Las cifras: {_S_CRIPTO}."], codigo("la segunda nota")),
    "56": combinable("56", "Brasa sagrada", "roja", 38, 94, "Una brasa que nunca se apaga, guardada en el cofre en un cuenco de barro.",
                     SIN_GENTE + "Un cuenco de barro con una brasa naranja que brilla sin apagarse, dentro de un cofre de madera abierto."),
    "51": app("51", "Las cámaras de colores", "Es un juego de la app: pintar las doce cámaras del templo, cada una con una pintura.", 58,
              ["La norma de la sacerdotisa, en la carta 26; el plano del templo, con puertas y cámaras ya pintadas, en las cartas 61 y 63.", "Empezad por una cámara con pocas vecinas y con vecinas ya pintadas: así queda una sola pintura posible.", f"Las doce cámaras: {_S_CAM}."],
              SIN_GENTE + "El plano de un templo egipcio con doce cámaras unidas por puertas, tres tarros de pintura (ocre, turquesa y lapislázuli) y un pincel."),
    "61": pieza("61", "camaras", "Media lámina del plano del templo.", ["Es la mitad de un plano: juntadla con la carta 63.", "Las líneas son puertas; las cámaras llenas ya están pintadas.", f"Las doce cámaras: {_S_CAM}."]),
    "63": pieza("63", "camaras", "Media lámina del plano del templo.", ["Es la mitad de un plano: juntadla con la carta 61.", "Las líneas son puertas; las cámaras llenas ya están pintadas.", f"Las doce cámaras: {_S_CAM}."]),
    "58": escena("58", "El secreto de la sacerdotisa", [69, 70, 71], [51, 61, 63, 26, 24],
                 "Henut aparece, riendo entre los tarros de pintura. «Me habéis ahorrado una semana. Os diré lo que no debo: el Ojo de Horus está en la cripta, pero para bajar hay que oír antes al visir. Quiere que el agua del Nilo llegue a todos los campos del valle, sin gastar de más». Ya conocéis la nota del visir.",
                 ["Hay que repartir el agua entre los campos."],
                 "Un patio de templo egipcio con tarros de pintura y una sacerdotisa de túnica blanca y pelo negro con una diadema de oro, riendo con las manos en la cintura. Cristina la mira con una sonrisa de complicidad y Alberto, con restos de pintura turquesa en la mejilla, levanta un pincel con gesto triunfal."),
    "69": app("69", "Los canales de riego", "Es un juego de la app: unir con canales los siete campos del valle gastando lo menos posible.", 80,
              ["El mapa de los campos, con lo que cuesta cada posible canal, en la carta 70; lo que quiere el visir, en la 71.", "Empezad por el canal más barato y seguid con el siguiente más barato que no cierre un círculo de agua.", f"Los canales: {_S_CAN}."],
              SIN_GENTE + "Un valle egipcio visto desde arriba, con siete campos verdes unidos por zanjas de riego y el río azul al fondo."),
    "70": gris("70", "Los campos del valle", "El mapa de los siete campos del valle, con lo que costaría cavar un canal entre cada dos.",
               ["Sirve para los canales (carta 69).", "Los números son los codos de zanja de cada canal posible.", f"Los canales: {_S_CAN}."], codigo("el mapa de los campos")),
    "71": gris("71", "La nota del visir", "Una nota del visir sobre el riego.",
               ["Sirve para los canales (carta 69).", "Todos los campos con agua, sin zanjas de más.", f"Los canales: {_S_CAN}."], codigo("la nota del visir")),
    "80": escena("80", "El visir", [72, 75, 79], [58, 69, 70, 71],
                 "El agua corre por los canales y el visir, un hombre alto con una tira de lino dorado al pecho, os recibe con una reverencia. «Ahora el reparto: tras la crecida, el río se lleva los mojones de los campos y hay que volver a medirlos. No saben cómo. Y yo, tampoco». Os da un plano del campo con las medidas.",
                 ["El campo por repartir son dos cartas."],
                 "Un campo egipcio junto al Nilo tras la crecida, con un visir alto de lino blanco y collar dorado señalando con un bastón el terreno vacío, y campesinos esperando. Alberto asiente con aire de seriedad profesional, midiendo con la vista, y Cristina mira el campo con las manos en la frente a modo de visera."),
    "72": app("72", "El reparto de tierras", "Es un juego de la app: dividir el campo en parcelas rectangulares, cada una con su número de casillas.", 82,
              ["El campo, con los números, son las cartas 75 y 79; la app solo muestra el campo vacío.", "Cada parcela es un rectángulo con un solo número, que dice cuántas casillas tiene. Empezad por los números más grandes o por los de las esquinas.", f"Las parcelas, de arriba abajo y de izquierda a derecha: {_S_TIE}."],
              SIN_GENTE + "Un gran campo egipcio cuadrado, vacío, visto desde arriba, con mojones de piedra en los bordes y cuerdas tensas."),
    "75": pieza("75", "tierras", "Media lámina del campo por repartir.", ["Es la mitad de un plano: juntadla con la carta 79.", "Cada número es el tamaño de una parcela.", f"Las parcelas: {_S_TIE}."]),
    "79": pieza("79", "tierras", "Media lámina del campo por repartir.", ["Es la mitad de un plano: juntadla con la carta 75.", "Cada número es el tamaño de una parcela.", f"Las parcelas: {_S_TIE}."]),
    "82": escena("82", "El visir agradecido", [85, 86, 87], [80, 72, 75, 79],
                 "Los campesinos replantan los mojones y el visir os entrega, para agradeceros, lo que guardaba un viejo sacerdote: las instrucciones para despertar a un «carro del sol» de latón y cristal. Os suena. Y una nota con dos acertijos sobre cinco sellos.",
                 ["La consola es el último puzle."],
                 "Los campesinos clavan mojones de piedra en un campo recién repartido, y el visir de lino blanco entrega a Cristina un papiro sellado. Ella lo desenrolla con una sonrisa emocionada, y Alberto, detrás, mira el aparato de latón que lleva en la mochila con las cejas muy altas."),
    "85": app("85", "La consola del Cronoportal", "Es un juego de la app: cada puzle resuelto dejó un sello en el aparato. Hay que tocar cinco en el orden de los acertijos.", 99,
              ["Los acertijos de la sacerdotisa están en las cartas 86 y 87; los sellos son los signos de los puzles que ya habéis resuelto.", "Cada acertijo describe un sello por lo que representa: lo que sube y baja, lo que se reparte, lo que se amasa...", f"Los cinco sellos, en orden: {_S_SEL}."],
              SIN_GENTE + "La consola del Cronoportal: un panel de latón con diez medallones de oro, cada uno con un signo egipcio distinto, y cinco huecos en fila."),
    "86": gris("86", "Primera parte del orden", "Los tres primeros sellos, en un acertijo.",
               ["Sirve para la consola (carta 85).", "Tres sellos: lo que sube y baja con el año, lo que se reparte con cordel y lo que se amasa y se come.", f"Los cinco sellos, en orden: {_S_SEL}."], codigo("los tres primeros sellos")),
    "87": gris("87", "Segunda parte del orden", "Los dos últimos sellos, en otro acertijo.",
               ["Sirve para la consola (carta 85).", "Dos sellos: el que mide con sus seis partes y el que empuja el sol.", f"Los cinco sellos, en orden: {_S_SEL}."], codigo("los dos últimos sellos")),
    # ------------------------------------------------------------------ La cripta y el final
    "94": escena("94", "La cripta del Ojo", [64, 66, 67], [38, 56, 30, 44, 33, 37, 39, 46],
                 "La brasa enciende la lámpara y una luz cálida baja por una escalera de piedra hasta una cripta redonda. En las paredes, un friso de azulejos con una figura que falta: un hueco entre los demás. Cuando el friso esté completo, la cripta se abrirá. El friso, dibujado, es lo único que se ve del hueco.",
                 ["El friso son dos cartas: juntadlas."],
                 "Una cripta circular egipcia iluminada por una lámpara de bronce con llama cálida, con un friso de azulejos de colores en la pared al que le falta uno. Cristina sostiene la lámpara en alto con gesto cauteloso y Alberto mira el friso con la cabeza ladeada, pensativo, apretando los labios."),
    "64": app("64", "El friso de azulejos", "Es un juego de la app: falta un azulejo en el friso de la cripta; hay que elegir el que lo completa entre seis.", 62,
              ["El friso, partido en dos láminas, son las cartas 66 y 67.", "Fijaos en cómo cambian la figura, el color y el tamaño en cada fila y en cada columna: cada cosa sigue su propia regla.", f"Es {_S_AZU}."],
              SIN_GENTE + "Un hueco cuadrado en un friso de azulejos de colores en la pared de una cripta egipcia, y seis azulejos sueltos de distintas figuras sobre una mesa de piedra."),
    "66": pieza("66", "azulejos", "Media lámina del friso de azulejos.", ["Es la mitad de un friso: juntadla con la carta 67.", "Cada azulejo lleva una figura, un color y un tamaño.", f"Es {_S_AZU}."]),
    "67": pieza("67", "azulejos", "Media lámina del friso de azulejos.", ["Es la mitad de un friso: juntadla con la carta 66.", "Cada azulejo lleva una figura, un color y un tamaño.", f"Es {_S_AZU}."]),
    "62": combinable("62", "Ojo de Horus", "roja", 12, 74, "El Ojo de Horus, una joya de oro y lapislázuli que guarda una energía azul antiquísima, escondida bajo una losa de la cripta.",
                     SIN_GENTE + "Un amuleto del Ojo de Horus de oro y lapislázuli con un fulgor azul en el centro, sobre un cojín de lino en un hueco de piedra."),
    "74": escena("74", "Cronoportal con energía", [], [62, 12, 64, 66, 67, 94, 57],
                 "El Ojo de Horus encaja en el Cronoportal y el aparato se llena de luz... pero se queda en un zumbido: le falta orden. Los sellos de todos los puzles que habéis resuelto están grabados en su consola y piden que los pongáis en el orden correcto.",
                 ["Falta despertar la consola."],
                 "El Cronoportal con el Ojo de Horus engarzado en el pecho, brillando con luz azul, en una cripta egipcia iluminada. Alberto ajusta los diales con la lengua entre los dientes y Cristina sostiene la lámpara con una sonrisa de alivio cansado."),
    "99": escena("99", "De vuelta a casa (FIN)", [], [74, 82, 85, 86, 87],
                 "Los cinco sellos brillan uno tras otro y el Cronoportal despierta con un zumbido grave. Salta un arco de luz azul y dorada y, en un instante, os arranca de la cripta. Aterrizáis en vuestro salón, con polvo dorado en la ropa y un amuleto del Ojo de Horus caliente en la mano. Cristina y Alberto se miran. «¿Otra vez?», dice él. FIN.",
                 [],
                 "La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ve la cripta egipcia iluminada por una lámpara. Llevan aún su ropa actual con polvo dorado y Cristina sostiene un amuleto del Ojo de Horus. Cristina ríe a carcajadas, llena de alegría; Alberto la mira con una ceja levantada y una sonrisa de incredulidad divertida. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(juego="Egipto, 1274 a.C. — El Ojo de Horus", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()})

SPEC = dict(final="99", needs={
    "24": ["14", "16"], "28": ["20", "18", "19", "21"], "57": ["22", "35"], "30": ["40", "41", "43", "45"], "36": ["48", "42", "49", "53"],
    "44": ["52", "54", "55", "59"], "56": ["46", "37", "39", "33"], "58": ["51", "26", "61", "63"], "80": ["69", "70", "71"], "94": ["38", "56"],
    "62": ["64", "66", "67"], "82": ["72", "75", "79"], "74": ["12", "62"], "99": ["85", "86", "87", "74"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_T = [
    ("leer", "P", "Llegada", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12."),
    ("leer", "10", "La cámara oculta", "Lee la carta 10. Descarta la P y coge 14, 16, 18, 19, 20, 21 y 22. Junta la pirámide: 19 arriba y 21 abajo."),
    ("app", "14", "El granero", f"En el móvil: Acción, 14. Un montón, su mitad y su cuarto suman 28 (16): {I.MONTON['solucion']} sacos. El mensaje te dice que cojas la 24.", "carta 24"),
    ("leer", "24", "El granero abierto", "Lee la carta 24. Descarta 14 y 16 y coge la 26 (guárdala para las cámaras)."),
    ("app", "20", "La pirámide", f"En el móvil: Acción, 20. Cada piedra suma las dos de debajo (18, 19 y 21): la base es {_S_PIRA}. El mensaje te dice que cojas la 28.", "carta 28"),
    ("leer", "28", "Tras el muro", "Lee la carta 28. Descarta 18, 19, 20 y 21 y coge la 35."),
    ("combinar", "22", "35", "El medallón", "Las dos mitades del medallón (22 y 35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El medallón de Tebas", "Lee la carta 57. Descarta 22, 35, 10 y 28 y coge 31 y 32."),
    ("leer", "31", "La sala del Nilo", "Lee la carta 31. Coge 40, 41, 43 y 45."),
    ("app", "40", "El nilómetro", f"En el móvil: Acción, 40. Las subidas de las crecidas (41, 43 y 45, con 7 palmos por codo) suben de dos en dos: {_S_NILO}. El mensaje te dice que cojas la 30.", "carta 30"),
    ("leer", "30", "Las compuertas", "Lee la carta 30. Descarta 31, 40, 41, 43 y 45 y coge la 38."),
    ("leer", "32", "La galería del friso", "Lee la carta 32. Coge 42, 48, 49 y 53. Junta el friso: 42 a la izquierda y 49 a la derecha."),
    ("app", "48", "El friso", f"En el móvil: Acción, 48. Animales que miran a la derecha (42, 49 y 53): {_S_FRISO}. El mensaje te dice que cojas la 36.", "carta 36"),
    ("leer", "36", "La casa de las medidas", "Lee la carta 36. Descarta 32, 42, 48, 49 y 53 y coge 52, 54, 55 y 59."),
    ("app", "52", "El heqat", f"En el móvil: Acción, 52. Los pagos (55 y 59) suman 37/64 con las partes de la carta 54: {_S_HEQAT}. El mensaje te dice que cojas la 44.", "carta 44"),
    ("leer", "44", "La casa del escriba", "Lee la carta 44. Descarta 36, 52, 54, 55 y 59 y coge 33, 37, 39, 46, 51, 61 y 63. Junta el plano: 61 a la izquierda y 63 a la derecha."),
    ("app", "46", "El cofre del escriba", f"En el móvil: Acción, 46. Con la suma (37) y las dos notas (39 y 33): {_S_CRIPTO}. El mensaje te dice que cojas la 56.", "carta 56"),
    ("app", "51", "Las cámaras de colores", f"En el móvil: Acción, 51. Con el papiro (26) y el plano (61 y 63): {_S_CAM}. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "El secreto de la sacerdotisa", "Lee la carta 58. Descarta 51, 61, 63, 26 y 24 y coge 69, 70 y 71."),
    ("app", "69", "Los canales", f"En el móvil: Acción, 69. El riego más barato (70 y 71): {_S_CAN}. El mensaje te dice que cojas la 80.", "carta 80"),
    ("leer", "80", "El visir", "Lee la carta 80. Descarta 58, 69, 70 y 71 y coge 72, 75 y 79. Junta el campo: 75 a la izquierda y 79 a la derecha."),
    ("app", "72", "El reparto de tierras", f"En el móvil: Acción, 72. Parcelas rectangulares con un número cada una (75 y 79): {_S_TIE}. El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "El visir agradecido", "Lee la carta 82. Descarta 80, 72, 75 y 79 y coge 85, 86 y 87."),
    ("combinar", "38", "56", "La lámpara", "La lámpara (38) y la brasa (56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "La cripta del Ojo", "Lee la carta 94. Descarta 38, 56, 30, 44, 33, 37, 39 y 46 y coge 64, 66 y 67. Junta el friso: 66 arriba y 67 abajo."),
    ("app", "64", "El friso de azulejos", f"En el móvil: Acción, 64. Con las tres reglas del friso (66 y 67): {_S_AZU}. El mensaje te dice que cojas la 62.", "carta 62"),
    ("combinar", "12", "62", "El Ojo de Horus", "El Cronoportal (12) y el Ojo de Horus (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "Cronoportal con energía", "Lee la carta 74. Descarta 62, 12, 64, 66, 67, 94 y 57."),
    ("app", "85", "La consola", f"En el móvil: Acción, 85. Con los acertijos (86 y 87): {_S_SEL}. El mensaje te dice que cojas la 99.", "carta 99"),
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

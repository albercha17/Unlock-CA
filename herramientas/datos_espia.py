"""Montecarlo, 1965: Operación Cristal — versión de 60 cartas (22 oct 2026), mucho más difícil y variada.

Once puzles de tipos que no salen en ningún otro juego de la serie, con las pistas dibujadas o en acertijo (ninguna carta explica cómo se resuelve su puzle):
una nota cifrada por sustitución, la ruta más rápida por unas calles cortadas, un skyline de rascacielos con las pistas del borde en dos cartas, la cifra de
un libro, una caja fuerte con jaulas (KenKen), la cuenta de cartas del crupier, los dígitos de control de unos pasaportes, un vuelo con escalas y husos
horarios, el manual de un desactivador de cables, la martingala de una ruleta y un teléfono rojo cuya clave se marca con las pulsaciones que dejaron otros
cinco puzles. Solo 16 cartas tienen a Cristina y Alberto (escenas); el resto son objetos y pistas sin personas. Las cartas-pista las dibuja
herramientas/espia.py (instancias_espia.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402
import instancias_espia as I  # noqa: E402

ESTILO = ("Ilustración pictórica semirrealista con aire de película de espías de los años 60 (como James Bond y La Pantera Rosa), paleta pop mediterránea de turquesa, rosa, dorado y blanco, "
          "luz de noche de gala con las luces del puerto de Montecarlo, casino, yates, hotel y terrazas con farolillos, formato vertical 2:3. Sin texto, letras ni números legibles en la imagen; "
          "los papeles, carteles y pantallas solo muestran rayas decorativas. Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado recogido en un moño alto con una diadema, ojos azules. Viste ropa de espía elegante de los años 60: un vestido corto rosa empolvado con cinturón blanco, guantes cortos blancos, grandes gafas de sol redondas subidas al pelo y zapatos de tacón bajo.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno engominado, barba cuidada, ojos marrones. Viste ropa de espía elegante de los años 60: un esmoquin negro entallado con pajarita, camisa blanca, un reloj de pulsera grande y un pequeño maletín plateado.",
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado recogido en un moño alto con una diadema, ojos azules, vestido corto rosa empolvado con cinturón blanco, guantes cortos blancos, grandes gafas de sol redondas subidas al pelo y zapatos de tacón bajo. "
        "Alberto: hombre de 27 años, informático, pelo moreno engominado, barba cuidada, ojos marrones, esmoquin negro entallado con pajarita, camisa blanca, reloj de pulsera grande y un pequeño maletín plateado. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo cinematográfico de película de espías de los años 60, colores pop de turquesa, rosa y dorado, y mucho contraste. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Cristina señala una foto antigua del casino de Montecarlo en un libro. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul y dorada y los dos son absorbidos por un túnel de luz. "
         "Escena 3 (8-12 s): caen en la terraza de un casino junto al puerto de Montecarlo, de noche, entre farolillos y yates; el aparato golpea una mesa y su cristal sale rodando, y una mano con guante negro lo recoge. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, con ropa de espías elegantes, asombrados, mirando cómo un yate negro se aleja del puerto; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe sordo al aterrizar, música de big band con vibráfono y bajo de espías, sin voz de narrador.")

SIN_GENTE = "Sin ninguna persona en la imagen. "

MOSAICOS = {
    "plano": dict(filas=2, cols=1, cartas=["19", "21"], titulo="El plano de Montecarlo"),
    "caja": dict(filas=1, cols=2, cartas=["54", "55"], titulo="La caja fuerte del joyero"),
    "pasaportes": dict(filas=2, cols=1, cartas=["61", "63"], titulo="Los pasaportes falsos"),
}
POS = {(2, 1): ["mitad de arriba", "mitad de abajo"], (1, 2): ["mitad izquierda", "mitad derecha"]}

_S_CRI = I.CRIPTOGRAMA["claro"]
_S_RUT = " → ".join(I.RUTA["nodos"][k] for k in I.RUTA["camino"]) + f" ({I.RUTA['mejor']} minutos)"
_S_RAS = " / ".join("".join(str(v) for v in f) for f in I.RASCACIELOS["solucion"])
_S_LIB = I.LIBRO["claro"]
_S_KEN = " / ".join("".join(str(v) for v in f) for f in I.KENKEN["solucion"])
_S_CON = f"{I.CONTEO['cuenta_corte']} en el corte y {I.CONTEO['cuenta_final']} al final"
_S_PAS = ", ".join(str(x) for x in I.PASAPORTES["digitos"])
_L = I.HUSOS["llegada"]
_S_HUS = f"{_L['dia']} día(s) después de la salida, a las {_L['hora']}:{_L['min']:02d}"
_S_CAB = ", ".join(f"carga {i + 1}: el cable {c['corta'] + 1}" for i, c in enumerate(I.CABLES["cargas"]))
_S_RUL = str(I.RULETA["final"])
_S_TEC = " + ".join(f"{I.PULSA[k]} ({l})" for k, l in zip(I.ORDEN, I.PALABRA))


def codigo(que):
    return f"Carta dibujada por código (herramientas/espia.py; no se pide a ChatGPT): {que}."


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
    # ------------------------------------------------------------------ El casino
    "P": escena("P", "Llegada a Montecarlo", [10, 12], [],
                "Décima parada del Cronoportal: Montecarlo, 1965, noche de gala. Aterrizáis en la terraza del casino, entre farolillos y copas de champán, y el aparato golpea una mesa. Su cristal de energía sale rodando y una mano con guante negro lo recoge al vuelo: es el Dr. Noche, un villano con capa que colecciona gemas, que susurra «perfecta para mi colección» y desaparece hacia su yate, el Neptuno. Una mujer con gafas de sol se os acerca: es la Agente Zorro, de una agencia secreta. «Llevamos meses detrás de él. Ayudadnos y recuperaréis vuestra gema, pero el yate zarpa a medianoche: tenéis noventa minutos». Os da un sobre.",
                ["Mirad a vuestro alrededor y revisad el aparato."],
                "La terraza de un casino de Montecarlo en 1965 de noche, con farolillos, copas de champán y yates en el puerto al fondo; un yate negro se aleja. En primer plano, el Cronoportal, un aparato de latón y cristal, humea contra una mesa con la luz azul apagándose. Cristina, con la boca abierta y los ojos muy abiertos de asombro, y Alberto, con una ceja arqueada y la pajarita torcida de incredulidad, se levantan aturdidos con ropa de espías elegantes."),
    "10": escena("10", "El sobre de la Agente Zorro", [14, 16, 18, 19, 20, 21, 22], ["P"],
                 "En el sobre hay una nota con letras sin sentido, firmada por Zorro (carta 16), y un acertijo de la policía sobre el desfile del Gran Premio (carta 18). Sobre el mantel, un plano de Montecarlo en dos láminas: juntad la 19 arriba y la 21 abajo (carta 20). Entre los papeles, Alberto encuentra además la mitad de un microfilm (carta 22).",
                 ["Hay dos puzles: la nota secreta y la persecución.", "El plano son dos cartas: juntadlas, una encima de otra."],
                 "Una mesa de terraza de un casino de Montecarlo en 1965 con un sobre abierto, una nota con letras raras, un plano de calles y la mitad de una tira de microfilm. Cristina lee la nota con los ojos entrecerrados y la nariz arrugada; Alberto, con una copa de champán en la mano, repasa el plano con la boca abierta."),
    "12": combinable("12", "Cronoportal sin cristal", "azul", 62, 74,
                     "El Cronoportal: una consola de latón y cristal con un anillo central apagado y un hueco vacío en el pecho, donde iba el cristal de energía.",
                     SIN_GENTE + "Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo de cristal central apagado y un hueco circular vacío en el pecho del aparato, sobre un mantel blanco de una mesa de terraza, con farolillos desenfocados al fondo."),
    "14": app("14", "La nota de la Agente Zorro", "Es un juego de la app: una nota escrita con un alfabeto cambiado, en el que cada letra es siempre otra. Hay que escribir el mensaje original.", 24,
              ["La nota está en la carta 16 y, en ella, Zorro da una pista: su firma.", "La primera palabra ya os da cinco letras del alfabeto cambiado. Buscad esas letras en el resto de la nota: las palabras cortas (EN, EL, DE, LA) caen enseguida.", f"El mensaje dice: {_S_CRI}. Teléfono rojo: pulsaciones {I.PULSA['14']}."],
              SIN_GENTE + "Una nota doblada con letras sin sentido sobre un mantel de casino, junto a una pluma estilográfica y un sello de lacre rosa, con luz de farolillo."),
    "16": gris("16", "La nota de Zorro", "Una nota interceptada en el casino, escrita con letras sin sentido, con una firma de Zorro debajo.",
               ["Es el mensaje de la nota secreta (carta 14).", "Cada letra del mensaje cambia siempre por la misma otra.", "Zorro firma con su cargo: la primera palabra es una pista."]),
    "18": gris("18", "El acertijo del desfile", "Un acertijo del cartel de la policía sobre las calles cortadas por el Gran Premio.",
               ["Dice qué glorietas están cortadas (carta 20).", "Hay que salir del Casino (A) y llegar al Puerto (I).", "Cada calle del plano lleva el tiempo que se tarda en recorrerla."]),
    "19": pieza("19", "plano", "Media lámina del plano de Montecarlo.", ["Es la mitad de una lámina: juntadla con la carta 21.", "Es un plano con nueve glorietas y las calles que las unen.", "El acertijo del desfile está en la carta 18."]),
    "21": pieza("21", "plano", "Media lámina del plano de Montecarlo.", ["Es la mitad de una lámina: juntadla con la carta 19.", "Es un plano con nueve glorietas y las calles que las unen.", "El acertijo del desfile está en la carta 18."]),
    "20": app("20", "La persecución por Montecarlo", "Es un juego de la app: llegar con el coche del Casino al Puerto por el camino más rápido, sin cruzar las glorietas que corta el desfile.", 28,
              ["El plano está en las cartas 19 y 21 y el acertijo del desfile, en la 18.", "Tachad primero las glorietas cortadas. Luego sumad los minutos de cada camino que llegue al Puerto y quedaos con el más corto.", f"El camino más rápido: {_S_RUT}."],
              SIN_GENTE + "Un coche deportivo descapotable de los años 60 en una curva del circuito urbano de Montecarlo, con el puerto y los yates al fondo, de noche, entre farolillos."),
    "22": combinable("22", "Media tira de microfilm", "azul", 35, 57, "Una mitad de una tira de microfilm, con una hilera de fotogramas diminutos.",
                     SIN_GENTE + "La mitad izquierda de una tira de microfilm con una hilera de fotogramas diminutos, sobre un mantel blanco de casino, con luz de farolillo."),
    "24": escena("24", "Zorro en el muelle", [26], [14, 16],
                 "Descifráis la nota: Zorro os espera en el muelle de la ruleta azul, junto al puerto. Allí os da la mano y os pasa discretamente una hoja con las normas de la aduana, por si acaso tenéis que revisar pasaportes más adelante (carta 26). «Guardadla —susurra—, el Dr. Noche tiene a medio puerto con documentos falsos».",
                 ["Mirad lo que os da Zorro."],
                 "Un muelle de Montecarlo de noche con un cartel luminoso en forma de ruleta azul y yates amarrados. La Agente Zorro, con gabardina y gafas de sol, entrega una hoja doblada a Cristina y Alberto. Cristina la coge con una sonrisa cómplice y el dedo en los labios; Alberto mira de reojo a ambos lados con cara de sospecha."),
    "26": gris("26", "La regla del aduanero", "Una hoja sellada de la aduana con la regla del dígito de control de los pasaportes.",
               ["Habla de los pasaportes (carta 51).", "Cada letra vale lo que su puesto en el abecedario más nueve.", "Los pesos son 7, 3 y 1, y se repiten."]),
    "28": escena("28", "El Puerto", [35], [18, 19, 20, 21],
                 "Llegáis al Puerto por el camino más corto y el coche patina frente a un almacén. Dentro, entre cajas de champán, un sobre rosa con la otra mitad del microfilm (carta 35).",
                 ["Mirad en el almacén."],
                 "El almacén de un puerto de Montecarlo, de noche, lleno de cajas de champán y cuerdas, con una lámpara colgada. Cristina saca un sobre rosa de una caja con los ojos como platos; Alberto, apoyado en la puerta, jadea con la lengua fuera."),
    "35": combinable("35", "Otra media tira de microfilm", "roja", 22, 57, "La otra mitad de la tira de microfilm, con la otra hilera de fotogramas.",
                     SIN_GENTE + "La mitad derecha de una tira de microfilm con una hilera de fotogramas diminutos, sobre un sobre rosa, con luz de farolillo."),
    "57": escena("57", "El microfilm completo", [31, 32], [22, 35, 10, 28],
                 "Juntáis las dos mitades y a la luz del proyector aparecen los planos secretos del Dr. Noche: una azotea de un hotel con torres de oficinas (carta 31) y la biblioteca del casino, donde se esconde su libro de cuentas (carta 32). Hay que visitar los dos.",
                 ["Dos sitios: la azotea del hotel y la biblioteca del casino."],
                 "Cristina y Alberto con un proyector de diapositivas antiguo sobre una mesa, que proyecta en la pared unos planos de un hotel y de una biblioteca, en la penumbra de una suite de los años 60. Cristina señala la pared con la boca entreabierta de emoción; Alberto levanta las cejas y se frota las manos."),
    # ------------------------------------------------------------------ Rama 1: la azotea del hotel
    "31": escena("31", "La azotea del hotel", [40, 41, 43, 45], [],
                 "En la azotea del hotel hay una maqueta de cinco torres que parece un panel de control con la rejilla vacía (carta 40). Los números del borde, que dicen cuántas torres se ven desde cada lado, están en dos láminas: arriba e izquierda en la 41; abajo y derecha en la 43. El arquitecto dejó escrita la regla en la carta 45.",
                 ["Un único puzle: el skyline de las torres."],
                 "La azotea de un hotel de lujo de Montecarlo de noche con una maqueta de torres de distintas alturas sobre una mesa y una rejilla de casillas vacía al lado, con las luces de la ciudad al fondo. Cristina compara la maqueta con la rejilla con el ceño fruncido; Alberto se agacha para mirar las torres a ras de mesa con un ojo cerrado."),
    "40": app("40", "El skyline del casino", "Es un juego de la app: colocar torres de una a cinco plantas, una por casilla, sin repetir alturas en ninguna fila ni columna, de modo que cada número del borde diga cuántas torres se ven desde allí.", 30,
              ["Los números del borde están en las cartas 41 y 43 y la regla, en la 45.", "Un 5 en el borde significa que se ven todas: están ordenadas de la más baja a la más alta. Un 1 significa que la más alta está justo en el borde.", f"El skyline, por filas: {_S_RAS}. Teléfono rojo: pulsaciones {I.PULSA['40']}."],
              SIN_GENTE + "Una maqueta de cinco torres de oficinas de distintas alturas sobre una mesa de una azotea, con una rejilla de cinco por cinco al lado, de noche, con las luces de Montecarlo al fondo."),
    "41": gris("41", "Los números del borde (arriba e izquierda)", "Una lámina con la rejilla del skyline y los números de su borde de arriba y de la izquierda.",
               ["Son las pistas del borde del skyline (carta 40).", "Esta lámina da solo dos lados: arriba e izquierda.", "Los otros dos lados están en la carta 43."]),
    "43": gris("43", "Los números del borde (abajo y derecha)", "Una lámina con la rejilla del skyline y los números de su borde de abajo y de la derecha.",
               ["Son las pistas del borde del skyline (carta 40).", "Esta lámina da solo dos lados: abajo y derecha.", "Los otros dos lados están en la carta 41."]),
    "45": gris("45", "La regla del arquitecto", "Una nota del arquitecto con la regla del skyline, escrita en versos.",
               ["Explica cómo se leen los números del borde (carta 40).", "Las torres altas esconden a las bajas que tienen detrás.", "Cada fila y cada columna tienen torres de todas las alturas."]),
    "30": escena("30", "La trampilla de la azotea", [38], [31, 40, 41, 43, 45],
                 "Las torres encajan y la maqueta se hunde en la mesa: debajo, una trampilla esconde media llave dorada con un llavero de ancla (carta 38).",
                 ["Mirad debajo de la maqueta."],
                 "Una mesa de azotea con una maqueta de torres que se ha hundido y deja ver una trampilla abierta con media llave dorada de ancla dentro, de noche. Cristina la saca con dos dedos y una sonrisa traviesa; Alberto la mira con la boca abierta y los ojos brillantes."),
    "38": combinable("38", "Mitad de la llave del camarote", "roja", 56, 94, "Una mitad de una llave dorada con un llavero de ancla, de las del camarote de un yate.",
                     SIN_GENTE + "La mitad izquierda de una llave dorada con un llavero en forma de ancla, de las de un camarote de yate, sobre un cojín de terciopelo rojo."),
    # ------------------------------------------------------------------ Rama 2: la biblioteca del casino
    "32": escena("32", "La biblioteca del casino", [42, 48, 49, 53], [],
                 "En la biblioteca hay una novela de bolsillo, «La última carta», con dos páginas marcadas con una cinta rosa (cartas 42 y 49). En el borde de un marcapáginas, el Dr. Noche anotó su mensaje con tres números por palabra (carta 53).",
                 ["Un único puzle: el mensaje escondido en el libro."],
                 "Una biblioteca elegante de un casino de los años 60 con estanterías hasta el techo, un sillón de cuero y una novela de bolsillo abierta sobre una mesa con una cinta rosa de marcapáginas. Cristina pasa un dedo por las páginas con la cabeza ladeada; Alberto cuenta con los dedos mirando el techo."),
    "48": app("48", "La cifra del libro", "Es un juego de la app: un mensaje escondido en una novela de bolsillo. Cada palabra del mensaje está dada por tres números (página, renglón y palabra). Hay que escribir el mensaje que sale.", 36,
              ["Las dos páginas del libro están en las cartas 42 y 49 y los números del mensaje, en la 53.", "Primero el número de página; luego, el renglón, contando desde arriba; y al final, la palabra de ese renglón, de izquierda a derecha.", f"El mensaje dice: {_S_LIB}."],
              SIN_GENTE + "Una novela de bolsillo abierta por la mitad sobre una mesa, con una cinta rosa de marcapáginas y un lápiz, con luz de lámpara de casino."),
    "42": gris("42", "La página 17 de «La última carta»", "Una página de la novela de bolsillo, con nueve renglones.", ["Es una de las dos páginas del libro (carta 48).", "Tiene nueve renglones.", "La otra página está en la carta 49."]),
    "49": gris("49", "La página 18 de «La última carta»", "Una página de la novela de bolsillo, con nueve renglones.", ["Es una de las dos páginas del libro (carta 48).", "Tiene nueve renglones.", "La otra página está en la carta 42."]),
    "53": gris("53", "Los renglones del mensaje", "Un marcapáginas con los números del mensaje, de tres en tres.", ["Cada grupo de tres números es una palabra del mensaje (carta 48).", "Siempre en el mismo orden: página, renglón, palabra.", "Las páginas del libro están en las cartas 42 y 49."]),
    "36": escena("36", "La caja fuerte del joyero", [52, 54, 55, 59], [32, 42, 48, 49, 53],
                 "El mensaje apunta a la joyería del casino, donde hay una caja fuerte a la vista de todos. Su cerradura tiene la forma de una rejilla de cinco por cinco (carta 52): el tablero con las jaulas ocupa dos láminas, que juntáis a izquierda y derecha (cartas 54 y 55), y la regla del joyero está grabada en la propia cerradura (carta 59).",
                 ["Un único puzle: abrir la caja fuerte."],
                 "La trastienda de una joyería de lujo de los años 60, con vitrinas de cristal y una caja fuerte redonda de acero en la pared, con una cerradura en forma de rejilla. Cristina examina la cerradura con una lupa de joyero y los ojos desorbitados; Alberto se limpia el sudor de la frente con un pañuelo y cara de agobio."),
    "52": app("52", "La caja fuerte del joyero", "Es un juego de la app: rellenar con cifras del 1 al 5 una rejilla de cinco por cinco, sin repetir en filas ni columnas, de modo que cada jaula de trazo grueso cumpla la operación que lleva escrita.", 44,
              ["El tablero con las jaulas está en las cartas 54 y 55 y la regla, en la 59.", "Empezad por las jaulas de una casilla (llevan el número solo) y por las que suman o multiplican pocas cifras: solo caben unas parejas.", f"La caja, por filas: {_S_KEN}. Teléfono rojo: pulsaciones {I.PULSA['52']}."],
              SIN_GENTE + "Una caja fuerte redonda de acero en una pared, con una cerradura en forma de rejilla de casillas y un resplandor dorado en una rendija, en la trastienda de una joyería de lujo."),
    "54": pieza("54", "caja", "Media lámina del tablero de la caja fuerte.", ["Es la mitad de una lámina: juntadla con la carta 55.", "Las jaulas llevan un número y una operación.", "La regla del joyero está en la carta 59."]),
    "55": pieza("55", "caja", "Media lámina del tablero de la caja fuerte.", ["Es la mitad de una lámina: juntadla con la carta 54.", "Las jaulas llevan un número y una operación.", "La regla del joyero está en la carta 59."]),
    "59": gris("59", "La regla del joyero", "Una nota grabada en la cerradura de la caja fuerte, en versos.", ["Explica cómo se rellena la caja (carta 52).", "Son cifras del uno al cinco.", "En la resta y la división manda la mayor sobre la menor."]),
    # ------------------------------------------------------------------ La sala de juego
    "44": escena("44", "La sala de juego", [33, 37, 39, 46, 51, 61, 63], [36, 52, 54, 55, 59],
                 "El joyero os abre la puerta de la sala de juego. En la mesa de blackjack, un crupier reparte veintiocho cartas seguidas (cartas 37 y 39) y susurra que el que lleve bien la cuenta se llevará una sorpresa (carta 46); la regla de la cuenta la cuelga en un cartel (carta 33). Al fondo, en la mesa de documentos, tres pasaportes sin acabar de sellar, en dos láminas: juntad la 61 arriba y la 63 abajo (carta 51).",
                 ["Hay dos puzles: la cuenta del crupier y los pasaportes."],
                 "Una sala de juego de un casino de Montecarlo en 1965, con una mesa de blackjack con fieltro verde y un crupier repartiendo cartas, y al fondo una mesa de documentos con pasaportes abiertos. Cristina, con una mano en la cadera, vigila al crupier con una ceja levantada de sospecha; Alberto mira los pasaportes con la boca torcida de duda."),
    "46": app("46", "La cuenta del crupier", "Es un juego de la app: el crupier reparte veintiocho cartas y cada una suma, resta o no cuenta según su valor. Hay que decir cuánto vale la cuenta al llegar al corte y cuánto al final.", 56,
              ["Las cartas están en las cartas 37 y 39 y la regla de la cuenta, en la 33.", "Contad carta a carta, en el orden en que salen, empezando de cero. En el corte hay que parar y anotar; luego se sigue desde ahí hasta la última.", f"La cuenta: {_S_CON}."],
              SIN_GENTE + "Una mesa de blackjack con fieltro verde y varias cartas boca arriba en fila, y un montoncito de fichas, bajo una lámpara de casino de los años 60."),
    "37": gris("37", "Las cartas del crupier (I)", "Las primeras catorce cartas que reparte el crupier, en el orden en que salen.", ["Son las primeras cartas de la cuenta (carta 46).", "Se leen en orden: de izquierda a derecha y de arriba abajo.", "Las otras catorce están en la carta 39."]),
    "39": gris("39", "Las cartas del crupier (II)", "Las últimas catorce cartas que reparte el crupier, en el orden en que salen.", ["Son las últimas cartas de la cuenta (carta 46).", "Se leen en orden: de izquierda a derecha y de arriba abajo.", "Las primeras catorce están en la carta 37."]),
    "33": gris("33", "La cuenta del crupier", "Un cartel de la mesa de blackjack con la regla de la cuenta, en versos.", ["Explica cómo se cuenta cada carta (carta 46).", "Hay tres clases de cartas: las que suman, las que restan y las que no cuentan.", "Se empieza de cero con la primera carta."]),
    "56": combinable("56", "Otra mitad de la llave", "roja", 38, 94, "La otra mitad de la llave dorada del camarote, que el crupier os desliza al terminar la cuenta.",
                     SIN_GENTE + "La mitad derecha de una llave dorada con un llavero en forma de ancla, de las de un camarote de yate, que una mano con guante blanco desliza sobre un tapete verde."),
    "51": app("51", "Los pasaportes falsos", "Es un juego de la app: en la zona de lectura de cada pasaporte falta el dígito de control del número del documento. Hay que calcular los tres.", 58,
              ["Los pasaportes están en las cartas 61 y 63 y la regla del aduanero, en la 26.", "Cada símbolo del número se multiplica por 7, por 3 o por 1, y vuelta a empezar. Se suma todo y de la suma solo vale la cifra de las unidades.", f"Los dígitos son {_S_PAS}. Teléfono rojo: pulsaciones {I.PULSA['51']}."],
              SIN_GENTE + "Tres pasaportes abiertos sobre una mesa de documentos, con un sello de caucho, una lupa y un tampón de tinta rosa, bajo una lámpara de despacho."),
    "61": pieza("61", "pasaportes", "Media lámina de los tres pasaportes falsos.", ["Es la mitad de una lámina: juntadla con la carta 63.", "Cada pasaporte lleva dos líneas de letras y números en el pie.", "La regla del aduanero está en la carta 26."]),
    "63": pieza("63", "pasaportes", "Media lámina de los tres pasaportes falsos.", ["Es la mitad de una lámina: juntadla con la carta 61.", "Cada pasaporte lleva dos líneas de letras y números en el pie.", "La regla del aduanero está en la carta 26."]),
    # ------------------------------------------------------------------ La aduana, el despacho y el yate
    "58": escena("58", "La aduana del puerto", [69, 70, 71], [51, 61, 63, 26, 24],
                 "Los pasaportes pasan el control y un aduanero os abre una puerta lateral, que da a un almacén aduanero. Allí hay cuatro cargas de explosivos con cables de colores (carta 69): el Dr. Noche las ha puesto para volar el muelle. El manual del desactivador, en dos hojas pegadas a la caja (cartas 70 y 71), dice qué cable cortar.",
                 ["Un único puzle: desactivar las cargas."],
                 "Un almacén aduanero de un puerto con cuatro cajas de madera con cables de colores asomando y un reloj de cuenta atrás en cada una, bajo una bombilla. Cristina, con un destornillador en la mano y la cara pálida, observa los cables conteniendo la respiración; Alberto lee un manual con un dedo en cada línea y la frente arrugada."),
    "69": app("69", "El desactivador", "Es un juego de la app: cuatro cargas con seis cables de colores cada una. Hay que cortar un cable en cada carga, el que diga el manual según los colores.", 80,
              ["El manual está en las cartas 70 y 71.", "Se aplica la primera regla del manual que se cumpla, de arriba abajo. Contad con cuidado los colores de cada carga antes de decidir.", f"Los cortes: {_S_CAB}. Teléfono rojo: pulsaciones {I.PULSA['69']}."],
              SIN_GENTE + "Un panel de conexiones de una centralita telefónica antigua, con seis cables de colores distintos enchufados en una fila de tomas y un reloj de pared encima, en un almacén con poca luz."),
    "70": gris("70", "El manual del desactivador (I)", "La primera hoja del manual del desactivador, con tres reglas numeradas.", ["Son las primeras reglas del manual (carta 69).", "Se mira de arriba abajo y se aplica la primera que se cumpla.", "Las otras reglas están en la carta 71."]),
    "71": gris("71", "El manual del desactivador (II)", "La segunda hoja del manual del desactivador, con las otras reglas numeradas.", ["Son las últimas reglas del manual (carta 69).", "La última sirve para cualquier otro caso.", "Las primeras reglas están en la carta 70."]),
    "80": escena("80", "El salón privado del Dr. Noche", [72, 75, 79], [58, 69, 70, 71],
                 "Las cargas quedan mudas y Zorro os lleva a un salón privado del casino donde el Dr. Noche tiene su ruleta particular. Un camarero chiva que el villano guarda la llave de su caja de caudales bajo la mesa de la ruleta, pero que solo cede a quien sepa cuánto queda en el banco tras sus últimos giros (carta 72). Los doce giros están anotados en una libreta (carta 75) y el sistema de apuestas, escrito en la pared (carta 79).",
                 ["Un único puzle: contar lo que queda en el banco."],
                 "Un salón privado de un casino de Montecarlo con una ruleta de lujo en el centro, una pared con letras doradas y una libreta de piel sobre el tapete. Cristina estudia la libreta con una sonrisa maliciosa; Alberto, con el sombrero hacia atrás, se rasca la cabeza mirando la ruleta."),
    "72": app("72", "La martingala", "Es un juego de la app: el Dr. Noche apuesta siempre al rojo con un sistema fijo. Hay que decir cuántas fichas le quedan en el banco tras los doce giros.", 82,
              ["Los giros están en la carta 75 y el sistema, en la 79.", "Seguid los giros uno a uno, desde el primero, anotando cuánto se apuesta y cuánto queda. El verde siempre pierde.", f"El banco queda en {_S_RUL} fichas."],
              SIN_GENTE + "Una ruleta de casino de lujo vista desde arriba con su bola blanca y varias torres de fichas sobre el tapete verde, bajo una lámpara de cristal, de noche."),
    "75": gris("75", "Los giros de la ruleta", "La libreta del crupier con el color de los doce giros, en el orden en que salieron.", ["Son los resultados de los giros (carta 72).", "Rojo, negro o verde.", "El sistema de apuestas está en la carta 79."]),
    "79": gris("79", "La martingala", "El sistema de apuestas del Dr. Noche, escrito con letras doradas en la pared.", ["Explica cuánto se apuesta en cada giro (carta 72).", "Se apuesta siempre al rojo.", "Depende de si se ha ganado o perdido en el giro anterior."]),
    "82": escena("82", "El yate Neptuno", [85, 86, 87], [80, 72, 75, 79],
                 "La llave os abre la pasarela del Neptuno, el yate negro del Dr. Noche, que arranca los motores. En cubierta hay un teléfono rojo directo con la agencia: la clave para frenar el yate son cinco pulsaciones, las que os dejaron cinco de vuestros puzles (carta 85). Dos hojas dicen en qué orden se marcan (carta 86) y cómo es el teclado (carta 87).",
                 ["Un único puzle: marcar la clave del teléfono rojo."],
                 "La cubierta de un yate negro de lujo de noche, con un teléfono rojo sobre un pedestal de caoba, las luces del puerto de Montecarlo al fondo y los motores echando humo. Cristina descuelga el teléfono con los ojos como platos; Alberto mira por encima del hombro con una mueca de tensión."),
    "85": app("85", "El teléfono rojo", "Es un juego de la app: un teclado de teléfono con letras. La clave se marca con cinco grupos de pulsaciones, los que dejaron otros cinco puzles, y forma una palabra.", 99,
              ["El orden de los cinco grupos está en la carta 86 y el teclado con las letras, en la 87.", "Cada grupo es una tecla pulsada varias veces: una pulsación es la primera letra de la tecla, dos pulsaciones la segunda, y así. Entre una letra y la siguiente hay que tocar «Pausa».", f"Las pulsaciones son {_S_TEC}: la palabra es {I.PALABRA}."],
              SIN_GENTE + "Un teléfono rojo de baquelita con teclado y una antena corta, sobre un pedestal de caoba en la cubierta de un yate, con las luces del puerto desenfocadas al fondo."),
    "86": gris("86", "Las cinco pulsaciones", "Una hoja del cuaderno de la Agente Zorro que dice en qué orden se marcan las cinco pulsaciones.", ["Explica el orden de las cinco pulsaciones.", "Cada una la dejó un puzle distinto.", "Se marca una letra por cada pulsación."]),
    "87": gris("87", "El teclado del teléfono", "El teclado del teléfono rojo, con las letras de cada tecla.", ["Sirve para leer las pulsaciones (carta 85).", "Cada tecla lleva varias letras.", "La pulsación número uno es la primera letra de la tecla."]),
    # ------------------------------------------------------------------ El camarote y el final
    "94": escena("94", "El camarote del Dr. Noche", [64, 66, 67], [38, 56, 30, 44, 33, 37, 39, 46],
                 "Las dos mitades de la llave encajan y abren el camarote del Dr. Noche. Dentro, ni rastro del villano: solo su caja de seguridad empotrada, con un teclado de hora y minuto (carta 64), y en el escritorio, su diario de viaje con el billete de un vuelo con escalas y una tabla de husos horarios (cartas 66 y 67). Dicen que el cristal está dentro.",
                 ["Un único puzle: la hora de llegada del vuelo."],
                 "El camarote de lujo de un yate negro, con una cama con colcha de seda, un escritorio con papeles y un billete de avión, y una caja de seguridad empotrada en la pared con un teclado. Cristina mira el billete con un dedo en la barbilla; Alberto se arremanga y ensaya cuentas en el aire con cara de concentración."),
    "64": app("64", "El vuelo con escalas", "Es un juego de la app: el Dr. Noche voló de Tokio a Montecarlo con dos escalas. Hay que decir a qué hora local de Montecarlo aterrizó y cuántos días después de la salida.", 62,
              ["El itinerario está en la carta 66 y los husos horarios, en la 67.", "Pasad todo a una misma hora (la de Greenwich) para sumar sin líos: horas de vuelo y de escala. Luego, volved a la hora de Montecarlo.", f"Aterrizó {_S_HUS}."],
              SIN_GENTE + "Una caja de seguridad empotrada en la pared de un camarote de yate, con un teclado numérico con luz verde, junto a un reloj de pared y un billete de avión sobre un escritorio."),
    "66": gris("66", "El itinerario de Zorro", "El billete del Dr. Noche, con tres vuelos y sus escalas.", ["Es el itinerario del viaje (carta 64).", "Dice cuánto dura cada vuelo y cada escala.", "Los husos horarios están en la carta 67."]),
    "67": gris("67", "Los husos horarios", "Una tabla de husos horarios de cinco ciudades, respecto al meridiano de Greenwich.", ["Sirve para pasar la hora de una ciudad a otra (carta 64).", "Al este del meridiano, el sol sale antes.", "Montecarlo está en el mismo huso que Roma."]),
    "62": combinable("62", "El cristal del Cronoportal", "roja", 12, 74, "El cristal del Cronoportal, que el Dr. Noche guardaba en su caja de seguridad, rodeado de joyas.",
                     SIN_GENTE + "Un cristal redondo de color azul brillante, del tamaño de una moneda grande, con destellos de luz, sobre un cojín de terciopelo negro rodeado de collares de perlas, en una caja de seguridad abierta."),
    "74": escena("74", "Cronoportal con el cristal", [], [62, 12, 64, 66, 67, 94, 57],
                 "Encajáis el cristal en el pecho del Cronoportal y el anillo se enciende con un arco de luz azul. Fuera suenan las sirenas: el Neptuno está a punto de zarpar y solo falta la clave del teléfono rojo (carta 85).",
                 ["Ya solo queda marcar la clave del teléfono rojo."],
                 "Cristina y Alberto encajan un cristal azul brillante en el hueco del Cronoportal, un aparato de latón y cristal con un anillo que se enciende con un arco de luz azul, sobre la cama de un camarote de yate de lujo. Cristina lo sostiene con las dos manos con una enorme sonrisa; Alberto contiene el aliento mirando el anillo con la boca abierta."),
    "99": escena("99", "De vuelta a casa (FIN)", [], [74, 82, 85, 86, 87],
                 "La clave se marca y el teléfono rojo se queda en silencio: en el puerto, la policía rodea el Neptuno justo cuando el anillo del Cronoportal se abre en un arco de luz. Aterrizáis en vuestro salón. Alberto mira el aparato: «Mañana, otro destino». Cristina sonríe y guarda en el bolsillo un pequeño sello rosa del casino. FIN.",
                 [],
                 "La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ven un yate negro, las luces del puerto de Montecarlo y una sirena de policía a lo lejos. Llevan aún su ropa de espías elegantes de los años 60. Cristina ríe a carcajadas con un sello rosa en la mano y Alberto grita de euforia con los brazos en alto. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(juego="Montecarlo, 1965 — Operación Cristal", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()})

SPEC = dict(final="99", needs={
    "24": ["14", "16"], "28": ["20", "18", "19", "21"], "57": ["22", "35"], "30": ["40", "41", "43", "45"], "36": ["48", "42", "49", "53"],
    "44": ["52", "54", "55", "59"], "56": ["46", "37", "39", "33"], "58": ["51", "26", "61", "63"], "80": ["69", "70", "71"], "94": ["38", "56"],
    "62": ["64", "66", "67"], "82": ["72", "75", "79"], "74": ["12", "62"], "99": ["85", "86", "87", "74"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_T = [
    ("leer", "P", "Llegada", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12."),
    ("leer", "10", "El sobre de la Agente Zorro", "Lee la carta 10. Descarta la P y coge 14, 16, 18, 19, 20, 21 y 22. Junta el plano: 19 arriba y 21 abajo."),
    ("app", "14", "La nota de la Agente Zorro", f"En el móvil: Acción, 14. Con la nota (16), el mensaje es {_S_CRI}. El mensaje te dice que cojas la 24. Anota las pulsaciones del teléfono rojo: {I.PULSA['14']}.", "carta 24"),
    ("leer", "24", "Zorro en el muelle", "Lee la carta 24. Descarta 14 y 16 y coge la 26 (guárdala para los pasaportes)."),
    ("app", "20", "La persecución por Montecarlo", f"En el móvil: Acción, 20. Con el plano (19 y 21) y el acertijo (18), el camino más rápido es {_S_RUT}. El mensaje te dice que cojas la 28.", "carta 28"),
    ("leer", "28", "El Puerto", "Lee la carta 28. Descarta 18, 19, 20 y 21 y coge la 35."),
    ("combinar", "22", "35", "El microfilm completo", "Las dos mitades del microfilm (22 y 35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El microfilm completo", "Lee la carta 57. Descarta 22, 35, 10 y 28 y coge 31 y 32."),
    ("leer", "31", "La azotea del hotel", "Lee la carta 31. Coge 40, 41, 43 y 45."),
    ("app", "40", "El skyline del casino", f"En el móvil: Acción, 40. Con los números del borde (41 y 43) y la regla (45), el skyline por filas es {_S_RAS}. El mensaje te dice que cojas la 30. Anota las pulsaciones: {I.PULSA['40']}.", "carta 30"),
    ("leer", "30", "La trampilla de la azotea", "Lee la carta 30. Descarta 31, 40, 41, 43 y 45 y coge la 38."),
    ("leer", "32", "La biblioteca del casino", "Lee la carta 32. Coge 42, 48, 49 y 53."),
    ("app", "48", "La cifra del libro", f"En el móvil: Acción, 48. Con las páginas (42 y 49) y los números (53), el mensaje es {_S_LIB}. El mensaje te dice que cojas la 36.", "carta 36"),
    ("leer", "36", "La caja fuerte del joyero", "Lee la carta 36. Descarta 32, 42, 48, 49 y 53 y coge 52, 54, 55 y 59. Junta el tablero: 54 a la izquierda y 55 a la derecha."),
    ("app", "52", "La caja fuerte del joyero", f"En el móvil: Acción, 52. Con las jaulas (54 y 55) y la regla (59), la caja por filas es {_S_KEN}. El mensaje te dice que cojas la 44. Anota las pulsaciones: {I.PULSA['52']}.", "carta 44"),
    ("leer", "44", "La sala de juego", "Lee la carta 44. Descarta 36, 52, 54, 55 y 59 y coge 33, 37, 39, 46, 51, 61 y 63. Junta los pasaportes: 61 arriba y 63 abajo."),
    ("app", "46", "La cuenta del crupier", f"En el móvil: Acción, 46. Con las cartas (37 y 39) y la regla (33), la cuenta es {_S_CON}. El mensaje te dice que cojas la 56.", "carta 56"),
    ("app", "51", "Los pasaportes falsos", f"En el móvil: Acción, 51. Con los pasaportes (61 y 63) y la regla (26), los dígitos de control son {_S_PAS}. El mensaje te dice que cojas la 58. Anota las pulsaciones: {I.PULSA['51']}.", "carta 58"),
    ("leer", "58", "La aduana del puerto", "Lee la carta 58. Descarta 51, 61, 63, 26 y 24 y coge 69, 70 y 71."),
    ("app", "69", "El desactivador", f"En el móvil: Acción, 69. Con el manual (70 y 71), los cortes son {_S_CAB}. El mensaje te dice que cojas la 80. Anota las pulsaciones: {I.PULSA['69']}.", "carta 80"),
    ("leer", "80", "El salón privado del Dr. Noche", "Lee la carta 80. Descarta 58, 69, 70 y 71 y coge 72, 75 y 79."),
    ("app", "72", "La martingala", f"En el móvil: Acción, 72. Con los giros (75) y el sistema (79), el banco queda en {_S_RUL} fichas. El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "El yate Neptuno", "Lee la carta 82. Descarta 80, 72, 75 y 79 y coge 85, 86 y 87."),
    ("combinar", "38", "56", "La llave del camarote", "Las dos mitades de la llave (38 y 56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "El camarote del Dr. Noche", "Lee la carta 94. Descarta 38, 56, 30, 44, 33, 37, 39 y 46 y coge 64, 66 y 67."),
    ("app", "64", "El vuelo con escalas", f"En el móvil: Acción, 64. Con el itinerario (66) y los husos (67), el Dr. Noche aterrizó {_S_HUS}. El mensaje te dice que cojas la 62.", "carta 62"),
    ("combinar", "12", "62", "El cristal", "El Cronoportal (12) y el cristal (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "Cronoportal con el cristal", "Lee la carta 74. Descarta 62, 12, 64, 66, 67, 94 y 57."),
    ("app", "85", "El teléfono rojo", f"En el móvil: Acción, 85. Con el orden (86) y el teclado (87), las pulsaciones {_S_TEC} dan la palabra {I.PALABRA}. El mensaje te dice que cojas la 99.", "carta 99"),
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

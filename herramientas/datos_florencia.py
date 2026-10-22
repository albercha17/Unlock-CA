"""Florencia, 1503: El Taller de Leonardo — versión de 60 cartas (21 oct 2026), mucho más difícil y variada.

Once puzles de tipos que no salen en ningún otro juego de la serie, con las pistas dibujadas o en acertijo (ninguna carta explica cómo se
resuelve su puzle): una escítala (mensaje en una tira enrollada en una vara), un punto de fuga, un futoshiki, el recorrido del caballo, la
mezcla de tres pigmentos, un tren de engranajes con eje compartido, torres de vigía (conjunto dominante), una caja tipo Mastermind, un hidato,
un montacargas de poleas y el cifrado de Vigenère final con la clave de cuatro puzles. Solo 15 cartas tienen a Cristina y Alberto
(escenas); el resto son objetos y pistas sin personas. Las cartas-pista las dibuja herramientas/florencia.py (instancias_florencia.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402
import instancias_florencia as I  # noqa: E402

ESTILO = ("Pintura digital con aire de óleo renacentista y estética de película de aventuras, luz cálida de velas y lámparas de aceite, "
          "paleta de ocres, sepia, rojo bermellón y verde oliva, con destellos azules del Cronoportal, formato vertical 2:3. "
          "Sin texto, letras ni números en la imagen; los bocetos y planos son solo dibujos decorativos sin escritura legible. "
          "Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen.")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado, ojos azules. Lleva ropa florentina de 1503: vestido azul oscuro con corpiño ajustado y mangas de lino blanco, el pelo suelto con una cinta.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Lleva ropa florentina de 1503: camisa blanca, jubón marrón, calzas oscuras, capa corta y botas de cuero, con una bolsa de cuero cruzada."
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado, ojos azules, vestido florentino azul oscuro de 1503 con corpiño y mangas de lino blanco. "
        "Alberto: hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones, camisa blanca, jubón marrón, calzas oscuras, capa corta y botas de cuero. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con animación de estilo pintura renacentista de película de aventuras, luz cálida de velas y colores ocres y azul turquesa. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Cristina señala un cuadro de Florencia en su libro con una sonrisa emocionada. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul, el salón se deforma y los dos son absorbidos por un túnel de luz con destellos dorados. "
         "Escena 3 (8-12 s): caen sobre el suelo de madera de un taller renacentista de noche, lleno de maquetas, engranajes, espejos y un ornitóptero de madera colgado del techo; el aparato humea y se apaga. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, vestidos con ropa de la época, asombrados, mirando alrededor; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe sordo al aterrizar, crujidos de madera, tictac de relojes y música renacentista de laúd, sin voz de narrador.")

ESTILO += " Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes)."
SIN_GENTE = "Sin ninguna persona en la imagen. "

MOSAICOS = {
    "suelo": dict(filas=2, cols=1, cartas=["19", "21"], titulo="El suelo del taller"),
    "leon": dict(filas=1, cols=2, cartas=["41", "43"], titulo="El tablero del león"),
    "patio": dict(filas=1, cols=2, cartas=["42", "49"], titulo="El patio del taller"),
    "plazas": dict(filas=1, cols=2, cartas=["61", "63"], titulo="Las plazas de la ciudad"),
    "escalera": dict(filas=2, cols=1, cartas=["66", "67"], titulo="La escalera de caracol"),
}
POS = {(2, 1): ["mitad de arriba", "mitad de abajo"], (1, 2): ["mitad izquierda", "mitad derecha"]}
_c = lambda x, y: f"{'ABCDEF'[x]}{y + 1}"
_NCOL = ["rojo", "azul", "verde", "amarillo", "violeta", "blanco"]
_S_ESC = "El mensaje dice «LA CLAVE ES ALAS»: la palabra es ALAS"
_S_PER = f"El punto de fuga está en la casilla {_c(*I.PERSPECTIVA['solucion'])}"
_S_FUT = " / ".join("fila " + str(y + 1) + ": " + " ".join(str(v) for v in f) for y, f in enumerate(I.FUTOSHIKI["solucion"]))
_S_CAB = " → ".join(_c(x, y) for x, y in I.CABALLO["ruta"])
_S_PIG = f"{I.PIGMENTOS['solucion'][0]} cucharadas del pigmento I, {I.PIGMENTOS['solucion'][1]} del II y {I.PIGMENTOS['solucion'][2]} del III"
_S_ENG = f"{I.ENGRANAJES['solucion']['vueltas']} vueltas hacia la {I.ENGRANAJES['solucion']['sentido']}"
_S_VIG = "torres en las plazas " + ", ".join(str(i + 1) for i in I.VIGILANTES["soluciones"][0])
_S_MAS = ", ".join(_NCOL[c] for c in I.MASTERMIND["solucion"])


def _grid_hidato():
    n = I.HIDATO["n"]
    g = [[0] * n for _ in range(n)]
    for i, (x, y) in enumerate(I.HIDATO["camino"]):
        g[y][x] = i + 1
    return " / ".join("fila " + str(y + 1) + ": " + " ".join(str(v) for v in f) for y, f in enumerate(g))


_S_HID = _grid_hidato()
_S_POL = f"El aparejo n.º {I.POLEAS['solucion'] + 1} (el de {I.POLEAS['sistemas'][I.POLEAS['solucion']]} cuerdas)"
_S_CIF = f"La clave SOLE (S de los pigmentos, O de las poleas, L de la caja de colores y E del caballo) da la palabra {I.CLARO}"


def codigo(que):
    return f"Carta dibujada por código (herramientas/florencia.py; no se pide a ChatGPT): {que}."


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
    # ------------------------------------------------------------------ El taller
    "P": escena("P", "Llegada al taller", [10, 12], [],
                "Tercer salto del Cronoportal: Florencia, año 1503. Cristina siempre ha soñado con ver el taller de Leonardo da Vinci. El salto vuelve a salir mal: aterrizáis de noche en el taller del maestro, que está fuera, y el aparato se queda sin energía. Alberto calcula que solo hay una forma de recargarlo: concentrar con una lente perfecta la primera luz del amanecer, que llegará dentro de hora y media.",
                ["Mirad a vuestro alrededor y revisad el aparato."],
                "El taller de Leonardo da Vinci de noche, a la luz de unas pocas velas, con maquetas, engranajes, espejos y un ornitóptero de madera colgado del techo. En el suelo, un aparato de latón y cristal (el Cronoportal) humea y se apaga. Cristina, con vestido florentino azul oscuro, mira alrededor con los ojos brillantes de emoción y las manos en el pecho; Alberto, con jubón marrón y capa corta, se sujeta la cabeza con una mueca de mareo."),
    "10": escena("10", "El taller de Leonardo", [14, 16, 18, 19, 20, 21, 22], ["P"],
                 "El taller está lleno de inventos a medio hacer. Sobre una mesa hay un cofre del maestro con una tira de cuero cosida a la tapa, llena de letras. En el suelo, el maestro dejó pintada una cuadrícula de perspectiva con unas rectas que se pierden hacia el fondo, y junto a ella, partido en dos, un compás de bronce.",
                 ["Hay dos puzles: el cofre y el suelo de la perspectiva.", "El suelo son dos cartas: juntadlas, una encima de otra."],
                 "El taller de Leonardo da Vinci con un cofre de madera sobre una mesa con una tira de cuero cosida a la tapa, y en el suelo una cuadrícula pintada con rectas que se juntan a lo lejos. Cristina toca la tira de cuero con una ceja arqueada de curiosidad y Alberto se agacha sobre las rectas del suelo con un dedo apoyado en los labios, pensativo."),
    "12": combinable("12", "Cronoportal sin energía", "azul", 62, 74,
                     "El Cronoportal con el anillo central apagado y sin su fuente de energía.",
                     SIN_GENTE + "Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo central apagado y un hueco circular vacío en el pecho del aparato, sobre una mesa de taller renacentista con virutas de madera."),
    "14": app("14", "El cofre del maestro", "Es un juego de la app: el cofre se abre con la palabra que esconde la tira de cuero de la tapa.", 24,
              ["La tira, y la vara de cuatro caras, en la carta 16.", "Leonardo escribió el mensaje enrollando la tira en una vara de cuatro caras y poniendo las letras a lo largo de la vara. Probad a volver a enrollarla: colocad las letras en cuatro columnas.", f"{_S_ESC}."],
              SIN_GENTE + "Un cofre de madera con herrajes de bronce sobre una mesa de taller, con una tira de cuero cosida a la tapa y una cerradura con letras."),
    "16": gris("16", "La tira del cofre", "La tira de cuero cosida a la tapa del cofre, y la vara del maestro vista de punta.",
               ["Sirve para el cofre (carta 14).", "La vara tiene cuatro caras: la tira se escribió enrollada en ella.", f"{_S_ESC}."], codigo("la tira de cuero y la vara")),
    "18": gris("18", "El acertijo del perspectivo", "Un acertijo del maestro pegado en el bastidor.",
               ["Sirve para el punto de fuga (carta 20).", "Alargad las rectas hasta que se encuentren.", f"{_S_PER}."], codigo("el acertijo del perspectivo")),
    "19": pieza("19", "suelo", "Media lámina del suelo del taller.", ["Es la mitad de una lámina: juntadla con la carta 21.", "Las rectas empiezan en la lámina de abajo y suben hacia la de arriba.", f"{_S_PER}."]),
    "21": pieza("21", "suelo", "Media lámina del suelo del taller.", ["Es la mitad de una lámina: juntadla con la carta 19.", "Las rectas empiezan en la lámina de abajo y suben hacia la de arriba.", f"{_S_PER}."]),
    "20": app("20", "El punto de fuga", "Es un juego de la app: marcar la casilla de la cuadrícula del suelo donde se juntan todas las rectas.", 28,
              ["El suelo, con la cuadrícula, son las cartas 19 y 21; el acertijo, la 18.", "Con una regla, alargad cada recta hacia arriba por encima del corte entre las dos láminas. Todas pasan por el mismo punto.", f"{_S_PER}."],
              SIN_GENTE + "El suelo de madera de un taller renacentista con una cuadrícula pintada y varias rectas que se pierden hacia el fondo."),
    "22": combinable("22", "Mitad de compás", "azul", 35, 57, "Una mitad de un compás de bronce con la punta de plata.",
                     SIN_GENTE + "La mitad de un compás de bronce de dibujo, con la punta de plata, sobre una mesa de taller renacentista."),
    "24": escena("24", "El cofre abierto", [26], [14, 16],
                 "La tapa se levanta con un chasquido y dentro hay pergaminos, plumas y un cuaderno de tapas de cuero con la letra de Leonardo, escrita al revés, de derecha a izquierda. Alberto lo acerca a una vela: es el plano de las plazas de Florencia, con un acertijo sobre torres de vigía.",
                 ["El cuaderno del maestro servirá más adelante."],
                 "Un cofre de madera abierto con pergaminos, plumas y un cuaderno de tapas de cuero con una escritura al revés. Alberto sostiene el cuaderno frente a un espejo de mano con los ojos muy abiertos de asombro y Cristina se asoma por encima de su hombro con la boca entreabierta."),
    "26": gris("26", "El cuaderno de Leonardo", "Una página del cuaderno de Leonardo, escrita al revés.",
               ["Sirve para las torres de vigía (carta 51).", "Una torre vigila su plaza y las plazas con calle directa. Buscad el menor número de torres.", f"{_S_VIG}."], codigo("el cuaderno de Leonardo")),
    "28": escena("28", "El suelo hundido", [35], [18, 19, 20, 21],
                 "Las rectas del suelo se encuentran y una losa se hunde con un crujido, dejando ver una cavidad con un nicho. Dentro, sobre un cojín de terciopelo, la otra mitad del compás de bronce.",
                 ["Lo que habéis encontrado se puede juntar con algo que ya tenéis."],
                 "El suelo de madera de un taller renacentista con una losa hundida que deja ver una cavidad con un nicho. Alberto saca la otra mitad de un compás de bronce con mucho cuidado, la lengua entre los dientes, y Cristina sujeta una vela con gesto maravillado."),
    "35": combinable("35", "Otra mitad de compás", "roja", 22, 57, "La otra mitad del compás de bronce, con un eje de plata.",
                     SIN_GENTE + "La otra mitad de un compás de bronce de dibujo, con un eje de plata, sobre un cojín de terciopelo rojo en un nicho."),
    "57": escena("57", "El compás de Leonardo", [31, 32], [22, 35, 10, 28],
                 "Las dos mitades se unen y el compás se abre solo, dibujando en el aire un arco de luz. En la pared del taller aparecen dos puertas: una lleva al león mecánico, el autómata del maestro; la otra, al patio, donde hay un tablero de ajedrez tallado en las losas. Hay que cruzar las dos.",
                 ["Hay dos caminos: el león mecánico y el patio de ajedrez. Podéis seguir los dos."],
                 "Un taller renacentista con un compás de bronce completo apoyado en una mesa, del que sale un arco de luz dorada, y dos puertas recién abiertas en la pared. Cristina sostiene el compás en alto con una sonrisa de triunfo; Alberto mira las dos puertas alternativamente con las cejas muy altas."),
    # ------------------------------------------------------------------ Rama 1: el león mecánico
    "31": escena("31", "El león mecánico", [40, 41, 43, 45], [],
                 "Un león de madera y bronce del tamaño de un caballo vigila una sala. Su pecho es un tablero de cinco por cinco con signos de desigualdad grabados: la boca del león solo se abre si se rellena. El tablero son dos láminas.",
                 ["El tablero son dos cartas: juntadlas."],
                 SIN_GENTE + "Un gran león mecánico de madera y bronce en una sala de taller renacentista, con un tablero cuadrado de casillas con signos grabado en el pecho."),
    "40": app("40", "El tablero del león", "Es un juego de la app: rellenar el tablero del pecho del león con los números del 1 al 5, respetando los signos.", 30,
              ["El tablero, con los signos, está en las cartas 41 y 43; el acertijo, en la 45.", "Cada signo señala hacia la casilla menor. Empezad por una casilla con muchos signos a su alrededor.", f"El tablero: {_S_FUT}."],
              SIN_GENTE + "Un tablero cuadrado de casillas vacías en el pecho de un león mecánico de bronce."),
    "41": pieza("41", "leon", "Media lámina del tablero del león.", ["Es la mitad de un tablero: juntadla con la carta 43.", "Hay signos de desigualdad entre casillas vecinas.", f"El tablero: {_S_FUT}."]),
    "43": pieza("43", "leon", "Media lámina del tablero del león.", ["Es la mitad de un tablero: juntadla con la carta 41.", "Hay signos de desigualdad entre casillas vecinas.", f"El tablero: {_S_FUT}."]),
    "45": gris("45", "El acertijo del león", "Un acertijo grabado en la base del león.",
               ["Sirve para el tablero (carta 40).", "El pico de cada signo señala la casilla de menor número.", f"El tablero: {_S_FUT}."], codigo("el acertijo del león")),
    "30": escena("30", "Las fauces del león", [38], [31, 40, 41, 43, 45],
                 "El león abre las fauces con un rugido de engranajes. En su interior, entre dientes de bronce, hay una lámpara de aceite de plata sin mecha: la lámpara con la que Leonardo ilumina las lentes del sótano.",
                 ["A la lámpara le falta una mecha."],
                 "Un león mecánico de madera y bronce con las fauces abiertas, y en su interior una lámpara de aceite de plata entre los dientes. Alberto mete el brazo con cara de pánico fingido y Cristina se tapa la boca para no reírse."),
    "38": combinable("38", "Lámpara sin mecha", "roja", 56, 94, "Una lámpara de aceite de plata, llena de aceite pero sin mecha.",
                     SIN_GENTE + "Una lámpara de aceite de plata con el depósito lleno y sin mecha, sobre un banco de taller renacentista."),
    # ------------------------------------------------------------------ Rama 2: el patio de ajedrez
    "32": escena("32", "El patio de ajedrez", [42, 48, 49, 53], [],
                 "El patio tiene las losas pintadas como un tablero de ajedrez, con algunas casillas tachadas con carbón. En una esquina, la estatua de un caballo de bronce. Leonardo dejó escrito en el muro que quien recorra el patio con los saltos del caballo, pisando todas las casillas libres, abrirá la puerta del fondo. El patio son dos láminas.",
                 ["El patio son dos cartas: juntadlas."],
                 "Un patio de un taller renacentista con las losas pintadas como un tablero de ajedrez, algunas casillas tachadas con carbón, y una estatua de un caballo de bronce en una esquina. Cristina salta de una casilla a otra con los brazos extendidos para no perder el equilibrio y Alberto la observa con los brazos cruzados y una sonrisa divertida."),
    "48": app("48", "El patio de ajedrez", "Es un juego de la app: recorrer el patio con saltos de caballo, pisando una vez cada casilla libre.", 36,
              ["El patio, con las casillas tachadas y la casilla de salida, son las cartas 42 y 49; el acertijo, la 53.", "Empezad por las casillas con pocas salidas posibles: las de las esquinas y las pegadas a una tachada. Después seguid el hilo.", f"Un recorrido que vale: {_S_CAB}."],
              SIN_GENTE + "Un patio de un taller renacentista con las losas pintadas como un tablero de ajedrez y la estatua de un caballo de bronce."),
    "42": pieza("42", "patio", "Media lámina del patio del taller.", ["Es la mitad de un plano: juntadla con la carta 49.", "Las casillas tachadas no se pisan; el caballo marca la salida.", f"Un recorrido que vale: {_S_CAB}."]),
    "49": pieza("49", "patio", "Media lámina del patio del taller.", ["Es la mitad de un plano: juntadla con la carta 42.", "Las casillas tachadas no se pisan; el caballo marca la salida.", f"Un recorrido que vale: {_S_CAB}."]),
    "53": gris("53", "El acertijo del caballo", "Un acertijo pintado en el muro del patio.",
               ["Sirve para el patio (carta 48).", "El caballo salta dos casillas en recto y una de lado.", f"Un recorrido que vale: {_S_CAB}."], codigo("el acertijo del caballo")),
    "36": escena("36", "El altillo de los pintores", [52, 54, 55, 59], [32, 42, 48, 49, 53],
                 "La puerta del fondo del patio lleva a un altillo donde los aprendices muelen pigmentos. Sobre una mesa hay tres frascos y un cuadro a medio pintar: el color del maestro, un tono que Leonardo inventó mezclando los tres. Hay que repetirlo.",
                 ["La paleta son varias cartas."],
                 "Un altillo de pintores de un taller renacentista con una mesa con tres frascos de pigmentos, pinceles y un cuadro a medio pintar. Cristina remueve un frasco con un pincel con gesto concentrado y Alberto compara el color de la mezcla con el del cuadro con los ojos entornados."),
    "52": app("52", "La paleta de Leonardo", "Es un juego de la app: decir cuántas cucharadas de cada pigmento hay que mezclar para conseguir el color del maestro.", 44,
              ["Lo que lleva cada pigmento, en la carta 54; el color que se quiere, en la 55; el acertijo, en la 59.", "Cada pigmento aporta gotas de rojo, de amarillo y de azul por cucharada. Probad con un solo color de gotas y con lo que cada pigmento ofrece.", f"La mezcla: {_S_PIG}."],
              SIN_GENTE + "Una mesa de pintor con tres frascos de cristal de pigmentos, una cuchara y una paleta de madera."),
    "54": gris("54", "Los tres pigmentos", "Los tres pigmentos y las gotas de cada color que lleva una cucharada de cada uno.",
               ["Sirve para la paleta (carta 52).", "Contad las gotas de rojo, amarillo y azul de cada pigmento.", f"La mezcla: {_S_PIG}."], codigo("los tres pigmentos")),
    "55": gris("55", "El color del maestro", "Las gotas de rojo, amarillo y azul que tiene el color del maestro.",
               ["Sirve para la paleta (carta 52).", "La mezcla debe sumar exactamente esas gotas.", f"La mezcla: {_S_PIG}."], codigo("el color del maestro")),
    "59": gris("59", "El acertijo de la paleta", "Un acertijo escrito en el cajón de la paleta.",
               ["Sirve para la paleta (carta 52).", "Se echan cucharadas enteras de los tres pigmentos.", f"La mezcla: {_S_PIG}."], codigo("el acertijo de la paleta")),
    # ------------------------------------------------------------------ La biblioteca
    "44": escena("44", "El estudio de Leonardo", [33, 37, 39, 46, 51, 61, 63], [36, 52, 54, 55, 59],
                 "El color seca y la pared del altillo se desliza: es el estudio de Leonardo, con estantes de libros, un gran reloj mecánico sin dar la hora y un plano de la ciudad. El reloj no marca la hora hasta que se averigüe cuánto gira una de sus ruedas, y el plano guarda un acertijo sobre las plazas. Tenéis dos encargos.",
                 ["Hay dos puzles: el reloj de ruedas y las torres de vigía. El cuaderno de Leonardo sirve aquí."],
                 "El estudio de Leonardo da Vinci con estantes de libros, un gran reloj mecánico de engranajes de bronce y un plano de la ciudad en la pared. Cristina observa los engranajes del reloj con la cabeza ladeada, curiosa, y Alberto sigue con el dedo las calles del plano con el ceño fruncido."),
    "46": app("46", "El reloj del taller", "Es un juego de la app: saber cuántas vueltas da la última rueda del reloj y hacia dónde, cuando se gira la manivela.", 56,
              ["El tren de ruedas, en la carta 37; la manivela, en la 39; el acertijo, en la 33.", "Cada par de ruedas que se tocan reparte las vueltas según los dientes; las que comparten eje giran igual. Contad los dientes de cada rueda.", f"Solución: {_S_ENG}."],
              SIN_GENTE + "Un reloj mecánico de engranajes de bronce con una manivela en un lateral, en un estudio renacentista."),
    "37": gris("37", "El tren de ruedas", "Las cuatro ruedas del reloj, con sus dientes.",
               ["Sirve para el reloj (carta 46).", "Contad los dientes de cada rueda.", f"Solución: {_S_ENG}."], codigo("el tren de engranajes")),
    "39": gris("39", "La manivela", "La manivela de la rueda A: cuántas vueltas y hacia dónde.",
               ["Sirve para el reloj (carta 46).", "Es lo que se gira de la rueda A.", f"Solución: {_S_ENG}."], codigo("la manivela")),
    "33": gris("33", "El acertijo del reloj", "Un acertijo grabado en el cárter del reloj.",
               ["Sirve para el reloj (carta 46).", "Ruedas que se tocan giran al revés; ruedas con un mismo eje giran juntas.", f"Solución: {_S_ENG}."], codigo("el acertijo del reloj")),
    "56": combinable("56", "Mecha de lino", "roja", 38, 94, "Una mecha de lino trenzado que cae de un hueco del reloj al marcar la hora.",
                     SIN_GENTE + "Una mecha de lino trenzado sobre una bandeja de plata junto a un reloj mecánico de engranajes."),
    "51": app("51", "Las torres de vigía", "Es un juego de la app: elegir en qué plazas levantar torres de vigía para que toda la ciudad quede vigilada con las menos posibles.", 58,
              ["El plano de las plazas son las cartas 61 y 63; el cuaderno de Leonardo, la 26.", "Una torre cubre su plaza y las vecinas por calle. Una plaza sin calles solo la cubre una torre propia. Probad con tres torres.", f"Una solución: {_S_VIG}."],
              SIN_GENTE + "El plano de una ciudad renacentista con plazas circulares unidas por calles, y pequeñas torres de vigía dibujadas encima de algunas."),
    "61": pieza("61", "plazas", "Media lámina del plano de las plazas.", ["Es la mitad de un plano: juntadla con la carta 63.", "Las plazas están numeradas y las líneas son calles.", f"Una solución: {_S_VIG}."]),
    "63": pieza("63", "plazas", "Media lámina del plano de las plazas.", ["Es la mitad de un plano: juntadla con la carta 61.", "Las plazas están numeradas y las líneas son calles.", f"Una solución: {_S_VIG}."]),
    "58": escena("58", "El permiso del Gonfaloniere", [69, 70, 71], [51, 61, 63, 26, 24],
                 "El Gonfaloniere, que miraba por la ventana, se sobresalta al veros: «¿Los de las torres? ¡Pasad!». Os deja pasar a su despacho, donde un aprendiz de Leonardo ha dejado una caja de pigmentos cerrada con cuatro colores. Sus intentos de abrirla están anotados en la tapa.",
                 ["Hay una caja de colores que abrir."],
                 "El despacho de un gobernante florentino con una gran ventana, un escritorio con una caja de madera cerrada y un hombre de gorro rojo y túnica oscura que sonríe. Cristina recibe un permiso sellado con una sonrisa radiante y Alberto se inclina con una reverencia exagerada y una ceja levantada."),
    "69": app("69", "La caja de pigmentos", "Es un juego de la app: la caja se abre con cuatro pigmentos de colores distintos en cierto orden.", 80,
              ["Los intentos del aprendiz y lo que acertó cada uno, en la carta 70; los seis pigmentos y la norma, en la 71.", "Un círculo negro es un color bien colocado; uno blanco, un color que está pero en otro sitio. Id descartando colores con los intentos.", f"El orden: {_S_MAS}."],
              SIN_GENTE + "Una caja de madera de pintor con cuatro huecos redondos en la tapa y seis frascos de pigmentos de colores alrededor."),
    "70": gris("70", "Los intentos del aprendiz", "Los intentos anotados en la tapa de la caja, con los aciertos de cada uno.",
               ["Sirve para la caja de pigmentos (carta 69).", "Cada fila es un intento; a la derecha, los aciertos.", f"El orden: {_S_MAS}."], codigo("los intentos de la caja")),
    "71": gris("71", "Los seis pigmentos", "Los seis pigmentos y lo que significan los aciertos.",
               ["Sirve para la caja de pigmentos (carta 69).", "Los cuatro pigmentos de la clave son distintos.", f"El orden: {_S_MAS}."], codigo("los seis pigmentos")),
    "80": escena("80", "El almacén de Leonardo", [72, 75, 79], [58, 69, 70, 71],
                 "La caja se abre y dentro hay una llave del almacén de Leonardo, en lo alto de una torre del taller. Allí guarda lo más pesado: lentes de cristal enormes, y para subirlas hay un montacargas de cuerdas. Hay que elegir el aparejo adecuado.",
                 ["El montacargas es de poleas."],
                 "El almacén de un taller renacentista con grandes lentes de cristal sobre mesas, poleas colgadas del techo y cuerdas enrolladas. Alberto tira de una cuerda con esfuerzo, la cara roja y los dientes apretados, y Cristina contempla una enorme lente con una sonrisa de asombro."),
    "72": app("72", "El montacargas", "Es un juego de la app: elegir el aparejo de poleas que alza la carga con lo que aguanta la mano y gasta la menor cuerda.", 82,
              ["Los cuatro aparejos, en la carta 75; la carga y lo que aguanta la mano, en la 79.", "Contad las cuerdas que sostienen el peso en el bloque de abajo: el peso se reparte entre ellas.", f"{_S_POL}."],
              SIN_GENTE + "Un montacargas de cuerdas y poleas de madera y bronce colgando del techo de un almacén renacentista, con un barril como carga."),
    "75": gris("75", "Los cuatro aparejos", "Los cuatro aparejos de poleas del almacén.",
               ["Sirve para el montacargas (carta 72).", "Contad las cuerdas que bajan al bloque de abajo.", f"{_S_POL}."], codigo("los cuatro aparejos")),
    "79": gris("79", "La carga y la mano", "Lo que pesa la carga y lo que aguanta la mano.",
               ["Sirve para el montacargas (carta 72).", "El peso se reparte entre las cuerdas que lo sostienen.", f"{_S_POL}."], codigo("la carga y la mano")),
    "82": escena("82", "El lucernario", [85, 86, 87], [80, 72, 75, 79],
                 "El montacargas os sube a lo más alto del taller, bajo el lucernario: una ventana cenital con un cristal en el que Leonardo escribió algo con letras de colores. Falta poco para el amanecer. Sobre una mesa, una tabla muy rara.",
                 ["El lucernario es el último puzle."],
                 "La estancia más alta de un taller renacentista, con un lucernario de cristal en el techo por el que entra una luz azul de madrugada, y una mesa con pergaminos. Cristina mira el cristal con los ojos muy abiertos y una sonrisa nerviosa, y Alberto compara dos pergaminos con las cejas fruncidas."),
    "85": app("85", "El lucernario", "Es un juego de la app: el mensaje del cristal está cifrado con una clave de cuatro letras, una de cada uno de cuatro puzles.", 99,
              ["El mensaje, con el acertijo de la clave, es la carta 86; la tabla, la 87.", "Cada puzle del acertijo dejó una letra al resolverse. Con la clave, cada letra del mensaje se corrige según la letra de la clave que le toca, repitiéndola.", f"{_S_CIF}."],
              SIN_GENTE + "Un lucernario circular en el techo de un taller con un cristal en el que se ven ocho letras de colores y, debajo, una mesa con un papiro."),
    "86": gris("86", "El mensaje del lucernario", "El mensaje del cristal, y el acertijo de la clave.",
               ["Sirve para el lucernario (carta 85).", "La clave se forma con las letras de cuatro puzles, en el orden del acertijo.", f"{_S_CIF}."], codigo("el mensaje del lucernario")),
    "87": gris("87", "La tabla del cifrador", "Una tabla de veintiséis filas y columnas de letras.",
               ["Sirve para el lucernario (carta 85).", "Cada letra del mensaje se busca en la fila de la letra de la clave que le toca.", f"{_S_CIF}."], codigo("la tabla de Vigenère")),
    # ------------------------------------------------------------------ El sótano y el final
    "94": escena("94", "El sótano de las lentes", [64, 66, 67], [38, 56, 30, 44, 33, 37, 39, 46],
                 "La mecha prende en la lámpara y la luz baja por una escalera hasta el sótano donde Leonardo pule sus lentes. La escalera, de caracol, tiene los peldaños numerados con pintura, pero faltan números: solo se baja pisando los peldaños seguidos en orden.",
                 ["La escalera son dos cartas: juntadlas."],
                 "Una escalera de caracol de piedra que baja a un sótano oscuro de un taller renacentista, iluminada por una lámpara de aceite de plata, con peldaños numerados con pintura. Cristina sostiene la lámpara con gesto cauteloso y Alberto pisa un peldaño con la punta del pie, tanteando con cara de duda."),
    "64": app("64", "La escalera de caracol", "Es un juego de la app: numerar los peldaños del 1 al 25 en un camino sin saltos, respetando los números que ya están puestos.", 62,
              ["Los números ya puestos, en las cartas 66 y 67 (dos mitades). Cada número está pegado al siguiente, también en diagonal.", "Uníos desde los números que ya están: ¿qué peldaños están entre el 2 y el 14? Probad los caminos más cortos.", f"El camino: {_S_HID}."],
              SIN_GENTE + "Una escalera de caracol de piedra vista desde arriba como un cuadrado de peldaños numerados con pintura blanca, algunos sin número."),
    "66": pieza("66", "escalera", "Media lámina de la escalera de caracol.", ["Es la mitad de una lámina: juntadla con la carta 67.", "Los peldaños con número ya están puestos.", f"El camino: {_S_HID}."]),
    "67": pieza("67", "escalera", "Media lámina de la escalera de caracol.", ["Es la mitad de una lámina: juntadla con la carta 66.", "Los peldaños con número ya están puestos.", f"El camino: {_S_HID}."]),
    "62": combinable("62", "Lente maestra", "roja", 12, 74, "La lente maestra de Leonardo: un cristal perfecto, pulido durante años, del tamaño de un plato.",
                     SIN_GENTE + "Una enorme lente de cristal perfecto del tamaño de un plato, sobre un cojín de terciopelo azul, reflejando la luz de una lámpara de aceite en un sótano."),
    "74": escena("74", "Cronoportal con la lente", [], [62, 12, 64, 66, 67, 94, 57],
                 "La lente maestra encaja en el pecho del Cronoportal. Solo falta la luz del amanecer, y ya asoma por el horizonte: hay que dejar que entre por el lucernario... pero el cristal del lucernario, cifrado, está tapado con un mensaje de Leonardo que solo se enciende con su palabra.",
                 ["Falta descifrar el lucernario."],
                 "El Cronoportal con una lente enorme encajada en el pecho, en el sótano de un taller renacentista iluminado por una lámpara. Alberto ajusta las antenas del aparato con la lengua entre los dientes y Cristina, a su lado, mira hacia arriba con una sonrisa expectante."),
    "99": escena("99", "De vuelta a casa (FIN)", [], [74, 82, 85, 86, 87],
                 "La palabra enciende el cristal, el primer rayo del alba cruza la lente y el Cronoportal despierta con un destello dorado. Se abre el portal justo cuando se oyen los pasos de Leonardo en la escalera. Cristina deja sobre la mesa una nota de agradecimiento, escrita al revés. Aterrizáis en vuestro salón. Alberto mira el aparato: «Mañana, otro destino». Cristina sonríe. FIN.",
                 [],
                 "La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ven el taller de Leonardo y una mesa con inventos. Llevan aún su ropa florentina. Cristina ríe con las manos en la boca, emocionada; Alberto mira el aparato con una sonrisa cansada y satisfecha. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(juego="Florencia, 1503 — El Taller de Leonardo", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()})

SPEC = dict(final="99", needs={
    "24": ["14", "16"], "28": ["20", "18", "19", "21"], "57": ["22", "35"], "30": ["40", "41", "43", "45"], "36": ["48", "42", "49", "53"],
    "44": ["52", "54", "55", "59"], "56": ["46", "37", "39", "33"], "58": ["51", "26", "61", "63"], "80": ["69", "70", "71"], "94": ["38", "56"],
    "62": ["64", "66", "67"], "82": ["72", "75", "79"], "74": ["12", "62"], "99": ["85", "86", "87", "74"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_T = [
    ("leer", "P", "Llegada", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12."),
    ("leer", "10", "El taller", "Lee la carta 10. Descarta la P y coge 14, 16, 18, 19, 20, 21 y 22. Junta el suelo: 19 arriba y 21 abajo."),
    ("app", "14", "El cofre del maestro", f"En el móvil: Acción, 14. La tira (16) enrollada en una vara de cuatro caras: {_S_ESC}. El mensaje te dice que cojas la 24.", "carta 24"),
    ("leer", "24", "El cofre abierto", "Lee la carta 24. Descarta 14 y 16 y coge la 26 (guárdala para las plazas)."),
    ("app", "20", "El punto de fuga", f"En el móvil: Acción, 20. Alargando las rectas del suelo (18, 19 y 21): {_S_PER}. El mensaje te dice que cojas la 28.", "carta 28"),
    ("leer", "28", "El suelo hundido", "Lee la carta 28. Descarta 18, 19, 20 y 21 y coge la 35."),
    ("combinar", "22", "35", "El compás", "Las dos mitades del compás (22 y 35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El compás de Leonardo", "Lee la carta 57. Descarta 22, 35, 10 y 28 y coge 31 y 32."),
    ("leer", "31", "El león mecánico", "Lee la carta 31. Coge 40, 41, 43 y 45. Junta el tablero: 41 a la izquierda y 43 a la derecha."),
    ("app", "40", "El tablero del león", f"En el móvil: Acción, 40. Con los signos (41, 43 y 45): {_S_FUT}. El mensaje te dice que cojas la 30.", "carta 30"),
    ("leer", "30", "Las fauces del león", "Lee la carta 30. Descarta 31, 40, 41, 43 y 45 y coge la 38."),
    ("leer", "32", "El patio de ajedrez", "Lee la carta 32. Coge 42, 48, 49 y 53. Junta el patio: 42 a la izquierda y 49 a la derecha."),
    ("app", "48", "El patio", f"En el móvil: Acción, 48. Con el patio (42 y 49) y el acertijo (53): {_S_CAB}. El mensaje te dice que cojas la 36. Anota la letra de la clave: E.", "carta 36"),
    ("leer", "36", "El altillo", "Lee la carta 36. Descarta 32, 42, 48, 49 y 53 y coge 52, 54, 55 y 59."),
    ("app", "52", "La paleta", f"En el móvil: Acción, 52. Con los pigmentos (54), el color (55) y el acertijo (59): {_S_PIG}. El mensaje te dice que cojas la 44. Anota la letra de la clave: S.", "carta 44"),
    ("leer", "44", "El estudio de Leonardo", "Lee la carta 44. Descarta 36, 52, 54, 55 y 59 y coge 33, 37, 39, 46, 51, 61 y 63. Junta el plano: 61 a la izquierda y 63 a la derecha."),
    ("app", "46", "El reloj", f"En el móvil: Acción, 46. Con el tren (37), la manivela (39) y el acertijo (33): {_S_ENG}. El mensaje te dice que cojas la 56.", "carta 56"),
    ("app", "51", "Las torres de vigía", f"En el móvil: Acción, 51. Con el plano (61 y 63) y el cuaderno (26): {_S_VIG}. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "El permiso del Gonfaloniere", "Lee la carta 58. Descarta 51, 61, 63, 26 y 24 y coge 69, 70 y 71."),
    ("app", "69", "La caja de pigmentos", f"En el móvil: Acción, 69. Con los intentos (70) y la norma (71): {_S_MAS}. El mensaje te dice que cojas la 80. Anota la letra de la clave: L.", "carta 80"),
    ("leer", "80", "El almacén de Leonardo", "Lee la carta 80. Descarta 58, 69, 70 y 71 y coge 72, 75 y 79."),
    ("app", "72", "El montacargas", f"En el móvil: Acción, 72. Con los aparejos (75) y la carga (79): {_S_POL}. El mensaje te dice que cojas la 82. Anota la letra de la clave: O.", "carta 82"),
    ("leer", "82", "El lucernario", "Lee la carta 82. Descarta 80, 72, 75 y 79 y coge 85, 86 y 87."),
    ("combinar", "38", "56", "La lámpara", "La lámpara (38) y la mecha (56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "El sótano de las lentes", "Lee la carta 94. Descarta 38, 56, 30, 44, 33, 37, 39 y 46 y coge 64, 66 y 67. Junta la escalera: 66 arriba y 67 abajo."),
    ("app", "64", "La escalera de caracol", f"En el móvil: Acción, 64. Con los números puestos (66 y 67): {_S_HID}. El mensaje te dice que cojas la 62.", "carta 62"),
    ("combinar", "12", "62", "La lente", "El Cronoportal (12) y la lente maestra (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "Cronoportal con la lente", "Lee la carta 74. Descarta 62, 12, 64, 66, 67, 94 y 57."),
    ("app", "85", "El lucernario", f"En el móvil: Acción, 85. Con el mensaje (86) y la tabla (87): {_S_CIF}. El mensaje te dice que cojas la 99.", "carta 99"),
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

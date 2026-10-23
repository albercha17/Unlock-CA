"""Pompeya, 79 d.C.: El Mosaico del Mundo — versión de 60 cartas (20 oct 2026), mucho más difícil y variada que la primera.

Diez puzles de tipos distintos, con las pistas como acertijos o dibujadas (ninguna carta explica cómo se resuelve su puzle): el mosaico laberinto
del atrio, las cuentas en números romanos, el sello del anillo, la fuente del jardín, el cuadrado SATOR, la balanza romana, los grafitis y el
plano de la manzana, el calendario romano, la huida por las calles y la carga de la barca. Solo 15 cartas tienen a Cristina y Alberto (escenas);
el resto son objetos y pistas sin personas. Las cartas-pista las dibuja herramientas/pompeya.py (instancias_pompeya.json)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402

INST = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_pompeya.json"), encoding="utf-8"))
LAB, CU, SE, FU, SA, ST, CA, CAL, HU, BA = (INST[k] for k in ("laberinto", "cuentas", "sello", "fuente", "sator", "statera", "calles",
                                                              "calendario", "huida", "barca"))
FIG = {"delfin": "delfín", "anfora": "ánfora", "laurel": "laurel", "lechuza": "lechuza", "racimo": "racimo", "concha": "concha",
       "lucerna": "lucerna", "escudo": "escudo"}
NOM_H = {"F": "foro", "A": "templo", "B": "termas", "C": "teatro", "D": "mercado", "E": "lupanar", "G": "anfiteatro", "P": "puerto"}
NOM_B = {"anfora_aceite": "ánfora de aceite", "anfora_vino": "ánfora de vino", "fardo_lana": "fardo de lana", "cofre_monedas": "cofre de monedas",
         "estatua_lar": "estatua del lar", "saco_trigo": "saco de trigo"}
_S_LAB = ", ".join(FIG[f] for f in LAB["solucion"])
_S_FU = ", ".join(FU["solucion"])
_S_FU_CERR = ", ".join(c for c in FU["compuertas"] if c not in FU["solucion"])
_S_CASA = f"la casa de la fila {CA['solucion'][0] + 1} (de norte a sur) y la columna {CA['solucion'][1] + 1} (de oeste a este)"
_S_HU = " → ".join(NOM_H[n] for n in HU["solucion"])
_S_BA = ", ".join(NOM_B[x] for x in BA["solucion"])

ESTILO = ("Ilustración pictórica semirrealista con aire de película histórica, luz cálida y dorada en Pompeya, arquitectura romana (columnas, mosaicos, "
          "frescos rojos y ocres, patios con impluvio), paleta de terracotas, ocres, azules marinos y blancos de mármol, con la columna de humo del Vesubio "
          "al fondo cuando se vea el cielo, formato vertical 2:3. Sin texto, letras ni números en la imagen; los rollos, tablillas y frescos son solo dibujos "
          "decorativos sin escritura legible. Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado recogido con una cinta, ojos azules. Viste ropa romana de época: una stola larga de lino verde oliva con un manto (palla) azul sobre los hombros, sandalias de cuero y un brazalete de bronce.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Viste ropa romana de época: una túnica corta color arena con cinturón de cuero, una capa corta sobre un hombro, sandalias de correas y una bolsa de cuero cruzada.",
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado recogido con una cinta, ojos azules, stola larga de lino verde oliva con manto azul, sandalias de cuero y brazalete de bronce. "
        "Alberto: hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones, túnica corta color arena con cinturón de cuero, capa corta, sandalias de correas y bolsa de cuero. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo cinematográfico semirrealista de película histórica, luz dorada de amanecer y tonos terracota y azul marino. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul y dorada y los dos son absorbidos por un túnel de luz. "
         "Escena 3 (8-12 s): caen sobre el suelo de mosaico de un atrio romano al amanecer, entre columnas; al fondo, el Vesubio lanza una columna de humo. El aparato humea y un cristal rojo sale rodando. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, con ropa romana, asombrados, mirando al volcán; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe sordo al aterrizar, retumbar lejano del volcán, lira y flauta, sin voz de narrador.")

MOSAICOS = {
    "atrio": dict(filas=2, cols=2, cartas=["16", "14", "17", "15"], titulo="Mosaico del atrio"),
    "sello": dict(filas=1, cols=2, cartas=["27", "29"], titulo="El lacre partido"),
    "calendario": dict(filas=1, cols=2, cartas=["61", "63"], titulo="El calendario de piedra"),
}
POS = {4: ["arriba a la izquierda", "arriba a la derecha", "abajo a la izquierda", "abajo a la derecha"], 2: ["mitad izquierda", "mitad derecha"]}


def codigo(que):
    return f"Carta dibujada por código (herramientas/pompeya.py; no se pide a ChatGPT): {que}."


def pieza(carta, mosaico, que, pistas):
    m = MOSAICOS[mosaico]
    i = m["cartas"].index(carta)
    pos = POS[len(m["cartas"])][i]
    return dict(titulo=f"Carta {carta} — {m['titulo']} ({pos})", tipo="gris",
                mosaico=dict(id=mosaico, filas=m["filas"], cols=m["cols"], fila=i // m["cols"], col=i % m["cols"]),
                descripcion=[que], pistas=pistas, arte=codigo(f"{pos} de «{m['titulo']}»"))


def gris(carta, titulo, que, pistas, arte):
    return dict(titulo=f"Carta {carta} — {titulo}", tipo="gris", descripcion=[que], pistas=pistas, arte=arte)


def app(carta, titulo, que, sale, pistas, arte):
    return dict(titulo=f"Carta {carta} — {titulo}", tipo="verde", descripcion=[que, f"Al resolverlo, coged la carta {sale}."], pistas=pistas, arte=arte)


def escena(carta, titulo, coge, descarta, texto, pistas, arte):
    lineas = [texto, "Coged las cartas " + _lista(coge) + "." if len(coge) > 1 else f"Coged la carta {coge[0]}."]
    if descarta:
        lineas[-1] += " Descartad " + ("las cartas " + _lista(descarta) if len(descarta) > 1 else f"la carta {descarta[0]}") + "."
    return dict(titulo=f"Carta {carta} — {titulo}", tipo="gris", coge=coge, descarta=descarta, descripcion=lineas, pistas=pistas + [lineas[-1]], arte=arte)


def _lista(xs):
    xs = [str(x) for x in xs]
    return ", ".join(xs[:-1]) + " y " + xs[-1] if len(xs) > 1 else xs[0]


def combinable(carta, titulo, color, con, da, que, arte):
    return dict(titulo=f"Carta {carta} — {titulo}", tipo=color, combina=[con, da],
                descripcion=[que, f"Combinadla con la carta {con}: sumad sus números ({carta} + {con} = {da}) y coged la carta {da}."],
                pistas=[que.split(".")[0] + ".", f"Se combina con la carta {con}.", f"{carta} + {con} = {da}."], arte=arte)


J = {
    "P": escena("P", "Llegada a Pompeya", [10, 12], [],
                "Séptima parada del Cronoportal: Pompeya, 24 de agosto del año 79. Aterrizáis en el atrio de una villa rica y el aparato golpea el borde del estanque: su cristal de energía sale volando y se pierde entre las columnas. Al fondo, el Vesubio echa humo. Nadie en la ciudad sabe lo que va a pasar hoy... salvo vosotros.",
                ["Mirad a vuestro alrededor y revisad el aparato."],
                "El atrio de una villa romana de Pompeya al amanecer: columnas, un estanque de lluvia y un suelo de mosaico; sobre los tejados, la columna de humo del Vesubio. En primer plano, un aparato de latón y cristal (el Cronoportal) humea en el suelo. Cristina, con los ojos muy abiertos de asombro, y Alberto, con una ceja arqueada de incredulidad, se levantan aturdidos con ropa romana."),
    "10": escena("10", "El atrio", [13, 14, 15, 16, 17, 18, 22], ["P"],
                 "Es la villa de Lucrecia, comerciante de aceite y de vino. El golpe ha partido el mosaico del suelo en cuatro placas. La puerta del despacho tiene un panel de bronce con huecos para figuras. Junto al mosaico, una tablilla firmada por Lucio, el mosaiquista. En el fondo del estanque brilla media llave de bronce.",
                 ["Las cuatro placas son un solo mosaico.", "La tablilla de Lucio es un acertijo sobre el mosaico."],
                 "El atrio de una villa romana con un mosaico roto en cuatro placas sobre las losas, una puerta de madera con un panel de bronce y un estanque con un brillo dorado en el fondo. Cristina se agacha junto a las placas con el ceño fruncido de concentración y Alberto mete la mano en el agua del estanque con cara de asco."),
    "12": combinable("12", "Cronoportal sin cristal", "azul", 62, 74, "El Cronoportal sin su cristal de energía: el anillo central está apagado y el hueco del pecho, vacío.",
                     "Primer plano del Cronoportal: una consola de latón y cristal con dos antenas de cobre, un anillo central apagado y un hueco circular vacío, apoyado en el suelo de mosaico de un atrio romano."),
    "13": app("13", "El panel del despacho", "Es un juego de la app: un panel de bronce con ocho figuras. Hay que tocar cuatro en el orden correcto.", 19,
              ["Juntad las cuatro placas del mosaico (14 a 17) y leed despacio la tablilla de Lucio (18).", "El sol y la puerta están en el mosaico: hay un único camino blanco de uno a otro, sin volver atrás. Las figuras de los ramales sin salida no cuentan.", f"Por orden: {_S_LAB}."],
              "Un panel de bronce en una puerta de madera romana con ocho medallones con figuras (delfín, ánfora, laurel, lechuza, racimo, concha, lucerna y escudo) y cuatro huecos vacíos."),
    "14": pieza("14", "atrio", "Una placa del mosaico del atrio.", ["Es una de las cuatro placas: juntadlas.", "Arriba, de izquierda a derecha: 16 y 14. Abajo: 17 y 15.", "Seguid la piedra blanca."]),
    "15": pieza("15", "atrio", "Una placa del mosaico del atrio.", ["Es una de las cuatro placas: juntadlas.", "Arriba, de izquierda a derecha: 16 y 14. Abajo: 17 y 15.", "Seguid la piedra blanca."]),
    "16": pieza("16", "atrio", "Una placa del mosaico del atrio.", ["Es una de las cuatro placas: juntadlas.", "Arriba, de izquierda a derecha: 16 y 14. Abajo: 17 y 15.", "Seguid la piedra blanca."]),
    "17": pieza("17", "atrio", "Una placa del mosaico del atrio.", ["Es una de las cuatro placas: juntadlas.", "Arriba, de izquierda a derecha: 16 y 14. Abajo: 17 y 15.", "Seguid la piedra blanca."]),
    "18": gris("18", "Tablilla de Lucio", "Un acertijo en verso del mosaiquista sobre su mosaico.",
               ["Es un acertijo sobre el mosaico del atrio.", "«Donde nace el sol» es el este, a la derecha; «donde se pone», el oeste. Solo cuenta la piedra blanca.", f"Las figuras que se saludan, en orden: {_S_LAB}."],
               codigo("la tablilla de Lucio")),
    "22": combinable("22", "Mitad de llave", "azul", 35, 57, "La mitad de una llave de bronce, con el ojo y medio paletón, sacada del estanque.",
                     "La mitad de una llave romana de bronce, con el ojo y medio paletón, mojada y brillante sobre las losas de un atrio."),
    "19": escena("19", "El despacho de Lucrecia", [20, 21, 23, 24, 25], [10, 13, 14, 15, 16, 17, 18],
                 "El panel cede y entráis en el tablinum, el despacho de Lucrecia. Hay un arca de bronce cerrada con un ábaco en la tapa, tres tablillas de cuentas de su esclavo Tiro y, clavada en la pared, la regla del escriba.",
                 ["El arca se abre con un número.", "Las tablillas son las cuentas de tres días."],
                 "El despacho de una villa romana con estantes de rollos y tablillas, una mesa con tres tablillas de cera y un arca de bronce con un ábaco de cuentas en la tapa. Alberto ojea una tablilla con la boca torcida de desconfianza y Cristina mueve una cuenta del ábaco, curiosa."),
    "20": app("20", "El arca de Lucrecia", "Es un juego de la app: el ábaco romano de la tapa del arca. Lucrecia guarda dentro el total verdadero de las ventas de los tres días.", 26,
              ["Hacen falta las tres tablillas (21, 23 y 24) y la regla del escriba (25).", "Pasad cada importe a nuestros números y sumad cada día: una de las sumas de Tiro está mal. Sumad los tres totales de verdad.", f"El total es {CU['total']} ({CU['total_romano']})."],
              "Un ábaco romano de bronce con cuatro columnas de cuentas sobre la tapa de un arca, con una cerradura decorada."),
    "21": gris("21", "Cuentas de Lucrecia (día I)", "Las ventas del primer día, en números romanos, y la suma de Tiro.",
               ["Son cuentas para el arca (carta 20).", "Leed los números romanos con la regla del escriba (carta 25).", f"El total verdadero de los tres días es {CU['total']}."], codigo("la tablilla del día I")),
    "23": gris("23", "Cuentas de Lucrecia (día II)", "Las ventas del segundo día, en números romanos, y la suma de Tiro.",
               ["Son cuentas para el arca (carta 20).", "Comprobad la suma de Tiro.", f"El total verdadero de los tres días es {CU['total']}."], codigo("la tablilla del día II")),
    "24": gris("24", "Cuentas de Lucrecia (día III)", "Las ventas del tercer día, en números romanos, y la suma de Tiro.",
               ["Son cuentas para el arca (carta 20).", "Comprobad la suma de Tiro.", f"El total verdadero de los tres días es {CU['total']}."], codigo("la tablilla del día III")),
    "25": gris("25", "La regla del escriba", "El valor de cada letra romana y ejemplos de cómo se leen las que restan.",
               ["Sirve para leer las cuentas (cartas 21, 23 y 24).", "Una letra pequeña delante de una grande resta: IV = 4, XC = 90.", "«Tiro suma mal»: una de las tres sumas está equivocada."], codigo("la regla del escriba")),
    "26": escena("26", "El arca abierta", [27, 28, 29], [19, 20, 21, 23, 24, 25],
                 "El arca se abre. Dentro hay monedas, una carta de Lucrecia cerrada con lacre, que se ha partido en dos al abrir la tapa, y un joyero con seis anillos de sello. Solo el anillo de Lucrecia rompe el hechizo del lacre, dice una inscripción... o eso cree Tiro.",
                 ["Hay un puzle: el joyero de anillos y el lacre partido."],
                 "Un arca de bronce abierta llena de monedas de oro, con una carta enrollada sellada con lacre rojo partido y un joyero con seis anillos de sello. Cristina sostiene la carta con los ojos brillantes de curiosidad y Alberto cuenta monedas con una sonrisa pícara."),
    "27": pieza("27", "sello", "La mitad izquierda del lacre de la carta.", ["Juntad las dos mitades del lacre (27 y 29).", "Lo que deja un sello en el lacre es su imagen en espejo.", "El anillo bueno es el que, al revés, da esta impronta."]),
    "29": pieza("29", "sello", "La mitad derecha del lacre de la carta.", ["Juntad las dos mitades del lacre (27 y 29).", "Lo que deja un sello en el lacre es su imagen en espejo.", "El anillo bueno es el que, al revés, da esta impronta."]),
    "28": app("28", "El joyero de anillos", "Es un juego de la app: seis anillos de sello. Hay que elegir el que selló la carta.", 30,
              ["Juntad las dos mitades del lacre (cartas 27 y 29).", "Un sello imprime al revés, como en un espejo: el anillo tiene que ser la impronta volteada, el delfín Y las letras. Ojo con los que solo tienen una de las dos cosas volteada.", "Es el anillo del delfín con «LVC» que se lee al derecho y el delfín mirando al otro lado que en el lacre."],
              "Un joyero de madera forrado de tela roja con seis anillos de oro con sellos grabados."),
    "30": escena("30", "La carta de Lucrecia", [32, 39], [26, 27, 28, 29],
                 "La carta dice: «Tiro: me llevo la gema roja que cayó del cielo al puerto, donde nos espera la barca. El monte ruge y no me fío. Cierra la despensa con la llave partida y apaga las lámparas. Te espero en el muelle». La despensa está en el peristilo; el comedor, al otro lado.",
                 ["El cristal lo tiene Lucrecia, camino del puerto.", "Hay que explorar el jardín y el comedor."],
                 "Un pasillo de una villa romana que da por un lado a un jardín con columnas y por el otro a un comedor con frescos rojos. Cristina lee una carta enrollada con cara de alarma y Alberto mira hacia el volcán por una ventana, preocupado."),
    "32": escena("32", "El peristilo", [33, 36, 37], [],
                 "El jardín de columnas tiene una fuente seca: el acueducto no llega desde que alguien cerró mal las compuertas. Al fondo del pilón se ve algo de bronce. Hay un plano del fontanero y el plano del jardín del jardinero.",
                 ["Hay un puzle: las compuertas de la fuente."],
                 "Un jardín romano con columnas, parterres de rosas, laureles, viña y lirios y una fuente seca en el centro con un brillo de bronce en el fondo; en un muro, una caja de compuertas de madera. Alberto tira de una palanca con todas sus fuerzas y Cristina mira el pilón vacío con los brazos en jarras."),
    "33": app("33", "Las compuertas", "Es un juego de la app: las nueve compuertas del acueducto de la villa. Hay que abrir y cerrar las justas para regar el jardín como quiere el jardinero.", 35,
              ["Hacen falta el plano del fontanero (carta 36) y el del jardinero (carta 37).", "Cada arqueta reparte a partes iguales entre sus compuertas abiertas y no se puede perder nada. Contad las ánforas de cada parterre.", f"Abiertas: {_S_FU}. Cerradas: {_S_FU_CERR}."],
              "Una caja de compuertas de madera con nueve palancas numeradas con números romanos junto a un canal de agua de piedra."),
    "35": combinable("35", "Otra mitad de llave", "roja", 22, 57, "La otra mitad de la llave de bronce, que apareció en el fondo de la fuente al volver el agua.",
                     "La otra mitad de una llave romana de bronce, en el fondo de una fuente de mármol con agua clara."),
    "36": gris("36", "El acueducto de la villa", "El plano del fontanero: el agua del acueducto, las arquetas, las compuertas y los parterres.",
               ["Sirve para las compuertas (carta 33).", "Cada arqueta reparte por igual entre sus compuertas abiertas; si todas están cerradas, se pierde.", f"Abiertas: {_S_FU}."], codigo("el plano del acueducto")),
    "37": gris("37", "El jardín de Lucrecia", "El plano del jardinero: lo que bebe cada parterre, apuntado con ánforas.",
               ["Sirve para las compuertas (carta 33).", "Cada ánfora es una medida de agua.", f"Abiertas: {_S_FU}."], codigo("el plano del jardín")),
    "39": escena("39", "El triclinio", [40, 41, 42], [],
                 "En el comedor quedan los restos de la cena. En una columna hay un grafito medio borrado y, debajo, un acertijo. Una tablilla de cera abre un nicho en la pared, si se escribe la palabra justa.",
                 ["Hay un puzle: el grafito, el acertijo y la tablilla."],
                 "Un comedor romano con tres lechos alrededor de una mesa con restos de una cena, paredes de frescos rojos y una columna con un grafito arañado; en un nicho, una tablilla de cera. Cristina pasa los dedos por el grafito, concentrada, y Alberto prueba una uva de la mesa con cara de culpa."),
    "40": app("40", "La tablilla de cera", "Es un juego de la app: una tablilla de cera donde se escribe una palabra de cinco letras.", 38,
              ["Hacen falta el grafito (carta 41) y el acertijo del sembrador (carta 42).", "El cuadrado se lee igual en las cuatro direcciones: cada letra borrada está repetida en otra casilla. La «cruz» es la fila y la columna del centro.", "La palabra es TENET."],
              "Una tablilla de cera romana con un punzón de hueso sobre una mesa de mármol."),
    "38": combinable("38", "Pedernal", "azul", 56, 94, "Un pedernal y un trozo de yesca para hacer fuego, que estaban en el nicho de la pared.",
                     "Un pedernal y un trozo de yesca sobre un paño en un nicho de pared romano."),
    "41": gris("41", "Grafito en la columna", "Un cuadrado de letras arañado en una columna, con varias letras borradas.",
               ["Sirve para la tablilla de cera (carta 40).", "Se lee igual en todas las direcciones: completadlo.", "La palabra de la cruz es TENET."], codigo("el grafito del cuadrado")),
    "42": gris("42", "El acertijo del sembrador", "Un acertijo en verso escrito bajo el grafito.",
               ["Habla del cuadrado de la columna (carta 41).", "La «cruz» es la fila y la columna del centro.", "La palabra es TENET."], codigo("el acertijo del sembrador")),
    "57": escena("57", "La despensa", [43, 45, 46], [22, 35, 32, 33, 36, 37],
                 "La llave abre la despensa: ánforas, sacos y una balanza romana. Lucrecia ha dejado un cofre colgado del gancho con un recibo del mercader, y en la viga, tres pesadas de prueba dibujadas con carbón. Si la balanza queda en equilibrio, se suelta el pestillo del cofre.",
                 ["Hay un puzle: la balanza romana, el recibo y las pesadas."],
                 "Una despensa romana llena de ánforas apiladas, sacos y quesos colgados, con una balanza romana de brazo largo de la que cuelga un cofre de madera. Alberto sujeta el contrapeso con cara de concentración y Cristina compara un papel con unos dibujos de carbón en la viga, dudosa."),
    "46": app("46", "La balanza romana", "Es un juego de la app: una balanza romana (statera) con el cofre colgado del gancho y un contrapeso que se mueve por las muescas del brazo. Hay que dejarla en equilibrio.", 56,
              ["Hacen falta las pesadas (carta 43) y el recibo (carta 45).", "De las pesadas sale lo que pesa cada cosa. Sumad el cofre entero. Con la balanza, peso × distancia a cada lado: el cofre cuelga a una muesca del eje.", f"El cofre pesa {ST['total']} libras: muesca {ST['muesca']}."],
              "Una balanza romana de bronce de brazo largo con muescas, un gancho con un cofre y un contrapeso con forma de cabeza."),
    "56": combinable("56", "Lámpara de aceite", "roja", 38, 94, "Una lámpara de aceite de bronce, llena pero apagada, que estaba dentro del cofre.",
                     "Una lámpara de aceite romana de bronce con forma de barca, llena pero apagada, sobre un paño dentro de un cofre."),
    "43": gris("43", "Las pesadas del mercader", "Tres pesadas de prueba dibujadas con carbón en la viga, todas en equilibrio.",
               ["Sirven para la balanza (carta 46).", "Juntad la segunda y la tercera: el vino pesa una libra más que los higos y entre los dos pesan cinco. Luego, la primera.", f"Aceite {ST['pesos']['aceite']}, vino {ST['pesos']['vino']}, higos {ST['pesos']['higos']} libras."], codigo("las pesadas")),
    "45": gris("45", "Recibo del mercader", "Lo que contiene el cofre de Lucrecia y lo que pesa el cofre vacío.",
               ["Sirve para la balanza (carta 46).", "No olvidéis el cofre vacío. Y el contrapeso pesa lo mismo que él.", f"El cofre pesa {ST['total']} libras: muesca {ST['muesca']}."], codigo("el recibo")),
    "94": escena("94", "El pasadizo de la calle", [51, 52, 53, 54, 55], [38, 56, 30, 39, 40, 41, 42, 57, 43, 45, 46],
                 "Con la lámpara encendida bajáis por el pasadizo de los esclavos hasta la calle. La ceniza empieza a caer. Tiro, el esclavo, os explica que Lucrecia no fue directa al puerto: pasó a esconder algo en una casa de la manzana. En las paredes hay grafitos sobre ella y, en el foro, el plano de la manzana.",
                 ["Hay un puzle: la casa donde paró Lucrecia."],
                 "Una calle de Pompeya con aceras altas, pasos de piedra y paredes pintadas llenas de grafitos, bajo una lluvia fina de ceniza gris; al fondo, el Vesubio. Cristina protege la llama de una lámpara de aceite con la mano, con cara de miedo, y Alberto lee un grafito con la nariz pegada a la pared."),
    "55": app("55", "La casa de la manzana", "Es un juego de la app: el plano de la manzana. Hay que tocar la casa donde paró Lucrecia.", 58,
              ["Hacen falta los tres grafitos (51, 52 y 53) y el plano (54).", "Cada grafito descarta casas: sin tienda, con la panadería pegada a un lado, con la puerta al sur y pintada de rojo.", f"Es {_S_CASA}."],
              "Un plano de una manzana de Pompeya pintado en una pared del foro, con casas de colores y puertas marcadas."),
    "51": gris("51", "Grafito: la casa", "Un grafito sobre la casa de Lucrecia.", ["Sirve para el plano (carta 55).", "«Solo hay casa»: no tiene tienda.", f"Es {_S_CASA}."], codigo("un grafito")),
    "52": gris("52", "Grafito: el pan", "Otro grafito sobre la casa de Lucrecia.", ["Sirve para el plano (carta 55).", "Una panadería pegada a la izquierda o a la derecha.", f"Es {_S_CASA}."], codigo("un grafito")),
    "53": gris("53", "Grafito: la puerta", "Otro grafito sobre la casa de Lucrecia.", ["Sirve para el plano (carta 55).", "El mar está al sur; y la casa es roja.", f"Es {_S_CASA}."], codigo("un grafito")),
    "54": gris("54", "Plano de la manzana", "El plano de la manzana copiado de la pared del foro: casas, tiendas, colores y puertas.",
               ["Sirve para la casa de la manzana (carta 55).", "Cruzad lo que dicen los tres grafitos.", f"Es {_S_CASA}."], codigo("el plano de la manzana")),
    "58": escena("58", "El templo de Isis", [59, 61, 63, 65], [94, 51, 52, 53, 54, 55],
                 "En la casa no está Lucrecia, pero sí una nota: «Dejé al sacerdote de Isis la llave de la puerta del mar». En el templo, el sacerdote solo la entrega a quien ponga en el calendario de piedra el día que dice la carta de Plinio.",
                 ["Hay un puzle: el calendario de piedra y la carta de Plinio."],
                 "El patio de un pequeño templo de Isis en Pompeya, con columnas, palmeras y un altar, bajo la ceniza que cae; un sacerdote con túnica de lino blanco sostiene una carta. Cristina habla con el sacerdote con gesto suplicante y Alberto mira el calendario de piedra con los ojos entrecerrados."),
    "59": app("59", "El calendario de piedra", "Es un juego de la app: el calendario de piedra del templo, con una clavija que se pone en un día de agosto.", 64,
              ["Hacen falta las dos mitades del calendario (61 y 63) y la carta de Plinio (65).", "Los romanos contaban hacia atrás desde las calendas, contando también el día de llegada. El ejemplo del calendario os enseña cómo.", f"Es el día {CAL['dia']} de agosto."],
              "Un calendario romano de piedra con los días de agosto grabados en casillas y una clavija de bronce."),
    "61": pieza("61", "calendario", "La mitad izquierda del calendario de piedra del templo.", ["Juntad las dos mitades (61 y 63).", "Fijaos en el ejemplo marcado en azul.", f"Es el día {CAL['dia']}."]),
    "63": pieza("63", "calendario", "La mitad derecha del calendario de piedra del templo.", ["Juntad las dos mitades (61 y 63).", "Fijaos en el ejemplo marcado en azul.", f"Es el día {CAL['dia']}."]),
    "65": gris("65", "Carta de Plinio", "Una carta de Plinio al sacerdote, con el día en que despertó el monte, a la manera romana.",
               ["Sirve para el calendario de piedra (carta 59).", "Contad hacia atrás desde las calendas de septiembre, contándolas a ellas.", f"Es el día {CAL['dia']} de agosto."], codigo("la carta de Plinio")),
    "64": escena("64", "La erupción", [66, 67, 75], [58, 59, 61, 63, 65],
                 "El sacerdote os da la llave de la puerta del mar justo cuando el monte revienta: una columna negra tapa el sol y llueven piedras. Hay que llegar al puerto desde el foro antes de que la ceniza cierre la puerta, por calles que se van cortando.",
                 ["Hay un puzle: la ruta hasta el puerto."],
                 "Una plaza de Pompeya en plena erupción: el cielo negro, una lluvia de piedras pómez y gente huyendo con fardos; al fondo, el Vesubio con una columna de fuego. Alberto sujeta a Cristina de la mano y tira de ella con cara de pánico, y Cristina se tapa la boca con el manto, con los ojos llorosos."),
    "66": app("66", "La huida", "Es un juego de la app: el plano de las calles. Hay que marcar la ruta del foro al puerto, cruce a cruce.", 69,
              ["Hacen falta el mapa (carta 67) y lo que grita el vigía (carta 75).", "Quitad las calles cortadas y sumad los pasos de cada ruta posible: solo una llega a tiempo.", f"Ruta: {_S_HU} ({HU['tiempo']} pasos)."],
              "Un plano de calles de Pompeya pintado en una tabla de madera, con los cruces marcados y ceniza encima."),
    "67": gris("67", "Las calles hasta el puerto", "El mapa de las calles del foro al puerto, con los pasos que se tarda en cada tramo en números romanos.",
               ["Sirve para la huida (carta 66).", "Sumad los tramos de cada ruta.", f"Ruta: {_S_HU}."], codigo("el mapa de las calles")),
    "75": gris("75", "El vigía de la torre", "Lo que grita el vigía: calles cortadas y cuánto falta para que la ceniza cierre la puerta.",
               ["Sirve para la huida (carta 66).", "Esas calles no se pueden usar.", f"Ruta: {_S_HU}."], codigo("los gritos del vigía")),
    "69": escena("69", "El puerto", [70, 71, 72, 76], [64, 66, 67, 75],
                 "En el muelle os espera Lucrecia con una barca pequeña y un montón de cosas que quiere salvar. El barquero no carga más de lo que aguanta su barca. Lucrecia os promete la gema roja si la ayudáis a cargarla bien.",
                 ["Hay un puzle: qué cargar en la barca."],
                 "Un muelle romano bajo la lluvia de ceniza, con una barca pequeña, un barquero viejo y un montón de ánforas, fardos y un cofre; una mujer romana rica con un collar del que cuelga un cristal rojo. Cristina negocia con la mujer con gesto decidido y Alberto, a punto de caerse al agua, sostiene un ánfora enorme con cara de agobio."),
    "70": app("70", "La barca", "Es un juego de la app: el muelle con seis cosas y la barca. Hay que cargar lo que pide Lucrecia y zarpar.", 82,
              ["Hacen falta el manifiesto (carta 71), el barquero (carta 72) y la tablilla de Lucrecia (carta 76).", "Lo más valioso que quepa: probad combinaciones sin pasar del peso.", f"Cargad: {_S_BA} (valor {BA['valor']})."],
              "Una barca de madera junto a un muelle romano con ánforas, un fardo de lana, un cofre, una estatuilla y un saco de trigo."),
    "71": gris("71", "La carga del muelle", "Las seis cosas del muelle, con lo que pesa y lo que vale cada una.", ["Sirve para la barca (carta 70).", "Pesas: peso. Monedas: valor.", f"Cargad: {_S_BA}."], codigo("el manifiesto")),
    "72": gris("72", "El barquero", "Lo que aguanta la barca del barquero.", ["Sirve para la barca (carta 70).", "No paséis de ese peso.", f"Cargad: {_S_BA}."], codigo("el barquero")),
    "76": gris("76", "Tablilla de Lucrecia", "Lo que pide Lucrecia que se salve.", ["Sirve para la barca (carta 70).", "Lo que más vale, sin hundir la barca.", f"Cargad: {_S_BA}."], codigo("la tablilla de Lucrecia")),
    "82": escena("82", "La gema de Lucrecia", [62], [69, 70, 71, 72, 76],
                 "La barca se aleja con lo que más valía y Lucrecia, agradecida, se arranca el colgante: es vuestro cristal de energía. «Que los dioses os lleven a casa», dice, antes de saltar a bordo.",
                 ["Lucrecia os da el cristal."],
                 "Una barca alejándose de un muelle romano bajo un cielo negro de ceniza; en primer plano, una mujer romana entrega un colgante con un cristal rojo. Cristina recibe el cristal con los ojos llenos de lágrimas de emoción y Alberto se despide con la mano, aliviado."),
    "62": combinable("62", "Cristal de energía", "roja", 12, 74, "El cristal de energía del Cronoportal, con su fulgor rojo, colgado de una cadena.",
                     "Un cristal rojo facetado con un fulgor interior, colgado de una cadena de oro, sobre una mano, con ceniza gris cayendo alrededor."),
    "74": escena("74", "Cronoportal reconectado", [99], [62, 12, 82],
                 "El cristal encaja y el Cronoportal se enciende entre la ceniza. Activadlo antes de que el aire se vuelva irrespirable.",
                 ["El portal ya funciona."],
                 "El Cronoportal encendido con un cristal rojo en su pecho y un arco de luz azul y dorada, en un muelle romano bajo una lluvia de ceniza. Cristina, con la cara tiznada de ceniza y gesto de urgencia, tira de Alberto, que carga el aparato tosiendo."),
    "99": dict(titulo="Carta 99 — De vuelta a casa (FIN)", tipo="gris", descarta=[74],
               descripcion=["El anillo se abre en un arco de luz y Cristina y Alberto salen de Pompeya justo cuando la ceniza lo cubre todo. Aterrizan en su salón, tiznados de gris.",
                            "Alberto se sacude la túnica: «Mañana, otro destino». Cristina sonríe: en el bolsillo lleva una tesela blanca del mosaico. Descartad la carta 74.", "FIN."],
               pistas=[],
               arte="La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ve Pompeya bajo una nube de ceniza. Llevan aún su ropa romana, cubierta de ceniza. Cristina ríe con una tesela blanca en la mano y Alberto tose y sonríe aliviado. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(juego="Pompeya, 79 d.C. — El Mosaico del Mundo", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()})

SPEC = dict(final="99", needs={
    "19": ["13", "14", "15", "16", "17", "18"], "26": ["20", "21", "23", "24", "25"], "30": ["28", "27", "29"], "35": ["33", "36", "37"],
    "38": ["40", "41", "42"], "57": ["22", "35"], "56": ["46", "43", "45"], "94": ["38", "56"], "58": ["55", "51", "52", "53", "54"],
    "64": ["59", "61", "63", "65"], "69": ["66", "67", "75"], "82": ["70", "71", "72", "76"], "74": ["62", "12"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_T = [
    ("leer", "P", "Llegada", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge 10 y 12."),
    ("leer", "10", "El atrio", "Lee la carta 10. Descarta la P y coge 13, 14, 15, 16, 17, 18 y 22. Junta las placas 16 y 14 arriba y 17 y 15 abajo."),
    ("app", "13", "El panel del despacho", f"En el móvil: Acción, 13. En el mosaico, el único camino blanco del sol (este) a la puerta (oeste) pasa por: {_S_LAB}. El mensaje te dice que cojas la 19.", "carta 19"),
    ("leer", "19", "El despacho", "Lee la carta 19. Descarta 10, 13, 14, 15, 16, 17 y 18 y coge 20, 21, 23, 24 y 25."),
    ("app", "20", "El arca", f"En el móvil: Acción, 20. Las sumas verdaderas de los tres días dan {CU['total']} ({CU['total_romano']}): ponlo en el ábaco. El mensaje te dice que cojas la 26.", "carta 26"),
    ("leer", "26", "El arca abierta", "Lee la carta 26. Descarta 19, 20, 21, 23, 24 y 25 y coge 27, 28 y 29."),
    ("app", "28", "El joyero", "En el móvil: Acción, 28. Elige el anillo cuyo sello, en espejo, da la impronta del lacre (27 y 29). El mensaje te dice que cojas la 30.", "carta 30"),
    ("leer", "30", "La carta de Lucrecia", "Lee la carta 30. Descarta 26, 27, 28 y 29 y coge 32 y 39."),
    ("leer", "32", "El peristilo", "Lee la carta 32. Coge 33, 36 y 37."),
    ("app", "33", "Las compuertas", f"En el móvil: Acción, 33. Deja abiertas {_S_FU} y cerradas {_S_FU_CERR}. El mensaje te dice que cojas la 35.", "carta 35"),
    ("combinar", "22", "35", "La llave", "Las dos mitades de la llave (22 y 35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "La despensa", "Lee la carta 57. Descarta 22, 35, 32, 33, 36 y 37 y coge 43, 45 y 46."),
    ("app", "46", "La balanza romana", f"En el móvil: Acción, 46. El cofre pesa {ST['total']} libras: pon el contrapeso en la muesca {ST['muesca']}. El mensaje te dice que cojas la 56.", "carta 56"),
    ("leer", "39", "El triclinio", "Lee la carta 39. Coge 40, 41 y 42."),
    ("app", "40", "La tablilla de cera", "En el móvil: Acción, 40. Completa el cuadrado por simetría: la palabra de la cruz es TENET. El mensaje te dice que cojas la 38.", "carta 38"),
    ("combinar", "38", "56", "La lámpara", "El pedernal (38) y la lámpara (56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "El pasadizo de la calle", "Lee la carta 94. Descarta 38, 56, 30, 39, 40, 41, 42, 57, 43, 45 y 46 y coge 51, 52, 53, 54 y 55."),
    ("app", "55", "La casa de la manzana", f"En el móvil: Acción, 55. Los tres grafitos dejan una sola casa: {_S_CASA}. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "El templo de Isis", "Lee la carta 58. Descarta 94, 51, 52, 53, 54 y 55 y coge 59, 61, 63 y 65."),
    ("app", "59", "El calendario", f"En el móvil: Acción, 59. Nueve días antes de las calendas de septiembre, contándolas: día {CAL['dia']}. El mensaje te dice que cojas la 64.", "carta 64"),
    ("leer", "64", "La erupción", "Lee la carta 64. Descarta 58, 59, 61, 63 y 65 y coge 66, 67 y 75."),
    ("app", "66", "La huida", f"En el móvil: Acción, 66. Sin las calles cortadas, la única ruta a tiempo es {_S_HU}. El mensaje te dice que cojas la 69.", "carta 69"),
    ("leer", "69", "El puerto", "Lee la carta 69. Descarta 64, 66, 67 y 75 y coge 70, 71, 72 y 76."),
    ("app", "70", "La barca", f"En el móvil: Acción, 70. Carga {_S_BA} y zarpa. El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "La gema de Lucrecia", "Lee la carta 82. Descarta 69, 70, 71, 72 y 76 y coge la 62."),
    ("combinar", "12", "62", "El cristal", "El Cronoportal (12) y el cristal (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "Cronoportal reconectado", "Lee la carta 74. Descarta 62, 12 y 82 y coge la 99."),
    ("leer", "99", "Final", "Lee la carta 99. Descarta la 74. En la mesa solo queda la 99. ¡Fin!"),
]
PASOS = []
for _p in _T:
    if _p[0] == "combinar":
        PASOS.append(dict(t=_p[3], que=_p[4], acciones=[("combinar", _p[1], _p[2])]))
    elif _p[0] == "app":
        PASOS.append(dict(t=_p[2], que=_p[3], acciones=[("app", _p[1], _p[4])]))
    else:
        PASOS.append(dict(t=_p[2], que=_p[3], acciones=[("leer", _p[1])]))
_amp.separar_mosaicos(J, PASOS, {"15": "P", "17": "P", "29": "19", "63": "94"})
_amp.recalcular_mesas(PASOS, J)

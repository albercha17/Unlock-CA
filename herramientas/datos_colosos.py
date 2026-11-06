"""Altamuralla: El Valle de los Colosos — decimocuarta parada del Cronoportal (60 cartas, 6 nov 2026), dificultad media-alta.

Una ciudad amurallada al borde de un valle donde duermen gigantes de piedra y musgo, los colosos. El cristal del Cronoportal cae al valle y nadie sale
de la muralla... hasta que la doctora Olvido Marván les da dos jeringuillas con un suero ámbar: a mitad de la partida (carta 44) Cristina y Alberto
se convierten en colosos de quince metros. Once puzles que no se parecen a los de ningún otro juego de la serie: faroles (Akari), crónica (línea de
tiempo), barracones (Fillomino), inscripción en lengua inventada, dosis del suero (tabla y jeringuillas), pisadas de coloso (Hitori), canto de los
colosos (Simon traducido), ofrendas (caja negra), palancas de la torre (memoria por etapas), tesoro (agrupar) y la inscripción de la cámara
(metapuzle indexado). Detalle del arco de la serie: la flor de cinco pétalos firma la inscripción de un viajero con un cristal que pasó hace cien años.
Inspirado en el género de «ciudad amurallada asediada por gigantes», sin personajes, nombres ni emblemas de ninguna obra concreta.
Las cartas-pista las dibuja herramientas/colosos.py (instancias_colosos.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402
import instancias_colosos as I  # noqa: E402

INST = I.INST

ESTILO = ("Ilustración pintada de aventura de fantasía, épica pero luminosa y amable, como una película de animación para toda la familia: una ciudad "
          "amurallada de piedra clara con tejados rojos y torres con campanas, un valle verde con niebla, cielos de atardecer naranja y violeta, luz "
          "dorada. Los colosos son gigantes amables de quince a veinte metros, de piel gris como la piedra, cubiertos de musgo, líquenes y enredaderas "
          "como si fueran una capa, con ojos ámbar grandes y dormilones y gesto bonachón; nunca dan miedo ni hay violencia. Formato vertical 2:3. "
          "Sin texto, letras ni números legibles en la imagen. Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la "
          "imagen. Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": ("Cristina: mujer de 26 años, pelo rubio muy rizado recogido en una coleta alta, ojos azules; lleva el abrigo corto de lona color mostaza "
                 "de la Guardia de las Campanas, con botones de latón y una campanita bordada en el brazo, pantalón marrón y botas altas. Cuando la escena "
                 "dice que es un coloso, es ella misma a escala gigante (quince metros), con la misma cara y la misma ropa agrandada, unas vetas ámbar "
                 "que brillan suavemente en las mejillas y los brazos y un vapor dorado que le sale de los hombros."),
    "Alberto": ("Alberto: hombre de 27 años, pelo moreno corto, barba cuidada, ojos marrones, gafas de protección subidas en la frente; lleva el mismo "
                "abrigo color mostaza de la Guardia de las Campanas, con un cinturón de herramientas. Cuando la escena dice que es un coloso, es él "
                "mismo a escala gigante (quince metros), con la misma cara y la misma ropa agrandada, vetas ámbar brillantes y vapor dorado."),
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y "
        "neutro, en dos versiones: a tamaño normal y convertidos en gigantes amables de quince metros junto a una casa diminuta. Mantén su parecido real "
        "con la foto en la cara. " + " ".join(PERSONAJES.values()) + " Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real en la cara, con el abrigo de la Guardia de las Campanas de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo de película de animación de aventura de fantasía, luz de atardecer dorada. Sin ningún "
         "texto, letra ni subtítulo en pantalla. Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos "
         "azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) encienden un aparato de latón y cristal con un anillo central. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul y dorada y los dos caen por un túnel de luz. Escena 3 (8-12 s): aparecen en lo "
         "alto de una muralla de piedra gigantesca al atardecer; un cristal azul sale disparado por encima del muro y cae a un valle verde con niebla. "
         "Escena 4 (12-15 s): plano general del valle, donde tres gigantes amables de piedra cubiertos de musgo abren los ojos ámbar y bostezan; "
         "fundido a negro. Sonido: zumbido eléctrico, silbido del portal, viento en la muralla, una campana lejana y un canto grave de gigantes.")

SIN_GENTE = "Sin ninguna persona en la imagen. "
GIGANTES = "Cristina y Alberto, ya convertidos en colosos de quince metros (su misma cara, su ropa agrandada, vetas ámbar y vapor dorado), "

MOSAICOS = {
    "cronica": dict(filas=2, cols=1, cartas=["19", "21"], titulo="La crónica de Altamuralla"),
    "piedra": dict(filas=2, cols=1, cartas=["42", "49"], titulo="La piedra del viajero"),
    "dosis": dict(filas=2, cols=1, cartas=["54", "55"], titulo="La tabla de dosis"),
    "cancionero": dict(filas=2, cols=1, cartas=["61", "63"], titulo="El cancionero de la doctora"),
}
POS = {(2, 1): ["mitad de arriba", "mitad de abajo"], (1, 2): ["mitad izquierda", "mitad derecha"]}

ref = I.ref
_FA = INST["faroles"]
_S_FAR = ", ".join(ref(f, c) for f, c in _FA["solucion"])
_CR = INST["cronica"]
_S_CRO = ", ".join(f"{i + 1}.º {I.SUCESOS[s]}" for i, s in enumerate(_CR["solucion"]))
_BA = INST["barracones"]
_S_BAR = "; ".join(f"fila {f + 1}: " + " ".join(str(_BA["solucion"][f"{f},{c}"]) for c in range(6)) for f in range(6))
_IN = INST["inscripcion"]
_NOMBRE = {"FLOR": "flor", "MURO": "muro", "VIAJERO": "viajero", "CRISTAL": "cristal", "COLOSO": "coloso", "BUSCAR": "buscar", "GUARDAR": "guardar",
           "ABRIR": "abrir", "NO": "no", "PLURAL": "plural (más de uno)", "CAMINO": "camino", "LUNA": "luna"}
_S_INS = ", ".join(_NOMBRE[w] for w in _IN["objetivo"]["glifos"])
_DO = INST["dosis"]
_S_DOS = (f"Cristina pesa {_DO['cristina']['peso']} kg y mide {_DO['cristina']['altura']} cm: {_DO['dosis']['Cristina']} ml; Alberto pesa "
          f"{_DO['alberto']['peso']} kg y mide {_DO['alberto']['altura']} cm: {_DO['dosis']['Alberto']} ml")
_PI = INST["pisadas"]
_S_PIS = ", ".join(ref(f, c) for f, c in _PI["solucion"])
_CA = INST["canto"]
_S_CAN = " / ".join(", ".join(r) for r in _CA["solucion"])
_S_TRA = ", ".join(f"{s} → {t}" for s, t in _CA["traduccion"].items())
_OF = INST["ofrendas"]
_S_OFR = ", ".join(str(i + 1) for i in _OF["solucion"])
_PA = INST["palancas"]
_TE = INST["tesoro"]
_S_TES = "; ".join(f"{_TE['condiciones'][g]}: " + ", ".join(_TE["objetos"][i]["letra"] for i in grupo) for g, grupo in enumerate(_TE["grupos"]))
_ME = INST["meta"]
_NOMBRE_APP = {"14": "los faroles", "20": "la crónica", "40": "los barracones", "48": "la inscripción", "52": "la dosis"}
_S_MET = ", ".join(f"{_NOMBRE_APP[a]} {_ME['marcas'][a]}" for a in _ME["orden"])


def codigo(que):
    return f"Carta dibujada por código (herramientas/colosos.py; no se pide a ChatGPT): {que}."


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
    # ------------------------------------------------------------------ Acto 1: la muralla
    "P": escena("P", "Altamuralla", [10, 12], [],
                "Decimocuarta parada del Cronoportal. El aparato os suelta en lo alto de una muralla de cincuenta metros, al atardecer. A un lado, una "
                "ciudad de tejados rojos; al otro, un valle verde donde duermen gigantes cubiertos de musgo: los colosos. Una sacudida, y el cristal de "
                "energía sale volando por encima del muro y cae al valle. «¿Ahí abajo? ¿Entre ellos?», susurra Alberto.",
                ["Mirad a vuestro alrededor y revisad el aparato."],
                "Lo alto de una muralla de piedra gigantesca al atardecer, con almenas y un camino de ronda. A un lado, una ciudad de tejados rojos y "
                "torres con campanas; al otro, un valle verde con niebla donde duermen tres colosos tumbados. Un destello azul (el cristal) cae hacia el "
                "valle. Cristina, con vaqueros y sudadera (aún con la ropa de casa), señala el destello con el brazo estirado y la boca abierta de "
                "asombro; Alberto, con vaqueros y camiseta, se agarra a una almena, pálido y con los ojos como platos. A sus pies, el Cronoportal "
                "humeando."),
    "10": escena("10", "El camino de ronda", [14, 16, 18, 19, 20, 21, 22], ["P"],
                 "Os detiene la sargento Ruth Albar, de la Guardia de las Campanas: «¿Bajar al valle? Nadie sale de Altamuralla. Ayudadme antes de "
                 "que anochezca y hablaremos». Os presta dos abrigos de la guardia. Hay que encender los faroles del camino de ronda (el plano de las "
                 "torres está en la carta 16), y el archivero quiere ordenada su crónica, partida en dos láminas, con su nota (carta 18). Junto a la "
                 "escalera, la jaula del elevador espera sin manivela.",
                 ["Hay dos puzles: los faroles y la crónica.", "La crónica son dos cartas: juntadlas, una encima de otra."],
                 "El camino de ronda de una muralla de piedra al atardecer, con faroles apagados en las almenas y una jaula de elevador de hierro junto "
                 "a una escalera. La sargento Ruth Albar (mujer de 40 años, pelirroja con una trenza, abrigo mostaza con galones y una campana de latón "
                 "al cinto) les tiende dos abrigos con el ceño fruncido pero los ojos curiosos. Cristina se pone el abrigo mostaza con una sonrisa "
                 "traviesa; Alberto mira por encima del muro hacia el valle tragando saliva."),
    "12": combinable("12", "Cronoportal sin cristal", "azul", 62, 74,
                     "El Cronoportal: una consola de latón y cristal con un anillo central apagado y un hueco vacío en el pecho, donde iba el cristal.",
                     SIN_GENTE + "Primer plano del Cronoportal: una consola de latón y cristal del tamaño de una maleta, con un anillo central apagado y "
                     "un hueco circular vacío en el pecho del aparato, sobre las losas de una muralla al atardecer, con una voluta de humo."),
    "14": app("14", "Los faroles del camino de ronda", "Es un juego de la app: el camino de ronda tiene que quedar iluminado entero antes de que "
              "anochezca. Un farol alumbra en línea recta hasta un muro, dos faroles no pueden verse, y las torres numeradas dicen cuántos faroles "
              "tienen pegados.", 24,
              ["El plano con los números de las torres está en la carta 16.",
               "Toda casilla del camino tiene que quedar iluminada. Un farol alumbra su fila y su columna hasta el primer muro; dos faroles nunca "
               "se ven entre sí; una torre con número tiene justo esos faroles en las casillas pegadas a ella (no en diagonal). Empezad por las "
               "torres con el número más alto y por las de 0.",
               f"Faroles en: {_S_FAR}. Marca de los faroles: {_ME['marcas']['14']}."],
              SIN_GENTE + "Un farol de hierro y cristal encendido con luz cálida sobre una almena de piedra, con una fila de faroles apagados que se "
              "pierde por el camino de ronda de una muralla al anochecer."),
    "16": gris("16", "El plano de las torres", "El plano del camino de ronda, con sus torres y el número de faroles que tiene pegados cada una.",
               ["Es el plano de los faroles (carta 14).", "Los cuadrados oscuros son torres; algunas llevan un número.",
                "El número cuenta los faroles en las casillas pegadas a la torre: arriba, abajo, a la izquierda y a la derecha."]),
    "18": gris("18", "La nota del archivero", "Una nota del archivero con dos frases sobre el orden de los sucesos de la ciudad.",
               ["Es parte de la crónica (carta 20).", "Son dos pistas del orden; las demás están en la crónica partida.",
                "Juntad estas dos pistas con las de la crónica: solo un orden las cumple todas."]),
    "19": pieza("19", "cronica", "Media lámina de la crónica de Altamuralla.", ["Es la mitad de una lámina: juntadla con la carta 21.",
                "Son pistas sobre el orden de los seis sucesos.", "La nota del archivero (carta 18) tiene otras dos."]),
    "21": pieza("21", "cronica", "Media lámina de la crónica de Altamuralla.", ["Es la mitad de una lámina: juntadla con la carta 19.",
                "Son pistas sobre el orden de los seis sucesos.", "La nota del archivero (carta 18) tiene otras dos."]),
    "20": app("20", "La crónica", "Es un juego de la app: los seis sucesos de la historia de Altamuralla, desordenados. Hay que ponerlos en el orden en "
              "que ocurrieron, del más antiguo al más reciente.", 28,
              ["Las pistas están en la nota del archivero (carta 18) y en la crónica partida (cartas 19 y 21).",
               "Apuntad seis huecos y colocad primero las pistas de «justo después»: son parejas pegadas. «Entre A y B hubo N sucesos» fija la "
               "distancia. Probad las pocas posiciones que quedan.",
               f"El orden: {_S_CRO}. Marca de la crónica: {_ME['marcas']['20']}."],
              SIN_GENTE + "Un archivo de piedra con estanterías llenas de legajos y un libro de crónicas enorme abierto sobre un atril, a la luz de una "
              "vela, con una ventana que da a la muralla."),
    "22": combinable("22", "La jaula del elevador", "azul", 35, 57, "La jaula de hierro del elevador de la muralla. Al torno le falta la manivela.",
                     SIN_GENTE + "Una jaula de elevador de hierro forjado colgada de cadenas junto al muro interior de una muralla, con un torno de "
                     "madera al que le falta la manivela, al atardecer."),
    "24": escena("24", "Los faroles encendidos", [26], [14, 16],
                 "Los faroles iluminan el camino de ronda como un collar de luces. La sargento sonríe por primera vez: «Así los colosos no se acercan "
                 "al muro». Os cuenta que de niña escuchaba su canto al anochecer, y os da la hoja donde lo apuntó (carta 26): «Si algún día habláis "
                 "con uno, os hará falta».",
                 ["Guardad la hoja de la sargento: servirá mucho más tarde."],
                 "El camino de ronda de una muralla de noche, iluminado por una larga fila de faroles cálidos que se pierde a lo lejos, con estrellas "
                 "sobre el valle. La sargento Ruth Albar (pelirroja con trenza, abrigo mostaza con galones) le da una hoja doblada a Cristina, que la "
                 "recibe emocionada con las dos manos; Alberto, apoyado en una almena, contempla los faroles con una sonrisa orgullosa de «lo hemos "
                 "hecho nosotros»."),
    "26": gris("26", "La hoja de la sargento", "La hoja que escribió la sargento de niña: un verso sobre cómo responder al canto de los colosos.",
               ["Sirve para el canto de los colosos (carta 51).", "Traduce uno de los cuatro sonidos y explica algo de la última ronda.",
                "La última ronda se responde al revés: de la última nota a la primera."]),
    "28": escena("28", "El archivo", [35], [18, 19, 20, 21],
                 "Con la crónica en orden, el archivero abre el cajón del suceso más antiguo. Dentro, envuelta en un trapo, está la manivela del "
                 "elevador (carta 35): «La escondí el día que llegó la doctora. Ella también quería bajar al valle».",
                 ["Mirad en el cajón del archivo."],
                 "Un archivo de piedra con estanterías de legajos. Un archivero anciano y menudo, con gafas en la punta de la nariz, abre un cajón "
                 "polvoriento del que saca una manivela de hierro envuelta en un trapo. Cristina se tapa la boca para no reírse con la nube de polvo; "
                 "Alberto estornuda con los ojos cerrados y las gafas de protección torcidas."),
    "35": combinable("35", "La manivela", "roja", 22, 57, "Una manivela de hierro gastada, envuelta en un trapo, con una campanita grabada.",
                     SIN_GENTE + "Una manivela de hierro gastada y envuelta a medias en un trapo, sobre una mesa de archivo de madera con legajos y "
                     "una vela."),
    "57": escena("57", "El elevador", [31, 32], [22, 35, 10, 28],
                 "La manivela encaja y la jaula baja chirriando hasta la ciudad. Abajo hay dos caminos: los barracones de la plaza, donde la gente se "
                 "refugia cada noche (carta 31), y la torre torcida de la doctora Olvido Marván, la única que estudia a los colosos (carta 32).",
                 ["Dos sitios: los barracones y la torre de la doctora."],
                 "Una jaula de elevador de hierro bajando por el muro interior de una muralla altísima, con la ciudad de tejados rojos iluminada abajo. "
                 "Dentro, Alberto gira la manivela con todas sus fuerzas, sudando y con la lengua fuera; Cristina, agarrada a los barrotes, mira hacia "
                 "abajo entusiasmada, con el pelo rizado al viento."),
    # ------------------------------------------------------------------ Rama 1: los barracones
    "31": escena("31", "Los barracones", [40, 41, 43, 45], [],
                 "En la plaza, el intendente se tira de los pelos: esta noche llegan familias de toda la muralla y no sabe cómo repartir los "
                 "barracones. Tiene su lista (carta 41), un plano a medio hacer (carta 43) y las normas de siempre (carta 45). «Si me ayudáis, os daré "
                 "algo que encontré junto al muro», promete.",
                 ["Un único puzle: el reparto de los barracones."],
                 "Una plaza empedrada de noche con barracones de madera alrededor y familias con fardos y faroles esperando. Un intendente bajito y "
                 "calvo, con un libro de cuentas bajo el brazo, se tira de los pelos. Cristina se agacha a hablar con una niña que lleva un gato en "
                 "brazos, sonriendo con ternura; Alberto, a su lado, examina el plano del intendente con el ceño fruncido de concentración."),
    "40": app("40", "Los barracones", "Es un juego de la app: el plano de los barracones de la plaza, de 6 x 6 camas. Hay que escribir en cada cama el "
              "tamaño del barracón al que pertenece, siguiendo las normas del intendente.", 30,
              ["Los números ya puestos están en la lista del intendente (carta 41) y en el plano (carta 43); las normas, en la carta 45.",
               "Un barracón de N camas es un grupo de N casillas pegadas, todas con el número N. Dos barracones del mismo tamaño no pueden tocarse "
               "por un lado. Empezad por los 1 (barracón de una sola cama) y por los números grandes que ya casi no tienen sitio para crecer.",
               f"El plano: {_S_BAR}. Marca de los barracones: {_ME['marcas']['40']}."],
              SIN_GENTE + "Un barracón de madera por dentro, con literas en fila, mantas de lana dobladas y faroles colgados, a la luz cálida de la "
              "noche."),
    "41": gris("41", "La lista del intendente", "La lista del intendente: algunas camas que ya sabe a qué tamaño de barracón pertenecen.",
               ["Son números del plano de los barracones (carta 40).", "Cada línea es una casilla (columna y fila) y su número.",
                "El resto de números ya puestos está en el plano a medio hacer (carta 43)."]),
    "43": gris("43", "El plano a medio hacer", "El plano de la plaza con algunos números ya escritos.",
               ["Son números del plano de los barracones (carta 40).", "Juntad estos números con los de la lista (carta 41).",
                "Las normas de los barracones están en la carta 45."]),
    "45": gris("45", "Las normas de los barracones", "Las normas de siempre del intendente, en verso.",
               ["Son las reglas del puzle de los barracones (carta 40).", "Cada barracón de N camas tiene N casillas con el número N.",
                "Dos barracones del mismo tamaño no se tocan por un lado (sí en diagonal)."]),
    "30": escena("30", "El regalo del intendente", [38], [31, 40, 41, 43, 45],
                 "Las familias entran en orden y el intendente cumple su palabra: os da la mitad de un cuerno de hueso enorme, tallado con flores "
                 "(carta 38). «Dicen que con él se llamaba a los colosos. La otra mitad se perdió en la ciudad el día del gran incendio».",
                 ["Mirad lo que os da el intendente."],
                 "La puerta de un barracón de madera de noche, con familias entrando abrigadas. El intendente, emocionado, le entrega a Alberto la "
                 "mitad de un cuerno de hueso enorme tallado con flores; Alberto lo sostiene con las dos manos, tambaleándose por el peso y con cara "
                 "de sorpresa; Cristina se ríe a carcajadas detrás de él."),
    "38": combinable("38", "Media cuerno", "roja", 56, 94, "La mitad de un cuerno de hueso enorme, tallado con flores de cinco pétalos.",
                     SIN_GENTE + "La mitad de un cuerno de hueso enorme, tallado con flores de cinco pétalos, partido limpiamente, sobre los "
                     "adoquines de una plaza a la luz de un farol."),
    # ------------------------------------------------------------------ Rama 2: la doctora
    "32": escena("32", "La torre de la doctora", [42, 48, 49, 53], [],
                 "La doctora Olvido Marván os abre con un matraz en la mano: «¿Queréis bajar al valle? Entonces leed esto». En su sótano hay una "
                 "piedra con frases en la lengua de un viajero que pasó por aquí hace cien años, partida en dos láminas, y su nota con lo que necesita "
                 "traducir (carta 53). Cada frase lleva la misma firma: una flor de cinco pétalos.",
                 ["Un único puzle: la inscripción del viajero.", "La piedra son dos cartas: juntadlas, una encima de otra."],
                 "Un sótano de piedra lleno de matraces, alambiques y plantas secas, con una losa de piedra grabada apoyada en la pared. La doctora "
                 "Olvido Marván (mujer de 60 años, pelo blanco en un moño con un lápiz, gafas redondas, delantal de cuero lleno de bolsillos con tubos) "
                 "sostiene un candil, entusiasmada. Cristina toca la flor de cinco pétalos grabada en la piedra, con la boca abierta de reconocimiento; "
                 "Alberto mira a Cristina de reojo, intrigado y un poco inquieto."),
    "48": app("48", "La inscripción del viajero", "Es un juego de la app: una piedra en blanco y doce signos de la lengua del viajero. Hay que escribir "
              "con ellos, en su orden, la frase que la doctora necesita traducir.", 36,
              ["Las frases del viajero con su traducción están en la piedra partida (cartas 42 y 49) y en la nota de la doctora (carta 53), que "
               "dice también qué frase hay que escribir.",
               "Comparad las frases: el signo que aparece en las mismas frases que una palabra es esa palabra. Fijaos en el orden: el viajero no "
               "escribe en el mismo orden que nosotros. Hay un signo para «no» y otro que se pone detrás de una palabra cuando hay más de uno.",
               f"La frase, signo a signo: {_S_INS}. Marca de la inscripción: {_ME['marcas']['48']}."],
              SIN_GENTE + "Una losa de piedra antigua grabada con signos geométricos desconocidos y una flor de cinco pétalos, a la luz de un candil, "
              "en un sótano lleno de matraces."),
    "42": pieza("42", "piedra", "Media lámina de la piedra del viajero.", ["Es la mitad de una lámina: juntadla con la carta 49.",
                "Cada frase en signos tiene debajo su traducción.", "La nota de la doctora (carta 53) tiene otra frase más."]),
    "49": pieza("49", "piedra", "Media lámina de la piedra del viajero.", ["Es la mitad de una lámina: juntadla con la carta 42.",
                "Cada frase en signos tiene debajo su traducción.", "La nota de la doctora (carta 53) tiene otra frase más."]),
    "53": gris("53", "La nota de la doctora", "La nota de la doctora: una frase más que ya tradujo y la que le falta por escribir.",
               ["Es la nota de la inscripción (carta 48).", "La frase de arriba ya está traducida: sirve de ejemplo.",
                "La frase de abajo es la que hay que escribir con los signos."]),
    "36": escena("36", "El suero", [52, 54, 55, 59], [32, 42, 48, 49, 53],
                 "«¡Los colosos no buscan el cristal!», lee la doctora. «No son peligrosos». Abre un armario: dos jeringuillas y un suero ámbar "
                 "destilado de la flor de cinco pétalos, que solo crece donde duermen los colosos. «Os convertirá en colosos durante una hora, pero la "
                 "dosis tiene que ser exacta». Su tabla de dosis está partida en dos láminas, y ya os ha pesado y medido (carta 59).",
                 ["Un único puzle: la dosis del suero.", "La tabla son dos cartas: juntadlas, una encima de otra."],
                 "Un laboratorio en lo alto de una torre torcida, con un armario abierto del que sale una luz ámbar: dos jeringuillas de cristal y "
                 "latón y un frasco de suero ámbar brillante con una flor de cinco pétalos dentro. La doctora Olvido Marván (pelo blanco en moño, "
                 "gafas redondas) sostiene el frasco con solemnidad. Cristina, de pie en una báscula antigua, sonríe nerviosa; Alberto mira la aguja "
                 "de la jeringuilla con cara de espanto y se aparta un paso."),
    "52": app("52", "La dosis", "Es un juego de la app: dos jeringuillas graduadas de 0 a 15 ml, una para Cristina y otra para Alberto. Hay que "
              "llenar cada una con la dosis exacta que dice la tabla de la doctora: mantened pulsado para llenar.", 44,
              ["La tabla está en dos láminas (cartas 54 y 55) y el peso y la estatura de cada uno, en la báscula y la vara (carta 59).",
               "Leed en la báscula el peso y en la vara la estatura de cada uno. La fila de la tabla es la del peso (de ese número a cuatro más) y "
               "la columna, la de la estatura (de ese número a nueve más).",
               f"{_S_DOS}. Marca de la dosis: {_ME['marcas']['52']}."],
              SIN_GENTE + "Dos jeringuillas antiguas de cristal y latón, graduadas, junto a un frasco de suero ámbar brillante con una flor de cinco "
              "pétalos dentro, sobre una mesa de laboratorio."),
    "54": pieza("54", "dosis", "Media lámina de la tabla de dosis de la doctora.", ["Es la mitad de una lámina: juntadla con la carta 55.",
                "Las filas son pesos y las columnas, estaturas.", "El peso y la estatura de cada uno están en la carta 59."]),
    "55": pieza("55", "dosis", "Media lámina de la tabla de dosis de la doctora.", ["Es la mitad de una lámina: juntadla con la carta 54.",
                "Las filas son pesos y las columnas, estaturas.", "El peso y la estatura de cada uno están en la carta 59."]),
    "59": gris("59", "La báscula y la vara", "La báscula de la doctora y su vara de medir, con las marcas de Cristina y de Alberto.",
               ["Sirve para la dosis (carta 52).", "Cada aguja de la báscula marca un peso; cada raya de la vara, una estatura.",
                "Leed con cuidado: cada rayita pequeña de la báscula es 1 kg y cada una de la vara, 1 cm."]),
    # ------------------------------------------------------------------ Acto 2: colosos
    "44": escena("44", "¡Colosos!", [33, 37, 39, 46, 51, 61, 63], [36, 52, 54, 55, 59],
                 "Un pinchazo, un calor dorado... y el suelo se aleja. Medís quince metros, con vuestra cara y los abrigos agrandados, y os sale vapor "
                 "ámbar de los hombros. «¡Soy enorme!», ríe Alberto, y casi tira una chimenea. Para llegar a la puerta grande hay que cruzar la plaza "
                 "pisando solo cobertizos vacíos (cartas 37, 33 y 39). Y desde el valle os llega un canto: el cancionero de la doctora os ayudará a "
                 "responder.",
                 ["Hay dos puzles: las pisadas y el canto de los colosos."],
                 GIGANTES + "de pie en medio de una ciudad de tejados rojos al anochecer, con las casas a la altura de sus rodillas y nubes de vapor "
                 "dorado saliendo de sus hombros. Alberto, gigante, se mira las manos enormes con una carcajada incrédula mientras roza una chimenea "
                 "con el codo; Cristina, gigante, se agacha con cuidado y una sonrisa maravillada hacia la doctora y la sargento, diminutas en la "
                 "plaza, que les saludan con pañuelos."),
    "46": app("46", "Las pisadas", "Es un juego de la app: la plaza vista desde arriba, con 6 x 6 tejados. Hay que marcar los cobertizos vacíos que "
              "pisaréis para cruzarla, siguiendo las tres reglas del paso del coloso.", 56,
              ["Los números de los tejados están en dos cartas (37 y 33) y las reglas, en la 39.",
               "En cada fila y en cada columna, los tejados que NO piséis no pueden repetir número. Dos pisadas no pueden estar pegadas por un lado, "
               "y las casas que queden sin pisar tienen que seguir unidas entre sí. Si una casilla está entre dos números iguales en su fila, "
               "la del medio no se pisa.",
               f"Pisadas en: {_S_PIS}."],
              SIN_GENTE + "Una plaza de una ciudad medieval vista desde muy arriba, con tejados rojos de distintas formas, chimeneas y cobertizos de "
              "madera, al anochecer, con la sombra enorme de un pie gigante sobre los adoquines."),
    "37": gris("37", "Los tejados del norte", "Las tres primeras filas de tejados de la plaza, cada uno con su número.",
               ["Son las filas 1 a 3 de las pisadas (carta 46).", "Las filas 4 a 6 están en la carta 33.", "Las reglas del paso del coloso, en la 39."]),
    "33": gris("33", "Los tejados del sur", "Las tres últimas filas de tejados de la plaza, cada uno con su número.",
               ["Son las filas 4 a 6 de las pisadas (carta 46).", "Las filas 1 a 3 están en la carta 37.", "Las reglas del paso del coloso, en la 39."]),
    "39": gris("39", "El paso del coloso", "Las tres reglas del paso del coloso, en verso, de la libreta de la doctora.",
               ["Son las reglas de las pisadas (carta 46).", "No se repite un número sin pisar en una fila ni en una columna.",
                "Dos pisadas nunca juntas por un lado, y la ciudad sin pisar, toda unida."]),
    "56": combinable("56", "La otra mitad del cuerno", "roja", 38, 94, "La otra mitad del cuerno de hueso, que asomaba entre las tablas de un cobertizo.",
                     SIN_GENTE + "La mitad de un cuerno de hueso tallado con flores de cinco pétalos, asomando entre las tablas rotas de un cobertizo "
                     "de madera, entre adoquines."),
    "51": app("51", "El canto de los colosos", "Es un juego de la app: los colosos del valle cantan con cuatro sonidos. Hay que responderles con las "
              "cuatro palabras de su lengua, sonido a sonido, en tres rondas.", 58,
              ["La traducción está repartida entre la hoja de la sargento (carta 26) y el cancionero de la doctora (cartas 61 y 63).",
               "Cada sonido se responde siempre con la misma palabra. Escuchad (o mirad) la ronda entera, traducidla y responded. La hoja de la "
               "sargento dice qué pasa en la última ronda.",
               f"La traducción: {_S_TRA}. La última ronda, al revés. Respuestas: {_S_CAN}."],
              SIN_GENTE + "Un valle verde con niebla al anochecer, con varios colosos de piedra y musgo sentados en corro con la cabeza levantada "
              "hacia la luna, cantando."),
    "61": pieza("61", "cancionero", "Media lámina del cancionero de la doctora.", ["Es la mitad de una lámina: juntadla con la carta 63.",
                "Traduce sonidos de los colosos a palabras.", "Uno de los cuatro sonidos lo traduce la hoja de la sargento (carta 26)."]),
    "63": pieza("63", "cancionero", "Media lámina del cancionero de la doctora.", ["Es la mitad de una lámina: juntadla con la carta 61.",
                "Traduce sonidos de los colosos a palabras.", "Uno de los cuatro sonidos lo traduce la hoja de la sargento (carta 26)."]),
    "58": escena("58", "El valle", [69, 70, 71], [51, 61, 63, 26, 24],
                 "Respondéis al canto y los colosos se apartan despacio, como una manada de vacas gigantes. Al fondo del valle, sentado entre ruinas, "
                 "el Coloso Viejo, con barba de musgo, mira el cielo. Delante tiene un montón de piedras: solo acepta ofrendas de tres piedras, a su "
                 "manera. La doctora apuntó cuáles acepta (carta 70), y en su cuaderno hay más (carta 71).",
                 ["Un único puzle: las ofrendas."],
                 GIGANTES + "caminando por un valle verde con niebla entre colosos de piedra y musgo que se apartan con calma, bostezando. Al fondo, "
                 "sentado entre ruinas, un coloso anciano con barba de musgo. Cristina, gigante, saluda a un coloso con la mano y una sonrisa cálida; "
                 "Alberto, gigante, camina de puntillas con cara de no querer pisar a nadie, mordiéndose el labio."),
    "69": app("69", "Las ofrendas", "Es un juego de la app: seis ofrendas nuevas de tres piedras cada una. Hay que elegir todas las que aceptaría el "
              "Coloso Viejo, y ninguna más.", 80,
              ["Las ofrendas que aceptó y las que rechazó están en las cartas 70 y 71.",
               "El Coloso Viejo sigue una sola regla, que mira el color o la forma de las piedras y su sitio. Comparad las aceptadas con las "
               "rechazadas que más se les parecen: ¿qué cambia? Las del cuaderno (carta 71) descartan las reglas que parecían buenas.",
               f"La regla: {_OF['regla']}. Acepta las ofrendas {_S_OFR}."],
              SIN_GENTE + "Un montón de piedras de colores (rojas, azules y blancas, unas redondas y otras puntiagudas) junto a la mano enorme de "
              "un coloso de piedra y musgo, en unas ruinas cubiertas de hierba."),
    "70": gris("70", "Las ofrendas de la doctora", "Las ofrendas que la doctora vio aceptar y rechazar al Coloso Viejo.",
               ["Son ejemplos para las ofrendas (carta 69).", "El signo dice si las aceptó o las rechazó.",
                "Hay más ejemplos en el cuaderno de la doctora (carta 71)."]),
    "71": gris("71", "El cuaderno de la doctora", "Tres ofrendas más del cuaderno de la doctora.",
               ["Son más ejemplos para las ofrendas (carta 69).", "Sin ellas, varias reglas parecen buenas.",
                "Fijaos en la forma de las piedras, además del color."]),
    "80": escena("80", "El Coloso Viejo", [72, 75, 79], [58, 69, 70, 71],
                 "El Coloso Viejo acepta vuestras ofrendas, sonríe con la boca llena de musgo y os señala la Torre del Reloj abandonada, en medio del "
                 "valle. La puerta se abre con cuatro palancas que solo un coloso puede mover; las instrucciones están en dos placas de latón (cartas "
                 "75 y 79).",
                 ["Un único puzle: las palancas de la torre."],
                 GIGANTES + "frente a un coloso anciano de piedra con barba de musgo que les señala con un dedo enorme una torre de reloj en ruinas "
                 "en medio del valle. Cristina, gigante, le ofrece tres piedras de colores en la palma de la mano con una sonrisa respetuosa; Alberto, "
                 "gigante, se rasca la cabeza mirando la torre con curiosidad de ingeniero."),
    "72": app("72", "Las palancas de la torre", "Es un juego de la app: la maquinaria de la Torre del Reloj tiene una esfera y cuatro palancas con "
              "dibujos. En cada una de las cinco etapas hay que tirar de la palanca correcta; si os equivocáis, todo vuelve a empezar.", 82,
              ["Las instrucciones están en dos placas: etapas 1 a 3 (carta 75) y etapas 4 y 5 (carta 79).",
               "En cada etapa, mirad el número de la esfera y buscad su línea en la placa. Apuntad siempre qué palanca pulsáis: su sitio (1.ª a "
               "4.ª, de izquierda a derecha) y su dibujo, porque las etapas siguientes os los pedirán. Al fallar, la esfera cambia.",
               "Las placas dicen, etapa a etapa: " + " · ".join(
                   f"etapa {e + 1}: " + "; ".join(f"esfera {d + 1}, {I.texto_regla(r)}" for d, r in enumerate(_PA["reglas"][e])) for e in range(5))],
              SIN_GENTE + "La maquinaria de una torre de reloj antigua por dentro, con engranajes de bronce gigantes, una esfera grande y cuatro "
              "palancas de hierro enormes, iluminada por la luz que entra por las grietas."),
    "75": gris("75", "La primera placa", "Una placa de latón con las instrucciones de las etapas 1, 2 y 3.",
               ["Son las instrucciones de las palancas (carta 72).", "Cada etapa tiene una línea por cada número de la esfera.",
                "Las etapas 4 y 5 están en la otra placa (carta 79)."]),
    "79": gris("79", "La segunda placa", "Una placa de latón con las instrucciones de las etapas 4 y 5.",
               ["Son las instrucciones de las palancas (carta 72).", "Algunas os piden recordar lo que pulsasteis antes.",
                "Las etapas 1 a 3 están en la otra placa (carta 75)."]),
    "82": escena("82", "La cámara del viajero", [85, 86, 87], [80, 72, 75, 79],
                 "Las palancas giran y la torre se abre. Dentro no hay tesoros: hay una cámara redonda con anillos de latón, como el Cronoportal, y en "
                 "la pared, la flor de cinco pétalos. «El viajero estuvo aquí», susurra Cristina. Hay una inscripción en rejilla (carta 86) y una "
                 "placa con cinco dibujos (carta 87): un panel para volver a casa. Pero sin el cristal, no se enciende.",
                 ["Un único puzle: el panel del viajero.", "Hace falta el cristal antes de usar el panel."],
                 GIGANTES + "agachados para asomarse a una cámara redonda dentro de una torre de reloj en ruinas, con anillos de latón en las paredes "
                 "como un portal antiguo y una flor de cinco pétalos grabada que brilla en azul. Cristina, gigante, tiene los ojos húmedos de emoción "
                 "y la mano en el pecho; Alberto, gigante, mira los anillos boquiabierto, con las gafas de protección bajadas."),
    # ------------------------------------------------------------------ Acto 3: el tesoro y la vuelta
    "94": escena("94", "El Gran Cuerno", [64, 66, 67], [38, 56, 30, 44, 33, 37, 39, 46],
                 "Las dos mitades encajan, y el cuerno suena como un canto de coloso. El Coloso Viejo se levanta y vuelca ante vosotros su tesoro: "
                 "dieciséis baratijas brillantes recogidas durante años (carta 66). Vuestro cristal está ahí, pero solo os lo dará si ordenáis su "
                 "colección como él la ordena (carta 67).",
                 ["Un único puzle: el tesoro del Coloso Viejo."],
                 GIGANTES + "en un valle al anochecer. Alberto, gigante, sopla con los mofletes hinchados un cuerno de hueso tallado con flores; "
                 "Cristina, gigante, se tapa los oídos riendo. Delante, un coloso anciano con barba de musgo vuelca con cuidado un cesto de baratijas "
                 "brillantes (anillos, monedas, llaves y campanitas) entre las que asoma un destello azul."),
    "64": app("64", "El tesoro del Coloso Viejo", "Es un juego de la app: dieciséis baratijas, de la A a la P. Hay que separarlas en los cuatro grupos de "
              "cuatro en que las ordena el Coloso Viejo.", 62,
              ["Las baratijas, con su material y sus muescas, están en la carta 66; cómo las agrupa el Coloso Viejo, en la 67.",
               "Cada baratija va en un solo grupo y cada grupo tiene exactamente cuatro. Algunas cumplen dos condiciones a la vez: colocad primero "
               "las que solo cumplen una y luego repartid las dudosas para que salgan cuatro y cuatro.",
               f"Los grupos: {_S_TES}."],
              SIN_GENTE + "Un montón de baratijas brillantes (anillos, monedas, llaves y campanitas de oro, plata, cobre y vidrio) sobre la palma "
              "abierta de una mano enorme de piedra y musgo."),
    "66": gris("66", "Las baratijas", "Las dieciséis baratijas del Coloso Viejo, con su letra, su material y sus muescas.",
               ["Son las baratijas del tesoro (carta 64).", "El color dice el material; las rayitas del borde son las muescas.",
                "Cómo las agrupa el Coloso Viejo está en la carta 67."]),
    "67": gris("67", "Cómo ordena el Coloso Viejo", "Las cuatro maneras en que el Coloso Viejo ordena su tesoro, apuntadas por la doctora.",
               ["Son los cuatro grupos del tesoro (carta 64).", "Cada línea describe un grupo de cuatro baratijas.",
                "Alguna baratija cumple dos líneas: solo cabe en una."]),
    "62": combinable("62", "El cristal del Cronoportal", "roja", 12, 74, "El cristal de energía del Cronoportal, azul y brillante, sin un rasguño.",
                     SIN_GENTE + "Un cristal de energía azul brillante, facetado, con destellos dorados, entre baratijas de oro, plata y cobre sobre la "
                     "palma de una mano enorme de piedra cubierta de musgo."),
    "74": escena("74", "El cristal en su sitio", [], [62, 12, 64, 66, 67, 94, 57],
                 "El Coloso Viejo os da el cristal con dos dedos, con muchísimo cuidado. Al encajarlo en el Cronoportal, se acaba la hora del suero: "
                 "una nube de vapor dorado y volvéis a vuestro tamaño. La doctora y la sargento llegan corriendo para despediros. «Contadle al mundo "
                 "que los colosos cantan», pide la doctora. Ahora, el panel del viajero.",
                 ["Ya solo queda el panel del viajero."],
                 "Una cámara redonda con anillos de latón dentro de una torre en ruinas, envuelta en vapor dorado. Cristina y Alberto, ya de tamaño "
                 "normal y con los abrigos mostaza, encajan el cristal azul en el Cronoportal, que se ilumina. La doctora Olvido Marván (pelo blanco, "
                 "gafas redondas) abraza a Cristina, que ríe con lágrimas; la sargento Ruth Albar (pelirroja con trenza) estrecha la mano de Alberto, "
                 "que sonríe con timidez. Por la puerta asoma el ojo ámbar enorme y bonachón del Coloso Viejo."),
    "85": app("85", "El panel del viajero", "Es un juego de la app: el panel de la cámara del viajero tiene un teclado de letras. Hay que escribir la "
              "palabra de cinco letras que esconde la inscripción, con las marcas que os dejaron cinco puzles.", 99,
              ["La inscripción está en la carta 86 y el orden de las cinco marcas, en la 87.",
               "Cinco puzles os dieron una marca de dos cifras: la primera cifra es la fila de la inscripción y la segunda, la columna. Leed las "
               "letras en el orden de los dibujos de la carta 87.",
               f"Las marcas, en orden: {_S_MET}. La palabra es {_ME['palabra']}."],
              SIN_GENTE + "Un panel de latón con un teclado de letras antiguas y una flor de cinco pétalos en el centro, en la pared de una cámara "
              "redonda con anillos de latón que brillan en azul."),
    "86": gris("86", "La inscripción de la cámara", "La inscripción del viajero, letra a letra, en una rejilla con las filas y las columnas numeradas.",
               ["Es la inscripción del panel (carta 85).", "Cada marca de dos cifras es una casilla: fila y columna.",
                "El orden de las marcas está en la carta 87."]),
    "87": gris("87", "La placa de los cinco dibujos", "Una placa con cinco dibujos en fila, uno por cada puzle que dejó una marca.",
               ["Es el orden de las letras del panel (carta 85).", "Cada dibujo es uno de los puzles que os dio una marca.",
                "Leed las letras de las marcas en el orden de los dibujos, de izquierda a derecha."]),
    "99": escena("99", "De vuelta a casa (FIN)", [], [74, 82, 85, 86, 87],
                 "El anillo se enciende en azul y oro y aparecéis en el salón de casa, aún con los abrigos de la guardia. Alberto se mira las manos: "
                 "tamaño normal. Cristina saca de su bolsillo una flor de cinco pétalos seca. «El viajero nos dejó el camino», dice. «¿Y si quería que "
                 "lo siguiéramos?». ¡Fin!",
                 [],
                 "El salón de una casa actual de noche, con un sofá, una lámpara encendida y el Cronoportal en el centro, cuyo anillo se apaga con las "
                 "últimas chispas azules y doradas. Cristina y Alberto acaban de llegar por el portal, aún con los abrigos mostaza de la guardia. "
                 "Alberto se mira las manos a tamaño normal con un alivio cómico, soltando el aire; Cristina, sentada en el brazo del sofá, contempla "
                 "pensativa y con una media sonrisa una flor seca de cinco pétalos en la palma de la mano. Por la ventana se ve llover."),
}

META = dict(juego="Altamuralla: El Valle de los Colosos", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()})

SPEC = dict(final="99", needs={
    "24": ["14", "16"], "28": ["20", "18", "19", "21"], "57": ["22", "35"], "30": ["40", "41", "43", "45"], "36": ["48", "42", "49", "53"],
    "44": ["52", "54", "55", "59"], "56": ["46", "37", "39", "33"], "58": ["51", "26", "61", "63"], "80": ["69", "70", "71"], "94": ["38", "56"],
    "62": ["64", "66", "67"], "82": ["72", "75", "79"], "74": ["12", "62"], "99": ["85", "86", "87", "74"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_M = _ME["marcas"]
_T = [
    ("leer", "P", "Llegada", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12."),
    ("leer", "10", "El camino de ronda", "Lee la carta 10. Descarta la P y coge 14, 16, 18, 19, 20, 21 y 22."),
    ("app", "14", "Los faroles", f"En el móvil: Acción, 14. Con el plano de las torres (16), pon faroles en {_S_FAR}. El mensaje te dice que cojas la 24. "
     f"Anota la marca de los faroles: {_M['14']}.", "carta 24"),
    ("leer", "24", "Los faroles encendidos", "Lee la carta 24. Descarta 14 y 16 y coge la 26 (guárdala para el canto)."),
    ("app", "20", "La crónica", f"En el móvil: Acción, 20. Con la nota (18) y la crónica (19 y 21): {_S_CRO}. El mensaje te dice que cojas la 28. Anota la "
     f"marca de la crónica: {_M['20']}.", "carta 28"),
    ("leer", "28", "El archivo", "Lee la carta 28. Descarta 18, 19, 20 y 21 y coge la 35."),
    ("combinar", "22", "35", "El elevador", "La jaula (22) y la manivela (35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El elevador", "Lee la carta 57. Descarta 22, 35, 10 y 28 y coge 31 y 32."),
    ("leer", "31", "Los barracones", "Lee la carta 31. Coge 40, 41, 43 y 45."),
    ("app", "40", "Los barracones", f"En el móvil: Acción, 40. Con la lista (41), el plano (43) y las normas (45): {_S_BAR}. El mensaje te dice que cojas "
     f"la 30. Anota la marca de los barracones: {_M['40']}.", "carta 30"),
    ("leer", "30", "El regalo del intendente", "Lee la carta 30. Descarta 31, 40, 41, 43 y 45 y coge la 38."),
    ("leer", "32", "La torre de la doctora", "Lee la carta 32. Coge 42, 48, 49 y 53."),
    ("app", "48", "La inscripción", f"En el móvil: Acción, 48. Con la piedra (42 y 49) y la nota (53), escribe los signos de: {_S_INS}. El mensaje te dice "
     f"que cojas la 36. Anota la marca de la inscripción: {_M['48']}.", "carta 36"),
    ("leer", "36", "El suero", "Lee la carta 36. Descarta 32, 42, 48, 49 y 53 y coge 52, 54, 55 y 59."),
    ("app", "52", "La dosis", f"En el móvil: Acción, 52. Con la tabla (54 y 55) y la báscula (59): {_S_DOS}. El mensaje te dice que cojas la 44. Anota la "
     f"marca de la dosis: {_M['52']}.", "carta 44"),
    ("leer", "44", "¡Colosos!", "Lee la carta 44. Descarta 36, 52, 54, 55 y 59 y coge 33, 37, 39, 46, 51, 61 y 63."),
    ("app", "46", "Las pisadas", f"En el móvil: Acción, 46. Con los tejados (37 y 33) y las reglas (39), pisa {_S_PIS}. El mensaje te dice que cojas la 56.",
     "carta 56"),
    ("app", "51", "El canto", f"En el móvil: Acción, 51. Con la hoja de la sargento (26) y el cancionero (61 y 63): {_S_TRA}; la última ronda, al revés. "
     f"Respuestas: {_S_CAN}. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "El valle", "Lee la carta 58. Descarta 51, 61, 63, 26 y 24 y coge 69, 70 y 71."),
    ("app", "69", "Las ofrendas", f"En el móvil: Acción, 69. Con las ofrendas (70 y 71), la regla es «{_OF['regla']}»: elige las ofrendas {_S_OFR}. El "
     "mensaje te dice que cojas la 80.", "carta 80"),
    ("leer", "80", "El Coloso Viejo", "Lee la carta 80. Descarta 58, 69, 70 y 71 y coge 72, 75 y 79."),
    ("app", "72", "Las palancas", "En el móvil: Acción, 72. Con las placas (75 y 79), en cada etapa mira la esfera y tira de la palanca que diga su línea, "
     "apuntando el sitio y el dibujo de cada una. El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "La cámara del viajero", "Lee la carta 82. Descarta 80, 72, 75 y 79 y coge 85, 86 y 87."),
    ("combinar", "38", "56", "El Gran Cuerno", "Las dos mitades del cuerno (38 y 56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "El Gran Cuerno", "Lee la carta 94. Descarta 38, 56, 30, 44, 33, 37, 39 y 46 y coge 64, 66 y 67."),
    ("app", "64", "El tesoro", f"En el móvil: Acción, 64. Con las baratijas (66) y las condiciones (67): {_S_TES}. El mensaje te dice que cojas la 62.",
     "carta 62"),
    ("combinar", "12", "62", "El cristal", "El Cronoportal (12) y el cristal (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "El cristal en su sitio", "Lee la carta 74. Descarta 62, 12, 64, 66, 67, 94 y 57."),
    ("app", "85", "El panel del viajero", f"En el móvil: Acción, 85. Con la inscripción (86) y la placa (87), las marcas en orden son {_S_MET}: escribe "
     f"{_ME['palabra']}. El mensaje te dice que cojas la 99.", "carta 99"),
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

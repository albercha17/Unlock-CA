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

J = {
    "P": dict(
        titulo="Carta P — Llegada al taller", tipo="gris", coge=[20, 22],
        descripcion=[
            "Cristina y Alberto estrenan una nueva parada del Cronoportal: Florencia, año 1503. Cristina siempre ha soñado con ver el taller de Leonardo da Vinci.",
            "El salto vuelve a salir mal: aterrizáis de noche en el taller del maestro, que está fuera, y el Cronoportal se queda sin energía. Alberto calcula que solo hay una forma de recargarlo: concentrar con una lente perfecta la primera luz del amanecer, que llegará dentro de una hora.",
            "Coged las cartas 20 y 22."],
        pistas=["Mirad a vuestro alrededor y revisad el aparato.", "Coged las cartas 20 y 22."],
        arte="Taller de un genio renacentista en Florencia, de noche, con mesas llenas de maquetas de madera, bocetos clavados en las paredes y un ornitóptero de madera colgado del techo. En el suelo, una consola de latón y cristal de aspecto retrofuturista (el Cronoportal) humea con una luz azul que se apaga. Cristina y Alberto, con ropa florentina, se levantan desconcertados a la luz de las velas."),
    "20": dict(
        titulo="Carta 20 — Taller de Leonardo", tipo="gris", coge=[24, 26, 28], descarta=["P"],
        descripcion=[
            "El taller: caballetes, maquetas, dibujos de anatomía y de máquinas. Sobre una mesa hay un cuaderno escrito al revés (carta 26); junto a la chimenea, un cofre de roble con cuatro ruedas numeradas (carta 24); y clavada en la pared, una nota con la letra apresurada de Salaì, el aprendiz de Leonardo (carta 28).",
            "Coged las cartas 24, 26 y 28. Descartad la carta P."],
        pistas=["Fijaos en la mesa, en la chimenea y en la pared.", "Coged las cartas 24, 26 y 28. Descartad la carta P."],
        arte="Gran taller renacentista iluminado por velas y un fuego bajo en la chimenea: una mesa con un cuaderno abierto, un cofre de roble con cuatro ruedas de latón junto a la chimenea y una nota clavada en la pared. Cristina examina el cofre y Alberto revisa el cuaderno con curiosidad."),
    "22": dict(
        titulo="Carta 22 — Cronoportal sin energía", tipo="azul", combina=[62, 84],
        descripcion=[
            "El Cronoportal: una consola de latón y cristal con un anillo central apagado y un indicador de batería casi vacío (un 2 %). Alberto lo tiene claro: «Necesito luz del amanecer concentrada por una lente de cristal perfecta».",
            "Cuando tengáis la lente maestra (carta 62), combinadla con el Cronoportal: sumad sus números (22 + 62 = 84) y coged la carta 84."],
        pistas=["Necesita una lente muy especial y la luz del amanecer.", "Combinad la carta 22 con la carta 62.", "Sumad los números de las dos cartas: 22 + 62 = 84."],
        arte="Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo de cristal central apagado y un indicador de batería casi vacío con una luz roja tenue, sobre una mesa de madera de taller."),
    "24": dict(
        titulo="Carta 24 — Cofre del maestro", tipo="verde",
        descripcion=[
            "Es un juego de la app: un cofre de roble con cuatro ruedas numeradas, que se abre con una combinación de cuatro cifras. El cuaderno de Leonardo (carta 26) la da, pero escrita como escribía él: al revés, en espejo.",
            "Al abrirlo, aparece lo que guardaba. Coged la carta 30."],
        pistas=["Leonardo escribía al revés para que nadie lo leyera.", "Leed el cuaderno (carta 26) ante un espejo, o con la cámara frontal del móvil apuntando a la pantalla o a la carta.", "La combinación es 2759."],
        arte="Primer plano de un cofre de roble con herrajes de hierro y cuatro ruedas numeradas de latón en la cerradura, sobre una mesa de taller, con luz de vela."),
    "26": dict(
        titulo="Carta 26 — Cuaderno de Leonardo", tipo="gris", textoEspejo=True,
        descripcion=["Un cuaderno abierto con la escritura en espejo de Leonardo, de derecha a izquierda: para leerlo hay que ponerlo frente a un espejo. Da la combinación del cofre (carta 24)."],
        pistas=["Leonardo escribía al revés. Usad un espejo o la cámara frontal del móvil.", "Es la combinación del cofre (carta 24)."],
        textoCarta=["Salaì, no mires: el cofre", "se abre con cuatro ruedas:", "DOS, SIETE, CINCO, NUEVE."],
        arte="Un cuaderno de papel viejo abierto sobre una mesa de madera, con bocetos de máquinas voladoras y columnas de escritura en espejo decorativa sin significado legible, junto a un tintero y una pluma."),
    "28": dict(
        titulo="Carta 28 — Nota de Salaì", tipo="gris",
        descripcion=["Una nota apresurada de Salaì, el aprendiz: explica cómo coloca siempre Leonardo el disco de cifrado. Sirve para el disco de Alberti (carta 32)."],
        pistas=["Fijaos en cómo se coloca el disco.", "Sirve para el disco de Alberti (carta 32)."],
        textoCarta=["Disco de Alberti: el maestro", "lo pone siempre con la A de fuera", "sobre la F de dentro."],
        arte="Una nota de papel clavada en una viga de madera con garabatos y manchas de tinta, junto a un disco de cobre con dos anillos de letras apoyado en la mesa; sin texto legible."),
    "30": dict(
        titulo="Carta 30 — Interior del cofre", tipo="gris", coge=[32, 35], descarta=[24, 26, 20],
        descripcion=[
            "Las cuatro ruedas encajan y el cofre se abre. Dentro hay un disco de cobre con dos anillos de letras (carta 32) y un pergamino con un mensaje de letras sin sentido (carta 35).",
            "Coged las cartas 32 y 35. Descartad las cartas 24, 26 y 20."],
        pistas=["Mirad lo que había dentro.", "Coged las cartas 32 y 35. Descartad las cartas 24, 26 y 20."],
        arte="El cofre de roble abierto: dentro, un disco de cobre con dos anillos concéntricos de letras decorativas sobre terciopelo rojo y un pergamino enrollado con un lacre. Cristina y Alberto se asoman con asombro."),
    "32": dict(
        titulo="Carta 32 — Disco de Alberti", tipo="verde",
        descripcion=[
            "Es un juego de la app: un disco de cobre con dos anillos de letras, el invento de cifrado de Leon Battista Alberti. Hay que colocarlo como indica la nota de Salaì (carta 28), descifrar el pergamino (carta 35) y escribir el nombre del guardián del taller.",
            "Al acertar, se abre un escondite. Coged la carta 36."],
        pistas=["Colocad el disco como dice la nota de Salaì.", "Por cada letra del pergamino, mirad cuál queda justo enfrente en el otro anillo.", "El mensaje dice: EL LEON GUARDA SU CORAZON. El guardián es el LEON."],
        arte="Primer plano de un disco de cifrado renacentista de cobre con dos anillos concéntricos de letras grabadas decorativas, uno de ellos girado, sobre un pergamino enrollado, con luz de vela."),
    "35": dict(
        titulo="Carta 35 — Pergamino cifrado", tipo="gris",
        descripcion=["Un pergamino con un mensaje en letras sin sentido: está cifrado con el disco de Alberti. Sirve para el disco (carta 32)."],
        pistas=["Es un mensaje cifrado.", "Sirve para el disco de Alberti (carta 32)."],
        textoCarta=["JQ QJTS", "LZFWIF XZ", "HTWFETS"],
        arte="Un pergamino desenrollado con un lacre rojo roto y filas de letras de aspecto antiguo (decorativas, sin significado legible), sobre una mesa de madera junto a una pluma."),
    "36": dict(
        titulo="Carta 36 — El león mecánico", tipo="gris", coge=[38, 40, 42], descarta=[30, 32, 35, 28],
        descripcion=[
            "Al decir el nombre del guardián se abre una trampilla bajo la ventana y aparece un león mecánico de madera y bronce con la panza abierta: dentro hay un mecanismo de engranajes (carta 38), un plano pegado a la tapa (carta 40) y una llave de cuerda (carta 42).",
            "Coged las cartas 38, 40 y 42. Descartad las cartas 30, 32, 35 y 28."],
        pistas=["Mirad dentro del león.", "Coged las cartas 38, 40 y 42. Descartad las cartas 30, 32, 35 y 28."],
        arte="Un león mecánico de tamaño natural, de madera y bronce, junto a una ventana del taller, con la panza abierta que deja ver un mecanismo de engranajes, un plano pegado a la tapa y una gran llave de bronce. Cristina y Alberto lo observan maravillados."),
    "38": dict(
        titulo="Carta 38 — Mecanismo del león", tipo="verde",
        descripcion=[
            "Es un juego de la app: un panel con clavijas y una bandeja de ruedas dentadas. Hay que montar una cadena de engranajes entre la manivela y la cuerda del reloj interno. El plano (carta 40) dice cómo debe girar la cuerda.",
            "Al acertar, el mecanismo arranca y una esfera marca un número: un modificador. Sumadlo a la llave de cuerda (carta 42) y coged la carta con esa suma."],
        pistas=["Dos ruedas solo engranan si se tocan justo por los bordes: la distancia entre sus clavijas es la suma de sus radios.", "Mirad el plano (carta 40): ¿cómo debe girar la cuerda respecto a la manivela?", "Hay dos cadenas posibles. La que hace girar la cuerda igual de rápido y al revés es: rueda pequeña en D, mediana en B y mediana en Z."],
        arte="Primer plano del mecanismo interior de un león mecánico: un panel de madera con clavijas de latón, varias ruedas dentadas de bronce de distintos tamaños engranadas entre sí y una manivela, con luz cálida de vela."),
    "40": dict(
        titulo="Carta 40 — Plano del mecanismo", tipo="gris",
        descripcion=["Un plano pegado a la tapa del león mecánico: indica cómo debe girar la cuerda del reloj interno. Sirve para el mecanismo (carta 38)."],
        pistas=["Es el objetivo del mecanismo.", "Sirve para el mecanismo del león (carta 38)."],
        textoCarta=["La cuerda del reloj debe girar", "igual de rápido que la manivela", "pero en sentido contrario."],
        arte="Un plano dibujado a tinta sobre papel, con círculos de distintos tamaños unidos por flechas curvas que indican giros, pegado en la tapa de madera de un autómata; sin texto legible."),
    "42": dict(
        titulo="Carta 42 — Llave de cuerda", tipo="roja", combina=["+9", 51],
        descripcion=[
            "Una gran llave de bronce para dar cuerda al león. Se combina con el modificador que dé el mecanismo (carta 38): sumad la llave y el modificador y coged la carta con esa suma.",
            "El mecanismo os dirá qué número sumar."],
        pistas=["Es una llave: necesita un número que sale del mecanismo del león.", "Resolved el mecanismo (carta 38): os dirá qué número sumar.", "El modificador es +9: 42 + 9 = 51."],
        arte="Una gran llave de bronce con un anillo ornamental y un paletón en forma de estrella, sobre un cojín de terciopelo rojo, con luz de vela."),
    "51": dict(
        titulo="Carta 51 — El altillo", tipo="gris", coge=[54, 56, 58, 60], descarta=[36, 38, 40, 42],
        descripcion=[
            "El león ruge, arranca y su lomo se abre a una escalera: el altillo. Allí hay una caja de nogal con un cierre numérico (carta 54) junto a un boceto del matemático Luca Pacioli, amigo de Leonardo (carta 56), y una trampilla sobre una cisterna (carta 58) con una nota clavada (carta 60).",
            "Coged las cartas 54, 56, 58 y 60. Descartad las cartas 36, 38, 40 y 42."],
        pistas=["Hay dos puzles en el altillo: la caja y la cisterna.", "Coged las cartas 54, 56, 58 y 60. Descartad las cartas 36, 38, 40 y 42."],
        arte="Un altillo de madera bajo el tejado con vigas, una caja de nogal sobre una mesa, un boceto geométrico clavado en un caballete y una trampilla abierta sobre una cisterna de piedra con agua oscura. Cristina y Alberto suben por una escalera de madera con una lámpara de aceite."),
    "54": dict(
        titulo="Carta 54 — Caja de Pacioli", tipo="verde",
        descripcion=[
            "Es un juego de la app: la caja de las lentes se cierra con una cuadrícula de 4×4 casillas que hay que llenar con los números del 1 al 16, sin repetir, de modo que todas las filas, las columnas y las dos diagonales sumen lo mismo. El boceto de Pacioli (carta 56) da algunos números.",
            "Al acertar se abre la caja y aparece la lente de Leonardo. Coged la carta 62."],
        pistas=["Todas las filas, columnas y diagonales deben dar la misma suma.", "Los números del 1 al 16 suman 136: repartidos en cuatro filas, ¿cuánto suma cada una?", "Cada línea suma 34. La solución es: 16 3 2 13 / 5 10 11 8 / 9 6 7 12 / 4 15 14 1."],
        arte="Primer plano de una caja de nogal con una placa de latón dividida en una cuadrícula de dieciséis casillas con números grabados decorativos, y una cerradura, sobre una mesa de madera."),
    "56": dict(
        titulo="Carta 56 — Boceto de Pacioli", tipo="gris",
        descripcion=["Un boceto del matemático Luca Pacioli con algunos números del cuadrado mágico de la caja (carta 54). Sirve para completar el cuadrado."],
        pistas=["Anotad esos números en la cuadrícula de la caja.", "Sirve para la caja de Pacioli (carta 54)."],
        textoCarta=["Fila 1:  · 3 · ·", "Fila 2:  · 10 · ·", "Fila 3:  · · 7 ·"],
        arte="Un boceto a tinta de un matemático renacentista con una cuadrícula de cuatro por cuatro casillas, compases y reglas dibujados alrededor, sobre papel viejo; sin texto legible."),
    "58": dict(
        titulo="Carta 58 — Cisterna", tipo="verde",
        descripcion=[
            "Es un juego de la app: dos jarras (una de 3 medidas y otra de 5) y el grifo de la cisterna. Se puede llenar una jarra, vaciarla o verter una en otra. Hay que dejar justo la cantidad que pide la nota (carta 60) en la jarra grande.",
            "Al acertar, la compuerta cede y se abre una escalera a la azotea. Coged la carta 74."],
        pistas=["Solo se puede llenar, vaciar o verter de una jarra en otra hasta llenarla.", "Empezad llenando la grande y vertiéndola en la pequeña.", "Llenar la grande, verter en la pequeña, vaciar la pequeña, verter en la pequeña los 2 que quedan, llenar la grande y verter en la pequeña hasta que se llene: en la grande quedan 4."],
        arte="Una cisterna de piedra bajo una trampilla de madera, con dos jarras de barro de distinto tamaño sobre el borde, un grifo de bronce y agua oscura reflejando una lámpara."),
    "60": dict(
        titulo="Carta 60 — Nota de la cisterna", tipo="gris",
        descripcion=["Una nota clavada junto a la cisterna: dice cuánta agua debe quedar en la jarra grande para que ceda la compuerta. Sirve para la cisterna (carta 58)."],
        pistas=["Es el objetivo de las jarras.", "Sirve para la cisterna (carta 58)."],
        textoCarta=["La compuerta cede cuando", "la jarra grande guarda", "justo cuatro medidas."],
        arte="Una nota de papel clavada con un clavo en una viga húmeda junto a una cisterna, con manchas de tinta y un dibujo de dos jarras; sin texto legible."),
    "62": dict(
        titulo="Carta 62 — Lente maestra", tipo="roja", combina=[22, 84], descarta=[54, 56],
        descripcion=[
            "La lente maestra de Leonardo: un disco de cristal de roca perfectamente pulido que concentra la luz como ninguna. Cristina: «Con esto, la luz del amanecer bastará».",
            "Combinadla con el Cronoportal (carta 22): sumad sus números (62 + 22 = 84) y coged la carta 84. Descartad las cartas 54 y 56."],
        pistas=["Es lo que el aparato necesita.", "Combinad la carta 62 con la carta 22.", "Sumad los números de las dos cartas: 62 + 22 = 84."],
        arte="Una lente de cristal de roca grande y perfectamente pulida en un soporte de bronce, sobre terciopelo azul oscuro, que concentra la luz de una vela en un punto brillante."),
    "84": dict(
        titulo="Carta 84 — Cronoportal con lente", tipo="gris", descarta=[22, 62],
        descripcion=[
            "La lente encaja delante del anillo central del Cronoportal. Ahora solo falta que la luz del amanecer llegue hasta ella: hay que abrir el lucernario del tejado y dirigir el rayo con espejos.",
            "Descartad las cartas 22 y 62."],
        pistas=["El aparato ya tiene su lente.", "Descartad las cartas 22 y 62."],
        arte="El Cronoportal con una gran lente de cristal de roca encajada delante de su anillo central, a la espera de luz, en medio del taller. Alberto ajusta un dial y Cristina mira el cielo por una ventana."),
    "74": dict(
        titulo="Carta 74 — La azotea", tipo="gris", coge=[66, 68, 70, 71, 72], descarta=[51, 58, 60],
        descripcion=[
            "La compuerta se abre y una escalera de caracol sube a la azotea, bajo el lucernario cerrado. Allí está el ornitóptero de Leonardo (carta 66) y tres notas: el cuaderno de vuelo (carta 68), una nota del viento (carta 70) y los apuntes de Salaì (carta 71). En un cofre abierto brillan los espejos ustorios del maestro (carta 72).",
            "Coged las cartas 66, 68, 70, 71 y 72. Descartad las cartas 51, 58 y 60."],
        pistas=["Hay un puzle: el ornitóptero, con tres notas.", "Coged las cartas 66, 68, 70, 71 y 72. Descartad las cartas 51, 58 y 60."],
        arte="Una azotea de madera bajo el tejado de un taller, con un lucernario cerrado en el techo, un ornitóptero de madera con grandes alas de tela sobre una rampa, tres notas clavadas en una viga y un cofre abierto con espejos de bronce brillantes. Cristina y Alberto lo miran con sorpresa."),
    "66": dict(
        titulo="Carta 66 — Ornitóptero", tipo="verde",
        descripcion=[
            "Es un juego de la app: hay que preparar el ornitóptero eligiendo ala, tela y lastre. Las notas (cartas 68, 70 y 71) dicen qué combinaciones no funcionan; solo una vuela. Al hacerlo, su ala golpea la palanca del lucernario y lo abre.",
            "Coged la carta 90."],
        pistas=["Leed las tres notas: cada frase descarta combinaciones.", "Empezad por el lastre: ¿qué cantidades quedan posibles?", "Ala larga, tela de seda y dos sacos de lastre."],
        arte="Un ornitóptero de madera de Leonardo da Vinci con grandes alas articuladas de tela, un asiento y sacos de lastre colgados, sobre una rampa de madera en una azotea, con las primeras luces del alba al fondo."),
    "68": dict(
        titulo="Carta 68 — Cuaderno de vuelo", tipo="gris",
        descripcion=["Un cuaderno de vuelo con apuntes sobre las alas del ornitóptero. Sirve para el ornitóptero (carta 66)."],
        pistas=["Es una de las tres notas del ornitóptero.", "Sirve para el ornitóptero (carta 66)."],
        textoCarta=["Ala corta: no levanta ni una pluma.", "Con ala media, siempre dos sacos.", "Ala larga: tres sacos son demasiados."],
        arte="Un cuaderno de apuntes abierto con dibujos de alas de pájaro y de murciélago, flechas de viento y proporciones, sobre una mesa de madera; sin texto legible."),
    "70": dict(
        titulo="Carta 70 — Nota del viento", tipo="gris",
        descripcion=["Una nota de Leonardo sobre el viento del amanecer y el lastre del ornitóptero. Sirve para el ornitóptero (carta 66)."],
        pistas=["Es una de las tres notas del ornitóptero.", "Sirve para el ornitóptero (carta 66)."],
        textoCarta=["El viento del alba empuja fuerte.", "Con un solo saco, el aparato cae de lado."],
        arte="Una nota de papel clavada en una viga con un dibujo de remolinos de viento y un saco de arena, con una veleta de bronce al fondo; sin texto legible."),
    "71": dict(
        titulo="Carta 71 — Apuntes de Salaì", tipo="gris",
        descripcion=["Unos apuntes de Salaì sobre las telas del ornitóptero. Sirven para el ornitóptero (carta 66)."],
        pistas=["Es una de las tres notas del ornitóptero.", "Sirve para el ornitóptero (carta 66)."],
        textoCarta=["Dos sacos y tela de cuero: vuelca.", "Lino y dos sacos: se arruga.", "Ala media con seda: sin fuerza."],
        arte="Unas muestras de tela de lino, seda y cuero sujetas a una tabla con alfileres, junto a unos apuntes con manchas de tinta; sin texto legible."),
    "72": dict(
        titulo="Carta 72 — Espejos ustorios", tipo="gris",
        descripcion=["Tres espejos de bronce pulido, con los que Leonardo concentraba la luz. Servirán para dirigir el rayo del amanecer hasta el Cronoportal (carta 92)."],
        pistas=["Sirven para dirigir la luz.", "Los necesitaréis en la última prueba (carta 92)."],
        arte="Tres espejos redondos de bronce pulido sobre soportes giratorios, dentro de un cofre abierto forrado de terciopelo, reflejando la luz de una lámpara."),
    "90": dict(
        titulo="Carta 90 — El lucernario", tipo="gris", coge=[92, 94], descarta=[74, 66, 68, 70, 71],
        descripcion=[
            "El ala del ornitóptero golpea la palanca: el lucernario se abre y entra el primer rayo del alba. El rayo está listo para ser dirigido (carta 92) y un plano del taller marca dónde va cada cosa (carta 94).",
            "Coged las cartas 92 y 94. Descartad las cartas 74, 66, 68, 70 y 71."],
        pistas=["La luz del amanecer ya entra.", "Coged las cartas 92 y 94. Descartad las cartas 74, 66, 68, 70 y 71."],
        arte="El lucernario del tejado de un taller renacentista abierto: un primer rayo dorado del amanecer entra en diagonal e ilumina el polvo en el aire, con el ornitóptero detrás. Cristina y Alberto miran hacia arriba con esperanza."),
    "92": dict(
        titulo="Carta 92 — Rayo del amanecer", tipo="verde",
        descripcion=[
            "Es un juego de la app: el taller visto desde arriba. Hay que colocar la lente en uno de los tres atriles y tres espejos de modo que el rayo que entra por el lucernario atraviese la lente y llegue al Cronoportal. El plano (carta 94) dice en qué atril va la lente.",
            "Al acertar, el portal de vuelta se abre. Coged la carta 99."],
        pistas=["La lente solo cabe en un atril: mirad el plano (carta 94).", "El rayo entra por arriba, en la primera columna; colocad la lente y buscad el camino con tres espejos.", "Lente en B3. Espejos: \\ en A2, \\ en C2 y / en C3."],
        arte="Vista cenital de un taller renacentista con un rayo de luz dorada que baja desde un lucernario, rebota en tres espejos de bronce y atraviesa una lente sobre un atril hasta llegar al Cronoportal, que brilla con luz azul."),
    "94": dict(
        titulo="Carta 94 — Plano solar", tipo="gris",
        descripcion=["Un plano del taller con una cruz sobre uno de los atriles: dice dónde va la lente. Sirve para el rayo del amanecer (carta 92)."],
        pistas=["Fijaos en la cruz del plano.", "Sirve para el rayo del amanecer (carta 92)."],
        textoCarta=["La lente de cristal de roca", "se apoya en el atril de la", "columna B, fila 3."],
        arte="Un plano dibujado a tinta del suelo de un taller visto desde arriba, con una cuadrícula, tres atriles marcados con círculos y una cruz sobre uno de ellos, sobre papel viejo; sin texto legible."),
    "99": dict(
        titulo="Carta 99 — De vuelta a casa (FIN)", tipo="gris", descarta=[84, 72, 90, 92, 94],
        descripcion=[
            "El rayo atraviesa la lente y el Cronoportal despierta con un destello dorado. Se abre el portal justo cuando se oyen los pasos de Leonardo en la escalera. Cristina deja sobre la mesa una nota de agradecimiento, escrita al revés.",
            "Aterrizan en su salón. Alberto mira el aparato: «Mañana, otro destino». Cristina sonríe. Descartad las cartas 84, 72, 90, 92 y 94.",
            "FIN."],
        pistas=[],
        arte="La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ven el taller de Leonardo con un rayo de amanecer, la lente brillante y el ornitóptero. Llevan aún su ropa florentina de 1503. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(
    juego="Florencia, 1503 — El Taller de Leonardo",
    estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
)

SPEC = dict(
    final="99",
    needs={"30": ["24", "26"], "36": ["32", "28", "35"], "51": ["38", "40", "42"], "62": ["54", "56"], "84": ["22", "62"],
           "74": ["58", "60"], "90": ["66", "68", "70", "71"], "99": ["92", "84", "72", "94"]},
    eventos={},
)

PARA_QUE = {
    "P": "Inicio: llegada al taller. Te manda coger la 20 y la 22.",
    "20": "El taller: reparte las cartas del taller y te quita la P.",
    "22": "El Cronoportal sin energía: se combina con la lente maestra (62).",
    "24": "Cofre del maestro (app): teclado de 4 cifras.",
    "26": "Cuaderno de Leonardo: texto escrito en espejo con la combinación del cofre.",
    "28": "Nota de Salaì: cómo se coloca el disco de cifrado.",
    "30": "Interior del cofre: aparece al abrirlo; reparte el disco y el pergamino.",
    "32": "Disco de Alberti (app): descifrar el pergamino con un disco de letras.",
    "35": "Pergamino cifrado: el mensaje que se descifra con el disco.",
    "36": "El león mecánico: aparece al descifrar; reparte el mecanismo, el plano y la llave.",
    "38": "Mecanismo del león (app): montar una cadena de engranajes; da un modificador.",
    "40": "Plano del mecanismo: cómo debe girar la cuerda.",
    "42": "Llave de cuerda: se suma al modificador del mecanismo (42 + 9 = 51).",
    "51": "El altillo: resultado de 42 + 9; reparte la caja, el boceto y la cisterna.",
    "54": "Caja de Pacioli (app): cuadrado mágico 4×4.",
    "56": "Boceto de Pacioli: números del cuadrado mágico.",
    "58": "Cisterna (app): puzle de las dos jarras.",
    "60": "Nota de la cisterna: cuánta agua debe quedar en la jarra grande.",
    "62": "Lente maestra: sale de la caja; se combina con el Cronoportal (22).",
    "84": "Cronoportal con lente: resultado de 22 + 62.",
    "74": "La azotea: aparece al abrir la compuerta de la cisterna; reparte el ornitóptero, las notas y los espejos.",
    "66": "Ornitóptero (app): puzle de lógica (ala, tela y lastre).",
    "68": "Cuaderno de vuelo: frases sobre las alas.",
    "70": "Nota del viento: frase sobre el lastre.",
    "71": "Apuntes de Salaì: frases sobre las telas.",
    "72": "Espejos ustorios: sirven para la última prueba (92).",
    "90": "El lucernario: aparece al volar el ornitóptero; reparte el rayo y el plano.",
    "92": "Rayo del amanecer (app): colocar lente y espejos para llevar la luz al Cronoportal.",
    "94": "Plano solar: en qué atril va la lente.",
    "99": "Final de la aventura.",
}

PASOS = [
    dict(t="Llegada al taller", que="Pon el Modo PC en el ordenador (solo debe haber la carta P en la mesa y el resto boca abajo en el mazo) y en el móvil abre el juego y pulsa Empezar. Lee la carta P: te manda coger la 20 y la 22.",
         acciones=[("leer", "P")], mesa=["P", "20", "22"]),
    dict(t="El taller", que="Lee la carta 20. Descarta la P y coge 24, 26 y 28. El cuaderno de Leonardo (26) está escrito en espejo: ponlo frente a un espejo (o usa la cámara frontal del móvil) y dice: «dos, siete, cinco, nueve».",
         acciones=[("leer", "20")], mesa=["20", "22", "24", "26", "28"]),
    dict(t="Abre el cofre", que="En el móvil: Acción, 24. Teclea 2 7 5 9. El mensaje te dice que cojas la 30.",
         acciones=[("app", "24", "carta 30")], mesa=["20", "22", "24", "26", "28", "30"]),
    dict(t="Dentro del cofre", que="Lee la carta 30. Descarta 24, 26 y 20 y coge 32 y 35. El pergamino (35) tiene letras sin sentido.",
         acciones=[("leer", "30")], mesa=["22", "28", "30", "32", "35"]),
    dict(t="Descifra el pergamino", que="La nota de Salaì (28) dice que la A de fuera va sobre la F de dentro. En el móvil: Acción, 32. Pon el disco así y descifra el pergamino (35): «EL LEON GUARDA SU CORAZON». Escribe LEON. El mensaje te dice que cojas la 36.",
         acciones=[("app", "32", "carta 36")], mesa=["22", "28", "30", "32", "35", "36"]),
    dict(t="El león mecánico", que="Lee la carta 36. Descarta 30, 32, 35 y 28 y coge 38, 40 y 42. El plano (40) dice que la cuerda debe girar igual de rápido que la manivela pero al revés.",
         acciones=[("leer", "36")], mesa=["22", "36", "38", "40", "42"]),
    dict(t="Monta los engranajes", que="En el móvil: Acción, 38. Pon una rueda pequeña en D, una mediana en B y una mediana en Z. Pulsa Girar. El mecanismo marca el modificador +9: suma 42 + 9 = 51 y coge la 51.",
         acciones=[("app", "38", "carta 51")], mesa=["22", "36", "38", "40", "42", "51"]),
    dict(t="El altillo", que="Lee la carta 51. Descarta 36, 38, 40 y 42 y coge 54, 56, 58 y 60. Hay dos puzles: la caja (54, con el boceto 56) y la cisterna (58, con la nota 60).",
         acciones=[("leer", "51")], mesa=["22", "51", "54", "56", "58", "60"]),
    dict(t="Completa el cuadrado mágico", que="En el móvil: Acción, 54. Las casillas bloqueadas son 16, 2 y 4; el boceto (56) añade 3, 10 y 7. Completa el cuadrado: todas las líneas suman 34. El mensaje te dice que cojas la 62.",
         acciones=[("app", "54", "carta 62")], mesa=["22", "51", "54", "56", "58", "60", "62"]),
    dict(t="La lente maestra", que="Lee la carta 62. Te manda descartar 54 y 56. Es combinable.",
         acciones=[("leer", "62")], mesa=["22", "51", "58", "60", "62"]),
    dict(t="Combina la lente con el Cronoportal", que="El Cronoportal (22) y la lente maestra (62) son combinables: 22 + 62 = 84. Coge la 84.",
         acciones=[("combinar", "22", "62")], mesa=["22", "51", "58", "60", "62", "84"]),
    dict(t="El Cronoportal con lente", que="Lee la carta 84. Te manda descartar 22 y 62.",
         acciones=[("leer", "84")], mesa=["51", "58", "60", "84"]),
    dict(t="Vacía la cisterna", que="La nota (60) pide cuatro medidas en la jarra grande. En el móvil: Acción, 58. Llena la grande, vierte en la pequeña, vacía la pequeña, vierte los 2 que quedan, llena la grande y vierte en la pequeña hasta llenarla. El mensaje te dice que cojas la 74.",
         acciones=[("app", "58", "carta 74")], mesa=["51", "58", "60", "84", "74"]),
    dict(t="La azotea", que="Lee la carta 74. Descarta 51, 58 y 60 y coge 66, 68, 70, 71 y 72. Las tres notas (68, 70 y 71) son para el ornitóptero (66).",
         acciones=[("leer", "74")], mesa=["84", "74", "66", "68", "70", "71", "72"]),
    dict(t="Prepara el ornitóptero", que="En el móvil: Acción, 66. Con las tres notas: el lastre solo puede ser de dos sacos, la tela de seda y el ala larga. Pulsa Probar vuelo. El mensaje te dice que cojas la 90.",
         acciones=[("app", "66", "carta 90")], mesa=["84", "74", "66", "68", "70", "71", "72", "90"]),
    dict(t="El lucernario", que="Lee la carta 90. Descarta 74, 66, 68, 70 y 71 y coge 92 y 94. El plano (94) dice que la lente va en el atril de la columna B, fila 3.",
         acciones=[("leer", "90")], mesa=["84", "72", "90", "92", "94"]),
    dict(t="Dirige el rayo del amanecer", que="En el móvil: Acción, 92. Pon la lente en B3 y tres espejos: \\ en A2, \\ en C2 y / en C3. Pulsa Probar. El mensaje te dice que cojas la 99.",
         acciones=[("app", "92", "carta 99")], mesa=["84", "72", "90", "92", "94", "99"]),
    dict(t="Final", que="Lee la carta 99. Descarta 84, 72, 90, 92 y 94. En la mesa solo queda la 99. ¡Fin!",
         acciones=[("leer", "99")], mesa=["99"]),
]

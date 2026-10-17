ESTILO = ("Ilustración digital semirrealista con aire de película de aventuras, luz dorada de atardecer entre vegetación exuberante del Cretácico "
          "(helechos gigantes, cícadas, coníferas), paleta de verdes profundos, ocres y naranja volcánico, con destellos azules del Cronoportal, formato vertical 2:3. "
          "Sin texto, letras ni números en la imagen; los mapas, cuadernos y paneles son solo dibujos decorativos sin escritura legible. "
          "Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen.")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado recogido en una coleta, ojos azules. Viste ropa de expedición paleontológica: camisa caqui remangada, chaleco de explorador con bolsillos, pantalón de campo, botas de montaña y sombrero de ala ancha.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Viste ropa de expedición paleontológica: camiseta verde oliva, chaleco caqui con muchos bolsillos, pantalón cargo, botas de montaña, gorra y una mochila."
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado recogido en una coleta, ojos azules, camisa caqui remangada, chaleco de explorador con bolsillos, pantalón de campo, botas de montaña y sombrero de ala ancha. "
        "Alberto: hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones, camiseta verde oliva, chaleco caqui con muchos bolsillos, pantalón cargo, botas de montaña, gorra y mochila. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con animación semirrealista de película de aventuras, luz dorada y colores verdes y naranjas. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones), vestidos de exploradores, rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Cristina sonríe emocionada ante la foto de un fósil de dinosaurio. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul, el salón se deforma y los dos son absorbidos por un túnel de luz con destellos dorados. "
         "Escena 3 (8-12 s): caen sobre la hierba de un valle del Cretácico al atardecer, entre helechos gigantes; un enorme saurópodo cruza al fondo y un punto de luz brillante, un asteroide, cruza el cielo; el aparato humea y se apaga. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, asombrados, mirando al cielo; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe sordo al aterrizar, rugidos lejanos, insectos y viento entre los helechos, música de aventura con percusión, sin voz de narrador.")

J = {
    "P": dict(
        titulo="Carta P — Llegada al Cretácico", tipo="gris", coge=[10, 12],
        descripcion=[
            "Cuarta parada del Cronoportal: el Cretácico superior, hace sesenta y seis millones de años. Cristina lleva toda la vida soñando con ver dinosaurios de verdad.",
            "El salto vuelve a salir mal: aterrizáis en un valle junto a un río, el aparato se golpea con una roca y su núcleo de energía sale rodando entre los helechos. Sin él, el Cronoportal está muerto. Y en el cielo, un punto de luz cada vez más brillante: un asteroide. Tenéis una hora y media antes de que el cielo se incendie.",
            "Coged las cartas 10 y 12."],
        pistas=["Mirad a vuestro alrededor y revisad el aparato.", "Coged las cartas 10 y 12."],
        arte="Un valle del Cretácico superior al atardecer, con helechos gigantes, cícadas y un río; al fondo un enorme saurópodo cruza entre la bruma y en el cielo naranja brilla un punto de luz muy intenso, un asteroide. En primer plano, un aparato de latón y cristal retrofuturista (el Cronoportal) humea sobre la hierba con una luz azul que se apaga. Cristina y Alberto, con ropa de expedición, se levantan desconcertados mirando el cielo."),
    "10": dict(
        titulo="Carta 10 — Campamento del doctor Ibarra", tipo="gris", coge=[14, 16, 18, 20, 22], descarta=["P"],
        descripcion=[
            "Entre los helechos, un campamento de campaña abandonado: la tienda del doctor Ibarra, un paleontólogo viajero que estuvo aquí antes que vosotros. Junto al río, unas huellas frescas en el barro (carta 14) y una guía de huellas clavada en un poste (carta 16). Más allá, una cuadrícula de cuerdas sobre un terreno removido (carta 20) con las notas de excavación (carta 18), y un rollo de cuerda sobre un baúl (carta 22).",
            "Coged las cartas 14, 16, 18, 20 y 22. Descartad la carta P."],
        pistas=["Hay dos puzles: las huellas del río y la excavación.", "Coged las cartas 14, 16, 18, 20 y 22. Descartad la carta P."],
        arte="Un campamento de campaña de un paleontólogo entre helechos gigantes: una tienda de lona, un baúl con una cuerda enrollada, una cuadrícula de cuerdas clavada sobre tierra removida y unas huellas grandes en el barro junto a un río. Cristina y Alberto lo examinan con curiosidad bajo la luz dorada del atardecer."),
    "12": dict(
        titulo="Carta 12 — Cronoportal sin núcleo", tipo="azul", combina=[62, 74],
        descripcion=[
            "El Cronoportal: una consola de latón y cristal con un anillo central apagado y un hueco vacío en el pecho, donde iba el núcleo de energía. Alberto: «Sin el núcleo no hay portal. Tiene que haber rodado por aquí cerca».",
            "Cuando recuperéis el núcleo (carta 62), combinadlo con el Cronoportal: sumad sus números (12 + 62 = 74) y coged la carta 74."],
        pistas=["Le falta una pieza: el núcleo de energía.", "Combinad la carta 12 con la carta 62.", "Sumad los números de las dos cartas: 12 + 62 = 74."],
        arte="Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo de cristal central apagado y un hueco circular vacío en el pecho del aparato, sobre una roca cubierta de musgo, con helechos al fondo."),
    "14": dict(
        titulo="Carta 14 — Huellas en el barro", tipo="verde",
        descripcion=[
            "Es un juego de la app: cuatro huellas en el barro del río. Hay que decir qué dinosaurio dejó cada una, usando la guía de huellas (carta 16).",
            "Al acertar, reconocéis quién ronda el vado y encontráis un croquis del valle. Coged la carta 26."],
        pistas=["Comparad la forma de cada huella con la guía de huellas (carta 16).", "Fijaos en los dedos: cuántos son, si tienen garras o son romos, y si la huella es redonda o ancha.", "De izquierda a derecha: Triceratops, Tiranosaurio, Anquilosaurio y Edmontosaurio."],
        arte="Primer plano de cuatro huellas distintas de dinosaurio marcadas en el barro húmedo de la orilla de un río: una casi redonda con cinco dedos cortos, otra de tres dedos largos con garras, otra muy ancha con cuatro dedos y otra de tres dedos gordos y romos. Luz dorada rasante."),
    "16": dict(
        titulo="Carta 16 — Guía de huellas", tipo="gris",
        descripcion=["Una guía de campo de huellas, clavada en un poste. Sirve para las huellas del río (carta 14)."],
        pistas=["Es una guía para reconocer huellas.", "Sirve para las huellas en el barro (carta 14)."],
        textoCarta=["Tiranosaurio: tres dedos con garras.", "Edmontosaurio: tres dedos gordos, sin garras.", "Triceratops: huella casi redonda, cinco dedos cortos.", "Anquilosaurio: muy ancha, cuatro dedos."],
        arte="Una guía de campo de papel desgastado clavada en un poste de madera junto a un río, con dibujos decorativos de huellas de dinosaurio y flechas, sin texto legible; helechos alrededor."),
    "18": dict(
        titulo="Carta 18 — Notas de excavación", tipo="gris",
        descripcion=["Las notas del doctor Ibarra sobre la excavación. Sirven para la cuadrícula (carta 20)."],
        pistas=["Es el método para leer la cuadrícula.", "Sirve para la excavación (carta 20)."],
        textoCarta=["Bajo la cuadrícula hay siete huesos.", "Cada número dice cuántos huesos tocan esa casilla, también en diagonal.", "Una casilla con número no esconde ningún hueso."],
        arte="Una libreta de campo con manchas de tierra abierta sobre un baúl, con dibujos decorativos de un hueso y una cuadrícula, junto a un pincel y una brocha; sin texto legible."),
    "20": dict(
        titulo="Carta 20 — Excavación", tipo="verde",
        descripcion=[
            "Es un juego de la app: una cuadrícula de casillas con algunos números. Hay que marcar dónde están enterrados los huesos, usando las notas del doctor (carta 18).",
            "Al acertar, aparece un esqueleto parcial y el equipo enterrado de Ibarra. Coged la carta 28."],
        pistas=["Las notas del doctor (carta 18) explican qué significan los números.", "Un 0 significa que ninguna de las casillas de alrededor tiene hueso. Empezad por ahí.", "Los huesos están en B2, C4, D1, D5, E2, E3 y F5."],
        arte="Una cuadrícula de cuerdas sobre un terreno de excavación paleontológica, con una brocha y pequeños huesos fosilizados apenas asomando de la tierra, y una pala clavada a un lado, a la luz del atardecer."),
    "22": dict(
        titulo="Carta 22 — Cuerda", tipo="roja", combina=[35, 57],
        descripcion=[
            "Un rollo de cuerda trenzada, resistente. Con un garfio de escalada servirá para trepar. Combinadla con el garfio que aparezca en la excavación (carta 35): sumad sus números (22 + 35 = 57) y coged la carta 57."],
        pistas=["Necesita algo con lo que engancharse.", "Cuando tengáis el garfio de escalada, combinadlo con la cuerda.", "Sumad los números de las dos cartas: 22 + 35 = 57."],
        arte="Un rollo grande de cuerda trenzada de cáñamo sobre un baúl de madera de campamento, con un mosquetón y un nudo marinero, luz cálida del atardecer."),
    "26": dict(
        titulo="Carta 26 — Croquis del barranco", tipo="gris", descarta=[14, 16],
        descripcion=[
            "Con las huellas identificadas, entendéis por dónde ronda cada animal y encontráis un croquis del corte del barranco, con la ordenación de las capas de roca. Sirve para los estratos (carta 51).",
            "Descartad las cartas 14 y 16."],
        pistas=["El croquis ordena algunas capas de roca.", "Sirve para los estratos (carta 51)."],
        textoCarta=["La ceniza del volcán cubre todo: es la capa de arriba.", "La arena con conchas, de un mar antiguo, es la del fondo.", "La arcilla está justo encima de la caliza."],
        arte="Un croquis dibujado a lápiz sobre papel de campo, clavado en una roca, con un corte de barranco en capas de colores distintos y flechas, sin texto legible, junto a unas huellas en el barro."),
    "28": dict(
        titulo="Carta 28 — El hallazgo", tipo="gris", coge=[35, 37], descarta=[20, 18],
        descripcion=[
            "Bajo la cuadrícula aparece el esqueleto parcial de un anquilosaurio y, enterrado a su lado, el equipo que Ibarra escondió: un garfio de escalada (carta 35) y una pieza de ámbar con un mosquito dentro (carta 37).",
            "Coged las cartas 35 y 37. Descartad las cartas 20 y 18."],
        pistas=["Mirad lo que había enterrado junto a los huesos.", "Coged las cartas 35 y 37. Descartad las cartas 20 y 18."],
        arte="Una excavación paleontológica con el esqueleto parcial de un dinosaurio acorazado asomando de la tierra; a su lado, un garfio de escalada de hierro y una pieza de ámbar dorado con un mosquito dentro sobre un paño. Cristina y Alberto se asoman con asombro."),
    "35": dict(
        titulo="Carta 35 — Garfio de escalada", tipo="azul", combina=[22, 57],
        descripcion=["Un garfio de hierro de tres uñas, con un anillo para atar una cuerda. Combinadlo con la cuerda (carta 22): sumad sus números (35 + 22 = 57) y coged la carta 57."],
        pistas=["Es un garfio: necesita una cuerda.", "Combinad la carta 35 con la carta 22.", "Sumad los números de las dos cartas: 35 + 22 = 57."],
        arte="Un garfio de escalada de hierro de tres uñas con un anillo, sobre un paño de lona, junto a un hueso fosilizado, con tierra aún pegada."),
    "37": dict(
        titulo="Carta 37 — Muestra de ámbar", tipo="gris",
        descripcion=["Una pieza de ámbar con un mosquito fosilizado. El doctor Ibarra anotó su cadena de ADN. Sirve para el secuenciador (carta 46)."],
        pistas=["Es una cadena de ADN anotada.", "Sirve para el secuenciador (carta 46)."],
        textoCarta=["Mosquito fosilizado. Cadena de ADN:", "A  T  G  C  C  G  T  A"],
        arte="Una pieza de ámbar dorado del tamaño de una mano, con un mosquito fosilizado dentro, sostenida sobre una tela con una lupa al lado, luz cálida de atardecer."),
    "57": dict(
        titulo="Carta 57 — El barranco", tipo="gris", coge=[40, 42], descarta=[22, 35, 28, 10],
        descripcion=[
            "Anudáis la cuerda al garfio y trepáis por el barranco hasta la orilla del río grande. Allí, una balsa de troncos atada a la orilla (carta 40) y el diario del doctor Ibarra, tirado sobre ella (carta 42).",
            "Coged las cartas 40 y 42. Descartad las cartas 22, 35, 28 y 10."],
        pistas=["Subís hasta la orilla del río.", "Coged las cartas 40 y 42. Descartad las cartas 22, 35, 28 y 10."],
        arte="Cristina y Alberto trepan por un barranco de roca roja con una cuerda atada a un garfio, hasta una orilla de río ancho con una balsa de troncos atada a la ribera y un diario abandonado sobre ella, helechos gigantes alrededor."),
    "40": dict(
        titulo="Carta 40 — Balsa del vado", tipo="verde",
        descripcion=[
            "Es un juego de la app: hay que cruzar el río en una balsa llevando a tres criaturas, de una en una: un pequeño compsognato, un bebé de driosaurio y un cesto de helechos. Las normas del doctor Ibarra (carta 42) dicen qué no puede quedarse sin vigilancia.",
            "Al cruzar a todos, llegáis a la otra orilla. Coged la carta 44."],
        pistas=["Leed el diario del doctor Ibarra (carta 42): dice qué criaturas no pueden quedarse juntas.", "En la balsa solo cabe una criatura con vosotros. A veces hay que volver sin nada, o traer a alguien de vuelta.", "Cruzad: el bebé, vacíos de vuelta, el compsognato, traed de vuelta al bebé, los helechos, vacíos de vuelta y por fin el bebé."],
        arte="Una balsa de troncos atada en la orilla de un río ancho del Cretácico, con un pequeño dinosaurio carnívoro bípedo del tamaño de un pollo, un bebé de dinosaurio herbívoro y un cesto de helechos esperando en la ribera, al atardecer."),
    "42": dict(
        titulo="Carta 42 — Diario del doctor Ibarra", tipo="verde",
        descripcion=["Es un juego de la app (solo lectura): el diario del doctor Ibarra. Explica las normas para cruzar el río con la balsa (carta 40)."],
        pistas=["Pasad las páginas con calma.", "Las normas del cruce están en el diario: sirven para la balsa (carta 40)."],
        arte="Un diario de campo de tapas de cuero abierto sobre los troncos de una balsa, con dibujos decorativos de dinosaurios pequeños y de un río, y una pluma estilográfica al lado; sin texto legible."),
    "44": dict(
        titulo="Carta 44 — La otra orilla", tipo="gris", coge=[46, 48, 51, 52], descarta=[40, 42, 57],
        descripcion=[
            "Al otro lado del río está el laboratorio de campaña del doctor Ibarra: una tienda con un secuenciador de ADN (carta 46) y un manual de laboratorio (carta 48). Un poco más allá, la pared de un barranco con capas de roca de colores, con el cuaderno de capas del doctor (carta 52) y un punto marcado donde escondió algo (carta 51).",
            "Coged las cartas 46, 48, 51 y 52. Descartad las cartas 40, 42 y 57."],
        pistas=["Hay dos puzles: el laboratorio y las capas de roca.", "Coged las cartas 46, 48, 51 y 52. Descartad las cartas 40, 42 y 57."],
        arte="La otra orilla de un río del Cretácico: una tienda de laboratorio de campaña con un aparato científico a la entrada y, más allá, la pared de un barranco con capas de roca de distintos colores y un cuaderno clavado. Cristina y Alberto acaban de desembarcar de la balsa."),
    "46": dict(
        titulo="Carta 46 — Secuenciador de ADN", tipo="verde",
        descripcion=[
            "Es un juego de la app: el secuenciador del doctor Ibarra, con una caja fuerte biométrica que se abre con la cadena complementaria del ADN del mosquito. La cadena de la muestra está en la carta 37 y el manual de laboratorio (carta 48) explica cómo se empareja.",
            "Al acertar, la caja se abre. Coged la carta 54."],
        pistas=["La muestra de ámbar (carta 37) da la cadena; el manual (carta 48) dice con qué se empareja cada letra.", "Cada letra de la cadena nueva es la pareja de la letra que está en su mismo sitio en la cadena de la muestra.", "La cadena nueva es T A C G G C A T."],
        arte="Primer plano de un secuenciador de ADN de laboratorio de campaña: una caja de metal con una pantalla, una rejilla de tubos de ensayo y una caja fuerte pequeña con cerradura biométrica, en una tienda de lona iluminada por una lámpara."),
    "48": dict(
        titulo="Carta 48 — Manual de laboratorio", tipo="gris",
        descripcion=["Una hoja del manual del laboratorio con la regla de emparejamiento del ADN. Sirve para el secuenciador (carta 46)."],
        pistas=["Es la regla del ADN.", "Sirve para el secuenciador (carta 46)."],
        textoCarta=["Las bases del ADN se emparejan siempre:", "A con T, y C con G.", "La cadena nueva se copia frente a la vieja, letra a letra."],
        arte="Una hoja de manual de laboratorio sujeta con una pinza sobre una mesa de campaña, con dibujos decorativos de la doble hélice del ADN y esquemas de moléculas, sin texto legible, junto a tubos de ensayo."),
    "51": dict(
        titulo="Carta 51 — Estratos", tipo="verde",
        descripcion=[
            "Es un juego de la app: seis capas de roca del barranco, mezcladas. Hay que ordenarlas de abajo arriba usando el croquis (carta 26) y el cuaderno de capas (carta 52). El escondite del doctor Ibarra está marcado en el lugar correcto.",
            "Al acertar, encontráis lo que escondió. Coged la carta 58."],
        pistas=["Los dos documentos (cartas 26 y 52) ordenan las capas con frases.", "Empezad por las capas fijas: la de arriba del todo y la del fondo.", "De abajo arriba: conchas, caliza, arcilla, arenisca, carbón y ceniza."],
        arte="La pared de un barranco con seis capas de roca claramente distintas: arena con conchas, caliza clara, arcilla verdosa, arenisca roja, una capa negra de carbón y ceniza volcánica gris arriba del todo, con una cruz pintada de rojo en un punto."),
    "52": dict(
        titulo="Carta 52 — Cuaderno de capas", tipo="gris",
        descripcion=["Un cuaderno de capas del doctor Ibarra. Sirve, junto con el croquis (carta 26), para ordenar los estratos (carta 51)."],
        pistas=["Son dos frases sobre capas de roca.", "Sirve para los estratos (carta 51)."],
        textoCarta=["El carbón está justo debajo de la ceniza.", "La arenisca está entre la arcilla y el carbón."],
        arte="Un cuaderno de dibujos geológicos abierto sobre una roca, con un corte de capas de colores dibujado a lápiz y un martillo de geólogo al lado; sin texto legible."),
    "54": dict(
        titulo="Carta 54 — La caja abierta", tipo="gris", coge=[56], descarta=[46, 48, 37],
        descripcion=[
            "La caja fuerte del secuenciador se abre con un chasquido. Dentro hay una batería de campaña, del tamaño de un puño, con un cable.",
            "Coged la carta 56. Descartad las cartas 46, 48 y 37."],
        pistas=["Mirad lo que había en la caja.", "Coged la carta 56. Descartad las cartas 46, 48 y 37."],
        arte="Una pequeña caja fuerte de laboratorio abierta, con una batería de campaña de color verde y un cable enrollado dentro, sobre una mesa de la tienda del laboratorio, con luz de lámpara."),
    "56": dict(
        titulo="Carta 56 — Batería de campaña", tipo="roja", combina=[38, 94],
        descripcion=["Una batería de campaña cargada. Alberto: «Le irá bien a una linterna». Combinadla con la linterna (carta 38): sumad sus números (56 + 38 = 94) y coged la carta 94."],
        pistas=["Es una batería: alimentará algo.", "Cuando tengáis la linterna, combinadla con la batería.", "Sumad los números de las dos cartas: 56 + 38 = 94."],
        arte="Una batería de campaña de color verde militar con dos bornes de latón y un asa, sobre una mesa de madera, con luz de lámpara."),
    "58": dict(
        titulo="Carta 58 — El escondite", tipo="gris", coge=[38], descarta=[51, 52, 26],
        descripcion=[
            "En la capa marcada, un hueco en la roca guarda el último escondite del doctor Ibarra: una linterna potente, sin pilas.",
            "Coged la carta 38. Descartad las cartas 51, 52 y 26."],
        pistas=["Mirad dentro del hueco.", "Coged la carta 38. Descartad las cartas 51, 52 y 26."],
        arte="Un hueco abierto en una capa de roca de un barranco, con una linterna de campaña grande y robusta dentro, y una cruz roja pintada junto a la entrada; Cristina la saca con cuidado."),
    "38": dict(
        titulo="Carta 38 — Linterna sin pilas", tipo="azul", combina=[56, 94],
        descripcion=["Una linterna de campaña muy potente, pero sin pilas. Combinadla con la batería (carta 56): sumad sus números (38 + 56 = 94) y coged la carta 94."],
        pistas=["Es una linterna sin pilas.", "Combinad la carta 38 con la carta 56.", "Sumad los números de las dos cartas: 38 + 56 = 94."],
        arte="Una linterna de campaña grande de metal oxidado con un foco ancho y un compartimento de pilas abierto y vacío, sobre una roca cubierta de musgo."),
    "94": dict(
        titulo="Carta 94 — La cueva", tipo="gris", coge=[64, 66], descarta=[56, 38, 44, 54, 58],
        descripcion=[
            "Con la linterna encendida, Alberto descubre la entrada de una cueva en la ladera, de donde sale un calor extraño: el núcleo debió de rodar hasta aquí. La entrada está cerrada por una pared de cristales apagados (carta 64) y, al lado, un dibujo rupestre muestra cómo deben brillar (carta 66).",
            "Coged las cartas 64 y 66. Descartad las cartas 56, 38, 44, 54 y 58."],
        pistas=["Hay un puzle: la pared de cristales.", "Coged las cartas 64 y 66. Descartad las cartas 56, 38, 44, 54 y 58."],
        arte="La entrada de una cueva en una ladera rocosa del Cretácico, iluminada por un haz de linterna; una pared de cristales apagados tapa el paso y a un lado hay un dibujo rupestre de cristales brillantes. Cristina y Alberto avanzan con la linterna. Cristina con cara de curiosidad y sorpresa; Alberto con miedo contenido y los ojos muy abiertos."),
    "64": dict(
        titulo="Carta 64 — Cristales de la cueva", tipo="verde",
        descripcion=[
            "Es un juego de la app: una pared de cristales apagados en filas. Al tocar uno, él y sus vecinos de arriba, abajo, izquierda y derecha cambian de estado (se encienden o se apagan). Hay que dejar iluminada la pared como muestra el dibujo rupestre (carta 66).",
            "Al acertar, la pared se abre. Coged la carta 78."],
        pistas=["El dibujo rupestre (carta 66) muestra qué cristales deben quedar encendidos.", "Cada pulsación cambia un cristal y los cuatro que lo rodean en cruz. No importa el orden de las pulsaciones.", "Pulsad B1, A2, B2, A3 y D3."],
        arte="Una pared de una cueva con una cuadrícula de cuatro por tres cristales de colores, algunos apagados y otros encendidos con luz azul, brillando débilmente en la oscuridad."),
    "66": dict(
        titulo="Carta 66 — Dibujo rupestre", tipo="gris",
        descripcion=["Un dibujo rupestre de cristales: indica cuáles deben brillar (●) y cuáles quedar apagados (○). Sirve para la pared de cristales (carta 64)."],
        pistas=["Es el dibujo de la pared terminada.", "Sirve para la pared de cristales (carta 64)."],
        textoCarta=["Así brilla la pared abierta:", "○ ○ ● ○", "● ● ● ●", "○ ○ ● ●"],
        arte="Un dibujo rupestre rojo y negro sobre la pared de una cueva, con formas de cristales y de manos abiertas, y figuras de animales, sin texto legible, iluminado por una linterna."),
    "78": dict(
        titulo="Carta 78 — La cámara del nido", tipo="gris", coge=[69, 70], descarta=[64, 66, 94],
        descripcion=[
            "La pared se abre y entráis en una cámara caliente, iluminada por la lava lejana. En el suelo hay tres nidos: uno de ramas, uno de piedras y uno de plumas, y en el primero, cuatro huevos enormes de distinto tamaño apilados (carta 69). Una nota de Ibarra (carta 70) cuelga de un palo.",
            "Coged las cartas 69 y 70. Descartad las cartas 64, 66 y 94."],
        pistas=["Hay un puzle: los huevos y los nidos.", "Coged las cartas 69 y 70. Descartad las cartas 64, 66 y 94."],
        arte="Una cámara de cueva caliente con tres nidos en el suelo (uno de ramas, uno de piedras y uno de plumas) y cuatro huevos de dinosaurio enormes apilados de mayor a menor en el nido de ramas, con el resplandor naranja de lava al fondo. Cristina y Alberto entran con cautela. Cristina con los ojos muy abiertos de asombro y una sonrisa nerviosa; Alberto con expresión de cautela y desconfianza, una ceja levantada."),
    "69": dict(
        titulo="Carta 69 — Huevos y nidos", tipo="verde",
        descripcion=[
            "Es un juego de la app: cuatro huevos de distinto tamaño apilados en un nido, y otros dos nidos vacíos. Hay que mover los huevos de uno en uno, nunca poniendo uno grande sobre uno más pequeño, hasta dejarlos en el nido que indica la nota de Ibarra (carta 70).",
            "Al acertar, queda libre el hueco donde está el núcleo. Coged la carta 80."],
        pistas=["Leed la nota (carta 70): dice en qué nido hay que dejar los huevos.", "Solo se mueve un huevo cada vez, y nunca uno grande sobre uno más pequeño. Con cuatro huevos hacen falta quince movimientos.", "Con cuatro huevos, el primer movimiento es llevar el más pequeño al nido de piedras; luego, seguid el patrón: el pequeño se mueve cada dos movimientos, siempre en el mismo sentido (ramas, piedras, plumas, ramas…)."],
        arte="Tres nidos de dinosaurio en el suelo de una cueva: uno de ramas con cuatro huevos enormes apilados de distinto tamaño, otro de piedras y otro de plumas vacíos, con luz naranja de lava."),
    "70": dict(
        titulo="Carta 70 — Nota de Ibarra", tipo="gris",
        descripcion=["Una nota del doctor Ibarra sobre los huevos. Sirve para los huevos y nidos (carta 69)."],
        pistas=["Dice dónde debéis dejar los huevos.", "Sirve para los huevos y nidos (carta 69)."],
        textoCarta=["El núcleo está debajo de los huevos.", "Pasadlos con cuidado, de uno en uno,", "al nido de plumas."],
        arte="Una nota de papel clavada con una espina de cactus en un palo clavado en el suelo de una cueva, con un dibujo decorativo de un huevo grande y flechas, sin texto legible."),
    "80": dict(
        titulo="Carta 80 — La boca del géiser", tipo="gris", coge=[72, 76], descarta=[69, 70, 78],
        descripcion=[
            "Con los huevos a salvo, queda a la vista un hueco de roca caliente: el núcleo del Cronoportal brilla dentro, sobre la boca de un géiser a punto de estallar. Hay tres válvulas de bronce con manómetros (carta 72) y unas marcas de Ibarra con la presión segura (carta 76).",
            "Coged las cartas 72 y 76. Descartad las cartas 69, 70 y 78."],
        pistas=["Hay que calmar el géiser antes de coger el núcleo.", "Coged las cartas 72 y 76. Descartad las cartas 69, 70 y 78."],
        arte="El hueco de una cueva con un pequeño géiser humeante y, sobre su boca, un núcleo de energía brillante de color azul; al lado, tres válvulas de bronce con manómetros circulares conectadas por tubos. Cristina y Alberto se acercan protegiéndose del vapor. Cristina con gesto de esfuerzo, entrecerrando los ojos por el vapor; Alberto con expresión de preocupación y la mano alzada para protegerse."),
    "72": dict(
        titulo="Carta 72 — Válvulas del géiser", tipo="verde",
        descripcion=[
            "Es un juego de la app: tres válvulas que se abren de 0 a 6 y tres manómetros. Cada manómetro mide la presión que resulta de combinar las válvulas, de forma distinta. Hay que lograr los valores de presión segura que dan las marcas de Ibarra (carta 76).",
            "Al acertar, el géiser se calma y podéis coger el núcleo. Coged la carta 82."],
        pistas=["Las marcas de Ibarra (carta 76) dicen qué lectura debe marcar cada manómetro.", "Probad cada válvula sola: veréis cómo afecta a cada manómetro.", "Válvulas: la primera en 3, la segunda en 1 y la tercera en 4."],
        arte="Tres válvulas de bronce con volantes y tres manómetros circulares con agujas, conectados por tubos oxidados junto a la boca de un géiser, en una cueva con vapor y luz naranja."),
    "76": dict(
        titulo="Carta 76 — Marcas de presión", tipo="gris",
        descripcion=["Marcas de Ibarra con la presión segura de cada manómetro. Sirven para las válvulas del géiser (carta 72)."],
        pistas=["Es la presión que debe marcar cada manómetro.", "Sirve para las válvulas del géiser (carta 72)."],
        textoCarta=["Presión segura del géiser:", "primer manómetro 7,", "segundo 5 y tercero 11."],
        arte="Tres marcas de pintura roja sobre una roca de cueva, junto a un dibujo decorativo de un manómetro y una aguja, sin texto legible, iluminado por una linterna."),
    "82": dict(
        titulo="Carta 82 — El núcleo", tipo="gris", coge=[62], descarta=[72, 76, 80],
        descripcion=[
            "El géiser se apaga con un suspiro de vapor. Cristina recoge con unas pinzas el núcleo, caliente y brillante.",
            "Coged la carta 62. Descartad las cartas 72, 76 y 80."],
        pistas=["Recoged el núcleo.", "Coged la carta 62. Descartad las cartas 72, 76 y 80."],
        arte="Cristina sostiene con unas pinzas largas un núcleo de energía esférico y brillante de color azul, junto a la boca de un géiser ya apagado; Alberto la ilumina con una linterna, en una cueva con vapor. Cristina muy concentrada, con la lengua entre los dientes; Alberto sonriendo aliviado."),
    "62": dict(
        titulo="Carta 62 — Núcleo de energía", tipo="roja", combina=[12, 74],
        descripcion=["El núcleo del Cronoportal: una esfera de cristal azul con un fulgor interior. Combinadlo con el Cronoportal (carta 12): sumad sus números (62 + 12 = 74) y coged la carta 74."],
        pistas=["Es la pieza que faltaba.", "Combinad la carta 62 con la carta 12.", "Sumad los números de las dos cartas: 62 + 12 = 74."],
        arte="Una esfera de cristal azul con un fulgor interior y finas líneas de energía, sostenida sobre la palma de una mano con un guante, sobre un fondo de cueva con luz naranja."),
    "74": dict(
        titulo="Carta 74 — Cronoportal reconectado", tipo="gris", coge=[84, 86], descarta=[62, 12, 82],
        descripcion=[
            "El núcleo encaja con un chasquido y el Cronoportal se enciende, pero su energía se escapa: el aparato necesita un conductor. Las notas de Ibarra (carta 86) hablan de un esqueleto fósil que se encuentra junto al claro, «el fósil de la tormenta», un tiranosaurio. Hay que reconstruirlo (carta 84) para que su estructura de huesos haga de antena.",
            "Coged las cartas 84 y 86. Descartad las cartas 62, 12 y 82."],
        pistas=["El portal necesita un conductor de energía.", "Coged las cartas 84 y 86. Descartad las cartas 62, 12 y 82."],
        arte="El Cronoportal encendido con el núcleo azul encajado en su pecho, en un claro al atardecer; a pocos pasos, los huesos sueltos de un gran tiranosaurio fosilizado esparcidos sobre la tierra, y en el cielo el asteroide cada vez más grande. Cristina y Alberto miran los huesos con determinación. Cristina con ceño fruncido y gesto de determinación; Alberto con la boca abierta de asombro mirando el cielo."),
    "84": dict(
        titulo="Carta 84 — El esqueleto", tipo="verde",
        descripcion=[
            "Es un juego de la app: los huesos de un tiranosaurio, sueltos. El cráneo ya está colocado y la punta de la cola también. Hay que ordenar las piezas intermedias de forma que las marcas de cada articulación coincidan, según las notas de Ibarra (carta 86). Dos de las piezas no son de este esqueleto.",
            "Al acertar, el esqueleto se alza y el portal se abre. Coged la carta 99."],
        pistas=["Las notas de Ibarra (carta 86) explican cómo encajan los huesos.", "Cada hueso lleva marcas en sus dos extremos: las que se tocan deben ser iguales. Dos piezas sobran.", "Del cráneo a la cola van cinco piezas: la primera empieza con dos marcas y cada una empieza con las marcas con las que acaba la anterior. Las otras dos sobran."],
        arte="Los huesos sueltos de un gran tiranosaurio ordenados sobre la tierra de un claro, con el cráneo ya colocado en un extremo, bajo un cielo naranja con el asteroide brillante, y el Cronoportal azul detrás."),
    "86": dict(
        titulo="Carta 86 — Notas de montaje", tipo="gris",
        descripcion=["Notas de Ibarra sobre cómo se monta el esqueleto. Sirven para el esqueleto (carta 84)."],
        pistas=["Es la regla del montaje.", "Sirve para el esqueleto (carta 84)."],
        textoCarta=["Los huesos solo encajan si las marcas", "de sus articulaciones son iguales.", "Dos piezas no son de este esqueleto."],
        arte="Una hoja de notas de campo sujeta con una piedra, con dibujos decorativos de un esqueleto de dinosaurio y de huesos con puntos en sus extremos, sin texto legible, al atardecer."),
    "99": dict(
        titulo="Carta 99 — De vuelta a casa (FIN)", tipo="gris", descarta=[74, 84, 86],
        descripcion=[
            "El esqueleto se alza como una antena gigantesca y el Cronoportal se llena de energía. Se abre el portal justo cuando el asteroide ya ilumina todo el valle. Cristina se despide con la mano de un saurópodo que contempla el cielo, ajeno a todo.",
            "Aterrizan en su salón. Alberto mira el aparato: «Mañana, otro destino». Cristina sonríe. Descartad las cartas 74, 84 y 86.",
            "FIN."],
        pistas=[],
        arte="La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ven el cielo naranja del Cretácico, el asteroide y el esqueleto de un tiranosaurio. Llevan aún su ropa de expedición con barro. Cristina ríe a carcajadas, llena de alegría; Alberto, con una mezcla de euforia y alivio divertido. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(
    juego="Cretácico, hace 66 millones de años — El Valle de los Gigantes",
    estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
)

SPEC = dict(
    final="99",
    needs={"26": ["14", "16"], "28": ["20", "18"], "57": ["22", "35"], "44": ["40", "42"], "54": ["46", "48", "37"],
           "58": ["51", "52", "26"], "94": ["56", "38"], "78": ["64", "66"], "80": ["69", "70"], "82": ["72", "76"],
           "74": ["62", "12"], "99": ["84", "86"]},
    eventos={},
)

PARA_QUE = {
    "P": "Inicio: llegada al valle. Te manda coger la 10 y la 12.",
    "10": "El campamento: reparte las huellas, la guía, la excavación, las notas y la cuerda.",
    "12": "El Cronoportal sin núcleo: se combina con el núcleo de energía (62).",
    "14": "Huellas en el barro (app): reconocer cuatro huellas de dinosaurio.",
    "16": "Guía de huellas: cómo es la huella de cada dinosaurio.",
    "18": "Notas de excavación: cómo leer los números de la cuadrícula.",
    "20": "Excavación (app): deducir dónde están los huesos, como un buscaminas.",
    "22": "Cuerda: se combina con el garfio (35).",
    "26": "Croquis del barranco: frases para ordenar las capas de roca; te manda descartar las huellas.",
    "28": "El hallazgo: reparte el garfio y el ámbar.",
    "35": "Garfio de escalada: se combina con la cuerda (22).",
    "37": "Muestra de ámbar: la cadena de ADN del mosquito.",
    "57": "El barranco: resultado de 22 + 35; reparte la balsa y el diario.",
    "40": "Balsa del vado (app): puzle clásico de cruzar el río con criaturas.",
    "42": "Diario del doctor Ibarra (app de lectura): las normas del cruce.",
    "44": "La otra orilla: reparte el laboratorio y las capas de roca.",
    "46": "Secuenciador de ADN (app): completar la cadena complementaria.",
    "48": "Manual de laboratorio: la regla de emparejamiento del ADN.",
    "51": "Estratos (app): ordenar seis capas de roca de abajo arriba.",
    "52": "Cuaderno de capas: dos frases sobre capas de roca.",
    "54": "La caja abierta: reparte la batería.",
    "56": "Batería de campaña: se combina con la linterna (38).",
    "58": "El escondite: reparte la linterna.",
    "38": "Linterna sin pilas: se combina con la batería (56).",
    "94": "La cueva: resultado de 56 + 38; reparte los cristales y el dibujo.",
    "64": "Cristales de la cueva (app): apagar y encender una pared (estilo «luces»).",
    "66": "Dibujo rupestre: cómo debe quedar la pared de cristales.",
    "78": "La cámara del nido: reparte los huevos y la nota.",
    "69": "Huevos y nidos (app): mover huevos de uno en uno, sin poner uno grande sobre otro más pequeño.",
    "70": "Nota de Ibarra: en qué nido hay que dejar los huevos.",
    "80": "La boca del géiser: reparte las válvulas y las marcas.",
    "72": "Válvulas del géiser (app): ajustar tres válvulas para que tres manómetros marquen lo pedido.",
    "76": "Marcas de presión: la lectura que debe marcar cada manómetro.",
    "82": "El núcleo: reparte el núcleo de energía.",
    "62": "Núcleo de energía: se combina con el Cronoportal (12).",
    "74": "Cronoportal reconectado: resultado de 62 + 12; reparte el esqueleto y las notas.",
    "84": "El esqueleto (app): ordenar los huesos haciendo coincidir las marcas de sus articulaciones.",
    "86": "Notas de montaje: la regla del esqueleto.",
    "99": "Final de la aventura.",
}

PASOS = [
    dict(t="Llegada al Cretácico", que="Pon el Modo PC en el ordenador (solo debe haber la carta P en la mesa y el resto boca abajo en el mazo) y en el móvil abre el juego y pulsa Empezar. Lee la carta P: te manda coger la 10 y la 12.",
         acciones=[("leer", "P")], mesa=["P", "10", "12"]),
    dict(t="El campamento", que="Lee la carta 10. Descarta la P y coge 14, 16, 18, 20 y 22. Hay dos puzles: las huellas (14, con la guía 16) y la excavación (20, con las notas 18).",
         acciones=[("leer", "10")], mesa=["10", "12", "14", "16", "18", "20", "22"]),
    dict(t="Reconoce las huellas", que="En el móvil: Acción, 14. La guía (16) describe cada huella. De izquierda a derecha: Triceratops, Tiranosaurio, Anquilosaurio y Edmontosaurio. El mensaje te dice que cojas la 26.",
         acciones=[("app", "14", "carta 26")], mesa=["10", "12", "14", "16", "18", "20", "22", "26"]),
    dict(t="El croquis", que="Lee la carta 26. Te manda descartar la 14 y la 16. Guárdala: sus frases sirven para los estratos más adelante.",
         acciones=[("leer", "26")], mesa=["10", "12", "18", "20", "22", "26"]),
    dict(t="Excava", que="En el móvil: Acción, 20. Las notas (18) dicen que hay siete huesos. Marca B2, C4, D1, D5, E2, E3 y F5. El mensaje te dice que cojas la 28.",
         acciones=[("app", "20", "carta 28")], mesa=["10", "12", "18", "20", "22", "26", "28"]),
    dict(t="El hallazgo", que="Lee la carta 28. Descarta 20 y 18 y coge 35 y 37. El garfio (35) es combinable; la muestra de ámbar (37) tiene una cadena de ADN.",
         acciones=[("leer", "28")], mesa=["10", "12", "22", "26", "28", "35", "37"]),
    dict(t="Cuerda con garfio", que="La cuerda (22) y el garfio (35) son combinables: 22 + 35 = 57. Coge la 57.",
         acciones=[("combinar", "22", "35")], mesa=["10", "12", "22", "26", "28", "35", "37", "57"]),
    dict(t="El barranco", que="Lee la carta 57. Descarta 22, 35, 28 y 10 y coge 40 y 42.",
         acciones=[("leer", "57")], mesa=["12", "26", "37", "57", "40", "42"]),
    dict(t="El diario de Ibarra", que="En el móvil: Acción, 42. Pasa las páginas: explican qué criaturas no pueden quedarse solas en la orilla.",
         acciones=[("app", "42", "")], mesa=["12", "26", "37", "57", "40", "42"]),
    dict(t="Cruza el río", que="En el móvil: Acción, 40. Con la balsa cruza: el bebé, vuelta sin nada, el compsognato, vuelta con el bebé, los helechos, vuelta sin nada y el bebé. El mensaje te dice que cojas la 44.",
         acciones=[("app", "40", "carta 44")], mesa=["12", "26", "37", "57", "40", "42", "44"]),
    dict(t="La otra orilla", que="Lee la carta 44. Descarta 40, 42 y 57 y coge 46, 48, 51 y 52. Hay dos puzles: el secuenciador (46, con la muestra 37 y el manual 48) y los estratos (51, con el croquis 26 y el cuaderno 52).",
         acciones=[("leer", "44")], mesa=["12", "26", "37", "44", "46", "48", "51", "52"]),
    dict(t="Abre la caja con el ADN", que="En el móvil: Acción, 46. La muestra (37) es A T G C C G T A; el manual (48) dice que A va con T y C con G. Escribe la cadena nueva: T A C G G C A T. El mensaje te dice que cojas la 54.",
         acciones=[("app", "46", "carta 54")], mesa=["12", "26", "37", "44", "46", "48", "51", "52", "54"]),
    dict(t="La caja abierta", que="Lee la carta 54. Descarta 46, 48 y 37 y coge la 56, una batería.",
         acciones=[("leer", "54")], mesa=["12", "26", "44", "51", "52", "54", "56"]),
    dict(t="Ordena los estratos", que="En el móvil: Acción, 51. Con el croquis (26) y el cuaderno (52), de abajo arriba: conchas, caliza, arcilla, arenisca, carbón y ceniza. El mensaje te dice que cojas la 58.",
         acciones=[("app", "51", "carta 58")], mesa=["12", "26", "44", "51", "52", "54", "56", "58"]),
    dict(t="El escondite", que="Lee la carta 58. Descarta 51, 52 y 26 y coge la 38, una linterna sin pilas.",
         acciones=[("leer", "58")], mesa=["12", "44", "54", "56", "58", "38"]),
    dict(t="Linterna con batería", que="La batería (56) y la linterna (38) son combinables: 56 + 38 = 94. Coge la 94.",
         acciones=[("combinar", "56", "38")], mesa=["12", "44", "54", "56", "58", "38", "94"]),
    dict(t="La cueva", que="Lee la carta 94. Descarta 56, 38, 44, 54 y 58 y coge 64 y 66. El dibujo rupestre (66) muestra cómo debe quedar la pared de cristales (64).",
         acciones=[("leer", "94")], mesa=["12", "94", "64", "66"]),
    dict(t="La pared de cristales", que="En el móvil: Acción, 64. Pulsa B1, A2, B2, A3 y D3 para dejar la pared como el dibujo (66). El mensaje te dice que cojas la 78.",
         acciones=[("app", "64", "carta 78")], mesa=["12", "94", "64", "66", "78"]),
    dict(t="La cámara del nido", que="Lee la carta 78. Descarta 64, 66 y 94 y coge 69 y 70. La nota (70) dice que los huevos deben acabar en el nido de plumas.",
         acciones=[("leer", "78")], mesa=["12", "78", "69", "70"]),
    dict(t="Mueve los huevos", que="En el móvil: Acción, 69. Pasa los cuatro huevos de uno en uno, sin poner uno grande sobre uno más pequeño, hasta el nido de plumas (quince movimientos). El mensaje te dice que cojas la 80.",
         acciones=[("app", "69", "carta 80")], mesa=["12", "78", "69", "70", "80"]),
    dict(t="La boca del géiser", que="Lee la carta 80. Descarta 69, 70 y 78 y coge 72 y 76. Las marcas (76) dan la presión segura de los tres manómetros: 7, 5 y 11.",
         acciones=[("leer", "80")], mesa=["12", "80", "72", "76"]),
    dict(t="Calma el géiser", que="En el móvil: Acción, 72. Pon las válvulas en 3, 1 y 4 para que los manómetros marquen 7, 5 y 11. El mensaje te dice que cojas la 82.",
         acciones=[("app", "72", "carta 82")], mesa=["12", "80", "72", "76", "82"]),
    dict(t="El núcleo", que="Lee la carta 82. Descarta 72, 76 y 80 y coge la 62, el núcleo de energía.",
         acciones=[("leer", "82")], mesa=["12", "82", "62"]),
    dict(t="Núcleo en el Cronoportal", que="El Cronoportal (12) y el núcleo (62) son combinables: 12 + 62 = 74. Coge la 74.",
         acciones=[("combinar", "12", "62")], mesa=["12", "82", "62", "74"]),
    dict(t="Cronoportal reconectado", que="Lee la carta 74. Descarta 62, 12 y 82 y coge 84 y 86. Las notas (86) explican cómo montar el esqueleto.",
         acciones=[("leer", "74")], mesa=["74", "84", "86"]),
    dict(t="Monta el esqueleto", que="En el móvil: Acción, 84. Con las notas (86), coloca del cráneo a la cola las cinco piezas que encadenan sus marcas: 2-4, 4-1, 1-3, 3-2 y 2 (sobran las otras dos). El mensaje te dice que cojas la 99.",
         acciones=[("app", "84", "carta 99")], mesa=["74", "84", "86", "99"]),
    dict(t="Final", que="Lee la carta 99. Descarta 74, 84 y 86. En la mesa solo queda la 99. ¡Fin!",
         acciones=[("leer", "99")], mesa=["99"]),
]

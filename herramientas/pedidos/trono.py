# Gráficos de los minijuegos de Trono (objetos sobre negro puro; se mezclan con `screen`; las texturas van a pantalla completa).
# `NEGRO` lo inyecta chatgpt_fondos.py. Generar con:  python herramientas/chatgpt_fondos.py --solo trono
# Los minijuegos funcionan sin estas imágenes (dibujos CSS/SVG de respaldo). Al generarlas, ejecutar herramientas/listar_imagenes_trono.py
# para que los minijuegos las usen (juegos/aventuras-ca/trono/img/ui/disponibles.json).
D = "juegos/aventuras-ca/trono/img/ui/"
EST = " Estilo pintura digital oscura, realista y cinematográfica de fantasía medieval, luz fría de invierno con destellos cálidos de antorcha."
FILA = " muy separados entre sí, cada uno centrado y del mismo tamaño."
SIN = " Sin texto, letras ni números. Sin personas. Vista plana, sin perspectiva."

PEDIDOS = [
    # ---- texturas del panel (se ponen con baja opacidad detrás de cada minijuego) ----
    dict(destino=D + "piedra.jpg", ancho=720,
         prompt="Crea una textura de muro de piedra negra de una fortaleza medieval, con sillares irregulares cubiertos de escarcha, musgo oscuro y manchas de hollín, "
                "luz fría con un reflejo cálido de antorcha en un lado y el centro liso y limpio para poder poner interfaz encima. Formato vertical 2:3." + SIN),
    dict(destino=D + "mesa.jpg", ancho=720,
         prompt="Crea una textura de tablero de una larga mesa de banquete de roble oscuro, vista desde arriba, con vetas, marcas de cuchillos y gotas de cera, "
                "iluminada por velas desde los bordes y el centro liso y limpio. Formato vertical 2:3." + SIN),
    dict(destino=D + "mapa.jpg", ancho=720,
         prompt="Crea una textura de pergamino de mapa antiguo, oscurecido y quemado por los bordes, con un marco de línea de tinta y pequeñas rosas de los vientos decorativas "
                "SIN ningún texto, luz de vela y el centro liso y limpio. Formato vertical 2:3." + SIN),
    dict(destino=D + "cripta.jpg", ancho=720,
         prompt="Crea una textura de suelo de losas de piedra negra de una cripta, agrietadas, con polvo y un brillo naranja muy tenue entre las juntas, "
                "vista desde arriba y el centro liso y limpio. Formato vertical 2:3." + SIN),
    dict(destino=D + "puerta.jpg", ancho=720,
         prompt="Crea una textura de una inmensa puerta de bronce oxidado con relieves de dragones y remaches, vista de frente, con reflejos de antorchas en los bordes "
                "y el centro liso y limpio. Formato vertical 2:3." + SIN),
    dict(destino=D + "pergamino.jpg", ancho=720,
         prompt="Crea una textura de pergamino de tapicera o maestre, color crema oscurecido con manchas, bordes desgastados y el centro liso y limpio. Formato vertical 2:3." + SIN),
    # ---- sprites sobre negro (modo screen) ----
    dict(destino=D + "cuervo.jpg", ancho=300,
         prompt="Crea un cuervo negro posado, visto de perfil y centrado, con plumas azuladas y un ojo brillante." + EST + NEGRO),
    dict(destino=D + "castillo.jpg", ancho=300,
         prompt="Crea una pequeña fortaleza medieval de piedra gris con dos torres y una muralla almenada, vista de frente y centrada, con nieve en los tejados." + EST + NEGRO),
    dict(destino=D + "antorcha.jpg", ancho=300,
         prompt="Crea la llama de una antorcha encendida, de color naranja y amarillo vivo, con chispas, vista de frente y centrada, solo el fuego sin el palo." + EST + NEGRO),
    # ---- piezas del atasco (texturas que rellenan cada pieza) ----
    dict(destino=D + "tronco.jpg", ancho=420,
         prompt="Crea una textura de un tronco de madera de pino gruesa y oscura, con corteza rugosa y anillos de hierro, vista desde arriba y en horizontal." + SIN),
    dict(destino=D + "carro.jpg", ancho=420,
         prompt="Crea una textura de la lona gris y las tablas de un carro de carga medieval, vista desde arriba, con cuerdas y remaches." + SIN),
    # ---- tapiz ----
    dict(destino=D + "tapiz/hilo.jpg", ancho=240,
         prompt="Crea una textura cuadrada de hilo de lana rojo y dorado tejido a mano, muy de cerca, con las fibras visibles, iluminación uniforme." + SIN),
    # ---- retratos de los consejeros (no van sobre negro: se recortan en un círculo) ----
    dict(destino=D + "consejeros", ancho=260, hoja=(4, 1), nombres=["aldric", "brenna", "corvin", "dalia"],
         prompt="Crea UNA SOLA IMAGEN apaisada con CUATRO retratos de busto de consejeros medievales, en una fila, cada uno centrado y del mismo tamaño y con el mismo fondo oscuro liso, "
                "de izquierda a derecha: 1) Aldric, un anciano calvo con cadenas de oro al cuello y gesto altivo; 2) Brenna, una mujer de pelo gris recogido con mirada fría; "
                "3) Corvin, un hombre joven con capa de piel y mirada franca; 4) Dalia, una mujer de ojos oscuros y trenza negra con gesto astuto." + EST + " Sin texto."),
]

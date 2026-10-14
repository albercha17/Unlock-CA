# Gráficos de los minijuegos de «Cuento» (objetos sobre negro puro que se mezclan con `screen`; las texturas van a pantalla completa).
# Mientras no existan, los minijuegos usan dibujos CSS de respaldo; al generarlas ejecuta `python herramientas/listar_imagenes_ui.py juegos/aventuras-ca/cuento`.
D = "juegos/aventuras-ca/cuento/img/ui/"
EST = " Estilo dibujos animados 2D clásicos de cuento, trazo limpio, colores vivos y suaves, luz mágica con destellos dorados."
FILA = " muy separados entre sí, cada uno centrado y del mismo tamaño."
SIN = " Sin texto, letras ni números. Sin personas. Vista plana, sin perspectiva."

PEDIDOS = [
    # ---- texturas generales ----
    dict(destino=D + "panel.jpg", ancho=720,
         prompt="Crea una textura de panel de cuento: un marco de enredaderas con florecitas y estrellitas doradas sobre un fondo morado profundo, con el centro liso y limpio para poder poner interfaz encima. Formato vertical 2:3." + EST + SIN),
    dict(destino=D + "papel.jpg", ancho=720,
         prompt="Crea una textura de pergamino de cuento: papel color crema con bordes desgastados y una fina filigrana dorada en las esquinas, el centro liso y limpio. Formato vertical 2:3." + EST + SIN),
    # ---- cartel de la panadería (14): se superpone con multiply sobre el cartel ----
    dict(destino=D + "cartel.jpg", ancho=640,
         prompt="Crea una textura de tablas de madera cálida de un cartel de panadería de cuento, con vetas, nudos y clavos pequeños, vista de frente plana, iluminación uniforme. Formato apaisado 4:3." + EST + SIN),
    # ---- puente del troll (20): columna estrecha del río ----
    dict(destino=D + "puente.jpg", ancho=320,
         prompt="Crea la imagen de un puente de piedra de cuento visto de frente, de noche, sobre un río azul oscuro con reflejos de luna y una luciérnaga dorada flotando. Formato vertical estrecho 1:3." + EST + " Fondo muy oscuro, casi negro. Sin texto, letras ni números. Sin personas."),
    # ---- vidriera (46): fondo del tablero 5x5 ----
    dict(destino=D + "vidriera.jpg", ancho=520,
         prompt="Crea una vidriera de catedral de cuento vista de frente: un marco de plomos dorados que forman una cuadrícula de cinco por cinco cuadrados con cristal oscuro azul noche y destellos tenues. Formato cuadrado." + EST + " Fondo muy oscuro. Sin texto, letras ni números. Sin personas."),
    # ---- sala de los espejos (64): fondo del tablero 5x5 ----
    dict(destino=D + "sala-espejos.jpg", ancho=520,
         prompt="Crea el suelo de piedra azulada de una sala de espejos de cuento visto desde arriba, con reflejos plateados y luz de luna muy suave, sin muros ni objetos. Formato cuadrado." + EST + " Muy oscuro. Sin texto, letras ni números. Sin personas."),
    # ---- tarros (69): fondo de la fila de tarros ----
    dict(destino=D + "tarros.jpg", ancho=640,
         prompt="Crea una mesa larga de cocina de castillo de cuento vista de frente, de madera cálida con utensilios de cocina colgados al fondo y un mantel a cuadros, sin tarros ni comida. Formato apaisado 4:3." + EST + SIN),
    # ---- página (84) ----
    dict(destino=D + "pagina.jpg", ancho=640,
         prompt="Crea una página en blanco de un libro de cuentos antiguo: papel color crema con una cenefa dorada muy fina en los bordes y el centro liso. Formato apaisado 4:3." + EST + SIN),
    # ---- hadas (51): sin ningún color rojo ni azul en las alas, para no delatar quién miente ----
    dict(destino=D + "hadas", ancho=260, hoja=(4, 1), nombres=["brisa", "lila", "nube", "dalia"],
         prompt="Crea UNA SOLA IMAGEN apaisada con CUATRO hadas pequeñas de cuento de cuerpo entero en una fila," + FILA +
                " De izquierda a derecha: 1) Brisa, de pelo castaño rizado y vestido verde menta; 2) Lila, de pelo morado en una trenza y vestido lila; "
                "3) Nube, de pelo blanco esponjoso y vestido gris perla; 4) Dalia, de pelo rubio con una flor y vestido amarillo. "
                "Todas tienen alas transparentes e iridiscentes de color dorado pálido (SIN rojo y SIN azul) y expresiones distintas: seria, traviesa, inocente y orgullosa." + EST + " Fondo negro puro (#000000) liso y uniforme. Sin texto, letras ni números."),
    # ---- animales de la caja de música (72) ----
    dict(destino=D + "animales", ancho=220, hoja=(3, 2), nombres=["conejo", "ciervo", "buho", "rana", "ardilla", "zorro"],
         prompt="Crea UNA SOLA IMAGEN apaisada con SEIS animalitos de bosque de cuento, tallados en madera dorada y pintados, vistos de frente, en dos filas de tres," + FILA +
                " Fila de arriba, de izquierda a derecha: un conejo, un ciervo, un búho. Fila de abajo: una rana, una ardilla, un zorro." + EST + " Fondo negro puro (#000000) liso y uniforme. Sin texto, letras ni números."),
]

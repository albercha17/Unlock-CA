# Gráficos de los minijuegos de Florencia (objetos sobre negro puro; se mezclan con `screen`).
D = "juegos/aventuras-ca/florencia/img/ui/"
EST = " Estilo pintura realista muy detallada del Renacimiento: latón, bronce, cristal, madera y pergamino, luz cálida de vela."
FILA = " muy separados entre sí, cada uno centrado y del mismo tamaño."

PEDIDOS = [
    dict(destino=D + "engranajes", ancho=300, hoja=(4, 1), nombres=["pequena", "mediana", "grande", "manivela"],
         prompt="Crea UNA SOLA IMAGEN apaisada con CUATRO engranajes de latón vistos exactamente desde arriba (perfectamente circulares), en una fila," + FILA +
                " De izquierda a derecha: 1) un engranaje con 8 dientes y 6 radios, 2) uno con 16 dientes y 8 radios, 3) uno con 32 dientes y 10 radios, "
                "4) un engranaje con 16 dientes y una manivela de madera con empuñadura clavada en el eje." + EST + NEGRO),
    dict(destino=D + "placas", ancho=200, hoja=(2, 1), nombres=["laton", "oscura"],
         prompt="Crea UNA SOLA IMAGEN con DOS placas cuadradas de latón vistas de frente, lado a lado," + FILA +
                " A la izquierda una placa de latón pulido y brillante con bordes biselados y cuatro remaches; a la derecha la MISMA placa pero de bronce oscuro y envejecido, apagada. Sin ningún número ni grabado." + EST + NEGRO),
    dict(destino=D + "vasos", ancho=260, hoja=(2, 1), nombres=["vaso3", "vaso5"],
         prompt="Crea UNA SOLA IMAGEN con DOS vasos cilíndricos de cristal transparente vacíos, de paredes rectas y borde de latón, vistos de frente, lado a lado," + FILA +
                " El de la izquierda es BAJO (la mitad de alto) y el de la derecha es ALTO (el doble de alto que el otro). Cristal muy transparente con reflejos." + EST + NEGRO),
    dict(destino=D + "ornitoptero", ancho=520, hoja=(1, 3), nombres=["corto", "medio", "largo"],
         prompt="Crea UNA SOLA IMAGEN con TRES versiones del ornitóptero de Leonardo da Vinci vistas de frente con las alas extendidas, APILADAS EN VERTICAL (una encima de otra, en tres filas), con las alas completas dentro del encuadre," + FILA +
                " Todas con la misma estructura de madera y un pequeño asiento central; la de arriba con alas CORTAS, la del centro con alas de longitud MEDIA y la de abajo con alas muy LARGAS. "
                "Alas de tela blanca natural sobre un armazón de madera." + EST + NEGRO),
    dict(destino=D + "saco.jpg", ancho=200,
         prompt="Crea un saco de arena de tela de yute atado con una cuerda, visto de frente." + NEGRO),
    dict(destino=D + "disco.jpg", ancho=640,
         prompt="Crea un disco de cifrado renacentista de bronce visto exactamente desde arriba (perfectamente circular): dos anillos concéntricos ornamentados con relieves decorativos "
                "y SIN NINGUNA LETRA NI NÚMERO, con un eje central de latón." + EST + NEGRO),
    dict(destino=D + "taller", ancho=420, hoja=(4, 1), nombres=["columna", "atril", "portal", "claraboya"],
         prompt="Crea UNA SOLA IMAGEN apaisada con CUATRO objetos vistos desde arriba, en una fila," + FILA +
                " De izquierda a derecha: 1) una columna de mármol cortada (sección circular con acanalados), 2) un atril de madera tallada para sostener una lente, 3) una consola de latón y cristal "
                "con un anillo central apagado (el Cronoportal), 4) un lucernario redondo de cristal por el que entra un rayo de luz dorada." + EST + NEGRO),
    dict(destino=D + "suelo.jpg", ancho=720,
         prompt="Crea una textura de suelo de taller renacentista visto desde arriba: grandes losas de piedra clara con juntas, polvo y manchas de tinta, luz cálida suave. "
                "Sin texto, letras ni números. Sin personas. Formato apaisado 3:2."),
    dict(destino=D + "rueda.jpg", ancho=200,
         prompt="Crea una rueda numérica de latón de cerradura de cofre, vista de frente, con un borde estriado y SIN NINGÚN NÚMERO NI LETRA." + NEGRO),
]

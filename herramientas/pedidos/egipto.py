# Gráficos de los minijuegos de Egipto (objetos sobre negro puro; se mezclan con `screen`).
D = "juegos/aventuras-ca/egipto/img/ui/"
EST = " Estilo pintura realista muy detallada del antiguo Egipto: oro, lapislázuli, piedra arenisca, luz cálida de antorcha."
FILA = " muy separados entre sí, cada uno centrado y del mismo tamaño, vistos de frente."

PEDIDOS = [
    dict(destino=D + "glifos", ancho=240, hoja=(4, 2),
         nombres=["vasija", "ojo", "sol", "escarabajo", "serpiente", "halcon", "agua", "toro"],
         prompt="Crea UNA SOLA IMAGEN con OCHO símbolos egipcios grabados en relieve dorado, dispuestos en una cuadrícula de 4 columnas por 2 filas," + FILA +
                " De izquierda a derecha y de arriba abajo: 1) una vasija de agua, 2) el ojo de Horus, 3) el disco solar con rayos, 4) un escarabajo sagrado, "
                "5) una serpiente cobra, 6) un halcón, 7) tres ondas de agua, 8) la cabeza de un toro. Relieve dorado brillante, sin fondo de piedra." + EST + NEGRO),
    dict(destino=D + "gemas", ancho=240, hoja=(4, 1), nombres=["amarilla", "azul", "verde", "roja"],
         prompt="Crea UNA SOLA IMAGEN apaisada con CUATRO gemas talladas con facetas, vistas desde arriba, en una fila," + FILA +
                " De izquierda a derecha: una gema AMARILLA (citrino), una AZUL (zafiro), una VERDE (esmeralda) y una ROJA (rubí), cada una con engarce dorado, muy brillantes y translúcidas." + NEGRO),
    dict(destino=D + "balanza-a", ancho=420, hoja=(2, 1), nombres=["pilar", "plato"],
         prompt="Crea UNA SOLA IMAGEN apaisada con DOS piezas de una balanza de oro egipcia, en una fila," + FILA +
                " De izquierda a derecha: 1) el pilar vertical con base y un cabezal con eje (sin brazo), 2) un plato colgante de oro con tres cadenas que se juntan arriba en un anillo." + EST + NEGRO),
    dict(destino=D + "balanza-a/brazo.jpg", ancho=640,
         prompt="Crea el brazo horizontal de una balanza de oro egipcia: una barra larga y recta, con adornos de lapislázuli, un eje central y dos ganchos en los extremos, "
                "vista de frente, ocupando TODO el ancho de la imagen, en formato muy apaisado 4:1." + EST + NEGRO),
    dict(destino=D + "balanza-b", ancho=300, hoja=(3, 1), nombres=["corazon", "pluma", "pesa"],
         prompt="Crea UNA SOLA IMAGEN apaisada con TRES objetos en una fila," + FILA +
                " De izquierda a derecha: 1) un corazón de piedra pulida rojiza, 2) una pluma de avestruz blanca (la pluma de Maat), 3) una pesa de piedra con asa de bronce." + EST + NEGRO),
    dict(destino=D + "piedra.jpg", ancho=420,
         prompt="Crea una textura de piedra arenisca antigua, vista de frente y plana, con grano fino y pequeñas grietas, tonos ocre dorado, iluminación cálida suave y uniforme. "
                "Sin texto, letras ni números. Sin personas. Formato cuadrado."),
    dict(destino=D + "papiro.jpg", ancho=720,
         prompt="Crea una textura de papiro egipcio antiguo, vista cenital plana, fibras visibles, tono dorado claro, bordes irregulares y envejecidos y el centro liso y limpio. "
                "El papiro debe llenar la imagen de borde a borde, SIN márgenes blancos ni fondo visible. Sin texto, letras ni números. Sin personas. Formato vertical 2:3."),
]

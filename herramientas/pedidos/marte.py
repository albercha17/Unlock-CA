# Gráficos de los minijuegos de Marte (objetos sobre negro puro; se mezclan con `screen`).
D = "juegos/aventuras-ca/marte/img/ui/"
EST = " Estilo pintura realista muy detallada de ciencia ficción, metal pulido y desgastado por el polvo rojo de Marte, luces naranjas y cian."
FILA = " muy separados entre sí, cada uno centrado y del mismo tamaño."

PEDIDOS = [
    dict(destino=D + "tuberias", ancho=300, hoja=(4, 1), nombres=["recta", "codo", "entrada", "salida"],
         prompt="Crea UNA SOLA IMAGEN apaisada con CUATRO piezas de tubería industrial de una colonia marciana vistas desde arriba, en una fila," + FILA +
                " De izquierda a derecha: 1) un tubo RECTO horizontal que atraviesa toda la pieza de lado a lado, con juntas y tornillos, 2) un CODO de tubería que une el borde IZQUIERDO con el borde INFERIOR en un cuarto de círculo, "
                "3) una válvula de entrada de oxígeno con un depósito azul y el tubo saliendo hacia la derecha, 4) una compuerta/esclusa de salida con una luz verde y el tubo entrando por la izquierda." + EST + NEGRO),
    dict(destino=D + "interruptores", ancho=220, hoja=(2, 1), nombres=["apagado", "encendido"],
         prompt="Crea UNA SOLA IMAGEN con DOS interruptores de palanca industriales idénticos, vistos de frente, lado a lado," + FILA +
                " A la izquierda uno APAGADO (palanca abajo, piloto apagado) y a la derecha el MISMO ENCENDIDO (palanca arriba, piloto naranja encendido). Carcasa de metal con tornillos." + EST + NEGRO),
    dict(destino=D + "monitor-marco.jpg", ancho=640,
         prompt="Crea un marco de monitor de ordenador de colonia marciana, visto de frente: un bisel grueso de metal gris con tornillos, botones pequeños y luces de estado naranjas, "
                "con la pantalla del centro COMPLETAMENTE NEGRA y rectangular. Formato apaisado 4:3." + EST + " Fondo negro puro. Sin texto, letras ni números. Sin personas."),
    dict(destino=D + "rover", ancho=240, hoja=(2, 1), nombres=["rover", "roca"],
         prompt="Crea UNA SOLA IMAGEN con DOS objetos vistos desde arriba, lado a lado," + FILA +
                " A la izquierda un pequeño rover de exploración marciano de seis ruedas con antena y panel solar; a la derecha una roca marciana rojiza y rugosa." + EST + NEGRO),
    dict(destino=D + "terreno.jpg", ancho=720,
         prompt="Crea una textura de terreno de Marte vista desde arriba, plana: tierra rojiza con grava fina y polvo, tonos óxido, iluminación uniforme sin sombras largas. "
                "Sin texto, letras ni números. Sin personas. Formato apaisado 3:2."),
    dict(destino=D + "modulos", ancho=240, hoja=(3, 2), nombres=["escudo", "radio", "luz", "bomba", "calefaccion", "ordenador"],
         prompt="Crea UNA SOLA IMAGEN con SEIS módulos de una colonia marciana en una cuadrícula de 3 columnas por 2 filas," + FILA +
                " De izquierda a derecha y de arriba abajo: 1) un generador de escudo protector con un cristal azul, 2) una antena parabólica de radio, 3) una lámpara LED de techo, "
                "4) una bomba de agua con tubos y manómetro, 5) un calefactor con resistencias al rojo, 6) un ordenador central con pantalla verde." + EST + NEGRO),
]

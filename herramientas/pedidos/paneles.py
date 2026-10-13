# Texturas generales del panel de los minijuegos (una por juego). `NEGRO` lo inyecta chatgpt_fondos.py.
SIN = " Sin texto, letras ni números. Sin personas. Vista frontal plana, sin perspectiva, formato vertical 2:3."

PEDIDOS = [
    dict(destino="juegos/el-faro/img/ui/panel.jpg",
         prompt="Crea una textura de panel de madera oscura de cabina de barco, con listones verticales, remaches y esquinas de latón envejecido, "
                "humedad y salitre, iluminación tenue de farol desde un lado y el centro liso y limpio para poder poner interfaz encima." + SIN),
    dict(destino="juegos/aventuras-ca/egipto/img/ui/panel.jpg",
         prompt="Crea una textura de losa de arenisca antigua del antiguo Egipto con un marco decorativo de bandas de jeroglíficos y lapislázuli "
                "en los bordes (sin significado legible), luz cálida de antorcha y el centro liso y limpio para poder poner interfaz encima." + SIN),
    dict(destino="juegos/aventuras-ca/marte/img/ui/panel.jpg",
         prompt="Crea una textura de panel metálico industrial de una colonia en Marte, cubierto de polvo rojizo fino, con tornillos, juntas, cables "
                "y pequeñas luces de estado naranjas en los bordes y el centro liso y limpio para poder poner interfaz encima." + SIN),
    dict(destino="juegos/aventuras-ca/florencia/img/ui/panel.jpg",
         prompt="Crea una textura de pergamino antiguo con bordes quemados y filigrana renacentista dorada decorativa en las esquinas, luz de vela "
                "y el centro liso y limpio para poder poner interfaz encima." + SIN),
]

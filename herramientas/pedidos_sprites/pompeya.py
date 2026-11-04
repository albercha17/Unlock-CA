# Sprites de «Pompeya, 79 d.C.» con ChatGPT: las seis cargas de la barca y las ocho figuras de los mosaicos.
ESTILO = (" Estilo de ilustración de aventura histórica romana pintada a mano, con luz cálida de mediodía mediterráneo, colores terrosos y detalles de cerámica, tela y piedra.")

PEDIDOS = [
    dict(destino="juegos/aventuras-ca/pompeya/img/ui", prefijo="carga-", hoja=(3, 2), ancho=300, clave="magenta",
         nombres=["anfora_aceite", "anfora_vino", "cofre_monedas", "estatua_lar", "fardo_lana", "saco_trigo"],
         prompt="Crea una hoja con 6 cargas de una barca romana, en 2 filas de 3, cada una entera y de frente: un ánfora de aceite de barro cocido clara con tapón; un ánfora de vino "
                "más oscura y rojiza con las asas; un cofre de madera lleno de monedas de oro; una pequeña estatua de bronce de un dios lar de pie; un fardo grande de lana blanca atado con cuerdas; "
                "un saco de trigo de tela atado." + ESTILO),
    dict(destino="juegos/aventuras-ca/pompeya/img/ui", prefijo="fig-", hoja=(4, 2), ancho=300, clave="magenta",
         nombres=["anfora", "concha", "delfin", "escudo", "laurel", "lechuza", "lucerna", "racimo"],
         prompt="Crea una hoja con 8 figuras de mosaico romano hechas con pequeñas teselas de colores, cada una dentro de un medallón circular, en 2 filas de 4, bien separadas: "
                "un ánfora; una concha; un delfín; un escudo redondo; una corona de laurel; una lechuza; una lucerna (lámpara de aceite de barro); un racimo de uvas. "
                "Teselas cuadradas pequeñas en azul, crema, oro y terracota." + ESTILO),
]

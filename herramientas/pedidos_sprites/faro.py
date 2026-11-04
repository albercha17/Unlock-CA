# Sprites de «El Faro de Cabo Niebla» con ChatGPT: los ocho objetos del estante del farero (sirven de objeto y, por su silueta, de sombra).
ESTILO = (" Estilo de ilustración pintada a mano en acuarela y gouache, de libro ilustrado de misterio marinero, con texturas de papel, tonos azul petróleo, gris niebla "
          "y toques de luz ámbar cálida; cada objeto con una silueta muy reconocible y distinta de las demás.")

PEDIDOS = [
    dict(destino="juegos/el-faro/img/ui", prefijo="spr-", hoja=(4, 2), ancho=360, clave="magenta",
         nombres=["farol", "ancla", "botella", "tetera", "gaviota", "catalejo", "campana", "llave"],
         prompt="Crea una hoja con 8 objetos del estante de un viejo farero, en 2 filas de 4, cada uno entero y de frente. Fila 1: un farol de marinero de latón con asa y cristal; "
                "un ancla de hierro oscuro; una botella de cristal verde con corcho; una tetera de latón con asa y pitorro. "
                "Fila 2: una gaviota blanca disecada posada, de perfil; un catalejo de latón y cuero, cerrado, puesto de pie; una campana de barco de bronce con su badajo; "
                "una llave grande antigua de hierro con ojo redondo." + ESTILO),
]

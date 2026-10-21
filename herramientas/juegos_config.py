"""Configuración común de los juegos de Aventuras C&A y generación de su index.html a partir de la plantilla del Faro."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import datos_egipto as E
import datos_marte as M
import datos_florencia as F
import datos_dinosaurios as D
import datos_cuento as C
import datos_trono as T
import datos_pompeya as P
import datos_arcade as A
import datos_oeste as W
import datos_espia as S
import datos_futbol as Fu
import datos_piratas as Pi
import datos_juguetes as Ju

FARO = "juegos/el-faro"
FARO_SINOPSIS = "Tormenta, la gran lámpara apagada y un carguero a ciegas rumbo a las rocas. Cristina y Alberto tienen hora y cuarto para encender el faro... y encontrar al abuelo Anselmo."


def leer(p):
    return open(p, encoding="utf-8").read()


def escribir(p, txt):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write(txt)


def sustituir(txt, viejo, nuevo, veces=1):
    if veces is None:
        assert viejo in txt, viejo
        return txt.replace(viejo, nuevo)
    assert txt.count(viejo) == veces, f"se esperaban {veces} apariciones de {viejo[:60]!r} y hay {txt.count(viejo)}"
    return txt.replace(viejo, nuevo)


JUEGOS = {
    "Egipto": dict(
        datos=E, dificultad=4, tema="egipto", titulo="Egipto, 1274 a.C.: El Ojo de Horus", emoji="🏺", minutos=90,
        grad="#4a3512,#150f05", acento="#e0b04a", acento2="#f2d27a", bg1="#120d05", bg2="#2a1d0a",
        sinopsis="Cristina y Alberto estrenan su Cronoportal y aterrizan en una cámara secreta bajo un templo de Tebas, en el año 1274 a.C., con el aparato sin energía. Para encontrar el Ojo de Horus tendrán que abrir un granero con un acertijo de sacos, desbloquear una pirámide de sumas, medir la crecida del Nilo, contar los animales de un friso, cuadrar las cuentas de un escriba con las partes del ojo, descifrar un criptograma de jeroglíficos, pintar las cámaras de un templo, trazar canales de riego, repartir un campo y completar un friso de azulejos. Solo tienen hora y media antes de que lleguen los sacerdotes.",
        minigames={"14": "14-monton.js", "20": "20-piramide.js", "40": "40-nilometro.js", "48": "48-friso.js", "52": "52-heqat.js", "46": "46-cripto.js",
                   "51": "51-camaras.js", "69": "69-canales.js", "64": "64-azulejos.js", "72": "72-tierras.js", "85": "85-sellos.js"},
        pal=("#7a5a1e", "#2a1d0a")),
    "Marte": dict(
        datos=M, dificultad=4, tema="marte", titulo="Marte, 2157: Cúpula Aurora", emoji="🚀", minutos=90,
        grad="#5a2a14,#12060a", acento="#ff8a50", acento2="#ffb085", bg1="#12070a", bg2="#2a120c",
        sinopsis="Segundo salto del Cronoportal: Marte, año 2157. La cúpula Aurora está a oscuras por una tormenta de polvo y el soporte vital se apaga. Cristina y Alberto tienen hora y media para encontrar el núcleo de fusión: una ventana de comunicaciones con tres satélites, un invernadero que sigue las reglas de la vida, una placa de cables, un campo de rocas, el brazo de una antena, una cuenta de cifras, el circuito del reactor, un rover con bucles, paneles de refrigeración, una sopa de letras y una consola final.",
        minigames={"14": "14-satelites.js", "20": "20-invernadero.js", "40": "40-cableado.js", "48": "48-rocas.js", "52": "52-brazo.js", "46": "46-cuenta.js",
                   "51": "51-anillo.js", "69": "69-programa.js", "64": "64-paneles.js", "72": "72-sopa.js", "85": "85-consola.js"},
        pal=("#8a3a1a", "#1c0c10")),
    "Florencia": dict(
        datos=F, dificultad=4, tema="florencia", titulo="Florencia, 1503: El Taller de Leonardo", emoji="🪞",
        grad="#5a3a1a,#140c06", acento="#d9a441", acento2="#f0c773", bg1="#120c07", bg2="#2a1c0e",
        sinopsis="Tercer salto del Cronoportal: Florencia, año 1503. Cristina y Alberto aterrizan de noche en el taller de Leonardo da Vinci, sin energía y con una hora hasta el amanecer. Solo la luz del alba, concentrada por la lente del maestro, puede recargar el aparato.",
        minigames={"24": "24-cofre.js", "32": "32-disco.js", "38": "38-engranajes.js", "54": "54-cuadrado.js", "58": "58-cisterna.js", "66": "66-ornitoptero.js", "92": "92-espejos.js", "46": "46-baul.js"},
        pal=("#6a4a22", "#1a1008")),
    "Dinosaurios": dict(
        datos=D, dificultad=4, tema="dinosaurios", titulo="Cretácico, hace 66 millones de años: El Valle de los Gigantes", emoji="🦖", minutos=90,
        grad="#2f5a22,#07120a", acento="#b5e35b", acento2="#d9f59a", bg1="#07120a", bg2="#12281a",
        sinopsis="Cuarto salto del Cronoportal: el Cretácico, hace sesenta y seis millones de años. Cristina y Alberto aterrizan en un valle de dinosaurios, el núcleo de energía del aparato sale rodando hacia un vado de barro y en el cielo brilla un asteroide. Entre huellas, nidos, un cráter, la lava, una manada, un corral, un pterosaurio y una ciénaga, tienen hora y media para recuperarlo y para encontrar a la doctora Ibarra, que lleva diecisiete años atrapada aquí.",
        minigames={"14": "14-huellas.js", "20": "20-manada.js", "40": "40-nidos.js", "48": "48-crater.js", "52": "52-lava.js", "46": "46-senderos.js",
                   "51": "51-arbol.js", "69": "69-corral.js", "72": "72-planear.js", "64": "64-barro.js", "85": "85-anillos.js"},
        pal=("#2f5a22", "#0a160c")),
    "Cuento": dict(
        datos=C, dificultad=3, tema="cuento", titulo="Érase una vez: El Libro de los Finales Felices", emoji="📖", minutos=90,
        grad="#4a2a8a,#120a2a", acento="#f6c453", acento2="#ffe08a", bg1="#0e0820", bg2="#241450",
        sinopsis="Quinto salto del Cronoportal, y esta vez no cae en una época sino dentro de un libro de cuentos: Cristina y Alberto se convierten en personajes de dibujos animados. El libro se queda sin color y el último cuento no tiene final. Para escribirlo hay que convencer a una panadera, cruzar el puente del troll, cambiar el pasado, saltar con botas de siete leguas, trepar por una habichuela, encender una vidriera, desenmascarar a dos hadas mentirosas, guiar un rayo de luna, devolver los colores al castillo y abrir una caja de música. Hora y media antes de que el libro se cierre con ellos dentro.",
        minigames={"14": "14-cartel.js", "20": "20-puente.js", "40": "40-salto.js", "48": "48-botas.js", "52": "52-habichuela.js", "46": "46-vidriera.js",
                   "51": "51-hadas.js", "64": "64-rayos.js", "69": "69-tarros.js", "72": "72-caja.js", "85": "85-pagina.js"},
        pal=("#5a3aa8", "#1a0e3a")),
    "Trono": dict(
        datos=T, dificultad=4, tema="trono", titulo="Reino de Hielo y Fuego: La Corona del Dragón", emoji="🐉", minutos=100,
        grad="#2c3a4a,#0a0f16", acento="#8fc7ee", acento2="#cfe8fb", bg1="#06090e", bg2="#121a24",
        sinopsis="Sexto salto del Cronoportal: un reino de hielo y fuego, en pleno invierno. Cristina y Alberto aterrizan en el patio de armas de la fortaleza de Piedra Negra, en mitad de una ventisca, con el aparato sin energía. Solo una esquirla de dragón puede encenderlo, y la tormenta cierra los pasos de montaña: tienen cien minutos antes de quedar atrapados hasta la primavera.",
        minigames={"14": "14-cuervo.js", "20": "20-banquete.js", "40": "40-caminos.js", "42": "42-cronica.js", "46": "46-lengua.js",
                   "51": "51-consejeros.js", "64": "64-antorchas.js", "69": "69-puerta.js", "72": "72-tapiz.js", "84": "84-profecia.js"},
        pal=("#3a4c60", "#0c121a")),
    "Pompeya": dict(
        datos=P, dificultad=3, tema="pompeya", titulo="Pompeya, 79 d.C.: El Mosaico del Mundo", emoji="🌋", minutos=90,
        grad="#6a3418,#150a06", acento="#e08a4a", acento2="#f5c08a", bg1="#120805", bg2="#2e150b",
        sinopsis="Séptimo salto del Cronoportal: Pompeya, 24 de agosto del año 79. Cristina y Alberto aterrizan en el atrio de una rica villa mientras el Vesubio humea en el horizonte, y el cristal de energía del aparato sale rodando. Para recuperarlo hay que seguir a su dueña por la villa, el jardín, la ciudad y el puerto: un mosaico laberinto, cuentas en números romanos, un sello, una fuente, un cuadrado mágico, una balanza romana, grafitos, el calendario romano, la huida y la barca. Hora y media antes de que caiga la ceniza.",
        minigames={"13": "13-panel.js", "20": "20-abaco.js", "28": "28-anillos.js", "33": "33-compuertas.js", "40": "40-tablilla.js", "46": "46-statera.js", "55": "55-calles.js", "59": "59-calendario.js", "66": "66-huida.js", "70": "70-barca.js"},
        pal=("#7a3a1a", "#1c0c08")),
    "Arcade": dict(
        datos=A, dificultad=4, tema="arcade", titulo="Game Over, 1985: La Última Moneda", emoji="🕹️", minutos=90,
        grad="#4a1a7a,#07040f", acento="#ff5ad8", acento2="#8ffcff", bg1="#07050f", bg2="#1a0a2e",
        sinopsis="Octavo salto del Cronoportal: un salón recreativo de 1985, a medianoche. El aparato golpea una máquina y su cristal de energía cae por la ranura de las fichas: Cristina y Alberto quedan atrapados dentro, convertidos en píxeles, con una cuenta atrás de hora y media hasta GAME OVER. Para salir tendrán que resolver un circuito de puertas lógicas, desatascar un aparcamiento de naves, dibujar un sprite comprimido, leer un mensaje en hexadecimal, colocar a cuatro fantasmas, completar un marcador mágico, ordenar una tabla de récords, resolver un puzle deslizante, cruzar una autopista con una rana, pagar con las menos monedas y arrancar la máquina con la clave de cuatro bytes.",
        minigames={"14": "14-circuito.js", "20": "20-atasco.js", "40": "40-sprite.js", "48": "48-ascii.js", "52": "52-fantasmas.js", "46": "46-cuadrado.js",
                   "51": "51-ranking.js", "64": "64-deslizante.js", "69": "69-rana.js", "72": "72-monedas.js", "85": "85-xor.js"},
        pal=("#5a2a9a", "#0e0620")),
    "Oeste": dict(
        datos=W, dificultad=3, tema="oeste", titulo="Dry Gulch, 1878: El Tren del Oro", emoji="🤠", minutos=90,
        grad="#7a4a1e,#160d06", acento="#e0a040", acento2="#f5d48a", bg1="#140c05", bg2="#33200e",
        sinopsis="Novena parada del Cronoportal: Dry Gulch, un pueblo del Lejano Oeste en 1878. El aparato golpea un barril en el apartadero de la estación y un jinete enmascarado, que cree haber encontrado una joya, se lleva el cristal de energía. Para recuperarlo hay que enganchar un tren, reconocer a un bandido en un cartel de «Se busca», seguir un mapa, volar un túnel con dos mechas y encontrar una barra de oro falsa, antes de que salga el tren del oro, dentro de hora y media.",
        minigames={"20": "20-candado.js", "24": "24-celda.js", "46": "46-caja.js", "48": "48-mechas.js", "69": "69-bascula.js"},
        pal=("#8a5a2a", "#1c1008")),
    "Espia": dict(
        datos=S, dificultad=3, tema="espia", titulo="Montecarlo, 1965: Operación Cristal", emoji="🕵️", minutos=75,
        grad="#0e5a6a,#07121a", acento="#ff6fa8", acento2="#7fe8f0", bg1="#06131a", bg2="#0e2a36",
        sinopsis="Décima parada del Cronoportal: Montecarlo, 1965, noche de gala. El aparato golpea una mesa del casino y el Dr. Noche, un villano con capa que colecciona gemas, se lleva el cristal de energía a su yate. Con la Agente Zorro, Cristina y Alberto tienen setenta y cinco minutos, hasta que el yate zarpe a medianoche, para superponer hojas transparentes, usar una rejilla de cifrado, cruzar un yate a ciegas, descifrar un skyline y desactivar cuatro cargas con un manual.",
        minigames={"20": "20-caja.js", "24": "24-teletipo.js", "46": "46-pasillos.js", "48": "48-skyline.js", "69": "69-desactivador.js", "36": "36-poker.js"},
        pal=("#1c7a8a", "#07202a")),
    "Futbol": dict(
        datos=Fu, dificultad=2, tema="futbol", titulo="La Final del Siglo, 1970: La Copa de Cristal", emoji="⚽", minutos=90,
        grad="#1f6a30,#06140a", acento="#f2c230", acento2="#a8ec96", bg1="#07140b", bg2="#12301a",
        sinopsis="Undécima parada del Cronoportal: el estadio del Club Estrella, en 1970, una hora y media antes de la final del siglo. El cristal de energía rueda hasta caer dentro de la Copa de cristal y solo saldrá del palco con el campeón. El entrenador os toma por su cuerpo técnico: para ayudarle a ganar hay que dar la vuelta a unos cromos, deducir una alineación, decidir jugadas del VAR, reconstruir los marcadores de una liguilla y marcar una tanda de penaltis.",
        minigames={"20": "20-cromos.js", "24": "24-pizarra.js", "46": "46-var.js", "48": "48-liguilla.js", "69": "69-penaltis.js"},
        pal=("#2f7a3a", "#0b2412")),
    "Piratas": dict(
        datos=Pi, dificultad=3, tema="piratas", titulo="Mar de las Brumas, 1715: El Tesoro de la Isla Calavera", emoji="🏴‍☠️", minutos=90,
        grad="#1c5a6a,#06141a", acento="#e8b84a", acento2="#9fe0e0", bg1="#06141a", bg2="#103440",
        sinopsis="Duodécima parada del Cronoportal: la cubierta de La Gaviota, un bergantín pirata del Caribe, en 1715. Un loro se lleva el cristal de energía al cofre de la capitana Bruma, que solo lo devolverá si encontráis el tesoro del capitán Calavera antes de que la marea cubra su cueva. Hay cartas que se pliegan como los mapas antiguos: fijad el rumbo, estibad la pólvora, burlad a una fragata que persigue siempre igual, encontrad una constelación girada en la tapa de un cofre, cruzad un suelo de losas trampa y cavad donde marca el mapa.",
        minigames={"24": "24-timon.js", "46": "46-bodega.js", "48": "48-persecucion.js", "66": "66-cofre.js", "79": "79-suelo.js", "69": "69-gruta.js", "61": "61-reloj.js"},
        pal=("#1f6a7a", "#08202a")),
    "Juguetes": dict(
        datos=Ju, dificultad=1, tema="juguetes", titulo="El Cuarto de Leo, 1995: La Noche de los Juguetes", emoji="🧸", minutos=60,
        grad="#3a6ad0,#121e48", acento="#ffcc33", acento2="#ff9ec0", bg1="#0e1838", bg2="#233f7a",
        sinopsis="Decimotercera parada del Cronoportal, y la más fácil: el aparato falla y os convierte en juguetes, una muñeca de trapo y un robot de hojalata, en el cuarto de Leo, un niño de 1995, la noche antes de la mudanza. Leo ha guardado el cristal creyendo que era una canica. Con el Capitán Pelusa y los demás juguetes, buscad las diferencias de una foto, construid una torre, desenredad una marioneta, hojead un cuaderno, cargad un tren y lanzad las canicas antes de que llegue el camión.",
        minigames={"24": "24-estanteria.js", "46": "46-torre.js", "48": "48-marioneta.js", "66": "66-tren.js", "69": "69-canicas.js", "64": "64-cubos.js"},
        pal=("#3a6ad0", "#121e48")),
}


def generar_index(index_faro, cfg):
    """index.html de un juego de Aventuras C&A a partir del del Faro (la plantilla de la app)."""
    ix = index_faro
    ix = sustituir(ix, '<html lang="es" data-tema="faro">', f'<html lang="es" data-tema="{cfg["tema"]}">')
    ix = sustituir(ix, "<title>Unlock C&amp;A - El Faro de Cabo Niebla</title>", f"<title>Aventuras C&amp;A - {cfg['titulo']}</title>")
    ix = sustituir(ix, FARO_SINOPSIS, cfg["sinopsis"])
    ix = sustituir(ix, '<div class="serie">Unlock C&amp;A</div>', '<div class="serie">Aventuras C&amp;A</div>')
    ix = sustituir(ix, "El Faro de Cabo Niebla", cfg["titulo"], veces=None)
    ix = sustituir(ix, "juego: 'faro',", f"juego: '{cfg['tema']}',")
    ix = sustituir(ix, "assets: '../../assets/',", "assets: '../../../assets/',")
    for viejo in ('src="../../assets/js/ajustes.js"', 'href="../../manifest.webmanifest"', 'href="../../assets/icons/apple-touch-icon.png"', 'href="../../assets/icons/favicon.png"'):
        ix = sustituir(ix, viejo, viejo.replace('"../../', '"../../../'))
    ix = sustituir(ix, "segundos: 4500,", f"segundos: {cfg.get('minutos', 60) * 60},")
    ix = sustituir(ix, "dificultad: 2,", f"dificultad: {cfg.get('dificultad', 3)},")
    ix = sustituir(ix, "← Volver al menú", "← Volver a Aventuras C&amp;A", veces=None)
    ix = sustituir(ix, "volver: '../../index.html',", "volver: '../index.html',")
    mapa = ",\n".join(f"      '{k}': './minijuegos/{v}'" for k, v in cfg["minigames"].items())
    viejo = re.search(r"      minijuegos: \{.*?\n      \}\n", ix, re.S).group(0)
    return ix.replace(viejo, "      minijuegos: {\n" + mapa + "\n      }\n")

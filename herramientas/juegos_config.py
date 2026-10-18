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

FARO = "juegos/el-faro"
FARO_SINOPSIS = "Tormenta, la gran lámpara apagada y un carguero a ciegas rumbo a las rocas. Inés y Marcos tienen una hora para encender el faro... y encontrar al abuelo Anselmo."


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
        datos=E, dificultad=3, tema="egipto", titulo="Egipto, 1274 a.C.: El Ojo de Horus", emoji="🏺",
        grad="#4a3512,#150f05", acento="#e0b04a", acento2="#f2d27a", bg1="#120d05", bg2="#2a1d0a",
        sinopsis="Cristina y Alberto estrenan su Cronoportal y aterrizan en una cámara secreta bajo un templo de Tebas, en el año 1274 a.C. Con el aparato sin energía y solo una hora antes de que lleguen los sacerdotes, tienen que encontrar el Ojo de Horus.",
        minigames={"15": "15-papiro.js", "23": "23-muro.js", "47": "47-balanza.js", "71": "71-anillos.js", "95": "95-cristales.js", "37": "37-tablilla.js", "34": "34-sarcofago.js"},
        pal=("#7a5a1e", "#2a1d0a")),
    "Marte": dict(
        datos=M, dificultad=3, tema="marte", titulo="Marte, 2157: Cúpula Aurora", emoji="🚀",
        grad="#5a2a14,#12060a", acento="#ff8a50", acento2="#ffb085", bg1="#12070a", bg2="#2a120c",
        sinopsis="Segundo salto del Cronoportal: Marte, año 2157. La cúpula Aurora está a oscuras por una tormenta de polvo y el soporte vital se apaga. Cristina y Alberto tienen una hora para encontrar el núcleo de fusión y volver a casa.",
        minigames={"21": "21-terminal.js", "52": "52-tuberias.js", "66": "66-esclusa.js", "88": "88-calibrador.js", "35": "35-diario.js", "48": "48-rover.js", "62": "62-energia.js"},
        pal=("#8a3a1a", "#1c0c10")),
    "Florencia": dict(
        datos=F, dificultad=4, tema="florencia", titulo="Florencia, 1503: El Taller de Leonardo", emoji="🪞",
        grad="#5a3a1a,#140c06", acento="#d9a441", acento2="#f0c773", bg1="#120c07", bg2="#2a1c0e",
        sinopsis="Tercer salto del Cronoportal: Florencia, año 1503. Cristina y Alberto aterrizan de noche en el taller de Leonardo da Vinci, sin energía y con una hora hasta el amanecer. Solo la luz del alba, concentrada por la lente del maestro, puede recargar el aparato.",
        minigames={"24": "24-cofre.js", "32": "32-disco.js", "38": "38-engranajes.js", "54": "54-cuadrado.js", "58": "58-cisterna.js", "66": "66-ornitoptero.js", "92": "92-espejos.js"},
        pal=("#6a4a22", "#1a1008")),
    "Dinosaurios": dict(
        datos=D, dificultad=3, tema="dinosaurios", titulo="Cretácico, hace 66 millones de años: El Valle de los Gigantes", emoji="🦖", minutos=90,
        grad="#2f5a22,#07120a", acento="#b5e35b", acento2="#d9f59a", bg1="#07120a", bg2="#12281a",
        sinopsis="Cuarto salto del Cronoportal: el Cretácico, hace sesenta y seis millones de años. Cristina y Alberto aterrizan en un valle de dinosaurios, pero el núcleo de energía del aparato sale rodando y en el cielo brilla un asteroide. Tienen hora y media para recuperarlo antes de que el cielo se incendie.",
        minigames={"14": "14-huellas.js", "20": "20-excavacion.js", "42": "42-diario.js", "40": "40-balsa.js", "46": "46-adn.js",
                   "51": "51-estratos.js", "64": "64-cristales.js", "69": "69-nidos.js", "72": "72-geiser.js", "84": "84-esqueleto.js"},
        pal=("#2f5a22", "#0a160c")),
    "Cuento": dict(
        datos=C, dificultad=2, tema="cuento", titulo="Érase una vez: El Libro de los Finales Felices", emoji="📖", minutos=75,
        grad="#4a2a8a,#120a2a", acento="#f6c453", acento2="#ffe08a", bg1="#0e0820", bg2="#241450",
        sinopsis="Quinto salto del Cronoportal, y esta vez no cae en una época sino dentro de un libro de cuentos: Cristina y Alberto se convierten en personajes de dibujos animados. El libro se está quedando sin color y sin tinta, y el último cuento no tiene final. Tienen setenta y cinco minutos para escribirlo antes de que el libro se cierre con ellos dentro.",
        minigames={"14": "14-cartel.js", "20": "20-puente.js", "40": "40-salto.js", "42": "42-cuento.js", "46": "46-vidriera.js",
                   "51": "51-hadas.js", "64": "64-rayos.js", "69": "69-tarros.js", "72": "72-caja.js", "84": "84-pagina.js"},
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
        sinopsis="Séptimo salto del Cronoportal: Pompeya, 24 de agosto del año 79. Cristina y Alberto aterrizan en el atrio de una rica villa mientras el Vesubio humea en el horizonte, y el cristal de energía del aparato sale rodando. Para encontrarlo hay que reconstruir los mosaicos y frescos de la casa juntando varias cartas. Tienen hora y media antes de que caiga la ceniza.",
        minigames={"20": "20-formas.js", "24": "24-flechas.js", "46": "46-rosetas.js", "48": "48-abaco.js", "69": "69-reloj.js"},
        pal=("#7a3a1a", "#1c0c08")),
    "Arcade": dict(
        datos=A, dificultad=3, tema="arcade", titulo="Game Over, 1985: La Última Moneda", emoji="🕹️", minutos=75,
        grad="#4a1a7a,#07040f", acento="#ff5ad8", acento2="#8ffcff", bg1="#07050f", bg2="#1a0a2e",
        sinopsis="Octavo salto del Cronoportal: un salón recreativo de 1985, a medianoche. El aparato golpea la máquina COSMIC QUEST y su cristal de energía cae por la ranura de las fichas: Cristina y Alberto quedan atrapados dentro, convertidos en píxeles. Para salir tienen que superar seis niveles (circuitos, radar, mandos, autopista y un jefe de bloques) antes de que el contador llegue a GAME OVER, en setenta y cinco minutos.",
        minigames={"20": "20-terminal.js", "24": "24-radar.js", "46": "46-mando.js", "48": "48-autopista.js", "69": "69-pozo.js"},
        pal=("#5a2a9a", "#0e0620")),
    "Oeste": dict(
        datos=W, dificultad=3, tema="oeste", titulo="Dry Gulch, 1878: El Tren del Oro", emoji="🤠", minutos=90,
        grad="#7a4a1e,#160d06", acento="#e0a040", acento2="#f5d48a", bg1="#140c05", bg2="#33200e",
        sinopsis="Novena parada del Cronoportal: Dry Gulch, un pueblo del Lejano Oeste en 1878. El aparato golpea un barril en el apartadero de la estación y un jinete enmascarado, que cree haber encontrado una joya, se lleva el cristal de energía. Para recuperarlo hay que enganchar un tren, reconocer a un bandido en un cartel de «Se busca», seguir un mapa, volar un túnel con dos mechas y encontrar una barra de oro falsa, antes de que salga el tren del oro, dentro de hora y media.",
        minigames={"20": "20-candado.js", "24": "24-celda.js", "46": "46-caja.js", "48": "48-mechas.js", "69": "69-bascula.js"},
        pal=("#8a5a2a", "#1c1008")),
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
    ix = sustituir(ix, "segundos: 3600,", f"segundos: {cfg.get('minutos', 60) * 60},")
    ix = sustituir(ix, "dificultad: 2,", f"dificultad: {cfg.get('dificultad', 3)},")
    ix = sustituir(ix, "← Volver al menú", "← Volver a Aventuras C&amp;A", veces=None)
    ix = sustituir(ix, "volver: '../../index.html',", "volver: '../index.html',")
    mapa = ",\n".join(f"      '{k}': './minijuegos/{v}'" for k, v in cfg["minigames"].items())
    viejo = re.search(r"      minijuegos: \{.*?\n      \}\n", ix, re.S).group(0)
    return ix.replace(viejo, "      minijuegos: {\n" + mapa + "\n      }\n")

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
}


def generar_index(index_faro, cfg):
    """index.html de un juego de Aventuras C&A a partir del del Faro (la plantilla de la app)."""
    ix = index_faro
    ix = sustituir(ix, '<html lang="es" data-tema="faro">', f'<html lang="es" data-tema="{cfg["tema"]}">')
    ix = sustituir(ix, "<title>Unlock C&amp;A - El Faro de Cabo Niebla</title>", f"<title>Aventuras C&amp;A - {cfg['titulo']}</title>")
    ix = sustituir(ix, FARO_SINOPSIS, cfg["sinopsis"])
    ix = sustituir(ix, '<div class="serie">Unlock C&amp;A</div>', '<div class="serie">Aventuras C&amp;A</div>')
    ix = sustituir(ix, "El Faro de Cabo Niebla", cfg["titulo"], veces=None)
    ix = sustituir(ix, "segundos: 3600,", f"segundos: {cfg.get('minutos', 60) * 60},")
    ix = sustituir(ix, "dificultad: 2,", f"dificultad: {cfg.get('dificultad', 3)},")
    ix = sustituir(ix, "← Volver al menú", "← Volver a Aventuras C&amp;A", veces=None)
    ix = sustituir(ix, "volver: '../../index.html',", "volver: '../index.html',")
    mapa = ",\n".join(f"      '{k}': './minijuegos/{v}'" for k, v in cfg["minigames"].items())
    viejo = re.search(r"      minijuegos: \{.*?\n      \}\n", ix, re.S).group(0)
    return ix.replace(viejo, "      minijuegos: {\n" + mapa + "\n      }\n")

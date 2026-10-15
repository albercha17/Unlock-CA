"""Genera el kit para crear los vídeos de introducción con un generador de vídeo con IA (gratuito o no):
  - juegos/laboratorio/videos.html  (página con un botón «Copiar» por cada texto; cómoda desde el móvil)
  - KIT-VIDEOS.md                   (el mismo contenido en texto, para copiar a mano)

Cada juego tiene 4 clips de 5 s (las 4 escenas del guion `_meta.video` de su cartas.json). El Faro no tiene guion en su cartas.json y se define aquí.
Uso (desde la raíz del repo):  python herramientas/generar_kit_videos.py
"""
import html
import json
import re

WEB = "https://albercha17.github.io/Unlock-CA/"
JUEGOS = [
    ("faro", "El Faro de Cabo Niebla", "juegos/el-faro/"),
    ("egipto", "Egipto, 1274 a.C.: El Ojo de Horus", "juegos/aventuras-ca/egipto/"),
    ("marte", "Marte, 2157: Cúpula Aurora", "juegos/aventuras-ca/marte/"),
    ("florencia", "Florencia, 1503: El Taller de Leonardo", "juegos/aventuras-ca/florencia/"),
    ("dinosaurios", "Cretácico: El Valle de los Gigantes", "juegos/aventuras-ca/dinosaurios/"),
    ("cuento", "Érase una vez: El Libro de los Finales Felices", "juegos/aventuras-ca/cuento/"),
    ("trono", "Reino de Hielo y Fuego: La Corona del Dragón", "juegos/aventuras-ca/trono/"),
]

FARO = dict(
    estilo="con estética cinematográfica semirrealista de película de aventuras, noche de tormenta, azules profundos y destellos dorados de linterna",
    escenas=[
        "Noche de tormenta sobre un acantilado: el faro de Cabo Niebla, una torre blanca con una banda roja, tiene la gran lámpara de la cima apagada; las olas rompen contra las rocas y, muy lejos, se ven las luces de un carguero.",
        "Inés (mujer de 30 años, pelo negro corto y liso, ojos verdes, chubasquero amarillo y botas de agua) y Marcos (hombre de 32 años, pelirrojo, gafas redondas, pecas, chaqueta impermeable gris y una mochila de la que asoma una antena de radio) suben corriendo hacia la puerta del faro con una linterna bajo la lluvia.",
        "Dentro del faro, Marcos sostiene una radio que crepita con la voz de la guardia costera mientras Inés mira con preocupación la escalera de caracol que sube a la lámpara apagada.",
        "Primer plano de Inés y Marcos mirando hacia arriba, con el haz de la linterna sobre la lámpara apagada; un relámpago ilumina el mar y el carguero, cada vez más cerca; fundido a negro.",
    ],
    sonido="trueno, lluvia fuerte, olas contra las rocas, crepitar de radio, música de tensión con cuerdas graves, sin voz de narrador",
)


def partir(video):
    """Divide el guion de 15 s de _meta.video en estilo, 4 escenas y sonido."""
    cab = video.split("Escena 1")[0]
    m = re.search(r"segundos, (.*?)\. ", cab + " ")
    estilo = m.group(1) if m else cab
    escenas = [e.strip() for e in re.findall(r"Escena \d \(\d+-\d+ s\): (.*?)(?= Escena \d \(|\s*Sonido:|$)", video, re.S)]
    s = re.search(r"Sonido: (.*)$", video, re.S)
    return dict(estilo=estilo.strip(), escenas=escenas, sonido=(s.group(1).strip().rstrip(".") if s else ""))


def carta_portal(cartas):
    for k, c in cartas.items():
        if not k.startswith("_") and "Cronoportal" in c["titulo"]:
            return k
    return "P"


def clips(clave, carpeta):
    datos = json.load(open(carpeta + "cartas.json", encoding="utf-8"))
    g = FARO if clave == "faro" else partir(datos["_meta"]["video"])
    assert len(g["escenas"]) == 4, clave
    portal = "7" if clave == "faro" else carta_portal(datos)
    imagenes = [("P" if clave == "faro" else portal), ("P" if clave == "faro" else portal), "P", "P"]
    estilos = "Mantén exactamente el mismo estilo visual, la misma paleta y los mismos personajes que en los demás clips de esta serie."
    salida = []
    for i, esc in enumerate(g["escenas"]):
        t = (f"Vídeo vertical 9:16 de 5 segundos, {g['estilo']}. {esc} {estilos} "
             f"Sin ningún texto, letra, número ni subtítulo en pantalla. Sonido: {g['sonido']}.")
        salida.append(dict(n=i + 1, prompt=t, imagen=imagenes[i], url=f"{WEB}{carpeta}img/{imagenes[i]}.jpg"))
    return salida


INTRO_PAGINAS = [
    ("Kling", "https://klingai.com", "Créditos diarios gratis (unos 66). Muy bueno con personas. Marca de agua y 720p en la versión gratis."),
    ("Google Veo (Gemini / Flow)", "https://gemini.google.com", "Créditos diarios gratis según la cuenta. Opción «Crear vídeo»; Flow en https://labs.google/fx/tools/flow."),
    ("Hailuo (MiniMax)", "https://hailuoai.video", "Créditos de prueba. Buena calidad de movimiento."),
    ("Dreamina / Seedance (CapCut)", "https://dreamina.capcut.com", "Créditos diarios gratis; sirve también para unir los clips (CapCut)."),
    ("Unir los clips (gratis)", "https://www.capcut.com", "CapCut (móvil o web) o Clipchamp (Windows) para pegar los 4 clips de 5 s en un solo vídeo de 20 s."),
]
PASOS = [
    "Entra en uno de los servicios (arriba) y elige «Imagen a vídeo» (si no lo hay, «Texto a vídeo»). Formato vertical 9:16, 5 segundos.",
    "Para cada clip: sube la ilustración que indica la ficha (descárgala con el enlace) y pega el texto con el botón Copiar. Genera el clip y descárgalo.",
    "Repite los 4 clips del juego. Si un clip sale mal, vuelve a generarlo (a veces hace falta 2 o 3 intentos).",
    "Une los 4 clips en orden con CapCut o Clipchamp (transición suave de medio segundo) y exporta MP4, vertical, 720p o más y menos de 25 MB.",
    "Ponle el nombre videoInicial.mp4 y súbelo a la carpeta video/ de su juego (por ejemplo juegos/aventuras-ca/cuento/video/videoInicial.mp4). La app lo reproduce al pulsar Empezar (con botón «Saltar vídeo»).",
]
CONSEJOS = [
    "Sube la ilustración como primer fotograma: es la forma de que Cristina y Alberto se parezcan a las cartas.",
    "Si el servicio añade música sola, déjala; la música de fondo del juego empieza después del vídeo.",
    "Si te piden elegir «movimiento de cámara», usa «zoom suave» o «avance lento».",
    "Si salen letras o números raros en pantalla, añade al final del texto: «Elimina cualquier texto o logotipo de la imagen».",
    "Las versiones gratis suelen poner marca de agua: para uso privado en casa vale; para publicarlo, revisa la licencia del servicio.",
]


def md(todos):
    L = ["# Kit para crear los vídeos de introducción con IA\n", "## Páginas\n"]
    L += [f"- **{n}** — {u} — {d}" for n, u, d in INTRO_PAGINAS]
    L += ["\n## Cómo se hace\n"] + [f"{i + 1}. {p}" for i, p in enumerate(PASOS)]
    L += ["\n## Consejos\n"] + [f"- {c}" for c in CONSEJOS]
    for clave, titulo, carpeta, cl in todos:
        L.append(f"\n---\n\n## {titulo}\n\nCarpeta de destino del vídeo: `{carpeta}video/videoInicial.mp4`\n")
        for c in cl:
            L.append(f"### Clip {c['n']} de 4 — ilustración a subir: {c['url']}\n\n```\n{c['prompt']}\n```\n")
    return "\n".join(L)


def pagina(todos):
    e = html.escape
    h = ['<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
         "<title>Kit de vídeos — Unlock C&amp;A</title><link rel=\"stylesheet\" href=\"lab.css\">",
         "<style>details{background:var(--panel);border:1px solid var(--linea);border-radius:14px;margin:10px 0;padding:4px 12px}summary{cursor:pointer;padding:12px 0;font-weight:800;color:var(--acento);min-height:44px}",
         ".clip{border-top:1px solid var(--linea);padding:10px 0}.clip h3{margin:0 0 6px;font-size:.92rem}.clip a{color:var(--acento);font-size:.82rem}",
         "textarea{width:100%;min-height:150px;margin:8px 0;background:#0b121a;color:var(--texto);border:1px solid var(--linea);border-radius:10px;padding:10px;font:.82rem/1.45 system-ui,sans-serif}",
         "ul,ol{padding-left:20px;line-height:1.6;font-size:.9rem}li a{color:var(--acento)}</style></head><body><div class=\"lab\">",
         '<a class="volver" href="index.html">← Laboratorio</a><h1>Kit de vídeos de introducción</h1>',
         '<p class="sub">Textos listos para pegar en un generador de vídeo con IA: 4 clips de 5 segundos por juego.</p>',
         '<div class="regla"><b>Páginas</b><ul>']
    h += [f'<li><a href="{u}" target="_blank" rel="noopener">{e(n)}</a> — {e(d)}</li>' for n, u, d in INTRO_PAGINAS]
    h += ["</ul><b>Cómo se hace</b><ol>"] + [f"<li>{e(p)}</li>" for p in PASOS] + ["</ol><b>Consejos</b><ul>"] + [f"<li>{e(c)}</li>" for c in CONSEJOS] + ["</ul></div>"]
    for clave, titulo, carpeta, cl in todos:
        h.append(f"<details><summary>{e(titulo)}</summary><p class=\"pista\">Destino del vídeo: <code>{e(carpeta)}video/videoInicial.mp4</code></p>")
        for c in cl:
            h.append(f'<div class="clip"><h3>Clip {c["n"]} de 4</h3><a href="{e(c["url"])}" target="_blank" rel="noopener" download>Ilustración a subir como primer fotograma ({e(c["imagen"])}.jpg)</a>'
                     f'<textarea readonly id="t-{clave}-{c["n"]}">{e(c["prompt"])}</textarea><button class="btn primario" data-t="t-{clave}-{c["n"]}">Copiar texto</button></div>')
        h.append("</details>")
    h.append("</div><script>document.addEventListener('click',function(ev){var b=ev.target.closest('button[data-t]');if(!b)return;var t=document.getElementById(b.dataset.t);t.select();"
             "var ok=false;try{ok=navigator.clipboard?(navigator.clipboard.writeText(t.value),true):document.execCommand('copy');}catch(e){try{ok=document.execCommand('copy');}catch(x){}}"
             "var o=b.textContent;b.textContent=ok?'¡Copiado!':'Selecciona y copia';setTimeout(function(){b.textContent=o;},1600);});</script></body></html>")
    return "\n".join(h)


def main():
    todos = [(c, t, p, clips(c, p)) for c, t, p in JUEGOS]
    open("KIT-VIDEOS.md", "w", encoding="utf-8", newline="\n").write(md(todos))
    open("juegos/laboratorio/videos.html", "w", encoding="utf-8", newline="\n").write(pagina(todos))
    print(len(todos), "juegos,", sum(len(x[3]) for x in todos), "textos -> KIT-VIDEOS.md y juegos/laboratorio/videos.html")


if __name__ == "__main__":
    main()

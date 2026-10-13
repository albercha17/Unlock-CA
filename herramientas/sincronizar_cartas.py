"""Genera cartas-data.js junto a cada cartas.json, para que pc.html, imprimir.html y prompts.html funcionen
tambien con doble clic (file://), donde el navegador bloquea fetch('cartas.json').

Uso (desde la raiz del repo):
    python herramientas/sincronizar_cartas.py            # escribe/actualiza todos
    python herramientas/sincronizar_cartas.py --comprobar   # solo avisa si alguno esta desfasado (sale con 1)

cartas.json es la fuente; cartas-data.js se genera y NO se edita a mano. Con servidor (GitHub Pages) las paginas
siguen leyendo cartas.json; cartas-data.js solo es el plan B.
"""
import glob
import json
import os
import sys

CABECERA = "// Generado por herramientas/sincronizar_cartas.py a partir de cartas.json. No editar a mano.\n"
AYUDA = """window.fetchCartas = function () {
  return fetch('cartas.json?v=' + Date.now(), {cache: 'no-store'})
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r; })
    .catch(function () {
      if (window.JUEGO_LOCAL) return {ok: true, json: function () { return Promise.resolve(window.JUEGO_LOCAL); }};
      throw new Error('sin cartas');
    });
};
"""


def contenido(json_path):
    datos = json.load(open(json_path, encoding="utf-8"))
    return CABECERA + "window.JUEGO_LOCAL = " + json.dumps(datos, ensure_ascii=False, indent=1) + ";\n" + AYUDA


def main():
    comprobar = "--comprobar" in sys.argv
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mal = []
    for cj in sorted(glob.glob(os.path.join(raiz, "juegos", "**", "cartas.json"), recursive=True)):
        carpeta = os.path.dirname(cj)
        if not any(os.path.exists(os.path.join(carpeta, p)) for p in ("pc.html", "imprimir.html", "prompts.html")):
            continue  # juegos sin esas paginas
        destino = os.path.join(carpeta, "cartas-data.js")
        nuevo = contenido(cj)
        actual = open(destino, encoding="utf-8", newline="").read().replace("\r\n", "\n") if os.path.exists(destino) else None
        rel = os.path.relpath(destino, raiz)
        if actual == nuevo:
            print("al dia   ", rel)
            continue
        if comprobar:
            mal.append(rel)
            print("DESFASADO", rel)
        else:
            open(destino, "w", encoding="utf-8", newline="\n").write(nuevo)
            print("escrito  ", rel)
    if mal:
        sys.exit("cartas-data.js desfasado: ejecuta python herramientas/sincronizar_cartas.py")


if __name__ == "__main__":
    main()

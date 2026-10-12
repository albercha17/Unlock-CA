"""Genera MANUAL.md (guia paso a paso y carta a carta) de un juego a partir de su cartas.json y su modulo de datos.

Uso (desde la raiz del repo):
    python herramientas/crear_manual_md.py Unlock-El-Faro datos_faro
    python herramientas/crear_manual_md.py Aventuras-CA/Egipto datos_egipto
Los pasos (PASOS) son los mismos que ejecuta ejecutar_manual.py en el navegador: si el manual dice algo, se ha comprobado.
"""
import importlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TIPO = {"gris": "Normal", "verde": "App", "roja": "Combina", "azul": "Combina"}


def orden(k):
    return (0, 0) if k == "P" else (1, int(k))


def tabla(s):
    return s.replace("|", "\\|")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    juego, modulo = sys.argv[1], sys.argv[2]
    datos = importlib.import_module(modulo)
    cartas = json.load(open(os.path.join(juego, "cartas.json"), encoding="utf-8"))
    titulo = cartas.pop("_meta")["juego"]
    primera = {}
    for i, p in enumerate(datos.PASOS, 1):
        for c in p["mesa"]:
            primera.setdefault(c, i)
    n_mazo = len(cartas) - 1

    L = [f"# Manual de partida — {titulo}", "",
         "> Este recorrido se ha ejecutado paso a paso en la web (Modo PC + app) con `herramientas/ejecutar_manual.py`: "
         "tras cada paso la mesa queda exactamente como se indica y la partida termina con solo la carta final en la mesa.", "",
         "## Preparación", "",
         f"- **PC:** abre el juego, pulsa *Modo PC* (o *Reiniciar* si ya habías jugado). Debe haber la carta **P** en la mesa y {n_mazo} cartas boca abajo en el mazo.",
         "- **Móvil:** abre el juego y pulsa *Empezar* (arranca la hora). *Acción* abre un minijuego con el número de su carta y *Pista* da ayuda de esa carta.",
         "- **Reglas:** «Coge» → a la mesa; «Descarta» → a los descartes (se pueden recuperar). Dos cartas con la etiqueta *Combina* se suman: el resultado es la carta que coges.", "",
         f"## Los {len(datos.PASOS)} pasos", ""]
    for i, p in enumerate(datos.PASOS, 1):
        L += [f"### Paso {i} — {p['t']}", "", p["que"], ""]
        for a in p["acciones"]:
            if a[0] == "app":
                L.append(f"- **En el móvil:** Acción → `{a[1]}`")
            if a[0] == "combinar":
                L.append(f"- **Suma:** `{a[1]} + {a[2]} = {int(a[1]) + int(a[2])}`")
        mesa = " ".join(f"`{c}`" for c in sorted(p["mesa"], key=orden))
        L += [f"- **La mesa queda con:** {mesa}", "- [ ] Hecho", ""]

    L += ["## Carta a carta", "", "| Carta | Nombre | Tipo | Impreso en la carta | Para qué sirve | Paso |", "|---|---|---|---|---|---|"]
    for k in sorted(cartas, key=orden):
        c = cartas[k]
        imp = []
        if c.get("coge"):
            imp.append("Coge " + ", ".join(map(str, c["coge"])))
        if c.get("descarta"):
            imp.append("Descarta " + ", ".join(map(str, c["descarta"])))
        if c.get("combina"):
            imp.append("Combinable: suma los números")
        if c.get("textoCarta"):
            imp.append("Texto: «" + " ".join(c["textoCarta"]) + "»")
        nombre = c["titulo"].split("—", 1)[1].strip()
        L.append(f"| {k} | {tabla(nombre)} | {TIPO[c['tipo']]} | {tabla('; '.join(imp) or '—')} | {tabla(datos.PARA_QUE[k])} | {primera.get(k, 1)} |")
    L += ["", "## Si algo no cuadra", "",
          "- **«No se pudo cargar el minijuego»:** la web aún no se ha actualizado. Espera un par de minutos y recarga con Ctrl+F5.",
          "- **El Modo PC no deja coger una carta:** ya la tienes en la mesa o está en los descartes.",
          "- **Una carta manda descartar algo que no tienes:** te has saltado un paso; vuelve al último paso hecho.", ""]
    ruta = os.path.join(juego, "MANUAL.md")
    open(ruta, "w", encoding="utf-8", newline="\n").write("\n".join(L))
    print("escrito", ruta, f"({len(datos.PASOS)} pasos, {len(cartas)} cartas)")


if __name__ == "__main__":
    main()

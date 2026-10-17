"""Comprueba los mosaicos de un juego (cartas que se juntan para formar un dibujo).

1. Las piezas de arte/ coinciden con el mosaico entero (mosaico-<nombre>.png) en el orden que dice cartas.json (_meta.mosaicos).
2. Ninguna pieza está en su sitio al empezar la Mesa de montaje, y la Mesa de montaje se puede resolver tocando piezas en el Modo PC.
3. Cada carta-mosaico se ve en pc.html con su número y sin franjas, y en imprimir.html con su número.

Uso (desde la raíz del repo, con un servidor local en marcha: python -m http.server 8890):
    python herramientas/probar_mosaicos.py http://127.0.0.1:8890 juegos/aventuras-ca/pompeya [carpeta_capturas]
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import By, nuevo_driver  # noqa: E402
from PIL import Image, ImageChops  # noqa: E402


def comprobar_arte(carpeta, meta):
    malos = []
    for k, m in meta.items():
        maestro = Image.open(f"{carpeta}/arte/mosaico-{k}.png").convert("RGB")
        w, h = maestro.size[0] // m["cols"], maestro.size[1] // m["filas"]
        for i, c in enumerate(m["cartas"]):
            f, col = divmod(i, m["cols"])
            trozo = maestro.crop((col * w, f * h, (col + 1) * w, (f + 1) * h))
            pieza = Image.open(f"{carpeta}/arte/{c}.png").convert("RGB")
            if pieza.size != trozo.size or ImageChops.difference(pieza, trozo).getbbox():
                malos.append(f"{k}: la carta {c} no es el trozo {i} del mosaico")
    return malos


def main(base, carpeta, capturas=None):
    datos = json.load(open(f"{carpeta}/cartas.json", encoding="utf-8"))
    meta = datos["_meta"]["mosaicos"]
    malos = comprobar_arte(carpeta, meta)
    for k, m in meta.items():
        for i, c in enumerate(m["cartas"]):
            mo = datos[c].get("mosaico")
            if mo != {"id": k, "filas": m["filas"], "cols": m["cols"], "fila": i // m["cols"], "col": i % m["cols"]}:
                malos.append(f"la carta {c} tiene un campo mosaico distinto: {mo}")
    print("piezas del arte:", "OK" if not malos else malos)

    d = nuevo_driver()
    try:
        d.get(f"{base}/{carpeta}/pc.html")
        time.sleep(1)
        d.execute_script("localStorage.clear()")
        d.get(f"{base}/{carpeta}/pc.html")
        time.sleep(1)
        for k, m in meta.items():
            assert not d.find_elements(By.CSS_SELECTOR, f".montar[data-mosaico='{k}']"), "el botón de montaje sale antes de tener las piezas"
            for c in m["cartas"]:
                d.find_element(By.ID, "qn").send_keys(c)
                d.find_element(By.ID, "qb").click()
                time.sleep(0.1)
            btn = d.find_elements(By.CSS_SELECTOR, f".montar[data-mosaico='{k}']")
            if not btn:
                malos.append(f"{k}: no aparece la Mesa de montaje con todas las piezas en mesa")
                continue
            # en mesa: sin franjas ni título, con número
            for c in m["cartas"]:
                it = [e for e in d.find_elements(By.CSS_SELECTOR, "#mesa .item") if e.find_element(By.CSS_SELECTOR, ".num").text == c][0]
                if it.find_elements(By.CSS_SELECTOR, ".acc, .tit, .texto, .etq"):
                    malos.append(f"{k}: la carta {c} en pc.html lleva franjas o título")
            if capturas and k in ("atrio", "digitos"):
                d.find_element(By.ID, "mesa").screenshot(f"{capturas}/mesa-{k}.png")
            btn[0].click()
            time.sleep(0.3)
            tiles = lambda: [t.get_attribute("data-id") for t in d.find_elements(By.CSS_SELECTOR, ".mt-tile")]  # noqa: E731
            inicial = tiles()
            if any(a == b for a, b in zip(inicial, m["cartas"])):
                malos.append(f"{k}: alguna pieza empieza en su sitio {inicial}")
            if capturas:
                d.save_screenshot(f"{capturas}/montaje-{k}-0.png")
            for i, c in enumerate(m["cartas"]):          # ordenación por selección tocando piezas
                actual = tiles()
                j = actual.index(c)
                if j != i:
                    d.find_elements(By.CSS_SELECTOR, ".mt-tile")[i].click()
                    d.find_elements(By.CSS_SELECTOR, ".mt-tile")[j].click()
                    time.sleep(0.1)
            if tiles() != m["cartas"] or not d.find_elements(By.CSS_SELECTOR, ".mt-grid.hecho"):
                malos.append(f"{k}: la Mesa de montaje no queda resuelta ({tiles()})")
            if capturas:
                d.save_screenshot(f"{capturas}/montaje-{k}-1.png")
            d.find_element(By.ID, "mCerrar").click()
            time.sleep(0.1)
        errs = [e["message"][:200] for e in d.get_log("browser") if e["level"] == "SEVERE" and "favicon" not in e["message"]]
        malos += errs

        d.get(f"file:///{os.path.abspath(carpeta).replace(os.sep, '/')}/imprimir.html")
        time.sleep(1.5)
        for k, m in meta.items():
            for c in m["cartas"]:
                el = [e for e in d.find_elements(By.CSS_SELECTOR, ".hoja .carta") if e.find_element(By.CSS_SELECTOR, ".num").text == c]
                if len(el) != 1 or el[0].find_elements(By.CSS_SELECTOR, ".acc, .tit, .texto"):
                    malos.append(f"{k}: la carta {c} impresa falta o lleva franjas")
        if capturas:
            hoja = d.find_elements(By.CSS_SELECTOR, ".hoja")[0]
            hoja.screenshot(f"{capturas}/hoja1.png")
    finally:
        d.quit()
    print("RESULTADO:", "OK" if not malos else malos)
    sys.exit(1 if malos else 0)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)

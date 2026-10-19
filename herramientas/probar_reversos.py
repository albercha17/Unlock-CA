"""Comprueba las cartas con dos caras de un juego (campo `reverso` en cartas.json).

1. Cada reverso (img/<id>r.jpg) existe y tiene el mismo tamaño que el anverso.
2. En pc.html solo las cartas con reverso tienen «Dar la vuelta»; al pulsarlo la carta muestra su reverso y al volver a pulsarlo, el anverso; en la carta ampliada también.
3. En imprimir.html hay hojas de reversos y las cartas de dos caras llevan su reverso ilustrado (la colocación de todos los reversos la comprueba probar_impresion.py).

Uso (desde la raíz del repo, con un servidor local en marcha: python -m http.server 8890):
    python herramientas/probar_reversos.py http://127.0.0.1:8890 juegos/aventuras-ca/futbol [carpeta_capturas]
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import By, nuevo_driver  # noqa: E402
from PIL import Image  # noqa: E402


def main(base, carpeta, capturas=None):
    datos = json.load(open(f"{carpeta}/cartas.json", encoding="utf-8"))
    datos.pop("_meta", None)
    con = [k for k, c in datos.items() if c.get("reverso")]
    malos = []
    for k in con:
        a, r = f"{carpeta}/img/{k}.jpg", f"{carpeta}/img/{k}r.jpg"
        if not os.path.exists(r):
            malos.append(f"falta el reverso {k}r.jpg")
        elif Image.open(a).size != Image.open(r).size:
            malos.append(f"el reverso de {k} no tiene el tamaño del anverso")
    print("reversos:", len(con), "cartas con dos caras", "OK" if not malos else malos)

    d = nuevo_driver()
    try:
        d.get(f"{base}/{carpeta}/pc.html")
        time.sleep(1)
        d.execute_script("localStorage.clear()")
        d.get(f"{base}/{carpeta}/pc.html")
        time.sleep(1)
        for k in list(datos)[:]:
            pass
        for k in con + [x for x in datos if x not in con][:2]:
            d.find_element(By.ID, "qn").send_keys(k)
            d.find_element(By.ID, "qb").click()
            time.sleep(0.1)

        def item(k):
            return [e for e in d.find_elements(By.CSS_SELECTOR, "#mesa .item") if e.find_element(By.CSS_SELECTOR, ".num").text == k][0]

        def fondo(k):
            return item(k).find_element(By.CSS_SELECTOR, ".arte").value_of_css_property("background-image")

        for k in [x for x in datos if x not in con and any(e.find_element(By.CSS_SELECTOR, ".num").text == x for e in d.find_elements(By.CSS_SELECTOR, "#mesa .item"))]:
            if item(k).find_elements(By.CSS_SELECTOR, ".voltear"):
                malos.append(f"la carta {k} no tiene reverso pero muestra «Dar la vuelta»")
        for k in con:
            antes = fondo(k)
            if f"/img/{k}.jpg" not in antes:
                malos.append(f"la carta {k} no empieza por su anverso: {antes}")
            item(k).find_element(By.CSS_SELECTOR, ".voltear").click()
            time.sleep(0.1)
            if f"/img/{k}r.jpg" not in fondo(k):
                malos.append(f"la carta {k} no muestra su reverso al darle la vuelta")
            if capturas and k == con[0]:
                d.find_element(By.ID, "mesa").screenshot(f"{capturas}/mesa-reverso.png")
            item(k).find_element(By.CSS_SELECTOR, ".voltear").click()
            time.sleep(0.1)
            if f"/img/{k}.jpg" not in fondo(k):
                malos.append(f"la carta {k} no vuelve a su anverso")
        # carta ampliada
        k = con[0]
        item(k).find_element(By.CSS_SELECTOR, ".carta-btn").click()
        time.sleep(0.2)
        z = d.find_element(By.ID, "zVoltear")
        if not z.is_displayed():
            malos.append("la carta ampliada con reverso no tiene «Dar la vuelta»")
        else:
            z.click()
            time.sleep(0.1)
            if f"/img/{k}r.jpg" not in d.find_element(By.CSS_SELECTOR, "#zoomCarta .arte").value_of_css_property("background-image"):
                malos.append("la carta ampliada no muestra el reverso")
        d.find_element(By.ID, "zCerrar").click()
        errs = [e["message"][:200] for e in d.get_log("browser") if e["level"] == "SEVERE" and "favicon" not in e["message"]]
        malos += errs

        d.get(f"file:///{os.path.abspath(carpeta).replace(os.sep, '/')}/imprimir.html")
        time.sleep(1.5)
        hojas = d.find_elements(By.CSS_SELECTOR, ".hoja")
        revs = d.find_elements(By.CSS_SELECTOR, ".rev")
        if sorted(r.find_element(By.CSS_SELECTOR, ".arte-rev").get_attribute("data-rev") for r in revs) != sorted(con):
            malos.append("las hojas de reversos no tienen exactamente un reverso por carta con dos caras")
        # la colocación de TODOS los reversos de todas las hojas (cartas normales y de dos caras) la comprueba probar_impresion.py
        if not any(h.get_attribute("class") and "hoja-reverso" in h.get_attribute("class") for h in hojas):
            malos.append("no hay hojas de reversos en imprimir.html")
        if capturas and revs:
            hojas[1].screenshot(f"{capturas}/hoja-reversos.png")
    finally:
        d.quit()
    print("RESULTADO:", "OK" if not malos else malos)
    sys.exit(1 if malos else 0)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)

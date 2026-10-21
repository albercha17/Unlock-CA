"""Prueba el tablero libre y los botones automáticos del Modo PC (pc.html) con el navegador real.

Uso (desde la raíz del repo, con un servidor local en marcha):
    python herramientas/probar_tablero.py http://127.0.0.1:8894 juegos/aventuras-ca/egipto [juegos/el-faro ...]
Comprueba: «Hacer lo que dice» coge y descarta de una vez, las cartas nuevas no se solapan, se arrastran con el ratón, la posición se guarda
al recargar, un arrastre no abre la carta ampliada, «Combinar con la N» coge la carta resultado y «Ordenar la mesa» recoloca.
"""
import sys
import time

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import nuevo_driver, By  # noqa: E402
from selenium.webdriver.common.action_chains import ActionChains  # noqa: E402


def ids(d, sec="mesa"):
    return [e.text for e in d.find_elements(By.CSS_SELECTOR, f"#{sec} .item .num")]


def rect(d, i):
    return d.execute_script("var r = arguments[0].getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom];", d.find_element(By.CSS_SELECTOR, f"#mesa .item[data-id='{i}']"))


def sin_solapes(d):
    rs = [rect(d, i) for i in ids(d)]
    for a in range(len(rs)):
        for b in range(a + 1, len(rs)):
            A, B = rs[a], rs[b]
            if A[0] < B[2] and B[0] < A[2] and A[1] < B[3] and B[1] < A[3]:
                return False
    return True


def probar(base, carpeta):
    d = nuevo_driver()
    try:
        url = f"{base}/{carpeta}/pc.html"
        d.get(url)
        d.execute_script("localStorage.clear()")
        d.get(url)
        time.sleep(1)
        assert ids(d) == ["P"], ids(d)
        # 1) automático
        d.find_element(By.CSS_SELECTOR, "#mesa .item[data-id='P'] .auto").click()
        time.sleep(0.3)
        assert sorted(ids(d)) == sorted(["P", "10", "12"]), ids(d)
        d.find_element(By.CSS_SELECTOR, "#mesa .item[data-id='10'] .auto").click()
        time.sleep(0.3)
        mesa = ids(d)
        assert "P" not in mesa and "14" in mesa, mesa
        assert sin_solapes(d), "hay cartas encima de otras al colocarse solas"
        # 2) arrastre
        a0 = rect(d, "14")
        carta = d.find_element(By.CSS_SELECTOR, "#mesa .item[data-id='14'] .carta-btn")
        ActionChains(d).click_and_hold(carta).move_by_offset(60, 30).move_by_offset(60, 30).release().perform()
        time.sleep(0.3)
        a1 = rect(d, "14")
        assert abs((a1[0] - a0[0]) - 120) < 6 and abs((a1[1] - a0[1]) - 60) < 6, (a0, a1)
        assert d.find_element(By.ID, "zoom").get_attribute("hidden") is not None, "el arrastre ha abierto la carta ampliada"
        # 3) se guarda
        d.get(url)
        time.sleep(1)
        a2 = rect(d, "14")
        assert abs(a2[0] - a1[0]) < 4 and abs(a2[1] - a1[1]) < 4, (a1, a2)
        # 4) clic normal abre la carta ampliada y el botón de la ampliada también funciona
        d.find_element(By.CSS_SELECTOR, "#mesa .item[data-id='14'] .carta-btn").click()
        time.sleep(0.3)
        assert d.find_element(By.ID, "zoom").get_attribute("hidden") is None, "un clic no abre la carta ampliada"
        d.find_element(By.ID, "zCerrar").click()
        # 5) combinar: hacen falta las dos cartas de la pareja en mesa
        d.find_element(By.ID, "qn").send_keys("62")
        d.find_element(By.ID, "qb").click()
        time.sleep(0.3)
        aut = d.find_elements(By.CSS_SELECTOR, "#mesa .item[data-id='12'] .auto")
        assert aut and "Combinar" in aut[0].text, "no sale «Combinar con la N» en la carta 12"
        d.execute_script("arguments[0].click()", aut[0])
        time.sleep(0.3)
        assert "74" in ids(d), ids(d)
        # 6) ordenar
        d.find_element(By.ID, "ordenar").click()
        time.sleep(0.4)
        orden = [int(x) for x in ids(d)]
        assert orden == sorted(orden), orden
        assert sin_solapes(d)
        errores = [e for e in d.get_log("browser") if e["level"] == "SEVERE" and "favicon" not in e["message"] and "video" not in e["message"].lower()]
        assert not errores, errores
        print("OK   ", carpeta)
    finally:
        d.quit()


if __name__ == "__main__":
    for c in sys.argv[2:]:
        probar(sys.argv[1], c)

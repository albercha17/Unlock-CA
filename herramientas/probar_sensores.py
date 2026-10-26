"""Prueba los puzles de sensor del Faro (juegos/el-faro/sensores.html) en modo simulado (?sim=1): silencio + soplo, agitar con fusible y las dos versiones táctiles.
Levanta su propio servidor local solo durante la prueba. Uso:  python herramientas/probar_sensores.py"""
import functools
import http.server
import os
import sys
import threading
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def servidor():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=RAIZ)
    h.log_message = lambda *a, **k: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def feedback(d):
    return d.find_element(By.CSS_SELECTOR, ".far-feedback").text


def clic(d, css):
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))


def esperar(d, f, seg):
    t0 = time.time()
    while time.time() - t0 < seg:
        if f():
            return True
        time.sleep(0.2)
    return False


def main():
    srv = servidor()
    base = f"http://127.0.0.1:{srv.server_address[1]}/juegos/el-faro/sensores.html"
    op = Options()
    op.add_argument("--headless=new")
    op.add_argument("--window-size=420,900")
    d = webdriver.Chrome(options=op)
    fallos = []
    try:
        # ---- micrófono simulado
        d.get(base + "?sim=1")
        clic(d, "#irSilencio")
        time.sleep(0.5)
        clic(d, "[data-sim='sala']")
        esperar(d, lambda: "Silencio" in d.find_element(By.CSS_SELECTOR, ".sil-e").text, 5)
        time.sleep(2)
        clic(d, "[data-sim='ruido']")
        esperar(d, lambda: "Shhh" in d.find_element(By.CSS_SELECTOR, ".sil-e").text, 3) or fallos.append("el ruido no reinicia el silencio")
        clic(d, "[data-sim='silencio']")
        esperar(d, lambda: "asentado" in d.find_element(By.CSS_SELECTOR, ".sil-e").text, 9) or fallos.append("no pasa a la fase de soplo tras 6 s de silencio")
        clic(d, "[data-sim='soplo']")
        esperar(d, lambda: "despeja" in feedback(d), 4) or fallos.append("el soplo no resuelve el puzle")
        print("micrófono simulado:", feedback(d)[:60])
        # ---- micrófono táctil
        d.get(base)
        clic(d, "#irSilencio")
        time.sleep(0.5)
        d.find_element(By.XPATH, "//button[normalize-space()='No puedo usar el micrófono']").click()
        time.sleep(0.4)
        d.execute_script("const b=document.querySelector('.sil-b');b.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));")
        esperar(d, lambda: d.find_elements(By.CSS_SELECTOR, ".sil-b[data-tactil='soplo']"), 9) or fallos.append("el botón mantenido no pasa a la fase de soplo")
        for _ in range(12):
            clic(d, ".sil-b[data-tactil='soplo']")
        esperar(d, lambda: "despeja" in feedback(d), 3) or fallos.append("los 12 toques no resuelven el puzle táctil")
        print("micrófono táctil:", feedback(d)[:60])
        # ---- agitar simulado
        d.get(base + "?sim=1")
        clic(d, "#irAgitar")
        time.sleep(0.5)
        clic(d, "[data-sim='generador']")
        clic(d, "[data-sim='fuerte']")
        esperar(d, lambda: "fusible" in d.find_element(By.CSS_SELECTOR, ".agi-e").text, 4) or fallos.append("agitar fuerte no funde el fusible")
        clic(d, "[data-sim='suave']")
        time.sleep(2)
        if "despierta" in feedback(d) or "enciende" in feedback(d):
            fallos.append("agitar suave no debería resolver")
        clic(d, "[data-sim='medio']")
        esperar(d, lambda: "enciende" in feedback(d), 8) or fallos.append("agitar con fuerza media no resuelve el puzle")
        print("agitar simulado:", feedback(d)[:60])
        # ---- agitar táctil
        d.get(base)
        clic(d, "#irAgitar")
        time.sleep(0.5)
        d.find_element(By.XPATH, "//button[normalize-space()='No puedo usar el movimiento']").click()
        time.sleep(0.4)
        t0 = time.time()
        while time.time() - t0 < 12 and "enciende" not in feedback(d):
            clic(d, ".agi-t")
            time.sleep(0.33)
        "enciende" in feedback(d) or fallos.append("la manivela táctil no resuelve el puzle")
        print("agitar táctil:", feedback(d)[:60])
        errores = [e for e in d.get_log("browser") if e["level"] == "SEVERE" and "favicon" not in e["message"] and "vibrate" not in e["message"]] if hasattr(d, "get_log") else []
        if errores:
            fallos.append("errores de consola: " + str(errores)[:200])
    finally:
        d.quit()
        srv.shutdown()
    print("FALLOS:", fallos if fallos else "ninguno")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()

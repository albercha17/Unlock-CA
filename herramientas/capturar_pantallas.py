"""Hace capturas de las pantallas principales en tamaño iPhone (menú, hub de aventuras, intro del juego, panel de juego y teclado de cartas).
Levanta su propio servidor local solo durante la captura. Uso:  python herramientas/capturar_pantallas.py <carpeta_salida> [prefijo]"""
import functools
import http.server
import os
import sys
import threading
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = sys.argv[1]
PREFIJO = sys.argv[2] if len(sys.argv) > 2 else ""


def servidor():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=RAIZ)
    h.log_message = lambda *a, **k: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main():
    os.makedirs(SALIDA, exist_ok=True)
    srv = servidor()
    base = f"http://127.0.0.1:{srv.server_address[1]}/"
    op = Options()
    op.add_argument("--headless=new")
    op.add_experimental_option("mobileEmulation", {"deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 2}, "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"})
    d = webdriver.Chrome(options=op)

    def foto(nombre, completa=False):
        time.sleep(1.2)
        ruta = os.path.join(SALIDA, f"{PREFIJO}{nombre}.png")
        if completa:
            alto = d.execute_script("return Math.min(document.documentElement.scrollHeight, 2400)")
            d.set_window_size(390, alto + 120)
            time.sleep(0.5)
        d.save_screenshot(ruta)
        print("ok", ruta)

    try:
        forzar = "var t=document.getElementById('todo'); if(t) t.hidden=false; var m=document.getElementById('mis'); if(m) m.hidden=true; document.body.classList.remove('accesos-pend');"
        d.get(base + "index.html")
        time.sleep(1.5)
        d.execute_script(forzar)
        foto("1-menu", True)
        d.get(base + "juegos/aventuras-ca/index.html")
        time.sleep(1.5)
        d.execute_script(forzar)
        foto("2-hub", True)
        d.get(base + "juegos/el-faro/index.html")
        foto("3-intro")
        d.execute_script("localStorage.clear()")
        d.execute_script("window.__t = true; document.getElementById('startBtn').click()")
        time.sleep(1.0)
        d.execute_script("var v=document.getElementById('skipVideoBtn'); if (v) v.click()")
        foto("4-juego")
        d.execute_script("document.getElementById('actionBtn').click()")
        foto("5-teclado")
    finally:
        d.quit()
        srv.shutdown()


if __name__ == "__main__":
    main()

"""Prueba el escaneo de cartas por QR SIN cámara: el QR impreso en cada carta (imprimir.html) se decodifica con el mismo lector que usa la app.

Arranca su propio servidor local. Comprueba, para cada juego:
  1. imprimir.html dibuja un QR en cada carta (con el texto «CA:<juego>:<número>»);
  2. el QR de varias cartas se vuelve a leer como imagen (generador + lector coinciden) y se interpreta como esa carta;
  3. un QR de otro juego o ajeno se rechaza con un mensaje claro.
Uso (desde la raíz del repo):  python herramientas/probar_qr.py
"""
import functools
import http.server
import json
import os
import sys
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

PUERTO = 8897
URL = f"http://127.0.0.1:{PUERTO}/"
JUEGOS = [("faro", "juegos/el-faro/"), ("egipto", "juegos/aventuras-ca/egipto/"), ("marte", "juegos/aventuras-ca/marte/"),
          ("florencia", "juegos/aventuras-ca/florencia/"), ("dinosaurios", "juegos/aventuras-ca/dinosaurios/"),
          ("cuento", "juegos/aventuras-ca/cuento/"), ("trono", "juegos/aventuras-ca/trono/"), ("pompeya", "juegos/aventuras-ca/pompeya/")]


class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


class S(http.server.ThreadingHTTPServer):
    def handle_error(self, *a):
        pass


JS = """
const hecho = arguments[arguments.length - 1];
(async () => {
  const esc = await import('/assets/js/escaner.js');
  await new Promise((ok) => { const s = document.createElement('script'); s.src = '/assets/js/vendor/jsQR.js'; s.onload = ok; document.head.appendChild(s); });
  const res = { total: 0, conQr: 0, leidos: 0, mal: [], ids: [] };
  const juego = arguments[0];
  const qrs = [...document.querySelectorAll('.carta .qr')];
  res.total = document.querySelectorAll('.carta:not(.dorso)').length;
  res.conQr = qrs.length;
  // leemos todas las cartas: dibujamos el SVG del QR en un canvas grande con margen blanco (como lo vería la cámara)
  for (const el of qrs) {
    const svg = el.querySelector('svg');
    const xml = new XMLSerializer().serializeToString(svg);
    const img = new Image();
    await new Promise((ok, mal) => { img.onload = ok; img.onerror = mal; img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(xml); });
    const c = document.createElement('canvas'); c.width = c.height = 260;
    const x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, 260, 260); x.drawImage(img, 30, 30, 200, 200);
    const t = esc.decodificar(x.getImageData(0, 0, 260, 260));
    const i = esc.interpretar(t, juego);
    if (i.id && i.id === el.dataset.qr.split(':')[2]) res.leidos++; else res.mal.push([el.dataset.qr, t]);
  }
  res.ajeno = esc.interpretar('CA:otrojuego:12', juego);
  res.basura = esc.interpretar('https://example.com', juego);
  hecho(res);
})().catch((e) => hecho({ error: String(e) }));
"""


def main():
    srv = S(("127.0.0.1", PUERTO), functools.partial(H, directory=os.getcwd()))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    o = webdriver.ChromeOptions()
    o.add_argument("--headless=new")
    o.add_argument("--window-size=1000,1300")
    d = webdriver.Chrome(options=o)
    d.set_script_timeout(120)
    fallos = 0
    try:
        for clave, ruta in JUEGOS:
            d.get(URL + ruta + "imprimir.html")
            time.sleep(2.5)
            r = d.execute_async_script(JS, clave)
            bien = ("error" not in r and r["conQr"] == r["total"] > 0 and r["leidos"] == r["conQr"] and not r["mal"]
                    and "otro juego" in (r["ajeno"].get("error") or "") and "no es de una carta" in (r["basura"].get("error") or ""))
            print(("OK    " if bien else "FALLO ") + f"{clave}: {r.get('leidos')}/{r.get('total')} QR leídos" + ("" if bien else " " + json.dumps(r)[:300]), flush=True)
            fallos += 0 if bien else 1
    finally:
        d.quit()
        srv.shutdown()
    print("RESULTADO:", "OK" if not fallos else f"{fallos} juegos con fallos")
    sys.exit(0 if not fallos else 1)


if __name__ == "__main__":
    main()

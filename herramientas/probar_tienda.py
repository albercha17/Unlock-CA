"""Prueba la tienda (tienda/index.html?demo) con Chrome headless: elegir 4 aventuras, subir fotos, validar y enviar.

Arranca su propio servidor local (y lo cierra al acabar). En modo ?demo no se envía nada a Supabase.
Uso: python herramientas/probar_tienda.py [carpeta_para_capturas]
"""
import functools
import http.server
import os
import sys
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPTURAS = sys.argv[1] if len(sys.argv) > 1 else None
FOTO = os.path.join(RAIZ, "juegos", "aventuras-ca", "egipto", "img", "P.jpg")
fallos = []
sys.stdout.reconfigure(encoding="utf-8")


def comprobar(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


def servidor():
    class Silencioso(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

    manejador = functools.partial(Silencioso, directory=RAIZ)
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), manejador)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def navegador(ancho, alto):
    o = webdriver.ChromeOptions()
    o.add_argument("--headless=new")
    o.add_argument(f"--window-size={ancho},{alto}")
    o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    return webdriver.Chrome(options=o)


def captura(d, nombre, pagina_entera=True):
    if not CAPTURAS:
        return
    if pagina_entera:
        alto = d.execute_script("return document.documentElement.scrollHeight")
        d.set_window_size(d.get_window_size()["width"], alto)
        time.sleep(0.4)
    d.save_screenshot(os.path.join(CAPTURAS, nombre))


def errores_consola(d):
    return [l["message"] for l in d.get_log("browser") if l["level"] == "SEVERE" and "favicon" not in l["message"]]


def flujo(d, url):
    d.get(url)
    time.sleep(1)
    js = d.execute_script
    import json as _json
    n_cat = len([j for j in _json.load(open(os.path.join(RAIZ, "juegos", "catalogo.json"), encoding="utf-8")) if j["ruta"].startswith("juegos/aventuras-ca/")])
    esperar_n = lambda: len(d.find_elements(By.CSS_SELECTOR, ".aventura")) == n_cat  # noqa: E731
    for _ in range(30):
        if esperar_n():
            break
        time.sleep(0.2)
    comprobar(esperar_n(), f"se pintan todas las aventuras del catálogo ({len(d.find_elements(By.CSS_SELECTOR, '.aventura'))} de {n_cat})")
    comprobar(len(d.find_elements(By.CSS_SELECTOR, "#selector-aventuras input")) == n_cat, "y todas se pueden elegir en el formulario")
    # buscador y filtro de dificultad
    vis = lambda sel: len([e for e in d.find_elements(By.CSS_SELECTOR, sel) if e.is_displayed()])  # noqa: E731
    barra = d.find_elements(By.CSS_SELECTOR, ".fj")
    comprobar(len(barra) == 2, "hay buscador en la lista de aventuras y en el formulario")
    caja = barra[0].find_element(By.TAG_NAME, "input")
    caja.send_keys("egipto")
    comprobar(vis("#lista-aventuras .aventura") == 1, "buscar «egipto» deja una aventura")
    caja.clear(); caja.send_keys("piratas"); time.sleep(0.2)
    comprobar(vis("#lista-aventuras .aventura") == 1, "buscar «piratas» (sin tilde ni mayúsculas) la encuentra")
    js("const i=document.querySelector('.fj input'); i.value=''; i.dispatchEvent(new Event('input'))")
    barra[0].find_element(By.CSS_SELECTOR, "[data-nivel=dificil]").click()
    difs = [int(e.get_attribute("data-dif")) for e in d.find_elements(By.CSS_SELECTOR, "#lista-aventuras .aventura") if e.is_displayed()]
    comprobar(difs and all(x >= 4 for x in difs), f"«Difícil» deja solo las difíciles ({difs})")
    caja.send_keys("zzzz")
    comprobar(d.find_elements(By.CSS_SELECTOR, ".fj-vacio")[0].is_displayed(), "sin resultados sale un aviso")
    js("const i=document.querySelector('.fj input'); i.value=''; i.dispatchEvent(new Event('input'))")
    barra[0].find_element(By.CSS_SELECTOR, "[data-nivel=todas]").click()
    comprobar(vis("#lista-aventuras .aventura") == n_cat, "«Todas» vuelve a enseñarlas todas")
    comprobar(d.find_element(By.ID, "resumen-precio").text == "49 €", "precio inicial 49 €")
    comprobar(not js("return [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src)"), "todas las imágenes cargan")

    # enviar vacío: debe marcar errores y no enviar
    js("document.getElementById('enviar').click()")
    time.sleep(0.4)
    comprobar("Elegid 4" in d.find_element(By.CSS_SELECTOR, '[data-error="aventuras"]').text, "aviso si faltan aventuras")
    comprobar(d.find_element(By.ID, "gracias").get_attribute("hidden") is not None, "no se envía un pedido vacío")

    # 4 desde las tarjetas; la 5.ª queda bloqueada
    for b in d.find_elements(By.CSS_SELECTOR, "[data-alternar]")[:4]:
        js("arguments[0].click()", b)
    comprobar(d.find_element(By.ID, "contador").text == "4/4", "contador 4/4")
    quinta = d.find_elements(By.CSS_SELECTOR, "[data-alternar]")[4]
    comprobar(not quinta.is_enabled(), "la quinta aventura queda bloqueada")
    comprobar(js("return document.querySelectorAll('#selector-aventuras input:checked').length") == 4, "el formulario refleja las 4 elegidas")
    # quitar una desde el formulario y poner otra
    js("document.querySelector('#selector-aventuras input:checked').click()")
    js("document.querySelector('#selector-aventuras input:not(:checked)').click()")
    comprobar(d.find_element(By.ID, "contador").text == "4/4", "cambiar una aventura desde el formulario")

    # protagonistas con fotos
    for i, nombre in enumerate(["Lucía", "Marcos"]):
        d.find_element(By.NAME, f"p{i}-nombre").send_keys(nombre)
        d.execute_script(f"document.querySelector('[name=p{i}-genero]').value = '{'mujer' if i == 0 else 'hombre'}'")
        d.find_element(By.CSS_SELECTOR, f'[data-subir="{i}"]').send_keys(FOTO)
        time.sleep(0.8)
    # con una sola foto por persona no deja enviar
    js("document.getElementById('enviar').click()")
    time.sleep(0.4)
    comprobar("Faltan fotos" in d.find_element(By.CSS_SELECTOR, '[data-error="p0-fotos"]').text, "exige 2 fotos por persona")
    for i in range(2):
        d.find_element(By.CSS_SELECTOR, f'[data-subir="{i}"]').send_keys(FOTO)
        time.sleep(0.8)
    d.find_element(By.CSS_SELECTOR, '[data-subir="0"]').send_keys(FOTO)
    time.sleep(0.8)
    comprobar(len(d.find_elements(By.CSS_SELECTOR, '[data-fotos="0"] .foto-mini')) == 3, "tres fotos en el protagonista 1")
    js("document.querySelector('[data-quitar=\"0-2\"]').click()")
    comprobar(len(d.find_elements(By.CSS_SELECTOR, '[data-fotos="0"] .foto-mini')) == 2, "quitar una foto")
    comprobar("Lucía y Marcos" in d.find_element(By.ID, "resumen-protas").text, "resumen con los protagonistas")

    # impreso: pide dirección y cambia el precio
    js("document.querySelector('input[name=formato][value=impreso]').click()")
    comprobar(d.find_element(By.ID, "resumen-precio").text == "79 €", "precio del impreso 79 €")
    comprobar(d.find_element(By.ID, "campo-direccion").is_displayed(), "aparece la dirección en el impreso")

    d.find_element(By.NAME, "nombre").send_keys("Lucía Pérez")
    d.find_element(By.NAME, "email").send_keys("lucia@ejemplo.com")
    js("document.getElementById('enviar').click()")
    time.sleep(0.4)
    comprobar(bool(d.find_element(By.CSS_SELECTOR, '[data-error="direccion"]').text), "exige dirección en el impreso")
    comprobar(bool(d.find_element(By.CSS_SELECTOR, '[data-error="acepta"]').text), "exige el permiso de las fotos")
    d.find_element(By.NAME, "direccion").send_keys("Calle Mayor 1, 28013 Madrid")
    js("document.querySelector('input[name=acepta]').click()")
    js("document.getElementById('enviar').click()")
    time.sleep(2)
    comprobar(d.find_element(By.ID, "gracias").is_displayed(), "pedido enviado (demo) y pantalla de gracias")
    comprobar(len(d.find_element(By.ID, "gracias-codigo").text) == 8, "número de pedido de 8 caracteres")
    comprobar(not errores_consola(d), f"sin errores en consola {errores_consola(d)}")


def main():
    s = servidor()
    base = f"http://127.0.0.1:{s.server_address[1]}/tienda/"
    try:
        for ancho, alto in ((1366, 900), (390, 844)):
            print(f"--- {ancho}px ---")
            d = navegador(ancho, alto)
            try:
                d.get(base + "?demo")
                time.sleep(1.2)
                desborde = d.execute_script("return document.documentElement.scrollWidth - document.documentElement.clientWidth")
                comprobar(desborde <= 0, f"sin scroll horizontal ({desborde}px)")
                captura(d, f"tienda-{ancho}.png")
                d.set_window_size(ancho, alto)
                flujo(d, base + "?demo")
            finally:
                d.quit()
    finally:
        s.shutdown()
    print("\nTodo correcto" if not fallos else f"\n{len(fallos)} fallo(s)")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()

"""Libera espacio en ChatGPT borrando imágenes de la Biblioteca (Chrome de depuración abierto con abrir_chrome_chatgpt.ps1, sesión iniciada).
Conserva las N más recientes (por defecto 50: la página las ordena de más nueva a más antigua) y borra el resto en lotes.
Uso:  python herramientas/chatgpt_limpiar_imagenes.py [--conservar 50] [--lote 150] [--tandas 20] [--probar]
--probar  borra un solo lote de 20 imágenes (para ver el cuadro de confirmación)."""
import argparse
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding="utf-8")
URL = "https://chatgpt.com/library?tab=images&storage_cleanup=true"
SEL = "//button[starts-with(@aria-label,'Seleccionar ')]"


def conectar():
    op = Options()
    op.debugger_address = "127.0.0.1:9222"
    return webdriver.Chrome(options=op)


def cargar(d, minimo):
    """Baja por la página hasta tener cargadas al menos `minimo` imágenes seleccionables (o hasta que no salgan más)."""
    previo, quietas = -1, 0
    while True:
        n = len(d.find_elements(By.XPATH, SEL))
        if n >= minimo or quietas >= 4:
            return n
        d.execute_script("""
          const els = [...document.querySelectorAll('main *')].filter(e => e.scrollHeight > e.clientHeight + 50 && ['auto','scroll'].includes(getComputedStyle(e).overflowY));
          (els.pop() || document.scrollingElement).scrollTo(0, 1e9);""")
        time.sleep(1.6)
        quietas = quietas + 1 if n == previo else 0
        previo = n


def estado_almacenamiento(d):
    d.get("https://chatgpt.com/settings/storage")
    time.sleep(5)
    t = d.find_element(By.TAG_NAME, "body").text
    return [l for l in t.splitlines() if "GB" in l or "imágenes" in l]


def lote(d, conservar, tam):
    d.get(URL)
    time.sleep(6)
    n = cargar(d, conservar + tam)
    botones = d.find_elements(By.XPATH, SEL)[conservar:conservar + tam]
    if not botones:
        return 0
    nombres = [b.get_attribute("aria-label") for b in botones]
    d.execute_script("arguments[0].forEach(b => b.click())", botones)
    time.sleep(2)
    marcadas = d.execute_script("return document.body.innerText.match(/(\\d+) seleccionad/)?.[1] || '0'")
    print(f"  cargadas {n}; marcadas {marcadas} de {len(botones)} (primera: {nombres[0][:40]}; última: {nombres[-1][:40]})", flush=True)
    d.find_element(By.XPATH, "//button[normalize-space()='Eliminar']").click()
    time.sleep(2)
    # cuadro de confirmación
    for t in ("Eliminar", "Borrar", "Confirmar", "Sí"):
        cs = [b for b in d.find_elements(By.XPATH, f"//div[@role='dialog' or @role='alertdialog']//button[normalize-space()='{t}']")]
        if cs:
            cs[-1].click()
            break
    time.sleep(25)                      # el borrado es asíncrono: si se recarga antes, se corta
    return len(botones)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conservar", type=int, default=50)
    ap.add_argument("--lote", type=int, default=150)
    ap.add_argument("--tandas", type=int, default=20)
    ap.add_argument("--probar", action="store_true")
    a = ap.parse_args()
    d = conectar()
    print("antes:", estado_almacenamiento(d), flush=True)
    for i in range(1 if a.probar else a.tandas):
        borradas = lote(d, a.conservar, 20 if a.probar else a.lote)
        print(f"tanda {i + 1}: {borradas} imágenes borradas", flush=True)
        if borradas == 0:
            break
    print("después:", estado_almacenamiento(d), flush=True)


if __name__ == "__main__":
    main()

"""Abre el visor de Pistas de la app con CADA carta del juego y recorre todas sus pistas.
Uso: python herramientas/probar_pistas.py http://127.0.0.1:8870 juegos/aventuras-ca/florencia"""
import sys, time, json
sys.path.insert(0, "herramientas")
from bot_core import *

BASE = sys.argv[1]
carpeta = sys.argv[2]
datos = json.load(open(f"{carpeta}/cartas.json", encoding="utf-8"))
ids = [k for k in datos if k != "_meta"]
d = nuevo_driver()
malos = []
try:
    abrir_app(d, f"{BASE}/{carpeta}/index.html")
    for k in ids:
        pistas = datos[k].get("pistas", [])
        d.find_element(By.ID, "hintBtn").click()
        time.sleep(0.25)
        for ch in k:
            d.find_element(By.CSS_SELECTOR, f".num-key[data-key='{ch}']").click()
        d.find_element(By.ID, "numOk").click()
        time.sleep(0.5)
        titulo = [e.text for e in d.find_elements(By.CSS_SELECTOR, ".pst-title") if e.is_displayed()]
        texto = [e.text for e in d.find_elements(By.CSS_SELECTOR, ".pst-text") if e.is_displayed()]
        msg = d.find_element(By.ID, "numMessage").text
        ok = bool(titulo) and datos[k]["titulo"].split("—")[1].strip() in titulo[0] if pistas else True
        if pistas:
            # recorrer todas las pistas con Siguiente
            vistas = [texto[0] if texto else ""]
            for _ in range(len(pistas) - 1):
                for b in d.find_elements(By.CSS_SELECTOR, ".pst-primary"):
                    if b.is_displayed() and b.is_enabled():
                        b.click(); time.sleep(0.15)
                        break
                t2 = [e.text for e in d.find_elements(By.CSS_SELECTOR, ".pst-text") if e.is_displayed()]
                vistas.append(t2[0] if t2 else "")
            ok = ok and all(v for v in vistas)
        if not ok:
            malos.append((k, titulo, texto, msg))
        # cerrar visor
        for b in d.find_elements(By.XPATH, "//button[normalize-space()='Cerrar']"):
            try:
                b.click(); time.sleep(0.2); break
            except Exception:
                pass
        print(k, "OK" if ok else "FALLA", "| pistas:", len(pistas), "| mensaje:", msg[:50])
    print("FALLOS:", malos)
finally:
    d.quit()

"""Comprueba que cada carta de imprimir.html muestra exactamente lo que dice cartas.json:
las franjas Coge / Descarta / Combinable (siempre deben estar en cualquier juego) y que no sobra ninguna.

Uso (desde la raiz del repo):
    python herramientas/probar_impresion.py juegos/el-faro juegos/aventuras-ca/egipto juegos/aventuras-ca/marte
Abre las paginas con file:// (como un doble clic), asi tambien prueba cartas-data.js.
"""
import json
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

JS = """
return [...document.querySelectorAll('.hoja .carta')].map(c => ({
  id: c.querySelector('.num') ? c.querySelector('.num').textContent.trim() : null,
  coge: [...c.querySelectorAll('.acc .coge i')].map(i => i.textContent.trim()),
  descarta: [...c.querySelectorAll('.acc .des i')].map(i => i.textContent.trim()),
  combina: !!c.querySelector('.acc .comb'),
  arte: (c.querySelector('.arte').style.backgroundImage || '')
}));
"""


def main(carpetas):
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    o = Options()
    o.add_argument("--headless=new")
    o.add_argument("--window-size=1100,1000")
    d = webdriver.Chrome(options=o)
    malos = 0
    try:
        for carpeta in carpetas:
            datos = json.load(open(os.path.join(raiz, carpeta, "cartas.json"), encoding="utf-8"))
            d.get("file:///" + os.path.join(raiz, carpeta, "imprimir.html").replace("\\", "/"))
            time.sleep(2.5)
            impresas = {c["id"]: c for c in d.execute_script(JS)}
            falta = [k for k in datos if k != "_meta" and k not in impresas]
            sobra = [k for k in impresas if k not in datos]
            errores = [f"faltan cartas impresas: {falta}"] if falta else []
            errores += [f"sobran cartas impresas: {sobra}"] if sobra else []
            sin_arte = []
            for k, c in datos.items():
                if k == "_meta" or k not in impresas:
                    continue
                p = impresas[k]
                if [str(x) for x in c.get("coge", [])] != p["coge"]:
                    errores.append(f"carta {k}: coge impreso {p['coge']} != {c.get('coge', [])}")
                if [str(x) for x in c.get("descarta", [])] != p["descarta"]:
                    errores.append(f"carta {k}: descarta impreso {p['descarta']} != {c.get('descarta', [])}")
                if bool(c.get("combina")) != p["combina"]:
                    errores.append(f"carta {k}: 'Combinable' impreso={p['combina']} pero cartas.json={bool(c.get('combina'))}")
                if "img/" not in p["arte"]:
                    sin_arte.append(k)
            if sin_arte:
                errores.append(f"sin ilustracion cargada: {sin_arte}")
            n = len(impresas)
            print(("OK   " if not errores else "FALLA"), carpeta, f"({n} cartas impresas)")
            for e in errores:
                print("      ", e)
            malos += len(errores)
    finally:
        d.quit()
    sys.exit(1 if malos else 0)


if __name__ == "__main__":
    import glob
    main(sys.argv[1:] or ["juegos/el-faro"] + sorted(p.replace("\\", "/").rsplit("/cartas.json", 1)[0] for p in glob.glob("juegos/aventuras-ca/*/cartas.json")))

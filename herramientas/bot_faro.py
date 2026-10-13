import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *

BASE = sys.argv[1]
J = "juegos/el-faro"


def s15(d):
    abrir_carta(d, "15")
    for _ in range(3):
        boton(d, "Siguiente →").click()
    texto = d.find_element(By.CSS_SELECTOR, ".far-hoja").text
    cerrar(d)
    return "(lector) " + texto[:40]


def s36(d):
    abrir_carta(d, "36")
    for ch in "0435":
        tecla(d, ch)
    tecla(d, "✓")
    m = feedback(d)
    cerrar(d)
    return m


def s52(d):
    abrir_carta(d, "52")
    for ch in "ANCLA":
        tecla(d, ch)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s85(d):
    abrir_carta(d, "85")
    js(d, "var r=document.getElementById('farDial'); r.value='91.7'; r.dispatchEvent(new Event('input'));")
    time.sleep(1.4)
    m = feedback(d)
    cerrar(d)
    return m


def s70(d):
    abrir_carta(d, "70")
    for i in range(3):
        js(d, "document.querySelectorAll('svg rect[fill=transparent]')[%d].dispatchEvent(new MouseEvent('click',{bubbles:true}));" % i)
        time.sleep(0.1)
    m = feedback(d)
    cerrar(d)
    return m


def s95(d):
    abrir_carta(d, "95")
    for paso in ["Abrir la válvula del aceite", "Cebar la mecha", "Girar el engranaje", "Encender el piloto", "Soltar el freno de la lente"]:
        d.find_element(By.XPATH, f"//button[contains(@class,'far-step')][.//span[text()='{paso}']]").click()
    boton(d, "Arrancar").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"15": s15, "36": s36, "52": s52, "85": s85, "70": s70, "95": s95}
REQUIERE = {
    "36": ["21", "19"],          # reloj + retraso del paraguas
    "52": ["15"],                # tabla de morse
    "85": ["74", "3"],           # mapa + brujula
    "70": ["27"],                # pista del nido
    "95": ["15", "12", "18", "82"]
}
ok = jugar("EL FARO", f"{BASE}/{J}/pc.html", f"{BASE}/{J}/index.html", SOLVERS, REQUIERE)
sys.exit(0 if ok else 1)

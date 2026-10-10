"""Genera las ilustraciones usando la web de ChatGPT (sin API, con tu suscripción).

Abre un Chrome VISIBLE con un perfil propio (se guarda en .chrome-profile para
no tener que iniciar sesión cada vez). La primera vez inicia sesión a mano.

Uso (desde esta carpeta):
    python generar_chatgpt.py                # todas las que falten
    python generar_chatgpt.py --solo 3 7 P   # solo esas cartas
    python generar_chatgpt.py --forzar       # regenera aunque existan

Se puede cortar y relanzar: salta las que ya están en arte/.
No toques el navegador mientras trabaja. Si ChatGPT te pone un límite de
imágenes, el script se detiene y lo relanzas más tarde.
"""
import argparse
import base64
import io
import json
import random
import sys
import time
from pathlib import Path

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).parent
ARTE = AQUI / "arte"
PERFIL = AQUI / ".chrome-profile"
HOJA = ARTE / "_personajes.png"
URL = "https://chatgpt.com/"
MAX_ESPERA_IMAGEN = 420  # segundos por imagen

JS_ESCRIBIR = """
const el = document.querySelector('#prompt-textarea');
el.focus();
document.execCommand('selectAll');
document.execCommand('delete');
document.execCommand('insertText', false, arguments[0]);
"""

JS_IMAGENES = """
const out = [];
const raiz = document.querySelectorAll('[data-message-author-role="assistant"] img');
const lista = raiz.length ? raiz : document.querySelectorAll('main img');
lista.forEach(i => { if (i.complete && i.naturalWidth >= 512 && i.src) out.push(i.src); });
return out;
"""

JS_DESCARGAR = """
const hecho = arguments[arguments.length - 1];
fetch(arguments[0], {credentials: 'include'})
  .then(r => r.blob())
  .then(b => { const fr = new FileReader(); fr.onloadend = () => hecho(fr.result); fr.readAsDataURL(b); })
  .catch(e => hecho('ERR:' + e));
"""


def cargar():
    datos = json.loads((AQUI / "cartas.json").read_text(encoding="utf-8"))
    return datos.pop("_meta"), datos


def orden(clave):
    return (0, 0) if clave == "P" else (1, int(clave))


def quienes_salen(arte, personajes):
    salen = [n for n in personajes if n in arte]
    if "anciano de barba blanca" in arte and "Anselmo" not in salen:
        salen.append("Anselmo")
    return salen


def prompt_carta(carta, meta):
    salen = quienes_salen(carta["arte"], meta["personajes"])
    p = ("Genera una imagen vertical con proporción 2:3 para una carta de juego de escape room. "
         + carta["arte"])
    if salen:
        p += (" Personajes (mantén exactamente el mismo aspecto que en las imágenes anteriores): "
              + " ".join(meta["personajes"][n] for n in salen))
    p += " " + meta["estilo"] + " Muy importante: no escribas ningún texto, letra ni número dentro de la imagen."
    return " ".join(p.split())


def prompt_hoja(meta):
    p = ("Genera una imagen: hoja de personajes (character sheet) con tres personas de cuerpo entero, "
         "de frente, sobre fondo claro y neutro. "
         + " ".join(f"{n}: {d}" for n, d in meta["personajes"].items())
         + " " + meta["estilo"] + " Sin ningún texto ni letras en la imagen.")
    return " ".join(p.split())


class Chat:
    def __init__(self):
        PERFIL.mkdir(exist_ok=True)
        opts = webdriver.ChromeOptions()
        opts.add_argument(f"--user-data-dir={PERFIL}")
        opts.add_argument("--window-size=1200,900")
        self.d = webdriver.Chrome(options=opts)
        self.d.set_script_timeout(90)
        self.vistas = set()

    def abrir(self):
        self.d.get(URL)
        for _ in range(30):
            if self.d.find_elements(By.CSS_SELECTOR, "#prompt-textarea"):
                return
            time.sleep(1)
        input("Inicia sesión en ChatGPT en la ventana de Chrome (y resuelve lo que te pida) y pulsa Enter aquí...")
        for _ in range(60):
            if self.d.find_elements(By.CSS_SELECTOR, "#prompt-textarea"):
                return
            time.sleep(1)
        sys.exit("No encuentro el cuadro de texto de ChatGPT.")

    def adjuntar(self, ruta):
        try:
            entrada = self.d.find_elements(By.CSS_SELECTOR, "input[type=file]")[0]
            entrada.send_keys(str(ruta))
            time.sleep(4)
            return True
        except Exception as e:  # noqa: BLE001
            print(f"  ! no pude adjuntar la referencia: {e}")
            return False

    def enviar(self, texto):
        self.d.execute_script(JS_ESCRIBIR, texto)
        time.sleep(1.5)
        botones = self.d.find_elements(By.CSS_SELECTOR, "button[data-testid='send-button']")
        if botones:
            botones[0].click()
        else:
            ActionChains(self.d).send_keys(Keys.ENTER).perform()

    def esperar_imagen(self):
        """Devuelve la URL de la imagen nueva o None si se agota el tiempo."""
        t0 = time.time()
        estable = 0
        while time.time() - t0 < MAX_ESPERA_IMAGEN:
            time.sleep(3)
            nuevas = [s for s in self.d.execute_script(JS_IMAGENES) if s not in self.vistas]
            generando = bool(self.d.find_elements(By.CSS_SELECTOR, "button[data-testid='stop-button']"))
            if nuevas and not generando:
                estable += 1
                if estable >= 2:
                    return nuevas[-1]
            else:
                estable = 0
        return None

    def descargar(self, src, destino):
        datos = self.d.execute_async_script(JS_DESCARGAR, src)
        if not datos or datos.startswith("ERR:"):
            raise RuntimeError(datos or "respuesta vacía")
        crudo = base64.b64decode(datos.split(",", 1)[1])
        Image.open(io.BytesIO(crudo)).convert("RGB").save(destino, "PNG")
        self.vistas.add(src)

    def hay_limite(self):
        texto = self.d.find_element(By.TAG_NAME, "body").text.lower()
        return any(p in texto for p in ("límite", "limite", "limit", "vuelve más tarde", "come back later"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo", nargs="*")
    ap.add_argument("--forzar", action="store_true")
    args = ap.parse_args()

    meta, cartas = cargar()
    ids = sorted(cartas, key=orden)
    if args.solo:
        malas = [i for i in args.solo if i not in cartas]
        if malas:
            sys.exit(f"Cartas que no existen: {malas}")
        ids = [i for i in ids if i in args.solo]
    pendientes = [i for i in ids if args.forzar or not (ARTE / f"{i}.png").exists()]
    if not pendientes and HOJA.exists():
        sys.exit("No falta ninguna imagen.")

    ARTE.mkdir(exist_ok=True)
    chat = Chat()
    try:
        chat.abrir()
        primera = True

        if not HOJA.exists() or args.forzar:
            print("Hoja de personajes...")
            chat.enviar(prompt_hoja(meta))
            src = chat.esperar_imagen()
            if not src:
                sys.exit("No salió la hoja de personajes (¿límite de imágenes?). Inténtalo más tarde.")
            chat.descargar(src, HOJA)
            print("  ok -> arte/_personajes.png")
            primera = False

        hechas = 0
        for n, i in enumerate(pendientes, 1):
            print(f"[{n}/{len(pendientes)}] Carta {i}: {cartas[i]['titulo']}")
            texto = prompt_carta(cartas[i], meta)
            if primera:
                if chat.adjuntar(HOJA):
                    texto = ("Usa a los personajes de la imagen adjunta como referencia fija en todas las "
                             "imágenes que te pida a partir de ahora. " + texto)
                primera = False
            chat.enviar(texto)
            src = chat.esperar_imagen()
            if not src:
                if chat.hay_limite():
                    print("  ! ChatGPT indica límite de imágenes. Relanza el script más tarde.")
                    break
                print("  x no salió imagen, paso a la siguiente")
                continue
            try:
                chat.descargar(src, ARTE / f"{i}.png")
            except Exception as e:  # noqa: BLE001
                print(f"  x no pude guardarla: {e}")
                continue
            hechas += 1
            print(f"  ok -> arte/{i}.png")
            time.sleep(random.uniform(8, 15))

        print(f"\nListo: {hechas} de {len(pendientes)} imágenes guardadas.")
    finally:
        input("Pulsa Enter para cerrar el navegador...")
        chat.d.quit()


if __name__ == "__main__":
    main()

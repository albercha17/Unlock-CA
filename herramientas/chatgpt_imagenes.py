"""Genera con la web de ChatGPT (Selenium, sin API) la hoja de personajes y las ilustraciones de las cartas.

1) Hoja de personajes: adjunta la FOTO de Cristina y Alberto y pide la hoja -> personajes/hoja.png
2) Cartas de cada juego: adjunta la hoja y pide cada carta -> <juego>/arte/ID.png
   (despues: python herramientas/preparar_imagenes.py <juego> las convierte a img/ID.jpg)

Todo lo privado queda FUERA de git: el perfil de Chrome con tu sesion vive en
%USERPROFILE%/.unlock-chatgpt-profile, y la foto, personajes/ y */arte/ estan en .gitignore.

Uso (desde la raiz del repo):
    python herramientas/chatgpt_imagenes.py --foto F1.jpg F2.jpg --hoja         # solo la hoja
    python herramientas/chatgpt_imagenes.py Aventuras-CA/Egipto                    # las cartas que falten
    python herramientas/chatgpt_imagenes.py Aventuras-CA/Marte --solo 10 33 P      # solo esas
    python herramientas/chatgpt_imagenes.py Aventuras-CA/Marte --forzar            # regenera todas
    python herramientas/chatgpt_imagenes.py --foto F.jpg --hoja Aventuras-CA/Egipto Aventuras-CA/Marte

La primera vez se abre Chrome: inicia sesion en ChatGPT a mano (el script espera hasta 10 min).
Se puede cortar y relanzar: salta lo que ya existe. Si ChatGPT pone limite de imagenes, para.
"""
import argparse
import base64
import io
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parent.parent
PERFIL = Path(os.path.expanduser("~")) / ".unlock-chatgpt-profile"
HOJA = RAIZ / "personajes" / "hoja.png"
URL = "https://chatgpt.com/"
MAX_ESPERA_IMAGEN = 420
CARTAS_POR_CHAT = 8

ESTILO_HOJA = ("Ilustración digital pintada con estética de película de aventuras, trazo limpio y colores "
               "naturales, formato vertical 2:3.")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado, ojos azules.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones.",
}

JS_ESCRIBIR = """
const el = document.querySelector("div[contenteditable='true'][role='textbox'], #prompt-textarea");
el.focus();
document.execCommand('selectAll');
document.execCommand('delete');
document.execCommand('insertText', false, arguments[0]);
"""

JS_IMAGENES = """
const out = [];
const raiz = document.querySelectorAll('[data-testid="generated-image-gallery"] img, [data-message-author-role="assistant"] img');
const lista = raiz;
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


def orden(clave):
    return (0, 0) if clave == "P" else (1, int(clave))


class Chat:
    def __init__(self, puerto=None):
        opts = webdriver.ChromeOptions()
        if puerto:
            # Chrome abierto por ti con abrir_chrome_chatgpt.ps1 (navegador normal, sin automatizar)
            opts.debugger_address = f"127.0.0.1:{puerto}"
        else:
            PERFIL.mkdir(exist_ok=True)
            opts.add_argument(f"--user-data-dir={PERFIL}")
            opts.add_argument("--window-size=1200,900")
        self.d = webdriver.Chrome(options=opts)
        self.d.set_script_timeout(90)
        self.vistas = set()

    def hay_cuadro(self):
        return bool(self.d.find_elements(By.CSS_SELECTOR, "div[contenteditable=true][role=textbox], #prompt-textarea"))

    def nuevo_chat(self):
        self.d.get(URL)
        for _ in range(20):
            if self.hay_cuadro():
                return
            time.sleep(1)
        print("Inicia sesión en ChatGPT en la ventana de Chrome (espero hasta 10 minutos)...")
        for _ in range(600):
            if self.hay_cuadro():
                return
            time.sleep(1)
        captura = Path(os.environ.get("TEMP", ".")) / "chatgpt_error.png"
        self.d.save_screenshot(str(captura))
        sys.exit(f"No encuentro el cuadro de texto de ChatGPT (url={self.d.current_url}, captura={captura}).")

    def adjuntar(self, ruta):
        try:
            self.d.find_elements(By.CSS_SELECTOR, "input[type=file][aria-label^=Adjuntar][accept*=image], input[type=file][multiple]")[0].send_keys(str(Path(ruta).resolve()))
            time.sleep(6)
            return True
        except Exception as e:  # noqa: BLE001
            print(f"  ! no pude adjuntar {ruta}: {e}")
            return False

    def enviar(self, texto):
        self.vistas.update(self.d.execute_script(JS_IMAGENES))  # lo que ya habia no cuenta como respuesta nueva
        self.d.execute_script(JS_ESCRIBIR, texto)
        time.sleep(1.5)
        botones = self.d.find_elements(By.CSS_SELECTOR, "button[data-testid='send-button']")
        if botones:
            botones[0].click()
        else:
            ActionChains(self.d).send_keys(Keys.ENTER).perform()

    def esperar_imagen(self):
        t0, estable = time.time(), 0
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
        destino.parent.mkdir(parents=True, exist_ok=True)
        Image.open(io.BytesIO(crudo)).convert("RGB").save(destino, "PNG")
        self.vistas.add(src)

    def hay_limite(self):
        texto = self.d.find_element(By.TAG_NAME, "body").text.lower()
        return any(p in texto for p in ("límite", "limite", "limit", "vuelve más tarde", "come back later"))


def prompt_hoja():
    p = ("Crea una imagen: hoja de personajes (character sheet) con las dos personas de la foto adjunta, "
         "de cuerpo entero y de frente, una al lado de la otra, sobre fondo claro y neutro. Mantén su "
         "parecido real con la foto (cara, pelo, barba, ojos). "
         + " ".join(PERSONAJES.values())
         + " Ropa actual y cómoda: ella vaqueros, zapatillas, camiseta y chaqueta ligera; él vaqueros, "
           "zapatillas, sudadera con capucha y mochila. Estilo: " + ESTILO_HOJA
         + " Sin ningún texto ni letras en la imagen.")
    return " ".join(p.split())


def prompt_carta(carta, meta):
    arte = carta["arte"]
    salen = [n for n in meta["personajes"] if n in arte]
    p = ("Crea una imagen vertical con proporción 2:3 para una carta de juego de escape room. " + arte)
    if salen:
        p += (" Personajes (mantén exactamente su cara, pelo, barba y rasgos como en la hoja de personajes adjunta, "
              "pero con la ropa que se indica aquí, no con la de la hoja): "
              + " ".join(meta["personajes"][n] for n in salen))
    p += " " + meta["estilo"] + " Muy importante: no escribas ningún texto, letra ni número dentro de la imagen."
    return " ".join(p.split())


def hacer_hoja(chat, foto, forzar):
    if HOJA.exists() and not forzar:
        print(f"La hoja ya existe: {HOJA}")
        return True
    if not foto or not all(Path(f).exists() for f in foto):
        sys.exit("Para la hoja necesito --foto RUTA (foto de Cristina y Alberto).")
    print("Hoja de personajes (con la foto)...")
    chat.nuevo_chat()
    if not all([chat.adjuntar(f) for f in foto]):
        return False
    chat.enviar(prompt_hoja())
    src = chat.esperar_imagen()
    if not src:
        print("  ! no salió la hoja" + (" (límite de imágenes)" if chat.hay_limite() else ""))
        return False
    chat.descargar(src, HOJA)
    print(f"  ok -> {HOJA}")
    return True


def hacer_juego(chat, carpeta, solo, forzar):
    base = RAIZ / carpeta
    datos = json.loads((base / "cartas.json").read_text(encoding="utf-8"))
    meta = datos.pop("_meta")
    ids = sorted(datos, key=orden)
    if solo:
        malas = [i for i in solo if i not in datos]
        if malas:
            sys.exit(f"Cartas que no existen en {carpeta}: {malas}")
        ids = [i for i in ids if i in solo]
    arte = base / "arte"
    pend = [i for i in ids if forzar or not (arte / f"{i}.png").exists()]
    print(f"\n== {carpeta}: {len(pend)} cartas por hacer ==")
    hechas, en_chat = 0, CARTAS_POR_CHAT
    for n, i in enumerate(pend, 1):
        if en_chat >= CARTAS_POR_CHAT:
            chat.nuevo_chat()
            en_chat = 0
            adjunta = chat.adjuntar(HOJA)
        texto = prompt_carta(datos[i], meta)
        if en_chat == 0 and adjunta:
            texto = ("Usa a los personajes de la hoja adjunta como referencia fija en todas las imágenes "
                     "que te pida a partir de ahora. " + texto)
        print(f"[{n}/{len(pend)}] Carta {i}: {datos[i]['titulo']}")
        chat.enviar(texto)
        src = chat.esperar_imagen()
        en_chat += 1
        if not src:
            if chat.hay_limite():
                print("  ! ChatGPT indica límite de imágenes. Relanza más tarde.")
                return hechas, False
            print("  x no salió imagen, paso a la siguiente")
            continue
        try:
            chat.descargar(src, arte / f"{i}.png")
        except Exception as e:  # noqa: BLE001
            print(f"  x no pude guardarla: {e}")
            continue
        hechas += 1
        print(f"  ok -> {carpeta}/arte/{i}.png")
        time.sleep(random.uniform(8, 15))
    return hechas, True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("juegos", nargs="*", help="carpetas de juego, p. ej. Aventuras-CA/Egipto")
    ap.add_argument("--foto", nargs="+", help="una o varias fotos de Cristina y Alberto (solo para la hoja)")
    ap.add_argument("--hoja", action="store_true", help="generar la hoja de personajes")
    ap.add_argument("--solo", nargs="*")
    ap.add_argument("--forzar", action="store_true")
    ap.add_argument("--conectar", action="store_true", help="usar el Chrome ya abierto con abrir_chrome_chatgpt.ps1 (puerto 9222)")
    args = ap.parse_args()
    if not args.juegos and not args.hoja:
        ap.error("indica --hoja y/o alguna carpeta de juego")

    chat = Chat(9222 if args.conectar else None)
    try:
        if args.hoja or not HOJA.exists():
            if not hacer_hoja(chat, args.foto, args.forzar and args.hoja):
                sys.exit("Sin hoja de personajes no sigo.")
        for carpeta in args.juegos:
            hechas, seguir = hacer_juego(chat, carpeta, args.solo, args.forzar)
            print(f"{carpeta}: {hechas} imágenes nuevas")
            if hechas:
                subprocess.run([sys.executable, str(RAIZ / "herramientas" / "preparar_imagenes.py"), carpeta], cwd=RAIZ)
            if not seguir:
                break
    finally:
        if not args.conectar:
            chat.d.quit()


if __name__ == "__main__":
    main()

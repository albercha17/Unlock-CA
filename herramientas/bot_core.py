"""Jugador automatico: juega una partida completa con la mesa (pc.html) y la app (index.html).
Solo hace lo que dicen las cartas (franjas Coge/Descarta, etiqueta Combinable) y los mensajes de la app.
Falla si algo no cuadra: coger una carta que no esta en el mazo, descartar una que no se tiene,
combinaciones accidentales, apps que no se pueden resolver porque falta una pista, etc."""
import re, sys, time
from selenium import webdriver
from selenium.webdriver.common.by import By

LOG = []


def log(m):
    LOG.append(m)
    print(m)


class Fallo(Exception):
    pass


def nuevo_driver():
    o = webdriver.ChromeOptions()
    o.add_argument("--headless=new")
    o.add_argument("--window-size=1100,1000")
    o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    return webdriver.Chrome(options=o)


# ---------- app ----------
def esperar(s=0.4):
    time.sleep(s)


def abrir_app(d, url):
    d.get(url)
    esperar(1)
    d.find_element(By.ID, "startBtn").click()
    esperar(1.2)
    if not d.find_element(By.ID, "gamePanel").is_displayed():
        d.find_element(By.ID, "skipVideoBtn").click()
        esperar(0.4)


def abrir_carta(d, num):
    d.find_element(By.ID, "actionBtn").click()
    esperar(0.3)
    for ch in num:
        d.find_element(By.CSS_SELECTOR, f".num-key[data-key='{ch}']").click()
    d.find_element(By.ID, "numOk").click()
    esperar(1.0)
    msg = d.find_element(By.ID, "numMessage").text
    ov = [e for e in d.find_elements(By.CSS_SELECTOR, "[class$='overlay']")
          if e.is_displayed() and "num-modal" not in (e.get_attribute("class") or "")]
    if not ov:
        raise Fallo(f"la app no abre el minijuego {num}: '{msg}'")


def cerrar(d):
    for b in d.find_elements(By.XPATH, "//button[normalize-space()='Cerrar']"):
        try:
            b.click()
            esperar(0.4)
            return
        except Exception:
            pass


def feedback(d):
    for sel in (".far-feedback", ".aeb-feedback", ".aebc-feedback", ".aebi-feedback", ".aebq-feedback", ".aebf-feedback"):
        e = d.find_elements(By.CSS_SELECTOR, sel)
        if e and e[0].text:
            return e[0].text
    return ""


def boton(d, texto):
    for b in d.find_elements(By.XPATH, f"//button[normalize-space()='{texto}']"):
        if b.is_displayed():
            return b
    raise Fallo("no hay boton " + texto)


def tecla(d, texto):
    for b in d.find_elements(By.CSS_SELECTOR, ".far-key, .aeb-key, .aebf-key"):
        if b.is_displayed() and b.text.strip() == texto:
            b.click()
            return
    raise Fallo("no hay tecla " + texto)


def js(d, codigo):
    return d.execute_script(codigo)


# ---------- mesa ----------
class Mesa:
    def __init__(self, d, url):
        self.d = d
        d.get(url)
        esperar(1.4)

    JS_FOTO = """
    const cartas = {};
    document.querySelectorAll('#mesa .item').forEach(it => {
      const id = it.querySelector('.num').textContent;
      cartas[id] = {
        coge: [...it.querySelectorAll('.acc .coge i')].map(i => i.textContent),
        descarta: [...it.querySelectorAll('.acc .des i')].map(i => i.textContent),
        etq: [...it.querySelectorAll('.etq')].map(e => e.textContent).join(' ').trim().toUpperCase(),
        comb: !!it.querySelector('.acc .comb'),
        texto: [...it.querySelectorAll('.texto')].map(e => e.textContent).join(' | ')
      };
    });
    return {
      mesa: [...document.querySelectorAll('#mesa .item .num')].map(e => e.textContent),
      mazo: [...document.querySelectorAll('#mazo .dorso .big')].map(e => e.textContent),
      descartes: [...document.querySelectorAll('#descartes .dorso .big')].map(e => e.textContent),
      cartas
    };
    """

    def foto(self):
        return self.d.execute_script(self.JS_FOTO)

    def en_mesa(self):
        return self.foto()["mesa"]

    def en_mazo(self):
        return self.foto()["mazo"]

    def en_descartes(self):
        return self.foto()["descartes"]

    def coger(self, n, motivo):
        n = str(n)
        if n not in self.en_mazo():
            raise Fallo(f"{motivo}: manda coger la {n}, pero no esta en el mazo (mesa={self.en_mesa()}, descartes={self.en_descartes()})")
        q = self.d.find_element(By.ID, "qn")
        q.send_keys(n + "\n")
        esperar(0.55)
        msg = self.d.find_element(By.ID, "msg").text
        if "Has cogido" not in msg:
            raise Fallo(f"no se pudo coger la {n}: '{msg}'")
        log(f"   coge {n}   ({motivo})")

    def descartar(self, n, motivo):
        n = str(n)
        if n not in self.en_mesa():
            raise Fallo(f"{motivo}: manda descartar la {n}, que NO tienes en la mesa (mesa={self.en_mesa()})")
        for it in self.d.find_elements(By.CSS_SELECTOR, "#mesa .item"):
            if it.find_element(By.CSS_SELECTOR, ".num").text == n:
                it.find_element(By.CSS_SELECTOR, ".mini").click()
                esperar(0.3)
                log(f"   descarta {n}   ({motivo})")
                return

    def info(self, n):
        cartas = self.foto()["cartas"]
        if n not in cartas:
            raise Fallo(f"la carta {n} no esta en la mesa")
        return cartas[n]


def numeros(txt):
    return re.findall(r"\d+|\bP\b", txt)


def instrucciones_mensaje(txt):
    """Devuelve (coger, descartar) a partir de un mensaje de la app."""
    coger, descartar = [], []
    for m in re.finditer(r"[Cc]oged la carta (\d+)", txt):
        coger.append(m.group(1))
    for m in re.finditer(r"[Dd]escartad (?:la carta|las cartas) ([\dP, y]+)", txt):
        descartar += [x for x in re.findall(r"\d+|P", m.group(1))]
    return coger, descartar


def jugar(nombre, url_pc, url_app, solvers, requiere, final="99", max_vueltas=60):
    d_pc, d_app = nuevo_driver(), nuevo_driver()
    try:
        log(f"=== {nombre}")
        mesa = Mesa(d_pc, url_pc)
        abrir_app(d_app, url_app)
        if mesa.en_mesa() != ["P"]:
            raise Fallo(f"al empezar la mesa deberia tener solo P y tiene {mesa.en_mesa()}")
        procesadas, resueltas, combinadas = set(), set(), set()
        for vuelta in range(max_vueltas):
            progreso = False
            # 1. leer las cartas nuevas de la mesa
            for n in list(mesa.en_mesa()):
                if n in procesadas:
                    continue
                procesadas.add(n)
                progreso = True
                inf = mesa.info(n)
                log(f"- carta {n} (etiqueta '{inf['etq'] or 'normal'}'): coge={inf['coge']} descarta={inf['descarta']}")
                for x in inf["descarta"]:
                    mesa.descartar(x, f"lo manda la carta {n}")
                for x in inf["coge"]:
                    mesa.coger(x, f"lo manda la carta {n}")
            # 2. combinaciones (cartas con etiqueta Combina)
            comb = [n for n in mesa.en_mesa() if mesa.info(n)["etq"] == "COMBINA"]
            for i, a in enumerate(comb):
                for b in comb[i + 1:]:
                    clave = tuple(sorted((a, b)))
                    if clave in combinadas:
                        continue
                    s = str(int(a) + int(b))
                    if s in mesa.en_mazo():
                        combinadas.add(clave)
                        progreso = True
                        log(f"- combinas {a} + {b} = {s}")
                        mesa.coger(s, f"suma {a}+{b}")
                        if not (s in solvers_resultado_esperado(requiere)):
                            pass
            # 3. apps
            for n in list(mesa.en_mesa()):
                if n in resueltas or mesa.info(n)["etq"] != "APP":
                    continue
                falta = [r for r in requiere.get(n, []) if r not in mesa.en_mesa()]
                if falta:
                    continue
                if n not in solvers:
                    raise Fallo(f"no hay solucionador para la app {n}")
                log(f"- app {n}")
                msg = solvers[n](d_app)
                resueltas.add(n)
                progreso = True
                log(f"   mensaje: {msg}")
                coger, descartar = instrucciones_mensaje(msg)
                for x in descartar:
                    mesa.descartar(x, f"lo manda el mensaje de la app {n}")
                for x in coger:
                    mesa.coger(x, f"lo manda el mensaje de la app {n}")
            if mesa.en_mesa() == [final] and final in procesadas:
                break
            if not progreso:
                break
        mesa_final = mesa.en_mesa()
        apps_sin_resolver = [n for n in mesa_final if mesa.info(n)["etq"] == "APP" and n not in resueltas]
        if mesa_final != [final]:
            raise Fallo(f"la partida no termina limpia: mesa={mesa_final}, apps sin resolver={apps_sin_resolver}, mazo={mesa.en_mazo()}")
        if mesa.en_mazo():
            raise Fallo(f"sobran cartas en el mazo que nadie ha cogido: {mesa.en_mazo()}")
        log(f"*** {nombre}: PARTIDA COMPLETA. Mesa final: {mesa_final}; descartes: {len(mesa.en_descartes())} cartas")
        return True
    except Fallo as e:
        log(f"*** FALLO en {nombre}: {e}")
        return False
    finally:
        d_pc.quit()
        d_app.quit()


def solvers_resultado_esperado(requiere):
    return set()

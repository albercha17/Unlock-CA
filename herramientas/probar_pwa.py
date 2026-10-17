"""Prueba la parte de app instalable y cuentas SIN depender de internet ni de Supabase real.

Arranca su propio servidor local (y lo cierra al acabar) y comprueba con Chrome headless:
  1. menús: dificultad, duración y nº de cartas visibles en todas las tarjetas;
  2. service worker: se registra, deja el cascarón en caché y los menús abren SIN conexión;
  3. juego sin conexión: el botón «Descargar para jugar sin conexión» guarda el juego y después se abre sin red;
  4. cuentas (con un Supabase simulado): login desde el menú, guardar la partida al terminar, «Mis partidas» y marcas en el menú;
  5. sin sesión: la partida se guarda en el dispositivo, se ofrece iniciar sesión y se sincroniza al entrar.
Uso (desde la raíz del repo):  python herramientas/probar_pwa.py [juego]     (por defecto: dinosaurios)
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

PUERTO = 8895
JUEGO = sys.argv[1] if len(sys.argv) > 1 else "dinosaurios"
RUTA = "juegos/el-faro/" if JUEGO == "faro" else f"juegos/aventuras-ca/{JUEGO}/"
URL = f"http://127.0.0.1:{PUERTO}/"

FAKE = """
window.supabase = { createClient: function () {
  var leer = function (k, d) { try { return JSON.parse(localStorage.getItem(k) || d); } catch (e) { return JSON.parse(d); } };
  var oyentes = [];
  var cl = {
    auth: {
      onAuthStateChange: function (fn) { oyentes.push(fn); },
      getSession: function () { return Promise.resolve({ data: { session: leer('fake-ses', 'null') } }); },
      signInWithPassword: function (o) {
        if (o.password === 'mala1234') return Promise.resolve({ error: { message: 'Invalid login credentials' } });
        var ses = { user: { email: o.email, id: 'u1' } }; localStorage.setItem('fake-ses', JSON.stringify(ses));
        setTimeout(function () { oyentes.forEach(function (f) { f('SIGNED_IN', ses); }); }, 10);
        return Promise.resolve({ data: { user: ses.user, session: ses } });
      },
      signUp: function (o) { return Promise.resolve({ data: { user: { email: o.email }, session: null } }); },
      signOut: function () { localStorage.removeItem('fake-ses'); setTimeout(function () { oyentes.forEach(function (f) { f('SIGNED_OUT', null); }); }, 10); return Promise.resolve({}); }
    },
    from: function () { return {
      upsert: function (filas) { var todas = leer('fake-filas', '[]'); filas.forEach(function (f) { if (!todas.some(function (x) { return x.cliente_id === f.cliente_id; })) todas.push(f); }); localStorage.setItem('fake-filas', JSON.stringify(todas)); return Promise.resolve({ error: null }); },
      select: function () { return { order: function () { return { limit: function () { return Promise.resolve({ data: leer('fake-filas', '[]').slice().reverse(), error: null }); } }; } }; }
    }; }
  };
  return cl;
} };
"""


class Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


class Servidor(http.server.ThreadingHTTPServer):
    def handle_error(self, request, client_address):  # conexiones cortadas por Chrome al cambiar de página: ruido sin importancia
        pass


def servidor():
    h = functools.partial(Silencioso, directory=os.getcwd())
    s = Servidor(("127.0.0.1", PUERTO), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


fallos = []


def ok(cond, msg):
    print(("OK    " if cond else "FALLO ") + msg, flush=True)
    if not cond:
        fallos.append(msg)


def esperar(fn, seg=15, paso=0.3):
    t0 = time.time()
    while time.time() - t0 < seg:
        try:
            v = fn()
            if v:
                return v
        except Exception:
            pass
        time.sleep(paso)
    return None


def nuevo(simulado=True):
    o = webdriver.ChromeOptions()
    o.add_argument("--headless=new")
    o.add_argument("--window-size=420,900")
    o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    d = webdriver.Chrome(options=o)
    if simulado:
        d.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": FAKE})
    return d


def sin_red(d, si):
    d.execute_cdp_cmd("Network.enable", {})
    d.execute_cdp_cmd("Network.emulateNetworkConditions", {"offline": si, "latency": 0, "downloadThroughput": -1, "uploadThroughput": -1})


def empezar_y_terminar(d):
    d.get(URL + RUTA + "index.html")
    esperar(lambda: d.find_element(By.ID, "startBtn").is_displayed())
    d.find_element(By.ID, "startBtn").click()
    time.sleep(1.2)
    if not d.find_element(By.ID, "gamePanel").is_displayed():
        d.find_element(By.ID, "skipVideoBtn").click()
    time.sleep(0.5)
    d.find_element(By.ID, "actionBtn").click()
    time.sleep(0.4)
    for ch in "99":
        d.find_element(By.CSS_SELECTOR, f".num-key[data-key='{ch}']").click()
    d.find_element(By.ID, "numOk").click()
    esperar(lambda: d.find_element(By.ID, "finalPanel").is_displayed())


def main():
    srv = servidor()
    d = nuevo()
    try:
        # ---------- 1. menús
        d.get(URL + "index.html")
        esperar(lambda: len(d.find_elements(By.CSS_SELECTOR, ".dif-fila")) >= 2)
        filas = d.find_elements(By.CSS_SELECTOR, ".dif-fila")
        ok(len(filas) == 2, f"menú principal: dificultad visible en las 2 tarjetas ({len(filas)})")
        d.get(URL + "juegos/aventuras-ca/index.html")
        esperar(lambda: len(d.find_elements(By.CSS_SELECTOR, ".dif-fila")) >= 6)
        filas = d.find_elements(By.CSS_SELECTOR, ".dif-fila")
        ok(len(filas) == 7, f"menú de aventuras: dificultad, minutos y cartas en las 7 tarjetas ({len(filas)})")
        ok(all("min" in f.text and "cartas" in f.text for f in filas), "cada fila indica minutos y número de cartas")
        # ---------- 2. service worker
        d.get(URL + "index.html")
        reg = esperar(lambda: d.execute_async_script("const h=arguments[arguments.length-1]; navigator.serviceWorker.ready.then(r=>h(!!r.active)).catch(()=>h(false));"), 20)
        ok(bool(reg), "el service worker se registra y queda activo")
        time.sleep(2)
        n = d.execute_async_script("const h=arguments[arguments.length-1]; caches.keys().then(async k=>{let t=0; for(const x of k){t+=(await (await caches.open(x)).keys()).length;} h(t);});")
        ok(n >= 15, f"el cascarón está en la caché ({n} ficheros)")
        d.get(URL + "index.html")  # ya controlado por el SW
        time.sleep(1.5)
        sin_red(d, True)
        d.get(URL + "index.html")
        ok("Unlock" in d.title and len(d.find_elements(By.CSS_SELECTOR, ".option")) == 2, "el menú principal abre SIN conexión")
        d.get(URL + "perfil.html")
        ok("Mis partidas" in d.title, "«Mis partidas» abre sin conexión")
        d.get(URL + "instalar.html")
        ok("Instalar" in d.title, "la página de instalación abre sin conexión")
        sin_red(d, False)
        # ---------- 3. juego sin conexión
        d.get(URL + RUTA + "index.html")
        esperar(lambda: d.find_element(By.ID, "offlineBtn").is_displayed(), 15)
        ok(d.find_element(By.ID, "offlineBtn").is_displayed(), "el juego muestra el botón de descarga sin conexión")
        d.find_element(By.ID, "offlineBtn").click()
        listo = esperar(lambda: "Listo" in d.find_element(By.ID, "offlineEstado").text, 90, 1)
        ok(bool(listo), "la descarga del juego termina sin fallos: " + d.find_element(By.ID, "offlineEstado").text)
        d.get(URL + "index.html")
        time.sleep(1)
        sin_red(d, True)
        d.get(URL + RUTA + "index.html")
        esperar(lambda: d.find_element(By.ID, "startBtn").is_displayed(), 10)
        ok(d.find_element(By.ID, "startBtn").is_displayed(), "el juego abre SIN conexión")
        d.find_element(By.ID, "startBtn").click()
        time.sleep(1.2)
        if not d.find_element(By.ID, "gamePanel").is_displayed():
            d.find_element(By.ID, "skipVideoBtn").click()
        d.find_element(By.ID, "hintBtn").click()
        time.sleep(0.4)
        for ch in "P":
            d.find_element(By.CSS_SELECTOR, f".num-key[data-key='{ch}']").click()
        d.find_element(By.ID, "numOk").click()
        time.sleep(1.5)
        ok(len(d.find_elements(By.CSS_SELECTOR, ".pst-root")) == 1, "sin conexión también funcionan las pistas")
        sin_red(d, False)
        d.execute_script("localStorage.clear()")

        # ---------- 4/5. cuentas
        # (a) sin sesión: se guarda en el dispositivo y ofrece iniciar sesión
        empezar_y_terminar(d)
        est = esperar(lambda: d.find_element(By.ID, "guardadoEstado").text, 10)
        ok("este dispositivo" in (est or ""), "sin sesión: la partida se guarda en el dispositivo (" + str(est) + ")")
        ok(d.find_element(By.ID, "guardarCuentaBtn").is_displayed(), "sin sesión: se ofrece iniciar sesión para guardarla")
        # (b) iniciar sesión desde ahí y sincronizar
        d.find_element(By.ID, "guardarCuentaBtn").click()
        esperar(lambda: d.find_elements(By.CSS_SELECTOR, ".cac-caja"))
        f = d.find_element(By.CSS_SELECTOR, ".cac-caja form")
        f.find_element(By.NAME, "email").clear()
        f.find_element(By.NAME, "email").send_keys("cristina@ejemplo.es")
        f.find_element(By.NAME, "clave").send_keys("mala1234")
        d.find_element(By.CSS_SELECTOR, ".cac-primario").click()
        esperar(lambda: "incorrectos" in d.find_element(By.CSS_SELECTOR, ".cac-msg").text)
        ok("incorrectos" in d.find_element(By.CSS_SELECTOR, ".cac-msg").text, "una contraseña mala da un error claro")
        f.find_element(By.NAME, "clave").clear()
        f.find_element(By.NAME, "clave").send_keys("buena1234")
        d.find_element(By.CSS_SELECTOR, ".cac-primario").click()
        guardada = esperar(lambda: "tu cuenta" in d.find_element(By.ID, "guardadoEstado").text, 10)
        ok(bool(guardada), "al entrar, la partida se sube a la cuenta: " + d.find_element(By.ID, "guardadoEstado").text)
        filas = d.execute_script("return JSON.parse(localStorage.getItem('fake-filas')||'[]')")
        ok(len(filas) == 1 and filas[0]["juego"] == JUEGO and filas[0]["tiempo_seg"] >= 0, f"la fila subida lleva el juego y el tiempo ({filas[:1]})")
        # (c) con sesión: segunda partida directa a la cuenta
        empezar_y_terminar(d)
        est = esperar(lambda: "tu cuenta" in d.find_element(By.ID, "guardadoEstado").text, 10)
        ok(bool(est), "con sesión: la partida se guarda directamente en la cuenta")
        # (d) Mis partidas y marcas en el menú
        d.get(URL + "perfil.html")
        esperar(lambda: len(d.find_elements(By.CSS_SELECTOR, "table tbody tr")) >= 2)
        ok(len(d.find_elements(By.CSS_SELECTOR, "table tbody tr")) == 2, "«Mis partidas» lista las 2 partidas")
        ok("cristina@ejemplo.es" in d.find_element(By.ID, "sub").text, "«Mis partidas» muestra la sesión iniciada")
        ganados = d.find_elements(By.CSS_SELECTOR, ".logro.on")
        ok(len(ganados) >= 3 and any("Primera aventura" in g.text for g in ganados), f"«Mis partidas» muestra logros ganados ({len(ganados)})")
        d.get(URL + "juegos/aventuras-ca/index.html" if JUEGO != "faro" else URL + "index.html")
        esperar(lambda: d.find_elements(By.CSS_SELECTOR, ".hecha"))
        ok(len(d.find_elements(By.CSS_SELECTOR, ".hecha")) >= 1 and "Completada" in d.find_element(By.CSS_SELECTOR, ".hecha").text, "el menú marca la aventura como completada con su mejor tiempo")
        # (e) cerrar sesión desde el menú
        d.find_element(By.CSS_SELECTOR, ".cac-btn.suave").click()
        esperar(lambda: "Iniciar sesión" in d.find_element(By.CSS_SELECTOR, ".cac-widget").text or "Entrar" in d.find_element(By.CSS_SELECTOR, ".cac-widget").text)
        ok("Mis partidas" not in d.find_element(By.CSS_SELECTOR, ".cac-widget").text, "cerrar sesión devuelve el botón de entrar")
        # ---------- 6. app nativa: barra inferior, ajustes, arranque y gestos
        for pag, activa in (("index.html", "Inicio"), ("juegos/aventuras-ca/index.html", "Aventuras"), ("perfil.html", "Partidas"), ("ajustes.html", "Ajustes")):
            d.get(URL + pag)
            esperar(lambda: d.find_elements(By.CSS_SELECTOR, ".ca-barra .ca-tab"))
            tabs = d.find_elements(By.CSS_SELECTOR, ".ca-barra .ca-tab")
            act = [t.text for t in d.find_elements(By.CSS_SELECTOR, ".ca-tab[aria-current='page']")]
            ok(len(tabs) == 4 and act == [activa], f"barra inferior en {pag}: 4 pestañas y activa «{activa}» ({act})")
        d.get(URL + "ajustes.html")
        esperar(lambda: d.find_elements(By.ID, "contraste"))
        d.execute_script("document.getElementById('contraste').click(); document.getElementById('movimiento').click(); document.querySelector(\".tam button[data-t='1.25']\").click();")
        time.sleep(0.4)
        d.get(URL + RUTA + "index.html")
        esperar(lambda: d.find_element(By.ID, "startBtn").is_displayed())
        h = d.execute_script("const h=document.documentElement; return [h.getAttribute('data-contraste'), h.getAttribute('data-movimiento'), h.style.zoom]")
        ok(h == ["alto", "reducido", "1.25"], f"los ajustes (contraste, movimiento, texto) se aplican en el juego ({h})")
        d.get(URL + "ajustes.html")
        esperar(lambda: d.find_elements(By.ID, "contraste"))
        d.execute_script("document.getElementById('contraste').click(); document.getElementById('movimiento').click(); document.querySelector(\".tam button[data-t='1']\").click();")
        time.sleep(0.3)
        d.get(URL + "index.html?splash")
        visto = esperar(lambda: d.find_elements(By.ID, "ca-splash"), 5, 0.1)
        ok(bool(visto), "la pantalla de arranque aparece al abrir la app")
        gone = esperar(lambda: not d.find_elements(By.ID, "ca-splash"), 8)
        ok(bool(gone), "y desaparece sola")
        # gesto: deslizar hacia abajo cierra el cuaderno
        d.execute_cdp_cmd("Emulation.setTouchEmulationEnabled", {"enabled": True})
        d.get(URL + RUTA + "index.html")
        esperar(lambda: d.find_element(By.ID, "startBtn").is_displayed())
        d.find_element(By.ID, "startBtn").click()
        time.sleep(1.2)
        if not d.find_element(By.ID, "gamePanel").is_displayed():
            d.find_element(By.ID, "skipVideoBtn").click()
        d.find_element(By.ID, "notebookBtn").click()
        time.sleep(0.6)
        r = d.execute_script("const r=document.querySelector('.cuaderno-caja').getBoundingClientRect(); return [r.left+r.width/2, r.top+20]")
        for tipo, y in (("touchStart", r[1]), ("touchMove", r[1] + 60), ("touchMove", r[1] + 160), ("touchEnd", r[1] + 160)):
            d.execute_cdp_cmd("Input.dispatchTouchEvent", {"type": tipo, "touchPoints": [] if tipo == "touchEnd" else [{"x": r[0], "y": y}]})
            time.sleep(0.05)
        time.sleep(0.6)
        cerrado = d.execute_script("return !document.getElementById('cuaderno').classList.contains('abierto')")
        ok(cerrado, "deslizar hacia abajo cierra el cuaderno")
        errores = [e for e in d.get_log("browser") if e["level"] == "SEVERE" and "favicon" not in e["message"] and "fonts.g" not in e["message"] and "ERR_INTERNET_DISCONNECTED" not in e["message"] and "net::ERR_FAILED" not in e["message"] and "videoInicial" not in e["message"]]
        ok(not errores, "sin errores de consola " + str([e["message"][:120] for e in errores[:3]]))
    finally:
        d.quit()
        srv.shutdown()
    print("RESULTADO:", "OK" if not fallos else f"{len(fallos)} fallos")
    sys.exit(0 if not fallos else 1)


if __name__ == "__main__":
    main()

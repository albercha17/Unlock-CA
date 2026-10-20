"""Prueba los accesos por cuenta (supabase/unlock_accesos.sql, assets/js/accesos.js, tienda/accesos.html) SIN Supabase real.

El servidor de prueba sustituye assets/js/vendor/supabase.js por uno falso que guarda las tablas en localStorage
e imita el RLS (cada cuenta solo lee sus accesos; solo el administrador escribe). Comprueba con Chrome headless:
  1. sin sesión: ni el menú ni el hub enseñan los juegos de Cristina y Alberto; sale la bienvenida para entrar;
  2. un cliente ve solo sus juegos, con su portada personalizada, su enlace y sus protagonistas (también en el hub);
  3. sin conexión, el cliente sigue viendo sus juegos (copia en el dispositivo);
  4. un cliente sin juegos ve un aviso claro;
  5. el administrador ve todo; «ver como» enseña lo que ve un cliente y se puede volver;
  6. el panel tienda/accesos.html: rechaza a quien no es administrador, se rellena desde un pedido, da acceso
     (personalizado para las aventuras del pack, normal para el resto), lista por correo y quita accesos.
Uso (desde la raíz del repo):  python herramientas/probar_accesos.py
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

sys.stdout.reconfigure(encoding="utf-8")
PUERTO = 8897
URL = f"http://127.0.0.1:{PUERTO}/"
ADMIN = "albercha17@gmail.com"

FAKE = r"""
(function () {
  var leer = function (k, d) { try { return JSON.parse(localStorage.getItem(k) || d); } catch (e) { return JSON.parse(d); } };
  var ADMIN = '__ADMIN__';
  window.supabase = { createClient: function (url, key, op) {
    var K = 'fake-ses-' + ((op && op.auth && op.auth.storageKey) || 'x');
    var oyentes = [];
    var ses = function () { return leer(K, 'null'); };
    var correo = function () { var s = ses(); return s ? s.user.email.toLowerCase() : ''; };
    var esAdmin = function () { return correo() === ADMIN; };
    function Q(t) {
      var st = { f: [], op: 'select', rows: null };
      var q = {
        select: function () { return q; }, order: function () { return q; }, limit: function () { return q; },
        eq: function (k, v) { st.f.push([k, v]); return q; },
        upsert: function (rows) { st.op = 'upsert'; st.rows = rows; return q; },
        delete: function () { st.op = 'delete'; return q; },
        then: function (a, b) { return Promise.resolve().then(run).then(a, b); }
      };
      function run() {
        var clave = 'fake-' + t;
        var todas = leer(clave, '[]');
        if (t === 'unlock_accesos') {
          if (!ses()) return { data: null, error: { message: 'JWT' } };
          if (st.op !== 'select' && !esAdmin()) return { data: null, error: { message: 'new row violates row-level security policy' } };
          if (st.op === 'upsert') {
            st.rows.forEach(function (r) {
              var i = todas.findIndex(function (x) { return x.email === r.email && x.juego === r.juego && x.url === r.url; });
              var fila = Object.assign({ id: 'a' + Math.random().toString(36).slice(2, 9), creado: new Date().toISOString() }, i >= 0 ? todas[i] : {}, r);
              if (i >= 0) todas[i] = fila; else todas.push(fila);
            });
            localStorage.setItem(clave, JSON.stringify(todas));
            return { data: null, error: null };
          }
          var vis = todas.filter(function (x) { return esAdmin() || x.email === correo(); })
            .filter(function (x) { return st.f.every(function (f) { return x[f[0]] === f[1]; }); });
          if (st.op === 'delete') {
            localStorage.setItem(clave, JSON.stringify(todas.filter(function (x) { return vis.indexOf(x) < 0; })));
            return { data: null, error: null };
          }
          return { data: vis, error: null };
        }
        if (st.op === 'upsert') { st.rows.forEach(function (r) { todas.push(r); }); localStorage.setItem(clave, JSON.stringify(todas)); return { error: null }; }
        return { data: todas, error: null };
      }
      return q;
    }
    return {
      auth: {
        onAuthStateChange: function (fn) { oyentes.push(fn); },
        getSession: function () { return Promise.resolve({ data: { session: ses() } }); },
        signInWithPassword: function (o) {
          var s = { user: { email: o.email, id: 'u-' + o.email } }; localStorage.setItem(K, JSON.stringify(s));
          setTimeout(function () { oyentes.forEach(function (f) { f('SIGNED_IN', s); }); }, 10);
          return Promise.resolve({ data: { user: s.user, session: s }, error: null });
        },
        signOut: function () { localStorage.removeItem(K); setTimeout(function () { oyentes.forEach(function (f) { f('SIGNED_OUT', null); }); }, 10); return Promise.resolve({}); }
      },
      rpc: function () {
        if (localStorage.getItem('fake-romper')) return Promise.resolve({ data: null, error: { message: 'Failed to fetch' } });  // «sin red»
        return Promise.resolve({ data: esAdmin(), error: null });
      },
      from: Q
    };
  } };
})();
""".replace("__ADMIN__", ADMIN)


class Manejador(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path.split("?")[0].endswith("assets/js/vendor/supabase.js"):
            datos = FAKE.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/javascript; charset=utf-8")
            self.send_header("Content-Length", str(len(datos)))
            self.end_headers()
            self.wfile.write(datos)
            return
        super().do_GET()


class Servidor(http.server.ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        pass


fallos = []


def ok(cond, msg):
    print(("OK    " if cond else "FALLO ") + msg, flush=True)
    if not cond:
        fallos.append(msg)


def esperar(fn, seg=10, paso=0.2):
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


def sesion(d, email, clave="ca-auth"):
    d.execute_script(f"localStorage.setItem('fake-ses-{clave}', JSON.stringify({{user:{{email:{json.dumps(email)},id:'u'}}}}))")


def visibles(d, sel):
    return [e for e in d.find_elements(By.CSS_SELECTOR, sel) if e.is_displayed()]


def main():
    srv = Servidor(("127.0.0.1", PUERTO), functools.partial(Manejador, directory=os.getcwd()))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    o = webdriver.ChromeOptions()
    o.add_argument("--headless=new")
    o.add_argument("--window-size=420,900")
    o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    d = webdriver.Chrome(options=o)
    try:
        d.get(URL + "instalar.html")
        d.execute_script("localStorage.clear(); sessionStorage.clear()")
        personal = URL + "juegos/aventuras-ca/egipto/index.html?pack=bea"
        portada = URL + "juegos/aventuras-ca/marte/img/P.jpg"
        accesos = [
            {"id": "a1", "email": "bea@ejemplo.es", "juego": "egipto", "url": personal, "portada": portada, "quienes": "Bea y Rubén", "creado": "2026-10-01"},
            {"id": "a2", "email": "bea@ejemplo.es", "juego": "faro", "url": "", "portada": "", "quienes": "Bea y Rubén", "creado": "2026-10-02"},
            {"id": "a3", "email": "otro@ejemplo.es", "juego": "marte", "url": "", "portada": "", "quienes": "", "creado": "2026-10-03"},
        ]
        d.execute_script(f"localStorage.setItem('fake-unlock_accesos', {json.dumps(json.dumps(accesos))})")

        # ---------- 1. sin sesión
        d.get(URL + "index.html")
        esperar(lambda: visibles(d, "#mis .mis-vacio"))
        ok(bool(visibles(d, "#mis .mis-vacio")) and "Entra con tu cuenta" in d.find_element(By.ID, "mis").text, "sin sesión: el menú pide entrar")
        ok(not d.find_element(By.ID, "todo").is_displayed(), "sin sesión: el menú no enseña los juegos de Cristina y Alberto")
        d.get(URL + "juegos/aventuras-ca/index.html")
        esperar(lambda: visibles(d, "#mis .mis-vacio"))
        ok(bool(visibles(d, "#mis .mis-vacio")) and not d.find_element(By.ID, "todo").is_displayed(), "sin sesión: el hub de aventuras tampoco")
        d.find_element(By.CSS_SELECTOR, "[data-entrar]").click()
        ok(bool(esperar(lambda: d.find_elements(By.CSS_SELECTOR, ".cac-caja"))), "el botón de la bienvenida abre la ventana de entrar")

        # ---------- 2. cliente con juegos
        sesion(d, "bea@ejemplo.es")
        d.get(URL + "index.html")
        esperar(lambda: visibles(d, "#mis .option"))
        tarjetas = visibles(d, "#mis .option")
        ok(len(tarjetas) == 2 and not d.find_element(By.ID, "todo").is_displayed(), f"el cliente ve solo sus 2 juegos ({len(tarjetas)})")
        hrefs = [t.get_attribute("href") for t in tarjetas]
        ok(hrefs[0] == personal and hrefs[1].endswith("juegos/el-faro/index.html"), f"cada juego enlaza a su pack o al juego normal ({hrefs})")
        fondo = tarjetas[0].find_element(By.CSS_SELECTOR, ".opt-thumb").value_of_css_property("background-image")
        ok("marte/img/P.jpg" in fondo, f"la portada es la personalizada ({fondo})")
        fondo2 = tarjetas[1].find_element(By.CSS_SELECTOR, ".opt-thumb").value_of_css_property("background-image")
        ok("el-faro/img/P.jpg" in fondo2, "sin portada propia, usa la del juego")
        texto = d.find_element(By.ID, "mis").text
        ok("las aventuras de bea y rubén" in texto.lower() and "con bea y rubén" in texto.lower(), "se ven los protagonistas")
        ok(len(d.find_elements(By.CSS_SELECTOR, "#mis .dif-fila")) == 2, "las tarjetas del cliente llevan dificultad y duración")
        ok("Marte" not in texto, "no ve los juegos de otras cuentas")
        d.get(URL + "juegos/aventuras-ca/index.html")
        esperar(lambda: visibles(d, "#mis .salto"))
        ok(len(visibles(d, "#mis .salto")) == 2 and not d.find_element(By.ID, "todo").is_displayed(), "en el hub de aventuras, también solo los suyos")
        img = d.find_element(By.CSS_SELECTOR, "#mis .salto img").get_attribute("src")
        ok(img == portada, "con la portada personalizada en el hub")

        # ---------- 3. sin conexión (la copia del dispositivo)
        d.execute_script("localStorage.setItem('fake-romper', '1')")  # Supabase deja de responder
        d.get(URL + "index.html")
        esperar(lambda: "Sin conexión" in d.find_element(By.ID, "mis").text)
        ok(len(visibles(d, "#mis .option")) == 2 and "Sin conexión" in d.find_element(By.ID, "mis").text,
           "sin conexión, sigue enseñando sus juegos (copia del dispositivo) y lo avisa")
        d.execute_script("localStorage.removeItem('fake-romper')")
        cache = json.loads(d.execute_script("return localStorage.getItem('ca-accesos')") or "{}")
        ok(cache.get("cuenta") == "bea@ejemplo.es" and len(cache.get("lista", [])) == 2, "la copia queda guardada por cuenta")

        # ---------- 3b. cliente con muchos juegos: buscador en su lista
        muchos = [{"id": "m" + j, "email": "muchos@ejemplo.es", "juego": j, "url": "", "portada": "", "quienes": "", "creado": "2026-10-0" + str(i)}
                  for i, j in enumerate(["egipto", "marte", "florencia", "cuento", "trono", "juguetes"])]
        d.execute_script("const a = JSON.parse(localStorage.getItem('fake-unlock_accesos')); localStorage.setItem('fake-unlock_accesos', JSON.stringify(a.concat(arguments[0])))", muchos)
        sesion(d, "muchos@ejemplo.es")
        d.get(URL + "index.html")
        esperar(lambda: d.find_elements(By.CSS_SELECTOR, "#mis .fj input"))
        ok(len(visibles(d, "#mis .option")) == 6 and bool(d.find_elements(By.CSS_SELECTOR, "#mis .fj")), "con más de 4 juegos, el cliente tiene buscador")
        d.find_element(By.CSS_SELECTOR, "#mis .fj input").send_keys("marte")
        ok(len(visibles(d, "#mis .option")) == 1, "y filtra sus juegos")

                # ---------- 4. cliente sin juegos
        sesion(d, "nadie@ejemplo.es")
        d.get(URL + "index.html")
        esperar(lambda: "Todavía no hay juegos" in d.find_element(By.ID, "mis").text)
        ok("Todavía no hay juegos" in d.find_element(By.ID, "mis").text and "nadie@ejemplo.es" in d.find_element(By.ID, "mis").text,
           "un cliente sin juegos ve un aviso con su correo")
        ok(not visibles(d, "#mis .option"), "y ninguna tarjeta (no hereda la copia de otra cuenta)")

        # ---------- 5. administrador y «ver como»
        sesion(d, ADMIN)
        d.get(URL + "index.html")
        esperar(lambda: d.find_element(By.ID, "todo").is_displayed())
        ok(d.find_element(By.ID, "todo").is_displayed() and not d.find_element(By.ID, "mis").is_displayed(), "el administrador ve el menú completo")
        d.get(URL + "juegos/aventuras-ca/index.html")
        esperar(lambda: len(visibles(d, "#todo .salto")) > 5)
        ok(len(visibles(d, "#todo .salto")) >= 11, f"y todas las aventuras de Cristina y Alberto ({len(visibles(d, '#todo .salto'))})")
        caja = d.find_element(By.CSS_SELECTOR, ".fj input")
        caja.send_keys("pompeya")
        ok(len(visibles(d, "#todo .salto[data-juego]")) == 1, "el hub tiene buscador: «pompeya» deja una")
        caja.clear()
        d.execute_script("document.querySelector('.fj input').dispatchEvent(new Event('input'))")
        d.find_element(By.CSS_SELECTOR, "[data-nivel=facil]").click()
        difs = [int(e.get_attribute("data-dif")) for e in visibles(d, "#todo .salto[data-juego]")]
        ok(difs and all(x <= 2 for x in difs), f"y filtro de dificultad: «Fácil» ({difs})")
        d.get(URL + "index.html?ver-como=bea@ejemplo.es")
        esperar(lambda: visibles(d, "#mis .option"))
        ok(len(visibles(d, "#mis .option")) == 2 and "viendo la app como" in d.find_element(By.ID, "mis").text, "«ver como» enseña lo que ve el cliente")
        ok("ver-como" not in d.current_url, "y limpia la dirección")
        d.find_element(By.CSS_SELECTOR, "[data-volver]").click()
        esperar(lambda: d.find_element(By.ID, "todo").is_displayed())
        ok(d.find_element(By.ID, "todo").is_displayed(), "«Volver a mi vista» devuelve el menú completo")

        # ---------- 6. panel de accesos
        d.get(URL + "tienda/accesos.html")
        esperar(lambda: d.find_element(By.ID, "login").is_displayed())
        f = d.find_element(By.ID, "form-login")
        f.find_element(By.NAME, "email").send_keys("bea@ejemplo.es")
        f.find_element(By.NAME, "clave").send_keys("123456")
        f.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
        esperar(lambda: "no es administradora" in d.find_element(By.ID, "error-login").text)
        ok("no es administradora" in d.find_element(By.ID, "error-login").text, "el panel rechaza a quien no es administrador")
        sesion(d, ADMIN, "ca-tienda-admin")
        d.get(URL + "tienda/accesos.html?email=Ana@Ejemplo.es&quienes=Ana%20y%20Luis&pack=https://pack-ana.netlify.app/&juegos=egipto,marte,faro&pedido=")
        esperar(lambda: d.find_element(By.ID, "panel").is_displayed())
        esperar(lambda: d.find_elements(By.CSS_SELECTOR, "#lista [data-email]"))
        ok(len(d.find_elements(By.CSS_SELECTOR, "#lista [data-email]")) == 3, "el panel lista los accesos agrupados por correo")
        marcados = [i.get_attribute("value") for i in d.find_elements(By.CSS_SELECTOR, "#juegos input:checked")]
        ok(marcados == ["faro", "egipto", "marte"], f"el enlace de un pedido rellena el formulario ({marcados})")
        d.find_element(By.CSS_SELECTOR, "#form-dar button[type=submit]").click()
        esperar(lambda: "✓" in d.find_element(By.ID, "error-dar").text)
        ok("ana@ejemplo.es" in d.find_element(By.ID, "error-dar").text and "no va en el pack" in d.find_element(By.ID, "error-dar").text,
           "confirma lo dado y avisa de que el Faro no va en el pack: " + d.find_element(By.ID, "error-dar").text)
        filas = {f["juego"]: f for f in json.loads(d.execute_script("return localStorage.getItem('fake-unlock_accesos')")) if f["email"] == "ana@ejemplo.es"}
        ok(set(filas) == {"egipto", "marte", "faro"}, f"se guardan los 3 juegos para ana@ejemplo.es ({sorted(filas)})")
        ok(filas.get("egipto", {}).get("url") == "https://pack-ana.netlify.app/juegos/aventuras-ca/egipto/index.html"
           and filas["egipto"]["portada"] == "https://pack-ana.netlify.app/juegos/aventuras-ca/egipto/img/P.jpg",
           "las aventuras apuntan al pack y a su portada")
        ok(filas.get("faro", {}).get("url") == "" and filas["faro"]["quienes"] == "Ana y Luis", "el Faro queda como juego normal")
        esperar(lambda: len(d.find_elements(By.CSS_SELECTOR, "#lista [data-email]")) == 4)
        ok(len(d.find_elements(By.CSS_SELECTOR, "#lista [data-email]")) == 4, "la lista se actualiza con la cuenta nueva")
        d.execute_script("window.confirm = () => true")
        grupo = d.find_element(By.CSS_SELECTOR, "#lista [data-email='ana@ejemplo.es']")
        grupo.find_element(By.CSS_SELECTOR, "[data-accion=quitar]").click()
        esperar(lambda: len(d.find_elements(By.CSS_SELECTOR, "#lista [data-email='ana@ejemplo.es'] .acceso")) == 2)
        ok(len(d.find_elements(By.CSS_SELECTOR, "#lista [data-email='ana@ejemplo.es'] .acceso")) == 2, "«Quitar» le quita ese juego")
        d.find_element(By.ID, "buscar").send_keys("bea")
        ok(len(visibles(d, "#lista [data-email]")) == 1, "el buscador filtra por correo")
        # el cliente nuevo entra en la app y ve lo que se le ha dado
        d.get(URL + "instalar.html")
        sesion(d, "ana@ejemplo.es")
        d.get(URL + "index.html")
        esperar(lambda: visibles(d, "#mis .option"))
        ok(len(visibles(d, "#mis .option")) == 2, "la cuenta nueva ve en la app los juegos que le quedan")

        errores = [x["message"] for x in d.get_log("browser") if x["level"] == "SEVERE" and "favicon" not in x["message"]
                   and "fonts.g" not in x["message"] and "netlify" not in x["message"]]
        ok(not errores, f"sin errores de consola {errores[:3]}")
    finally:
        d.quit()
        srv.shutdown()
    print("RESULTADO:", f"{len(fallos)} fallos" if fallos else "todo bien")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()

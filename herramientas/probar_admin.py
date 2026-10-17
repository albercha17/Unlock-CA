"""Prueba el panel de pedidos (tienda/admin.html) con Chrome headless y un Supabase SIMULADO (no toca la base de datos real).

El servidor de prueba sustituye assets/js/vendor/supabase.js por un falso con dos pedidos de ejemplo.
Uso: python herramientas/probar_admin.py [carpeta_para_capturas]
"""
import functools
import http.server
import os
import sys
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPTURAS = sys.argv[1] if len(sys.argv) > 1 else None
fallos = []

FALSO = r"""
(() => {
  const A = '11111111-aaaa-4aaa-8aaa-111111111111', B = '22222222-bbbb-4bbb-8bbb-222222222222';
  const pedidos = [
    { id: A, creado: '2026-10-17T10:00:00Z', estado: 'nuevo', nombre: '<img src=x onerror="window.__xss=1">Lucía', email: 'lucia@ejemplo.com',
      telefono: '600000000', aventuras: ['egipto', 'marte', 'cuento', 'trono'], formato: 'impreso', precio: 79,
      ocasion: 'Aniversario', fecha_deseada: '2026-12-01', dedicatoria: 'Para vosotros', direccion: 'Calle Mayor 1', notas: null,
      protagonistas: [{ nombre: 'Lucía', genero: 'mujer', edad: '34', sobre: 'enfermera', fotos: [A + '/p1-1.jpg'] },
                      { nombre: 'Marcos', genero: 'hombre', edad: '36', sobre: '', fotos: [A + '/p2-1.jpg'] }],
      progreso: null, entrega_url: null },
    { id: B, creado: '2026-10-16T10:00:00Z', estado: 'listo', nombre: 'Ana', email: 'ana@ejemplo.com', telefono: null,
      aventuras: ['egipto', 'marte', 'florencia', 'dinosaurios'], formato: 'digital', precio: 49,
      protagonistas: [{ nombre: 'Ana', genero: 'mujer', fotos: [B + '/p1-1.jpg'] }, { nombre: 'Leo', genero: 'niño', fotos: [B + '/p2-1.jpg'] }],
      progreso: 'Listo: 38 ilustraciones con los protagonistas.', entrega_url: 'https://cronoportal-prueba.netlify.app' },
  ];
  window.__llamadas = [];
  let sesion = null;
  const ok = (data) => Promise.resolve({ data, error: null });
  const consulta = () => {
    const q = { _accion: 'select', _cambios: null,
      select() { return q; }, order() { return q; },
      update(c) { q._accion = 'update'; q._cambios = c; return q; },
      delete() { q._accion = 'delete'; return q; },
      eq(_, id) {
        window.__llamadas.push([q._accion, id, q._cambios]);
        const i = pedidos.findIndex((p) => p.id === id);
        if (q._accion === 'update') Object.assign(pedidos[i], q._cambios);
        if (q._accion === 'delete') pedidos.splice(i, 1);
        return ok(null);
      },
      then(res, rej) { return ok(JSON.parse(JSON.stringify(pedidos))).then(res, rej); },
    };
    return q;
  };
  window.supabase = { createClient: () => ({
    auth: {
      getSession: () => ok({ session: sesion }),
      onAuthStateChange: () => ({ data: { subscription: { unsubscribe() {} } } }),
      signInWithPassword: ({ email, password }) => password === 'buena'
        ? (sesion = { user: { email } }, ok({ session: sesion }))
        : Promise.resolve({ data: null, error: { message: 'Invalid login credentials' } }),
      signOut: () => { sesion = null; return ok(null); },
    },
    rpc: () => ok(true),
    from: () => consulta(),
    storage: { from: () => ({
      createSignedUrls: (rutas) => ok(rutas.filter((r) => !r.endsWith('hoja.jpg')).map((path) => ({ path, signedUrl: '../juegos/aventuras-ca/egipto/img/P.jpg', error: null }))),
      list: () => ok([{ name: 'p1-1.jpg' }]),
      remove: (r) => { window.__llamadas.push(['remove', r]); return ok(null); },
    }) },
  }) };
})();
"""


def comprobar(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


class Manejador(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path.split("?")[0].endswith("/assets/js/vendor/supabase.js"):
            cuerpo = FALSO.encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript")
            self.send_header("Content-Length", str(len(cuerpo)))
            self.end_headers()
            self.wfile.write(cuerpo)
            return
        super().do_GET()


def main():
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Manejador, directory=RAIZ))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{s.server_address[1]}/tienda/admin.html"
    try:
        for ancho in (1280, 390):
            print(f"--- {ancho}px ---")
            o = webdriver.ChromeOptions()
            o.add_argument("--headless=new")
            o.add_argument(f"--window-size={ancho},1000")
            o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
            d = webdriver.Chrome(options=o)
            js = d.execute_script
            try:
                d.get(url)
                time.sleep(1)
                comprobar(d.find_element(By.ID, "login").is_displayed(), "sin sesión se pide entrar")
                d.find_element(By.NAME, "email").send_keys("admin@ejemplo.com")
                d.find_element(By.NAME, "clave").send_keys("mala")
                js("document.querySelector('#form-login button[type=submit]').click()")
                time.sleep(0.5)
                comprobar("incorrectos" in d.find_element(By.ID, "error-login").text, "contraseña mala: aviso")
                d.find_element(By.NAME, "clave").clear()
                d.find_element(By.NAME, "clave").send_keys("buena")
                js("document.querySelector('#form-login button[type=submit]').click()")
                time.sleep(1)
                comprobar(d.find_element(By.ID, "panel").is_displayed(), "entra al panel")
                comprobar(len(d.find_elements(By.CSS_SELECTOR, ".pedido-admin")) == 2, "dos pedidos activos")
                comprobar(not js("return window.__xss"), "el HTML del cliente no se ejecuta")
                comprobar("<img" in d.find_element(By.CSS_SELECTOR, ".cliente").text, "el nombre raro se muestra como texto")
                comprobar(len(d.find_elements(By.CSS_SELECTOR, ".fotos-admin img")) == 4, "se ven las 4 fotos")
                comprobar(d.find_elements(By.CSS_SELECTOR, '.estado-listo a[href*="netlify"]') != [], "enlace al pack listo")
                if CAPTURAS:
                    alto = js("return document.documentElement.scrollHeight")
                    d.set_window_size(ancho, alto)
                    time.sleep(0.4)
                    d.save_screenshot(os.path.join(CAPTURAS, f"admin-{ancho}.png"))
                    d.set_window_size(ancho, 1000)
                desborde = js("return document.documentElement.scrollWidth - document.documentElement.clientWidth")
                comprobar(desborde <= 0, f"sin scroll horizontal ({desborde}px)")

                # Desarrollarlo
                js("window.confirm = () => true")
                js("document.querySelector('.estado-nuevo [data-accion=desarrollar]').click()")
                time.sleep(0.8)
                ll = js("return window.__llamadas")
                comprobar(ll and ll[-1][0] == "update" and ll[-1][2]["estado"] == "desarrollar", "Desarrollarlo pone el estado «desarrollar»")
                comprobar("Desarrollándose" in d.find_element(By.CSS_SELECTOR, ".estado-desarrollar footer").text, "el botón pasa a «Desarrollándose…»")
                comprobar(d.find_element(By.CSS_SELECTOR, ".estado-desarrollar .progreso").is_displayed(), "se ve el progreso")

                # filtros
                js("document.querySelector('[data-filtro=listo]').click()")
                comprobar(len(d.find_elements(By.CSS_SELECTOR, ".pedido-admin")) == 1, "filtro «Listos»")
                # marcar entregado
                js("document.querySelector('[data-accion=entregado]').click()")
                time.sleep(0.6)
                comprobar(js("return window.__llamadas.at(-1)[2].estado") == "entregado", "marcar entregado")
                # borrar
                js("document.querySelector('[data-filtro=todos]').click()")
                js("document.querySelector('[data-accion=borrar]').click()")
                time.sleep(0.8)
                comprobar(any(x[0] == "remove" for x in js("return window.__llamadas")), "borrar quita también las fotos")
                comprobar(len(d.find_elements(By.CSS_SELECTOR, ".pedido-admin")) == 1, "queda un pedido tras borrar")
                errores = [l["message"] for l in d.get_log("browser") if l["level"] == "SEVERE" and "favicon" not in l["message"] and "/x" not in l["message"]]
                comprobar(not errores, f"sin errores en consola {errores}")
            finally:
                d.quit()
    finally:
        s.shutdown()
    print("\nTodo correcto" if not fallos else f"\n{len(fallos)} fallo(s)")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()

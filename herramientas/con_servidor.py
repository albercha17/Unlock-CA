"""Arranca un servidor local en un puerto libre SOLO mientras dura un comando y sustituye {URL} por su dirección (sin dejar procesos en segundo plano).
Uso:  python herramientas/con_servidor.py python herramientas/probar_apps.py {URL} juegos/el-faro solvers_faro"""
import functools
import http.server
import os
import subprocess
import sys
import threading

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=RAIZ)
    h.log_message = lambda *a, **k: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_address[1]}"
    cmd = [sys.executable if a == "python" else a.replace("{URL}", url) for a in sys.argv[1:]]
    try:
        sys.exit(subprocess.call(cmd, cwd=RAIZ))
    finally:
        srv.shutdown()


if __name__ == "__main__":
    main()

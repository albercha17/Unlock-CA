"""Ayudas para AMPLIAR juegos ya publicados hasta el mínimo de 36 cartas (regla del 20 oct 2026) sin tocar sus ilustraciones.

  - recalcular_mesas(PASOS, J): rehace la mesa esperada de cada paso del manual simulando las acciones (leer, app, combinar), así que al
    insertar pasos nuevos no hay que escribir las mesas a mano. Si se le pasa `comprobar`, avisa si una mesa ya escrita no coincide.
  - escribir_cartas(Juego): escribe cartas.json, spec_<juego>.json e img/pendientes.json desde datos_<juego>.py (sin regenerar el resto
    de la carpeta, al contrario que construir_aventuras.py) y pone una ilustración provisional a las cartas nuevas sin imagen.
  - cambiar_mensaje(ruta_js, viejo, nuevo): cambia el «Coged la carta N» de un minijuego.
Uso:  python herramientas/ampliacion.py Marte [Egipto ...]
"""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)

ORDEN_CAMPOS = ["titulo", "tipo", "coge", "descarta", "combina", "descripcion", "pistas", "textoCarta", "textoEspejo", "mosaico", "reverso",
                "plegado", "arte"]


def _orden(k):
    return (k != "P", int(k) if k != "P" else 0)


def recalcular_mesas(pasos, J, comprobar=False):
    mesa = set()
    for i, p in enumerate(pasos):
        for a in p["acciones"]:
            if a[0] == "leer":
                c = J[a[1]]
                if a[1] == "P":
                    mesa = {"P"}
                for d in c.get("descarta", []):
                    mesa.discard(str(d))
                for h in c.get("coge", []):
                    mesa.add(str(h))
            elif a[0] == "app":
                if a[2].startswith("carta "):
                    mesa.add(a[2].split()[-1])
            elif a[0] == "combinar":
                mesa.add(str(int(a[1]) + int(a[2])))
        nueva = sorted(mesa, key=_orden)
        if comprobar and p.get("mesa") is not None and sorted(p["mesa"]) != sorted(nueva):
            print(f"  aviso: paso {i + 1} «{p['t']}»: mesa escrita {sorted(p['mesa'])} y simulada {sorted(nueva)}")
        p["mesa"] = nueva
    return pasos


def escribir_cartas(nombre):
    from juegos_config import JUEGOS
    from construir_aventuras_util import placeholder
    cfg = JUEGOS[nombre]
    datos = cfg["datos"]
    base = os.path.join(RAIZ, "juegos", "aventuras-ca", nombre.lower())
    ruta = os.path.join(base, "cartas.json")
    viejo = json.load(open(ruta, encoding="utf-8"))
    out = {"_meta": getattr(datos, "META", None) or viejo.get("_meta")}
    for k, c in datos.J.items():
        out[k] = {campo: c[campo] for campo in ORDEN_CAMPOS if campo in c}
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(os.path.join(AQUI, f"spec_{nombre.lower()}.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(datos.SPEC, f, ensure_ascii=False, indent=2)
    pend_ruta = os.path.join(base, "img", "pendientes.json")
    pend = set(json.load(open(pend_ruta, encoding="utf-8"))) if os.path.exists(pend_ruta) else set()
    for k, c in datos.J.items():
        img = os.path.join(base, "img", f"{k}.jpg")
        if not os.path.exists(img):
            placeholder(img, c["titulo"].split("—", 1)[1].strip(), *cfg["pal"])
            pend.add(k)
    pend &= set(datos.J)
    json.dump(sorted(pend, key=_orden), open(pend_ruta, "w", encoding="utf-8"))
    subprocess.run([sys.executable, os.path.join(AQUI, "sincronizar_cartas.py")], check=True, stdout=subprocess.DEVNULL)
    print(f"{nombre}: {len(datos.J)} cartas; ilustraciones pendientes: {sorted(pend, key=_orden)}")


def cambiar_mensaje(ruta, viejo, nuevo):
    s = open(ruta, encoding="utf-8").read()
    if nuevo in s and viejo not in s:
        return
    assert s.count(viejo) == 1, f"{ruta}: no encuentro {viejo!r}"
    open(ruta, "w", encoding="utf-8", newline="\n").write(s.replace(viejo, nuevo))


if __name__ == "__main__":
    for n in sys.argv[1:]:
        escribir_cartas(n)

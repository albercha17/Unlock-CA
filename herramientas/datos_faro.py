"""Datos del manual del Faro: pasos ejecutables, para que sirve cada carta y dependencias para el verificador."""
PASOS = [{'t': 'Empieza la partida',
  'que': 'Pon el Modo PC en el ordenador (solo debe haber la carta P en la mesa y 23 cartas boca abajo en el mazo). En el móvil abre el juego y '
         'pulsa Empezar.',
  'acciones': [('leer', 'P')],
  'mesa': ['7', 'P']},
 {'t': 'El recibidor',
  'que': 'Lee la carta 7. Te manda descartar la P y coger cinco cartas.',
  'acciones': [('leer', '7')],
  'mesa': ['7', '15', '21', '19', '12', '36']},
 {'t': 'Lee el cuaderno en la app',
  'que': 'En el móvil: Acción, escribe 15. Pasa las 4 páginas. Trae la tabla de morse, un aviso sobre el reloj y parte del arranque de la lámpara. '
         'No hay nada que resolver y no pausa el tiempo.',
  'acciones': [('app', '15', 'lector')],
  'mesa': ['7', '15', '21', '19', '12', '36']},
 {'t': 'Abre la puerta de la escalera',
  'que': 'El reloj (21) está parado a las 3:15 y la etiqueta del paraguas (19) dice que atrasa 1 h 20 min: 3:15 + 1:20 = 4:35. En el móvil: Acción, '
         '36, código 0435. El mensaje te dice que cojas la 40.',
  'acciones': [('app', '36', 'carta 40')],
  'mesa': ['7', '15', '21', '19', '12', '36', '40']},
 {'t': 'La escalera',
  'que': 'Lee la carta 40. Descarta 7, 36, 21 y 19 y coge 52, 30, 27 y 18. Lee lo que ponen la 12 (taza), la 27 (nido) y la 18 (gaviota): son pasos '
         'y pistas que necesitarás más tarde.',
  'acciones': [('leer', '40')],
  'mesa': ['15', '12', '40', '52', '30', '27', '18']},
 {'t': 'El mensaje de la ventana',
  'que': 'En el móvil: Acción, 52. Mira los destellos de la luz (cortos = punto, largos = raya) y apúntalos en un papel; puedes pulsar «Repetir '
         'mensaje». Descífralos con la tabla de morse del cuaderno (15). La palabra es ANCLA. El mensaje te dice que cojas la 33.',
  'acciones': [('app', '52', 'carta 33')],
  'mesa': ['15', '12', '40', '52', '30', '27', '18', '33']},
 {'t': 'El ancla',
  'que': 'Lee la carta 33. Te manda descartar la 52.',
  'acciones': [('leer', '33')],
  'mesa': ['15', '12', '40', '30', '27', '18', '33']},
 {'t': 'Combina el ancla con la puerta',
  'que': 'Las cartas 33 (ancla) y 30 (puerta de máquinas) son combinables: suma sus números, 33 + 30 = 63, y coge la 63.',
  'acciones': [('combinar', '33', '30')],
  'mesa': ['15', '12', '40', '30', '27', '18', '33', '63']},
 {'t': 'La sala de máquinas',
  'que': 'Lee la carta 63. Descarta 33, 30 y 40 y coge 74, 85, 72 y 3. Lee el mapa (74): la frecuencia es 91,_ y le falta la décima. La brújula (3) '
         'dice «Siete vientos, siete décimas»: la décima es 7.',
  'acciones': [('leer', '63')],
  'mesa': ['15', '12', '27', '18', '63', '74', '85', '72', '3']},
 {'t': 'Sintoniza la radio',
  'que': 'En el móvil: Acción, 85. Gira la rueda grande (arrástrala en círculo con el dedo) hasta acercarte a 91 y afina con la rueda pequeña hasta '
         'que la lectura marque 91,7 MHz. El mensaje te dice que cojas la 78.',
  'acciones': [('app', '85', 'carta 78')],
  'mesa': ['15', '12', '27', '18', '63', '74', '85', '72', '3', '78']},
 {'t': 'La sala de la lente',
  'que': 'Lee la carta 78. Descarta 63, 85, 74 y 3 y coge 70, 10 y 95.',
  'acciones': [('leer', '78')],
  'mesa': ['15', '12', '27', '18', '78', '72', '70', '10', '95']},
 {'t': 'Llena la lámpara',
  'que': 'Las cartas 72 (bidón) y 10 (lámpara vacía) son combinables: 72 + 10 = 82. Coge la 82 y léela: te manda descartar 72 y 10.',
  'acciones': [('combinar', '72', '10'), ('leer', '82')],
  'mesa': ['15', '12', '27', '18', '78', '70', '95', '82']},
 {'t': 'Alinea los espejos',
  'que': 'En el móvil: Acción, 70. El papel del nido (27) dice que la luz sube, cruza y baja: lleva el rayo a la galería, luego a la lente y por último a la lámpara (gira los espejos B4, B3, D3, D2, G2, G3 y F3). El mensaje te dice '
         'que descartes la 70 y la 27.',
  'acciones': [('app', '70', 'Descartad las cartas 70 y 27')],
  'mesa': ['15', '12', '18', '78', '95', '82']},
 {'t': 'Arranca la lámpara',
  'que': 'En el móvil: Acción, 95. El orden sale de tres cartas: el cuaderno (el aceite es lo primero y el piloto va justo tras el engranaje), la '
         'taza (12: la mecha se ceba antes de girar nada) y la gaviota (18: el freno, el último). Orden: aceite, mecha, engranaje, piloto, freno. El '
         'mensaje te dice que cojas la 99.',
  'acciones': [('app', '95', 'carta 99')],
  'mesa': ['15', '12', '18', '78', '95', '82', '99']},
 {'t': 'Final',
  'que': 'Lee la carta 99. Te manda descartar 78, 95, 82, 15, 12 y 18. En la mesa solo queda la 99. ¡Fin!',
  'acciones': [('leer', '99')],
  'mesa': ['99']}]

PARA_QUE = {
    "P": "Inicio de la partida: te manda coger la 7.",
    "7": "El recibidor: reparte las cartas de pistas y te quita la P.",
    "15": "Cuaderno (app, solo lectura): tabla de morse, aviso del reloj y parte del orden de arranque.",
    "21": "Reloj parado a las 3:15: base del código de la puerta.",
    "19": "Etiqueta del paraguas: el reloj atrasa 1 h 20 min (corrige la hora del reloj).",
    "12": "Taza: «La mecha se ceba antes de girar nada» (un paso del arranque, carta 95).",
    "36": "Puerta con teclado (app): código 0435 = 3:15 + 1 h 20 min.",
    "40": "La escalera: da las cartas del rellano y descarta lo que ya no hace falta.",
    "52": "Ventana de señales (app): se descifra el morse y sale la palabra ANCLA.",
    "30": "Puerta de máquinas: se combina con la 33.",
    "27": "Nido: el papel dice «La luz sube, cruza y baja» (pista para los espejos, carta 70).",
    "18": "Gaviota: «El freno, el último. Siempre» (un paso del arranque, carta 95).",
    "33": "Ancla con la llave: se combina con la 30.",
    "63": "Sala de máquinas: es el resultado de 33 + 30.",
    "74": "Mapa: la frecuencia del faro es 91,_ MHz (falta la décima).",
    "3": "Brújula: «Siete vientos, siete décimas» (la décima es 7).",
    "85": "Radio (app): hay que sintonizar 91,7 MHz.",
    "72": "Bidón de aceite: se combina con la 10.",
    "78": "Sala de la lente: da las cartas de la lente y descarta las de la sala de máquinas.",
    "10": "Lámpara vacía: se combina con la 72.",
    "82": "Lámpara llena: es el resultado de 72 + 10; hace falta para el arranque.",
    "70": "Espejos (app): llevar el rayo por la galería, la lente y la lámpara, en ese orden; al acabar manda descartar la 70 y la 27.",
    "95": "Panel de arranque (app): ordenar los cinco pasos del arranque.",
    "99": "Final de la partida."
}

SPEC = {'final': '99',
 'needs': {'40': ['36', '21', '19'],
           '33': ['52', '15'],
           '63': ['33', '30'],
           '78': ['85', '74', '3'],
           '82': ['72', '10'],
           '99': ['95', '82', '15', '12', '18', 'e70']},
 'eventos': {'e70': {'needs': ['70', '27'], 'descarta': ['70', '27']}}}


# ================================================================== ampliación a 36 cartas (20 oct 2026)
# Entre la radio y la sala de la lente: el plano de la bahía, la lámpara de la mesa y el temporizador de la lente (ampliar_faro.py).
import json as _json  # noqa: E402
import os as _os  # noqa: E402

_AQUI = _os.path.dirname(_os.path.abspath(__file__))
_AMP = _json.load(open(_os.path.join(_AQUI, "instancias_ampliacion.json"), encoding="utf-8"))
_J = _json.load(open(_os.path.join(_AQUI, "..", "juegos", "el-faro", "cartas.json"), encoding="utf-8"))
_TIERRA = ", ".join(f"{'ABCDEF'[f]}{c + 1}" for f, c in _AMP["faro_bahia"]["tierra"])
_ORDEN = ", ".join(_AMP["faro_sombras"]["solucion"])
_LUZ = " ".join(str(s + 1) for s, v in enumerate(_AMP["faro_destellos"]["solucion"]) if v)

PASOS[0]["que"] = PASOS[0]["que"].replace("23 cartas boca abajo", "35 cartas boca abajo")
_i = next(i for i, p in enumerate(PASOS) if p["acciones"][0][:2] == ("app", "85"))
PASOS[_i]["que"] = PASOS[_i]["que"].replace("cojas la 78", "cojas la 44")
PASOS[_i]["acciones"] = [("app", "85", "carta 44")]
_nuevos = [
    dict(t="La guardia costera", que="Lee la carta 44. Coge 45, 46 y 47: el plano de la bahía está partido en dos hojas.", acciones=[("leer", "44")]),
    dict(t="El plano de la bahía", que=f"En el móvil: Acción, 45. Marca como islote: {_TIERRA}. Pulsa Transmitir. El mensaje te dice que cojas la 54.",
         acciones=[("app", "45", "carta 54")]),
    dict(t="El cuarto de guardia", que="Lee la carta 54. Descarta 44, 45, 46 y 47 y coge 55, 56 y 57.", acciones=[("leer", "54")]),
    dict(t="La lámpara de la mesa", que=f"En el móvil: Acción, 55. Pon en la mesa, de izquierda a derecha: {_ORDEN}. Enciende la lámpara. El mensaje te dice que cojas la 64.",
         acciones=[("app", "55", "carta 64")]),
    dict(t="La escalera de hierro", que="Lee la carta 64. Descarta 54, 55, 56 y 57 y coge 65, 66 y 67.", acciones=[("leer", "64")]),
    dict(t="El temporizador de la lente", que=f"En el móvil: Acción, 65. Cabo Niebla es destello, destello, destello y largo: enciende los segundos {_LUZ}. Pulsa Programar. El mensaje te dice que cojas la 78.",
         acciones=[("app", "65", "carta 78")]),
]
_mesa = set(PASOS[_i]["mesa"]) - {"78"} | {"44"}
PASOS[_i]["mesa"] = sorted(_mesa)
for _p in _nuevos:
    _a = _p["acciones"][0]
    if _a[0] == "leer":
        _mesa -= {str(x) for x in _J[_a[1]].get("descarta", [])}
        _mesa |= {str(x) for x in _J[_a[1]].get("coge", [])}
    else:
        _mesa.add(_a[2].split()[-1])
    _p["mesa"] = sorted(_mesa)
PASOS[_i + 1:_i + 1] = _nuevos
_j = next(i for i, p in enumerate(PASOS) if p["acciones"][0][:2] == ("leer", "78"))
PASOS[_j]["que"] = PASOS[_j]["que"] + " Descarta también 64, 65, 66 y 67."

SPEC["needs"]["44"] = SPEC["needs"].pop("78")
SPEC["needs"].update({"54": ["45", "46", "47"], "64": ["55", "56", "57"], "78": ["65", "66", "67"]})
PARA_QUE.update({
    "44": "La guardia costera: reparte el plano de la bahía.", "45": "El plano de la bahía (app): marcar los islotes.",
    "46": "Plano de la bahía (filas A a C).", "47": "Plano de la bahía (filas D a F) y reglas.",
    "54": "El cuarto de guardia: reparte la lámpara, la sombra y el estante.", "55": "La lámpara de la mesa (app): reproducir la sombra.",
    "56": "La sombra pintada en la pared.", "57": "El estante del farero: las cosas que dan sombra.",
    "64": "La escalera de hierro: reparte el temporizador, el almanaque y la nota.", "65": "El temporizador de la lente (app): la luz de Cabo Niebla.",
    "66": "Almanaque de faros.", "67": "Nota de Anselmo: cómo leer el almanaque.",
    "78": "Sala de la lente: aparece al programar el temporizador.",
})

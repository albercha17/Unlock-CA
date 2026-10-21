// Carta 20 — La manada del abrevadero: cuántos tricerátops y cuántos velocirraptores hay tras los helechos. Arriba asoman las cabezas
// y abajo las patas (las dos mitades, cartas 19 y 21). Solución única (instancias_dinosaurios.py, MANADA).
import { openGame } from './ui.js';
import { contador } from './valle.js';

const D = /*DATOS*/{"cabezas": 13, "patas": 40, "solucion": {"triceratops": 7, "velociraptor": 6}}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 20 — La manada del abrevadero', instr: 'Antes de cruzar el abrevadero hay que saber qué hay detrás de los helechos. Decid cuántos animales hay de cada clase.', ...opts });
  const tri = contador('Tricerátops', 30, () => ui.say(''), 'triceratops');
  const rap = contador('Velocirraptores', 30, () => ui.say(''), 'velociraptor');
  ui.body.append(tri.el, rap.el);
  let resuelto = false;
  ui.button('Cruzar', 'primary', () => {
    if (resuelto) return;
    const t = tri.valor(), r = rap.valor();
    if (t === D.solucion.triceratops && r === D.solucion.velociraptor) {
      resuelto = true;
      ui.say('Los tricerátops beben tranquilos y los raptores, al veros contar, se esconden. Pasáis sin un rasguño. Coged la carta 28.', 'ok');
    } else if (t + r !== D.cabezas) ui.say('Con esos números no salen las cabezas que asoman por encima (cartas 19 y 21).', 'bad');
    else ui.say('Las cabezas cuadran, pero las patas de abajo no (cartas 19 y 21).', 'bad');
  });
  return { close: ui.close };
}

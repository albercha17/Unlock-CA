// Carta 64 — El vuelo con escalas: el Dr. Noche voló de Tokio a Montecarlo con dos escalas. Hay que decir a qué hora local llegó, y si fue el mismo día de
// la salida o más tarde. El itinerario, en la carta 66; los husos horarios, en la 67 (instancias_espia.py, HUSOS).
import { openGame } from './ui.js';
import { contador } from './comun.js';

const D = /*DATOS*/{"llegada": {"dia": 1, "hora": 15, "min": 30}}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 64 — El vuelo con escalas', instr: 'Decid cuándo aterrizó en Montecarlo, en hora de Montecarlo: cuántos días después de la salida, y la hora y los minutos. El itinerario está en la carta 66 y los husos, en la 67.', ...opts });
  const dia = contador('Días después de la salida', 0, 3, 0, 'dia');
  const hora = contador('Hora (0 a 23)', 0, 23, 0, 'hora');
  const min = contador('Minutos', 0, 59, 0, 'min');
  ui.body.append(dia.el, hora.el, min.el);
  let resuelto = false;
  ui.button('Abrir la caja de seguridad', 'primary', () => {
    if (resuelto) return;
    const L = D.llegada;
    if (dia.valor() !== L.dia) { ui.say('El día no cuadra: contad bien los husos y las horas de vuelo y de escala.', 'bad'); return; }
    if (hora.valor() !== L.hora || min.valor() !== L.min) { ui.say('El día es bueno, pero la hora de aterrizaje no cuadra.', 'bad'); return; }
    resuelto = true;
    ui.say('Clic: la caja se abre y dentro, sobre un cojín, brilla el cristal del Cronoportal. Coged la carta 62.', 'ok');
  });
  return { close: ui.close };
}

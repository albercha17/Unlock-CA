// Carta 42 — Diario del doctor Ibarra: lector. Contiene las normas del cruce del río (carta 40).
import { abrirLector } from './lector.js';

const PAGINAS = [
  {
    titulo: 'Día 1 — El valle',
    texto: [
      'Soy el doctor Ibarra, paleontólogo. Este valle, al final del Cretácico, es el sueño de cualquier científico: tiranosaurios, tricerátops, edmontosaurios y hasta un saurópodo gigante que baja a beber al río cada tarde.',
      'Mi Cronoportal se estropeó y tuve que marcharme a toda prisa. Dejo mi equipo repartido por el valle, por si alguien lo necesita.'
    ]
  },
  {
    titulo: 'Día 9 — El vado',
    texto: [
      'Para cruzar el río grande uso una balsa de troncos. Cabemos nosotros y una sola criatura o carga cada vez. Hay que remar los dos a la vez, así que lo que se queda en la orilla se queda sin vigilancia.',
      'En esta orilla viven un pequeño compsognato (un carnívoro del tamaño de un pollo) y un bebé de driosaurio que me sigue a todas partes. Y siempre llevo un cesto de helechos para alimentar al bebé.'
    ]
  },
  {
    titulo: 'Día 9 — Normas del cruce',
    texto: [
      'Dos reglas, aprendidas a las malas. Si dejo solos al compsognato y al bebé de driosaurio, el compsognato lo ataca. Y si dejo solos al bebé y los helechos, el bebé se los come todos.',
      'El compsognato no come helechos: si se quedan solos el compsognato y los helechos, no pasa nada.'
    ]
  },
  {
    titulo: 'Día 21 — El cielo',
    texto: [
      'Esta noche ha aparecido un punto de luz nuevo en el cielo. Cada noche es más grande. Lo he calculado dos veces y no me gusta nada el resultado.',
      'Si alguien lee esto y todavía tiene un aparato en condiciones: no os quedéis. Yo ya no tengo tiempo. — Ibarra'
    ]
  }
];

export function startMinigame(opts = {}) {
  return abrirLector({
    titulo: 'Carta 42 — Diario del doctor Ibarra',
    instr: 'Pasa las páginas con calma. Aquí hay cosas que os harán falta.',
    paginas: PAGINAS,
    tema: 'papiro',
    opts
  });
}

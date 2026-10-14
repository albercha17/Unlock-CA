// Carta 42 — El cuento del Búho: lector. Contiene las reglas de los saltos al pasado (carta 40).
import { abrirLector } from './lector.js';

const PAGINAS = [
  {
    titulo: 'Había una vez...',
    texto: [
      'Había una vez un camino que llevaba de la aldea al castillo. Un día unos viajeros del tiempo, que no eran de este libro, se pusieron a mirar cómo era el camino antes y cómo es ahora.',
      'Yo soy el Búho Narrador y lo he visto todo. Os cuento cómo funcionan los saltos.'
    ]
  },
  {
    titulo: 'Las reglas de los saltos',
    texto: [
      'El camino tiene siete casillas, de la aldea (la primera) al castillo (la última). Solo se pueden cambiar las cinco del medio.',
      'Tenéis exactamente tres saltos al pasado. En cada casilla se puede hacer una sola acción. Lo que hagáis en «Había una vez» cambia esa misma casilla en «Y ahora».'
    ]
  },
  {
    titulo: 'Plantar la habichuela',
    texto: [
      'Si plantáis la habichuela donde hoy hay un río (en el pasado era una charca), crece una enredadera gigante que hace de puente y se puede pasar.',
      'Si la plantáis entre zarzas, crece enredada y las zarzas siguen estorbando. Si la plantáis en una roca, la roca sigue ahí. En una casilla libre nace una habichuela, que no estorba.'
    ]
  },
  {
    titulo: 'Cavar',
    texto: [
      'Si cavéis donde hoy hay una roca, la roca se hunde y deja un hueco por el que se puede pasar.',
      'Si cavéis en una casilla libre, queda un foso que no se puede cruzar. En un río o entre zarzas, cavar no cambia nada.'
    ]
  },
  {
    titulo: 'Encender fuego',
    texto: [
      'El fuego del pasado deja ceniza en el presente. Si prendéis fuego donde hoy hay zarzas, las zarzas se queman y se puede pasar.',
      'En una casilla libre solo deja ceniza, que no estorba. En un río o en una roca, el fuego no cambia nada.'
    ],
    pie: 'Recordad: el camino queda libre cuando ninguna casilla del medio estorba.'
  }
];

export function startMinigame(opts = {}) {
  return abrirLector({
    titulo: 'Carta 42 — El cuento del Búho',
    instr: 'Pasa las páginas con calma. Aquí están las reglas de los saltos al pasado.',
    paginas: PAGINAS,
    tema: 'papiro',
    opts
  });
}

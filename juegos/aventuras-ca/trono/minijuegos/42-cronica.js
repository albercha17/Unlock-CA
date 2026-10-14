// Carta 42 — Crónica del maestre: lector. Contiene los caminos de los castillos E y G del mapa (carta 40).
import { abrirLector } from './lector.js';

const PAGINAS = [
  {
    titulo: 'Crónica del maestre Osric — El reino',
    texto: [
      'Soy Osric, maestre de Piedra Negra desde hace cuarenta inviernos. Escribo esto porque este invierno es el más duro que recuerdo y el Gran Muro cruje por las noches.',
      'El reino se sostiene sobre ocho castillos, unidos por caminos de piedra que la nieve cubre cada año. Cuando se cierran los pasos, los castillos quedan aislados hasta la primavera.'
    ]
  },
  {
    titulo: 'Los ocho castillos',
    texto: [
      'En el mapa los he señalado con letras, de la A a la H. Los caminos van siempre en línea recta, de castillo a castillo, y nunca se cruzan: ningún carro puede pasar por encima de otro camino.',
      'Entre dos castillos vecinos hay uno o dos caminos: los dobles son los que usan las caravanas de grano.'
    ]
  },
  {
    titulo: 'Las guarniciones del sur',
    texto: [
      'Anoto aquí lo que no he podido dibujar en el mapa. El castillo E, la Torre del Cuervo, tiene tres caminos que salen de él. El castillo G, el Puerto de Hierro, el más concurrido, tiene cuatro.',
      'Todos los demás castillos llevan su número escrito en el mapa. Si unes los ocho sin cruzar ningún camino, el reino queda a salvo de la nieve.'
    ]
  },
  {
    titulo: 'La profecía',
    texto: [
      'Mi abuelo me enseñó una profecía muy antigua del reino. Dice que cada castillo guarda una palabra, y que quien las reúna todas y las ponga en orden sabrá cómo vencer al invierno.',
      'Yo solo recuerdo las pistas para ordenarla. Las dejaré anotadas por si algún día hacen falta. — Osric'
    ]
  }
];

export function startMinigame(opts = {}) {
  return abrirLector({
    titulo: 'Carta 42 — Crónica del maestre',
    instr: 'Pasad las páginas con calma. Aquí hay datos que os harán falta.',
    paginas: PAGINAS,
    tema: 'papiro',
    opts
  });
}

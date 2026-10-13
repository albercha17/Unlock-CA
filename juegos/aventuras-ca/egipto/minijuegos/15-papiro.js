// Carta 15 — Papiro del escriba: lector. Contiene los colores de los cuatro cristales (carta 95).
import { abrirLector } from './lector.js';

const PAGINAS = [
  {
    titulo: 'Plegaria a Thot',
    texto: [
      'Thot, señor de la escritura, guía mi mano. Yo, Nebamón, escriba del templo de Amón, dejo aquí lo que los visitantes necesitarán.',
      'Quien lea esto no pertenece a nuestra época: lo sé por el brillo extraño de su aparato. Que los dioses os protejan, viajeros.'
    ]
  },
  {
    titulo: 'Los cuatro cristales',
    texto: [
      'En el pecho del guardián duermen cuatro cristales, y cada uno tiene su color:',
      'El Sol es amarillo. El Nilo es azul. El Papiro es verde. La Sangre es roja.',
      'Despertarán al Ojo si se tocan en el orden que el guardián recuerda.'
    ]
  },
  {
    titulo: 'El Juicio de Maat',
    texto: [
      'Para pasar la sala de las balanzas, el peso del corazón debe igualarse con pesas de piedra: ni un deben más, ni uno menos.',
      'Mira el papiro del juicio: allí anoté cuánto pesa el corazón del escriba.'
    ]
  },
  {
    titulo: 'Antes del alba',
    texto: [
      'Los sacerdotes entran en el templo al salir el sol. Dentro de una hora, esta cámara dejará de ser secreta.',
      'El Ojo de Horus es lo único capaz de despertar vuestro aparato extraño. Usadlo con respeto.'
    ]
  }
];

export function startMinigame(opts = {}) {
  return abrirLector({
    titulo: 'Carta 15 — Papiro del escriba',
    instr: 'Pasa las páginas con calma. Aquí hay cosas que os harán falta.',
    paginas: PAGINAS,
    tema: 'papiro',
    opts
  });
}

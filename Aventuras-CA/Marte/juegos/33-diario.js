// Carta 33 — Diario de la doctora Reyes: lector. Contiene la amplitud del calibrador (carta 88).
import { abrirLector } from './lector.js';

const PAGINAS = [
  {
    titulo: 'Registro 001',
    texto: [
      'Soy la doctora Reyes, jefa de la colonia Aurora. Si alguien escucha esto: la tormenta de polvo nos obligó a evacuar la cúpula. Cerré las compuertas y dejé el soporte vital en mínimos.',
      'Si volvéis, el sistema os reconocerá por el código de seguridad de la terminal del hangar.'
    ]
  },
  {
    titulo: 'Registro 014 — Viajeros',
    texto: [
      'Llevo años estudiando las leyendas sobre aparatos de portales. Si algún día aparece uno en mi hangar, esto le ayudará.',
      'Calibración del Cronoportal: amplitud 3. La frecuencia la anoté donde nunca se me olvida: en mi tomatera favorita.'
    ]
  },
  {
    titulo: 'Registro 020 — Esclusa',
    texto: [
      'La esclusa del reactor solo se abre con traje presurizado completo, casco incluido. El código está en el plano de la cúpula y va en binario: los ingenieros siempre fueron unos presumidos.',
      'No intentéis cruzar sin el traje. Allí fuera no hay aire.'
    ]
  },
  {
    titulo: 'Registro 021 — Último',
    texto: [
      'El núcleo de fusión sigue en la sala del reactor. Es lo único con energía suficiente para recargar un aparato así.',
      'Quien lo use, que lo use bien. Y que cuide mis tomates. — Reyes'
    ]
  }
];

export function startMinigame(opts = {}) {
  return abrirLector({
    titulo: 'Carta 33 — Diario de la doctora Reyes',
    instr: 'Pasa las páginas con calma. Aquí hay datos que os harán falta.',
    paginas: PAGINAS,
    tema: 'terminal',
    opts
  });
}

window.calentamientoHints = [
  {
    titulo: 'Candado de colores',
    descripcion: 'Cuatro cables alimentan un panel. Solo una combinación de colores restablece la energía.',
    pistas: [
      'Observa los interruptores: cada color se repite el mismo número de veces en filas y columnas.',
      'Hay un patrón creciente de izquierda a derecha: rojo, azul, verde, amarillo.',
      'El cable correcto es aquel que completa la secuencia que falta en la fila inferior.'
    ],
    solucion: 'Pulsa los interruptores rojo, azul, verde y amarillo en ese orden. La luz piloto se enciende.',
    minijuego: {
      etiqueta: 'Practicar panel',
      url: 'minijuegos/candado-colores/index.html'
    }
  },
  {
    titulo: 'Mensaje cifrado',
    descripcion: 'Un walkie-talkie reproduce un mensaje con letras aparentemente aleatorias.',
    pistas: [
      'Algunas letras se repiten cada cuatro posiciones.',
      'Reagrupa el mensaje en columnas de cuatro. Léelo de arriba abajo.',
      'Las iniciales forman la palabra “ECO”. Es una transposición simple.'
    ],
    solucion: 'La frase oculta es “ECO LISTO”. Pulsa el botón ECO del walkie para desbloquear la frecuencia.',
    minijuego: {
      etiqueta: 'Abrir consola',
      url: 'minijuegos/mensaje-cifrado/index.html'
    }
  },
  {
    titulo: 'Candado numérico',
    descripcion: 'Un candado de tres dígitos muestra pictogramas de engranajes, linternas y llaves.',
    pistas: [
      'Cuenta los objetos escondidos en la sala de preparación (los pictogramas son pistas visuales).',
      'Cada icono vale el número de objetos reales que aparece en la ficha de juego.',
      'Engranajes (3), linternas (1) y llaves (5) forman el código.'
    ],
    solucion: 'Introduce el código 3-1-5 para abrir el candado final.',
    minijuego: {
      etiqueta: 'Simular candado',
      url: 'minijuegos/candado-numerico/index.html'
    }
  }
];

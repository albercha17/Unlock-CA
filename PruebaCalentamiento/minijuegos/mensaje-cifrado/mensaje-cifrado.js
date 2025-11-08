(function () {
  const mensajeCodificado = 'EICSOTLO';
  const inputColumnas = document.getElementById('column-count');
  const contenedorCuadricula = document.getElementById('cipher-grid');
  const salidaColumnas = document.getElementById('column-output');
  const botonRenderizar = document.getElementById('render-grid');
  const botonLeer = document.getElementById('read-columns');
  const formulario = document.getElementById('guess-form');
  const entradaRespuesta = document.getElementById('guess-input');
  const mensajeRespuesta = document.getElementById('guess-feedback');

  let resuelto = false;

  function clamp(valor, minimo, maximo) {
    return Math.min(Math.max(valor, minimo), maximo);
  }

  function limpiarCuadricula() {
    contenedorCuadricula.innerHTML = '';
    salidaColumnas.textContent = '';
  }

  function renderizarCuadricula(columnas) {
    limpiarCuadricula();
    const letras = mensajeCodificado.split('');
    const filas = Math.ceil(letras.length / columnas);

    for (let fila = 0; fila < filas; fila += 1) {
      const filaElemento = document.createElement('div');
      filaElemento.className = 'cipher-row';
      filaElemento.style.gridTemplateColumns = `repeat(${columnas}, minmax(3.2rem, 1fr))`;

      for (let columna = 0; columna < columnas; columna += 1) {
        const indice = fila * columnas + columna;
        const celda = document.createElement('div');
        celda.className = 'cipher-cell';
        const letra = letras[indice];
        if (letra) {
          celda.textContent = letra;
        } else {
          celda.classList.add('is-empty');
          celda.textContent = '·';
        }
        filaElemento.appendChild(celda);
      }

      contenedorCuadricula.appendChild(filaElemento);
    }

    salidaColumnas.textContent = 'Coloca las letras y utiliza "Leer por columnas" para descubrir el mensaje.';
  }

  function leerPorColumnas(columnas) {
    if (!contenedorCuadricula.children.length) {
      renderizarCuadricula(columnas);
    }

    const letras = mensajeCodificado.split('');
    const filas = Math.ceil(letras.length / columnas);
    const resultado = [];

    for (let columna = 0; columna < columnas; columna += 1) {
      for (let fila = 0; fila < filas; fila += 1) {
        const indice = fila * columnas + columna;
        if (indice < letras.length) {
          resultado.push(letras[indice]);
        }
      }
    }

    salidaColumnas.textContent = `Lectura por columnas: ${resultado.join('').replace(/(.{3})/g, '$1 ').trim()}`;
  }

  function normalizarTexto(texto) {
    return texto
      .toLocaleLowerCase('es')
      .normalize('NFD')
      .replace(/\p{Diacritic}/gu, '')
      .replace(/[^a-z0-9]/g, '');
  }

  function mostrarRespuesta(tipo, texto) {
    mensajeRespuesta.classList.remove('is-success', 'is-error');
    if (tipo === 'ok') {
      mensajeRespuesta.classList.add('is-success');
    } else if (tipo === 'error') {
      mensajeRespuesta.classList.add('is-error');
    }
    mensajeRespuesta.textContent = texto;
  }

  botonRenderizar.addEventListener('click', () => {
    const columnas = clamp(Number.parseInt(inputColumnas.value, 10) || 4, 2, 6);
    inputColumnas.value = columnas;
    renderizarCuadricula(columnas);
  });

  botonLeer.addEventListener('click', () => {
    const columnas = clamp(Number.parseInt(inputColumnas.value, 10) || 4, 2, 6);
    inputColumnas.value = columnas;
    leerPorColumnas(columnas);
  });

  formulario.addEventListener('submit', (evento) => {
    evento.preventDefault();
    if (resuelto) {
      return;
    }

    const respuesta = normalizarTexto(entradaRespuesta.value);
    const solucion = normalizarTexto('ECO LISTO');

    if (!respuesta) {
      mostrarRespuesta('error', 'Introduce una frase para poder comprobarla.');
      return;
    }

    if (respuesta === solucion) {
      resuelto = true;
      mostrarRespuesta('ok', '¡Correcto! Has sintonizado el canal ECO y desbloqueado la comunicación.');
      entradaRespuesta.disabled = true;
      formulario.querySelector('button[type="submit"]').disabled = true;
    } else {
      mostrarRespuesta('error', 'La frase no coincide. Revisa la tabla y vuelve a intentarlo.');
    }
  });

  // Inicialización
  renderizarCuadricula(Number.parseInt(inputColumnas.value, 10));
  mostrarRespuesta(null, 'Organiza las letras y escribe la frase que descubras.');
})();

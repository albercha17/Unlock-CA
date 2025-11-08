(function () {
  const secuenciaCorrecta = ['rojo', 'azul', 'verde', 'amarillo'];
  const botones = Array.from(document.querySelectorAll('[data-color]'));
  const mensaje = document.querySelector('.pad-feedback');
  const historial = document.getElementById('history');
  const botonReset = document.getElementById('reset');

  let intentoActual = [];

  function setMensaje(tipo, texto) {
    mensaje.classList.remove('is-success', 'is-error');
    if (tipo === 'ok') {
      mensaje.classList.add('is-success');
    } else if (tipo === 'error') {
      mensaje.classList.add('is-error');
    }
    mensaje.textContent = texto;
  }

  function registrarHistorial(colores, esCorrecto) {
    const item = document.createElement('li');
    const texto = colores.map((color) => color.charAt(0).toUpperCase() + color.slice(1)).join(' → ');
    const resultado = esCorrecto ? '✔️ Correcto' : '✖️ Incorrecto';
    item.innerHTML = `<span>${texto}</span> · ${resultado}`;
    if (historial.children.length >= 5) {
      historial.removeChild(historial.lastElementChild);
    }
    historial.insertBefore(item, historial.firstChild);
  }

  function deshabilitarBotones() {
    botones.forEach((boton) => {
      boton.disabled = true;
      boton.classList.add('is-disabled');
    });
    botonReset.disabled = true;
    botonReset.classList.add('is-disabled');
  }

  function reiniciarIntento({ anunciar = true } = {}) {
    intentoActual = [];
    if (anunciar) {
      setMensaje(null, 'Secuencia reiniciada. Prueba un nuevo orden.');
    }
  }

  function comprobarSecuencia() {
    const esCorrecto = secuenciaCorrecta.every((color, index) => intentoActual[index] === color);
    registrarHistorial(intentoActual, esCorrecto);

    if (esCorrecto) {
      setMensaje('ok', '¡Perfecto! Has activado el panel y la luz piloto se enciende.');
      deshabilitarBotones();
    } else {
      setMensaje('error', 'La secuencia no coincide. Ajusta el orden e inténtalo de nuevo.');
      reiniciarIntento({ anunciar: false });
    }
  }

  botones.forEach((boton) => {
    boton.addEventListener('click', () => {
      if (boton.disabled) {
        return;
      }

      intentoActual.push(boton.dataset.color);
      setMensaje(null, `Has pulsado: ${intentoActual.join(' → ')}`);

      if (intentoActual.length === secuenciaCorrecta.length) {
        comprobarSecuencia();
      }
    });
  });

  botonReset.addEventListener('click', () => {
    reiniciarIntento();
  });

  // Mensaje inicial
  setMensaje(null, 'Pulsa los interruptores para probar una combinación.');
})();

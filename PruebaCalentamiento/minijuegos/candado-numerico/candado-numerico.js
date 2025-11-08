(function () {
  const codigoCorrecto = [3, 1, 5];
  const diales = Array.from(document.querySelectorAll('.dial'));
  const historial = document.getElementById('lock-history');
  const mensaje = document.getElementById('lock-feedback');
  const botonProbar = document.getElementById('try-code');
  const botonReiniciar = document.getElementById('reset-code');

  const valores = [0, 0, 0];
  let desbloqueado = false;

  function actualizarDial(indice) {
    const dial = diales[indice];
    const pantalla = dial.querySelector('.dial-display');
    pantalla.textContent = valores[indice];
  }

  function actualizarTodos() {
    valores.forEach((_, indice) => actualizarDial(indice));
  }

  function setMensaje(tipo, texto) {
    mensaje.classList.remove('is-success', 'is-error');
    if (tipo === 'ok') {
      mensaje.classList.add('is-success');
    } else if (tipo === 'error') {
      mensaje.classList.add('is-error');
    }
    mensaje.textContent = texto;
  }

  function registrarIntento(combinacion, esCorrecto) {
    const elemento = document.createElement('li');
    elemento.dataset.success = esCorrecto ? 'true' : 'false';
    const texto = combinacion.join(' - ');
    elemento.textContent = `${texto} ${esCorrecto ? '✔️' : '✖️'}`;
    historial.insertBefore(elemento, historial.firstChild);
    if (historial.children.length > 6) {
      historial.removeChild(historial.lastChild);
    }
  }

  function ajustarValor(indice, delta) {
    if (desbloqueado) {
      return;
    }
    valores[indice] = (valores[indice] + delta + 10) % 10;
    actualizarDial(indice);
  }

  function establecerBloqueo(activo) {
    desbloqueado = activo;
    diales.forEach((dial) => {
      dial.querySelectorAll('.dial-btn').forEach((boton) => {
        boton.disabled = activo;
        if (activo) {
          boton.classList.add('is-disabled');
        } else {
          boton.classList.remove('is-disabled');
        }
      });
    });
    botonProbar.disabled = activo;
  }

  diales.forEach((dial) => {
    const indice = Number.parseInt(dial.dataset.index, 10);
    dial.querySelectorAll('.dial-btn').forEach((boton) => {
      const accion = boton.dataset.action === 'up' ? 1 : -1;
      boton.addEventListener('click', () => {
        ajustarValor(indice, accion);
      });
    });
  });

  botonProbar.addEventListener('click', () => {
    if (desbloqueado) {
      return;
    }
    const combinacion = [...valores];
    const esCorrecto = codigoCorrecto.every((numero, indice) => numero === combinacion[indice]);
    registrarIntento(combinacion, esCorrecto);

    if (esCorrecto) {
      setMensaje('ok', '¡Código 3-1-5 correcto! El candado se abre con un chasquido.');
      establecerBloqueo(true);
    } else {
      setMensaje('error', 'Código incorrecto. Ajusta los diales según los objetos que has contado.');
    }
  });

  botonReiniciar.addEventListener('click', () => {
    valores.fill(0);
    actualizarTodos();
    setMensaje(null, 'Diales reiniciados. Prueba otra combinación.');
    establecerBloqueo(false);
  });

  actualizarTodos();
  setMensaje(null, 'Configura los diales y pulsa «Probar código».');
})();

// cuenta-ui.js — ventana de inicio de sesión y botón de cuenta (se usa en los menús, en «Mis partidas» y al terminar una partida).
import { sesion, entrar, registrar, salir, alCambiarSesion, usuarioRecordado } from './cuenta.js';

const ID_CSS = 'ca-cuenta-css';

function asegurarCss() {
  if (document.getElementById(ID_CSS)) return;
  const l = document.createElement('link');
  l.id = ID_CSS;
  l.rel = 'stylesheet';
  l.href = new URL('../css/cuenta.css', import.meta.url).href;
  document.head.appendChild(l);
}

/** Abre la ventana de login. Devuelve una promesa con el usuario si entra, o null si se cierra. */
export function abrirLogin({ motivo = '' } = {}) {
  asegurarCss();
  return new Promise((resolve) => {
    const fondo = document.createElement('div');
    fondo.className = 'cac-fondo';
    fondo.innerHTML =
      '<div class="cac-caja" role="dialog" aria-modal="true" aria-labelledby="cac-titulo">' +
      '<h2 id="cac-titulo">Tu cuenta</h2>' +
      '<p class="cac-motivo"></p>' +
      '<form novalidate>' +
      '<label>Correo<input type="email" name="email" autocomplete="email" inputmode="email" autocapitalize="off" required></label>' +
      '<label>Contraseña<input type="password" name="clave" autocomplete="current-password" minlength="6" required></label>' +
      '<p class="cac-msg" role="alert" aria-live="assertive"></p>' +
      '<div class="cac-botones"><button type="submit" class="cac-primario" data-accion="entrar">Entrar</button>' +
      '<button type="button" class="cac-sec" data-accion="crear">Crear cuenta</button></div>' +
      '</form>' +
      '<button type="button" class="cac-cerrar">Ahora no</button>' +
      '<p class="cac-nota">Es la misma cuenta que usas en La Arena. Sin cuenta, tus partidas se guardan solo en este dispositivo.</p>' +
      '</div>';
    document.body.appendChild(fondo);
    const form = fondo.querySelector('form');
    const msg = fondo.querySelector('.cac-msg');
    fondo.querySelector('.cac-motivo').textContent = motivo;
    form.elements.email.value = usuarioRecordado();
    const botones = fondo.querySelectorAll('.cac-botones button');
    const cerrar = (u) => { document.removeEventListener('keydown', onTecla); fondo.remove(); resolve(u || null); };
    const onTecla = (e) => { if (e.key === 'Escape') cerrar(null); };
    document.addEventListener('keydown', onTecla);
    fondo.querySelector('.cac-cerrar').addEventListener('click', () => cerrar(null));
    fondo.addEventListener('click', (e) => { if (e.target === fondo) cerrar(null); });

    async function enviar(accion) {
      const email = form.elements.email.value.trim();
      const clave = form.elements.clave.value;
      if (!/^\S+@\S+\.\S+$/.test(email)) { msg.className = 'cac-msg mal'; msg.textContent = 'Escribe un correo válido.'; return; }
      if (clave.length < 6) { msg.className = 'cac-msg mal'; msg.textContent = 'La contraseña debe tener al menos 6 caracteres.'; return; }
      botones.forEach((b) => { b.disabled = true; });
      msg.className = 'cac-msg'; msg.textContent = accion === 'crear' ? 'Creando la cuenta…' : 'Entrando…';
      const r = accion === 'crear' ? await registrar(email, clave) : await entrar(email, clave);
      botones.forEach((b) => { b.disabled = false; });
      if (!r.ok) { msg.className = 'cac-msg mal'; msg.textContent = r.mensaje; return; }
      if (r.pendiente) { msg.className = 'cac-msg ok'; msg.textContent = r.mensaje; return; }
      cerrar(r.usuario);
    }
    form.addEventListener('submit', (e) => { e.preventDefault(); enviar('entrar'); });
    fondo.querySelector('[data-accion="crear"]').addEventListener('click', () => { form.elements.clave.autocomplete = 'new-password'; enviar('crear'); });
    form.elements.email.focus();
  });
}

/** Pinta en `contenedor` un botón «Iniciar sesión» o, con sesión, el correo con enlace a «Mis partidas» y «Salir». */
export function montarCuenta(contenedor, { perfil = 'perfil.html' } = {}) {
  asegurarCss();
  contenedor.classList.add('cac-widget');
  function pintar(u) {
    const email = u ? u.email : '';
    contenedor.replaceChildren();
    if (!u) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'cac-btn';
      b.textContent = usuarioRecordado() ? 'Entrar (' + usuarioRecordado() + ')' : 'Iniciar sesión';
      b.addEventListener('click', async () => { const x = await abrirLogin({ motivo: 'Entra para guardar tus partidas y ver cuánto tardaste en cada una.' }); if (x) pintar(x); });
      contenedor.appendChild(b);
      return;
    }
    const a = document.createElement('a');
    a.className = 'cac-btn';
    a.href = perfil;
    a.textContent = 'Mis partidas · ' + email;
    const s = document.createElement('button');
    s.type = 'button';
    s.className = 'cac-btn suave';
    s.textContent = 'Salir';
    s.addEventListener('click', async () => { await salir(); pintar(null); });
    contenedor.append(a, s);
  }
  pintar(null);
  sesion().then(pintar);
  alCambiarSesion(pintar);
}

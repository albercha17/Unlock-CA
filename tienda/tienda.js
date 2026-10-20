// tienda.js — página de venta: elegir 4 aventuras, subir fotos de los protagonistas y enviar el pedido a Supabase.
// Los pedidos van a la tabla tienda_pedidos y las fotos al bucket privado tienda-fotos (supabase/tienda_pedidos.sql).
// Con ?demo en la URL no se envía nada: sirve para probar la página.
(() => {
  'use strict';

  // ---------- ajustes de venta (cambiar aquí) ----------
  const PRECIOS = { digital: 49, impreso: 79 };            // euros por pack de 4
  const PLAZOS = { digital: '7 días', impreso: '12 días' };
  const POR_PACK = 4;
  const PROTAGONISTAS = 2;
  const FOTOS_MIN = 2;                                      // por protagonista: con dos, ChatGPT acierta más el parecido
  const FOTOS_MAX = 3;
  const LADO_MAX = 1600;                                    // px: las fotos se reducen antes de subirlas

  // La clave «publishable» es pública por diseño: la seguridad la da el RLS de supabase/tienda_pedidos.sql.
  const SUPABASE_URL = 'https://tomwaoskswxfbwxsrkkl.supabase.co';
  const SUPABASE_KEY = 'sb_publishable_GcN8b2gK-85Fqpeomul48g_DhUAPTZY';
  const DEMO = new URLSearchParams(location.search).has('demo');

  const AVENTURAS = [
    { id: 'egipto', nombre: 'El Ojo de Horus', epoca: 'Egipto, 1274 a.C.', dificultad: 3, minutos: 60,
      texto: 'Una cámara secreta bajo el templo de Karnak, una sala funeraria sellada y un amuleto que brilla con luz propia. Una hora antes de que lleguen los sacerdotes.' },
    { id: 'marte', nombre: 'Cúpula Aurora', epoca: 'Marte, 2157', dificultad: 3, minutos: 60,
      texto: 'Una colonia a oscuras por una tormenta de polvo, el oxígeno en las últimas y un núcleo de fusión al otro lado de la esclusa.' },
    { id: 'florencia', nombre: 'El Taller de Leonardo', epoca: 'Florencia, 1503', dificultad: 4, minutos: 60,
      texto: 'De noche, en el taller de Leonardo da Vinci: un cofre con escritura al revés, un león mecánico y una lente perfecta antes del amanecer.' },
    { id: 'dinosaurios', nombre: 'El Valle de los Gigantes', epoca: 'Cretácico, hace 66 millones de años', dificultad: 3, minutos: 90,
      texto: 'Un valle lleno de dinosaurios, un núcleo de energía perdido y un asteroide en el cielo. Hora y media y diez puzles para volver a casa.' },
    { id: 'cuento', nombre: 'El Libro de los Finales Felices', epoca: 'Érase una vez', dificultad: 2, minutos: 75,
      texto: 'Caéis dentro de un libro de cuentos y os convertís en dibujos animados. El libro pierde el color y el último cuento no tiene final.' },
    { id: 'trono', nombre: 'La Corona del Dragón', epoca: 'Reino de Hielo y Fuego', dificultad: 4, minutos: 100,
      texto: 'Una fortaleza en mitad de la ventisca, casas nobles que mienten y un dragón dormido. Cien minutos antes de que la nieve cierre los pasos.' },
    { id: 'pompeya', nombre: 'El Mosaico del Mundo', epoca: 'Pompeya, 79 d.C.', dificultad: 3, minutos: 90,
      texto: 'Una villa romana mientras el Vesubio humea. Los mosaicos están rotos en placas sueltas: juntad las cartas para ver el dibujo entero antes de que caiga la ceniza.' },
    { id: 'arcade', nombre: 'La Última Moneda', epoca: 'Dentro de una recreativa, 1985', dificultad: 3, minutos: 75,
      texto: 'Quedáis atrapados dentro de una máquina recreativa, convertidos en píxeles. Seis niveles para llegar al corazón de la máquina antes del GAME OVER.' },
    { id: 'oeste', nombre: 'El Tren del Oro', epoca: 'Lejano Oeste, 1878', dificultad: 3, minutos: 90,
      texto: 'Un jinete enmascarado se lleva el cristal del Cronoportal. Enganchad un tren, reconoced al bandido en un cartel de «Se busca» y volad un túnel antes de que salga el tren del oro.' },
    { id: 'espia', nombre: 'Operación Cristal', epoca: 'Montecarlo, 1965', dificultad: 3, minutos: 75,
      texto: 'Una noche de gala en el casino y un villano con capa que huye a su yate. Hojas que se superponen, una rejilla de cifrado y cuatro cargas que desactivar antes de medianoche.' },
    { id: 'futbol', nombre: 'La Copa de Cristal', epoca: 'La Final del Siglo, 1970', dificultad: 2, minutos: 90,
      texto: 'El cristal cae dentro de la copa de la final del siglo. Dad la vuelta a los cromos, deducid la alineación del rival, decidid jugadas del VAR y marcad una tanda de penaltis.' },
    { id: 'piratas', nombre: 'El Tesoro de la Isla Calavera', epoca: 'Mar de las Brumas, 1715', dificultad: 3, minutos: 90,
      texto: 'Un loro se lleva el cristal al cofre de la capitana Bruma. Encontrad el tesoro del capitán Calavera antes de que la marea cubra su cueva, con cartas que se pliegan como mapas antiguos.' },
    { id: 'juguetes', nombre: 'La Noche de los Juguetes', epoca: 'El Cuarto de Leo, 1995', dificultad: 1, minutos: 60,
      texto: 'Os convertís en una muñeca de trapo y un robot de hojalata la noche antes de una mudanza. La más fácil: perfecta para estrenarse o para jugar con peques.' },
  ];
  const portada = (id) => `../juegos/aventuras-ca/${id}/img/P.jpg`;

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const form = $('#form-pedido');
  const elegidas = new Set();
  const protas = Array.from({ length: PROTAGONISTAS }, () => ({ fotos: [] }));   // fotos: [{ blob, url }]

  // ---------- precios y plazos en los textos ----------
  $$('[data-precio]').forEach((el) => { el.textContent = `${PRECIOS[el.dataset.precio]} €`; });
  $$('[data-plazo]').forEach((el) => { el.textContent = PLAZOS[el.dataset.plazo]; });

  // ---------- aventuras: tarjetas de presentación y selector del formulario ----------
  const puntos = (n) => Array.from({ length: 5 }, (_, i) => `<i class="${i < n ? 'on' : ''}"></i>`).join('');

  // juegos/catalogo.json manda: pone al día dificultad y minutos y añade cualquier aventura nueva que aún no tenga texto aquí
  async function completarConCatalogo() {
    try {
      const cat = await (await fetch('../juegos/catalogo.json')).json();
      for (const j of cat) {
        if (!j.ruta.startsWith('juegos/aventuras-ca/')) continue;   // solo las del Cronoportal se personalizan
        const a = AVENTURAS.find((x) => x.id === j.id);
        if (a) { a.dificultad = j.dificultad; a.minutos = j.minutos; continue; }
        const [epoca, nombre] = j.nombre.includes(':') ? j.nombre.split(/:\s*/, 2) : ['Nueva aventura', j.nombre];
        AVENTURAS.push({ id: j.id, nombre, epoca, dificultad: j.dificultad, minutos: j.minutos,
          texto: `Un nuevo salto del Cronoportal: ${j.cartas} cartas y ${j.minutos} minutos para volver a casa.` });
      }
    } catch { /* sin catálogo: las de la lista */ }
  }

  function pintarAventuras() {
  $('#lista-aventuras').innerHTML = AVENTURAS.map((a) => `
    <article class="aventura" data-id="${a.id}" data-dif="${a.dificultad}" data-buscar="${a.id}">
      <span class="sello">En vuestro pack</span>
      <img class="aventura-img" src="${portada(a.id)}" alt="Portada de ${a.nombre}" loading="lazy">
      <div class="aventura-cuerpo">
        <span class="aventura-epoca">${a.epoca}</span>
        <h3>${a.nombre}</h3>
        <p title="${a.texto}">${a.texto}</p>
        <div class="aventura-meta">
          <span class="dificultad" title="Dificultad ${a.dificultad} de 5">Dificultad ${puntos(a.dificultad)}</span>
          <span>${a.minutos} min</span>
        </div>
        <button class="btn btn-linea btn-sm" type="button" data-alternar="${a.id}">Añadir al pack</button>
      </div>
    </article>`).join('');

  $('#selector-aventuras').innerHTML = AVENTURAS.map((a) => `
    <label class="opcion" data-dif="${a.dificultad}" data-buscar="${a.epoca} ${a.id}">
      <input type="checkbox" name="aventura" value="${a.id}">
      <img src="${portada(a.id)}" alt="" loading="lazy">
      <span>${a.nombre}</span>
    </label>`).join('');
  $$('[data-n-aventuras]').forEach((el) => { el.textContent = AVENTURAS.length; });
  filtros.forEach((f) => f && f.aplicar());
  }
  // buscador y filtro de dificultad (assets/js/filtro-juegos.js): cada vez hay más aventuras
  const filtros = [];
  pintarAventuras();
  if (window.FiltroJuegos) {
    filtros.push(window.FiltroJuegos.montar($('#lista-aventuras'), { items: '.aventura', nombre: 'aventura' }));
    filtros.push(window.FiltroJuegos.montar($('#selector-aventuras'), { items: '.opcion', nombre: 'aventura' }));
  }
  completarConCatalogo().then(() => { pintarAventuras(); pintarEleccion(); });

  function alternar(id, quiere) {
    if (quiere && elegidas.size >= POR_PACK) return false;
    if (quiere) elegidas.add(id); else elegidas.delete(id);
    pintarEleccion();
    return true;
  }

  function pintarEleccion() {
    const lleno = elegidas.size >= POR_PACK;
    $$('#selector-aventuras input').forEach((i) => {
      i.checked = elegidas.has(i.value);
      i.disabled = lleno && !i.checked;
    });
    $$('.aventura').forEach((c) => {
      const si = elegidas.has(c.dataset.id);
      c.classList.toggle('elegida', si);
      const b = $('[data-alternar]', c);
      b.textContent = si ? '✓ En el pack' : (lleno ? 'Pack completo' : 'Añadir al pack');
      b.disabled = lleno && !si;
    });
    const cont = $('#contador');
    cont.textContent = `${elegidas.size}/${POR_PACK}`;
    cont.classList.toggle('completo', lleno);
    if (lleno) error('aventuras', '');
    pintarResumen();
  }

  $('#selector-aventuras').addEventListener('change', (e) => {
    if (e.target.name === 'aventura') alternar(e.target.value, e.target.checked);
  });
  $('#lista-aventuras').addEventListener('click', (e) => {
    const b = e.target.closest('[data-alternar]');
    if (!b) return;
    const id = b.dataset.alternar;
    alternar(id, !elegidas.has(id));
    if (elegidas.size === POR_PACK && elegidas.has(id)) aviso(`¡Pack completo! Bajad a «Cread vuestro pack» para terminar.`);
  });

  // ---------- protagonistas ----------
  $('#protas').innerHTML = protas.map((_, i) => `
    <div class="prota" data-prota="${i}">
      <h4>Protagonista ${i + 1}</h4>
      <label>Nombre
        <input name="p${i}-nombre" maxlength="60" placeholder="${i === 0 ? 'Lucía' : 'Marcos'}">
        <span class="error" data-error="p${i}-nombre"></span>
      </label>
      <div>
        <div class="fotos" data-fotos="${i}"></div>
        <span class="error" data-error="p${i}-fotos"></span>
      </div>
      <label>Es…
        <select name="p${i}-genero">
          <option value="">Elegid</option>
          <option value="mujer">Mujer</option>
          <option value="hombre">Hombre</option>
          <option value="niña">Niña</option>
          <option value="niño">Niño</option>
        </select>
        <span class="error" data-error="p${i}-genero"></span>
      </label>
      <label>Edad aproximada <small>(para dibujaros bien)</small>
        <input name="p${i}-edad" maxlength="20" inputmode="numeric" placeholder="${i === 0 ? '34' : '36'}">
      </label>
      <label>Algo sobre esta persona <small>(profesión, aficiones…)</small>
        <input name="p${i}-sobre" maxlength="200" placeholder="${i === 0 ? 'Enfermera, le encantan los gatos' : 'Profesor de música, fan de Tolkien'}">
      </label>
    </div>`).join('');

  function pintarFotos(i) {
    const caja = $(`[data-fotos="${i}"]`);
    const p = protas[i];
    caja.innerHTML = p.fotos.map((f, j) => `
      <div class="foto-mini"><img src="${f.url}" alt="Foto ${j + 1} de protagonista ${i + 1}">
        <button type="button" data-quitar="${i}-${j}" aria-label="Quitar foto ${j + 1}">✕</button></div>`).join('')
      + (p.fotos.length < FOTOS_MAX
        ? `<label class="subir"><span><b>+</b>${p.fotos.length >= FOTOS_MIN ? 'Otra foto (opcional)' : `Foto ${p.fotos.length + 1} de ${FOTOS_MIN}`}</span><input type="file" accept="image/*" data-subir="${i}" ${FOTOS_MAX - p.fotos.length > 1 ? 'multiple' : ''}></label>`
        : '');
    pintarResumen();
  }

  $('#protas').addEventListener('change', async (e) => {
    const inp = e.target.closest('[data-subir]');
    if (!inp) return;
    const i = +inp.dataset.subir;
    const archivos = [...inp.files].slice(0, FOTOS_MAX - protas[i].fotos.length);
    error(`p${i}-fotos`, '');
    for (const a of archivos) {
      if (!a.type.startsWith('image/')) { error(`p${i}-fotos`, 'Eso no parece una foto.'); continue; }
      try {
        const blob = await reducir(a);
        protas[i].fotos.push({ blob, url: URL.createObjectURL(blob) });
      } catch {
        error(`p${i}-fotos`, 'No pudimos abrir esa foto. Probad con otra (JPG o PNG).');
      }
    }
    pintarFotos(i);
  });
  $('#protas').addEventListener('click', (e) => {
    const b = e.target.closest('[data-quitar]');
    if (!b) return;
    const [i, j] = b.dataset.quitar.split('-').map(Number);
    URL.revokeObjectURL(protas[i].fotos[j].url);
    protas[i].fotos.splice(j, 1);
    pintarFotos(i);
  });
  $('#protas').addEventListener('input', pintarResumen);

  // Reduce la foto a LADO_MAX px y la pasa a JPEG: sube rápido y no supera el límite del bucket.
  function reducir(archivo) {
    return new Promise((ok, mal) => {
      const img = new Image();
      const url = URL.createObjectURL(archivo);
      img.onload = () => {
        const k = Math.min(1, LADO_MAX / Math.max(img.naturalWidth, img.naturalHeight));
        const c = document.createElement('canvas');
        c.width = Math.round(img.naturalWidth * k);
        c.height = Math.round(img.naturalHeight * k);
        c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
        URL.revokeObjectURL(url);
        c.toBlob((b) => (b ? ok(b) : mal(new Error('sin imagen'))), 'image/jpeg', 0.88);
      };
      img.onerror = () => { URL.revokeObjectURL(url); mal(new Error('foto ilegible')); };
      img.src = url;
    });
  }

  // ---------- formato ----------
  const formato = () => form.elements.formato.value;
  form.addEventListener('change', (e) => {
    if (e.target.name === 'formato') {
      $('#campo-direccion').hidden = formato() !== 'impreso';
      pintarResumen();
    }
  });
  $$('[data-elegir-formato]').forEach((a) => a.addEventListener('click', () => {
    form.elements.formato.value = a.dataset.elegirFormato;
    form.dispatchEvent(new Event('change'));
    $('#campo-direccion').hidden = formato() !== 'impreso';
    pintarResumen();
  }));
  // la fecha deseada no puede ser anterior a hoy
  form.elements.fecha_deseada.min = new Date().toISOString().slice(0, 10);

  // ---------- resumen ----------
  function pintarResumen() {
    const lista = $('#resumen-lista');
    const nombres = AVENTURAS.filter((a) => elegidas.has(a.id)).map((a) => `<li>${a.nombre}</li>`);
    const faltan = POR_PACK - elegidas.size;
    lista.innerHTML = nombres.join('') + (faltan ? `<li class="vacio">Faltan ${faltan} aventura${faltan > 1 ? 's' : ''}</li>` : '');
    const nombresProtas = protas.map((_, i) => (form.elements[`p${i}-nombre`]?.value || '').trim()).filter(Boolean);
    const fotos = protas.reduce((n, p) => n + p.fotos.length, 0);
    $('#resumen-protas').textContent = nombresProtas.length ? `${nombresProtas.join(' y ')} · ${fotos} foto${fotos === 1 ? '' : 's'}` : '—';
    $('#resumen-formato').textContent = formato() === 'impreso' ? 'Impreso en caja' : 'Digital';
    $('#resumen-precio').textContent = `${PRECIOS[formato()]} €`;
  }

  // ---------- validación ----------
  function error(campo, msg) {
    const el = $(`[data-error="${campo}"]`);
    if (el) el.textContent = msg;
    const inp = form.elements[campo];
    if (inp && inp.classList) inp.classList.toggle('invalido', !!msg);
  }

  function validar() {
    const fallos = [];
    const f = form.elements;
    const marca = (campo, msg) => { error(campo, msg); if (msg) fallos.push(campo); };
    marca('aventuras', elegidas.size === POR_PACK ? '' : `Elegid ${POR_PACK} aventuras (lleváis ${elegidas.size}).`);
    protas.forEach((p, i) => {
      marca(`p${i}-nombre`, f[`p${i}-nombre`].value.trim() ? '' : 'Falta el nombre.');
      marca(`p${i}-fotos`, p.fotos.length >= FOTOS_MIN ? ''
        : `Faltan fotos: ${p.fotos.length ? 'falta 1 más' : `subid ${FOTOS_MIN}`} (dos fotos distintas de la cara).`);
      marca(`p${i}-genero`, f[`p${i}-genero`].value ? '' : 'Elegid una opción: nos ayuda a dibujarle bien.');
    });
    marca('direccion', formato() === 'impreso' && !f.direccion.value.trim() ? 'Necesitamos la dirección para enviar la caja.' : '');
    marca('nombre', f.nombre.value.trim() ? '' : 'Falta vuestro nombre.');
    marca('email', /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.email.value.trim()) ? '' : 'Revisad el correo: ahí os mandaremos la prueba.');
    marca('acepta', f.acepta.checked ? '' : 'Necesitamos vuestro permiso para usar las fotos.');
    return fallos;
  }

  // ---------- envío ----------
  let cliente = null;
  function supa() {
    if (!cliente) {
      if (!window.supabase || !window.supabase.createClient) throw new Error('No se pudo cargar la conexión. Revisad internet y recargad la página.');
      cliente = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY, { auth: { persistSession: false, autoRefreshToken: false } });
    }
    return cliente;
  }

  const nuevoId = () => (crypto.randomUUID ? crypto.randomUUID()
    : 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => { const r = Math.random() * 16 | 0; return (c === 'x' ? r : (r & 3 | 8)).toString(16); }));

  function traducir(err) {
    const m = (err && (err.message || err.error || String(err))) || '';
    if (/bucket not found|relation .* does not exist|schema cache|Could not find the table/i.test(m)) return 'La tienda todavía no está lista para recibir pedidos. Probad de nuevo en unas horas.';
    if (/row-level security|violates/i.test(m)) return 'El pedido no pasó una comprobación. Revisad los datos y volved a intentarlo.';
    if (/Failed to fetch|NetworkError|network/i.test(m)) return 'Sin conexión. Revisad internet y volved a intentarlo.';
    return m || 'Algo falló al enviar el pedido. Volved a intentarlo.';
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    $('#error-envio').textContent = '';
    const fallos = validar();
    if (fallos.length) {
      const primero = $(`[data-error="${fallos[0]}"]`);
      (primero.closest('.prota, label, fieldset') || primero).scrollIntoView({ behavior: 'smooth', block: 'center' });
      $('#error-envio').textContent = 'Falta algún dato: está marcado en rojo.';
      return;
    }

    const btn = $('#enviar');
    btn.disabled = true;
    const f = form.elements;
    const id = nuevoId();
    try {
      const datosProtas = [];
      const total = protas.reduce((n, p) => n + p.fotos.length, 0);
      let subidas = 0;
      for (const [i, p] of protas.entries()) {
        const rutas = [];
        for (const [j, foto] of p.fotos.entries()) {
          btn.textContent = `Subiendo fotos… ${++subidas}/${total}`;
          const ruta = `${id}/p${i + 1}-${j + 1}.jpg`;
          if (!DEMO) {
            const { error: err } = await supa().storage.from('tienda-fotos').upload(ruta, foto.blob, { contentType: 'image/jpeg', upsert: false });
            if (err) throw err;
          }
          rutas.push(ruta);
        }
        datosProtas.push({ nombre: f[`p${i}-nombre`].value.trim(), genero: f[`p${i}-genero`].value, edad: f[`p${i}-edad`].value.trim(), sobre: f[`p${i}-sobre`].value.trim(), fotos: rutas });
      }

      btn.textContent = 'Enviando pedido…';
      const fila = {
        id,
        nombre: f.nombre.value.trim(),
        email: f.email.value.trim(),
        telefono: f.telefono.value.trim() || null,
        aventuras: AVENTURAS.filter((a) => elegidas.has(a.id)).map((a) => a.id),
        protagonistas: datosProtas,
        formato: formato(),
        precio: PRECIOS[formato()],
        ocasion: f.ocasion.value || null,
        fecha_deseada: f.fecha_deseada.value || null,
        dedicatoria: f.dedicatoria.value.trim() || null,
        direccion: formato() === 'impreso' ? f.direccion.value.trim() : null,
        notas: f.notas.value.trim() || null,
        acepta: true,
      };
      if (DEMO) { console.info('[demo] pedido que se enviaría:', fila); await new Promise((r) => setTimeout(r, 600)); }
      else {
        const { error: err } = await supa().from('tienda_pedidos').insert(fila);
        if (err) throw err;
      }

      $('#gracias-codigo').textContent = id.slice(0, 8).toUpperCase();
      $('#gracias-email').textContent = fila.email;
      form.hidden = true;
      const gracias = $('#gracias');
      gracias.hidden = false;
      gracias.focus();
      gracias.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } catch (err) {
      console.error(err);
      $('#error-envio').textContent = traducir(err);
      btn.disabled = false;
      btn.textContent = 'Enviar pedido';
    }
  });

  // ---------- aviso flotante ----------
  let temporizador;
  function aviso(texto) {
    let el = $('#aviso');
    if (!el) {
      el = document.createElement('div');
      el.id = 'aviso';
      el.setAttribute('role', 'status');
      el.style.cssText = 'position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:50;max-width:calc(100% - 32px);padding:12px 20px;border-radius:999px;background:#e9b65c;color:#2a1a04;font-weight:600;box-shadow:0 12px 30px rgba(0,0,0,.45);transition:opacity .3s';
      document.body.append(el);
    }
    el.textContent = texto;
    el.style.opacity = '1';
    clearTimeout(temporizador);
    temporizador = setTimeout(() => { el.style.opacity = '0'; }, 3200);
  }

  protas.forEach((_, i) => pintarFotos(i));
  pintarEleccion();
})();

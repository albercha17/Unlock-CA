// Ayudas comunes de los minijuegos de «Cuento»: las letras del libro (una por puzle resuelto) y las imágenes opcionales.
// - guardarLetra(carta, letra): el libro recuerda la letra aunque se cierre y se vuelva a abrir el minijuego.
// - leerLetras(): {carta: letra} de lo ya resuelto en ESTA partida (se ignoran las letras anteriores al último «Empezar»).
// - conImagen(contenedor, nombre, opciones): añade ./img/ui/<nombre> solo si está en img/ui/lista.json (así no hay peticiones 404).
//   Si la imagen no existe, el dibujo CSS de respaldo del minijuego se ve igual de bien.

const CLAVE = 'cuento-letras';

/** Marca de tiempo del último «Empezar» (la app guarda la partida en localStorage con ese dato). */
function inicioPartida() {
  try {
    const g = JSON.parse(localStorage.getItem('ca-partida:' + location.pathname.replace(/index\.html$/, '')) || 'null');
    return g && g.empezada ? g.empezada : 0;
  } catch (e) { return 0; }
}

export function guardarLetra(carta, letra) {
  try {
    const l = JSON.parse(localStorage.getItem(CLAVE) || '{}');
    l[String(carta)] = { l: letra, t: Date.now() };
    localStorage.setItem(CLAVE, JSON.stringify(l));
  } catch (e) { /* sin almacenamiento: el jugador aún tiene la letra en el mensaje */ }
}

export function leerLetras() {
  try {
    const l = JSON.parse(localStorage.getItem(CLAVE) || '{}');
    const desde = inicioPartida();
    const r = {};
    Object.keys(l).forEach((c) => { if (l[c] && l[c].t >= desde) r[c] = l[c].l; });
    return r;
  } catch (e) { return {}; }
}

let listaPromesa = null;
function lista() {
  if (!listaPromesa) {
    listaPromesa = fetch('./img/ui/lista.json', { cache: 'no-store' }).then((r) => (r.ok ? r.json() : [])).catch(() => []);
  }
  return listaPromesa;
}

/** Añade la imagen ./img/ui/<nombre> dentro de `cont` si existe. Devuelve una promesa con el <img> o null. */
export async function conImagen(cont, nombre, { clase = 'cu-img', mezcla = 'screen', alt = '' } = {}) {
  const l = await lista();
  if (!Array.isArray(l) || !l.includes(nombre)) return null;
  const im = document.createElement('img');
  im.className = clase;
  im.alt = alt;
  im.src = './img/ui/' + nombre;
  im.style.mixBlendMode = mezcla;
  cont.appendChild(im);
  return im;
}

export function estilo(id, css) {
  if (document.getElementById(id)) return;
  const s = document.createElement('style');
  s.id = id;
  s.textContent = css;
  document.head.appendChild(s);
}

export const NOMBRES_COLUMNA = 'ABCDEFGH';

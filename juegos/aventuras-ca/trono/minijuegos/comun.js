// Ayudas comunes de los minijuegos de «Trono»: palabras de la profecía y dibujos opcionales.
//
// Palabras de la profecía: cada puzle de la fortaleza, al resolverse, enseña una palabra y la guarda en el navegador; la carta 84 las recoge
// (si alguien cierra la app, las palabras ya ganadas siguen ahí).
//
// Dibujos opcionales: los minijuegos se ven bien sin imágenes (formas CSS/SVG de respaldo). Si existe el dibujo en ./img/ui/<nombre>
// (generado con ChatGPT más adelante, ver PENDIENTE-IMAGENES.md), se usa encima.

const CLAVE = 'ca-palabra:trono:';

export function guardarPalabra(carta, palabra) {
  try { localStorage.setItem(CLAVE + carta, palabra); } catch (e) { /* sin almacenamiento: la partida sigue, pero la carta 84 no podrá recogerla */ }
}

export function leerPalabra(carta) {
  try { return localStorage.getItem(CLAVE + carta) || ''; } catch (e) { return ''; }
}

let indice = null;
function cargarIndice() {
  // ./img/ui/disponibles.json lista los dibujos ya generados (lo escribe herramientas/indice_imagenes.py): así no se piden ficheros que no existen
  if (!indice) indice = fetch('./img/ui/disponibles.json', { cache: 'no-store' }).then(r => (r.ok ? r.json() : [])).catch(() => []);
  return indice;
}

/** Si el dibujo ./img/ui/<nombre> está disponible, lo pone como fondo de `el` (variable --img) y marca el elemento con la clase `img`. */
export function conImagen(el, nombre) {
  cargarIndice().then(lista => {
    if (lista.includes(nombre)) {
      el.style.setProperty('--img', 'url("./img/ui/' + nombre + '")');
      el.classList.add('img');
    }
  });
}

/** Como ui.textura, pero solo si la textura está disponible. */
export function texturaSi(ui, nombre, opciones) {
  cargarIndice().then(lista => { if (lista.includes(nombre)) ui.textura(nombre, opciones); });
}

/** Añade al cuerpo del minijuego una hoja de estilos propia. */
export function estilo(body, css) {
  const s = document.createElement('style');
  s.textContent = css;
  body.appendChild(s);
}

/** Utilidad para los solucionadores y las pruebas: columna A-F -> índice. */
export const LETRAS = 'ABCDEFGH';

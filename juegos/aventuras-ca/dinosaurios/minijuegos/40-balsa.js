// Carta 40 — Balsa del vado: cruzar el río con un compsognato, un bebé de driosaurio y un cesto de helechos.
// La balsa lleva a Cristina y Alberto (siempre) y a una sola criatura. Normas del diario (carta 42):
//   - el compsognato ataca al bebé si se quedan solos; el bebé se come los helechos si se quedan solos.
// Solución mínima: bebé, (vacío), compsognato, bebé de vuelta, helechos, (vacío), bebé (siete viajes).
import { openGame } from './ui.js';

const ITEMS = [
  { k: 'compsognato', nombre: 'Compsognato' },
  { k: 'driosaurio', nombre: 'Bebé de driosaurio' },
  { k: 'helechos', nombre: 'Cesto de helechos' }
];
const IMG = './img/ui/';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 40 — Balsa del vado',
    instr: 'Pasa a las tres criaturas a la otra orilla. Toca una criatura para subirla a la balsa (o bajarla) y pulsa Cruzar.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .bal-rio{position:relative;display:grid;grid-template-columns:.85fr 1.6fr .85fr;max-width:360px;height:250px;margin:0 auto 8px;border-radius:12px;border:3px solid #3a2a12;overflow:hidden;box-shadow:inset 0 0 22px rgba(0,0,0,.6)}
    .bal-orilla{position:relative;display:flex;flex-direction:column;justify-content:space-evenly;align-items:center;background:linear-gradient(rgba(10,18,6,.25),rgba(10,18,6,.45)),url(${IMG}orilla.jpg) center/cover}
    .bal-agua{position:relative;background:linear-gradient(rgba(6,26,30,.2),rgba(6,26,30,.35)),url(${IMG}rio.jpg) center/cover}
    .bal-item{position:relative;width:66px;height:58px;padding:0;border:2px solid transparent;border-radius:10px;background:none;cursor:pointer}
    .bal-item img{display:block;width:100%;height:100%;object-fit:contain;mix-blend-mode:screen;filter:drop-shadow(0 3px 3px rgba(0,0,0,.6))}
    .bal-item.cargado{border-color:#ffd27a;background:rgba(0,0,0,.25)}
    .bal-balsa{position:absolute;top:50%;width:88px;height:100px;margin-top:-50px;transition:left .9s ease-in-out}
    .bal-balsa img.base{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;mix-blend-mode:screen}
    .bal-carga{position:absolute;left:50%;top:-6px;transform:translateX(-50%);width:70px;height:56px}
    .bal-carga .bal-item{width:100%;height:100%}
    .bal-info{color:#d6e6c0;font-size:.85rem;text-align:center;margin-bottom:6px}
  `;
  ui.body.appendChild(style);

  const rio = document.createElement('div');
  rio.className = 'bal-rio';
  const izq = document.createElement('div');
  izq.className = 'bal-orilla';
  const agua = document.createElement('div');
  agua.className = 'bal-agua';
  const der = document.createElement('div');
  der.className = 'bal-orilla';
  rio.append(izq, agua, der);
  const balsa = document.createElement('div');
  balsa.className = 'bal-balsa';
  balsa.innerHTML = '<img class="base" alt="Balsa" src="' + IMG + 'balsa.jpg">';
  agua.appendChild(balsa);
  const info = document.createElement('div');
  info.className = 'bal-info';
  ui.body.append(rio, info);

  const orilla = { compsognato: 0, driosaurio: 0, helechos: 0 };   // 0 = izquierda, 1 = derecha
  let lado = 0;                // orilla de la balsa
  let carga = null;            // criatura a bordo
  let viajes = 0;
  let ocupado = false;
  let resuelto = false;

  function boton(it) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'bal-item' + (carga === it.k ? ' cargado' : '');
    b.dataset.k = it.k;
    b.setAttribute('aria-label', it.nombre);
    b.innerHTML = '<img alt="" src="' + IMG + 'criaturas/' + it.k + '.jpg">';
    b.addEventListener('click', () => {
      if (ocupado || resuelto) return;
      if (carga === it.k) { carga = null; }
      else if (carga) { ui.say('En la balsa solo cabe una criatura. Baja primero la que va a bordo.', 'bad'); return; }
      else if (orilla[it.k] !== lado) { ui.say('Esa criatura está en la otra orilla.', 'bad'); return; }
      else carga = it.k;
      ui.say('');
      pintar();
    });
    return b;
  }

  function pintar() {
    izq.innerHTML = '';
    der.innerHTML = '';
    ITEMS.forEach(it => {
      if (carga === it.k) return;
      (orilla[it.k] === 0 ? izq : der).appendChild(boton(it));
    });
    balsa.querySelectorAll('.bal-carga').forEach(n => n.remove());
    if (carga) {
      const c = document.createElement('div');
      c.className = 'bal-carga';
      c.appendChild(boton(ITEMS.find(i => i.k === carga)));
      balsa.appendChild(c);
    }
    balsa.style.left = lado === 0 ? '4px' : 'calc(100% - 92px)';
    balsa.dataset.lado = String(lado);
    info.textContent = 'Viajes: ' + viajes + ' · La balsa está en la orilla ' + (lado === 0 ? 'izquierda' : 'derecha');
  }

  function peligro(l) {
    // lo que queda en la orilla l sin la balsa
    const en = k => orilla[k] === l;
    if (en('compsognato') && en('driosaurio')) return 'El compsognato se abalanza sobre el bebé de driosaurio mientras remáis. Hay que volver a empezar el viaje.';
    if (en('driosaurio') && en('helechos')) return 'El bebé de driosaurio devora los helechos mientras remáis. Hay que volver a empezar el viaje.';
    return null;
  }

  async function cruzar() {
    if (ocupado || resuelto) return;
    const origen = lado;
    ocupado = true;
    ui.say('');
    lado = 1 - lado;
    if (carga) orilla[carga] = lado;
    pintar();
    await new Promise(r => setTimeout(r, 950));
    const mal = peligro(origen);
    if (mal) {
      // se deshace el viaje
      if (carga) orilla[carga] = origen;
      lado = origen;
      ui.say(mal, 'bad');
    } else {
      viajes++;
      carga = null;
      if (ITEMS.every(i => orilla[i.k] === 1)) {
        resuelto = true;
        pintar();
        ui.say('¡Las tres criaturas han cruzado sanas y salvas! En la otra orilla se ve la tienda del laboratorio de Ibarra. Coged la carta 44.', 'ok');
        ocupado = false;
        return;
      }
    }
    ocupado = false;
    pintar();
  }

  ui.button('Cruzar el río', 'primary', cruzar);
  ui.button('Empezar de nuevo', 'ghost', () => {
    if (ocupado || resuelto) return;
    ITEMS.forEach(i => { orilla[i.k] = 0; });
    lado = 0; carga = null; viajes = 0;
    ui.say('');
    pintar();
  });

  pintar();
  return { close: ui.close };
}

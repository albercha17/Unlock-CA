// Carta 20 — El puente del troll: cuatro duendes cruzan con un único farolillo-luciérnaga. Cruzan de uno en uno o de dos en dos
// (al paso del más lento) y el farolillo hay que devolverlo. Los tiempos están en la carta 18 (la app no los enseña) y el límite es de 15 minutos.
// Solución mínima: 15 minutos (única en tiempo). Letra del libro: E.
import { openGame } from './ui.js';
import { guardarLetra, estilo, conImagen } from './libro.js';

const LETRA = 'E';
const LIMITE = 15;
const DUENDES = [
  { n: 'Bigotes', t: 1, color: '#e88b3a', forma: 'bigote' },
  { n: 'Pétalo', t: 2, color: '#ee6fa6', forma: 'petalo' },
  { n: 'Gruñón', t: 5, color: '#6aa84f', forma: 'ceño' },
  { n: 'Abuela Musgo', t: 8, color: '#5b8f8a', forma: 'moño' }
];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 20 — El puente del troll',
    instr: 'Pasad a los cuatro duendes al otro lado antes de que amanezca. Solo hay un farolillo: cruzan de uno en uno o de dos en dos, y alguien debe devolverlo. Los tiempos están en la carta 18.',
    ...opts
  });
  estilo('cu-puente-estilo', `
    .pue-escena{display:grid;grid-template-columns:1fr 54px 1fr;gap:6px;align-items:stretch;margin-bottom:8px}
    .pue-orilla{background:linear-gradient(180deg,rgba(60,40,120,.55),rgba(30,18,70,.7));border:1px solid rgba(255,224,138,.35);border-radius:12px;min-height:210px;padding:8px;display:flex;flex-direction:column;gap:8px;align-items:stretch}
    .pue-orilla h4{margin:0;font-size:.78rem;color:#ffe08a;letter-spacing:.04em;font-weight:600}
    .pue-rio{border-radius:10px;background:repeating-linear-gradient(0deg,#2b2f7a 0 8px,#3a40a0 8px 16px);display:flex;align-items:center;justify-content:center;font-size:.68rem;color:#bcc3ff;text-align:center;position:relative}
    .pue-rio::after{content:"";position:absolute;left:-4px;right:-4px;top:42%;height:16px;background:linear-gradient(180deg,#9a8f80,#6c6358);border-radius:4px;box-shadow:0 2px 0 #3a342c}
    .pue-duende{display:flex;align-items:center;gap:8px;width:100%;min-height:52px;border-radius:12px;border:2px solid rgba(255,224,138,.35);background:rgba(255,255,255,.08);color:#fff;font:600 .9rem inherit;font-family:inherit;padding:4px 8px;cursor:pointer;text-align:left}
    .pue-duende.sel{border-color:#ffe08a;box-shadow:0 0 14px rgba(255,224,138,.6);background:rgba(255,224,138,.18)}
    .pue-cara{position:relative;width:34px;height:34px;flex:none;border-radius:50% 50% 46% 46%;background:var(--c,#e88b3a);border:2px solid rgba(0,0,0,.35)}
    .pue-cara::before,.pue-cara::after{content:"";position:absolute;top:13px;width:5px;height:5px;border-radius:50%;background:#1a0e30}
    .pue-cara::before{left:8px}.pue-cara::after{right:8px}
    .pue-cara i{position:absolute;left:50%;transform:translateX(-50%);display:block}
    .pue-cara i.bigote{bottom:6px;width:16px;height:4px;border-radius:0 0 8px 8px;background:#3a2410}
    .pue-cara i.petalo{top:-6px;width:12px;height:12px;border-radius:50% 0;background:#fff2a8;transform:translateX(-50%) rotate(45deg)}
    .pue-cara i.ceño{top:9px;width:24px;height:3px;background:#1a0e30;transform:translateX(-50%) rotate(-6deg)}
    .pue-cara i.moño{top:-8px;width:16px;height:12px;border-radius:50%;background:#d9d9d9;border:1px solid #888}
    .pue-farol{display:flex;align-items:center;gap:6px;font-size:.78rem;color:#ffe08a;min-height:26px}
    .pue-farol b{width:14px;height:14px;border-radius:50%;background:radial-gradient(circle,#fffbc0,#ffd23a 60%,transparent 70%);box-shadow:0 0 12px #ffe27a;display:inline-block}
    .pue-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.5;pointer-events:none;border-radius:10px}
  `);

  const escena = document.createElement('div');
  escena.className = 'pue-escena';
  const izq = document.createElement('div');
  izq.className = 'pue-orilla';
  izq.dataset.lado = 'izq';
  const rio = document.createElement('div');
  rio.className = 'pue-rio';
  rio.textContent = 'puente del troll';
  const der = document.createElement('div');
  der.className = 'pue-orilla';
  der.dataset.lado = 'der';
  escena.append(izq, rio, der);
  ui.body.appendChild(escena);
  conImagen(rio, 'puente.jpg', { clase: 'pue-img', mezcla: 'screen' });

  const info = document.createElement('div');
  info.style.cssText = 'font-size:.82rem;color:#d8e2ee;margin:4px 0';
  ui.body.appendChild(info);

  let lado, farol, sel, gastado, resuelto;

  function pintar() {
    [['izq', izq, 'Orilla de la aldea'], ['der', der, 'Otra orilla']].forEach(([o, cont, titulo]) => {
      cont.replaceChildren();
      const h = document.createElement('h4');
      h.textContent = titulo;
      cont.appendChild(h);
      const f = document.createElement('div');
      f.className = 'pue-farol';
      f.innerHTML = farol === o ? '<b></b><span>Farolillo aquí</span>' : '<span>&nbsp;</span>';
      cont.appendChild(f);
      DUENDES.forEach((d, i) => {
        if (lado[i] !== o) return;
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'pue-duende' + (sel.has(i) ? ' sel' : '');
        b.dataset.i = String(i);
        b.dataset.n = d.n;
        b.setAttribute('aria-label', d.n + (sel.has(i) ? ', elegido para cruzar' : ''));
        b.innerHTML = '<span class="pue-cara" style="--c:' + d.color + '"><i class="' + d.forma + '"></i></span><span>' + d.n + '</span>';
        b.addEventListener('click', () => {
          if (resuelto || farol !== o) { if (!resuelto) ui.say('Ese duende no tiene el farolillo en su orilla.', 'bad'); return; }
          if (sel.has(i)) sel.delete(i);
          else if (sel.size < 2) sel.add(i);
          else { ui.say('El farolillo solo alumbra a dos duendes como mucho.', 'bad'); return; }
          ui.say('');
          pintar();
        });
        cont.appendChild(b);
      });
    });
    info.textContent = 'Cruces hechos: ' + cruces + '. El sol sale dentro de ' + LIMITE + ' minutos.';
  }
  let cruces = 0;

  function cruzar() {
    if (resuelto) return;
    if (!sel.size) { ui.say('Elige a uno o dos duendes de la orilla donde está el farolillo.', 'bad'); return; }
    const destino = farol === 'izq' ? 'der' : 'izq';
    gastado += Math.max(...[...sel].map((i) => DUENDES[i].t));
    sel.forEach((i) => { lado[i] = destino; });
    sel = new Set();
    farol = destino;
    cruces++;
    ui.say('');
    pintar();
    if (lado.every((x) => x === 'der')) {
      if (gastado <= LIMITE) {
        resuelto = true;
        guardarLetra('20', LETRA);
        ui.say('¡Los cuatro al otro lado en ' + gastado + ' minutos, justo antes del amanecer! El troll se aparta con un bostezo. Coged la carta 28. Letra del libro: ' + LETRA + '.', 'ok');
      } else {
        ui.say('Habéis tardado ' + gastado + ' minutos y el sol ya ha salido (el límite era ' + LIMITE + '). Empezad de nuevo y repartid mejor quién vuelve con el farolillo.', 'bad');
      }
    }
  }
  function inicio() {
    lado = DUENDES.map(() => 'izq'); farol = 'izq'; sel = new Set(); gastado = 0; cruces = 0; resuelto = false;
    ui.say('');
    pintar();
  }
  ui.button('Cruzar', 'primary', cruzar).classList.add('pue-cruzar');
  ui.button('Empezar de nuevo', 'ghost', inicio);
  inicio();
  return { close: ui.close };
}

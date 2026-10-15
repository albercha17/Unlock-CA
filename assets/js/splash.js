/* splash.js — pantalla de arranque con el Cronoportal, solo al abrir la app instalada (o con ?splash en la dirección) y una vez por sesión.
   Script clásico que va en el <head> para pintarse antes que el contenido. */
(function () {
  var instalada = (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) || window.navigator.standalone === true;
  var forzada = /[?&]splash\b/.test(location.search);
  if (!instalada && !forzada) return;
  try { if (sessionStorage.getItem('ca-splash') && !forzada) return; sessionStorage.setItem('ca-splash', '1'); } catch (e) { /* sin almacenamiento: se muestra igual */ }
  var script = document.currentScript;
  var base = new URL('../../', script ? script.src : location.href);
  var reducido = document.documentElement.getAttribute('data-movimiento') === 'reducido' || (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var st = document.createElement('style');
  st.textContent = '#ca-splash{position:fixed;inset:0;z-index:99999;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;background:radial-gradient(circle at 50% 38%,#16404c,#071013 70%);color:#f0c773;font-family:"Poppins",system-ui,-apple-system,sans-serif;transition:opacity .45s ease}' +
    '#ca-splash.fuera{opacity:0;pointer-events:none}' +
    '#ca-splash img{width:128px;height:128px;border-radius:30px;box-shadow:0 0 60px rgba(61,214,198,.45);' + (reducido ? '' : 'animation:ca-splash-late 1.6s ease-in-out infinite;') + '}' +
    '#ca-splash b{font-size:1.5rem;letter-spacing:.02em}#ca-splash small{color:#8fb0b8;font-size:.8rem;letter-spacing:.14em;text-transform:uppercase;margin-top:-10px}' +
    '@keyframes ca-splash-late{0%,100%{transform:scale(1);box-shadow:0 0 40px rgba(61,214,198,.3)}50%{transform:scale(1.06);box-shadow:0 0 80px rgba(61,214,198,.6)}}';
  var d = document.createElement('div');
  d.id = 'ca-splash';
  d.setAttribute('aria-hidden', 'true');
  d.innerHTML = '<img alt="" src="' + new URL('assets/icons/icon-192.png', base).href + '"><b>Unlock C&amp;A</b><small>Cristina y Alberto</small>';
  document.documentElement.appendChild(st);
  document.documentElement.appendChild(d);
  function quitar() { d.classList.add('fuera'); setTimeout(function () { d.remove(); st.remove(); }, 520); }
  var minimo = reducido ? 350 : 1000;
  function cuando() { setTimeout(quitar, minimo); } // se ve al menos un segundo desde que la página está cargada
  if (document.readyState === 'complete') cuando(); else window.addEventListener('load', cuando);
  setTimeout(quitar, 4000);
})();

// estilos.js · utilidades comunes de los «Estilos recreados» (Viegas IA · Motion Lab)
// Lee los parámetros del bloque <script id="params" type="application/json"> (o window.PARAMS) y el formato del #hash.
(function () {
  const bloque = document.getElementById('params');
  const P = Object.assign(bloque ? JSON.parse(bloque.textContent) : {}, window.PARAMS || {});
  const FMT = (location.hash.match(/(16x9|9x16|1x1|4x5)/) || [0, P.formato || '16x9'])[1];
  const [W, H] = ({ '16x9': [1920, 1080], '9x16': [1080, 1920], '1x1': [1080, 1080], '4x5': [1080, 1350] })[FMT];
  const LOGO_V = (c = '#08090C') => `<svg viewBox="0 0 24 24"><path d="M4 4h4.2L12 15.5 15.8 4H20l-6 16h-4z" fill="${c}"/></svg>`;
  const LOGO_CLAUDE = (c = 'var(--logo)') => `<svg viewBox="0 0 100 100"><path style="fill:${c}" d="m19.6 66.5 19.7-11 .3-1-.3-.5h-1l-3.3-.2-11.2-.3L14 53l-9.5-.5-2.4-.5L0 49l.2-1.5 2-1.3 2.9.2 6.3.5 9.5.6 6.9.4L38 49.1h1.6l.2-.7-.5-.4-.4-.4L29 41l-10.6-7-5.6-4.1-3-2-1.5-2-.6-4.2 2.7-3 3.7.3.9.2 3.7 2.9 8 6.1L37 36l1.5 1.2.6-.4.1-.3-.7-1.1L33 25l-6-10.4-2.7-4.3-.7-2.6c-.3-1-.4-2-.4-3l3-4.2L28 0l4.2.6L33.8 2l2.6 6 4.1 9.3L47 29.9l2 3.8 1 3.4.3 1h.7v-.5l.5-7.2 1-8.7 1-11.2.3-3.2 1.6-3.8 3-2L61 2.6l2 2.9-.3 1.8-1.1 7.7L59 27.1l-1.5 8.2h.9l1-1.1 4.1-5.4 6.9-8.6 3-3.5L77 13l2.3-1.8h4.3l3.1 4.7-1.4 4.9-4.4 5.6-3.7 4.7-5.3 7.1-3.2 5.7.3.4h.7l12-2.6 6.4-1.1 7.6-1.3 3.5 1.6.4 1.6-1.4 3.4-8.2 2-9.6 2-14.3 3.3-.2.1.2.3 6.4.6 2.8.2h6.8l12.6 1 3.3 2 1.9 2.7-.3 2-5.1 2.6-6.8-1.6-16-3.8-5.4-1.3h-.8v.4l4.6 4.5 8.3 7.5L89 80.1l.5 2.4-1.3 2-1.4-.2-9.2-7-3.6-3-8-6.8h-.5v.7l1.8 2.7 9.8 14.7.5 4.5-.7 1.4-2.6 1-2.7-.6-5.8-8-6-9-4.7-8.2-.5.4-2.9 30.2-1.3 1.5-3 1.2-2.5-2-1.4-3 1.4-6.2 1.6-8 1.3-6.4 1.2-7.9.7-2.6v-.2H49L43 72l-9 12.3-7.2 7.6-1.7.7-3-1.5.3-2.8L24 86l10-12.8 6-7.9 4-4.6-.1-.5h-.3L17.2 77.4l-4.7.6-2-2 .2-3 1-1 8-5.5Z"/></svg>`;
  // lienzo a pantalla completa (o del tamaño pedido) para dibujar con canvas en cada fotograma
  function lienzo(MG, w = W, h = H, padre) {
    const c = document.createElement('canvas'); c.width = w; c.height = h; c.className = 'mg-abs'; c.style.left = '0'; c.style.top = '0';
    (padre || MG.mundo).appendChild(c); return { c, x: c.getContext('2d'), w, h };
  }
  // color de un token CSS (para canvas)
  const token = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  // aleatorio con semilla (determinista)
  const azar = (s) => () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  window.EST = { P, FMT, W, H, VERT: H > W, U: Math.min(W, H) / 1080, LOGO_V, LOGO_CLAUDE, lienzo, token, azar };
})();

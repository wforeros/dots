// cta.js · Pack de CTAs animados · Viegas IA (motor del kit motion-graphics-viegas)
// Lee los parámetros (bloque <script id="params">, window.PARAMS, ?parametro=valor de la URL y #formato) y da las piezas comunes:
// logos reales (YouTube, Instagram, TikTok, Claude, mascota de Claude Code), cursor, colocación por «posicion», salida y textos por idioma.
//
// Parámetros comunes (todas las escenas):
//   usuario «@viegasestudio» · canal «Viegas Estudio» · palabra «CLAUDE» · texto (frase principal; vacío = la del idioma)
//   acento «#D97757» · idioma es|en|pt · posicion arriba|centro|abajo (+ -izquierda/-derecha) · duracion (s) · formato 9x16|16x9|1x1
//   fondo transparente|oscuro|verde · escala (1 = tamaño normal)
// Ver en el navegador en bucle: escena.html?vivo  ·  Renderizar: window.seek(t) (lo usa scripts/render-cta.mjs)
(function () {
  const q = new URLSearchParams(location.search);
  const bloque = document.getElementById('params');
  const BASE = { usuario: '@viegasestudio', canal: 'Viegas Estudio', palabra: 'CLAUDE', texto: '', acento: '#D97757', idioma: 'es',
    posicion: 'centro', duracion: 5, formato: '9x16', fondo: 'transparente', escala: 1 };
  const P = Object.assign({}, BASE, bloque ? JSON.parse(bloque.textContent) : {}, window.PARAMS || {});
  for (const [k, v] of q) { if (k === 'vivo' || k === 'ver') continue; P[k] = typeof P[k] === 'number' ? (parseFloat(v) || P[k]) : v; }
  const h = location.hash.match(/(16x9|9x16|1x1|4x5)/); if (h) P.formato = h[1];
  if (!/^(16x9|9x16|1x1|4x5)$/.test(P.formato)) P.formato = '9x16';
  if (P.escala && typeof P.escala === 'object') P.escala = P.escala[P.formato] ?? 1;   // escala por formato en el bloque de parámetros
  P.duracion = Math.min(30, Math.max(2.5, +P.duracion || 5)); P.escala = Math.min(2.5, Math.max(0.3, +P.escala || 1));
  if (!/^#[0-9a-f]{3,8}$/i.test(P.acento)) P.acento = '#D97757';
  P.usuario = String(P.usuario || '').trim().replace(/^@*/, '@'); if (P.usuario === '@') P.usuario = '@usuario';
  P.user = P.usuario.slice(1);
  P.palabra = String(P.palabra || 'CLAUDE').trim().slice(0, 24) || 'CLAUDE';
  const [W, H] = ({ '16x9': [1920, 1080], '9x16': [1080, 1920], '1x1': [1080, 1080], '4x5': [1080, 1350] })[P.formato];
  const VERT = H > W;
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

  // ---------- textos por idioma (sin faltas: revisados a mano)
  const TX = {
    es: { suscribete: 'Suscríbete', suscrito: 'Suscrito', siguenos: 'Síguenos', sigueme: 'Sígueme', seguir: 'Seguir', siguiendo: 'Siguiendo',
      comenta: 'Comenta', comentaLa: 'Comenta la palabra', teLoEnvio: 'y te lo envío por mensaje', anade: 'Añade un comentario…', publicar: 'Publicar',
      campana: 'Activa la campana', campanaSub: 'para no perderte ningún vídeo', suscriptores: 'suscriptores', seguidores: 'seguidores', siguiendoN: 'siguiendo',
      publicaciones: 'publicaciones', enRedes: 'Síguenos en redes', enTodas: 'en todas las redes', ahora: 'ahora', responder: 'Responder', mensaje: 'Mensaje',
      enYT: 'en YouTube', enIG: 'en Instagram', enTT: 'en TikTok', alCanal: 'al canal', aqui: 'Aquí lo tienes', enlace: 'Te dejo el enlace',
      nuevo: 'te ha enviado un mensaje', masCont: 'para más contenido como este', meGusta: 'Me gusta', nuevoVideo: 'Nuevo vídeo cada semana', escribe: 'Escribe' },
    en: { suscribete: 'Subscribe', suscrito: 'Subscribed', siguenos: 'Follow us', sigueme: 'Follow me', seguir: 'Follow', siguiendo: 'Following',
      comenta: 'Comment', comentaLa: 'Comment the word', teLoEnvio: "and I'll send it to you", anade: 'Add a comment…', publicar: 'Post',
      campana: 'Turn on notifications', campanaSub: 'so you never miss a video', suscriptores: 'subscribers', seguidores: 'followers', siguiendoN: 'following',
      publicaciones: 'posts', enRedes: 'Follow us', enTodas: 'everywhere', ahora: 'now', responder: 'Reply', mensaje: 'Message',
      enYT: 'on YouTube', enIG: 'on Instagram', enTT: 'on TikTok', alCanal: 'to the channel', aqui: 'Here you go', enlace: "Here's the link",
      nuevo: 'sent you a message', masCont: 'for more content like this', meGusta: 'Like', nuevoVideo: 'New video every week', escribe: 'Type' },
    pt: { suscribete: 'Inscreva-se', suscrito: 'Inscrito', siguenos: 'Siga-nos', sigueme: 'Me siga', seguir: 'Seguir', siguiendo: 'Seguindo',
      comenta: 'Comente', comentaLa: 'Comente a palavra', teLoEnvio: 'e eu te envio por mensagem', anade: 'Adicione um comentário…', publicar: 'Publicar',
      campana: 'Ative o sininho', campanaSub: 'para não perder nenhum vídeo', suscriptores: 'inscritos', seguidores: 'seguidores', siguiendoN: 'seguindo',
      publicaciones: 'publicações', enRedes: 'Siga-nos', enTodas: 'em todas as redes', ahora: 'agora', responder: 'Responder', mensaje: 'Mensagem',
      enYT: 'no YouTube', enIG: 'no Instagram', enTT: 'no TikTok', alCanal: 'no canal', aqui: 'Aqui está', enlace: 'Aqui está o link',
      nuevo: 'enviou uma mensagem', masCont: 'para mais conteúdo como este', meGusta: 'Curtir', nuevoVideo: 'Vídeo novo toda semana', escribe: 'Digite' },
  };
  const T = TX[P.idioma] || TX.es;

  // ---------- logos reales (YouTube y TikTok: svgl; Instagram: svgl; Claude y mascota: oficiales, SIEMPRE en coral #D97757)
  const CORAL = '#D97757';
  const CL = window.CTA_LOGOS || {};   // logos.js (cárgalo antes que cta.js)
  const LOGO = {
    youtube: (w = 120) => `<svg width="${w}" height="${w * 180 / 256}" viewBox="0 0 256 180">${CL.youtube}</svg>`,
    instagram: (w = 120) => `<svg width="${w}" height="${w}" viewBox="0 0 264.583 264.583" xmlns:xlink="http://www.w3.org/1999/xlink">${CL.instagram}</svg>`,
    // TikTok: la nota con sus dos sombras cian y rosa; el trazo principal en blanco (fondos oscuros) o negro
    tiktok: (w = 120, tinta = '#fff') => `<svg width="${w}" height="${w * 398.67 / 352.28}" viewBox="0 0 352.28 398.67">${CL.tiktok.replace('__TINTA__', tinta)}</svg>`,
    // solo la nota de TikTok (un color), para capas cian/rosa separadas
    tiktokNota: (w = 120, c = '#fff') => `<svg width="${w}" height="${w * 398.67 / 352.28}" viewBox="0 0 352.28 398.67"><path fill="${c}" d="${CL.tiktokNota}"/></svg>`,
    claude: (w = 60) => `<svg width="${w}" height="${w}" viewBox="0 0 100 100"><path fill="${CORAL}" d="${CL.claude}"/></svg>`,
    mascota: (w = 80) => `<svg width="${w}" height="${w * 15 / 24}" viewBox="0 5 24 15"><path fill="${CORAL}" fill-rule="evenodd" d="${CL.mascota}"/></svg>`,
  };
  // iconos de interfaz (dibujados como los de las apps, no logos)
  const ICO = {
    campana: (w = 40, c = 'currentColor') => `<svg width="${w}" height="${w}" viewBox="0 0 24 24"><path fill="${c}" d="M12 22a2.5 2.5 0 0 0 2.45-2h-4.9A2.5 2.5 0 0 0 12 22Zm7-6V11a7 7 0 0 0-5.5-6.84V3.5a1.5 1.5 0 0 0-3 0v.66A7 7 0 0 0 5 11v5l-2 2v1h18v-1l-2-2Z"/></svg>`,
    check: (w = 28, c = 'currentColor') => `<svg width="${w}" height="${w}" viewBox="0 0 24 24"><path fill="none" stroke="${c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M5 12.5l4.5 4.5L19 7.5"/></svg>`,
    corazon: (w = 40, c = '#FF3040') => `<svg width="${w}" height="${w}" viewBox="0 0 24 24"><path fill="${c}" d="M12 21.2 10.6 20C5.4 15.3 2 12.3 2 8.5 2 5.4 4.4 3 7.5 3c1.7 0 3.4.8 4.5 2.1C13.1 3.8 14.8 3 16.5 3 19.6 3 22 5.4 22 8.5c0 3.8-3.4 6.8-8.6 11.5L12 21.2Z"/></svg>`,
    corazonLinea: (w = 40, c = '#fff') => `<svg width="${w}" height="${w}" viewBox="0 0 24 24"><path fill="none" stroke="${c}" stroke-width="1.9" d="M12 20.2 10.9 19.2C5.9 14.7 3 12 3 8.6 3 6 5 4 7.6 4c1.6 0 3.2.8 4.4 2.1C13.2 4.8 14.8 4 16.4 4 19 4 21 6 21 8.6c0 3.4-2.9 6.1-7.9 10.6L12 20.2Z"/></svg>`,
    bocadillo: (w = 40, c = '#fff') => `<svg width="${w}" height="${w}" viewBox="0 0 24 24"><path fill="none" stroke="${c}" stroke-width="1.9" stroke-linejoin="round" d="M20.7 16.2A9 9 0 1 0 17 19.9L21.5 21Z"/></svg>`,
    avion: (w = 40, c = '#fff') => `<svg width="${w}" height="${w}" viewBox="0 0 24 24"><path fill="none" stroke="${c}" stroke-width="1.9" stroke-linejoin="round" d="M22 3 9.2 10.1M22 3l-7.6 18-4.1-8.7L2 8.4Z"/></svg>`,
    mas: (w = 28, c = '#fff') => `<svg width="${w}" height="${w}" viewBox="0 0 24 24"><path stroke="${c}" stroke-width="3.2" stroke-linecap="round" d="M12 5v14M5 12h14"/></svg>`,
    flecha: (w = 40, c = 'currentColor') => `<svg width="${w}" height="${w}" viewBox="0 0 24 24"><path fill="none" stroke="${c}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" d="M12 4v15m-6.5-6.5L12 19l6.5-6.5"/></svg>`,
    cursor: (w = 54) => `<svg width="${w}" height="${w * 1.35}" viewBox="0 0 20 27"><path d="M1.5 1.5v20.6l5.3-5.1 3.4 8 3.6-1.5-3.4-7.9h7.3Z" fill="#111" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>`,
    nota: (w = 30, c = '#fff') => `<svg width="${w}" height="${w}" viewBox="0 0 24 24"><path fill="${c}" d="M9 18.5a3 3 0 1 1-2-2.83V5l12-2v12.5a3 3 0 1 1-2-2.83V7.3l-8 1.3Z"/></svg>`,
  };

  // ---------- colocación: el grupo del CTA se ancla según «posicion» (arriba / centro / abajo, y en horizontal -izquierda / -derecha)
  function ancla() {
    const p = String(P.posicion || 'centro');
    let y = p.includes('arriba') ? 0.24 : p.includes('abajo') ? (VERT ? 0.72 : 0.76) : 0.5, x = 0.5;
    if (p.includes('izquierda')) x = VERT ? 0.5 : 0.28; if (p.includes('derecha')) x = VERT ? 0.5 : 0.72;
    if (P.formato === '1x1' && p.includes('arriba')) y = 0.28;
    return { x: W * x, y: H * y };
  }
  const k = (t, a, b) => Math.max(0, Math.min(1, (t - a) / (b - a)));
  const pon = (el, x, y, s = 1, extra = '') => { el.style.transform = `translate(${x}px,${y}px) translate(-50%,-50%) scale(${s}) ${extra}`; };

  // arranque común: fondo, acento, grupo anclado y salida suave al final (fundido + desenfoque gaussiano + caída leve)
  function inicio(MG) {
    const raiz = document.documentElement.style;
    raiz.setProperty('--acento', P.acento); raiz.setProperty('--acento2', P.acento);
    const m = P.acento.replace('#', ''), hx = m.length === 3 ? m.split('').map((c) => c + c).join('') : m.slice(0, 6);
    raiz.setProperty('--acento-rgb', [0, 2, 4].map((i) => parseInt(hx.slice(i, i + 2), 16)).join(','));
    const fondo = document.querySelector('.mg-fondo');
    if (P.fondo === 'oscuro' && fondo) fondo.style.background = `radial-gradient(70% 55% at 50% 60%, #1B1A1F, #0C0C0F 70%), #0C0C0F`;
    if (P.fondo === 'verde' && fondo) fondo.style.background = '#00B140';
    const a = ancla(), G = document.createElement('div'); G.className = 'cta-g'; MG.mundo.appendChild(G);
    const base = `translate(${a.x}px,${a.y}px) scale(${P.escala})`; G.style.transform = base;
    const D = P.duracion;
    return {
      G, a,
      el: (html) => MG.el(html, G),
      salida(t, dur = 0.55) {
        const s = MG.curvas.entradaCubica(k(t, D - dur, D - 0.04));
        G.style.opacity = (1 - s).toFixed(3);
        G.style.filter = s > 0.01 ? `blur(${(s * 16).toFixed(2)}px)` : 'none';
        G.style.transform = `${base} translateY(${s * 26}px) scale(${1 - s * 0.05})`;
      },
    };
  }

  // cursor: entra desde fuera con curva de cámara, se posa sobre (x, y) y «pulsa» en tc
  function cursor(MG, padre) { const c = MG.el(`<div class="cta-cursor">${ICO.cursor()}</div>`, padre); const r = MG.el('<div class="cta-onda"></div>', padre); return { c, r }; }
  function mueveCursor(MG, cur, t, tramos, tc) {
    // tramos: [[t0, t1, x0, y0, x1, y1], ...] con curva entradaSalidaQuint (arranque suave, frenada larga)
    let x = tramos[0][2], y = tramos[0][3];
    for (const [a, b, x0, y0, x1, y1] of tramos) { if (t >= a) { const p = MG.curvas.entradaSalidaQuint(k(t, a, b)); x = x0 + (x1 - x0) * p; y = y0 + (y1 - y0) * p; } }
    const pre = (tc || []).reduce((m, c) => Math.max(m, Math.sin(Math.PI * k(t, c - 0.08, c + 0.14))), 0);
    cur.c.style.transform = `translate(${x}px,${y}px) scale(${1 - pre * 0.16})`;
    const ul = tramos[tramos.length - 1];   // en el último tramo (si hay más de uno) el cursor se va y se apaga
    cur.c.style.opacity = Math.min(1, k(t, tramos[0][0], tramos[0][0] + 0.25)) * (tramos.length > 1 ? 1 - k(t, (ul[0] + ul[1]) / 2, ul[1]) : 1);
    // onda del clic
    const ult = (tc || []).filter((c) => t >= c).pop();
    if (ult !== undefined && t - ult < 0.6) { const p = MG.curvas.salidaCubica(k(t, ult, ult + 0.6)); cur.r.style.opacity = (1 - p) * 0.9; cur.r.style.transform = `translate(${x}px,${y}px) translate(-50%,-50%) scale(${0.3 + p * 1.6})`; }
    else cur.r.style.opacity = 0;
    return { x, y };
  }
  // pulsación de un botón (se hunde y vuelve con rebote)
  const pulsa = (MG, t, tc) => 1 - 0.07 * Math.sin(Math.PI * k(t, tc - 0.06, tc + 0.12)) + 0.03 * (MG.curvas.rebote(k(t, tc + 0.12, tc + 0.7)) - 1) * -0;
  // texto que se escribe letra a letra
  const teclea = (txt, t, t0, cps = 14) => { const n = Math.max(0, Math.floor((t - t0) * cps)); return [...txt].slice(0, n).join(''); };
  // avatar: iniciales del canal en un círculo con el acento
  const iniciales = (s) => esc(String(s).replace(/^@/, '').split(/[\s._-]+/).filter(Boolean).slice(0, 2).map((p) => p[0]).join('').toUpperCase() || 'V');
  // contador con separador de miles del idioma
  const miles = (n) => Math.round(n).toLocaleString(P.idioma === 'en' ? 'en-US' : P.idioma === 'pt' ? 'pt-BR' : 'es-ES', { useGrouping: true }).replace(/^(\d)\.(\d{3})$/, P.idioma === 'en' ? '$1,$2' : '$1.$2');

  // trocea un texto en letras (o palabras) para animarlas por separado
  const trocea = (el, txt, modo = 'letras') => { el.innerHTML = (modo === 'letras' ? [...String(txt)] : String(txt).split(' ')).map((c) => `<span class="tz">${esc(c)}</span>`).join(modo === 'letras' ? '' : '<span class="tz"> </span>'); return [...el.querySelectorAll('.tz')]; };
  // entrada «sube con desenfoque» (norma 3b): cada trozo sube 20-40 px, de borroso a nítido, con ease-out largo
  function sube(MG, trozos, t, t0, paso = 0.04, o = {}) {
    trozos.forEach((s, i) => {
      const p = MG.curvas[o.curva || 'salidaExpo'](k(t, t0 + i * paso, t0 + i * paso + (o.d || 0.5)));
      s.style.opacity = Math.min(1, p * 1.7);
      s.style.transform = `translateY(${(1 - p) * (o.dy ?? 34)}px) scale(${o.s0 ? o.s0 + (1 - o.s0) * p : 1})`;
      s.style.filter = p < 0.995 ? `blur(${((1 - p) * (o.blur ?? 12)).toFixed(2)}px)` : 'none';
    });
  }
  // cifra corta: 48200 → «48,2 mil» (es/pt) o «48.2K» (en); texto libre se deja tal cual
  const corto = (v) => { const n = +String(v).replace(/[^\d]/g, ''); if (!/^\s*\d[\d.,\s]*$/.test(String(v)) || !n) return esc(v); if (n < 10000) return miles(n);
    const x = (n >= 1e6 ? n / 1e6 : n / 1e3).toLocaleString(P.idioma === 'en' ? 'en-US' : 'es-ES', { maximumFractionDigits: 1 });
    return x + (P.idioma === 'en' ? (n >= 1e6 ? 'M' : 'K') : n >= 1e6 ? ' M' : ' mil'); };
  window.CTA = { corto, trocea, sube, P, T, W, H, VERT, LOGO, ICO, CORAL, esc, k, pon, inicio, cursor, mueveCursor, pulsa, teclea, iniciales, miles, ancla };

  // ---------- modo «vivo» (navegador / configurador del Laboratorio): bucle en tiempo real, reinicio por postMessage
  if (q.has('vivo')) {
    let t0 = 0, pausa = false, tp = 0;
    const listo = () => new Promise((ok) => { const m = () => (window.__listo ? ok() : setTimeout(m, 30)); m(); });
    listo().then(() => {
      const D = window.__duracion || P.duracion; t0 = performance.now();
      parent.postMessage({ cta: 'inicio', dur: D, w: W, h: H }, '*');
      const bucle = () => {
        const t = pausa ? tp : ((performance.now() - t0) / 1000);
        if (!pausa && t >= D) { t0 = performance.now(); parent.postMessage({ cta: 'inicio', dur: D, w: W, h: H }, '*'); }
        window.seek(Math.min(t, D - 0.001)); requestAnimationFrame(bucle);
      };
      requestAnimationFrame(bucle);
      addEventListener('message', (e) => {
        const d = e.data || {};
        if (d.cta === 'reinicia') { pausa = false; t0 = performance.now(); parent.postMessage({ cta: 'inicio', dur: D, w: W, h: H }, '*'); }
        if (d.cta === 'pausa') { pausa = true; tp = Math.min(D, (performance.now() - t0) / 1000); }
        if (d.cta === 'sigue') { pausa = false; t0 = performance.now() - tp * 1000; }
      });
    });
  }
})();

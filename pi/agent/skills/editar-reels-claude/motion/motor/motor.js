// motor.js · Motion Graphics Viegas
// Motor de animación determinista: cada fotograma se pinta desde cero con window.seek(t), así el render es exacto
// fotograma a fotograma (nada de requestAnimationFrame ni de CSS transitions). Lo usa cada escena (escena.html).
//
//   <script src="../motor/motor.js"></script>
//   escena({ duracion: 6, ancho: 1920, alto: 1080, fondo: 'marca' }, (MG) => { ...crear elementos...; return (t) => { ...pintar el instante t... }; });
//
// API (todo en MG): curvas · entra · pon · desenfoca · camara · tarjeta · texto · linea · contador · lerp · k

(function () {
  'use strict';
  const cl = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
  const k = (t, a, b) => cl((t - a) / (b - a));           // progreso 0–1 de t entre a y b
  const lerp = (a, b, x) => a + (b - a) * x;

  // ---------------------------------------------------------------- curvas de velocidad (las de After Effects y algunas más)
  // Todas reciben x en 0–1 y devuelven el progreso. Las de rebote se pasan de 1 y vuelven (eso es lo que se ve «natural»).
  function bezier(x1, y1, x2, y2) {                        // cubic-bezier como en CSS / el editor de gráficos de AE
    const A = (a, b) => 1 - 3 * b + 3 * a, B = (a, b) => 3 * b - 6 * a, C = (a) => 3 * a;
    const f = (t, a, b) => ((A(a, b) * t + B(a, b)) * t + C(a)) * t, df = (t, a, b) => 3 * A(a, b) * t * t + 2 * B(a, b) * t + C(a);
    return (x) => { x = cl(x); let t = x; for (let i = 0; i < 8; i++) { const d = df(t, x1, x2); if (Math.abs(d) < 1e-6) break; t -= (f(t, x1, x2) - x) / d; } return f(cl(t), y1, y2); };
  }
  function muelle(amort = 5.5, frec = 1.15) {               // muelle amortiguado: 1 − e^(−amort·x)·cos(2π·frec·x)
    return (x) => { x = cl(x); return x >= 1 ? 1 : 1 - Math.exp(-amort * x) * Math.cos(2 * Math.PI * frec * x); };
  }
  const curvas = {
    lineal: (x) => cl(x),
    suave: (x) => { x = cl(x); return x * x * (3 - 2 * x); },
    entradaCubica: (x) => cl(x) ** 3,
    salidaCubica: (x) => 1 - (1 - cl(x)) ** 3,
    salidaQuint: (x) => 1 - (1 - cl(x)) ** 5,             // «ease out» fuerte: llega rápido y se posa
    entradaSalidaQuint: (x) => { x = cl(x); return x < 0.5 ? 16 * x ** 5 : 1 - Math.pow(-2 * x + 2, 5) / 2; },
    salidaExpo: (x) => (cl(x) >= 1 ? 1 : 1 - Math.pow(2, -10 * cl(x))),
    atras: (x, c = 1.4) => { x = cl(x); return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2; },   // «back»: se pasa una vez
    rebote: muelle(5.5, 1.15),                            // rebote natural (se pasa ~10 % y se asienta) · el de la marca
    reboteSuave: muelle(6.5, 0.95),                       // para cámaras y recorridos largos
    reboteFuerte: muelle(4.2, 1.6),
    afterEffects: bezier(0.33, 0, 0.67, 1),               // «Easy Ease» de AE (33 % de influencia)
    afterEffects75: bezier(0.75, 0, 0.25, 1),             // Easy Ease con 75 % de influencia (más «apple»)
    bezier, muelle,
  };

  // ---------------------------------------------------------------- desenfoque de movimiento direccional (obturador de 180°)
  const SVGNS = 'http://www.w3.org/2000/svg';
  let defs = null, nf = 0;
  const MB = 1 / 160;                                      // σ = |v| / 160 (px/s → px de desenfoque)
  function desenfoca(el, sx, sy) {
    sx = Math.min(70, sx || 0); sy = Math.min(70, sy || 0);
    if (sx < 0.2 && sy < 0.2) { el.style.filter = 'none'; return; }
    if (!defs) { defs = document.createElementNS(SVGNS, 'svg'); defs.setAttribute('width', 0); defs.setAttribute('height', 0); defs.style.position = 'absolute'; document.body.appendChild(defs); }
    if (!el._mg) {
      const id = 'mg' + (nf++), f = document.createElementNS(SVGNS, 'filter');
      f.setAttribute('id', id); f.setAttribute('x', '-60%'); f.setAttribute('y', '-60%'); f.setAttribute('width', '220%'); f.setAttribute('height', '220%');
      f.setAttribute('color-interpolation-filters', 'sRGB');
      const g = document.createElementNS(SVGNS, 'feGaussianBlur'); f.appendChild(g); defs.appendChild(f); el._mg = {g, id};
    }
    el._mg.g.setAttribute('stdDeviation', `${sx.toFixed(2)} ${sy.toFixed(2)}`);
    el.style.filter = `url(#${el._mg.id})`;
  }

  // ---------------------------------------------------------------- entrada estándar: fundido + desplazamiento con curva + desenfoque de movimiento
  // opciones: d (duración), dx, dy, escala0, curva, base (blur extra mientras llega), extra (blur fijo, p. ej. por profundidad)
  const DT = 1 / 60;
  function entra(el, t, t0, o = {}) {
    const d = o.d ?? 0.7, dx = o.dx ?? 0, dy = o.dy ?? 220, s0 = o.escala0 ?? 0.94, cv = curvas[o.curva || 'rebote'] || o.curva;
    const largo = (o.curva || 'rebote').startsWith?.('rebote') ? d * 1.5 : d;   // el muelle necesita más tiempo para asentarse
    const P = (u) => cv(k(u, t0, t0 + largo)), p = P(t), q = P(t - DT);
    const vx = dx * (p - q) / DT, vy = dy * (p - q) / DT, r = Math.max(0, 1 - p);
    el.style.opacity = Math.min(1, Math.max(0, p) * 1.8);
    if (o.desenfoque !== false) desenfoca(el, Math.abs(vx) * MB + r * (o.base ?? 3) + (o.extra || 0), Math.abs(vy) * MB + r * (o.base ?? 3) + (o.extra || 0));
    return { x: (1 - p) * dx, y: (1 - p) * dy, s: lerp(s0, 1, p), p };
  }
  function pon(el, x, y, s = 1, extra = '') { el.style.transform = `translate(${x}px,${y}px) scale(${s}) ${extra}`; }

  // ---------------------------------------------------------------- cámara: la escena nunca se queda quieta
  let vista = null, duracion = 5;
  function camara(t, z0 = 1, z1 = 1.08, ox, oy) {
    vista.style.transformOrigin = `${ox ?? ANCHO / 2}px ${oy ?? ALTO / 2}px`;
    vista.style.transform = `scale(${lerp(z0, z1, t / duracion)})`;
  }

  // ---------------------------------------------------------------- vídeos dentro de la escena (tarjetas, pantallas): se colocan fotograma a fotograma
  const VIDS = [], DESPUES = [];
  function tarjeta(src, w, h, t0 = 0, o = {}) {
    const c = document.createElement('div'); c.className = 'mg-tarjeta mg-abs'; c.style.width = w + 'px'; c.style.height = h + 'px';
    const v = document.createElement('video'); v.muted = true; v.playsInline = true; v.preload = 'auto'; v.src = src; c.appendChild(v);
    (o.padre || mundo).appendChild(c); VIDS.push({ v, t0, off: o.desde ?? 0.5, bucle: o.bucle ?? true, fijo: o.fijo }); return c;
  }
  // vídeo sin tarjeta (por ejemplo, como textura de un objeto 3D): se coloca igual, fotograma a fotograma
  let almacen = null;
  function video(src, t0 = 0, o = {}) {
    if (!almacen) { almacen = document.createElement('div'); almacen.style.cssText = 'position:absolute;width:1px;height:1px;overflow:hidden;opacity:0'; document.body.appendChild(almacen); }
    const v = document.createElement('video'); v.muted = true; v.playsInline = true; v.preload = 'auto'; v.crossOrigin = 'anonymous'; v.src = src; almacen.appendChild(v);
    VIDS.push({ v, t0, off: o.desde ?? 0.5, bucle: o.bucle ?? true, fijo: o.fijo }); return v;
  }
  function tiempoVideo(o, t) {
    if (o.fijo !== undefined) return o.fijo;
    let x = t - o.t0 + o.off; const dur = (o.v.duration && isFinite(o.v.duration)) ? o.v.duration - 0.05 : 7.9;
    if (o.bucle) x = ((x % dur) + dur) % dur;
    return Math.min(dur, Math.max(0, x));
  }
  function ponVideo(v, x) {
    x = Math.round(x * 30) / 30 + 0.004;
    if (Math.abs(v.currentTime - x) < 0.003) return Promise.resolve();
    return new Promise((ok) => { const f = () => { v.removeEventListener('seeked', f); ok(); }; v.addEventListener('seeked', f); v.currentTime = x; });
  }

  // ---------------------------------------------------------------- texto que entra por palabras o letras (escalonado)
  function texto(txt, clase = '', modo = 'palabras') {
    const el = document.createElement('div'); el.className = 'mg-abs ' + clase;
    const partes = modo === 'letras' ? [...txt] : txt.split(' ');
    el.innerHTML = partes.map((p) => `<span class="mg-trozo">${p === ' ' ? '&nbsp;' : p}</span>`).join(modo === 'letras' ? '' : ' ');
    mundo.appendChild(el); el.trozos = [...el.querySelectorAll('.mg-trozo')]; return el;
  }
  function animaTexto(el, t, t0, o = {}) {
    const paso = o.paso ?? 0.05;
    el.trozos.forEach((s, i) => { const e = entra(s, t, t0 + i * paso, { d: o.d ?? 0.6, dx: 0, dy: o.dy ?? 60, escala0: 1, curva: o.curva, base: 2 });
      s.style.display = 'inline-block'; s.style.transform = `translateY(${e.y}px)`; });
  }

  // ---------------------------------------------------------------- línea que se dibuja (trazo SVG)
  let capaSvg = null;
  function linea(d, color = 'var(--acento)', ancho = 3) {
    if (!capaSvg) { capaSvg = document.createElementNS(SVGNS, 'svg'); capaSvg.setAttribute('class', 'mg-abs'); capaSvg.setAttribute('width', ANCHO * 3); capaSvg.setAttribute('height', ALTO * 3); capaSvg.style.overflow = 'visible'; mundo.appendChild(capaSvg); }
    const p = document.createElementNS(SVGNS, 'path'); p.setAttribute('d', d); p.setAttribute('fill', 'none'); p.style.stroke = color;   // en style: así acepta var(--acento)
    p.setAttribute('stroke-width', ancho); p.setAttribute('stroke-linecap', 'round'); capaSvg.appendChild(p);
    const L = p.getTotalLength(); p.style.strokeDasharray = L;
    p.dibuja = (x) => { p.style.strokeDashoffset = L * (1 - cl(x)); p.style.opacity = x > 0 ? 1 : 0; }; p.dibuja(0); return p;
  }

  // ---------------------------------------------------------------- contador numérico con curva
  function contador(el, t, t0, t1, desde, hasta, o = {}) {
    const v = lerp(desde, hasta, (curvas[o.curva || 'salidaQuint'])(k(t, t0, t1)));
    el.textContent = (o.prefijo || '') + v.toLocaleString(o.idioma || 'es-ES', { maximumFractionDigits: o.decimales ?? 0, minimumFractionDigits: o.decimales ?? 0 }) + (o.sufijo || '');
  }

  // ---------------------------------------------------------------- fondo vivo
  // escena({ fondo: 'marca',
  //   trama: { tipo: 'rejilla'|'lineas'|'puntos'|'nada', tamano: 70, intensidad: .5 },   // tamaño en px, intensidad 0–1
  //   halo: .3 (fuerza 0–1) o { fuerza: .3, x: 50, y: 112 },                              // MG.halo(x, y) lo mueve en cada fotograma
  //   degradado: 'aurora'|'barrido'|'suave' o { tipo, fuerza: .35, ciclo: 12 } })          // ciclo en s: el bucle cierra perfecto
  function fondoVivo(cfg, fondo) {
    const raiz = document.body.style, nada = () => {};
    if (cfg.trama || cfg.halo !== undefined) {
      const tr = cfg.trama || { tipo: 'rejilla' }, s = tr.tamano || 70, a = tr.intensidad ?? 1, c = `rgba(var(--claro), ${(0.07 * a).toFixed(3)})`;
      const pat = { rejilla: `linear-gradient(${c} 1px, transparent 1px) 0 0/${s}px ${s}px, linear-gradient(90deg, ${c} 1px, transparent 1px) 0 0/${s}px ${s}px`,
        lineas: `linear-gradient(${c} 1px, transparent 1px) 0 0/100% ${s}px`,
        puntos: `radial-gradient(circle, rgba(var(--claro), ${(0.22 * a).toFixed(3)}) 0 ${Math.max(1.2, s * .04)}px, transparent ${Math.max(1.2, s * .04) + 1}px) 0 0/${s}px ${s}px`, nada: '' }[tr.tipo || 'rejilla'];
      const h = typeof cfg.halo === 'object' ? cfg.halo : { fuerza: cfg.halo ?? .3 };
      raiz.setProperty('--halo-x', (h.x ?? 50) + '%'); raiz.setProperty('--halo-y', (h.y ?? 112) + '%');
      const f = h.fuerza ?? .3;
      fondo.className = 'mg-fondo';
      fondo.style.background = `radial-gradient(60% 48% at var(--halo-x) var(--halo-y), rgba(var(--halo), ${f}), rgba(var(--halo), ${(f / 3).toFixed(3)}) 45%, transparent 72%)${pat ? ', ' + pat : ''}, var(--fondo)`;
    }
    if (!cfg.degradado) return nada;
    const d = typeof cfg.degradado === 'string' ? { tipo: cfg.degradado } : cfg.degradado, ciclo = d.ciclo || 12, fu = d.fuerza ?? .35;
    const capa = document.createElement('div'); capa.className = 'mg-degradado mg-degradado-' + d.tipo; capa.style.opacity = fu; fondo.after(capa);
    return (t) => {
      const fase = (t / ciclo) * Math.PI * 2;
      if (d.tipo === 'suave') capa.style.backgroundPosition = `${((t / ciclo) * 300) % 300}% ${((t / ciclo) * 300) % 300}%`;
      else if (d.tipo === 'aurora') capa.style.transform = `translate(${(Math.sin(fase) * 9).toFixed(2)}%, ${(Math.sin(fase * 2 + 1) * 6).toFixed(2)}%) scale(${(1.05 + Math.sin(fase + 2) * .1).toFixed(3)})`;
      else if (d.tipo === 'barrido') capa.style.transform = `rotate(${(t / ciclo) * 360}deg)`;
    };
  }

  // ---------------------------------------------------------------- arranque de la escena
  let ANCHO = 1920, ALTO = 1080, mundo = null;
  function escena(cfg, crear) {
    ANCHO = cfg.ancho || 1920; ALTO = cfg.alto || 1080; duracion = cfg.duracion || 5;
    if (cfg.fondo === 'transparente') { document.documentElement.style.background = 'transparent'; document.body.style.background = 'transparent'; }   // si no, estilo.css pinta el fondo y el render --transparente sale opaco
    document.documentElement.style.setProperty('--ancho', ANCHO + 'px'); document.documentElement.style.setProperty('--alto', ALTO + 'px');
    const fondo = document.createElement('div'); fondo.className = 'mg-fondo ' + (cfg.fondo ? 'mg-fondo-' + cfg.fondo : ''); document.body.appendChild(fondo);
    const pintaFondo = fondoVivo(cfg, fondo);   // trama, halo y degradado animado configurables (deterministas: dependen solo de t)
    vista = document.createElement('div'); vista.className = 'mg-vista'; document.body.appendChild(vista);
    mundo = document.createElement('div'); mundo.className = 'mg-mundo'; vista.appendChild(mundo);
    const MG = { curvas, entra, pon, desenfoca, camara, tarjeta, video, despues: (f) => DESPUES.push(f),
      registrar: (v, o = {}) => VIDS.push({ v, t0: o.t0 ?? 0, off: o.off ?? 0.5, bucle: o.bucle ?? true, fijo: o.fijo }), texto, animaTexto, linea, contador, lerp, k, cl, mundo, vista,
      get ANCHO() { return ANCHO; }, get ALTO() { return ALTO; }, DT, MB,
      el: (html, padre) => { const d = document.createElement('div'); d.innerHTML = html.trim(); const n = d.firstChild; (padre || mundo).appendChild(n); return n; } };
    MG.halo = (x, y) => { document.body.style.setProperty('--halo-x', x + '%'); document.body.style.setProperty('--halo-y', y + '%'); };   // mover el halo (en % del lienzo)
    const pintaEscena = crear(MG) || (() => {}), pinta = (t) => { pintaFondo(t); pintaEscena(t); };
    const listos = MG._listos || [];
    window.__duracion = duracion; window.__ancho = ANCHO; window.__alto = ALTO;
    window.seek = async (t) => {
      pinta(t);
      await Promise.all(VIDS.map((o) => ponVideo(o.v, tiempoVideo(o, t))));
      for (const f of DESPUES) await f(t);   // p. ej. el render 3D, cuando los vídeos ya están en su fotograma
      await new Promise((ok) => requestAnimationFrame(() => requestAnimationFrame(ok)));
    };
    const cargado = (v) => new Promise((ok) => { if (v.readyState >= 2) ok(); else { v.addEventListener('loadeddata', ok, { once: true }); v.addEventListener('error', ok, { once: true }); } });
    Promise.all([...listos, document.fonts.ready, ...[...document.images].map((im) => im.decode().catch(() => {})), ...VIDS.map((o) => cargado(o.v))])
      .then(() => window.seek(0)).then(() => { window.__listo = true; });
    // vista previa en el navegador: ?ver reproduce en tiempo real
    if (location.search.includes('ver')) { const t0 = performance.now(); const bucle = () => { const t = ((performance.now() - t0) / 1000) % duracion; pinta(t); VIDS.forEach((o) => { o.v.currentTime = tiempoVideo(o, t); }); DESPUES.forEach((f) => f(t)); requestAnimationFrame(bucle); }; setTimeout(bucle, 300); }
  }
  window.escena = escena;
  window.MGcurvas = curvas;
})();

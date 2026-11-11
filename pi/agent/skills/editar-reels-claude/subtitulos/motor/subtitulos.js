// subtitulos.js · Viegas IA · motor de subtítulos fotograma a fotograma
// -----------------------------------------------------------------------------------------------
// Cada plantilla (estilos/<id>/plantilla.html) carga este motor y su estilo.json. Lee los datos de una carpeta:
//   words.json     {"duration": 8.5, "words": [{"w": "Ya", "start": 0.0, "end": 0.4, "clave": false}, ...]}
//   keywords.json  {"claves": ["Claude Code", "subtítulos"]}          (opcional; también vale "clave": true en words.json)
//   recursos.json  {"recursos": {"Claude Code": {"tipo": "mascota", "archivo": "recursos/claude-code-mascota.svg"}}}  (opcional)
// URL: plantilla.html?datos=../../demo/vertical/&formato=9x16[&desde=0&hasta=8]
// Nada se anima con el reloj: todo se pinta desde cero con window.seek(t) (render exacto, fotograma a fotograma).
// window.listo es una promesa que se cumple cuando fuentes, datos e imágenes están cargados.
(function () {
  'use strict';
  // ---- NORMAS REELS PRO (Diego, 24-10-2026) · motor v2: valores por defecto que heredan TODOS los estilos ----
  // 1) tamaños ≈1,6× (9:16: palabra 64-76 px, clave 110-150 px; 16:9 ×1,6 con 80-104 px y clave 130-170 px)
  // 2) entrada con degradado de desenfoque de abajo arriba (máscara borroso→nítido), subiendo 20-40 px, 0,25-0,4 s, ease-out
  // 3) alternancia por frase: palabra → caracteres → línea, sin repetir dos seguidas
  // 4) palabra clave con escala suave (0,92 → 1)
  // Un estilo puede afinar dentro de esos márgenes, nunca salirse. window.NORMAS_SUBTITULOS = false las desactiva (solo para comparar).
  const NORMAS = {
    version: '2.0.1',
    factor: 1.6,
    tam: { '9x16': [64, 76], '16x9': [80, 104] }, tamClave: { '9x16': [110, 150], '16x9': [130, 170] },
    dy: [20, 40], dur: [0.25, 0.4], curva: 'salidaCubica', blur: 7,
    modos: ['palabra', 'letras', 'grupo'],
    escalaClave: [0.92, 1.08],
  };
  const acota = (x, [a, b]) => Math.min(b, Math.max(a, x));
  const cl = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
  const k = (t, a, b) => cl((t - a) / (b - a));
  const lerp = (a, b, x) => a + (b - a) * x;
  // Curvas de velocidad (las del motor de motion graphics de Diego): entradas rápidas que se posan, sin rebote en textos.
  const CURVAS = {
    lineal: (x) => cl(x),
    suave: (x) => { x = cl(x); return x * x * (3 - 2 * x); },
    salidaCubica: (x) => 1 - (1 - cl(x)) ** 3,
    salidaQuint: (x) => 1 - (1 - cl(x)) ** 5,
    salidaExpo: (x) => (cl(x) >= 1 ? 1 : 1 - Math.pow(2, -10 * cl(x))),
    atras: (x, c = 1.25) => { x = cl(x); return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2; },  // solo iconos: se pasa un pelo y vuelve
  };
  const norm = (s) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^\w%$€]/g, '');
  const limpia = (s, quitar) => (quitar ? s.replace(/^[¿¡"«(]+/, '').replace(/[.,;:!?"»)…]+$/, '') : s);
  const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  async function json(url, def) { try { const r = await fetch(url); if (!r.ok) return def; return await r.json(); } catch { return def; } }

  // Marca en las palabras las frases de una lista (varias palabras seguidas, sin importar tildes ni mayúsculas).
  function marcar(words, frases, fn) {
    const toks = words.map((w) => norm(w.w));
    frases.forEach((f, fi) => {
      const ft = f.split(/\s+/).map(norm).filter(Boolean);
      if (!ft.length) return;
      for (let i = 0; i + ft.length <= toks.length; i++) {
        if (ft.every((x, j) => toks[i + j] === x)) fn(i, ft.length, f, fi);
      }
    });
  }

  // Agrupa las palabras en trozos como los edita Diego: 1-4 palabras, corte en pausas y en final de frase,
  // y (si el estilo lo pide) la palabra clave sola, en grande.
  function agrupar(words, A, dur) {
    const g = [];
    let cur = [];
    const flush = () => { if (cur.length) g.push({ words: cur }), (cur = []); };
    words.forEach((w, i) => {
      const prev = words[i - 1];
      const chars = cur.reduce((s, x) => s + x.txt.length + 1, 0) + w.txt.length;
      const cambiaClave = A.claveSola && cur.length && (!!w.kid !== !!cur[cur.length - 1].kid || (w.kid && w.kid !== cur[cur.length - 1].kid));
      const apilarOk = A.apilar && w.k && cur.length && !cur[cur.length - 1].k;   // en «apilar» la clave cierra el trozo
      const dentro = cur.length && w.kid && w.kid === cur[cur.length - 1].kid;          // nunca partir una frase clave
      const largo = w.kid && !dentro ? words.filter((x) => x.kid === w.kid).length : 1;   // la frase clave entra entera
      if (dentro) { /* sigue */ }
      else if (cur.length && !apilarOk && (cur.length + largo - 1 >= A.maxPalabras || chars > A.maxCaracteres || (prev && w.start - prev.end > A.pausa) || cambiaClave)) flush();
      else if (apilarOk && (prev && w.start - prev.end > A.pausa)) flush();
      cur.push(w);
      const fin = /[.!?…]$/.test(w.w) || (A.cortarEnComa && /,$/.test(w.w));
      if (fin || (A.apilar && w.k && !(words[i + 1] && words[i + 1].kid === w.kid))) flush();
    });
    flush();
    g.forEach((x) => { x.start = x.words[0].start; });
    g.forEach((x, i) => {
      const ultimo = x.words[x.words.length - 1].end;
      const sig = g[i + 1] ? g[i + 1].start : dur;
      x.end = Math.min(sig, ultimo + A.cola);
      if (i === g.length - 1) x.end = Math.min(dur, ultimo + A.colaFinal);
      if (x.end - x.start < A.minimo) x.end = Math.min(sig, x.start + A.minimo);
      x.clave = x.words.some((w) => w.k);
    });
    return g;
  }

  function aplicaVars(el, vars) { Object.entries(vars || {}).forEach(([n, v]) => el.style.setProperty('--' + n, v)); }

  // 7 capas para el desenfoque progresivo: el contenido nítido va en .nit y las copias borrosas encima, en su franja
  function capas(el) {
    if (el._capas) return el._capas;
    const nit = document.createElement('span');
    nit.style.cssText = 'display:inherit;align-items:inherit;position:relative';
    while (el.firstChild) nit.appendChild(el.firstChild);
    el.style.position = 'relative'; el.appendChild(nit);
    const cap = [];
    for (let j = 0; j < 7; j++) {
      const c = nit.cloneNode(true);
      c.style.cssText = 'display:inherit;align-items:inherit;position:absolute;left:0;top:0;right:0;bottom:0;pointer-events:none';
      c.querySelectorAll('img, .ico, .chip').forEach((x) => { x.style.visibility = 'hidden'; });
      el.appendChild(c); cap.push(c);
    }
    return (el._capas = { nit, cap });
  }

  async function iniciar() {
    const q = new URLSearchParams(location.search);
    const base = new URL(q.get('datos') || '../../demo/vertical/', location.href);
    const E = await json('estilo.json', null);
    if (!E) throw new Error('Falta estilo.json');
    const formato = q.get('formato') || E.formatoPorDefecto || '9x16';
    const F = E.formatos[formato];
    if (!F) throw new Error('El estilo no tiene formato ' + formato);
    const D = await json(new URL('words.json', base), null);
    const KW = await json(new URL('keywords.json', base), { claves: [] });
    const RC = await json(new URL('recursos.json', base), { recursos: {} });
    const OC = (await json(new URL('ocultar.json', base), { tramos: [] })).tramos || [];
    const A = Object.assign({ maxPalabras: 3, maxCaracteres: 20, pausa: 0.5, cola: 0.35, colaFinal: 0.6, minimo: 0.4, claveSola: false, apilar: false, cortarEnComa: true, quitarPuntuacion: true }, E.agrupar, F.agrupar);
    const dur = D.duration || D.words[D.words.length - 1].end + 0.6;

    // palabras + claves + recursos
    const words = D.words.map((w) => ({ w: w.w, txt: limpia(w.w, A.quitarPuntuacion), start: w.start, end: w.end, k: !!w.clave, kid: w.clave ? 'm' + w.start : null }));
    marcar(words, KW.claves || [], (i, n, f, fi) => { for (let j = 0; j < n; j++) { words[i + j].k = true; words[i + j].kid = 'k' + fi + '-' + i; } });
    const rec = RC.recursos || {};
    marcar(words, Object.keys(rec).sort((a, b) => a.length - b.length), (i, n, f) => { words[i].rec = Object.assign({ frase: words.slice(i, i + n).map((x) => x.txt).join(' ') }, rec[f]); });
    const grupos = agrupar(words.filter((w) => w.txt), A, dur);

    // lienzo
    const L = document.getElementById('lienzo') || document.body.appendChild(Object.assign(document.createElement('div'), { id: 'lienzo' }));
    L.dataset.formato = formato;
    L.style.width = F.ancho + 'px'; L.style.height = F.alto + 'px';
    aplicaVars(document.documentElement, E.vars); aplicaVars(document.documentElement, F.vars);
    let deg = null;
    if (F.degradado) {
      deg = document.createElement('div'); deg.id = 'degradado';
      deg.style.height = F.degradado.alto + 'px';
      deg.style.background = `linear-gradient(180deg, rgba(0,0,0,0), rgba(0,0,0,${F.degradado.opacidad}))`;
      L.appendChild(deg);
    }
    const N = window.NORMAS_SUBTITULOS === false ? null : NORMAS;
    if (N) {   // tamaños: ×1,6 dentro de los márgenes de las normas (en horizontal, proporcional)
      const cs = getComputedStyle(document.documentElement), fk = formato === '16x9' ? '16x9' : '9x16';
      const px = (n) => parseFloat(cs.getPropertyValue('--' + n)) || 0;
      const t0 = px('tam'), tc = px('tam-clave');
      if (t0) document.documentElement.style.setProperty('--tam', acota(t0 * N.factor, N.tam[fk]).toFixed(1) + 'px');
      if (tc) document.documentElement.style.setProperty('--tam-clave', acota(tc * N.factor, N.tamClave[fk]).toFixed(1) + 'px');
      const ajusta = (an) => an && Object.assign(an, { dy: acota(Math.abs(an.dy || 30), N.dy), dur: acota(an.dur || 0.32, N.dur),
        curva: an.curva === 'atras' ? an.curva : N.curva, blur: Math.max(an.blur || 0, N.blur), degradado: true });
      E.entrada = ajusta(Object.assign({}, E.entrada)); E.entradaClave = ajusta(Object.assign({}, E.entrada, E.entradaClave));
      E.entradaClave.escala0 = acota(E.entradaClave.escala0 ?? 0.92, N.escalaClave);
      if (Math.abs(E.entradaClave.escala0 - 1) < 0.02) E.entradaClave.escala0 = 0.92;
      E.modos = N.modos;   // alternancia por frase sin repetir
    }
    const modos = E.modos || [E.revelar || 'grupo'];
    const imgs = [];
    let frase = 0;
    grupos.forEach((g, gi) => {
      g.modo = modos[frase % modos.length];
      if (/[.!?…]$/.test(g.words[g.words.length - 1].w)) frase++;
      const el = document.createElement('div');
      el.className = 'grupo' + (g.clave ? ' clave' : '') + (A.apilar && g.clave ? ' apilado' : '');
      el.style.left = F.izq + 'px'; el.style.right = F.der + 'px'; el.style.top = F.centroY + 'px';
      const filas = A.apilar && g.clave ? [g.words.filter((w) => !w.k), g.words.filter((w) => w.k)].filter((r) => r.length) : [g.words];
      filas.forEach((fila, fi) => {
        const cont = filas.length > 1 ? el.appendChild(Object.assign(document.createElement('div'), { className: 'fila' + (fila[0].k ? ' fila-clave' : ' fila-intro') })) : el;
        fila.forEach((w) => {
          const s = document.createElement('span');
          s.className = 'w' + (w.k ? ' k' : '');
          let txt = w.txt;
          if (E.mayusculas === 'todo' || (E.mayusculas === 'clave' && w.k)) txt = txt.toLocaleUpperCase('es');
          const usaLetras = (w.k ? E.entradaClave || E.entrada : E.entrada).tipo === 'letras' || g.modo === 'letras';
          s.innerHTML = usaLetras ? [...txt].map((c) => `<span class="ch">${esc(c)}</span>`).join('') : esc(txt);
          if (w.rec && (E.recurso || {}).modo !== 'chip') {
            const im = document.createElement('img'); im.className = 'ico' + (w.rec.tipo === 'mascota' ? ' mascota' : ''); im.src = new URL(w.rec.archivo, base).href;
            (E.recurso && E.recurso.lado === 'derecha') ? s.appendChild(im) : s.prepend(im);
            imgs.push(im); w.ico = im;
          }
          if (w.rec && (E.recurso || {}).modo === 'chip') {
            const c = document.createElement('div'); c.className = 'chip';
            c.innerHTML = `<img src="${new URL(w.rec.archivo, base).href}"><span>${esc(w.rec.etiqueta || w.rec.frase)}</span>`;
            el.appendChild(c); imgs.push(c.querySelector('img')); w.chip = c;
          }
          cont.appendChild(s); w.el = s; w.chs = [...s.querySelectorAll('.ch')];
        });
      });
      L.appendChild(el); g.el = el;
    });
    await document.fonts.ready;
    await Promise.all(imgs.map((im) => (im.complete ? 0 : new Promise((r) => { im.onload = im.onerror = r; }))));
    // centra cada trozo en su centroY (alto real medido una vez)
    // si un trozo con clave no cabe en una línea, se encoge la clave hasta que quepa (nunca se parte en dos líneas)
    grupos.forEach((g) => {
      if (!g.clave || (A.apilar && g.words.some((w) => !w.k))) return;
      g.el.style.flexWrap = 'nowrap'; g.el.style.justifyContent = 'safe center';
      const disp = g.el.clientWidth, real = g.el.scrollWidth;
      if (real > disp) { const fs = parseFloat(getComputedStyle(g.words.find((w) => w.k).el).fontSize); g.el.style.setProperty('--tam-clave', (fs * disp / real * 0.98).toFixed(1) + 'px'); }
      if (g.el.scrollWidth > g.el.clientWidth + 1) { g.el.style.flexWrap = 'wrap'; g.el.style.justifyContent = 'center'; }   // si aún no cabe (palabras normales largas), dos líneas: nunca cortado
    });
    grupos.forEach((g) => { g.el.style.visibility = 'visible'; g.h = g.el.offsetHeight; g.el.style.top = (F.centroY - g.h / 2) + 'px'; g.el.style.visibility = 'hidden'; });

    // el desenfoque se suma al filtro propio del estilo (drop-shadow, etc.), no lo sustituye
    const filtro = (el, bl) => {
      if (el._f === undefined) { el._f = getComputedStyle(el).filter; if (el._f === 'none') el._f = ''; }
      return ((bl > 0.05 ? `blur(${bl.toFixed(2)}px) ` : '') + el._f).trim() || 'none';
    };
    const oculto = (t) => OC.some(([a, b]) => t >= a && t < b);
    const pinta = (el, p, an, fantasma) => {
      const vis = fantasma ? fantasma + (1 - fantasma) * Math.min(1, p * 1.6) : Math.min(1, p * 1.6);
      el.style.opacity = vis;
      const dy = (1 - p) * (an.dy || 0), sc = lerp(an.escala0 ?? 1, 1, p), bl = (1 - p) * (an.blur || 0);
      el.style.transform = `translate3d(0, ${dy.toFixed(2)}px, 0) scale(${sc.toFixed(4)})`;
      el.style.filter = filtro(el, bl);
      // degradado de desenfoque de abajo arriba (como el «Desenfoque gaussiano» de After Effects): la capa nítida aparece de arriba
      // abajo con una máscara en degradado y debajo hay 7 copias con blur() creciente, cada una visible en su franja (solapadas)
      if (an.degradado) {
        const C = capas(el), R = (1 - p) * 100, B = (an.blur || 7) * 1.6, n = C.length;
        const mk = (e, m) => { e.style.webkitMaskImage = m; e.style.maskImage = m; };
        if (p >= 0.999) { mk(C.nit, 'none'); C.cap.forEach((c) => { c.style.display = 'none'; }); }
        else {
          mk(C.nit, `linear-gradient(to top, transparent 0%, #000 ${R.toFixed(2)}%)`);
          C.cap.forEach((c, j) => {   // j = 0 abajo (la más borrosa) … n-1 arriba (casi nítida)
            const a = (j - 1) / n * R, b0 = j / n * R, b1 = (j + 1) / n * R, b2 = (j + 2) / n * R;
            c.style.display = '';
            c.style.filter = `blur(${(B * (n - j) / n * (1 - p)).toFixed(2)}px)`;
            mk(c, `linear-gradient(to top, ${j ? 'transparent ' + a.toFixed(2) + '%, ' : ''}#000 ${b0.toFixed(2)}%, #000 ${b1.toFixed(2)}%, transparent ${b2.toFixed(2)}%)`);
          });
        }
        el.style.filter = filtro(el, 0);   // el desenfoque lo llevan las capas, no el conjunto
      }
    };
    window.seek = (t) => {
      let algo = false;
      grupos.forEach((g) => {
        const on = t >= g.start - 0.04 && t < g.end && !oculto(g.start);
        g.el.style.visibility = on ? 'visible' : 'hidden';
        if (!on) return;
        algo = true;
        const salida = E.salida ? cl((g.end - t) / E.salida) : 1;
        g.el.style.opacity = salida;
        g.words.forEach((w) => {
          const an = Object.assign({}, E.entrada, w.k ? E.entradaClave : null);
          const curva = CURVAS[an.curva] || CURVAS.salidaCubica;
          const t0 = (g.modo === 'grupo' ? g.start : w.start) - (an.antes ?? 0.02);
          const fantasma = g.modo === 'palabra' ? (w.k ? E.fantasmaClave ?? E.fantasma ?? 0 : E.fantasma ?? 0) : 0;
          if (w.chs.length && (an.tipo === 'letras' || g.modo === 'letras')) {
            w.el.style.opacity = 1; w.el.style.transform = 'none'; w.el.style.filter = 'none';
            const st = an.stagger ?? 0.025;
            w.chs.forEach((c, i) => pinta(c, curva(k(t, t0 + i * st, t0 + i * st + an.dur)), an, fantasma));
          } else pinta(w.el, curva(k(t, t0, t0 + an.dur)), an, fantasma);
          const R = Object.assign({ antes: 0.15, dur: 0.4, curva: 'salidaQuint', escala0: 0.55, blur: 6, dy: 0 }, E.recurso);
          const rp = (CURVAS[R.curva] || CURVAS.salidaQuint)(k(t, w.start - R.antes, w.start - R.antes + R.dur));
          if (w.ico) { w.ico.style.opacity = Math.min(1, rp * 1.5); w.ico.style.transform = `scale(${lerp(R.escala0, 1, rp).toFixed(4)}) rotate(${((1 - rp) * (R.giro || 0)).toFixed(2)}deg)`; w.ico.style.filter = filtro(w.ico, (1 - rp) * R.blur); }
          if (w.chip) { w.chip.style.opacity = Math.min(1, rp * 1.5); w.chip.style.transform = `translate(-50%, ${((1 - rp) * (R.dy || 24)).toFixed(2)}px) scale(${lerp(R.escala0, 1, rp).toFixed(4)})`; w.chip.style.filter = filtro(w.chip, (1 - rp) * R.blur); }
        });
      });
      if (deg) {
        const act = grupos.filter((g) => !oculto(g.start));
        const a0 = act.length ? act[0].start : 0, a1 = act.length ? act[act.length - 1].end : 0;
        deg.style.opacity = Math.min(cl(k(t, a0 - 0.3, a0)), cl(k(t, a1 + 0.3, a1)));
      }
      return algo;
    };
    window.subtitulos = { grupos: grupos.map((g) => ({ start: g.start, end: g.end, texto: g.words.map((w) => w.txt).join(' '), clave: g.clave })), duracion: dur, ancho: F.ancho, alto: F.alto, formato };
    window.seek(Number(q.get('t') || 0));
  }
  window.listo = iniciar().catch((e) => { document.body.innerHTML = `<pre style="color:red;font:20px monospace">${e.stack}</pre>`; throw e; });
})();

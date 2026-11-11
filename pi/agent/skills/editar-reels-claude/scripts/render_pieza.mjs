// render_pieza.mjs · Reels con Motion (kit gratis de Viegas Estudio)
// Fotografía una pieza de motion graphics (motion/piezas/<pieza>.html) fotograma a fotograma con Chrome sin ventana
// y la guarda como vídeo con transparencia (.mov) para ponerla encima del reel. También saca una foto suelta para revisar.
//
//   node scripts/render_pieza.mjs <pieza> --salida graficos/titulo.mov [--params graficos/titulo.json] [--fps 30]
//   node scripts/render_pieza.mjs <pieza> --foto 1.5 --salida graficos/titulo.png [--params ...]
//
// <pieza>: el nombre del archivo sin .html (titulo-cinetico, lista-escalonada, contador-estadistica, chat-notificaciones,
//          lower-third, cta-comenta, cta-instagram, cta-youtube).
// --params: JSON con los textos y colores que quieras cambiar (manda sobre el bloque «params» de la pieza). Siempre 9:16.
// Se ejecuta con prioridad baja para que el ordenador siga usable mientras renderiza.
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import os from 'node:os';
import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

try { os.setPriority(os.constants.priority.PRIORITY_BELOW_NORMAL); } catch {}
const SKILL = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf('--' + n); return i >= 0 ? (args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true) : d; };
const PIEZA = args[0];
if (!PIEZA || PIEZA.startsWith('--')) { console.error('Uso: node render_pieza.mjs <pieza> --salida archivo.mov [--params p.json]'); process.exit(1); }
const html = path.join(SKILL, 'motion', 'piezas', PIEZA + '.html');
if (!fs.existsSync(html)) { console.error('No existe la pieza', PIEZA, '→ mira motion/piezas/'); process.exit(1); }
const FPS = Number(opt('fps', 30)), FOTO = opt('foto', null);
const SALIDA = path.resolve(opt('salida', PIEZA + (FOTO !== null ? '.png' : '.mov')));
const PARAMS = opt('params', null) ? JSON.parse(fs.readFileSync(path.resolve(opt('params')), 'utf8')) : {};
PARAMS.formato = '9x16';

let chromium;
for (const base of [path.join(SKILL, 'package.json'), path.join(process.cwd(), 'package.json')]) {
  try { ({ chromium } = createRequire(base)('playwright')); break; } catch {}
}
if (!chromium) { console.error('Falta Playwright. Ejecuta: python scripts/comprobar_equipo.py --instalar'); process.exit(1); }
const pwCache = (() => { try { const d = path.join(os.homedir(), '.cache', 'ms-playwright'); return fs.readdirSync(d).filter((n) => n.startsWith('chromium-')).sort().reverse().flatMap((n) => [path.join(d, n, 'chrome-linux64', 'chrome'), path.join(d, n, 'chrome-linux', 'chrome')]); } catch { return []; } })();
const chrome = [process.env.CHROME_PATH, ...pwCache, 'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  path.join(process.env.LOCALAPPDATA || '', 'Google/Chrome/Application/chrome.exe'), '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome', '/usr/bin/chromium'].filter(Boolean).find((p) => fs.existsSync(p));

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.ttf': 'font/ttf', '.otf': 'font/otf', '.woff2': 'font/woff2', '.mp4': 'video/mp4' };
const srv = await new Promise((ok) => {
  const s = http.createServer((q, r) => {
    const p = path.join(SKILL, decodeURIComponent(q.url.split('?')[0]));
    if (!p.startsWith(SKILL) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); r.end(); return; }
    r.writeHead(200, { 'Content-Type': MIME[path.extname(p).toLowerCase()] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r);
  });
  s.listen(0, '127.0.0.1', () => ok(s));
});

const browser = await chromium.launch({ executablePath: chrome, args: ['--force-color-profile=srgb', '--font-render-hinting=none'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on('pageerror', (e) => console.error('Error en la pieza:', e.message));
await page.addInitScript((p) => { window.PARAMS = p; }, PARAMS);
await page.goto(`http://127.0.0.1:${srv.address().port}/motion/piezas/${PIEZA}.html#9x16`);
await page.waitForFunction(() => window.__listo === true, null, { timeout: 60000 });
const dur = await page.evaluate(() => window.__duracion);
fs.mkdirSync(path.dirname(SALIDA), { recursive: true });

if (FOTO !== null) {
  await page.evaluate((t) => window.seek(t), Number(FOTO));
  await page.screenshot({ path: SALIDA, omitBackground: true });
  console.log(`✓ foto ${SALIDA} (t = ${FOTO} s de ${dur} s)`);
} else {
  const N = Math.round(dur * FPS);
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'prores_ks', '-profile:v', '4444',
    '-pix_fmt', 'yuva444p10le', SALIDA], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let i = 0; i < N; i++) {
    await page.evaluate((t) => window.seek(t), i / FPS);
    const png = await page.screenshot({ type: 'png', omitBackground: true });
    if (!ff.stdin.write(png)) await new Promise((r) => ff.stdin.once('drain', r));
    if (i % 30 === 0) process.stdout.write(`\r${PIEZA}: ${Math.round((100 * i) / N)} %`);
  }
  ff.stdin.end();
  await new Promise((r) => ff.on('close', r));
  console.log(`\r✓ ${SALIDA} · ${dur} s · ${N} fotogramas · ${((Date.now() - t0) / 1000).toFixed(0)} s`);
}
await browser.close(); srv.close();

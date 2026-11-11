// render.mjs · Viegas IA · Subtítulos
// Fotografía una plantilla fotograma a fotograma (window.seek) con Chrome sin ventana y la monta sobre un clip con ffmpeg,
// o la deja como capa transparente (.mov ProRes 4444 con alfa) para montarla en la edición.
//
//   node motor/render.mjs --estilo reel-claude-duet --datos demo/vertical --formato 9x16 --salida estilos/reel-claude-duet/preview-9x16.mp4
//        [--clip demo/vertical/clip.mp4] [--fps 30] [--transparente] [--desde 0 --hasta 8]
//
// --datos: la carpeta del proyecto con words.json, keywords.json, recursos.json y ocultar.json (cualquier ruta).
// --escala 2: renderiza al doble (4K). Playwright: `npm i playwright` en la carpeta subtitulos/ (o el de la skill).
// Codifica con NVENC si hay NVIDIA; si no, x264.
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import os from 'node:os';
import { spawn, spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

try { os.setPriority(os.constants.priority.PRIORITY_BELOW_NORMAL); } catch {}
const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf('--' + n); return i >= 0 ? (args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true) : d; };
const ESTILO = opt('estilo'), DATOS = opt('datos', 'demo/vertical'), FORMATO = opt('formato', '9x16');
const FPS = Number(opt('fps', 30)), TRANSP = !!opt('transparente', false);
const SALIDA = path.resolve(opt('salida', path.join(RAIZ, 'estilos', ESTILO || '', `preview-${FORMATO}${TRANSP ? '.mov' : '.mp4'}`)));
const CLIP = path.resolve(opt('clip', path.join(DATOS, 'clip.mp4')));
const DIR_DATOS = path.resolve(DATOS);
const ESCALA = Number(opt('escala', 1));
if (!ESTILO) { console.error('Falta --estilo <id>'); process.exit(1); }

let chromium;
for (const base of [path.join(RAIZ, 'package.json'), path.join(RAIZ, '..', 'package.json'), path.join(RAIZ, '..', 'scripts', 'package.json'), path.join(RAIZ, '..', 'plantilla', 'escenas', 'package.json'), ...['Documents', 'Documentos', path.join('OneDrive', 'Documentos')].flatMap((d) => ['Motion Graphics', 'Interfaces 3D'].map((c) => path.join(os.homedir(), d, c, 'package.json')))]) {
  try { ({ chromium } = createRequire(base)('playwright')); break; } catch {}
}
if (!chromium) { console.error('Falta Playwright (npm i playwright en esta carpeta).'); process.exit(1); }
const pwCache = (() => { try { const d = path.join(os.homedir(), '.cache', 'ms-playwright'); return fs.readdirSync(d).filter((n) => n.startsWith('chromium-')).sort().reverse().flatMap((n) => [path.join(d, n, 'chrome-linux64', 'chrome'), path.join(d, n, 'chrome-linux', 'chrome')]); } catch { return []; } })();
const chrome = [process.env.CHROME_PATH, ...pwCache, 'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  path.join(process.env.LOCALAPPDATA || '', 'Google/Chrome/Application/chrome.exe'), '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'].filter(Boolean).find((p) => fs.existsSync(p));

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.otf': 'font/otf', '.ttf': 'font/ttf', '.woff2': 'font/woff2' };
const srv = await new Promise((ok) => {
  const s = http.createServer((q, r) => {
    const u = decodeURIComponent(q.url.split('?')[0]);
    const p = u.startsWith('/datos/') ? path.join(DIR_DATOS, u.slice(7)) : path.join(RAIZ, u);
    if (!(p.startsWith(RAIZ) || p.startsWith(DIR_DATOS)) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); r.end(); return; }
    r.writeHead(200, { 'Content-Type': MIME[path.extname(p).toLowerCase()] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r);
  });
  s.listen(0, '127.0.0.1', () => ok(s));
});
const url = `http://127.0.0.1:${srv.address().port}/estilos/${encodeURIComponent(ESTILO)}/plantilla.html?formato=${FORMATO}&datos=${encodeURIComponent('/datos/')}`;

const browser = await chromium.launch({ executablePath: chrome, args: ['--disable-gpu-vsync', '--force-color-profile=srgb', '--font-render-hinting=none'] });
const est = JSON.parse(fs.readFileSync(path.join(RAIZ, 'estilos', ESTILO, 'estilo.json'), 'utf8'));
const F = est.formatos[FORMATO];
const page = await browser.newPage({ viewport: { width: F.ancho, height: F.alto }, deviceScaleFactor: ESCALA });
page.on('pageerror', (e) => console.error('Error en la página:', e.message));
await page.goto(url);
const info = await page.evaluate(async () => { await window.listo; return window.subtitulos; });
const desde = Number(opt('desde', 0)), hasta = Number(opt('hasta', info.duracion));
const N = Math.round((hasta - desde) * FPS);

const nvenc = spawnSync('ffmpeg', ['-hide_banner', '-v', 'error', '-f', 'lavfi', '-i', 'color=black:s=256x256:d=0.1', '-c:v', 'h264_nvenc', '-f', 'null', '-']).status === 0;
const venc = nvenc ? ['-c:v', 'h264_nvenc', '-preset', 'p5', '-rc', 'vbr', '-cq', '23', '-b:v', '0'] : ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22'];
fs.mkdirSync(path.dirname(SALIDA), { recursive: true });
const ff = TRANSP
  ? ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', SALIDA]
  : ['-y', '-v', 'error', '-ss', String(desde), '-t', String(hasta - desde), '-i', CLIP, '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
     '-filter_complex', `[0:v]scale=${F.ancho * ESCALA}:${F.alto * ESCALA},fps=${FPS},setsar=1[b];[b][1:v]overlay=0:0:eof_action=pass,format=yuv420p[v]`, '-map', '[v]', '-map', '0:a?',
     ...venc, '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', '-shortest', SALIDA];
const p = spawn('ffmpeg', ff, { stdio: ['pipe', 'inherit', 'inherit'] });
const t0 = Date.now();
for (let i = 0; i < N; i++) {
  await page.evaluate((t) => window.seek(t), desde + i / FPS);
  const png = await page.screenshot({ type: 'png', omitBackground: true });
  if (!p.stdin.write(png)) await new Promise((r) => p.stdin.once('drain', r));
}
p.stdin.end();
await new Promise((r) => p.on('close', r));
await browser.close(); srv.close();
console.log(`✓ ${SALIDA} · ${N} fotogramas · ${((Date.now() - t0) / 1000).toFixed(1)} s`);

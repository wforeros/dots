// SynthFlow Studio sin interfaz: genera la MÚSICA de fondo o los EFECTOS en WAV, sin descargar nada (todo es síntesis, sin derechos).
//
//   node scripts/synthflow_render.mjs music synthwave 40 musica.wav     (géneros: synthwave | lofi)
//   node scripts/synthflow_render.mjs sfx sfx/                          (whoosh, impact, riser, uiclick, glitch, braaam)
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

try { os.setPriority(os.constants.priority.PRIORITY_BELOW_NORMAL); } catch {}
const SKILL = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const { chromium } = createRequire(path.join(SKILL, 'package.json'))('playwright');
const pwCache = (() => { try { const d = path.join(os.homedir(), '.cache', 'ms-playwright'); return fs.readdirSync(d).filter((n) => n.startsWith('chromium-')).sort().reverse().flatMap((n) => [path.join(d, n, 'chrome-linux64', 'chrome'), path.join(d, n, 'chrome-linux', 'chrome')]); } catch { return []; } })();
const chrome = [process.env.CHROME_PATH, ...pwCache, 'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  path.join(process.env.LOCALAPPDATA || '', 'Google/Chrome/Application/chrome.exe'), 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium'].filter(Boolean).find((p) => fs.existsSync(p));
if (!chrome) { console.error('No encuentro Chrome ni Edge. Instala Google Chrome.'); process.exit(1); }
const [mode = 'music', ...rest] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: chrome, args: ['--autoplay-policy=no-user-gesture-required'] });
const page = await browser.newPage();
page.on('pageerror', (e) => console.error('Error en SynthFlow:', e.message));
await page.goto('file:///' + path.join(SKILL, 'synthflow', 'synthflow.html').replace(/\\/g, '/'), { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1500);
await page.evaluate(() => { window.__toB64 = async (blob) => { const b = new Uint8Array(await blob.arrayBuffer()); let s = ''; for (let i = 0; i < b.length; i += 0x8000) s += String.fromCharCode.apply(null, b.subarray(i, i + 0x8000)); return btoa(s); }; });
if (mode === 'music') {
  const [genre = 'synthwave', secs = '40', out = 'musica.wav'] = rest;
  const b64 = await page.evaluate(async ([g, s]) => { selectGenre(g); const buf = await renderProceduralTrackOffline(Number(s), 48000); return window.__toB64(encodeAudioBufferToWAV(buf, 16, false, true)); }, [genre, secs]);
  fs.writeFileSync(path.resolve(out), Buffer.from(b64, 'base64'));
  console.log(`música ${genre} · ${secs} s → ${out}`);
} else if (mode === 'sfx') {
  const dir = path.resolve(rest[0] || 'sfx'); fs.mkdirSync(dir, { recursive: true });
  for (const type of ['whoosh', 'impact', 'riser', 'uiclick', 'glitch', 'braaam']) {
    const b64 = await page.evaluate(async (type) => { let c = null; const o = window.downloadBlob; window.downloadBlob = (b) => { c = b; }; try { await downloadSingleSFX(type); } finally { window.downloadBlob = o; } return c ? window.__toB64(c) : null; }, type);
    if (b64) { fs.writeFileSync(path.join(dir, type + '.wav'), Buffer.from(b64, 'base64')); console.log('efecto →', path.join(dir, type + '.wav')); }
  }
} else console.error('Modo desconocido. Usa: music | sfx');
await browser.close();

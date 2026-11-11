"""Comprueba que el ordenador tiene todo lo que necesita la skill (Windows y Mac) y dice cómo instalar lo que falte.

  python comprobar_equipo.py              → informe
  python comprobar_equipo.py --instalar   → instala SOLO lo de dentro de la skill (Playwright) y Whisper con pip.
                                            El agente lo lanza únicamente después de que la persona diga «sí».
Programas: Python 3.10+, ffmpeg, Node 18+, Google Chrome, Whisper (openai-whisper) y Playwright (dentro de la skill).
"""
import glob, os, platform, re, shutil, subprocess, sys

for s in (sys.stdout, sys.stderr):
    try: s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAC, WIN = platform.system() == "Darwin", platform.system() == "Windows"
COMO = {
    "ffmpeg": "winget install Gyan.FFmpeg" if WIN else "brew install ffmpeg",
    "node": "winget install OpenJS.NodeJS.LTS" if WIN else "brew install node",
    "chrome": "winget install Google.Chrome" if WIN else "descárgalo de https://www.google.com/chrome/",
    "whisper": f'"{sys.executable}" -m pip install -U openai-whisper',
    "playwright": f'cd "{SKILL}" && npm install',
}


def ver(cmd):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout.strip().splitlines()[0]
    except Exception: return ""


def chrome():
    rutas = [os.environ.get("CHROME_PATH", ""), r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
             os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Google\Chrome\Application\chrome.exe"), "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
             "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
             *sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome")), reverse=True)]
    return next((r for r in rutas if r and os.path.exists(r)), "")


def whisper_python():
    """El Python que ya tiene Whisper: este, o cualquier otro instalado (py -0p en Windows, python3.x en Mac)."""
    cands = [[sys.executable]]
    if WIN and shutil.which("py"):
        for l in ver_todo(["py", "-0p"]):
            m = re.search(r"([A-Za-z]:\\.+?\.exe)", l)   # rutas con espacios (C:\Users\John Doe\…)
            p = m.group(1) if m else (l.split()[-1] if l.strip() else "")
            if p.lower().endswith("python.exe"): cands.append([p])
    # venv dedicado (recomendado en Linux: torch no tiene wheels para Python 3.14+)
    for v in sorted(glob.glob(os.path.expanduser("~/.venvs/*/bin/python*"))):
        cands.append([v])
    for n in ("python3.13", "python3.12", "python3.11", "python3.10", "python3"):
        if shutil.which(n): cands.append([shutil.which(n)])
    for c in cands:
        if subprocess.run(c + ["-c", "import whisper"], capture_output=True).returncode == 0: return c[0]
    return ""


def ver_todo(cmd):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout.splitlines()
    except Exception: return []


res = {
    "python": (sys.version_info >= (3, 10), f"Python {platform.python_version()}"),
    "ffmpeg": (bool(shutil.which("ffmpeg")), ver(["ffmpeg", "-version"])[:40]),
    "node": (bool(shutil.which("node")) and ver(["node", "-v"]).lstrip("v").split(".")[0].isdigit() and int(ver(["node", "-v"]).lstrip("v").split(".")[0]) >= 18, ver(["node", "-v"])),
    "chrome": (bool(chrome()), chrome()),
    "whisper": (bool(WPY := whisper_python()), f"Python para Whisper: {WPY}"),
    "playwright": (os.path.isdir(os.path.join(SKILL, "node_modules", "playwright")), "dentro de la skill"),
}

if "--instalar" in sys.argv:
    if not res["playwright"][0] and shutil.which("npm"):
        print("Instalando Playwright dentro de la skill (usa tu Chrome, no descarga otro navegador)…")
        subprocess.run("npm install --no-audit --no-fund", shell=True, cwd=SKILL, env={**os.environ, "PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD": "1"})
    if not res["whisper"][0]:
        print("Instalando Whisper (la transcripción, unos 2 GB con sus dependencias)…")
        subprocess.run([sys.executable, "-m", "pip", "install", "-U", "openai-whisper"])
    sys.exit(0)

print(f"Sistema: {platform.system()} {platform.machine()}")
falta = []
for k, (ok, det) in res.items():
    print(f"  {'✓' if ok else '✗'} {k:<11} {det if ok else 'FALTA'}")
    if not ok: falta.append(k)
if falta:
    print("\nFALTA:")
    for k in falta:
        print(f"  {k}: {COMO.get(k, 'instala Python 3.10+ desde https://www.python.org/downloads/ (marca «Add to PATH» en Windows)')}")
    print("\nDespués de instalar ffmpeg o Node, cierra y vuelve a abrir Pi para que los encuentre.")
else:
    print("\nTodo listo ✓")
gpu = subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=black:s=256x256:d=0.1", "-c:v", "h264_nvenc", "-f", "null", "-"], capture_output=True).returncode == 0 if res["ffmpeg"][0] else False
if WPY and os.path.normcase(WPY) != os.path.normcase(sys.executable):
    print(f"\nAVISO: Whisper está en otro Python. Para transcribir usa: \"{WPY}\" scripts/transcribir.py …  (no lo instales otra vez)")
print(f"Velocidad: {'rápida (tarjeta NVIDIA)' if gpu else 'normal (sin tarjeta NVIDIA): un reel de 45 s tarda unos 10-20 min'}")

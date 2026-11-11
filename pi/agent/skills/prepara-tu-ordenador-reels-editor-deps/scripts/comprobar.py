"""Preparar equipo (Viegas Estudio, gratis) · comprobar el ordenador (NO instala nada).

  python comprobar.py              → informe legible con ✓ / ✗ y la solución de cada fallo
  python comprobar.py --json       → lo mismo en JSON (para Claude)
  python comprobar.py --informe RUTA.md   → además guarda el informe en un archivo Markdown

Solo usa la biblioteca estándar de Python: funciona aunque falte todo lo demás.
Windows y Mac (Linux también, de forma básica).
"""
import argparse, ctypes, datetime, importlib.util, json, os, platform, re, shutil, subprocess, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OS = {"Windows": "windows", "Darwin": "mac"}.get(platform.system(), "linux")
HOME = os.path.expanduser("~")

ap = argparse.ArgumentParser()
ap.add_argument("--json", action="store_true")
ap.add_argument("--informe", default="")
a = ap.parse_args()


def run(cmd, timeout=20):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           shell=(OS == "windows" and cmd[0] in ("npm", "npx", "claude")))
        return r.returncode, ((r.stdout or "") + (r.stderr or "")).strip()
    except Exception as e:
        return -1, str(e)


# Comandos de instalación (Claude los ejecuta SOLO con permiso del alumno, uno a uno)
INSTALAR = {
    "node":     {"windows": "winget install -e --id OpenJS.NodeJS.LTS", "mac": "brew install node", "linux": "sudo apt install -y nodejs npm"},
    "ffmpeg":   {"windows": "winget install -e --id Gyan.FFmpeg", "mac": "brew install ffmpeg", "linux": "sudo apt install -y ffmpeg"},
    "python":   {"windows": "winget install -e --id Python.Python.3.12", "mac": "brew install python@3.12", "linux": "sudo apt install -y python3 python3-pip"},
    "git":      {"windows": "winget install -e --id Git.Git", "mac": "xcode-select --install   (o: brew install git)", "linux": "sudo apt install -y git"},
    "chrome":   {"windows": "winget install -e --id Google.Chrome", "mac": "brew install --cask google-chrome", "linux": "sudo apt install -y chromium"},
    "playwright": {k: "npx -y playwright@1.48.2 install chromium" for k in ("windows", "mac", "linux")},
    "whisper":  {k: "{PY} -m pip install --user faster-whisper" for k in ("windows", "mac", "linux")},
    "brew":     {"mac": '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'},
    "winget":   {"windows": "Abre Microsoft Store, busca «Instalador de aplicación» (App Installer) y pulsa Actualizar"},
}

items = []


def add(key, nombre, ok, detalle, para, obligatorio=True, fix_key=None, aviso=False):
    fix = None
    if not ok:
        fix = INSTALAR.get(fix_key or key, {}).get(OS)
    items.append({"item": key, "nombre": nombre, "ok": bool(ok), "aviso": aviso, "detalle": detalle,
                  "para": para, "obligatorio": obligatorio, "instalar": fix})


def version_num(txt):
    m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", txt or "")
    return tuple(int(x or 0) for x in m.groups()) if m else (0, 0, 0)


# ---------- Sistema ----------
sistema = {"so": OS, "version": platform.platform(), "arquitectura": platform.machine(), "python_que_ejecuta": sys.executable}

# Gestor de paquetes
if OS == "windows":
    c, o = run(["winget", "--version"])
    add("winget", "winget (instalador de Windows)", c == 0, o.splitlines()[0] if c == 0 else "no encontrado", "instalar el resto con un comando")
elif OS == "mac":
    p = shutil.which("brew") or next((x for x in ("/opt/homebrew/bin/brew", "/usr/local/bin/brew") if os.path.exists(x)), None)
    add("brew", "Homebrew (instalador de Mac)", bool(p), p or "no encontrado", "instalar el resto con un comando")

# ---------- Programas ----------
c, o = run(["node", "--version"])
v = version_num(o)
add("node", "Node.js LTS", c == 0 and v[0] >= 18, (o if c == 0 else "no encontrado") + ("" if c != 0 or v[0] >= 18 else " · demasiado antiguo (hace falta 18 o más)"),
    "el panel de revisión, los motion graphics y Playwright")

c, o = run(["ffmpeg", "-version"])
add("ffmpeg", "FFmpeg", c == 0, o.splitlines()[0][:60] if c == 0 else "no encontrado", "cortar, unir y exportar vídeo y audio")
add("ffprobe", "FFprobe", shutil.which("ffprobe") is not None, shutil.which("ffprobe") or "no encontrado", "leer duración y tamaño de los vídeos", fix_key="ffmpeg")

# Python: buscamos el mejor (3.11+) entre los instalados
pythons = []
cands = [sys.executable]
if OS == "windows":
    c, o = run(["py", "-0p"])
    if c == 0:
        cands += [ln.split()[-1] for ln in o.splitlines() if ln.strip().endswith(".exe")]
for n in ("python3", "python", "python3.12", "python3.11"):
    w = shutil.which(n)
    if w:
        cands.append(w)
vistos = set()
for p in cands:
    rp = os.path.realpath(p).lower()
    if rp in vistos or "windowsapps" in rp:  # el «python» falso de la Microsoft Store
        continue
    vistos.add(rp)
    c, o = run([p, "-c", "import sys,importlib.util as u;print(sys.version.split()[0]);print(int(bool(u.find_spec('faster_whisper'))),int(bool(u.find_spec('whisper'))),int(bool(u.find_spec('torch'))))"])
    if c == 0:
        ls = o.splitlines()
        fw, w, t = (int(x) for x in ls[1].split())
        pythons.append({"ruta": p, "version": ls[0], "faster_whisper": bool(fw), "whisper": bool(w), "torch": bool(t)})
buenos = [p for p in pythons if version_num(p["version"]) >= (3, 11, 0)]
# preferimos el que ya tiene whisper
mejor = sorted(buenos, key=lambda p: (p["faster_whisper"] or p["whisper"], p["torch"], version_num(p["version"])), reverse=True)
mejor = mejor[0] if mejor else None
add("python", "Python 3.11 o más", bool(mejor), f"Python {mejor['version']} · {mejor['ruta']}" if mejor else
    ("solo versiones antiguas: " + ", ".join(p["version"] for p in pythons) if pythons else "no encontrado"), "transcribir y analizar los clips")

c, o = run(["git", "--version"])
add("git", "Git", c == 0, o if c == 0 else "no encontrado", "descargar herramientas y guardar versiones", obligatorio=False)

# Chrome / Chromium de Playwright
chrome = None
if OS == "windows":
    for base in (os.environ.get("ProgramFiles", ""), os.environ.get("ProgramFiles(x86)", ""), os.environ.get("LOCALAPPDATA", "")):
        p = os.path.join(base, "Google", "Chrome", "Application", "chrome.exe")
        if base and os.path.exists(p):
            chrome = p
    if not chrome:
        for base in (os.environ.get("ProgramFiles(x86)", ""), os.environ.get("ProgramFiles", "")):
            p = os.path.join(base, "Microsoft", "Edge", "Application", "msedge.exe")
            if base and os.path.exists(p):
                chrome = p + " (Edge: también vale)"
elif OS == "mac":
    p = "/Applications/Google Chrome.app"
    chrome = p if os.path.exists(p) else None
else:
    chrome = shutil.which("google-chrome") or shutil.which("chromium")
pw_dir = {"windows": os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright"),
          "mac": os.path.join(HOME, "Library", "Caches", "ms-playwright")}.get(OS, os.path.join(HOME, ".cache", "ms-playwright"))
pw = os.path.isdir(pw_dir) and any(d.startswith("chromium") for d in os.listdir(pw_dir))
add("chrome", "Chrome o Edge", bool(chrome), chrome or "no encontrado", "ver las guías y el panel de revisión", obligatorio=False)
add("playwright", "Navegador de Playwright", pw, pw_dir if pw else "no descargado", "renderizar motion graphics en HTML", obligatorio=False)

# Whisper
if mejor and (mejor["faster_whisper"] or mejor["whisper"]):
    cual = "faster-whisper" if mejor["faster_whisper"] else "whisper (OpenAI)"
    add("whisper", "Whisper (transcripción)", True, f"{cual} en {mejor['ruta']}", "transcribir lo que dices palabra a palabra")
else:
    otro = next((p for p in pythons if p["faster_whisper"] or p["whisper"]), None)
    add("whisper", "Whisper (transcripción)", False, f"está en otro Python ({otro['ruta']})" if otro else "no instalado",
        "transcribir lo que dices palabra a palabra")
    if items[-1]["instalar"]:
        items[-1]["instalar"] = items[-1]["instalar"].replace("{PY}", f'"{mejor["ruta"]}"' if mejor else "python")

# Claude Code
c, o = run(["claude", "--version"])
add("claude", "Claude Code", c == 0, o.splitlines()[0] if c == 0 else "no encontrado en el PATH (si estás hablando con Claude Code, ya lo tienes)",
    "todo", obligatorio=False)

# ---------- Hardware ----------
def ram_gb():
    try:
        if OS == "windows":
            class M(ctypes.Structure):
                _fields_ = [("l", ctypes.c_ulong), ("m", ctypes.c_ulong), ("t", ctypes.c_ulonglong), ("a", ctypes.c_ulonglong),
                            ("tp", ctypes.c_ulonglong), ("ap", ctypes.c_ulonglong), ("tv", ctypes.c_ulonglong), ("av", ctypes.c_ulonglong), ("e", ctypes.c_ulonglong)]
            m = M(); m.l = ctypes.sizeof(M)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            return m.t / 1024 ** 3
        if OS == "mac":
            return int(run(["sysctl", "-n", "hw.memsize"])[1]) / 1024 ** 3
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1024 ** 3
    except Exception:
        return 0


gpu, vram = "", 0
c, o = run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"])
if c == 0 and o:
    n, m = o.splitlines()[0].rsplit(",", 1)
    gpu, vram = n.strip(), round(int(m) / 1024)
elif OS == "mac":
    chip = run(["sysctl", "-n", "machdep.cpu.brand_string"])[1]
    gpu = chip + (" (Apple Silicon: buena para vídeo)" if "Apple" in chip else " (Mac Intel: irá lento)")
elif OS == "windows":
    c, o = run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_VideoController).Name"])
    gpu = (o.splitlines() or [""])[0] if c == 0 else ""

ram = round(ram_gb())
libre = round(shutil.disk_usage(HOME).free / 1024 ** 3)
apple = OS == "mac" and "Apple" in gpu
nvidia = vram > 0

add("ram", "Memoria RAM", ram >= 8, f"{ram} GB (mínimo 8 · recomendado 16 o más)", "abrir vídeos 4K sin que se cuelgue", aviso=8 <= ram < 16)
add("disco", "Espacio libre en disco", libre >= 20, f"{libre} GB libres (mínimo 20 · recomendado 100)", "copias de trabajo y exportaciones", aviso=20 <= libre < 100)
add("gpu", "Tarjeta gráfica", nvidia or apple, (f"{gpu} · {vram} GB" if nvidia else gpu or "no detectada") +
    ("" if nvidia or apple else " · funcionará, pero transcribir y exportar será lento"), "transcribir y exportar rápido", obligatorio=False)

if nvidia and vram >= 8 or apple and ram >= 16:
    perfil = "rápido"
elif nvidia or apple:
    perfil = "medio"
else:
    perfil = "lento"
calidad = "4K" if perfil == "rápido" else "1080p"

oblig_fallan = [i for i in items if i["obligatorio"] and not i["ok"]]
llega = ram >= 8 and libre >= 20
resumen = {
    "llega_al_minimo": llega,
    "todo_listo": llega and not oblig_fallan,
    "perfil": perfil,
    "calidad_recomendada": calidad,
    "python_recomendado": mejor["ruta"] if mejor else None,
    "faltan": [i["item"] for i in items if not i["ok"]],
}

SOLUCIONES = [
    ("«winget no se reconoce»", "Actualiza «Instalador de aplicación» en Microsoft Store y abre una terminal nueva."),
    ("Instalé algo y sigue saliendo ✗", "Cierra Claude Code y ábrelo otra vez: los programas nuevos solo se ven en una sesión nueva."),
    ("«python» abre la Microsoft Store", "Es un acceso falso de Windows. Instala Python con winget y desactiva «Alias de ejecución de aplicaciones» para python en Configuración."),
    ("brew: command not found (Mac)", "Tras instalar Homebrew, ejecuta las dos líneas «eval ...» que te muestra al final, o abre una terminal nueva."),
    ("pip: «externally-managed-environment» (Mac)", "Usa: python3 -m pip install --user --break-system-packages faster-whisper, o pide a Claude que cree un entorno virtual."),
    ("Whisper muy lento", "Sin tarjeta NVIDIA ni Apple Silicon es normal. Usa el modelo «small» (más rápido, algo menos preciso)."),
    ("Permiso denegado / acceso denegado", "Acepta el aviso de Windows (UAC) o escribe tu contraseña del Mac cuando te la pida el instalador. Claude nunca la escribe por ti."),
    ("Playwright no descarga", "Comprueba tu conexión o el antivirus/proxy de empresa; vuelve a intentarlo en otra red."),
]


def texto():
    L = ["# Informe del equipo · Preparar equipo (Viegas Estudio)", f"_{datetime.datetime.now():%d/%m/%Y %H:%M} · {sistema['version']}_", ""]
    for i in items:
        marca = "✓" if i["ok"] and not i["aviso"] else ("!" if i["ok"] else ("✗" if i["obligatorio"] else "·"))
        L.append(f"{marca} **{i['nombre']}** — {i['detalle']}  _(para {i['para']})_")
        if i["instalar"]:
            L.append(f"    → Cómo se arregla: `{i['instalar']}`")
    L += ["", f"**Tarjeta / chip:** {gpu or 'no detectada'} · **RAM:** {ram} GB · **Disco libre:** {libre} GB",
          f"**Perfil:** {perfil} · **Calidad recomendada para exportar:** {calidad}",
          f"**¿Llega al mínimo?** {'Sí' if llega else 'No (mira RAM y disco)'} · **¿Todo listo?** {'Sí ✓' if resumen['todo_listo'] else 'Todavía no'}",
          "", "## Si algo falla"] + [f"- **{p}**: {s}" for p, s in SOLUCIONES]
    L += ["", "_Leyenda: ✓ bien · ! funciona pero justo · ✗ falta y hace falta · · opcional_"]
    return "\n".join(L)


out = {"sistema": sistema, "hardware": {"gpu": gpu, "vram_gb": vram, "ram_gb": ram, "disco_libre_gb": libre},
       "items": items, "pythons": pythons, "resumen": resumen, "soluciones": SOLUCIONES}
if a.informe:
    with open(a.informe, "w", encoding="utf-8") as f:
        f.write(texto() + "\n")
print(json.dumps(out, ensure_ascii=False, indent=1) if a.json else texto())
if not a.json and resumen["todo_listo"]:
    print("\n✅ Tu equipo ya está listo." + (f" Tarjeta detectada: {gpu}." if gpu else ""))

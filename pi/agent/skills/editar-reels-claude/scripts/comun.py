"""Utilidades compartidas: qué codificador de vídeo y qué dispositivo de PyTorch usar en este ordenador.

  NVIDIA (Windows / Linux) → h264_nvenc + CUDA       (rápido)
  Mac con Apple Silicon    → h264_videotoolbox + MPS (medio)
  Sin tarjeta gráfica      → libx264 + CPU           (lento, pero funciona)
"""
import functools, platform, subprocess, sys

for _s in (sys.stdout, sys.stderr):   # la consola de Windows no es UTF-8 por defecto (→, ×, ñ…)
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


@functools.lru_cache(None)
def encoder_ok(name):
    """Prueba de verdad el codificador (estar compilado en ffmpeg no basta: NVENC necesita la tarjeta)."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=320x240:d=0.2", "-c:v", name, "-f", "null", "-"],
                       capture_output=True)
    return r.returncode == 0


def pick_encoder(mode="auto"):
    """mode: auto | nvenc | videotoolbox | cpu"""
    if mode in ("nvenc", "videotoolbox", "cpu"):
        return mode
    if encoder_ok("h264_nvenc"):
        return "nvenc"
    if platform.system() == "Darwin" and encoder_ok("h264_videotoolbox"):
        return "videotoolbox"
    return "cpu"


def venc(kind="hq", mode="auto", w=2160, h=3840, fps=30):
    """Argumentos de vídeo para ffmpeg. kind: hq (máster de trabajo) | lq (vista previa ligera)."""
    enc = pick_encoder(mode)
    if enc == "nvenc":
        return ["-c:v", "h264_nvenc", "-preset", "p6" if kind == "hq" else "p5", "-rc", "vbr", "-cq", "17" if kind == "hq" else "28", "-b:v", "0"]
    if enc == "videotoolbox":
        bpp = 0.25 if kind == "hq" else 0.06   # bits por píxel: ~62 Mb/s en 4K30 para el máster
        return ["-c:v", "h264_videotoolbox", "-b:v", f"{int(w * h * fps * bpp / 1e6)}M", "-allow_sw", "1"]
    return ["-c:v", "libx264", "-preset", "medium" if kind == "hq" else "veryfast", "-crf", "16" if kind == "hq" else "26"]


def add_enc_args(ap):
    ap.add_argument("--enc", default="auto", choices=["auto", "nvenc", "videotoolbox", "cpu"], help="codificador de vídeo (auto lo detecta)")
    ap.add_argument("--gpu", action="store_true", help="equivale a --enc nvenc (se mantiene por compatibilidad)")


def enc_mode(a):
    return "nvenc" if getattr(a, "gpu", False) else a.enc


def torch_device(allow_mps=True):
    import torch
    if torch.cuda.is_available():
        return "cuda"
    if allow_mps and getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def probe(path):
    """(ancho, alto, fps) del primer stream de vídeo."""
    import json
    st = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate", "-of", "json", path],
                                   capture_output=True, text=True, check=True).stdout)["streams"][0]
    n, d = st["r_frame_rate"].split("/")
    return st["width"], st["height"], round(float(n) / float(d or 1))

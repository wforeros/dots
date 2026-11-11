"""Pasada 0 · Preparar la toma.
Copia la fuente a la carpeta de trabajo (nunca se edita el original), la pone en vertical y extrae el audio.

  python prepare.py --src "mi toma.mp4" --work trabajo --res 4k
  python prepare.py --src "mi toma.mp4" --work trabajo --res 1080 --crop 0.5     (horizontal normal → recorta el centro)
  python prepare.py --src "mi toma.mp4" --work trabajo --rotate 90               (cámara de lado → gira)

Vídeo horizontal: el script NO adivina. Guarda trabajo/fotograma.jpg y se detiene. Mira el fotograma:
  - la persona sale tumbada (la cámara estaba de lado) → --rotate 90 (o 270 si sale cabeza abajo con 90)
  - la persona sale derecha (plano horizontal normal)   → --crop 0.5 (0 = borde izquierdo, 1 = derecho; centra a la persona)
--res: 4k (2160×3840) | 1080 (1080×1920, mucho más rápido sin tarjeta gráfica)
Salida en --work: source.*, fotograma.jpg, vertical.mp4, audio16k.wav (para Whisper), audio48k.wav (para la mezcla).
"""
import argparse, json, os, shutil, subprocess, sys
from comun import add_enc_args, enc_mode, pick_encoder, venc

ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True)
ap.add_argument("--work", default="trabajo")
ap.add_argument("--res", default="4k", choices=["4k", "1080"])
ap.add_argument("--rotate", default="auto", choices=["auto", "0", "90", "180", "270"])
ap.add_argument("--crop", type=float, default=None, help="recorta a 9:16 un vídeo horizontal; posición horizontal 0-1")
ap.add_argument("--fps", type=int, default=30)
add_enc_args(ap)
a = ap.parse_args()

os.makedirs(a.work, exist_ok=True)
src = os.path.join(a.work, "source" + os.path.splitext(a.src)[1].lower())
if not (os.path.exists(src) and os.path.getsize(src) == os.path.getsize(a.src)):
    shutil.copy2(a.src, src)

# ffprobe ya aplica la rotación de los metadatos del móvil, así que w×h es lo que se ve.
info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,codec_name,r_frame_rate:stream_side_data=rotation:format=duration",
                                  "-of", "json", src], capture_output=True, text=True, check=True).stdout)
st = info["streams"][0]
w, h = st["width"], st["height"]
rot_meta = next((abs(int(sd.get("rotation", 0))) for sd in st.get("side_data_list", []) if "rotation" in sd), 0)
if rot_meta in (90, 270):
    w, h = h, w
dur = float(info["format"]["duration"])
print(f"fuente: {w}×{h} {st['codec_name']} {st['r_frame_rate']} fps · {dur:.2f} s")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(min(1.0, dur / 2)), "-i", src, "-frames:v", "1", "-vf", "scale=-2:720", os.path.join(a.work, "fotograma.jpg")], check=True)

rot = a.rotate
if rot == "auto":
    if w > h and a.crop is None:
        print("\nVÍDEO HORIZONTAL. Mira trabajo/fotograma.jpg y vuelve a lanzar con:\n"
              "  --rotate 90 (o 270)  si la persona sale tumbada (la cámara estaba de lado)\n"
              "  --crop 0.5           si sale derecha (recorta el centro a 9:16; ajusta 0-1 para centrar a la persona)")
        sys.exit(2)
    rot = "0"
vf = {"0": [], "90": ["transpose=1"], "180": ["transpose=1,transpose=1"], "270": ["transpose=2"]}[rot]
if a.crop is not None:
    x = max(0.0, min(1.0, a.crop))
    vf.append(f"crop=ih*9/16:ih:(iw-ih*9/16)*{x:.3f}:0")
W, H = (2160, 3840) if a.res == "4k" else (1080, 1920)
vf += [f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos", f"crop={W}:{H}", f"fps={a.fps}", "setsar=1"]
if a.res == "4k" and max(w, h) < 3000:
    print("aviso: la fuente no es 4K; se escala hacia arriba. Con --res 1080 irá más rápido y se verá igual.")

mode = enc_mode(a)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", ",".join(vf), *venc("hq", mode, W, H, a.fps), "-pix_fmt", "yuv420p", "-an",
                os.path.join(a.work, "vertical.mp4")], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", os.path.join(a.work, "audio16k.wav")], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-c:a", "pcm_s24le", "-ar", "48000", os.path.join(a.work, "audio48k.wav")], check=True)
print(f"listo · {W}×{H} · giro {rot}°{' · recorte ' + str(a.crop) if a.crop is not None else ''} · {a.fps} fps · codificador {pick_encoder(mode)}"
      f" → {a.work}/vertical.mp4, audio16k.wav, audio48k.wav")

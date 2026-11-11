"""Pasada 1B · Cortar pausas y tomas falsas y recalcular words.json en la línea de tiempo nueva.

  python cut.py --work trabajo --keep trabajo/keep.json [--enc auto] [--words-only]

keep.json (lo escribe Claude tras analyze.py y lo aprueba el humano):
{
  "segments": [[2.70, 7.57], [8.14, 14.79]],     ← tramos que SE QUEDAN (segundos del original), con ~0,1 s de respiración
  "fixes": {"CloudCode": "Claude Code", ".5.": null}   ← correcciones de palabras (null = borrar)
}
Salida: cut.mp4 (máster), preview.mp4 (1080×1920 ligera), words.json (el reloj de todo el proyecto).
"""
import argparse, json, os, subprocess
from comun import add_enc_args, enc_mode, probe, venc

ap = argparse.ArgumentParser()
ap.add_argument("--work", default="trabajo")
ap.add_argument("--keep", required=True)
ap.add_argument("--fps", type=int, default=30)
add_enc_args(ap)
ap.add_argument("--words-only", action="store_true")
a = ap.parse_args()
P = lambda f: os.path.join(a.work, f)

cfg = json.load(open(a.keep, encoding="utf-8"))
snap = lambda t: round(t * a.fps) / a.fps
KEEP = [(snap(s), snap(e)) for s, e in cfg["segments"]]
FIX = cfg.get("fixes", {})

# Cada palabra va al tramo con el que más se solapa (nunca por el punto medio: se pierden palabras cortas).
raw = json.load(open(P("words-raw.json"), encoding="utf-8"))["words"]
offs, t = [], 0.0
for s, e in KEEP:
    offs.append(t); t += e - s
words = []
for w in raw:
    best, ov = None, 0.0
    for i, (s, e) in enumerate(KEEP):
        o = min(w["end"], e) - max(w["start"], s)
        if o > ov:
            best, ov = i, o
    if best is None or ov < min(0.15, 0.5 * (w["end"] - w["start"])):
        continue
    txt = FIX.get(w["w"], w["w"])
    if txt is None:
        continue
    s, e = KEEP[best]
    words.append({"w": txt, "start": round(max(w["start"], s) - s + offs[best], 3), "end": round(min(w["end"], e) - s + offs[best], 3)})
json.dump({"duration": round(t, 3), "fps": a.fps, "segments": KEEP, "words": words}, open(P("words.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"duración → {t:.2f} s · {len(KEEP)} tramos · {len(words)} palabras")
print(" ".join(x["w"] for x in words))
if a.words_only:
    raise SystemExit

W, H, _ = probe(P("vertical.mp4"))
venc_hq = venc("hq", enc_mode(a), W, H, a.fps)
venc_lq = venc("lq", enc_mode(a), 1080, 1920, a.fps)


def build(out, tail, venc):
    parts, labels = [], ""
    for i, (s, e) in enumerate(KEEP):
        d = e - s
        parts.append(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS{tail}[v{i}]")
        parts.append(f"[1:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={d - 0.012:.3f}:d=0.012[a{i}]")
        labels += f"[v{i}][a{i}]"
    parts.append(f"{labels}concat=n={len(KEEP)}:v=1:a=1[v][a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", P("vertical.mp4"), "-i", P("audio48k.wav"), "-filter_complex", ";".join(parts),
                    "-map", "[v]", "-map", "[a]", *venc, "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", P(out)], check=True)


build("cut.mp4", "", venc_hq)
build("preview.mp4", ",scale=1080:-2:flags=lanczos", venc_lq)
print("ok → cut.mp4, preview.mp4, words.json")

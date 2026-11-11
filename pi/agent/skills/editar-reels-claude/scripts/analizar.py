"""Pasada 1A · Qué cortar: tabla de palabras, pausas > 0,4 s, repeticiones (tomas falsas) y silencios reales del audio.

  python analyze.py --words trabajo/words-raw.json --audio trabajo/audio48k.wav

Ojo: Whisper alarga palabras sobre los silencios. Los puntos de corte se afinan con el audio
(silencios de ffmpeg y, si hace falta, --rms 44.9:46.4 para ver la energía cada 50 ms en un tramo).
"""
import argparse, json, re, subprocess
import comun  # consola UTF-8 en Windows

ap = argparse.ArgumentParser()
ap.add_argument("--words", required=True)
ap.add_argument("--audio", required=True)
ap.add_argument("--pause", type=float, default=0.4)
ap.add_argument("--silence-db", type=float, default=-38)
ap.add_argument("--rms", default="", help="tramo inicio:fin para ver la energía cada 50 ms")
a = ap.parse_args()

W = json.load(open(a.words, encoding="utf-8"))["words"]
print("Nº  palabra              inicio   fin     prob")
for i, w in enumerate(W):
    print(f"{i:3d} {w['w']:<20} {w['start']:7.2f} {w['end']:7.2f}  {w['p']:.2f}{' ?' if w['p'] < 0.6 else ''}")

print(f"\nPAUSAS ENTRE PALABRAS > {a.pause} s")
print(f"  inicio: {W[0]['start']:.2f} s de aire antes de «{W[0]['w']}»")
for i in range(1, len(W)):
    gap = W[i]["start"] - W[i - 1]["end"]
    if gap > a.pause:
        print(f"  {W[i-1]['end']:6.2f} → {W[i]['start']:6.2f} ({gap:.2f} s) entre «{W[i-1]['w']}» y «{W[i]['w']}»")

print("\nREPETICIONES (posibles tomas falsas)")
norm = [re.sub(r"[^\wáéíóúñü]", "", w["w"].lower()) for w in W]
for n in range(1, 7):
    for i in range(len(W) - 2 * n + 1):
        if norm[i:i + n] == norm[i + n:i + 2 * n] and all(norm[i:i + n]):
            print(f"  x{n}: «{' '.join(w['w'] for w in W[i:i+n])}» {W[i]['start']:.2f}–{W[i+2*n-1]['end']:.2f}")

r = subprocess.run(["ffmpeg", "-hide_banner", "-i", a.audio, "-af", f"silencedetect=noise={a.silence_db}dB:d=0.35", "-f", "null", "-"], capture_output=True, text=True)
print(f"\nSILENCIOS DE AUDIO ({a.silence_db} dB, > 0,35 s)")
for s, e in re.findall(r"silence_start: ([\d.]+).*?silence_end: ([\d.]+)", r.stderr, re.S):
    print(f"  {float(s):6.2f} → {float(e):6.2f} ({float(e) - float(s):.2f} s)")

if a.rms:
    t0, t1 = a.rms.split(":")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", t0, "-to", t1, "-i", a.audio, "-af",
                        "astats=metadata=1:reset=1:length=0.05,ametadata=print:key=lavfi.astats.Overall.RMS_level", "-f", "null", "-"], capture_output=True, text=True)
    vals = re.findall(r"pts_time:([\d.]+).*?RMS_level=(-?[\d.]+|-inf)", r.stderr, re.S)
    print(f"\nENERGÍA {t0}–{t1} s (dB cada 50 ms; por debajo de −50 es silencio)")
    print("  " + "  ".join(f"{float(t0) + float(t):.2f}:{v if v != '-inf' else '-99'}" for t, v in vals))

"""Montaje final · Reels con Motion (kit gratis de Viegas Estudio)
Zoom suave constante en cada plano + subtítulos + motion graphics encima + voz limpia a −14 LUFS → MP4 1080×1920.

  python montar.py --work trabajo --plan trabajo/plan.json --out "FINAL - mi reel.mp4" [--musica Música/tema.mp3]

plan.json (lo escribe Claude y lo aprueba la persona):
{
  "subtitulos": "trabajo/subtitulos.mov",
  "piezas": [ {"archivo": "graficos/titulo.mov", "t": 0.4}, {"archivo": "graficos/cta.mov", "t": 38.2} ],
  "zoom": [1.0, 1.08]
}
- El zoom va de 100 % a 108 % en cada plano (alternando: acerca / aleja) y se ancla a la altura de la cara, para no cortarla nunca.
- Las piezas se ponen encima en su segundo «t». Las de pantalla completa tapan TODO (nunca medio cuerpo).
- Voz: sin reductor de ruido, filtro de graves a 40 Hz, +5 dB de cuerpo a 200 Hz, compresión suave y máster a −14 LUFS (pico −1,5 dBTP).
Se ejecuta con prioridad baja para que el ordenador siga usable.
"""
import argparse, json, os, platform, re, subprocess
from comun import pick_encoder

if platform.system() == "Windows":
    import ctypes
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)  # por debajo de lo normal (los hijos lo heredan)
else:
    try: os.nice(10)
    except Exception: pass

ap = argparse.ArgumentParser()
ap.add_argument("--work", default="trabajo")
ap.add_argument("--plan", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--musica", default="", help="música opcional: suena 18 dB por debajo de la voz")
ap.add_argument("--fps", type=int, default=30)
a = ap.parse_args()
P = lambda f: os.path.join(a.work, f)
plan = json.load(open(a.plan, encoding="utf-8"))
words = json.load(open(P("words.json"), encoding="utf-8"))
SEG, DUR = words["segments"], words["duration"]
z0, z1 = plan.get("zoom", [1.0, 1.08])
run = lambda c: subprocess.run(c, capture_output=True, text=True, check=True)

# 1 · vídeo: cada plano con su zoom (supermuestreo ×2 para que el zoom sea liso, sin saltitos)
parts, labels, t = [], "", 0.0
for i, (s, e) in enumerate(SEG):
    d = e - s; n = max(1, round(d * a.fps))
    za, zb = (z0, z1) if i % 2 == 0 else (z1, z0 + (z1 - z0) * 0.35)
    z = f"{za}+({zb}-{za})*on/{n}"
    parts.append(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS,scale=2160:3840:flags=lanczos,"
                 f"zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih*0.36-ih/zoom*0.36':d=1:s=1080x1920:fps={a.fps},setsar=1[v{i}]")
    labels += f"[v{i}]"
parts.append(f"{labels}concat=n={len(SEG)}:v=1:a=0[base]")
ins = ["-i", P("vertical.mp4")]
cur, k = "[base]", 1
capas = ([{"archivo": plan["subtitulos"], "t": 0}] if plan.get("subtitulos") else []) + plan.get("piezas", [])
for c in capas:
    ins += ["-itsoffset", str(c["t"]), "-i", c["archivo"]]
    parts.append(f"{cur}[{k}:v]overlay=0:0:eof_action=pass:format=auto[o{k}]"); cur = f"[o{k}]"; k += 1
parts.append(f"{cur}format=yuv420p[vout]")

# 2 · audio: voz de los mismos tramos, limpia y con cuerpo
voz = "highpass=f=40,bass=g=5:f=200:w=0.7,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=140:makeup=2"
ains = ["-i", P("audio48k.wav")]; ai = k
ap_ = ""
for i, (s, e) in enumerate(SEG):
    parts.append(f"[{ai}:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={e - s - 0.012:.3f}:d=0.012[a{i}]"); ap_ += f"[a{i}]"
parts.append(f"{ap_}concat=n={len(SEG)}:v=0:a=1,{voz},aformat=channel_layouts=stereo[voz]")
if a.musica:
    ains += ["-stream_loop", "-1", "-i", a.musica]
    parts.append(f"[{ai + 1}:a]volume=-18dB,afade=t=out:st={max(0, DUR - 1.5)}:d=1.5,atrim=0:{DUR}[mus];[voz][mus]amix=inputs=2:duration=first:normalize=0[mez]")
    amap = "[mez]"
else:
    amap = "[voz]"
enc = pick_encoder()
venc = (["-c:v", "h264_nvenc", "-preset", "p5", "-rc", "vbr", "-cq", "20", "-b:v", "0"] if enc == "nvenc" else
        ["-c:v", "h264_videotoolbox", "-b:v", "16M"] if enc == "videotoolbox" else ["-c:v", "libx264", "-preset", "medium", "-crf", "19"])
tmp = P("_montaje.mkv")
print(f"montando {len(SEG)} planos · {len(capas)} capas · {DUR:.1f} s · codificador {enc} …")
run(["ffmpeg", "-v", "error", "-y", *ins, *ains, "-filter_complex", ";".join(parts), "-map", "[vout]", "-map", amap, "-t", str(DUR),
     *venc, "-r", str(a.fps), "-c:a", "pcm_s24le", "-ar", "48000", tmp])

# 3 · máster a −14 LUFS en dos pasadas
m = run(["ffmpeg", "-hide_banner", "-i", tmp, "-vn", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]).stderr
j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:"
      f"measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000")
run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-map", "0:v", "-map", "0:a", "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "256k",
     "-movflags", "+faststart", a.out])
os.remove(tmp)
r = run(["ffmpeg", "-hide_banner", "-i", a.out, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
lu, pk = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1], re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1]
print(f"✓ {a.out} · {lu} LUFS · pico {pk} dBTP")

"""Crea la carpeta de reels del usuario (una sola vez). No borra ni sobrescribe nada.

  python crear_carpeta.py --dest "C:/Users/yo/Documents/Reels con Claude"

Reels con Claude/
  Mi estilo/      Reglas-de-estilo.md (la crea Claude contigo), referencias/, tipografias/, logos/
  Tomas/          tus vídeos grabados, tal cual salen de la cámara o el móvil
  Música/         opcional: tu música (si no, Claude la genera con SynthFlow)
  Reels/          un proyecto por reel: lo crea Claude (trabajo/, graficos/ y el FINAL)
"""
import argparse, os
import comun  # consola UTF-8 en Windows

LEEME = {
    "Mi estilo": "Aquí vive tu estilo. Claude lo lee antes de editar cada reel.\n- Reglas-de-estilo.md: colores (HEX), tipografías, animaciones y normas. La crea Claude contigo.\n",
    "Mi estilo/referencias": "Capturas y vídeos de reels que te gustan. Claude los mira para crear tu guía de estilo.\n",
    "Mi estilo/tipografias": "Tus fuentes (.ttf u .otf). Si no pones ninguna, se usan Anton y Rajdhani, que vienen con la skill.\n",
    "Mi estilo/logos": "Tu logo y los logos que salen en tus vídeos (mejor en .svg o .png con fondo transparente).\n",
    "Tomas": "Deja aquí tus vídeos grabados. Nunca se modifican: Claude trabaja con una copia.\n",
    "Música": "Opcional. Si dejas aquí tu música, Claude puede usarla. Si no, la genera con SynthFlow.\n",
    "Reels": "Un proyecto por reel, lo crea Claude. Dentro está el vídeo FINAL y la portada.\nLa carpeta trabajo/ de cada proyecto ocupa bastante: puedes borrarla cuando el reel esté publicado.\n",
}

ap = argparse.ArgumentParser()
ap.add_argument("--dest", required=True)
a = ap.parse_args()
for sub, txt in LEEME.items():
    d = os.path.join(a.dest, *sub.split("/"))
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, "LEEME.txt")
    if not os.path.exists(f):
        open(f, "w", encoding="utf-8").write(txt)
print(f"carpeta lista → {a.dest}")
for sub in LEEME:
    print("  ", sub + "/")

---
name: video-editor-mix
description: "Edita un reel vertical 9:16 (Instagram, TikTok, Shorts) de principio a fin con HyperFrames y te deja abrir el editor local (HyperFrames Studio, en el navegador) para retocar a mano lo que quieras: elige la mejor toma de cada frase (el último intento), quita silencios y muletillas, recorta de 4K, saca al hablante del fondo para poner palabras detrás de su cabeza, aplica uno de tres looks con acento coral Claude #D97757, subtítulos grandes con la palabra clave en coral, motion graphics construidos en paralelo, música y SFX sutiles, y exporta en 1080p a −14 LUFS siguiendo las 10 normas Reels Pro. Úsala cuando pidan editar un reel o un short, quitar silencios, poner subtítulos o gráficos, abrir el editor para cambiar algo, o revisar un montaje. Triggers: /video-editor-mix, «edita este reel», «abre el editor», «cambia este texto», «ponme subtítulos»."
---

# /video-editor-mix

Reel acabado a partir de clips en bruto, **sin salir de este ordenador**: HyperFrames construye el vídeo con HTML
y lo renderiza, y **tú sí puedes abrir el editor** (Studio en `localhost`) para tocar lo que quieras antes del render.

Lee antes de construir: `references/normas-reels.md` (las 10 normas Reels Pro), `references/looks.md` (los tres
looks y sus valores exactos), `references/layout.md` (zona segura y fórmula de las palabras detrás de la cabeza),
`references/gotchas.md` (cada trampa que ya se pisó una vez). Lee `references/overlays.md` cuando el guion pida
un insert animado (una app en pantalla, el perfil de Instagram, un SKILL.md pasando).

Funciona en macOS, Linux y Windows. `setup.py` detecta la máquina al principio de cada ejecución y todos los
comandos salen de ese registro: nunca adivines rutas ni shells, mira "Esta máquina" tras el paso 0.

## Las 10 normas (no se rompen)

Están completas en `references/normas-reels.md`. En la práctica, dentro de este pipeline:

1. **Gancho en 2 s.** El EDL abre con la frase que dice de qué va; en los dos primeros segundos no se pone nada más
   que el gancho (ni lista, ni contador, ni rótulo).
2. **Cero silencios, cero repeticiones.** Última toma de cada frase, sin aire muerto entre secciones, y se comprueba
   re-transcribiendo el corte (paso 4), no a oído.
3. **Subtítulos grandes.** Nunca por debajo de 56 px a 1080 de ancho: el tamaño sale del look, no de la prisa.
4. **Una palabra clave por frase, en coral y sola en pantalla.** En el build es la clase `y` (coral), un grupo
   `GROUPS` por frase, nada más en ese instante.
5. **Entradas suaves, desenfoque gaussiano.** `filter:blur(22px)` → 0 en `.2s`; prohibido `boxblur`/`avgblur`.
6. **La cámara nunca está quieta.** Cada plano lleva su zoom (1.3-1.9 desde el 4K en dos planos seguidos del mismo
   ángulo, o push-in lento); cada corte, su punch.
7. **Una idea por pantalla.** Un gráfico por idea y disparado en la palabra que la dice. Si dos compiten, sobra uno.
8. **La cara es sagrada.** Zona segura y fórmula de `layout.md`: detrás de la cabeza se ve al menos ~70 % de cada
   letra. Si un elemento tiene que tapar, tapa la pantalla entera.
9. **Logos reales, tildes revisadas, coral intacto.** El acento es coral Claude `#D97757` y **no se cambia** salvo
   que el usuario lo pida de forma explícita (entonces `ACCENT=#RRGGBB` al construir). Los logos no se recolorean.
10. **−14 LUFS.** El archivo que se entrega sale normalizado (paso 8), con la música muy por debajo de la voz.

## Reglas de taller
- Nunca borres archivos del usuario: los originales se leen, jamás se modifican.
- Los cortes se demuestran desde el render final (`check_cuts.py`), no desde capturas del proyecto.
- SFX sutiles (`SFX_GAIN = 0.75` de los volúmenes base), nunca por encima de la voz.
- Crédito en pantalla (@usuario) siempre que salgan reels de otra persona. Números reales solo del perfil del
  usuario; lo demás (comentaristas, historial de chat) son marcadores genéricos, nunca una persona real.
- Una decision nueva de estilo se pregunta una vez; después se aplica sin volver a discutirla.

## Paso 0 · Preparación (solo la primera vez)

`SK` es la carpeta de este `SKILL.md`, con ruta completa (en Pi, normalmente `~/.pi/agent/skills/video-editor-mix`).

Mira `SK/config.json`. **Si existe**, cárgalo (nombre, Instagram, look por defecto, carpetas), ejecuta el setup
como en el punto 3 y sigue a "Esta máquina".

**Si no existe:**
1. "¡Bienvenido a /video-editor-mix! Esto se hace una vez, dos minutos."
2. Pregunta en un solo mensaje: nombre (va en el rótulo de tu Instagram), @usuario, look por defecto (**bold**
   —palabras cinéticas detrás de la cabeza—, **cool girl** —cálido, serif itálica, tus reels orbitándote— o
   **cool dude** —editorial oscuro—), carpeta de clips (por defecto `~/Downloads`) y carpeta de proyectos
   (por defecto `~/reel-edits`).
3. Ejecuta el setup con el Python que haya, en este orden, hasta que imprima líneas `STATUS`:
   `python3 "SK/scripts/setup.py"`, luego `python "SK/scripts/setup.py"`, luego `py -3 "SK/scripts/setup.py"`.
   Ninguno arranca: falta Python; da el arreglo del sistema y para (Windows `winget install --id Python.Python.3.12 -e`,
   Mac `brew install python`, Linux `sudo apt install python3 python3-venv`).
   - ffmpeg / node / venv en MISSING: la línea trae el arreglo exacto para **esta** máquina; dáselo y espera a READY.
   - En Windows, que el usuario pegue los comandos en su PowerShell (winget pide aceptar términos la primera vez)
     y cierre Pi del todo antes de reabrirlo, o los programas nuevos no aparecen.
   - El script descarga los 6 SFX. Si siguen en MISSING (sin internet) es opcional: el reel sale sin SFX.
4. Los reels y las cifras los da el usuario: deja sus clips en `assets/reels/` y dice sus números. No se scrapea nada.
5. Guarda `SK/config.json` (nunca secretos):
   ```json
   {"name": "...", "instagram": "usuario-sin-@", "defaultLook": "bold", "accent": "#D97757",
    "clipsDir": "~/Downloads", "projectsDir": "~/reel-edits", "setupComplete": true, "setupDate": "YYYY-MM-DD"}
   ```
   `accent` se queda en coral salvo que el usuario pida otro color.
6. "Listo. Arranco /video-editor-mix..." y sigue.

## Esta máquina (leer en cada ejecución)

Lee `SK/.platform.json`, que escribe `setup.py`:
- `PY` = el `python` del registro (`.venv/bin/python` en Mac y Linux, `.venv/Scripts/python.exe` en Windows). **Todo**
  script Python de esta skill se ejecuta con él, nunca con un `python3` a pelo.
- `HF` = `PY "SK/scripts/hf.py"`: arranca el HyperFrames fijado (`npx --yes hyperframes@0.8.34 ...`) con el Node
  correcto en cualquier sistema. Sin `nvm use`, sin líos de `npx.cmd`.
- `cutout`: `CoreML` (Apple Silicon) o `CPU` (Windows, Linux, Intel: el paso lento; avísalo y lánzalo en segundo plano).

`setup.py` reescribe el archivo en cada ejecución, así que siempre está al día. Si falta: no llegó a READY.

Un solo estilo de comando, válido en zsh, bash, Git Bash y PowerShell:
- Rutas completas entre comillas dobles y con barras normales: `"PY" "SK/scripts/ingest.py" "<proyecto>"`.
- En PowerShell, `&` delante: `& "PY" "SK/scripts/ingest.py" "<proyecto>"`.
- Un comando por llamada. Sin `&&`, sin `VAR=1 comando`, sin `~` dentro de argumentos, sin `source`.
- `ffmpeg` y `ffprobe` están en PATH en todos los sistemas; los comandos sueltos de ffmpeg son iguales en todos.

## Flujo

### 1 · Entrada
Los clips que nombre el usuario o, si no, los vídeos más nuevos de `clipsDir`. Crea `<projectsDir>/<slug-corto>/`.
Si manda enlaces de referencia (reels de IG, pins), descárgalos y mira fotogramas antes de diseñar nada (`overlays.md`).

### 2 · Ingesta
```bash
PY SK/scripts/ingest.py <proyecto> <clips o carpeta> [--newest 5]
```
Mira `work/sheets.jpg` (planos y ángulos) y lee `transcript.txt` (líneas por clip, palabras con tiempos, mapa de habla).

### 3 · Elegir tomas → `<proyecto>/edl.json`
- Reconstruye el guion: la gente repite una frase hasta que sale. Se queda **la última toma limpia y completa**
  (norma 2), salvo que el usuario diga otra cosa ("lo bueno empieza en 0:47" = una toma continua desde ahí).
- In/out desde el mapa de habla: empieza ~0.05-0.07 s antes de la primera palabra, corta donde empieza el silencio
  tras la última. Sin aire muerto entre secciones; confirma las pausas dudosas con `silencedetect` antes de recortar
  (Whisper inventa una palabra al principio de un corte).
- Dos segmentos seguidos del mismo ángulo: uno de ellos con punch (zoom 1.3-1.9 desde el 4K, `cx`/`cy` en el pecho).
- Palabras dudosas (clave, disparador del CTA): re-transcribe ese trozo con `medium.en` y un prompt con los nombres.
- Formato: `[{"id": "hook", "clip": "c1", "in": 12.66, "out": 15.72, "zoom": 1.0, "cx": 0.5, "cy": 0.5, "line": "..."}]`
- Pásale el EDL al usuario como tabla corta (línea, clip, look por sección) y sigue; no esperes.

### 4 · Montar, transcribir, recortar el fondo
```bash
PY SK/scripts/assemble.py <proyecto>            # aroll.mp4 limpio, 30 fps CFR + segments.json con frames exactos
PY SK/scripts/transcribe_cut.py <proyecto> "<nombres y palabras clave del guion>"
PY SK/scripts/cutout.py <proyecto>              # en segundo plano; comprueba que los frames del cutout == los del aroll
PY SK/scripts/headpos.py <proyecto>             # posición de cabeza/cuerpo por segmento
```
Un cutout a la vez (~1.5 GB de RAM); imprime progreso cada 30 s. **Comprueba los empalmes por lo que se oye**:
vuelve a pasar `transcribe_cut.py` sobre el `aroll.mp4` y compara con el texto esperado; si queda un resto de palabra
o falta una sílaba, mueve el borde del segmento en `edl.json` y repite.

### 5 · Inserts en paralelo (en cuanto el EDL esté cerrado)
Por cada insert animado del guion, lanza un subagente en segundo plano con la plantilla de `references/overlays.md`
(tamaño fijo, duración fija, beats clavados a las palabras, webm con transparencia). Tú sigues montando mientras trabajan.

### 6 · Construir
Copia `SK/assets/template/` dentro del proyecto (`build.py`, `hyperframes.json`, `package.json`, `assets/fonts`,
`assets/sfx`) y adapta `build.py`: es el build acabado de un reel real. Conserva la maquinaria, reescribe el contenido
(la docstring dice qué es cada cosa).
- Qué look dónde: `defaultLook` para todo el reel; una línea del guion que nombre un look cambia su sección.
- Órbita y rejilla de perfil usan los reels del usuario (`assets/reels/`).
- Acento: coral `#D97757`. Solo con `ACCENT=#RRGGBB` si lo piden de forma explícita.
- Itera desde la carpeta del proyecto: `HF lint` (0 errores), luego `PY build.py --safe`, luego
  `HF snapshot --at <10-20 momentos> --no-end --describe false`. Mira las hojas de contacto y corrige zona segura,
  legibilidad y jerarquía. Si copiaste un `build.py` viejo y no entiende `--safe`, usa `SAFE=1 "PY" build.py`.

### 7 · Revisión en el editor (Studio) — opcional, cuando el usuario quiere tocar a mano

Aquí el usuario **sí** abre un editor: HyperFrames Studio sirve el proyecto en el navegador con timeline, propiedades
y vista previa con hot-reload. Es para retoques finos (posición, tamaño, texto, tiempos), no para rehacer el guion.

```bash
HF preview --background --port 3002        # desde la carpeta del proyecto
HF preview --status --json                 # ¿sigue vivo?
HF preview --stop                          # al terminar la revisión
```
1. Comprueba que la URL que imprime responde 200 (`curl -s -o /dev/null -w '%{http_code}'`) y dale la URL completa,
   con su `#project/<nombre-del-proyecto>`. Sin ese fragmento, Studio abre sin proyecto.
2. **Mientras edita, no ejecutes `PY build.py`**: reescribe `index.html` y se lleva por delante sus cambios. Si hay
   que reconstruir, avisa, guarda antes una copia de `index.html` en `work/` y dile qué se va a perder.
3. Si dice "cambia esto", "hazlo más grande", "mueve lo que he seleccionado":
   `HF preview --context --json --context-fields selection` (o `--context-fields selection,lint`). Trae archivo,
   selector, caja y texto del elemento seleccionado. Si sale `no-selection`, pídele que pulse el elemento en Studio.
4. Al acabar, dos caminos; decide con el usuario (una vez):
   - **Se queda como lo dejó**: renderiza desde `index.html` tal cual (`HF render ...`, paso 8). Rápido, pero el
     siguiente `build.py` lo pierde.
   - **Que aguante reconstrucciones**: pasa sus retoques a `build.py` (la fuente de verdad) y reconstruye.
5. Cierra el preview (`HF preview --stop`) antes de renderizar la versión final, para no dejar servidores colgados.

### 8 · Render, volumen y QA
```bash
PY build.py                                 # sin --safe
HF render -o renders/<slug>-vN.mp4 --quality high
PY SK/scripts/check_cuts.py <proyecto> renders/<slug>-vN.mp4 --phone
```
- **Norma 10**: mide y normaliza la voz a −14 LUFS integrados:
  `ffmpeg -i in.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k out.mp4`, y vuelve a medir
  (`-af ebur128=peak=true`) para confirmar −14 ±1. La música, muy por debajo de la voz.
- Mira `work/cut_check.jpg`: cada fotograma después de un corte enseña el plano nuevo limpio. Revisa picos de audio
  (`volumedetect`, máximo sobre −2 a −5 dB) y el silencio en las juntas.
- Nada de fotogramas negros (`blackdetect`) y ninguna frase perdida (compara lo transcrito con lo que se oye).

### 9 · Entrega
Manda o señala la copia de móvil (720p) y el render bueno. Cuenta en lenguaje llano qué cambió y qué necesita
decisión del usuario. Guarda todas las versiones en `renders/`; antes de re-montar, copia `assets/` + `segments.json`
a `work/vN/`.

## Valores por defecto que ya salieron de feedback real (no se reabren)
- El look se construye con etalonaje y tipografía; no se sustituye el fondo por una habitación generada por IA.
- Sin grano de película. Oscuro vale, pero el sujeto iluminado y la piel sin irse a rojo.
- Los subtítulos de entrada centrados delante del hablante se leen mejor que las líneas pegadas al borde izquierdo.
- Las palabras detrás de la cabeza son la firma, pero solo cuando se leen.
- Coral `#D97757` es el acento por defecto en todo el reel (norma 9); cualquier otro color, solo si lo piden.

---
Basado en `/video-edit` de [@tenfoldmarc](https://instagram.com/tenfoldmarc) y en las normas de Viegas Estudio.

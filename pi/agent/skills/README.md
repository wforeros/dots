# Skills

Skills de Pi instaladas en `~/.pi/agent/skills/` (= `~/dots/pi/agent/skills/`).

Cada skill es un directorio con un `SKILL.md` (frontmatter `name` + `description`)
y, opcionalmente, `reference/` y `scripts/`.

## Instaladas

| Skill | Tipo | Versión | Fuente | Versionado aquí |
|---|---|---|---|---|
| [`impeccable`](https://impeccable.style) | terceros | 4.5.0 (CLI 0.1.11) | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) · Apache-2.0 | ❌ ignorada en git |
| `prepara-tu-ordenador-reels-editor-deps` | propia (port de Viegas Estudio) | 1.0.0 | `preparar-equipo.zip` (versión gratis) · sin licencia indicada | ✅ sí |
| `editar-reels-claude` | propia (port de Viegas Estudio) | 2.0.0 | `reels-motion-gratis.zip` (v2 gratis) · sin licencia indicada | ✅ sí |

### editar-reels-claude

Edita un reel vertical de cabeza parlante: corta silencios y tomas falsas, subtítulos
con palabra clave en coral, zoom suave, 8 motion graphics editables, música sintetizada
sin derechos y export 1080p a −14 LUFS. Todo con ffmpeg + Whisper + Chrome headless.

- Ruta local: `pi/agent/skills/editar-reels-claude/`
- Requiere `node_modules` propio (`npm install` en la carpeta) y Whisper en un Python
  aparte. `scripts/comprobar_equipo.py` dice qué falta; `--instalar` instala ambos
  (pide permiso antes).
- Portado de Claude Code a Pi: `{SKILL}/`→rutas relativas, `python`→`python3`,
  referencias al host→`Pi`, preguntas→chat.
- Parches propios sobre el original: rutas de Chrome para **Linux** (sistema y caché de
  Playwright) en `comprobar_equipo.py`, `subtitulos/motor/render.mjs` y
  `scripts/render_pieza.mjs`; y arreglo de rutas con espacios en `py -0p`.
- Ojo: pide `playwright@1.56.1`, mientras que `prepara-tu-ordenador-reels-editor-deps`
  sugiere `1.48.2`. Manda esta (1.56.1).


### prepara-tu-ordenador-reels-editor-deps

Comprueba el equipo (SO, GPU, RAM, disco) e instala lo que falte (winget/brew:
FFmpeg, Node LTS, Python 3.12, Git, Chrome/Edge, `faster-whisper`, Playwright)
preguntando permiso ítem por ítem. Termina con un informe ✓/✗ en Markdown.

- Ruta local: `pi/agent/skills/prepara-tu-ordenador-reels-editor-deps/`
- **Solo invocación explícita**: `disable-model-invocation: true` → no se autoselecciona
  por contexto; hay que lanzarla con `/skill:prepara-tu-ordenador-reels-editor-deps`.
  Instala software, así que no debe dispararse sola.
- `scripts/comprobar.py`: solo biblioteca estándar, solo lectura, no instala nada
  (`winget/node/ffmpeg/git/claude --version`, `nvidia-smi`, `sysctl`, `powershell -NoProfile`).
  Único fichero que escribe: el `--informe` que le pases.
- **Pendiente y conocido**: el único paso peligroso es `curl … Homebrew/install/HEAD/install.sh
  | bash` (código remoto sin fijar versión). Preferir el `.pkg` oficial.
- Portado de Claude Code a Pi: se cambiaron solo las referencias al host
  (`Claude Code`→`Pi`, `AskUserQuestion`→preguntar en el chat, `{SKILL}/`→rutas
  relativas). El script sigue detectando el CLI `claude`, es informativo.

### impeccable

Diseño/rediseño de interfaces frontend: crítica, auditoría, pulido, tipografía,
color, layout, motion, accesibilidad, responsive, sistemas de diseño.

- Ruta local: `pi/agent/skills/impeccable/` (~20M, casi todo el binario del launcher en `scripts/`)
- Depende de su propio launcher: `scripts/impeccable context`, `npx impeccable *`
- **No se versiona** porque es de terceros y voluminosa — ver `.gitignore`:
  `pi/agent/skills/impeccable/`
- Reinstalar/actualizar: seguir las instrucciones de <https://impeccable.style/docs/>
  (el `VERSION` del launcher vive en `scripts/VERSION`, la versión del skill en
  el frontmatter de `SKILL.md`)

## Añadir una skill propia

```text
pi/agent/skills/<nombre>/
├── SKILL.md          # frontmatter: name, description
├── reference/        # opcional: docs que la skill va leyendo
└── scripts/          # opcional: ejecutables
```

Después añádela a la tabla de arriba indicando `propia` en la columna *Tipo*
(las propias sí se versionan). Si es de terceros o pesa mucho, añádela al
`.gitignore` y documenta aquí cómo reinstalarla.

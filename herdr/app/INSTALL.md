# Instalar la configuración de Herdr app

Guía para un agente. Instala la configuración de **herdr-app** (la ventana GPUI)
que vive en este directorio. No aplica al TUI de Herdr (`../config.toml`) ni al
resto del repo.

La fuente de verdad es el repo en WSL, en `~/dots/herdr/app`. Asume que el repo
está clonado en `~/dots`. Si no, ajusta las rutas.

## 0. Requisitos

- Herdr app instalada. En WSL es la versión de Windows; en Unix, la de tu sistema.
- Herdr app debe haberse abierto al menos una vez en su máquina. Sin eso no
  existe su carpeta de configuración.

## 1. Detectar el entorno

```sh
if grep -qi microsoft /proc/version 2>/dev/null; then echo wsl
elif [ "$(uname)" = Darwin ] || [ "$(uname)" = Linux ]; then echo unix
else echo desconocido; fi
```

- `wsl`: sigue la sección 2. La app corre en Windows y lee
  `C:\Users\PC\.config\herdr-app`. **No crees un symlink en WSL**: no ayudaría.
- `unix` (macOS o Linux nativo): sigue la sección 3.
- `desconocido`: para y pregunta al usuario.

## 2. WSL: ejecutar el script de sincronización

Prerrequisitos:

- `jq` instalado en WSL (`command -v jq`).
- `/mnt/c` montado.
- La carpeta de Windows existe: `/mnt/c/Users/PC/.config/herdr-app`. El script
  la lee porque necesita `installed.json`, que Herdr crea al arrancar. Si no
  existe, para y pide al usuario que abra Herdr en Windows una vez.

Ejecuta:

```sh
cd ~/dots
bash bin/herdr-app-sync.sh
```

Qué hace el script:

- Copia de WSL a Windows solo lo que es del usuario: `settings.json`,
  `keys.json`, `layouts/*.json`, `mods/*/*` y `themes/*.json`.
- Se salta lo que instala Herdr (`main`, `terminals`, `win98`, `atom-one-dark`…),
  listado en `installed.json`.
- Es de un sentido: WSL pisa a Windows. Los cambios que se hayan hecho en la UI de
  Windows se pierden. Si quieres conservarlos, ejecuta antes
  `bin/herdr-app-sync.sh --pull` (no es parte de la instalación normal).

Variables opcionales: `HERDR_APP_DOTS` (por defecto `~/dots/herdr/app`) y
`HERDR_APP_WIN` (por defecto `/mnt/c/Users/PC/.config/herdr-app`).

Atajo: `setup.sh` de la raíz ejecuta el mismo script si la carpeta de Windows existe.

## 3. Unix (macOS / Linux nativo): symlink

En Unix solo hace falta un symlink de la carpeta de la app al repo:

```sh
TARGET="$HOME/.config/herdr-app"
SRC="$HOME/dots/herdr/app"

mkdir -p "$HOME/.config"
if [ -L "$TARGET" ]; then
  ln -sfn "$SRC" "$TARGET"            # ya era symlink: se reemplaza
elif [ -e "$TARGET" ]; then
  echo "Ya existe $TARGET y no es symlink. Muévela y reintenta:"
  echo "  mv \"$TARGET\" \"$TARGET.bak-$(date +%Y%m%d%H%M%S)\""
  exit 1
else
  ln -s "$SRC" "$TARGET"
fi
readlink "$TARGET"                     # debe imprimir $SRC
```

No borres una carpeta existente sin preguntar: puede tener estado de la app.

Al arrancar, la app escribe su estado en esa carpeta (ver sección 5).

## 4. Mods con repo propio

`herdr-gitdiff` (el panel Changes) no está en este repo. Vive en su propio repo y se
instala con su `install.sh`. Solo si el usuario lo quiere:

```sh
# Repo: ~/documents/herdr/mods/herdr-gitdiff
cd ~/documents/herdr/mods/herdr-gitdiff
# WSL:
HERDR_APP_HOME='C:\Users\PC\.config\herdr-app' \
HERDR_APP_BIN=/mnt/c/Users/PC/AppData/Local/Programs/herdr-app/herdr-app.exe \
./install.sh
# Unix: sin variables de WSL, según su README
./install.sh
```

Si no está instalado, el layout muestra el panel Changes vacío.

`git-graph` (el panel Graph) tampoco se versiona aquí. Viene de
<https://github.com/rabeeh-ta/herdr-git-graph> (MIT, © Rabeeh T A). Copia su
`mods/git-graph/` a la carpeta de mods de la app:

```sh
git clone https://github.com/rabeeh-ta/herdr-git-graph /tmp/herdr-git-graph
# WSL: /mnt/c/Users/PC/.config/herdr-app/mods/   Unix: ~/.config/herdr-app/mods/ (en symlink, esto es el repo)
cp -R /tmp/herdr-git-graph/mods/git-graph <carpeta de mods de la app>/
```

Si el usuario quiere el layout sin Graph, quita el bloque `graph` de `panel-body` en
`layouts/main-tabs.json` y el botón Graph de `tabs-graph`. Con el layout actual,
sin este mod el panel Graph sale vacío.

`herdr-t3` (layout) tampoco se versiona aquí. Se instala desde su repo con su
`scripts/update.sh`. Es opcional.

## 5. Verificar

```sh
herdr-app status          # debe decir sin errores (errors: [])
herdr-app check <mod>     # por cada mod que toques, debe decir "check passed"
ls ~/.config/herdr-app/layouts/*.error 2>/dev/null   # en Unix; en WSL mira en /mnt/c/Users/PC/.config/herdr-app/layouts/
```

Si hay un `*.error`, la app conservó la versión anterior del archivo. Lee el error,
corrígelo y vuelve a instalar.

Abre el panel Graph/Changes y arrástrale el borde. Debe poder crecer sin tope
(el layout ya no tiene `max`).

## Problemas conocidos

- **`git-graph` no está versionado aquí a propósito.** Es de un repo ajeno (sección 4).
  `.gitignore` tiene `herdr/app/mods/git*/`, así que tampoco aparece en `git status`.
  Un clon nuevo sin pasos de la sección 4 tiene el botón Graph pero el panel vacío.
- **Unix: la app escribe estado dentro del repo.** Con el symlink, `shared.json`,
  `installed.json`, `seen.json`, `window.json`, `windows.json`, `view.json`,
  `telemetry/`, `frame/`, `update-notes*`, `herdr-app.sock` y `data/` aparecen en
  `git status`. No los añadas al commit. `data/` ya está en `.gitignore`; el resto
  no. Si molesta, añádelos a `.gitignore`.
- **WSL no tiene symlink.** Si alguien crea uno en `~/.config/herdr-app` en WSL, no
  afecta a la app de Windows.

## No toques

- `AGENTS.md`: lo escribe la app en cada arranque. Tus ediciones se pierden.
- `installed.json`, `view.json`, `window.json`, `telemetry/`: estado de la app.

# Herdr app (Windows GUI)

Configuración de **herdr-app** (la ventana GPUI en Windows), mantenida aquí como
fuente de verdad. El TUI es otra cosa: está en `../config.toml` y `../workspace-tabs/`.

## Desplegar

```sh
bin/herdr-app-sync.sh          # repo -> C:\Users\PC\.config\herdr-app
bin/herdr-app-sync.sh --pull   # app -> repo (si cambias algo en la UI de Settings)
```

Solo copia lo que es tuyo: `settings.json`, `keys.json`, `layouts/*.json`,
`mods/*/*` y `themes/*.json`. Los mods, layouts y temas que instala Herdr
(`win98`, `atom-one-dark`, `main`, `terminals`…) se saltan siempre, igual que
`jsconfig.json`, `*.d.ts` y `*.error` que la app genera en las carpetas de mods.

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| `layouts/main-tabs.json` | clon de `main` con un bloque de 1px para el mod `space-tabs`. El layout activo. |
| `mods/space-tabs/` | Da a cada space nuevo las pestañas **Agents / Code / Commands** (no hay evento `space.created`: mira `spaces()` y guarda los ids en `shared.json`). |
| `mods/tmux-prefix/` | Copia de `herdrdev/herdr-layout-examples/tmux-prefix` (herdr.dev/mods), adaptada: prefijo **`ctrl+a`**, splits `v` / `-`, `N` nuevo space (hereda máquina y carpeta del actual), `w`/`s` picker, `b` sidebar, `,`/`$` renombrar, `X`/`D` cerrar pestaña/space, `o`/`g` worktrees, `G` panel Changes, `H` hunk diff. |
| `themes/catppuccin.json` | Catppuccin Mocha (la app no lo trae; sus temas son graphite/ink/moss/paper/atom-one-dark/win98). |
| `settings.json` | `theme: catppuccin`, zoom 1.3, dark, sonidos. |
| `keys.json` | Mapa `alt+letra` (= `prefix+letra` del TUI) y `ctrl+shift+…`. |

Notas: `keys.json` abre el prefijo con `ctrl+a`; `ctrl+a ctrl+a` manda un `^A`
literal al terminal. La ruta de hunk va absoluta porque el core en
`wsl` arranca con un PATH mínimo sin linuxbrew.

Los cambios se aplican en vivo; `herdr-app status` y `herdr-app check <mod>`
dicen si algo quedó mal (`errors: []` / `check passed`).

## Mods con repo propio

No todos los mods viven aquí. Un mod que se publica por su cuenta tiene su
propio repo y su propio `install.sh`, y `herdr-app-sync.sh` no lo toca.

### `gitdiff` (panel Changes)

- Repo: `~/documents/herdr/mods/herdr-gitdiff` (remoto `git@github.com:wforeros/herdr-gitdiff.git`).
- Qué hace: lista de archivos cambiados, cada uno se despliega con sus hunks, números de línea, `+`/`−` y resaltado de sintaxis. Solo lectura.
- Instalación (desde WSL, apuntando a la app de Windows):

  ```sh
  cd ~/documents/herdr/mods/herdr-gitdiff
  HERDR_APP_HOME='C:\Users\PC\.config\herdr-app' HERDR_APP_BIN=/mnt/c/Users/PC/AppData/Local/Programs/herdr-app/herdr-app.exe ./install.sh
  ```

- El layout `layouts/main-tabs.json` ya lo usa en el bloque `changes` (`"mod": "gitdiff"`).
  Si el mod no está instalado, el panel Changes sale vacío. Instálalo antes de
  sincronizar el layout en otra máquina.
- Para quitarlo: `./install.sh --uninstall` (con las mismas variables) y volver a
  `"mod": "changes"` en el layout si quieres el panel de serie.

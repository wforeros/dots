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
| `mods/tmux-prefix/` | Copia de `herdrdev/herdr-layout-examples/tmux-prefix` (herdr.dev/mods), adaptada: prefijo **`ctrl+a`**, splits `v` / `-`, `N` nuevo space (hereda máquina y carpeta del actual), `w`/`s` picker, `b` sidebar, `,`/`$` renombrar, `X`/`D` cerrar pestaña/space, `o`/`g` worktrees, `G` lazygit, `H` hunk diff. |
| `themes/catppuccin.json` | Catppuccin Mocha (la app no lo trae; sus temas son graphite/ink/moss/paper/atom-one-dark/win98). |
| `settings.json` | `theme: catppuccin`, zoom 1.3, dark, sonidos. |
| `keys.json` | Mapa `alt+letra` (= `prefix+letra` del TUI) y `ctrl+shift+…`. |

Notas: `keys.json` abre el prefijo con `ctrl+a`; `ctrl+a ctrl+a` manda un `^A`
literal al terminal. Las rutas de lazygit/hunk van absolutas porque el core en
`wsl` arranca con un PATH mínimo sin linuxbrew.

Los cambios se aplican en vivo; `herdr-app status` y `herdr-app check <mod>`
dicen si algo quedó mal (`errors: []` / `check passed`).

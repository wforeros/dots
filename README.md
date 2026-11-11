# Archivos de Configuración

Este repositorio contiene mis archivos de configuración (dot files) para varias herramientas y aplicaciones que utilizo en mi entorno de desarrollo. Aquí encontrarás configuraciones para `tmux`, `neovim (nvim)`, y varios scripts útiles.

## Contenido

- [tmux](#tmux)
- [neovim (nvim)](#neovim-nvim)
- [Instalación de Herdr con un agente](#instalación-de-herdr-con-un-agente)
- [Herdr (app de Windows)](#herdr)
- [Scripts](#scripts)
- [Zsh](#zsh)
- [i3wm](https://i3wm.org/) (Para el gestor de ventanas) / [GlazeWM](https://github.com/glzr-io/glazewm) (Gestor de ventanas para Windows)
- [compton](https://github.com/chjj/compton) (Para trasparencia)
- [feh](https://feh.finalrewind.org/) (Para poner fondos)

## Instalación de Herdr con un agente

Las instrucciones de instalación de la app de Herdr están en [`herdr/app/INSTALL.md`](./herdr/app/INSTALL.md). Es la forma más fácil: dile a tu agente que lo lea y ejecute sus pasos, por ejemplo:

> Lee `herdr/app/INSTALL.md` y ejecuta las instrucciones para instalar mi configuración de Herdr.

El documento detecta si estás en WSL o en Unix y sigue el camino correcto.

## tmux

La configuración de `tmux` incluye:

- Atajos de teclado personalizados
- Configuración de la barra de estado
- Plugins para mejorar la funcionalidad

## neovim (nvim)

La configuración de `neovim` incluye:

- Plugins gestionados con `vim-plug`
- Atajos de teclado personalizados
- Configuración de LSP (Language Server Protocol)
- Temas y colores personalizados

Para más detalles, revisa el directorio [`nvim`](./nvim).

## Herdr

La configuración de la app de Herdr (Windows) y sus mods vive en [`herdr/app`](./herdr/app/README.md). Ahí está explicado cómo se sincroniza con Windows, qué hace cada mod y cómo instalar los que viven en repos propios (como `gitdiff`).

## Scripts

Actualmente, los scripts disponibles son:

- `bin/tmux-sessionizer`: Abre explorador de fzf para seleccionar una carpeta y crear una nueva sesión de `tmux` desde esa carpeta.

## Zsh

La configuración de `zsh` funciona con ohmyzsh e incluye:

- Atajos de teclado personalizados
- Plugins para mejorar la funcionalidad

## Otros

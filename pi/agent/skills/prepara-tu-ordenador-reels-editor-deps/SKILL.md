---
name: prepara-tu-ordenador-reels-editor-deps
disable-model-invocation: true
description: Deja listo el ordenador (Windows o Mac) para editar vídeo y crear contenido con Pi. Comprueba sistema, tarjeta gráfica, RAM y disco; mira qué falta (FFmpeg, Python 3.11+, Node.js LTS, Git, Chrome/Edge, Playwright y Whisper) y lo instala con winget o Homebrew, pidiendo permiso antes de cada instalación; termina con un informe ✓/✗. Úsala cuando se pida «prepara mi ordenador», «instala lo que hace falta», «comprueba mi equipo» o algo falle porque falta un programa (ffmpeg, python, node, whisper…). Versión gratis de Viegas Estudio.
---

# Prepara tu ordenador · versión gratis (Viegas Estudio)

Quien te habla puede no haber usado nunca una terminal. **Habla claro, en español, sin jerga**, con una frase antes de cada paso. Nunca le pidas que escriba comandos: los ejecutas tú.

Las rutas de abajo son relativas a la carpeta de este `SKILL.md`. El script `scripts/comprobar.py` solo usa la biblioteca estándar de Python y **no instala nada**.

## Reglas
- **Primero se comprueba, luego se instala.** Nunca instales algo que ya está.
- **Permiso antes de cada instalación**, una por una, preguntándolo en el chat: qué es, para qué sirve en una frase, cuánto ocupa más o menos y el comando. Opciones: «Sí, instálalo (recomendado)» · «Ahora no».
- Nunca escribas contraseñas por la persona. Si sale el aviso de Windows (UAC) o el Mac pide la contraseña, dile que lo acepte ella.
- No cambies la configuración del sistema ni desinstales nada.
- Si un instalador falla, mira «Si algo falla» al final del informe, explica la causa en sencillo y propón la solución.

## Paso 0 · ¿Hay Python?
Prueba `python --version`, `python3 --version` y, en Windows, `py -0p`. Si no hay ninguno (o solo el acceso falso de Microsoft Store), pide permiso e instala Python primero:
- Windows: `winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements`
- Mac: si no hay `brew`, pide permiso para instalar Homebrew (pedirá la contraseña del Mac):
  `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` y luego `brew install python@3.12`.

## Paso 1 · Comprobar (no instala nada)
```bash
python scripts/comprobar.py           # legible, para enseñarlo
python scripts/comprobar.py --json    # para que lo leas tú
```
Resume en 4-6 líneas: sistema, tarjeta gráfica, RAM, disco, si **llega al mínimo** (tabla de abajo) y qué falta.

## Paso 2 · Instalar lo que falte (con permiso, en este orden)
Usa el campo `instalar` de cada elemento del JSON. Orden: gestor (winget/brew) → FFmpeg → Node.js LTS → Python → Git → Chrome/Edge → Whisper → Playwright.
- En Windows añade a winget `--accept-package-agreements --accept-source-agreements` (es aceptar las licencias de esos programas: dilo en la pregunta).
- **Whisper**: instala `faster-whisper` en el Python recomendado (`resumen.python_recomendado`). Si ya hay `whisper` o `faster-whisper` en algún Python, no instales otro. Si hay varios Python y el que abre `python` no es el que tiene Whisper, díselo y apunta la ruta del bueno en el informe.
- Tras instalar FFmpeg, Node o Python puede que no se vean hasta abrir una sesión nueva de Pi: compruébalo con la ruta completa o pide reiniciar Pi al final.

## Paso 3 · Informe final
```bash
python scripts/comprobar.py --informe "<carpeta Documentos del usuario>/informe-equipo.md"
```
Lo marcado con «·» es opcional y no impide dar el equipo por listo (ofrece instalarlo igualmente, con permiso). Si todo lo obligatorio está en ✓, termina con **«✅ Tu equipo ya está listo»**, la tarjeta gráfica detectada, la calidad recomendada (4K o 1080p) y el siguiente paso: «Ya puedes instalar las skills gratis de Viegas Estudio, por ejemplo la de editar reels con motion graphics». Si queda algo en ✗, lista qué falta y por qué, en una línea cada uno.

## El ordenador
| | Mínimo (funciona) | Recomendado (va fluido) |
|---|---|---|
| Sistema | Windows 10 (22H2) o macOS 13 | Windows 11 o macOS 14 o más nuevo |
| RAM | 8 GB | 16 GB o más |
| Tarjeta gráfica | ninguna especial (irá lento) | NVIDIA RTX con 8 GB o más, o Mac con chip M |
| Disco libre | 20 GB | 100 GB en SSD |

## Si pregunta cómo configurar Pi
- Modelo potente con esfuerzo medio; para tareas sencillas, esfuerzo bajo o un modelo más rápido.
- Deja los permisos en modo normal (Pi pregunta antes de ejecutar). Para comandos que se repiten mucho (ffmpeg, python) puede permitirlos siempre.
- Abre siempre Pi en su carpeta de trabajo y pulsa **Confiar** solo en carpetas suyas.

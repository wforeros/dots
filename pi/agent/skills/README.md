# Skills

Skills de Pi instaladas en `~/.pi/agent/skills/` (= `~/dots/pi/agent/skills/`).

Cada skill es un directorio con un `SKILL.md` (frontmatter `name` + `description`)
y, opcionalmente, `reference/` y `scripts/`.

## Instaladas

| Skill | Tipo | Versión | Fuente | Versionado aquí |
|---|---|---|---|---|
| [`impeccable`](https://impeccable.style) | terceros | 4.5.0 (CLI 0.1.11) | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) · Apache-2.0 | ❌ ignorada en git |

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

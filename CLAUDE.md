# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Blender 5.1+ addon for the Sequence Editor. Adds video/audio editing tools accessible via a panel in the `N` sidebar (tab "ChepeCarlos").

## Common Commands

```bash
# Verify registration without opening Blender UI
make blenderaddon-bg

# Check Blender version
make blenderaddon-check

# Package as installable zip
make zip

# Install directly to Blender's addons directory
make install-local

# Launch Blender with the addon loaded (dev mode, no factory startup)
make blenderaddon-dev
```

The `BLENDER` variable in the Makefile points to a local Blender binary; override it if the path differs.

## Architecture

**Entry point:** `__init__.py` — imports all operators from `operaciones/`, registers them plus the panel via `bpy.utils.register_class`, and installs keyboard shortcuts via `operaciones/macros.py`.

**UI:** `mipanel.py` — single `bpy.types.Panel` subclass (`bl_idname = "MY_PT_panel"`) that draws all buttons. Each button calls an operator by its `bl_idname`.

**Operators** (`operaciones/`): Each file defines one `bpy.types.Operator` subclass registered under the `scene.` namespace. The pattern is consistent: `poll()` guards availability, `execute()` does the work, `return {"FINISHED"}`.

| File | Operator bl_idname | Purpose |
|---|---|---|
| `superInsertar.py` | `scene.superinsertar` | Insert clip at cursor position |
| `subtitulos.py` | `scene.subtitulo` | Insert subtitle strips from `out.json` |
| `sobreponeraudio.py` | `scene.sobreponeraudio` | Overlay audio on selected clips |
| `alinear.py` | `scene.superaliniar` | Align selected clips |
| `zoon.py` | `scene.superzoon` | Scale selected clips |
| `mover.py` | `scene.moverclip` | Move clips in timeline |
| `indice.py` | `scene.superindice` | Convert timeline markers to text strips |
| `exportar.py` | `scene.exportarindice` | Export marker index |
| `exportarextras.py` | `scene.exportarextra` | Export markers by prefix (link/tarjeta/video/ads/etc.) |
| `autoanotar.py` | `scene.autoanotar` | Auto-annotate clips |
| `superAnimar.py` | `scene.superanimar` | Apply preset animations to clips |
| `palabraPorMinuto.py` | `scene.ppm` | Calculate words per minute |
| `hueva.py` | `scene.hueva` | Copy current cursor time to clipboard |
| `macros.py` | — | Keyboard shortcut registration |

**Shared utilities:**
- `operaciones/FuncionesArchivos.py` — all JSON config file I/O. Config root is `~/.config/pluginBlenderChepeCarlos/`. Use `ObtenerArchivo(relative_path)`, `ObtenerValor(file, key)`, `SalvarValor(file, key, value)`.
- `operaciones/funcionesExtras.py` — helpers like `asignarDinámica` (set property by name at runtime) and `cargarFuente` (load font for `blf`).
- `operaciones/extras.py` — UI helpers like `mostrarMensajeBox`.

## Config Files

All runtime config lives in `~/.config/pluginBlenderChepeCarlos/data/`:

- `insertar.json` — clip insertion defaults (path, volume, scale, opacity, angle, etc.)
- `blender_subtitulo.json` — subtitle strip style properties
- `blender_subtitulo_resaltado.json` — highlighted word strip style
- `blender_subtitulo_extra.json` — subtitle extra settings (`fuente`, `espera`, `palabras_linea`)
- `blender.json` — general plugin config

Per-project overrides: place `blender_subtitulo.json`, `blender_subtitulo_resaltado.json`, or `blender_subtitulo_extra.json` next to the `.blend` file — they are merged on top of the global config at runtime.

## Subtitles Data Format

The subtitles operator (`scene.subtitulo`) looks for a file relative to the `.blend` file:

```
subtitulo_{blend_filename}/out.json
```

The JSON must have a `segments` key, where each segment has a `words` list with `word`, `start`, and `end` (seconds as floats).

## Keyboard Shortcuts (defined in `macros.py`)

All shortcuts are in the `SEQUENCE_EDITOR` context:

| Shortcut | Operator |
|---|---|
| `Ctrl+Shift+Y` | superinsertar |
| `Ctrl+Shift+Q` | superanimar |
| `Ctrl+Shift+O` | sobreponeraudio |
| `Ctrl+R` | superaliniar |
| `Ctrl+P` | superzoon (set) |
| `Ctrl+U` | superzoon (increment) |
| `Ctrl+J` | moverclip |
| `Ctrl+Shift+U` | hueva |

## Blender API Compatibility

The code targets Blender 5.1+. The Sequence Editor API changed between versions — `sequences` vs `strips` and `sequences_all` vs `strips_all` are checked with `hasattr` guards in several operators for backwards compatibility.

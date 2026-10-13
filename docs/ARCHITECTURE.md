# ai-storyboard-generator — Architecture

A modular Windows desktop toolkit that turns a script or logline into a
shot-by-shot storyboard: panel layout, camera notes, dialogue, timing, and
optional AI-generated concept frames.

## Package map

```
storyboard/
  cli/            # typer entrypoints (storyboard, sbgen)
  desktop/        # PySide6 launcher + main window
  core/           # pipeline orchestration, project model
  features/       # feature modules (board, shotlist, frames, export)
  handlers/       # per-feature request handlers, dispatched by core
  services/       # external services: image backends, LLM planners
  models/         # pydantic schemas + local model registry
  config/         # loader, defaults, schema
  utils/          # logging, io, timing, text
  native/         # pybind11 C++ helpers (frame tiling, perceptual hash)
```

## Pipeline

`ScriptParser -> SceneSplitter -> ShotPlanner -> FrameComposer -> Exporter`

Each stage is a handler registered in `storyboard/handlers/registry.py`.
The core `BoardPipeline` walks the registry in order, passing a
`BoardContext` dataclass. Handlers may emit progress events on the
`PipelineBus` (Qt signal on desktop, rich progress on CLI).

## Feature modules

Feature modules under `storyboard/features/` are self-contained: each
declares a `FEATURE` manifest, registers its handlers, and may ship its
own config section. Removing a feature folder must not break the core.

## Image backends

`storyboard/services/image_backends/` speaks a narrow protocol:

```python
class ImageBackend(Protocol):
    async def render(self, prompt: str, *, width: int, height: int,
                     seed: int | None = None) -> bytes: ...
```

Local (diffusers) and remote (HTTP) backends both implement it. The
composer picks a backend per project from `config/local.toml`.
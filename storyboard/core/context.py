"""Shared state passed through the pipeline. One instance per run."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from storyboard.models.schemas import Board, Script


@dataclass(slots=True)
class BoardContext:
    """Mutable run state. Handlers read upstream fields and write their own."""

    project_dir: Path
    config: dict
    script: Script | None = None
    board: Board | None = None
    frame_paths: dict[str, Path] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    cancelled: bool = False

    def warn(self, message: str) -> None:
        self.warnings.append(message)
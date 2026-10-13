"""BoardPipeline — walks registered handlers in order, emits progress events."""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Callable

from storyboard.core.context import BoardContext
from storyboard.handlers.registry import HandlerRegistry, StageHandler

log = logging.getLogger(__name__)


@dataclass(slots=True)
class StageResult:
    name: str
    seconds: float
    ok: bool
    error: str | None = None


@dataclass(slots=True)
class PipelineReport:
    stages: list[StageResult] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(s.ok for s in self.stages)


ProgressFn = Callable[[str, int, int], None]


class BoardPipeline:
    """Runs handlers in registration order.

    Handlers are expected to be idempotent per stage and to raise
    `StoryboardError` on failure. A failing handler aborts the run unless
    it is registered as optional.
    """

    def __init__(self, registry: HandlerRegistry, on_progress: ProgressFn | None = None) -> None:
        self._registry = registry
        self._on_progress = on_progress

    def run(self, ctx: BoardContext) -> PipelineReport:
        report = PipelineReport()
        handlers = self._registry.ordered()
        total = len(handlers)
        for index, handler in enumerate(handlers, start=1):
            if ctx.cancelled:
                log.warning("pipeline cancelled before stage %s", handler.stage)
                break
            if self._on_progress:
                self._on_progress(handler.stage, index, total)
            started = time.perf_counter()
            try:
                handler.run(ctx)
                elapsed = time.perf_counter() - started
                report.stages.append(StageResult(handler.stage, elapsed, ok=True))
            except Exception as exc:  # noqa: BLE001 - handler boundary
                elapsed = time.perf_counter() - started
                if handler.optional:
                    log.exception("optional stage %s failed", handler.stage)
                    ctx.warn(f"{handler.stage} skipped: {exc}")
                    report.stages.append(StageResult(handler.stage, elapsed, ok=True, error=str(exc)))
                    continue
                report.stages.append(StageResult(handler.stage, elapsed, ok=False, error=str(exc)))
                raise
        return report
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
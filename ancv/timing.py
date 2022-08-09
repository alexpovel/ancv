from dataclasses import dataclass, field
from datetime import timedelta
from time import perf_counter
from typing import Optional


@dataclass
class Stopwatch:
    """A simple stopwatch for timing execution.

    Call it with a segment name, and it will start timing that segment, stopping when it
    is called again with the next segment or explicitly with `stop()`.

    The results are available in the `timings` attribute.
    """

    timings: dict[str, timedelta] = field(default_factory=dict)
    _start: Optional[float] = field(repr=False, default=None)
    _current_segment: Optional[str] = field(repr=False, default=None)
    _finished: bool = field(repr=False, default=False)

    def __getitem__(self, key: str) -> timedelta:
        return self.timings[key]

    def __call__(self, segment: str) -> None:
        stop = perf_counter()

        if segment in self.timings or segment == self._current_segment:
            raise ValueError(f"Segment '{segment}' already exists.")

        if self._current_segment is not None and self._start is not None:
            self.timings[self._current_segment] = timedelta(seconds=stop - self._start)

        if self._finished:
            self._start = None
            self._current_segment = None
            self._finished = False
        else:
            self._start = perf_counter()
            self._current_segment = segment

    def stop(self) -> None:
        """Stops the current segment and adds it to the timings.

        Calling the stopwatch again with a new segment will restart it.
        """
        self._finished = True
        self(segment="__final_segment__")

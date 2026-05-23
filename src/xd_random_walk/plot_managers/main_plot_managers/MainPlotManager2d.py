from .BasePlotManager import BaseMainPlotManager
from typing import Literal
from matplotlib.collections import LineCollection
import numpy as np


class MainPlotManager2d(BaseMainPlotManager):
    def __init__(
        self,
        num_samples: int = 1,
        generator_type: Literal["discrete", "uniform", "normal"] = "discrete",
        show_taken_path: bool = False,
        tail_length: int = 5000,
    ) -> None:
        super().__init__(dims=2, num_samples=num_samples, generator_type=generator_type)

        self._axes = self._fig.add_subplot(111)
        self._axes.grid(True, "both", alpha=0.5)
        self._axes.axhline(y=0, color="black", linewidth=1.5, zorder=2)
        self._axes.axvline(x=0, color="black", linewidth=1.5, zorder=2)

        if show_taken_path:
            self._history = np.zeros(
                (num_samples, tail_length, 2), dtype=self._data_type
            )
            self._history_idx = 0
            self._history_filled = False
            self._tail_length = tail_length
            self._lines = LineCollection([], colors=self._colors, alpha=0.5)
            self._axes.add_collection(self._lines)
        else:
            self._tail_length = None
            self._history = None
            self._lines = None

        self._scatter = self._axes.scatter(
            self._points[:, 0], self._points[:, 1], c=self._colors, zorder=3, s=18
        )
        self._plot = self._axes.plot()

    def _update_plot(self) -> tuple:
        self._scatter.set_offsets(self._points)

        if self._history is not None:
            self._history[:, self._history_idx, :] = self._points
            self._history_idx += 1

            if self._history_idx >= self._tail_length:  # type: ignore
                self._history_idx = 0
                self._history_filled = True

            if self._history_filled:
                segments = np.roll(self._history, -self._history_idx, axis=1)
            else:
                segments = self._history[:, : self._history_idx, :]
            self._lines.set_segments(segments)

        self._axes.set_xlim(self._ranges[0, 0], self._ranges[0, 1])
        self._axes.set_ylim(self._ranges[1, 0], self._ranges[1, 1])

        artists = [self._scatter]
        if self._history is not None:
            artists.append(self._lines)

        return (
            (self._scatter, self._lines)
            if self._history is not None
            else self._scatter,
        )

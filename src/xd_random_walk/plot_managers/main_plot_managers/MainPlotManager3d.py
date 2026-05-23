from typing import Literal
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.artist import Artist

from .BasePlotManager import BaseMainPlotManager


class MainPlotManager3d(BaseMainPlotManager):
    """Manages the 3-dimensional scatter plot and Line3DCollection traces."""

    def __init__(
        self,
        num_samples: int = 500,
        generator_type: Literal["discrete", "uniform", "normal"] = "discrete",
        show_taken_path: bool = False,
        tail_length: int = 100,
    ) -> None:
        super().__init__(dims=3, num_samples=num_samples, generator_type=generator_type)

        self._axes = self._fig.add_subplot(111, projection="3d")
        self._axes.grid(True, alpha=0.5)

        if show_taken_path:
            self._tail_length = tail_length
            self._history = np.zeros(
                (num_samples, tail_length, 3), dtype=self._data_type
            )
            self._history_idx = 0
            self._history_filled = False

            self._lines = Line3DCollection(
                [np.zeros((2, 3))], colors=self._colors, alpha=0.5
            )
            self._axes.add_collection3d(self._lines)
        else:
            self._tail_length = None
            self._history = None
            self._lines = None

        self._scatter = self._axes.scatter(
            self._points[:, 0],
            self._points[:, 1],
            self._points[:, 2],
            c=self._colors,
            s=18,
            depthshade=True,
        )

    def _update_plot(self) -> tuple[Artist, ...]:
        self._scatter._offsets3d = (
            self._points[:, 0],
            self._points[:, 1],
            self._points[:, 2],
        )

        artists: list[Artist] = [self._scatter]

        if self._history is not None and self._lines is not None:
            self._history[:, self._history_idx, :] = self._points
            self._history_idx += 1

            if self._history_idx >= self._tail_length:
                self._history_idx = 0
                self._history_filled = True

            # Guard against 1-point rendering crashes in mplot3d
            if self._history_idx > 1 or self._history_filled:
                if self._history_filled:
                    segments = np.roll(self._history, -self._history_idx, axis=1)
                else:
                    segments = self._history[:, : self._history_idx, :]

                # mplot3d strictly requires a Python list of arrays, not raw 3D numpy arrays
                self._lines.set_segments(list(segments))

            artists.append(self._lines)

        self._axes.set_xlim3d(self._ranges[0, 0], self._ranges[0, 1])
        self._axes.set_ylim3d(self._ranges[1, 0], self._ranges[1, 1])
        self._axes.set_zlim3d(self._ranges[2, 0], self._ranges[2, 1])

        return tuple(artists)

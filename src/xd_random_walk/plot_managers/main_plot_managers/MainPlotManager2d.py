from .BasePlotManager import BaseMainPlotManager
from typing import Literal
from collections import deque
from matplotlib.collections import PathCollection


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
            self._tail_length = tail_length
            self._history = [deque(maxlen=tail_length) for _ in range(num_samples)]
            self._lines = [
                self._axes.plot([], [], color=self._colors[i], alpha=0.5)[0]
                for i in range(num_samples)
            ]
        else:
            self._tail_length = None
            self._history = None
            self._lines = None

        self._scatter = self._axes.scatter(
            self._points[:, 0], self._points[:, 1], c=self._colors, zorder=3, s=18
        )
        self._plot = self._axes.plot()

    def _update_plot(self) -> tuple[PathCollection]:
        self._scatter.set_offsets(self._points)

        if self._history is not None:
            for i in range(len(self._points)):
                self._history[i].append(self._points[i].copy())

                if len(self._history[i]) > 0 and self._lines is not None:
                    x_data, y_data = zip(*self._history[i])
                    self._lines[i].set_data(x_data, y_data)

        self._axes.set_xlim(self._ranges[0, 0], self._ranges[0, 1])  # type: ignore
        self._axes.set_ylim(self._ranges[1, 0], self._ranges[1, 1])  # type: ignore

        return (self._scatter,)

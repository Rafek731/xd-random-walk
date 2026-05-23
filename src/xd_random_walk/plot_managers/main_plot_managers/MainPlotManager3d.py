from mpl_toolkits.mplot3d.art3d import Line3DCollection
import numpy as np

from .BasePlotManager import BaseMainPlotManager
from typing import Literal
from mpl_toolkits.mplot3d.art3d import Line3DCollection

class MainPlotManager3d(BaseMainPlotManager):
    def __init__(
        self,
        num_samples: int = 500,
        generator_type: Literal["discrete", "uniform", "normal"] = "discrete",
        show_taken_path: bool = False,
        tail_length: int = 100,
    ) -> None:
        super().__init__(dims=3, num_samples=num_samples, generator_type=generator_type)
        self._axes = self._fig.add_subplot(111, projection='3d')
        self._axes.grid(True, alpha=0.5)

        if show_taken_path:
            self._tail_length = tail_length
            self._history = np.zeros((num_samples, tail_length, 3), dtype=self._data_type)
            self._history_idx = 0       
            self._history_filled = False 

            self._lines = Line3DCollection(
                [np.zeros((2, 3))], 
                colors=self._colors, 
                alpha=0.5
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
            depthshade=True 
        )
    def _update_plot(self) -> tuple:
        self._scatter._offsets3d = (self._points[:, 0], self._points[:, 1], self._points[:, 2])

        if self._history is not None:
            self._history[:, self._history_idx, :] = self._points
            self._history_idx += 1
            
            if self._history_idx >= self._tail_length:
                self._history_idx = 0
                self._history_filled = True

            if self._history_filled:
                segments = np.roll(self._history, -self._history_idx, axis=1)
            else:
                segments = self._history[:, :self._history_idx, :]
            self._lines.set_segments(segments)

        self._axes.set_xlim3d(self._ranges[0, 0], self._ranges[0, 1])
        self._axes.set_ylim3d(self._ranges[1, 0], self._ranges[1, 1])
        self._axes.set_zlim3d(self._ranges[2, 0], self._ranges[2, 1]) 

        artists = [self._scatter]
        if self._history is not None:
            artists.append(self._lines)
            
        return tuple(artists)
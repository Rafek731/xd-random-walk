from typing import Literal
import math
from matplotlib.collections import PathCollection
import numpy as np

from .BasePlotManager import BaseMainPlotManager


class MainPlotManagerxd(BaseMainPlotManager):
    def __init__(self, dims: int, num_samples: int = 1, generator_type: Literal['discrete'] | Literal['uniform'] | Literal['normal'] = "discrete") -> None:
        super().__init__(dims, num_samples, generator_type)
        rows, cols = self._get_optimal_grid(dims)
        self._axes = []
        self._scatters = []

        for i in range(dims):
            ax = self._fig.add_subplot(rows, cols, i + 1)
            ax.get_yaxis().set_visible(False)
            for spine in ['top', 'right', 'left']:
                ax.spines[spine].set_visible(False)
            ax.spines['bottom'].set_position('center')
            ax.set_title(f"Dimension {i+1}", loc='left', fontsize=10, color='gray')

            scatter = ax.scatter(
                self._points[:, i],
                np.zeros(num_samples),
                c=self._colors,
                s=25,
                zorder=3
            )
            self._axes.append(ax)
            self._scatters.append(scatter)
        self._fig.tight_layout()


    def _get_optimal_grid(self, n_items: int, aspect_ratio: float = 16/9) -> tuple[int, int]:
        cols = max(1, round(math.sqrt(n_items * aspect_ratio)))
        rows = math.ceil(n_items / cols)
        
        return rows, cols
    
    def _update_plot(self) -> tuple[PathCollection]:
        for d in range(self._dims):
            new_offsets = np.c_[self._points[:, d], np.zeros(self._num_samples)]
            self._scatters[d].set_offsets(new_offsets)
            self._axes[d].set_xlim(self._ranges[d, 0], self._ranges[d, 1])
        return tuple(self._scatters)
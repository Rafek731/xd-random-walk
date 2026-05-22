from dataclasses import dataclass, field
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
import matplotlib.pyplot as plt
import numpy as np
from typing import Literal
from abc import ABC, abstractmethod

from xd_random_walk.RandomVector import DiscreteRVG, UniformRVG, RandomVectorGenerator

def plot_manager_factory(dims: int) -> MainPlotManager:
    pass

class MainPlotManager(ABC):
    _dims: int
    _rvg: RandomVectorGenerator
    _fig: Figure
    _axes: Axes|list[Axes]|None
    _points: np.ndarray
    _ranges: np.ndarray
    _current_avg_distance: float
    _avg_distance: float
    _avg_weight: int

    def __init__(self, dims: int, num_samples: int = 1, generator_type: Literal['discrete', 'uniform'] = 'discrete') -> None:
        self._dims = dims
        match generator_type:
            case 'discrete':
                self._rvg = DiscreteRVG(dims, num_samples)
            case 'uniform':
                self._rvg = UniformRVG(dims, num_samples)
            case _:
                raise ValueError('This generator type is not allowed')
        
        self._fig = plt.figure()
        self._points = np.zeros((num_samples, dims), dtype=float)
        self._ranges = np.array([[-1, 1] for _ in range(dims)], dtype=float)
        self._current_avg_distance = 0
        self._avg_distance = 0
        self._avg_weight = 0 

        self._axes = None

    def update(self, frame=None):
        self._move_points()
        self._update_avgs()
        return self._update_plot()       

    def _move_points(self) -> None:
        self._points += next(self._rvg)

    def _update_avgs(self) -> None:
        distances = np.sum(self._points ** 2, axis=1) ** 0.5
        self._current_avg_distance = np.average(distances)
        self._avg_distance = np.average(
            [self._avg_distance, self._current_avg_distance], 
            weights=[self._avg_weight, len(distances)]
        )
        self._avg_weight += len(self._points)

    @abstractmethod
    def _update_plot(self) -> tuple[PathCollection]:
        pass

    @property
    def avg_distance(self) -> float:
        return self._avg_distance

class MainPlotManager2d(MainPlotManager):
    def __init__(self, num_samples: int = 1, generator_type: Literal['discrete', 'uniform'] = 'discrete') -> None:
        super().__init__(dims=2, num_samples=num_samples, generator_type=generator_type)
        
        self._axes = self._fig.add_subplot(111) 
        self.scatter = self._axes.scatter(
            self._points[:, 0], 
            self._points[:, 1],
            c=np.arange(num_samples),
            cmap='rainbow'
        )
        
    def _update_plot(self) -> tuple[PathCollection]:
        self.scatter.set_offsets(self._points)
        min_x, min_y = np.min(self._points, axis=0)
        max_x, max_y = np.max(self._points, axis=0)
        x_padding, y_padding = (self._ranges[:, 1] - self._ranges[:, 0]) * 0.05
        self._ranges[0, 0] = min(self._ranges[0, 0], min_x - x_padding)
        self._ranges[0, 1] = max(self._ranges[0, 1], max_x + x_padding)
        self._ranges[1, 0] = min(self._ranges[1, 0], min_y - y_padding)
        self._ranges[1, 1] = max(self._ranges[1, 1], max_y + y_padding)

        self._axes.set_xlim(self._ranges[0, 0], self._ranges[0, 1]) # type: ignore
        self._axes.set_ylim(self._ranges[1, 0], self._ranges[1, 1]) # type: ignore

        return self.scatter,


class MainPlotManager3d(MainPlotManager):
    pass

class MainPlotManagerxd(MainPlotManager):
    pass

    


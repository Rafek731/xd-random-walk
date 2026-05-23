from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
import matplotlib.pyplot as plt
from matplotlib.typing import ColorType

import numpy as np

from typing import Literal
from abc import ABC, abstractmethod

from xd_random_walk.RandomVector import (
    DiscreteRVG,
    UniformRVG,
    NormalRVG,
    RandomVectorGenerator,
)
from ..colors import get_colors


class BaseMainPlotManager(ABC):
    __slots__ = [
        "_dims",
        "_num_samples",
        "_rvg",
        "_fig",
        "_axes",
        "_points",
        "_ranges",
        "_current_avg_distance",
        "_avg_distance",
        "_avg_weight",
        "_data_type",
        "_colors",
    ]
    _dims: int
    _num_samples: int
    _rvg: RandomVectorGenerator
    _fig: Figure
    _axes: Axes | list[Axes] | None
    _points: np.ndarray
    _colors: list[ColorType]
    _ranges: np.ndarray
    _avg_distance: float
    _data_type: type

    def __init__(
        self,
        dims: int,
        num_samples: int = 1,
        generator_type: Literal["discrete", "uniform", "normal"] = "discrete",
    ) -> None:
        self._dims = dims
        self._num_samples = num_samples

        match generator_type:
            case "discrete":
                self._rvg = DiscreteRVG(dims, num_samples)
                self._data_type = int
            case "uniform":
                self._rvg = UniformRVG(dims, num_samples)
                self._data_type = float
            case "normal":
                self._rvg = NormalRVG(dims, num_samples)
                self._data_type = float
            case _:
                raise ValueError("This generator type is not allowed")

        self._fig = plt.figure('Points visualization')
        self._points = np.zeros((num_samples, dims), dtype=self._data_type)
        self._ranges = np.array([[-1, 1] for _ in range(dims)], dtype=self._data_type)
        self._colors = get_colors(num_samples)
        self._current_avg_distance = 0
        self._avg_distance = 0
        self._avg_weight = 0

        self._axes = None

    def update(self, frame=None):
        self._move_points()
        self._update_ranges()
        self._update_avgs()
        return self._update_plot()

    def _move_points(self) -> None:
        self._points += next(self._rvg)

    def _update_avgs(self) -> None:
        self._avg_distance = np.average(np.sum(self._points**2, axis=1) ** 0.5)

    def _update_ranges(self, padding_percent: float = 5) -> None:
        maxes = np.max(self._points, axis=0)
        mins = np.min(self._points, axis=0)

        paddings = (
            np.maximum((maxes - mins), np.ones(maxes.shape)) * padding_percent / 100
        )

        self._ranges[:, 0] = np.minimum(self._ranges[:, 0], mins - paddings)
        self._ranges[:, 1] = np.maximum(self._ranges[:, 1], maxes + paddings)

    @abstractmethod
    def _update_plot(self) -> tuple[PathCollection]:
        pass

    @property
    def avg_distance(self) -> float:
        return self._avg_distance

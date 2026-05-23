from abc import ABC, abstractmethod
from typing import Literal

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.artist import Artist
from matplotlib.typing import ColorType

from xd_random_walk.RandomVector import (
    DiscreteRVG,
    UniformRVG,
    NormalRVG,
    RandomVectorGenerator,
)
from ..colors import get_colors


class BaseMainPlotManager(ABC):
    """Abstract base class handling state and logic for N-dimensional spatial random walks."""

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

    def __init__(
        self,
        dims: int,
        num_samples: int = 1,
        generator_type: Literal["discrete", "uniform", "normal"] = "discrete",
    ) -> None:
        self._dims = dims
        self._num_samples = num_samples

        if generator_type == "discrete":
            self._rvg: RandomVectorGenerator = DiscreteRVG(dims, num_samples)
            self._data_type: type = int
        elif generator_type == "uniform":
            self._rvg = UniformRVG(dims, num_samples)
            self._data_type = float
        elif generator_type == "normal":
            self._rvg = NormalRVG(dims, num_samples)
            self._data_type = float
        else:
            raise ValueError(f"Generator type '{generator_type}' is not supported.")

        self._fig: Figure = plt.figure("Points visualization")
        self._points: np.ndarray = np.zeros((num_samples, dims), dtype=self._data_type)
        self._ranges: np.ndarray = np.array([[-1, 1] for _ in range(dims)], dtype=float)
        self._colors: list[ColorType] = get_colors(num_samples)

        self._current_avg_distance: float = 0.0
        self._avg_distance: float = 0.0
        self._avg_weight: float = 0.0
        self._axes: Axes | list[Axes] | None = None

    def update(self, frame: int | None = None) -> tuple[Artist, ...]:
        """Calculates logic and triggers the visual refresh."""
        self._move_points()
        self._update_ranges()
        self._update_avgs()
        return self._update_plot()

    def _move_points(self) -> None:
        """Applies the next vector generation to current point positions."""
        self._points += next(self._rvg)

    def _update_avgs(self) -> None:
        """Calculates the mean absolute distance of all particles from the origin."""
        self._avg_distance = float(np.average(np.sum(self._points**2, axis=1) ** 0.5))

    def _update_ranges(self, padding_percent: float = 5.0) -> None:
        """Expands the spatial ranges to ensure all points remain in camera view."""
        maxes = np.max(self._points, axis=0)
        mins = np.min(self._points, axis=0)

        paddings = (
            np.maximum((maxes - mins), np.ones(maxes.shape)) * padding_percent / 100
        )

        self._ranges[:, 0] = np.minimum(self._ranges[:, 0], mins - paddings)
        self._ranges[:, 1] = np.maximum(self._ranges[:, 1], maxes + paddings)

    @abstractmethod
    def _update_plot(self) -> tuple[Artist, ...]:
        """Draws the points and returns a tuple of Matplotlib Artists updated."""
        pass

    @property
    def avg_distance(self) -> float:
        return self._avg_distance

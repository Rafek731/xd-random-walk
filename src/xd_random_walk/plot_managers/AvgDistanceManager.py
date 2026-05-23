from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


class AvgDistanceManager:
    _averages: list[float]
    _step: int

    _fig: Figure
    _ax: Axes

    _a: float
    _sum_numerator: float
    _sum_denominator: float

    def __init__(self) -> None:
        self._fig = plt.figure("Avarage distance")
        self._ax = self._fig.add_subplot(111)

        self._ax.set_xlabel("N (steps)")
        self._ax.set_ylabel("Distance from Origin")
        self._ax.grid(True, linestyle="--", alpha=0.5)

        self._averages = []
        self._step = 0

        self._sum_numerator = 0.0
        self._sum_denominator = 0.0

        self._avg_line = self._ax.plot([], [], label="Current Step Avg", color="blue")[
            0
        ]
        self._regression_line = self._ax.plot(
            [], [], label="a*sqrt(N)", color="red", linestyle="--"
        )[0]

        self._ax.legend()

    def _fit_a(self, current_avg: float):
        if self._step < 2:
            self._a = 1.0
            return

        self._sum_numerator += current_avg * (self._step ** 0.5)
        self._sum_denominator += self._step

        if self._step > 1:
            self._a = self._sum_numerator / self._sum_denominator

    def update_data(self, new_avg: float):
        self._averages.append(new_avg)
        self._step += 1
        self._fit_a(new_avg)

    def _update_plot(self):
        steps = np.arange(1, self._step + 1)
        self._avg_line.set_data(steps, self._averages)

        theoretical_y = [self._a * (n**0.5) for n in steps]
        self._regression_line.set_data(steps, theoretical_y)

        if self._step > 0:
            self._ax.set_xlim(0, max(10, self._step * 1.05))
            max_y = max(max(self._averages), max(theoretical_y), 1)
            self._ax.set_ylim(0, max_y * 1.1)

        return self._avg_line, self._regression_line

    def update(self):
        return self._update_plot()

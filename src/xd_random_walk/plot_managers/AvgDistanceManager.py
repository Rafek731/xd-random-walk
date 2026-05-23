import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D


class AvgDistanceManager:
    """Manages the 2D plot tracking the average distance of walkers from the origin over time.

    Uses an O(1) memory algorithm for continuous mathematical regression.
    """

    __slots__ = [
        "_averages",
        "_step",
        "_fig",
        "_ax",
        "_a",
        "_sum_numerator",
        "_sum_denominator",
        "_avg_line",
        "_regression_line",
    ]

    def __init__(self) -> None:
        self._fig: Figure = plt.figure("Average distance")
        self._ax: Axes = self._fig.add_subplot(111)

        self._ax.set_xlabel("N (steps)")
        self._ax.set_ylabel("Distance from Origin")
        self._ax.grid(True, linestyle="--", alpha=0.5)

        self._averages: list[float] = []
        self._step: int = 0

        self._sum_numerator: float = 0.0
        self._sum_denominator: float = 0.0
        self._a: float = 1.0

        self._avg_line: Line2D = self._ax.plot(
            [], [], label="Current avg distance", color="blue"
        )[0]

        self._regression_line: Line2D = self._ax.plot(
            [],
            [],
            label=f"{self._a:.5f}*sqrt(N) (sqrt regression)",
            color="red",
            linestyle="--",
        )[0]

        self._ax.legend()

    def _fit_a(self, current_avg: float) -> None:
        """Updates the least-squares regression coefficient dynamically."""
        if self._step < 2:
            self._a = 1.0
            return

        self._sum_numerator += current_avg * (self._step**0.5)
        self._sum_denominator += self._step

        if self._step > 1:
            self._a = self._sum_numerator / self._sum_denominator

    def update_data(self, new_avg: float) -> None:
        """Pushes a new data point to the history and calculates the new regression."""
        self._averages.append(new_avg)
        self._step += 1
        self._fit_a(new_avg)

    def _update_plot(self) -> tuple[Line2D, Line2D]:
        """Redraws the theoretical and empirical lines onto the axes."""
        steps = np.arange(self._step)
        self._avg_line.set_data(steps, self._averages)

        theoretical_y = [self._a * (n**0.5) for n in steps]
        self._regression_line.set_data(steps, theoretical_y)

        self._regression_line.set_label(f"{self._a:.5f} * sqrt(N) (sqrt regression)")
        self._ax.legend(loc="upper left")

        if self._step > 0:
            self._ax.set_xlim(0, max(10, self._step * 1.05))
            max_y = max(max(self._averages), max(theoretical_y), 1)
            self._ax.set_ylim(0, max_y * 1.1)

        return self._avg_line, self._regression_line

    def update(self) -> tuple[Line2D, Line2D]:
        """Primary update loop for FuncAnimation."""
        return self._update_plot()

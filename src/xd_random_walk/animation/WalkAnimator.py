from dataclasses import dataclass, field
from typing import Literal

import matplotlib.pyplot as plt
import matplotlib.animation as anim

from xd_random_walk.plot_managers import (
    get_plot_manager,
    BaseMainPlotManager,
    AvgDistanceManager,
)


@dataclass(slots=True)
class WalkAnimator:
    """Orchestrates the Matplotlib animations for both the spatial walk and statistical averages.

    Attributes:
        dims (int): Number of dimensions for the spatial plot.
        num_samples (int): Number of independent walkers.
        generator_type (Literal["discrete", "uniform", "normal"]): Step distribution.
        show_path (bool): Whether to render trails behind the walkers.
        tail_length (int): Number of historical steps to remember for the trails.
        interval (float): Animation refresh rate in milliseconds.
    """

    dims: int = 2
    num_samples: int = 1
    generator_type: Literal["discrete", "uniform", "normal"] = "discrete"
    show_path: bool = False
    tail_length: int = 2500
    interval: float = 50

    main_anim: anim.FuncAnimation = field(init=False)
    main_manager: BaseMainPlotManager = field(init=False)

    avg_anim: anim.FuncAnimation = field(init=False)
    avg_manager: AvgDistanceManager = field(init=False)

    def __post_init__(self) -> None:
        """Initializes the plot managers and links them to FuncAnimations."""
        self.main_manager = get_plot_manager(
            self.dims,
            self.num_samples,
            self.generator_type,
            self.show_path,
            self.tail_length,
        )

        self.main_anim = anim.FuncAnimation(
            fig=self.main_manager._fig,
            func=self.main_manager.update,
            frames=None,
            interval=self.interval,
            blit=False,
            cache_frame_data=False,
        )

        self.avg_manager = AvgDistanceManager()
        self.avg_anim = anim.FuncAnimation(
            fig=self.avg_manager._fig,
            func=self._update_avg_window,
            frames=None,
            interval=self.interval,
            blit=False,
            cache_frame_data=False,
        )

    def _update_avg_window(self, frame: int) -> tuple:
        """Bridge method to sync the main manager's data to the average distance plot."""
        self.avg_manager.update_data(self.main_manager.avg_distance)
        return self.avg_manager.update()

    def __enter__(self) -> "WalkAnimator":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        pass

    def animate(self) -> None:
        """Starts the Matplotlib event loop and displays the windows."""
        plt.show()

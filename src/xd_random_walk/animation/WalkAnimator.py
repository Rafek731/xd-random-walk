import matplotlib.pyplot as plt
import matplotlib.animation as anim
from dataclasses import dataclass, field
from typing import Literal

from xd_random_walk.plot_managers import get_plot_manager, BaseMainPlotManager


@dataclass(slots=True)
class WalkAnimator:
    dims: int = 2
    num_samples: int = 1
    generator_type: Literal["discrete", "uniform", "normal"] = "discrete"
    show_path: bool = False
    tail_length: int = 2500
    interval: float = 50

    main_anim: anim.FuncAnimation = field(init=False)
    main_manager: BaseMainPlotManager = field(init=False)

    def __post_init__(self):
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
            interval=50,
            blit=False,
            cache_frame_data=False,
        )

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc, tb):
        pass

    def animate(self):
        plt.show()

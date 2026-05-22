from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
from dataclasses import dataclass, field

from xd_random_walk.plot_managers import MainPlotManager2d

@dataclass(slots=True)
class WalkAnimator:
    dims: int = 2
    num_samples: int = 1
    interval: float = 50

    main_anim: anim.FuncAnimation = field(init=False)
    main_manager: MainPlotManager2d = field(init=False)

    def __post_init__(self):
        self.main_manager = MainPlotManager2d(num_samples=self.num_samples)
        self.main_anim = anim.FuncAnimation(
            fig=self.main_manager._fig,
            func=self.main_manager.update,
            frames=None,
            interval = 50,
            blit = False,
            cache_frame_data=False
        )
    
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc, tb):
        pass

    def animate(self):
        plt.show()

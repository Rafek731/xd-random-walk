from .MainPlotManager2d import MainPlotManager2d
from .MainPlotManager3d import MainPlotManager3d
from .MainPlotManagerxd import MainPlotManagerxd
from .BasePlotManager import BaseMainPlotManager
from typing import Literal


def get_plot_manager(
    dims: int,
    num_samples: int = 1,
    generator_type: Literal["discrete", "uniform", "normal"] = "discrete",
    show_path: bool = False,
    tail_length: int = 2500,
) -> BaseMainPlotManager:
    if dims < 2:
        raise ValueError
    if dims == 2:
        return MainPlotManager2d(num_samples, generator_type, show_path, tail_length)
    if dims == 3:
        return MainPlotManager3d(num_samples, generator_type, show_path, tail_length)
    else:
        return MainPlotManagerxd(dims, num_snum_samples, generator_type)

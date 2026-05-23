from typing import Literal

from .MainPlotManager2d import MainPlotManager2d
from .MainPlotManager3d import MainPlotManager3d
from .MainPlotManagerxd import MainPlotManagerxd
from .BasePlotManager import BaseMainPlotManager


def get_plot_manager(
    dims: int,
    num_samples: int = 1,
    generator_type: Literal["discrete", "uniform", "normal"] = "discrete",
    show_path: bool = False,
    tail_length: int = 2500,
) -> BaseMainPlotManager:
    """Factory function yielding the correct PlotManager based on dimensional requirements.

    Args:
        dims (int): Number of target dimensions.
        num_samples (int): Total particles to trace.
        generator_type (Literal["discrete", "uniform", "normal"]): Mathematics distribution.
        show_path (bool): Display trailing lines (2D/3D only).
        tail_length (int): History limit for traces.

    Returns:
        BaseMainPlotManager: The initialized manager subclass handling those specific dimensions.

    Raises:
        ValueError: If dimension requested is < 1.
    """
    if dims < 1:
        raise ValueError("Dimensions must be 1 or greater.")
    elif dims == 2:
        return MainPlotManager2d(num_samples, generator_type, show_path, tail_length)
    elif dims == 3:
        return MainPlotManager3d(num_samples, generator_type, show_path, tail_length)
    else:
        return MainPlotManagerxd(dims, num_samples, generator_type)

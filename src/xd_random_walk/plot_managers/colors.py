import numpy as np
from matplotlib.colors import XKCD_COLORS
from matplotlib.typing import ColorType


def get_colors(n: int) -> list[ColorType]:
    """Generates a list of distinct colors for sample tracking.

    Args:
        n (int): Number of colors to generate.

    Returns:
        list[ColorType]: A list of randomized hex colors drawn from the XKCD dictionary.
    """
    colors = list(XKCD_COLORS.values())
    np.random.shuffle(colors)
    return [colors[i % len(colors)] for i in range(n)]

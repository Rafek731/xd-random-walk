from matplotlib.colors import XKCD_COLORS
from matplotlib.typing import ColorType
import numpy as np


def get_colors(n: int) -> list[ColorType]:
    colors = list(XKCD_COLORS.values())
    np.random.shuffle(colors)
    return [colors[i % len(colors)] for i in range(n)]

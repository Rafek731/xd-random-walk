#!/usr/bin/env python3

from xd_random_walk.cli import parse_cli
import matplotlib.pyplot as plt
from walk import walk1d, walk2d, walk3d, walkxd


def main() -> int:
    args = parse_cli()
    main_fig = plt.figure()
    plot_fig = plt.figure()

    if args.dim < 0:
        raise ValueError(f'Dimension must be a positive integer, but {args.dim} was given')
    
    match args.dim:
        case 1:
            walk1d.walk(main_fig, plot_fig)
        case 2:
            walk2d.walk(main_fig, plot_fig)
        case 3:
            walk3d.walk(main_fig, plot_fig)
        case _:
            walkxd.walk(main_fig, plot_fig, args.dim)
    return 0


if __name__ == "__main__":
    main()

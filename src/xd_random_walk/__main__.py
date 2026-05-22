#!/usr/bin/env python3

from xd_random_walk.cli import parse_cli
import matplotlib.pyplot as plt
from xd_random_walk.animation import WalkAnimator


def main() -> int:
    args = parse_cli()
    animator = WalkAnimator(args.dims, num_samples=args.num_samples)
    animator.animate()
    return 0


if __name__ == "__main__":
    main()

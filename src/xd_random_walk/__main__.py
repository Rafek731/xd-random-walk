#!/usr/bin/env python3

from xd_random_walk.cli import parse_cli
from xd_random_walk.animation import WalkAnimator


def main() -> int:
    args = parse_cli()
    animator = WalkAnimator(
        args.dims,
        args.num_samples,
        args.distribution,
        args.show_path,
        args.tail,
        args.interval,
    )
    animator.animate()
    return 0


if __name__ == "__main__":
    main()

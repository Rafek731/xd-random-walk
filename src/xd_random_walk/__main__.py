#!/usr/bin/env python3
import sys

from xd_random_walk.cli import parse_cli
from xd_random_walk.animation.WalkAnimator import WalkAnimator


def main() -> int:
    """Main entry point for the XD random walk application.

    Returns:
        int: Exit status code (0 for success).
    """
    args = parse_cli()

    animator = WalkAnimator(
        dims=args.dims,
        num_samples=args.num_samples,
        generator_type=args.distribution,
        show_path=args.show_path,
        tail_length=args.tail,
        interval=args.interval,
    )

    animator.animate()
    return 0


if __name__ == "__main__":
    sys.exit(main())

import argparse


def parse_cli() -> argparse.Namespace:
    """Parses command-line arguments for the XD random walk simulation.

    Returns:
        argparse.Namespace: The parsed command-line arguments containing parameters
        like dimensions, number of samples, distribution type, and plot settings.
    """
    parser = argparse.ArgumentParser(
        description="A high-performance, multi-dimensional random walk simulator."
    )
    parser.add_argument(
        "-d",
        "--dimensions",
        type=int,
        default=2,
        dest="dims",
        help="Number of dimensions for the simulation (e.g., 1, 2, 3, or n-dimensional).",
    )
    parser.add_argument(
        "-n",
        "--num-samples",
        type=int,
        default=500,
        dest="num_samples",
        help="Number of independent points/particles to simulate.",
    )
    parser.add_argument(
        "-p",
        "--show-path",
        action="store_true",
        default=False,
        dest="show_path",
        help="Display the trailing paths of points (supported in 2D and 3D). "
        "Warning: Heavy performance impact for >10 points.",
    )
    parser.add_argument(
        "-t",
        "--tail",
        type=int,
        default=100,
        dest="tail",
        help="Number of historical steps to show in the path trail. Defaults to 100.",
    )
    parser.add_argument(
        "-D",
        "--distribution",
        choices=["discrete", "uniform", "normal"],
        default="discrete",
        dest="distribution",
        help="The probability distribution used to generate random steps.",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=100,
        dest="interval",
        help="Animation refresh interval in milliseconds.",
    )
    return parser.parse_args()

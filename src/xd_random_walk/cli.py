import argparse


def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--dimensions",
        type=int,
        default=2,
        dest="dims",
        help="Determine how many dimensions use to perform simulation.",
    )
    parser.add_argument(
        "-n",
        "--num-samples",
        type=int,
        default=500,
        dest="num_samples",
        help="Specify how many points to use in simulation.",
    )
    parser.add_argument(
        "-p",
        "--show-path",
        action="store_true",
        default=False,
        dest="show_path",
        help="Whether to show the path that point took or not (defaults to False), works only in 2d and 3d mode. (If you don't show path then you can show grater number of points on the plot, I highly recommend showing path only for up to 10 points then it looses sense).",
    )
    parser.add_argument(
        "-t",
        "--tail",
        type=int,
        default=100,
        dest="tail",
        help="How many steps back of the point's path to show. Defaults to 100.",
    )
    parser.add_argument(
        "-D",
        "--distribution",
        choices=["discrete", "uniform", "normal"],
        default="discrete",
        dest="distribution",
        help="Which distribution to choose to generate steps. Possible choices are 'discrete', 'uniform' and 'normal'."
    )
    parser.add_argument("-i", "--interval", type=int, default=100, dest="interval")
    return parser.parse_args()

import argparse


def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dimensions",
        "-d",
        type=int,
        default=3,
        dest="dims",
        help="Determine how many dimensions use to perform simulation.",
    )
    parser.add_argument(
        "--num_samples",
        "-n",
        type=int,
        default=50,
        dest="num_samples",
        help="Specify how many points to show.",
    )
    parser.add_argument(
        "--path",
        "-p",
        action="store_true",
        default=False,
        dest="show_path",
        help="Whether to show the path that piont took or not (defaults to false).",
    )
    parser.add_argument(
        "--tail",
        "-t",
        type=int,
        default=5000,
        dest="tail",
        help="How many steps back of the point to show. Defaults to 5000.",
    )
    parser.add_argument(
        "--distribution",
        "-D",
        choices=["discrete", "uniform", "normal"],
        default="discrete",
        dest="distribution",
    )
    parser.add_argument("--interval", "-i", type=int, default=50, dest="interval")
    return parser.parse_args()

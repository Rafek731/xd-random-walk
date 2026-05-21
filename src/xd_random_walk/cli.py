import argparse

def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dimensions',
                        '-d',
                        type=int,
                        default=3,
                        dest='dim',)
    return parser.parse_args()
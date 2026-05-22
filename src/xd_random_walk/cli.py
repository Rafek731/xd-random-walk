import argparse

def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dimensions',
                        '-d',
                        type=int,
                        default=3,
                        dest='dims',)
    parser.add_argument('--num_samples',
                        '-n',
                        type=int,
                        default=50,
                        dest='num_samples')
    return parser.parse_args()
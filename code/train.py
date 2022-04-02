import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    return parser.parse_args()


if __name__ == "__main__":
    parse_args()
    experiment_loggers = None

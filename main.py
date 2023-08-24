from argparse import ArgumentParser
import json
from src.aco import AntColonyOptimizer


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--config", required=True, type=str, help="Name of json file with config")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    with open(args.config) as f:
        config_args = json.load(f)

    aco = AntColonyOptimizer(config_args)
    aco.run()
    aco.results.write_results(1)
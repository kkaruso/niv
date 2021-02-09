import argparse
import yaml
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--convert', type=Path, metavar='', help='Import .yaml to convert to .svg')
args = parser.parse_args()


if __name__ == '__main__':
    if args.convert is not None:
        file_name = str(args.convert).split('\\')[-1]  # get filename
        print(file_name)
        with open(file_name, 'r') as stream:
            try:
                print(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                print(exc)

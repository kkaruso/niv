import argparse
from pathlib import Path


class ArgParser:

    def __init__(self):
        return

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--Import', type=Path, metavar='', help='Visualize .yaml file')
        parser.add_argument('-e', '--export', type=Path, metavar='', help='Export .yaml to .svg file')
        parser.add_argument('-r', '--run', type=Path, metavar='', help='Visualize local network')
        parser.add_argument('-g', '--gui', type=Path, metavar='', help='Start NIV Gui')

        return parser.parse_args()

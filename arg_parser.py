import argparse
from pathlib import Path


class ArgParser:
    """
    A class for parsing the console arguments

    Methods
    -------
    set_args():
        Adds the needed arguments to the ArgumentParser class
    """

    def __init__(self):
        return

    @staticmethod
    def set_args():
        """
        Adds the needed arguments to the ArgumentParser class

            :returns:
                Argument strings converted to objects and assigned as attributes of the namespace
        """
        parser = argparse.ArgumentParser(prog="niv",
                                         description="Creates a visualization of your network infrastructure",
                                         add_help=False)
        parser.add_argument('-h', '--help', action='help',  help='Show this help message and exit')
        parser.add_argument('-v', '--version', action='version', version='1.0', help="Show program's version "
                                                                                     "number and exit")
        parser.add_argument('-r', '--run', type=Path, metavar='', help='Create visualization without exporting '
                                                                       'any files')
        parser.add_argument('-e', '--export', type=Path, metavar='', help='Export .yaml and .svg file to given path'
                                                                          ' or to current directory if no path given')
        parser.add_argument('-i', '--import', type=Path, metavar='', help='Create visualization with a given .yaml '
                                                                          'file')
        parser.add_argument('-g', '--gui', type=Path, metavar='', help='Start niv gui')

        # parser.print_help()

        return parser.parse_args()

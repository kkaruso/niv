import argparse
import os
import pathlib
import sys
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

        :return: Argument strings converted to objects and assigned as attributes of the namespace
        """
        parser = argparse.ArgumentParser(prog="niv",
                                         description="Creates a visualization of your network infrastructure",
                                         add_help=False)
        parser.add_argument('-h', '--help', action='help', help='Show this help message and exit')
        parser.add_argument('-v', '--version', action='version', version='1.0', help="Show program's version "
                                                                                     "number and exit")
        parser.add_argument('-r', '--run', action='store_true',
                            help='Create visualization without exporting any files')
        parser.add_argument('-s', '--save', type=Path, nargs='?', metavar='',
                            help='Save .yaml and .svg file to given path or to current directory if no path given')
        parser.add_argument('-l', '--load', type=check_file(), nargs='?', metavar='',
                            help='Create visualization with a given .yaml file')
        parser.add_argument('-g', '--gui', action='store_true', help='Start niv gui')

        # parser.print_help()
        print(parser.parse_args('-r -s this/is/a/path'.split()))

        args = parser.parse_args()

        return args

    def check_file(self, string):
        """
        Check if file exists in path

        :param string: path to the file as a string
        :return: path, if it exists
        """
        if os.path.isfile(string):
            return string
        else:
            print("No such file '{}'".format(string), file=sys.stderr)

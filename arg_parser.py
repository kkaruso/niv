import argparse
import os
import sys


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

    def set_args(self, args):
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
        parser.add_argument('-s', '--save', type=self.is_path_to_yaml_file, nargs='?', metavar='',
                            help='Save .yaml and .svg file to given path or to current directory if no path given')
        parser.add_argument('-l', '--load', type=self.is_path_to_yaml_file, nargs='?', metavar='',
                            help='Create visualization with a given .yaml file')
        parser.add_argument('-g', '--gui', action='store_true', help='Start niv gui')

        # parser.print_help()
        # print(parser.parse_args('-r'.split()))
        if len(args) == 0:
            print('You didnt specify any arguments, here is some help:\n')
            parser.print_help()

        return parser.parse_args(args)

    @staticmethod
    def is_path_to_yaml_file(file_path):
        """
        Checks if file path is valid and file is a .yaml file
        :param file_path: path to file
        :return: path of file or raise error
        """
        # call .strip to remove all whitespaces in the path
        file_path = file_path.lstrip()
        if os.path.isfile(file_path):
            file_name = file_path.split('\\')[-1]
            file_type = file_name.split('.')[-1]
            if file_type == "yaml":
                return file_path
            else:
                raise argparse.ArgumentTypeError(f'\n"{file_name}" is not a .yaml')
        else:
            raise argparse.ArgumentTypeError(f'\n"{file_path}" is not a valid file path')

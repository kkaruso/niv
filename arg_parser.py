"""
Parser class for Arguments when you start NIV
"""

import argparse
import os
from config_parser import ConfigParser


class ArgParser:
    """
    A class for parsing the console arguments

    Methods
    -------
    set_args():
        Adds the needed arguments to the ArgumentParser class
    """
    config_parsers = ConfigParser()
    config = config_parsers.get_config()

    # Dictionary for argument choices
    ICONS = [1, 2, 3]
    DETAIL = [1, 2, 3]

    def __init__(self, args):
        self.args = args
        self.parser = argparse.ArgumentParser
        self.set_args()

    def set_args(self):
        """
        Adds the needed arguments to the ArgumentParser class

        :return: Argument strings converted to objects and assigned as attributes of the namespace
        """
        parser = argparse.ArgumentParser(prog="niv",
                                         description="Creates a visualization of your network infrastructure",
                                         add_help=False)

        optional = parser.add_argument_group('optional arguments')

        optional.add_argument('-v', '--version', action='version', version='1.0',
                              help="Show program's version number and exit")

        optional.add_argument('-h', '--help', action='help', help='Show this help message and exit')

        subparsers = parser.add_subparsers(dest="command")

        optional.add_argument('-d', '--detail', type=int, nargs='?', metavar='INT',
                              default=self.config["DEFAULT"]["std_details"], choices=self.DETAIL,
                              help='The level of detail you want to use for the visualization; 1: least detail, '
                                   '2: medium detail, 3: most detail (DEFAULT: 1)')

        load_parser = subparsers.add_parser('load', help='Create visualization with a given .yaml file')

        run_parser = subparsers.add_parser('run', help='Create visualization without saving any files')

        gui_parser = subparsers.add_parser('gui', help='Start niv gui')

        load_parser.add_argument('-s', '--save', type=self.save_to_path,
                                 nargs='?', metavar='OUTPUT_PATH',
                                 help='Save .svg, .png or .jpeg file to a given path (DEFAULT: .svg)')

        load_parser.add_argument('-p', '--path', type=self.is_path_to_yaml_file,
                                 required=True, help='Path to .yaml file')

        run_parser.add_argument('-s', '--save', type=self.save_to_path,
                                metavar='OUTPUT_PATH',
                                help='Save .svg, .png or .jpeg file to a given path (DEFAULT: .svg)')

        # If no argument given, print help
        if len(self.args) == 0:
            print('You didnt specify any arguments, here is some help:\n')
            parser.print_help()
        self.parser = parser.parse_args(self.args)
        print(self.args)
        return self.parser

    def get_parser(self):
        """
        :return: returns set parser from set_parser()
        """
        return self.parser

    def get_save_path(self):

        return self.args[self.args.index('-s') + 1]

    def get_load_path(self):
        return self.args[self.args.index('-p') + 1]

    @staticmethod
    def is_path_to_yaml_file(file_path):
        """
        Checks if file path is valid and file is a .yaml file

        :param file_path: path to file
        :return: path of file or raise error
        """
        # call lstrip() to remove all whitespaces in front of the path
        file_path = file_path.lstrip()
        if os.path.isfile(file_path):
            file_name = file_path.split('/')[-1]
            file_type = file_name.split('.')[-1]
            if file_type == "yaml":
                return file_path
            raise Exception(f'\n"{file_name}" is not a .yaml')
        raise Exception(f'\n"{file_path}" is not a valid file path')

    def create_filename(self):
        """
        generate name from input file and return it
        :return: generated filename
        """
        file_name = self.get_load_path()
        file_format = self.config["DEFAULT"]["std_type"]
        file_name = file_name.split('/')[-1].split('.')[0]
        file_name = f"{file_name}{file_format}"
        return file_name

    def save_to_path(self, file_path):
        """
        Checks if the path is a file path or a directory path
        and creates the output file in the corresponding
        directory with a suitable name, if no name is given

        :param file_path: path to where the file should be saved
        :return: path to file or raise error
        """
        # Call lstrip() to remove all whitespaces in front of the path
        file_path = file_path.lstrip()
        last_element = file_path.split('/')[-1]
        # Workaround that adds a "./" at the start of the path if no "./" is entered
        if file_path[0:2] != "./":
            file_path = "./" + file_path
        path = file_path.removesuffix(f'{last_element}')

        # If the path is just a '.' create a file in the current directory
        if file_path == '.':
            # file_name = ArgParser.create_filename(f"{file_path}/")
            file_name = self.create_filename()
            # Create the file in the current directory
            file = open(f"{file_name}", "a")
            file.close()
            return file_name

        # If there is a '.' in the name of the last element of the
        # path, it is a file, else it is a directory
        if '.' in last_element:
            # Check if the file has the right format (.svg, .png, .jpeg), else raise Exception
            if last_element.lower().endswith(('.svg', '.png', '.jpg', 'pdf')):
                # Check if the directory above the file exists, else raise Exception
                if os.path.isdir(path):
                    return file_path
                    # raise FileExistsError(f"{last_element} already exists")
                raise Exception(f'\n"{path}": directory doesn\'t exist')
            raise TypeError(f"{last_element} is the wrong file format (must be either .svg, .png, .jpg, .pdf)")

        # Check if directory exists. If it does return the file_path, else raise Exception
        if os.path.isdir(file_path):
            # Check if last symbol is a "/" otherwise add a "/"
            if file_path[-1] != "/":
                file_path += "/"
            file_name = self.create_filename()
            # Create the file in the given directory
            file = open(f"{file_path}{file_name}", "a")
            file.close()
            return file_path
        raise Exception(f'\n"{file_path}": directory doesn\'t exist')

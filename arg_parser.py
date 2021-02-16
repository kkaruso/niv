import argparse
import os
import sys
from datetime import date


class ArgParser:
    """
    A class for parsing the console arguments

    Methods
    -------
    set_args():
        Adds the needed arguments to the ArgumentParser class
    """

    # Dictionary for argument choices
    ICONS = [1, 2, 3]
    DETAIL = [1, 2, 3]

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

        parser.add_argument('-s', '--save', type=self.save_to_path, nargs='?', metavar='OUTPUT_PATH',
                            help='Save .svg, .png or .jpeg file to a given path (DEFAULT: .svg)')

        parser.add_argument('-l', '--load', type=self.is_path_to_yaml_file, nargs='?', metavar='INPUT_PATH',
                            help='Create visualization with a given .yaml file')

        parser.add_argument('-i', '--icons', type=int, nargs='?', metavar='INT', default=1, choices=self.ICONS,
                            help='Choose the icons you want to use for the visualization; 1: cisco, 2: osa (DEFAULT: 1)')

        parser.add_argument('-d', '--detail', type=int, nargs='?', metavar='INT', default=1, choices=self.DETAIL,
                            help='The level of detail you want to use for the visualization; 1: least detail, '
                                 '2: medium detail, 3: most detail (DEFAULT: 1)')

        parser.add_argument('-r', '--run', action='store_true',
                            help='Create visualization without saving any files')

        parser.add_argument('-g', '--gui', action='store_true', help='Start niv gui')

        # print(parser.parse_args("-s .".split()))
        # If no argument given, print help
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
        # call lstrip() to remove all whitespaces in front of the path
        file_path = file_path.lstrip()
        if os.path.isfile(file_path):
            file_name = file_path.split('/')[-1]
            file_type = file_name.split('.')[-1]
            if file_type == "yaml":
                return file_path
            else:
                raise argparse.ArgumentTypeError(f'\n"{file_name}" is not a .yaml')
        else:
            raise Exception(f'\n"{file_path}" is not a valid file path')

    @staticmethod
    def create_filename(file_path):
        """
        Generate a file name with today's date

        :param file_path: path to where the file should be saved
        :return generated filename
        """
        i = 1
        date_today = "{:%Y%m%d}".format(date.today())
        file_name = f"{date_today}_NIV_Diagram.svg"
        # Add an incrementing number to end of file if file name already exists
        while os.path.isfile(f"{file_path}{file_name}"):
            file_name = file_name.split('.')[0].split('-')[0]
            file_name = f"{file_name}-{i}"
            file_name = f"{file_name}.svg"
            i += 1

        return file_name

    @staticmethod
    def save_to_path(file_path):
        """
        Checks if the path is a file path or a directory path and creates the output file in the corresponding
        directory with a suitable name, if no name is given

        :param file_path: path to where the file should be saved
        :return: path to file or raise error
        """
        # print(f"Filepath: {file_path}")
        # Call lstrip() to remove all whitespaces in front of the path
        file_path = file_path.lstrip()
        last_element = file_path.split('/')[-1]
        # print(f"Last element: {last_element}")

        # If the path is just a '.' create a file in the current directory
        if file_path == '.':
            file_name = ArgParser.create_filename(f"{file_path}/")
            # create the file in the current directory
            f = open(f"{file_name}", "a")
            f.close()
            return file_name

        # If there is a '.' in the name of the last element of the path, it is a file, else it is a directory
        elif '.' in last_element:
            # Check if file already exists. If it doesn't create file, else raise exception
            if not os.path.isfile(file_path):
                # TODO: create file and check if file format is correct (.svg, .png, .jpeg)
                return file_path
            else:
                raise FileExistsError(f"{last_element} already exists")

        else:
            # Check if directory exists. If it does return the file_path, else raise exception
            if os.path.isdir(file_path):
                # Check if last symbol is a "/" otherwise add a "/"
                if file_path[-1] != "/":
                    file_path += "/"
                file_name = ArgParser.create_filename(file_path)
                # Create file in the given directory
                f = open(f"{file_path}{file_name}", "a")
                f.close()
                return file_path
            else:
                raise Exception(f'\n"{file_path}": directory doesn\'t exist')

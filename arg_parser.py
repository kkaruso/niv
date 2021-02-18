import argparse
import os
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

        parser.add_argument('-v', '--version', action='version', version='1.0',
                            help="Show program's version number and exit")

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

        # print(parser.parse_args("-g".split()))
        # If no argument given, print help
        if len(args) == 0:
            print('You didnt specify any arguments, here is some help:\n')
            parser.print_help()

        # Checks if the arguments are compatible with each other, else raise Exception
        if self.check_args_compatibility(args):
            return parser.parse_args(args)
        else:
            Exception("Arguments are not compatible")

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
        Generate a file name with today's date and check
        if file with the same name already exists. If it does add a
        number at the end of the name

        :param file_path: path to where the file should be saved
        :return: generated filename
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
            file_name = ArgParser.create_filename(f"{file_path}/")
            # Create the file in the current directory
            f = open(f"{file_name}", "a")
            f.close()
            return file_name

        # If there is a '.' in the name of the last element of the
        # path, it is a file, else it is a directory
        elif '.' in last_element:
            # Check if the file has the right format (.svg, .png, .jpeg), else raise Exception
            if last_element.lower().endswith(('.svg', '.png', '.jpeg')):
                # Check if the directory above the file exists, else raise Exception
                if os.path.isdir(path):
                    # Check if file already exists. If it doesn't create file, else raise FileExistsError
                    if not os.path.isfile(file_path):
                        # Create the given file in the given directory
                        f = open(f"{file_path}", "a")
                        f.close()
                        return file_path
                    else:
                        raise FileExistsError(f"{last_element} already exists")
                else:
                    raise Exception(f'\n"{path}": directory doesn\'t exist')
            else:
                raise TypeError(f"{last_element} is the wrong file format (must be either .svg, .png, .jpeg)")

        else:
            # Check if directory exists. If it does return the file_path, else raise Exception
            if os.path.isdir(file_path):
                # Check if last symbol is a "/" otherwise add a "/"
                if file_path[-1] != "/":
                    file_path += "/"
                file_name = ArgParser.create_filename(file_path)
                # Create the file in the given directory
                f = open(f"{file_path}{file_name}", "a")
                f.close()
                return file_path
            else:
                raise Exception(f'\n"{file_path}": directory doesn\'t exist')

    @staticmethod
    def check_args_compatibility(args):
        """
        Checks if the given arguments are compatible with each other
        (e.g: --gui can't be used with any other argument)

        :param args: parsed arguments as a namespace
        :return: true, if arguments are compatible. false, if not
        """
        # Set variable to True if argument is given
        icons = "--icons" in args or "-i" in args
        detail = "--detail" in args or "-d" in args
        load = "--load" in args or "-l" in args
        save = "--save" in args or "-s" in args
        run = "--run" in args or "-r" in args
        gui = "--gui" in args or "-g" in args

        # If no arguments are given
        if len(args) == 0:
            return True
        # If -g/--gui is used with any other argument, raise ArgumentError
        elif (icons or detail or load or save or run) and gui:
            raise Exception("Can\'t use -g/--gui with other arguments :)")
        # If -r/--run is used with -l/--load, raise ArgumentError
        elif run and load:
            raise Exception("Can\'t use -r/--run with -l/--load :)")
        # If neither load, run or gui are as arguments -> the program would do nothing
        elif not (load or run or gui):
            raise Exception("To use NIV you need either load, run or gui as an argument :)")
        return True

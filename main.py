"""
Main
"""
import sys
from arg_parser import ArgParser
from build_diagram import BuildDiagram

if __name__ == '__main__':

    # Create an instance of the ArgParser class
    arg_parser = ArgParser(sys.argv[1:])
    # Call the function "set_args"
    args = arg_parser.get_parser()

    if args.command == 'load':
        if arg_parser.get_save_path:
            print(arg_parser.get_save_path())
            print(arg_parser.get_load_path())
          #  diagram_builder = BuildDiagram(arg_parser.get_load_path(), str(arg_parser.get_save_path))
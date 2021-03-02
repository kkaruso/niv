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

    diagram_builder = BuildDiagram("templates/template.yaml", "Test_Diagram.svg")
    diagram_builder.create_diagram()

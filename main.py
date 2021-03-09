"""
Main
"""
import os
import sys
from contextlib import suppress
from arg_parser import ArgParser
from build_diagram import BuildDiagram
from niv_logger import NivLogger

if __name__ == '__main__':
    # Create an instance of the logger Class
    Logger = NivLogger
    Logger.clear_log()

    try:
        # Create an instance of the ArgParser class
        arg_parser = ArgParser(sys.argv[1:])
        # Call the function "set_args"
        args = arg_parser.get_parser()
        with suppress(KeyError):
            diagram_builder = BuildDiagram("templates/template.yaml", "Test_Diagram.svg",
                                           arg_parser.get_detail_level(), arg_parser.get_verbose())
            diagram_builder.run()

    except (OSError, ValueError, TypeError, AssertionError) as error_message:
        # create variables to look on which files the error occurred
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

        # add log message in log file
        Logger.log_error(f"Unexpected Error in: {fname} in line {exc_tb.tb_lineno}")
        print(error_message)

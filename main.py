"""
Main
"""
import sys
from arg_parser import ArgParser

# Create an instance of the ArgParser class
arg_parser = ArgParser(sys.argv[1:])
# Call the function "set_args"
args = arg_parser.get_parser()

print(args.load)
print(f"Test: {str(arg_parser.get_load())}\n")

from unittest import TestCase
from arg_parser import ArgParser
import argparse


class TestArgParser(TestCase):
    """
    A class for testing functions of ArgParser class
    """

    def test_set_args(self):
        """
        set_args function test
        """
        parser = ArgParser()
        self.assertEqual(argparse.Namespace(run=None, save=None, load=None, gui=None), parser.set_args())

    # TODO: add test for is_path_to_yaml_file()

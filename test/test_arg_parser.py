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
        self.assertEqual(argparse.Namespace(run=False, save=None, load=None, gui=False), parser.set_args(""))

        self.assertTrue(parser.set_args(["--run"]))
        self.assertTrue(parser.set_args(["-r"]))

        self.assertTrue(parser.set_args(["--gui"]))
        self.assertTrue(parser.set_args(["-g"]))

        self.assertEqual(argparse.Namespace(run=True, save=None, load=None, gui=False), parser.set_args(["--run"]))
        self.assertEqual(argparse.Namespace(run=True, save=None, load=None, gui=False), parser.set_args(["-r"]))

        self.assertEqual(argparse.Namespace(run=False, save=None, load=None, gui=True), parser.set_args(["--gui"]))
        self.assertEqual(argparse.Namespace(run=False, save=None, load=None, gui=True), parser.set_args(["-g"]))

        self.assertEqual(argparse.Namespace(run=True, save=None, load=None, gui=True), parser.set_args(["-g", "-r"]))
        self.assertEqual(argparse.Namespace(run=True, save="test.yaml", load=None, gui=False),
                         parser.set_args(["-s test.yaml", "-r"]))

        self.assertEqual(argparse.Namespace(run=False, save="test.yaml", load=None, gui=False),
                         parser.set_args(["-s test.yaml"]))
        # self.assertEqual(argparse.Namespace(run=False, save="test.yaml", load=None, gui=False),
        #                 parser.set_args(["--save test.yaml"]))

        self.assertEqual(argparse.Namespace(run=False, save=None, load="test.yaml", gui=False),
                         parser.set_args(["-l test.yaml"]))
    # TODO: add test for is_path_to_yaml_file()

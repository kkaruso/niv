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
        self.assertEqual(argparse.Namespace(save=None, load=None, icons=1, detail=1, run=False, gui=False),
                         parser.set_args(""))

        self.assertTrue(parser.set_args(["--run"]))

        self.assertTrue(parser.set_args(["-r"]))

        self.assertTrue(parser.set_args(["--gui"]))

        self.assertTrue(parser.set_args(["-g"]))

        self.assertEqual(argparse.Namespace(save=None, load=None, icons=1, detail=1, run=True, gui=False),
                         parser.set_args(["--run"]))

        self.assertEqual(argparse.Namespace(save=None, load=None, icons=1, detail=1, run=True, gui=False),
                         parser.set_args(["-r"]))

        self.assertEqual(argparse.Namespace(save=None, load=None, icons=1, detail=1, run=False, gui=True),
                         parser.set_args(["--gui"]))

        self.assertEqual(argparse.Namespace(save=None, load=None, icons=1, detail=1, run=False, gui=True),
                         parser.set_args(["-g"]))

        self.assertEqual(argparse.Namespace(save=None, load=None, icons=1, detail=1, run=True, gui=True),
                         parser.set_args(["-g", "-r"]))

        self.assertEqual(argparse.Namespace(save="test2.yaml", load=None, icons=1, detail=1, run=True, gui=False),
                         parser.set_args(["-s", "test2.yaml", "-r"]))

        self.assertEqual(argparse.Namespace(save="test2.yaml", load=None, icons=1, detail=1, run=False, gui=False),
                         parser.set_args(["-s", "test2.yaml"]))

        self.assertEqual(argparse.Namespace(save="test2.yaml", load=None, icons=1, detail=1, run=False, gui=False),
                         parser.set_args(["--save", "test2.yaml"]))

        self.assertEqual(argparse.Namespace(save=None, load="test.yaml", icons=1, detail=1, run=False, gui=False),
                         parser.set_args(["-l", "test.yaml"]))

        self.assertEqual(argparse.Namespace(save=None, load="test.yaml", icons=1, detail=1, run=False, gui=False),
                         parser.set_args(["--load", "test.yaml"]))

        self.assertEqual(argparse.Namespace(save=None, load="test.yaml", icons=1, detail=1, run=False, gui=True),
                         parser.set_args(["-g", "-l", "test.yaml"]))

        self.assertEqual(argparse.Namespace(save="test2.yaml", load="test.yaml", icons=1, detail=1, run=True, gui=True),
                         parser.set_args(["-r", "-s", "test2.yaml", "-g", "-l", "test.yaml"]))

        self.assertEqual(argparse.Namespace(save=None, load=None, icons=2, detail=2, run=False, gui=False),
                         parser.set_args(["-i", "2", "-d", "2"]))

        self.assertEqual(argparse.Namespace(save=None, load=None, icons=2, detail=1, run=True, gui=False),
                         parser.set_args(["-r", "-i", "2"]))

    def test_is_path_to_yaml_file(self):
        """
        is_path_to_yaml_file function test
        """
        parser = ArgParser()
        with self.assertRaises(Exception):
            parser.is_path_to_yaml_file("this/is/a/path")

        with self.assertRaises(Exception):
            parser.is_path_to_yaml_file("this/is/a/path/test.yaml")

        with self.assertRaises(argparse.ArgumentTypeError):
            parser.is_path_to_yaml_file("test.txt")

        self.assertEqual("test.yaml", parser.is_path_to_yaml_file("test.yaml"))

        self.assertIsNotNone("test.yaml", parser.is_path_to_yaml_file("test.yaml"))

    def test_save_to_path(self):
        """
        save_to_path function test
        """
        parser = ArgParser()
        with self.assertRaises(Exception):
            parser.save_to_path("test_directory/")

        with self.assertRaises(FileExistsError):
            parser.save_to_path("test.yaml")

        self.assertEqual("test2.yaml", parser.save_to_path("test2.yaml"))

        self.assertEqual("testdirectory", parser.save_to_path("testdirectory"))

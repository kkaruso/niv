"""
Includes all tests for arg_parser
"""
import argparse
import os
import shutil
from unittest import TestCase

from src import yaml_parser
from src.arg_parser import ArgParser


class TestArgParser(TestCase):
    """
    A class for testing functions of ArgParser class
    """
    test_directory_path = "testdirectory/"

    def setUp(self) -> None:
        """
        Setup tests directories and files for testing
        """
        try:
            os.mkdir(self.test_directory_path)
            with open("tests.txt", "w"):
                pass
            with open("tests.yaml", "w"):
                pass
            with open("tests.svg", "w"):
                pass

        except OSError:
            print(f"Creation of the directory {self.test_directory_path} failed")
        else:
            print(f"Successfully created the directory {self.test_directory_path}")
            print("Successfully created tests files")

    def test_set_args(self):
        """
        set_args function tests
        """
        path_to_project = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config = yaml_parser.get_yaml(path_to_project + '/config.yaml')
        detail = config.get('default').get('std_details')
        parser = ArgParser("")

        self.assertEqual(argparse.Namespace(save=None, load=None, detail=detail, verbose=False),
                         parser.get_parser())

        parser = ArgParser(["-s", f"{self.test_directory_path}test2.svg", "-l", "./tests.yaml"])
        self.assertEqual(
            argparse.Namespace(save=[f"./{self.test_directory_path}test2.svg"], load=["./tests.yaml"],
                               detail=detail, verbose=False),
            parser.get_parser())

        parser = ArgParser(["-l", "./tests.yaml"])
        self.assertEqual(argparse.Namespace(save=None, load=["./tests.yaml"], detail=detail, verbose=False),
                         parser.get_parser())

        parser = ArgParser(["--load", "./tests.yaml"])
        self.assertEqual(argparse.Namespace(save=None, load=["./tests.yaml"], detail=detail, verbose=False),
                         parser.get_parser())

        parser = ArgParser(["-d", "2", "-l", "./tests.yaml"])
        self.assertEqual(argparse.Namespace(save=None, load=["./tests.yaml"], detail=2, verbose=False),
                         parser.get_parser())

        parser = ArgParser(["-l", "./tests.yaml", "-vv"])
        self.assertEqual(argparse.Namespace(save=None, load=["./tests.yaml"], detail=detail, verbose=True),
                         parser.get_parser())

    def test_is_path_to_yaml_file(self):
        """
        is_path_to_yaml_file function tests
        """
        parser = ArgParser(["-l", "./tests.yaml"])
        with self.assertRaises(Exception):
            parser.is_path_to_yaml_file("./this/is/a/path")

        with self.assertRaises(Exception):
            parser.is_path_to_yaml_file("./this/is/a/path/tests.svg")

        with self.assertRaises(Exception):
            parser.is_path_to_yaml_file("./tests.txt")

        self.assertEqual("./tests.yaml", parser.is_path_to_yaml_file("./tests.yaml"))

    def test_get_load(self):
        """
        get_load function tests
        """
        parser = ArgParser(["-l", "./tests.yaml"])
        self.assertEqual("./tests.yaml", parser.get_load())

        parser = ArgParser(["-l", "./tests.yaml", "-s", f"{self.test_directory_path}test.svg"])
        self.assertEqual("./tests.yaml", parser.get_load())

        parser = ArgParser(["-l", "./tests.yaml", "-s", "./"])
        self.assertEqual("./tests.yaml", parser.get_load())

        parser = ArgParser(["-l", "./tests.yaml", "-s", "."])
        self.assertEqual("./tests.yaml", parser.get_load())

        parser = ArgParser(["-s", ".", "-l", "./tests.yaml"])
        self.assertEqual("./tests.yaml", parser.get_load())

    def test_save_to_path(self):
        """
        save_to_path function tests
        """
        parser = ArgParser(["-l", "./tests.yaml"])

        self.assertEqual("./tests.svg", parser.save_to_path("./"))

        self.assertEqual("./tests.svg", parser.save_to_path("."))

        self.assertEqual("ein_anderer_test.svg", parser.save_to_path("ein_anderer_test.svg"))

        self.assertEqual("testdirectory/tests.svg", parser.save_to_path("testdirectory/tests.svg"))

        self.assertEqual(f"{self.test_directory_path}test2.svg",
                         parser.save_to_path(f"{self.test_directory_path}test2.svg"))

        self.assertEqual(f"{self.test_directory_path}tests.svg", parser.save_to_path(f"{self.test_directory_path}"))

        self.assertEqual("testdirectory/tests.svg",
                         parser.save_to_path(f"{self.test_directory_path}"))

        with self.assertRaises(OSError):
            parser.save_to_path("./testslmao/")

        with self.assertRaises(OSError):
            parser.save_to_path("./testslmao/")

        parser = ArgParser(["-l", "tests.yaml", "-s", "."])

        self.assertEqual("./tests.svg", parser.get_save_path()[0])

    def test_create_filename(self):
        """
        create_filename function tests
        """
        parser = ArgParser(["-l", "./tests.yaml"])
        file_name = "tests.svg"

        self.assertEqual(file_name, parser.create_filename())

    def test_check_args_compatibility(self):
        """
        check_args_compatibility function tests
        """

        with self.assertRaises(Exception):
            ArgParser(["-d"])

        with self.assertRaises(Exception):
            ArgParser(["-s"])

        with self.assertRaises(Exception):
            ArgParser(["-d", "-s"])

        with self.assertRaises(Exception):
            ArgParser(["-d"])

        with self.assertRaises(Exception):
            ArgParser(["-d", "-s"])

        with self.assertRaises(Exception):
            ArgParser(["-s"])

        with self.assertRaises(Exception):
            ArgParser(["Test"])

        with self.assertRaises(Exception):
            ArgParser(["123"])

        parser = ArgParser(["-l", "./tests.yaml"])
        self.assertTrue(parser.check_args_compatibility())

    def tearDown(self) -> None:
        """
        Removes files and directory created by testing
        """
        try:
            shutil.rmtree(f'{self.test_directory_path}', ignore_errors=True)
            os.remove("tests.svg")
            os.remove("tests.txt")
            os.remove("tests.yaml")
        except OSError:
            print(f"Deletion of the directory {self.test_directory_path} failed")
        else:
            print(f"Successfully deleted the directory {self.test_directory_path}")
            print("Successfully deleted Test files")

from unittest import TestCase
from arg_parser import ArgParser
import argparse
import os
import shutil


class TestArgParser(TestCase):
    """
    A class for testing functions of ArgParser class
    """
    testdirectory_path = "testdirectory/"

    def setUp(self) -> None:
        """
        Setup test directories and files for testing
        """
        try:
            os.mkdir(self.testdirectory_path)
        except OSError:
            print(f"Creation of the directory {self.testdirectory_path} failed")
        else:
            print(f"Successfully created the directory {self.testdirectory_path}")

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

        self.assertEqual(argparse.Namespace(save=None, load="test.svg", icons=1, detail=1, run=False, gui=False),
                         parser.set_args(["-l", "test.svg"]))

        self.assertEqual(argparse.Namespace(save=None, load="test.svg", icons=1, detail=1, run=False, gui=False),
                         parser.set_args(["--load", "test.svg"]))

        self.assertEqual(argparse.Namespace(save=None, load="test.svg", icons=1, detail=1, run=False, gui=True),
                         parser.set_args(["-g", "-l", "test.svg"]))

        self.assertEqual(argparse.Namespace(save="test2.yaml", load="test.svg", icons=1, detail=1, run=True, gui=True),
                         parser.set_args(["-r", "-s", "test2.yaml", "-g", "-l", "test.svg"]))

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
            parser.is_path_to_yaml_file("this/is/a/path/test.svg")

        with self.assertRaises(argparse.ArgumentTypeError):
            parser.is_path_to_yaml_file("test.txt")

        self.assertEqual("test.svg", parser.is_path_to_yaml_file("test.svg"))

        self.assertIsNotNone("test.svg", parser.is_path_to_yaml_file("test.svg"))

    def test_save_to_path(self):
        """
        save_to_path function test
        """
        parser = ArgParser()
        with self.assertRaises(Exception):
            parser.save_to_path("test_directory/")

        with self.assertRaises(FileExistsError):
            parser.save_to_path("test.svg")

        with self.assertRaises(TypeError):
            parser.save_to_path("test.yaml")

        self.assertEqual(f"./{self.testdirectory_path}test2.svg",
                         parser.save_to_path(f"{self.testdirectory_path}test2.svg"))

        # first file in testdirectory
        self.assertEqual(f"./{self.testdirectory_path}", parser.save_to_path(f"{self.testdirectory_path}"))

        from datetime import date
        date_today = "{:%Y%m%d}".format(date.today())
        file_name = f"{date_today}_NIV_Diagram"

        # second file -> -1
        self.assertEqual("./testdirectory/",
                         parser.save_to_path(f"./{self.testdirectory_path}"))
        # third file -> -2
        # create file and give directory_list the array of created files
        # the new file should be on the second position

        parser.save_to_path(f"{self.testdirectory_path}")
        directory_list = os.listdir(f"{self.testdirectory_path}")
        self.assertEqual(f"{file_name}-2.svg", f"{directory_list[1]}")

    def test_create_filename(self):
        """
        create_filename function test
        """
        from datetime import date
        parser = ArgParser()
        date_today = "{:%Y%m%d}".format(date.today())
        file_name = f"{date_today}_NIV_Diagram.svg"

        self.assertEqual(file_name, parser.create_filename("."))

    def tearDown(self) -> None:
        """
        Removes files and directory created by testing
        """
        try:
            shutil.rmtree(f'{self.testdirectory_path}', ignore_errors=True)
        except OSError:
            print(f"Deletion of the directory {self.testdirectory_path} failed")
        else:
            print(f"Successfully deleted the directory {self.testdirectory_path}")

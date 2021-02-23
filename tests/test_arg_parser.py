from unittest import TestCase
from arg_parser import ArgParser
import argparse
import os
import shutil


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
        # TODO: Fix tests
        parser = ArgParser("")
        self.assertEqual(argparse.Namespace(save=None, load=None, icons=1, detail=1, run=False, gui=False),
                         parser.get_parser())

        parser = ArgParser(["--run"])
        self.assertTrue(parser.get_parser())

        parser = ArgParser(["-r"])
        self.assertTrue(parser.get_parser())

        parser = ArgParser(["--gui"])
        self.assertTrue(parser.get_parser())

        parser = ArgParser(["-g"])
        self.assertTrue(parser.get_parser())

        parser = ArgParser(["--run"])
        self.assertEqual(argparse.Namespace(save=None, load=None, icons=1, detail=1, run=True, gui=False),
                         parser.get_parser())

        parser = ArgParser(["-r"])
        self.assertEqual(argparse.Namespace(save=None, load=None, icons=1, detail=1, run=True, gui=False),
                         parser.get_parser())

        parser = ArgParser(["--gui"])
        self.assertEqual(argparse.Namespace(save=None, load=None, icons=1, detail=1, run=False, gui=True),
                         parser.get_parser())

        parser = ArgParser(["-g"])
        self.assertEqual(argparse.Namespace(save=None, load=None, icons=1, detail=1, run=False, gui=True),
                         parser.get_parser())

        parser = ArgParser(["-s", f"{self.test_directory_path}test2.svg", "-r"])
        self.assertEqual(
            argparse.Namespace(save=f"./{self.test_directory_path}test2.svg", load=None, icons=1, detail=1, run=True,
                               gui=False),
            parser.get_parser())

        parser = ArgParser(["-s", f"{self.test_directory_path}test3.svg", "-r"])
        self.assertEqual(
            argparse.Namespace(save=f"./{self.test_directory_path}test3.svg", load=None, icons=1, detail=1, run=True,
                               gui=False),
            parser.get_parser())

        parser = ArgParser(["--save", f"{self.test_directory_path}test4.svg", "-r"])
        self.assertEqual(
            argparse.Namespace(save=f"./{self.test_directory_path}test4.svg", load=None, icons=1, detail=1, run=True,
                               gui=False),
            parser.get_parser())

        parser = ArgParser(["-l", "./tests.yaml"])
        self.assertEqual(argparse.Namespace(save=None, load="./tests.yaml", icons=1, detail=1, run=False, gui=False),
                         parser.get_parser())

        parser = ArgParser(["--load", "./tests.yaml"])
        self.assertEqual(argparse.Namespace(save=None, load="./tests.yaml", icons=1, detail=1, run=False, gui=False),
                         parser.get_parser())

        parser = ArgParser(["-d", "2", "-l", "./tests.yaml"])
        self.assertEqual(argparse.Namespace(save=None, load="./tests.yaml", icons=1, detail=2, run=False, gui=False),
                         parser.get_parser())

        parser = ArgParser(["-i", "2", "-d", "2", "-r"])
        self.assertEqual(argparse.Namespace(save=None, load=None, icons=2, detail=2, run=True, gui=False),
                         parser.get_parser())

        parser = ArgParser(["-r", "-i", "2"])
        self.assertEqual(argparse.Namespace(save=None, load=None, icons=2, detail=1, run=True, gui=False),
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
        parser = ArgParser(["-l", "./tests.yaml"])

        self.assertEqual("./tests.yaml", parser.get_load())

    def test_save_to_path(self):
        """
        save_to_path function tests
        """
        parser = ArgParser(["-l", "./tests.yaml"])
        with self.assertRaises(Exception):
            parser.save_to_path("./test_directory/")

        with self.assertRaises(FileExistsError):
            parser.save_to_path("./tests.svg")

        with self.assertRaises(TypeError):
            parser.save_to_path("./tests.yaml")

        self.assertEqual(f"./{self.test_directory_path}test2.svg",
                         parser.save_to_path(f"{self.test_directory_path}test2.svg"))

        # first file in testdirectory
        self.assertEqual(f"./{self.test_directory_path}", parser.save_to_path(f"{self.test_directory_path}"))

        from datetime import date
        date_today = "{:%Y%m%d}".format(date.today())
        file_name = f"{date_today}_NIV_Diagram"

        # second file -> -1
        self.assertEqual("./testdirectory/",
                         parser.save_to_path(f"./{self.test_directory_path}"))
        # third file -> -2
        # create file and give directory_list the array of created files
        # the new file should be on the second position

        parser.save_to_path(f"{self.test_directory_path}")
        directory_list = os.listdir(f"{self.test_directory_path}")
        self.assertEqual(f"{file_name}-2.svg", f"{directory_list[1]}")

    def test_create_filename(self):
        """
        create_filename function tests
        """
        from datetime import date
        parser = ArgParser(["-l", "./tests.yaml"])
        date_today = "{:%Y%m%d}".format(date.today())
        file_name = f"{date_today}_NIV_Diagram.svg"

        self.assertEqual(file_name, parser.create_filename("."))

    def test_check_args_compatibility(self):
        """
        check_args_compatibility function tests
        """

        with self.assertRaises(Exception):
            ArgParser(["-g", "-i"])

        with self.assertRaises(Exception):
            ArgParser(["-r", "-l"])

        with self.assertRaises(Exception):
            ArgParser(["-g", "-s", "-l"])

        with self.assertRaises(Exception):
            ArgParser(["-r", "-s", "-l"])

        with self.assertRaises(Exception):
            ArgParser(["-d"])

        with self.assertRaises(Exception):
            ArgParser(["-i"])

        with self.assertRaises(Exception):
            ArgParser(["-s"])

        with self.assertRaises(Exception):
            ArgParser(["-d", "-i", "-s"])

        with self.assertRaises(Exception):
            ArgParser(["-d", "-i"])

        with self.assertRaises(Exception):
            ArgParser(["-d", "-s"])

        with self.assertRaises(Exception):
            ArgParser(["-i", "-s"])

        with self.assertRaises(Exception):
            ArgParser(["Test"])

        with self.assertRaises(Exception):
            ArgParser(["123"])

        self.assertTrue(["-r"])

        self.assertTrue(["-l"])

        self.assertTrue(["-s"])

        self.assertTrue(["-g"])

        self.assertTrue(["-i"])

        self.assertTrue(["-d"])

        self.assertTrue(["-d", "-r", "-i"])

        self.assertTrue(["-d", "-i", "-l"])

        self.assertTrue(["-s", "-l"])

        self.assertTrue(["-r", "-s"])

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

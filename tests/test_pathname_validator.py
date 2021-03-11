"""
Includes all tests for pathname_validator
"""
import os
from unittest import TestCase
from src import pathname_validitor as pv


class TestPathnameValidator(TestCase):
    """
    A Class for testing functions of build_diagram
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

        except OSError:
            print(f"Creation of the directory {self.test_directory_path} failed")
        else:
            print(f"Successfully created the directory {self.test_directory_path}")
            print("Successfully created tests files")

    def test_is_pathname_valid(self):
        self.assertTrue(pv.is_pathname_valid("./"))
        self.assertTrue(pv.is_pathname_valid("."))
        self.assertTrue(pv.is_pathname_valid("./test_diagram.py"))
        self.assertTrue(pv.is_pathname_valid(os.getcwd()))
        self.assertTrue(pv.is_pathname_valid("../"))
        self.assertTrue(pv.is_pathname_valid("../../../"))

        self.assertFalse(pv.is_pathname_valid(""))
        self.assertFalse(pv.is_pathname_valid("random://test/"))

    def test_is_path_exists_or_creatable(self):
        self.assertTrue(pv.is_path_exists_or_creatable("."))
        self.assertTrue(pv.is_path_exists_or_creatable("./"))
        self.assertTrue(pv.is_path_exists_or_creatable(os.getcwd()))
        self.assertTrue(pv.is_path_exists_or_creatable("../"))
        self.assertTrue(pv.is_path_exists_or_creatable("./test_diagram.py"))

    def test_is_file_not_in_directory(self):
        self.assertTrue(pv.is_file_not_in_directory("tests2.txt"))
        self.assertFalse(pv.is_file_not_in_directory("tests.txt"))
        self.assertTrue(pv.is_file_not_in_directory("Tests.txt"))

    def test_check_file_format(self):
        self.assertTrue(pv.check_file_format("nicename.svg"))
        self.assertTrue(pv.check_file_format("nicename.pdf"))
        self.assertTrue(pv.check_file_format("nicename.jpg"))
        self.assertTrue(pv.check_file_format("nicename.png"))
        self.assertTrue(pv.check_file_format("../nicename.svg"))

        self.assertFalse(pv.check_file_format("notnicename.lala"))

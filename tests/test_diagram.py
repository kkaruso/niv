"""
Includes all tests for build_diagram
"""
from unittest import TestCase
import os

from src.build_diagram.build_diagram import BuildDiagram
from src.diagrams import Diagram


class TestBuildDiagram(TestCase):
    """
    A Class for testing functions of build_diagram
    """
    test_directory_path = "testdirectory/"

    def setUp(self) -> None:
        """
        Setup test file
        """
        with open("test.svg", "w"):
            pass

    def test_create_diagram(self):
        print("ICH BIN HIER BEI : ")
        print(os.getcwd())
        print("HIER SIND DIESE FILES")
        print(os.listdir("."))

        path_to_project = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        yaml = path_to_project + '/templates/template.yaml'

        self.assertIsNotNone(BuildDiagram(yaml, "Test_Diagram.svg", 1, False))

        self.assertIsNotNone(BuildDiagram(yaml, None, 1, False))

        with self.assertRaises(FileNotFoundError):
            self.assertIsNone(BuildDiagram("../../templates/template.yaml", "Test_Diagram.svg", 1, False))

    def tearDown(self) -> None:
        """
        Remove test file
        """
        os.remove("test.svg")

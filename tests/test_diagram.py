"""
Includes all tests for build_diagram
"""
from unittest import TestCase
import os

from build_diagram import BuildDiagram
from diagrams import Diagram


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

    def test_create_nodes(self):
        """
        create_nodes tests
        """
        with Diagram("test", filename="test", outformat="svg", show=False):
            members = []
            diagram = BuildDiagram(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/tests/test_template.yaml', "", 1, False)
            diagram.create_nodes(members)

            test_members = ["cloud1", "db1", "deviceScanner1"]
            self.assertEqual(test_members, members)

    def test_create_diagram(self):
        self.assertIsNotNone(BuildDiagram("../templates/template.yaml", "Test_Diagram.svg", 1, False))

        # self.assertIsNotNone(BuildDiagram("../templates/template.yaml", None, 1, False))

        with self.assertRaises(FileNotFoundError):
            self.assertIsNone(BuildDiagram("templates/template.yaml", "Test_Diagram.svg", 1, False))

    def tearDown(self) -> None:
        """
        Remove test file
        """
        os.remove("test.svg")

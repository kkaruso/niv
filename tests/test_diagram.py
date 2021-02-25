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
            instances = []
            members = []
            diagram = BuildDiagram(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/templates/template.yaml', "")
            diagram.create_nodes(instances, members)

            test_members = ['OsaCloud', 'OsaDatabase', 'OsaDeviceScanner', 'OsaServer', 'OsaServerWeb',
                            'OsaServerTerminal']
            self.assertEqual(test_members, members)

    def test_create_connections(self):
        """
        create_connections tests
        """
        with Diagram("test", filename="test", outformat="svg", show=False):
            instance_names = []
            instances = []
            members = []
            diagram = BuildDiagram(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/templates/template.yaml', "")
            diagram.create_nodes(instances, members)
            diagram.create_connections(instances, instance_names)

            test_instance_names = ['OsaDesktopImac', 'OsaCloud', 'OsaDatabase', 'OsaDeviceScanner', 'OsaServerWeb',
                                   'OsaServerTerminal']

            self.assertEqual(test_instance_names, instance_names)

    def tearDown(self) -> None:
        """
        Remove test file
        """
        os.remove("test.svg")
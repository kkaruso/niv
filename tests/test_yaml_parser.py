"""
module to test yam_parser
"""
import os
from unittest import TestCase
import yaml

from yaml_parser import get_yaml


# TODO: DARWIN MUSS HIER PYLINT MIT 10/10 SCHAFFEN UND MAX 1 IGNORE

class Test(TestCase):
    """
    class to test the yaml_parser functions
    """

    def setUp(self) -> None:
        data = {'name': 'Silenthand Olleander', 'race': 'Human', 'traits': ['ONE_HAND', 'ONE_EYE']}
        with open('tests.yaml', 'w') as stream:
            yaml.dump(data, stream)

    def test_get_yaml(self):
        """
        function to test get_yaml
        """
        yaml_parsed = get_yaml("tests.yaml")
        data = {'name': 'Silenthand Olleander', 'race': 'Human', 'traits': ['ONE_HAND', 'ONE_EYE']}
        self.assertEqual(data, yaml_parsed)

    def tearDown(self) -> None:
        os.remove("tests.yaml")

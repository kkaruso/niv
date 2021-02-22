from unittest import TestCase
from yaml_parser import get_yaml

import yaml
import os


class Test(TestCase):
    def setUp(self) -> None:
        data = {'name': 'Silenthand Olleander', 'race': 'Human', 'traits': ['ONE_HAND', 'ONE_EYE']}
        with open('test.yaml', 'w') as stream:
            yaml.dump(data, stream)

    def test_get_yaml(self):
        yaml_parsed = get_yaml("test.yaml")
        data = {'name': 'Silenthand Olleander', 'race': 'Human', 'traits': ['ONE_HAND', 'ONE_EYE']}
        self.assertEqual(data, yaml_parsed)

    def tearDown(self) -> None:
        os.remove("test.yaml")

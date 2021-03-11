"""
Includes all tests for pathname_validator
"""
import os
from unittest import TestCase
import pathname_validitor as pv


class TestPathnameValidator(TestCase):
    """
    A Class for testing functions of build_diagram
    """

    def test_is_pathname_valid(self):
        self.assertTrue(pv.is_pathname_valid("./"))
        self.assertTrue(pv.is_pathname_valid("."))
        self.assertTrue(pv.is_pathname_valid("./test_diagram.py"))
        self.assertTrue(pv.is_pathname_valid(os.getcwd()))
        self.assertTrue(pv.is_pathname_valid("../"))
        self.assertTrue(pv.is_pathname_valid("../../../"))

        self.assertFalse(pv.is_pathname_valid(""))
        self.assertFalse(pv.is_pathname_valid("/c://hello"))

    def test_is_path_exists_or_creatable(self):
        self.assertTrue(pv.is_path_exists_or_creatable("."))
        self.assertTrue(pv.is_path_exists_or_creatable("./"))
        self.assertTrue(pv.is_path_exists_or_creatable(os.getcwd()))
        self.assertTrue(pv.is_path_exists_or_creatable("../"))
        self.assertTrue(pv.is_path_exists_or_creatable("./test_diagram.py"))

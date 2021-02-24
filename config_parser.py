"""
Parser class config.ini
"""
import os
import configparser


class ConfigParser:
    """
    A class for passing the config.ini file
    """

    def __init__(self):
        pass

    def get_config(self):
        """
        Creates an object from configparser and loads the config file "config.ini"
        :return: List of read config.ini.
        """
        config = configparser.ConfigParser()
        config.read(self.get_config_path())
        return config

    @staticmethod
    def get_config_path():
        """
        :return: absolute path of config.ini
        """
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/niv/config.ini'

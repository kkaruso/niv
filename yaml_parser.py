"""
Parses given .yaml file
"""
import yaml


# TODO: DARWIN MUSS HIER DAS IST EINE KLASSE PACKEN

def get_yaml(path):
    """
    Reads in a .yaml file from a given path

    :param path: path to the .yaml file
    :return: yaml object or Exception
    """
    with open(f"{path}", "r") as stream:
        try:
            yaml_parsed = yaml.safe_load(stream)
            print(f"parsed yaml as dict: {yaml_parsed}\n")
            return yaml_parsed
        except yaml.YAMLError as exc:
            raise Exception from exc

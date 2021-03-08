"""
Parses given .yaml file
"""
import yaml


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


def create_yaml_defaults(path):
    """
    Creates yaml_defaults.yaml at given path

    :param path: path where the .yaml file will be created
    :return: empty yaml defaults
    """
    print("No yaml_defaults.yaml found. Creating file in " + path)
    data = {'diagram': {'backgroundColor': None, 'padding': None, 'layout': None, 'connectionStyle': None,
                        'direction': None},
            'title': {'text': None, 'subText': None, 'fontSize': None, 'author': None, 'company': None, 'date': None,
                      'version': None},
            'icons': {'text': None, 'x': None, 'y': None, 'ip': None, 'port': None, 'url': None},
            'groups': {'name': None, 'url': None}, 'connections': {'text': None, 'color': None}}
    with open(path, 'w') as file:
        yaml.dump(data, file)
    return data

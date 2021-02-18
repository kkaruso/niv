"""
Yaml Parser
"""
import yaml

with open("templates/template.yaml", "r") as stream:
    try:
        print(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)
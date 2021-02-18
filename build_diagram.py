from diagrams.azure.mobile import MobileEngagement
from diagrams.oci.connectivity import CDN
from scour import scour
from diagrams import Cluster
from diagrams.aws.compute import Compute
from diagrams import Diagram
from diagrams.aws.database import RDS
import yaml_parser

# Get the parsed yaml in form of a dictionary
yaml = yaml_parser.get_yaml("templates/template.yaml")

print(yaml.get("groups"))

# Create variables for dynamically getting the values from the .yaml file for creating the graph
title = yaml.get("title").get("text")
group_count = len(yaml.get("groups"))
groups = list(yaml.get("groups").keys())
group_members = yaml.get("groups").get("pcs").get("members")
node_count = len(yaml.get("icons"))
nodes = list(yaml.get("icons").keys())
connections = []
for i in range(0, len(yaml.get("connections"))):
    connections.append(yaml.get("connections")[i].get("endpoints"))

print(f"groups: {groups}")
print(f"group_members: {group_members}")
print(f"nodes: {nodes}")
print(f"connections: {connections}")

output_format = "svg"

filename = "Test_Diagram"

full_filename = f"{filename}.{output_format}"

# IP Example
ip = "192.168.x.x"

# Create a instance of the Diagram class to create a diagram context
with Diagram(f"{title}", filename=filename, outformat=output_format, show=False):
    # Group 1
    with Cluster("Gruppe 1"):
        # The Mater Device in the Group
        master1 = CDN("Switch")
        # internal connections
        master1 << [MobileEngagement("Device 1\n" + ip), Compute("Device 2\n" + ip)]

    # Group 2
    with Cluster("Gruppe 2"):
        master2 = CDN("Switch")
        master2 << [MobileEngagement("Device 1\n" + ip), Compute("Device 2\n" + ip)]

    # Group 3
    with Cluster("Gruppe 3"):
        master3 = CDN("Switch")
        master3 << [MobileEngagement("Device 1\n" + ip), RDS("Device 2\n" + ip)]

    # External Connections between the Groups can be: From >> To, To << From or Point - Point
    master2 >> master1 << master3

# Fix SVG-Icons Bug (source: https://github.com/mingrammer/diagrams/issues/8)
with open(full_filename, "r") as f:
    in_string = f.read()
    out_string = scour.scourString(in_string)

with open(full_filename, "w") as f:
    f.write(out_string)

# def set_variables():

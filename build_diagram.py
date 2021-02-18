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

print(yaml.get("title").get("text"))
title = yaml.get("title").get("text")

output_format = "svg"

filename = "Test_Diagram"

full_filename = f"{filename}.{output_format}"

graph_attr = {
    "layout": "dot",
}

# IP Example
ip = "192.168.x.x"

# Create a instance of the Diagram class to create a diagram context
with Diagram(f"{title}", filename=filename, outformat=output_format, show=True, graph_attr=graph_attr):
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

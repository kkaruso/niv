from scour import scour
import yaml_parser
from diagrams import *
from diagrams.icons.opensecur import *


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

graph_attr = {
    "layout": "fdp",
    "area": "1",
    "center": "true",
    "comment": "blabla",
    "compound": "false",
    "style": "invis"
}

clus_attr = {
    "penwidth": "4.0"
}

# Create a instance of the Diagram class to create a diagram context
with Diagram(f"\n{title}", filename=filename, outformat=output_format, show=True, graph_attr=graph_attr):
    # Group 1
    with Cluster("Gruppe 1"):
        # The Mater Device in the Group
        master1 = OsaDeviceWirelessRouter("Router" + ip)
        # internal connections
        master1 - OsaHub("Switch") - [OsaDesktop("PC \n" + ip), OsaPrinter("Printer\n" + ip),
                                      OsaIphone("Iphone\n" + ip), OsaDeviceScanner("Scanenr\n" + ip),
                                      OsaServer("Server\n" + ip) - OsaServer("Server")]

    # Group 2
    with Cluster("Gruppe 2", graph_attr=clus_attr):
        master2 = OsaDeviceWirelessRouter("Router" + ip)
        master2 - OsaHub("Switch") - [OsaDesktop("PC \n" + ip), OsaPrinter("Printer\n" + ip),
                                      OsaIphone("Iphone\n" + ip), OsaDeviceScanner("Scanenr\n" + ip),
                                      OsaServer("Server\n" + ip)]

    # Group 3
    with Cluster("Gruppe 3"):
        hub1 = OsaHub("Switch", shape="plantext", pin="True")
        hub2 = OsaHub("Switch", pin="True", pos="2")
        master3 = OsaDeviceWirelessRouter("Router" + ip)
        master3 - [hub1, hub2]
        hub1 - [OsaPrinter("Printer" + ip), OsaDeviceScanner("Scanenr" + ip)]
        hub2 - [OsaIphone("Iphone" + ip), OsaDesktop("Desktop" + ip)]

    # External Connections between the Groups can be: From >> To, To << From or Point - Point
    master2 - master1 - master3

# Fix SVG-Icons Bug (source: https://github.com/mingrammer/diagrams/issues/8)
with open(full_filename, "r") as f:
    in_string = f.read()
    out_string = scour.scourString(in_string)

with open(full_filename, "w") as f:
    f.write(out_string)

# def set_variables():

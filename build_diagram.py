# pylint: disable=unused-wildcard-import, method-hidden
# pylint: disable=unused-import
# pylint: disable=wildcard-import
"""
build_diagram.py
Dynamically creates the diagram
"""
from scour import scour
import yaml_parser
from diagrams import *
from diagrams.icons.osa import *
from diagrams.icons.cisco import *

# Get the parsed yaml in form of a dictionary
yaml = yaml_parser.get_yaml("templates/template.yaml")

# Create variables for dynamically getting the values from the .yaml file for creating the graph
title = yaml.get("title").get("text")
group_count = len(yaml.get("groups"))
groups = list(yaml.get("groups").keys())
group_members = {}
for member in yaml.get("groups").keys():
    # Creates new key value pairs in group_members dict for each group with its members
    group_members[f'{member}'] = yaml.get('groups')[member].get('members')
node_count = len(yaml.get("icons"))
nodes = list(yaml.get("icons").keys())
connections = []
for i in range(0, len(yaml.get("connections"))):
    connections.append(yaml.get("connections")[i].get("endpoints"))

print("Created variables from .yaml:")
print(f"title: {title}")
print(f"group_count: {group_count}")
print(f"groups: {groups}")
print(f"group_members: {group_members}")
print(f"node_count: {node_count}")
print(f"nodes: {nodes}")
print(f"connections: {connections}\n")

output_format = "svg"

filename = "Test_Diagram"

full_filename = f"{filename}.{output_format}"

# IP Example
ip = "192.168.x.x"

link = f"\n<a xlink:href=\"Test_Diagram.svg\"> {ip} </a>"

# Create an instance of the Diagram class to create a diagram context
with Diagram(f"\n{title}", filename=filename, outformat=output_format, show=True):
    instances = []
    nodes_not_in_groups = []
    members = []

    # Dynamically create the amount of nodes that are not a member of a group
    print(f"group_members: {group_members}")
    print(f"nodes: {nodes}")

    # Fill "members" list with all the group members
    for group_name in group_members:
        for member in list(group_members.get(group_name)):
            print(f"member: {member}")
            members.append(member)

    # If a node is not a member of a group, create it outside of a cluster
    for node in nodes:
        if node not in members:
            nodes_not_in_groups.append(node)
            instances.append(globals()[node](f"{node}" + link))
    # print(f"nodes_not_in_groups: {nodes_not_in_groups}\n")

    # Dynamically create the amount of groups given by "group_count" with the corresponding group name
    for group_name in group_members:
        print(f"group_name: {group_name}")
        with Cluster(f"{group_name}"):
            # Create a node for each member in every group
            for member in list(group_members.get(group_name)):
                print(f"member: {member}")
                # Create an instance of the node class with the "member" name, if not valid print name of not valid node
                try:
                    instances.append(globals()[member](f"{member}" + link))
                except KeyError:
                    print(f"KeyError: {member} is not a valid node name!")

    # Get the names of the instances as strings to create the connections
    instance_names = []
    for i, instance in enumerate(instances):
        instance_name = str(instance).split('.')[-1].split('>')[0]
        instance_names.append(instance_name)

    # print(f"\ninstances: {instances}")
    # print(f"connections: {connections}")
    # print(f"instance_name: {instance_names}")

    # Create connections
    for j in range(len(instance_names)):
        for n in range(len(connections)):
            if instance_names[j] == connections[n][0]:
                for k in range(len(instance_names)):
                    if connections[n][1] == instance_names[k]:
                        instances[k] - instances[j]


    # # Group 1
    # with Cluster("Gruppe 1"):
    #     # The Mater Device in the Group
    #     master1 = OsaDeviceWirelessRouter("Router" + ip)
    #     # internal connections
    #     master1 - OsaHub("Switch") - [OsaDesktop("PC \n" + ip), OsaPrinter("Printer\n" + ip),
    #                                   OsaIphone("Iphone\n" + ip), OsaDeviceScanner("Scanner\n" + ip),
    #                                   OsaServer("Server\n" + ip) - OsaServer("Server")]
    #
    # # Group 2
    # with Cluster("Gruppe 2", graph_attr=clus_attr):
    #     master2 = OsaDeviceWirelessRouter("Router" + ip)
    #     master2 - OsaHub("Switch") - [OsaDesktop("PC \n" + ip), OsaPrinter("Printer\n" + ip),
    #                                   OsaIphone("Iphone\n" + ip), OsaDeviceScanner("Scanenr\n" + ip),
    #                                   OsaServer("Server\n" + ip)]
    #
    # # Group 3
    # with Cluster("Gruppe 3"):
    #     hub1 = OsaHub("Switch", shape="plantext", pin="True")
    #     hub2 = OsaHub("Switch", pin="True", pos="2")
    #     master3 = OsaDeviceWirelessRouter("Router" + ip)
    #     master3 - [hub1, hub2]
    #     hub1 - [OsaPrinter("Printer" + ip), OsaDeviceScanner("Scanenr" + ip)]
    #     hub2 - [OsaIphone("Iphone" + ip), OsaDesktop("Desktop" + ip)]
    #
    # # External Connections between the Groups can be: From >> To, To << From or Point - Point
    # master2 - master1 - master3

# Fix SVG-Icons Bug (source: https://github.com/mingrammer/diagrams/issues/8)
with open(full_filename, "r") as f:
    in_string = f.read()
    out_string = scour.scourString(in_string)

with open(full_filename, "w") as f:
    f.write(out_string)

fin = open(f"{filename}.{output_format}", "rt")
data = fin.read()
data = data.replace('&lt;', '<').replace('&gt;', '>')
fin.close()
fin = open(f"{filename}.{output_format}", "wt")
fin.write(data)
fin.close()
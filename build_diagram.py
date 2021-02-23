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


class BuildDiagram:
    """
    Handles creation of diagram
    """
    OUTPUT_FORMAT = "svg"

    FILENAME = "Test_Diagram"

    full_filename = f"{FILENAME}.{OUTPUT_FORMAT}"

    # IP Example
    IP = "192.168.x.x"

    link = f"\n<a xlink:href=\"Test_Diagram.svg\"> {IP} </a>"

    def __init__(self, load_path, save_path):
        self.yaml = yaml_parser.get_yaml(load_path)
        # TODO: Implement save_path somehow and cleanup

        # Create variables for dynamically getting the values from the .yaml file for creating the graph
        self.title = self.yaml.get("title").get("text")
        self.group_count = len(self.yaml.get("groups"))
        self.groups = list(self.yaml.get("groups").keys())
        self.group_members = {}
        for member in self.yaml.get("groups").keys():
            # Creates new key value pairs in group_members dict for each group with its members
            self.group_members[f'{member}'] = self.yaml.get('groups')[member].get('members')
        self.node_count = len(self.yaml.get("icons"))
        self.nodes = list(self.yaml.get("icons").keys())
        self.connections = []
        for i in range(0, len(self.yaml.get("connections"))):
            self.connections.append(self.yaml.get("connections")[i].get("endpoints"))

        print("Created variables from .yaml:")
        print(f"title: {self.title}")
        print(f"group_count: {self.group_count}")
        print(f"groups: {self.groups}")
        print(f"group_members: {self.group_members}")
        print(f"node_count: {self.node_count}")
        print(f"nodes: {self.nodes}")
        print(f"connections: {self.connections}\n")

    def create_diagram(self):
        """
        Builds the diagram
        """

        # Create an instance of the Diagram class to create a diagram context
        with Diagram(f"\n{self.title}", filename=self.FILENAME, outformat=self.OUTPUT_FORMAT, show=True):
            instances = []
            nodes_not_in_groups = []
            members = []

            # Dynamically create the amount of nodes that are not a member of a group
            print(f"group_members: {self.group_members}")
            print(f"nodes: {self.nodes}")

            # Fill "members" list with all the group members
            for group_name in self.group_members:
                for member in list(self.group_members.get(group_name)):
                    print(f"member: {member}")
                    members.append(member)

            # If a node is not a member of a group, create it outside of a cluster
            for node in self.nodes:
                if node not in members:
                    nodes_not_in_groups.append(node)
                    instances.append(globals()[node](f"{node}" + self.link))
            # print(f"nodes_not_in_groups: {nodes_not_in_groups}\n")

            # Dynamically create the amount of groups given by "group_count" with the corresponding group name
            for group_name in self.group_members:
                print(f"group_name: {group_name}")
                with Cluster(f"{group_name}"):
                    # Create a node for each member in every group
                    for member in list(self.group_members.get(group_name)):
                        print(f"member: {member}")
                        # Create an instance of the node class with the "member" name, if not valid print name of not
                        # valid node
                        try:
                            instances.append(globals()[member](f"{member}" + self.link))
                        except KeyError:
                            print(f"KeyError: {member} is not a valid node name!")

            # Get the names of the instances as strings to create the connections
            instance_names = []
            for instance in instances:
                instance_name = str(instance).split('.')[-1].split('>')[0]
                instance_names.append(instance_name)

            # print(f"\ninstances: {instances}")
            # print(f"connections: {connections}")
            # print(f"instance_name: {instance_names}")

            # Create connections
            for j, _ in enumerate(instance_names):
                for k, _ in enumerate(self.connections):
                    if instance_names[j] == self.connections[k][0]:
                        for l, _ in enumerate(instance_names):
                            if self.connections[k][1] == instance_names[l]:
                                _ = instances[l] - instances[j]

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
        with open(self.full_filename, "r") as file:
            in_string = file.read()
            out_string = scour.scourString(in_string)

        with open(self.full_filename, "w") as file:
            file.write(out_string)

        self.html_to_ascii()

    def html_to_ascii(self):
        """
        Replace html-entity with ascii-symbol
        :return:
        """
        fin = open(f"{self.FILENAME}.{self.OUTPUT_FORMAT}", "rt")
        data = fin.read()
        data = data.replace('&lt;', '<').replace('&gt;', '>')
        fin.close()
        fin = open(f"{self.FILENAME}.{self.OUTPUT_FORMAT}", "wt")
        fin.write(data)
        fin.close()

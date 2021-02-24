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
from config_parser import ConfigParser


class BuildDiagram:
    """
    Handles creation of diagram
    """
    # OUTPUT_FORMAT = "svg"

    # FILENAME = "Test_Diagram"

    # full_filename = f"{FILENAME}.{OUTPUT_FORMAT}"

    # IP Example
    IP = "192.168.x.x"

    config_parsers = ConfigParser()
    config = config_parsers.get_config()

    # TODO: Check if icon names are valid by somehow comparing them to the classes in osa.py and cisco.py or to the
    #   icon catalog

    def __init__(self, load_path, save_path):
        # Initialize variables for dynamically getting the values from the .yaml file
        # TODO: cleanup (delete not needed comments like old prints)

        # Load the .yaml from the given path
        self.yaml = yaml_parser.get_yaml(load_path)

        self.save_path = save_path
        self.output_format = save_path.split('.')[-1]
        self.filename = os.path.splitext(save_path)[0]

        self.link = f"\n<a xlink:href=\"{self.save_path}\"> {self.IP} </a>"

        # Get title of the diagram, the amount of groups and the groups itself
        self.title = self.yaml.get("title").get("text")
        self.group_count = len(self.yaml.get("groups"))
        self.groups = list(self.yaml.get("groups").keys())

        # Go through each group and take the group name as the key and save the list of members as values in
        # "group_members" dictionary
        self.group_members = {}
        for member in self.yaml.get("groups").keys():
            self.group_members[f'{member}'] = self.yaml.get('groups')[member].get('members')

        # Get nodes and the amount of nodes
        self.node_count = len(self.yaml.get("icons"))
        self.nodes = list(self.yaml.get("icons").keys())

        # Go through each node and save the text in "nodes_text" dictionary with the node name as the key
        self.nodes_text = {}
        for node in self.yaml.get("icons"):
            self.nodes_text[f'{node}'] = self.yaml.get("icons").get(f'{node}').get('text')

        # Save each endpoint of a connection as a list in "connections" list
        self.connections = []
        for i in range(0, len(self.yaml.get("connections"))):
            self.connections.append(self.yaml.get("connections")[i].get("endpoints"))

        # Just for "debugging"
        # TODO: delete when finished with the file
        print(f"output_format: {self.output_format}")
        print(f"save_path: {self.save_path}")
        print(f"filename: {self.filename}\n")

        print("Created variables from .yaml:")
        print(f"title: {self.title}")
        print(f"group_count: {self.group_count}")
        print(f"groups: {self.groups}")
        print(f"group_members: {self.group_members}")
        print(f"node_count: {self.node_count}")
        print(f"nodes: {self.nodes}")
        print(f"nodes_text: {self.nodes_text}")
        print(f"connections: {self.connections}\n")

    def create_diagram(self):
        """
        Creates the diagram with the right amount of of nodes, clusters and connections
        """

        # Create an instance of the Diagram class to create a diagram context
        with Diagram(f"\n{self.title}", filename=self.filename, outformat=self.output_format,
                     show=self.config["DEFAULT"]["open_in_browser"] == "True"):
            instances = []
            nodes_not_in_groups = []
            members = []

            print(f"group_members: {self.group_members}")
            print(f"nodes: {self.nodes}")

            # Fill "members" list with all the group members
            for group_name in self.group_members:
                for member in list(self.group_members.get(group_name)):
                    # print(f"member: {member}")
                    members.append(member)

            # If a node is not a member of a group, create it outside of a cluster
            for node in self.nodes:
                if node not in members:
                    nodes_not_in_groups.append(node)
                    instances.append(globals()[node](f"{self.nodes_text[node]}" + self.link))

            # Dynamically create the amount of groups given by "group_count" with the corresponding group name
            for group_name in self.group_members:
                # print(f"group_name: {group_name}")
                with Cluster(f"{group_name}"):
                    # Create a node for each member in every group
                    for member in list(self.group_members.get(group_name)):
                        # print(f"member: {member}")
                        # Create an instance of the node class with the "member" name, if not valid print name of not
                        # valid node
                        try:
                            instances.append(globals()[member](f"{self.nodes_text[member]}" + self.link))
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
        with open(self.save_path, "r") as file:
            in_string = file.read()
            out_string = scour.scourString(in_string)

        with open(self.save_path, "w") as file:
            file.write(out_string)

        # TODO: Add logic to only embed links in .svg (and maybe .pdf if it's possible)
        # Only add link to diagram if it's a .svg
        # if self.output_format == "svg":
        self.html_to_ascii()

    def html_to_ascii(self):
        """
        Replace html-entity with ascii-symbol for embedding hyperlinks in svg
        """
        fin = open(f"{self.save_path}", "rt")
        data = fin.read()
        data = data.replace('&lt;', '<').replace('&gt;', '>')
        fin.close()
        fin = open(f"{self.save_path}", "wt")
        fin.write(data)
        fin.close()

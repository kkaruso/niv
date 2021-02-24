# pylint: disable=unused-wildcard-import, method-hidden
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=fixme
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

        # Get title of the diagram
        self.title = self.yaml.get("title").get("text")

        # Get name and members of groups and save as key value pairs in "group_members"
        self.group_members = {}
        for member in self.yaml.get("groups").keys():
            self.group_members[f'{member}'] = self.yaml.get('groups')[member].get('members')

        # Get name and text of nodes and save as key value pairs in "nodes_text"
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
        print(f"group_members: {self.group_members}")
        print(f"nodes_text: {self.nodes_text}")
        print(f"connections: {self.connections}\n")

    def set_instances(self, instances, members):
        # If a node is not a member of a group, create it outside of a cluster
        for node in self.nodes_text:
            if node not in members:
                instances.append(globals()[node](f"{self.nodes_text[node]}" + self.link))

        # Dynamically create the amount of groups given by "group_count" with the corresponding group name
        for group_name in self.group_members:
            with Cluster(f"{group_name}"):
                # Create a node for each member in every group
                for member in list(self.group_members.get(group_name)):
                    # Create an instance of the node class with the "member" name, if not valid print name of not
                    # valid node
                    try:
                        instances.append(globals()[member](f"{self.nodes_text[member]}" + self.link))
                    except KeyError:
                        print(f"KeyError: {member} is not given within 'icons', that's why it does not show in "
                              f"the diagram")

    def set_members(self, members):
        for group_name in self.group_members:
            for member in list(self.group_members.get(group_name)):
                members.append(member)

    def create_diagram(self):
        """
        Creates the diagram with the right amount of of nodes, clusters and connections
        """

        # Create an instance of the Diagram class to create a diagram context
        with Diagram(f"\n{self.title}", filename=self.filename, outformat=self.output_format,
                     show=self.config["DEFAULT"]["open_in_browser"] == "True"):
            instances = []
            members = []
            instance_names = []

            self.set_members(members)
            self.set_instances(instances, members)

            # Get the names of the instances as strings to create the connections
            for instance in instances:
                instance_name = str(instance).split('.')[-1].split('>')[0]
                instance_names.append(instance_name)

            # Create connections
            for j, _ in enumerate(instance_names):
                for k, _ in enumerate(self.connections):
                    if instance_names[j] == self.connections[k][0]:
                        for m, _ in enumerate(instance_names):
                            if self.connections[k][1] == instance_names[m]:
                                _ = instances[m] - instances[j]

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

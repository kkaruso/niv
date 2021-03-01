# pylint: disable=unused-wildcard-import, method-hidden
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=fixme
# pylint: disable=too-many-instance-attributes
"""
build_diagram.py
Dynamically creates the diagram
"""
import yaml_parser
from diagrams import *
from diagrams.icons.ciscoPng import *
from diagrams.icons.osa import *
from diagrams.icons.cisco import *
from diagrams.icons.osaPng import *
from config_parser import ConfigParser


class BuildDiagram:
    """
    Handles creation of diagram
    """

    # IP Example
    IP = "192.168.x.x"

    config_parsers = ConfigParser()
    config = config_parsers.get_config()

    # TODO: Add coordinates in icons and groups and integrate into create_diagram function
    # TODO: Add options for different layouts and to change graph_attr in .yaml
    def __init__(self, load_path, save_path):
        # Initialize variables for dynamically getting the values from the .yaml file
        # TODO: cleanup (delete not needed comments like old prints)
        # Load the .yaml from the given path
        self.yaml = yaml_parser.get_yaml(load_path)
        self.save_path = save_path
        self.load_path = load_path
        self.output_format = save_path.split('.')[-1]
        self.filename = os.path.splitext(save_path)[0]

        # TODO: Add checks if value not given
        # Load diagram properties
        self.graph_bg_color = self.yaml.get("diagram").get("backgroundColor")
        self.graph_padding = self.yaml.get("diagram").get("padding")
        self.graph_layout = self.yaml.get("diagram").get("layout")

        # Load title properties
        self.title_text = self.yaml.get("title").get("text")
        self.title_subtext = self.yaml.get("title").get("subText")
        self.title_font_size = self.yaml.get("title").get("fontSize")

        # TODO: Only add link when output_format is svg
        if self.output_format == "svg":
            self.link = f"\n<a xlink:href=\"{self.filename}.svg\"> {self.IP} </a>"
        else:
            self.link = ""

        # Only get coordinates if layout = neato
        if self.graph_layout == "neato":
            # Get X coordinate of each node
            self.nodes_x = {}
            for node in self.yaml.get("icons"):
                self.nodes_x[f'{node}'] = self.yaml.get("icons").get(f'{node}').get('x')

            # Get Y coordinate of each node
            self.nodes_y = {}
            for node in self.yaml.get("icons"):
                self.nodes_y[f'{node}'] = self.yaml.get("icons").get(f'{node}').get('y')

            print(f"Xs: {self.nodes_x}\n")
            print(f"Ys: {self.nodes_y}\n")

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

        # Get the URL of each group, clear empty URLs
        self.group_url = {}
        for url in self.yaml.get("groups").keys():
            self.group_url[f'{url}'] = self.yaml.get('groups')[url].get('url')
            if self.yaml.get('groups')[url].get('url') is None:
                self.group_url[f'{url}'] = ""

        self.instances = []

        # Just for "debugging"
        # TODO: delete when finished with the file
        print(f"graph_bg_color: {self.graph_bg_color}")
        print(f"graph_padding: {self.graph_padding}")
        print(f"graph_layout: {self.graph_layout}\n")

        print(f"title_text: {self.title_text}")
        print(f"title_subtext: {self.title_subtext}")
        print(f"title_font_size: {self.title_font_size}\n")

        print(f"output_format: {self.output_format}")
        print(f"save_path: {self.save_path}")
        print(f"filename: {self.filename}\n")

        print(f"group_members: {self.group_members}")
        print(f"nodes_text: {self.nodes_text}")
        print(f"connections: {self.connections}")
        print(f"group_url: {self.group_url}\n")

    def create_nodes(self, instances, members):
        """
        Create nodes outside and inside of clusters
        """
        # Fill "members" list with all the group members
        for group_name in self.group_members:
            for member in list(self.group_members.get(group_name)):
                members.append(member)

        # If a node is not a member of a group, create it outside of a cluster
        for node in self.nodes_text:
            if node not in members:
                # self.create_single_node(self.instances, node)
                try:
                    # Only pass coordinates to node creation if layout == neato
                    if self.graph_layout == "neato":
                        instances.append(
                            globals()[node](f"{self.nodes_text[node]}" + self.link, pos=f"{self.nodes_x[node]},"
                                                                                        f"{self.nodes_y[node]}!"))
                    else:
                        instances.append(
                            globals()[node](f"{self.nodes_text[node]}" + self.link))
                except KeyError:
                    print(f"KeyError in {self.load_path}: '{node}' is not a valid icon, that's why it does not show "
                          f"in the diagram. Please refer to the icon catalog for more information about available "
                          f"icons.")

        # Dynamically create the amount of groups given by "group_count" with the corresponding group name
        for group_name in self.group_members:
            clustr_attr = {
                "fontname": "helvetica-bold",
                "URL": f"{self.group_url[group_name]}"
            }
            with Cluster(f"{group_name}", graph_attr=clustr_attr):
                # Create a node for each member in every group
                for member in list(self.group_members.get(group_name)):
                    # self.create_single_node(self.instances, member)
                    # Create an instance of the node class, if not valid print name of not valid node
                    try:
                        # Only pass coordinates to node creation if layout == neato
                        if self.graph_layout == "neato":
                            instances.append(
                                globals()[member](f"{self.nodes_text[member]}" + self.link,
                                                  pos=f"{self.nodes_x[member]},"
                                                      f"{self.nodes_y[member]}!"))
                        else:
                            instances.append(
                                globals()[member](f"{self.nodes_text[member]}" + self.link))
                    except KeyError:
                        print(
                            f"KeyError in {self.load_path}: '{member}' is not given in 'icons', that's why it does "
                            f"not show in the diagram. Add it to 'icons' or remove it as a member.")

    def create_connections(self, instances, instance_names):
        """
        Create connections between nodes
        """
        # Get the names of the instances as strings to create the connections
        for instance in instances:
            instance_name = str(instance).split('.')[-1].split('>')[0]
            instance_names.append(instance_name)

        # Check if any endpoints are not given in 'icons', if not print an error
        for connection in self.connections:
            for endpoint in connection:
                if endpoint not in self.nodes_text:
                    print(f"KeyError in {self.load_path}: '{endpoint}' is not given in 'icons', that's why it "
                          f"does not show in the diagram. Add it to 'icons' or remove it as an endpoint.")

        # Create connections
        for i, _ in enumerate(instance_names):
            for j, _ in enumerate(self.connections):
                if instance_names[i] == self.connections[j][0]:
                    for k, _ in enumerate(instance_names):
                        if self.connections[j][1] == instance_names[k]:
                            _ = instances[k] - instances[i]

    def create_diagram(self):
        """
        Creates the diagram with the right amount of of nodes, clusters and connections
        """

        graph_attr = {
            "bgcolor": f"{self.graph_bg_color}",
            "pad": f"{self.graph_padding}",
            "layout": f"{self.graph_layout}",
            "fontsize": f"{self.title_font_size}",
            "fontname": "helvetica-bold"
        }

        with Diagram(f"{self.title_text} \n {self.title_subtext}", filename=self.filename, outformat=self.output_format,
                     show=self.config["DEFAULT"]["open_in_browser"] == "True", graph_attr=graph_attr):
            members = []
            instance_names = []

            # Create nodes and clusters
            self.create_nodes(self.instances, members)
            # Create connections
            self.create_connections(self.instances, instance_names)
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
        data = data.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
        fin.close()
        fin = open(f"{self.save_path}", "wt")
        fin.write(data)
        fin.close()

    def create_single_node(self, member):
        """
        Creates a single node
        """
        try:
            # Only pass coordinates to node creation if layout == neato
            if self.graph_layout == "neato":
                self.instances.append(
                    globals()[member](f"{self.nodes_text[member]}" + self.link,
                                      pos=f"{self.nodes_x[member]}, {self.nodes_y[member]}!"))
            else:
                self.instances.append(
                    globals()[member](f"{self.nodes_text[member]}" + self.link))
        except KeyError:
            print(
                f"KeyError in {self.load_path}: '{member}' is not given in 'icons', that's why it does "
                f"not show in the diagram. Add it to 'icons' or remove it as a member.")

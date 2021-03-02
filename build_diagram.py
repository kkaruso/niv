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


class BuildDiagram:
    """
    Handles creation of diagram
    """

    config = yaml_parser.get_yaml(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/niv/config.yaml')

    # TODO: Add check if ip is a valid ip and check if url is a valid url (for ip checking:
    #  https://stackoverflow.com/questions/3462784/check-if-a-string-matches-an-ip-address-pattern-in-python)
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

        # TODO: Create function like "fill_dictionary(dict, field)" or so for the following for loops
        # Get name and text of nodes and save as key value pairs in "nodes_text"
        self.nodes_text = {}
        self.fill_icon_dictionary(self.nodes_text, "text")
        # for node in self.yaml.get("icons"):
        #     self.nodes_text[node] = self.yaml.get("icons").get(node).get('text')
        #     if self.yaml.get('icons')[node].get('text') is None:
        #         self.nodes_text[node] = ""

        # Get ip of each node
        self.nodes_ip = {}
        self.fill_icon_dictionary(self.nodes_ip, "ip")
        # for node in self.yaml.get("icons"):
        #     self.nodes_ip[node] = self.yaml.get("icons").get(node).get('ip')
        #     if self.yaml.get('icons')[node].get('ip') is None:
        #         self.nodes_ip[node] = ""

        # Get port of each node
        self.nodes_port = {}
        self.fill_icon_dictionary(self.nodes_port, "port")
        # for node in self.yaml.get("icons"):
        #     self.nodes_port[node] = self.yaml.get("icons").get(node).get('port')
        #     if self.yaml.get('icons')[node].get('port') is None:
        #         self.nodes_port[node] = ""

        # Get the URL of each node, clear empty URLs
        self.nodes_url = {}
        self.fill_icon_dictionary(self.nodes_url, "url")
        # for url in self.yaml.get("icons").keys():
        #     self.nodes_url[url] = self.yaml.get('icons')[url].get('url')
        #     if self.yaml.get('icons')[url].get('url') is None:
        #         self.nodes_url[url] = ""

        # Save each endpoint of a connection as a list in "connections" list
        self.connections = []
        for i in range(0, len(self.yaml.get("connections"))):
            self.connections.append(self.yaml.get("connections")[i].get("endpoints"))

        # Get name and members of groups and save as key value pairs in "group_members"
        self.group_members = {}
        for member in self.yaml.get("groups").keys():
            self.group_members[member] = self.yaml.get('groups')[member].get('members')

        # Get the URL of each group, clear empty URLs
        self.group_url = {}
        for url in self.yaml.get("groups").keys():
            self.group_url[url] = self.yaml.get('groups')[url].get('url')
            if self.yaml.get('groups')[url].get('url') is None:
                self.group_url[url] = ""

        # Only get coordinates from nodes if layout = neato
        if self.graph_layout == "neato":
            # Get X coordinate of each node
            self.nodes_x = {}
            for node in self.yaml.get("icons"):
                # Check if a value for x is given, if not set it to 0 to prevent crashing
                if self.yaml.get("icons").get(node).get('x') is not None:
                    self.nodes_x[node] = self.yaml.get("icons").get(node).get('x')
                else:
                    self.nodes_x[node] = 0

            # Get Y coordinate of each node
            self.nodes_y = {}
            for node in self.yaml.get("icons"):
                # Check if a value for y is given, if not set it to 0 to prevent crashing
                if self.yaml.get("icons").get(node).get('y') is not None:
                    self.nodes_y[node] = self.yaml.get("icons").get(node).get('y')
                else:
                    self.nodes_y[node] = 0

            print(f"Xs: {self.nodes_x}\n")
            print(f"Ys: {self.nodes_y}\n")

        self.instances = []

        # Just for "debugging"
        # TODO: delete when finished with the file
        print(f"output_format: {self.output_format}")
        print(f"save_path: {self.save_path}")
        print(f"filename: {self.filename}\n")

        print("Created variables from .yaml:")
        print(f"title: {self.title_text}")
        print(f"group_members: {self.group_members}")
        print(f"group_url: {self.group_url}")
        print(f"nodes_text: {self.nodes_text}")
        print(f"nodes_url: {self.nodes_url}")
        print(f"nodes_ip: {self.nodes_ip}")
        print(f"connections: {self.connections}\n")

    def create_nodes(self, members):
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
                self.create_single_node(node)

        # Dynamically create the amount of groups given by "group_count" with the corresponding group name
        for group_name in self.group_members:
            clustr_attr = {
                "fontname": "helvetica-bold",
                "margin": "20",
                "URL": f"{self.group_url[group_name]}"
            }
            with Cluster(group_name, graph_attr=clustr_attr):
                # Create a node for each member in every group
                for member in list(self.group_members.get(group_name)):
                    self.create_single_node(member)

    def create_connections(self, instance_names):
        """
        Create connections between nodes
        """
        # Get the names of the instances as strings to create the connections
        for instance in self.instances:
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
                            _ = self.instances[k] - self.instances[i]

    def create_diagram(self):
        """
        Creates the diagram with the right amount of of nodes, clusters and connections
        """

        graph_attr = {
            "bgcolor": f"{self.graph_bg_color}",
            "pad": f"{self.graph_padding}",
            "layout": f"{self.graph_layout}",
            "fontsize": f"{self.title_font_size}",
            "fontname": "helvetica-bold",
            "nodesep": "1.0",
            "ranksep": "2.0",
            "splines": "curved"
        }

        with Diagram(f"{self.title_text}\n{self.title_subtext}", filename=self.filename, outformat=self.output_format,
                     show=self.config.get('default').get('open_in_browser'), graph_attr=graph_attr):
            members = []
            instance_names = []

            # Create nodes and clusters
            self.create_nodes(members)
            # Create connections
            self.create_connections(instance_names)

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

    def create_single_node(self, node):
        """
        Create an instance of a given node class, if not valid print name of not valid node
        """
        try:
            node_text = f"{self.nodes_text[node]}\n" \
                        f"{self.nodes_ip[node]}\n" \
                        f"{self.nodes_port[node]}"
            # Remove double newlines for the case when port is given but no url
            node_text = node_text.replace("\n\n", "\n")

            # Only pass coordinates to node creation if layout == neato
            if self.graph_layout == "neato":
                # If output format is other than svg, create diagram with png icons, else with svg icons
                if self.output_format != "svg":
                    self.instances.append(
                        globals()[node + "Png"](node_text,
                                                URL=self.nodes_url[node],
                                                pos=f"{self.nodes_x[node]}, {self.nodes_y[node]}!"))
                else:
                    self.instances.append(
                        globals()[node](node_text,
                                        URL=self.nodes_url[node],
                                        pos=f"{self.nodes_x[node]}, {self.nodes_y[node]}!"))
            else:
                self.instances.append(
                    globals()[node](node_text,
                                    URL=self.nodes_url[node]))
        except KeyError:
            print(
                f"KeyError in {self.load_path}: '{node}' is not given in 'icons', that's why it does "
                f"not show in the diagram. Add it to 'icons' or remove it as a member.")

    def fill_icon_dictionary(self, _dict, _field):
        """
        Fills a given dictionary with information from a field in a .yaml

        :param _dict: the given dictionary to fill
        :param _field: to fill the dictionary with
        """
        for node in self.yaml.get("icons"):
            _dict[node] = self.yaml.get("icons").get(node).get(_field)
            if self.yaml.get('icons')[node].get(_field) is None:
                _dict[node] = ""

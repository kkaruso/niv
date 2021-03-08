# pylint: disable=unused-wildcard-import, method-hidden
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=fixme
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-statements
"""
build_diagram.py
Dynamically creates the diagram
"""
import ipaddress
from datetime import datetime
import yaml_parser
from niv_logger import NivLogger
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
    counter = 1

    # TODO: Add check if ip is a valid ip and check if url is a valid url (for ip checking:
    #  https://stackoverflow.com/questions/3462784/check-if-a-string-matches-an-ip-address-pattern-in-python)

    # TODO: Find a way to add margins between node and its text, and margin between the diagram and the title
    def __init__(self, load_path, save_path, detail_level):
        # Initialize variables for dynamically getting the values from the .yaml file
        # TODO: cleanup (delete not needed comments like old prints)
        # Load the .yaml from the given path
        self.yaml = yaml_parser.get_yaml(load_path)
        self.save_path = save_path
        self.load_path = load_path
        self.detail_level = detail_level
        self.output_format = save_path.split('.')[-1]
        self.filename = os.path.splitext(save_path)[0]

        # TODO: Add checks if value not given
        # Load diagram properties
        self.graph_bg_color = self.set_variables("diagram", "backgroundColor", "transparent")
        self.graph_padding = self.set_variables("diagram", "padding", 0.5)
        self.graph_layout = self.set_variables("diagram", "layout", "fdp")
        self.graph_splines = self.set_variables("diagram", "connectionStyle", "spline")
        self.graph_direction = self.set_variables("diagram", "direction", "LR")

        # Load title properties (others are in set_diagram_title())
        self.title_font_size = self.set_variables("title", "fontSize", 15)

        # TODO: Add placeholder icon to set as default for nodes_icon
        # Get icon of each node
        self.nodes_icon = self.fill_dictionary("nodes", "icon", "")

        # Get text of each node
        self.nodes_text = self.fill_dictionary("nodes", "text", "node")

        # Get ip of each node
        self.nodes_ip = self.fill_dictionary("nodes", "ip", "")

        # Get port of each node
        self.nodes_port = self.fill_dictionary("nodes", "port", "")

        # Get the URL of each node, clear empty URLs
        self.nodes_url = self.fill_dictionary("nodes", "url", "")

        # Get name of each group
        self.group_name = self.fill_dictionary("groups", "name", "Group")

        # Get members of each group
        self.group_members = self.fill_dictionary("groups", "members", "")

        # Get the URL of each group, clear empty URLs
        self.group_url = self.fill_dictionary("groups", "url", "")

        # Only get coordinates from nodes if layout = neato
        if self.graph_layout == "neato":
            # Get X coordinate of each node
            self.nodes_x = self.fill_dictionary("nodes", "x", 0)

            # Get Y coordinate of each node
            self.nodes_y = self.fill_dictionary("nodes", "y", 0)

            print(f"\nXs: {self.nodes_x}")
            print(f"Ys: {self.nodes_y}\n")

        # Save each endpoint of a connection as a list in "connections" list
        self.connections_endpoints = []
        for i in range(0, len(self.yaml.get("connections"))):
            self.connections_endpoints.append(self.yaml.get("connections")[i].get("endpoints"))

        # Get color of connections
        self.connections_color = self.fill_connection_dictionary("connections", "color", "#7B8894")

        # Get text of connections
        self.connections_text = self.fill_connection_dictionary("connections", "text", "")

        # Get width of connections
        self.connections_width = self.fill_connection_dictionary("connections", "width", "")

        self.instances_keys = []
        self.instances = []

        # Just for "debugging"
        # TODO: delete when finished with the file
        print(f"output_format: {self.output_format}")
        print(f"save_path: {self.save_path}")
        print(f"filename: {self.filename}")
        print(f"detail_level: {self.detail_level}\n")

        print("Created variables from .yaml:")
        print(f"graph_bg_color: {self.graph_bg_color}")
        print(f"graph_padding: {self.graph_padding}")
        print(f"graph_layout: {self.graph_layout}")
        print(f"graph_splines: {self.graph_splines}")
        print(f"graph_direction: {self.graph_direction}\n")
        print(f"title_fontsize: {self.title_font_size}\n")
        print(f"nodes_icon: {self.nodes_icon}")
        print(f"nodes_text: {self.nodes_text}")
        print(f"nodes_url: {self.nodes_url}")
        print(f"nodes_ip: {self.nodes_ip}\n")
        print(f"group_name: {self.group_name}")
        print(f"group_members: {self.group_members}")
        print(f"group_url: {self.group_url}\n")
        print(f"connections: {self.connections_endpoints}")
        print(f"connections_color: {self.connections_color}")
        print(f"connections_text: {self.connections_text}\n")

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
        for name in self.group_members:
            clustr_attr = {
                "fontname": "helvetica-bold",
                "margin": "20",
                # "URL": f"{self.group_url[name]}"
                # Connect the main diagram with the created under-diagrams with a URL-link
                "URL": f"group_diagrams/{self.filename}_{name}.{self.output_format}"

            }
            with Cluster(self.group_name[name], graph_attr=clustr_attr):
                # Create a node for each member in every group
                for member in list(self.group_members.get(name)):
                    self.create_single_node(member)

    def create_connections(self):
        """
        Create connections between nodes
        """

        # Get the names of the instances as strings to create the connections
        # for instance in self.instances:
        #     # Only get the name of the icon as a string
        #     instance_name = str(instance).split('.')[-1].split('>')[0]
        #     print(f"INSTANCE_NAMES_1:{instance_name}")
        #     if self.output_format != "svg":
        #         instance_name = str(instance).split('.')[-1].split('Png')[0]
        #         print(f"INSTANCE_NAMES_2:{instance_name}")
        # Get the key of the name of the instance in the dictionary
        # key_of_instance_name = list(self.nodes_icon.keys())[list(self.nodes_icon.values()).index(instance_name)]
        # instance_names.append(instance_name)

        # Check if any endpoints are not given in 'nodes', if not print an error
        for connection in self.connections_endpoints:
            for endpoint in connection:
                if endpoint not in self.nodes_text:
                    print(f"KeyError in {self.load_path}: '{endpoint}' is not given in 'nodes', that's why it "
                          f"does not show in the diagram. Add it to 'nodes' or remove it as an endpoint.")

        # Create connections
        for i, _ in enumerate(self.instances_keys):
            for j, _ in enumerate(self.connections_endpoints):
                if self.instances_keys[i] == self.connections_endpoints[j][0]:
                    for k, _ in enumerate(self.instances_keys):
                        if self.connections_endpoints[j][1] == self.instances_keys[k]:
                            _ = self.instances[k] - \
                                Edge(color=f"{self.connections_color[j]}",
                                     label=f"{self.connections_text[j]}",
                                     tooltip=f"{self.connections_text[j]}",
                                     labeltooltip=f"{self.connections_text[j]}",
                                     penwidth=f"{self.connections_width[j]}") - \
                                self.instances[i]

        # Clear both lists to have empty lists for every diagram creation to fix not seeing connections
        # when multiple diagrams are created
        self.instances_keys.clear()
        self.instances = []

    def run(self):
        """
        Checks detail level and call create_diagram()
        """
        if self.detail_level == 0:
            for i in range(2):
                self.create_diagram(suffix=str(i))
                self.counter += 1
        else:
            self.create_diagram()

    def create_diagram(self, suffix=""):
        """
        Creates the diagram with the right amount of nodes, clusters and connections
        """
        members = []
        graph_attr = {
            "bgcolor": f"{self.graph_bg_color}",
            "pad": f"{self.graph_padding}",
            "layout": f"{self.graph_layout}",
            "fontsize": f"{self.title_font_size}",
            "fontname": "helvetica-bold",
            "nodesep": "1.0",
            "ranksep": "2.0",
            "splines": f"{self.graph_splines}",
            "rankdir": f"{self.graph_direction}"
        }
        with Diagram(self.set_diagram_title(),
                     filename=self.filename + suffix,
                     outformat=self.output_format,
                     show=self.config.get('default').get('open_in_browser'), graph_attr=graph_attr):
            # Create nodes and clusters
            self.create_nodes(members)
            # Create connections
            self.create_connections()

        # Create a separated diagram for each group in the main diagram and save it in group_diagrams/
        for _, i in enumerate(self.yaml.get("groups")):
            with Diagram(self.set_diagram_title(),
                         filename=f"group_diagrams/{self.filename}_{i}",
                         outformat=self.output_format,
                         show=False, graph_attr=graph_attr):

                # Create the nodes of the group inside a cluster
                with Cluster(self.yaml.get("groups").get(f"{i}").get("name")):
                    for member in list(self.group_members.get(i)):
                        self.create_single_node(member)
                    # Create connections inside the group
                    self.create_connections()

    def set_diagram_title(self):
        """
        Build title for diagram from title section in .yaml

        :return: Title of diagram
        """
        _dict = {"Title": self.set_variables("title", "text", "Diagram"),
                 "Description": self.set_variables("title", "subText", ""),
                 "Author": self.set_variables("title", "author", ""),
                 "Date": self.set_variables("title", "date", datetime.today().strftime('%d.%m.%Y')),
                 "Company": self.set_variables("title", "company", ""),
                 "Version": self.set_variables("title", "version", 1.0)}
        title = ""
        for item in _dict:
            if _dict[item] != "":
                title += item + ": " + str(_dict[item]) + "\n"
        return title

    def create_single_node(self, node):
        """
        Create an instance of a given node class, if not valid print name of not valid node
        """
        try:
            # For detail level 0 check counter to create corresponding text nodes
            # Counter checks how many diagrams have been created thus far
            if self.detail_level == 0:
                if self.counter == 1:
                    node_text = f"\n{self.nodes_text[node]}\n" \
                                f" {self.nodes_ip[node]}\n"
                else:
                    node_text = f"\n{self.nodes_text[node]}\n" \
                                f" {self.nodes_ip[node]}\n" \
                                f" {self.nodes_port[node]}"
            # Detail level 1 shows text and IP's
            elif self.detail_level == 1:
                node_text = f"\n{self.nodes_text[node]}\n" \
                            f" {self.nodes_ip[node]}\n"
            # Detail level 2 shows text, IP's and Ports
            else:
                node_text = f"\n{self.nodes_text[node]}\n" \
                            f" {self.nodes_ip[node]}\n" \
                            f" {self.nodes_port[node]}"

            # Remove double newlines for the case when port is given but no url
            node_text = node_text.replace("\n\n", "\n")

            try:
                # Only pass coordinates to node creation if layout == neato
                if self.graph_layout == "neato":
                    # If output format is other than svg, create diagram with png nodes, else with svg nodes
                    if self.output_format != "svg":
                        self.instances.append(
                            globals()[self.nodes_icon[node] + "Png"](node_text,
                                                                     URL=self.nodes_url[node],
                                                                     pos=f"{self.nodes_x[node]}, {self.nodes_y[node]}!",
                                                                     tooltip=f"{self.nodes_text[node]}"))
                    else:
                        self.instances.append(
                            globals()[self.nodes_icon[node]](node_text,
                                                             URL=self.nodes_url[node],
                                                             pos=f"{self.nodes_x[node]}, {self.nodes_y[node]}!",
                                                             tooltip=f"{self.nodes_text[node]}"))
                else:
                    if self.output_format != "svg":
                        self.instances.append(
                            globals()[self.nodes_icon[node] + "Png"](node_text,
                                                                     URL=self.nodes_url[node],
                                                                     tooltip=f"{self.nodes_text[node]}"))
                    else:
                        self.instances.append(
                            globals()[self.nodes_icon[node]](node_text,
                                                             URL=self.nodes_url[node],
                                                             tooltip=f"{self.nodes_text[node]}"))
                self.instances_keys.append(node)
            except KeyError:
                print(
                    f"KeyError in {self.load_path}: '{self.nodes_icon[node]}' is not a valid icon, "
                    f"that's why it does not show in the diagram "
                    f"Please take a look at the icon catalog in resources or remove the node.")

        except KeyError:
            print(
                f"KeyError in {self.load_path}: '{node}' is not given in 'nodes', that's why it does "
                f"not show in the diagram. Add it to 'nodes' or remove it as a member.")

    def fill_connection_dictionary(self, _object: str, _subobject: str, _default: any) -> dict:
        """
        Fills a given dictionary with color or text of connection from a .yaml

        :param _object: object in the .yaml
        :param _subobject: sub-object in the .yaml
        :param _default: default value for the variable
        :return: filled dictionary
        """
        _dict = {}
        for i, connection in enumerate(self.yaml.get(_object)):
            if connection.get(_subobject) is not None:
                _dict[i] = connection.get(_subobject)
            else:
                _dict[i] = _default
        return _dict

    def fill_dictionary(self, _object: str, _subobject: str, _default: any) -> dict:
        """
        Fills a given dictionary with information from a .yaml

        :param _object: object in the .yaml
        :param _subobject: sub-object in the .yaml
        :param _default: default value for the variable
        :return: filled dictionary
        """
        _dict = {}
        for i in self.yaml.get(_object):
            _dict[i] = self.yaml.get(_object).get(i).get(_subobject)
            if self.yaml.get(_object)[i].get(_subobject) is None:
                if _object == "groups" and _subobject == "members":
                    print(f"{i}: No members given, group won\'t be shown. Add members to group or remove group! :)")
                _dict[i] = _default
            elif _subobject == "ip":
                if not self.validate_ip(_dict[i]):
                    print(f"'{_dict[i]}' does not seem to be a valid IPv4 or IPv6 address")

        return _dict

    def set_variables(self, _object: str, _subobject: str, _default: any):
        """
        Set a given variable

        :param _object: object in the .yaml
        :param _subobject: sub-object in the .yaml
        :param _default: default value for the variable
        """
        _var = None
        if self.yaml.get(_object).get(_subobject) is not None:
            _var = self.yaml.get(_object).get(_subobject)
        else:
            _var = _default
        return _var

    @staticmethod
    def validate_ip(ip_string: str) -> bool:
        """
        Check if an ip is a valid IPv4/6 address

        :param ip_string: IP to check
        :return: True if IP is valid, otherwise false
        """
        try:
            ipaddress.ip_address(ip_string)
            return True

        except ValueError as error:
            logger = NivLogger()
            logger.log_error(error)
            return False

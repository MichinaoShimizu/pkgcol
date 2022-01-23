from __future__ import print_function
import networkx as nx
from pyvis.network import Network


class DependencyGraph:
    def __init__(self):
        self.g = nx.DiGraph()

    def show(self, file_path):
        self.net.show(file_path)

    def data_setting(self, dict, filter_words):
        filter_exist = len(filter_words) > 0
        for repo_name in dict.keys():
            for package_name in dict[repo_name].keys():
                if filter_exist:
                    for word in filter_words:
                        if package_name.find(word) > 0:
                            nx.add_path(self.g, [repo_name, package_name])
                else:
                    nx.add_path(self.g, [repo_name, package_name])

    def graph_setting(self, scale_num):
        self.net = Network(directed=True, width='100%', height='100%')
        node_scale = dict(self.g.degree)
        node_scale.update((x, scale_num * y) for x, y in node_scale.items())
        nx.set_node_attributes(self.g, node_scale, 'size')
        self.net.from_nx(self.g)

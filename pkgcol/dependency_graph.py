from __future__ import print_function
import networkx as nx
from pyvis.network import Network
from logger import get_module_logger

logger = get_module_logger(__name__)


class DependencyGraph:
    def __init__(self, dict):
        self.dict = dict
        self.g = nx.DiGraph()
        self.net = Network(
            notebook=True, directed=True, layout=None,
            bgcolor='#FFFFFF', font_color='#000000',
            height='100%', width='100%',
            heading='Dependency Graph'
        )

    def show(self, file_path):
        self.net.show(file_path)
        logger.info(file_path)
        return 0

    def data_setting(self, filter_words):
        for repo_name in self.dict.keys():
            for package_name in self.dict[repo_name].keys():
                if len(filter_words) > 0:
                    for word in filter_words:
                        if package_name.find(word) > 0:
                            nx.add_path(self.g, [repo_name, package_name])
                else:
                    nx.add_path(self.g, [repo_name, package_name])

    def graph_setting(self, scale_num):
        # node_scale = dict(self.g.degree)
        # node_scale.update((x, scale_num * y) for x, y in node_scale.items())
        # nx.set_node_attributes(self.g, node_scale, 'size')
        self.net.from_nx(self.g)
        # self.net.show_buttons(True)

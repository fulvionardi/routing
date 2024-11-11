import networkx as nx

class graph:
    def __init__(self, node_n, link_p = None, radius = None):
        if radius == None:
            self.G = nx.erdos_renyi_graph(node_n, link_p)
        else:
            self.G = nx.random_geometric_graph(node_n, radius)

    def generate_graph():
        print("Generating Graph")

    def get_graph(self):
        return self.G
import queue

import networkx as nx
import RREQ

class graph:

    def __init__(self, node_n, link_p = None, radius = None):
        self.neighbours = [None] * node_n
        self.seq_numbers = [[] for i in range(node_n)]
        if radius == None:
            self.G = nx.erdos_renyi_graph(node_n, link_p)
            self.G.adjacency()
        else:
            self.G = nx.random_geometric_graph(node_n, radius)
        for n, nbrdict in self.G.adjacency():
            self.neighbours[n] = [neigb for neigb in nbrdict]

    def generate_graph():
        print("Generating Graph")

    def get_graph(self):
        return self.G

    def start_routing(self, node, dest, id):
        rreqs = RREQ.rreq(node, dest, id, 0)

        q = queue.Queue()
        for n in self.neighbours[node]:
            q.put((n, rreqs, [node]))

        while not q.empty():
            (p, rreqs, path) = q.get()
            rreqn = RREQ.rreq(rreqs.source, rreqs.dest, rreqs.id, rreqs.seq + 1)
            path.append(p)
            for n in self.neighbours[p]:
                if n == rreqs.dest:
                    path.append(n)
                    return path
                if not self.seq_numbers[n].__contains__(rreqn.id):
                    self.seq_numbers[n].append(rreqn.id)
                    q.put((n, rreqn, path))

        return []

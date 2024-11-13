import queue

import networkx as nx
import RREQ
import random
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt



class graph:

    def __init__(self, node_n, average_d = 0, rewiring_p = 0, link_p = 0, radius = 0, graph_type = 0):

        self.G = None

        self.neighborhood = {}  # Initialize the neighborhood dictionary
        self.seq_numbers = [[] for _ in range(node_n)]  # Initialize sequence numbers
        self.previous = {}  # To track visited nodes for path reconstruction

        if graph_type == 0:
            self.wsg(node_n, average_d, rewiring_p)
        elif graph_type == 1:
            self.rnd(node_n, radius)
        else: 
            self.erg(node_n, link_p)

        self.connect_graph()
        self.initialize_neighborhood()
        
        self.color_map = ["skyblue"] * self.G.number_of_nodes()
        
    def wsg(self, num_nodes, avg_degree, rewiring_prob):
        self.G = nx.watts_strogatz_graph(num_nodes, avg_degree, rewiring_prob) 
    def rnd(self, num_nodes, radius):
        self.G = nx.random_geometric_graph(num_nodes, radius)

    def erg(self, num_nodes, link_p):
        self.G = nx.erdos_renyi_graph(num_nodes, link_p)

    def connect_graph(self):
        # Check connectivity and reconnect if needed
        if not nx.is_connected(self.G):
            components = list(nx.connected_components(self.G))
            for i in range(len(components) - 1):
                u = list(components[i])[0]
                v = list(components[i + 1])[0]
                self.G.add_edge(u, v)  # Connect the components

    def initialize_neighborhood(self):
        """Populate the neighborhood dictionary for each node."""
        self.neighborhood = {node: list(self.G.neighbors(node)) for node in self.G.nodes}
        print("Neighborhood dictionary initialized:", self.neighborhood)
    
    def create_window(self):
        # Create a new Tkinter window
        window = tk.Toplevel()  # Use Toplevel to open a separate window
        window.title("Graph")
        window.geometry("800x800")
        print("Drawing Graph")

        # Create a matplotlib figure and axis
        self.fig, self.ax = plt.subplots(figsize=(7, 7))  # Corrected order
        self.canvas = FigureCanvasTkAgg(self.fig, master=window)

        self.draw_graph()

        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def draw_graph(self):
        self.ax.clear()

        # Draw the graph on the matplotlib figure
        nx.draw(self.G, ax=self.ax, with_labels=True, node_size=500, node_color=self.color_map, font_size=10, font_weight="bold")
        self.ax.set_title("Graph Visualization")

        # Refresh the canvas
        self.canvas.draw()
        
    
    def get_neighbors(self, node):
        """Return the neighbors of the specified node using the neighborhood dictionary."""
        if node in self.neighborhood:
            return self.neighborhood[node]
        else:
            print("Node out of range.")
            return []
        
    def broadcast(self, node, probability=0):
        """Broadcast to neighboring nodes based on a probability."""
        destination = []
        for neighbor in self.get_neighbors(node):
            if random.random() >= probability:
                destination.append(neighbor) 
                if neighbor not in self.previous:
                    self.previous[neighbor] = node
        return destination
    
    def get_path(self, node, dest):
        """Get the path from the starting node to the destination using the previous dictionary."""
        if dest not in self.previous:
            print("No path found from node to destination.")
            return []

        path = []
        current = dest
        while current != node:
            path.append(current)
            current = self.previous.get(current)
            if current is None:
                print("Incomplete path; the destination is unreachable from the source.")
                return []

        path.append(node)
        path.reverse()
        
        return path
    
    def set_node_colors(self, nodes, color):
        """Change color of specific nodes in the color map."""
        for node in nodes:
            if 0 <= node < len(self.color_map):  # Ensure node index is within bounds
                self.color_map[node] = color

        self.draw_graph()


    def start_routing(self, node, dest):
        """Start routing from a node to a destination using flooding."""
        broadcasted = {node}
        flooding = [node]

        while flooding:
            n = flooding.pop(0)

            if n == dest:
                print(f"Destination {dest} reached.")
                break

            for neighbor in self.broadcast(n):
                if neighbor not in broadcasted:
                    broadcasted.add(neighbor)
                    flooding.append(neighbor)

        print("Routing completed.")
        print("Broadcasted nodes:", broadcasted)
        print("Calculated Path:", self.get_path(node, dest))
import queue

import networkx as nx
import random
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time



class graph:

    def __init__(self, node_n, average_d = 0, rewiring_p = 0, link_p = 0, radius = 0, graph_type = 0, connectivity = True):

        self.G = None
        self.window_open = False
        self.neighborhood = {}  # Initialize the neighborhood dictionary
        self.seq_numbers = [[] for _ in range(node_n)]  # Initialize sequence numbers
        self.previous = {}  # To track visited nodes for path reconstruction

        if graph_type == 0:
            self.wsg(node_n, average_d, rewiring_p)
        elif graph_type == 1:
            self.rnd(node_n, radius)
        else: 
            self.erg(node_n, link_p)

        self.pos = nx.spring_layout(self.G)

        if (connectivity == True):
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
        # print("Neighborhood dictionary initialized:", self.neighborhood)
    
    def create_window(self):
        # Only create the window if it's not already open
        if self.window_open:
            return

        # Create a new Tkinter window
        window = tk.Toplevel()
        window.title("Graph")
        window.geometry("800x800")
        self.window_open = True  # Set the window_open flag to True

        def on_close():
            self.window_open = False  # Reset the flag when the window is closed
            window.destroy()

        # Bind the close event to on_close
        window.protocol("WM_DELETE_WINDOW", on_close)

        # Create a matplotlib figure and axis
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=window)

        self.draw_graph()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def draw_graph(self):
        self.ax.clear()

        # Draw the graph on the matplotlib figure
        nx.draw(self.G, pos=self.pos, ax=self.ax, with_labels=True, node_size=500, node_color=self.color_map, font_size=10, font_weight="bold")
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
        
    def broadcast(self, node, failure_p=0):
        """Broadcast to neighboring nodes based on a probability."""
        destination = []
        for neighbor in self.get_neighbors(node):
            if random.random() >= failure_p:
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
    
    def set_node_colors(self, nodes, color, nodes2 = [], color2 = "red"):
        """Change color of specific nodes in the color map."""
        for node in nodes:
            if 0 <= node < len(self.color_map):  # Ensure node index is within bounds
                self.color_map[node] = color

        for node in nodes2:
            if 0 <= node < len(self.color_map):  # Ensure node index is within bounds
                self.color_map[node] = color2

    
    def all_combination(self, times, failure_p = 0):
        self.received_packets = {node: 0 for node in self.G.nodes()}
        self.steps_for_arrival = 0
        self.succssful = 0
        self.hop_sum = 0

        i = 0

        for source in self.G.nodes():
            for dest in self.G.nodes():
                if source < dest:  # Ensures (source, dest) is unique and avoids (source, source)
                    i += 1
                    self.route_multiple(source, dest, times, failure_p, combination = True)

        total = i * times

        avg_received_packets = sum(self.received_packets.values()) / (len(self.G.nodes) * total)
        avg_steps_for_arrival = self.steps_for_arrival / total
        success_rate = self.succssful / total
        if (self.succssful != 0):
            avg_hop = self.hop_sum / self.succssful
        else:
            avg_hop = 0

        print("Average Received Packet per Node: ", avg_received_packets)
        print("Average Steps for Routing: ", avg_steps_for_arrival)
        print("Routing Success Rate: ", success_rate)
        print("Average Routing Hops", avg_hop)

        return avg_received_packets, avg_steps_for_arrival, success_rate, avg_hop



    def route_multiple(self, source, dest, times, failure_p=0, delay = 1, animated = False, combination = False):
        if not combination:
            self.received_packets = {node: 0 for node in self.G.nodes()}
            self.steps_for_arrival = 0
            self.succssful = 0
            self.hop_sum = 0


        for i in range(times):
            self.previous = {}
            if animated:
                self.start_routing_animate(source, dest, failure_p, delay)
            else:
                self.start_routing(source, dest, failure_p)


        if not (combination or animated):

            avg_received_packets = sum(self.received_packets.values()) / (len(self.G.nodes) * times)
            avg_steps_for_arrival = self.steps_for_arrival / times
            success_rate = self.succssful / times

            if (self.succssful != 0):
                avg_hop = self.hop_sum / self.succssful
            else:
                avg_hop = 0

            print("Average Received Packet per Node: ", avg_received_packets)
            print("Average Steps for Routing: ", avg_steps_for_arrival)
            print("Routing Success Rate: ", success_rate)
            print("Average Routing Hops", avg_hop)



    def start_routing(self, node, dest, failure_p=0):
        complete = False
        reached = False
        sending = False
        broadcasted = set()
        flooding = {node}
        flooded = {node}
        path = []

        while flooding or not complete:
            # Temporary set to collect new nodes to flood
            new_flooded = set()

            for n in flooding:

                if n == dest and not reached:
                    print(f"Destination {dest} reached.")
                    reached = True
                    path = self.get_path(node, dest)
                    forward = path[1:]
                    backtrack = path.copy()
                    broadcasted.add(n)

                if n not in broadcasted:
                    broadcast = self.broadcast(n, failure_p=failure_p)
                    broadcasted.add(n)
                    # Add neighbors to new_flooded instead of flooded directly
                    for neighbor in broadcast:
                        self.received_packets[neighbor] += 1
                        new_flooded.add(neighbor)


            flooded.update(new_flooded)



            if sending and not complete:
                self.steps_for_arrival += 1
                if random.random() >= failure_p:
                    self.received_packets[forward.pop(0)] += 1
                if not forward:
                    complete = True

            if reached and not sending:
                self.steps_for_arrival += 1
                if random.random() >= failure_p:
                    self.received_packets[backtrack.pop(-1)] += 1
                if not backtrack:
                    sending = True

            if not reached:
                self.steps_for_arrival += 1
                if not new_flooded:
                    break

            # Update flooding to the newly found nodes
            
            flooding = new_flooded

        if complete:
            self.hop_sum += len(path) - 1
            self.succssful += 1


        self.steps_for_arrival -= 1
        print("Routing completed.")
        # print("Broadcasted nodes:", broadcasted)
        print("Calculated Path:", self.get_path(node, dest))


    def start_routing_animate(self, node, dest, failure_p=0, delay = 1):
        if not self.window_open or (not hasattr(self, 'ax') or not hasattr(self, 'canvas')):
            self.create_window()
        self.set_node_colors(self.G.nodes(), "skyblue", nodes2=[node, dest], color2="#5E6EE6")

        complete = False
        reached = False
        sending = False
        broadcasted = set()
        flooding = {node}
        flooded = {node}
        path = []

        while flooding or not complete:
            # Temporary set to collect new nodes to flood
            new_flooded = set()

            self.set_node_colors(list(flooding), "#F5B642", nodes2=[node, dest], color2="#5E6EE6")

            for n in flooding:
                if n == dest and not reached:
                    print(f"Destination {dest} reached.")
                    reached = True
                    path = self.get_path(node, dest)
                    forward = path[1:]
                    backtrack = path.copy()
                    broadcasted.add(n)

                if n not in broadcasted:
                    broadcast = self.broadcast(n, failure_p=failure_p)
                    broadcasted.add(n)
                    # Add neighbors to new_flooded instead of flooded directly
                    for neighbor in broadcast:
                        new_flooded.add(neighbor)



            # Now update flooded after the loop completes
            flooded.update(new_flooded)

            if not reached and not new_flooded:  # No more nodes to flood and destination not reached
                print(f"Destination {dest} is not reachable.")
                break  # Exit the loop

            if reached:
                self.set_node_colors(path, "#6AAB5C", nodes2=[node, dest], color2="#5E6EE6")

            if sending and not complete:
                self.color_map[forward.pop(0)] = "#518546"
                if not forward:
                    complete = True

            if reached and not sending:
                self.color_map[backtrack.pop(-1)] = "#CF720E"
                if not backtrack:
                    sending = True


            self.canvas.flush_events()   # Process events to refresh the canvas
            self.draw_graph()

            time.sleep(delay)
            # Update flooding to the newly found nodes

            flooding = new_flooded


        print("Routing completed.")
        print("Broadcasted nodes:", broadcasted)
        print("Calculated Path:", self.get_path(node, dest))


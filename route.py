import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# Initialize the main window
root = tk.Tk()
root.title("Dynamic Network Graph with Color Changing Nodes")
root.geometry("800x800")

# Create a NetworkX graph
G = nx.Graph()
# Add some nodes and edges
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (2, 5)])

canvas = FigureCanvasTkAgg(None, master=root)

# Function to generate random "package position"
def update_package_position():
    # Generate a random position to simulate package moving
    return random.choice(list(G.nodes))

# Function to update node colors based on "package position"
def update_graph():
    # Randomly select a node for package position
    package_position = update_package_position()
    
    # Define node colors, change the color of the node with the package
    node_colors = ["blue" if node != package_position else "red" for node in G.nodes]
    
    # Draw the graph with updated colors
    plt.clf()  # Clear the plot to update
    nx.draw(G, pos, node_color=node_colors, with_labels=True, node_size=500, font_size=12)
    
    # Refresh the canvas
    canvas.draw()

# Generate the layout for positioning nodes
pos = nx.spring_layout(G)


def draw_graph(graph):
    # Draw the initial network graph
    fig, ax = plt.subplots(figsize=(6, 6))
    nx.draw(graph, pos, with_labels=True, node_size=500, font_size=12)
    canvas = FigureCanvasTkAgg(fig, master=root)  # Attach to Tkinter window
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Button to update graph colors
update_button = tk.Button(root, text="Move Package", command=update_graph)
update_button.pack()


draw_button = tk.Button(root, text="Draw Graph", command=draw_graph(G))
draw_button.pack()

# Start the GUI main loop
root.mainloop()
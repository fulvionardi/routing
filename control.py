import tkinter as tk
import random
from graph import graph
from components import slider, button, combo_box
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Function to create the control panel window
def control_panel():
    # Initialize the control panel window
    root = tk.Tk()
    root.title("Control Panel")
    root.geometry("500x500")
    
    def draw():
        my_graph = graph(node_n = numbers.get_value(), average_d = avg_degree.get_value(), rewiring_p = rewiring_probability.get_value(), 
                        radius = radius.get_value(), link_p = link_probability.get_value(), graph_type = combobox.get_selected())
        my_graph.start_routing(4, 18)
        my_graph.create_window()
        my_graph.set_node_colors([1,18], "red")

    numbers = slider("Node Number:", 0, 100, 0, 0, 0, root, default_value = 20)

    avg_degree = slider("Average Degree:", 0, 100, 1, 0, 0, root, default_value = 5)

    rewiring_probability = slider("Rewiring Probability:", 0, 1, 2, 0, 1, root, default_value = 0)

    loss_probability = slider("Packet Loss Probability:", 0, 1, 3, 0, 1, root, default_value = 0)

    link_probability = slider("Link Probability:", 0, 1, 4, 0, 1, root, default_value = 0)

    radius = slider("Radius:", 0, 1, 5, 0, 1, root, default_value = 0)

    mybutton = button("Draw Graph", draw, 6, 0, root)

    combobox = combo_box(7, 0, root)
    
    root.mainloop()

if __name__ == "__main__":
    control_panel()  

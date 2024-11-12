import tkinter as tk
import random
from graph import graph
from components import slider, button
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Function to create the control panel window
def control_panel():
    # Initialize the control panel window
    root = tk.Tk()
    root.title("Control Panel")
    root.geometry("500x500")

    def generate_graph():
        # my_graph = graph(numbers.get_value(), probability.get_value())
        my_graph = graph(numbers.get_value(), radius = radius.get_value())
        path = my_graph.start_routing(4, 18, 20)
        print(path.__sizeof__())
        return my_graph.get_graph()

    def draw_graph():
        graph = generate_graph()
        # Create a new Tkinter window
        window = tk.Toplevel()  # Use Toplevel to open a separate window
        window.title("Graph")
        window.geometry("800x800")
        print("Drawing Graph")

        # Create a matplotlib figure and axis
        fig, ax = plt.subplots(figsize=(7, 7))
        
        # Draw the graph on the matplotlib figure
        nx.draw(graph, ax=ax, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold")
        ax.set_title("Graph Visualization")

        # Embed the matplotlib figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_value():
        print(probability.get_value())


    numbers = slider("Node Number:", 0, 100, 0, 0, 0, root)

    probability = slider("Link Probability:", 0, 1, 1, 0, 2, root)

    radius = slider("Radius:", 0, 1, 2, 0, 1, root)

    mybutton = button("Draw Graph", draw_graph, 3, 0, root)
    
    root.mainloop()

if __name__ == "__main__":
    control_panel()  

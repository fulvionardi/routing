import tkinter as tk
import random
from graph import graph
from components import slider, button, combo_box, check_box
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Function to create the control panel window
def control_panel():
    # Initialize the control panel window
    root = tk.Tk()
    root.title("Control Panel")
    root.geometry("700x270")

    my_graph = None
    
    def generate_graph():
        nonlocal my_graph
        my_graph = graph(node_n = node_n.get_value(), average_d = average_d.get_value(), rewiring_p = rewiring_p.get_value(), 
                        radius = radius.get_value(), link_p = link_p.get_value(), graph_type = graph_type.get_value(),
                        connectivity = connectivity.get_value())

    def draw():
        generate_graph()
        my_graph.create_window()

    def route():
        if my_graph is None:
            generate_graph()

        my_graph.route_multiple(source.get_value(), destination.get_value(), packet_n.get_value(), failure_p = failure_p.get_value(), delay = delay.get_value(), animated = animate.get_value())

    def check_properties():
        avg_recieved_packets_arr = []
        avg_steps_for_arrival_arr = []
        success_rate_arr = []
        avg_hop_arr = []
        n = 1000
        for i in range(n):
            my_graph = graph(node_n=node_n.get_value(), average_d=average_d.get_value(),
                             rewiring_p=rewiring_p.get_value(),
                             radius=radius.get_value(), link_p=link_p.get_value(), graph_type=graph_type.get_value(),
                             connectivity=connectivity.get_value())

            generate_graph()

            avg_received_packets, avg_steps_for_arrival, success_rate, avg_hop =\
                my_graph.all_combination(packet_n.get_value(), failure_p.get_value())
            avg_recieved_packets_arr.append(avg_received_packets)
            avg_steps_for_arrival_arr.append(avg_steps_for_arrival)
            success_rate_arr.append(success_rate)
            avg_hop_arr.append(avg_hop)

        df = pd.DataFrame({'avg_received_packets': avg_recieved_packets_arr,
                           'avg_steps_for_arrival': avg_steps_for_arrival_arr,
                           'success_rate': success_rate_arr,
                           'avg_hop': avg_hop_arr})
        df.to_csv('output_nodes_{}_prob_{}_times_{}.csv'.format(node_n.get_value(), link_p.get_value(), n), index = False)
        print("Done !!")
    def on_graph_type_change(selected_index):
        if selected_index == 0:  # "Watts Strogatz"
            rewiring_p.enable()
            average_d.enable()
            radius.disable()
            link_p.disable()
        elif selected_index == 1:  # "Random Geometric"
            rewiring_p.disable()
            average_d.disable()
            radius.enable()
            link_p.disable()
        elif selected_index == 2:  # "Erdos Renyi"
            rewiring_p.disable()
            average_d.disable()
            radius.disable()
            link_p.enable()


    

    node_n = slider("Node Number:", 0, 100, 0, 0, 0, root, default_value = 20)

    average_d = slider("Average Degree:", 0, 100, 1, 0, 0, root, default_value = 5)

    rewiring_p = slider("Rewiring Probability:", 0, 1, 2, 0, 1, root, default_value = 0)

    link_p = slider("Link Probability:", 0, 1, 3, 0, 1, root, default_value = 0)

    radius = slider("Radius:", 0, 1, 4, 0, 1, root, default_value = 0)

    graph_type = combo_box(5, 0, root, callback=on_graph_type_change)

    connectivity  = check_box("Enforce Connectivity", 6, 0, root)

    draw_button = button("Draw Graph", draw, 6, 2, root)




    source = slider("Source Node:", 0, 100, 0, 4, 0, root, default_value = 0)

    destination = slider("Destination Node:", 0, 100, 1, 4, 0, root, default_value = 10)

    failure_p = slider("Packet Loss Probability:", 0, 1, 2, 4, 1, root, default_value = 0)

    packet_n = slider("Packet Number:", 0, 20, 3, 4, 0, root, default_value = 1)

    delay = slider("Delay:", 0, 4, 4, 4, 1, root, default_value = 1)

    animate  = check_box("Animate Route", 5, 4, root)     

    route_button = button("Find Route", route, 6, 5, root)

    route_combination = button("Check Properties", check_properties, 6, 6, root)


    on_graph_type_change(graph_type.get_value())
    # on_draw_graph()

    root.mainloop()

if __name__ == "__main__":
    control_panel()  

class Node:
    def __init__(self, node_id):
        """
        Initialize the Node with a unique identifier and an empty routing table.
        
        :param node_id: Unique identifier for the node (e.g., an integer or string).
        """
        self.node_id = node_id
        self.routing_table = {}  # Dictionary to represent the routing table
        # Example: {destination: {"next_hop": <node_id>, "cost": <distance>}}
        self.neighbors = {}  # To store direct neighbors and their link costs
    
    def add_neighbor(self, neighbor_id, cost):
        """
        Add or update a neighbor with the given cost.
        
        :param neighbor_id: ID of the neighboring node.
        :param cost: Cost of the link to the neighbor.
        """
        self.neighbors[neighbor_id] = cost
        # Update routing table for the direct neighbor
        self.routing_table[neighbor_id] = {"next_hop": neighbor_id, "cost": cost}
    
    def update_routing_table(self, destination, next_hop, cost):
        """
        Update the routing table with a new route.
        
        :param destination: The destination node ID.
        :param next_hop: The next hop node ID to reach the destination.
        :param cost: The cost to reach the destination via the next hop.
        """
        self.routing_table[destination] = {"next_hop": next_hop, "cost": cost}
    
    def get_route(self, destination):
        """
        Retrieve the route to a specific destination from the routing table.
        
        :param destination: The destination node ID.
        :return: A dictionary with 'next_hop' and 'cost', or None if no route exists.
        """
        return self.routing_table.get(destination)
    
    def print_routing_table(self):
        """
        Print the current routing table for debugging.
        """
        print(f"Routing Table for Node {self.node_id}:")
        for dest, info in self.routing_table.items():
            print(f"Destination: {dest}, Next Hop: {info['next_hop']}, Cost: {info['cost']}")
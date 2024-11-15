def start_routing_animate(self, node, dest, failure_p=0, animate=False):
        if animate:
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
        packet_location = 0

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

            time.sleep(1)
            # Update flooding to the newly found nodes
            flooding = new_flooded


        print("Routing completed.")
        print("Broadcasted nodes:", broadcasted)
        print("Calculated Path:", self.get_path(node, dest))
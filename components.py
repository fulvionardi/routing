import tkinter as tk
from tkinter import ttk

class slider():
    def __init__(self, label, min_val, max_val, row, column, decimals, root, default_value = 0):

        self.decimals = decimals

        self.entry_value = tk.DoubleVar()

        if decimals == 0:
            self.entry_value = tk.IntVar()

        validate_command = (root.register(self.validate_number_input), '%d', '%P')

        slider_label = tk.Label(root, text = label)
        slider_label.grid(row=row, column=column, sticky="w", padx=4, pady=5) 
        slider_entry = tk.Entry(root, textvariable = self.entry_value, validatecommand = validate_command, width=5)
        slider_entry.grid(row=row, column=column + 1, pady=5)
        slider_scale = tk.Scale(root, from_=min_val, to=max_val, orient="horizontal", resolution = (max_val - min_val) / 100, showvalue=False, variable=self.entry_value, command=self.scale_changed)
        slider_scale.grid(row=row, column=column + 2, pady=5)

        self.entry_value.set(default_value)

        self.entry_value.trace_add("write", self.entry_changed)


    # Function to update the Entry widget when the Scale is changed
    def scale_changed(self, value):
        # Update the Entry with the current Scale value
        self.entry_value.set(self.cast(value))

    # Function to update the Scale when the Entry is changed
    def entry_changed(self, *args):
        try:
            # Update the Scale with the current Entry value
            value = self.cast(self.entry_value.get())
            self.entry_value.set(value)
        except ValueError:
            pass  # Ignore non-integer input

    def validate_number_input(action, value):
        if action == "1":  # Insert action
            try:
                # Try to convert the input to a float
                float(value)
                return True  # If conversion succeeds, allow the input
            except ValueError:
                return False  # If conversion fails, reject the input
        return True  # Allow delete action
    
    def get_value(self):
        return self.entry_value.get()
    
    def cast(self, value):
        if self.decimals == 0:
            return int(value)
        else:
            return round(float(value), self.decimals)
        

class button():
    def __init__(self, text, function, row, column, root):
        button = tk.Button(root, text=text, command=function)
        button.grid(row=row, column=column, pady=5)


class combo_box():
    def __init__(self, row, column, root, label = "Graph Type"):


        self.selected = 0
        self.options = ["Watts Strogatz", "Random Geometric", "Erdos Renyi"]
        self.combo = ttk.Combobox(root, values=self.options, state="readonly")
        self.combo.set("Select an option")  # Set the default text
        self.combo.grid(row=row, column=column, padx=10, pady=10)
        self.combo.set(self.options[0])  # Set the default text


        # Bind the selection event to the callback function
        self.combo.bind("<<ComboboxSelected>>", self.on_combo_select)
    
    def on_combo_select(self, event):
        selected_value = self.combo.get()
        self.selected = self.options.index(selected_value)  # Update selected index
        print("Selected:", selected_value)

    def get_selected(self):
        return self.selected


import tkinter as tk
from tkinter import ttk

class slider:
    def __init__(self, label, min_val, max_val, row, column, decimals, root, default_value=0):
        self.decimals = decimals
        self.entry_value = tk.DoubleVar()

        if decimals == 0:
            self.entry_value = tk.IntVar()

        validate_command = (root.register(self.validate_number_input), '%d', '%P')

        # Create the Label
        self.slider_label = tk.Label(root, text=label)
        self.slider_label.grid(row=row, column=column, sticky="w", padx=4, pady=5)

        # Create the Entry
        self.slider_entry = tk.Entry(root, textvariable=self.entry_value, validate="key", validatecommand=validate_command, width=5)
        self.slider_entry.grid(row=row, column=column + 1, pady=5)

        # Create the Scale
        self.slider_scale = tk.Scale(root, from_=min_val, to=max_val, orient="horizontal",
                                     resolution=(max_val - min_val) / 100, showvalue=False,
                                     variable=self.entry_value, troughcolor="white", command=self.scale_changed)
        self.slider_scale.grid(row=row, column=column + 2, pady=5, padx=(0, 40))

        # Set the default value
        self.entry_value.set(default_value)

        # Trace changes in the Entry field
        self.entry_value.trace_add("write", self.entry_changed)

    # Function to update the Entry widget when the Scale is changed
    def scale_changed(self, value):
        self.entry_value.set(self.cast(value))

    # Function to update the Scale when the Entry is changed
    def entry_changed(self, *args):
        try:
            value = self.cast(self.entry_value.get())
            self.entry_value.set(value)
        except ValueError:
            pass  # Ignore non-numeric input

    def validate_number_input(self, action, value):
        if action == "1":  # Insert action
            try:
                float(value)  # Attempt to convert the input to a float
                return True
            except ValueError:
                return False  # Reject the input if it's not a valid float
        return True  # Allow deletion

    def get_value(self):
        return self.entry_value.get()

    def cast(self, value):
        if self.decimals == 0:
            return int(value)
        else:
            return round(float(value), self.decimals)

    # Disable the Entry and Scale widgets with visual changes
    def disable(self):
        # self.slider_entry.config(state="disabled", background="lightgray", disabledforeground="darkgray")
        self.slider_entry.config(state="disabled")
        self.slider_scale.config(state="disabled", bg="lightgray",  troughcolor="lightgray")

    # Enable the Entry and Scale widgets with normal colors
    def enable(self):
        # self.slider_entry.config(state="normal", background="white", disabledforeground="black")
        self.slider_entry.config(state="normal")
        self.slider_scale.config(state="normal", bg="SystemButtonFace", troughcolor="white")

class button():
    def __init__(self, text, function, row, column, root):
        self.button = tk.Button(root, text=text, command=function)
        self.button.grid(row=row, column=column, pady=5)

    def disable(self):
        self.button.config(state="disabled")

    def enable(self):
        self.button.config(state="normal")

class check_box():
    def __init__(self, text, row, column, root, default_value = 1):

        self.checkbox_var = tk.IntVar(value=default_value)

        self.check_box = tk.Checkbutton(root, text=text, variable=self.checkbox_var)
        self.check_box.grid(row=row, column=column, pady=5)

    def get_value(self):
        return self.checkbox_var.get()
    
    def disable(self):
        self.check_box.config(state="disabled")

    def enable(self):
        self.check_box.config(state="normal")

class combo_box_graph():
    def __init__(self, row, column, root, label="Graph Type", callback=None):
        self.selected = 0
        self.options = ["Watts Strogatz", "Random Geometric", "Erdos Renyi"]
        self.combo = ttk.Combobox(root, values=self.options, state="readonly")
        self.combo.set("Select an option")  # Set the default text
        self.combo.grid(row=row, column=column, padx=10, pady=10)
        self.combo.set(self.options[0])  # Set the initial default text

        self.callback = callback  # Store the callback function

        # Bind the selection event to the callback function
        self.combo.bind("<<ComboboxSelected>>", self.on_combo_select)
    
    def on_combo_select(self, event):
        selected_value = self.combo.get()
        self.selected = self.options.index(selected_value)  # Update selected index
        print("Selected:", selected_value)
        if self.callback:
            self.callback(self.selected)  # Call the callback with the selected index

    def get_value(self):
        return self.selected
    
class combo_box_route():
    def __init__(self, row, column, root, label="Route Type", callback=None):
        self.selected = 0
        self.options = ["Reactive", "Proactive"]
        self.combo = ttk.Combobox(root, values=self.options, state="readonly")
        self.combo.set("Select an option")  # Set the default text
        self.combo.grid(row=row, column=column, padx=10, pady=10)
        self.combo.set(self.options[0])  # Set the initial default text

        self.callback = callback  # Store the callback function

        # Bind the selection event to the callback function
        self.combo.bind("<<ComboboxSelected>>", self.on_combo_select)
    
    def on_combo_select(self, event):
        selected_value = self.combo.get()
        self.selected = self.options.index(selected_value)  # Update selected index
        print("Selected:", selected_value)
        if self.callback:
            self.callback(self.selected)  # Call the callback with the selected index

    def get_value(self):
        return self.selected


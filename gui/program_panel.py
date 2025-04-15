import tkinter as tk
from tkinter import ttk


class ProgramPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = tk.Label(self, text="Program", font=("Arial", 14, "bold"))
        self.label.pack(anchor="n")

        self.listbox = tk.Listbox(self, font=("Courier", 14), width=20, height=30)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update_program(self, instructions: list[str]):
        """Update the program listing shown."""
        self.listbox.delete(0, tk.END)
        for index, line in enumerate(instructions):
            self.listbox.insert(tk.END, f"{index:03}: {line}")

    def highlight_line(self, line_number: int, color="red"):
        """Highlight the currently executing line."""
        self.clear_highlight()
        if 0 <= line_number < self.listbox.size():
            self.listbox.itemconfig(line_number, {'bg': color, 'fg': 'white'})
            self.listbox.see(line_number)

    def clear_highlight(self):
        """Remove all highlighting."""
        for i in range(self.listbox.size()):
            self.listbox.itemconfig(i, {'bg': 'white', 'fg': 'black'})

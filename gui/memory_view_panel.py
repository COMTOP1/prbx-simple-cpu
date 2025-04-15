import math
import tkinter as tk
from tkinter import ttk


class MemoryView(tk.Frame):
    memory_size: int

    def __init__(self, master, memory_size=256, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        mem_label = tk.Label(master, text="Memory", font=("Arial", 12, "bold"))
        mem_label.pack(pady=(10, 5))

        self.memory_size = memory_size
        self.memory = [0] * memory_size

        # Treeview setup
        self.tree = ttk.Treeview(self, columns=('Address', 'Value'), show='headings', height=30)
        self.tree.heading('Address', text='Address')
        self.tree.heading('Value', text='Value')
        self.tree.column('Address', width=80, anchor='center')
        self.tree.column('Value', width=80, anchor='center')

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.populate_memory()

    def build_memory_labels(self):
        for addr in range(self.memory_size):
            address_label = tk.Label(self.scrollable_frame, text=f"{addr:02X}", width=5,
                                     anchor='e', fg='lightgray', bg='black', font=('Courier', 10))
            value_label = tk.Label(self.scrollable_frame, text=f"{self.memory[addr]:02X}", width=5,
                                   anchor='w', fg='cyan', bg='black', font=('Courier', 10))

            address_label.grid(row=addr, column=0, sticky='e', padx=(5, 2))
            value_label.grid(row=addr, column=1, sticky='w', padx=(2, 5))
            self.entries.append((address_label, value_label))

    def populate_memory(self):
        for addr in range(self.memory_size):
            self.tree.insert('', 'end', iid=str(addr), values=(f"0x{addr:02X} ({addr})", f"0x{self.memory[addr]:04X}"))

    def update_memory(self, new_memory):
        """Update memory display."""
        self.memory = new_memory
        for addr, val in enumerate(new_memory):
            self.tree.item(str(addr), values=(f"0x{addr:02X} ({addr})", f"{val:04X}"))

    def update_value(self, addr, val):
        """Update memory displayed in a single location."""
        if addr < 0 or addr > self.memory_size:
            raise ValueError('Address out of range')
        if val < 0 or val >= math.pow(2, 16):
            raise ValueError('Value out of range')
        self.memory[addr] = val
        self.tree.item(str(addr), values=(f"0x{addr:02X} ({addr})", f"0x{val:04X}"))

    def highlight_address(self, addr, color='red'):
        """Highlight a specific memory address row."""
        if 0 <= addr < self.memory_size:
            self.tree.tag_configure(f"highlight_{addr}", background=color, foreground='white')
            self.tree.item(str(addr), tags=(f"highlight_{addr}",))

    def clear_highlight(self):
        for addr in range(self.memory_size):
            self.tree.item(str(addr), tags=())

    def clear_memory(self):
        for addr in range(self.memory_size):
            self.tree.item(str(addr), values=(f"0x{addr:02X} ({addr})", f"0x{0:04X}"))

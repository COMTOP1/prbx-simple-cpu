import tkinter as tk


class MicroInstructionPanel(tk.Frame):
    def __init__(self, master, instructions, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.instruction_labels = {}
        self.configure(bg="black")

        row = 0
        col = 0
        for instr in instructions:
            lbl = tk.Label(
                self, text=instr, bg="black", fg="white", width=14,
                font=("Courier", 11, "bold"), relief=tk.FLAT
            )
            lbl.grid(row=row, column=col, padx=2, pady=2)
            self.instruction_labels[instr] = lbl
            col += 1
            if col % 8 == 0:
                row += 1
                col = 0

    def set_active(self, active_instructions):
        for name, label in self.instruction_labels.items():
            if name in active_instructions:
                label.config(bg="red", fg="white")
            else:
                label.config(bg="black", fg="white")
import tkinter as tk
from tkinter import ttk

class InstructionBar:
    def __init__(self, root, on_step_change):
        self.frame = ttk.Frame(root)
        self.frame.pack(fill=tk.X, pady=5, side=tk.TOP)

        self.instruction_label = ttk.Label(self.frame, text="Instruction: HALT", font=("Arial", 18, "bold"))
        self.instruction_label.pack(side=tk.LEFT, padx=10)

        self.step_label = ttk.Label(self.frame, text="Step: 0 / 0", font=("Arial", 18))
        self.step_label.pack(side=tk.LEFT, padx=10)

        # Navigation buttons
        self.next_button = ttk.Button(self.frame, text="Next →", command=lambda: on_step_change(1))
        self.next_button.pack(side=tk.RIGHT, padx=5)

        self.prev_button = ttk.Button(self.frame, text="← Back", command=lambda: on_step_change(-1))
        self.prev_button.pack(side=tk.RIGHT, padx=5)

        # Step tracking
        self.current_step = 0
        self.total_steps = 0

    def update_instruction(self, instruction_text):
        self.instruction_label.config(text=f"Instruction: {instruction_text}")

    def update_step(self, current, total):
        self.current_step = current
        self.total_steps = total
        self.step_label.config(text=f"Step: {current} / {total}")

    def enable_buttons(self, enable=True):
        state = tk.NORMAL if enable else tk.DISABLED
        self.prev_button.config(state=state)
        self.next_button.config(state=state)

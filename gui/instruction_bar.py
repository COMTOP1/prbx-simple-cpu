import tkinter as tk
from tkinter import ttk
from typing import Callable, List

from gui.cpu_execution_step import CPUExecutionStep


class InstructionBar:
    __frame: tk.Frame
    __on_step_change: Callable[[int, List[CPUExecutionStep]], None]
    execution_steps: List[CPUExecutionStep]

    def __init__(self, root: tk.Tk, execution_steps: List[CPUExecutionStep], on_step_change: Callable[[int, List[CPUExecutionStep]], None]):
        self.__frame = ttk.Frame(root)
        self.__frame.pack(fill=tk.X, pady=5, side=tk.TOP)

        self.__on_step_change = on_step_change
        self.execution_steps = execution_steps

        self.instruction_label = ttk.Label(self.__frame, text=f"Instruction: {execution_steps[0].instruction_name}", font=("Arial", 18, "bold"))
        self.instruction_label.pack(side=tk.LEFT, padx=10)

        self.step_label = ttk.Label(self.__frame, text=f"Step: 0 / {len(execution_steps)-1}", font=("Arial", 18))
        self.step_label.pack(side=tk.LEFT, padx=10)

        self.desc_label = ttk.Label(self.__frame, text=f"Description: {execution_steps[0].micro_instruction_desc}", font=("Arial", 16))
        self.desc_label.pack(side=tk.LEFT, padx=10)

        # Navigation buttons
        self.next_button = ttk.Button(self.__frame, text="Next →", command=lambda: self.__on_step_change(1, self.execution_steps))
        self.next_button.pack(side=tk.RIGHT, padx=5)

        self.prev_button = ttk.Button(self.__frame, text="← Back", command=lambda: self.__on_step_change(-1, self.execution_steps))
        self.prev_button.pack(side=tk.RIGHT, padx=5)

        # Step tracking
        self.current_step = 0
        self.total_steps = len(self.execution_steps) - 1

    def update_steps(self, execution_steps: list[CPUExecutionStep]):
        self.execution_steps = execution_steps
        self.total_steps = len(execution_steps) - 1
        self.current_step = 0
        self.next_button.config(command=lambda: self.__on_step_change(1, self.execution_steps))
        self.prev_button.config(command=lambda: self.__on_step_change(-1, self.execution_steps))
        self.__on_step_change(0, self.execution_steps)

    def update_instruction(self, instruction_text: str):
        self.instruction_label.config(text=f"Instruction: {instruction_text}")

    def update_description(self, description_text: str):
        self.desc_label.config(text=f"Description: {description_text}")

    def update_step(self, current: int, total: int):
        self.current_step = current
        self.total_steps = total
        self.step_label.config(text=f"Step: {current} / {total}")

    def enable_buttons(self, enable=True):
        state = tk.NORMAL if enable else tk.DISABLED
        self.prev_button.config(state=state)
        self.next_button.config(state=state)

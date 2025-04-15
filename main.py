import argparse
import os
import tkinter as tk
from tkinter import ttk, filedialog

import gui.cpu_execution_step
from gui.cpu_blocks import CPUBlockDiagram
from gui.cpu_connections import CPUConnections
from gui.cpu_execution_step import CPUExecutionStep
from gui.cpu_readout_panel import CPUReadout, BITS_16_TYPE, BITS_8_TYPE, BOOL_TYPE, BIT_1_TYPE
from gui.instruction_bar import InstructionBar
from gui.memory_view_panel import MemoryView
from gui.micro_instruction_panel import MicroInstructionPanel
from gui.program_panel import ProgramPanel
from instructions import MOVE, ADD, SUB, AND, LOAD, STORE, ADDM, SUBM, JUMPU, JUMPZ, JUMPNZ, HALT, INVALID
from parser import parser
from sections.accumulator import Accumulator
from sections.control_bus import ControlBus, PC_EN, IR_WR, ACC_EN, RAM_EN, PC_LD, ACC_CTL2, \
    ACC_CTL1, ACC_CTL0, ADDR_SEL, DATA_SEL, RAM_WR, ZERO_FLAG, NOT_ZERO_FLAG, PC_INC, \
    HALT_FLAG, ACC_WR
from sections.data_bus import DataBus
from sections.instruction_register import InstructionRegister
from sections.memory import Memory
from sections.mux import Mux
from sections.program_counter import ProgramCounter


def empty_function():
    pass

class Run:
    __parser = argparse.ArgumentParser(
        prog='Simple CPU instruction set simulator',
        description='Simple CPU instruction set simulator is a teaching tool showing ' +
                    'how a CPU operates and assembly is executed')

    __memory: Memory
    __control_bus: ControlBus
    __instruction_register: InstructionRegister
    __program_counter: ProgramCounter
    __internal_bus: DataBus
    __data_in_bus: DataBus
    __data_out_bus: DataBus
    __address_bus: DataBus
    __accumulator: Accumulator
    __alu_mux: Mux
    __addr_mux: Mux
    __zero_flag: bool

    cpu_blocks: CPUBlockDiagram
    micro_panel: MicroInstructionPanel
    readout_frame: CPUReadout
    memory_panel: MemoryView
    program_panel: ProgramPanel
    instruction_bar: InstructionBar

    __args: argparse.Namespace

    def __init__(self):
        simulator_presenting_group = self.__parser.add_mutually_exclusive_group()
        simulator_presenting_group.add_argument("-cli", "--cli-simulator",
                help="Selecting command line simulator", action='store_true')
        simulator_presenting_group.add_argument("-gui", "--gui-simulator",
                help="Selecting graphical simulator", action='store_true')

        self.__args = self.__parser.parse_args()

        self.__memory = Memory(256)
        self.__control_bus = ControlBus()
        self.__instruction_register = InstructionRegister()
        self.__program_counter = ProgramCounter()
        self.__internal_bus = DataBus(16)
        self.__data_in_bus = DataBus(16)
        self.__data_out_bus = DataBus(16)
        self.__address_bus = DataBus(8)
        self.__accumulator = Accumulator()
        self.__alu_mux = Mux(8)
        self.__addr_mux = Mux(8)

    def __set_defaults(self):
        self.__alu_mux.set_input_0(0)
        self.__alu_mux.set_control(0)
        self.__addr_mux.set_input_0(0)
        self.__addr_mux.set_control(0)
        self.__data_in_bus.clear()
        self.__data_out_bus.clear()
        self.__address_bus.clear()
        self.__internal_bus.clear()
        self.__program_counter.insert(0)
        self.__instruction_register.insert(0)
        self.__memory.clear()
        self.__accumulator.insert(0)
        self.__zero_flag = False

    def insert_into_accumulator(self, execution_step: CPUExecutionStep, value: int):
        execution_step.record_bus(gui.cpu_execution_step.ALU_ACC, value, BITS_8_TYPE)
        if (self.__control_bus.read_control_bus() & ACC_WR) >> 8:
            self.__accumulator.insert(value)
            execution_step.record_control_line(gui.cpu_execution_step.ACC_WR)

    def process_alu_control(self, execution_step: CPUExecutionStep):
        if (not (self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
                and not (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
                and not (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            self.insert_into_accumulator(execution_step,
                (self.__data_in_bus.read() + self.__alu_mux.get()) & 0b11111111)
        elif (not (self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
              and not (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
              and (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            self.insert_into_accumulator(execution_step,
                (self.__data_in_bus.read() - self.__alu_mux.get()) & 0b11111111)
            execution_step.record_control_line(gui.cpu_execution_step.ACC_CTL0)
        elif (not (self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
              and (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
              and not (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            self.insert_into_accumulator(execution_step,
                (self.__alu_mux.get() & self.__data_in_bus.read()) & 0b11111111)
            execution_step.record_control_line(gui.cpu_execution_step.ACC_CTL1)
        elif (not (self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
              and (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
              and (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            empty_function()
            execution_step.record_control_line(gui.cpu_execution_step.ACC_CTL0)
            execution_step.record_control_line(gui.cpu_execution_step.ACC_CTL1)
        elif ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
              and not (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
              and not (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            self.insert_into_accumulator(execution_step,
                 self.__alu_mux.get() & 0b11111111)
            execution_step.record_control_line(gui.cpu_execution_step.ACC_CTL2)
        elif ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
              and not (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
              and (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            empty_function()
            execution_step.record_control_line(gui.cpu_execution_step.ACC_CTL0)
            execution_step.record_control_line(gui.cpu_execution_step.ACC_CTL2)
        elif ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
              and (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
              and not (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            empty_function()
            execution_step.record_control_line(gui.cpu_execution_step.ACC_CTL1)
            execution_step.record_control_line(gui.cpu_execution_step.ACC_CTL2)
        elif ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
              and (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
              and (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            empty_function()
            execution_step.record_control_line(gui.cpu_execution_step.ACC_CTL0)
            execution_step.record_control_line(gui.cpu_execution_step.ACC_CTL1)
            execution_step.record_control_line(gui.cpu_execution_step.ACC_CTL2)
        else:
            print(f"Invalid ALU control combination: "
                 f"ACC_CTL2: {(self.__control_bus.read_control_bus() & ACC_CTL2) >> 7}, "
                 f"ACC_CTL1: {(self.__control_bus.read_control_bus() & ACC_CTL1) >> 6}, "
                 f"ACC_CTL0: {(self.__control_bus.read_control_bus() & ACC_CTL0) >> 5}")
        self.__zero_flag = self.__accumulator.get() == 0
        execution_step.record_component(gui.cpu_execution_step.ZERO, self.__zero_flag, BOOL_TYPE)

    def process_control_bus(self, execution_step: CPUExecutionStep) -> bool:
        if (self.__control_bus.read_control_bus() & HALT_FLAG) >> 16:
            print("HALT")
            execution_step.record_control_line(gui.cpu_execution_step.HALT_FLAG)
            return True
        # Process any micro-instruction that writes to a bus as other micro-instructions will read from this
        if (self.__control_bus.read_control_bus() & ADDR_SEL) >> 4:
            self.__addr_mux.set_control(1)
            execution_step.record_control_line(gui.cpu_execution_step.ADDR_SEL)
            execution_step.record_component(gui.cpu_execution_step.ADDR_MUX, 1, BIT_1_TYPE)
        else:
            self.__addr_mux.set_control(0)
            execution_step.record_component(gui.cpu_execution_step.ADDR_MUX, 0, BIT_1_TYPE)
        if (self.__control_bus.read_control_bus() & DATA_SEL) >> 3:
            self.__alu_mux.set_control(1)
            execution_step.record_control_line(gui.cpu_execution_step.DATA_SEL)
            execution_step.record_component(gui.cpu_execution_step.DATA_MUX, 1, BIT_1_TYPE)
        else:
            self.__alu_mux.set_control(0)
            execution_step.record_component(gui.cpu_execution_step.DATA_MUX, 0, BIT_1_TYPE)
        if (self.__control_bus.read_control_bus() & PC_EN) >> 13:
            self.__addr_mux.set_input_0(self.__program_counter.get())
            execution_step.record_control_line(gui.cpu_execution_step.PC_EN)
        if (self.__control_bus.read_control_bus() & PC_INC) >> 12:
            self.__program_counter.enable()
            execution_step.record_control_line(gui.cpu_execution_step.PC_INC)
        if (self.__control_bus.read_control_bus() & ACC_EN) >> 9:
            self.__data_in_bus.clear()
            self.__data_in_bus.write(self.__accumulator.get())
            execution_step.record_control_line(gui.cpu_execution_step.ACC_EN)
        else:
            self.__data_in_bus.clear()
        if (self.__control_bus.read_control_bus() & RAM_EN) >> 2:
            self.__data_out_bus.clear()
            self.__data_out_bus.write(self.__memory.get(self.__addr_mux.get()))
            execution_step.record_control_line(gui.cpu_execution_step.RAM_EN)
            execution_step.record_memory_read_snapshot(self.__addr_mux.get())
        else:
            self.__data_out_bus.clear()
        if (self.__control_bus.read_control_bus() & IR_WR) >> 9:
            self.__instruction_register.insert(self.__data_out_bus.read())
            execution_step.record_control_line(gui.cpu_execution_step.IR_WR)
        self.__internal_bus.clear()
        self.__internal_bus.write(self.__instruction_register.get())

        self.__addr_mux.set_input_1(self.__internal_bus.read() & 0B11111111)
        self.__alu_mux.set_input_0(self.__internal_bus.read() & 0B11111111)
        self.__alu_mux.set_input_1(self.__data_out_bus.read() & 0B11111111)

        # All outputs have been processed and now we will read from things
        # The IR is set by default when there is data on the data out bus
        self.process_alu_control(execution_step)
        if (self.__control_bus.read_control_bus() & PC_LD) >> 10:
            if (self.__control_bus.read_control_bus() & ZERO_FLAG) >> 14:
                execution_step.record_control_line(gui.cpu_execution_step.ZERO_FLAG)
                if self.__zero_flag:
                    self.__program_counter.insert(self.__internal_bus.read() & 0B11111111)
                    execution_step.record_control_line(gui.cpu_execution_step.PC_LD)
            elif (self.__control_bus.read_control_bus() & NOT_ZERO_FLAG) >> 15:
                execution_step.record_control_line(gui.cpu_execution_step.NOT_ZERO_FLAG)
                if not self.__zero_flag:
                    self.__program_counter.insert(self.__internal_bus.read() & 0B11111111)
                    execution_step.record_control_line(gui.cpu_execution_step.PC_LD)
            else:
                execution_step.record_control_line(gui.cpu_execution_step.PC_LD)
                self.__program_counter.insert(self.__internal_bus.read() & 0B11111111)
        if (self.__control_bus.read_control_bus() & RAM_WR) >> 1:
            initial_value = self.__memory.get(self.__addr_mux.get())
            self.__memory.insert(self.__addr_mux.get(), self.__data_in_bus.read())
            execution_step.record_control_line(gui.cpu_execution_step.RAM_WR)
            execution_step.record_memory_write_snapshot(self.__addr_mux.get(), self.__data_in_bus.read(), initial_value)
        execution_step.record_component(gui.cpu_execution_step.PC, self.__program_counter.get(), BITS_8_TYPE)
        execution_step.record_component(gui.cpu_execution_step.IR, self.__instruction_register.get(), BITS_16_TYPE)
        execution_step.record_component(gui.cpu_execution_step.ACC, self.__accumulator.get(), BITS_8_TYPE)
        execution_step.record_bus(gui.cpu_execution_step.ADDR_BUS, self.__addr_mux.get(), BITS_8_TYPE)
        execution_step.record_bus(gui.cpu_execution_step.INTERNAL_BUS, self.__internal_bus.read(), BITS_16_TYPE)
        execution_step.record_bus(gui.cpu_execution_step.DATA_IN_BUS, self.__data_in_bus.read(), BITS_16_TYPE)
        execution_step.record_bus(gui.cpu_execution_step.DATA_OUT_BUS, self.__data_out_bus.read(), BITS_16_TYPE)
        return False

    def gui(self):
        def on_step_change(direction: int, execution_steps: list[CPUExecutionStep]) -> None:
            current_step = self.instruction_bar.current_step
            new_step = current_step + direction
            if 0 <= new_step <= self.instruction_bar.total_steps:
                self.memory_panel.clear_highlight()

                if direction < 0 and current_step != len(execution_steps):
                    mem_snapshot = execution_steps[current_step].memory_write_snapshot
                    for addr, (new_val, old_val) in mem_snapshot.items():
                        self.memory_panel.update_value(addr, old_val)

                self.instruction_bar.update_step(new_step, self.instruction_bar.total_steps)
                self.instruction_bar.update_instruction(execution_steps[new_step].instruction_name)
                self.instruction_bar.update_description(execution_steps[new_step].micro_instruction_desc)

                readout_list: list[tuple[str, str]] = []
                component_list: list[tuple[str, str]] = []
                for name, value in execution_steps[new_step].component_values.items():
                    str_value, int_value = value
                    component_list.append((name, str_value))
                    if name == "ACC" or name == "PC" or name == "IR" or name == "Zero":
                        readout_list.append((name, str_value))
                for name, value in execution_steps[new_step].bus_values.items():
                    str_value, int_value = value
                    component_list.append((name, str_value))
                    if name == "DATA_OUT_BUS" or name == "DATA_IN_BUS" or name == "INTERNAL_BUS":
                        readout_list.append((name, str_value))
                    elif name == "ADDR_BUS":
                        readout_list.append(("ADDRESS_BUS", str_value))
                self.cpu_blocks.update_block_value(component_list)
                self.readout_frame.update_values_formatted(readout_list)

                self.micro_panel.set_active(execution_steps[new_step].control_lines)

                for addr, (new_val, old_val) in execution_steps[new_step].memory_write_snapshot.items():
                    self.memory_panel.update_value(addr, new_val)
                    self.memory_panel.highlight_address(addr)

                memory_read_snapshot = execution_steps[new_step].memory_read_snapshot
                if memory_read_snapshot != -1:
                    self.memory_panel.highlight_address(memory_read_snapshot, color="green")

        def open_file():
            initial_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = filedialog.askopenfilename(filetypes=[("DAT files", "*.dat")], initialdir=initial_dir)

            if file_path:
                file_name.set(file_path)
                f = open(file_path)
                contents = f.read()
                execution_steps, parsed_instructions = self.run_emulator(contents)
                self.instruction_bar.update_steps(execution_steps)

        print('gui')
        root = tk.Tk()
        root.title("SimpleCPU Emulator")
        root.geometry("1430x850")
        root.configure(bg="black")

        # Create a frame for the top bar
        top_bar = tk.Frame(root, height=40, background="grey16")
        top_bar.pack(fill="x", side="top")

        # Create a StringVar to hold the filename
        file_name = tk.StringVar()

        # Create a button to open the file explorer
        open_button = tk.Button(top_bar, text="Open File", command=open_file, background="white", foreground="black")
        open_button.pack(side="left", padx=10)

        # Create a label to display the filename
        file_label = tk.Label(top_bar, textvariable=file_name, fg="white", bg="grey16")
        file_label.pack(side="left", padx=10, pady=2)

        steps, parsed_instructions = self.run_emulator(self.unparsed_instructions)

        self.instruction_bar = InstructionBar(root, steps, on_step_change)

        # === Top frame to hold canvas and memory ===
        top_frame = tk.Frame(root)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # --- Canvas area ---
        canvas_frame = tk.Frame(top_frame)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(canvas_frame, bg="white", width=1000, height=600)
        canvas.pack(fill=tk.BOTH, expand=True)

        self.cpu_blocks = CPUBlockDiagram(canvas)
        self.cpu_blocks.draw_all_blocks()
        connections = CPUConnections(canvas)
        connections.draw_connections()

        # --- Micro-instruction Readout (under canvas) ---
        self.micro_panel = MicroInstructionPanel(canvas, [
            "IR_WR", "ACC_WR", "ACC_EN", "ACC_CTL0", "ACC_CTL1", "ACC_CTL2",
            "DATA_SEL", "ADDR_SEL",
            "RAM_EN", "RAM_WR", "PC_EN", "PC_LD", "PC_INC",
            "ZERO_FLAG", "NOT_ZERO_FLAG",
            "HALT_FLAG"
        ])
        self.micro_panel.pack(side=tk.BOTTOM, fill=tk.X)

        # --- CPU Readout (under canvas) ---
        self.readout_frame = CPUReadout(canvas, [
            ("DATA_OUT_BUS", BITS_16_TYPE), ("DATA_IN_BUS", BITS_16_TYPE),
            ("INTERNAL_BUS", BITS_16_TYPE), ("ADDRESS_BUS", BITS_8_TYPE),
            ("ACC", BITS_8_TYPE), ("PC", BITS_8_TYPE), ("IR", BITS_8_TYPE),
            ("ZERO", BOOL_TYPE)
        ])
        self.readout_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.program_panel = ProgramPanel(top_frame)
        self.program_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        self.program_panel.update_program(parsed_instructions)

        # --- Memory display ---
        memory_frame = tk.Frame(top_frame)
        memory_frame.pack(side=tk.RIGHT, fill=tk.Y)

        memory_listbox = tk.Listbox(memory_frame, font=("Courier", 10), width=20)
        scrollbar = ttk.Scrollbar(memory_frame, orient=tk.VERTICAL, command=memory_listbox.yview)
        memory_listbox.config(yscrollcommand=scrollbar.set)
        memory_listbox.pack(side=tk.LEFT, fill=tk.Y)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.memory_panel = MemoryView(memory_listbox, memory_size=256)
        self.memory_panel.pack(side='right', fill='y')

        for initial_address, initial_value_tuple in steps[0].memory_write_snapshot.items():
            initial_value, do_not_used = initial_value_tuple
            self.memory_panel.update_value(initial_address, initial_value)
            self.memory_panel.highlight_address(initial_address)

        root.mainloop()

    def cli(self):
        print('cli')
        self.run_emulator(self.unparsed_instructions)

    unparsed_instructions = '''MOVE 150
        STORE 101
        MOVE 20
        STORE 102
        MOVE 100
        STORE 103
        LOAD 101
        ADDM 103
        STORE 104
        SUBM 102
        STORE 105
        JUMPNZ 13
        JUMPU 21
        SUB 11
        STORE 106
        ADD 23
        STORE 107
        AND 231
        STORE 108
        MOVE 0
        JUMPZ 11
        HALT'''

    # unparsed_instructions = '''MOVE 5
    # STORE 30
    # MOVE 4
    # STORE 31
    # MOVE 1
    # STORE 33
    # MOVE 0
    # STORE 34
    # LOAD 34       ; Clear ACC = 0
    # STORE 32      ; RESULT = 0
    # LOAD 31       ; Load B (multiplier)
    # STORE 35      ; TEMP_COUNTER = B LOOP after
    # LOAD 35       ; Load counter
    # JUMPZ 21      ; If zero, we're done
    # LOAD 32       ; Load current result
    # ADDM 30       ; Add A (multiplicand)
    # STORE 32      ; Store back to RESULT
    # LOAD 35       ; Load counter
    # SUBM 33       ; Subtract 1
    # STORE 35      ; Store back
    # JUMPNZ 12      ; If not zero, continue
    # HALT'''

    def run_emulator(self, unparsed_instructions: str):
        self.__set_defaults()
        parsed_instructions, memory = parser(unparsed_instructions)
        step = 0
        initial_step = CPUExecutionStep(step, "INITIAL", "The initial state of the CPU before execution")
        i = 0
        while i < len(memory):
            self.__memory.insert(i, memory[i])
            initial_step.record_memory_write_snapshot(i, memory[i], 0)
            i += 1
        run = True
        max_runs = 1000
        i = 0
        execution_steps: list[CPUExecutionStep] = [initial_step]
        while i < max_runs and run:
            mem_val = self.__memory.get(self.__program_counter.get())
            print(f"{self.__program_counter.get()} 0x{mem_val:04x}")
            if (mem_val >> 12) == 0X0:
                instruction = MOVE
                instruction_text = f"MOVE {mem_val & 0xFF}"
            elif (mem_val >> 12) == 0X1:
                instruction = ADD
                instruction_text = f"ADD {mem_val & 0xFF}"
            elif (mem_val >> 12) == 0X2:
                instruction = SUB
                instruction_text = f"SUB {mem_val & 0xFF}"
            elif (mem_val >> 12) == 0X3:
                instruction = AND
                instruction_text = f"AND {mem_val & 0xFF}"
            elif (mem_val >> 12) == 0X4:
                instruction = LOAD
                instruction_text = f"LOAD {mem_val & 0xFF}"
            elif (mem_val >> 12) == 0X5:
                instruction = STORE
                instruction_text = f"STORE {mem_val & 0xFF}"
            elif (mem_val >> 12) == 0X6:
                instruction = ADDM
                instruction_text = f"ADDM {mem_val & 0xFF}"
            elif (mem_val >> 12) == 0X7:
                instruction = SUBM
                instruction_text = f"SUBM {mem_val & 0xFF}"
            elif (mem_val >> 12) == 0X8:
                instruction = JUMPU
                instruction_text = f"JUMPU {mem_val & 0xFF}"
            elif (mem_val >> 12) == 0X9:
                instruction = JUMPZ
                instruction_text = f"JUMPZ {mem_val & 0xFF}"
            elif (mem_val >> 12) == 0XA:
                instruction = JUMPNZ
                instruction_text = f"JUMPNZ {mem_val & 0xFF}"
            elif (mem_val >> 12) == 0XF:
                instruction = HALT
                instruction_text = "HALT"
            else:
                instruction = INVALID
                instruction_text = f"INVALID - {mem_val}"
            print(instruction_text)
            for instructions, desc in instruction:
                step += 1
                execution_step = CPUExecutionStep(step, instruction_text, desc)
                self.__control_bus.clear()
                self.__control_bus.add_control(instructions)
                if self.process_control_bus(execution_step):
                    run = False
                execution_steps.append(execution_step)
            i += 1
        return execution_steps, parsed_instructions

    def run(self):
        if self.__args.gui_simulator:
            self.gui()
        elif self.__args.cli_simulator:
            self.cli()
        else:
            raise Exception('No simulator selected')


if __name__ == '__main__':
    Run().run()

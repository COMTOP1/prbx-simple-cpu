import argparse
import tkinter as tk
from tkinter import ttk

from gui.cpu_blocks import CPUBlockDiagram
from gui.cpu_connections import CPUConnections
from gui.cpu_readout_panel import CPUReadout, BITS_16_TYPE, BITS_8_TYPE, BOOL_TYPE
from gui.instruction_bar import InstructionBar
from gui.memory_view_panel import MemoryView
from gui.micro_instruction_panel import MicroInstructionPanel
from instructions import MOVE, ADD, SUB, AND, LOAD, STORE, ADDM, SUBM, JUMPU, JUMPZ, JUMPNZ, HALT
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

    def __set_control_defaults(self):
        self.__alu_mux.set_input_0(0)
        self.__alu_mux.set_control(0)
        self.__addr_mux.set_input_0(0)
        self.__addr_mux.set_control(0)
        self.__data_in_bus.clear()
        self.__data_out_bus.clear()
        self.__address_bus.clear()
        self.__internal_bus.clear()

    def insert_into_accumulator(self, value: int):
        if (self.__control_bus.read_control_bus() & ACC_WR) >> 8:
            self.__accumulator.insert(value)

    def process_alu_control(self):
        if (not (self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
                and not (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
                and not (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            self.insert_into_accumulator(
                (self.__data_in_bus.read() + self.__alu_mux.get()) & 0b11111111)
        elif (not (self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
              and not (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
              and (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            self.insert_into_accumulator(
                (self.__data_in_bus.read() - self.__alu_mux.get()) & 0b11111111)
        elif (not (self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
              and (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
              and not (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            self.insert_into_accumulator(
                (self.__alu_mux.get() & self.__data_in_bus.read()) & 0b11111111)
        elif (not (self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
              and (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
              and (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            empty_function()
        elif ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
              and not (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
              and not (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            self.insert_into_accumulator(self.__alu_mux.get() & 0b11111111)
        elif ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
              and not (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
              and (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            empty_function()
        elif ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
              and (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
              and not (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            empty_function()
        elif ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7
              and (self.__control_bus.read_control_bus() & ACC_CTL1) >> 6
              and (self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            empty_function()
        else:
            raise ValueError(f"Invalid ALU control combination: "
                 f"ACC_CTL2: {(self.__control_bus.read_control_bus() & ACC_CTL2) >> 7}, "
                 f"ACC_CTL1: {(self.__control_bus.read_control_bus() & ACC_CTL1) >> 6}, "
                 f"ACC_CTL0: {(self.__control_bus.read_control_bus() & ACC_CTL0) >> 5}")
        self.__zero_flag = self.__accumulator.get() == 0

    def process_control_bus(self) -> bool:
        if (self.__control_bus.read_control_bus() & HALT_FLAG) >> 16:
            print("HALT")
            return True
        # Process any micro-instruction that writes to a bus as other micro-instructions will read from this
        if (self.__control_bus.read_control_bus() & ADDR_SEL) >> 4:
            self.__addr_mux.set_control(1)
        else: self.__addr_mux.set_control(0)
        if (self.__control_bus.read_control_bus() & DATA_SEL) >> 3:
            self.__alu_mux.set_control(1)
        else: self.__alu_mux.set_control(0)
        if (self.__control_bus.read_control_bus() & PC_EN) >> 13:
            self.__addr_mux.set_input_0(self.__program_counter.get())
        if (self.__control_bus.read_control_bus() & PC_INC) >> 12:
            self.__program_counter.enable()
        if (self.__control_bus.read_control_bus() & ACC_EN) >> 9:
            self.__data_in_bus.clear()
            self.__data_in_bus.write(self.__accumulator.get())
        if (self.__control_bus.read_control_bus() & RAM_EN) >> 2:
            self.__data_out_bus.clear()
            self.__data_out_bus.write(self.__memory.get(self.__addr_mux.get()))
        if (self.__control_bus.read_control_bus() & IR_WR) >> 9:
            self.__instruction_register.insert(self.__data_out_bus.read())

        self.__internal_bus.clear()
        self.__internal_bus.write(self.__instruction_register.get())

        self.__addr_mux.set_input_1(self.__internal_bus.read() & 0B11111111)
        self.__alu_mux.set_input_0(self.__internal_bus.read() & 0B11111111)
        self.__alu_mux.set_input_1(self.__data_out_bus.read() & 0B11111111)

        # All outputs have been processed and now we will read from things
        # The IR is set by default when there is data on the data out bus
        self.process_alu_control()
        if (self.__control_bus.read_control_bus() & PC_LD) >> 10:
            if (self.__control_bus.read_control_bus() & ZERO_FLAG) >> 14:
                if self.__zero_flag:
                    self.__program_counter.insert(self.__internal_bus.read() & 0B11111111)
            elif (self.__control_bus.read_control_bus() & NOT_ZERO_FLAG) >> 15:
                if not self.__zero_flag:
                    self.__program_counter.insert(self.__internal_bus.read() & 0B11111111)
            else:
                self.__program_counter.insert(self.__internal_bus.read() & 0B11111111)
        if (self.__control_bus.read_control_bus() & RAM_WR) >> 1:
            self.__memory.insert(self.__addr_mux.get(), self.__data_in_bus.read())
        return False

    def gui(self):
        def on_step_change(direction):
            # You'd use this to change the current step and trigger redraws
            new_step = self.instruction_bar.current_step + direction
            if 0 <= new_step <= self.instruction_bar.total_steps:
                self.instruction_bar.update_step(new_step, self.instruction_bar.total_steps)
                # Add logic to update CPU/memory state here
                print(f"Changed to step {new_step}")

        window = tk.Tk()
        print('gui')
        root = window
        root.title("SimpleCPU Emulator")
        root.geometry("1200x800")
        root.configure(bg="black")

        self.instruction_bar = InstructionBar(root, on_step_change)

        # === Top frame to hold canvas and memory ===
        top_frame = tk.Frame(root)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # --- Canvas area ---
        canvas_frame = tk.Frame(top_frame)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(canvas_frame, bg="white", width=1000, height=600)
        canvas.pack(fill=tk.BOTH, expand=True)

        cpu_blocks = CPUBlockDiagram(canvas)
        cpu_blocks.draw_all_blocks()
        connections = CPUConnections(canvas)
        connections.draw_connections()

        # --- Micro-instruction Readout (under canvas) ---
        micro_panel = MicroInstructionPanel(canvas, [
            "IR_WR", "ACC_WR", "ACC_EN", "ACC_CTL0", "ACC_CTL1", "ACC_CTL2",
            "DATA_SEL", "ADDR_SEL",
            "RAM_EN", "RAM_WR", "PC_EN", "PC_LD", "PC_INC",
            "ZERO_FLAG", "NOT_ZERO_FLAG",
            "HALT_FLAG"
        ])
        micro_panel.pack(side=tk.BOTTOM, fill=tk.X)

        # --- CPU Readout (under canvas) ---
        readout_frame = CPUReadout(canvas, [
            ("DATA_OUT_BUS", BITS_16_TYPE), ("DATA_IN_BUS", BITS_16_TYPE),
            ("INTERNAL_BUS", BITS_16_TYPE), ("ADDRESS_BUS", BITS_8_TYPE),
            ("ACC", BITS_8_TYPE), ("PC", BITS_8_TYPE), ("IR", BITS_8_TYPE),
            ("ZERO", BOOL_TYPE)
        ])
        readout_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # --- Memory display ---
        memory_frame = tk.Frame(top_frame)
        memory_frame.pack(side=tk.RIGHT, fill=tk.Y)

        memory_listbox = tk.Listbox(memory_frame, font=("Courier", 10), width=20)
        scrollbar = ttk.Scrollbar(memory_frame, orient=tk.VERTICAL, command=memory_listbox.yview)
        memory_listbox.config(yscrollcommand=scrollbar.set)
        memory_listbox.pack(side=tk.LEFT, fill=tk.Y)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        memory_panel = MemoryView(memory_listbox, memory_size=256)
        memory_panel.pack(side='right', fill='y')

        # Example update (simulate micro-instruction being active)
        def simulate_update1():
            active = {"ACC_EN", "RAM_EN", "PC_INC", "IR_WR"}
            micro_panel.set_active(active)
            readout_frame.update_values([
                ("DATA_OUT_BUS", 0x3F, BITS_16_TYPE),
                ("DATA_IN_BUS", 0x12, BITS_16_TYPE),
                ("INTERNAL_BUS", 0xAB, BITS_16_TYPE),
                ("ADDRESS_BUS", 0x1C, BITS_8_TYPE),
                ("ACC", 0x4E, BITS_8_TYPE),
                ("PC", 0x0A, BITS_8_TYPE),
                ("IR", 0xB2, BITS_8_TYPE),
                ("ZERO", 1, BOOL_TYPE),
            ])
            cpu_blocks.update_block_value([("ACC", "0x11"), ("ZERO", "True"), ("ALU_ACC", "0x32"), ("ADDR_MUX", "1")])

        def simulate_update2():
            active = {"NOT_ZERO_FLAG", "HALT_FLAG"}
            micro_panel.set_active(active)
            self.instruction_bar.update_instruction("MOVE 2")
            self.instruction_bar.update_step(5, 31)

        def simulate_update3():
            active = {"ACC_CTL0", "ACC_CTL1"}
            micro_panel.set_active(active)
            memory_panel.clear_highlight()

        def simulate_ram():
            memory_panel.update_value(12, 120)
            memory_panel.highlight_address(12)

        root.after(2000, simulate_update1)
        root.after(4000, simulate_update2)
        root.after(6000, simulate_update3)

        root.after(3000, simulate_ram)

        root.mainloop()

    def cli(self):
        print('cli')
        self.run_emulator()

    def run_emulator(self):
        parsed_instructions, memory = parser('''MOVE 150
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
        HALT''')
        i = 0
        while i < len(memory):
            self.__memory.insert(i, memory[i])
            i += 1
        run = True
        max_runs = 1000
        i = 0
        while i < max_runs and run:
            mem_val = self.__memory.get(self.__program_counter.get())
            print(f"{self.__program_counter.get()} 0x{mem_val:04x}")
            if (mem_val >> 12) == 0X0:
                instruction = MOVE
            elif (mem_val >> 12) == 0X1:
                instruction = ADD
            elif (mem_val >> 12) == 0X2:
                instruction = SUB
            elif (mem_val >> 12) == 0X3:
                instruction = AND
            elif (mem_val >> 12) == 0X4:
                instruction = LOAD
            elif (mem_val >> 12) == 0X5:
                instruction = STORE
            elif (mem_val >> 12) == 0X6:
                instruction = ADDM
            elif (mem_val >> 12) == 0X7:
                instruction = SUBM
            elif (mem_val >> 12) == 0X8:
                instruction = JUMPU
            elif (mem_val >> 12) == 0X9:
                instruction = JUMPZ
            elif (mem_val >> 12) == 0XA:
                instruction = JUMPNZ
            elif (mem_val >> 12) == 0XF:
                instruction = HALT
            else:
                raise ValueError(f"Invalid instruction: 0x{mem_val:04x}")
            for instructions, desc in instruction:
                self.__control_bus.clear()
                self.__control_bus.add_control(instructions)
                if self.process_control_bus():
                    run = False
            i += 1
        print("ADDM", self.__memory.get(104))
        print("SUBM", self.__memory.get(105))
        print("SUB", self.__memory.get(106))
        print("ADD", self.__memory.get(107))
        print("AND", self.__memory.get(108))

    def run(self):
        if self.__args.gui_simulator:
            self.gui()
        elif self.__args.cli_simulator:
            self.cli()
        else:
            raise Exception('No simulator selected')


if __name__ == '__main__':
    Run().run()

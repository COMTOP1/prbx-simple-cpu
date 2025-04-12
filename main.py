import argparse
import tkinter as tk
from tkinter import ttk

from gui.cpu_blocks import CPUBlockDiagram
from gui.cpu_readout_panel import CPUReadout, BITS_16_TYPE, BITS_8_TYPE, BOOL_TYPE
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
        window = tk.Tk()
        print('gui')
        self.root = window
        self.root.title("CPU Emulator")
        self.root.configure(bg="white")
        self.canvas = tk.Canvas(self.root, width=1000, height=700, bg="white", highlightthickness=0)
        self.canvas.pack()
        self.draw_components()
        self.draw_connections()
        self.create_memory_display()
        self.root.mainloop()

    def create_memory_display(self):
        frame = tk.Frame(self.root, bg="white")
        frame.place(x=720, y=320, width=180, height=300)

        canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Dummy memory content for display
        for i in range(256):
            addr = f"{i:03}"
            data = f"{'00000000':>8}"  # Replace with real memory lookup
            row = tk.Frame(scroll_frame, bg="white")
            tk.Label(row, text=addr, width=5, anchor="w", font=("Courier", 9), bg="white").pack(side="left")
            tk.Label(row, text=data, width=10, anchor="w", font=("Courier", 9), bg="white").pack(side="left")
            row.pack(anchor="w")

    def draw_components(self):
        # Boxes: label, x1, y1, x2, y2
        boxes = [
            ("Instruction Register (IR)", 100, 100, 220, 160),
            ("Control Logic", 60, 250, 180, 310),
            ("ALU", 230, 300, 330, 370),
            ("MUX 0", 190, 200, 240, 260),
            ("MUX 1", 420, 260, 470, 310),
            ("Program Counter (PC)", 480, 200, 600, 260),
            ("Accumulator (ACC)", 230, 390, 330, 440),
            ("Zero", 340, 390, 390, 440),
            # ("MEMORY", 720, 120, 900, 300),
        ]
        for label, x1, y1, x2, y2 in boxes:
            self.canvas.create_rectangle(x1, y1, x2, y2, width=3, fill="#f0f0f0")
            self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=label, font=("Helvetica", 10, "bold"))

    def draw_connections(self):
        # Line colors
        colors = {
            "data": "#4da6ff",        # Blue
            "address": "#99ff99",     # Light green
            "control": "#ff4d4d",     # Red
            "internal": "#b366ff"     # Purple
        }

        line_width = 4

        # Data Bus (data_out_bus and data_in_bus)
        self.hline(220, 130, 720, colors["data"], line_width)   # IR to Memory (data_out)
        self.hline(330, 410, 720, colors["data"], line_width)   # ACC to Memory (data_in)

        # Address Bus
        self.vline(470, 285, 310, colors["address"], line_width)   # MUX to PC
        self.hline(470, 285, 720, colors["address"], line_width)   # to Memory

        # Internal Bus (from IR to MUXs, ALU)
        self.vline(160, 160, 200, colors["internal"], line_width)
        self.hline(160, 200, 190, colors["internal"], line_width)
        self.vline(600, 230, 260, colors["internal"], line_width)
        self.hline(600, 260, 720, colors["internal"], line_width)

        # Control Bus
        self.vline(120, 310, 440, colors["control"], line_width)
        self.hline(120, 440, 230, colors["control"], line_width)
        self.hline(120, 320, 470, colors["control"], line_width)
        self.hline(120, 330, 330, colors["control"], line_width)
        self.hline(120, 340, 390, colors["control"], line_width)

    def hline(self, x1, y1, x2, color, width):
        self.canvas.create_line(x1, y1, x2, y1, fill=color, width=width)

    def vline(self, x1, y1, y2, color, width):
        self.canvas.create_line(x1, y1, x1, y2, fill=color, width=width)

    def cli(self):
        print('cli')
        parsed = parser('''MOVE 150
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
        while i < len(parsed):
            self.__memory.insert(i, parsed[i])
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
            for instructions in instruction:
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
        return
        for instruction in parsed:
            if instruction.split(" ")[0] == "MOVE":
                for micro in MOVE:
                    self.__control_bus.clear()
                    self.__control_bus.add_control(micro)
                    self.process_control_bus()
                    print(micro)
            elif instruction.split(" ")[0] == "ADDM":
                for micro in ADDM:
                    print(micro)

    def run(self):
        if self.__args.gui_simulator:
            self.gui()
        elif self.__args.cli_simulator:
            self.cli()
        else:
            raise Exception('No simulator selected')


if __name__ == '__main__':
    Run().run()

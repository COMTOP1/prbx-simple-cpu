import argparse
import tkinter as tk

from instructions import MOVE, ADD, SUB, AND, LOAD, STORE, ADDM, SUBM, JUMPU, JUMPZ, JUMPNZ, HALT
from parser import parser
from sections.accumulator import Accumulator
from sections.control_bus import ControlBus, PC_EN, IR_WR, ACC_EN, RAM_EN, PC_LD, ACC_CTL2, ACC_CTL1, ACC_CTL0, \
    ADDR_SEL, DATA_SEL, RAM_WR, ZERO_FLAG, NOT_ZERO_FLAG, PC_INC, HALT_FLAG, ACC_WR
from sections.data_bus import DataBus
from sections.instruction_register import InstructionRegister
from sections.memory import Memory
from sections.mux import Mux
from sections.program_counter import ProgramCounter


def empty_function():
    pass

class Run:
    __parser = argparse.ArgumentParser(prog='Simple CPU instruction set simulator',
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
            # print(100, value)
            self.__accumulator.insert(value)

    def process_alu_control(self):
        # print(1)
        if not ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7) and not ((self.__control_bus.read_control_bus() & ACC_CTL1) >> 6) and not ((self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            self.insert_into_accumulator((self.__data_in_bus.read() + self.__alu_mux.get()) & 0b11111111)
            # print(2, self.__data_in_bus.read(), self.__alu_mux.get())
            # print(self.__accumulator.get())
        elif not ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7) and not ((self.__control_bus.read_control_bus() & ACC_CTL1) >> 6) and ((self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            self.insert_into_accumulator((self.__data_in_bus.read() - self.__alu_mux.get()) & 0b11111111)
            # print(3, self.__data_in_bus.read(), self.__alu_mux.get())
        elif not ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7) and ((self.__control_bus.read_control_bus() & ACC_CTL1) >> 6) and not ((self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            self.insert_into_accumulator((self.__alu_mux.get() & self.__data_in_bus.read()) & 0b11111111)
            # print(4)
        elif not ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7) and ((self.__control_bus.read_control_bus() & ACC_CTL1) >> 6) and ((self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            empty_function()
            # print(5)
        elif ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7) and not ((self.__control_bus.read_control_bus() & ACC_CTL1) >> 6) and not ((self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            self.insert_into_accumulator(self.__alu_mux.get() & 0b11111111)
            # print(6)
        elif ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7) and not ((self.__control_bus.read_control_bus() & ACC_CTL1) >> 6) and ((self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            empty_function()
            # print(7)
        elif ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7) and ((self.__control_bus.read_control_bus() & ACC_CTL1) >> 6) and not ((self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            empty_function()
            # print(8)
        elif ((self.__control_bus.read_control_bus() & ACC_CTL2) >> 7) and ((self.__control_bus.read_control_bus() & ACC_CTL1) >> 6) and ((self.__control_bus.read_control_bus() & ACC_CTL0) >> 5):
            empty_function()
            # print(9)
        else:
            raise ValueError(f"Invalid ALU control combination: ACC_CTL2: {(self.__control_bus.read_control_bus() & ACC_CTL2) >> 7}, ACC_CTL1: {(self.__control_bus.read_control_bus() & ACC_CTL1) >> 6}, ACC_CTL0: {(self.__control_bus.read_control_bus() & ACC_CTL0) >> 5}")
        self.__zero_flag = self.__accumulator.get() == 0
        # print(9.5, self.__zero_flag, self.__accumulator.get())

    def process_control_bus(self) -> bool:
        # self.__set_control_defaults()
        # print(10)
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
            # print(15, self.__program_counter.get())
        if (self.__control_bus.read_control_bus() & PC_INC) >> 12:
            self.__program_counter.enable()
        if (self.__control_bus.read_control_bus() & ACC_EN) >> 9:
            self.__data_in_bus.clear()
            self.__data_in_bus.write(self.__accumulator.get())
            # print(17)
        if (self.__control_bus.read_control_bus() & RAM_EN) >> 2:
            self.__data_out_bus.clear()
            self.__data_out_bus.write(self.__memory.get(self.__addr_mux.get()))
            # print(11, self.__memory.get(self.__addr_mux.get()) & 0B11111111, self.__data_out_bus.read() & 0B11111111, self.__addr_mux.get() & 0B11111111)
        # print(12, self.__data_out_bus.read() & 0B11111111)
        if (self.__control_bus.read_control_bus() & IR_WR) >> 9:
            self.__instruction_register.insert(self.__data_out_bus.read())
            # print(13, self.__instruction_register.get() & 0B11111111)
        self.__internal_bus.clear()
        self.__internal_bus.write(self.__instruction_register.get())
        # print(13.5, self.__instruction_register.get() & 0B11111111)
        self.__addr_mux.set_input_1(self.__internal_bus.read() & 0B11111111)
        self.__alu_mux.set_input_0(self.__internal_bus.read() & 0B11111111)
        self.__alu_mux.set_input_1(self.__data_out_bus.read() & 0B11111111)
        # print(18, self.__data_out_bus.read() & 0B11111111, self.__internal_bus.read() & 0B11111111, self.__alu_mux.get() & 0B11111111)
        # All outputs have been processed and now we will read from things
        # The IR is set by default when there is data on the data out bus
        self.process_alu_control()
        # print(19)
        if (self.__control_bus.read_control_bus() & PC_LD) >> 10:
            # print(21)
            if (self.__control_bus.read_control_bus() & ZERO_FLAG) >> 14:
                # print(22)
                if self.__zero_flag:
                    # print(23, self.__internal_bus.read() & 0B11111111)
                    self.__program_counter.insert(self.__internal_bus.read() & 0B11111111)
            elif (self.__control_bus.read_control_bus() & NOT_ZERO_FLAG) >> 15:
                # print(24)
                if not self.__zero_flag:
                    self.__program_counter.insert(self.__internal_bus.read() & 0B11111111)
                    # print(25, self.__internal_bus.read() & 0B11111111)
            else:
                # print(26, self.__program_counter.get(), self.__internal_bus.read() & 0B11111111)
                self.__program_counter.insert(self.__internal_bus.read() & 0B11111111)
        if (self.__control_bus.read_control_bus() & RAM_WR) >> 1:
            # print(27, self.__addr_mux.get(), self.__data_in_bus.read())
            self.__memory.insert(self.__addr_mux.get(), self.__data_in_bus.read())
        return False

    def gui(self):
        window = tk.Tk()
        window.title('SimpleCPU')
        label = tk.Label(text="This is a pain!")
        label.pack()
        #
        # window.mainloop()
        print('gui')

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
        print(len(parsed))
        while i < len(parsed):
            self.__memory.insert(i, parsed[i])
            hex_string = format(parsed[i], '0{}x'.format(4))
            print(i, "0x"+hex_string)
            # self.__control_bus.clear()
            # self.__control_bus.add_control(memory)
            # self.process_control_bus()
            i += 1
        run = True
        max_runs = 1000
        i = 0
        while i < max_runs and run:
            mem_val = self.__memory.get(self.__program_counter.get())
            print(self.__program_counter.get(), "0x"+format(mem_val, '0{}x'.format(4)))
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
                raise ValueError("Invalid instruction:", "0x"+format(mem_val, '0{}x'.format(4)))
            for instructions in instruction:
                self.__control_bus.clear()
                self.__control_bus.add_control(instructions)
                if self.process_control_bus():
                    run = False
            i += 1
        # while run and i < max_run:
        #
        #     i += 1
        print(self.__memory.get(100))
        print(self.__memory.get(101))
        print(self.__memory.get(103))
        print(self.__memory.get(104))
        print(self.__memory.get(105))
        print(self.__memory.get(106))
        print(self.__memory.get(107))
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
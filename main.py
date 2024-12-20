import argparse
import tkinter as tk

from sections.accumulator import Accumulator
from sections.control_bus import ControlBus, PC_EN, IR_EN, ACC_EN
from sections.data_bus import DataBus
from sections.instruction_register import InstructionRegister
from sections.memory import Memory
from sections.mux import Mux
from sections.program_counter import ProgramCounter


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

    def process_control_bus(self):
        self.__set_control_defaults()
        if (self.__control_bus.read_control_bus() & PC_EN) >> 11:
            self.__addr_mux.set_input_0(self.__program_counter.get())
        if (self.__control_bus.read_control_bus() & IR_EN) >> 9:
            self.__internal_bus.write(self.__instruction_register.get())
            self.__alu_mux.set_input_0(self.__internal_bus.read())
            self.__addr_mux.set_input_1(self.__internal_bus.read())
        if (self.__control_bus.read_control_bus() & ACC_EN) >> 8:
            self.__address_bus.write(self.__accumulator.get())

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

    def run(self):
        if self.__args.gui_simulator:
            self.gui()
        elif self.__args.cli_simulator:
            self.cli()
        else:
            raise Exception('No simulator selected')


if __name__ == '__main__':
    Run().run()
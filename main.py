import argparse

from sections.control_bus import ControlBus
from sections.data_bus import DataBus
from sections.instruction_register import InstructionRegister
from sections.memory import Memory
from sections.mux import Mux
from sections.program_counter import ProgramCounter


class Run:
    __parser = argparse.ArgumentParser(prog='Simple CPU instruction set simulator',
                                     description='Simple CPU instruction set simulator is a teaching tool showing how a CPU operates and assembly is executed')

    __memory: Memory
    __control_bus: ControlBus
    __instruction_register: InstructionRegister
    __program_counter: ProgramCounter
    __internal_bus: DataBus
    __data_in_bus: DataBus
    __data_out_bus: DataBus
    __address_bus: DataBus
    __alu_mux: Mux
    __addr_mux: Mux

    def __init__(self):
        simulator_presenting_group = self.__parser.add_mutually_exclusive_group()
        simulator_presenting_group.add_argument("-cli", "--cli-simulator", help="Selecting command line simulator",
                                              action='store_true')
        simulator_presenting_group.add_argument("-gui", "--gui-simulator", help="Selecting graphical simulator",
                                              action='store_true')

        args = self.__parser.parse_args()

        self.__control_bus = ControlBus()
        self.__instruction_register = InstructionRegister()
        self.__program_counter = ProgramCounter()
        self.__internal_bus = DataBus(16)
        self.__data_in_bus = DataBus(16)
        self.__data_out_bus = DataBus(16)
        self.__address_bus = DataBus(8)
        self.__alu_mux = Mux()
        self.__addr_mux = Mux()


if __name__ == '__main__':
    Run()
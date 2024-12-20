import math
from os import error

class InstructionRegister:
    __content: int = 0

    def insert(self, value: int):
        if value < 0 or value >= math.pow(2, 16):
            raise error(f'Instruction Register value {value} out of range')
        self.__content = value

    def get(self):
        return self.__content
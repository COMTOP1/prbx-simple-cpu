import math
from os import error

class ProgramCounter:
    __content: int = 0

    def insert(self, value: int):
        if value < 0 or value >= math.pow(2, 8):
            raise error(f'Program Counter value {value} out of range')
        self.__content = value

    def enable(self):
        self.__content += 1

    def get(self):
        return self.__content
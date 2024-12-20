import math

class ProgramCounter:
    __content: int = 0

    def insert(self, value: int):
        if value < 0 or value >= math.pow(2, 8):
            raise ValueError(f'Program Counter value {value} out of range')
        self.__content = value

    def enable(self):
        self.__content += 1
        if self.__content == math.pow(2, 8):
            self.__content = 0

    def get(self):
        return self.__content
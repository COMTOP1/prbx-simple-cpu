import math
from os import error

class Accumulator:
    __content: int = 0

    def insert(self, value: int):
        if value < 0 or value >= math.pow(2, 8):
            raise error(f'Accumulator value {value} out of range')
        self.__content = value

    def get(self):
        return self.__content
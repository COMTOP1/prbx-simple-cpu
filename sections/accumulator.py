import math

class Accumulator:
    __content: int = 0

    def insert(self, value: int):
        if value < 0 or value >= math.pow(2, 8):
            raise ValueError(f'Accumulator value {value} out of range')
        self.__content = value

    def get(self):
        return self.__content
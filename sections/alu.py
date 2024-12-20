import math
from os import error

class ALU:
    __content: int = 0
    __size: int = 0

    def __init__(self, size: int):
        if size != 8 or size != 16:
            raise error(f'ALU {size} is not a valid size')
        self.__size = size

    def insert(self, value: int):
        if value < 0 or value >= math.pow(2, self.__size):
            raise error(f'ALU value {value} out of range')
        self.__content = value

    def get(self):
        return self.__content
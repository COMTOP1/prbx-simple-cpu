import math

class DataBus:
    __width: int = 0
    __data: int = 0

    def __init__(self, width):
        if width < 8 or width > 16:
            raise ValueError(f'DataBus {width} is not a valid width')
        self.__width = width

    def write(self, value):
        if value < 0 or value >= math.pow(2, self.__width):
            raise ValueError(f'DataBus value {value} out of range')
        self.__data = self.__data | value   # Simulating multiple sources writing at the same time

    def read(self):
        return self.__data

    def clear(self):
        self.__data = 0
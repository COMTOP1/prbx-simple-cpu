import math


class Mux:
    __control_input: int = 0

    __input_0: int = 0
    __input_1: int = 0

    __size: int = 0

    def __init__(self, size: int):
        if size < 8 or size > 16:
            raise ValueError('mux size must be between 8 and 16')
        self.__size = size

    def set_control(self, control_input: int):
        if control_input < 0 or control_input > 1:
            raise ValueError('control_input must be between 0 and 1')
        self.__control_input = control_input

    def set_input_0(self, input_0: int):
        if input_0 < 0 or input_0 > math.pow(2, self.__size):
            raise ValueError(f'mux input_0 must be between 0 and 2^{self.__size} inclusive')
        self.__input_0 = input_0

    def set_input_1(self, input_1: int):
        if input_1 < 0 or input_1 > math.pow(2, self.__size):
            raise ValueError(f'mux input_1 must be between 0 and 2^{self.__size} inclusive')
        self.__input_1 = input_1

    def get(self):
        if self.__control_input == 0:
            return self.__input_0
        else:
            return self.__input_1
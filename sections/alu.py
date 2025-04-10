import math

class ALU:
    __input_a: int = 0
    __input_b: int = 0

    __size: int = 0

    __control_0: bool = 0
    __control_1: bool = 0
    __control_2: bool = 0

    __output_mask: int = 0

    def __init__(self, size: int):
        if size != 8 and size != 16:
            raise ValueError(f'ALU {size} is not a valid size')
        self.__size = size
        if size == 8:
            self.__output_mask = 0b11111111
        elif size == 16:
            self.__output_mask = 0b1111111111111111

    def set_input_a(self, input_a: int):
        if input_a < 0 or input_a >= math.pow(2, self.__size):
            raise ValueError(f'ALU input a {input_a} out of range')
        self.__input_a = input_a

    def set_input_b(self, input_b: int):
        if input_b < 0 or input_b >= math.pow(2, self.__size):
            raise ValueError(f'ALU input b {input_b} out of range')
        self.__input_b = input_b

    def set_control(self, control: int):
        if control < 0 or control > 7:
            raise ValueError(f'ALU control {control} out of range')
        self.__control_0 = control & 0b001 > 0
        self.__control_1 = control & 0b010 > 1
        self.__control_2 = control & 0b100 > 2

    def get(self):
        if not self.__control_0 and not self.__control_1 and not self.__control_2:
            return (self.__input_a + self.__input_b) & self.__output_mask
        if self.__control_0 and not self.__control_1 and not self.__control_2:
            temp: int = self.__input_a - self.__input_b
            while temp < 0:
                temp = int(math.pow(2, self.__size)) - temp
            return temp & self.__output_mask
        if not self.__control_0 and self.__control_1 and not self.__control_2:
            return (self.__input_a & self.__input_b) & self.__output_mask
        if not self.__control_0 and not self.__control_1 and self.__control_2:
            return self.__input_b & self.__output_mask
        return 0

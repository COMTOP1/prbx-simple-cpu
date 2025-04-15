import math

class Memory:
    __memory: list[int] = [0]
    __length: int

    def __init__(self, length: int):
        if length <= 0 or length > math.pow(2, 16):
            raise ValueError(f'Memory length {length} is invalid')
        self.__length = length
        self.__memory = [0] * self.__length

    def insert(self, index: int, value: int):
        if index < 0 or index >= len(self.__memory):
            raise IndexError(f'Memory index {index} out of range of length {len(self.__memory)}')
        if value < 0 or value >= math.pow(2, 16):
            raise ValueError(f'Memory value {value} out of range')
        self.__memory[index] = value

    def get(self, index: int):
        if index < 0 or index >= len(self.__memory):
            raise IndexError(f'Memory index {index} out of range')
        return self.__memory[index]

    def clear(self):
        self.__memory = [0] * self.__length

    def length(self) -> int:
        return len(self.__memory)

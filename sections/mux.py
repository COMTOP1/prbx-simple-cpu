class Mux:
    __control_input: int = 0

    __input_0: int = 0
    __input_1: int = 0

    def set_control(self, control_input: int):
        self.__control_input = control_input

    def set_input_0(self, input_0: int):
        self.__input_0 = input_0

    def set_input_1(self, input_1: int):
        self.__input_1 = input_1

    def get(self):
        if self.__control_input == 0:
            return self.__input_0
        else:
            return self.__input_1
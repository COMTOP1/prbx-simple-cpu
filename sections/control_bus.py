type ControlLine = int

PC_EN: ControlLine =    0B100000000000
"""
PC_EN - Program Counter enable

The Program Counter outputs to the Address Bus
"""
PC_LD: ControlLine =    0B010000000000
"""
PC_LD - Program Counter load

The Program Counter outputs to the Address Bus mux
"""
IR_EN: ControlLine =    0B001000000000
"""
IR_EN - Instruction Register enable

The Program Counter outputs to the Internal Bus
"""
ACC_EN: ControlLine =   0B000100000000
"""
ACC_EN - Accumulator enable

The Accumulator outputs to the Data In Bus
"""
ACC_CTL2: ControlLine = 0B000010000000
"""
ACC_CTL2 - ALU control line 2

The control line 2 is part of ALU control
"""
ACC_CTL1: ControlLine = 0B000001000000
"""
ACC_CTL1 - ALU control line 1

The control line 1 is part of ALU control
"""
ACC_CTL0: ControlLine = 0B000000100000
"""
ACC_CTL0 - ALU control line 0

The control line 0 is part of ALU control
"""
ADDR_SEL: ControlLine = 0B000000010000
"""
ADDR_SEL - Address mux selector

Signal 0 passes the Program Counter to the Address Bus

Signal 1 passes the Internal Bus to the Address Bus
"""
DATA_SEL: ControlLine = 0B000000001000
"""
DATA_SEL - Data mux selector

Signal 0 passes the Internal Bus to the ALU

Signal 1 passes the Data Out Bus to the ALU
"""
RAM_EN: ControlLine =   0B000000000100
"""
RAM_EN - RAM enable

The RAM outputs to the Data Out Bus (not used)
"""
RAM_WR: ControlLine =   0B000000000010
"""
RAM_WR - RAM write enable

The RAM accepts data in from the Data In Bus
"""
ROM_EN: ControlLine =   0B000000000001
"""
ROM_EN - ROM enable

The RAM outputs to the Data Out Bus (not used)
"""

class ControlBus:
    """
    Control bus is the emulation of the SimpleCPU control bus
    """
    __bus: ControlLine

    def __init__(self):
        self.__bus = 0

    def add_control(self, bus: ControlLine):
        self.__bus = self.__bus | bus

    def read_control_bus(self) -> ControlLine:
        return self.__bus

    def clear(self):
        self.__bus = 0
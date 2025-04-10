type ControlLine = int

HALT_FLAG: ControlLine =        0B10000000000000000
"""
HALT_FLAG - stops the program (0X10000)
"""
NOT_ZERO_FLAG: ControlLine =    0B01000000000000000
"""
NOT_ZERO_FLAG - Internal not zero flag (0X8000)
"""
ZERO_FLAG: ControlLine =        0B00100000000000000
"""
ZERO_FLAG - Internal zero flag (0X4000)
"""

PC_EN: ControlLine =            0B00010000000000000
"""
PC_EN - Program Counter enable (0X2000)

The Program Counter outputs to the Address Bus
"""
PC_INC: ControlLine =           0B00001000000000000
"""
PC_INC - Program Counter increment (0X1000)

The Program Counter will increment it's value
"""
PC_LD: ControlLine =            0B00000100000000000
"""
PC_LD - Program Counter load (0X800)

The Program Counter outputs to the Address Bus mux
"""
IR_WR: ControlLine =            0B00000010000000000
"""
IR_WR - Instruction Register write enable (0X400)

The Instruction Register can be written to
"""
ACC_EN: ControlLine =           0B00000001000000000
"""
ACC_EN - Accumulator enable (0X200)

The Accumulator outputs to the Data In Bus
"""
ACC_WR: ControlLine =           0B00000000100000000
"""
ACC_WR - Accumulator write enable (0X100)

The Accumulator can be written to
"""
ACC_CTL2: ControlLine =         0B00000000010000000
"""
ACC_CTL2 - ALU control line 2 (0X80)

The control line 2 is part of ALU control
"""
ACC_CTL1: ControlLine =         0B00000000001000000
"""
ACC_CTL1 - ALU control line 1 (0X40)

The control line 1 is part of ALU control
"""
ACC_CTL0: ControlLine =         0B00000000000100000
"""
ACC_CTL0 - ALU control line 0 (0X20)

The control line 0 is part of ALU control
"""
ADDR_SEL: ControlLine =         0B00000000000010000
"""
ADDR_SEL - Address mux selector (0X10)

Signal 0 passes the Program Counter to the Address Bus (unset)

Signal 1 passes the Internal Bus to the Address Bus
"""
DATA_SEL: ControlLine =         0B00000000000001000
"""
DATA_SEL - Data mux selector (0X8)

Signal 0 passes the Internal Bus to the ALU (unset)

Signal 1 passes the Data Out Bus to the ALU
"""
RAM_EN: ControlLine =           0B00000000000000100
"""
RAM_EN - RAM enable (0X4)

The RAM outputs to the Data Out Bus
"""
RAM_WR: ControlLine =           0B00000000000000010
"""
RAM_WR - RAM write enable (0X2)

The RAM accepts data in from the Data In Bus
"""
ROM_EN: ControlLine =           0B00000000000000001
"""
ROM_EN - ROM enable (0X1)

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

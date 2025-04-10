from sections.control_bus import IR_WR, ACC_CTL0, ACC_CTL1, ACC_CTL2, PC_EN, ACC_EN, DATA_SEL, \
    ADDR_SEL, RAM_EN, RAM_WR, PC_LD, ZERO_FLAG, NOT_ZERO_FLAG, ControlLine, PC_INC, HALT_FLAG, \
    ACC_WR

type Instruction = list[ControlLine]

MOVE: Instruction =     [RAM_EN | PC_EN | IR_WR,
                         ACC_CTL2 | ACC_WR,
                         PC_INC]
ADD: Instruction =      [RAM_EN | PC_EN | IR_WR,
                         ACC_WR | ACC_EN,
                         PC_INC]
SUB: Instruction =      [RAM_EN | PC_EN | IR_WR,
                         ACC_CTL0 | ACC_WR | ACC_EN,
                         PC_INC]
AND: Instruction =      [RAM_EN | PC_EN | IR_WR,
                         ACC_CTL1 | ACC_WR | ACC_EN,
                         PC_INC]
LOAD: Instruction =     [RAM_EN | PC_EN | IR_WR,
                         ADDR_SEL | RAM_EN | DATA_SEL | ACC_CTL2 | ACC_WR,
                         PC_INC]
STORE: Instruction =    [RAM_EN | PC_EN | IR_WR,
                         ADDR_SEL | RAM_WR | ACC_EN,
                         PC_INC]
ADDM: Instruction =     [RAM_EN | PC_EN | IR_WR,
                         ADDR_SEL | RAM_EN | ACC_WR | DATA_SEL | ACC_EN,
                         PC_INC]
SUBM: Instruction =     [RAM_EN | PC_EN | IR_WR,
                         ADDR_SEL | RAM_EN | ACC_WR | DATA_SEL | ACC_EN | ACC_CTL0,
                         PC_INC]
JUMPU: Instruction =    [RAM_EN | PC_EN | IR_WR,
                         PC_LD]
JUMPZ: Instruction =    [RAM_EN | PC_EN | IR_WR,
                         PC_INC,  # Added if it is not zero then it will proceed
                         ZERO_FLAG | PC_LD]
JUMPNZ: Instruction =   [RAM_EN | PC_EN | IR_WR,
                         PC_INC,  # Added if it is zero then it will proceed
                         NOT_ZERO_FLAG | PC_LD]
HALT: Instruction =     [RAM_EN | PC_EN | IR_WR,
                         HALT_FLAG]

INSTRUCTIONS: list[Instruction] = [
    MOVE,
    ADD,
    SUB,
    AND,
    LOAD,
    STORE,
    ADDM,
    SUBM,
    JUMPU,
    JUMPZ,
    JUMPNZ,
    HALT,
]

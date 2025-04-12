"""
Instructions module contains the instructions that can be executed and all the
micro-instructions required
"""
from sections.control_bus import IR_WR, ACC_CTL0, ACC_CTL1, ACC_CTL2, PC_EN, ACC_EN, DATA_SEL, \
    ADDR_SEL, RAM_EN, RAM_WR, PC_LD, ZERO_FLAG, NOT_ZERO_FLAG, ControlLine, PC_INC, HALT_FLAG, \
    ACC_WR

type Instruction = list[tuple[ControlLine, str]]

MOVE: Instruction =     [(RAM_EN | PC_EN | IR_WR, "Fetch and decode MOVE"),
                         (ACC_CTL2 | ACC_WR, "Move the value from IR to ACC"),
                         (PC_INC, "Increment counter")]
ADD: Instruction =      [(RAM_EN | PC_EN | IR_WR, "Fetch and decode ADD"),
                         (ACC_WR | ACC_EN, "Add contents of IR to ACC"),
                         (PC_INC, "Increment counter")]
SUB: Instruction =      [(RAM_EN | PC_EN | IR_WR, "Fetch and decode SUB"),
                         (ACC_CTL0 | ACC_WR | ACC_EN, "Subtracts contents of ACC from IR"),
                         (PC_INC, "Increment counter")]
AND: Instruction =      [(RAM_EN | PC_EN | IR_WR, "Fetch and decode AND"),
                         (ACC_CTL1 | ACC_WR | ACC_EN, "Ands the contents of ACC and IR"),
                         (PC_INC, "Increment counter")]
LOAD: Instruction =     [(RAM_EN | PC_EN | IR_WR, "Fetch and decode LOAD"),
                         (ADDR_SEL | RAM_EN | DATA_SEL | ACC_CTL2 | ACC_WR, "Loads the contents of the memory location to ACC"),
                         (PC_INC, "Increment counter")]
STORE: Instruction =    [(RAM_EN | PC_EN | IR_WR, "Fetch and decode STORE"),
                         (ADDR_SEL | RAM_WR | ACC_EN, "Moves the contents of the ACC to the memory location"),
                         (PC_INC, "Increment counter")]
ADDM: Instruction =     [(RAM_EN | PC_EN | IR_WR, "Fetch and decode ADDM"),
                         (ADDR_SEL | RAM_EN | ACC_WR | DATA_SEL | ACC_EN, "Add contents of ACC to the value of memory location"),
                         (PC_INC, "Increment counter")]
SUBM: Instruction =     [(RAM_EN | PC_EN | IR_WR, "Fetch and decode SUBM"),
                         (ADDR_SEL | RAM_EN | ACC_WR | DATA_SEL | ACC_EN | ACC_CTL0, "Subtracts contents of ACC from value of the memory location"),
                         (PC_INC, "Increment counter")]
JUMPU: Instruction =    [(RAM_EN | PC_EN | IR_WR, "Fetch and decode JUMPU"),
                         (PC_LD, "Moves the contents of the IR into the PC")]
JUMPZ: Instruction =    [(RAM_EN | PC_EN | IR_WR, "Fetch and decode JUMPZ"),
                         (PC_INC, "Increment counter incase ACC is not zero"),
                         (ZERO_FLAG | PC_LD, "Changes the contents of the PC if the ACC is zero")]
JUMPNZ: Instruction =   [(RAM_EN | PC_EN | IR_WR, "Fetch and decode JUMPNZ"),
                         (PC_INC, "Increment counter incase ACC is zero"),
                         (NOT_ZERO_FLAG | PC_LD, "Changes the contents of the PC if the ACC is not zero")]
HALT: Instruction =     [(RAM_EN | PC_EN | IR_WR, "Fetch and decode HALT"),
                         (HALT_FLAG, "Stops the execution of the program")]

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

from sections.control_bus import IR_EN, ACC_CTL0, ACC_CTL1, ACC_CTL2, ROM_EN, PC_EN, ACC_EN, DATA_SEL, ADDR_SEL, RAM_EN, \
    RAM_WR, PC_LD

type Instruction = list[int]

MOVE: Instruction = [IR_EN | ACC_CTL2 | ROM_EN,
                     PC_EN | ACC_CTL2,
                     ACC_EN | ACC_CTL2]
ADD: Instruction  = [IR_EN | ROM_EN,
                     PC_EN,
                     ACC_EN]
SUB: Instruction  = [IR_EN | ACC_CTL0 | ROM_EN,
                     PC_EN | ACC_CTL0,
                     ACC_EN | ACC_CTL0]
AND: Instruction = [IR_EN | ACC_CTL1 | ROM_EN,
                    PC_EN | ACC_CTL1,
                    ACC_EN | ACC_CTL1]
LOAD: Instruction = [IR_EN | ACC_CTL2 | DATA_SEL | ROM_EN,
                     PC_EN | ACC_CTL2 | ADDR_SEL | DATA_SEL | RAM_EN,
                     ACC_EN | ACC_CTL2 | ADDR_SEL | DATA_SEL | RAM_EN]
STORE: Instruction = [IR_EN | ROM_EN,
                      PC_EN | ADDR_SEL | RAM_WR | RAM_EN,
                      ADDR_SEL | RAM_EN]
ADDM: Instruction = [IR_EN | DATA_SEL | ROM_EN,
                     PC_EN | ADDR_SEL | DATA_SEL | RAM_EN,
                     ACC_EN | ADDR_SEL | DATA_SEL | RAM_EN]
SUBM: Instruction = [IR_EN | ACC_CTL0 | DATA_SEL | ROM_EN,
                     PC_EN | ACC_CTL0 | ADDR_SEL | DATA_SEL | RAM_EN,
                     ACC_EN | ACC_CTL0 | ADDR_SEL | DATA_SEL | RAM_EN]
JUMPU: Instruction = [IR_EN | ROM_EN,
                      IR_EN | PC_LD]